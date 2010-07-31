# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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
        self.generalLayout = QtGui.QHBoxLayout(self)
        self.generalLayout.setSpacing(8)
        self.generalLayout.setMargin(8)
        self.generalLayout.setObjectName(u'generalLayout')
        self.generalLeftLayout = QtGui.QVBoxLayout()
        self.generalLeftLayout.setObjectName(u'generalLeftLayout')
        self.generalLeftLayout.setSpacing(8)
        self.generalLeftLayout.setMargin(0)
        self.generalLayout.addLayout(self.generalLeftLayout)
        self.monitorGroupBox = QtGui.QGroupBox(self)
        self.monitorGroupBox.setObjectName(u'monitorGroupBox')
        self.monitorLayout = QtGui.QVBoxLayout(self.monitorGroupBox)
        self.monitorLayout.setSpacing(8)
        self.monitorLayout.setMargin(8)
        self.monitorLayout.setObjectName(u'monitorLayout')
        self.monitorLabel = QtGui.QLabel(self.monitorGroupBox)
        self.monitorLabel.setObjectName(u'monitorLabel')
        self.monitorLayout.addWidget(self.monitorLabel)
        self.monitorComboBox = QtGui.QComboBox(self.monitorGroupBox)
        self.monitorComboBox.setObjectName(u'monitorComboBox')
        self.monitorLayout.addWidget(self.monitorComboBox)
        self.displayOnMonitorCheck = QtGui.QCheckBox(self.monitorGroupBox)
        self.displayOnMonitorCheck.setObjectName(u'monitorComboBox')
        self.monitorLayout.addWidget(self.displayOnMonitorCheck)
        self.generalLeftLayout.addWidget(self.monitorGroupBox)
        self.startupGroupBox = QtGui.QGroupBox(self)
        self.startupGroupBox.setObjectName(u'startupGroupBox')
        self.startupLayout = QtGui.QVBoxLayout(self.startupGroupBox)
        self.startupLayout.setSpacing(8)
        self.startupLayout.setMargin(8)
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
        self.generalLeftLayout.addWidget(self.startupGroupBox)
        self.settingsGroupBox = QtGui.QGroupBox(self)
        self.settingsGroupBox.setObjectName(u'settingsGroupBox')
        self.settingsLayout = QtGui.QGridLayout(self.settingsGroupBox)
        self.settingsLayout.setSpacing(8)
        self.settingsLayout.setMargin(8)
        self.settingsLayout.setObjectName(u'settingsLayout')
        self.saveCheckServiceCheckBox = QtGui.QCheckBox(self.settingsGroupBox)
        self.saveCheckServiceCheckBox.setObjectName(u'saveCheckServiceCheckBox')
        self.settingsLayout.addWidget(self.saveCheckServiceCheckBox, 0, 0, 1, 2)
        self.autoPreviewCheckBox = QtGui.QCheckBox(self.settingsGroupBox)
        self.autoPreviewCheckBox.setObjectName(u'autoPreviewCheckBox')
        self.settingsLayout.addWidget(self.autoPreviewCheckBox, 1, 0, 1, 2)
        # Moved here from image tab
        self.timeoutLabel = QtGui.QLabel(self.settingsGroupBox)
        self.timeoutLabel.setObjectName("timeoutLabel")
        self.settingsLayout.addWidget(self.timeoutLabel, 2, 0, 1, 1)
        self.timeoutSpinBox = QtGui.QSpinBox(self.settingsGroupBox)
        self.timeoutSpinBox.setObjectName("timeoutSpinBox")
        self.settingsLayout.addWidget(self.timeoutSpinBox, 2, 1, 1, 1)
        self.generalLeftLayout.addWidget(self.settingsGroupBox)
        self.generalLeftSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.generalLeftLayout.addItem(self.generalLeftSpacer)
        self.generalRightLayout = QtGui.QVBoxLayout()
        self.generalRightLayout.setSpacing(8)
        self.generalRightLayout.setMargin(0)
        self.generalRightLayout.setObjectName(u'generalRightLayout')
        self.generalLayout.addLayout(self.generalRightLayout)
        self.ccliGroupBox = QtGui.QGroupBox(self)
        self.ccliGroupBox.setObjectName(u'ccliGroupBox')
        self.ccliLayout = QtGui.QGridLayout(self.ccliGroupBox)
        self.ccliLayout.setMargin(8)
        self.ccliLayout.setSpacing(8)
        self.ccliLayout.setObjectName(u'ccliLayout')
        self.numberLabel = QtGui.QLabel(self.ccliGroupBox)
        self.numberLabel.setObjectName(u'numberLabel')
        self.ccliLayout.addWidget(self.numberLabel, 0, 0, 1, 1)
        self.numberEdit = QtGui.QLineEdit(self.ccliGroupBox)
        self.numberEdit.setObjectName(u'numberEdit')
        self.ccliLayout.addWidget(self.numberEdit, 0, 1, 1, 1)
        self.usernameLabel = QtGui.QLabel(self.ccliGroupBox)
        self.usernameLabel.setObjectName(u'usernameLabel')
        self.ccliLayout.addWidget(self.usernameLabel, 1, 0, 1, 1)
        self.usernameEdit = QtGui.QLineEdit(self.ccliGroupBox)
        self.usernameEdit.setObjectName(u'usernameEdit')
        self.ccliLayout.addWidget(self.usernameEdit, 1, 1, 1, 1)
        self.passwordLabel = QtGui.QLabel(self.ccliGroupBox)
        self.passwordLabel.setObjectName(u'passwordLabel')
        self.ccliLayout.addWidget(self.passwordLabel, 2, 0, 1, 1)
        self.passwordEdit = QtGui.QLineEdit(self.ccliGroupBox)
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordEdit.setObjectName(u'passwordEdit')
        self.ccliLayout.addWidget(self.passwordEdit, 2, 1, 1, 1)
        self.generalRightLayout.addWidget(self.ccliGroupBox)
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
        self.generalRightLayout.addWidget(self.displayGroupBox)
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
        self.generalRightSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.generalRightLayout.addItem(self.generalRightSpacer)
        # Signals and slots
        QtCore.QObject.connect(self.overrideCheckBox,
            QtCore.SIGNAL(u'toggled(bool)'), self.onOverrideCheckBoxToggled)

    def retranslateUi(self):
        """
        Translate the general settings tab to the currently selected language
        """
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
        self.numberLabel.setText(
            translate('OpenLP.GeneralTab', 'CCLI number:'))
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
        for screen in self.screens.screen_list:
            screen_name = u'%s %d' % (translate('OpenLP.GeneralTab', 'Screen'),
                screen[u'number'] + 1)
            if screen[u'primary']:
                screen_name = u'%s (%s)' % (screen_name,
                    translate('OpenLP.GeneralTab', 'primary'))
            self.monitorComboBox.addItem(screen_name)
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
        self.overrideChanged = False

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
        settings.setValue(u'save prompt',
            QtCore.QVariant(self.saveCheckServiceCheckBox.isChecked()))
        settings.setValue(u'auto preview',
            QtCore.QVariant(self.autoPreviewCheckBox.isChecked()))
        settings.setValue(u'loop delay', 
            QtCore.QVariant(self.timeoutSpinBox.value()))
        Receiver.send_message(u'slidecontroller_live_spin_delay',
            self.timeoutSpinBox.value())            
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
        #Monitor Number has changed.
        if self.screens.monitor_number != self.monitorNumber:
            self.screens.monitor_number = self.monitorNumber
            self.screens.set_current_display(self.monitorNumber)
            Receiver.send_message(u'config_screen_changed')
        Receiver.send_message(u'config_updated')
        # On save update the screens as well
        self.postSetUp()

    def postSetUp(self):
        """
        Apply settings after settings tab has loaded
        """
        Receiver.send_message(u'slidecontroller_live_spin_delay',
            self.timeoutSpinBox.value())
        # Reset screens after initial definition
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
        self.overrideChanged = True
