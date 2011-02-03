# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import build_icon, translate
from openlp.core.lib.ui import save_cancel_button_box, delete_push_button, \
    up_down_push_button_set

class Ui_CustomEditDialog(object):
    def setupUi(self, customEditDialog):
        customEditDialog.setObjectName(u'customEditDialog')
        customEditDialog.resize(450, 350)
        customEditDialog.setWindowIcon(
            build_icon(u':/icon/openlp.org-icon-32.bmp'))
        self.dialogLayout = QtGui.QVBoxLayout(customEditDialog)
        self.dialogLayout.setObjectName(u'dialogLayout')
        self.titleLayout = QtGui.QHBoxLayout()
        self.titleLayout.setObjectName(u'titleLayout')
        self.titleLabel = QtGui.QLabel(customEditDialog)
        self.titleLabel.setObjectName(u'titleLabel')
        self.titleLayout.addWidget(self.titleLabel)
        self.titleEdit = QtGui.QLineEdit(customEditDialog)
        self.titleLabel.setBuddy(self.titleEdit)
        self.titleEdit.setObjectName(u'titleEdit')
        self.titleLayout.addWidget(self.titleEdit)
        self.dialogLayout.addLayout(self.titleLayout)
        self.centralLayout = QtGui.QHBoxLayout()
        self.centralLayout.setObjectName(u'centralLayout')
        self.slideListView = QtGui.QListWidget(customEditDialog)
        self.slideListView.setAlternatingRowColors(True)
        self.slideListView.setObjectName(u'slideListView')
        self.centralLayout.addWidget(self.slideListView)
        self.buttonLayout = QtGui.QVBoxLayout()
        self.buttonLayout.setObjectName(u'buttonLayout')
        self.addButton = QtGui.QPushButton(customEditDialog)
        self.addButton.setObjectName(u'addButton')
        self.buttonLayout.addWidget(self.addButton)
        self.editButton = QtGui.QPushButton(customEditDialog)
        self.editButton.setObjectName(u'editButton')
        self.buttonLayout.addWidget(self.editButton)
        self.editAllButton = QtGui.QPushButton(customEditDialog)
        self.editAllButton.setObjectName(u'editAllButton')
        self.buttonLayout.addWidget(self.editAllButton)
        self.deleteButton = delete_push_button(customEditDialog)
        self.buttonLayout.addWidget(self.deleteButton)
        self.buttonLayout.addStretch()
        self.upButton, self.downButton = up_down_push_button_set(
            customEditDialog)
        self.buttonLayout.addWidget(self.upButton)
        self.buttonLayout.addWidget(self.downButton)
        self.centralLayout.addLayout(self.buttonLayout)
        self.dialogLayout.addLayout(self.centralLayout)
        self.bottomFormLayout = QtGui.QFormLayout()
        self.bottomFormLayout.setObjectName(u'bottomFormLayout')
        self.themeLabel = QtGui.QLabel(customEditDialog)
        self.themeLabel.setObjectName(u'themeLabel')
        self.themeComboBox = QtGui.QComboBox(customEditDialog)
        self.themeComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.themeComboBox.setObjectName(u'themeComboBox')
        self.themeLabel.setBuddy(self.themeComboBox)
        self.bottomFormLayout.addRow(self.themeLabel, self.themeComboBox)
        self.creditLabel = QtGui.QLabel(customEditDialog)
        self.creditLabel.setObjectName(u'creditLabel')
        self.creditEdit = QtGui.QLineEdit(customEditDialog)
        self.creditEdit.setObjectName(u'creditEdit')
        self.creditLabel.setBuddy(self.creditEdit)
        self.bottomFormLayout.addRow(self.creditLabel, self.creditEdit)
        self.dialogLayout.addLayout(self.bottomFormLayout)
        self.buttonBox = save_cancel_button_box(customEditDialog)
        self.dialogLayout.addWidget(self.buttonBox)
        self.retranslateUi(customEditDialog)
        QtCore.QMetaObject.connectSlotsByName(customEditDialog)

    def retranslateUi(self, customEditDialog):
        customEditDialog.setWindowTitle(
            translate('CustomPlugin.EditCustomForm', 'Edit Custom Slides'))
        self.titleLabel.setText(
            translate('CustomPlugin.EditCustomForm', '&Title:'))
        self.addButton.setText(
            translate('CustomPlugin.EditCustomForm', '&Add'))
        self.addButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Add a new slide at '
            'bottom.'))
        self.editButton.setText(
            translate('CustomPlugin.EditCustomForm', '&Edit'))
        self.editButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Edit the selected '
            'slide.'))
        self.editAllButton.setText(
            translate('CustomPlugin.EditCustomForm', 'Ed&it All'))
        self.editAllButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Edit all the slides at '
            'once.'))
        self.themeLabel.setText(
            translate('CustomPlugin.EditCustomForm', 'The&me:'))
        self.creditLabel.setText(
            translate('CustomPlugin.EditCustomForm', '&Credits:'))
