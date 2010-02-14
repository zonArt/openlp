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

from datetime import date

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
        QtCore.QObject.connect(self.CancelButton,
                               QtCore.SIGNAL(u'clicked()'),
                               AlertForm.close)
        QtCore.QObject.connect(self.DisplayButton,
                               QtCore.SIGNAL(u'clicked()'),
                               self.onDisplayClicked)
        QtCore.QObject.connect(self.AlertEntryEditItem,
            QtCore.SIGNAL(u'textChanged(const QString&)'),
            self.onTextChanged)
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
            self.AlertListWidget.addItem(item_name)

    def onDisplayClicked(self):
        self.triggerAlert(unicode(self.AlertEntryEditItem.text()))
        if self.parent.alertsTab.save_history and self.history_required:
            alert = AlertItem()
            alert.text = unicode(self.AlertEntryEditItem.text())
            self.manager.save_alert(alert)
        self.history_required = False
        self.loadList()

    def onTextChanged(self):
        #Data has changed by editing it so potential storage
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
            self.AlertEntryEditItem.setText(bitem.text())
        self.history_required = False

    def triggerAlert(self, text):
        self.parent.alertsmanager.displayAlert(text)
