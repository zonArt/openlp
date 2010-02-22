# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

class Ui_SongUsageDetailDialog(object):
    def setupUi(self, AuditDetailDialog):
        AuditDetailDialog.setObjectName(u'AuditDetailDialog')
        AuditDetailDialog.resize(609, 413)
        self.verticalLayout = QtGui.QVBoxLayout(AuditDetailDialog)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.DateRangeGroupBox = QtGui.QGroupBox(AuditDetailDialog)
        self.DateRangeGroupBox.setObjectName(u'DateRangeGroupBox')
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.DateRangeGroupBox)
        self.verticalLayout_2.setObjectName(u'verticalLayout_2')
        self.DateHorizontalLayout = QtGui.QHBoxLayout()
        self.DateHorizontalLayout.setObjectName(u'DateHorizontalLayout')
        self.FromDate = QtGui.QCalendarWidget(self.DateRangeGroupBox)
        self.FromDate.setObjectName(u'FromDate')
        self.DateHorizontalLayout.addWidget(self.FromDate)
        self.ToLabel = QtGui.QLabel(self.DateRangeGroupBox)
        self.ToLabel.setScaledContents(False)
        self.ToLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ToLabel.setObjectName(u'ToLabel')
        self.DateHorizontalLayout.addWidget(self.ToLabel)
        self.ToDate = QtGui.QCalendarWidget(self.DateRangeGroupBox)
        self.ToDate.setObjectName(u'ToDate')
        self.DateHorizontalLayout.addWidget(self.ToDate)
        self.verticalLayout_2.addLayout(self.DateHorizontalLayout)
        self.FileGroupBox = QtGui.QGroupBox(self.DateRangeGroupBox)
        self.FileGroupBox.setObjectName(u'FileGroupBox')
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.FileGroupBox)
        self.verticalLayout_4.setObjectName(u'verticalLayout_4')
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.FileLineEdit = QtGui.QLineEdit(self.FileGroupBox)
        self.FileLineEdit.setObjectName(u'FileLineEdit')
        self.horizontalLayout.addWidget(self.FileLineEdit)
        self.SaveFilePushButton = QtGui.QPushButton(self.FileGroupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/exports/export_load.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveFilePushButton.setIcon(icon)
        self.SaveFilePushButton.setObjectName(u'SaveFilePushButton')
        self.horizontalLayout.addWidget(self.SaveFilePushButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.FileGroupBox)
        self.verticalLayout.addWidget(self.DateRangeGroupBox)
        self.buttonBox = QtGui.QDialogButtonBox(AuditDetailDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u'buttonBox')
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AuditDetailDialog)
        QtCore.QObject.connect(self.buttonBox,
                                QtCore.SIGNAL(u'accepted()'),
                                AuditDetailDialog.accept)
        QtCore.QObject.connect(self.buttonBox,
                               QtCore.SIGNAL(u'rejected()'),
                               AuditDetailDialog.close)
        QtCore.QObject.connect(self.SaveFilePushButton,
                               QtCore.SIGNAL(u'pressed()'),
                               AuditDetailDialog.defineOutputLocation)
        QtCore.QMetaObject.connectSlotsByName(AuditDetailDialog)

    def retranslateUi(self, AuditDetailDialog):
        AuditDetailDialog.setWindowTitle(self.trUtf8('Audit Detail Extraction'))
        self.DateRangeGroupBox.setTitle(self.trUtf8('ASelect Date Range'))
        self.ToLabel.setText(self.trUtf8('to'))
        self.FileGroupBox.setTitle(self.trUtf8('Report Location'))
