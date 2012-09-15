# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Edwin Lunando, Joshua Miller, Stevan Pettit,  #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Simon Scudder, Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon      #
# Tibble, Dave Warnock, Frode Woldsund                                        #
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
import os
import sys
from PyQt4 import QtCore, QtGui

from openlp.core.lib import OpenLPToolbar, Receiver, translate
from openlp.core.lib.settings import Settings
from openlp.core.lib.mediaplayer import MediaPlayer
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui.media import MediaState, MediaInfo, MediaType, \
    get_media_players, set_media_players
from openlp.core.utils import AppLocation

log = logging.getLogger(__name__)

class MediaController(object):
    """
    The implementation of the Media Controller. The Media Controller adds an own
    class for every Player. Currently these are QtWebkit, Phonon and Vlc.
    """

    def __init__(self, parent):
        self.parent = parent
        self.mediaPlayers = {}
        self.controller = []
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
            QtCore.SIGNAL(u'playbackPlay'), self.video_play)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'playbackPause'), self.video_pause)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'playbackStop'), self.video_stop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'seekSlider'), self.video_seek)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'volumeSlider'), self.video_volume)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_hide'), self.video_hide)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_blank'), self.video_blank)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_unblank'), self.video_unblank)
        # Signals for background video
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songs_hide'), self.video_hide)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songs_unblank'), self.video_unblank)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'mediaitem_media_rebuild'), self.set_active_players)

    def set_active_players(self):
        savedPlayers = get_media_players()[0]
        for player in self.mediaPlayers.keys():
            self.mediaPlayers[player].isActive = player in savedPlayers

    def register_controllers(self, controller):
        """
        Register each media Player controller (Webkit, Phonon, etc) and store
        for later use
        """
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
            # TODO vlc backend is not yet working on Mac OS X.
            # For now just ignore vlc backend on Mac OS X.
            if sys.platform == 'darwin' and filename == 'vlcplayer.py':
                log.warn(u'Disabling vlc media player')
                continue
            if filename.endswith(u'player.py') and not \
                filename == 'media_player.py':  # TODO This file was renamed.
                path = os.path.join(controller_dir, filename)
                if os.path.isfile(path):
                    modulename = u'openlp.core.ui.media.' + \
                        os.path.splitext(filename)[0]
                    log.debug(u'Importing controller %s', modulename)
                    try:
                        __import__(modulename, globals(), locals(), [])
                    # On some platforms importing vlc.py might cause
                    # also OSError exceptions. (e.g. Mac OS X)
                    except (ImportError, OSError):
                        log.warn(u'Failed to import %s on path %s',
                            modulename, path)
        controller_classes = MediaPlayer.__subclasses__()
        for controller_class in controller_classes:
            controller = controller_class(self)
            self.register_controllers(controller)
        if not self.mediaPlayers:
            return False
        savedPlayers, overriddenPlayer = get_media_players()
        invalidMediaPlayers = [mediaPlayer for mediaPlayer in savedPlayers
            if not mediaPlayer in self.mediaPlayers or not
            self.mediaPlayers[mediaPlayer].check_available()]
        if invalidMediaPlayers:
            for invalidPlayer in invalidMediaPlayers:
                savedPlayers.remove(invalidPlayer)
            set_media_players(savedPlayers, overriddenPlayer)
        self.set_active_players()
        return True

    def video_state(self):
        """
        Check if there is a running media Player and do updating stuff (e.g.
        update the UI)
        """
        if not self.curDisplayMediaPlayer.keys():
            self.timer.stop()
        else:
            for display in self.curDisplayMediaPlayer.keys():
                self.curDisplayMediaPlayer[display].resize(display)
                self.curDisplayMediaPlayer[display].update_ui(display)
                if self.curDisplayMediaPlayer[display].state == \
                    MediaState.Playing:
                    return
        # no players are active anymore
        for display in self.curDisplayMediaPlayer.keys():
            if self.curDisplayMediaPlayer[display].state != MediaState.Paused:
                display.controller.seekSlider.setSliderPosition(0)
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
        controller.mediabar.addToolbarAction(u'playbackPlay',
            text=u'media_playback_play',
            icon=u':/slides/media_playback_start.png',
            tooltip=translate('OpenLP.SlideController', 'Start playing media.'),
            triggers=controller.sendToPlugins)
        controller.mediabar.addToolbarAction(u'playbackPause',
            text=u'media_playback_pause',
            icon=u':/slides/media_playback_pause.png',
            tooltip=translate('OpenLP.SlideController', 'Pause playing media.'),
            triggers=controller.sendToPlugins)
        controller.mediabar.addToolbarAction(u'playbackStop',
            text=u'media_playback_stop',
            icon=u':/slides/media_playback_stop.png',
            tooltip=translate('OpenLP.SlideController', 'Stop playing media.'),
            triggers=controller.sendToPlugins)
        # Build the seekSlider.
        controller.seekSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        controller.seekSlider.setMaximum(1000)
        controller.seekSlider.setTracking(False)
        controller.seekSlider.setToolTip(translate(
            'OpenLP.SlideController', 'Video position.'))
        controller.seekSlider.setGeometry(QtCore.QRect(90, 260, 221, 24))
        controller.seekSlider.setObjectName(u'seekSlider')
        controller.mediabar.addToolbarWidget(controller.seekSlider)
        # Build the volumeSlider.
        controller.volumeSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        controller.volumeSlider.setTickInterval(10)
        controller.volumeSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        controller.volumeSlider.setMinimum(0)
        controller.volumeSlider.setMaximum(100)
        controller.volumeSlider.setTracking(True)
        controller.volumeSlider.setToolTip(translate(
            'OpenLP.SlideController', 'Audio Volume.'))
        controller.volumeSlider.setValue(controller.media_info.volume)
        controller.volumeSlider.setGeometry(QtCore.QRect(90, 160, 221, 24))
        controller.volumeSlider.setObjectName(u'volumeSlider')
        controller.mediabar.addToolbarWidget(controller.volumeSlider)
        control_panel.addWidget(controller.mediabar)
        controller.mediabar.setVisible(False)
        # Signals
        QtCore.QObject.connect(controller.seekSlider,
            QtCore.SIGNAL(u'valueChanged(int)'), controller.sendToPlugins)
        QtCore.QObject.connect(controller.volumeSlider,
            QtCore.SIGNAL(u'valueChanged(int)'), controller.sendToPlugins)

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
        if controller.isLive and controller.display:
            if self.curDisplayMediaPlayer and value:
                if self.curDisplayMediaPlayer[controller.display] != \
                    self.mediaPlayers[u'webkit']:
                    controller.display.setTransparency(False)
        # Special controls: Here media type specific Controls will be enabled
        # (e.g. for DVD control, ...)
        # TODO

    def resize(self, controller, display, player):
        """
        After Mainwindow changes or Splitter moved all related media widgets
        have to be resized
        """
        player.resize(display)

    def video(self, controller, file, muted, isBackground, hidden=False):
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
            if controller.media_info.is_background:
                # ignore start/end time
                controller.media_info.start_time = 0
                controller.media_info.end_time = 0
            else:
                controller.media_info.start_time = \
                    display.serviceItem.start_time
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
        if controller.isLive and not controller.media_info.is_background:
            display.frame.evaluateJavaScript(u'show_video( \
            "setBackBoard", null, null, null,"visible");')
        # now start playing - Preview is autoplay!
        autoplay = False
        # Preview requested
        if not controller.isLive:
            autoplay = True
        # Visible or background requested
        elif not hidden or controller.media_info.is_background:
            autoplay = True
        # Unblank on load set
        elif Settings().value(u'general/auto unblank',
            QtCore.QVariant(False)).toBool():
            autoplay = True
        if autoplay:
            if not self.video_play([controller]):
                critical_error_message_box(
                    translate('MediaPlugin.MediaItem', 'Unsupported File'),
                    unicode(translate('MediaPlugin.MediaItem',
                    'Unsupported File')))
                return False
        self.set_controls_visible(controller, True)
        log.debug(u'use %s controller' % self.curDisplayMediaPlayer[display])
        return True

    def check_file_type(self, controller, display):
        """
        Select the correct media Player type from the prioritized Player list
        """
        usedPlayers, overriddenPlayer = get_media_players()
        if overriddenPlayer and overriddenPlayer != u'auto':
            usedPlayers = [overriddenPlayer]
        if controller.media_info.file_info.isFile():
            suffix = u'*.%s' % \
                controller.media_info.file_info.suffix().toLower()
            for title in usedPlayers:
                player = self.mediaPlayers[title]
                if suffix in player.video_extensions_list:
                    if not controller.media_info.is_background or \
                        controller.media_info.is_background and \
                        player.canBackground:
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
                    self.curDisplayMediaPlayer[display].set_visible(display,
                        True)
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
                controller.seekSlider.setSliderPosition(0)

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
        self.set_controls_visible(controller, False)
        for display in self.curDisplayMediaPlayer.keys():
            if display.controller == controller:
                display.override = {}
                self.curDisplayMediaPlayer[display].reset(display)
                self.curDisplayMediaPlayer[display].set_visible(display, False)
                display.frame.evaluateJavaScript(u'show_video( \
                "setBackBoard", null, null, null,"hidden");')
                del self.curDisplayMediaPlayer[display]

    def video_hide(self, msg):
        """
        Hide the related video Widget

        ``msg``
            First element is the boolean for Live indication
        """
        isLive = msg[1]
        if not isLive:
            return
        controller = self.parent.liveController
        for display in self.curDisplayMediaPlayer.keys():
            if display.controller != controller or \
                self.curDisplayMediaPlayer[display].state != MediaState.Playing:
                continue
            self.curDisplayMediaPlayer[display].pause(display)
            self.curDisplayMediaPlayer[display].set_visible(display, False)

    def video_blank(self, msg):
        """
        Blank the related video Widget

        ``msg``
            First element is the boolean for Live indication
            Second element is the hide mode
        """
        isLive = msg[1]
        hide_mode = msg[2]
        if not isLive:
            return
        Receiver.send_message(u'live_display_hide', hide_mode)
        controller = self.parent.liveController
        for display in self.curDisplayMediaPlayer.keys():
            if display.controller != controller or \
                self.curDisplayMediaPlayer[display].state != MediaState.Playing:
                continue
            self.curDisplayMediaPlayer[display].pause(display)
            self.curDisplayMediaPlayer[display].set_visible(display, False)

    def video_unblank(self, msg):
        """
        Unblank the related video Widget

        ``msg``
            First element is not relevant in this context
            Second element is the boolean for Live indication
        """
        Receiver.send_message(u'live_display_show')
        isLive = msg[1]
        if not isLive:
            return
        controller = self.parent.liveController
        for display in self.curDisplayMediaPlayer.keys():
            if display.controller != controller or \
                self.curDisplayMediaPlayer[display].state != MediaState.Paused:
                continue
            if self.curDisplayMediaPlayer[display].play(display):
                self.curDisplayMediaPlayer[display].set_visible(display, True)
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
                video_list.extend([item for item in player.video_extensions_list
                    if item not in video_list])
        return video_list

    def finalise(self):
        self.timer.stop()
        for controller in self.controller:
            self.video_reset(controller)
