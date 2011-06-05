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
from datetime import datetime
try:
    import vlc
except:
    pass
from PyQt4 import QtCore, QtGui
from openlp.core.lib import Receiver
from openlp.plugins.media.lib import MediaAPI, MediaState

log = logging.getLogger(__name__)

class VlcAPI(MediaAPI):
    """
    Specialiced MediaAPI class
    to reflect Features of the Vlc API
    """
    def __init__(self, parent):
        MediaAPI.__init__(self, parent)
        self.parent = parent
        self.video_extensions_list = [
            u'*.3gp'
            , u'*.asf', u'*.wmv'
            , u'*.au'
            , u'*.avi'
            , u'*.flv'
            , u'*.mov'
            , u'*.mp4'
            , u'*.ogm', u'*.ogg'
            , u'*.mkv', u'*.mka'
            , u'*.ts', u'*.mpg'
            , u'*.mpg', u'*.mp3', u'*.mp2'
            , u'*.nsc'
            , u'*.nsv'
            , u'*.nut'
            , u'*.ra', u'*.ram', u'*.rm', u'*.rv' ,u'*.rmbv'
            , u'*.a52', u'*.dts', u'*.aac', u'*.flac' ,u'*.dv', u'*.vid'
            , u'*.tta', u'*.tac'
            , u'*.ty'
            , u'*.wav', u'*.dts'
            , u'*.xa'
            , u'*.iso'
            ]

    def setup_controls(self, controller, control_panel):
        pass

    def setup(self, display):
        display.vlcWidget = QtGui.QFrame(display)
        # creating a basic vlc instance
        if display.hasAudio:
            display.vlcInstance = vlc.Instance()
        else:
            display.vlcInstance = vlc.Instance('--no-audio')
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
        if sys.platform == "linux2": # for Linux using the X Server
            display.vlcMediaPlayer.set_xwindow(int(display.vlcWidget.winId()))
        elif sys.platform == "win32": # for Windows
            display.vlcMediaPlayer.set_hwnd(int(display.vlcWidget.winId()))
        elif sys.platform == "darwin": # for MacOS
            display.vlcMediaPlayer.set_agl(int(display.vlcWidget.winId()))
        self.hasOwnWidget = True

    @staticmethod
    def is_available():
        try:
            import vlc
            return True
        except:
            return False

    def get_supported_file_types(self):
        self.supported_file_types = ['avi']
        self.additional_extensions = {
            u'audio/ac3': [u'.ac3'],
            u'audio/flac': [u'.flac'],
            u'audio/x-m4a': [u'.m4a'],
            u'audio/midi': [u'.mid', u'.midi'],
            u'audio/x-mp3': [u'.mp3'],
            u'audio/mpeg': [u'.mp3', u'.mp2', u'.mpga', u'.mpega', u'.m4a'],
            u'audio/qcelp': [u'.qcp'],
            u'audio/x-wma': [u'.wma'],
            u'audio/x-ms-wma': [u'.wma'],
            u'video/x-flv': [u'.flv'],
            u'video/x-matroska': [u'.mpv', u'.mkv'],
            u'video/x-wmv': [u'.wmv'],
            u'video/x-ms-wmv': [u'.wmv']}

    def load(self, display):
        log.debug(u'load vid in Vlc Controller')
        controller = display.parent
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
        return True

    def mediaStateWait(self, display, mediaState):
        """
        Wait for the video to change its state
        Wait no longer than 5 seconds.
        """
        start = datetime.now()
        while not mediaState == display.vlcMedia.get_state():
            if display.vlcMedia.get_state() == vlc.State.Error:
                return False
            Receiver.send_message(u'openlp_process_events')
            if (datetime.now() - start).seconds > 5:
                return False
        return True

    def resize(self, display):
        display.vlcWidget.resize(display.size())

    def play(self, display):
        self.set_visible(display, True)
        display.vlcMediaPlayer.play()
        if self.mediaStateWait(display, vlc.State.Playing):
            self.state = MediaState.Playing

    def pause(self, display):
        display.vlcMediaPlayer.pause()
        if self.mediaStateWait(display, vlc.State.Paused):
            self.state = MediaState.Paused

    def stop(self, display):
        display.vlcMediaPlayer.stop()
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        display.vlcMediaPlayer.audio_set_volume(vol)

    def seek(self, display, seekVal):
        if display.vlcMediaPlayer.is_seekable():
            display.vlcMediaPlayer.set_position(seekVal/1000.0)

    def reset(self, display):
        display.vlcMediaPlayer.stop()
        display.vlcWidget.setVisible(False)
        self.state = MediaState.Off

    def set_visible(self, display, status):
        if self.hasOwnWidget:
            display.vlcWidget.setVisible(status)

    def update_ui(self, display):
        controller = display.parent
        controller.seekSlider.setMaximum(1000)
        if not controller.seekSlider.isSliderDown():
            currentPos = display.vlcMediaPlayer.get_position() * 1000
            controller.seekSlider.setSliderPosition(currentPos)

    def get_supported_file_types(self):
        pass
