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

import logging
import os, os.path

from PyQt4 import QtCore, QtGui
from openlp.core.lib import ThemeXML, Renderer, file_to_xml, str_to_bool, \
    translate

from amendthemedialog import Ui_AmendThemeDialog

log = logging.getLogger(u'AmendThemeForm')

class AmendThemeForm(QtGui.QDialog,  Ui_AmendThemeDialog):

    def __init__(self, thememanager, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.thememanager = thememanager
        self.path = None
        self.theme = ThemeXML()
        self.setupUi(self)
        #define signals
        #Buttons
        QtCore.QObject.connect(self.Color1PushButton ,
            QtCore.SIGNAL(u'pressed()'), self.onColor1PushButtonClicked)
        QtCore.QObject.connect(self.Color2PushButton ,
            QtCore.SIGNAL(u'pressed()'), self.onColor2PushButtonClicked)
        QtCore.QObject.connect(self.FontMainColorPushButton,
            QtCore.SIGNAL(u'pressed()'), self.onFontMainColorPushButtonClicked)
        QtCore.QObject.connect(self.FontFooterColorPushButton,
            QtCore.SIGNAL(u'pressed()'),
            self.onFontFooterColorPushButtonClicked)
        QtCore.QObject.connect(self.OutlineColorPushButton,
            QtCore.SIGNAL(u'pressed()'), self.onOutlineColorPushButtonClicked)
        QtCore.QObject.connect(self.ShadowColorPushButton,
            QtCore.SIGNAL(u'pressed()'), self.onShadowColorPushButtonClicked)
        QtCore.QObject.connect(self.ImageToolButton,
            QtCore.SIGNAL(u'pressed()'), self.onImageToolButtonClicked)
        #Combo boxes
        QtCore.QObject.connect(self.BackgroundComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onBackgroundComboBoxSelected)
        QtCore.QObject.connect(self.BackgroundTypeComboBox,
            QtCore.SIGNAL(u'activated(int)'),
            self.onBackgroundTypeComboBoxSelected)
        QtCore.QObject.connect(self.GradientComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onGradientComboBoxSelected)
        QtCore.QObject.connect(self.FontMainComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onFontMainComboBoxSelected)
        QtCore.QObject.connect(self.FontMainWeightComboBox,
            QtCore.SIGNAL(u'activated(int)'),
            self.onFontMainWeightComboBoxSelected)
        QtCore.QObject.connect(self.FontFooterComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onFontFooterComboBoxSelected)
        QtCore.QObject.connect(self.FontFooterWeightComboBox,
            QtCore.SIGNAL(u'activated(int)'),
            self.onFontFooterWeightComboBoxSelected)
        QtCore.QObject.connect(self.HorizontalComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onHorizontalComboBoxSelected)
        QtCore.QObject.connect(self.VerticalComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onVerticalComboBoxSelected)
        #Spin boxes
        QtCore.QObject.connect(self.FontMainSizeSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontMainSizeSpinBoxChanged)
        QtCore.QObject.connect(self.FontFooterSizeSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontFooterSizeSpinBoxChanged)
        QtCore.QObject.connect(self.FontMainDefaultCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onFontMainDefaultCheckBoxChanged)
        QtCore.QObject.connect(self.FontMainXSpinBox,
            QtCore.SIGNAL(u'editingFinished()'), self.onFontMainXSpinBoxChanged)
        QtCore.QObject.connect(self.FontMainYSpinBox,
            QtCore.SIGNAL(u'editingFinished()'), self.onFontMainYSpinBoxChanged)
        QtCore.QObject.connect(self.FontMainWidthSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontMainWidthSpinBoxChanged)
        QtCore.QObject.connect(self.FontMainHeightSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontMainHeightSpinBoxChanged)
        QtCore.QObject.connect(self.FontFooterDefaultCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onFontFooterDefaultCheckBoxChanged)
        QtCore.QObject.connect(self.FontFooterXSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontFooterXSpinBoxChanged)
        QtCore.QObject.connect(self.FontFooterYSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontFooterYSpinBoxChanged)
        QtCore.QObject.connect(self.FontFooterWidthSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontFooterWidthSpinBoxChanged)
        QtCore.QObject.connect(self.FontFooterHeightSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontFooterHeightSpinBoxChanged)
        QtCore.QObject.connect(self.OutlineCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.onOutlineCheckBoxChanged)
        QtCore.QObject.connect(self.ShadowCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.onShadowCheckBoxChanged)

    def accept(self):
        new_theme = ThemeXML()
        theme_name = unicode(self.ThemeNameEdit.displayText())
        new_theme.new_document(theme_name)
        save_from = None
        save_to = None
        if self.theme.background_mode == u'transparent':
            new_theme.add_background_transparent()
        else:
            if self.theme.background_type == u'solid':
                new_theme.add_background_solid( \
                    unicode(self.theme.background_color))
            elif self.theme.background_type == u'gradient':
                new_theme.add_background_gradient( \
                    unicode(self.theme.background_startColor),
                    unicode(self.theme.background_endColor),
                    self.theme.background_direction)
            else:
                (path, filename) = \
                    os.path.split(unicode(self.theme.background_filename))
                new_theme.add_background_image(filename)
                save_to= os.path.join(self.path, theme_name, filename )
                save_from = self.theme.background_filename

        new_theme.add_font(unicode(self.theme.font_main_name),
                unicode(self.theme.font_main_color),
                unicode(self.theme.font_main_proportion),
                unicode(self.theme.font_main_override), u'main',
                unicode(self.theme.font_main_weight),
                unicode(self.theme.font_main_italics),
                unicode(self.theme.font_main_x),
                unicode(self.theme.font_main_y),
                unicode(self.theme.font_main_width),
                unicode(self.theme.font_main_height))
        new_theme.add_font(unicode(self.theme.font_footer_name),
                unicode(self.theme.font_footer_color),
                unicode(self.theme.font_footer_proportion),
                unicode(self.theme.font_footer_override), u'footer',
                unicode(self.theme.font_footer_weight),
                unicode(self.theme.font_footer_italics),
                unicode(self.theme.font_footer_x),
                unicode(self.theme.font_footer_y),
                unicode(self.theme.font_footer_width),
                unicode(self.theme.font_footer_height) )
        new_theme.add_display(unicode(self.theme.display_shadow),
                unicode(self.theme.display_shadow_color),
                unicode(self.theme.display_outline),
                unicode(self.theme.display_outline_color),
                unicode(self.theme.display_horizontalAlign),
                unicode(self.theme.display_verticalAlign),
                unicode(self.theme.display_wrapStyle))
        theme = new_theme.extract_xml()
        pretty_theme = new_theme.extract_formatted_xml()
        if self.thememanager.saveTheme(theme_name, theme, pretty_theme,
            save_from, save_to) is not False:
            return QtGui.QDialog.accept(self)

    def loadTheme(self, theme):
        log.debug(u'LoadTheme %s', theme)
        if theme == None:
            self.theme.parse(self.baseTheme())
        else:
            xml_file = os.path.join(self.path, theme, theme + u'.xml')
            xml = file_to_xml(xml_file)
            self.theme.parse(xml)
            self.theme.extend_image_filename(self.path)
        self.cleanTheme(self.theme)
        self.allowPreview = False
        self.paintUi(self.theme)
        self.allowPreview = True
        self.previewTheme(self.theme)

    def cleanTheme(self, theme):
        self.theme.background_color = theme.background_color.strip()
        self.theme.background_direction = theme.background_direction.strip()
        self.theme.background_endColor = theme.background_endColor.strip()
        if theme.background_filename:
            self.theme.background_filename = theme.background_filename.strip()
        #self.theme.background_mode
        self.theme.background_startColor = theme.background_startColor.strip()
        #self.theme.background_type
        if theme.display_display:
            self.theme.display_display = theme.display_display.strip()
        self.theme.display_horizontalAlign = \
            theme.display_horizontalAlign.strip()
        self.theme.display_outline = str_to_bool(theme.display_outline)
        #self.theme.display_outline_color
        self.theme.display_shadow = str_to_bool(theme.display_shadow)
        #self.theme.display_shadow_color
        self.theme.display_verticalAlign = \
            theme.display_verticalAlign.strip()
        self.theme.display_wrapStyle = theme.display_wrapStyle.strip()
        self.theme.font_footer_color = theme.font_footer_color.strip()
        self.theme.font_footer_height = theme.font_footer_height.strip()
        self.theme.font_footer_italics = str_to_bool(theme.font_footer_italics)
        self.theme.font_footer_name = theme.font_footer_name.strip()
        #self.theme.font_footer_override
        self.theme.font_footer_proportion = \
            theme.font_footer_proportion.strip()
        self.theme.font_footer_weight = theme.font_footer_weight.strip()
        self.theme.font_footer_width = theme.font_footer_width.strip()
        self.theme.font_footer_x = theme.font_footer_x.strip()
        self.theme.font_footer_y = theme.font_footer_y.strip()
        self.theme.font_main_color = theme.font_main_color.strip()
        self.theme.font_main_height = theme.font_main_height.strip()
        self.theme.font_main_italics = str_to_bool(theme.font_main_italics)
        self.theme.font_main_name = theme.font_main_name.strip()
        #self.theme.font_main_override
        self.theme.font_main_proportion = theme.font_main_proportion.strip()
        self.theme.font_main_weight = theme.font_main_weight.strip()
        self.theme.font_main_x = theme.font_main_x.strip()
        self.theme.font_main_y = theme.font_main_y.strip()
        #self.theme.theme_mode
        self.theme.theme_name = theme.theme_name.strip()
        #self.theme.theme_version

    def onImageToolButtonClicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        if filename != "":
            self.ImageLineEdit.setText(filename)
            self.theme.background_filename = filename
            self.previewTheme(self.theme)
    #
    #Main Font Tab
    #
    def onFontMainComboBoxSelected(self):
        self.theme.font_main_name = self.FontMainComboBox.currentFont().family()
        self.previewTheme(self.theme)

    def onFontMainWeightComboBoxSelected(self, value):
        if value  ==0:
            self.theme.font_main_weight = u'Normal'
            self.theme.font_main_italics = False
        elif value  == 1:
            self.theme.font_main_weight = u'Bold'
            self.theme.font_main_italics = False
        elif value  == 2:
            self.theme.font_main_weight = u'Normal'
            self.theme.font_main_italics = True
        else:
            self.theme.font_main_weight = u'Bold'
            self.theme.font_main_italics = True
        self.previewTheme(self.theme)

    def onFontMainColorPushButtonClicked(self):
        self.theme.font_main_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.theme.font_main_color), self).name()

        self.FontMainColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(self.theme.font_main_color))
        self.previewTheme(self.theme)

    def onFontMainSizeSpinBoxChanged(self):
        if self.theme.font_main_proportion != self.FontMainSizeSpinBox.value():
            self.theme.font_main_proportion = self.FontMainSizeSpinBox.value()
            self.previewTheme(self.theme)

    def onFontMainDefaultCheckBoxChanged(self, value):
        if value == 2:  # checked
            self.theme.font_main_override = False
        else:
            self.theme.font_main_override = True

        if int(self.theme.font_main_x) == 0 and \
            int(self.theme.font_main_y) == 0 and \
            int(self.theme.font_main_width) == 0 and \
            int(self.theme.font_main_height) == 0:
            self.theme.font_main_x = u'10'
            self.theme.font_main_y = u'10'
            self.theme.font_main_width = u'1024'
            self.theme.font_main_height = u'730'
            self.FontMainXSpinBox.setValue(int(self.theme.font_main_x))
            self.FontMainYSpinBox.setValue(int(self.theme.font_main_y))
            self.FontMainWidthSpinBox.setValue(int(self.theme.font_main_width))
            self.FontMainHeightSpinBox.setValue(int( \
                self.theme.font_main_height))
        self.stateChanging(self.theme)
        self.previewTheme(self.theme)

    def onFontMainXSpinBoxChanged(self):
        if self.theme.font_main_x != self.FontMainXSpinBox.value():
            self.theme.font_main_x = self.FontMainXSpinBox.value()
            self.previewTheme(self.theme)

    def onFontMainYSpinBoxChanged(self):
        if self.theme.font_main_y != self.FontMainYSpinBox.value():
            self.theme.font_main_y = self.FontMainYSpinBox.value()
            self.previewTheme(self.theme)

    def onFontMainWidthSpinBoxChanged(self):
        if self.theme.font_main_width != self.FontMainWidthSpinBox.value():
            self.theme.font_main_width = self.FontMainWidthSpinBox.value()
            self.previewTheme(self.theme)

    def onFontMainHeightSpinBoxChanged(self):
        if self.theme.font_main_height != self.FontMainHeightSpinBox.value():
            self.theme.font_main_height = self.FontMainHeightSpinBox.value()
            self.previewTheme(self.theme)
    #
    #Footer Font Tab
    #
    def onFontFooterComboBoxSelected(self):
        self.theme.font_footer_name = \
            self.FontFooterComboBox.currentFont().family()
        self.previewTheme(self.theme)

    def onFontFooterWeightComboBoxSelected(self, value):
        if value  == 0:
            self.theme.font_footer_weight = u'Normal'
            self.theme.font_footer_italics = False
        elif value  == 1:
            self.theme.font_footer_weight = u'Bold'
            self.theme.font_footer_italics = False
        elif value  == 2:
            self.theme.font_footer_weight = u'Normal'
            self.theme.font_footer_italics = True
        else:
            self.theme.font_footer_weight = u'Bold'
            self.theme.font_footer_italics = True
        self.previewTheme(self.theme)

    def onFontFooterColorPushButtonClicked(self):
        self.theme.font_footer_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.theme.font_footer_color), self).name()

        self.FontFooterColorPushButton.setStyleSheet(
            'background-color: %s' % unicode(self.theme.font_footer_color))
        self.previewTheme(self.theme)

    def onFontFooterSizeSpinBoxChanged(self):
        if self.theme.font_footer_proportion != \
            self.FontFooterSizeSpinBox.value():
            self.theme.font_footer_proportion = \
                self.FontFooterSizeSpinBox.value()
            self.previewTheme(self.theme)

    def onFontFooterDefaultCheckBoxChanged(self, value):
        if value == 2:  # checked
            self.theme.font_footer_override = False
        else:
            self.theme.font_footer_override = True

        if int(self.theme.font_footer_x) == 0 and \
            int(self.theme.font_footer_y) == 0 and \
            int(self.theme.font_footer_width) == 0 and \
            int(self.theme.font_footer_height) == 0:
            self.theme.font_footer_x = u'10'
            self.theme.font_footer_y = u'730'
            self.theme.font_footer_width = u'1024'
            self.theme.font_footer_height = u'38'

            self.FontFooterXSpinBox.setValue(int(self.theme.font_footer_x))
            self.FontFooterYSpinBox.setValue(int(self.theme.font_footer_y))
            self.FontFooterWidthSpinBox.setValue(int( \
                self.theme.font_footer_width))
            self.FontFooterHeightSpinBox.setValue(int( \
                self.theme.font_footer_height))

        self.stateChanging(self.theme)
        self.previewTheme(self.theme)

    def onFontFooterXSpinBoxChanged(self):
        if self.theme.font_footer_x != self.FontFooterXSpinBox.value():
            self.theme.font_footer_x = self.FontFooterXSpinBox.value()
            self.previewTheme(self.theme)

    def onFontFooterYSpinBoxChanged(self):
        if self.theme.font_footer_y != self.FontFooterYSpinBox.value():
            self.theme.font_footer_y = self.FontFooterYSpinBox.value()
            self.previewTheme(self.theme)

    def onFontFooterWidthSpinBoxChanged(self):
        if self.theme.font_footer_width != self.FontFooterWidthSpinBox.value():
            self.theme.font_footer_width = self.FontFooterWidthSpinBox.value()
            self.previewTheme(self.theme)

    def onFontFooterHeightSpinBoxChanged(self):
        if self.theme.font_footer_height != \
            self.FontFooterHeightSpinBox.value():
            self.theme.font_footer_height = self.FontFooterHeightSpinBox.value()
            self.previewTheme(self.theme)
    #
    #Background Tab
    #
    def onGradientComboBoxSelected(self, currentIndex):
        self.setBackground(self.BackgroundTypeComboBox.currentIndex(),
            currentIndex)

    def onBackgroundComboBoxSelected(self, currentIndex):
        if currentIndex == 0: # Opaque
            self.theme.background_mode = u'opaque'
        else:
            self.theme.background_mode = u'transparent'
        self.stateChanging(self.theme)
        self.previewTheme(self.theme)

    def onBackgroundTypeComboBoxSelected(self, currentIndex):
        self.setBackground(currentIndex, self.GradientComboBox.currentIndex())

    def setBackground(self, background, gradient):
        if background == 0: # Solid
            self.theme.background_type = u'solid'
            if self.theme.background_color is None :
                self.theme.background_color = u'#000000'
        elif background == 1: # Gradient
            self.theme.background_type = u'gradient'
            if gradient == 0: # Horizontal
                self.theme.background_direction = u'horizontal'
            elif gradient == 1: # vertical
                self.theme.background_direction = u'vertical'
            else:
                self.theme.background_direction = u'circular'
            if self.theme.background_startColor is None :
                self.theme.background_startColor = u'#000000'
            if self.theme.background_endColor is None :
                self.theme.background_endColor = u'#ff0000'
        else:
            self.theme.background_type = u'image'
        self.stateChanging(self.theme)
        self.previewTheme(self.theme)

    def onColor1PushButtonClicked(self):
        if self.theme.background_type == u'solid':
            self.theme.background_color = QtGui.QColorDialog.getColor(
                QtGui.QColor(self.theme.background_color), self).name()
            self.Color1PushButton.setStyleSheet(
                u'background-color: %s' % unicode(self.theme.background_color))
        else:
            self.theme.background_startColor = QtGui.QColorDialog.getColor(
                QtGui.QColor(self.theme.background_startColor), self).name()
            self.Color1PushButton.setStyleSheet(
                u'background-color: %s' % \
                    unicode(self.theme.background_startColor))

        self.previewTheme(self.theme)

    def onColor2PushButtonClicked(self):
        self.theme.background_endColor = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.theme.background_endColor), self).name()
        self.Color2PushButton.setStyleSheet(
            u'background-color: %s' % unicode(self.theme.background_endColor))

        self.previewTheme(self.theme)
    #
    #Other Tab
    #
    def onOutlineCheckBoxChanged(self, value):
        if value == 2:  # checked
            self.theme.display_outline = True
        else:
            self.theme.display_outline = False
        self.stateChanging(self.theme)
        self.previewTheme(self.theme)

    def onOutlineColorPushButtonClicked(self):
        self.theme.display_outline_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.theme.display_outline_color), self).name()
        self.OutlineColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(self.theme.display_outline_color))
        self.previewTheme(self.theme)

    def onShadowCheckBoxChanged(self, value):
        if value == 2:  # checked
            self.theme.display_shadow = True
        else:
            self.theme.display_shadow = False
        self.stateChanging(self.theme)
        self.previewTheme(self.theme)

    def onShadowColorPushButtonClicked(self):
        self.theme.display_shadow_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.theme.display_shadow_color), self).name()
        self.ShadowColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(self.theme.display_shadow_color))
        self.previewTheme(self.theme)

    def onHorizontalComboBoxSelected(self, currentIndex):
        self.theme.display_horizontalAlign = currentIndex
        self.stateChanging(self.theme)
        self.previewTheme(self.theme)

    def onVerticalComboBoxSelected(self, currentIndex):
        self.theme.display_verticalAlign = currentIndex
        self.stateChanging(self.theme)
        self.previewTheme(self.theme)
    #
    #Local Methods
    #
    def baseTheme(self):
        log.debug(u'base theme created')
        newtheme = ThemeXML()
        newtheme.new_document(u'New Theme')
        newtheme.add_background_solid(unicode(u'#000000'))
        newtheme.add_font(unicode(QtGui.QFont().family()), unicode(u'#FFFFFF'),
            unicode(30), u'False')
        newtheme.add_font(unicode(QtGui.QFont().family()), unicode(u'#FFFFFF'),
            unicode(12), u'False', u'footer')
        newtheme.add_display(u'False', unicode(u'#FFFFFF'), u'False',
            unicode(u'#FFFFFF'),
            unicode(0), unicode(0), unicode(0))

        return newtheme.extract_xml()

    def paintUi(self, theme):
        self.stateChanging(theme)
        self.ThemeNameEdit.setText(self.theme.theme_name)
        if self.theme.background_mode == u'opaque':
            self.BackgroundComboBox.setCurrentIndex(0)
        else:
            self.BackgroundComboBox.setCurrentIndex(1)

        if theme.background_type == u'solid':
            self.BackgroundTypeComboBox.setCurrentIndex(0)
        elif theme.background_type == u'gradient':
            self.BackgroundTypeComboBox.setCurrentIndex(1)
        else:
            self.BackgroundTypeComboBox.setCurrentIndex(2)

        if self.theme.background_direction == u'horizontal':
            self.GradientComboBox.setCurrentIndex(0)
        elif self.theme.background_direction == u'vertical':
            self.GradientComboBox.setCurrentIndex(1)
        else:
            self.GradientComboBox.setCurrentIndex(2)

        self.FontMainSizeSpinBox.setValue(int(self.theme.font_main_proportion))
        if not self.theme.font_main_italics and \
            self.theme.font_main_weight == u'Normal':
            self.FontMainWeightComboBox.setCurrentIndex(0)
        elif not self.theme.font_main_italics and \
            self.theme.font_main_weight == u'Bold':
            self.FontMainWeightComboBox.setCurrentIndex(1)
        elif self.theme.font_main_italics and \
            self.theme.font_main_weight == u'Normal':
            self.FontMainWeightComboBox.setCurrentIndex(2)
        else:
            self.FontMainWeightComboBox.setCurrentIndex(3)

        self.FontMainXSpinBox.setValue(int(self.theme.font_main_x))
        self.FontMainYSpinBox.setValue(int(self.theme.font_main_y))
        self.FontMainWidthSpinBox.setValue(int(self.theme.font_main_width))
        self.FontMainHeightSpinBox.setValue(int(self.theme.font_main_height))
        self.FontFooterSizeSpinBox.setValue(
            int(self.theme.font_footer_proportion))
        if not self.theme.font_footer_italics and \
            self.theme.font_footer_weight == u'Normal':
            self.FontFooterWeightComboBox.setCurrentIndex(0)
        elif not self.theme.font_footer_italics and \
            self.theme.font_footer_weight == u'Bold':
            self.FontFooterWeightComboBox.setCurrentIndex(1)
        elif self.theme.font_footer_italics and \
            self.theme.font_footer_weight == u'Normal':
            self.FontFooterWeightComboBox.setCurrentIndex(2)
        else:
            self.FontFooterWeightComboBox.setCurrentIndex(3)
        self.FontFooterXSpinBox.setValue(int(self.theme.font_footer_x))
        self.FontFooterYSpinBox.setValue(int(self.theme.font_footer_y))
        self.FontFooterWidthSpinBox.setValue(int(self.theme.font_footer_width))
        self.FontFooterHeightSpinBox.setValue(
            int(self.theme.font_footer_height))
        self.FontMainColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(theme.font_main_color))
        self.FontFooterColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(theme.font_footer_color))

        if self.theme.font_main_override == False:
            self.FontMainDefaultCheckBox.setChecked(True)
        else:
            self.FontMainDefaultCheckBox.setChecked(False)

        if self.theme.font_footer_override == False:
            self.FontFooterDefaultCheckBox.setChecked(True)
        else:
            self.FontFooterDefaultCheckBox.setChecked(False)

        self.OutlineColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(theme.display_outline_color))
        self.ShadowColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(theme.display_shadow_color))

        if self.theme.display_outline:
            self.OutlineCheckBox.setChecked(True)
            self.OutlineColorPushButton.setEnabled(True)
        else:
            self.OutlineCheckBox.setChecked(False)
            self.OutlineColorPushButton.setEnabled(False)

        if self.theme.display_shadow:
            self.ShadowCheckBox.setChecked(True)
            self.ShadowColorPushButton.setEnabled(True)
        else:
            self.ShadowCheckBox.setChecked(False)
            self.ShadowColorPushButton.setEnabled(False)

        self.HorizontalComboBox.setCurrentIndex(
            int(self.theme.display_horizontalAlign))
        self.VerticalComboBox.setCurrentIndex(
            int(self.theme.display_verticalAlign))

    def stateChanging(self, theme):
        if theme.background_mode == u'transparent':
                self.Color1Label.setVisible(False)
                self.Color1PushButton.setVisible(False)
                self.Color2Label.setVisible(False)
                self.Color2PushButton.setVisible(False)
                self.ImageLabel.setVisible(False)
                self.ImageLineEdit.setVisible(False)
                self.ImageFilenameWidget.setVisible(False)
                self.GradientLabel.setVisible(False)
                self.GradientComboBox.setVisible(False)
                self.BackgroundTypeComboBox.setVisible(False)
                self.BackgroundTypeLabel.setVisible(False)
        else:
            self.BackgroundTypeComboBox.setVisible(True)
            self.BackgroundTypeLabel.setVisible(True)
            if theme.background_type == u'solid':
                self.Color1PushButton.setStyleSheet(
                    u'background-color: %s' % unicode(theme.background_color))
                self.Color1Label.setText(translate(u'ThemeManager',
                    u'Background Color:'))
                self.Color1Label.setVisible(True)
                self.Color1PushButton.setVisible(True)
                self.Color2Label.setVisible(False)
                self.Color2PushButton.setVisible(False)
                self.ImageLabel.setVisible(False)
                self.ImageLineEdit.setVisible(False)
                self.ImageFilenameWidget.setVisible(False)
                self.GradientLabel.setVisible(False)
                self.GradientComboBox.setVisible(False)
            elif theme.background_type == u'gradient':
                self.Color1PushButton.setStyleSheet(u'background-color: %s' \
                    % unicode(theme.background_startColor))
                self.Color2PushButton.setStyleSheet(u'background-color: %s' \
                    % unicode(theme.background_endColor))
                self.Color1Label.setText(translate(u'ThemeManager',
                    u'First  Color:'))
                self.Color2Label.setText(translate(u'ThemeManager',
                    u'Second Color:'))
                self.Color1Label.setVisible(True)
                self.Color1PushButton.setVisible(True)
                self.Color2Label.setVisible(True)
                self.Color2PushButton.setVisible(True)
                self.ImageLabel.setVisible(False)
                self.ImageLineEdit.setVisible(False)
                self.ImageFilenameWidget.setVisible(False)
                self.GradientLabel.setVisible(True)
                self.GradientComboBox.setVisible(True)
            else: # must be image
                self.Color1Label.setVisible(False)
                self.Color1PushButton.setVisible(False)
                self.Color2Label.setVisible(False)
                self.Color2PushButton.setVisible(False)
                self.ImageLabel.setVisible(True)
                self.ImageLineEdit.setVisible(True)
                self.ImageFilenameWidget.setVisible(True)
                self.GradientLabel.setVisible(False)
                self.GradientComboBox.setVisible(False)

        if theme.font_main_override == False:
            self.FontMainXSpinBox.setEnabled(False)
            self.FontMainYSpinBox.setEnabled(False)
            self.FontMainWidthSpinBox.setEnabled(False)
            self.FontMainHeightSpinBox.setEnabled(False)
        else:
            self.FontMainXSpinBox.setEnabled(True)
            self.FontMainYSpinBox.setEnabled(True)
            self.FontMainWidthSpinBox.setEnabled(True)
            self.FontMainHeightSpinBox.setEnabled(True)

        if theme.font_footer_override == False:
            self.FontFooterXSpinBox.setEnabled(False)
            self.FontFooterYSpinBox.setEnabled(False)
            self.FontFooterWidthSpinBox.setEnabled(False)
            self.FontFooterHeightSpinBox.setEnabled(False)
        else:
            self.FontFooterXSpinBox.setEnabled(True)
            self.FontFooterYSpinBox.setEnabled(True)
            self.FontFooterWidthSpinBox.setEnabled(True)
            self.FontFooterHeightSpinBox.setEnabled(True)

        if self.theme.display_outline:
            self.OutlineColorPushButton.setEnabled(True)
        else:
            self.OutlineColorPushButton.setEnabled(False)

        if self.theme.display_shadow:
            self.ShadowColorPushButton.setEnabled(True)
        else:
            self.ShadowColorPushButton.setEnabled(False)

    def previewTheme(self, theme):
        if self.allowPreview:
            frame = self.thememanager.generateImage(theme)
            self.ThemePreview.setPixmap(QtGui.QPixmap.fromImage(frame))
