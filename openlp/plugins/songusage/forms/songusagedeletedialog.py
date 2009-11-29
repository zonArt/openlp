# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auditdeletedialog.ui'
#
# Created: Sun Oct 11 11:34:45 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SongUsageDeleteDialog(object):
    def setupUi(self, AuditDeleteDialog):
        AuditDeleteDialog.setObjectName(u'AuditDeleteDialog')
        AuditDeleteDialog.resize(291, 243)
        self.layoutWidget = QtGui.QWidget(AuditDeleteDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 247, 181))
        self.layoutWidget.setObjectName(u'layoutWidget')
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.DeleteCalendar = QtGui.QCalendarWidget(self.layoutWidget)
        self.DeleteCalendar.setFirstDayOfWeek(QtCore.Qt.Sunday)
        self.DeleteCalendar.setGridVisible(True)
        self.DeleteCalendar.setVerticalHeaderFormat(
            QtGui.QCalendarWidget.NoVerticalHeader)
        self.DeleteCalendar.setObjectName(u'DeleteCalendar')
        self.verticalLayout.addWidget(self.DeleteCalendar)
        self.buttonBox = QtGui.QDialogButtonBox(AuditDeleteDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 210, 245, 25))
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u'buttonBox')

        self.retranslateUi(AuditDeleteDialog)
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL(u'accepted()'),
            AuditDeleteDialog.accept)
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL(u'rejected()'),
            AuditDeleteDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AuditDeleteDialog)

    def retranslateUi(self, AuditDeleteDialog):
        AuditDeleteDialog.setWindowTitle(self.trUtf8('Audit Delete'))

