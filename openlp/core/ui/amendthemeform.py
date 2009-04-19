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
import logging
import os, os.path

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QColor, QFont
from openlp.core.lib import ThemeXML
from openlp.core import fileToXML
from openlp.core import Renderer
from openlp.core import translate

from amendthemedialog import Ui_AmendThemeDialog

log = logging.getLogger(u'AmendThemeForm')

class AmendThemeForm(QtGui.QDialog,  Ui_AmendThemeDialog):

    def __init__(self, thememanager, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.thememanager = thememanager
        self.setupUi(self)

        #define signals
        #Buttons
        QtCore.QObject.connect(self.Color1PushButton ,
            QtCore.SIGNAL("pressed()"), self.onColor1PushButtonClicked)
        QtCore.QObject.connect(self.Color2PushButton ,
            QtCore.SIGNAL("pressed()"), self.onColor2PushButtonClicked)
        QtCore.QObject.connect(self.MainFontColorPushButton,
            QtCore.SIGNAL("pressed()"), self.onMainFontColorPushButtonClicked)
        QtCore.QObject.connect(self.FontFooterColorPushButton,
            QtCore.SIGNAL("pressed()"), self.onFontFooterColorPushButtonClicked)
        #Combo boxes
        QtCore.QObject.connect(self.BackgroundComboBox,
            QtCore.SIGNAL("activated(int)"), self.onBackgroundComboBoxSelected)
        QtCore.QObject.connect(self.BackgroundTypeComboBox,
            QtCore.SIGNAL("activated(int)"), self.onBackgroundTypeComboBoxSelected)
        QtCore.QObject.connect(self.GradientComboBox,
            QtCore.SIGNAL("activated(int)"), self.onGradientComboBoxSelected)


    def accept(self):
        return QtGui.QDialog.accept(self)

    def themePath(self, path):
        self.path = path

    def loadTheme(self, theme):
        self.theme = ThemeXML()
        if theme == None:
            self.theme.parse(self.baseTheme())
        else:
            xml_file = os.path.join(self.path, theme, theme+u'.xml')
            xml = fileToXML(xml_file)
            self.theme.parse(xml)
        self.paintUi(self.theme)
        self.previewTheme(self.theme)

    def onGradientComboBoxSelected(self, currentIndex):
        if currentIndex == 0: # Horizontal
            self.theme.background_direction = u'horizontal'
        elif currentIndex == 1: # vertical
            self.theme.background_direction = u'vertical'
        else:
            self.theme.background_direction = u'circular'
        self.stateChanging(self.theme)
        self.previewTheme(self.theme)

    def onBackgroundComboBoxSelected(self, currentIndex):
        if currentIndex == 0: # Opaque
            self.theme.background_mode = u'opaque'
        else:
            self.theme.background_mode = u'transparent'
        self.stateChanging(self.theme)
        self.previewTheme(self.theme)

    def onBackgroundTypeComboBoxSelected(self, currentIndex):
        if currentIndex == 0: # Solid
            self.theme.background_type = u'solid'
            if self.theme.background_direction == None: # never defined
                self.theme.background_direction = u'horizontal'
            if self.theme.background_startColor is None :
                self.theme.background_startColor = u'#000000'
            if self.theme.background_endColor is None :
                self.theme.background_endColor = u'#000000'
        elif currentIndex == 1: # Gradient
            self.theme.background_type = u'gradient'
            if self.theme.background_direction == None: # never defined
                self.theme.background_direction = u'horizontal'
            if self.theme.background_startColor is None :
                self.theme.background_startColor = u'#000000'
            if self.theme.background_endColor is None :
                self.theme.background_endColor = u'#000000'
        else:
            self.theme.background_type = u'image'
        self.stateChanging(self.theme)
        self.previewTheme(self.theme)

    def onColor1PushButtonClicked(self):
        if self.theme.background_type == u'solid':
            self.theme.background_color = QtGui.QColorDialog.getColor(
                QColor(self.theme.background_color), self).name()
            self.Color1PushButton.setStyleSheet(
                'background-color: %s' % str(self.theme.background_color))
        else:
            self.theme.background_startColor = QtGui.QColorDialog.getColor(
                QColor(self.theme.background_startColor), self).name()
            self.Color1PushButton.setStyleSheet(
                'background-color: %s' % str(self.theme.background_startColor))

        self.previewTheme(self.theme)

    def onColor2PushButtonClicked(self):
        self.theme.background_endColor = QtGui.QColorDialog.getColor(
            QColor(self.theme.background_endColor), self).name()
        self.Color2PushButton.setStyleSheet(
            'background-color: %s' % str(self.theme.background_endColor))

        self.previewTheme(self.theme)

    def onMainFontColorPushButtonClicked(self):
        self.theme.font_main_color = QtGui.QColorDialog.getColor(
            QColor(self.theme.font_main_color), self).name()

        self.MainFontColorPushButton.setStyleSheet(
            'background-color: %s' % str(self.theme.font_main_color))
        self.previewTheme(self.theme)

    def onFontFooterColorPushButtonClicked(self):
        self.theme.font_footer_color = QtGui.QColorDialog.getColor(
            QColor(self.theme.font_footer_color), self).name()

        self.FontFooterColorPushButton.setStyleSheet(
            'background-color: %s' % str(self.theme.font_footer_color))
        self.previewTheme(self.theme)

    def baseTheme(self):
        log.debug(u'base Theme')
        newtheme = ThemeXML()
        newtheme.new_document(u'New Theme')
        newtheme.add_background_solid(str(u'#000000'))
        newtheme.add_font(str(QFont().family()), str(u'#FFFFFF'), str(30), u'False')
        newtheme.add_font(str(QFont().family()), str(u'#FFFFFF'), str(12), u'False', u'footer')
        newtheme.add_display(str(False), str(u'#FFFFFF'), str(False), str(u'#FFFFFF'),
            str(0), str(0), str(0))

        return newtheme.extract_xml()

    def paintUi(self, theme):
        print theme  # leave as helpful for initial development
        self.stateChanging(theme)
        self.BackgroundTypeComboBox.setCurrentIndex(0)
        self.BackgroundComboBox.setCurrentIndex(0)
        self.GradientComboBox.setCurrentIndex(0)
        self.MainFontColorPushButton.setStyleSheet(
            'background-color: %s' % str(theme.font_main_color))
        self.FontFooterColorPushButton.setStyleSheet(
            'background-color: %s' % str(theme.font_footer_color))

    def stateChanging(self, theme):
        if theme.background_type == u'solid':
            self.Color1PushButton.setStyleSheet(
                'background-color: %s' % str(theme.background_color))
            self.Color1Label.setText(translate(u'ThemeManager', u'Background Font:'))
            self.Color1Label.setVisible(True)
            self.Color1PushButton.setVisible(True)
            self.Color2Label.setVisible(False)
            self.Color2PushButton.setVisible(False)
        elif theme.background_type == u'gradient':
            self.Color1PushButton.setStyleSheet(
                'background-color: %s' % str(theme.background_startColor))
            self.Color2PushButton.setStyleSheet(
                'background-color: %s' % str(theme.background_endColor))
            self.Color1Label.setText(translate(u'ThemeManager', u'First  Color:'))
            self.Color2Label.setText(translate(u'ThemeManager', u'Second Color:'))
            self.Color1Label.setVisible(True)
            self.Color1PushButton.setVisible(True)
            self.Color2Label.setVisible(True)
            self.Color2PushButton.setVisible(True)
        else: # must be image
            self.Color1Label.setVisible(False)
            self.Color1PushButton.setVisible(False)
            self.Color2Label.setVisible(False)
            self.Color2PushButton.setVisible(False)

    def previewTheme(self, theme):
        frame = self.thememanager.generateImage(theme)
        self.ThemePreview.setPixmap(frame)
