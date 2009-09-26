# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auditdeletedialog.ui'
#
# Created: Fri Sep 25 21:03:48 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AuditDeleteDialog(object):
    def setupUi(self, AuditDeleteDialog):
        AuditDeleteDialog.setObjectName("AuditDeleteDialog")
        AuditDeleteDialog.resize(291, 202)
        self.layoutWidget = QtGui.QWidget(AuditDeleteDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 247, 181))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.DeleteCalendar = QtGui.QCalendarWidget(self.layoutWidget)
        self.DeleteCalendar.setFirstDayOfWeek(QtCore.Qt.Sunday)
        self.DeleteCalendar.setGridVisible(True)
        self.DeleteCalendar.setVerticalHeaderFormat(QtGui.QCalendarWidget.NoVerticalHeader)
        self.DeleteCalendar.setObjectName("DeleteCalendar")
        self.verticalLayout.addWidget(self.DeleteCalendar)
        self.buttonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AuditDeleteDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AuditDeleteDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AuditDeleteDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AuditDeleteDialog)

    def retranslateUi(self, AuditDeleteDialog):
        AuditDeleteDialog.setWindowTitle(QtGui.QApplication.translate("AuditDeleteDialog", "Audit Delete ", None, QtGui.QApplication.UnicodeUTF8))

