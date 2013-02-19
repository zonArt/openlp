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
        self.verticalLayout = QtGui.QVBoxLayout(songUsageDetailDialog)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.dateRangeGroupBox = QtGui.QGroupBox(songUsageDetailDialog)
        self.dateRangeGroupBox.setObjectName(u'dateRangeGroupBox')
        self.dateHorizontalLayout = QtGui.QHBoxLayout(self.dateRangeGroupBox)
        self.dateHorizontalLayout.setSpacing(8)
        self.dateHorizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.dateHorizontalLayout.setObjectName(u'dateHorizontalLayout')
        self.fromDate = QtGui.QCalendarWidget(self.dateRangeGroupBox)
        self.fromDate.setObjectName(u'fromDate')
        self.dateHorizontalLayout.addWidget(self.fromDate)
        self.toLabel = QtGui.QLabel(self.dateRangeGroupBox)
        self.toLabel.setScaledContents(False)
        self.toLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.toLabel.setObjectName(u'toLabel')
        self.dateHorizontalLayout.addWidget(self.toLabel)
        self.toDate = QtGui.QCalendarWidget(self.dateRangeGroupBox)
        self.toDate.setObjectName(u'toDate')
        self.dateHorizontalLayout.addWidget(self.toDate)
        self.verticalLayout.addWidget(self.dateRangeGroupBox)
        self.fileGroupBox = QtGui.QGroupBox(self.dateRangeGroupBox)
        self.fileGroupBox.setObjectName(u'fileGroupBox')
        self.fileHorizontalLayout = QtGui.QHBoxLayout(self.fileGroupBox)
        self.fileHorizontalLayout.setSpacing(8)
        self.fileHorizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.fileHorizontalLayout.setObjectName(u'fileHorizontalLayout')
        self.fileLineEdit = QtGui.QLineEdit(self.fileGroupBox)
        self.fileLineEdit.setObjectName(u'fileLineEdit')
        self.fileLineEdit.setReadOnly(True)
        self.fileHorizontalLayout.addWidget(self.fileLineEdit)
        self.saveFilePushButton = QtGui.QPushButton(self.fileGroupBox)
        self.saveFilePushButton.setMaximumWidth(self.saveFilePushButton.size().height())
        self.saveFilePushButton.setIcon(build_icon(u':/general/general_open.png'))
        self.saveFilePushButton.setObjectName(u'saveFilePushButton')
        self.fileHorizontalLayout.addWidget(self.saveFilePushButton)
        self.verticalLayout.addWidget(self.fileGroupBox)
        self.button_box = create_button_box(songUsageDetailDialog, u'button_box', [u'cancel', u'ok'])
        self.verticalLayout.addWidget(self.button_box)
        self.retranslateUi(songUsageDetailDialog)
        QtCore.QObject.connect(self.saveFilePushButton, QtCore.SIGNAL(u'clicked()'),
            songUsageDetailDialog.defineOutputLocation)

    def retranslateUi(self, songUsageDetailDialog):
        songUsageDetailDialog.setWindowTitle(translate('SongUsagePlugin.SongUsageDetailForm', 'Song Usage Extraction'))
        self.dateRangeGroupBox.setTitle(translate('SongUsagePlugin.SongUsageDetailForm', 'Select Date Range'))
        self.toLabel.setText(translate('SongUsagePlugin.SongUsageDetailForm', 'to'))
        self.fileGroupBox.setTitle(translate('SongUsagePlugin.SongUsageDetailForm', 'Report Location'))
