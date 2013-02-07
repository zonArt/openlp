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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab, Receiver, Settings, UiStrings, translate
from openlp.core.lib.ui import create_valign_selection_widgets

class AlertsTab(SettingsTab):
    """
    AlertsTab is the alerts settings tab in the settings dialog.
    """
    def __init__(self, parent, name, visible_title, icon_path):
        SettingsTab.__init__(self, parent, name, visible_title, icon_path)

    def setupUi(self):
        self.setObjectName(u'AlertsTab')
        SettingsTab.setupUi(self)
        self.fontGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.fontGroupBox.setObjectName(u'fontGroupBox')
        self.fontLayout = QtGui.QFormLayout(self.fontGroupBox)
        self.fontLayout.setObjectName(u'fontLayout')
        self.fontLabel = QtGui.QLabel(self.fontGroupBox)
        self.fontLabel.setObjectName(u'fontLabel')
        self.fontComboBox = QtGui.QFontComboBox(self.fontGroupBox)
        self.fontComboBox.setObjectName(u'fontComboBox')
        self.fontLayout.addRow(self.fontLabel, self.fontComboBox)
        self.fontColorLabel = QtGui.QLabel(self.fontGroupBox)
        self.fontColorLabel.setObjectName(u'fontColorLabel')
        self.colorLayout = QtGui.QHBoxLayout()
        self.colorLayout.setObjectName(u'colorLayout')
        self.fontColorButton = QtGui.QPushButton(self.fontGroupBox)
        self.fontColorButton.setObjectName(u'fontColorButton')
        self.colorLayout.addWidget(self.fontColorButton)
        self.colorLayout.addSpacing(20)
        self.backgroundColorLabel = QtGui.QLabel(self.fontGroupBox)
        self.backgroundColorLabel.setObjectName(u'backgroundColorLabel')
        self.colorLayout.addWidget(self.backgroundColorLabel)
        self.backgroundColorButton = QtGui.QPushButton(self.fontGroupBox)
        self.backgroundColorButton.setObjectName(u'backgroundColorButton')
        self.colorLayout.addWidget(self.backgroundColorButton)
        self.fontLayout.addRow(self.fontColorLabel, self.colorLayout)
        self.fontSizeLabel = QtGui.QLabel(self.fontGroupBox)
        self.fontSizeLabel.setObjectName(u'fontSizeLabel')
        self.fontSizeSpinBox = QtGui.QSpinBox(self.fontGroupBox)
        self.fontSizeSpinBox.setObjectName(u'fontSizeSpinBox')
        self.fontLayout.addRow(self.fontSizeLabel, self.fontSizeSpinBox)
        self.timeoutLabel = QtGui.QLabel(self.fontGroupBox)
        self.timeoutLabel.setObjectName(u'timeoutLabel')
        self.timeoutSpinBox = QtGui.QSpinBox(self.fontGroupBox)
        self.timeoutSpinBox.setMaximum(180)
        self.timeoutSpinBox.setObjectName(u'timeoutSpinBox')
        self.fontLayout.addRow(self.timeoutLabel, self.timeoutSpinBox)
        self.verticalLabel, self.verticalComboBox = create_valign_selection_widgets(self.fontGroupBox)
        self.verticalLabel.setObjectName(u'verticalLabel')
        self.verticalComboBox.setObjectName(u'verticalComboBox')
        self.fontLayout.addRow(self.verticalLabel, self.verticalComboBox)
        self.leftLayout.addWidget(self.fontGroupBox)
        self.leftLayout.addStretch()
        self.previewGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.previewGroupBox.setObjectName(u'previewGroupBox')
        self.previewLayout = QtGui.QVBoxLayout(self.previewGroupBox)
        self.previewLayout.setObjectName(u'previewLayout')
        self.fontPreview = QtGui.QLineEdit(self.previewGroupBox)
        self.fontPreview.setObjectName(u'fontPreview')
        self.previewLayout.addWidget(self.fontPreview)
        self.rightLayout.addWidget(self.previewGroupBox)
        self.rightLayout.addStretch()
        # Signals and slots
        QtCore.QObject.connect(self.backgroundColorButton, QtCore.SIGNAL(u'clicked()'),
            self.onBackgroundColorButtonClicked)
        QtCore.QObject.connect(self.fontColorButton, QtCore.SIGNAL(u'clicked()'), self.onFontColorButtonClicked)
        QtCore.QObject.connect(self.fontComboBox, QtCore.SIGNAL(u'activated(int)'), self.onFontComboBoxClicked)
        QtCore.QObject.connect(self.timeoutSpinBox, QtCore.SIGNAL(u'valueChanged(int)'), self.onTimeoutSpinBoxChanged)
        QtCore.QObject.connect(self.fontSizeSpinBox, QtCore.SIGNAL(u'valueChanged(int)'), self.onFontSizeSpinBoxChanged)

    def retranslateUi(self):
        self.fontGroupBox.setTitle(translate('AlertsPlugin.AlertsTab', 'Font'))
        self.fontLabel.setText(translate('AlertsPlugin.AlertsTab', 'Font name:'))
        self.fontColorLabel.setText(translate('AlertsPlugin.AlertsTab', 'Font color:'))
        self.backgroundColorLabel.setText(translate('AlertsPlugin.AlertsTab', 'Background color:'))
        self.fontSizeLabel.setText(translate('AlertsPlugin.AlertsTab', 'Font size:'))
        self.fontSizeSpinBox.setSuffix(UiStrings().FontSizePtUnit)
        self.timeoutLabel.setText(translate('AlertsPlugin.AlertsTab', 'Alert timeout:'))
        self.timeoutSpinBox.setSuffix(UiStrings().Seconds)
        self.previewGroupBox.setTitle(UiStrings().Preview)
        self.fontPreview.setText(UiStrings().OLPV2x)

    def onBackgroundColorButtonClicked(self):
        new_color = QtGui.QColorDialog.getColor(QtGui.QColor(self.bg_color), self)
        if new_color.isValid():
            self.bg_color = new_color.name()
            self.backgroundColorButton.setStyleSheet(u'background-color: %s' % self.bg_color)
            self.updateDisplay()

    def onFontComboBoxClicked(self):
        self.updateDisplay()

    def onFontColorButtonClicked(self):
        new_color = QtGui.QColorDialog.getColor(QtGui.QColor(self.font_color), self)
        if new_color.isValid():
            self.font_color = new_color.name()
            self.fontColorButton.setStyleSheet(u'background-color: %s' % self.font_color)
            self.updateDisplay()

    def onTimeoutSpinBoxChanged(self):
        self.timeout = self.timeoutSpinBox.value()
        self.changed = True

    def onFontSizeSpinBoxChanged(self):
        self.font_size = self.fontSizeSpinBox.value()
        self.updateDisplay()

    def load(self):
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        self.timeout = settings.value(u'timeout')
        self.font_color = settings.value(u'font color')
        self.font_size = settings.value(u'font size')
        self.bg_color = settings.value(u'background color')
        self.font_face = settings.value(u'font face')
        self.location = settings.value(u'location')
        settings.endGroup()
        self.fontSizeSpinBox.setValue(self.font_size)
        self.timeoutSpinBox.setValue(self.timeout)
        self.fontColorButton.setStyleSheet(u'background-color: %s' % self.font_color)
        self.backgroundColorButton.setStyleSheet(u'background-color: %s' % self.bg_color)
        self.verticalComboBox.setCurrentIndex(self.location)
        font = QtGui.QFont()
        font.setFamily(self.font_face)
        self.fontComboBox.setCurrentFont(font)
        self.updateDisplay()
        self.changed = False

    def save(self):
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        # Check value has changed as no event handles this field
        if settings.value(u'location') != self.verticalComboBox.currentIndex():
            self.changed = True
        settings.setValue(u'background color', self.bg_color)
        settings.setValue(u'font color', self.font_color)
        settings.setValue(u'font size', self.font_size)
        self.font_face = self.fontComboBox.currentFont().family()
        settings.setValue(u'font face', self.font_face)
        settings.setValue(u'timeout', self.timeout)
        self.location = self.verticalComboBox.currentIndex()
        settings.setValue(u'location', self.location)
        settings.endGroup()
        if self.changed:
            Receiver.send_message(u'update_display_css')
        self.changed = False

    def updateDisplay(self):
        font = QtGui.QFont()
        font.setFamily(self.fontComboBox.currentFont().family())
        font.setBold(True)
        font.setPointSize(self.font_size)
        self.fontPreview.setFont(font)
        self.fontPreview.setStyleSheet(u'background-color: %s; color: %s' % (self.bg_color, self.font_color))
        self.changed = True

