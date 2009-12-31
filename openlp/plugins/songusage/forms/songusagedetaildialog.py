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
        AuditDetailDialog.resize(593, 501)
        self.buttonBox = QtGui.QDialogButtonBox(AuditDetailDialog)
        self.buttonBox.setGeometry(QtCore.QRect(420, 470, 170, 25))
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u'buttonBox')
        self.FileGroupBox = QtGui.QGroupBox(AuditDetailDialog)
        self.FileGroupBox.setGeometry(QtCore.QRect(10, 370, 571, 70))
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
        icon.addPixmap(QtGui.QPixmap(u':/exports/export_load.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveFilePushButton.setIcon(icon)
        self.SaveFilePushButton.setObjectName(u'SaveFilePushButton')
        self.horizontalLayout.addWidget(self.SaveFilePushButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.layoutWidget = QtGui.QWidget(AuditDetailDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 561, 361))
        self.layoutWidget.setObjectName(u'layoutWidget')
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u'verticalLayout_3')
        self.ReportTypeGroup = QtGui.QGroupBox(self.layoutWidget)
        self.ReportTypeGroup.setObjectName(u'ReportTypeGroup')
        self.layoutWidget1 = QtGui.QWidget(self.ReportTypeGroup)
        self.layoutWidget1.setGeometry(QtCore.QRect(50, 40, 481, 23))
        self.layoutWidget1.setObjectName(u'layoutWidget1')
        self.ReportHorizontalLayout = QtGui.QHBoxLayout(self.layoutWidget1)
        self.ReportHorizontalLayout.setObjectName(u'ReportHorizontalLayout')
        self.SummaryReport = QtGui.QRadioButton(self.layoutWidget1)
        self.SummaryReport.setObjectName(u'SummaryReport')
        self.ReportHorizontalLayout.addWidget(self.SummaryReport)
        self.DetailedReport = QtGui.QRadioButton(self.layoutWidget1)
        self.DetailedReport.setChecked(True)
        self.DetailedReport.setObjectName(u'DetailedReport')
        self.ReportHorizontalLayout.addWidget(self.DetailedReport)
        self.verticalLayout_3.addWidget(self.ReportTypeGroup)
        self.DateRangeGroupBox = QtGui.QGroupBox(self.layoutWidget)
        self.DateRangeGroupBox.setObjectName(u'DateRangeGroupBox')
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.DateRangeGroupBox)
        self.verticalLayout_2.setObjectName(u'verticalLayout_2')
        self.DateHorizontalLayout = QtGui.QHBoxLayout()
        self.DateHorizontalLayout.setObjectName(u'DateHorizontalLayout')
        self.FromDateEdit = QtGui.QDateEdit(self.DateRangeGroupBox)
        self.FromDateEdit.setCalendarPopup(True)
        self.FromDateEdit.setObjectName(u'FromDateEdit')
        self.DateHorizontalLayout.addWidget(self.FromDateEdit)
        self.To = QtGui.QLabel(self.DateRangeGroupBox)
        self.To.setObjectName(u'To')
        self.DateHorizontalLayout.addWidget(self.To)
        self.ToDateEdit = QtGui.QDateEdit(self.DateRangeGroupBox)
        self.ToDateEdit.setCalendarPopup(True)
        self.ToDateEdit.setObjectName(u'ToDateEdit')
        self.DateHorizontalLayout.addWidget(self.ToDateEdit)
        self.verticalLayout_2.addLayout(self.DateHorizontalLayout)
        self.verticalLayout_3.addWidget(self.DateRangeGroupBox)
        self.TimePeriodGroupBox = QtGui.QGroupBox(self.layoutWidget)
        self.TimePeriodGroupBox.setObjectName(u'TimePeriodGroupBox')
        self.verticalLayout = QtGui.QVBoxLayout(self.TimePeriodGroupBox)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.FirstHorizontalLayout = QtGui.QHBoxLayout()
        self.FirstHorizontalLayout.setObjectName(u'FirstHorizontalLayout')
        self.FirstCheckBox = QtGui.QCheckBox(self.TimePeriodGroupBox)
        self.FirstCheckBox.setChecked(True)
        self.FirstCheckBox.setObjectName(u'FirstCheckBox')
        self.FirstHorizontalLayout.addWidget(self.FirstCheckBox)
        self.FirstFromTimeEdit = QtGui.QTimeEdit(self.TimePeriodGroupBox)
        self.FirstFromTimeEdit.setTime(QtCore.QTime(9, 0, 0))
        self.FirstFromTimeEdit.setObjectName(u'FirstFromTimeEdit')
        self.FirstHorizontalLayout.addWidget(self.FirstFromTimeEdit)
        self.FirstTo = QtGui.QLabel(self.TimePeriodGroupBox)
        self.FirstTo.setObjectName(u'FirstTo')
        self.FirstHorizontalLayout.addWidget(self.FirstTo)
        self.FirstToTimeEdit = QtGui.QTimeEdit(self.TimePeriodGroupBox)
        self.FirstToTimeEdit.setCalendarPopup(True)
        self.FirstToTimeEdit.setTime(QtCore.QTime(10, 0, 0))
        self.FirstToTimeEdit.setObjectName(u'FirstToTimeEdit')
        self.FirstHorizontalLayout.addWidget(self.FirstToTimeEdit)
        self.verticalLayout.addLayout(self.FirstHorizontalLayout)
        self.SecondHorizontalLayout = QtGui.QHBoxLayout()
        self.SecondHorizontalLayout.setObjectName(u'SecondHorizontalLayout')
        self.SecondCheckBox = QtGui.QCheckBox(self.TimePeriodGroupBox)
        self.SecondCheckBox.setChecked(True)
        self.SecondCheckBox.setObjectName(u'SecondCheckBox')
        self.SecondHorizontalLayout.addWidget(self.SecondCheckBox)
        self.SecondFromTimeEdit = QtGui.QTimeEdit(self.TimePeriodGroupBox)
        self.SecondFromTimeEdit.setTime(QtCore.QTime(10, 45, 0))
        self.SecondFromTimeEdit.setObjectName(u'SecondFromTimeEdit')
        self.SecondHorizontalLayout.addWidget(self.SecondFromTimeEdit)
        self.SecondTo = QtGui.QLabel(self.TimePeriodGroupBox)
        self.SecondTo.setObjectName(u'SecondTo')
        self.SecondHorizontalLayout.addWidget(self.SecondTo)
        self.SecondToTimeEdit = QtGui.QTimeEdit(self.TimePeriodGroupBox)
        self.SecondToTimeEdit.setObjectName(u'SecondToTimeEdit')
        self.SecondHorizontalLayout.addWidget(self.SecondToTimeEdit)
        self.verticalLayout.addLayout(self.SecondHorizontalLayout)
        self.ThirdHorizontalLayout = QtGui.QHBoxLayout()
        self.ThirdHorizontalLayout.setObjectName(u'ThirdHorizontalLayout')
        self.ThirdCheckBox = QtGui.QCheckBox(self.TimePeriodGroupBox)
        self.ThirdCheckBox.setChecked(True)
        self.ThirdCheckBox.setObjectName(u'ThirdCheckBox')
        self.ThirdHorizontalLayout.addWidget(self.ThirdCheckBox)
        self.ThirdFromTimeEdit = QtGui.QTimeEdit(self.TimePeriodGroupBox)
        self.ThirdFromTimeEdit.setTime(QtCore.QTime(18, 30, 0))
        self.ThirdFromTimeEdit.setObjectName(u'ThirdFromTimeEdit')
        self.ThirdHorizontalLayout.addWidget(self.ThirdFromTimeEdit)
        self.ThirdTo = QtGui.QLabel(self.TimePeriodGroupBox)
        self.ThirdTo.setObjectName(u'ThirdTo')
        self.ThirdHorizontalLayout.addWidget(self.ThirdTo)
        self.ThirdToTimeEdit = QtGui.QTimeEdit(self.TimePeriodGroupBox)
        self.ThirdToTimeEdit.setTime(QtCore.QTime(19, 30, 0))
        self.ThirdToTimeEdit.setObjectName(u'ThirdToTimeEdit')
        self.ThirdHorizontalLayout.addWidget(self.ThirdToTimeEdit)
        self.verticalLayout.addLayout(self.ThirdHorizontalLayout)
        self.verticalLayout_3.addWidget(self.TimePeriodGroupBox)

        self.retranslateUi(AuditDetailDialog)
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL(u'accepted()'),
            AuditDetailDialog.accept)
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL(u'rejected()'),
            AuditDetailDialog.close)
        QtCore.QObject.connect(
            self.FirstCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            AuditDetailDialog.changeFirstService)
        QtCore.QObject.connect(
            self.SecondCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            AuditDetailDialog.changeSecondService)
        QtCore.QObject.connect(
            self.ThirdCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            AuditDetailDialog.changeThirdService)
        QtCore.QObject.connect(
            self.SaveFilePushButton, QtCore.SIGNAL(u'pressed()'),
            AuditDetailDialog.defineOutputLocation)
        QtCore.QMetaObject.connectSlotsByName(AuditDetailDialog)

    def retranslateUi(self, AuditDetailDialog):
        AuditDetailDialog.setWindowTitle(self.trUtf8('Audit Detail Extraction'))
        self.FileGroupBox.setTitle(self.trUtf8('Report Location'))
        self.ReportTypeGroup.setTitle(self.trUtf8('Report Type'))
        self.SummaryReport.setText(self.trUtf8('Summary'))
        self.DetailedReport.setText(self.trUtf8('Detailed'))
        self.DateRangeGroupBox.setTitle(self.trUtf8('Select Date Range'))
        self.FromDateEdit.setDisplayFormat(self.trUtf8('dd/MM/yyyy'))
        self.To.setText(self.trUtf8('to'))
        self.ToDateEdit.setDisplayFormat(self.trUtf8('dd/MM/yyyy'))
        self.TimePeriodGroupBox.setTitle(self.trUtf8('Select Time Periods'))
        self.FirstCheckBox.setText(self.trUtf8('First Service'))
        self.FirstFromTimeEdit.setDisplayFormat(self.trUtf8('hh:mm AP'))
        self.FirstTo.setText(self.trUtf8('to'))
        self.FirstToTimeEdit.setDisplayFormat(self.trUtf8('hh:mm AP'))
        self.SecondCheckBox.setText(self.trUtf8('Second Service'))
        self.SecondFromTimeEdit.setDisplayFormat(self.trUtf8('hh:mm AP'))
        self.SecondTo.setText(self.trUtf8('to'))
        self.SecondToTimeEdit.setDisplayFormat(self.trUtf8('hh:mm AP'))
        self.ThirdCheckBox.setText(self.trUtf8('Third Service'))
        self.ThirdFromTimeEdit.setDisplayFormat(self.trUtf8('hh:mm AP'))
        self.ThirdTo.setText(self.trUtf8('to'))
        self.ThirdToTimeEdit.setDisplayFormat(self.trUtf8('hh:mm AP'))