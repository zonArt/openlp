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
Package to test the openlp.core.ui.media.systemplayer package.
"""
from unittest import TestCase

from PyQt5 import QtCore, QtMultimedia

from openlp.core.common import Registry
from openlp.core.ui.media import MediaState
from openlp.core.ui.media.systemplayer import SystemPlayer, CheckMediaWorker, ADDITIONAL_EXT

from tests.functional import MagicMock, call, patch


class TestSystemPlayer(TestCase):
    """
    Test the system media player
    """
    @patch('openlp.core.ui.media.systemplayer.mimetypes')
    @patch('openlp.core.ui.media.systemplayer.QtMultimedia.QMediaPlayer')
    def test_constructor(self, MockQMediaPlayer, mocked_mimetypes):
        """
        Test the SystemPlayer constructor
        """
        # GIVEN: The SystemPlayer class and a mockedQMediaPlayer
        mocked_media_player = MagicMock()
        mocked_media_player.supportedMimeTypes.return_value = [
            'application/postscript',
            'audio/aiff',
            'audio/x-aiff',
            'text/html',
            'video/animaflex',
            'video/x-ms-asf'
        ]
        mocked_mimetypes.guess_all_extensions.side_effect = [
            ['.aiff'],
            ['.aiff'],
            ['.afl'],
            ['.asf']
        ]
        MockQMediaPlayer.return_value = mocked_media_player

        # WHEN: An object is created from it
        player = SystemPlayer(self)

        # THEN: The correct initial values should be set up
        self.assertEqual('system', player.name)
        self.assertEqual('System', player.original_name)
        self.assertEqual('&System', player.display_name)
        self.assertEqual(self, player.parent)
        self.assertEqual(ADDITIONAL_EXT, player.additional_extensions)
        MockQMediaPlayer.assert_called_once_with(None, QtMultimedia.QMediaPlayer.VideoSurface)
        mocked_mimetypes.init.assert_called_once_with()
        mocked_media_player.service.assert_called_once_with()
        mocked_media_player.supportedMimeTypes.assert_called_once_with()
        self.assertEqual(['*.aiff'], player.audio_extensions_list)
        self.assertEqual(['*.afl', '*.asf'], player.video_extensions_list)

    @patch('openlp.core.ui.media.systemplayer.QtMultimediaWidgets.QVideoWidget')
    @patch('openlp.core.ui.media.systemplayer.QtMultimedia.QMediaPlayer')
    def test_setup(self, MockQMediaPlayer, MockQVideoWidget):
        """
        Test the setup() method of SystemPlayer
        """
        # GIVEN: A SystemPlayer instance and a mock display
        player = SystemPlayer(self)
        mocked_display = MagicMock()
        mocked_display.size.return_value = [1, 2, 3, 4]
        mocked_video_widget = MagicMock()
        mocked_media_player = MagicMock()
        MockQVideoWidget.return_value = mocked_video_widget
        MockQMediaPlayer.return_value = mocked_media_player

        # WHEN: setup() is run
        player.setup(mocked_display)

        # THEN: The player should have a display widget
        MockQVideoWidget.assert_called_once_with(mocked_display)
        self.assertEqual(mocked_video_widget, mocked_display.video_widget)
        mocked_display.size.assert_called_once_with()
        mocked_video_widget.resize.assert_called_once_with([1, 2, 3, 4])
        MockQMediaPlayer.assert_called_with(mocked_display)
        self.assertEqual(mocked_media_player, mocked_display.media_player)
        mocked_media_player.setVideoOutput.assert_called_once_with(mocked_video_widget)
        mocked_video_widget.raise_.assert_called_once_with()
        mocked_video_widget.hide.assert_called_once_with()
        self.assertTrue(player.has_own_widget)

    def test_disconnect_slots(self):
        """
        Test that we the disconnect slots method catches the TypeError
        """
        # GIVEN: A SystemPlayer class and a signal that throws a TypeError
        player = SystemPlayer(self)
        mocked_signal = MagicMock()
        mocked_signal.disconnect.side_effect = \
            TypeError('disconnect() failed between \'durationChanged\' and all its connections')

        # WHEN: disconnect_slots() is called
        player.disconnect_slots(mocked_signal)

        # THEN: disconnect should have been called and the exception should have been ignored
        mocked_signal.disconnect.assert_called_once_with()

    def test_check_available(self):
        """
        Test the check_available() method on SystemPlayer
        """
        # GIVEN: A SystemPlayer instance
        player = SystemPlayer(self)

        # WHEN: check_available is run
        result = player.check_available()

        # THEN: it should be available
        self.assertTrue(result)

    def test_load_valid_media(self):
        """
        Test the load() method of SystemPlayer with a valid media file
        """
        # GIVEN: A SystemPlayer instance and a mocked display
        player = SystemPlayer(self)
        mocked_display = MagicMock()
        mocked_display.controller.media_info.volume = 1
        mocked_display.controller.media_info.file_info.absoluteFilePath.return_value = '/path/to/file'

        # WHEN: The load() method is run
        with patch.object(player, 'check_media') as mocked_check_media, \
                patch.object(player, 'volume') as mocked_volume:
            mocked_check_media.return_value = True
            result = player.load(mocked_display)

        # THEN: the file is sent to the video widget
        mocked_display.controller.media_info.file_info.absoluteFilePath.assert_called_once_with()
        mocked_check_media.assert_called_once_with('/path/to/file')
        mocked_display.media_player.setMedia.assert_called_once_with(
            QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile('/path/to/file')))
        mocked_volume.assert_called_once_with(mocked_display, 1)
        self.assertTrue(result)

    def test_load_invalid_media(self):
        """
        Test the load() method of SystemPlayer with an invalid media file
        """
        # GIVEN: A SystemPlayer instance and a mocked display
        player = SystemPlayer(self)
        mocked_display = MagicMock()
        mocked_display.controller.media_info.volume = 1
        mocked_display.controller.media_info.file_info.absoluteFilePath.return_value = '/path/to/file'

        # WHEN: The load() method is run
        with patch.object(player, 'check_media') as mocked_check_media, \
                patch.object(player, 'volume') as mocked_volume:
            mocked_check_media.return_value = False
            result = player.load(mocked_display)

        # THEN: stuff
        mocked_display.controller.media_info.file_info.absoluteFilePath.assert_called_once_with()
        mocked_check_media.assert_called_once_with('/path/to/file')
        self.assertFalse(result)

    def test_resize(self):
        """
        Test the resize() method of the SystemPlayer
        """
        # GIVEN: A SystemPlayer instance and a mocked display
        player = SystemPlayer(self)
        mocked_display = MagicMock()
        mocked_display.size.return_value = [1, 2, 3, 4]

        # WHEN: The resize() method is called
        player.resize(mocked_display)

        # THEN: The player is resized
        mocked_display.size.assert_called_once_with()
        mocked_display.video_widget.resize.assert_called_once_with([1, 2, 3, 4])

    @patch('openlp.core.ui.media.systemplayer.functools')
    def test_play_is_live(self, mocked_functools):
        """
        Test the play() method of the SystemPlayer on the live display
        """
        # GIVEN: A SystemPlayer instance and a mocked display
        mocked_functools.partial.return_value = 'function'
        player = SystemPlayer(self)
        mocked_display = MagicMock()
        mocked_display.controller.is_live = True
        mocked_display.controller.media_info.start_time = 1
        mocked_display.controller.media_info.volume = 1

        # WHEN: play() is called
        with patch.object(player, 'get_live_state') as mocked_get_live_state, \
                patch.object(player, 'seek') as mocked_seek, \
                patch.object(player, 'volume') as mocked_volume, \
                patch.object(player, 'set_state') as mocked_set_state, \
                patch.object(player, 'disconnect_slots') as mocked_disconnect_slots:
            mocked_get_live_state.return_value = QtMultimedia.QMediaPlayer.PlayingState
            result = player.play(mocked_display)

        # THEN: the media file is played
        mocked_get_live_state.assert_called_once_with()
        mocked_display.media_player.play.assert_called_once_with()
        mocked_seek.assert_called_once_with(mocked_display, 1000)
        mocked_volume.assert_called_once_with(mocked_display, 1)
        mocked_disconnect_slots.assert_called_once_with(mocked_display.media_player.durationChanged)
        mocked_display.media_player.durationChanged.connect.assert_called_once_with('function')
        mocked_set_state.assert_called_once_with(MediaState.Playing, mocked_display)
        mocked_display.video_widget.raise_.assert_called_once_with()
        self.assertTrue(result)

    @patch('openlp.core.ui.media.systemplayer.functools')
    def test_play_is_preview(self, mocked_functools):
        """
        Test the play() method of the SystemPlayer on the preview display
        """
        # GIVEN: A SystemPlayer instance and a mocked display
        mocked_functools.partial.return_value = 'function'
        player = SystemPlayer(self)
        mocked_display = MagicMock()
        mocked_display.controller.is_live = False
        mocked_display.controller.media_info.start_time = 1
        mocked_display.controller.media_info.volume = 1

        # WHEN: play() is called
        with patch.object(player, 'get_preview_state') as mocked_get_preview_state, \
                patch.object(player, 'seek') as mocked_seek, \
                patch.object(player, 'volume') as mocked_volume, \
                patch.object(player, 'set_state') as mocked_set_state:
            mocked_get_preview_state.return_value = QtMultimedia.QMediaPlayer.PlayingState
            result = player.play(mocked_display)

        # THEN: the media file is played
        mocked_get_preview_state.assert_called_once_with()
        mocked_display.media_player.play.assert_called_once_with()
        mocked_seek.assert_called_once_with(mocked_display, 1000)
        mocked_volume.assert_called_once_with(mocked_display, 1)
        mocked_display.media_player.durationChanged.connect.assert_called_once_with('function')
        mocked_set_state.assert_called_once_with(MediaState.Playing, mocked_display)
        mocked_display.video_widget.raise_.assert_called_once_with()
        self.assertTrue(result)

    def test_pause_is_live(self):
        """
        Test the pause() method of the SystemPlayer on the live display
        """
        # GIVEN: A SystemPlayer instance
        player = SystemPlayer(self)
        mocked_display = MagicMock()
        mocked_display.controller.is_live = True

        # WHEN: The pause method is called
        with patch.object(player, 'get_live_state') as mocked_get_live_state, \
                patch.object(player, 'set_state') as mocked_set_state:
            mocked_get_live_state.return_value = QtMultimedia.QMediaPlayer.PausedState
            player.pause(mocked_display)

        # THEN: The video is paused
        mocked_display.media_player.pause.assert_called_once_with()
        mocked_get_live_state.assert_called_once_with()
        mocked_set_state.assert_called_once_with(MediaState.Paused, mocked_display)

    def test_pause_is_preview(self):
        """
        Test the pause() method of the SystemPlayer on the preview display
        """
        # GIVEN: A SystemPlayer instance
        player = SystemPlayer(self)
        mocked_display = MagicMock()
        mocked_display.controller.is_live = False

        # WHEN: The pause method is called
        with patch.object(player, 'get_preview_state') as mocked_get_preview_state, \
                patch.object(player, 'set_state') as mocked_set_state:
            mocked_get_preview_state.return_value = QtMultimedia.QMediaPlayer.PausedState
            player.pause(mocked_display)

        # THEN: The video is paused
        mocked_display.media_player.pause.assert_called_once_with()
        mocked_get_preview_state.assert_called_once_with()
        mocked_set_state.assert_called_once_with(MediaState.Paused, mocked_display)

    def test_stop(self):
        """
        Test the stop() method of the SystemPlayer
        """
        # GIVEN: A SystemPlayer instance
        player = SystemPlayer(self)
        mocked_display = MagicMock()

        # WHEN: The stop method is called
        with patch.object(player, 'set_visible') as mocked_set_visible, \
                patch.object(player, 'set_state') as mocked_set_state:
            player.stop(mocked_display)

        # THEN: The video is stopped
        mocked_display.media_player.stop.assert_called_once_with()
        mocked_set_visible.assert_called_once_with(mocked_display, False)
        mocked_set_state.assert_called_once_with(MediaState.Stopped, mocked_display)

    def test_volume(self):
        """
        Test the volume() method of the SystemPlayer
        """
        # GIVEN: A SystemPlayer instance
        player = SystemPlayer(self)
        mocked_display = MagicMock()
        mocked_display.has_audio = True

        # WHEN: The stop method is called
        player.volume(mocked_display, 2)

        # THEN: The video is stopped
        mocked_display.media_player.setVolume.assert_called_once_with(2)

    def test_seek(self):
        """
        Test the seek() method of the SystemPlayer
        """
        # GIVEN: A SystemPlayer instance
        player = SystemPlayer(self)
        mocked_display = MagicMock()

        # WHEN: The stop method is called
        player.seek(mocked_display, 2)

        # THEN: The video is stopped
        mocked_display.media_player.setPosition.assert_called_once_with(2)

    def test_reset(self):
        """
        Test the reset() method of the SystemPlayer
        """
        # GIVEN: A SystemPlayer instance
        player = SystemPlayer(self)
        mocked_display = MagicMock()

        # WHEN: reset() is called
        with patch.object(player, 'set_state') as mocked_set_state, \
                patch.object(player, 'set_visible') as mocked_set_visible:
            player.reset(mocked_display)

        # THEN: The media player is reset
        mocked_display.media_player.stop()
        mocked_display.media_player.setMedia.assert_called_once_with(QtMultimedia.QMediaContent())
        mocked_set_visible.assert_called_once_with(mocked_display, False)
        mocked_display.video_widget.setVisible.assert_called_once_with(False)
        mocked_set_state.assert_called_once_with(MediaState.Off, mocked_display)

    def test_set_visible(self):
        """
        Test the set_visible() method on the SystemPlayer
        """
        # GIVEN: A SystemPlayer instance and a mocked display
        player = SystemPlayer(self)
        player.has_own_widget = True
        mocked_display = MagicMock()

        # WHEN: set_visible() is called
        player.set_visible(mocked_display, True)

        # THEN: The widget should be visible
        mocked_display.video_widget.setVisible.assert_called_once_with(True)

    def test_set_duration(self):
        """
        Test the set_duration() method of the SystemPlayer
        """
        # GIVEN: a mocked controller
        mocked_controller = MagicMock()
        mocked_controller.media_info.length = 5

        # WHEN: The set_duration() is called. NB: the 10 here is ignored by the code
        SystemPlayer.set_duration(mocked_controller, 10)

        # THEN: The maximum length of the slider should be set
        mocked_controller.seek_slider.setMaximum.assert_called_once_with(5)

    def test_update_ui(self):
        """
        Test the update_ui() method on the SystemPlayer
        """
        # GIVEN: A SystemPlayer instance
        player = SystemPlayer(self)
        player.state = MediaState.Playing
        mocked_display = MagicMock()
        mocked_display.media_player.state.return_value = QtMultimedia.QMediaPlayer.PausedState
        mocked_display.controller.media_info.end_time = 1
        mocked_display.media_player.position.return_value = 2
        mocked_display.controller.seek_slider.isSliderDown.return_value = False

        # WHEN: update_ui() is called
        with patch.object(player, 'stop') as mocked_stop, \
                patch.object(player, 'set_visible') as mocked_set_visible:
            player.update_ui(mocked_display)

        # THEN: The UI is updated
        expected_stop_calls = [call(mocked_display), call(mocked_display)]
        expected_position_calls = [call(), call()]
        expected_block_signals_calls = [call(True), call(False)]
        mocked_display.media_player.state.assert_called_once_with()
        self.assertEqual(2, mocked_stop.call_count)
        self.assertEqual(expected_stop_calls, mocked_stop.call_args_list)
        self.assertEqual(2, mocked_display.media_player.position.call_count)
        self.assertEqual(expected_position_calls, mocked_display.media_player.position.call_args_list)
        mocked_set_visible.assert_called_once_with(mocked_display, False)
        mocked_display.controller.seek_slider.isSliderDown.assert_called_once_with()
        self.assertEqual(expected_block_signals_calls,
                         mocked_display.controller.seek_slider.blockSignals.call_args_list)
        mocked_display.controller.seek_slider.setSliderPosition.assert_called_once_with(2)

    def test_get_media_display_css(self):
        """
        Test the get_media_display_css() method of the SystemPlayer
        """
        # GIVEN: A SystemPlayer instance
        player = SystemPlayer(self)

        # WHEN: get_media_display_css() is called
        result = player.get_media_display_css()

        # THEN: The css should be empty
        self.assertEqual('', result)

    def test_get_info(self):
        """
        Test the get_info() method of the SystemPlayer
        """
        # GIVEN: A SystemPlayer instance
        player = SystemPlayer(self)

        # WHEN: get_info() is called
        result = player.get_info()

        # THEN: The info should be correct
        expected_info = 'This media player uses your operating system to provide media capabilities.<br/> ' \
            '<strong>Audio</strong><br/>[]<br/><strong>Video</strong><br/>[]<br/>'
        self.assertEqual(expected_info, result)

    @patch('openlp.core.ui.media.systemplayer.CheckMediaWorker')
    @patch('openlp.core.ui.media.systemplayer.QtCore.QThread')
    def test_check_media(self, MockQThread, MockCheckMediaWorker):
        """
        Test the check_media() method of the SystemPlayer
        """
        # GIVEN: A SystemPlayer instance and a mocked thread
        valid_file = '/path/to/video.ogv'
        mocked_application = MagicMock()
        Registry().create()
        Registry().register('application', mocked_application)
        player = SystemPlayer(self)
        mocked_thread = MagicMock()
        mocked_thread.isRunning.side_effect = [True, False]
        mocked_thread.quit = 'quit'  # actually supposed to be a slot, but it's all mocked out anyway
        MockQThread.return_value = mocked_thread
        mocked_check_media_worker = MagicMock()
        mocked_check_media_worker.play = 'play'
        mocked_check_media_worker.result = True
        MockCheckMediaWorker.return_value = mocked_check_media_worker

        # WHEN: check_media() is called with a valid media file
        result = player.check_media(valid_file)

        # THEN: It should return True
        MockQThread.assert_called_once_with()
        MockCheckMediaWorker.assert_called_once_with(valid_file)
        mocked_check_media_worker.setVolume.assert_called_once_with(0)
        mocked_check_media_worker.moveToThread.assert_called_once_with(mocked_thread)
        mocked_check_media_worker.finished.connect.assert_called_once_with('quit')
        mocked_thread.started.connect.assert_called_once_with('play')
        mocked_thread.start.assert_called_once_with()
        self.assertEqual(2, mocked_thread.isRunning.call_count)
        mocked_application.processEvents.assert_called_once_with()
        self.assertTrue(result)


class TestCheckMediaWorker(TestCase):
    """
    Test the CheckMediaWorker class
    """
    def test_constructor(self):
        """
        Test the constructor of the CheckMediaWorker class
        """
        # GIVEN: A file path
        path = 'file.ogv'

        # WHEN: The CheckMediaWorker object is instantiated
        worker = CheckMediaWorker(path)

        # THEN: The correct values should be set up
        self.assertIsNotNone(worker)

    def test_signals_media(self):
        """
        Test the signals() signal of the CheckMediaWorker class with a "media" origin
        """
        # GIVEN: A CheckMediaWorker instance
        worker = CheckMediaWorker('file.ogv')

        # WHEN: signals() is called with media and BufferedMedia
        with patch.object(worker, 'stop') as mocked_stop, \
                patch.object(worker, 'finished') as mocked_finished:
            worker.signals('media', worker.BufferedMedia)

        # THEN: The worker should exit and the result should be True
        mocked_stop.assert_called_once_with()
        mocked_finished.emit.assert_called_once_with()
        self.assertTrue(worker.result)

    def test_signals_error(self):
        """
        Test the signals() signal of the CheckMediaWorker class with a "error" origin
        """
        # GIVEN: A CheckMediaWorker instance
        worker = CheckMediaWorker('file.ogv')

        # WHEN: signals() is called with error and BufferedMedia
        with patch.object(worker, 'stop') as mocked_stop, \
                patch.object(worker, 'finished') as mocked_finished:
            worker.signals('error', None)

        # THEN: The worker should exit and the result should be True
        mocked_stop.assert_called_once_with()
        mocked_finished.emit.assert_called_once_with()
        self.assertFalse(worker.result)
