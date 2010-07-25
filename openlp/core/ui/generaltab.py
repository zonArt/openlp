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

from openlp.core.lib import SettingsTab, Receiver, translate

class GeneralTab(SettingsTab):
    """
    GeneralTab is the general settings tab in the settings dialog.
    """
    def __init__(self, screens):
        """
        Initialise the general settings tab
        """
        self.screens = screens
        self.monitorNumber = 0
        SettingsTab.__init__(self, u'General')

    def preLoad(self):
        """
        Set up the display screen and set correct screen values.
        If not set before default to last screen.
        """
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        self.monitorNumber = settings.value(u'monitor',
            QtCore.QVariant(self.screens.display_count - 1)).toInt()[0]
        self.screens.set_current_display(self.monitorNumber)
        self.screens.monitor_number = self.monitorNumber
        self.screens.display = settings.value(
            u'display on monitor', QtCore.QVariant(True)).toBool()
        settings.endGroup()

    def setupUi(self):
        """
        Create the user interface for the general settings tab
        """
        self.setObjectName(u'GeneralTab')
        self.tabTitleVisible = translate('OpenLP.GeneralTab', 'General')
        self.GeneralLayout = QtGui.QHBoxLayout(self)
        self.GeneralLayout.setSpacing(8)
        self.GeneralLayout.setMargin(8)
        self.GeneralLayout.setObjectName(u'GeneralLayout')
        self.GeneralLeftLayout = QtGui.QVBoxLayout()
        self.GeneralLeftLayout.setObjectName(u'GeneralLeftLayout')
        self.GeneralLeftLayout.setSpacing(8)
        self.GeneralLeftLayout.setMargin(0)
        self.GeneralLayout.addLayout(self.GeneralLeftLayout)
        self.MonitorGroupBox = QtGui.QGroupBox(self)
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
        self.MonitorLayout.addWidget(self.MonitorComboBox)
        self.DisplayOnMonitorCheck = QtGui.QCheckBox(self.MonitorGroupBox)
        self.DisplayOnMonitorCheck.setObjectName(u'MonitorComboBox')
        self.MonitorLayout.addWidget(self.DisplayOnMonitorCheck)
        self.GeneralLeftLayout.addWidget(self.MonitorGroupBox)
        self.StartupGroupBox = QtGui.QGroupBox(self)
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
        self.SettingsGroupBox = QtGui.QGroupBox(self)
        self.SettingsGroupBox.setObjectName(u'SettingsGroupBox')
        self.SettingsLayout = QtGui.QVBoxLayout(self.SettingsGroupBox)
        self.SettingsLayout.setSpacing(8)
        self.SettingsLayout.setMargin(8)
        self.SettingsLayout.setObjectName(u'SettingsLayout')
        self.SaveCheckServiceCheckBox = QtGui.QCheckBox(self.SettingsGroupBox)
        self.SaveCheckServiceCheckBox.setObjectName(u'SaveCheckServiceCheckBox')
        self.SettingsLayout.addWidget(self.SaveCheckServiceCheckBox)
        self.GeneralLeftLayout.addWidget(self.SettingsGroupBox)
        self.AutoPreviewCheckBox = QtGui.QCheckBox(self.SettingsGroupBox)
        self.AutoPreviewCheckBox.setObjectName(u'AutoPreviewCheckBox')
        self.SettingsLayout.addWidget(self.AutoPreviewCheckBox)
        self.GeneralLeftLayout.addWidget(self.SettingsGroupBox)
        self.GeneralLeftSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.GeneralLeftLayout.addItem(self.GeneralLeftSpacer)
        self.GeneralRightLayout = QtGui.QVBoxLayout()
        self.GeneralRightLayout.setSpacing(8)
        self.GeneralRightLayout.setMargin(0)
        self.GeneralRightLayout.setObjectName(u'GeneralRightLayout')
        self.GeneralLayout.addLayout(self.GeneralRightLayout)
        self.CCLIGroupBox = QtGui.QGroupBox(self)
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
        # Moved here from display tab
        self.displayGroupBox = QtGui.QGroupBox(self)
        self.displayGroupBox.setObjectName(u'displayGroupBox')
        self.displayLayout = QtGui.QVBoxLayout(self.displayGroupBox)
        self.displayLayout.setSpacing(8)
        self.displayLayout.setMargin(8)
        self.displayLayout.setObjectName(u'displayLayout')
        self.currentLayout = QtGui.QHBoxLayout()
        self.currentLayout.setSpacing(8)
        self.currentLayout.setMargin(0)
        self.currentLayout.setObjectName(u'currentLayout')
        self.currentXLayout = QtGui.QVBoxLayout()
        self.currentXLayout.setSpacing(0)
        self.currentXLayout.setMargin(0)
        self.currentXLayout.setObjectName(u'currentXLayout')
        self.currentXLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentXLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentXLabel.setObjectName(u'currentXLabel')
        self.currentXLayout.addWidget(self.currentXLabel)
        self.currentXValueLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentXValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentXValueLabel.setObjectName(u'currentXValueLabel')
        self.currentXLayout.addWidget(self.currentXValueLabel)
        self.currentLayout.addLayout(self.currentXLayout)
        self.currentYLayout = QtGui.QVBoxLayout()
        self.currentYLayout.setSpacing(0)
        self.currentYLayout.setMargin(0)
        self.currentYLayout.setObjectName(u'currentYLayout')
        self.currentYLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentYLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentYLabel.setObjectName(u'currentYLabel')
        self.currentYLayout.addWidget(self.currentYLabel)
        self.currentYValueLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentYValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentYValueLabel.setObjectName(u'currentYValueLabel')
        self.currentYLayout.addWidget(self.currentYValueLabel)
        self.currentLayout.addLayout(self.currentYLayout)
        self.currentHeightLayout = QtGui.QVBoxLayout()
        self.currentHeightLayout.setSpacing(0)
        self.currentHeightLayout.setMargin(0)
        self.currentHeightLayout.setObjectName(u'currentHeightLayout')
        self.currentHeightLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentHeightLabel.setMaximumSize(QtCore.QSize(100, 16777215))
        self.currentHeightLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentHeightLabel.setObjectName(u'currentHeightLabel')
        self.currentHeightLayout.addWidget(self.currentHeightLabel)
        self.currentHeightValueLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentHeightValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentHeightValueLabel.setObjectName(u'Height')
        self.currentHeightLayout.addWidget(self.currentHeightValueLabel)
        self.currentLayout.addLayout(self.currentHeightLayout)
        self.currentWidthLayout = QtGui.QVBoxLayout()
        self.currentWidthLayout.setSpacing(0)
        self.currentWidthLayout.setMargin(0)
        self.currentWidthLayout.setObjectName(u'currentWidthLayout')
        self.currentWidthLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentWidthLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentWidthLabel.setObjectName(u'currentWidthLabel')
        self.currentWidthLayout.addWidget(self.currentWidthLabel)
        self.currentWidthValueLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentWidthValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentWidthValueLabel.setObjectName(u'currentWidthValueLabel')
        self.currentWidthLayout.addWidget(self.currentWidthValueLabel)
        self.currentLayout.addLayout(self.currentWidthLayout)
        self.displayLayout.addLayout(self.currentLayout)
        self.overrideCheckBox = QtGui.QCheckBox(self.displayGroupBox)
        self.overrideCheckBox.setObjectName(u'overrideCheckBox')
        self.displayLayout.addWidget(self.overrideCheckBox)
        self.GeneralRightLayout.addWidget(self.displayGroupBox)
        # Custom position
        self.customLayout = QtGui.QHBoxLayout()
        self.customLayout.setSpacing(8)
        self.customLayout.setMargin(0)
        self.customLayout.setObjectName(u'customLayout')
        self.customXLayout = QtGui.QVBoxLayout()
        self.customXLayout.setSpacing(0)
        self.customXLayout.setMargin(0)
        self.customXLayout.setObjectName(u'customXLayout')
        self.customXLabel = QtGui.QLabel(self.displayGroupBox)
        self.customXLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.customXLabel.setObjectName(u'customXLabel')
        self.customXLayout.addWidget(self.customXLabel)
        self.customXValueEdit = QtGui.QLineEdit(self.displayGroupBox)
        self.customXValueEdit.setObjectName(u'customXValueEdit')
        self.customXLayout.addWidget(self.customXValueEdit)
        self.customLayout.addLayout(self.customXLayout)
        self.customYLayout = QtGui.QVBoxLayout()
        self.customYLayout.setSpacing(0)
        self.customYLayout.setMargin(0)
        self.customYLayout.setObjectName(u'customYLayout')
        self.customYLabel = QtGui.QLabel(self.displayGroupBox)
        self.customYLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.customYLabel.setObjectName(u'customYLabel')
        self.customYLayout.addWidget(self.customYLabel)
        self.customYValueEdit = QtGui.QLineEdit(self.displayGroupBox)
        self.customYValueEdit.setObjectName(u'customYValueEdit')
        self.customYLayout.addWidget(self.customYValueEdit)
        self.customLayout.addLayout(self.customYLayout)
        self.customHeightLayout = QtGui.QVBoxLayout()
        self.customHeightLayout.setSpacing(0)
        self.customHeightLayout.setMargin(0)
        self.customHeightLayout.setObjectName(u'customHeightLayout')
        self.customHeightLabel = QtGui.QLabel(self.displayGroupBox)
        self.customHeightLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.customHeightLabel.setObjectName(u'customHeightLabel')
        self.customHeightLayout.addWidget(self.customHeightLabel)
        self.customHeightValueEdit = QtGui.QLineEdit(self.displayGroupBox)
        self.customHeightValueEdit.setObjectName(u'customHeightValueEdit')
        self.customHeightLayout.addWidget(self.customHeightValueEdit)
        self.customLayout.addLayout(self.customHeightLayout)
        self.customWidthLayout = QtGui.QVBoxLayout()
        self.customWidthLayout.setSpacing(0)
        self.customWidthLayout.setMargin(0)
        self.customWidthLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.customWidthLayout.setObjectName(u'customWidthLayout')
        self.customWidthLabel = QtGui.QLabel(self.displayGroupBox)
        self.customWidthLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.customWidthLabel.setObjectName(u'customWidthLabel')
        self.customWidthLayout.addWidget(self.customWidthLabel)
        self.customWidthValueEdit = QtGui.QLineEdit(self.displayGroupBox)
        self.customWidthValueEdit.setObjectName(u'customWidthValueEdit')
        self.customWidthLayout.addWidget(self.customWidthValueEdit)
        self.customLayout.addLayout(self.customWidthLayout)
        self.displayLayout.addLayout(self.customLayout)
        # Bottom spacer
        self.GeneralRightSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.GeneralRightLayout.addItem(self.GeneralRightSpacer)
        # Signals and slots
        QtCore.QObject.connect(self.overrideCheckBox,
            QtCore.SIGNAL(u'toggled(bool)'), self.onOverrideCheckBoxToggled)

    def retranslateUi(self):
        """
        Translate the general settings tab to the currently selected language
        """
        self.MonitorGroupBox.setTitle(translate('OpenLP.GeneralTab', 'Monitors'))
        self.MonitorLabel.setText(translate('OpenLP.GeneralTab',
            'Select monitor for output display:'))
        self.DisplayOnMonitorCheck.setText(
            translate('OpenLP.GeneralTab', 'Display if a single screen'))
        self.StartupGroupBox.setTitle(
            translate('OpenLP.GeneralTab', 'Application Startup'))
        self.WarningCheckBox.setText(
            translate('OpenLP.GeneralTab', 'Show blank screen warning'))
        self.AutoOpenCheckBox.setText(translate('OpenLP.GeneralTab',
            'Automatically open the last service'))
        self.ShowSplashCheckBox.setText(
            translate('OpenLP.GeneralTab', 'Show the splash screen'))
        self.SettingsGroupBox.setTitle(
            translate('OpenLP.GeneralTab', 'Application Settings'))
        self.SaveCheckServiceCheckBox.setText(translate('OpenLP.GeneralTab',
            'Prompt to save before starting a new service'))
        self.AutoPreviewCheckBox.setText(translate('OpenLP.GeneralTab',
            'Automatically preview next item in service'))
        self.CCLIGroupBox.setTitle(
            translate('OpenLP.GeneralTab', 'CCLI Details'))
        self.NumberLabel.setText(
            translate('OpenLP.GeneralTab', 'CCLI number:'))
        self.UsernameLabel.setText(
            translate('OpenLP.GeneralTab', 'SongSelect username:'))
        self.PasswordLabel.setText(
            translate('OpenLP.GeneralTab', 'SongSelect password:'))
        # Moved from display tab
        self.displayGroupBox.setTitle(
            translate('OpenLP.GeneralTab', 'Display Position'))
        self.currentXLabel.setText(translate('OpenLP.GeneralTab', 'X'))
        self.currentXValueLabel.setText(u'0')
        self.currentYLabel.setText(translate('OpenLP.GeneralTab', 'Y'))
        self.currentYValueLabel.setText(u'0')
        self.currentHeightLabel.setText(
            translate('OpenLP.GeneralTab', 'Height'))
        self.currentHeightValueLabel.setText(u'0')
        self.currentWidthLabel.setText(
            translate('OpenLP.GeneralTab', 'Width'))
        self.currentWidthValueLabel.setText(u'0')
        self.overrideCheckBox.setText(translate('OpenLP.GeneralTab',
            'Override display position'))
        self.customXLabel.setText(translate('OpenLP.GeneralTab', 'X'))
        self.customYLabel.setText(translate('OpenLP.GeneralTab', 'Y'))
        self.customHeightLabel.setText(
            translate('OpenLP.GeneralTab', 'Height'))
        self.customWidthLabel.setText(translate('OpenLP.GeneralTab', 'Width'))

    def load(self):
        """
        Load the settings to populate the form
        """
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        for screen in self.screens.screen_list:
            screen_name = u'%s %d' % (translate('OpenLP.GeneralTab', 'Screen'),
                screen[u'number'] + 1)
            if screen[u'primary']:
                screen_name = u'%s (%s)' % (screen_name,
                    translate('OpenLP.GeneralTab', 'primary'))
            self.MonitorComboBox.addItem(screen_name)
        self.NumberEdit.setText(unicode(settings.value(
            u'ccli number', QtCore.QVariant(u'')).toString()))
        self.UsernameEdit.setText(unicode(settings.value(
            u'songselect username', QtCore.QVariant(u'')).toString()))
        self.PasswordEdit.setText(unicode(settings.value(
            u'songselect password', QtCore.QVariant(u'')).toString()))
        self.SaveCheckServiceCheckBox.setChecked(settings.value(u'save prompt',
            QtCore.QVariant(False)).toBool())
        self.MonitorComboBox.setCurrentIndex(self.monitorNumber)
        self.DisplayOnMonitorCheck.setChecked(self.screens.display)
        self.WarningCheckBox.setChecked(settings.value(u'blank warning',
            QtCore.QVariant(False)).toBool())
        self.AutoOpenCheckBox.setChecked(settings.value(u'auto open',
            QtCore.QVariant(False)).toBool())
        self.ShowSplashCheckBox.setChecked(settings.value(u'show splash',
            QtCore.QVariant(True)).toBool())
        self.AutoPreviewCheckBox.setChecked(settings.value(u'auto preview',
            QtCore.QVariant(False)).toBool())
        self.currentXValueLabel.setText(
            unicode(self.screens.current[u'size'].x()))
        self.currentYValueLabel.setText(
            unicode(self.screens.current[u'size'].y()))
        self.currentHeightValueLabel.setText(
            unicode(self.screens.current[u'size'].height()))
        self.currentWidthValueLabel.setText(
            unicode(self.screens.current[u'size'].width()))
        self.overrideCheckBox.setChecked(settings.value(u'override position',
            QtCore.QVariant(False)).toBool())
        if self.overrideCheckBox.isChecked():
            self.customXValueEdit.setText(settings.value(u'x position',
                QtCore.QVariant(self.screens.current[u'size'].x())).toString())
            self.customYValueEdit.setText(settings.value(u'y position',
                QtCore.QVariant(self.screens.current[u'size'].y())).toString())
            self.customHeightValueEdit.setText(
                settings.value(u'height', QtCore.QVariant(
                self.screens.current[u'size'].height())).toString())
            self.customWidthValueEdit.setText(
                settings.value(u'width', QtCore.QVariant(
                self.screens.current[u'size'].width())).toString())
        else:
            self.customXValueEdit.setText(
                unicode(self.screens.current[u'size'].x()))
            self.customYValueEdit.setText(
                unicode(self.screens.current[u'size'].y()))
            self.customHeightValueEdit.setText(
                unicode(self.screens.current[u'size'].height()))
            self.customWidthValueEdit.setText(
                unicode(self.screens.current[u'size'].width()))
        settings.endGroup()
        self.customXValueEdit.setEnabled(self.overrideCheckBox.isChecked())
        self.customYValueEdit.setEnabled(self.overrideCheckBox.isChecked())
        self.customHeightValueEdit.setEnabled(self.overrideCheckBox.isChecked())
        self.customWidthValueEdit.setEnabled(self.overrideCheckBox.isChecked())
        self.override_changed = False

    def save(self):
        """
        Save the settings from the form
        """
        self.monitorNumber = self.MonitorComboBox.currentIndex()
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'monitor', QtCore.QVariant(self.monitorNumber))
        settings.setValue(u'display on monitor',
            QtCore.QVariant(self.DisplayOnMonitorCheck.isChecked()))
        settings.setValue(u'blank warning',
            QtCore.QVariant(self.WarningCheckBox.isChecked()))
        settings.setValue(u'auto open',
            QtCore.QVariant(self.AutoOpenCheckBox.isChecked()))
        settings.setValue(u'show splash',
            QtCore.QVariant(self.ShowSplashCheckBox.isChecked()))
        settings.setValue(u'save prompt',
            QtCore.QVariant(self.SaveCheckServiceCheckBox.isChecked()))
        settings.setValue(u'auto preview',
            QtCore.QVariant(self.AutoPreviewCheckBox.isChecked()))
        settings.setValue(u'ccli number',
            QtCore.QVariant(self.NumberEdit.displayText()))
        settings.setValue(u'songselect username',
            QtCore.QVariant(self.UsernameEdit.displayText()))
        settings.setValue(u'songselect password',
            QtCore.QVariant(self.PasswordEdit.displayText()))
        settings.setValue(u'x position',
            QtCore.QVariant(self.customXValueEdit.text()))
        settings.setValue(u'y position',
            QtCore.QVariant(self.customYValueEdit.text()))
        settings.setValue(u'height',
            QtCore.QVariant(self.customHeightValueEdit.text()))
        settings.setValue(u'width',
            QtCore.QVariant(self.customWidthValueEdit.text()))
        settings.setValue(u'override position',
            QtCore.QVariant(self.overrideCheckBox.isChecked()))
        settings.endGroup()
        self.screens.display = self.DisplayOnMonitorCheck.isChecked()
        #Monitor Number has changed.
        if self.screens.monitor_number != self.monitorNumber:
            self.screens.monitor_number = self.monitorNumber
            self.screens.set_current_display(self.monitorNumber)
            Receiver.send_message(u'config_screen_changed')
        Receiver.send_message(u'config_updated')
        # On save update the strings as well
        self.postSetUp()

    def postSetUp(self):
        """
        Set Strings after initial definition
        """
        self.screens.override[u'size'] = QtCore.QRect(
            int(self.customXValueEdit.text()),
            int(self.customYValueEdit.text()),
            int(self.customWidthValueEdit.text()),
            int(self.customHeightValueEdit.text()))
        if self.overrideCheckBox.isChecked():
            self.screens.set_override_display()
            Receiver.send_message(u'config_screen_changed')
        else:
            self.screens.reset_current_display()

    def onOverrideCheckBoxToggled(self, checked):
        """
        Toggle screen state depending on check box state
        """
        self.customXValueEdit.setEnabled(checked)
        self.customYValueEdit.setEnabled(checked)
        self.customHeightValueEdit.setEnabled(checked)
        self.customWidthValueEdit.setEnabled(checked)
        self.override_changed = True

