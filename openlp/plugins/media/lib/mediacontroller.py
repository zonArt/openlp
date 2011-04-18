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
from openlp.plugins.media.lib import MediaBackends
from webkitcontroller import WebkitController
from phononcontroller import PhononController

log = logging.getLogger(__name__)

class MediaManager(object):
    """
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
        #self.displayVlcController = VlcController(self)

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


    def setDisplay(self, display):
        print display
        #self.setupVlcController(display)
        self.setupPhononController(display)
        self.setupWebkitController(display)


    def setupWebkitController(self, display):
        #self.displayWebkitController[display] = display.webView
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
        QtCore.QObject.connect(display.mediaObject,
            QtCore.SIGNAL(u'stateChanged(Phonon::State, Phonon::State)'),
            display.videoHelper)
#        display.mediaObject.stateChanged.connect(self.videoState)
#        QtCore.QObject.connect(display.mediaObject,
#            QtCore.SIGNAL(u'finished()'),
#            self.videoFinished)
#        QtCore.QObject.connect(display.mediaObject,
#            QtCore.SIGNAL(u'tick(qint64)'),
#            self.videoTick)

        #self.displayPhononController[display] = display.mediaObject

    def setupVlcController(self, display):
        display.vlcWidget = QtGui.QWidget(display)
        instance=vlc.Instance()
        self.movieName = None
        player=instance.media_player_new(self.movieName)
        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform == "linux2": # for Linux using the X Server
            player.set_xwindow(self.hwnd)
        elif sys.platform == "win32": # for Windows
            player.set_hwnd(self.hwnd)
        elif sys.platform == "darwin": # for MacOS
            player.set_agl(self.hwnd)

        display.vlcWidget.setGeometry(QtCore.QRect(0, 0,
            display.screen[u'size'].width(), display.screen[u'size'].height()))
        display.vlcWidget.raise_()
        #self.displayVlcController[display] = player

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
        usePhonon = QtCore.QSettings().value(
            u'media/use phonon', QtCore.QVariant(True)).toBool()
        if usePhonon:
            self.curDisplayMediaController[display] = self.displayPhononController
            display.phononWidget.setVisible(True)
            display.webView.setVisible(False)

        else:
            self.curDisplayMediaController[display] = self.displayWebkitController
            display.phononWidget.setVisible(False)
            display.webView.setVisible(True)

        self.curDisplayMediaController[display].load(display, videoPath, volume)
        if display.isLive:
            Receiver.send_message(u'maindisplay_active')
        return
        if isBackground or not display.usePhonon:
            if videoPath.endswith(u'.swf'):
                js = u'show_flash("load","%s");' % \
                    (videoPath.replace(u'\\', u'\\\\'))
            else:
                js = u'show_video("init", "%s", %s, true); show_video("play");' % \
                    (videoPath.replace(u'\\', u'\\\\'), str(vol))
            display.frame.evaluateJavaScript(js)
        else:
            display.phononActive = True
            display.mediaObject.stop()
            display.mediaObject.clearQueue()
            display.mediaObject.setCurrentSource(Phonon.MediaSource(videoPath))
            # Need the timer to trigger set the trigger to 200ms
            # Value taken from web documentation.
            if display.serviceItem.end_time != 0:
                display.mediaObject.setTickInterval(200)
            display.mediaObject.play()
            display.webView.setVisible(False)
            display.phononWidget.setVisible(True)
            display.audio.setVolume(vol)
        # Update the preview frame.
        if display.isLive:
            Receiver.send_message(u'maindisplay_active')

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
        print type(display)
        if type(display) is types.ListType:
            return
        print display, self.curDisplayMediaController
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

    def videoState(self, newState, oldState):
        """
        Start the video at a predetermined point.
        """
        print "display", self.sender()
#        if newState == Phonon.PlayingState \
#            and oldState != Phonon.PausedState \
#            and self.serviceItem.start_time > 0:
#            # set start time in milliseconds
#            self.mediaObject.seek(self.serviceItem.start_time * 1000)

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
        if display in self.curDisplayMediaController:
            self.curDisplayMediaController[display].reset(display)
