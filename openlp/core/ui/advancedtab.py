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
from openlp.core.lib import SlideLimits
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
        self.displayChanged = False
        # 7 stands for now, 0 to 6 is Monday to Sunday.
        self.defaultServiceDay = 7
        # 11 o'clock is the most popular time for morning service.
        self.defaultServiceHour = 11
        self.defaultServiceMinute = 0
        self.defaultServiceName = unicode(translate('OpenLP.AdvancedTab',
            'Service %Y-%m-%d %H-%M',
            'This is the default default service name template, which can be '
            'found under Advanced in Settings, Configure OpenLP. Please do not '
            'include any of the following characters: /\\?*|<>\[\]":+\n'
            'You can use any of the directives as shown on page '
            'http://docs.python.org/library/datetime.html'
            '#strftime-strptime-behavior , but if possible, please keep '
            'the resulting string sortable by name.'))
        self.defaultImage = u':/graphics/openlp-splash-screen.png'
        self.defaultColor = u'#ffffff'
        self.icon_path = u':/system/system_settings.png'
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
        self.serviceNameGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.serviceNameGroupBox.setObjectName(u'serviceNameGroupBox')
        self.serviceNameLayout = QtGui.QFormLayout(
            self.serviceNameGroupBox)
        self.serviceNameCheckBox = QtGui.QCheckBox(
            self.serviceNameGroupBox)
        self.serviceNameCheckBox.setObjectName(u'serviceNameCheckBox')
        self.serviceNameLayout.setObjectName(u'serviceNameLayout')
        self.serviceNameLayout.addRow(self.serviceNameCheckBox)
        self.serviceNameTimeLabel = QtGui.QLabel(self.serviceNameGroupBox)
        self.serviceNameTimeLabel.setObjectName(u'serviceNameTimeLabel')
        self.serviceNameDay = QtGui.QComboBox(
            self.serviceNameGroupBox)
        self.serviceNameDay.addItems(
            [u'', u'', u'', u'', u'', u'', u'', u''])
        self.serviceNameDay.setObjectName(
            u'serviceNameDay')
        self.serviceNameTime = QtGui.QTimeEdit(self.serviceNameGroupBox)
        self.serviceNameTime.setObjectName(u'serviceNameTime')
        self.serviceNameTimeHBox = QtGui.QHBoxLayout()
        self.serviceNameTimeHBox.setObjectName(u'serviceNameTimeHBox')
        self.serviceNameTimeHBox.addWidget(self.serviceNameDay)
        self.serviceNameTimeHBox.addWidget(self.serviceNameTime)
        self.serviceNameLayout.addRow(self.serviceNameTimeLabel,
            self.serviceNameTimeHBox)
        self.serviceNameLabel = QtGui.QLabel(self.serviceNameGroupBox)
        self.serviceNameLabel.setObjectName(u'serviceNameLabel')
        self.serviceNameEdit = QtGui.QLineEdit(self.serviceNameGroupBox)
        self.serviceNameEdit.setObjectName(u'serviceNameEdit')
        self.serviceNameEdit.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp(r'[^/\\?*|<>\[\]":+]+'), self))
        self.serviceNameRevertButton = QtGui.QToolButton(
            self.serviceNameGroupBox)
        self.serviceNameRevertButton.setObjectName(
            u'serviceNameRevertButton')
        self.serviceNameRevertButton.setIcon(
            build_icon(u':/general/general_revert.png'))
        self.serviceNameHBox = QtGui.QHBoxLayout()
        self.serviceNameHBox.setObjectName(u'serviceNameHBox')
        self.serviceNameHBox.addWidget(self.serviceNameEdit)
        self.serviceNameHBox.addWidget(self.serviceNameRevertButton)
        self.serviceNameLayout.addRow(self.serviceNameLabel,
            self.serviceNameHBox)
        self.serviceNameExampleLabel = QtGui.QLabel(
            self.serviceNameGroupBox)
        self.serviceNameExampleLabel.setObjectName(
            u'serviceNameExampleLabel')
        self.serviceNameExample = QtGui.QLabel(self.serviceNameGroupBox)
        self.serviceNameExample.setObjectName(u'serviceNameExample')
        self.serviceNameLayout.addRow(self.serviceNameExampleLabel,
            self.serviceNameExample)
        self.leftLayout.addWidget(self.serviceNameGroupBox)
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
        self.leftLayout.addWidget(self.defaultImageGroupBox)
        self.hideMouseGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.hideMouseGroupBox.setObjectName(u'hideMouseGroupBox')
        self.hideMouseLayout = QtGui.QVBoxLayout(self.hideMouseGroupBox)
        self.hideMouseLayout.setObjectName(u'hideMouseLayout')
        self.hideMouseCheckBox = QtGui.QCheckBox(self.hideMouseGroupBox)
        self.hideMouseCheckBox.setObjectName(u'hideMouseCheckBox')
        self.hideMouseLayout.addWidget(self.hideMouseCheckBox)
        self.leftLayout.addWidget(self.hideMouseGroupBox)
        self.leftLayout.addStretch()
        # Service Item Slide Limits
        self.slideGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.slideGroupBox.setObjectName(u'slideGroupBox')
        self.slideLayout = QtGui.QFormLayout(self.slideGroupBox)
        self.slideLayout.setLabelAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.slideLayout.setFormAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.slideLayout.setObjectName(u'slideLayout')
        self.endSlideRadioButton = QtGui.QRadioButton(self.slideGroupBox)
        self.endSlideRadioButton.setObjectName(u'endSlideRadioButton')
        self.endSlideLabel = QtGui.QLabel(self.slideGroupBox)
        self.endSlideLabel.setWordWrap(True)
        self.endSlideLabel.setObjectName(u'endSlideLabel')
        self.slideLayout.addRow(self.endSlideRadioButton, self.endSlideLabel)
        self.wrapSlideRadioButton = QtGui.QRadioButton(self.slideGroupBox)
        self.wrapSlideRadioButton.setObjectName(u'wrapSlideRadioButton')
        self.wrapSlideLabel = QtGui.QLabel(self.slideGroupBox)
        self.wrapSlideLabel.setWordWrap(True)
        self.wrapSlideLabel.setObjectName(u'wrapSlideLabel')
        self.slideLayout.addRow(self.wrapSlideRadioButton,
            self.wrapSlideLabel)
        self.nextItemRadioButton = QtGui.QRadioButton(self.slideGroupBox)
        self.nextItemRadioButton.setChecked(True)
        self.nextItemRadioButton.setObjectName(u'nextItemRadioButton')
        self.nextItemLabel = QtGui.QLabel(self.slideGroupBox)
        self.nextItemLabel.setWordWrap(True)
        self.nextItemLabel.setObjectName(u'nextItemLabel')
        self.slideLayout.addRow(self.nextItemRadioButton,
            self.nextItemLabel)
        self.rightLayout.addWidget(self.slideGroupBox)
        self.x11GroupBox = QtGui.QGroupBox(self.leftColumn)
        self.x11GroupBox.setObjectName(u'x11GroupBox')
        self.x11Layout = QtGui.QVBoxLayout(self.x11GroupBox)
        self.x11Layout.setObjectName(u'x11Layout')
        self.x11BypassCheckBox = QtGui.QCheckBox(self.x11GroupBox)
        self.x11BypassCheckBox.setObjectName(u'x11BypassCheckBox')
        self.x11Layout.addWidget(self.x11BypassCheckBox)
        self.rightLayout.addWidget(self.x11GroupBox)
        self.rightLayout.addStretch()

        self.shouldUpdateServiceNameExample = False
        QtCore.QObject.connect(self.serviceNameCheckBox,
            QtCore.SIGNAL(u'toggled(bool)'), self.serviceNameCheckBoxToggled)
        QtCore.QObject.connect(self.serviceNameDay,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onServiceNameDayChanged)
        QtCore.QObject.connect(self.serviceNameTime,
            QtCore.SIGNAL(u'timeChanged(QTime)'),
            self.updateServiceNameExample)
        QtCore.QObject.connect(self.serviceNameEdit,
            QtCore.SIGNAL(u'textChanged(QString)'),
            self.updateServiceNameExample)
        QtCore.QObject.connect(self.serviceNameRevertButton,
            QtCore.SIGNAL(u'pressed()'),
            self.onServiceNameRevertButtonPressed)
        QtCore.QObject.connect(self.defaultColorButton,
            QtCore.SIGNAL(u'pressed()'), self.onDefaultColorButtonPressed)
        QtCore.QObject.connect(self.defaultBrowseButton,
            QtCore.SIGNAL(u'pressed()'), self.onDefaultBrowseButtonPressed)
        QtCore.QObject.connect(self.defaultRevertButton,
            QtCore.SIGNAL(u'pressed()'), self.onDefaultRevertButtonPressed)
        QtCore.QObject.connect(self.x11BypassCheckBox,
            QtCore.SIGNAL(u'toggled(bool)'), self.onX11BypassCheckBoxToggled)
        QtCore.QObject.connect(self.endSlideRadioButton,
            QtCore.SIGNAL(u'pressed()'), self.onEndSlideButtonPressed)
        QtCore.QObject.connect(self.wrapSlideRadioButton,
            QtCore.SIGNAL(u'pressed()'), self.onWrapSlideButtonPressed)
        QtCore.QObject.connect(self.nextItemRadioButton,
            QtCore.SIGNAL(u'pressed()'), self.onnextItemButtonPressed)

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
        self.serviceNameGroupBox.setTitle(
            translate('OpenLP.AdvancedTab', 'Default Service Name'))
        self.serviceNameCheckBox.setText(
            translate('OpenLP.AdvancedTab', 'Enable default service name'))
        self.serviceNameTimeLabel.setText(
            translate('OpenLP.AdvancedTab', 'Date and Time:'))
        self.serviceNameDay.setItemText(0,
            translate('OpenLP.AdvancedTab', 'Monday'))
        self.serviceNameDay.setItemText(1,
            translate('OpenLP.AdvancedTab', 'Tuesday'))
        self.serviceNameDay.setItemText(2,
            translate('OpenLP.AdvancedTab', 'Wednesday'))
        self.serviceNameDay.setItemText(3,
            translate('OpenLP.AdvancedTab', 'Thurdsday'))
        self.serviceNameDay.setItemText(4,
            translate('OpenLP.AdvancedTab', 'Friday'))
        self.serviceNameDay.setItemText(5,
            translate('OpenLP.AdvancedTab', 'Saturday'))
        self.serviceNameDay.setItemText(6,
            translate('OpenLP.AdvancedTab', 'Sunday'))
        self.serviceNameDay.setItemText(7,
            translate('OpenLP.AdvancedTab', 'Now'))
        self.serviceNameTime.setToolTip(translate('OpenLP.AdvancedTab',
            'Time when usual service starts.'))
        self.serviceNameLabel.setText(
            translate('OpenLP.AdvancedTab', 'Name:'))
        self.serviceNameEdit.setToolTip(translate('OpenLP.AdvancedTab',
            'Consult the OpenLP manual for usage.'))
        self.serviceNameRevertButton.setToolTip(unicode(
            translate('OpenLP.AdvancedTab',
            'Revert to the default service name "%s".')) %
            self.defaultServiceName)
        self.serviceNameExampleLabel.setText(translate('OpenLP.AdvancedTab',
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
        # Slide Limits
        self.slideGroupBox.setTitle(
            translate('OpenLP.GeneralTab', 'Service Item Slide Limits'))
        self.endSlideRadioButton.setText(
            translate('OpenLP.GeneralTab', '&End Slide'))
        self.endSlideLabel.setText(
            translate('OpenLP.GeneralTab', 'Up and down arrow keys '
            'stop at the top and bottom slides of each Service Item.'))
        self.wrapSlideRadioButton.setText(
            translate('OpenLP.GeneralTab', '&Wrap Slide'))
        self.wrapSlideLabel.setText(
            translate('OpenLP.GeneralTab', 'Up and down arrow keys '
            'wrap around at the top and bottom slides of each Service Item.'))
        self.nextItemRadioButton.setText(
            translate('OpenLP.GeneralTab', '&Next Item'))
        self.nextItemLabel.setText(
            translate('OpenLP.GeneralTab', 'Up and down arrow keys '
            'advance to the the next or previous Service Item from the '
            'top and bottom slides of each Service Item.'))

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
        self.serviceNameDay.setCurrentIndex(
            settings.value(u'default service day',
            QtCore.QVariant(self.defaultServiceDay)).toInt()[0])
        self.serviceNameTime.setTime(QtCore.QTime(
            settings.value(u'default service hour',
            self.defaultServiceHour).toInt()[0],
            settings.value(u'default service minute',
            self.defaultServiceMinute).toInt()[0]))
        self.shouldUpdateServiceNameExample = True
        self.serviceNameEdit.setText(settings.value(u'default service name',
            self.defaultServiceName).toString())
        default_service_enabled = settings.value(u'default service enabled',
            QtCore.QVariant(True)).toBool()
        self.serviceNameCheckBox.setChecked(default_service_enabled)
        self.serviceNameCheckBoxToggled(default_service_enabled)
        self.x11BypassCheckBox.setChecked(
            settings.value(u'x11 bypass wm', QtCore.QVariant(True)).toBool())
        self.defaultColor = settings.value(u'default color',
            QtCore.QVariant(u'#ffffff')).toString()
        self.defaultFileEdit.setText(settings.value(u'default image',
            QtCore.QVariant(u':/graphics/openlp-splash-screen.png'))\
            .toString())
        self.slide_limits = settings.value(
            u'slide limits', QtCore.QVariant(SlideLimits.End)).toInt()[0]
        if self.slide_limits == SlideLimits.End:
            self.endSlideRadioButton.setChecked(True)
        elif self.slide_limits == SlideLimits.Wrap:
            self.wrapSlideRadioButton.setChecked(True)
        else:
            self.nextItemRadioButton.setChecked(True)
        settings.endGroup()
        self.defaultColorButton.setStyleSheet(
            u'background-color: %s' % self.defaultColor)

    def save(self):
        """
        Save settings to disk.
        """
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'default service enabled',
            self.serviceNameCheckBox.isChecked())
        service_name = unicode(self.serviceNameEdit.text())
        preset_is_valid = self.generateServiceNameExample()[0]
        if service_name == self.defaultServiceName or not preset_is_valid:
            settings.remove(u'default service name')
            self.serviceNameEdit.setText(service_name)
        else:
            settings.setValue(u'default service name', service_name)
        settings.setValue(u'default service day',
            self.serviceNameDay.currentIndex())
        settings.setValue(u'default service hour',
            self.serviceNameTime.time().hour())
        settings.setValue(u'default service minute',
            self.serviceNameTime.time().minute())
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
        settings.setValue(u'default color', self.defaultColor)
        settings.setValue(u'default image', self.defaultFileEdit.text())
        settings.setValue(u'slide limits', QtCore.QVariant(self.slide_limits))
        settings.endGroup()
        if self.displayChanged:
            Receiver.send_message(u'config_screen_changed')
            self.displayChanged = False
        Receiver.send_message(u'slidecontroller_update_slide_limits')

    def serviceNameCheckBoxToggled(self, default_service_enabled):
        self.serviceNameDay.setEnabled(default_service_enabled)
        time_enabled = default_service_enabled and \
            self.serviceNameDay.currentIndex() is not 7
        self.serviceNameTime.setEnabled(time_enabled)
        self.serviceNameEdit.setEnabled(default_service_enabled)
        self.serviceNameRevertButton.setEnabled(default_service_enabled)

    def generateServiceNameExample(self):
        preset_is_valid = True
        if self.serviceNameDay.currentIndex() == 7:
            time = datetime.now()
        else:
            now = datetime.now()
            day_delta = self.serviceNameDay.currentIndex() - now.weekday()
            if day_delta < 0:
                day_delta += 7
            time = now + timedelta(days=day_delta)
            time = time.replace(hour = self.serviceNameTime.time().hour(),
                minute = self.serviceNameTime.time().minute())
        try:
            service_name_example = time.strftime(unicode(
                self.serviceNameEdit.text()))
        except ValueError:
            preset_is_valid = False
            service_name_example = translate('OpenLP.AdvancedTab',
                'Syntax error.')
        return preset_is_valid, service_name_example

    def updateServiceNameExample(self, returned_value):
        if not self.shouldUpdateServiceNameExample:
            return
        name_example = self.generateServiceNameExample()[1]
        self.serviceNameExample.setText(name_example)

    def onServiceNameDayChanged(self, service_day):
        self.serviceNameTime.setEnabled(service_day is not 7)
        self.updateServiceNameExample(None)

    def onServiceNameRevertButtonPressed(self):
        self.serviceNameEdit.setText(self.defaultServiceName)
        self.serviceNameEdit.setFocus()

    def onDefaultColorButtonPressed(self):
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.defaultColor), self)
        if new_color.isValid():
            self.defaultColor = new_color.name()
            self.defaultColorButton.setStyleSheet(
                u'background-color: %s' % self.defaultColor)

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
        self.displayChanged = True

    def onEndSlideButtonPressed(self):
        self.slide_limits = SlideLimits.End

    def onWrapSlideButtonPressed(self):
        self.slide_limits = SlideLimits.Wrap

    def onnextItemButtonPressed(self):
        self.slide_limits = SlideLimits.Next
