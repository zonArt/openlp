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

import os
import sys
import logging
import time
from datetime import datetime


from PyQt4 import QtCore, QtGui

from openlp.plugins.media.forms.mediaclipselectordialog import Ui_MediaClipSelector
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui.media.vendor import vlc

log = logging.getLogger(__name__)


class MediaClipSelectorForm(QtGui.QDialog, Ui_MediaClipSelector):
    """
    Class to manage the clip selection
    """
    log.info('%s MediaClipSelectorForm loaded', __name__)

    def __init__(self, media_item, parent, manager):
        """
        Constructor
        """
        super(MediaClipSelectorForm, self).__init__(parent)
        self.media_item = media_item
        self.setupUi(self)
        self.playback_length = 0
        self.position_horizontalslider.setMinimum(0)
        self.disable_all()
        self.toggle_disable_load_media(False)
        # most actions auto-connect due to the functions name, so only a few left to do
        self.close_pushbutton.clicked.connect(self.reject)

    def reject(self):
        """
        Exit Dialog and do not save
        """
        log.debug('MediaClipSelectorForm.reject')
        self.vlc_media_player.stop()
        QtGui.QDialog.reject(self)

    def exec_(self):
        """
        Start dialog
        """
        self.setup_vlc()
        return QtGui.QDialog.exec_(self)

    def setup_vlc(self):
        """
        Setup VLC instance and mediaplayer
        """
        self.vlc_instance = vlc.Instance()
        # creating an empty vlc media player
        self.vlc_media_player = self.vlc_instance.media_player_new()
        # The media player has to be 'connected' to the QFrame.
        # (otherwise a video would be displayed in it's own window)
        # This is platform specific!
        # You have to give the id of the QFrame (or similar object)
        # to vlc, different platforms have different functions for this.
        win_id = int(self.media_view_frame.winId())
        if sys.platform == "win32":
            self.vlc_media_player.set_hwnd(win_id)
        elif sys.platform == "darwin":
            # We have to use 'set_nsobject' since Qt4 on OSX uses Cocoa
            # framework and not the old Carbon.
            self.vlc_media_player.set_nsobject(win_id)
        else:
            # for Linux using the X Server
            self.vlc_media_player.set_xwindow(win_id)
        self.vlc_media = None
        # Setup timer every 100 ms to update position
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(100)

    @QtCore.pyqtSlot(bool)
    def on_load_disc_pushbutton_clicked(self, clicked):
        """
        Load the media when the load-button has been clicked

        :param clicked: Given from signal, not used.
        """
        self.disable_all()
        path = self.media_path_combobox.currentText()
        if path == '':
            log.debug('no given path')
            critical_error_message_box('Error', 'No path was given')
            self.toggle_disable_load_media(False)
            return
        self.vlc_media = self.vlc_instance.media_new_path(path)
        if not self.vlc_media:
            log.debug('vlc media player is none')
            critical_error_message_box('Error', 'An error happened during initialization of VLC player')
            self.toggle_disable_load_media(False)
            return
        # put the media in the media player
        self.vlc_media_player.set_media(self.vlc_media)
        self.vlc_media_player.audio_set_mute(True)
        # start playback to get vlc to parse the media
        if self.vlc_media_player.play() < 0:
            log.debug('vlc play returned error')
            critical_error_message_box('Error', 'An error happen when starting VLC player')
            self.toggle_disable_load_media(False)
            return
        self.vlc_media_player.audio_set_mute(True)
        if not self.media_state_wait(vlc.State.Playing):
            return
        self.vlc_media_player.pause()
        self.vlc_media_player.set_time(0)
        # Get titles, insert in combobox
        titles = self.vlc_media_player.video_get_title_description()
        self.title_combo_box.clear()
        for title in titles:
            self.title_combo_box.addItem(title[1].decode(), title[0])
        # Main title is usually title #1
        if len(titles) > 1:
            self.title_combo_box.setCurrentIndex(1)
        else:
            self.title_combo_box.setCurrentIndex(0)
        # Enable audio track combobox if anything is in it
        if len(titles) > 0:
            self.title_combo_box.setDisabled(False)
        self.toggle_disable_load_media(False)

    @QtCore.pyqtSlot(bool)
    def on_pause_pushbutton_clicked(self, clicked):
        """
        Pause the playback

        :param clicked: Given from signal, not used.
        """
        self.vlc_media_player.pause()

    @QtCore.pyqtSlot(bool)
    def on_play_pushbutton_clicked(self, clicked):
        """
        Start the playback

        :param clicked: Given from signal, not used.
        """
        self.vlc_media_player.play()

    @QtCore.pyqtSlot(bool)
    def on_set_start_pushbutton_clicked(self, clicked):
        """
        Copy the current player position to start_timeedit

        :param clicked: Given from signal, not used.
        """
        vlc_ms_pos = self.vlc_media_player.get_time()
        time = QtCore.QTime()
        new_pos_time = time.addMSecs(vlc_ms_pos)
        self.start_timeedit.setTime(new_pos_time)
        # If start time is after end time, update end time.
        end_time = self.end_timeedit.time()
        if end_time < new_pos_time:
            self.end_timeedit.setTime(new_pos_time)

    @QtCore.pyqtSlot(bool)
    def on_set_end_pushbutton_clicked(self, clicked):
        """
        Copy the current player position to end_timeedit

        :param clicked: Given from signal, not used.
        """
        vlc_ms_pos = self.vlc_media_player.get_time()
        time = QtCore.QTime()
        new_pos_time = time.addMSecs(vlc_ms_pos)
        self.end_timeedit.setTime(new_pos_time)
        # If start time is after end time, update end time.
        start_time = self.start_timeedit.time()
        if start_time > new_pos_time:
            self.start_timeedit.setTime(new_pos_time)

    @QtCore.pyqtSlot(bool)
    def on_jump_end_pushbutton_clicked(self, clicked):
        """
        Set the player position to the position stored in end_timeedit

        :param clicked: Given from signal, not used.
        """
        end_time = self.end_timeedit.time()
        end_time_ms = end_time.hour() * 60 * 60 * 1000 + \
                      end_time.minute() * 60 * 1000 + \
                      end_time.second() * 1000 + \
                      end_time.msec()
        self.vlc_media_player.set_time(end_time_ms)

    @QtCore.pyqtSlot(bool)
    def on_jump_start_pushbutton_clicked(self, clicked):
        """
        Set the player position to the position stored in start_timeedit

        :param clicked: Given from signal, not used.
        """
        start_time = self.start_timeedit.time()
        start_time_ms = start_time.hour() * 60 * 60 * 1000 + \
                      start_time.minute() * 60 * 1000 + \
                      start_time.second() * 1000 + \
                      start_time.msec()
        self.vlc_media_player.set_time(start_time_ms)

    @QtCore.pyqtSlot(int)
    def on_title_combo_box_currentIndexChanged(self, index):
        """
        When a new title is chosen, it is loaded by VLC and info about audio and subtitle tracks is reloaded

        :param index: The index of the newly chosen title track.
        """
        log.debug('in on_title_combo_box_changed, index: ', str(index))
        self.vlc_media_player.set_title(index)
        self.vlc_media_player.set_time(0)
        self.vlc_media_player.play()
        self.vlc_media_player.audio_set_mute(True)
        if not self.media_state_wait(vlc.State.Playing):
            return
        # pause
        self.vlc_media_player.pause()
        self.vlc_media_player.set_time(0)
        # Get audio tracks, insert in combobox
        audio_tracks = self.vlc_media_player.audio_get_track_description()
        self.audio_tracks_combobox.clear()
        for audio_track in audio_tracks:
            self.audio_tracks_combobox.addItem(audio_track[1].decode(), audio_track[0])
        # Enable audio track combobox if anything is in it
        if len(audio_tracks) > 0:
            self.audio_tracks_combobox.setDisabled(False)
            # First track is "deactivated", so set to next if it exists
            if len(audio_tracks) > 1:
                self.audio_tracks_combobox.setCurrentIndex(1)
        # Get subtitle tracks, insert in combobox
        subtitles_tracks = self.vlc_media_player.video_get_spu_description()
        self.subtitle_tracks_combobox.clear()
        for subtitle_track in subtitles_tracks:
            self.subtitle_tracks_combobox.addItem(subtitle_track[1].decode(), subtitle_track[0])
        # Enable subtitle track combobox is anything in it
        if len(subtitles_tracks) > 0:
            self.subtitle_tracks_combobox.setDisabled(False)
            # First track is "deactivated", so set to next if it exists
            if len(subtitles_tracks) > 1:
                self.subtitle_tracks_combobox.setCurrentIndex(1)
        self.vlc_media_player.audio_set_mute(False)
        self.playback_length = self.vlc_media_player.get_length()
        self.position_horizontalslider.setMaximum(self.playback_length)
        # If a title or audio track is available the player is enabled
        if self.title_combo_box.count() > 0 or len(audio_tracks) > 0:
            self.toggle_disable_player(False)

    @QtCore.pyqtSlot(int)
    def on_audio_tracks_combobox_currentIndexChanged(self, index):
        """
        When a new audio track is chosen update audio track bing played by VLC

        :param index: The index of the newly chosen audio track.
        """
        audio_track = self.audio_tracks_combobox.itemData(index)
        log.debug('in on_audio_tracks_combobox_currentIndexChanged, index: ', str(index), ' audio_track: ', audio_track)
        if audio_track and int(audio_track) > 0:
            self.vlc_media_player.audio_set_track(int(audio_track))

    @QtCore.pyqtSlot(int)
    def on_subtitle_tracks_combobox_currentIndexChanged(self, index):
        """
        When a new subtitle track is chosen update subtitle track bing played by VLC

        :param index: The index of the newly chosen subtitle.
        """
        subtitle_track = self.subtitle_tracks_combobox.itemData(index)
        if subtitle_track:
            self.vlc_media_player.video_set_spu(int(subtitle_track))

    def on_position_horizontalslider_sliderMoved(self, position):
        """
        Set player position according to new slider position.

        :param position: Position to seek to.
        """
        self.vlc_media_player.set_time(position)

    def update_position(self):
        """
        Update slider position and displayed time according to VLC player position.
        """
        if self.vlc_media_player:
            vlc_ms_pos = self.vlc_media_player.get_time()
            rounded_vlc_ms_pos = int(round(vlc_ms_pos / 100.0) * 100.0)
            time = QtCore.QTime()
            new_pos_time = time.addMSecs(rounded_vlc_ms_pos)
            self.media_position_timeedit.setTime(new_pos_time)
            self.position_horizontalslider.setSliderPosition(vlc_ms_pos)

    def disable_all(self):
        """
        Disable all elements in the dialog
        """
        self.toggle_disable_load_media(True)
        self.title_combo_box.setDisabled(True)
        self.audio_tracks_combobox.setDisabled(True)
        self.subtitle_tracks_combobox.setDisabled(True)
        self.toggle_disable_player(True)

    def toggle_disable_load_media(self, action):
        """
        Enable/disable load media combobox and button.

        :param action: If True elements are disabled, if False they are enabled.
        """
        self.media_path_combobox.setDisabled(action)
        self.load_disc_pushbutton.setDisabled(action)

    def toggle_disable_player(self, action):
        """
        Enable/disable player elements.

        :param action: If True elements are disabled, if False they are enabled.
        """
        self.play_pushbutton.setDisabled(action)
        self.pause_pushbutton.setDisabled(action)
        self.position_horizontalslider.setDisabled(action)
        self.media_position_timeedit.setDisabled(action)
        self.start_timeedit.setDisabled(action)
        self.set_start_pushbutton.setDisabled(action)
        self.jump_start_pushbutton.setDisabled(action)
        self.end_timeedit.setDisabled(action)
        self.set_end_pushbutton.setDisabled(action)
        self.jump_end_pushbutton.setDisabled(action)
        self.preview_pushbutton.setDisabled(action)
        self.save_pushbutton.setDisabled(action)

    @QtCore.pyqtSlot(bool)
    def on_save_pushbutton_clicked(self, clicked):
        """
        Saves the current media and trackinfo as a clip to the mediamanager

        :param clicked: Given from signal, not used.
        """
        log.debug('in on_save_pushbutton_clicked')
        start_time = self.start_timeedit.time()
        start_time_ms = start_time.hour() * 60 * 60 * 1000 + \
                      start_time.minute() * 60 * 1000 + \
                      start_time.second() * 1000 + \
                      start_time.msec()
        end_time = self.end_timeedit.time()
        end_time_ms = end_time.hour() * 60 * 60 * 1000 + \
                      end_time.minute() * 60 * 1000 + \
                      end_time.second() * 1000 + \
                      end_time.msec()
        title = self.title_combo_box.itemData(self.title_combo_box.currentIndex())
        audio_track = self.audio_tracks_combobox.itemData(self.audio_tracks_combobox.currentIndex())
        subtitle_track = self.subtitle_tracks_combobox.itemData(self.subtitle_tracks_combobox.currentIndex())
        path = self.media_path_combobox.currentText()
        optical = 'optical:' + str(title) + ':' + str(audio_track) + ':' + str(subtitle_track) + ':' + str(
            start_time_ms) + ':' + str(end_time_ms) + ':' + path
        self.media_item.add_optical_clip(optical)

    def media_state_wait(self, media_state):
        """
        Wait for the video to change its state
        Wait no longer than 15 seconds. (loading an iso file needs a long time)

        :param media_state: VLC media state to wait for.
        :return: True if state was reached within 15 seconds, False if not or error occurred.
        """
        start = datetime.now()
        while not media_state == self.vlc_media.get_state():
            if self.vlc_media.get_state() == vlc.State.Error:
                return False
            if (datetime.now() - start).seconds > 15:
                return False
        return True
