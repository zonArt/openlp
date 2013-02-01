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

from PyQt4 import QtGui

from openlp.core.lib import build_icon, translate
from openlp.core.lib.ui import create_button, create_button_box

class Ui_AlertDialog(object):
    def setupUi(self, alertDialog):
        alertDialog.setObjectName(u'alertDialog')
        alertDialog.resize(400, 300)
        alertDialog.setWindowIcon(build_icon(u':/icon/openlp-logo-16x16.png'))
        self.alertDialogLayout = QtGui.QGridLayout(alertDialog)
        self.alertDialogLayout.setObjectName(u'alertDialogLayout')
        self.alertTextLayout = QtGui.QFormLayout()
        self.alertTextLayout.setObjectName(u'alertTextLayout')
        self.alertEntryLabel = QtGui.QLabel(alertDialog)
        self.alertEntryLabel.setObjectName(u'alertEntryLabel')
        self.alertTextEdit = QtGui.QLineEdit(alertDialog)
        self.alertTextEdit.setObjectName(u'alertTextEdit')
        self.alertEntryLabel.setBuddy(self.alertTextEdit)
        self.alertTextLayout.addRow(self.alertEntryLabel, self.alertTextEdit)
        self.alertParameter = QtGui.QLabel(alertDialog)
        self.alertParameter.setObjectName(u'alertParameter')
        self.parameterEdit = QtGui.QLineEdit(alertDialog)
        self.parameterEdit.setObjectName(u'parameterEdit')
        self.alertParameter.setBuddy(self.parameterEdit)
        self.alertTextLayout.addRow(self.alertParameter, self.parameterEdit)
        self.alertDialogLayout.addLayout(self.alertTextLayout, 0, 0, 1, 2)
        self.alertListWidget = QtGui.QListWidget(alertDialog)
        self.alertListWidget.setAlternatingRowColors(True)
        self.alertListWidget.setObjectName(u'alertListWidget')
        self.alertDialogLayout.addWidget(self.alertListWidget, 1, 0)
        self.manageButtonLayout = QtGui.QVBoxLayout()
        self.manageButtonLayout.setObjectName(u'manageButtonLayout')
        self.newButton = QtGui.QPushButton(alertDialog)
        self.newButton.setIcon(build_icon(u':/general/general_new.png'))
        self.newButton.setObjectName(u'newButton')
        self.manageButtonLayout.addWidget(self.newButton)
        self.saveButton = QtGui.QPushButton(alertDialog)
        self.saveButton.setEnabled(False)
        self.saveButton.setIcon(build_icon(u':/general/general_save.png'))
        self.saveButton.setObjectName(u'saveButton')
        self.manageButtonLayout.addWidget(self.saveButton)
        self.deleteButton = create_button(alertDialog, u'deleteButton', role=u'delete', enabled=False,
            click=alertDialog.onDeleteButtonClicked)
        self.manageButtonLayout.addWidget(self.deleteButton)
        self.manageButtonLayout.addStretch()
        self.alertDialogLayout.addLayout(self.manageButtonLayout, 1, 1)
        displayIcon = build_icon(u':/general/general_live.png')
        self.displayButton = create_button(alertDialog, u'displayButton', icon=displayIcon, enabled=False)
        self.displayCloseButton = create_button(alertDialog, u'displayCloseButton', icon=displayIcon, enabled=False)
        self.button_box = create_button_box(alertDialog, u'button_box', [u'close'],
            [self.displayButton, self.displayCloseButton])
        self.alertDialogLayout.addWidget(self.button_box, 2, 0, 1, 2)
        self.retranslateUi(alertDialog)

    def retranslateUi(self, alertDialog):
        alertDialog.setWindowTitle(translate('AlertsPlugin.AlertForm', 'Alert Message'))
        self.alertEntryLabel.setText(translate('AlertsPlugin.AlertForm', 'Alert &text:'))
        self.alertParameter.setText(translate('AlertsPlugin.AlertForm', '&Parameter:'))
        self.newButton.setText(translate('AlertsPlugin.AlertForm', '&New'))
        self.saveButton.setText(translate('AlertsPlugin.AlertForm', '&Save'))
        self.displayButton.setText(translate('AlertsPlugin.AlertForm', 'Displ&ay'))
        self.displayCloseButton.setText(translate('AlertsPlugin.AlertForm', 'Display && Cl&ose'))
