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

class GeneralForm(object):
    """
    This is not a standard form
    It is a holder for General settings used by the rendering components
    It provides the Settings Tab to control the Output Configuration
    """
    def __init__(self):
        pass
    def get_settings_tab_item(self):

        self.SettingsTabItem= SettingsTabItem()

        self.DisplayTab = QtGui.QWidget()
        self.DisplayTab.setObjectName("DisplayTab")
        self.DisplayTabLayout = QtGui.QHBoxLayout(self.DisplayTab)
        self.DisplayTabLayout.setSpacing(8)
        self.DisplayTabLayout.setMargin(8)
        self.DisplayTabLayout.setObjectName("DisplayTabLayout")
        self.LeftColumn = QtGui.QWidget(self.DisplayTab)
        self.LeftColumn.setObjectName("LeftColumn")
        self.LeftColumnLayout = QtGui.QVBoxLayout(self.LeftColumn)
        self.LeftColumnLayout.setSpacing(8)
        self.LeftColumnLayout.setMargin(0)
        self.LeftColumnLayout.setObjectName("LeftColumnLayout")
        self.MonitorGroupBox = QtGui.QGroupBox(self.LeftColumn)
        self.MonitorGroupBox.setObjectName("MonitorGroupBox")
        self.MonitorLayout = QtGui.QVBoxLayout(self.MonitorGroupBox)
        self.MonitorLayout.setSpacing(8)
        self.MonitorLayout.setMargin(8)
        self.MonitorLayout.setObjectName("MonitorLayout")
        self.MonitorLabel = QtGui.QLabel(self.MonitorGroupBox)
        self.MonitorLabel.setObjectName("MonitorLabel")
        self.MonitorLayout.addWidget(self.MonitorLabel)
        self.MonitorComboBox = QtGui.QComboBox(self.MonitorGroupBox)
        self.MonitorComboBox.setObjectName("MonitorComboBox")
        self.MonitorComboBox.addItem(QtCore.QString())
        self.MonitorComboBox.addItem(QtCore.QString())
        self.MonitorLayout.addWidget(self.MonitorComboBox)
        self.LeftColumnLayout.addWidget(self.MonitorGroupBox)
        self.FontSizeGroupBox = QtGui.QGroupBox(self.LeftColumn)
        self.FontSizeGroupBox.setObjectName("FontSizeGroupBox")
        self.FontSizeLayout = QtGui.QVBoxLayout(self.FontSizeGroupBox)
        self.FontSizeLayout.setSpacing(8)
        self.FontSizeLayout.setMargin(8)
        self.FontSizeLayout.setObjectName("FontSizeLayout")
        self.AutoResizeRadioButton = QtGui.QRadioButton(self.FontSizeGroupBox)
        self.AutoResizeRadioButton.setChecked(True)
        self.AutoResizeRadioButton.setObjectName("AutoResizeRadioButton")
        self.FontSizeLayout.addWidget(self.AutoResizeRadioButton)
        self.WrapLinesRadioButton = QtGui.QRadioButton(self.FontSizeGroupBox)
        self.WrapLinesRadioButton.setObjectName("WrapLinesRadioButton")
        self.FontSizeLayout.addWidget(self.WrapLinesRadioButton)
        self.LeftColumnLayout.addWidget(self.FontSizeGroupBox)
        self.SongDisplayGroupBox = QtGui.QGroupBox(self.LeftColumn)
        self.SongDisplayGroupBox.setObjectName("SongDisplayGroupBox")
        self.SongDisplayLayout = QtGui.QVBoxLayout(self.SongDisplayGroupBox)
        self.SongDisplayLayout.setSpacing(8)
        self.SongDisplayLayout.setMargin(8)
        self.SongDisplayLayout.setObjectName("SongDisplayLayout")
        self.EnableCreditsCheckBox = QtGui.QCheckBox(self.SongDisplayGroupBox)
        self.EnableCreditsCheckBox.setChecked(True)
        self.EnableCreditsCheckBox.setObjectName("EnableCreditsCheckBox")
        self.SongDisplayLayout.addWidget(self.EnableCreditsCheckBox)
        self.LeftColumnLayout.addWidget(self.SongDisplayGroupBox)
        self.BlankScreenGroupBox = QtGui.QGroupBox(self.LeftColumn)
        self.BlankScreenGroupBox.setObjectName("BlankScreenGroupBox")
        self.BlankScreenLayout = QtGui.QVBoxLayout(self.BlankScreenGroupBox)
        self.BlankScreenLayout.setSpacing(8)
        self.BlankScreenLayout.setMargin(8)
        self.BlankScreenLayout.setObjectName("BlankScreenLayout")
        self.WarningCheckBox = QtGui.QCheckBox(self.BlankScreenGroupBox)
        self.WarningCheckBox.setObjectName("WarningCheckBox")
        self.BlankScreenLayout.addWidget(self.WarningCheckBox)
        self.LeftColumnLayout.addWidget(self.BlankScreenGroupBox)
        self.AutoOpenGroupBox = QtGui.QGroupBox(self.LeftColumn)
        self.AutoOpenGroupBox.setObjectName("AutoOpenGroupBox")
        self.AutoOpenLayout = QtGui.QVBoxLayout(self.AutoOpenGroupBox)
        self.AutoOpenLayout.setObjectName("AutoOpenLayout")
        self.AutoOpenCheckBox = QtGui.QCheckBox(self.AutoOpenGroupBox)
        self.AutoOpenCheckBox.setObjectName("AutoOpenCheckBox")
        self.AutoOpenLayout.addWidget(self.AutoOpenCheckBox)
        self.LeftColumnLayout.addWidget(self.AutoOpenGroupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.LeftColumnLayout.addItem(spacerItem)
        self.DisplayTabLayout.addWidget(self.LeftColumn)
        self.RightColumn = QtGui.QWidget(self.DisplayTab)
        self.RightColumn.setObjectName("RightColumn")
        self.RightColumnLayout = QtGui.QVBoxLayout(self.RightColumn)
        self.RightColumnLayout.setSpacing(8)
        self.RightColumnLayout.setMargin(0)
        self.RightColumnLayout.setObjectName("RightColumnLayout")
        self.DisplayTabLayout.addWidget(self.RightColumn)

        self.MonitorGroupBox.setTitle(QtGui.QApplication.translate("SettingsForm", "Monitors", None, QtGui.QApplication.UnicodeUTF8))
        self.MonitorLabel.setText(QtGui.QApplication.translate("SettingsForm", "Select monitor for output display:", None, QtGui.QApplication.UnicodeUTF8))
        self.MonitorComboBox.setItemText(0, QtGui.QApplication.translate("SettingsForm", "Monitor 1 on X11 Windowing System", None, QtGui.QApplication.UnicodeUTF8))
        self.MonitorComboBox.setItemText(1, QtGui.QApplication.translate("SettingsForm", "Monitor 2 on X11 Windowing System", None, QtGui.QApplication.UnicodeUTF8))
        self.FontSizeGroupBox.setTitle(QtGui.QApplication.translate("SettingsForm", "Font Size", None, QtGui.QApplication.UnicodeUTF8))
        self.AutoResizeRadioButton.setText(QtGui.QApplication.translate("SettingsForm", "Automatically resize font to fit text to slide", None, QtGui.QApplication.UnicodeUTF8))
        self.WrapLinesRadioButton.setText(QtGui.QApplication.translate("SettingsForm", "Wrap long lines to keep desired font", None, QtGui.QApplication.UnicodeUTF8))
        self.SongDisplayGroupBox.setTitle(QtGui.QApplication.translate("SettingsForm", "Song Display", None, QtGui.QApplication.UnicodeUTF8))
        self.EnableCreditsCheckBox.setText(QtGui.QApplication.translate("SettingsForm", "Enable displaying of song credits", None, QtGui.QApplication.UnicodeUTF8))
        self.BlankScreenGroupBox.setTitle(QtGui.QApplication.translate("SettingsForm", "Blank Screen", None, QtGui.QApplication.UnicodeUTF8))
        self.WarningCheckBox.setText(QtGui.QApplication.translate("SettingsForm", "Show warning on startup", None, QtGui.QApplication.UnicodeUTF8))
        self.AutoOpenGroupBox.setTitle(QtGui.QApplication.translate("SettingsForm", "Auto Open Last Service", None, QtGui.QApplication.UnicodeUTF8))
        self.AutoOpenCheckBox.setText(QtGui.QApplication.translate("SettingsForm", "Automatically open the last service at startup", None, QtGui.QApplication.UnicodeUTF8))

        self.SettingsTabItem.setTabText(QtGui.QApplication.translate("SettingsForm", "General", None, QtGui.QApplication.UnicodeUTF8))

        self.SettingsTabItem.add_items(self.DisplayTab)
        return self.SettingsTabItem


    def load_settings(self):
        pass

    def save_settings(self):
        pass
