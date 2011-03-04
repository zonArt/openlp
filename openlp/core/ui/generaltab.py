# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab, Receiver, translate
from openlp.core.lib.ui import UiStrings

log = logging.getLogger(__name__)

class ValidEdit(QtGui.QLineEdit):
    """
    Only allow numeric characters to be edited
    """
    def __init__(self, parent):
        """
        Set up Override and Validator
        """
        QtGui.QLineEdit.__init__(self, parent)
        self.setValidator(QtGui.QIntValidator(0, 9999, self))

    def validText(self):
        """
        Only return Integers. Space is 0
        """
        if self.text().isEmpty():
            return QtCore.QString(u'0')
        else:
            return self.text()


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
        # Set to True to allow PostSetup to work on application start up
        self.overrideChanged = True
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
        SettingsTab.setupUi(self)
        self.monitorGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.monitorGroupBox.setObjectName(u'monitorGroupBox')
        self.monitorLayout = QtGui.QFormLayout(self.monitorGroupBox)
        self.monitorLayout.setObjectName(u'monitorLayout')
        self.monitorLabel = QtGui.QLabel(self.monitorGroupBox)
        self.monitorLabel.setObjectName(u'monitorLabel')
        self.monitorLayout.addRow(self.monitorLabel)
        self.monitorComboBox = QtGui.QComboBox(self.monitorGroupBox)
        self.monitorComboBox.setObjectName(u'monitorComboBox')
        self.monitorLayout.addRow(self.monitorComboBox)
        self.displayOnMonitorCheck = QtGui.QCheckBox(self.monitorGroupBox)
        self.displayOnMonitorCheck.setObjectName(u'monitorComboBox')
        self.monitorLayout.addRow(self.displayOnMonitorCheck)
        self.leftLayout.addWidget(self.monitorGroupBox)
        self.startupGroupBox = QtGui.QGroupBox(self.leftColumn)
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
        self.leftLayout.addWidget(self.startupGroupBox)
        self.settingsGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.settingsGroupBox.setObjectName(u'settingsGroupBox')
        self.settingsLayout = QtGui.QFormLayout(self.settingsGroupBox)
        self.settingsLayout.setObjectName(u'settingsLayout')
        self.saveCheckServiceCheckBox = QtGui.QCheckBox(self.settingsGroupBox)
        self.saveCheckServiceCheckBox.setObjectName(u'saveCheckServiceCheckBox')
        self.settingsLayout.addRow(self.saveCheckServiceCheckBox)
        self.autoPreviewCheckBox = QtGui.QCheckBox(self.settingsGroupBox)
        self.autoPreviewCheckBox.setObjectName(u'autoPreviewCheckBox')
        self.settingsLayout.addRow(self.autoPreviewCheckBox)
        # Moved here from image tab
        self.timeoutLabel = QtGui.QLabel(self.settingsGroupBox)
        self.timeoutLabel.setObjectName(u'timeoutLabel')
        self.timeoutSpinBox = QtGui.QSpinBox(self.settingsGroupBox)
        self.timeoutSpinBox.setObjectName(u'timeoutSpinBox')
        self.settingsLayout.addRow(self.timeoutLabel, self.timeoutSpinBox)
        self.leftLayout.addWidget(self.settingsGroupBox)
        self.leftLayout.addStretch()
        self.ccliGroupBox = QtGui.QGroupBox(self.rightColumn)
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
        self.rightLayout.addWidget(self.ccliGroupBox)
        # Moved here from display tab
        self.displayGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.displayGroupBox.setObjectName(u'displayGroupBox')
        self.displayLayout = QtGui.QGridLayout(self.displayGroupBox)
        self.displayLayout.setObjectName(u'displayLayout')
        self.currentXLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentXLabel.setObjectName(u'currentXLabel')
        self.displayLayout.addWidget(self.currentXLabel, 0, 0)
        self.currentXValueLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentXValueLabel.setObjectName(u'currentXValueLabel')
        self.displayLayout.addWidget(self.currentXValueLabel, 1, 0)
        self.currentYLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentYLabel.setObjectName(u'currentYLabel')
        self.displayLayout.addWidget(self.currentYLabel, 0, 1)
        self.currentYValueLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentYValueLabel.setObjectName(u'currentYValueLabel')
        self.displayLayout.addWidget(self.currentYValueLabel, 1, 1)
        self.currentWidthLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentWidthLabel.setObjectName(u'currentWidthLabel')
        self.displayLayout.addWidget(self.currentWidthLabel, 0, 2)
        self.currentWidthValueLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentWidthValueLabel.setObjectName(u'currentWidthValueLabel')
        self.displayLayout.addWidget(self.currentWidthValueLabel, 1, 2)
        self.currentHeightLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentHeightLabel.setObjectName(u'currentHeightLabel')
        self.displayLayout.addWidget(self.currentHeightLabel, 0, 3)
        self.currentHeightValueLabel = QtGui.QLabel(self.displayGroupBox)
        self.currentHeightValueLabel.setObjectName(u'Height')
        self.displayLayout.addWidget(self.currentHeightValueLabel, 1, 3)
        self.overrideCheckBox = QtGui.QCheckBox(self.displayGroupBox)
        self.overrideCheckBox.setObjectName(u'overrideCheckBox')
        self.displayLayout.addWidget(self.overrideCheckBox, 2, 0, 1, 4)
        self.rightLayout.addWidget(self.displayGroupBox)
        # Custom position
        self.customXLabel = QtGui.QLabel(self.displayGroupBox)
        self.customXLabel.setObjectName(u'customXLabel')
        self.displayLayout.addWidget(self.customXLabel, 3, 0)
        self.customXValueEdit = ValidEdit(self.displayGroupBox)
        self.customXValueEdit.setObjectName(u'customXValueEdit')
        self.displayLayout.addWidget(self.customXValueEdit, 4, 0)
        self.customYLabel = QtGui.QLabel(self.displayGroupBox)
        self.customYLabel.setObjectName(u'customYLabel')
        self.displayLayout.addWidget(self.customYLabel, 3, 1)
        self.customYValueEdit = ValidEdit(self.displayGroupBox)
        self.customYValueEdit.setObjectName(u'customYValueEdit')
        self.displayLayout.addWidget(self.customYValueEdit, 4, 1)
        self.customWidthLabel = QtGui.QLabel(self.displayGroupBox)
        self.customWidthLabel.setObjectName(u'customWidthLabel')
        self.displayLayout.addWidget(self.customWidthLabel, 3, 2)
        self.customWidthValueEdit = ValidEdit(self.displayGroupBox)
        self.customWidthValueEdit.setObjectName(u'customWidthValueEdit')
        self.displayLayout.addWidget(self.customWidthValueEdit, 4, 2)
        self.customHeightLabel = QtGui.QLabel(self.displayGroupBox)
        self.customHeightLabel.setObjectName(u'customHeightLabel')
        self.displayLayout.addWidget(self.customHeightLabel, 3, 3)
        self.customHeightValueEdit = ValidEdit(self.displayGroupBox)
        self.customHeightValueEdit.setObjectName(u'customHeightValueEdit')
        self.displayLayout.addWidget(self.customHeightValueEdit, 4, 3)
        self.rightLayout.addWidget(self.displayGroupBox)
        self.rightLayout.addStretch()
        # Signals and slots
        QtCore.QObject.connect(self.overrideCheckBox,
            QtCore.SIGNAL(u'toggled(bool)'), self.onOverrideCheckBoxToggled)
        QtCore.QObject.connect(self.customHeightValueEdit,
            QtCore.SIGNAL(u'textEdited(const QString&)'),
            self.onDisplayPositionChanged)
        QtCore.QObject.connect(self.customWidthValueEdit,
            QtCore.SIGNAL(u'textEdited(const QString&)'),
            self.onDisplayPositionChanged)
        QtCore.QObject.connect(self.customYValueEdit,
            QtCore.SIGNAL(u'textEdited(const QString&)'),
            self.onDisplayPositionChanged)
        QtCore.QObject.connect(self.customXValueEdit,
            QtCore.SIGNAL(u'textEdited(const QString&)'),
            self.onDisplayPositionChanged)
        # Reload the tab, as the screen resolution/count may have changed.
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_screen_changed'), self.load)

    def retranslateUi(self):
        """
        Translate the general settings tab to the currently selected language
        """
        self.tabTitleVisible = translate('OpenLP.GeneralTab', 'General')
        self.monitorGroupBox.setTitle(translate('OpenLP.GeneralTab',
            'Monitors'))
        self.monitorLabel.setText(translate('OpenLP.GeneralTab',
            'Select monitor for output display:'))
        self.displayOnMonitorCheck.setText(
            translate('OpenLP.GeneralTab', 'Display if a single screen'))
        self.startupGroupBox.setTitle(
            translate('OpenLP.GeneralTab', 'Application Startup'))
        self.warningCheckBox.setText(
            translate('OpenLP.GeneralTab', 'Show blank screen warning'))
        self.autoOpenCheckBox.setText(translate('OpenLP.GeneralTab',
            'Automatically open the last service'))
        self.showSplashCheckBox.setText(
            translate('OpenLP.GeneralTab', 'Show the splash screen'))
        self.checkForUpdatesCheckBox.setText(
            translate('OpenLP.GeneralTab', 'Check for updates to OpenLP'))
        self.settingsGroupBox.setTitle(
            translate('OpenLP.GeneralTab', 'Application Settings'))
        self.saveCheckServiceCheckBox.setText(translate('OpenLP.GeneralTab',
            'Prompt to save before starting a new service'))
        self.autoPreviewCheckBox.setText(translate('OpenLP.GeneralTab',
            'Automatically preview next item in service'))
        self.timeoutLabel.setText(translate('OpenLP.GeneralTab',
            'Slide loop delay:'))
        self.timeoutSpinBox.setSuffix(
            translate('OpenLP.GeneralTab', ' sec'))
        self.ccliGroupBox.setTitle(
            translate('OpenLP.GeneralTab', 'CCLI Details'))
        self.numberLabel.setText(UiStrings.CCLINumberLabel)
        self.usernameLabel.setText(
            translate('OpenLP.GeneralTab', 'SongSelect username:'))
        self.passwordLabel.setText(
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
        self.monitorComboBox.clear()
        for screen in self.screens.get_screen_list():
            self.monitorComboBox.addItem(screen)
        self.numberEdit.setText(unicode(settings.value(
            u'ccli number', QtCore.QVariant(u'')).toString()))
        self.usernameEdit.setText(unicode(settings.value(
            u'songselect username', QtCore.QVariant(u'')).toString()))
        self.passwordEdit.setText(unicode(settings.value(
            u'songselect password', QtCore.QVariant(u'')).toString()))
        self.saveCheckServiceCheckBox.setChecked(settings.value(u'save prompt',
            QtCore.QVariant(False)).toBool())
        self.monitorComboBox.setCurrentIndex(self.monitorNumber)
        self.displayOnMonitorCheck.setChecked(self.screens.display)
        self.warningCheckBox.setChecked(settings.value(u'blank warning',
            QtCore.QVariant(False)).toBool())
        self.autoOpenCheckBox.setChecked(settings.value(u'auto open',
            QtCore.QVariant(False)).toBool())
        self.showSplashCheckBox.setChecked(settings.value(u'show splash',
            QtCore.QVariant(True)).toBool())
        self.checkForUpdatesCheckBox.setChecked(settings.value(u'update check',
            QtCore.QVariant(True)).toBool())
        self.autoPreviewCheckBox.setChecked(settings.value(u'auto preview',
            QtCore.QVariant(False)).toBool())
        self.timeoutSpinBox.setValue(settings.value(u'loop delay',
           QtCore.QVariant(5)).toInt()[0])
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
        settings.endGroup()
        self.customXValueEdit.setEnabled(self.overrideCheckBox.isChecked())
        self.customYValueEdit.setEnabled(self.overrideCheckBox.isChecked())
        self.customHeightValueEdit.setEnabled(self.overrideCheckBox.isChecked())
        self.customWidthValueEdit.setEnabled(self.overrideCheckBox.isChecked())

    def save(self):
        """
        Save the settings from the form
        """
        self.monitorNumber = self.monitorComboBox.currentIndex()
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'monitor', QtCore.QVariant(self.monitorNumber))
        settings.setValue(u'display on monitor',
            QtCore.QVariant(self.displayOnMonitorCheck.isChecked()))
        settings.setValue(u'blank warning',
            QtCore.QVariant(self.warningCheckBox.isChecked()))
        settings.setValue(u'auto open',
            QtCore.QVariant(self.autoOpenCheckBox.isChecked()))
        settings.setValue(u'show splash',
            QtCore.QVariant(self.showSplashCheckBox.isChecked()))
        settings.setValue(u'update check',
            QtCore.QVariant(self.checkForUpdatesCheckBox.isChecked()))
        settings.setValue(u'save prompt',
            QtCore.QVariant(self.saveCheckServiceCheckBox.isChecked()))
        settings.setValue(u'auto preview',
            QtCore.QVariant(self.autoPreviewCheckBox.isChecked()))
        settings.setValue(u'loop delay',
            QtCore.QVariant(self.timeoutSpinBox.value()))
        settings.setValue(u'ccli number',
            QtCore.QVariant(self.numberEdit.displayText()))
        settings.setValue(u'songselect username',
            QtCore.QVariant(self.usernameEdit.displayText()))
        settings.setValue(u'songselect password',
            QtCore.QVariant(self.passwordEdit.displayText()))
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
        self.screens.display = self.displayOnMonitorCheck.isChecked()
        # Monitor Number has changed.
        postUpdate = False
        if self.screens.monitor_number != self.monitorNumber:
            self.screens.monitor_number = self.monitorNumber
            self.screens.set_current_display(self.monitorNumber)
            postUpdate = True
        # On save update the screens as well
        self.postSetUp(postUpdate)

    def postSetUp(self, postUpdate=False):
        """
        Apply settings after settings tab has loaded and most of the
        system so must be delayed
        """
        Receiver.send_message(u'slidecontroller_live_spin_delay',
            self.timeoutSpinBox.value())
        # Reset screens after initial definition
        if self.overrideChanged:
            self.screens.override[u'size'] = QtCore.QRect(
                int(self.customXValueEdit.validText()),
                int(self.customYValueEdit.validText()),
                int(self.customWidthValueEdit.validText()),
                int(self.customHeightValueEdit.validText()))
        if self.overrideCheckBox.isChecked():
            self.screens.set_override_display()
        else:
            self.screens.reset_current_display()
        # Order is important so be careful if you change
        if self.overrideChanged or postUpdate:
            Receiver.send_message(u'config_screen_changed')
        self.overrideChanged = False

    def onOverrideCheckBoxToggled(self, checked):
        """
        Toggle screen state depending on check box state.

        ``checked``
            The state of the check box (boolean).
        """
        self.customXValueEdit.setEnabled(checked)
        self.customYValueEdit.setEnabled(checked)
        self.customHeightValueEdit.setEnabled(checked)
        self.customWidthValueEdit.setEnabled(checked)
        self.overrideChanged = True

    def onDisplayPositionChanged(self):
        """
        Called when the width, height, x position or y position has changed.
        """
        self.overrideChanged = True
