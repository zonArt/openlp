# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QColor, QFont

from openlp.core import translate
from openlp.core.lib import SettingsTab
from openlp.core.resources import *

class AlertsTab(SettingsTab):
    """
    AlertsTab is the alerts settings tab in the settings dialog.
    """
    def __init__(self):
        SettingsTab.__init__(self, u'Alerts')

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

        self.FontColourButton = QtGui.QPushButton(self.ColorWidget)
        self.FontColourButton.setObjectName("FontColourButton")
        self.ColorLayout.addWidget(self.FontColourButton)

#        self.FontColorPanel = QtGui.QGraphicsView(self.ColorWidget)
#        self.FontColorPanel.setMinimumSize(QtCore.QSize(24, 24))
#        self.FontColorPanel.setMaximumSize(QtCore.QSize(24, 24))
#        self.FontColorPanel.setObjectName(u'FontColorPanel')
#        self.ColorLayout.addWidget(self.FontColorPanel)

        self.ColorSpacerItem = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ColorLayout.addItem(self.ColorSpacerItem)
        self.BackgroundColorLabel = QtGui.QLabel(self.ColorWidget)
        self.BackgroundColorLabel.setObjectName(u'BackgroundColorLabel')
        self.ColorLayout.addWidget(self.BackgroundColorLabel)
        
        self.BackgroundColourButton = QtGui.QPushButton(self.ColorWidget)
        self.BackgroundColourButton.setObjectName("BackgroundColourButton")
        self.ColorLayout.addWidget(self.BackgroundColourButton)
        
#        self.BackgroundColorPanel = QtGui.QGraphicsView(self.ColorWidget)
#        self.BackgroundColorPanel.setMinimumSize(QtCore.QSize(24, 24))
#        self.BackgroundColorPanel.setMaximumSize(QtCore.QSize(24, 24))
#        self.BackgroundColorPanel.setObjectName(u'BackgroundColorPanel')
#        self.ColorLayout.addWidget(self.BackgroundColorPanel)
        
        
        self.FontLayout.addWidget(self.ColorWidget)
        self.LengthWidget = QtGui.QWidget(self.FontGroupBox)
        self.LengthWidget.setObjectName(u'LengthWidget')
        self.LengthLayout = QtGui.QHBoxLayout(self.LengthWidget)
        self.LengthLayout.setSpacing(8)
        self.LengthLayout.setMargin(0)
        self.LengthLayout.setObjectName(u'LengthLayout')
        self.LengthLabel = QtGui.QLabel(self.LengthWidget)
        self.LengthLabel.setObjectName(u'LengthLabel')
        self.LengthLayout.addWidget(self.LengthLabel)
        self.LengthSpinBox = QtGui.QSpinBox(self.LengthWidget)
        self.LengthSpinBox.setMaximum(180)
        #self.LengthSpinBox.setProperty(u'value', QtCore.QVariant(5))
        self.LengthSpinBox.setObjectName(u'LengthSpinBox')
        self.LengthLayout.addWidget(self.LengthSpinBox)
        self.LengthSpacer = QtGui.QSpacerItem(147, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.LengthLayout.addItem(self.LengthSpacer)
        self.FontLayout.addWidget(self.LengthWidget)
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PreviewGroupBox.sizePolicy().hasHeightForWidth())
        self.PreviewGroupBox.setSizePolicy(sizePolicy)
        self.PreviewGroupBox.setObjectName(u'PreviewGroupBox')
        self.PreviewLayout = QtGui.QVBoxLayout(self.PreviewGroupBox)
        self.PreviewLayout.setSpacing(8)
        self.PreviewLayout.setMargin(8)
        self.PreviewLayout.setObjectName(u'PreviewLayout')
        
        #self.FontPreview = QtGui.QGraphicsView(self.PreviewGroupBox)        
        self.FontPreview = QtGui.QTextEdit(self.PreviewGroupBox)
        self.FontPreview.setMaximumSize(QtCore.QSize(16777215, 64))
        self.FontPreview.setObjectName(u'FontPreview')
        self.PreviewLayout.addWidget(self.FontPreview)
        
        self.SlideRightLayout.addWidget(self.PreviewGroupBox)
        self.SlideRightSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.SlideRightLayout.addItem(self.SlideRightSpacer)
        self.AlertsLayout.addWidget(self.AlertRightColumn)
        
        QtCore.QObject.connect(self.BackgroundColourButton, \
                               QtCore.SIGNAL("pressed()"), self.onBackgroundColourButtonclicked)
        QtCore.QObject.connect(self.FontColourButton, \
                               QtCore.SIGNAL("pressed()"), self.onFontColourButtonclicked)
        QtCore.QObject.connect(self.FontComboBox,\
                               QtCore.SIGNAL("activated(int)"), self.onFontComboBoxclicked)
        QtCore.QObject.connect(self.LengthSpinBox,\
                               QtCore.SIGNAL("valueChanged(int)"), self.onLengthSpinBoxchanged)                                   

    def retranslateUi(self):
        self.FontGroupBox.setTitle(translate(u'AlertsTab', u'Font'))
        self.FontLabel.setText(translate(u'AlertsTab', u'Font Name:'))
        self.FontColorLabel.setText(translate(u'AlertsTab', u'Font Color:'))
        self.BackgroundColorLabel.setText(translate(u'AlertsTab', u'Background Color:'))
        self.LengthLabel.setText(translate(u'AlertsTab', u'Display length:'))
        self.LengthSpinBox.setSuffix(translate(u'AlertsTab', u's'))
        self.PreviewGroupBox.setTitle(translate(u'AlertsTab', u'Preview'))
    
    def onBackgroundColourButtonclicked(self):
        self.bg_color = QtGui.QColorDialog.getColor(QColor(self.bg_color), self).name()
        self.BackgroundColourButton.setStyleSheet('background-color: %s' % self.bg_color)
        self._update_display()        

    def onFontComboBoxclicked(self):
        self._update_display()

    def onFontColourButtonclicked(self):
        self.font_color = QtGui.QColorDialog.getColor(QColor(self.font_color), self).name()
        self.FontColourButton.setStyleSheet('background-color: %s' % self.font_color)
        self._update_display()        

    def onLengthSpinBoxchanged(self):
        self.spin_length = self.LengthSpinBox.value()

    def load(self):
        self.spin_length = self.config.get_config("spin length",u"5" )
        self.LengthSpinBox.setValue(int(self.spin_length))
        self.font_color = self.config.get_config("font color",u"#ffffff" )
        self.FontColourButton.setStyleSheet('background-color: %s' % self.font_color)        
        self.bg_color = self.config.get_config("background color",u"#00007f" )
        self.BackgroundColourButton.setStyleSheet('background-color: %s' % self.bg_color)
        self.font_text = self.config.get_config("text font",u"Century Schoolbook L,12,-1,5,50,0,0,0,0,0" )
        font = QFont()
        font.fromString(self.font_text)
        self.FontComboBox.setCurrentFont(font)
        self.FontPreview.setReadOnly(True)
        self.FontPreview.setText("Openlp-2 is cool")
        self._update_display()
        
    def save(self):
        self.config.set_config("background color", str(self.bg_color))
        self.config.set_config("font color", str(self.font_color))
        font = self.FontComboBox.currentFont().toString()
        self.config.set_config("text font", str(font))
        self.config.set_config("spin length", str(self.spin_length))
 
 
    def _update_display(self):
        font =self.FontComboBox.currentFont()
        font.setBold(True)
        font.setPointSize(20)
        self.FontPreview.setFont(font)
        self.FontPreview.setStyleSheet("alignment : centre; background-color: "+ self.bg_color+ "; color: " + self.font_color)
        
    def load(self):
        pass
        
    def save(self):
        pass
