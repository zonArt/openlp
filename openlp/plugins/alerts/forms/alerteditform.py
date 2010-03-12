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

from PyQt4 import QtGui, QtCore
from openlp.plugins.alerts.lib.models import AlertItem

from alerteditdialog import Ui_AlertEditDialog

class AlertEditForm(QtGui.QDialog, Ui_AlertEditDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, manager, parent):
        """
        Constructor
        """
        self.manager = manager
        self.parent = parent
        QtGui.QDialog.__init__(self, None)
        self.setupUi(self)
        QtCore.QObject.connect(self.DeleteButton,
                               QtCore.SIGNAL(u'clicked()'),
                               self.onDeleteClick)
        QtCore.QObject.connect(self.ClearButton,
                               QtCore.SIGNAL(u'clicked()'),
                               self.onClearClick)
        QtCore.QObject.connect(self.EditButton,
                               QtCore.SIGNAL(u'clicked()'),
                               self.onEditClick)
        QtCore.QObject.connect(self.AddButton,
                               QtCore.SIGNAL(u'clicked()'),
                               self.onAddClick)
        QtCore.QObject.connect(self.SaveButton,
                               QtCore.SIGNAL(u'clicked()'),
                               self.onSaveClick)
        QtCore.QObject.connect(self.buttonBox,
                               QtCore.SIGNAL(u'rejected()'), self.close)
        QtCore.QObject.connect(self.AlertLineEdit,
            QtCore.SIGNAL(u'textChanged(const QString&)'),
            self.onTextChanged)
        QtCore.QObject.connect(self.AlertListWidget,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
            self.onItemSelected)
        QtCore.QObject.connect(self.AlertListWidget,
            QtCore.SIGNAL(u'clicked(QModelIndex)'),
            self.onItemSelected)

    def loadList(self):
        self.AlertListWidget.clear()
        alerts = self.manager.get_all_alerts()
        for alert in alerts:
            item_name = QtGui.QListWidgetItem(alert.text)
            item_name.setData(
                QtCore.Qt.UserRole, QtCore.QVariant(alert.id))
            self.AlertListWidget.addItem(item_name)
        self.AddButton.setEnabled(True)
        self.ClearButton.setEnabled(False)
        self.SaveButton.setEnabled(False)
        self.EditButton.setEnabled(False)
        self.DeleteButton.setEnabled(False)

    def onItemSelected(self):
        if self.AlertLineEdit.text():
            QtGui.QMessageBox.information(self,
                self.trUtf8('Item selected to Edit'),
                self.trUtf8('Please Save or Clear seletced item'))
        else:
            self.EditButton.setEnabled(True)
            self.DeleteButton.setEnabled(True)

    def onDeleteClick(self):
        item = self.AlertListWidget.currentItem()
        if item:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.parent.manager.delete_alert(item_id)
            row = self.AlertListWidget.row(item)
            self.AlertListWidget.takeItem(row)
        self.AddButton.setEnabled(True)
        self.SaveButton.setEnabled(False)
        self.DeleteButton.setEnabled(False)
        self.EditButton.setEnabled(False)

    def onEditClick(self):
        item = self.AlertListWidget.currentItem()
        if item:
            self.item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.AlertLineEdit.setText(unicode(item.text()))
        self.AddButton.setEnabled(True)
        self.ClearButton.setEnabled(True)
        self.SaveButton.setEnabled(True)
        self.DeleteButton.setEnabled(True)
        self.EditButton.setEnabled(False)

    def onClearClick(self):
        self.AlertLineEdit.setText(u'')
        self.AddButton.setEnabled(False)
        self.ClearButton.setEnabled(True)
        self.SaveButton.setEnabled(False)
        self.DeleteButton.setEnabled(False)
        self.EditButton.setEnabled(False)

    def onAddClick(self):
        if len(self.AlertLineEdit.text()) == 0:
            QtGui.QMessageBox.information(self,
                self.trUtf8('Item selected to Add'),
                self.trUtf8('Missing data'))
        else:
            alert = AlertItem()
            alert.text = unicode(self.AlertLineEdit.text())
            self.manager.save_alert(alert)
        self.onClearClick()
        self.loadList()

    def onSaveClick(self):
        alert = self.manager.get_alert(self.item_id)
        alert.text = unicode(self.AlertLineEdit.text())
        self.manager.save_alert(alert)
        self.onClearClick()
        self.loadList()

    def onTextChanged(self):
        self.AddButton.setEnabled(True)

    def onDoubleClick(self):
        """
        List item has been double clicked to display it
        """
        items = self.AlertListWidget.selectedIndexes()
        for item in items:
            bitem = self.AlertListWidget.item(item.row())
            self.triggerAlert(bitem.text())

    def onSingleClick(self):
        """
        List item has been single clicked to add it to
        the edit field so it can be changed.
        """
        items = self.AlertListWidget.selectedIndexes()
        for item in items:
            bitem = self.AlertListWidget.item(item.row())
            self.AlertEntryEditItem.setText(bitem.text())

    def triggerAlert(self, text):
        self.parent.alertsmanager.displayAlert(text)
