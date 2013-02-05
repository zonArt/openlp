# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
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
import sys

from PyQt4 import QtGui

from openlp.core.lib import Settings, translate
from openlp.core.ui.media import MediaState
from openlp.core.ui.media.mediaplayer import MediaPlayer

log = logging.getLogger(__name__)

VLC_AVAILABLE = False
try:
    from openlp.core.ui.media.vendor import vlc
    VLC_AVAILABLE = bool(vlc.get_default_instance())
except (ImportError, NameError, NotImplementedError):
    pass
except OSError, e:
    if sys.platform.startswith('win'):
        if not isinstance(e, WindowsError) and e.winerror != 126:
            raise
    else:
        raise

if VLC_AVAILABLE:
    try:
        version = vlc.libvlc_get_version()
    except:
        version = u'0.0.0'
    if LooseVersion(version) < LooseVersion('1.1.0'):
        VLC_AVAILABLE = False
        log.debug(u'VLC could not be loaded: %s' % version)

AUDIO_EXT = [u'*.mp3', u'*.wav', u'*.wma', u'*.ogg']

VIDEO_EXT = [
    u'*.3gp',
    u'*.asf', u'*.wmv',
    u'*.au',
    u'*.avi',
    u'*.flv',
    u'*.mov',
    u'*.mp4', u'*.m4v',
    u'*.ogm', u'*.ogv',
    u'*.mkv', u'*.mka',
    u'*.ts', u'*.mpg',
    u'*.mpg', u'*.mp2',
    u'*.nsc',
    u'*.nsv',
    u'*.nut',
    u'*.ra', u'*.ram', u'*.rm', u'*.rv', u'*.rmbv',
    u'*.a52', u'*.dts', u'*.aac', u'*.flac', u'*.dv', u'*.vid',
    u'*.tta', u'*.tac',
    u'*.ty',
    u'*.dts',
    u'*.xa',
    u'*.iso',
    u'*.vob',
    u'*.webm'
]


class VlcPlayer(MediaPlayer):
    """
    A specialised version of the MediaPlayer class, which provides a VLC
    display.
    """

    def __init__(self, parent):
        """
        Constructor
        """
        MediaPlayer.__init__(self, parent, u'vlc')
        self.original_name = u'VLC'
        self.display_name = u'&VLC'
        self.parent = parent
        self.canFolder = True
        self.audio_extensions_list = AUDIO_EXT
        self.video_extensions_list = VIDEO_EXT

    def setup(self, display):
        """
        Set up the media player
        """
        display.vlcWidget = QtGui.QFrame(display)
        display.vlcWidget.setFrameStyle(QtGui.QFrame.NoFrame)
        # creating a basic vlc instance
        command_line_options = u'--no-video-title-show'
        if not display.hasAudio:
            command_line_options += u' --no-audio --no-video-title-show'
        if Settings().value(u'advanced/hide mouse') and display.controller.isLive:
            command_line_options += u' --mouse-hide-timeout=0'
        display.vlcInstance = vlc.Instance(command_line_options)
        display.vlcInstance.set_log_verbosity(2)
        # creating an empty vlc media player
        display.vlcMediaPlayer = display.vlcInstance.media_player_new()
        display.vlcWidget.resize(display.size())
        display.vlcWidget.raise_()
        display.vlcWidget.hide()
        # The media player has to be 'connected' to the QFrame.
        # (otherwise a video would be displayed in it's own window)
        # This is platform specific!
        # You have to give the id of the QFrame (or similar object)
        # to vlc, different platforms have different functions for this.
        win_id = int(display.vlcWidget.winId())
        if sys.platform == "win32":
            display.vlcMediaPlayer.set_hwnd(win_id)
        elif sys.platform == "darwin":
            # We have to use 'set_nsobject' since Qt4 on OSX uses Cocoa
            # framework and not the old Carbon.
            display.vlcMediaPlayer.set_nsobject(win_id)
        else:
            # for Linux using the X Server
            display.vlcMediaPlayer.set_xwindow(win_id)
        self.hasOwnWidget = True

    def check_available(self):
        """
        Return the availability of VLC
        """
        return VLC_AVAILABLE

    def load(self, display):
        """
        Load a video into VLC
        """
        log.debug(u'load vid in Vlc Controller')
        controller = display.controller
        volume = controller.media_info.volume
        file_path = str(controller.media_info.file_info.absoluteFilePath())
        path = os.path.normcase(file_path)
        # create the media
        display.vlcMedia = display.vlcInstance.media_new_path(path)
        # put the media in the media player
        display.vlcMediaPlayer.set_media(display.vlcMedia)
        # parse the metadata of the file
        display.vlcMedia.parse()
        self.volume(display, volume)
        # We need to set media_info.length during load because we want
        # to avoid start and stop the video twice. Once for real playback
        # and once to just get media length.
        #
        # Media plugin depends on knowing media length before playback.
        controller.media_info.length = int(display.vlcMediaPlayer.get_media().get_duration() / 1000)
        return True

    def media_state_wait(self, display, mediaState):
        """
        Wait for the video to change its state
        Wait no longer than 60 seconds. (loading an iso file needs a long time)
        """
        start = datetime.now()
        while not mediaState == display.vlcMedia.get_state():
            if display.vlcMedia.get_state() == vlc.State.Error:
                return False
            self.application.process_events()
            if (datetime.now() - start).seconds > 60:
                return False
        return True

    def resize(self, display):
        """
        Resize the player
        """
        display.vlcWidget.resize(display.size())

    def play(self, display):
        """
        Play the current item
        """
        controller = display.controller
        start_time = 0
        if self.state != MediaState.Paused and controller.media_info.start_time > 0:
            start_time = controller.media_info.start_time
        display.vlcMediaPlayer.play()
        if not self.media_state_wait(display, vlc.State.Playing):
            return False
        self.volume(display, controller.media_info.volume)
        if start_time > 0:
            self.seek(display, controller.media_info.start_time * 1000)
        controller.media_info.length = int(display.vlcMediaPlayer.get_media().get_duration() / 1000)
        controller.seekSlider.setMaximum(controller.media_info.length * 1000)
        self.state = MediaState.Playing
        display.vlcWidget.raise_()
        return True

    def pause(self, display):
        """
        Pause the current item
        """
        if display.vlcMedia.get_state() != vlc.State.Playing:
            return
        display.vlcMediaPlayer.pause()
        if self.media_state_wait(display, vlc.State.Paused):
            self.state = MediaState.Paused

    def stop(self, display):
        """
        Stop the current item
        """
        display.vlcMediaPlayer.stop()
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        """
        Set the volume
        """
        if display.hasAudio:
            display.vlcMediaPlayer.audio_set_volume(vol)

    def seek(self, display, seekVal):
        """
        Go to a particular position
        """
        if display.vlcMediaPlayer.is_seekable():
            display.vlcMediaPlayer.set_time(seekVal)

    def reset(self, display):
        """
        Reset the player
        """
        display.vlcMediaPlayer.stop()
        display.vlcWidget.setVisible(False)
        self.state = MediaState.Off

    def set_visible(self, display, status):
        """
        Set the visibility
        """
        if self.hasOwnWidget:
            display.vlcWidget.setVisible(status)

    def update_ui(self, display):
        """
        Update the UI
        """
        # Stop video if playback is finished.
        if display.vlcMedia.get_state() == vlc.State.Ended:
            self.stop(display)
        controller = display.controller
        if controller.media_info.end_time > 0:
            if display.vlcMediaPlayer.get_time() > controller.media_info.end_time * 1000:
                self.stop(display)
                self.set_visible(display, False)
        if not controller.seekSlider.isSliderDown():
            controller.seekSlider.blockSignals(True)
            controller.seekSlider.setSliderPosition(display.vlcMediaPlayer.get_time())
            controller.seekSlider.blockSignals(False)

    def get_info(self):
        """
        Return some information about this player
        """
        return(translate('Media.player', 'VLC is an external player which '
            'supports a number of different formats.') +
            u'<br/> <strong>' + translate('Media.player', 'Audio') +
            u'</strong><br/>' + unicode(AUDIO_EXT) + u'<br/><strong>' +
            translate('Media.player', 'Video') + u'</strong><br/>' +
            unicode(VIDEO_EXT) + u'<br/>')
