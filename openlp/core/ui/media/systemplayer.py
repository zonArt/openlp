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
The :mod:`~openlp.core.ui.media.systemplayer` contains the system (aka QtMultimedia) player component.
"""
import functools
import logging
import mimetypes

from PyQt5 import QtCore, QtMultimedia, QtMultimediaWidgets

from openlp.core.lib import translate
from openlp.core.ui.media import MediaState
from openlp.core.ui.media.mediaplayer import MediaPlayer


log = logging.getLogger(__name__)

ADDITIONAL_EXT = {
    'audio/ac3': ['.ac3'],
    'audio/flac': ['.flac'],
    'audio/x-m4a': ['.m4a'],
    'audio/midi': ['.mid', '.midi'],
    'audio/x-mp3': ['.mp3'],
    'audio/mpeg': ['.mp3', '.mp2', '.mpga', '.mpega', '.m4a'],
    'audio/qcelp': ['.qcp'],
    'audio/x-wma': ['.wma'],
    'audio/x-ms-wma': ['.wma'],
    'video/x-flv': ['.flv'],
    'video/x-matroska': ['.mpv', '.mkv'],
    'video/x-wmv': ['.wmv'],
    'video/x-mpg': ['.mpg'],
    'video/mpeg': ['.mp4', '.mts', '.mov'],
    'video/x-ms-wmv': ['.wmv']
}


class SystemPlayer(MediaPlayer):
    """
    A specialised version of the MediaPlayer class, which provides a QtMultimedia display.
    """

    def __init__(self, parent):
        """
        Constructor
        """
        super(SystemPlayer, self).__init__(parent, 'system')
        self.original_name = 'System'
        self.display_name = '&System'
        self.parent = parent
        self.additional_extensions = ADDITIONAL_EXT
        self.media_player = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
        mimetypes.init()
        media_service = self.media_player.service()
        log.info(media_service.__class__.__name__)
        # supportedMimeTypes doesn't return anything on Linux and Windows and
        # the mimetypes it returns on Mac OS X may not be playable.
        supported_codecs = self.media_player.supportedMimeTypes()
        for mime_type in supported_codecs:
            mime_type = str(mime_type)
            log.info(mime_type)
            if mime_type.startswith('audio/'):
                self._add_to_list(self.audio_extensions_list, mime_type)
            elif mime_type.startswith('video/'):
                self._add_to_list(self.video_extensions_list, mime_type)

    def _add_to_list(self, mime_type_list, mimetype):
        """
        Add mimetypes to the provided list
        """
        # Add all extensions which mimetypes provides us for supported types.
        extensions = mimetypes.guess_all_extensions(str(mimetype))
        for extension in extensions:
            ext = '*%s' % extension
            if ext not in mime_type_list:
                mime_type_list.append(ext)
        log.info('MediaPlugin: %s extensions: %s' % (mimetype, ' '.join(extensions)))

    def setup(self, display):
        """
        Set up the player widgets
        :param display:
        """
        display.video_widget = QtMultimediaWidgets.QVideoWidget(display)
        display.video_widget.resize(display.size())
        display.media_player = QtMultimedia.QMediaPlayer(display)
        display.media_player.setVideoOutput(display.video_widget)
        display.video_widget.raise_()
        display.video_widget.hide()
        self.has_own_widget = True

    def check_available(self):
        """
        Check if the player is available
        """
        return True

    def load(self, display):
        """
        Load a video into the display
        :param display:
        """
        log.debug('load vid in System Controller')
        controller = display.controller
        volume = controller.media_info.volume
        path = controller.media_info.file_info.absoluteFilePath()
        # Check if file is playable due to mimetype filters being nonexistent on Linux and Windows
        if self.check_media(path):
            display.media_player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(path)))
            self.volume(display, volume)
            return True
        else:
            return False

    def resize(self, display):
        """
        Resize the display
        :param display:
        """
        display.video_widget.resize(display.size())

    def play(self, display):
        """
        Play the current media item
        :param display:
        """
        log.info('Play the current item')
        controller = display.controller
        start_time = 0
        if display.media_player.state() != QtMultimedia.QMediaPlayer.PausedState and \
                controller.media_info.start_time > 0:
            start_time = controller.media_info.start_time
        display.media_player.play()
        if start_time > 0:
            self.seek(display, controller.media_info.start_time * 1000)
        self.volume(display, controller.media_info.volume)
        display.media_player.durationChanged.connect(functools.partial(self.set_duration, controller))
        self.state = MediaState.Playing
        display.video_widget.raise_()
        return True

    def pause(self, display):
        """
        Pause the current media item
        """
        display.media_player.pause()
        if display.media_player.state() == QtMultimedia.QMediaPlayer.PausedState:
            self.state = MediaState.Paused

    def stop(self, display):
        """
        Stop the current media item
        """
        display.media_player.blockSignals(True)
        display.media_player.durationChanged.disconnect()
        display.media_player.blockSignals(False)
        display.media_player.stop()
        self.set_visible(display, False)
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        """
        Set the volume
        """
        if display.has_audio:
            display.media_player.setVolume(vol)

    def seek(self, display, seek_value):
        """
        Go to a particular point in the current media item
        """
        display.media_player.setPosition(seek_value)

    def reset(self, display):
        """
        Reset the media player
        """
        display.media_player.stop()
        display.media_player.setMedia(QtMultimedia.QMediaContent())
        self.set_visible(display, False)
        display.video_widget.setVisible(False)
        self.state = MediaState.Off

    def set_visible(self, display, status):
        """
        Set the visibility of the widget
        """
        if self.has_own_widget:
            display.video_widget.setVisible(status)

    @staticmethod
    def set_duration(controller, duration):
        controller.media_info.length = int(duration / 1000)
        controller.seek_slider.setMaximum(controller.media_info.length * 1000)

    def update_ui(self, display):
        """
        Update the UI
        """
        if display.media_player.state() == QtMultimedia.QMediaPlayer.PausedState and self.state != MediaState.Paused:
            self.stop(display)
        controller = display.controller
        if controller.media_info.end_time > 0:
            if display.media_player.position() > controller.media_info.end_time * 1000:
                self.stop(display)
                self.set_visible(display, False)
        if not controller.seek_slider.isSliderDown():
            controller.seek_slider.blockSignals(True)
            controller.seek_slider.setSliderPosition(display.media_player.position())
            controller.seek_slider.blockSignals(False)

    def get_media_display_css(self):
        """
        Add css style sheets to htmlbuilder
        """
        return ''

    def get_info(self):
        """
        Return some info about this player
        """
        return (translate('Media.player', 'This media player uses your operating system '
                                          'to provide media capabilities.') +
                '<br/> <strong>' + translate('Media.player', 'Audio') +
                '</strong><br/>' + str(self.audio_extensions_list) +
                '<br/><strong>' + translate('Media.player', 'Video') +
                '</strong><br/>' + str(self.video_extensions_list) + '<br/>')

    def check_media(self, path):
        """
        Check if a file can be played
        Uses a separate QMediaPlayer in a thread

        :param path: Path to file to be checked
        :return: True if file can be played otherwise False
        """
        thread = QtCore.QThread()
        check_media_player = CheckMedia(path)
        check_media_player.setVolume(0)
        check_media_player.moveToThread(thread)
        check_media_player.finished.connect(thread.quit)
        thread.started.connect(check_media_player.play)
        thread.start()
        while thread.isRunning():
            self.application.processEvents()
        return check_media_player.result


class CheckMedia(QtMultimedia.QMediaPlayer):
    """
    Class used to check if a media file is playable
    """
    finished = QtCore.pyqtSignal()

    def __init__(self, path):
        super(CheckMedia, self).__init__(None, QtMultimedia.QMediaPlayer.VideoSurface)
        self.result = None

        self.error.connect(functools.partial(self.signals, 'error'))
        self.mediaStatusChanged.connect(functools.partial(self.signals, 'media'))

        self.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(path)))

    def signals(self, origin, status):
        if origin == 'media' and status == self.BufferedMedia:
            self.result = True
            self.stop()
            self.finished.emit()
        elif origin == 'error' and status != self.NoError:
            self.result = False
            self.stop()
            self.finished.emit()
