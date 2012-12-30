# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
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
The :mod:`advancedtab` provides an advanced settings facility.
"""
from datetime import datetime, timedelta
import logging
import os
import sys

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab, translate, build_icon,  Receiver, Settings
from openlp.core.lib.ui import UiStrings
from openlp.core.utils import get_images_filter, AppLocation, format_time
from openlp.core.lib import SlideLimits

log = logging.getLogger(__name__)

class AdvancedTab(SettingsTab):
    """
    The :class:`AdvancedTab` manages the advanced settings tab including the UI
    and the loading and saving of the displayed settings.
    """
    def __init__(self, parent):
        """
        Initialise the settings tab
        """
        self.displayChanged = False
        # 7 stands for now, 0 to 6 is Monday to Sunday.
        self.defaultServiceDay = 7
        # 11 o'clock is the most popular time for morning service.
        self.defaultServiceHour = 11
        self.defaultServiceMinute = 0
        self.defaultServiceName = translate('OpenLP.AdvancedTab',
            'Service %Y-%m-%d %H-%M',
            'This may not contain any of the following characters: '
            '/\\?*|<>\[\]":+\n'
            'See http://docs.python.org/library/datetime.html'
            '#strftime-strptime-behavior for more information.')
        self.defaultImage = u':/graphics/openlp-splash-screen.png'
        self.defaultColor = u'#ffffff'
        self.dataExists = False
        self.iconPath = u':/system/system_settings.png'
        advanced_translated = translate('OpenLP.AdvancedTab', 'Advanced')
        SettingsTab.__init__(self, parent, u'Advanced', advanced_translated)

    def setupUi(self):
        """
        Configure the UI elements for the tab.
        """
        self.setObjectName(u'AdvancedTab')
        SettingsTab.setupUi(self)
        self.uiGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.uiGroupBox.setObjectName(u'uiGroupBox')
        self.uiLayout = QtGui.QFormLayout(self.uiGroupBox)
        self.uiLayout.setObjectName(u'uiLayout')
        self.recentLabel = QtGui.QLabel(self.uiGroupBox)
        self.recentLabel.setObjectName(u'recentLabel')
        self.recentSpinBox = QtGui.QSpinBox(self.uiGroupBox)
        self.recentSpinBox.setObjectName(u'recentSpinBox')
        self.recentSpinBox.setMinimum(0)
        self.uiLayout.addRow(self.recentLabel, self.recentSpinBox)
        self.mediaPluginCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.mediaPluginCheckBox.setObjectName(u'mediaPluginCheckBox')
        self.uiLayout.addRow(self.mediaPluginCheckBox)
        self.doubleClickLiveCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.doubleClickLiveCheckBox.setObjectName(u'doubleClickLiveCheckBox')
        self.uiLayout.addRow(self.doubleClickLiveCheckBox)
        self.singleClickPreviewCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.singleClickPreviewCheckBox.setObjectName(u'singleClickPreviewCheckBox')
        self.uiLayout.addRow(self.singleClickPreviewCheckBox)
        self.expandServiceItemCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.expandServiceItemCheckBox.setObjectName(u'expandServiceItemCheckBox')
        self.uiLayout.addRow(self.expandServiceItemCheckBox)
        self.enableAutoCloseCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.enableAutoCloseCheckBox.setObjectName(u'enableAutoCloseCheckBox')
        self.uiLayout.addRow(self.enableAutoCloseCheckBox)
        self.leftLayout.addWidget(self.uiGroupBox)
        # Default service name
        self.serviceNameGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.serviceNameGroupBox.setObjectName(u'serviceNameGroupBox')
        self.serviceNameLayout = QtGui.QFormLayout(self.serviceNameGroupBox)
        self.serviceNameCheckBox = QtGui.QCheckBox(self.serviceNameGroupBox)
        self.serviceNameCheckBox.setObjectName(u'serviceNameCheckBox')
        self.serviceNameLayout.setObjectName(u'serviceNameLayout')
        self.serviceNameLayout.addRow(self.serviceNameCheckBox)
        self.serviceNameTimeLabel = QtGui.QLabel(self.serviceNameGroupBox)
        self.serviceNameTimeLabel.setObjectName(u'serviceNameTimeLabel')
        self.serviceNameDay = QtGui.QComboBox(self.serviceNameGroupBox)
        self.serviceNameDay.addItems([u'', u'', u'', u'', u'', u'', u'', u''])
        self.serviceNameDay.setObjectName(u'serviceNameDay')
        self.serviceNameTime = QtGui.QTimeEdit(self.serviceNameGroupBox)
        self.serviceNameTime.setObjectName(u'serviceNameTime')
        self.serviceNameTimeHBox = QtGui.QHBoxLayout()
        self.serviceNameTimeHBox.setObjectName(u'serviceNameTimeHBox')
        self.serviceNameTimeHBox.addWidget(self.serviceNameDay)
        self.serviceNameTimeHBox.addWidget(self.serviceNameTime)
        self.serviceNameLayout.addRow(self.serviceNameTimeLabel, self.serviceNameTimeHBox)
        self.serviceNameLabel = QtGui.QLabel(self.serviceNameGroupBox)
        self.serviceNameLabel.setObjectName(u'serviceNameLabel')
        self.serviceNameEdit = QtGui.QLineEdit(self.serviceNameGroupBox)
        self.serviceNameEdit.setObjectName(u'serviceNameEdit')
        self.serviceNameEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'[^/\\?*|<>\[\]":+]+'), self))
        self.serviceNameRevertButton = QtGui.QToolButton(self.serviceNameGroupBox)
        self.serviceNameRevertButton.setObjectName(u'serviceNameRevertButton')
        self.serviceNameRevertButton.setIcon(build_icon(u':/general/general_revert.png'))
        self.serviceNameHBox = QtGui.QHBoxLayout()
        self.serviceNameHBox.setObjectName(u'serviceNameHBox')
        self.serviceNameHBox.addWidget(self.serviceNameEdit)
        self.serviceNameHBox.addWidget(self.serviceNameRevertButton)
        self.serviceNameLayout.addRow(self.serviceNameLabel, self.serviceNameHBox)
        self.serviceNameExampleLabel = QtGui.QLabel(self.serviceNameGroupBox)
        self.serviceNameExampleLabel.setObjectName(u'serviceNameExampleLabel')
        self.serviceNameExample = QtGui.QLabel(self.serviceNameGroupBox)
        self.serviceNameExample.setObjectName(u'serviceNameExample')
        self.serviceNameLayout.addRow(self.serviceNameExampleLabel, self.serviceNameExample)
        self.leftLayout.addWidget(self.serviceNameGroupBox)
        # Data Directory
        self.dataDirectoryGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.dataDirectoryGroupBox.setObjectName(u'dataDirectoryGroupBox')
        self.dataDirectoryLayout = QtGui.QFormLayout(self.dataDirectoryGroupBox)
        self.dataDirectoryLayout.setObjectName(u'dataDirectoryLayout')
        self.dataDirectoryCurrentLabel = QtGui.QLabel(self.dataDirectoryGroupBox)
        self.dataDirectoryCurrentLabel.setObjectName(            u'dataDirectoryCurrentLabel')
        self.dataDirectoryLabel = QtGui.QLabel(self.dataDirectoryGroupBox)
        self.dataDirectoryLabel.setObjectName(u'dataDirectoryLabel')
        self.dataDirectoryNewLabel = QtGui.QLabel(self.dataDirectoryGroupBox)
        self.dataDirectoryNewLabel.setObjectName(u'dataDirectoryCurrentLabel')
        self.newDataDirectoryEdit = QtGui.QLineEdit(self.dataDirectoryGroupBox)
        self.newDataDirectoryEdit.setObjectName(u'newDataDirectoryEdit')
        self.newDataDirectoryEdit.setReadOnly(True)
        self.newDataDirectoryHasFilesLabel = QtGui.QLabel(self.dataDirectoryGroupBox)
        self.newDataDirectoryHasFilesLabel.setObjectName(u'newDataDirectoryHasFilesLabel')
        self.newDataDirectoryHasFilesLabel.setWordWrap(True)
        self.dataDirectoryBrowseButton = QtGui.QToolButton(self.dataDirectoryGroupBox)
        self.dataDirectoryBrowseButton.setObjectName(u'dataDirectoryBrowseButton')
        self.dataDirectoryBrowseButton.setIcon(build_icon(u':/general/general_open.png'))
        self.dataDirectoryDefaultButton = QtGui.QToolButton(self.dataDirectoryGroupBox)
        self.dataDirectoryDefaultButton.setObjectName(u'dataDirectoryDefaultButton')
        self.dataDirectoryDefaultButton.setIcon(build_icon(u':/general/general_revert.png'))
        self.dataDirectoryCancelButton = QtGui.QToolButton(self.dataDirectoryGroupBox)
        self.dataDirectoryCancelButton.setObjectName(u'dataDirectoryCancelButton')
        self.dataDirectoryCancelButton.setIcon(build_icon(u':/general/general_delete.png'))
        self.newDataDirectoryLabelHBox = QtGui.QHBoxLayout()
        self.newDataDirectoryLabelHBox.setObjectName(u'newDataDirectoryLabelHBox')
        self.newDataDirectoryLabelHBox.addWidget(self.newDataDirectoryEdit)
        self.newDataDirectoryLabelHBox.addWidget(self.dataDirectoryBrowseButton)
        self.newDataDirectoryLabelHBox.addWidget(self.dataDirectoryDefaultButton)
        self.dataDirectoryCopyCheckHBox = QtGui.QHBoxLayout()
        self.dataDirectoryCopyCheckHBox.setObjectName(u'dataDirectoryCopyCheckHBox')
        self.dataDirectoryCopyCheckBox = QtGui.QCheckBox(self.dataDirectoryGroupBox)
        self.dataDirectoryCopyCheckBox.setObjectName(u'dataDirectoryCopyCheckBox')
        self.dataDirectoryCopyCheckHBox.addWidget(self.dataDirectoryCopyCheckBox)
        self.dataDirectoryCopyCheckHBox.addStretch()
        self.dataDirectoryCopyCheckHBox.addWidget(self.dataDirectoryCancelButton)
        self.dataDirectoryLayout.addRow(self.dataDirectoryCurrentLabel, self.dataDirectoryLabel)
        self.dataDirectoryLayout.addRow(self.dataDirectoryNewLabel, self.newDataDirectoryLabelHBox)
        self.dataDirectoryLayout.addRow(self.dataDirectoryCopyCheckHBox)
        self.dataDirectoryLayout.addRow(self.newDataDirectoryHasFilesLabel)
        self.leftLayout.addWidget(self.dataDirectoryGroupBox)
        self.leftLayout.addStretch()
        # Default Image
        self.defaultImageGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.defaultImageGroupBox.setObjectName(u'defaultImageGroupBox')
        self.defaultImageLayout = QtGui.QFormLayout(self.defaultImageGroupBox)
        self.defaultImageLayout.setObjectName(u'defaultImageLayout')
        self.defaultColorLabel = QtGui.QLabel(self.defaultImageGroupBox)
        self.defaultColorLabel.setObjectName(u'defaultColorLabel')
        self.defaultColorButton = QtGui.QPushButton(self.defaultImageGroupBox)
        self.defaultColorButton.setObjectName(u'defaultColorButton')
        self.defaultImageLayout.addRow(self.defaultColorLabel, self.defaultColorButton)
        self.defaultFileLabel = QtGui.QLabel(self.defaultImageGroupBox)
        self.defaultFileLabel.setObjectName(u'defaultFileLabel')
        self.defaultFileEdit = QtGui.QLineEdit(self.defaultImageGroupBox)
        self.defaultFileEdit.setObjectName(u'defaultFileEdit')
        self.defaultBrowseButton = QtGui.QToolButton(self.defaultImageGroupBox)
        self.defaultBrowseButton.setObjectName(u'defaultBrowseButton')
        self.defaultBrowseButton.setIcon(build_icon(u':/general/general_open.png'))
        self.defaultRevertButton = QtGui.QToolButton(self.defaultImageGroupBox)
        self.defaultRevertButton.setObjectName(u'defaultRevertButton')
        self.defaultRevertButton.setIcon(build_icon(u':/general/general_revert.png'))
        self.defaultFileLayout = QtGui.QHBoxLayout()
        self.defaultFileLayout.setObjectName(u'defaultFileLayout')
        self.defaultFileLayout.addWidget(self.defaultFileEdit)
        self.defaultFileLayout.addWidget(self.defaultBrowseButton)
        self.defaultFileLayout.addWidget(self.defaultRevertButton)
        self.defaultImageLayout.addRow(self.defaultFileLabel, self.defaultFileLayout)
        self.rightLayout.addWidget(self.defaultImageGroupBox)
        # Hide mouse
        self.hideMouseGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.hideMouseGroupBox.setObjectName(u'hideMouseGroupBox')
        self.hideMouseLayout = QtGui.QVBoxLayout(self.hideMouseGroupBox)
        self.hideMouseLayout.setObjectName(u'hideMouseLayout')
        self.hideMouseCheckBox = QtGui.QCheckBox(self.hideMouseGroupBox)
        self.hideMouseCheckBox.setObjectName(u'hideMouseCheckBox')
        self.hideMouseLayout.addWidget(self.hideMouseCheckBox)
        self.rightLayout.addWidget(self.hideMouseGroupBox)
        # Service Item Slide Limits
        self.slideGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.slideGroupBox.setObjectName(u'slideGroupBox')
        self.slideLayout = QtGui.QVBoxLayout(self.slideGroupBox)
        self.slideLayout.setObjectName(u'slideLayout')
        self.slideLabel = QtGui.QLabel(self.slideGroupBox)
        self.slideLabel.setWordWrap(True)
        self.slideLayout.addWidget(self.slideLabel)
        self.endSlideRadioButton = QtGui.QRadioButton(self.slideGroupBox)
        self.endSlideRadioButton.setObjectName(u'endSlideRadioButton')
        self.slideLayout.addWidget(self.endSlideRadioButton)
        self.wrapSlideRadioButton = QtGui.QRadioButton(self.slideGroupBox)
        self.wrapSlideRadioButton.setObjectName(u'wrapSlideRadioButton')
        self.slideLayout.addWidget(self.wrapSlideRadioButton)
        self.nextItemRadioButton = QtGui.QRadioButton(self.slideGroupBox)
        self.nextItemRadioButton.setObjectName(u'nextItemRadioButton')
        self.slideLayout.addWidget(self.nextItemRadioButton)
        self.rightLayout.addWidget(self.slideGroupBox)
        # Workarounds
        self.workaroundGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.workaroundGroupBox.setObjectName(u'workaroundGroupBox')
        self.workaroundLayout = QtGui.QVBoxLayout(self.workaroundGroupBox)
        self.workaroundLayout.setObjectName(u'workaroundLayout')
        self.x11BypassCheckBox = QtGui.QCheckBox(self.workaroundGroupBox)
        self.x11BypassCheckBox.setObjectName(u'x11BypassCheckBox')
        self.workaroundLayout.addWidget(self.x11BypassCheckBox)
        self.alternateRowsCheckBox = QtGui.QCheckBox(self.workaroundGroupBox)
        self.alternateRowsCheckBox.setObjectName(u'alternateRowsCheckBox')
        self.workaroundLayout.addWidget(self.alternateRowsCheckBox)
        self.rightLayout.addWidget(self.workaroundGroupBox)
        self.rightLayout.addStretch()
        self.shouldUpdateServiceNameExample = False
        QtCore.QObject.connect(self.serviceNameCheckBox, QtCore.SIGNAL(u'toggled(bool)'),
            self.serviceNameCheckBoxToggled)
        QtCore.QObject.connect(self.serviceNameDay, QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onServiceNameDayChanged)
        QtCore.QObject.connect(self.serviceNameTime, QtCore.SIGNAL(u'timeChanged(QTime)'),
            self.updateServiceNameExample)
        QtCore.QObject.connect(self.serviceNameEdit, QtCore.SIGNAL(u'textChanged(QString)'),
            self.updateServiceNameExample)
        QtCore.QObject.connect(self.serviceNameRevertButton, QtCore.SIGNAL(u'clicked()'),
            self.onServiceNameRevertButtonClicked)
        QtCore.QObject.connect(self.defaultColorButton, QtCore.SIGNAL(u'clicked()'), self.onDefaultColorButtonClicked)
        QtCore.QObject.connect(self.defaultBrowseButton, QtCore.SIGNAL(u'clicked()'), self.onDefaultBrowseButtonClicked)
        QtCore.QObject.connect(self.defaultRevertButton, QtCore.SIGNAL(u'clicked()'), self.onDefaultRevertButtonClicked)
        QtCore.QObject.connect(self.x11BypassCheckBox, QtCore.SIGNAL(u'toggled(bool)'), self.onX11BypassCheckBoxToggled)
        QtCore.QObject.connect(self.alternateRowsCheckBox,
            QtCore.SIGNAL(u'toggled(bool)'), self.onAlternateRowsCheckBoxToggled)
        QtCore.QObject.connect(self.dataDirectoryBrowseButton, QtCore.SIGNAL(u'clicked()'),
            self.onDataDirectoryBrowseButtonClicked)
        QtCore.QObject.connect(self.dataDirectoryDefaultButton, QtCore.SIGNAL(u'clicked()'),
            self.onDataDirectoryDefaultButtonClicked)
        QtCore.QObject.connect(self.dataDirectoryCancelButton, QtCore.SIGNAL(u'clicked()'),
            self.onDataDirectoryCancelButtonClicked)
        QtCore.QObject.connect(self.dataDirectoryCopyCheckBox, QtCore.SIGNAL(u'toggled(bool)'),
            self.onDataDirectoryCopyCheckBoxToggled)
        QtCore.QObject.connect(self.endSlideRadioButton, QtCore.SIGNAL(u'clicked()'), self.onEndSlideButtonClicked)
        QtCore.QObject.connect(self.wrapSlideRadioButton, QtCore.SIGNAL(u'clicked()'), self.onWrapSlideButtonClicked)
        QtCore.QObject.connect(self.nextItemRadioButton, QtCore.SIGNAL(u'clicked()'), self.onnextItemButtonClicked)

    def retranslateUi(self):
        """
        Setup the interface translation strings.
        """
        self.tabTitleVisible = UiStrings().Advanced
        self.uiGroupBox.setTitle(translate('OpenLP.AdvancedTab', 'UI Settings'))
        self.dataDirectoryGroupBox.setTitle(translate('OpenLP.AdvancedTab', 'Data Location'))
        self.recentLabel.setText(translate('OpenLP.AdvancedTab', 'Number of recent files to display:'))
        self.mediaPluginCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Remember active media manager tab on startup'))
        self.doubleClickLiveCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Double-click to send items straight to live'))
        self.singleClickPreviewCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Preview items when clicked in Media Manager'))
        self.expandServiceItemCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Expand new service items on creation'))
        self.enableAutoCloseCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Enable application exit confirmation'))
        self.serviceNameGroupBox.setTitle(translate('OpenLP.AdvancedTab', 'Default Service Name'))
        self.serviceNameCheckBox.setText(translate('OpenLP.AdvancedTab', 'Enable default service name'))
        self.serviceNameTimeLabel.setText(translate('OpenLP.AdvancedTab', 'Date and Time:'))
        self.serviceNameDay.setItemText(0, translate('OpenLP.AdvancedTab', 'Monday'))
        self.serviceNameDay.setItemText(1, translate('OpenLP.AdvancedTab', 'Tuesday'))
        self.serviceNameDay.setItemText(2, translate('OpenLP.AdvancedTab', 'Wednesday'))
        self.serviceNameDay.setItemText(3, translate('OpenLP.AdvancedTab', 'Thurdsday'))
        self.serviceNameDay.setItemText(4, translate('OpenLP.AdvancedTab', 'Friday'))
        self.serviceNameDay.setItemText(5, translate('OpenLP.AdvancedTab', 'Saturday'))
        self.serviceNameDay.setItemText(6, translate('OpenLP.AdvancedTab', 'Sunday'))
        self.serviceNameDay.setItemText(7, translate('OpenLP.AdvancedTab', 'Now'))
        self.serviceNameTime.setToolTip(translate('OpenLP.AdvancedTab',
            'Time when usual service starts.'))
        self.serviceNameLabel.setText(translate('OpenLP.AdvancedTab', 'Name:'))
        self.serviceNameEdit.setToolTip(translate('OpenLP.AdvancedTab', 'Consult the OpenLP manual for usage.'))
        self.serviceNameRevertButton.setToolTip(
            translate('OpenLP.AdvancedTab', 'Revert to the default service name "%s".') % self.defaultServiceName)
        self.serviceNameExampleLabel.setText(translate('OpenLP.AdvancedTab', 'Example:'))
        self.hideMouseGroupBox.setTitle(translate('OpenLP.AdvancedTab', 'Mouse Cursor'))
        self.hideMouseCheckBox.setText(translate('OpenLP.AdvancedTab', 'Hide mouse cursor when over display window'))
        self.defaultImageGroupBox.setTitle(translate('OpenLP.AdvancedTab', 'Default Image'))
        self.defaultColorLabel.setText(translate('OpenLP.AdvancedTab', 'Background color:'))
        self.defaultColorButton.setToolTip(translate('OpenLP.AdvancedTab', 'Click to select a color.'))
        self.defaultFileLabel.setText(translate('OpenLP.AdvancedTab', 'Image file:'))
        self.defaultBrowseButton.setToolTip(translate('OpenLP.AdvancedTab', 'Browse for an image file to display.'))
        self.defaultRevertButton.setToolTip(translate('OpenLP.AdvancedTab', 'Revert to the default OpenLP logo.'))
        self.dataDirectoryCurrentLabel.setText(translate('OpenLP.AdvancedTab', 'Current path:'))
        self.dataDirectoryNewLabel.setText(translate('OpenLP.AdvancedTab', 'Custom path:'))
        self.dataDirectoryBrowseButton.setToolTip(translate('OpenLP.AdvancedTab', 'Browse for new data file location.'))
        self.dataDirectoryDefaultButton.setToolTip(
            translate('OpenLP.AdvancedTab', 'Set the data location to the default.'))
        self.dataDirectoryCancelButton.setText(translate('OpenLP.AdvancedTab', 'Cancel'))
        self.dataDirectoryCancelButton.setToolTip(
            translate('OpenLP.AdvancedTab', 'Cancel OpenLP data directory location change.'))
        self.dataDirectoryCopyCheckBox.setText(translate('OpenLP.AdvancedTab', 'Copy data to new location.'))
        self.dataDirectoryCopyCheckBox.setToolTip(translate(
            'OpenLP.AdvancedTab', 'Copy the OpenLP data files to the new location.'))
        self.newDataDirectoryHasFilesLabel.setText(
            translate('OpenLP.AdvancedTab', '<strong>WARNING:</strong> New data directory location contains '
                'OpenLP data files.  These files WILL be replaced during a copy.'))
        self.workaroundGroupBox.setTitle(translate('OpenLP.AdvancedTab', 'Workarounds'))
        self.x11BypassCheckBox.setText(translate('OpenLP.AdvancedTab','Bypass X11 Window Manager'))
        self.alternateRowsCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Disable alternating row colors in lists'))
        # Slide Limits
        self.slideGroupBox.setTitle(translate('OpenLP.GeneralTab', 'Service Item Slide Limits'))
        self.slideLabel.setText(translate('OpenLP.GeneralTab', 'Behavior of next/previous on the last/first slide:'))
        self.endSlideRadioButton.setText(translate('OpenLP.GeneralTab', '&Remain on Slide'))
        self.wrapSlideRadioButton.setText(translate('OpenLP.GeneralTab', '&Wrap around'))
        self.nextItemRadioButton.setText(translate('OpenLP.GeneralTab', '&Move to next/previous service item'))

    def load(self):
        """
        Load settings from disk.
        """
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        # The max recent files value does not have an interface and so never
        # gets actually stored in the settings therefore the default value of
        # 20 will always be used.
        self.recentSpinBox.setMaximum(settings.value(u'max recent files', 20))
        self.recentSpinBox.setValue(settings.value(u'recent file count', 4))
        self.mediaPluginCheckBox.setChecked(settings.value(u'save current plugin', False))
        self.doubleClickLiveCheckBox.setChecked(settings.value(u'double click live', False))
        self.singleClickPreviewCheckBox.setChecked(settings.value(u'single click preview', False))
        self.expandServiceItemCheckBox.setChecked(settings.value(u'expand service item', False))
        self.enableAutoCloseCheckBox.setChecked(settings.value(u'enable exit confirmation', True))
        self.hideMouseCheckBox.setChecked(settings.value(u'hide mouse', True))
        self.serviceNameDay.setCurrentIndex(settings.value(u'default service day', self.defaultServiceDay))
        self.serviceNameTime.setTime(QtCore.QTime(settings.value(u'default service hour', self.defaultServiceHour),
            settings.value(u'default service minute',self.defaultServiceMinute)))
        self.shouldUpdateServiceNameExample = True
        self.serviceNameEdit.setText(settings.value(u'default service name',
            self.defaultServiceName))
        default_service_enabled = settings.value(u'default service enabled', True)
        self.serviceNameCheckBox.setChecked(default_service_enabled)
        self.serviceNameCheckBoxToggled(default_service_enabled)
        # Fix for bug #1014422.
        x11_bypass_default = True
        if sys.platform.startswith(u'linux'):
            # Default to False on Gnome.
            x11_bypass_default = bool(not
                os.environ.get(u'GNOME_DESKTOP_SESSION_ID'))
            # Default to False on XFce
            if os.environ.get(u'DESKTOP_SESSION') == u'xfce':
                x11_bypass_default = False
        self.x11BypassCheckBox.setChecked(settings.value(u'x11 bypass wm', x11_bypass_default))
        # Fix for bug #936281.
        # Prevent the dialog displayed by the alternateRowsCheckBox to display.
        signalsBlocked = self.alternateRowsCheckBox.blockSignals(True)
        self.alternateRowsCheckBox.setChecked(settings.value(u'alternate rows', sys.platform.startswith(u'win')))
        self.alternateRowsCheckBox.blockSignals(signalsBlocked)
        self.defaultColor = settings.value(u'default color', u'#ffffff')
        self.defaultFileEdit.setText(settings.value(u'default image', u':/graphics/openlp-splash-screen.png'))
        self.slide_limits = settings.value(u'slide limits', SlideLimits.End)
        if self.slide_limits == SlideLimits.End:
            self.endSlideRadioButton.setChecked(True)
        elif self.slide_limits == SlideLimits.Wrap:
            self.wrapSlideRadioButton.setChecked(True)
        else:
            self.nextItemRadioButton.setChecked(True)
        settings.endGroup()
        self.dataDirectoryCopyCheckBox.hide()
        self.newDataDirectoryHasFilesLabel.hide()
        self.dataDirectoryCancelButton.hide()
        # Since data location can be changed, make sure the path is present.
        self.currentDataPath = AppLocation.get_data_path()
        if not os.path.exists(self.currentDataPath):
            log.error(u'Data path not found %s' % self.currentDataPath)
            answer = QtGui.QMessageBox.critical(self,
                translate('OpenLP.AdvancedTab',
                'Data Directory Error'),
                translate('OpenLP.AdvancedTab',
                'OpenLP data directory was not found\n\n%s\n\n'
                'This data directory was previously changed from the OpenLP '
                'default location.  If the new location was on removable '
                'media, that media needs to be made available.\n\n'
                'Click "No" to stop loading OpenLP. allowing you to fix '
                'the the problem.\n\n'
                'Click "Yes" to reset the data directory to the default '
                'location.').replace('%s', self.currentDataPath),
                QtGui.QMessageBox.StandardButtons(
                QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No),
                QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.No:
                log.info(u'User requested termination')
                Receiver.send_message(u'cleanup')
                sys.exit()
            # Set data location to default.
            settings.remove(u'advanced/data path')
            self.currentDataPath = AppLocation.get_data_path()
            log.warning(u'User requested data path set to default %s' % self.currentDataPath)
        self.dataDirectoryLabel.setText(os.path.abspath(self.currentDataPath))
        self.defaultColorButton.setStyleSheet(u'background-color: %s' % self.defaultColor)
        # Don't allow data directory move if running portable.
        if settings.value(u'advanced/is portable', False):
            self.dataDirectoryGroupBox.hide()

    def save(self):
        """
        Save settings to disk.
        """
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'default service enabled',
            self.serviceNameCheckBox.isChecked())
        service_name = self.serviceNameEdit.text()
        preset_is_valid = self.generateServiceNameExample()[0]
        if service_name == self.defaultServiceName or not preset_is_valid:
            settings.remove(u'default service name')
            self.serviceNameEdit.setText(service_name)
        else:
            settings.setValue(u'default service name', service_name)
        settings.setValue(u'default service day', self.serviceNameDay.currentIndex())
        settings.setValue(u'default service hour', self.serviceNameTime.time().hour())
        settings.setValue(u'default service minute', self.serviceNameTime.time().minute())
        settings.setValue(u'recent file count', self.recentSpinBox.value())
        settings.setValue(u'save current plugin', self.mediaPluginCheckBox.isChecked())
        settings.setValue(u'double click live', self.doubleClickLiveCheckBox.isChecked())
        settings.setValue(u'single click preview', self.singleClickPreviewCheckBox.isChecked())
        settings.setValue(u'expand service item', self.expandServiceItemCheckBox.isChecked())
        settings.setValue(u'enable exit confirmation', self.enableAutoCloseCheckBox.isChecked())
        settings.setValue(u'hide mouse', self.hideMouseCheckBox.isChecked())
        settings.setValue(u'x11 bypass wm', self.x11BypassCheckBox.isChecked())
        settings.setValue(u'alternate rows', self.alternateRowsCheckBox.isChecked())
        settings.setValue(u'default color', self.defaultColor)
        settings.setValue(u'default image', self.defaultFileEdit.text())
        settings.setValue(u'slide limits', self.slide_limits)
        settings.endGroup()
        if self.displayChanged:
            Receiver.send_message(u'config_screen_changed')
            self.displayChanged = False
        Receiver.send_message(u'slidecontroller_update_slide_limits')

    def cancel(self):
        # Dialogue was cancelled, remove any pending data path change.
        self.onDataDirectoryCancelButtonClicked()
        SettingsTab.cancel(self)

    def serviceNameCheckBoxToggled(self, default_service_enabled):
        self.serviceNameDay.setEnabled(default_service_enabled)
        time_enabled = default_service_enabled and self.serviceNameDay.currentIndex() is not 7
        self.serviceNameTime.setEnabled(time_enabled)
        self.serviceNameEdit.setEnabled(default_service_enabled)
        self.serviceNameRevertButton.setEnabled(default_service_enabled)

    def generateServiceNameExample(self):
        preset_is_valid = True
        if self.serviceNameDay.currentIndex() == 7:
            local_time = datetime.now()
        else:
            now = datetime.now()
            day_delta = self.serviceNameDay.currentIndex() - now.weekday()
            if day_delta < 0:
                day_delta += 7
            time = now + timedelta(days=day_delta)
            local_time = time.replace(hour = self.serviceNameTime.time().hour(),
                minute = self.serviceNameTime.time().minute())
        try:
            service_name_example = format_time(unicode(self.serviceNameEdit.text()), local_time)
        except ValueError:
            preset_is_valid = False
            service_name_example = translate('OpenLP.AdvancedTab', 'Syntax error.')
        return preset_is_valid, service_name_example

    def updateServiceNameExample(self, returned_value):
        if not self.shouldUpdateServiceNameExample:
            return
        name_example = self.generateServiceNameExample()[1]
        self.serviceNameExample.setText(name_example)

    def onServiceNameDayChanged(self, service_day):
        self.serviceNameTime.setEnabled(service_day is not 7)
        self.updateServiceNameExample(None)

    def onServiceNameRevertButtonClicked(self):
        self.serviceNameEdit.setText(self.defaultServiceName)
        self.serviceNameEdit.setFocus()

    def onDefaultColorButtonClicked(self):
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.defaultColor), self)
        if new_color.isValid():
            self.defaultColor = new_color.name()
            self.defaultColorButton.setStyleSheet(u'background-color: %s' % self.defaultColor)

    def onDefaultBrowseButtonClicked(self):
        file_filters = u'%s;;%s (*.*) (*)' % (get_images_filter(),
            UiStrings().AllFiles)
        filename = QtGui.QFileDialog.getOpenFileName(self,
            translate('OpenLP.AdvancedTab', 'Open File'), '', file_filters)
        if filename:
            self.defaultFileEdit.setText(filename)
        self.defaultFileEdit.setFocus()

    def onDataDirectoryBrowseButtonClicked(self):
        """
        Browse for a new data directory location.
        """
        old_root_path = unicode(self.dataDirectoryLabel.text())
        # Get the new directory location.
        new_data_path = unicode(QtGui.QFileDialog.getExistingDirectory(self,
            translate('OpenLP.AdvancedTab', 'Select Data Directory Location'), old_root_path,
            options = QtGui.QFileDialog.ShowDirsOnly))
        # Set the new data path.
        if new_data_path:
            new_data_path = os.path.normpath(new_data_path)
            if self.currentDataPath.lower() == new_data_path.lower():
                self.onDataDirectoryCancelButtonClicked()
                return
        else:
            return
        # Make sure they want to change the data.
        answer = QtGui.QMessageBox.question(self,
            translate('OpenLP.AdvancedTab', 'Confirm Data Directory Change'),
            translate('OpenLP.AdvancedTab', 'Are you sure you want to change the location of the OpenLP '
                'data directory to:\n\n%s\n\n '
                'The data directory will be changed when OpenLP is closed.').replace('%s', new_data_path),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No), QtGui.QMessageBox.No)
        if answer != QtGui.QMessageBox.Yes:
            return
        # Check if data already exists here.
        self.checkDataOverwrite(new_data_path)
        # Save the new location.
        Receiver.send_message(u'set_new_data_path', new_data_path)
        self.newDataDirectoryEdit.setText(new_data_path)
        self.dataDirectoryCancelButton.show()

    def onDataDirectoryDefaultButtonClicked(self):
        """
        Re-set the data directory location to the 'default' location.
        """
        new_data_path = AppLocation.get_directory(AppLocation.DataDir)
        if self.currentDataPath.lower() != new_data_path.lower():
            # Make sure they want to change the data location back to the
            # default.
            answer = QtGui.QMessageBox.question(self,
                translate('OpenLP.AdvancedTab', 'Reset Data Directory'),
                translate('OpenLP.AdvancedTab', 'Are you sure you want to change the location of the OpenLP '
                'data directory to the default location?\n\nThis location will be used after OpenLP is closed.'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No), QtGui.QMessageBox.No)
            if answer != QtGui.QMessageBox.Yes:
                return
            self.checkDataOverwrite(new_data_path)
            # Save the new location.
            Receiver.send_message(u'set_new_data_path', new_data_path)
            self.newDataDirectoryEdit.setText(os.path.abspath(new_data_path))
            self.dataDirectoryCancelButton.show()
        else:
            # We cancel the change in case user changed their mind.
            self.onDataDirectoryCancelButtonClicked()

    def onDataDirectoryCopyCheckBoxToggled(self):
        Receiver.send_message(u'set_copy_data',
            self.dataDirectoryCopyCheckBox.isChecked())
        if self.dataExists:
            if self.dataDirectoryCopyCheckBox.isChecked():
                self.newDataDirectoryHasFilesLabel.show()
            else:
                self.newDataDirectoryHasFilesLabel.hide()

    def checkDataOverwrite(self, data_path ):
        test_path = os.path.join(data_path, u'songs')
        self.dataDirectoryCopyCheckBox.show()
        if os.path.exists(test_path):
            self.dataExists = True
            # Check is they want to replace existing data.
            answer = QtGui.QMessageBox.warning(self,
                translate('OpenLP.AdvancedTab', 'Overwrite Existing Data'),
                translate('OpenLP.AdvancedTab', 'WARNING: \n\nThe location you have selected \n\n%s\n\n'
                'appears to contain OpenLP data files. Do you wish to replace these files with the current data files?'
                ).replace('%s', os.path.abspath(data_path,)),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No), QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes:
                self.dataDirectoryCopyCheckBox.setChecked(True)
                self.newDataDirectoryHasFilesLabel.show()
            else:
                self.dataDirectoryCopyCheckBox.setChecked(False)
                self.newDataDirectoryHasFilesLabel.hide()
        else:
            self.dataExists = False
            self.dataDirectoryCopyCheckBox.setChecked(True)
            self.newDataDirectoryHasFilesLabel.hide()

    def onDataDirectoryCancelButtonClicked(self):
        """
        Cancel the data directory location change
        """
        self.newDataDirectoryEdit.clear()
        self.dataDirectoryCopyCheckBox.setChecked(False)
        Receiver.send_message(u'set_new_data_path', u'')
        Receiver.send_message(u'set_copy_data', False)
        self.dataDirectoryCopyCheckBox.hide()
        self.dataDirectoryCancelButton.hide()
        self.newDataDirectoryHasFilesLabel.hide()

    def onDefaultRevertButtonClicked(self):
        self.defaultFileEdit.setText(u':/graphics/openlp-splash-screen.png')
        self.defaultFileEdit.setFocus()

    def onX11BypassCheckBoxToggled(self, checked):
        """
        Toggle X11 bypass flag on maindisplay depending on check box state.

        ``checked``
            The state of the check box (boolean).
        """
        self.displayChanged = True
        
    def onAlternateRowsCheckBoxToggled(self, checked):
        """
        Notify user about required restart.

        ``checked``
        The state of the check box (boolean).
        """
        QtGui.QMessageBox.information(self,
            translate('OpenLP.AdvancedTab', 'Restart Required'),
            translate('OpenLP.AdvancedTab',
                'This change will only take effect once OpenLP has been restarted.'))

    def onEndSlideButtonClicked(self):
        self.slide_limits = SlideLimits.End

    def onWrapSlideButtonClicked(self):
        self.slide_limits = SlideLimits.Wrap

    def onnextItemButtonClicked(self):
        self.slide_limits = SlideLimits.Next
