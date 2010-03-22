# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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
from openlp.core.lib import build_icon

class Ui_customEditDialog(object):
    def setupUi(self, customEditDialog):
        customEditDialog.setObjectName(u'customEditDialog')
        customEditDialog.resize(590, 541)
        icon = build_icon(u':/icon/openlp.org-icon-32.bmp')
        customEditDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(customEditDialog)
        self.gridLayout.setObjectName(u'gridLayout')
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.TitleLabel = QtGui.QLabel(customEditDialog)
        self.TitleLabel.setObjectName(u'TitleLabel')
        self.horizontalLayout.addWidget(self.TitleLabel)
        self.TitleEdit = QtGui.QLineEdit(customEditDialog)
        self.TitleEdit.setObjectName(u'TitleEdit')
        self.horizontalLayout.addWidget(self.TitleEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u'horizontalLayout_4')
        self.VerseListView = QtGui.QListWidget(customEditDialog)
        self.VerseListView.setAlternatingRowColors(True)
        self.VerseListView.setObjectName(u'VerseListView')
        self.horizontalLayout_4.addWidget(self.VerseListView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.UpButton = QtGui.QPushButton(customEditDialog)
        icon1 = build_icon(u':/services/service_up.png')
        self.UpButton.setIcon(icon1)
        self.UpButton.setObjectName(u'UpButton')
        self.verticalLayout.addWidget(self.UpButton)
        spacerItem = QtGui.QSpacerItem(20, 128,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.DownButton = QtGui.QPushButton(customEditDialog)
        icon2 = build_icon(u':/services/service_down.png')
        self.DownButton.setIcon(icon2)
        self.DownButton.setObjectName(u'DownButton')
        self.verticalLayout.addWidget(self.DownButton)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.EditWidget = QtGui.QWidget(customEditDialog)
        self.EditWidget.setObjectName(u'EditWidget')
        self.EditLayout_3 = QtGui.QHBoxLayout(self.EditWidget)
        self.EditLayout_3.setSpacing(8)
        self.EditLayout_3.setMargin(0)
        self.EditLayout_3.setObjectName(u'EditLayout_3')
        self.VerseTextEdit = QtGui.QTextEdit(self.EditWidget)
        self.VerseTextEdit.setObjectName(u'VerseTextEdit')
        self.EditLayout_3.addWidget(self.VerseTextEdit)
        self.ButtonWidge = QtGui.QWidget(self.EditWidget)
        self.ButtonWidge.setObjectName(u'ButtonWidge')
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.ButtonWidge)
        self.verticalLayout_2.setObjectName(u'verticalLayout_2')
        self.AddButton = QtGui.QPushButton(self.ButtonWidge)
        self.AddButton.setObjectName(u'AddButton')
        self.verticalLayout_2.addWidget(self.AddButton)
        self.EditButton = QtGui.QPushButton(self.ButtonWidge)
        self.EditButton.setObjectName(u'EditButton')
        self.verticalLayout_2.addWidget(self.EditButton)
        self.EditAllButton = QtGui.QPushButton(self.ButtonWidge)
        self.EditAllButton.setObjectName(u'EditAllButton')
        self.verticalLayout_2.addWidget(self.EditAllButton)
        self.SaveButton = QtGui.QPushButton(self.ButtonWidge)
        self.SaveButton.setObjectName(u'SaveButton')
        self.verticalLayout_2.addWidget(self.SaveButton)
        self.DeleteButton = QtGui.QPushButton(self.ButtonWidge)
        self.DeleteButton.setObjectName(u'DeleteButton')
        self.verticalLayout_2.addWidget(self.DeleteButton)
        self.ClearButton = QtGui.QPushButton(self.ButtonWidge)
        self.ClearButton.setObjectName(u'ClearButton')
        self.verticalLayout_2.addWidget(self.ClearButton)
        spacerItem1 = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.EditLayout_3.addWidget(self.ButtonWidge)
        self.gridLayout.addWidget(self.EditWidget, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u'horizontalLayout_3')
        self.ThemeLabel = QtGui.QLabel(customEditDialog)
        self.ThemeLabel.setObjectName(u'ThemeLabel')
        self.horizontalLayout_3.addWidget(self.ThemeLabel)
        self.ThemeComboBox = QtGui.QComboBox(customEditDialog)
        self.ThemeComboBox.setObjectName(u'ThemeComboBox')
        self.horizontalLayout_3.addWidget(self.ThemeComboBox)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u'horizontalLayout_2')
        self.CreditLabel = QtGui.QLabel(customEditDialog)
        self.CreditLabel.setObjectName(u'CreditLabel')
        self.horizontalLayout_2.addWidget(self.CreditLabel)
        self.CreditEdit = QtGui.QLineEdit(customEditDialog)
        self.CreditEdit.setObjectName(u'CreditEdit')
        self.horizontalLayout_2.addWidget(self.CreditEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(customEditDialog)
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(u'buttonBox')
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)

        self.retranslateUi(customEditDialog)
        QtCore.QObject.connect(self.buttonBox,
            QtCore.SIGNAL(u'rejected()'), customEditDialog.closePressed)
        QtCore.QObject.connect(self.buttonBox,
            QtCore.SIGNAL(u'accepted()'), customEditDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(customEditDialog)
        customEditDialog.setTabOrder(self.TitleEdit, self.VerseTextEdit)
        customEditDialog.setTabOrder(self.VerseTextEdit, self.AddButton)
        customEditDialog.setTabOrder(self.AddButton, self.VerseListView)
        customEditDialog.setTabOrder(self.VerseListView, self.EditButton)
        customEditDialog.setTabOrder(self.EditButton, self.EditAllButton)
        customEditDialog.setTabOrder(self.EditAllButton, self.SaveButton)
        customEditDialog.setTabOrder(self.SaveButton, self.DeleteButton)
        customEditDialog.setTabOrder(self.DeleteButton, self.CreditEdit)
        customEditDialog.setTabOrder(self.CreditEdit, self.UpButton)
        customEditDialog.setTabOrder(self.UpButton, self.DownButton)
        customEditDialog.setTabOrder(self.DownButton, self.ThemeComboBox)
        customEditDialog.setTabOrder(self.ThemeComboBox, self.buttonBox)

    def retranslateUi(self, customEditDialog):
        self.UpButton.setToolTip(self.trUtf8('Move slide Up 1'))
        self.DownButton.setToolTip(self.trUtf8('Move slide down 1'))
        customEditDialog.setWindowTitle(self.trUtf8('Edit Custom Slides'))
        self.TitleLabel.setText(self.trUtf8('Title:'))
        self.AddButton.setText(self.trUtf8('Add New'))
        self.AddButton.setToolTip(self.trUtf8('Add new slide at bottom'))
        self.EditButton.setText(self.trUtf8('Edit'))
        self.EditButton.setToolTip(self.trUtf8('Edit selected slide'))
        self.EditAllButton.setText(self.trUtf8('Edit All'))
        self.EditAllButton.setToolTip(self.trUtf8('Edit all slides'))
        self.SaveButton.setText(self.trUtf8('Save'))
        self.SaveButton.setToolTip(self.trUtf8('Replace edited slide'))
        self.DeleteButton.setText(self.trUtf8('Delete'))
        self.DeleteButton.setToolTip(self.trUtf8('Delete selected slide'))
        self.ClearButton.setText(self.trUtf8('Clear'))
        self.ClearButton.setToolTip(self.trUtf8('Clear edit area'))
        self.ThemeLabel.setText(self.trUtf8('Theme:'))
        self.ThemeComboBox.setToolTip(self.trUtf8('Set Theme for Slides'))
        self.CreditLabel.setText(self.trUtf8('Credits:'))
