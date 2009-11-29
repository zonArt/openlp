# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from openlp.core.lib import SettingsTab, str_to_bool

class GeneralTab(SettingsTab):
    """
    GeneralTab is the general settings tab in the settings dialog.
    """
    def __init__(self, screen_list):
        self.screen_list = screen_list
        SettingsTab.__init__(self, u'General')

    def setupUi(self):
        self.setObjectName(u'GeneralTab')
        self.tabTitleVisible = self.trUtf8('General')
        self.GeneralLayout = QtGui.QHBoxLayout(self)
        self.GeneralLayout.setSpacing(8)
        self.GeneralLayout.setMargin(8)
        self.GeneralLayout.setObjectName(u'GeneralLayout')
        self.GeneralLeftWidget = QtGui.QWidget(self)
        self.GeneralLeftWidget.setObjectName(u'GeneralLeftWidget')
        self.GeneralLeftLayout = QtGui.QVBoxLayout(self.GeneralLeftWidget)
        self.GeneralLeftLayout.setObjectName(u'GeneralLeftLayout')
        self.GeneralLeftLayout.setSpacing(8)
        self.GeneralLeftLayout.setMargin(0)
        self.MonitorGroupBox = QtGui.QGroupBox(self.GeneralLeftWidget)
        self.MonitorGroupBox.setObjectName(u'MonitorGroupBox')
        self.MonitorLayout = QtGui.QVBoxLayout(self.MonitorGroupBox)
        self.MonitorLayout.setSpacing(8)
        self.MonitorLayout.setMargin(8)
        self.MonitorLayout.setObjectName(u'MonitorLayout')
        self.MonitorLabel = QtGui.QLabel(self.MonitorGroupBox)
        self.MonitorLabel.setObjectName(u'MonitorLabel')
        self.MonitorLayout.addWidget(self.MonitorLabel)
        self.MonitorComboBox = QtGui.QComboBox(self.MonitorGroupBox)
        self.MonitorComboBox.setObjectName(u'MonitorComboBox')
        self.MonitorLayout.addWidget(self.MonitorComboBox)
        self.GeneralLeftLayout.addWidget(self.MonitorGroupBox)
        self.StartupGroupBox = QtGui.QGroupBox(self.GeneralLeftWidget)
        self.StartupGroupBox.setObjectName(u'StartupGroupBox')
        self.StartupLayout = QtGui.QVBoxLayout(self.StartupGroupBox)
        self.StartupLayout.setSpacing(8)
        self.StartupLayout.setMargin(8)
        self.StartupLayout.setObjectName(u'StartupLayout')
        self.WarningCheckBox = QtGui.QCheckBox(self.StartupGroupBox)
        self.WarningCheckBox.setObjectName(u'WarningCheckBox')
        self.StartupLayout.addWidget(self.WarningCheckBox)
        self.AutoOpenCheckBox = QtGui.QCheckBox(self.StartupGroupBox)
        self.AutoOpenCheckBox.setObjectName(u'AutoOpenCheckBox')
        self.StartupLayout.addWidget(self.AutoOpenCheckBox)
        self.ShowSplashCheckBox = QtGui.QCheckBox(self.StartupGroupBox)
        self.ShowSplashCheckBox.setObjectName(u'ShowSplashCheckBox')
        self.StartupLayout.addWidget(self.ShowSplashCheckBox)
        self.GeneralLeftLayout.addWidget(self.StartupGroupBox)
        self.SettingsGroupBox = QtGui.QGroupBox(self.GeneralLeftWidget)
        self.SettingsGroupBox.setObjectName(u'SettingsGroupBox')
        self.SettingsLayout = QtGui.QVBoxLayout(self.SettingsGroupBox)
        self.SettingsLayout.setSpacing(8)
        self.SettingsLayout.setMargin(8)
        self.SettingsLayout.setObjectName(u'SettingsLayout')
        self.SaveCheckServiceCheckBox = QtGui.QCheckBox(self.SettingsGroupBox)
        self.SaveCheckServiceCheckBox.setObjectName(u'SaveCheckServiceCheckBox')
        self.SettingsLayout.addWidget(self.SaveCheckServiceCheckBox)
        self.GeneralLeftLayout.addWidget(self.SettingsGroupBox)
        self.GeneralLeftSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.GeneralLeftLayout.addItem(self.GeneralLeftSpacer)
        self.GeneralLayout.addWidget(self.GeneralLeftWidget)
        self.GeneralRightWidget = QtGui.QWidget(self)
        self.GeneralRightWidget.setObjectName(u'GeneralRightWidget')
        self.GeneralRightLayout = QtGui.QVBoxLayout(self.GeneralRightWidget)
        self.GeneralRightLayout.setSpacing(8)
        self.GeneralRightLayout.setMargin(0)
        self.GeneralRightLayout.setObjectName(u'GeneralRightLayout')
        self.CCLIGroupBox = QtGui.QGroupBox(self.GeneralRightWidget)
        self.CCLIGroupBox.setObjectName(u'CCLIGroupBox')
        self.CCLILayout = QtGui.QGridLayout(self.CCLIGroupBox)
        self.CCLILayout.setMargin(8)
        self.CCLILayout.setSpacing(8)
        self.CCLILayout.setObjectName(u'CCLILayout')
        self.NumberLabel = QtGui.QLabel(self.CCLIGroupBox)
        self.NumberLabel.setObjectName(u'NumberLabel')
        self.CCLILayout.addWidget(self.NumberLabel, 0, 0, 1, 1)
        self.NumberEdit = QtGui.QLineEdit(self.CCLIGroupBox)
        self.NumberEdit.setObjectName(u'NumberEdit')
        self.CCLILayout.addWidget(self.NumberEdit, 0, 1, 1, 1)
        self.UsernameLabel = QtGui.QLabel(self.CCLIGroupBox)
        self.UsernameLabel.setObjectName(u'UsernameLabel')
        self.CCLILayout.addWidget(self.UsernameLabel, 1, 0, 1, 1)
        self.UsernameEdit = QtGui.QLineEdit(self.CCLIGroupBox)
        self.UsernameEdit.setObjectName(u'UsernameEdit')
        self.CCLILayout.addWidget(self.UsernameEdit, 1, 1, 1, 1)
        self.PasswordLabel = QtGui.QLabel(self.CCLIGroupBox)
        self.PasswordLabel.setObjectName(u'PasswordLabel')
        self.CCLILayout.addWidget(self.PasswordLabel, 2, 0, 1, 1)
        self.PasswordEdit = QtGui.QLineEdit(self.CCLIGroupBox)
        self.PasswordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.PasswordEdit.setObjectName(u'PasswordEdit')
        self.CCLILayout.addWidget(self.PasswordEdit, 2, 1, 1, 1)
        self.GeneralRightLayout.addWidget(self.CCLIGroupBox)
        self.GeneralRightSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.GeneralRightLayout.addItem(self.GeneralRightSpacer)
        self.GeneralLayout.addWidget(self.GeneralRightWidget)
        QtCore.QObject.connect(self.MonitorComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onMonitorComboBoxChanged)
        QtCore.QObject.connect(self.WarningCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.onWarningCheckBoxChanged)
        QtCore.QObject.connect(self.AutoOpenCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.onAutoOpenCheckBoxChanged)
        QtCore.QObject.connect(self.ShowSplashCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.onShowSplashCheckBoxChanged)
        QtCore.QObject.connect(self.SaveCheckServiceCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.onSaveCheckServiceCheckBox)
        QtCore.QObject.connect(self.NumberEdit,
            QtCore.SIGNAL(u'editingFinished()'), self.onNumberEditLostFocus)
        QtCore.QObject.connect(self.UsernameEdit,
            QtCore.SIGNAL(u'editingFinished()'), self.onUsernameEditLostFocus)
        QtCore.QObject.connect(self.PasswordEdit,
            QtCore.SIGNAL(u'editingFinished()'), self.onPasswordEditLostFocus)

    def retranslateUi(self):
        self.MonitorGroupBox.setTitle(self.trUtf8('Monitors'))
        self.MonitorLabel.setText(self.trUtf8('Select monitor for output display:'))
        self.StartupGroupBox.setTitle(self.trUtf8('Application Startup'))
        self.WarningCheckBox.setText(self.trUtf8('Show blank screen warning'))
        self.AutoOpenCheckBox.setText(self.trUtf8('Automatically open the last service'))
        self.ShowSplashCheckBox.setText(self.trUtf8('Show the splash screen'))
        self.SettingsGroupBox.setTitle(self.trUtf8('Application Settings'))
        self.SaveCheckServiceCheckBox.setText(self.trUtf8('Prompt to save Service before starting New'))
        self.CCLIGroupBox.setTitle(self.trUtf8('CCLI Details'))
        self.NumberLabel.setText(self.trUtf8('CCLI Number:'))
        self.UsernameLabel.setText(self.trUtf8('SongSelect Username:'))
        self.PasswordLabel.setText(self.trUtf8('SongSelect Password:'))

    def onMonitorComboBoxChanged(self):
        self.MonitorNumber = self.MonitorComboBox.currentIndex()

    def onAutoOpenCheckBoxChanged(self, value):
        self.AutoOpen = (value == QtCore.Qt.Checked)

    def onShowSplashCheckBoxChanged(self, value):
        self.ShowSplash = (value == QtCore.Qt.Checked)

    def onWarningCheckBoxChanged(self, value):
        self.Warning = (value == QtCore.Qt.Checked)

    def onSaveCheckServiceCheckBox(self, value):
        self.PromptSaveService = (value == QtCore.Qt.Checked)

    def onNumberEditLostFocus(self):
        self.CCLNumber = self.NumberEdit.displayText()

    def onUsernameEditLostFocus(self):
        self.Username = self.UsernameEdit.displayText()

    def onPasswordEditLostFocus(self):
        self.Password = self.PasswordEdit.displayText()

    def load(self):
        for screen in self.screen_list:
            screen_name = u'%s %d' % (self.trUtf8('Screen'), screen[u'number'] + 1)
            if screen[u'primary']:
                screen_name = u'%s (%s)' % (self.trUtf8('primary'), screen_name)
            self.MonitorComboBox.addItem(screen_name)
        # Get the configs
        self.MonitorNumber = int(self.config.get_config(u'Monitor', u'0'))
        self.Warning = str_to_bool(self.config.get_config(u'Blank Warning', u'False'))
        self.AutoOpen = str_to_bool(self.config.get_config(u'Auto Open', u'False'))
        self.ShowSplash = str_to_bool(self.config.get_config(u'show splash', u'True'))
        self.PromptSaveService = str_to_bool(self.config.get_config(u'prompt save service', u'False'))
        self.CCLNumber = unicode(self.config.get_config(u'CCL Number', u'XXX'))
        self.Username = unicode(self.config.get_config(u'User Name', u''))
        self.Password = unicode(self.config.get_config(u'Password', u''))
        self.SaveCheckServiceCheckBox.setChecked(self.PromptSaveService)
        # Set a few things up
        self.MonitorComboBox.setCurrentIndex(self.MonitorNumber)
        self.WarningCheckBox.setChecked(self.Warning)
        self.AutoOpenCheckBox.setChecked(self.AutoOpen)
        self.ShowSplashCheckBox.setChecked(self.ShowSplash)
        self.NumberEdit.setText(self.CCLNumber)
        self.UsernameEdit.setText(self.Username)
        self.PasswordEdit.setText(self.Password)

    def save(self):
        self.config.set_config(u'Monitor', self.MonitorNumber)
        self.config.set_config(u'Blank Warning', self.Warning)
        self.config.set_config(u'Auto Open', self.AutoOpen)
        self.config.set_config(u'show splash', self.ShowSplash)
        self.config.set_config(u'prompt save service', self.PromptSaveService)
        self.config.set_config(u'CCL Number', self.CCLNumber)
        self.config.set_config(u'User Name', self.Username)
        self.config.set_config(u'Password', self.Password)
