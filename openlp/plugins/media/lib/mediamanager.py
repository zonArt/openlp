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

import sys, os,time
from PyQt4 import QtCore, QtGui, QtWebKit

from openlp.core.lib import OpenLPToolbar, Receiver, translate
from openlp.core.lib.ui import UiStrings, critical_error_message_box
from openlp.plugins.media.lib import MediaAPI, MediaState, MediaInfo
from webkitapi import WebkitAPI
from phononapi import PhononAPI
from vlcapi import VlcAPI

log = logging.getLogger(__name__)

class MediaManager(object):
    """
    The implementation of a Media Manager
    The idea is to separate the media related implementation
    into the plugin files and unify the access from other parts of code
    The media manager adds an own class for every API
    Currently these are QtWebkit, Phonon and planed Vlc.
    Manager
    - different API classes with specialised Access functions

    Controller
    - have general and API specific control Elements
    - have one or more displays (Preview, Live, ...) with different settings

    Display
    - have API-Specific Display Elements
    - have media info for current media
    """

    def __init__(self, parent):
        self.parent = parent
        self.APIs = {}
        self.controller = []
        self.curDisplayMediaAPI = {}
        #Timer for video state
        self.Timer = QtCore.QTimer()
        self.Timer.setInterval(200)
        self.withLivePreview = False
        #Signals
        QtCore.QObject.connect(self.Timer,
            QtCore.SIGNAL("timeout()"), self.video_state)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'setup_display'), self.setup_display)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_video'), self.video)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'Media Start'), self.video_play)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'Media Pause'), self.video_pause)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'Media Stop'), self.video_stop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'seekSlider'), self.video_seek)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'volumeSlider'), self.video_volume)
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
        Check if there is an assigned media API and do some
        updating stuff (e.g. update the UI)
        """
        isAnyonePlaying = False
        if len(self.curDisplayMediaAPI.keys()) == 0:
            self.Timer.stop()
        else:
            for display in self.curDisplayMediaAPI.keys():
                self.curDisplayMediaAPI[display].update_ui(display)
                if self.curDisplayMediaAPI[display] \
                    .state == MediaState.Playing:
                    isAnyonePlaying = True
        if not isAnyonePlaying:
            self.Timer.stop()

    def display_css(self):
        """
        Add css style sheets to htmlbuilder
        """
        css = u'';
        for api in self.APIs.values():
            css+= api.display_css()
        return css

    def display_javascript(self):
        """
        Add javascript functions to htmlbuilder
        """
        js = u''
        for api in self.APIs.values():
            js+= api.display_javascript()
        return js

    def display_html(self):
        """
        Add html code to htmlbuilder
        """
        html = u''
        for api in self.APIs.values():
            html+= api.display_html()
        return html

    def addControllerItems(self, controller, control_panel):
        self.controller.append(controller)
        self.setup_generic_controls(controller, control_panel)
        for api in self.APIs.values():
            api.setup_controls(controller, control_panel)

    def setup_generic_controls(self, controller, control_panel):
        controller.media_info = MediaInfo()
        # Build a Media ToolBar
        controller.mediabar = OpenLPToolbar(controller)
        controller.mediabar.addToolbarButton(
            u'Media Start', u':/slides/media_playback_start.png',
            translate('OpenLP.SlideController', 'Start playing media'),
            controller.sendToPlugins)
        controller.mediabar.addToolbarButton(
            u'Media Pause', u':/slides/media_playback_pause.png',
            translate('OpenLP.SlideController', 'Pause playing media'),
            controller.sendToPlugins)
        controller.mediabar.addToolbarButton(
            u'Media Stop', u':/slides/media_playback_stop.png',
            translate('OpenLP.SlideController', 'Stop playing media'),
            controller.sendToPlugins)
        # Build the seekSlider.
        controller.seekSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        controller.seekSlider.setMaximum(1000)
        # Build the volumeSlider.
        controller.volumeSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        controller.volumeSlider.setTickInterval(10)
        controller.volumeSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        controller.volumeSlider.setMinimum(0)
        controller.volumeSlider.setMaximum(100)
        controller.volumeSlider.setValue(controller.media_info.volume)
        controller.seekSlider.setGeometry(QtCore.QRect(90, 260, 221, 24))
        controller.seekSlider.setObjectName(u'seekSlider')
        controller.mediabar.addToolbarWidget(u'Seek Slider', controller.seekSlider)
        controller.volumeSlider.setGeometry(QtCore.QRect(90, 160, 221, 24))
        controller.volumeSlider.setObjectName(u'volumeSlider')
        controller.mediabar.addToolbarWidget(u'Audio Volume', controller.volumeSlider)
        control_panel.addWidget(controller.mediabar)
        controller.mediabar.setVisible(False)
        #Signals
        QtCore.QObject.connect(controller.seekSlider,
            QtCore.SIGNAL(u'sliderMoved(int)'), controller.sendToPlugins)
        QtCore.QObject.connect(controller.volumeSlider,
            QtCore.SIGNAL(u'sliderMoved(int)'), controller.sendToPlugins)

    def setup_display(self, display):
        """
        After a new display is configured, all media related widget
        will be created too
        """
        display.hasAudio = True
        if not self.withLivePreview and \
            display == self.parent.liveController.previewDisplay:
            return
        if display == self.parent.previewController.previewDisplay or \
            display == self.parent.liveController.previewDisplay:
            display.hasAudio = False
        for api in self.APIs.values():
            api.setup(display)

    def set_controls_visible(self, controller, value):
        # Generic controls
        controller.mediabar.setVisible(value)
        # Special controls
#        for api in self.APIs.values():
#            api.setup_controls(controller, control_panel)

    def resize(self, controller, display, api):
        """
        After Mainwindow changes or Splitter moved all related media
        widgets have to be resized
        """
        if display == self.parent.previewController.previewDisplay or \
            display == self.parent.liveController.previewDisplay:
            display.resize(controller.slidePreview.size())
        api.resize(display)

    def video(self, msg):
        """
        Loads and starts a video to run with the option of sound
        """
        log.debug(u'video')
        controller = msg[0]
        isValid = False
        # stop running videos
        self.video_reset(controller)
        controller.media_info = MediaInfo()
        controller.media_info.volume = controller.volumeSlider.value()
        controller.media_info.file_info = QtCore.QFileInfo(msg[1])
        controller.media_info.is_background = msg[2]
        if controller.isLive:
            if self.withLivePreview:
                display = controller.previewDisplay
                isValid = self.check_file_type(controller, display)
            display = controller.display
            isValid = self.check_file_type(controller, display)
        else:
            display = controller.previewDisplay
            isValid = self.check_file_type(controller, display)
        if not isValid:
            #Media could not be loaded correctly
            critical_error_message_box(
                translate('MediaPlugin.MediaItem', 'Unsupported File'),
                unicode(translate('MediaPlugin.MediaItem',
                'Unsupported File')))
            return
        #now start playing
        self.video_play([controller])
        self.video_pause([controller])
        self.video_seek([controller, 0])
        self.video_play([controller])
        self.set_controls_visible(controller, True)

    def check_file_type(self, controller, display):
        """
        Used to choose the right media API type
        from the prioritized API list
        """
        apiSettings = str(QtCore.QSettings().value(u'media/apis',
            QtCore.QVariant(u'Webkit')).toString())
        usedAPIs = apiSettings.split(u',')
        if controller.media_info.file_info.isFile():
            suffix = u'*.%s' % controller.media_info.file_info.suffix()
            for title in usedAPIs:
                api = self.APIs[title]
                if suffix in api.video_extensions_list:
                    if not controller.media_info.is_background or \
                        controller.media_info.is_background and api.canBackground:
                            self.resize(controller, display, api)
                            if api.load(display):
                                self.curDisplayMediaAPI[display] = api
                                return True
        # no valid api found
        return False

    def video_play(self, msg):
        """
        Responds to the request to play a loaded video
        """
        log.debug(u'video_play')
        controller = msg[0]
        for display in self.curDisplayMediaAPI.keys():
            if display.controller == controller:
                self.curDisplayMediaAPI[display].play(display)
        # Start Timer for ui updates
        if not self.Timer.isActive():
            self.Timer.start()

    def video_pause(self, msg):
        """
        Responds to the request to pause a loaded video
        """
        log.debug(u'videoPause')
        controller = msg[0]
        for display in self.curDisplayMediaAPI.keys():
            if display.controller == controller:
                self.curDisplayMediaAPI[display].pause(display)

    def video_stop(self, msg):
        """
        Responds to the request to stop a loaded video
        """
        log.debug(u'video_stop')
        controller = msg[0]
        for display in self.curDisplayMediaAPI.keys():
            if display.controller == controller:
                self.curDisplayMediaAPI[display].stop(display)
                self.curDisplayMediaAPI[display].set_visible(display, False)

    def video_volume(self, msg):
        """
        Changes the volume of a running video
        """
        controller = msg[0]
        vol = msg[1]
        log.debug(u'video_volume %d' % vol)
        for display in self.curDisplayMediaAPI.keys():
            if display.controller == controller:
                self.curDisplayMediaAPI[display].volume(display, vol)

    def video_seek(self, msg):
        """
        Responds to the request to change the seek Slider of a loaded video
        """
        log.debug(u'video_seek')
        controller = msg[0]
        seekVal = msg[1]
        for display in self.curDisplayMediaAPI.keys():
            if display.controller == controller:
                self.curDisplayMediaAPI[display].seek(display, seekVal)

    def video_reset(self, controller):
        """
        Responds to the request to reset a loaded video
        """
        log.debug(u'video_reset')
        for display in self.curDisplayMediaAPI.keys():
            if display.controller == controller:
                self.curDisplayMediaAPI[display].reset(display)
                del self.curDisplayMediaAPI[display]
        self.set_controls_visible(controller, False)

    def video_hide(self, msg):
        """
        Hide the related video Widget
        """
        isLive = msg[1]
        if isLive:
            controller = self.parent.liveController
            for display in self.curDisplayMediaAPI.keys():
                if display.controller == controller:
                    if self.curDisplayMediaAPI[display] \
                        .state == MediaState.Playing:
                        self.curDisplayMediaAPI[display].pause(display)
                        self.curDisplayMediaAPI[display] \
                            .set_visible(display, False)

    def video_blank(self, msg):
        """
        Blank the related video Widget
        """
        isLive = msg[1]
        if isLive:
            controller = self.parent.liveController
            for display in self.curDisplayMediaAPI.keys():
                if display.controller == controller:
                    if self.curDisplayMediaAPI[display] \
                        .state == MediaState.Playing:
                        self.curDisplayMediaAPI[display].pause(display)
                        self.curDisplayMediaAPI[display] \
                            .set_visible(display, False)

    def video_unblank(self, msg):
        """
        Unblank the related video Widget
        """
        Receiver.send_message(u'maindisplay_show')
        isLive = msg[1]
        if isLive:
            controller = self.parent.liveController
            for display in self.curDisplayMediaAPI.keys():
                if display.controller == controller:
                    if self.curDisplayMediaAPI[display] \
                        .state == MediaState.Paused:
                        self.curDisplayMediaAPI[display].play(display)
                        self.curDisplayMediaAPI[display] \
                            .set_visible(display, True)

    def get_audio_extensions_list(self):
        audio_list = []
        for api in self.APIs.values():
            for item in api.audio_extensions_list:
                if not item in audio_list:
                    audio_list.append(item)
        return audio_list

    def get_video_extensions_list(self):
        video_list = []
        for api in self.APIs.values():
            for item in api.video_extensions_list:
                if not item in video_list:
                    video_list.append(item)
        return video_list
