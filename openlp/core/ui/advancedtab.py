# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab, translate, build_icon,  Receiver
from openlp.core.lib.ui import UiStrings
from openlp.core.utils import get_images_filter

class AdvancedTab(SettingsTab):
    """
    The :class:`AdvancedTab` manages the advanced settings tab including the UI
    and the loading and saving of the displayed settings.
    """
    def __init__(self, parent):
        """
        Initialise the settings tab
        """
        self.display_changed = False
        advancedTranslated = translate('OpenLP.AdvancedTab', 'Advanced')
        # 7 stands for now, 0 to 6 is Monday to Sunday.
        self.default_service_day = 7
        # 11 o'clock is the most popular time for morning service.
        self.default_service_hour = 11
        self.default_service_minute = 0
        self.default_service_name = unicode(translate('OpenLP.AdvancedTab',
            'Service %Y-%m-%d %H-%M',
            'This is the default default service name template, which can be '
            'found under Advanced in Settings, Configure OpenLP. Please do not '
            'include any of the following characters: /\\?*|<>\[\]":+\n'
            'You can use any of the directives as shown on page '
            'http://docs.python.org/library/datetime.html'
            '#strftime-strptime-behavior , but if possible, please keep '
            'the resulting string sortable by name.'))
        self.default_image = u':/graphics/openlp-splash-screen.png'
        self.default_color = u'#ffffff'
        self.icon_path = u':/system/system_settings.png'
        SettingsTab.__init__(self, parent, u'Advanced', advancedTranslated)

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
        self.singleClickPreviewCheckBox.setObjectName(
            u'singleClickPreviewCheckBox')
        self.uiLayout.addRow(self.singleClickPreviewCheckBox)
        self.expandServiceItemCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.expandServiceItemCheckBox.setObjectName(
            u'expandServiceItemCheckBox')
        self.uiLayout.addRow(self.expandServiceItemCheckBox)
        self.enableAutoCloseCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.enableAutoCloseCheckBox.setObjectName(
            u'enableAutoCloseCheckBox')
        self.uiLayout.addRow(self.enableAutoCloseCheckBox)
        self.leftLayout.addWidget(self.uiGroupBox)
        self.defaultServiceGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.defaultServiceGroupBox.setObjectName(u'defaultServiceGroupBox')
        self.defaultServiceLayout = QtGui.QFormLayout(
            self.defaultServiceGroupBox)
        self.defaultServiceCheckBox = QtGui.QCheckBox(
            self.defaultServiceGroupBox)
        self.defaultServiceCheckBox.setObjectName(u'defaultServiceCheckBox')
        self.defaultServiceLayout.setObjectName(u'defaultServiceLayout')
        self.defaultServiceLayout.addRow(self.defaultServiceCheckBox)
        self.defaultServiceTimeLabel = QtGui.QLabel(self.defaultServiceGroupBox)
        self.defaultServiceTimeLabel.setObjectName(u'defaultServiceTimeLabel')
        self.defaultServiceDay = QtGui.QComboBox(
            self.defaultServiceGroupBox)
        self.defaultServiceDay.addItems(
            [u'', u'', u'', u'', u'', u'', u'', u''])
        self.defaultServiceDay.setObjectName(
            u'defaultServiceDay')
        self.defaultServiceTime = QtGui.QTimeEdit(self.defaultServiceGroupBox)
        self.defaultServiceTime.setObjectName(u'defaultServiceTime')
        self.defaultServiceTimeHBox = QtGui.QHBoxLayout()
        self.defaultServiceTimeHBox.setObjectName(u'defaultServiceTimeHBox')
        self.defaultServiceTimeHBox.addWidget(self.defaultServiceDay)
        self.defaultServiceTimeHBox.addWidget(self.defaultServiceTime)
        self.defaultServiceLayout.addRow(self.defaultServiceTimeLabel,
            self.defaultServiceTimeHBox)
        self.defaultServiceLabel = QtGui.QLabel(self.defaultServiceGroupBox)
        self.defaultServiceLabel.setObjectName(u'defaultServiceLabel')
        self.defaultServiceName = QtGui.QLineEdit(self.defaultServiceGroupBox)
        self.defaultServiceName.setObjectName(u'defaultServiceName')
        self.defaultServiceName.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp(r'[^/\\?*|<>\[\]":+]+'), self))
        self.defaultServiceRevertButton = QtGui.QToolButton(
            self.defaultServiceGroupBox)
        self.defaultServiceRevertButton.setObjectName(
            u'defaultServiceRevertButton')
        self.defaultServiceRevertButton.setIcon(
            build_icon(u':/general/general_revert.png'))
        self.defaultServiceHBox = QtGui.QHBoxLayout()
        self.defaultServiceHBox.setObjectName(u'defaultServiceHBox')
        self.defaultServiceHBox.addWidget(self.defaultServiceName)
        self.defaultServiceHBox.addWidget(self.defaultServiceRevertButton)
        self.defaultServiceLayout.addRow(self.defaultServiceLabel,
            self.defaultServiceHBox)
        self.defaultServiceExampleLabel = QtGui.QLabel(
            self.defaultServiceGroupBox)
        self.defaultServiceExampleLabel.setObjectName(
            u'defaultServiceExampleLabel')
        self.defaultServiceExample = QtGui.QLabel(self.defaultServiceGroupBox)
        self.defaultServiceExample.setObjectName(u'defaultServiceExample')
        self.defaultServiceLayout.addRow(self.defaultServiceExampleLabel,
            self.defaultServiceExample)
        self.leftLayout.addWidget(self.defaultServiceGroupBox)
        self.leftLayout.addStretch()
        self.defaultImageGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.defaultImageGroupBox.setObjectName(u'defaultImageGroupBox')
        self.defaultImageLayout = QtGui.QFormLayout(self.defaultImageGroupBox)
        self.defaultImageLayout.setObjectName(u'defaultImageLayout')
        self.defaultColorLabel = QtGui.QLabel(self.defaultImageGroupBox)
        self.defaultColorLabel.setObjectName(u'defaultColorLabel')
        self.defaultColorButton = QtGui.QPushButton(self.defaultImageGroupBox)
        self.defaultColorButton.setObjectName(u'defaultColorButton')
        self.defaultImageLayout.addRow(self.defaultColorLabel,
            self.defaultColorButton)
        self.defaultFileLabel = QtGui.QLabel(self.defaultImageGroupBox)
        self.defaultFileLabel.setObjectName(u'defaultFileLabel')
        self.defaultFileEdit = QtGui.QLineEdit(self.defaultImageGroupBox)
        self.defaultFileEdit.setObjectName(u'defaultFileEdit')
        self.defaultBrowseButton = QtGui.QToolButton(self.defaultImageGroupBox)
        self.defaultBrowseButton.setObjectName(u'defaultBrowseButton')
        self.defaultBrowseButton.setIcon(
            build_icon(u':/general/general_open.png'))
        self.defaultRevertButton = QtGui.QToolButton(self.defaultImageGroupBox)
        self.defaultRevertButton.setObjectName(u'defaultRevertButton')
        self.defaultRevertButton.setIcon(
            build_icon(u':/general/general_revert.png'))
        self.defaultFileLayout = QtGui.QHBoxLayout()
        self.defaultFileLayout.setObjectName(u'defaultFileLayout')
        self.defaultFileLayout.addWidget(self.defaultFileEdit)
        self.defaultFileLayout.addWidget(self.defaultBrowseButton)
        self.defaultFileLayout.addWidget(self.defaultRevertButton)
        self.defaultImageLayout.addRow(self.defaultFileLabel,
            self.defaultFileLayout)
        self.rightLayout.addWidget(self.defaultImageGroupBox)
        self.hideMouseGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.hideMouseGroupBox.setObjectName(u'hideMouseGroupBox')
        self.hideMouseLayout = QtGui.QVBoxLayout(self.hideMouseGroupBox)
        self.hideMouseLayout.setObjectName(u'hideMouseLayout')
        self.hideMouseCheckBox = QtGui.QCheckBox(self.hideMouseGroupBox)
        self.hideMouseCheckBox.setObjectName(u'hideMouseCheckBox')
        self.hideMouseLayout.addWidget(self.hideMouseCheckBox)
        self.rightLayout.addWidget(self.hideMouseGroupBox)
        self.x11GroupBox = QtGui.QGroupBox(self.leftColumn)
        self.x11GroupBox.setObjectName(u'x11GroupBox')
        self.x11Layout = QtGui.QVBoxLayout(self.x11GroupBox)
        self.x11Layout.setObjectName(u'x11Layout')
        self.x11BypassCheckBox = QtGui.QCheckBox(self.x11GroupBox)
        self.x11BypassCheckBox.setObjectName(u'x11BypassCheckBox')
        self.x11Layout.addWidget(self.x11BypassCheckBox)
        self.rightLayout.addWidget(self.x11GroupBox)
        self.rightLayout.addStretch()

        QtCore.QObject.connect(self.defaultServiceCheckBox,
            QtCore.SIGNAL(u'toggled(bool)'), self.defaultServiceCheckBoxToggled)
        QtCore.QObject.connect(self.defaultServiceDay,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onDefaultServiceDayChanged)
        QtCore.QObject.connect(self.defaultServiceTime,
            QtCore.SIGNAL(u'timeChanged(QTime)'),
            self.onDefaultServiceTimeChanged)
        QtCore.QObject.connect(self.defaultServiceName,
            QtCore.SIGNAL(u'textChanged(QString)'),
            self.onDefaultServiceNameChanged)
        QtCore.QObject.connect(self.defaultServiceRevertButton,
            QtCore.SIGNAL(u'pressed()'),
            self.onDefaultServiceRevertButtonPressed)
        QtCore.QObject.connect(self.defaultColorButton,
            QtCore.SIGNAL(u'pressed()'), self.onDefaultColorButtonPressed)
        QtCore.QObject.connect(self.defaultBrowseButton,
            QtCore.SIGNAL(u'pressed()'), self.onDefaultBrowseButtonPressed)
        QtCore.QObject.connect(self.defaultRevertButton,
            QtCore.SIGNAL(u'pressed()'), self.onDefaultRevertButtonPressed)
        QtCore.QObject.connect(self.x11BypassCheckBox,
            QtCore.SIGNAL(u'toggled(bool)'), self.onX11BypassCheckBoxToggled)

    def retranslateUi(self):
        """
        Setup the interface translation strings.
        """
        self.tabTitleVisible = UiStrings().Advanced
        self.uiGroupBox.setTitle(
            translate('OpenLP.AdvancedTab', 'UI Settings'))
        self.recentLabel.setText(
            translate('OpenLP.AdvancedTab',
                'Number of recent files to display:'))
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
        self.defaultServiceGroupBox.setTitle(
            translate('OpenLP.AdvancedTab', 'Default Service Name'))
        self.defaultServiceCheckBox.setText(
            translate('OpenLP.AdvancedTab', 'Enable default service name'))
        self.defaultServiceTimeLabel.setText(
            translate('OpenLP.AdvancedTab', 'Date and Time:'))
        self.defaultServiceDay.setItemText(0,
            translate('OpenLP.AdvancedTab', 'Monday'))
        self.defaultServiceDay.setItemText(1,
            translate('OpenLP.AdvancedTab', 'Tuesday'))
        self.defaultServiceDay.setItemText(2,
            translate('OpenLP.AdvancedTab', 'Wednesday'))
        self.defaultServiceDay.setItemText(3,
            translate('OpenLP.AdvancedTab', 'Thurdsday'))
        self.defaultServiceDay.setItemText(4,
            translate('OpenLP.AdvancedTab', 'Friday'))
        self.defaultServiceDay.setItemText(5,
            translate('OpenLP.AdvancedTab', 'Saturday'))
        self.defaultServiceDay.setItemText(6,
            translate('OpenLP.AdvancedTab', 'Sunday'))
        self.defaultServiceDay.setItemText(7,
            translate('OpenLP.AdvancedTab', 'Now'))
        self.defaultServiceTime.setToolTip(translate('OpenLP.AdvancedTab',
            'Time when usual service starts.'))
        self.defaultServiceLabel.setText(
            translate('OpenLP.AdvancedTab', 'Name:'))
        self.defaultServiceName.setToolTip(translate('OpenLP.AdvancedTab',
            'Consult the OpenLP manual for usage.'))
        self.defaultServiceRevertButton.setToolTip(unicode(
            translate('OpenLP.AdvancedTab',
            'Revert to the default service name "%s".')) %
            self.default_service_name)
        self.defaultServiceExampleLabel.setText(translate('OpenLP.AdvancedTab',
            'Example:'))
        self.hideMouseGroupBox.setTitle(translate('OpenLP.AdvancedTab',
            'Mouse Cursor'))
        self.hideMouseCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Hide mouse cursor when over display window'))
        self.defaultImageGroupBox.setTitle(translate('OpenLP.AdvancedTab',
            'Default Image'))
        self.defaultColorLabel.setText(translate('OpenLP.AdvancedTab',
            'Background color:'))
        self.defaultColorButton.setToolTip(translate('OpenLP.AdvancedTab',
            'Click to select a color.'))
        self.defaultFileLabel.setText(translate('OpenLP.AdvancedTab',
            'Image file:'))
        self.defaultBrowseButton.setToolTip(translate('OpenLP.AdvancedTab',
            'Browse for an image file to display.'))
        self.defaultRevertButton.setToolTip(translate('OpenLP.AdvancedTab',
            'Revert to the default OpenLP logo.'))
        self.x11GroupBox.setTitle(translate('OpenLP.AdvancedTab',
            'X11'))
        self.x11BypassCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Bypass X11 Window Manager'))

    def load(self):
        """
        Load settings from disk.
        """
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        # The max recent files value does not have an interface and so never
        # gets actually stored in the settings therefore the default value of
        # 20 will always be used.
        self.recentSpinBox.setMaximum(QtCore.QSettings().value(
            u'max recent files', QtCore.QVariant(20)).toInt()[0])
        self.recentSpinBox.setValue(settings.value(u'recent file count',
            QtCore.QVariant(4)).toInt()[0])
        self.mediaPluginCheckBox.setChecked(
            settings.value(u'save current plugin',
            QtCore.QVariant(False)).toBool())
        self.doubleClickLiveCheckBox.setChecked(
            settings.value(u'double click live',
            QtCore.QVariant(False)).toBool())
        self.singleClickPreviewCheckBox.setChecked(
            settings.value(u'single click preview',
            QtCore.QVariant(False)).toBool())
        self.expandServiceItemCheckBox.setChecked(
            settings.value(u'expand service item',
            QtCore.QVariant(False)).toBool())
        self.enableAutoCloseCheckBox.setChecked(
            settings.value(u'enable exit confirmation',
            QtCore.QVariant(True)).toBool())
        self.hideMouseCheckBox.setChecked(
            settings.value(u'hide mouse', QtCore.QVariant(False)).toBool())
        default_service_enabled = settings.value(u'default service enabled',
            QtCore.QVariant(True)).toBool()
        self.service_day, ok = settings.value(u'default service day',
            QtCore.QVariant(self.default_service_day)).toInt()
        self.service_hour, ok = settings.value(u'default service hour',
            self.default_service_hour).toInt()
        self.service_minute, ok = settings.value(u'default service minute',
            self.default_service_minute).toInt()
        self.service_name = unicode(settings.value(u'default service name',
            self.default_service_name).toString())
        self.defaultServiceDay.setCurrentIndex(self.service_day)
        self.defaultServiceTime.setTime(
            QtCore.QTime(self.service_hour, self.service_minute))
        self.defaultServiceName.setText(self.service_name)
        self.defaultServiceCheckBox.setChecked(default_service_enabled)
        self.defaultServiceCheckBoxToggled(default_service_enabled)
        self.x11BypassCheckBox.setChecked(
            settings.value(u'x11 bypass wm', QtCore.QVariant(True)).toBool())
        self.default_color = settings.value(u'default color',
            QtCore.QVariant(u'#ffffff')).toString()
        self.defaultFileEdit.setText(settings.value(u'default image',
            QtCore.QVariant(u':/graphics/openlp-splash-screen.png'))\
            .toString())
        settings.endGroup()
        self.defaultColorButton.setStyleSheet(
            u'background-color: %s' % self.default_color)

    def save(self):
        """
        Save settings to disk.
        """
        preset_is_valid, name_example = self.generate_service_name_example()
        if not preset_is_valid:
            self.service_name = self.default_service_name
            self.defaultServiceName.setText(self.service_name)
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'default service enabled',
            self.defaultServiceCheckBox.isChecked())
        if self.service_name == self.default_service_name:
            settings.remove(u'default service name')
        else:
            settings.setValue(u'default service name', self.service_name)
        settings.setValue(u'default service day',
            self.defaultServiceDay.currentIndex())
        settings.setValue(u'default service hour',
            self.defaultServiceTime.time().hour())
        settings.setValue(u'default service minute',
            self.defaultServiceTime.time().minute())
        settings.setValue(u'recent file count',
            QtCore.QVariant(self.recentSpinBox.value()))
        settings.setValue(u'save current plugin',
            QtCore.QVariant(self.mediaPluginCheckBox.isChecked()))
        settings.setValue(u'double click live',
            QtCore.QVariant(self.doubleClickLiveCheckBox.isChecked()))
        settings.setValue(u'single click preview',
            QtCore.QVariant(self.singleClickPreviewCheckBox.isChecked()))
        settings.setValue(u'expand service item',
            QtCore.QVariant(self.expandServiceItemCheckBox.isChecked()))
        settings.setValue(u'enable exit confirmation',
            QtCore.QVariant(self.enableAutoCloseCheckBox.isChecked()))
        settings.setValue(u'hide mouse',
            QtCore.QVariant(self.hideMouseCheckBox.isChecked()))
        settings.setValue(u'x11 bypass wm',
            QtCore.QVariant(self.x11BypassCheckBox.isChecked()))
        settings.setValue(u'default color', self.default_color)
        settings.setValue(u'default image', self.defaultFileEdit.text())
        settings.endGroup()
        if self.display_changed:
            Receiver.send_message(u'config_screen_changed')
            self.display_changed = False

    def defaultServiceCheckBoxToggled(self, default_service_enabled):
        self.defaultServiceDay.setEnabled(default_service_enabled)
        time_enabled = default_service_enabled and self.service_day is not 7
        self.defaultServiceTime.setEnabled(time_enabled)
        self.defaultServiceName.setEnabled(default_service_enabled)
        self.defaultServiceRevertButton.setEnabled(default_service_enabled)

    def generate_service_name_example(self):
        preset_is_valid = True
        if self.service_day == 7:
            time = datetime.now()
        else:
            now = datetime.now()
            day_delta = self.service_day - now.weekday()
            if day_delta < 0:
                day_delta += 7
            time = now + timedelta(days=day_delta)
            time = time.replace(hour = self.service_hour,
                minute = self.service_minute)
        try:
            service_name_example = time.strftime(unicode(self.service_name))
        except ValueError:
            preset_is_valid = False
            service_name_example = translate('OpenLP.AdvancedTab',
                'Syntax error.')
        return preset_is_valid, service_name_example

    def updateServiceNameExample(self):
        preset_is_valid, name_example = self.generate_service_name_example()
        self.defaultServiceExample.setText(name_example)

    def onDefaultServiceDayChanged(self, index):
        self.service_day = index
        self.defaultServiceTime.setEnabled(self.service_day is not 7)
        self.updateServiceNameExample()

    def onDefaultServiceTimeChanged(self, time):
        self.service_hour = time.hour()
        self.service_minute = time.minute()
        self.updateServiceNameExample()

    def onDefaultServiceNameChanged(self, name):
        self.service_name = name
        self.updateServiceNameExample()

    def onDefaultServiceRevertButtonPressed(self):
        self.defaultServiceName.setText(self.default_service_name)
        self.defaultServiceName.setFocus()

    def onDefaultColorButtonPressed(self):
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.default_color), self)
        if new_color.isValid():
            self.default_color = new_color.name()
            self.defaultColorButton.setStyleSheet(
                u'background-color: %s' % self.default_color)

    def onDefaultBrowseButtonPressed(self):
        file_filters = u'%s;;%s (*.*) (*)' % (get_images_filter(),
            UiStrings().AllFiles)
        filename = QtGui.QFileDialog.getOpenFileName(self,
            translate('OpenLP.AdvancedTab', 'Open File'), '',
            file_filters)
        if filename:
            self.defaultFileEdit.setText(filename)
        self.defaultFileEdit.setFocus()

    def onDefaultRevertButtonPressed(self):
        self.defaultFileEdit.setText(u':/graphics/openlp-splash-screen.png')
        self.defaultFileEdit.setFocus()

    def onX11BypassCheckBoxToggled(self, checked):
        """
        Toggle X11 bypass flag on maindisplay depending on check box state.

        ``checked``
            The state of the check box (boolean).
        """
        self.display_changed = True
