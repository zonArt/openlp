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


from PyQt4 import QtCore, QtGui
from openlp.core.common import translate


class Ui_MediaClipSelector(object):
    def setupUi(self, MediaClipSelector):
        MediaClipSelector.setObjectName("MediaClipSelector")
        MediaClipSelector.resize(683, 739)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MediaClipSelector.sizePolicy().hasHeightForWidth())
        MediaClipSelector.setSizePolicy(sizePolicy)
        MediaClipSelector.setMinimumSize(QtCore.QSize(683, 686))
        MediaClipSelector.setFocusPolicy(QtCore.Qt.NoFocus)
        MediaClipSelector.setAutoFillBackground(False)
        MediaClipSelector.setInputMethodHints(QtCore.Qt.ImhNone)
        self.centralwidget = QtGui.QWidget(MediaClipSelector)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.media_path_combobox = QtGui.QComboBox(self.centralwidget)
        self.media_path_combobox.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.media_path_combobox.sizePolicy().hasHeightForWidth())
        self.media_path_combobox.setSizePolicy(sizePolicy)
        self.media_path_combobox.setEditable(True)
        self.media_path_combobox.setObjectName("media_path_combobox")
        self.gridLayout.addWidget(self.media_path_combobox, 0, 2, 1, 2)
        self.start_timeedit = QtGui.QTimeEdit(self.centralwidget)
        self.start_timeedit.setEnabled(True)
        self.start_timeedit.setObjectName("start_timeedit")
        self.gridLayout.addWidget(self.start_timeedit, 7, 2, 1, 1)
        self.end_timeedit = QtGui.QTimeEdit(self.centralwidget)
        self.end_timeedit.setEnabled(True)
        self.end_timeedit.setObjectName("end_timeedit")
        self.gridLayout.addWidget(self.end_timeedit, 8, 2, 1, 1)
        self.set_start_pushbutton = QtGui.QPushButton(self.centralwidget)
        self.set_start_pushbutton.setEnabled(True)
        self.set_start_pushbutton.setObjectName("set_start_pushbutton")
        self.gridLayout.addWidget(self.set_start_pushbutton, 7, 3, 1, 1)
        self.load_disc_pushbutton = QtGui.QPushButton(self.centralwidget)
        self.load_disc_pushbutton.setEnabled(True)
        self.load_disc_pushbutton.setObjectName("load_disc_pushbutton")
        self.gridLayout.addWidget(self.load_disc_pushbutton, 0, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 9, 3, 1, 1)
        self.play_pushbutton = QtGui.QPushButton(self.centralwidget)
        self.play_pushbutton.setEnabled(True)
        self.play_pushbutton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/slides/media_playback_start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pushbutton.setIcon(icon)
        self.play_pushbutton.setObjectName("play_pushbutton")
        self.gridLayout.addWidget(self.play_pushbutton, 6, 0, 1, 1)
        self.end_point_label = QtGui.QLabel(self.centralwidget)
        self.end_point_label.setEnabled(True)
        self.end_point_label.setObjectName("end_point_label")
        self.gridLayout.addWidget(self.end_point_label, 8, 0, 1, 1)
        self.subtitle_tracks_combobox = QtGui.QComboBox(self.centralwidget)
        self.subtitle_tracks_combobox.setEnabled(True)
        self.subtitle_tracks_combobox.setObjectName("subtitle_tracks_combobox")
        self.gridLayout.addWidget(self.subtitle_tracks_combobox, 4, 2, 1, 2)
        self.title_label = QtGui.QLabel(self.centralwidget)
        self.title_label.setEnabled(True)
        self.title_label.setObjectName("title_label")
        self.gridLayout.addWidget(self.title_label, 2, 0, 1, 1)
        self.audio_tracks_combobox = QtGui.QComboBox(self.centralwidget)
        self.audio_tracks_combobox.setEnabled(True)
        self.audio_tracks_combobox.setObjectName("audio_tracks_combobox")
        self.gridLayout.addWidget(self.audio_tracks_combobox, 3, 2, 1, 2)
        self.set_end_pushbutton = QtGui.QPushButton(self.centralwidget)
        self.set_end_pushbutton.setEnabled(True)
        self.set_end_pushbutton.setObjectName("set_end_pushbutton")
        self.gridLayout.addWidget(self.set_end_pushbutton, 8, 3, 1, 1)
        self.save_pushbutton = QtGui.QPushButton(self.centralwidget)
        self.save_pushbutton.setEnabled(True)
        self.save_pushbutton.setObjectName("save_pushbutton")
        self.gridLayout.addWidget(self.save_pushbutton, 10, 3, 1, 1)
        self.close_pushbutton = QtGui.QPushButton(self.centralwidget)
        self.close_pushbutton.setEnabled(True)
        self.close_pushbutton.setObjectName("close_pushbutton")
        self.gridLayout.addWidget(self.close_pushbutton, 10, 4, 1, 1)
        self.start_point_label = QtGui.QLabel(self.centralwidget)
        self.start_point_label.setEnabled(True)
        self.start_point_label.setObjectName("start_point_label")
        self.gridLayout.addWidget(self.start_point_label, 7, 0, 1, 2)
        self.jump_start_pushbutton = QtGui.QPushButton(self.centralwidget)
        self.jump_start_pushbutton.setEnabled(True)
        self.jump_start_pushbutton.setObjectName("jump_start_pushbutton")
        self.gridLayout.addWidget(self.jump_start_pushbutton, 7, 4, 1, 1)
        self.audio_track_label = QtGui.QLabel(self.centralwidget)
        self.audio_track_label.setEnabled(True)
        self.audio_track_label.setObjectName("audio_track_label")
        self.gridLayout.addWidget(self.audio_track_label, 3, 0, 1, 2)
        self.media_position_timeedit = QtGui.QTimeEdit(self.centralwidget)
        self.media_position_timeedit.setEnabled(True)
        self.media_position_timeedit.setReadOnly(True)
        self.media_position_timeedit.setObjectName("media_position_timeedit")
        self.gridLayout.addWidget(self.media_position_timeedit, 6, 4, 1, 1)
        self.media_view_frame = QtGui.QFrame(self.centralwidget)
        self.media_view_frame.setMinimumSize(QtCore.QSize(665, 375))
        self.media_view_frame.setStyleSheet("background-color:black;")
        self.media_view_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.media_view_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.media_view_frame.setObjectName("media_view_frame")
        self.gridLayout.addWidget(self.media_view_frame, 5, 0, 1, 5)
        self.subtitle_track_label = QtGui.QLabel(self.centralwidget)
        self.subtitle_track_label.setEnabled(True)
        self.subtitle_track_label.setObjectName("subtitle_track_label")
        self.gridLayout.addWidget(self.subtitle_track_label, 4, 0, 1, 2)
        self.jump_end_pushbutton = QtGui.QPushButton(self.centralwidget)
        self.jump_end_pushbutton.setEnabled(True)
        self.jump_end_pushbutton.setObjectName("jump_end_pushbutton")
        self.gridLayout.addWidget(self.jump_end_pushbutton, 8, 4, 1, 1)
        self.media_path_label = QtGui.QLabel(self.centralwidget)
        self.media_path_label.setEnabled(True)
        self.media_path_label.setObjectName("media_path_label")
        self.gridLayout.addWidget(self.media_path_label, 0, 0, 1, 2)
        self.title_combo_box = QtGui.QComboBox(self.centralwidget)
        self.title_combo_box.setEnabled(True)
        self.title_combo_box.setProperty("currentText", "")
        self.title_combo_box.setObjectName("title_combo_box")
        self.gridLayout.addWidget(self.title_combo_box, 2, 2, 1, 2)
        self.position_horizontalslider = QtGui.QSlider(self.centralwidget)
        self.position_horizontalslider.setEnabled(True)
        self.position_horizontalslider.setTracking(False)
        self.position_horizontalslider.setOrientation(QtCore.Qt.Horizontal)
        self.position_horizontalslider.setInvertedAppearance(False)
        self.position_horizontalslider.setObjectName("position_horizontalslider")
        self.gridLayout.addWidget(self.position_horizontalslider, 6, 1, 1, 3)
        self.retranslateUi(MediaClipSelector)
        #QtCore.QMetaObject.connectSlotsByName(MediaClipSelector)
        MediaClipSelector.setTabOrder(self.media_path_combobox, self.load_disc_pushbutton)
        MediaClipSelector.setTabOrder(self.load_disc_pushbutton, self.title_combo_box)
        MediaClipSelector.setTabOrder(self.title_combo_box, self.audio_tracks_combobox)
        MediaClipSelector.setTabOrder(self.audio_tracks_combobox, self.subtitle_tracks_combobox)
        MediaClipSelector.setTabOrder(self.subtitle_tracks_combobox, self.play_pushbutton)
        MediaClipSelector.setTabOrder(self.play_pushbutton, self.position_horizontalslider)
        MediaClipSelector.setTabOrder(self.position_horizontalslider, self.media_position_timeedit)
        MediaClipSelector.setTabOrder(self.media_position_timeedit, self.start_timeedit)
        MediaClipSelector.setTabOrder(self.start_timeedit, self.set_start_pushbutton)
        MediaClipSelector.setTabOrder(self.set_start_pushbutton, self.jump_start_pushbutton)
        MediaClipSelector.setTabOrder(self.jump_start_pushbutton, self.end_timeedit)
        MediaClipSelector.setTabOrder(self.end_timeedit, self.set_end_pushbutton)
        MediaClipSelector.setTabOrder(self.set_end_pushbutton, self.jump_end_pushbutton)
        MediaClipSelector.setTabOrder(self.jump_end_pushbutton, self.save_pushbutton)
        MediaClipSelector.setTabOrder(self.save_pushbutton, self.close_pushbutton)

    def retranslateUi(self, MediaClipSelector):
        MediaClipSelector.setWindowTitle(translate("MediaPlugin.MediaClipSelector", "Select media clip", None))
        self.start_timeedit.setDisplayFormat(translate("MediaPlugin.MediaClipSelector", "HH:mm:ss.z", None))
        self.end_timeedit.setDisplayFormat(translate("MediaPlugin.MediaClipSelector", "HH:mm:ss.z", None))
        self.set_start_pushbutton.setText(translate("MediaPlugin.MediaClipSelector",
                                                    "Set current position as start point", None))
        self.load_disc_pushbutton.setText(translate("MediaPlugin.MediaClipSelector", "Load disc", None))
        self.end_point_label.setText(translate("MediaPlugin.MediaClipSelector", "End point", None))
        self.title_label.setText(translate("MediaPlugin.MediaClipSelector", "Title", None))
        self.set_end_pushbutton.setText(translate("MediaPlugin.MediaClipSelector",
                                                  "Set current position as end point", None))
        self.save_pushbutton.setText(translate("MediaPlugin.MediaClipSelector", "Save current clip", None))
        self.close_pushbutton.setText(translate("MediaPlugin.MediaClipSelector", "Close", None))
        self.start_point_label.setText(translate("MediaPlugin.MediaClipSelector", "Start point", None))
        self.jump_start_pushbutton.setText(translate("MediaPlugin.MediaClipSelector", "Jump to start point", None))
        self.audio_track_label.setText(translate("MediaPlugin.MediaClipSelector", "Audio track", None))
        self.media_position_timeedit.setDisplayFormat(translate("MediaPlugin.MediaClipSelector", "HH:mm:ss.z", None))
        self.subtitle_track_label.setText(translate("MediaPlugin.MediaClipSelector", "Subtitle track", None))
        self.jump_end_pushbutton.setText(translate("MediaPlugin.MediaClipSelector", "Jump to end point", None))
        self.media_path_label.setText(translate("MediaPlugin.MediaClipSelector", "Media path", None))
        self.media_path_combobox.lineEdit().setPlaceholderText(translate("MediaPlugin.MediaClipSelector",
                                                                         "Select drive from list", None))
