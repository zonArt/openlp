# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

from alertdialog import Ui_AlertDialog

class AlertForm(QtGui.QDialog, Ui_AlertDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, manager, parent):
        """
        Constructor
        """
        self.manager = manager
        self.parent = parent
        self.history_required = True
        QtGui.QDialog.__init__(self, None)
        self.setupUi(self)
        QtCore.QObject.connect(self.DisplayButton,
                               QtCore.SIGNAL(u'clicked()'),
                               self.onDisplayClicked)
        QtCore.QObject.connect(self.DisplayCloseButton,
                               QtCore.SIGNAL(u'clicked()'),
                               self.onDisplayCloseClicked)
        QtCore.QObject.connect(self.AlertTextEdit,
            QtCore.SIGNAL(u'textChanged(const QString&)'),
            self.onTextChanged)
        QtCore.QObject.connect(self.NewButton,
                               QtCore.SIGNAL(u'clicked()'),
                               self.onNewClick)
        QtCore.QObject.connect(self.DeleteButton,
                               QtCore.SIGNAL(u'clicked()'),
                               self.onDeleteClick)
        QtCore.QObject.connect(self.EditButton,
                               QtCore.SIGNAL(u'clicked()'),
                               self.onEditClick)
        QtCore.QObject.connect(self.SaveButton,
                               QtCore.SIGNAL(u'clicked()'),
                               self.onSaveClick)
        QtCore.QObject.connect(self.AlertListWidget,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
            self.onDoubleClick)
        QtCore.QObject.connect(self.AlertListWidget,
            QtCore.SIGNAL(u'clicked(QModelIndex)'),
            self.onSingleClick)

    def loadList(self):
        self.AlertListWidget.clear()
        alerts = self.manager.get_all_alerts()
        for alert in alerts:
            item_name = QtGui.QListWidgetItem(alert.text)
            item_name.setData(
                QtCore.Qt.UserRole, QtCore.QVariant(alert.id))
            self.AlertListWidget.addItem(item_name)
        self.SaveButton.setEnabled(False)
        self.EditButton.setEnabled(False)
        self.DeleteButton.setEnabled(False)

    def onDisplayClicked(self):
        if self.triggerAlert(unicode(self.AlertTextEdit.text())):
            self.history_required = False
            self.loadList()

    def onDisplayCloseClicked(self):
        if self.triggerAlert(unicode(self.AlertTextEdit.text())):
            self.close()

    def onDeleteClick(self):
        item = self.AlertListWidget.currentItem()
        if item:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.parent.manager.delete_alert(item_id)
            row = self.AlertListWidget.row(item)
            self.AlertListWidget.takeItem(row)
        self.AlertTextEdit.setText(u'')
        self.SaveButton.setEnabled(False)
        self.DeleteButton.setEnabled(False)
        self.EditButton.setEnabled(False)

    def onEditClick(self):
        item = self.AlertListWidget.currentItem()
        if item:
            self.item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.AlertTextEdit.setText(unicode(item.text()))
        self.SaveButton.setEnabled(True)
        self.DeleteButton.setEnabled(True)
        self.EditButton.setEnabled(False)

    def onNewClick(self):
        if len(self.AlertTextEdit.text()) == 0:
            QtGui.QMessageBox.information(self,
                self.trUtf8('Item selected to Add'),
                self.trUtf8('Missing data'))
        else:
            alert = AlertItem()
            alert.text = unicode(self.AlertTextEdit.text())
            self.manager.save_alert(alert)
        self.onClearClick()
        self.loadList()

    def onSaveClick(self):
        alert = self.manager.get_alert(self.item_id)
        alert.text = unicode(self.AlertTextEdit.text())
        self.manager.save_alert(alert)
        self.onClearClick()
        self.loadList()

    def onTextChanged(self):
        #Data has changed by editing it so potential storage required
        self.history_required = True

    def onDoubleClick(self):
        """
        List item has been double clicked to display it
        """
        items = self.AlertListWidget.selectedIndexes()
        for item in items:
            bitem = self.AlertListWidget.item(item.row())
            self.triggerAlert(bitem.text())
        self.history_required = False

    def onSingleClick(self):
        """
        List item has been single clicked to add it to
        the edit field so it can be changed.
        """
        items = self.AlertListWidget.selectedIndexes()
        for item in items:
            bitem = self.AlertListWidget.item(item.row())
            self.AlertTextEdit.setText(bitem.text())
        self.history_required = False
        self.EditButton.setEnabled(True)
        self.DeleteButton.setEnabled(True)

    def triggerAlert(self, text):
        if text:
            self.parent.alertsmanager.displayAlert(text)
            if self.parent.alertsTab.save_history and self.history_required:
                alert = AlertItem()
                alert.text = unicode(self.AlertTextEdit.text())
                self.manager.save_alert(alert)
            return True
        return False
