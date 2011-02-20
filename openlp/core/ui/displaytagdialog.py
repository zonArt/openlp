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

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DisplayTagDialog(object):

    def setupUi(self, displayTagDialog):
#        displayTagDialog.setObjectName(u'displayTagDialog')
#        displayTagDialog.resize(700, 500)
#        displayTagDialog.setWindowIcon(
#            build_icon(u':/system/system_settings.png'))
#        self.settingsLayout = QtGui.QVBoxLayout(displayTagDialog)
#        self.settingsLayout.setObjectName(u'settingsLayout')
#        self.editGroupBox = QtGui.QGroupBox(displayTagDialog)
#        self.editGroupBox.setGeometry(QtCore.QRect(10, 220, 650, 181))
#        self.editGroupBox.setObjectName(u'editGroupBox')
#        self.updatePushButton = QtGui.QPushButton(self.editGroupBox)
#        self.updatePushButton.setGeometry(QtCore.QRect(550, 140, 71, 26))
#        self.updatePushButton.setObjectName(u'updatePushButton')
#        self.layoutWidget = QtGui.QWidget(self.editGroupBox)
#        self.layoutWidget.setGeometry(QtCore.QRect(5, 20, 571, 114))
#        self.layoutWidget.setObjectName(u'layoutWidget')
#        self.formLayout = QtGui.QFormLayout(self.layoutWidget)
#        self.formLayout.setObjectName(u'formLayout')
#        self.descriptionLabel = QtGui.QLabel(self.layoutWidget)
#        self.descriptionLabel.setAlignment(QtCore.Qt.AlignCenter)
#        self.descriptionLabel.setObjectName(u'descriptionLabel')
#        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
#            self.descriptionLabel)
#        self.descriptionLineEdit = QtGui.QLineEdit(self.layoutWidget)
#        self.descriptionLineEdit.setObjectName(u'descriptionLineEdit')
#        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
#            self.descriptionLineEdit)
#        self.tagLabel = QtGui.QLabel(self.layoutWidget)
#        self.tagLabel.setAlignment(QtCore.Qt.AlignCenter)
#        self.tagLabel.setObjectName(u'tagLabel')
#        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.tagLabel)
#        self.tagLineEdit = QtGui.QLineEdit(self.layoutWidget)
#        self.tagLineEdit.setMaximumSize(QtCore.QSize(50, 16777215))
#        self.tagLineEdit.setMaxLength(5)
#        self.tagLineEdit.setObjectName(u'tagLineEdit')
#        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
#            self.tagLineEdit)
#        self.startTagLabel = QtGui.QLabel(self.layoutWidget)
#        self.startTagLabel.setAlignment(QtCore.Qt.AlignCenter)
#        self.startTagLabel.setObjectName(u'startTagLabel')
#        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
#            self.startTagLabel)
#        self.startTagLineEdit = QtGui.QLineEdit(self.layoutWidget)
#        self.startTagLineEdit.setObjectName(u'startTagLineEdit')
#        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
#            self.startTagLineEdit)
#        self.endTagLabel = QtGui.QLabel(self.layoutWidget)
#        self.endTagLabel.setAlignment(QtCore.Qt.AlignCenter)
#        self.endTagLabel.setObjectName(u'endTagLabel')
#        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
#            self.endTagLabel)
#        self.endTagLineEdit = QtGui.QLineEdit(self.layoutWidget)
#        self.endTagLineEdit.setObjectName(u'endTagLineEdit')
#        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
#            self.endTagLineEdit)
#        self.defaultPushButton = QtGui.QPushButton(displayTagDialog)
#        self.defaultPushButton.setGeometry(QtCore.QRect(430, 188, 71, 26))
#        self.defaultPushButton.setObjectName(u'updatePushButton')
#        self.deletePushButton = QtGui.QPushButton(displayTagDialog)
#        self.deletePushButton.setGeometry(QtCore.QRect(510, 188, 71, 26))
#        self.deletePushButton.setObjectName(u'deletePushButton')
#        self.newPushButton = QtGui.QPushButton(displayTagDialog)
#        self.newPushButton.setGeometry(QtCore.QRect(600, 188, 71, 26))
#        self.newPushButton.setObjectName(u'newPushButton')
#        self.tagTableWidget = QtGui.QTableWidget(displayTagDialog)
#        self.tagTableWidget.setGeometry(QtCore.QRect(10, 10, 650, 171))
#        self.tagTableWidget.setHorizontalScrollBarPolicy(
#            QtCore.Qt.ScrollBarAlwaysOff)
#        self.tagTableWidget.setEditTriggers(
#            QtGui.QAbstractItemView.NoEditTriggers)
#        self.tagTableWidget.setAlternatingRowColors(True)
#        self.tagTableWidget.setSelectionMode(
#            QtGui.QAbstractItemView.SingleSelection)
#        self.tagTableWidget.setSelectionBehavior(
#            QtGui.QAbstractItemView.SelectRows)
#        self.tagTableWidget.setCornerButtonEnabled(False)
#        self.tagTableWidget.setObjectName(u'tagTableWidget')
#        self.tagTableWidget.setColumnCount(4)
#        self.tagTableWidget.setRowCount(0)
#        item = QtGui.QTableWidgetItem()
#        self.tagTableWidget.setHorizontalHeaderItem(0, item)
#        item = QtGui.QTableWidgetItem()
#        self.tagTableWidget.setHorizontalHeaderItem(1, item)
#        item = QtGui.QTableWidgetItem()
#        self.tagTableWidget.setHorizontalHeaderItem(2, item)
#        item = QtGui.QTableWidgetItem()
#        self.tagTableWidget.setHorizontalHeaderItem(3, item)
#
#        self.buttonBox = create_accept_reject_button_box(displayTagDialog, True)
#        self.settingsLayout.addWidget(self.buttonBox)
#        self.retranslateUi(displayTagDialog)
#        QtCore.QMetaObject.connectSlotsByName(displayTagDialog)
        displayTagDialog.setObjectName(_fromUtf8("displayTagDialog"))
        displayTagDialog.resize(717, 554)
        self.editGroupBox = QtGui.QGroupBox(displayTagDialog)
        self.editGroupBox.setGeometry(QtCore.QRect(10, 320, 691, 181))
        self.editGroupBox.setObjectName(_fromUtf8("editGroupBox"))
        self.updatePushButton = QtGui.QPushButton(self.editGroupBox)
        self.updatePushButton.setGeometry(QtCore.QRect(600, 140, 73, 26))
        self.updatePushButton.setObjectName(_fromUtf8("updatePushButton"))
        self.layoutWidget = QtGui.QWidget(self.editGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 50, 571, 114))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.layoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.descriptionLabel = QtGui.QLabel(self.layoutWidget)
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.descriptionLabel)
        self.descriptionLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.descriptionLineEdit.setObjectName(_fromUtf8("descriptionLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.descriptionLineEdit)
        self.tagLabel = QtGui.QLabel(self.layoutWidget)
        self.tagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tagLabel.setObjectName(_fromUtf8("tagLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.tagLabel)
        self.tagLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.tagLineEdit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.tagLineEdit.setMaxLength(5)
        self.tagLineEdit.setObjectName(_fromUtf8("tagLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.tagLineEdit)
        self.startTagLabel = QtGui.QLabel(self.layoutWidget)
        self.startTagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.startTagLabel.setObjectName(_fromUtf8("startTagLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.startTagLabel)
        self.startTagLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.startTagLineEdit.setObjectName(_fromUtf8("startTagLineEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.startTagLineEdit)
        self.endTagLabel = QtGui.QLabel(self.layoutWidget)
        self.endTagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.endTagLabel.setObjectName(_fromUtf8("endTagLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.endTagLabel)
        self.endTagLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.endTagLineEdit.setObjectName(_fromUtf8("endTagLineEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.endTagLineEdit)
        self.addPushButton = QtGui.QPushButton(self.editGroupBox)
        self.addPushButton.setGeometry(QtCore.QRect(600, 40, 71, 26))
        self.addPushButton.setObjectName(_fromUtf8("addPushButton"))
        self.newPushButton = QtGui.QPushButton(self.editGroupBox)
        self.newPushButton.setGeometry(QtCore.QRect(600, 70, 71, 26))
        self.newPushButton.setObjectName(_fromUtf8("newPushButton"))
        self.buttonBox = QtGui.QDialogButtonBox(displayTagDialog)
        self.buttonBox.setGeometry(QtCore.QRect(540, 510, 162, 26))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.deletePushButton = QtGui.QPushButton(displayTagDialog)
        self.deletePushButton.setGeometry(QtCore.QRect(630, 280, 71, 26))
        self.deletePushButton.setObjectName(_fromUtf8("deletePushButton"))
        self.tagTableWidget = QtGui.QTableWidget(displayTagDialog)
        self.tagTableWidget.setGeometry(QtCore.QRect(10, 10, 691, 271))
        self.tagTableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tagTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tagTableWidget.setAlternatingRowColors(True)
        self.tagTableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tagTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tagTableWidget.setCornerButtonEnabled(False)
        self.tagTableWidget.setObjectName(_fromUtf8("tagTableWidget"))
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
        self.defaultPushButton = QtGui.QPushButton(displayTagDialog)
        self.defaultPushButton.setGeometry(QtCore.QRect(550, 280, 71, 26))
        self.defaultPushButton.setObjectName(_fromUtf8("defaultPushButton"))

        self.retranslateUi(displayTagDialog)
        QtCore.QMetaObject.connectSlotsByName(displayTagDialog)

    def retranslateUi(self, displayTagDialog):
        displayTagDialog.setWindowTitle(translate('OpenLP.displayTagForm',
            'Configure Display Tags'))
        self.editGroupBox.setTitle(
            translate('OpenLP.DisplayTagTab', 'Edit Selection'))
        self.updatePushButton.setText(
            translate('OpenLP.DisplayTagTab', 'Update'))
        self.descriptionLabel.setText(
            translate('OpenLP.DisplayTagTab', 'Description'))
        self.tagLabel.setText(translate('OpenLP.DisplayTagTab', 'Tag'))
        self.startTagLabel.setText(
            translate('OpenLP.DisplayTagTab', 'Start tag'))
        self.endTagLabel.setText(translate('OpenLP.DisplayTagTab', 'End tag'))
        self.deletePushButton.setText(UiStrings.Delete)
        self.defaultPushButton.setText(
            translate('OpenLP.DisplayTagTab', 'Default'))
        self.newPushButton.setText(UiStrings.New)
        self.tagTableWidget.horizontalHeaderItem(0)\
            .setText(translate('OpenLP.DisplayTagTab', 'Description'))
        self.tagTableWidget.horizontalHeaderItem(1)\
            .setText(translate('OpenLP.DisplayTagTab', 'Tag id'))
        self.tagTableWidget.horizontalHeaderItem(2)\
            .setText(translate('OpenLP.DisplayTagTab', 'Start Html'))
        self.tagTableWidget.horizontalHeaderItem(3)\
            .setText(translate('OpenLP.DisplayTagTab', 'End Html'))
        self.tagTableWidget.setColumnWidth(0, 120)
        self.tagTableWidget.setColumnWidth(1, 40)
        self.tagTableWidget.setColumnWidth(2, 240)
        self.tagTableWidget.setColumnWidth(3, 200)

        displayTagDialog.setWindowTitle(QtGui.QApplication.translate("displayTagDialog", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.editGroupBox.setTitle(QtGui.QApplication.translate("displayTagDialog", "Edit Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.updatePushButton.setText(QtGui.QApplication.translate("displayTagDialog", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.descriptionLabel.setText(QtGui.QApplication.translate("displayTagDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.tagLabel.setText(QtGui.QApplication.translate("displayTagDialog", "Tag", None, QtGui.QApplication.UnicodeUTF8))
        self.startTagLabel.setText(QtGui.QApplication.translate("displayTagDialog", "Start tag", None, QtGui.QApplication.UnicodeUTF8))
        self.endTagLabel.setText(QtGui.QApplication.translate("displayTagDialog", "End tag", None, QtGui.QApplication.UnicodeUTF8))
        self.addPushButton.setText(QtGui.QApplication.translate("displayTagDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.newPushButton.setText(QtGui.QApplication.translate("displayTagDialog", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.deletePushButton.setText(QtGui.QApplication.translate("displayTagDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tagTableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("displayTagDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.tagTableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("displayTagDialog", "Key", None, QtGui.QApplication.UnicodeUTF8))
        self.tagTableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("displayTagDialog", "Start Tag", None, QtGui.QApplication.UnicodeUTF8))
        self.tagTableWidget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("displayTagDialog", "End Tag", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultPushButton.setText(QtGui.QApplication.translate("displayTagDialog", "Default", None, QtGui.QApplication.UnicodeUTF8))


