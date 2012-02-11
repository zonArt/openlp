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
        self.display_changed = False
        advancedTranslated = translate('OpenLP.AdvancedTab', 'Advanced')
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
        self.x11BypassCheckBox.setChecked(
            settings.value(u'x11 bypass wm', QtCore.QVariant(True)).toBool())
        self.default_color = settings.value(u'default color',
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
            u'background-color: %s' % self.default_color)

    def save(self):
        """
        Save settings to disk.
        """
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
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
        settings.setValue(u'slide limits', QtCore.QVariant(self.slide_limits))
        settings.endGroup()
        if self.display_changed:
            Receiver.send_message(u'config_screen_changed')
            self.display_changed = False
        Receiver.send_message(u'slidecontroller_update_slide_limits')

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

    def onEndSlideButtonPressed(self):
        self.slide_limits = SlideLimits.End

    def onWrapSlideButtonPressed(self):
        self.slide_limits = SlideLimits.Wrap

    def onnextItemButtonPressed(self):
        self.slide_limits = SlideLimits.Next
