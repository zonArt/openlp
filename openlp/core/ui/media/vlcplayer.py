# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
The :mod:`~openlp.core.ui.media.vlcplayer` module contains our VLC component wrapper
"""
from datetime import datetime
from distutils.version import LooseVersion
import logging
import os
import threading

from PyQt4 import QtGui

from openlp.core.common import Settings, is_win, is_macosx
from openlp.core.lib import translate
from openlp.core.ui.media import MediaState, MediaType
from openlp.core.ui.media.mediaplayer import MediaPlayer

log = logging.getLogger(__name__)

VLC_AVAILABLE = False
try:
    from openlp.core.ui.media.vendor import vlc
    VLC_AVAILABLE = bool(vlc.get_default_instance())
except (ImportError, NameError, NotImplementedError):
    pass
except OSError as e:
    if is_win():
        if not isinstance(e, WindowsError) and e.winerror != 126:
            raise
    elif is_macosx():
        pass
    else:
        raise

if VLC_AVAILABLE:
    try:
        VERSION = vlc.libvlc_get_version().decode('UTF-8')
    except:
        VERSION = '0.0.0'
    # LooseVersion does not work when a string contains letter and digits (e. g. 2.0.5 Twoflower).
    # http://bugs.python.org/issue14894
    if LooseVersion(VERSION.split()[0]) < LooseVersion('1.1.0'):
        VLC_AVAILABLE = False
        log.debug('VLC could not be loaded, because the vlc version is too old: %s' % VERSION)

AUDIO_EXT = ['*.mp3', '*.wav', '*.wma', '*.ogg']

VIDEO_EXT = [
    '*.3gp',
    '*.asf', '*.wmv',
    '*.au',
    '*.avi',
    '*.flv',
    '*.mov',
    '*.mp4', '*.m4v',
    '*.ogm', '*.ogv',
    '*.mkv', '*.mka',
    '*.ts', '*.mpg',
    '*.mpg', '*.mp2',
    '*.nsc',
    '*.nsv',
    '*.nut',
    '*.ra', '*.ram', '*.rm', '*.rv', '*.rmbv',
    '*.a52', '*.dts', '*.aac', '*.flac', '*.dv', '*.vid',
    '*.tta', '*.tac',
    '*.ty',
    '*.dts',
    '*.xa',
    '*.iso',
    '*.vob',
    '*.webm'
]


class VlcPlayer(MediaPlayer):
    """
    A specialised version of the MediaPlayer class, which provides a VLC display.
    """

    def __init__(self, parent):
        """
        Constructor
        """
        super(VlcPlayer, self).__init__(parent, 'vlc')
        self.original_name = 'VLC'
        self.display_name = '&VLC'
        self.parent = parent
        self.can_folder = True
        self.audio_extensions_list = AUDIO_EXT
        self.video_extensions_list = VIDEO_EXT

    def setup(self, display):
        """
        Set up the media player
        """
        display.vlc_widget = QtGui.QFrame(display)
        display.vlc_widget.setFrameStyle(QtGui.QFrame.NoFrame)
        # creating a basic vlc instance
        command_line_options = '--no-video-title-show'
        if not display.has_audio:
            command_line_options += ' --no-audio --no-video-title-show'
        if Settings().value('advanced/hide mouse') and display.controller.is_live:
            command_line_options += ' --mouse-hide-timeout=0'
        display.vlc_instance = vlc.Instance(command_line_options)
        # creating an empty vlc media player
        display.vlc_media_player = display.vlc_instance.media_player_new()
        display.vlc_widget.resize(display.size())
        display.vlc_widget.raise_()
        display.vlc_widget.hide()
        # The media player has to be 'connected' to the QFrame.
        # (otherwise a video would be displayed in it's own window)
        # This is platform specific!
        # You have to give the id of the QFrame (or similar object)
        # to vlc, different platforms have different functions for this.
        win_id = int(display.vlc_widget.winId())
        if is_win():
            display.vlc_media_player.set_hwnd(win_id)
        elif is_macosx():
            # We have to use 'set_nsobject' since Qt4 on OSX uses Cocoa
            # framework and not the old Carbon.
            display.vlc_media_player.set_nsobject(win_id)
        else:
            # for Linux using the X Server
            display.vlc_media_player.set_xwindow(win_id)
        self.has_own_widget = True

    def check_available(self):
        """
        Return the availability of VLC
        """
        return VLC_AVAILABLE

    def load(self, display):
        """
        Load a video into VLC
        """
        log.debug('load vid in Vlc Controller')
        controller = display.controller
        volume = controller.media_info.volume
        file_path = str(controller.media_info.file_info.absoluteFilePath())
        path = os.path.normcase(file_path)
        # create the media
        if controller.media_info.media_type == MediaType.CD:
            display.vlc_media = display.vlc_instance.media_new_location('cdda://' + path)
            display.vlc_media_player.set_media(display.vlc_media)
            display.vlc_media_player.play()
            # Wait for media to start playing. In this case VLC actually returns an error.
            self.media_state_wait(display, vlc.State.Playing)
            # If subitems exists, this is a CD
            audio_cd_tracks = display.vlc_media.subitems()
            if not audio_cd_tracks or audio_cd_tracks.count() < 1:
                return False
            display.vlc_media = audio_cd_tracks.item_at_index(controller.media_info.title_track)
        else:
            display.vlc_media = display.vlc_instance.media_new_path(path)
        # put the media in the media player
        display.vlc_media_player.set_media(display.vlc_media)
        # parse the metadata of the file
        display.vlc_media.parse()
        self.volume(display, volume)
        # We need to set media_info.length during load because we want
        # to avoid start and stop the video twice. Once for real playback
        # and once to just get media length.
        #
        # Media plugin depends on knowing media length before playback.
        controller.media_info.length = int(display.vlc_media_player.get_media().get_duration() / 1000)
        return True

    def media_state_wait(self, display, media_state):
        """
        Wait for the video to change its state
        Wait no longer than 60 seconds. (loading an iso file needs a long time)
        """
        start = datetime.now()
        while not media_state == display.vlc_media.get_state():
            if display.vlc_media.get_state() == vlc.State.Error:
                return False
            self.application.process_events()
            if (datetime.now() - start).seconds > 60:
                return False
        return True

    def resize(self, display):
        """
        Resize the player
        """
        display.vlc_widget.resize(display.size())

    def play(self, display):
        """
        Play the current item
        """
        controller = display.controller
        start_time = 0
        log.debug('vlc play')
        if self.state != MediaState.Paused and controller.media_info.start_time > 0:
            start_time = controller.media_info.start_time
        threading.Thread(target=display.vlc_media_player.play).start()
        if not self.media_state_wait(display, vlc.State.Playing):
            return False
        if self.state != MediaState.Paused and controller.media_info.start_time > 0:
            log.debug('vlc play, starttime set')
            start_time = controller.media_info.start_time
        log.debug('mediatype: ' + str(controller.media_info.media_type))
        # Set tracks for the optical device
        if controller.media_info.media_type == MediaType.DVD:
            log.debug('vlc play, playing started')
            if controller.media_info.title_track > 0:
                log.debug('vlc play, title_track set: ' + str(controller.media_info.title_track))
                display.vlc_media_player.set_title(controller.media_info.title_track)
            display.vlc_media_player.play()
            if not self.media_state_wait(display, vlc.State.Playing):
                return False
            if controller.media_info.audio_track > 0:
                display.vlc_media_player.audio_set_track(controller.media_info.audio_track)
                log.debug('vlc play, audio_track set: ' + str(controller.media_info.audio_track))
            if controller.media_info.subtitle_track > 0:
                display.vlc_media_player.video_set_spu(controller.media_info.subtitle_track)
                log.debug('vlc play, subtitle_track set: ' + str(controller.media_info.subtitle_track))
            if controller.media_info.start_time > 0:
                log.debug('vlc play, starttime set: ' + str(controller.media_info.start_time))
                start_time = controller.media_info.start_time
            controller.media_info.length = controller.media_info.end_time - controller.media_info.start_time
        else:
            controller.media_info.length = int(display.vlc_media_player.get_media().get_duration() / 1000)
        self.volume(display, controller.media_info.volume)
        if start_time > 0 and display.vlc_media_player.is_seekable():
            display.vlc_media_player.set_time(int(start_time * 1000))
        controller.seek_slider.setMaximum(controller.media_info.length * 1000)
        self.state = MediaState.Playing
        display.vlc_widget.raise_()
        return True

    def pause(self, display):
        """
        Pause the current item
        """
        if display.vlc_media.get_state() != vlc.State.Playing:
            return
        display.vlc_media_player.pause()
        if self.media_state_wait(display, vlc.State.Paused):
            self.state = MediaState.Paused

    def stop(self, display):
        """
        Stop the current item
        """
        threading.Thread(target=display.vlc_media_player.stop).start()
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        """
        Set the volume
        """
        if display.has_audio:
            display.vlc_media_player.audio_set_volume(vol)

    def seek(self, display, seek_value):
        """
        Go to a particular position
        """
        if display.controller.media_info.media_type == MediaType.CD \
                or display.controller.media_info.media_type == MediaType.DVD:
            seek_value += int(display.controller.media_info.start_time * 1000)
        if display.vlc_media_player.is_seekable():
            display.vlc_media_player.set_time(seek_value)

    def reset(self, display):
        """
        Reset the player
        """
        display.vlc_media_player.stop()
        display.vlc_widget.setVisible(False)
        self.state = MediaState.Off

    def set_visible(self, display, status):
        """
        Set the visibility
        """
        if self.has_own_widget:
            display.vlc_widget.setVisible(status)

    def update_ui(self, display):
        """
        Update the UI
        """
        # Stop video if playback is finished.
        if display.vlc_media.get_state() == vlc.State.Ended:
            self.stop(display)
        controller = display.controller
        if controller.media_info.end_time > 0:
            if display.vlc_media_player.get_time() > controller.media_info.end_time * 1000:
                self.stop(display)
                self.set_visible(display, False)
        if not controller.seek_slider.isSliderDown():
            controller.seek_slider.blockSignals(True)
            if display.controller.media_info.media_type == MediaType.CD \
                    or display.controller.media_info.media_type == MediaType.DVD:
                controller.seek_slider.setSliderPosition(display.vlc_media_player.get_time() -
                                                         int(display.controller.media_info.start_time * 1000))
            else:
                controller.seek_slider.setSliderPosition(display.vlc_media_player.get_time())
            controller.seek_slider.blockSignals(False)

    def get_info(self):
        """
        Return some information about this player
        """
        return(translate('Media.player', 'VLC is an external player which '
               'supports a number of different formats.') +
               '<br/> <strong>' + translate('Media.player', 'Audio') +
               '</strong><br/>' + str(AUDIO_EXT) + '<br/><strong>' +
               translate('Media.player', 'Video') + '</strong><br/>' +
               str(VIDEO_EXT) + '<br/>')
