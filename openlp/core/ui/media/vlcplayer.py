# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
import sys
import ctypes
from PyQt5 import QtWidgets

from openlp.core.common import Settings, is_win, is_macosx, is_linux
from openlp.core.lib import translate
from openlp.core.ui.media import MediaState, MediaType
from openlp.core.ui.media.mediaplayer import MediaPlayer

log = logging.getLogger(__name__)

# Audio and video extensions copied from 'include/vlc_interface.h' from vlc 2.2.0 source
AUDIO_EXT = ['*.3ga', '*.669', '*.a52', '*.aac', '*.ac3', '*.adt', '*.adts', '*.aif', '*.aifc', '*.aiff', '*.amr',
             '*.aob', '*.ape', '*.awb', '*.caf', '*.dts', '*.flac', '*.it', '*.kar', '*.m4a', '*.m4b', '*.m4p', '*.m5p',
             '*.mid', '*.mka', '*.mlp', '*.mod', '*.mpa', '*.mp1', '*.mp2', '*.mp3', '*.mpc', '*.mpga', '*.mus',
             '*.oga', '*.ogg', '*.oma', '*.opus', '*.qcp', '*.ra', '*.rmi', '*.s3m', '*.sid', '*.spx', '*.thd', '*.tta',
             '*.voc', '*.vqf', '*.w64', '*.wav', '*.wma', '*.wv', '*.xa', '*.xm']

VIDEO_EXT = ['*.3g2', '*.3gp', '*.3gp2', '*.3gpp', '*.amv', '*.asf', '*.avi', '*.bik', '*.divx', '*.drc', '*.dv',
             '*.f4v', '*.flv', '*.gvi', '*.gxf', '*.iso', '*.m1v', '*.m2v', '*.m2t', '*.m2ts', '*.m4v', '*.mkv',
             '*.mov', '*.mp2', '*.mp2v', '*.mp4', '*.mp4v', '*.mpe', '*.mpeg', '*.mpeg1', '*.mpeg2', '*.mpeg4', '*.mpg',
             '*.mpv2', '*.mts', '*.mtv', '*.mxf', '*.mxg', '*.nsv', '*.nuv', '*.ogg', '*.ogm', '*.ogv', '*.ogx', '*.ps',
             '*.rec', '*.rm', '*.rmvb', '*.rpl', '*.thp', '*.tod', '*.ts', '*.tts', '*.txd', '*.vob', '*.vro', '*.webm',
             '*.wm', '*.wmv', '*.wtv', '*.xesc',
             # These extensions was not in the official list, added manually.
             '*.nut', '*.rv', '*.xvid']


def get_vlc():
    """
    In order to make this module more testable, we have to wrap the VLC import inside a method. We do this so that we
    can mock out the VLC module entirely.

    :return: The "vlc" module, or None
    """
    if 'openlp.core.ui.media.vendor.vlc' in sys.modules:
        # If VLC has already been imported, no need to do all the stuff below again
        return sys.modules['openlp.core.ui.media.vendor.vlc']
    is_vlc_available = False
    try:
        if is_macosx():
            # Newer versions of VLC on OS X need this. See https://forum.videolan.org/viewtopic.php?t=124521
            os.environ['VLC_PLUGIN_PATH'] = '/Applications/VLC.app/Contents/MacOS/plugins'
        # On Windows when frozen in PyInstaller, we need to blank SetDllDirectoryW to allow loading of the VLC dll.
        # This is due to limitations (by desgin) in PyInstaller. SetDllDirectoryW original value is restored once
        # VLC has been imported.
        if is_win():
            buffer_size = 1024
            dll_directory = ctypes.create_unicode_buffer(buffer_size)
            new_buffer_size = ctypes.windll.kernel32.GetDllDirectoryW(buffer_size, dll_directory)
            dll_directory = ''.join(dll_directory[:new_buffer_size]).replace('\0', '')
            log.debug('Original DllDirectory: %s' % dll_directory)
            ctypes.windll.kernel32.SetDllDirectoryW(None)
        from openlp.core.ui.media.vendor import vlc
        if is_win():
            ctypes.windll.kernel32.SetDllDirectoryW(dll_directory)
        is_vlc_available = bool(vlc.get_default_instance())
    except (ImportError, NameError, NotImplementedError):
        pass
    except OSError as e:
        if is_win():
            if not isinstance(e, WindowsError) and e.winerror != 126:
                raise
        else:
            pass
    if is_vlc_available:
        try:
            VERSION = vlc.libvlc_get_version().decode('UTF-8')
        except:
            VERSION = '0.0.0'
        # LooseVersion does not work when a string contains letter and digits (e. g. 2.0.5 Twoflower).
        # http://bugs.python.org/issue14894
        if LooseVersion(VERSION.split()[0]) < LooseVersion('1.1.0'):
            is_vlc_available = False
            log.debug('VLC could not be loaded, because the vlc version is too old: %s' % VERSION)
    if is_vlc_available:
        return vlc
    else:
        return None


# On linux we need to initialise X threads, but not when running tests.
# This needs to happen on module load and not in get_vlc(), otherwise it can cause crashes on some DE on some setups
# (reported on Gnome3, Unity, Cinnamon, all GTK+ based) when using native filedialogs...
if is_linux() and 'nose' not in sys.argv[0] and get_vlc():
    import ctypes
    try:
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so.6')
        except OSError:
            # If libx11.so.6 was not found, fallback to more generic libx11.so
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
        x11.XInitThreads()
    except:
        log.exception('Failed to run XInitThreads(), VLC might not work properly!')


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

        :param display: The display where the media is
        :return:
        """
        vlc = get_vlc()
        display.vlc_widget = QtWidgets.QFrame(display)
        display.vlc_widget.setFrameStyle(QtWidgets.QFrame.NoFrame)
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
            # We have to use 'set_nsobject' since Qt5 on OSX uses Cocoa
            # framework and not the old Carbon.
            display.vlc_media_player.set_nsobject(win_id)
        else:
            # for Linux/*BSD using the X Server
            display.vlc_media_player.set_xwindow(win_id)
        self.has_own_widget = True

    def check_available(self):
        """
        Return the availability of VLC
        """
        return get_vlc() is not None

    def load(self, display):
        """
        Load a video into VLC

        :param display: The display where the media is
        :return:
        """
        vlc = get_vlc()
        log.debug('load vid in Vlc Controller')
        controller = display.controller
        volume = controller.media_info.volume
        file_path = str(controller.media_info.file_info.absoluteFilePath())
        path = os.path.normcase(file_path)
        # create the media
        if controller.media_info.media_type == MediaType.CD:
            if is_win():
                path = '/' + path
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
        return True

    def media_state_wait(self, display, media_state):
        """
        Wait for the video to change its state
        Wait no longer than 60 seconds. (loading an iso file needs a long time)

        :param media_state: The state of the playing media
        :param display: The display where the media is
        :return:
        """
        vlc = get_vlc()
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

        :param display: The display where the media is
        :return:
        """
        display.vlc_widget.resize(display.size())

    def play(self, display):
        """
        Play the current item

        :param display: The display where the media is
        :return:
        """
        vlc = get_vlc()
        controller = display.controller
        start_time = 0
        log.debug('vlc play')
        if self.state != MediaState.Paused and controller.media_info.start_time > 0:
            start_time = controller.media_info.start_time
        threading.Thread(target=display.vlc_media_player.play).start()
        if not self.media_state_wait(display, vlc.State.Playing):
            return False
        if self.state != MediaState.Paused and controller.media_info.start_time > 0:
            log.debug('vlc play, start time set')
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
        self.volume(display, controller.media_info.volume)
        if start_time > 0 and display.vlc_media_player.is_seekable():
            display.vlc_media_player.set_time(int(start_time))
        controller.seek_slider.setMaximum(controller.media_info.length)
        self.state = MediaState.Playing
        display.vlc_widget.raise_()
        return True

    def pause(self, display):
        """
        Pause the current item

        :param display: The display where the media is
        :return:
        """
        vlc = get_vlc()
        if display.vlc_media.get_state() != vlc.State.Playing:
            return
        display.vlc_media_player.pause()
        if self.media_state_wait(display, vlc.State.Paused):
            self.state = MediaState.Paused

    def stop(self, display):
        """
        Stop the current item

        :param display: The display where the media is
        :return:
        """
        threading.Thread(target=display.vlc_media_player.stop).start()
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        """
        Set the volume

        :param vol: The volume to be sets
        :param display: The display where the media is
        :return:
        """
        if display.has_audio:
            display.vlc_media_player.audio_set_volume(vol)

    def seek(self, display, seek_value):
        """
        Go to a particular position

        :param seek_value: The position of where a seek goes to
        :param display: The display where the media is
        """
        if display.controller.media_info.media_type == MediaType.CD \
                or display.controller.media_info.media_type == MediaType.DVD:
            seek_value += int(display.controller.media_info.start_time * 1000)
        if display.vlc_media_player.is_seekable():
            display.vlc_media_player.set_time(seek_value)

    def reset(self, display):
        """
        Reset the player

        :param display: The display where the media is
        """
        display.vlc_media_player.stop()
        display.vlc_widget.setVisible(False)
        self.state = MediaState.Off

    def set_visible(self, display, status):
        """
        Set the visibility

        :param display: The display where the media is
        :param status: The visibility status
        """
        if self.has_own_widget:
            display.vlc_widget.setVisible(status)

    def update_ui(self, display):
        """
        Update the UI

        :param display: The display where the media is
        """
        vlc = get_vlc()
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
