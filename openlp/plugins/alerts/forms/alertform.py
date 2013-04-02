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

from PyQt4 import QtGui, QtCore

from openlp.core.lib import translate
from openlp.plugins.alerts.lib.db import AlertItem

from alertdialog import Ui_AlertDialog


class AlertForm(QtGui.QDialog, Ui_AlertDialog):
    """
    Provide UI for the alert system
    """
    def __init__(self, plugin):
        """
        Initialise the alert form
        """
        self.manager = plugin.manager
        self.plugin = plugin
        self.item_id = None
        super(AlertForm, self).__init__(self.plugin.main_window)
        self.setupUi(self)
        QtCore.QObject.connect(self.displayButton, QtCore.SIGNAL(u'clicked()'), self.onDisplayClicked)
        QtCore.QObject.connect(self.displayCloseButton, QtCore.SIGNAL(u'clicked()'), self.onDisplayCloseClicked)
        QtCore.QObject.connect(self.alertTextEdit, QtCore.SIGNAL(u'textChanged(const QString&)'), self.onTextChanged)
        QtCore.QObject.connect(self.newButton, QtCore.SIGNAL(u'clicked()'), self.onNewClick)
        QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL(u'clicked()'), self.onSaveClick)
        QtCore.QObject.connect(self.alertListWidget, QtCore.SIGNAL(u'doubleClicked(QModelIndex)'), self.onDoubleClick)
        QtCore.QObject.connect(self.alertListWidget, QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onSingleClick)
        QtCore.QObject.connect(self.alertListWidget, QtCore.SIGNAL(u'currentRowChanged(int)'), self.onCurrentRowChanged)

    def exec_(self):
        """
        Execute the dialog and return the exit code.
        """
        self.displayButton.setEnabled(False)
        self.displayCloseButton.setEnabled(False)
        self.alertTextEdit.setText(u'')
        return QtGui.QDialog.exec_(self)

    def loadList(self):
        """
        Loads the list with alerts.
        """
        self.alertListWidget.clear()
        alerts = self.manager.get_all_objects(AlertItem, order_by_ref=AlertItem.text)
        for alert in alerts:
            item_name = QtGui.QListWidgetItem(alert.text)
            item_name.setData(QtCore.Qt.UserRole, alert.id)
            self.alertListWidget.addItem(item_name)
            if alert.text == unicode(self.alertTextEdit.text()):
                self.item_id = alert.id
                self.alertListWidget.setCurrentRow(self.alertListWidget.row(item_name))

    def onDisplayClicked(self):
        """
        Display the current alert text.
        """
        self.triggerAlert(self.alertTextEdit.text())

    def onDisplayCloseClicked(self):
        """
        Close the alert preview.
        """
        if self.triggerAlert(self.alertTextEdit.text()):
            self.close()

    def onDeleteButtonClicked(self):
        """
        Deletes the selected item.
        """
        item = self.alertListWidget.currentItem()
        if item:
            item_id = item.data(QtCore.Qt.UserRole)
            self.manager.delete_object(AlertItem, item_id)
            row = self.alertListWidget.row(item)
            self.alertListWidget.takeItem(row)
        self.item_id = None
        self.alertTextEdit.setText(u'')

    def onNewClick(self):
        """
        Create a new alert.
        """
        if not self.alertTextEdit.text():
            QtGui.QMessageBox.information(self,
                translate('AlertsPlugin.AlertForm', 'New Alert'),
                translate('AlertsPlugin.AlertForm', 'You haven\'t specified any text for your alert. \n'
                    'Please type in some text before clicking New.'))
        else:
            alert = AlertItem()
            alert.text = self.alertTextEdit.text()
            self.manager.save_object(alert)
        self.loadList()

    def onSaveClick(self):
        """
        Save the alert, we are editing.
        """
        if self.item_id:
            alert = self.manager.get_object(AlertItem, self.item_id)
            alert.text = self.alertTextEdit.text()
            self.manager.save_object(alert)
            self.item_id = None
            self.loadList()
        self.saveButton.setEnabled(False)

    def onTextChanged(self):
        """
        Enable save button when data has been changed by editing the form.
        """
        # Only enable the button, if we are editing an item.
        if self.item_id:
            self.saveButton.setEnabled(True)
        if self.alertTextEdit.text():
            self.displayButton.setEnabled(True)
            self.displayCloseButton.setEnabled(True)
        else:
            self.displayButton.setEnabled(False)
            self.displayCloseButton.setEnabled(False)

    def onDoubleClick(self):
        """
        List item has been double clicked to display it.
        """
        item = self.alertListWidget.selectedIndexes()[0]
        bitem = self.alertListWidget.item(item.row())
        self.triggerAlert(bitem.text())
        self.alertTextEdit.setText(bitem.text())
        self.item_id = bitem.data(QtCore.Qt.UserRole)
        self.saveButton.setEnabled(False)

    def onSingleClick(self):
        """
        List item has been single clicked to add it to the edit field so it can
        be changed.
        """
        item = self.alertListWidget.selectedIndexes()[0]
        bitem = self.alertListWidget.item(item.row())
        self.alertTextEdit.setText(bitem.text())
        self.item_id = bitem.data(QtCore.Qt.UserRole)
        # If the alert does not contain '<>' we clear the ParameterEdit field.
        if self.alertTextEdit.text().find(u'<>') == -1:
            self.parameterEdit.setText(u'')
        self.saveButton.setEnabled(False)

    def triggerAlert(self, text):
        """
        Prepares the alert text for displaying.

        ``text``
            The alert text (unicode).
        """
        if not text:
            return False
        # We found '<>' in the alert text, but the ParameterEdit field is empty.
        if text.find(u'<>') != -1 and not self.parameterEdit.text() and QtGui.QMessageBox.question(self,
                translate('AlertsPlugin.AlertForm', 'No Parameter Found'),
                translate('AlertsPlugin.AlertForm', 'You have not entered a parameter to be replaced.\n'
                    'Do you want to continue anyway?'),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)) == QtGui.QMessageBox.No:
            self.parameterEdit.setFocus()
            return False
        # The ParameterEdit field is not empty, but we have not found '<>'
        # in the alert text.
        elif text.find(u'<>') == -1 and self.parameterEdit.text() and QtGui.QMessageBox.question(self,
                translate('AlertsPlugin.AlertForm', 'No Placeholder Found'),
                translate('AlertsPlugin.AlertForm', 'The alert text does not contain \'<>\'.\n'
                    'Do you want to continue anyway?'),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)) == QtGui.QMessageBox.No:
            self.parameterEdit.setFocus()
            return False
        text = text.replace(u'<>', self.parameterEdit.text())
        self.plugin.alertsmanager.displayAlert(text)
        return True

    def onCurrentRowChanged(self, row):
        """
        Called when the *alertListWidget*'s current row has been changed. This
        enables or disables buttons which require an item to act on.

        ``row``
            The row (int). If there is no current row, the value is -1.
        """
        if row == -1:
            self.displayButton.setEnabled(False)
            self.displayCloseButton.setEnabled(False)
            self.saveButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.displayButton.setEnabled(True)
            self.displayCloseButton.setEnabled(True)
            self.deleteButton.setEnabled(True)
            # We do not need to enable the save button, as it is only enabled
            # when typing text in the "alertTextEdit".
