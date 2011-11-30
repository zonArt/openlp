# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
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
from openlp.core.lib.mediaplayer import MediaPlayer
from openlp.core.lib.ui import UiStrings, critical_error_message_box
from openlp.core.ui.media import MediaState, MediaInfo, MediaType
from openlp.core.utils import AppLocation

log = logging.getLogger(__name__)

class MediaController(object):
    """
    The implementation of the Media Controller. The Media Controller adds an own
    class for every Player. Currently these are QtWebkit, Phonon and planed Vlc.
    """

    def __init__(self, parent):
        self.parent = parent
        self.mediaPlayers = {}
        self.controller = []
        self.overridenPlayer = ''
        self.curDisplayMediaPlayer = {}
        # Timer for video state
        self.timer = QtCore.QTimer()
        self.timer.setInterval(200)
        self.withLivePreview = False
        self.check_available_media_players()
        # Signals
        QtCore.QObject.connect(self.timer,
            QtCore.SIGNAL("timeout()"), self.video_state)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_playback_play'), self.video_play)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_playback_pause'), self.video_pause)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_playback_stop'), self.video_stop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'seek_slider'), self.video_seek)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'volume_slider'), self.video_volume)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_hide'), self.video_hide)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_blank'), self.video_blank)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_unblank'), self.video_unblank)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_override_player'), self.override_player)
        # Signals for background video
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songs_hide'), self.video_hide)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songs_unblank'), self.video_unblank)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'mediaitem_media_rebuild'), self.set_active_players)

    def set_active_players(self):
        playerSettings = str(QtCore.QSettings().value(u'media/players',
            QtCore.QVariant(u'webkit')).toString())
        if len(playerSettings) == 0:
            playerSettings = u'webkit'
        savedPlayers = playerSettings.split(u',')
        for player in self.mediaPlayers.keys():
            if player in savedPlayers:
                self.mediaPlayers[player].isActive = True
            else:
                self.mediaPlayers[player].isActive = False

    def register_controllers(self, controller):
        """
        Register each media Player controller (Webkit, Phonon, etc) and store
        for later use
        """
        if controller.check_available():
            self.mediaPlayers[controller.name] = controller

    def check_available_media_players(self):
        """
        Check to see if we have any media Player's available. If Not do not
        install the plugin.
        """
        log.debug(u'check_available_media_players')
        controller_dir = os.path.join(
            AppLocation.get_directory(AppLocation.AppDir),
            u'core', u'ui', u'media')
        for filename in os.listdir(controller_dir):
            if filename.endswith(u'player.py') and \
                not filename == 'media_player.py':
                path = os.path.join(controller_dir, filename)
                if os.path.isfile(path):
                    modulename = u'openlp.core.ui.media.' + \
                        os.path.splitext(filename)[0]
                    log.debug(u'Importing controller %s', modulename)
                    try:
                        __import__(modulename, globals(), locals(), [])
                    except ImportError:
                        log.warn(u'Failed to import %s on path %s',
                            modulename, path)
        controller_classes = MediaPlayer.__subclasses__()
        for controller_class in controller_classes:
            controller = controller_class(self)
            self.register_controllers(controller)
        if self.mediaPlayers:
            playerSettings = str(QtCore.QSettings().value(u'media/players',
                QtCore.QVariant(u'webkit')).toString())
            savedPlayers = playerSettings.split(u',')
            invalidMediaPlayers = [mediaPlayer for mediaPlayer in savedPlayers \
                if not mediaPlayer in self.mediaPlayers]
            if len(invalidMediaPlayers)>0:
                [savedPlayers.remove(invalidPlayer) for invalidPlayer in invalidMediaPlayers]
                newPlayerSetting = u','.join(savedPlayers)
                QtCore.QSettings().setValue(u'media/players',
                    QtCore.QVariant(newPlayerSetting))
            self.set_active_players()
            return True
        else:
            return False

    def video_state(self):
        """
        Check if there is a running media Player and do updating stuff (e.g.
        update the UI)
        """
        if len(self.curDisplayMediaPlayer.keys()) == 0:
            self.timer.stop()
        else:
            for display in self.curDisplayMediaPlayer.keys():
                self.curDisplayMediaPlayer[display].resize(display)
                self.curDisplayMediaPlayer[display].update_ui(display)
                if self.curDisplayMediaPlayer[display] \
                    .state == MediaState.Playing:
                    return
        self.timer.stop()

    def get_media_display_css(self):
        """
        Add css style sheets to htmlbuilder
        """
        css = u''
        for player in self.mediaPlayers.values():
            if player.isActive:
                css += player.get_media_display_css()
        return css

    def get_media_display_javascript(self):
        """
        Add javascript functions to htmlbuilder
        """
        js = u''
        for player in self.mediaPlayers.values():
            if player.isActive:
                js += player.get_media_display_javascript()
        return js

    def get_media_display_html(self):
        """
        Add html code to htmlbuilder
        """
        html = u''
        for player in self.mediaPlayers.values():
            if player.isActive:
                html += player.get_media_display_html()
        return html

    def add_controller_items(self, controller, control_panel):
        self.controller.append(controller)
        self.setup_generic_controls(controller, control_panel)
        self.setup_special_controls(controller, control_panel)

    def setup_generic_controls(self, controller, control_panel):
        """
        Add generic media control items (valid for all types of medias)
        """
        controller.media_info = MediaInfo()
        # Build a Media ToolBar
        controller.mediabar = OpenLPToolbar(controller)
        controller.mediabar.addToolbarButton(
            u'media_playback_play', u':/slides/media_playback_start.png',
            translate('OpenLP.SlideController', 'Start playing media'),
            controller.sendToPlugins)
        controller.mediabar.addToolbarButton(
            u'media_playback_pause', u':/slides/media_playback_pause.png',
            translate('OpenLP.SlideController', 'Pause playing media'),
            controller.sendToPlugins)
        controller.mediabar.addToolbarButton(
            u'media_playback_stop', u':/slides/media_playback_stop.png',
            translate('OpenLP.SlideController', 'Stop playing media'),
            controller.sendToPlugins)
        # Build the seekSlider.
        controller.seekSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        controller.seekSlider.setMaximum(1000)
        controller.seekSlider.setToolTip(translate(
            'OpenLP.SlideController', 'Video position.'))
        controller.seekSlider.setGeometry(QtCore.QRect(90, 260, 221, 24))
        controller.seekSlider.setObjectName(u'seek_slider')
        controller.mediabar.addToolbarWidget(u'Seek Slider', 
            controller.seekSlider)
        # Build the volumeSlider.
        controller.volumeSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        controller.volumeSlider.setTickInterval(10)
        controller.volumeSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        controller.volumeSlider.setMinimum(0)
        controller.volumeSlider.setMaximum(100)
        controller.volumeSlider.setToolTip(translate(
            'OpenLP.SlideController', 'Audio Volume.'))
        controller.volumeSlider.setValue(controller.media_info.volume)
        controller.volumeSlider.setGeometry(QtCore.QRect(90, 160, 221, 24))
        controller.volumeSlider.setObjectName(u'volume_slider')
        controller.mediabar.addToolbarWidget(u'Audio Volume', 
            controller.volumeSlider)
        control_panel.addWidget(controller.mediabar)
        controller.mediabar.setVisible(False)
        # Signals
        QtCore.QObject.connect(controller.seekSlider,
            QtCore.SIGNAL(u'sliderMoved(int)'), controller.sendToPlugins)
        QtCore.QObject.connect(controller.volumeSlider,
            QtCore.SIGNAL(u'sliderMoved(int)'), controller.sendToPlugins)

    def setup_special_controls(self, controller, control_panel):
        """
        Special media Toolbars will be created here (e.g. for DVD Playback)
        """
        controller.media_info = MediaInfo()
        # TODO: add Toolbar for DVD, ...

    def setup_display(self, display):
        """
        After a new display is configured, all media related widget will be 
        created too
        """
        # clean up possible running old media files
        self.finalise()
        # update player status
        self.set_active_players()
        display.hasAudio = True
        if not self.withLivePreview and \
            display == self.parent.liveController.previewDisplay:
            return
        if display == self.parent.previewController.previewDisplay or \
            display == self.parent.liveController.previewDisplay:
            display.hasAudio = False
        for player in self.mediaPlayers.values():
            if player.isActive:
                player.setup(display)

    def set_controls_visible(self, controller, value):
        # Generic controls
        controller.mediabar.setVisible(value)
        # Special controls: Here media type specific Controls will be enabled 
        # (e.g. for DVD control, ...)
        # TODO

    def resize(self, controller, display, player):
        """
        After Mainwindow changes or Splitter moved all related media widgets 
        have to be resized
        """
        player.resize(display)

    def video(self, controller, file, muted, isBackground):
        """
        Loads and starts a video to run with the option of sound
        """
        log.debug(u'video')
        isValid = False
        # stop running videos
        self.video_reset(controller)
        controller.media_info = MediaInfo()
        if muted:
            controller.media_info.volume = 0
        else:
            controller.media_info.volume = controller.volumeSlider.value()
        controller.media_info.file_info = QtCore.QFileInfo(file)
        controller.media_info.is_background = isBackground
        display = None
        if controller.isLive:
            if self.withLivePreview and controller.previewDisplay:
                display = controller.previewDisplay
                isValid = self.check_file_type(controller, display)
            display = controller.display
            isValid = self.check_file_type(controller, display)
            display.override[u'theme'] = u''
            display.override[u'video'] = True
            controller.media_info.start_time = display.serviceItem.start_time
            controller.media_info.end_time = display.serviceItem.end_time
        elif controller.previewDisplay:
            display = controller.previewDisplay
            isValid = self.check_file_type(controller, display)
        if not isValid:
            # Media could not be loaded correctly
            critical_error_message_box(
                translate('MediaPlugin.MediaItem', 'Unsupported File'),
                unicode(translate('MediaPlugin.MediaItem',
                'Unsupported File')))
            return False
        # dont care about actual theme, set a black background
        if controller.isLive and ( \
            controller.media_info.is_background == False):
            display.frame.evaluateJavaScript(u'show_video( \
            "setBackBoard", null, null, null,"visible");')
        # now start playing
        if self.video_play([controller], False):
            self.video_pause([controller])
            self.video_seek([controller, [0]])
            if controller.isLive and \
                (QtCore.QSettings().value(u'general/auto unblank',
                QtCore.QVariant(False)).toBool() or \
                controller.media_info.is_background == True) or \
                controller.isLive == False:
                self.video_play([controller])
            self.set_controls_visible(controller, True)
            log.debug(u'use %s controller' % self.curDisplayMediaPlayer[display])
            return True
        else:
            critical_error_message_box(
                translate('MediaPlugin.MediaItem', 'Unsupported File'),
                unicode(translate('MediaPlugin.MediaItem',
                'Unsupported File')))
        return False

    def check_file_type(self, controller, display):
        """
        Used to choose the right media Player type from the prioritized Player list
        """
        playerSettings = str(QtCore.QSettings().value(u'media/players',
            QtCore.QVariant(u'webkit')).toString())
        usedPlayers = playerSettings.split(u',')
        if QtCore.QSettings().value(u'media/override player',
            QtCore.QVariant(QtCore.Qt.Unchecked)) == QtCore.Qt.Checked:
            if self.overridenPlayer != '':
                usedPlayers = [self.overridenPlayer]
        if controller.media_info.file_info.isFile():
            suffix = u'*.%s' % controller.media_info.file_info.suffix().toLower()
            for title in usedPlayers:
                player = self.mediaPlayers[title]
                if suffix in player.video_extensions_list:
                    if not controller.media_info.is_background or \
                        controller.media_info.is_background and player.canBackground:
                            self.resize(controller, display, player)
                            if player.load(display):
                                self.curDisplayMediaPlayer[display] = player
                                controller.media_info.media_type = MediaType.Video
                                return True
                if suffix in player.audio_extensions_list:
                    if player.load(display):
                        self.curDisplayMediaPlayer[display] = player
                        controller.media_info.media_type = MediaType.Audio
                        return True
        else:
            for title in usedPlayers:
                player = self.mediaPlayers[title]
                if player.canFolder:
                    self.resize(controller, display, player)
                    if player.load(display):
                        self.curDisplayMediaPlayer[display] = player
                        controller.media_info.media_type = MediaType.Video
                        return True
        # no valid player found
        return False

    def video_play(self, msg, status=True):
        """
        Responds to the request to play a loaded video
        
         ``msg``
            First element is the controller which should be used
        """
        log.debug(u'video_play')
        controller = msg[0]
        for display in self.curDisplayMediaPlayer.keys():
            if display.controller == controller:
                if not self.curDisplayMediaPlayer[display].play(display):
                    return False
                if status:
                    display.frame.evaluateJavaScript(u'show_blank("desktop");')
                    self.curDisplayMediaPlayer[display].set_visible(display, True)
                    if controller.isLive:
                        if controller.hideMenu.defaultAction().isChecked():
                            controller.hideMenu.defaultAction().trigger()
        # Start Timer for ui updates
        if not self.timer.isActive():
            self.timer.start()
        return True

    def video_pause(self, msg):
        """
        Responds to the request to pause a loaded video

        ``msg``
            First element is the controller which should be used
        """
        log.debug(u'video_pause')
        controller = msg[0]
        for display in self.curDisplayMediaPlayer.keys():
            if display.controller == controller:
                self.curDisplayMediaPlayer[display].pause(display)

    def video_stop(self, msg):
        """
        Responds to the request to stop a loaded video

        ``msg``
            First element is the controller which should be used
        """
        log.debug(u'video_stop')
        controller = msg[0]
        for display in self.curDisplayMediaPlayer.keys():
            if display.controller == controller:
                display.frame.evaluateJavaScript(u'show_blank("black");')
                self.curDisplayMediaPlayer[display].stop(display)
                self.curDisplayMediaPlayer[display].set_visible(display, False)

    def video_volume(self, msg):
        """
        Changes the volume of a running video

        ``msg``
            First element is the controller which should be used
        """
        controller = msg[0]
        vol = msg[1][0]
        log.debug(u'video_volume %d' % vol)
        for display in self.curDisplayMediaPlayer.keys():
            if display.controller == controller:
                self.curDisplayMediaPlayer[display].volume(display, vol)

    def video_seek(self, msg):
        """
        Responds to the request to change the seek Slider of a loaded video

        ``msg``
            First element is the controller which should be used
            Second element is a list with the seek Value as first element
        """
        log.debug(u'video_seek')
        controller = msg[0]
        seekVal = msg[1][0]
        for display in self.curDisplayMediaPlayer.keys():
            if display.controller == controller:
                self.curDisplayMediaPlayer[display].seek(display, seekVal)

    def video_reset(self, controller):
        """
        Responds to the request to reset a loaded video
        """
        log.debug(u'video_reset')
        for display in self.curDisplayMediaPlayer.keys():
            if display.controller == controller:
                display.override = {}
                self.curDisplayMediaPlayer[display].reset(display)
                self.curDisplayMediaPlayer[display].set_visible(display, False)
                display.frame.evaluateJavaScript(u'show_video( \
                "setBackBoard", null, null, null,"hidden");')
                del self.curDisplayMediaPlayer[display]
        self.set_controls_visible(controller, False)

    def video_hide(self, msg):
        """
        Hide the related video Widget

        ``msg``
            First element is the boolean for Live indication
        """
        isLive = msg[1]
        if isLive:
            controller = self.parent.liveController
            for display in self.curDisplayMediaPlayer.keys():
                if display.controller == controller:
                    if self.curDisplayMediaPlayer[display] \
                        .state == MediaState.Playing:
                        self.curDisplayMediaPlayer[display].pause(display)
                        self.curDisplayMediaPlayer[display] \
                            .set_visible(display, False)

    def video_blank(self, msg):
        """
        Blank the related video Widget

        ``msg``
            First element is the boolean for Live indication
            Second element is the hide mode
        """
        isLive = msg[1]
        hide_mode = msg[2]
        if isLive:
            Receiver.send_message(u'live_display_hide', hide_mode)
            controller = self.parent.liveController
            for display in self.curDisplayMediaPlayer.keys():
                if display.controller == controller:
                    if self.curDisplayMediaPlayer[display] \
                        .state == MediaState.Playing:
                        self.curDisplayMediaPlayer[display].pause(display)
                        self.curDisplayMediaPlayer[display] \
                            .set_visible(display, False)

    def video_unblank(self, msg):
        """
        Unblank the related video Widget

        ``msg``
            First element is not relevant in this context
            Second element is the boolean for Live indication
        """
        Receiver.send_message(u'live_display_show')
        isLive = msg[1]
        if isLive:
            controller = self.parent.liveController
            for display in self.curDisplayMediaPlayer.keys():
                if display.controller == controller:
                    if self.curDisplayMediaPlayer[display] \
                        .state == MediaState.Paused:
                        if self.curDisplayMediaPlayer[display].play(display):
                            self.curDisplayMediaPlayer[display] \
                                .set_visible(display, True)
                                    # Start Timer for ui updates
                            if not self.timer.isActive():
                                self.timer.start()


    def get_audio_extensions_list(self):
        audio_list = []
        for player in self.mediaPlayers.values():
            if player.isActive:
                for item in player.audio_extensions_list:
                    if not item in audio_list:
                        audio_list.append(item)
        return audio_list

    def get_video_extensions_list(self):
        video_list = []
        for player in self.mediaPlayers.values():
            if player.isActive:
                for item in player.video_extensions_list:
                    if not item in video_list:
                        video_list.append(item)
        return video_list

    def override_player(self, override_player):
        playerSettings = str(QtCore.QSettings().value(u'media/players',
            QtCore.QVariant(u'webkit')).toString())
        usedPlayers = playerSettings.split(u',')
        if override_player in usedPlayers:
            self.overridenPlayer = override_player
        else:
            self.overridenPlayer = ''

    def finalise(self):
        self.timer.stop()
        for controller in self.controller:
            self.video_reset(controller)
