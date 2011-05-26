# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Jeffrey Smith, Maikel            #
# Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund                    #
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
from openlp.core.lib.ui import create_accept_reject_button_box

class Ui_SongUsageDetailDialog(object):
    def setupUi(self, songUsageDetailDialog):
        songUsageDetailDialog.setObjectName(u'songUsageDetailDialog')
        songUsageDetailDialog.resize(609, 413)
        self.verticalLayout = QtGui.QVBoxLayout(songUsageDetailDialog)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.dateRangeGroupBox = QtGui.QGroupBox(songUsageDetailDialog)
        self.dateRangeGroupBox.setObjectName(u'dateRangeGroupBox')
        self.verticalLayout2 = QtGui.QVBoxLayout(self.dateRangeGroupBox)
        self.verticalLayout2.setObjectName(u'verticalLayout2')
        self.dateHorizontalLayout = QtGui.QHBoxLayout()
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
        self.verticalLayout2.addLayout(self.dateHorizontalLayout)
        self.fileGroupBox = QtGui.QGroupBox(self.dateRangeGroupBox)
        self.fileGroupBox.setObjectName(u'fileGroupBox')
        self.verticalLayout4 = QtGui.QVBoxLayout(self.fileGroupBox)
        self.verticalLayout4.setObjectName(u'verticalLayout4')
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.fileLineEdit = QtGui.QLineEdit(self.fileGroupBox)
        self.fileLineEdit.setObjectName(u'fileLineEdit')
        self.fileLineEdit.setReadOnly(True)
        self.fileLineEdit.setEnabled(False)
        self.horizontalLayout.addWidget(self.fileLineEdit)
        self.saveFilePushButton = QtGui.QPushButton(self.fileGroupBox)
        self.saveFilePushButton.setIcon(
            build_icon(u':/general/general_open.png'))
        self.saveFilePushButton.setObjectName(u'saveFilePushButton')
        self.horizontalLayout.addWidget(self.saveFilePushButton)
        self.verticalLayout4.addLayout(self.horizontalLayout)
        self.verticalLayout2.addWidget(self.fileGroupBox)
        self.verticalLayout.addWidget(self.dateRangeGroupBox)
        self.buttonBox = create_accept_reject_button_box(
            songUsageDetailDialog, True)
        self.verticalLayout.addWidget(self.buttonBox)
        self.retranslateUi(songUsageDetailDialog)
        QtCore.QObject.connect(self.saveFilePushButton,
            QtCore.SIGNAL(u'pressed()'),
            songUsageDetailDialog.defineOutputLocation)
        QtCore.QMetaObject.connectSlotsByName(songUsageDetailDialog)

    def retranslateUi(self, songUsageDetailDialog):
        songUsageDetailDialog.setWindowTitle(
            translate('SongUsagePlugin.SongUsageDetailForm',
            'Song Usage Extraction'))
        self.dateRangeGroupBox.setTitle(
            translate('SongUsagePlugin.SongUsageDetailForm',
            'Select Date Range'))
        self.toLabel.setText(
            translate('SongUsagePlugin.SongUsageDetailForm', 'to'))
        self.fileGroupBox.setTitle(
            translate('SongUsagePlugin.SongUsageDetailForm',
            'Report Location'))
