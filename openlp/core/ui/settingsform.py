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
from PyQt4.QtGui import QDialog

from openlp.core.lib import SettingsTab
from openlp.core.resources import *
from openlp.core.ui import AlertForm

class SettingsForm(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.first_time = True
        self.plugin_list = []
        
    def add_virtual_plugin(self, plugin):
        """
        Method to allow Core to register screens to behave like plugins
        """
        self.plugin_list.append(plugin)
        
    def receive_plugins(self, plugins):
        """
        Method to allow Plugin Manager to add plugins which want settings
        """
        print "got plugins ", plugins
        for plugin in plugins:
            self.plugin_list.append(plugin)
        print plugins
        
    def generateUi(self):
        """
        Method build UI. 
        Called by mainmenu AFTER all plugins have been installed.
        """
        if self.first_time:
            self.setupUi(self) 
            self.first_time = False

    def onSaveButton(self):
        pass
    def onResetButton(self):
        pass

    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(602, 502)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/openlp.org-icon-32.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SettingsDialog.setWindowIcon(icon)
        
        self.SettingsTabWidget = QtGui.QTabWidget(SettingsDialog)
        self.SettingsTabWidget.setGeometry(QtCore.QRect(0, 0, 669, 500))
        self.SettingsTabWidget.setObjectName("SettingsTabWidget")
        
       
        self.ThemesTab = QtGui.QWidget()
        self.ThemesTab.setObjectName("ThemesTab")
        self.ThemesTabLayout = QtGui.QHBoxLayout(self.ThemesTab)
        self.ThemesTabLayout.setSpacing(8)
        self.ThemesTabLayout.setMargin(8)
        self.ThemesTabLayout.setObjectName("ThemesTabLayout")
        self.GlobalGroupBox = QtGui.QGroupBox(self.ThemesTab)
        self.GlobalGroupBox.setObjectName("GlobalGroupBox")
        self.GlobalGroupBoxLayout = QtGui.QVBoxLayout(self.GlobalGroupBox)
        self.GlobalGroupBoxLayout.setSpacing(8)
        self.GlobalGroupBoxLayout.setMargin(8)
        self.GlobalGroupBoxLayout.setObjectName("GlobalGroupBoxLayout")
        self.DefaultComboBox = QtGui.QComboBox(self.GlobalGroupBox)
        self.DefaultComboBox.setObjectName("DefaultComboBox")
        self.DefaultComboBox.addItem(QtCore.QString())
        self.DefaultComboBox.addItem(QtCore.QString())
        self.DefaultComboBox.addItem(QtCore.QString())
        self.GlobalGroupBoxLayout.addWidget(self.DefaultComboBox)
        self.DefaultListView = QtGui.QListView(self.GlobalGroupBox)
        self.DefaultListView.setObjectName("DefaultListView")
        self.GlobalGroupBoxLayout.addWidget(self.DefaultListView)
        self.ThemesTabLayout.addWidget(self.GlobalGroupBox)
        self.LevelGroupBox = QtGui.QGroupBox(self.ThemesTab)
        self.LevelGroupBox.setObjectName("LevelGroupBox")
        self.formLayout = QtGui.QFormLayout(self.LevelGroupBox)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout.setMargin(8)
        self.formLayout.setSpacing(8)
        self.formLayout.setObjectName("formLayout")
        self.SongLevelRadioButton = QtGui.QRadioButton(self.LevelGroupBox)
        self.SongLevelRadioButton.setObjectName("SongLevelRadioButton")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.SongLevelRadioButton)
        self.SongLevelLabel = QtGui.QLabel(self.LevelGroupBox)
        self.SongLevelLabel.setWordWrap(True)
        self.SongLevelLabel.setObjectName("SongLevelLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.SongLevelLabel)
        self.ServiceLevelRadioButton = QtGui.QRadioButton(self.LevelGroupBox)
        self.ServiceLevelRadioButton.setObjectName("ServiceLevelRadioButton")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.ServiceLevelRadioButton)
        self.ServiceLevelLabel = QtGui.QLabel(self.LevelGroupBox)
        self.ServiceLevelLabel.setWordWrap(True)
        self.ServiceLevelLabel.setObjectName("ServiceLevelLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.ServiceLevelLabel)
        self.GlobalLevelRadioButton = QtGui.QRadioButton(self.LevelGroupBox)
        self.GlobalLevelRadioButton.setChecked(True)
        self.GlobalLevelRadioButton.setObjectName("GlobalLevelRadioButton")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.GlobalLevelRadioButton)
        self.GlobalLevelLabel = QtGui.QLabel(self.LevelGroupBox)
        self.GlobalLevelLabel.setWordWrap(True)
        self.GlobalLevelLabel.setObjectName("GlobalLevelLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.GlobalLevelLabel)
        self.ThemesTabLayout.addWidget(self.LevelGroupBox)
        self.SettingsTabWidget.addTab(self.ThemesTab, "")
        
        self.SlideTab = QtGui.QWidget()
        self.SlideTab.setObjectName("SlideTab")
        self.SlideLayout = QtGui.QHBoxLayout(self.SlideTab)
        self.SlideLayout.setSpacing(8)
        self.SlideLayout.setMargin(8)
        self.SlideLayout.setObjectName("SlideLayout")
        self.SlideLeftColumn = QtGui.QWidget(self.SlideTab)
        self.SlideLeftColumn.setObjectName("SlideLeftColumn")
        self.SlideLeftLayout = QtGui.QVBoxLayout(self.SlideLeftColumn)
        self.SlideLeftLayout.setSpacing(8)
        self.SlideLeftLayout.setMargin(0)
        self.SlideLeftLayout.setObjectName("SlideLeftLayout")
        spacerItem3 = QtGui.QSpacerItem(20, 94, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.SlideLeftLayout.addItem(spacerItem3)
        self.SlideLayout.addWidget(self.SlideLeftColumn)
        self.widget = QtGui.QWidget(self.SlideTab)
        self.widget.setObjectName("widget")
        self.SlideRightLayout = QtGui.QVBoxLayout(self.widget)
        self.SlideRightLayout.setSpacing(8)
        self.SlideRightLayout.setMargin(0)
        self.SlideRightLayout.setObjectName("SlideRightLayout")
        self.SongWizardGroupBox = QtGui.QGroupBox(self.widget)
        self.SongWizardGroupBox.setObjectName("SongWizardGroupBox")
        self.SongWizardLayout = QtGui.QVBoxLayout(self.SongWizardGroupBox)
        self.SongWizardLayout.setSpacing(8)
        self.SongWizardLayout.setMargin(8)
        self.SongWizardLayout.setObjectName("SongWizardLayout")
        self.SongWizardCheckBox = QtGui.QCheckBox(self.SongWizardGroupBox)
        self.SongWizardCheckBox.setChecked(True)
        self.SongWizardCheckBox.setObjectName("SongWizardCheckBox")
        self.SongWizardLayout.addWidget(self.SongWizardCheckBox)
        self.SlideRightLayout.addWidget(self.SongWizardGroupBox)
        self.SlideWrapAroundGroupBox = QtGui.QGroupBox(self.widget)
        self.SlideWrapAroundGroupBox.setObjectName("SlideWrapAroundGroupBox")
        self.SlideWrapAroundLayout = QtGui.QVBoxLayout(self.SlideWrapAroundGroupBox)
        self.SlideWrapAroundLayout.setSpacing(8)
        self.SlideWrapAroundLayout.setMargin(8)
        self.SlideWrapAroundLayout.setObjectName("SlideWrapAroundLayout")
        self.SlideWrapAroundCheckBox = QtGui.QCheckBox(self.SlideWrapAroundGroupBox)
        self.SlideWrapAroundCheckBox.setObjectName("SlideWrapAroundCheckBox")
        self.SlideWrapAroundLayout.addWidget(self.SlideWrapAroundCheckBox)
        self.SlideRightLayout.addWidget(self.SlideWrapAroundGroupBox)
        self.TimedCyclingGroupBox = QtGui.QGroupBox(self.widget)
        self.TimedCyclingGroupBox.setObjectName("TimedCyclingGroupBox")
        self.TimedCyclingLayout = QtGui.QVBoxLayout(self.TimedCyclingGroupBox)
        self.TimedCyclingLayout.setSpacing(8)
        self.TimedCyclingLayout.setMargin(8)
        self.TimedCyclingLayout.setObjectName("TimedCyclingLayout")
        self.IntervalWidget = QtGui.QWidget(self.TimedCyclingGroupBox)
        self.IntervalWidget.setObjectName("IntervalWidget")
        self.IntervalLayout = QtGui.QHBoxLayout(self.IntervalWidget)
        self.IntervalLayout.setSpacing(8)
        self.IntervalLayout.setMargin(0)
        self.IntervalLayout.setObjectName("IntervalLayout")
        self.UpdateIntervalLabel = QtGui.QLabel(self.IntervalWidget)
        self.UpdateIntervalLabel.setObjectName("UpdateIntervalLabel")
        self.IntervalLayout.addWidget(self.UpdateIntervalLabel)
        self.IntervalSpinBox = QtGui.QSpinBox(self.IntervalWidget)
        self.IntervalSpinBox.setProperty("value", QtCore.QVariant(30))
        self.IntervalSpinBox.setMaximum(600)
        self.IntervalSpinBox.setObjectName("IntervalSpinBox")
        self.IntervalLayout.addWidget(self.IntervalSpinBox)
        spacerItem4 = QtGui.QSpacerItem(139, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.IntervalLayout.addItem(spacerItem4)
        self.TimedCyclingLayout.addWidget(self.IntervalWidget)
        self.EnabledCyclingCheckBox = QtGui.QCheckBox(self.TimedCyclingGroupBox)
        self.EnabledCyclingCheckBox.setObjectName("EnabledCyclingCheckBox")
        self.TimedCyclingLayout.addWidget(self.EnabledCyclingCheckBox)
        self.SlideRightLayout.addWidget(self.TimedCyclingGroupBox)
        self.CCLIGroupBox = QtGui.QGroupBox(self.widget)
        self.CCLIGroupBox.setObjectName("CCLIGroupBox")
        self.CCLILayout = QtGui.QGridLayout(self.CCLIGroupBox)
        self.CCLILayout.setMargin(8)
        self.CCLILayout.setSpacing(8)
        self.CCLILayout.setObjectName("CCLILayout")
        self.NumberLabel = QtGui.QLabel(self.CCLIGroupBox)
        self.NumberLabel.setObjectName("NumberLabel")
        self.CCLILayout.addWidget(self.NumberLabel, 0, 0, 1, 1)
        self.NumberEdit = QtGui.QLineEdit(self.CCLIGroupBox)
        self.NumberEdit.setObjectName("NumberEdit")
        self.CCLILayout.addWidget(self.NumberEdit, 0, 1, 1, 1)
        self.UsernameLabel = QtGui.QLabel(self.CCLIGroupBox)
        self.UsernameLabel.setObjectName("UsernameLabel")
        self.CCLILayout.addWidget(self.UsernameLabel, 1, 0, 1, 1)
        self.UsernameEdit = QtGui.QLineEdit(self.CCLIGroupBox)
        self.UsernameEdit.setObjectName("UsernameEdit")
        self.CCLILayout.addWidget(self.UsernameEdit, 1, 1, 1, 1)
        self.PasswordLabel = QtGui.QLabel(self.CCLIGroupBox)
        self.PasswordLabel.setObjectName("PasswordLabel")
        self.CCLILayout.addWidget(self.PasswordLabel, 2, 0, 1, 1)
        self.PasswordEdit = QtGui.QLineEdit(self.CCLIGroupBox)
        self.PasswordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.PasswordEdit.setObjectName("PasswordEdit")
        self.CCLILayout.addWidget(self.PasswordEdit, 2, 1, 1, 1)
        self.SlideRightLayout.addWidget(self.CCLIGroupBox)
        self.SearchGroupBox_3 = QtGui.QGroupBox(self.widget)
        self.SearchGroupBox_3.setObjectName("SearchGroupBox_3")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.SearchGroupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.SearchCheckBox_3 = QtGui.QCheckBox(self.SearchGroupBox_3)
        self.SearchCheckBox_3.setChecked(True)
        self.SearchCheckBox_3.setObjectName("SearchCheckBox_3")
        self.verticalLayout_3.addWidget(self.SearchCheckBox_3)
        self.SlideRightLayout.addWidget(self.SearchGroupBox_3)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.SlideRightLayout.addItem(spacerItem5)
        self.SlideLayout.addWidget(self.widget)
        self.SettingsTabWidget.addTab(self.SlideTab, "")
        
        #### Core Code below here
        
        for plugin in self.plugin_list:
            settings_tab_item = plugin.get_settings_tab_item()
            if settings_tab_item is not None:
                self.SettingsTabWidget.addTab(settings_tab_item, settings_tab_item.tabText)
 
        self.SaveButton = QtGui.QPushButton(SettingsDialog)
        self.SaveButton.setGeometry(QtCore.QRect(490, 470, 81, 26))
        self.SaveButton.setObjectName("SaveButton")
        self.CancelButton = QtGui.QPushButton(SettingsDialog)
        self.CancelButton.setGeometry(QtCore.QRect(400, 470, 81, 26))
        self.CancelButton.setObjectName("CancelButton")
        self.ResetButton = QtGui.QPushButton(SettingsDialog)
        self.ResetButton.setGeometry(QtCore.QRect(310, 470, 81, 26))
        self.ResetButton.setObjectName("ResetButton")
        
        QtCore.QObject.connect(self.CancelButton, QtCore.SIGNAL("clicked()"), self.close)        

        self.retranslateUi(SettingsDialog)
        self.SettingsTabWidget.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QtGui.QApplication.translate("SettingsDialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))        

        self.GlobalGroupBox.setTitle(QtGui.QApplication.translate("SettingsDialog", "Global theme", None, QtGui.QApplication.UnicodeUTF8))
        self.DefaultComboBox.setItemText(0, QtGui.QApplication.translate("SettingsDialog", "African Sunset", None, QtGui.QApplication.UnicodeUTF8))
        self.DefaultComboBox.setItemText(1, QtGui.QApplication.translate("SettingsDialog", "Snowy Mountains", None, QtGui.QApplication.UnicodeUTF8))
        self.DefaultComboBox.setItemText(2, QtGui.QApplication.translate("SettingsDialog", "Wilderness", None, QtGui.QApplication.UnicodeUTF8))
        self.LevelGroupBox.setTitle(QtGui.QApplication.translate("SettingsDialog", "Theme level", None, QtGui.QApplication.UnicodeUTF8))
        self.SongLevelRadioButton.setText(QtGui.QApplication.translate("SettingsDialog", "Song level", None, QtGui.QApplication.UnicodeUTF8))
        self.SongLevelLabel.setText(QtGui.QApplication.translate("SettingsDialog", "Use the theme from each song in the database. If a song doesn\'t have a theme associated with it, then use the service\'s theme. If the service doesn\'t have a theme, then use the global theme.", None, QtGui.QApplication.UnicodeUTF8))
        self.ServiceLevelRadioButton.setText(QtGui.QApplication.translate("SettingsDialog", "Service level", None, QtGui.QApplication.UnicodeUTF8))
        self.ServiceLevelLabel.setText(QtGui.QApplication.translate("SettingsDialog", "Use the theme from the service , overriding any of the individual songs\' themes. If the service doesn\'t have a theme, then use the global theme.", None, QtGui.QApplication.UnicodeUTF8))
        self.GlobalLevelRadioButton.setText(QtGui.QApplication.translate("SettingsDialog", "Global level", None, QtGui.QApplication.UnicodeUTF8))
        self.GlobalLevelLabel.setText(QtGui.QApplication.translate("SettingsDialog", "Use the global theme, overriding any themes associated wither either the service or the songs.", None, QtGui.QApplication.UnicodeUTF8))
        self.SettingsTabWidget.setTabText(self.SettingsTabWidget.indexOf(self.ThemesTab), QtGui.QApplication.translate("SettingsDialog", "Song Theme", None, QtGui.QApplication.UnicodeUTF8))
        self.SongWizardGroupBox.setTitle(QtGui.QApplication.translate("SettingsDialog", "Song Wizard", None, QtGui.QApplication.UnicodeUTF8))
        self.SongWizardCheckBox.setText(QtGui.QApplication.translate("SettingsDialog", "Use the Song Wizard to add songs", None, QtGui.QApplication.UnicodeUTF8))
        self.SlideWrapAroundGroupBox.setTitle(QtGui.QApplication.translate("SettingsDialog", "Slide Wrap Around", None, QtGui.QApplication.UnicodeUTF8))
        self.SlideWrapAroundCheckBox.setText(QtGui.QApplication.translate("SettingsDialog", "Enable slide wrap around", None, QtGui.QApplication.UnicodeUTF8))
        self.TimedCyclingGroupBox.setTitle(QtGui.QApplication.translate("SettingsDialog", "Timed Cycling", None, QtGui.QApplication.UnicodeUTF8))
        self.UpdateIntervalLabel.setText(QtGui.QApplication.translate("SettingsDialog", "Update interval:", None, QtGui.QApplication.UnicodeUTF8))
        self.IntervalSpinBox.setSuffix(QtGui.QApplication.translate("SettingsDialog", "s", None, QtGui.QApplication.UnicodeUTF8))
        self.EnabledCyclingCheckBox.setText(QtGui.QApplication.translate("SettingsDialog", "Enable timed cycling", None, QtGui.QApplication.UnicodeUTF8))
        self.CCLIGroupBox.setTitle(QtGui.QApplication.translate("SettingsDialog", "CCLI Details", None, QtGui.QApplication.UnicodeUTF8))
        self.NumberLabel.setText(QtGui.QApplication.translate("SettingsDialog", "CCLI Number:", None, QtGui.QApplication.UnicodeUTF8))
        self.UsernameLabel.setText(QtGui.QApplication.translate("SettingsDialog", "SongSelect Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.PasswordLabel.setText(QtGui.QApplication.translate("SettingsDialog", "SongSelect Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.SearchGroupBox_3.setTitle(QtGui.QApplication.translate("SettingsDialog", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.SearchCheckBox_3.setText(QtGui.QApplication.translate("SettingsDialog", "Enabled search-as-you-type", None, QtGui.QApplication.UnicodeUTF8))
        self.SettingsTabWidget.setTabText(self.SettingsTabWidget.indexOf(self.SlideTab), QtGui.QApplication.translate("SettingsDialog", "Songs", None, QtGui.QApplication.UnicodeUTF8))
        
        self.SaveButton.setText(QtGui.QApplication.translate("SettingsDialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("SettingsDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.ResetButton.setText(QtGui.QApplication.translate("SettingsDialog", "Reset", None, QtGui.QApplication.UnicodeUTF8))

