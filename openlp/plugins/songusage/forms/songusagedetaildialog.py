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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import build_icon, translate
from openlp.core.lib.ui import create_button_box


class Ui_SongUsageDetailDialog(object):
    def setupUi(self, songUsageDetailDialog):
        songUsageDetailDialog.setObjectName(u'songUsageDetailDialog')
        songUsageDetailDialog.resize(609, 413)
        self.vertical_layout = QtGui.QVBoxLayout(songUsageDetailDialog)
        self.vertical_layout.setSpacing(8)
        self.vertical_layout.setContentsMargins(8, 8, 8, 8)
        self.vertical_layout.setObjectName(u'vertical_layout')
        self.date_range_group_box = QtGui.QGroupBox(songUsageDetailDialog)
        self.date_range_group_box.setObjectName(u'date_range_group_box')
        self.date_horizontal_layout = QtGui.QHBoxLayout(self.date_range_group_box)
        self.date_horizontal_layout.setSpacing(8)
        self.date_horizontal_layout.setContentsMargins(8, 8, 8, 8)
        self.date_horizontal_layout.setObjectName(u'date_horizontal_layout')
        self.from_date = QtGui.QCalendarWidget(self.date_range_group_box)
        self.from_date.setObjectName(u'from_date')
        self.date_horizontal_layout.addWidget(self.from_date)
        self.to_label = QtGui.QLabel(self.date_range_group_box)
        self.to_label.setScaledContents(False)
        self.to_label.setAlignment(QtCore.Qt.AlignCenter)
        self.to_label.setObjectName(u'to_label')
        self.date_horizontal_layout.addWidget(self.to_label)
        self.to_date = QtGui.QCalendarWidget(self.date_range_group_box)
        self.to_date.setObjectName(u'to_date')
        self.date_horizontal_layout.addWidget(self.to_date)
        self.vertical_layout.addWidget(self.date_range_group_box)
        self.file_group_box = QtGui.QGroupBox(self.date_range_group_box)
        self.file_group_box.setObjectName(u'file_group_box')
        self.file_horizontal_layout = QtGui.QHBoxLayout(self.file_group_box)
        self.file_horizontal_layout.setSpacing(8)
        self.file_horizontal_layout.setContentsMargins(8, 8, 8, 8)
        self.file_horizontal_layout.setObjectName(u'file_horizontal_layout')
        self.file_line_edit = QtGui.QLineEdit(self.file_group_box)
        self.file_line_edit.setObjectName(u'file_line_edit')
        self.file_line_edit.setReadOnly(True)
        self.file_horizontal_layout.addWidget(self.file_line_edit)
        self.save_file_push_button = QtGui.QPushButton(self.file_group_box)
        self.save_file_push_button.setMaximumWidth(self.save_file_push_button.size().height())
        self.save_file_push_button.setIcon(build_icon(u':/general/general_open.png'))
        self.save_file_push_button.setObjectName(u'save_file_push_button')
        self.file_horizontal_layout.addWidget(self.save_file_push_button)
        self.vertical_layout.addWidget(self.file_group_box)
        self.button_box = create_button_box(songUsageDetailDialog, u'button_box', [u'cancel', u'ok'])
        self.vertical_layout.addWidget(self.button_box)
        self.retranslateUi(songUsageDetailDialog)
        self.save_file_push_button.clicked.connect(songUsageDetailDialog.define_output_location)

    def retranslateUi(self, songUsageDetailDialog):
        songUsageDetailDialog.setWindowTitle(translate('SongUsagePlugin.SongUsageDetailForm', 'Song Usage Extraction'))
        self.date_range_group_box.setTitle(translate('SongUsagePlugin.SongUsageDetailForm', 'Select Date Range'))
        self.to_label.setText(translate('SongUsagePlugin.SongUsageDetailForm', 'to'))
        self.file_group_box.setTitle(translate('SongUsagePlugin.SongUsageDetailForm', 'Report Location'))
