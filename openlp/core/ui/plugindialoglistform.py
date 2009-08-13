# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plugindialoglistform.ui'
#
# Created: Thu Aug 13 05:52:06 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

import logging
from PyQt4 import QtCore, QtGui
from openlp.core.lib import translate

class PluginForm(QtGui.QDialog):
    global log
    log = logging.getLogger(u'PluginForm')

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, None)
        self.parent = parent
        self.setupUi(self)
        log.debug(u'Defined')

    def setupUi(self, PluginViewDialog):
        PluginViewDialog.setObjectName("PluginViewDialog")
        PluginViewDialog.resize(400, 393)
        self.PluginViewList = QtGui.QTableWidget(PluginViewDialog)
        self.PluginViewList.setGeometry(QtCore.QRect(20, 10, 371, 331))
        self.PluginViewList.setObjectName("PluginViewList")
        self.PluginViewList.setShowGrid(False)
        self.PluginViewList.setGridStyle(QtCore.Qt.SolidLine)
        self.PluginViewList.setSortingEnabled(False)
        self.PluginViewList.setColumnCount(3)
        item = QtGui.QTableWidgetItem()
        self.PluginViewList.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.PluginViewList.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.PluginViewList.setHorizontalHeaderItem(2, item)
        self.PluginViewList.horizontalHeader().setVisible(True)
        self.PluginViewList.verticalHeader().setVisible(False)
        self.ButtonBox = QtGui.QDialogButtonBox(PluginViewDialog)
        self.ButtonBox.setGeometry(QtCore.QRect(220, 350, 170, 25))
        self.ButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.ButtonBox.setObjectName("ButtonBox")

        self.retranslateUi(PluginViewDialog)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL("accepted()"), PluginViewDialog.close)
        QtCore.QMetaObject.connectSlotsByName(PluginViewDialog)

    def retranslateUi(self, PluginViewDialog):
        PluginViewDialog.setWindowTitle(QtGui.QApplication.translate("PluginViewDialog", "Plugin list", None, QtGui.QApplication.UnicodeUTF8))
        self.PluginViewList.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("PluginViewDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.PluginViewList.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("PluginViewDialog", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.PluginViewList.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("PluginViewDialog", "Status", None, QtGui.QApplication.UnicodeUTF8))

    def load(self):
        """
        Load the plugin details into the screen
        """
        for plugin in self.parent.plugin_manager.plugin_list:
            row = self.PluginViewList.rowCount()
            self.PluginViewList.setRowCount(row + 1)
            item1 = QtGui.QTableWidgetItem(plugin[u'name'])
            item1.setTextAlignment(QtCore.Qt.AlignVCenter)
            item2 = QtGui.QTableWidgetItem(plugin[u'version'])
            item2.setTextAlignment(QtCore.Qt.AlignVCenter)
            item3 = QtGui.QTableWidgetItem(plugin[u'status'])
            item3.setTextAlignment(QtCore.Qt.AlignVCenter)
            self.PluginViewList.setItem(row, 0, item1)
            self.PluginViewList.setItem(row, 1, item2)
            self.PluginViewList.setItem(row, 2, item3)
            self.PluginViewList.setRowHeight(row, 15)



