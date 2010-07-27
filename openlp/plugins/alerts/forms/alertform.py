# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

from openlp.core.lib import translate
from openlp.plugins.alerts.lib.db import AlertItem

from alertdialog import Ui_AlertDialog

class AlertForm(QtGui.QDialog, Ui_AlertDialog):
    """
    Provide UI for the alert system
    """
    def __init__(self, manager, parent):
        """
        Initialise the alert form
        """
        self.manager = manager
        self.parent = parent
        self.item_id = None
        QtGui.QDialog.__init__(self, None)
        self.setupUi(self)
        QtCore.QObject.connect(self.DisplayButton, QtCore.SIGNAL(u'clicked()'),
            self.onDisplayClicked)
        QtCore.QObject.connect(self.DisplayCloseButton,
            QtCore.SIGNAL(u'clicked()'), self.onDisplayCloseClicked)
        QtCore.QObject.connect(self.AlertTextEdit,
            QtCore.SIGNAL(u'textChanged(const QString&)'), self.onTextChanged)
        QtCore.QObject.connect(self.NewButton, QtCore.SIGNAL(u'clicked()'),
            self.onNewClick)
        QtCore.QObject.connect(self.DeleteButton, QtCore.SIGNAL(u'clicked()'),
            self.onDeleteClick)
        QtCore.QObject.connect(self.SaveButton, QtCore.SIGNAL(u'clicked()'),
            self.onSaveClick)
        QtCore.QObject.connect(self.AlertListWidget,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'), self.onDoubleClick)
        QtCore.QObject.connect(self.AlertListWidget,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onSingleClick)

    def loadList(self):
        self.AlertListWidget.clear()
        alerts = self.manager.get_all_objects(AlertItem,
            order_by_ref=AlertItem.text)
        for alert in alerts:
            item_name = QtGui.QListWidgetItem(alert.text)
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(alert.id))
            self.AlertListWidget.addItem(item_name)
        self.SaveButton.setEnabled(False)
        self.DeleteButton.setEnabled(False)

    def onDisplayClicked(self):
        if self.triggerAlert(unicode(self.AlertTextEdit.text())):
            self.loadList()

    def onDisplayCloseClicked(self):
        if self.triggerAlert(unicode(self.AlertTextEdit.text())):
            self.close()

    def onDeleteClick(self):
        item = self.AlertListWidget.currentItem()
        if item:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.manager.delete_object(AlertItem, item_id)
            row = self.AlertListWidget.row(item)
            self.AlertListWidget.takeItem(row)
        self.AlertTextEdit.setText(u'')
        self.SaveButton.setEnabled(False)
        self.DeleteButton.setEnabled(False)

    def onNewClick(self):
        if len(self.AlertTextEdit.text()) == 0:
            QtGui.QMessageBox.information(self,
                translate('AlertsPlugin.AlertForm', 'New Alert'),
                translate('AlertsPlugin.AlertForm', 'You haven\'t specified '
                    'any text for your alert. Please type in some text before '
                    'clicking New.'))
        else:
            alert = AlertItem()
            alert.text = unicode(self.AlertTextEdit.text())
            self.manager.save_object(alert)
        self.AlertTextEdit.setText(u'')
        self.loadList()

    def onSaveClick(self):
        """
        Save an alert
        """
        if self.item_id:
            alert = self.manager.get_object(AlertItem, self.item_id)
            alert.text = unicode(self.AlertTextEdit.text())
            self.manager.save_object(alert)
            self.item_id = None
            self.loadList()
        else:
            self.onNewClick()

    def onTextChanged(self):
        """
        Enable save button when data has been changed by editing the form
        """
        self.SaveButton.setEnabled(True)

    def onDoubleClick(self):
        """
        List item has been double clicked to display it
        """
        items = self.AlertListWidget.selectedIndexes()
        for item in items:
            bitem = self.AlertListWidget.item(item.row())
            self.triggerAlert(bitem.text())
            self.AlertTextEdit.setText(bitem.text())
            self.item_id = (bitem.data(QtCore.Qt.UserRole)).toInt()[0]
        self.SaveButton.setEnabled(False)
        self.DeleteButton.setEnabled(True)

    def onSingleClick(self):
        """
        List item has been single clicked to add it to
        the edit field so it can be changed.
        """
        items = self.AlertListWidget.selectedIndexes()
        for item in items:
            bitem = self.AlertListWidget.item(item.row())
            self.AlertTextEdit.setText(bitem.text())
            self.item_id = (bitem.data(QtCore.Qt.UserRole)).toInt()[0]
        self.SaveButton.setEnabled(False)
        self.DeleteButton.setEnabled(True)

    def triggerAlert(self, text):
        if text:
            text = text.replace(u'<>', unicode(self.ParameterEdit.text()))
            self.parent.alertsmanager.displayAlert(text)
            return True
        return False
