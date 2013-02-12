# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
The general tab of the configuration dialog.
"""
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, Settings, SettingsTab, ScreenList, UiStrings, translate

log = logging.getLogger(__name__)


class GeneralTab(SettingsTab):
    """
    GeneralTab is the general settings tab in the settings dialog.
    """
    def __init__(self, parent):
        """
        Initialise the general settings tab
        """
        self.screens = ScreenList()
        self.iconPath = u':/icon/openlp-logo-16x16.png'
        generalTranslated = translate('OpenLP.GeneralTab', 'General')
        SettingsTab.__init__(self, parent, u'General', generalTranslated)

    def setupUi(self):
        """
        Create the user interface for the general settings tab
        """
        self.setObjectName(u'GeneralTab')
        SettingsTab.setupUi(self)
        self.tabLayout.setStretch(1, 1)
        # Monitors
        self.monitorGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.monitorGroupBox.setObjectName(u'monitorGroupBox')
        self.monitorLayout = QtGui.QGridLayout(self.monitorGroupBox)
        self.monitorLayout.setObjectName(u'monitorLayout')
        self.monitorRadioButton = QtGui.QRadioButton(self.monitorGroupBox)
        self.monitorRadioButton.setObjectName(u'monitorRadioButton')
        self.monitorLayout.addWidget(self.monitorRadioButton, 0, 0, 1, 5)
        self.monitorComboBox = QtGui.QComboBox(self.monitorGroupBox)
        self.monitorComboBox.setObjectName(u'monitorComboBox')
        self.monitorLayout.addWidget(self.monitorComboBox, 1, 1, 1, 4)
        # Display Position
        self.overrideRadioButton = QtGui.QRadioButton(self.monitorGroupBox)
        self.overrideRadioButton.setObjectName(u'overrideRadioButton')
        self.monitorLayout.addWidget(self.overrideRadioButton, 2, 0, 1, 5)
        # Custom position
        self.customXLabel = QtGui.QLabel(self.monitorGroupBox)
        self.customXLabel.setObjectName(u'customXLabel')
        self.monitorLayout.addWidget(self.customXLabel, 3, 1)
        self.customXValueEdit = QtGui.QSpinBox(self.monitorGroupBox)
        self.customXValueEdit.setObjectName(u'customXValueEdit')
        self.customXValueEdit.setRange(-9999, 9999)
        self.monitorLayout.addWidget(self.customXValueEdit, 4, 1)
        self.customYLabel = QtGui.QLabel(self.monitorGroupBox)
        self.customYLabel.setObjectName(u'customYLabel')
        self.monitorLayout.addWidget(self.customYLabel, 3, 2)
        self.customYValueEdit = QtGui.QSpinBox(self.monitorGroupBox)
        self.customYValueEdit.setObjectName(u'customYValueEdit')
        self.customYValueEdit.setRange(-9999, 9999)
        self.monitorLayout.addWidget(self.customYValueEdit, 4, 2)
        self.customWidthLabel = QtGui.QLabel(self.monitorGroupBox)
        self.customWidthLabel.setObjectName(u'customWidthLabel')
        self.monitorLayout.addWidget(self.customWidthLabel, 3, 3)
        self.customWidthValueEdit = QtGui.QSpinBox(self.monitorGroupBox)
        self.customWidthValueEdit.setObjectName(u'customWidthValueEdit')
        self.customWidthValueEdit.setMaximum(9999)
        self.monitorLayout.addWidget(self.customWidthValueEdit, 4, 3)
        self.customHeightLabel = QtGui.QLabel(self.monitorGroupBox)
        self.customHeightLabel.setObjectName(u'customHeightLabel')
        self.monitorLayout.addWidget(self.customHeightLabel, 3, 4)
        self.customHeightValueEdit = QtGui.QSpinBox(self.monitorGroupBox)
        self.customHeightValueEdit.setObjectName(u'customHeightValueEdit')
        self.customHeightValueEdit.setMaximum(9999)
        self.monitorLayout.addWidget(self.customHeightValueEdit, 4, 4)
        self.displayOnMonitorCheck = QtGui.QCheckBox(self.monitorGroupBox)
        self.displayOnMonitorCheck.setObjectName(u'monitorComboBox')
        self.monitorLayout.addWidget(self.displayOnMonitorCheck, 5, 0, 1, 5)
        # Set up the stretchiness of each column, so that the first column
        # less stretchy (and therefore smaller) than the others
        self.monitorLayout.setColumnStretch(0, 1)
        self.monitorLayout.setColumnStretch(1, 3)
        self.monitorLayout.setColumnStretch(2, 3)
        self.monitorLayout.setColumnStretch(3, 3)
        self.monitorLayout.setColumnStretch(4, 3)
        self.leftLayout.addWidget(self.monitorGroupBox)
        # CCLI Details
        self.ccliGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.ccliGroupBox.setObjectName(u'ccliGroupBox')
        self.ccliLayout = QtGui.QFormLayout(self.ccliGroupBox)
        self.ccliLayout.setObjectName(u'ccliLayout')
        self.numberLabel = QtGui.QLabel(self.ccliGroupBox)
        self.numberLabel.setObjectName(u'numberLabel')
        self.numberEdit = QtGui.QLineEdit(self.ccliGroupBox)
        self.numberEdit.setValidator(QtGui.QIntValidator())
        self.numberEdit.setObjectName(u'numberEdit')
        self.ccliLayout.addRow(self.numberLabel, self.numberEdit)
        self.usernameLabel = QtGui.QLabel(self.ccliGroupBox)
        self.usernameLabel.setObjectName(u'usernameLabel')
        self.usernameEdit = QtGui.QLineEdit(self.ccliGroupBox)
        self.usernameEdit.setObjectName(u'usernameEdit')
        self.ccliLayout.addRow(self.usernameLabel, self.usernameEdit)
        self.passwordLabel = QtGui.QLabel(self.ccliGroupBox)
        self.passwordLabel.setObjectName(u'passwordLabel')
        self.passwordEdit = QtGui.QLineEdit(self.ccliGroupBox)
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordEdit.setObjectName(u'passwordEdit')
        self.ccliLayout.addRow(self.passwordLabel, self.passwordEdit)
        self.leftLayout.addWidget(self.ccliGroupBox)
        # Background audio
        self.audioGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.audioGroupBox.setObjectName(u'audioGroupBox')
        self.audioLayout = QtGui.QVBoxLayout(self.audioGroupBox)
        self.audioLayout.setObjectName(u'audioLayout')
        self.startPausedCheckBox = QtGui.QCheckBox(self.audioGroupBox)
        self.startPausedCheckBox.setObjectName(u'startPausedCheckBox')
        self.audioLayout.addWidget(self.startPausedCheckBox)
        self.repeatListCheckBox = QtGui.QCheckBox(self.audioGroupBox)
        self.repeatListCheckBox.setObjectName(u'repeatListCheckBox')
        self.audioLayout.addWidget(self.repeatListCheckBox)
        self.leftLayout.addWidget(self.audioGroupBox)
        self.leftLayout.addStretch()
        # Application Startup
        self.startupGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.startupGroupBox.setObjectName(u'startupGroupBox')
        self.startupLayout = QtGui.QVBoxLayout(self.startupGroupBox)
        self.startupLayout.setObjectName(u'startupLayout')
        self.warningCheckBox = QtGui.QCheckBox(self.startupGroupBox)
        self.warningCheckBox.setObjectName(u'warningCheckBox')
        self.startupLayout.addWidget(self.warningCheckBox)
        self.autoOpenCheckBox = QtGui.QCheckBox(self.startupGroupBox)
        self.autoOpenCheckBox.setObjectName(u'autoOpenCheckBox')
        self.startupLayout.addWidget(self.autoOpenCheckBox)
        self.showSplashCheckBox = QtGui.QCheckBox(self.startupGroupBox)
        self.showSplashCheckBox.setObjectName(u'showSplashCheckBox')
        self.startupLayout.addWidget(self.showSplashCheckBox)
        self.checkForUpdatesCheckBox = QtGui.QCheckBox(self.startupGroupBox)
        self.checkForUpdatesCheckBox.setObjectName(u'checkForUpdatesCheckBox')
        self.startupLayout.addWidget(self.checkForUpdatesCheckBox)
        self.rightLayout.addWidget(self.startupGroupBox)
        # Application Settings
        self.settingsGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.settingsGroupBox.setObjectName(u'settingsGroupBox')
        self.settingsLayout = QtGui.QFormLayout(self.settingsGroupBox)
        self.settingsLayout.setObjectName(u'settingsLayout')
        self.saveCheckServiceCheckBox = QtGui.QCheckBox(self.settingsGroupBox)
        self.saveCheckServiceCheckBox.setObjectName(u'saveCheckServiceCheckBox')
        self.settingsLayout.addRow(self.saveCheckServiceCheckBox)
        self.autoUnblankCheckBox = QtGui.QCheckBox(self.settingsGroupBox)
        self.autoUnblankCheckBox.setObjectName(u'autoUnblankCheckBox')
        self.settingsLayout.addRow(self.autoUnblankCheckBox)
        self.autoPreviewCheckBox = QtGui.QCheckBox(self.settingsGroupBox)
        self.autoPreviewCheckBox.setObjectName(u'autoPreviewCheckBox')
        self.settingsLayout.addRow(self.autoPreviewCheckBox)
        # Moved here from image tab
        self.timeoutLabel = QtGui.QLabel(self.settingsGroupBox)
        self.timeoutLabel.setObjectName(u'timeoutLabel')
        self.timeoutSpinBox = QtGui.QSpinBox(self.settingsGroupBox)
        self.timeoutSpinBox.setObjectName(u'timeoutSpinBox')
        self.timeoutSpinBox.setRange(1, 180)
        self.settingsLayout.addRow(self.timeoutLabel, self.timeoutSpinBox)
        self.rightLayout.addWidget(self.settingsGroupBox)
        self.rightLayout.addStretch()
        # Signals and slots
        QtCore.QObject.connect(self.overrideRadioButton, QtCore.SIGNAL(u'toggled(bool)'),
            self.onOverrideRadioButtonPressed)
        QtCore.QObject.connect(self.customHeightValueEdit, QtCore.SIGNAL(u'valueChanged(int)'), self.onDisplayChanged)
        QtCore.QObject.connect(self.customWidthValueEdit, QtCore.SIGNAL(u'valueChanged(int)'), self.onDisplayChanged)
        QtCore.QObject.connect(self.customYValueEdit, QtCore.SIGNAL(u'valueChanged(int)'), self.onDisplayChanged)
        QtCore.QObject.connect(self.customXValueEdit, QtCore.SIGNAL(u'valueChanged(int)'), self.onDisplayChanged)
        QtCore.QObject.connect(self.monitorComboBox, QtCore.SIGNAL(u'currentIndexChanged(int)'), self.onDisplayChanged)
        # Reload the tab, as the screen resolution/count may have changed.
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'config_screen_changed'), self.load)
        # Remove for now
        self.usernameLabel.setVisible(False)
        self.usernameEdit.setVisible(False)
        self.passwordLabel.setVisible(False)
        self.passwordEdit.setVisible(False)

    def retranslateUi(self):
        """
        Translate the general settings tab to the currently selected language
        """
        self.tabTitleVisible = translate('OpenLP.GeneralTab', 'General')
        self.monitorGroupBox.setTitle(translate('OpenLP.GeneralTab', 'Monitors'))
        self.monitorRadioButton.setText(translate('OpenLP.GeneralTab', 'Select monitor for output display:'))
        self.displayOnMonitorCheck.setText(translate('OpenLP.GeneralTab', 'Display if a single screen'))
        self.startupGroupBox.setTitle(translate('OpenLP.GeneralTab', 'Application Startup'))
        self.warningCheckBox.setText(translate('OpenLP.GeneralTab', 'Show blank screen warning'))
        self.autoOpenCheckBox.setText(translate('OpenLP.GeneralTab', 'Automatically open the last service'))
        self.showSplashCheckBox.setText(translate('OpenLP.GeneralTab', 'Show the splash screen'))
        self.checkForUpdatesCheckBox.setText(translate('OpenLP.GeneralTab', 'Check for updates to OpenLP'))
        self.settingsGroupBox.setTitle(translate('OpenLP.GeneralTab', 'Application Settings'))
        self.saveCheckServiceCheckBox.setText(translate('OpenLP.GeneralTab',
            'Prompt to save before starting a new service'))
        self.autoUnblankCheckBox.setText(translate('OpenLP.GeneralTab', 'Unblank display when adding new live item'))
        self.autoPreviewCheckBox.setText(translate('OpenLP.GeneralTab', 'Automatically preview next item in service'))
        self.timeoutLabel.setText(translate('OpenLP.GeneralTab', 'Timed slide interval:'))
        self.timeoutSpinBox.setSuffix(translate('OpenLP.GeneralTab', ' sec'))
        self.ccliGroupBox.setTitle(translate('OpenLP.GeneralTab', 'CCLI Details'))
        self.numberLabel.setText(UiStrings().CCLINumberLabel)
        self.usernameLabel.setText(translate('OpenLP.GeneralTab', 'SongSelect username:'))
        self.passwordLabel.setText(translate('OpenLP.GeneralTab', 'SongSelect password:'))
        # Moved from display tab
        self.overrideRadioButton.setText(translate('OpenLP.GeneralTab',
            'Override display position:'))
        self.customXLabel.setText(translate('OpenLP.GeneralTab', 'X'))
        self.customYLabel.setText(translate('OpenLP.GeneralTab', 'Y'))
        self.customHeightLabel.setText(translate('OpenLP.GeneralTab', 'Height'))
        self.customWidthLabel.setText(translate('OpenLP.GeneralTab', 'Width'))
        self.audioGroupBox.setTitle(translate('OpenLP.GeneralTab', 'Background Audio'))
        self.startPausedCheckBox.setText(translate('OpenLP.GeneralTab', 'Start background audio paused'))
        self.repeatListCheckBox.setText(translate('OpenLP.GeneralTab', 'Repeat track list'))

    def load(self):
        """
        Load the settings to populate the form
        """
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        self.monitorComboBox.clear()
        self.monitorComboBox.addItems(self.screens.get_screen_list())
        monitorNumber = settings.value(u'monitor')
        self.monitorComboBox.setCurrentIndex(monitorNumber)
        self.numberEdit.setText(settings.value(u'ccli number'))
        self.usernameEdit.setText(settings.value(u'songselect username'))
        self.passwordEdit.setText(settings.value(u'songselect password'))
        self.saveCheckServiceCheckBox.setChecked(settings.value(u'save prompt'))
        self.autoUnblankCheckBox.setChecked(settings.value(u'auto unblank'))
        self.displayOnMonitorCheck.setChecked(self.screens.display)
        self.warningCheckBox.setChecked(settings.value(u'blank warning'))
        self.autoOpenCheckBox.setChecked(settings.value(u'auto open'))
        self.showSplashCheckBox.setChecked(settings.value(u'show splash'))
        self.checkForUpdatesCheckBox.setChecked(settings.value(u'update check'))
        self.autoPreviewCheckBox.setChecked(settings.value(u'auto preview'))
        self.timeoutSpinBox.setValue(settings.value(u'loop delay'))
        self.monitorRadioButton.setChecked(not settings.value(u'override position',))
        self.overrideRadioButton.setChecked(settings.value(u'override position'))
        self.customXValueEdit.setValue(settings.value(u'x position'))
        self.customYValueEdit.setValue(settings.value(u'y position'))
        self.customHeightValueEdit.setValue(settings.value(u'height'))
        self.customWidthValueEdit.setValue(settings.value(u'width'))
        self.startPausedCheckBox.setChecked(settings.value(u'audio start paused'))
        self.repeatListCheckBox.setChecked(settings.value(u'audio repeat list'))
        settings.endGroup()
        self.monitorComboBox.setDisabled(self.overrideRadioButton.isChecked())
        self.customXValueEdit.setEnabled(self.overrideRadioButton.isChecked())
        self.customYValueEdit.setEnabled(self.overrideRadioButton.isChecked())
        self.customHeightValueEdit.setEnabled(self.overrideRadioButton.isChecked())
        self.customWidthValueEdit.setEnabled(self.overrideRadioButton.isChecked())
        self.display_changed = False
        settings.beginGroup(self.settingsSection)

    def save(self):
        """
        Save the settings from the form
        """
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'monitor', self.monitorComboBox.currentIndex())
        settings.setValue(u'display on monitor', self.displayOnMonitorCheck.isChecked())
        settings.setValue(u'blank warning', self.warningCheckBox.isChecked())
        settings.setValue(u'auto open', self.autoOpenCheckBox.isChecked())
        settings.setValue(u'show splash', self.showSplashCheckBox.isChecked())
        settings.setValue(u'update check', self.checkForUpdatesCheckBox.isChecked())
        settings.setValue(u'save prompt', self.saveCheckServiceCheckBox.isChecked())
        settings.setValue(u'auto unblank', self.autoUnblankCheckBox.isChecked())
        settings.setValue(u'auto preview', self.autoPreviewCheckBox.isChecked())
        settings.setValue(u'loop delay', self.timeoutSpinBox.value())
        settings.setValue(u'ccli number', self.numberEdit.displayText())
        settings.setValue(u'songselect username', self.usernameEdit.displayText())
        settings.setValue(u'songselect password', self.passwordEdit.displayText())
        settings.setValue(u'x position', self.customXValueEdit.value())
        settings.setValue(u'y position', self.customYValueEdit.value())
        settings.setValue(u'height', self.customHeightValueEdit.value())
        settings.setValue(u'width', self.customWidthValueEdit.value())
        settings.setValue(u'override position', self.overrideRadioButton.isChecked())
        settings.setValue(u'audio start paused', self.startPausedCheckBox.isChecked())
        settings.setValue(u'audio repeat list', self.repeatListCheckBox.isChecked())
        settings.endGroup()
        # On save update the screens as well
        self.postSetUp(True)

    def postSetUp(self, postUpdate=False):
        """
        Apply settings after settings tab has loaded and most of the
        system so must be delayed
        """
        Receiver.send_message(u'slidecontroller_live_spin_delay', self.timeoutSpinBox.value())
        # Do not continue on start up.
        if not postUpdate:
            return
        self.screens.set_current_display(self.monitorComboBox.currentIndex())
        self.screens.display = self.displayOnMonitorCheck.isChecked()
        self.screens.override[u'size'] = QtCore.QRect(
            self.customXValueEdit.value(),
            self.customYValueEdit.value(),
            self.customWidthValueEdit.value(),
            self.customHeightValueEdit.value())
        if self.overrideRadioButton.isChecked():
            self.screens.set_override_display()
        else:
            self.screens.reset_current_display()
        if self.display_changed:
            Receiver.send_message(u'config_screen_changed')
        self.display_changed = False

    def onOverrideRadioButtonPressed(self, checked):
        """
        Toggle screen state depending on check box state.

        ``checked``
            The state of the check box (boolean).
        """
        self.monitorComboBox.setDisabled(checked)
        self.customXValueEdit.setEnabled(checked)
        self.customYValueEdit.setEnabled(checked)
        self.customHeightValueEdit.setEnabled(checked)
        self.customWidthValueEdit.setEnabled(checked)
        self.display_changed = True

    def onDisplayChanged(self):
        """
        Called when the width, height, x position or y position has changed.
        """
        self.display_changed = True
