#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import logging

import sys, types
from PyQt4 import QtCore
import vlc

from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

from openlp.core.lib import Receiver
from openlp.plugins.media.lib import MediaBackends, MediaStates
from webkitcontroller import WebkitController
from phononcontroller import PhononController
from vlccontroller import VlcController

log = logging.getLogger(__name__)

class MediaManager(object):
    """
        The implementation of a Media Manager
        The idea is to separate the media related implementation into the plugin files
        and unify the access from other parts of code
        The media manager adds an own class for every type of backend
        Currently these are QtWebkit, Phonon and planed Vlc.
        On the other hand currently the previewController display only use phonon for media output.
        So I would suggest to rename the maindisplay.py to display.py and modify the code,
        so that the display class can be used for the maindisplay as well as for the previewController display.

        Workflow idea:
        - OpenLP is starting
        - Live display and preview display are call setup
        - Live display and preview display send signal with a pointer to their own to the media controller ('media_set_display')
        - media controller register all available displays and create for each display all types of media backends (see setDisplay)
        - in the OpenLP configuration dialog the user no longe will decide between using Webkit OR Phonon.
        - instead of this there is a list widget with all available backends and the user can switch off/on the backends
        and change the priority order
        (this is necessary, because of not all backends can play all media files and text over video is currently only with QtWebkit possible)
        - later on, if the user add a new media service item the signal ('media_video') will be send
        - as a result of this the media manager checks which controller is needed for this filetyp
        and assign the related backend controller to the right display
        - Now all related media stuff (play, pause, ...) will be routed to the related backend controller and there processed
        - if one or more medias loaded a generic 200ms Timer will be started peridiodically to refresh the UI
        - Signal ('media_reset') will close the related video and disconnect the backend from the display

        Advantages:
        - clean and easy interface from other parts of code (slidecontroller and display classes)
        - more and better configuration possibilities inside the special backend controllers
        - same handling for preview and live display (or later on other additionally displays with their slide controllers)

        Disadvantages:
        - because of there will be display widgets created outside of the maindisplay.py file it is more complicate to read the code
        - some more signals are send arround the system

        Notices:
        - the flash support uses the flash plugin from Mozilla. So there is a js-check that this plugin is installed.
        - maybe there would be the installed flashplugin of the IE possible could also used, but I'm not sure about this?
        - I would suggest to not hide the main toolbar in case of media, instead of this the media toolbar should be
        visible as second toolbar (so the screen can be blanked also during a running video, ...)
    """
    def __init__(self, parent):
        self.parent = parent

        self.availableBackends = [
            MediaBackends.Webkit,
            MediaBackends.Phonon,
            MediaBackends.Vlc]
        self.curDisplayMediaController = {}
        self.displayWebkitController = WebkitController(self)
        self.displayPhononController = PhononController(self)
        self.displayVlcController = VlcController(self)

        self.Timer = QtCore.QTimer()
        self.Timer.setInterval(200)

        QtCore.QObject.connect(self.Timer,
            QtCore.SIGNAL("timeout()"), self.videoState)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_set_display'), self.setDisplay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_video'), self.video)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_play'), self.videoPlay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_pause'), self.videoPause)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_stop'), self.videoStop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_seek'), self.videoSeek)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_volume'), self.videoVolume)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_reset'), self.videoReset)

    def videoState(self):
        """
        check if there is an assigned media backend and do some
        updating stuff (e.g. update the UI)
        """
        isAnyonePlaying = False
        if len(self.curDisplayMediaController.keys()) == 0:
            self.Timer.stop()
        else:
            for display in self.curDisplayMediaController.keys():
                self.curDisplayMediaController[display].updateUI(display)
                if self.curDisplayMediaController[display].state == MediaStates.PlayingState:
                    isAnyonePlaying = True
        if not isAnyonePlaying:
            self.Timer.stop()

    def setDisplay(self, display):
        self.setupVlcController(display)
        self.setupPhononController(display)
        self.setupWebkitController(display)


    def setupWebkitController(self, display):
        display.webView.raise_()

    def setupPhononController(self, display):
        display.phononWidget = Phonon.VideoWidget(display)
        display.phononWidget.setVisible(False)
        display.phononWidget.setGeometry(QtCore.QRect(0, 0,
            display.screen[u'size'].width(), display.screen[u'size'].height()))
        display.mediaObject = Phonon.MediaObject(display)
        display.audio = Phonon.AudioOutput(Phonon.VideoCategory, display.mediaObject)
        Phonon.createPath(display.mediaObject, display.phononWidget)
        Phonon.createPath(display.mediaObject, display.audio)
        display.phononWidget.raise_()

    def setupVlcController(self, display):
        display.vlcWidget = QtGui.QFrame(display)
        # creating a basic vlc instance
        display.vlcInstance = vlc.Instance()
        # creating an empty vlc media player
        display.vlcMediaPlayer = display.vlcInstance.media_player_new()
        display.vlcWidget.setGeometry(QtCore.QRect(0, 0,
            display.screen[u'size'].width(), display.screen[u'size'].height()))
        display.vlcWidget.raise_()

    def video(self, msg):
        """
        Loads and starts a video to run with the option of sound
        """
        display = msg[0]
        videoPath = msg[1]
        volume = msg[2]
        isBackground = msg[3]

        log.debug(u'video')
        display.webLoaded = True
        display.setGeometry(display.screen[u'size'])
        # We are running a background theme
        display.override[u'theme'] = u''
        display.override[u'video'] = True
        vol = float(volume) / float(10)
        self.checkFileType(display, videoPath, isBackground)
        self.curDisplayMediaController[display].load(display, videoPath, volume)
        if display.isLive:
            Receiver.send_message(u'maindisplay_active')

    def checkFileType(self, display, videoPath, isBackground):
        """
            Used to choose the right media backend type
            from the prioritized backend list
        """
        usePhonon = QtCore.QSettings().value(
            u'media/use phonon', QtCore.QVariant(True)).toBool()
        useVlc = True
        if videoPath.endswith(u'.swf'):
            useVlc = False
            usePhonon = False
        elif videoPath.endswith(u'.wmv'):
            useVlc = False
            usePhonon = True
        
        if useVlc:
            self.curDisplayMediaController[display] = self.displayVlcController
            display.phononWidget.setVisible(False)
            display.webView.setVisible(False)
            display.vlcWidget.setVisible(True)
        elif usePhonon and not isBackground:
            self.curDisplayMediaController[display] = self.displayPhononController
            display.phononWidget.setVisible(True)
            display.webView.setVisible(False)
            display.vlcWidget.setVisible(False)
        else:
            self.curDisplayMediaController[display] = self.displayWebkitController
            display.phononWidget.setVisible(False)
            display.webView.setVisible(True)
            display.vlcWidget.setVisible(False)
        if len(self.curDisplayMediaController) > 0:
            if not self.Timer.isActive():
                self.Timer.start()


    def resetVideo(self):
        """
        Used after Video plugin has changed the background
        """
        log.debug(u'resetVideo')
        if display.phononActive:
            display.mediaObject.stop()
            display.mediaObject.clearQueue()
            display.webView.setVisible(True)
            display.phononWidget.setVisible(False)
            display.phononActive = False
        else:
            display.frame.evaluateJavaScript(u'show_video("close");')
            display.frame.evaluateJavaScript(u'show_flash("close");')
        display.override = {}
        # Update the preview frame.
        if display.isLive:
            Receiver.send_message(u'maindisplay_active')

    def videoPlay(self, display):
        """
        Responds to the request to play a loaded video
        """
        log.debug(u'videoPlay')
        self.curDisplayMediaController[display].play(display)
        # show screen
        if display.isLive:
            if not self.Timer.isActive():
                self.Timer.start()
            display.setVisible(True)

    def videoPause(self, display):
        """
        Responds to the request to pause a loaded video
        """
        log.debug(u'videoPause')
        if display in self.curDisplayMediaController:
            self.curDisplayMediaController[display].pause(display)
        return

    def videoStop(self, display):
        """
        Responds to the request to stop a loaded video
        """
        log.debug(u'videoStop')
        if type(display) is types.ListType:
            return
        if display in self.curDisplayMediaController:
            self.curDisplayMediaController[display].stop(display)
        if display.isLive:
            display.setVisible(False)


    def videoVolume(self, msg):
        """
        Changes the volume of a running video
        """
        display = msg[0]
        volume = msg[1]
        log.debug(u'videoVolume %d' % volume)
        vol = float(volume) / float(10)
        if display.phononActive:
            display.audio.setVolume(vol)
        else:
            display.frame.evaluateJavaScript(u'show_video(null, null, %s);' %
                str(vol))

    def videoFinished(self):
        """
        Blank the Video when it has finished so the final frame is not left
        hanging
        """
        display.videoStop()
        display.hideDisplay(HideMode.Blank)
        display.phononActive = False
        display.videoHide = True

    def videoTick(self, tick):
        """
        Triggered on video tick every 200 milli seconds
        """
        if tick > display.serviceItem.end_time * 1000:
            display.videoFinished()

    def videoSeek(self, msg):
        """
        Responds to the request to change the seek Slider of a loaded video
        """
        log.debug(u'videoSeek')
        display = msg[0]
        seekVal = msg[1]
        if display in self.curDisplayMediaController:
            self.curDisplayMediaController[display].seek(display, seekVal)

    def videoReset(self, display):
        """
        Responds to the request to reset a loaded video
        """
        log.debug(u'videoReset')
        print "videoReset"
        if display in self.curDisplayMediaController:
            self.curDisplayMediaController[display].reset(display)
            self.curDisplayMediaController[display]
