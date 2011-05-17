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

import sys, os
from PyQt4 import QtCore
#try:
#    import vlc
#except:
#    pass
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.phonon import Phonon

from openlp.core.lib import Receiver
from openlp.plugins.media.lib import MediaBackends, MediaState
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
    """

    def __init__(self, parent):
        self.parent = parent
        self.backend = {}
        self.curDisplayMediaController = {}
        #one controller for every backend
        if WebkitController.is_available():
            self.backend['webkit'] = WebkitController(self)
        if PhononController.is_available():
            self.backend['phonon'] = PhononController(self)
        if VlcController.is_available():
            self.backend['vlc'] = VlcController(self)
        #Timer for video state
        self.Timer = QtCore.QTimer()
        self.Timer.setInterval(200)
        #signals
        QtCore.QObject.connect(self.Timer,
            QtCore.SIGNAL("timeout()"), self.video_state)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'setup_display'), self.setup_display)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_video'), self.video)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_play'), self.video_play)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_pause'), self.video_pause)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_stop'), self.video_stop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_seek'), self.video_seek)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_volume'), self.video_volume)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_reset'), self.video_reset)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_hide'), self.video_hide)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_blank'), self.video_blank)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_unblank'), self.video_unblank)

    def video_state(self):
        """
        Check if there is an assigned media backend and do some
        updating stuff (e.g. update the UI)
        """
        isAnyonePlaying = False
        if len(self.curDisplayMediaController.keys()) == 0:
            self.Timer.stop()
        else:
            for display in self.curDisplayMediaController.keys():
                if display == self.parent.previewController.previewDisplay or \
                    display == self.parent.previewController.display:
                    self.curDisplayMediaController[display].update_ui(self.parent.previewController, display)
                else:
                    self.curDisplayMediaController[display].update_ui(self.parent.liveController, display)
                if self.curDisplayMediaController[display].state == MediaState.Playing:
                    isAnyonePlaying = True
        if not isAnyonePlaying:
            self.Timer.stop()

    def setup_display(self, display):
        # check controller relevant displays
        if display == self.parent.previewController.previewDisplay or \
            display == self.parent.liveController.display:
            for backend_typ in self.backend.values():
                backend_typ.setup(display)

    def resize(self, controller):
        """
        after Mainwindow changes or Splitter moved all related media
        widgets have to be resized
        """
        pass
        #has to be clarified
        #for display in self.curDisplayMediaController.keys():
        #    self.curDisplayMediaController[display].resize(display, controller)

    def video(self, msg):
        """
        Loads and starts a video to run with the option of sound
        """
        controller = msg[0]
        videoPath = os.path.abspath(msg[1])
        volume = msg[2]
        isBackground = msg[3]
        log.debug(u'video')
        vol = float(volume) / float(10)
        #stop running videos
        self.video_reset(controller)
        if controller.isLive:
            # We are running a background theme
            controller.display.override[u'theme'] = u''
            controller.display.override[u'video'] = True
#            display = controller.previewDisplay
#            self.check_file_type(display, videoPath, False)
#            self.curDisplayMediaController[display].load(display, videoPath, volume)
            display = controller.display
            self.check_file_type(display, videoPath, False)
            self.curDisplayMediaController[display].load(display, videoPath, volume)
            controller.display.webLoaded = True
        else:
            display = controller.previewDisplay
            self.check_file_type(display, videoPath, False)
            self.curDisplayMediaController[display].load(display, videoPath, volume)
        #check size of all media_widgets
        self.resize(controller)
        #now start playing
        for display in self.curDisplayMediaController.keys():
            if display.parent == controller:
                self.curDisplayMediaController[display].play(display)

    def check_file_type(self, display, videoPath, isBackground):
        """
        Used to choose the right media backend type
        from the prioritized backend list
        """
        if videoPath.endswith(u'.swf') or isBackground:
            self.curDisplayMediaController[display] = self.backend['webkit']
        elif videoPath.endswith(u'.wmv'):
            self.curDisplayMediaController[display] = self.backend['phonon']
        else:
            self.curDisplayMediaController[display] = self.backend['vlc']
        for key in self.backend.keys():
            if self.backend[key] == self.curDisplayMediaController[display]:
                self.backend[key].set_visible(display, True)
#            else:
#                self.backend[key].set_visible(display, False)
        if len(self.curDisplayMediaController) > 0:
            if not self.Timer.isActive():
                self.Timer.start()

    def video_play(self, controller):
        """
        Responds to the request to play a loaded video
        """
        log.debug(u'video_play')
        for display in self.curDisplayMediaController.keys():
            if display.parent == controller:
                self.curDisplayMediaController[display].play(display)
        # show screen
        if not self.Timer.isActive():
            self.Timer.start()
        #display.setVisible(True)

    def video_pause(self, controller):
        """
        Responds to the request to pause a loaded video
        """
        log.debug(u'videoPause')
        for display in self.curDisplayMediaController.keys():
            if display.parent == controller:
                self.curDisplayMediaController[display].pause(display)

    def video_stop(self, controller):
        """
        Responds to the request to stop a loaded video
        """
        log.debug(u'video_stop')
        for display in self.curDisplayMediaController.keys():
            if display.parent == controller:
                self.curDisplayMediaController[display].stop(display)
                self.curDisplayMediaController[display].set_visible(display, False)

    def video_volume(self, msg):
        """
        Changes the volume of a running video
        """
        controller = msg[0]
        volume = msg[1]
        log.debug(u'video_volume %d' % volume)
        vol = float(volume) / float(10)
        for display in self.curDisplayMediaController.keys():
            if display.parent == controller:
                self.curDisplayMediaController[display].volume(display, vol)

    def video_finished(self):
        """
        Blank the Video when it has finished so the final frame is not left
        hanging
        """
        display.videoStop()
        display.hideDisplay(HideMode.Blank)
        display.videoHide = True

    def video_tick(self, tick):
        """
        Triggered on video tick every 200 milli seconds
        """
        if tick > display.serviceItem.end_time * 1000:
            display.videoFinished()

    def video_seek(self, msg):
        """
        Responds to the request to change the seek Slider of a loaded video
        """
        log.debug(u'video_seek')
        controller = msg[0]
        seekVal = msg[1]
        for display in self.curDisplayMediaController.keys():
            if display.parent == controller:
                self.curDisplayMediaController[display].seek(display, seekVal)


    def video_reset(self, controller):
        """
        Responds to the request to reset a loaded video
        """
        log.debug(u'video_reset')
        for display in self.curDisplayMediaController.keys():
            if display.parent == controller:
                self.curDisplayMediaController[display].reset(display)
                del self.curDisplayMediaController[display]
#        if controller.isLive:
            #Receiver.send_message(u'maindisplay_active')

    def video_hide(self, msg):
        """
        Hide the related video Widget
        """
        print "hide"
        isLive = msg[1]
        if isLive:
            controller = self.parent.liveController
            for display in self.curDisplayMediaController.keys():
                if display.parent == controller:
                    if self.curDisplayMediaController[display].state == MediaState.Playing:
                        self.curDisplayMediaController[display].pause(display)
                        self.curDisplayMediaController[display].set_visible(display, False)

    def video_blank(self, msg):
        """
        Blank the related video Widget
        """
        print "blank"
        isLive = msg[1]
        if isLive:
            controller = self.parent.liveController
            for display in self.curDisplayMediaController.keys():
                if display.parent == controller:
                    if self.curDisplayMediaController[display].state == MediaState.Playing:
                        self.curDisplayMediaController[display].pause(display)
                        self.curDisplayMediaController[display].set_visible(display, False)

    def video_unblank(self, msg):
        """
        Unblank the related video Widget
        """
        print "unblank"
        Receiver.send_message(u'maindisplay_show')
        isLive = msg[1]
        if isLive:
            controller = self.parent.liveController
            for display in self.curDisplayMediaController.keys():
                if display.parent == controller:
                    if self.curDisplayMediaController[display].state == MediaState.Paused:
                        self.curDisplayMediaController[display].play(display)
                        self.curDisplayMediaController[display].set_visible(display, True)
