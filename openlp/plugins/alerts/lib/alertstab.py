# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

from openlp.core.lib import SettingsTab

class AlertsTab(SettingsTab):
    """
    AlertsTab is the alerts settings tab in the settings dialog.
    """
    def __init__(self, parent):
        self.parent = parent
        self.manager = parent.manager
        SettingsTab.__init__(self, parent.name)

    def setupUi(self):
        self.setObjectName(u'AlertsTab')
        self.tabTitleVisible = self.trUtf8('Alerts')
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
        self.FontSizeWidget = QtGui.QWidget(self.FontGroupBox)
        self.FontSizeWidget.setObjectName(u'FontSizeWidget')
        self.FontSizeLayout = QtGui.QHBoxLayout(self.FontSizeWidget)
        self.FontSizeLayout.setSpacing(8)
        self.FontSizeLayout.setMargin(0)
        self.FontSizeLayout.setObjectName(u'FontSizeLayout')
        self.FontSizeLabel = QtGui.QLabel(self.FontSizeWidget)
        self.FontSizeLabel.setObjectName(u'FontSizeLabel')
        self.FontSizeLayout.addWidget(self.FontSizeLabel)
        self.FontSizeSpinBox = QtGui.QSpinBox(self.FontSizeWidget)
        self.FontSizeSpinBox.setObjectName(u'FontSizeSpinBox')
        self.FontSizeLayout.addWidget(self.FontSizeSpinBox)
        self.FontSizeSpacer = QtGui.QSpacerItem(147, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.FontSizeLayout.addItem(self.FontSizeSpacer)
        self.FontLayout.addWidget(self.FontSizeWidget)
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
        self.LocationWidget = QtGui.QWidget(self.FontGroupBox)
        self.LocationWidget.setObjectName(u'LocationWidget')
        self.LocationLayout = QtGui.QHBoxLayout(self.LocationWidget)
        self.LocationLayout.setSpacing(8)
        self.LocationLayout.setMargin(0)
        self.LocationLayout.setObjectName(u'LocationLayout')
        self.LocationLabel = QtGui.QLabel(self.LocationWidget)
        self.LocationLabel.setObjectName(u'LocationLabel')
        self.LocationLayout.addWidget(self.LocationLabel)
        self.LocationComboBox = QtGui.QComboBox(self.LocationWidget)
        self.LocationComboBox.addItem(QtCore.QString())
        self.LocationComboBox.addItem(QtCore.QString())
        self.LocationComboBox.setObjectName(u'LocationComboBox')
        self.LocationLayout.addWidget(self.LocationComboBox)
        self.LocationSpacer = QtGui.QSpacerItem(147, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.LocationLayout.addItem(self.LocationSpacer)
        self.FontLayout.addWidget(self.LocationWidget)
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
        self.FontPreview.setFixedSize(QtCore.QSize(350, 100))
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
        QtCore.QObject.connect(self.LocationComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onLocationComboBoxClicked)
        QtCore.QObject.connect(self.TimeoutSpinBox,
            QtCore.SIGNAL(u'valueChanged(int)'), self.onTimeoutSpinBoxChanged)
        QtCore.QObject.connect(self.FontSizeSpinBox,
            QtCore.SIGNAL(u'valueChanged(int)'), self.onFontSizeSpinBoxChanged)

    def retranslateUi(self):
        self.FontGroupBox.setTitle(self.trUtf8('Font'))
        self.FontLabel.setText(self.trUtf8('Font Name:'))
        self.FontColorLabel.setText(self.trUtf8('Font Color:'))
        self.BackgroundColorLabel.setText(self.trUtf8('Background Color:'))
        self.FontSizeLabel.setText(self.trUtf8('Font Size:'))
        self.FontSizeSpinBox.setSuffix(self.trUtf8('pt'))
        self.TimeoutLabel.setText(self.trUtf8('Alert timeout:'))
        self.TimeoutSpinBox.setSuffix(self.trUtf8('s'))
        self.LocationLabel.setText(self.trUtf8('Location:'))
        self.PreviewGroupBox.setTitle(self.trUtf8('Preview'))
        self.FontPreview.setText(self.trUtf8('openlp.org'))
        self.LocationComboBox.setItemText(0, self.trUtf8('Top'))
        self.LocationComboBox.setItemText(1, self.trUtf8('Bottom'))

    def onBackgroundColorButtonClicked(self):
        self.bg_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.bg_color), self).name()
        self.BackgroundColorButton.setStyleSheet(
            u'background-color: %s' % self.bg_color)
        self.updateDisplay()

    def onFontComboBoxClicked(self):
        self.updateDisplay()

    def onLocationComboBoxClicked(self, location):
        self.location = location

    def onFontColorButtonClicked(self):
        self.font_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.font_color), self).name()
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
            u'location', QtCore.QVariant(0)).toInt()[0]
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

    def onItemSelected(self):
        self.EditButton.setEnabled(True)
        self.DeleteButton.setEnabled(True)

    def save(self):
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        self.font_face = self.FontComboBox.currentFont().family()
        settings.setValue(u'background color', QtCore.QVariant(self.bg_color))
        settings.setValue(u'font color', QtCore.QVariant(self.font_color))
        settings.setValue(u'font size', QtCore.QVariant(self.font_size))
        settings.setValue(u'font face', QtCore.QVariant(self.font_face))
        settings.setValue(u'timeout', QtCore.QVariant(self.timeout))
        settings.setValue(u'location',
            QtCore.QVariant(self.LocationComboBox.currentIndex()))
        settings.endGroup()

    def updateDisplay(self):
        font = QtGui.QFont()
        font.setFamily(self.FontComboBox.currentFont().family())
        font.setBold(True)
        font.setPointSize(self.font_size)
        self.FontPreview.setFont(font)
        self.FontPreview.setStyleSheet(u'background-color: %s; color: %s' % \
            (self.bg_color, self.font_color))
