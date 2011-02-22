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

from openlp.core.lib import translate, build_icon
from openlp.core.lib.ui import UiStrings, create_accept_reject_button_box

class Ui_DisplayTagDialog(object):

    def setupUi(self, displayTagDialog):
        displayTagDialog.setObjectName(u'displayTagDialog')
        displayTagDialog.resize(725, 548)
        self.widget = QtGui.QWidget(displayTagDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 701, 521))
        self.widget.setObjectName(u'widget')
        self.listdataGridLayout = QtGui.QGridLayout(self.widget)
        self.listdataGridLayout.setMargin(0)
        self.listdataGridLayout.setObjectName(u'listdataGridLayout')
        self.tagTableWidget = QtGui.QTableWidget(self.widget)
        self.tagTableWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.tagTableWidget.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)
        self.tagTableWidget.setAlternatingRowColors(True)
        self.tagTableWidget.setSelectionMode(
            QtGui.QAbstractItemView.SingleSelection)
        self.tagTableWidget.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)
        self.tagTableWidget.setCornerButtonEnabled(False)
        self.tagTableWidget.setObjectName(u'tagTableWidget')
        self.tagTableWidget.setColumnCount(4)
        self.tagTableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tagTableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tagTableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tagTableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tagTableWidget.setHorizontalHeaderItem(3, item)
        self.listdataGridLayout.addWidget(self.tagTableWidget, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        spacerItem = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.defaultPushButton = QtGui.QPushButton(self.widget)
        self.defaultPushButton.setObjectName(u'defaultPushButton')
        self.horizontalLayout.addWidget(self.defaultPushButton)
        self.deletePushButton = QtGui.QPushButton(self.widget)
        self.deletePushButton.setObjectName(u'deletePushButton')
        self.horizontalLayout.addWidget(self.deletePushButton)
        self.listdataGridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.editGroupBox = QtGui.QGroupBox(self.widget)
        self.editGroupBox.setObjectName(u'editGroupBox')
        self.dataGridLayout = QtGui.QGridLayout(self.editGroupBox)
        self.dataGridLayout.setObjectName(u'dataGridLayout')
        self.descriptionLabel = QtGui.QLabel(self.editGroupBox)
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.descriptionLabel.setObjectName(u'descriptionLabel')
        self.dataGridLayout.addWidget(self.descriptionLabel, 0, 0, 1, 1)
        self.descriptionLineEdit = QtGui.QLineEdit(self.editGroupBox)
        self.descriptionLineEdit.setObjectName(u'descriptionLineEdit')
        self.dataGridLayout.addWidget(self.descriptionLineEdit, 0, 1, 2, 1)
        self.newPushButton = QtGui.QPushButton(self.editGroupBox)
        self.newPushButton.setObjectName(u'newPushButton')
        self.dataGridLayout.addWidget(self.newPushButton, 0, 2, 2, 1)
        self.tagLabel = QtGui.QLabel(self.editGroupBox)
        self.tagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tagLabel.setObjectName(u'tagLabel')
        self.dataGridLayout.addWidget(self.tagLabel, 2, 0, 1, 1)
        self.tagLineEdit = QtGui.QLineEdit(self.editGroupBox)
        self.tagLineEdit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.tagLineEdit.setMaxLength(5)
        self.tagLineEdit.setObjectName(u'tagLineEdit')
        self.dataGridLayout.addWidget(self.tagLineEdit, 2, 1, 1, 1)
        self.startTagLabel = QtGui.QLabel(self.editGroupBox)
        self.startTagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.startTagLabel.setObjectName(u'startTagLabel')
        self.dataGridLayout.addWidget(self.startTagLabel, 3, 0, 1, 1)
        self.startTagLineEdit = QtGui.QLineEdit(self.editGroupBox)
        self.startTagLineEdit.setObjectName(u'startTagLineEdit')
        self.dataGridLayout.addWidget(self.startTagLineEdit, 3, 1, 1, 1)
        self.endTagLabel = QtGui.QLabel(self.editGroupBox)
        self.endTagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.endTagLabel.setObjectName(u'endTagLabel')
        self.dataGridLayout.addWidget(self.endTagLabel, 4, 0, 1, 1)
        self.endTagLineEdit = QtGui.QLineEdit(self.editGroupBox)
        self.endTagLineEdit.setObjectName(u'endTagLineEdit')
        self.dataGridLayout.addWidget(self.endTagLineEdit, 4, 1, 1, 1)
        self.updatePushButton = QtGui.QPushButton(self.editGroupBox)
        self.updatePushButton.setObjectName(u'updatePushButton')
        self.dataGridLayout.addWidget(self.updatePushButton, 4, 2, 1, 1)
        self.listdataGridLayout.addWidget(self.editGroupBox, 2, 0, 1, 1)
        self.buttonBox = create_accept_reject_button_box(displayTagDialog)
        self.listdataGridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(displayTagDialog)
        QtCore.QMetaObject.connectSlotsByName(displayTagDialog)

    def retranslateUi(self, displayTagDialog):
        displayTagDialog.setWindowTitle(translate('OpenLP.displayTagDialog',
            'Configure Display Tags'))
        self.editGroupBox.setTitle(
            translate('OpenLP.DisplayTagDialog', 'Edit Selection'))
        self.updatePushButton.setText(
            translate('OpenLP.DisplayTagDialog', 'Update'))
        self.descriptionLabel.setText(
            translate('OpenLP.DisplayTagDialog', 'Description'))
        self.tagLabel.setText(translate('OpenLP.DisplayTagDialog', 'Tag'))
        self.startTagLabel.setText(
            translate('OpenLP.DisplayTagDialog', 'Start tag'))
        self.endTagLabel.setText(translate('OpenLP.DisplayTagDialog', 'End tag'))
        self.deletePushButton.setText(UiStrings.Delete)
        self.defaultPushButton.setText(
            translate('OpenLP.DisplayTagDialog', 'Default'))
        self.newPushButton.setText(UiStrings.New)
        self.tagTableWidget.horizontalHeaderItem(0).setText(
            translate('OpenLP.DisplayTagDialog', 'Description'))
        self.tagTableWidget.horizontalHeaderItem(1).setText(
            translate('OpenLP.DisplayTagDialog', 'Tag id'))
        self.tagTableWidget.horizontalHeaderItem(2).setText(
            translate('OpenLP.DisplayTagDialog', 'Start Html'))
        self.tagTableWidget.horizontalHeaderItem(3).setText(
            translate('OpenLP.DisplayTagDialog', 'End Html'))
        self.tagTableWidget.setColumnWidth(0, 120)
        self.tagTableWidget.setColumnWidth(1, 40)
        self.tagTableWidget.setColumnWidth(2, 240)
        self.tagTableWidget.setColumnWidth(3, 240)
