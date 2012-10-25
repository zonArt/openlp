# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Eric Ludin, Edwin Lunando, Brian T. Meyer,    #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Erode Woldsund, Martin Zibricky                                             #
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

from datetime import datetime
from distutils.version import LooseVersion
import logging
import os
import sys

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver
from openlp.core.lib.settings import Settings
from openlp.core.lib.mediaplayer import MediaPlayer
from openlp.core.ui.media import MediaState

log = logging.getLogger(__name__)

VLC_AVAILABLE = False
try:
    import vlc
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
    u'*.mp4',
    u'*.ogm', u'*.ogv',
    u'*.mkv', u'*.mka',
    u'*.ts', u'*.mpg',
    u'*.mpg', u'*.mp2',
    u'*.nsc',
    u'*.nsv',
    u'*.nut',
    u'*.ra', u'*.ram', u'*.rm', u'*.rv' ,u'*.rmbv',
    u'*.a52', u'*.dts', u'*.aac', u'*.flac' ,u'*.dv', u'*.vid',
    u'*.tta', u'*.tac',
    u'*.ty',
    u'*.dts',
    u'*.xa',
    u'*.iso',
    u'*.vob'
]


class VlcPlayer(MediaPlayer):
    """
    A specialised version of the MediaPlayer class, which provides a VLC
    display.
    """

    def __init__(self, parent):
        MediaPlayer.__init__(self, parent, u'vlc')
        self.original_name = u'VLC'
        self.display_name = u'&VLC'
        self.parent = parent
        self.canFolder = True
        self.audio_extensions_list = AUDIO_EXT
        self.video_extensions_list = VIDEO_EXT

    def setup(self, display):
        display.vlcWidget = QtGui.QFrame(display)
        # creating a basic vlc instance
        command_line_options = u'--no-video-title-show'
        if not display.hasAudio:
            command_line_options += u' --no-audio --no-video-title-show'
        if Settings().value(u'advanced/hide mouse',
            QtCore.QVariant(False)).toBool() and \
            display.controller.isLive:
            command_line_options += u' --mouse-hide-timeout=0'
        display.vlcInstance = vlc.Instance(command_line_options)
        display.vlcInstance.set_log_verbosity(2)
        # creating an empty vlc media player
        display.vlcMediaPlayer = display.vlcInstance.media_player_new()
        display.vlcWidget.resize(display.size())
        display.vlcWidget.raise_()
        display.vlcWidget.hide()
        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform == "win32":
            display.vlcMediaPlayer.set_hwnd(int(display.vlcWidget.winId()))
        elif sys.platform == "darwin":
            display.vlcMediaPlayer.set_agl(int(display.vlcWidget.winId()))
        else:
            # for Linux using the X Server
            display.vlcMediaPlayer.set_xwindow(int(display.vlcWidget.winId()))
        self.hasOwnWidget = True

    def check_available(self):
        return VLC_AVAILABLE

    def load(self, display):
        log.debug(u'load vid in Vlc Controller')
        controller = display.controller
        volume = controller.media_info.volume
        file_path = str(
            controller.media_info.file_info.absoluteFilePath().toUtf8())
        path = os.path.normcase(file_path)
        # create the media
        display.vlcMedia = display.vlcInstance.media_new_path(path)
        # put the media in the media player
        display.vlcMediaPlayer.set_media(display.vlcMedia)
        # parse the metadata of the file
        display.vlcMedia.parse()
        self.volume(display, volume)
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
            Receiver.send_message(u'openlp_process_events')
            if (datetime.now() - start).seconds > 60:
                return False
        return True

    def resize(self, display):
        display.vlcWidget.resize(display.size())

    def play(self, display):
        controller = display.controller
        start_time = 0
        if controller.media_info.start_time > 0:
            start_time = controller.media_info.start_time
        display.vlcMediaPlayer.play()
        if not self.media_state_wait(display, vlc.State.Playing):
            return False
        if start_time > 0:
            self.seek(display, controller.media_info.start_time * 1000)
        controller.media_info.length = \
            int(display.vlcMediaPlayer.get_media().get_duration() / 1000)
        controller.seekSlider.setMaximum(controller.media_info.length * 1000)
        self.state = MediaState.Playing
        display.vlcWidget.raise_()
        return True

    def pause(self, display):
        if display.vlcMedia.get_state() != vlc.State.Playing:
            return
        display.vlcMediaPlayer.pause()
        if self.media_state_wait(display, vlc.State.Paused):
            self.state = MediaState.Paused

    def stop(self, display):
        display.vlcMediaPlayer.stop()
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        if display.hasAudio:
            display.vlcMediaPlayer.audio_set_volume(vol)

    def seek(self, display, seekVal):
        if display.vlcMediaPlayer.is_seekable():
            display.vlcMediaPlayer.set_time(seekVal)

    def reset(self, display):
        display.vlcMediaPlayer.stop()
        display.vlcWidget.setVisible(False)
        self.state = MediaState.Off

    def set_visible(self, display, status):
        if self.hasOwnWidget:
            display.vlcWidget.setVisible(status)

    def update_ui(self, display):
        if display.vlcMedia.get_state() == vlc.State.Ended:
            self.stop(display)
        controller = display.controller
        if controller.media_info.end_time > 0:
            if display.vlcMediaPlayer.get_time() > \
                controller.media_info.end_time * 1000:
                self.stop(display)
                self.set_visible(display, False)
        if not controller.seekSlider.isSliderDown():
            controller.seekSlider.setSliderPosition( \
                display.vlcMediaPlayer.get_time())

