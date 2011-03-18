# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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

from openlp.core.lib import build_icon, translate
from openlp.core.lib.ui import create_delete_push_button

class Ui_AlertDialog(object):
    def setupUi(self, alertDialog):
        alertDialog.setObjectName(u'alertDialog')
        alertDialog.resize(400, 300)
        alertDialog.setWindowIcon(build_icon(u':/icon/openlp.org-icon-32.bmp'))
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
        self.deleteButton = create_delete_push_button(alertDialog)
        self.deleteButton.setEnabled(False)
        self.manageButtonLayout.addWidget(self.deleteButton)
        self.manageButtonLayout.addStretch()
        self.alertDialogLayout.addLayout(self.manageButtonLayout, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(alertDialog)
        self.buttonBox.addButton(QtGui.QDialogButtonBox.Close)
        displayIcon = build_icon(u':/general/general_live.png')
        self.displayButton = QtGui.QPushButton(alertDialog)
        self.displayButton.setEnabled(False)
        self.displayButton.setIcon(displayIcon)
        self.displayButton.setObjectName(u'displayButton')
        self.buttonBox.addButton(self.displayButton,
            QtGui.QDialogButtonBox.ActionRole)
        self.displayCloseButton = QtGui.QPushButton(alertDialog)
        self.displayCloseButton.setEnabled(False)
        self.displayCloseButton.setIcon(displayIcon)
        self.displayCloseButton.setObjectName(u'displayCloseButton')
        self.buttonBox.addButton(self.displayCloseButton,
            QtGui.QDialogButtonBox.ActionRole)
        self.alertDialogLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.retranslateUi(alertDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'rejected()'),
            alertDialog.close)
        QtCore.QMetaObject.connectSlotsByName(alertDialog)

    def retranslateUi(self, alertDialog):
        alertDialog.setWindowTitle(
            translate('AlertsPlugin.AlertForm', 'Alert Message'))
        self.alertEntryLabel.setText(
            translate('AlertsPlugin.AlertForm', 'Alert &text:'))
        self.alertParameter.setText(
            translate('AlertsPlugin.AlertForm', '&Parameter:'))
        self.newButton.setText(
            translate('AlertsPlugin.AlertForm', '&New'))
        self.saveButton.setText(
            translate('AlertsPlugin.AlertForm', '&Save'))
        self.displayButton.setText(
            translate('AlertsPlugin.AlertForm', 'Displ&ay'))
        self.displayCloseButton.setText(
            translate('AlertsPlugin.AlertForm', 'Display && Cl&ose'))
