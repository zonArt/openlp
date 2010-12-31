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

class Ui_CustomEditDialog(object):
    def setupUi(self, customEditDialog):
        customEditDialog.setObjectName(u'customEditDialog')
        customEditDialog.resize(590, 541)
        customEditDialog.setWindowIcon(
            build_icon(u':/icon/openlp.org-icon-32.bmp'))
        self.gridLayout = QtGui.QGridLayout(customEditDialog)
        self.gridLayout.setObjectName(u'gridLayout')
        self.horizontalLayout3 = QtGui.QHBoxLayout()
        self.horizontalLayout3.setObjectName(u'horizontalLayout3')
        self.themeLabel = QtGui.QLabel(customEditDialog)
        self.themeLabel.setObjectName(u'themeLabel')
        self.horizontalLayout3.addWidget(self.themeLabel)
        self.themeComboBox = QtGui.QComboBox(customEditDialog)
        self.themeLabel.setBuddy(self.themeComboBox)
        self.themeComboBox.setObjectName(u'themeComboBox')
        self.horizontalLayout3.addWidget(self.themeComboBox)
        self.gridLayout.addLayout(self.horizontalLayout3, 2, 0, 1, 1)
        self.horizontalLayout2 = QtGui.QHBoxLayout()
        self.horizontalLayout2.setObjectName(u'horizontalLayout2')
        self.creditLabel = QtGui.QLabel(customEditDialog)
        self.creditLabel.setObjectName(u'creditLabel')
        self.horizontalLayout2.addWidget(self.creditLabel)
        self.creditEdit = QtGui.QLineEdit(customEditDialog)
        self.creditLabel.setBuddy(self.creditEdit)
        self.creditEdit.setObjectName(u'creditEdit')
        self.horizontalLayout2.addWidget(self.creditEdit)
        self.gridLayout.addLayout(self.horizontalLayout2, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(customEditDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(u'buttonBox')
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 1)
        self.horizontalLayout4 = QtGui.QHBoxLayout()
        self.horizontalLayout4.setObjectName(u'horizontalLayout4')
        self.slideListView = QtGui.QListWidget(customEditDialog)
        self.slideListView.setAlternatingRowColors(True)
        self.slideListView.setObjectName(u'slideListView')
        self.horizontalLayout4.addWidget(self.slideListView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.addButton = QtGui.QPushButton(customEditDialog)
        self.addButton.setObjectName(u'addButton')
        self.verticalLayout.addWidget(self.addButton)
        self.editButton = QtGui.QPushButton(customEditDialog)
        self.editButton.setObjectName(u'editButton')
        self.verticalLayout.addWidget(self.editButton)
        self.editAllButton = QtGui.QPushButton(customEditDialog)
        self.editAllButton.setObjectName(u'editAllButton')
        self.verticalLayout.addWidget(self.editAllButton)
        self.deleteButton = QtGui.QPushButton(customEditDialog)
        self.deleteButton.setObjectName(u'deleteButton')
        self.verticalLayout.addWidget(self.deleteButton)
        spacerItem = QtGui.QSpacerItem(20, 128, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.upButton = QtGui.QPushButton(customEditDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(u':/services/service_up.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.upButton.setIcon(icon1)
        self.upButton.setObjectName(u'upButton')
        self.verticalLayout.addWidget(self.upButton)
        self.downButton = QtGui.QPushButton(customEditDialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(u':/services/service_down.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downButton.setIcon(icon2)
        self.downButton.setObjectName(u'downButton')
        self.verticalLayout.addWidget(self.downButton)
        self.horizontalLayout4.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout4, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.titleLabel = QtGui.QLabel(customEditDialog)
        self.titleLabel.setObjectName(u'titleLabel')
        self.horizontalLayout.addWidget(self.titleLabel)
        self.titleEdit = QtGui.QLineEdit(customEditDialog)
        self.titleLabel.setBuddy(self.titleEdit)
        self.titleEdit.setObjectName(u'titleEdit')
        self.horizontalLayout.addWidget(self.titleEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(customEditDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'accepted()'),
            customEditDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'rejected()'),
            customEditDialog.closePressed)
        QtCore.QMetaObject.connectSlotsByName(customEditDialog)

    def retranslateUi(self, customEditDialog):
        customEditDialog.setWindowTitle(
            translate('CustomPlugin.EditCustomForm', 'Edit Custom Slides'))
        self.upButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Move slide up one '
            'position.'))
        self.downButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Move slide down one '
            'position.'))
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
        self.deleteButton.setText(
            translate('CustomPlugin.EditCustomForm', '&Delete'))
        self.deleteButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Delete the selected '
            'slide.'))
        self.themeLabel.setText(
            translate('CustomPlugin.EditCustomForm', 'The&me:'))
        self.creditLabel.setText(
            translate('CustomPlugin.EditCustomForm', '&Credits:'))