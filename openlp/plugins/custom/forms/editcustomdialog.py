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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import build_icon, translate
from openlp.core.ui import SpellTextEdit

class Ui_CustomEditDialog(object):
    def setupUi(self, customEditDialog):
        customEditDialog.setObjectName(u'customEditDialog')
        customEditDialog.resize(590, 541)
        customEditDialog.setWindowIcon(
            build_icon(u':/icon/openlp.org-icon-32.bmp'))
        self.gridLayout = QtGui.QGridLayout(customEditDialog)
        self.gridLayout.setObjectName(u'gridLayout')
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
        self.horizontalLayout4 = QtGui.QHBoxLayout()
        self.horizontalLayout4.setObjectName(u'horizontalLayout4')
        self.verseListView = QtGui.QListWidget(customEditDialog)
        self.verseListView.setAlternatingRowColors(True)
        self.verseListView.setObjectName(u'verseListView')
        self.horizontalLayout4.addWidget(self.verseListView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.upButton = QtGui.QPushButton(customEditDialog)
        self.upButton.setIcon(build_icon(u':/services/service_up.png'))
        self.upButton.setObjectName(u'upButton')
        self.verticalLayout.addWidget(self.upButton)
        spacerItem = QtGui.QSpacerItem(20, 128, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.downButton = QtGui.QPushButton(customEditDialog)
        self.downButton.setIcon(build_icon(u':/services/service_down.png'))
        self.downButton.setObjectName(u'downButton')
        self.verticalLayout.addWidget(self.downButton)
        self.horizontalLayout4.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout4, 1, 0, 1, 1)
        self.editWidget = QtGui.QWidget(customEditDialog)
        self.editWidget.setObjectName(u'editWidget')
        self.editLayout3 = QtGui.QHBoxLayout(self.editWidget)
        self.editLayout3.setSpacing(8)
        self.editLayout3.setMargin(0)
        self.editLayout3.setObjectName(u'editLayout3')
        self.verseTextEdit = SpellTextEdit(self.editWidget)
        self.verseTextEdit.setObjectName(u'verseTextEdit')
        self.editLayout3.addWidget(self.verseTextEdit)
        self.buttonWidget = QtGui.QWidget(self.editWidget)
        self.buttonWidget.setObjectName(u'buttonWidget')
        self.verticalLayout2 = QtGui.QVBoxLayout(self.buttonWidget)
        self.verticalLayout2.setObjectName(u'verticalLayout2')
        self.addButton = QtGui.QPushButton(self.buttonWidget)
        self.addButton.setObjectName(u'addButton')
        self.verticalLayout2.addWidget(self.addButton)
        self.editButton = QtGui.QPushButton(self.buttonWidget)
        self.editButton.setObjectName(u'editButton')
        self.verticalLayout2.addWidget(self.editButton)
        self.editAllButton = QtGui.QPushButton(self.buttonWidget)
        self.editAllButton.setObjectName(u'editAllButton')
        self.verticalLayout2.addWidget(self.editAllButton)
        self.saveButton = QtGui.QPushButton(self.buttonWidget)
        self.saveButton.setObjectName(u'saveButton')
        self.verticalLayout2.addWidget(self.saveButton)
        self.deleteButton = QtGui.QPushButton(self.buttonWidget)
        self.deleteButton.setObjectName(u'deleteButton')
        self.verticalLayout2.addWidget(self.deleteButton)
        self.clearButton = QtGui.QPushButton(self.buttonWidget)
        self.clearButton.setObjectName(u'clearButton')
        self.verticalLayout2.addWidget(self.clearButton)
        self.splitButton = QtGui.QPushButton(self.buttonWidget)
        self.splitButton.setObjectName(u'splitButton')
        self.verticalLayout2.addWidget(self.splitButton)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.verticalLayout2.addItem(spacerItem1)
        self.editLayout3.addWidget(self.buttonWidget)
        self.gridLayout.addWidget(self.editWidget, 2, 0, 1, 1)
        self.horizontalLayout3 = QtGui.QHBoxLayout()
        self.horizontalLayout3.setObjectName(u'horizontalLayout3')
        self.themeLabel = QtGui.QLabel(customEditDialog)
        self.themeLabel.setObjectName(u'themeLabel')
        self.horizontalLayout3.addWidget(self.themeLabel)
        self.themeComboBox = QtGui.QComboBox(customEditDialog)
        self.themeLabel.setBuddy(self.themeComboBox)
        self.themeComboBox.setObjectName(u'themeComboBox')
        self.horizontalLayout3.addWidget(self.themeComboBox)
        self.gridLayout.addLayout(self.horizontalLayout3, 3, 0, 1, 1)
        self.horizontalLayout2 = QtGui.QHBoxLayout()
        self.horizontalLayout2.setObjectName(u'horizontalLayout2')
        self.creditLabel = QtGui.QLabel(customEditDialog)
        self.creditLabel.setObjectName(u'creditLabel')
        self.horizontalLayout2.addWidget(self.creditLabel)
        self.creditEdit = QtGui.QLineEdit(customEditDialog)
        self.creditLabel.setBuddy(self.creditEdit)
        self.creditEdit.setObjectName(u'creditEdit')
        self.horizontalLayout2.addWidget(self.creditEdit)
        self.gridLayout.addLayout(self.horizontalLayout2, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(customEditDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(u'buttonBox')
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)
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
            translate('CustomPlugin.EditCustomForm', 'Move slide up once '
                'position.'))
        self.downButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Move slide down one '
                'position.'))
        self.titleLabel.setText(
            translate('CustomPlugin.EditCustomForm', '&Title:'))
        self.addButton.setText(
            translate('CustomPlugin.EditCustomForm', 'Add New'))
        self.addButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Add a new slide at '
                'bottom.'))
        self.editButton.setText(
            translate('CustomPlugin.EditCustomForm', 'Edit'))
        self.editButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Edit the selected '
                'slide.'))
        self.editAllButton.setText(
            translate('CustomPlugin.EditCustomForm', 'Edit All'))
        self.editAllButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Edit all the slides at '
                'once.'))
        self.saveButton.setText(
            translate('CustomPlugin.EditCustomForm', 'Save'))
        self.saveButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Save the slide currently '
                'being edited.'))
        self.deleteButton.setText(
            translate('CustomPlugin.EditCustomForm', 'Delete'))
        self.deleteButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Delete the selected '
                'slide.'))
        self.clearButton.setText(
            translate('CustomPlugin.EditCustomForm', 'Clear'))
        self.clearButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Clear edit area'))
        self.splitButton.setText(
            translate('CustomPlugin.EditCustomForm', 'Split Slide'))
        self.splitButton.setToolTip(
            translate('CustomPlugin.EditCustomForm', 'Split a slide into two '
                'by inserting a slide splitter.'))
        self.themeLabel.setText(
            translate('CustomPlugin.EditCustomForm', 'The&me:'))
        self.creditLabel.setText(
            translate('CustomPlugin.EditCustomForm', '&Credits:'))
