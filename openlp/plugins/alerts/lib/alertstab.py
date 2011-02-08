# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
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

from openlp.core.lib import SettingsTab, translate
from openlp.core.lib.ui import create_valign_combo

class AlertsTab(SettingsTab):
    """
    AlertsTab is the alerts settings tab in the settings dialog.
    """
    def __init__(self, parent, visible_title):
        self.parent = parent
        self.manager = parent.manager
        SettingsTab.__init__(self, parent.name, visible_title)

    def setupUi(self):
        self.setObjectName(u'AlertsTab')
        SettingsTab.setupUi(self)
        self.fontGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.fontGroupBox.setObjectName(u'fontGroupBox')
        self.fontLayout = QtGui.QFormLayout(self.fontGroupBox)
        self.fontLayout.setObjectName(u'fontLayout')
        self.FontLabel = QtGui.QLabel(self.fontGroupBox)
        self.FontLabel.setObjectName(u'FontLabel')
        self.FontComboBox = QtGui.QFontComboBox(self.fontGroupBox)
        self.FontComboBox.setObjectName(u'FontComboBox')
        self.fontLayout.addRow(self.FontLabel, self.FontComboBox)
        self.FontColorLabel = QtGui.QLabel(self.fontGroupBox)
        self.FontColorLabel.setObjectName(u'FontColorLabel')
        self.ColorLayout = QtGui.QHBoxLayout()
        self.ColorLayout.setObjectName(u'ColorLayout')
        self.FontColorButton = QtGui.QPushButton(self.fontGroupBox)
        self.FontColorButton.setObjectName(u'FontColorButton')
        self.ColorLayout.addWidget(self.FontColorButton)
        self.ColorLayout.addSpacing(20)
        self.BackgroundColorLabel = QtGui.QLabel(self.fontGroupBox)
        self.BackgroundColorLabel.setObjectName(u'BackgroundColorLabel')
        self.ColorLayout.addWidget(self.BackgroundColorLabel)
        self.BackgroundColorButton = QtGui.QPushButton(self.fontGroupBox)
        self.BackgroundColorButton.setObjectName(u'BackgroundColorButton')
        self.ColorLayout.addWidget(self.BackgroundColorButton)
        self.fontLayout.addRow(self.FontColorLabel, self.ColorLayout)
        self.FontSizeLabel = QtGui.QLabel(self.fontGroupBox)
        self.FontSizeLabel.setObjectName(u'FontSizeLabel')
        self.FontSizeSpinBox = QtGui.QSpinBox(self.fontGroupBox)
        self.FontSizeSpinBox.setObjectName(u'FontSizeSpinBox')
        self.fontLayout.addRow(self.FontSizeLabel, self.FontSizeSpinBox)
        self.TimeoutLabel = QtGui.QLabel(self.fontGroupBox)
        self.TimeoutLabel.setObjectName(u'TimeoutLabel')
        self.TimeoutSpinBox = QtGui.QSpinBox(self.fontGroupBox)
        self.TimeoutSpinBox.setMaximum(180)
        self.TimeoutSpinBox.setObjectName(u'TimeoutSpinBox')
        self.fontLayout.addRow(self.TimeoutLabel, self.TimeoutSpinBox)
        create_valign_combo(self.fontGroupBox, self.fontLayout)
        self.leftLayout.addWidget(self.fontGroupBox)
        self.leftLayout.addStretch()
        self.PreviewGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.PreviewGroupBox.setObjectName(u'PreviewGroupBox')
        self.PreviewLayout = QtGui.QVBoxLayout(self.PreviewGroupBox)
        self.PreviewLayout.setObjectName(u'PreviewLayout')
        self.FontPreview = QtGui.QLineEdit(self.PreviewGroupBox)
        self.FontPreview.setObjectName(u'FontPreview')
        self.PreviewLayout.addWidget(self.FontPreview)
        self.rightLayout.addWidget(self.PreviewGroupBox)
        self.rightLayout.addStretch()
        # Signals and slots
        QtCore.QObject.connect(self.BackgroundColorButton,
            QtCore.SIGNAL(u'pressed()'), self.onBackgroundColorButtonClicked)
        QtCore.QObject.connect(self.FontColorButton,
            QtCore.SIGNAL(u'pressed()'), self.onFontColorButtonClicked)
        QtCore.QObject.connect(self.FontComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onFontComboBoxClicked)
        QtCore.QObject.connect(self.TimeoutSpinBox,
            QtCore.SIGNAL(u'valueChanged(int)'), self.onTimeoutSpinBoxChanged)
        QtCore.QObject.connect(self.FontSizeSpinBox,
            QtCore.SIGNAL(u'valueChanged(int)'), self.onFontSizeSpinBoxChanged)

    def retranslateUi(self):
        self.fontGroupBox.setTitle(
            translate('AlertsPlugin.AlertsTab', 'Font'))
        self.FontLabel.setText(
            translate('AlertsPlugin.AlertsTab', 'Font name:'))
        self.FontColorLabel.setText(
            translate('AlertsPlugin.AlertsTab', 'Font color:'))
        self.BackgroundColorLabel.setText(
            translate('AlertsPlugin.AlertsTab', 'Background color:'))
        self.FontSizeLabel.setText(
            translate('AlertsPlugin.AlertsTab', 'Font size:'))
        self.FontSizeSpinBox.setSuffix(
            translate('AlertsPlugin.AlertsTab', 'pt'))
        self.TimeoutLabel.setText(
            translate('AlertsPlugin.AlertsTab', 'Alert timeout:'))
        self.TimeoutSpinBox.setSuffix(
            translate('AlertsPlugin.AlertsTab', 's'))
        self.PreviewGroupBox.setTitle(
            translate('AlertsPlugin.AlertsTab', 'Preview'))
        self.FontPreview.setText(
            translate('AlertsPlugin.AlertsTab', 'OpenLP 2.0'))

    def onBackgroundColorButtonClicked(self):
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.bg_color), self)
        if new_color.isValid():
            self.bg_color = new_color.name()
            self.BackgroundColorButton.setStyleSheet(
                u'background-color: %s' % self.bg_color)
            self.updateDisplay()

    def onFontComboBoxClicked(self):
        self.updateDisplay()

    def onFontColorButtonClicked(self):
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.font_color), self)
        if new_color.isValid():
            self.font_color = new_color.name()
            self.FontColorButton.setStyleSheet(
                u'background-color: %s' % self.font_color)
            self.updateDisplay()

    def onTimeoutSpinBoxChanged(self):
        self.timeout = self.TimeoutSpinBox.value()

    def onFontSizeSpinBoxChanged(self):
        self.font_size = self.FontSizeSpinBox.value()
        self.updateDisplay()

    def load(self):
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        self.timeout = settings.value(u'timeout', QtCore.QVariant(5)).toInt()[0]
        self.font_color = unicode(settings.value(
            u'font color', QtCore.QVariant(u'#ffffff')).toString())
        self.font_size = settings.value(
            u'font size', QtCore.QVariant(40)).toInt()[0]
        self.bg_color = unicode(settings.value(
            u'background color', QtCore.QVariant(u'#660000')).toString())
        self.font_face = unicode(settings.value(
            u'font face', QtCore.QVariant(QtGui.QFont().family())).toString())
        self.location = settings.value(
            u'location', QtCore.QVariant(1)).toInt()[0]
        settings.endGroup()
        self.FontSizeSpinBox.setValue(self.font_size)
        self.TimeoutSpinBox.setValue(self.timeout)
        self.FontColorButton.setStyleSheet(
            u'background-color: %s' % self.font_color)
        self.BackgroundColorButton.setStyleSheet(
            u'background-color: %s' % self.bg_color)
        self.LocationComboBox.setCurrentIndex(self.location)
        font = QtGui.QFont()
        font.setFamily(self.font_face)
        self.FontComboBox.setCurrentFont(font)
        self.updateDisplay()

    def save(self):
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'background color', QtCore.QVariant(self.bg_color))
        settings.setValue(u'font color', QtCore.QVariant(self.font_color))
        settings.setValue(u'font size', QtCore.QVariant(self.font_size))
        self.font_face = self.FontComboBox.currentFont().family()
        settings.setValue(u'font face', QtCore.QVariant(self.font_face))
        settings.setValue(u'timeout', QtCore.QVariant(self.timeout))
        self.location = self.LocationComboBox.currentIndex()
        settings.setValue(u'location', QtCore.QVariant(self.location))
        settings.endGroup()

    def updateDisplay(self):
        font = QtGui.QFont()
        font.setFamily(self.FontComboBox.currentFont().family())
        font.setBold(True)
        font.setPointSize(self.font_size)
        self.FontPreview.setFont(font)
        self.FontPreview.setStyleSheet(u'background-color: %s; color: %s' %
            (self.bg_color, self.font_color))
