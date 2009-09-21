# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

class AlertsTab(SettingsTab):
    """
    AlertsTab is the alerts settings tab in the settings dialog.
    """
    def __init__(self):
        self.font_color = '#ffffff'
        self.bg_color = '#660000'
        SettingsTab.__init__(
            self, translate(u'AlertsTab', u'Alerts'), u'Alerts')

    def setupUi(self):
        self.setObjectName(u'AlertsTab')
        self.AlertsLayout = QtGui.QHBoxLayout(self)
        self.AlertsLayout.setSpacing(8)
        self.AlertsLayout.setMargin(8)
        self.AlertsLayout.setObjectName(u'AlertsLayout')
        self.AlertLeftColumn = QtGui.QWidget(self)
        self.AlertLeftColumn.setObjectName(u'AlertLeftColumn')
        self.SlideLeftLayout = QtGui.QVBoxLayout(self.AlertLeftColumn)
        self.SlideLeftLayout.setSpacing(8)
        self.SlideLeftLayout.setMargin(0)
        self.SlideLeftLayout.setObjectName(u'SlideLeftLayout')
        self.FontGroupBox = QtGui.QGroupBox(self.AlertLeftColumn)
        self.FontGroupBox.setObjectName(u'FontGroupBox')
        self.FontLayout = QtGui.QVBoxLayout(self.FontGroupBox)
        self.FontLayout.setSpacing(8)
        self.FontLayout.setMargin(8)
        self.FontLayout.setObjectName(u'FontLayout')
        self.FontLabel = QtGui.QLabel(self.FontGroupBox)
        self.FontLabel.setObjectName(u'FontLabel')
        self.FontLayout.addWidget(self.FontLabel)
        self.FontComboBox = QtGui.QFontComboBox(self.FontGroupBox)
        self.FontComboBox.setObjectName(u'FontComboBox')
        self.FontLayout.addWidget(self.FontComboBox)
        self.ColorWidget = QtGui.QWidget(self.FontGroupBox)
        self.ColorWidget.setObjectName(u'ColorWidget')
        self.ColorLayout = QtGui.QHBoxLayout(self.ColorWidget)
        self.ColorLayout.setSpacing(8)
        self.ColorLayout.setMargin(0)
        self.ColorLayout.setObjectName(u'ColorLayout')
        self.FontColorLabel = QtGui.QLabel(self.ColorWidget)
        self.FontColorLabel.setObjectName(u'FontColorLabel')
        self.ColorLayout.addWidget(self.FontColorLabel)
        self.FontColorButton = QtGui.QPushButton(self.ColorWidget)
        self.FontColorButton.setObjectName(u'FontColorButton')
        self.ColorLayout.addWidget(self.FontColorButton)
        self.ColorSpacerItem = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ColorLayout.addItem(self.ColorSpacerItem)
        self.BackgroundColorLabel = QtGui.QLabel(self.ColorWidget)
        self.BackgroundColorLabel.setObjectName(u'BackgroundColorLabel')
        self.ColorLayout.addWidget(self.BackgroundColorLabel)
        self.BackgroundColorButton = QtGui.QPushButton(self.ColorWidget)
        self.BackgroundColorButton.setObjectName(u'BackgroundColorButton')
        self.ColorLayout.addWidget(self.BackgroundColorButton)
        self.FontLayout.addWidget(self.ColorWidget)
        self.TimeoutWidget = QtGui.QWidget(self.FontGroupBox)
        self.TimeoutWidget.setObjectName(u'TimeoutWidget')
        self.TimeoutLayout = QtGui.QHBoxLayout(self.TimeoutWidget)
        self.TimeoutLayout.setSpacing(8)
        self.TimeoutLayout.setMargin(0)
        self.TimeoutLayout.setObjectName(u'TimeoutLayout')
        self.TimeoutLabel = QtGui.QLabel(self.TimeoutWidget)
        self.TimeoutLabel.setObjectName(u'TimeoutLabel')
        self.TimeoutLayout.addWidget(self.TimeoutLabel)
        self.TimeoutSpinBox = QtGui.QSpinBox(self.TimeoutWidget)
        self.TimeoutSpinBox.setMaximum(180)
        self.TimeoutSpinBox.setObjectName(u'TimeoutSpinBox')
        self.TimeoutLayout.addWidget(self.TimeoutSpinBox)
        self.TimeoutSpacer = QtGui.QSpacerItem(147, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.TimeoutLayout.addItem(self.TimeoutSpacer)
        self.FontLayout.addWidget(self.TimeoutWidget)
        self.SlideLeftLayout.addWidget(self.FontGroupBox)
        self.SlideLeftSpacer = QtGui.QSpacerItem(20, 94,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.SlideLeftLayout.addItem(self.SlideLeftSpacer)
        self.AlertsLayout.addWidget(self.AlertLeftColumn)
        self.AlertRightColumn = QtGui.QWidget(self)
        self.AlertRightColumn.setObjectName(u'AlertRightColumn')
        self.SlideRightLayout = QtGui.QVBoxLayout(self.AlertRightColumn)
        self.SlideRightLayout.setSpacing(8)
        self.SlideRightLayout.setMargin(0)
        self.SlideRightLayout.setObjectName(u'SlideRightLayout')
        self.PreviewGroupBox = QtGui.QGroupBox(self.AlertRightColumn)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PreviewGroupBox.sizePolicy().hasHeightForWidth())
        self.PreviewGroupBox.setSizePolicy(sizePolicy)
        self.PreviewGroupBox.setObjectName(u'PreviewGroupBox')
        self.PreviewLayout = QtGui.QVBoxLayout(self.PreviewGroupBox)
        self.PreviewLayout.setSpacing(8)
        self.PreviewLayout.setMargin(8)
        self.PreviewLayout.setObjectName(u'PreviewLayout')
        self.FontPreview = QtGui.QLineEdit(self.PreviewGroupBox)
        self.FontPreview.setMinimumSize(QtCore.QSize(280, 100))
        self.FontPreview.setReadOnly(True)
        self.FontPreview.setFocusPolicy(QtCore.Qt.NoFocus)
        self.FontPreview.setAlignment(
            QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.FontPreview.setObjectName(u'FontPreview')
        self.PreviewLayout.addWidget(self.FontPreview)
        self.SlideRightLayout.addWidget(self.PreviewGroupBox)
        self.SlideRightSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.SlideRightLayout.addItem(self.SlideRightSpacer)
        self.AlertsLayout.addWidget(self.AlertRightColumn)
        # Signals and slots
        QtCore.QObject.connect(self.BackgroundColorButton,
            QtCore.SIGNAL(u'pressed()'), self.onBackgroundColorButtonClicked)
        QtCore.QObject.connect(self.FontColorButton,
            QtCore.SIGNAL(u'pressed()'), self.onFontColorButtonClicked)
        QtCore.QObject.connect(self.FontComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onFontComboBoxClicked)
        QtCore.QObject.connect(self.TimeoutSpinBox,
            QtCore.SIGNAL(u'valueChanged(int)'), self.onTimeoutSpinBoxChanged)

    def retranslateUi(self):
        self.FontGroupBox.setTitle(translate(u'AlertsTab', u'Font'))
        self.FontLabel.setText(translate(u'AlertsTab', u'Font Name:'))
        self.FontColorLabel.setText(translate(u'AlertsTab', u'Font Color:'))
        self.BackgroundColorLabel.setText(
            translate(u'AlertsTab', u'Background Color:'))
        self.TimeoutLabel.setText(translate(u'AlertsTab', u'Alert timeout:'))
        self.TimeoutSpinBox.setSuffix(translate(u'AlertsTab', u's'))
        self.PreviewGroupBox.setTitle(translate(u'AlertsTab', u'Preview'))
        self.FontPreview.setText(
            translate(u'AlertsTab', u'openlp.org 2.0 rocks!'))

    def onBackgroundColorButtonClicked(self):
        self.bg_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.bg_color), self).name()
        self.BackgroundColorButton.setStyleSheet(
            u'background-color: %s' % self.bg_color)
        self.updateDisplay()

    def onFontComboBoxClicked(self):
        self.updateDisplay()

    def onFontColorButtonClicked(self):
        self.font_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.font_color), self).name()
        self.FontColorButton.setStyleSheet(
            u'background-color: %s' % self.font_color)
        self.updateDisplay()

    def onTimeoutSpinBoxChanged(self):
        self.timeout = self.TimeoutSpinBox.value()

    def load(self):
        self.timeout = int(self.config.get_config(u'timeout', 5))
        self.font_color = unicode(
            self.config.get_config(u'font color', u'#ffffff'))
        self.bg_color = unicode(
            self.config.get_config(u'background color', u'#660000'))
        self.font_face = unicode(
            self.config.get_config(u'font face', QtGui.QFont().family()))
        self.TimeoutSpinBox.setValue(self.timeout)
        self.FontColorButton.setStyleSheet(
            u'background-color: %s' % self.font_color)
        self.BackgroundColorButton.setStyleSheet(
            u'background-color: %s' % self.bg_color)
        font = QtGui.QFont()
        font.setFamily(self.font_face)
        self.FontComboBox.setCurrentFont(font)
        self.updateDisplay()

    def save(self):
        self.font_face = self.FontComboBox.currentFont().family()
        self.config.set_config(u'background color', unicode(self.bg_color))
        self.config.set_config(u'font color', unicode(self.font_color))
        self.config.set_config(u'font face', unicode(self.font_face))
        self.config.set_config(u'timeout', unicode(self.timeout))

    def updateDisplay(self):
        font = QtGui.QFont()
        font.setFamily(self.FontComboBox.currentFont().family())
        font.setBold(True)
        font.setPointSize(16)
        self.FontPreview.setFont(font)
        self.FontPreview.setStyleSheet(u'background-color: %s; color: %s' % \
            (self.bg_color, self.font_color))
