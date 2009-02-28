# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

from PyQt4 import QtCore, QtGui

from openlp.core.resources import *
from openlp.core.lib import SettingsTab

class AlertForm(object):

    def __init__(self):
        self.AlertForm = QtGui.QWidget()
        self.setupUi()

    def setupUi(self):
        self.AlertForm.setObjectName("AlertForm")
        self.AlertForm.resize(370, 105)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/openlp.org-icon-32.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AlertForm.setWindowIcon(icon)
        self.AlertFormLayout = QtGui.QVBoxLayout(self.AlertForm)
        self.AlertFormLayout.setSpacing(8)
        self.AlertFormLayout.setMargin(8)
        self.AlertFormLayout.setObjectName("AlertFormLayout")
        self.AlertEntryWidget = QtGui.QWidget(self.AlertForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlertEntryWidget.sizePolicy().hasHeightForWidth())
        self.AlertEntryWidget.setSizePolicy(sizePolicy)
        self.AlertEntryWidget.setObjectName("AlertEntryWidget")
        self.AlertEntryLabel = QtGui.QLabel(self.AlertEntryWidget)
        self.AlertEntryLabel.setGeometry(QtCore.QRect(0, 0, 353, 16))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlertEntryLabel.sizePolicy().hasHeightForWidth())
        self.AlertEntryLabel.setSizePolicy(sizePolicy)
        self.AlertEntryLabel.setObjectName("AlertEntryLabel")
        self.AlertEntryEditItem = QtGui.QLineEdit(self.AlertEntryWidget)
        self.AlertEntryEditItem.setGeometry(QtCore.QRect(0, 20, 353, 21))
        self.AlertEntryEditItem.setObjectName("AlertEntryEditItem")
        self.AlertFormLayout.addWidget(self.AlertEntryWidget)
        self.ButtonBoxWidget = QtGui.QWidget(self.AlertForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonBoxWidget.sizePolicy().hasHeightForWidth())
        self.ButtonBoxWidget.setSizePolicy(sizePolicy)
        self.ButtonBoxWidget.setObjectName("ButtonBoxWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.ButtonBoxWidget)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(267, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.DisplayButton = QtGui.QPushButton(self.ButtonBoxWidget)
        self.DisplayButton.setObjectName("DisplayButton")
        self.horizontalLayout.addWidget(self.DisplayButton)
        self.CancelButton = QtGui.QPushButton(self.ButtonBoxWidget)
        self.CancelButton.setObjectName("CancelButton")
        self.horizontalLayout.addWidget(self.CancelButton)
        self.AlertFormLayout.addWidget(self.ButtonBoxWidget)

        self.retranslateUi()
        QtCore.QObject.connect(self.CancelButton, QtCore.SIGNAL("clicked()"), self.AlertForm.close)
        QtCore.QMetaObject.connectSlotsByName(self.AlertForm)

    def retranslateUi(self):
        self.AlertForm.setWindowTitle(QtGui.QApplication.translate("AlertForm", "Alert Message", None, QtGui.QApplication.UnicodeUTF8))
        self.AlertEntryLabel.setText(QtGui.QApplication.translate("AlertForm", "Alert Text:", None, QtGui.QApplication.UnicodeUTF8))
        self.DisplayButton.setText(QtGui.QApplication.translate("AlertForm", "Display", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("AlertForm", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

    def show(self):
        self.AlertForm.show()
        
    def get_settings_tab_item(self):
        
        self.SettingsTabItem= SettingsTab()
        
        self.Alerts = QtGui.QWidget()
        self.Alerts.setObjectName("Alerts")
        self.formLayout_2 = QtGui.QFormLayout(self.Alerts)
        self.formLayout_2.setObjectName("formLayout_2")
        self.AlertGroupBox = QtGui.QGroupBox(self.Alerts)
        self.AlertGroupBox.setObjectName("AlertGroupBox")
        self.gridLayout = QtGui.QGridLayout(self.AlertGroupBox)
        self.gridLayout.setMargin(8)
        self.gridLayout.setObjectName("gridLayout")
        self.FontLabel = QtGui.QLabel(self.AlertGroupBox)
        self.FontLabel.setObjectName("FontLabel")
        self.gridLayout.addWidget(self.FontLabel, 0, 0, 1, 1)
        self.FontComboBox = QtGui.QFontComboBox(self.AlertGroupBox)
        self.FontComboBox.setObjectName("FontComboBox")
        self.gridLayout.addWidget(self.FontComboBox, 1, 0, 1, 1)
        self.ColorWidget = QtGui.QWidget(self.AlertGroupBox)
        self.ColorWidget.setObjectName("ColorWidget")
        self.ColorLayout = QtGui.QHBoxLayout(self.ColorWidget)
        self.ColorLayout.setSpacing(8)
        self.ColorLayout.setMargin(0)
        self.ColorLayout.setObjectName("ColorLayout")
        self.FontColorLabel = QtGui.QLabel(self.ColorWidget)
        self.FontColorLabel.setObjectName("FontColorLabel")
        self.ColorLayout.addWidget(self.FontColorLabel)
        self.FontColorPanel = QtGui.QGraphicsView(self.ColorWidget)
        self.FontColorPanel.setMinimumSize(QtCore.QSize(24, 24))
        self.FontColorPanel.setMaximumSize(QtCore.QSize(24, 24))
        self.FontColorPanel.setObjectName("FontColorPanel")
        self.ColorLayout.addWidget(self.FontColorPanel)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ColorLayout.addItem(spacerItem1)
        self.BackgroundColorLabel = QtGui.QLabel(self.ColorWidget)
        self.BackgroundColorLabel.setObjectName("BackgroundColorLabel")
        self.ColorLayout.addWidget(self.BackgroundColorLabel)
        self.BackgroundColorPanel = QtGui.QGraphicsView(self.ColorWidget)
        self.BackgroundColorPanel.setMinimumSize(QtCore.QSize(24, 24))
        self.BackgroundColorPanel.setMaximumSize(QtCore.QSize(24, 24))
        self.BackgroundColorPanel.setObjectName("BackgroundColorPanel")
        self.ColorLayout.addWidget(self.BackgroundColorPanel)
        self.gridLayout.addWidget(self.ColorWidget, 2, 0, 1, 1)
        self.FontPreview = QtGui.QGraphicsView(self.AlertGroupBox)
        self.FontPreview.setMaximumSize(QtCore.QSize(16777215, 64))
        self.FontPreview.setObjectName("FontPreview")
        self.gridLayout.addWidget(self.FontPreview, 3, 0, 1, 1)
        self.LengthWidget = QtGui.QWidget(self.AlertGroupBox)
        self.LengthWidget.setObjectName("LengthWidget")
        self.LengthLayout = QtGui.QHBoxLayout(self.LengthWidget)
        self.LengthLayout.setSpacing(8)
        self.LengthLayout.setMargin(0)
        self.LengthLayout.setObjectName("LengthLayout")
        self.LengthLabel = QtGui.QLabel(self.LengthWidget)
        self.LengthLabel.setObjectName("LengthLabel")
        self.LengthLayout.addWidget(self.LengthLabel)
        self.LengthSpinBox = QtGui.QSpinBox(self.LengthWidget)
        self.LengthSpinBox.setProperty("value", QtCore.QVariant(5))
        self.LengthSpinBox.setMaximum(180)
        self.LengthSpinBox.setObjectName("LengthSpinBox")
        self.LengthLayout.addWidget(self.LengthSpinBox)
        spacerItem2 = QtGui.QSpacerItem(147, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.LengthLayout.addItem(spacerItem2)
        self.gridLayout.addWidget(self.LengthWidget, 4, 0, 1, 1)
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.AlertGroupBox)
        
        self.AlertGroupBox.setTitle(QtGui.QApplication.translate("SettingsDialog", "Alerts", None, QtGui.QApplication.UnicodeUTF8))
        self.FontLabel.setText(QtGui.QApplication.translate("SettingsDialog", "Font Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.FontColorLabel.setText(QtGui.QApplication.translate("SettingsDialog", "Font Color:", None, QtGui.QApplication.UnicodeUTF8))
        self.BackgroundColorLabel.setText(QtGui.QApplication.translate("SettingsDialog", "Background Color:", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthLabel.setText(QtGui.QApplication.translate("SettingsDialog", "Display length:", None, QtGui.QApplication.UnicodeUTF8))
        self.LengthSpinBox.setSuffix(QtGui.QApplication.translate("SettingsDialog", "s", None, QtGui.QApplication.UnicodeUTF8))
        self.SettingsTabItem.setTabText(QtGui.QApplication.translate("SettingsDialog", "Alerts", None, QtGui.QApplication.UnicodeUTF8))        
        self.SettingsTabItem.add_items(self.Alerts)
        
        return self.SettingsTabItem

        
    def load_settings(self):
        pass
        
    def save_settings(self):
        pass
