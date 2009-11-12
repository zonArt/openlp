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
import os
import os.path

from PyQt4 import QtCore, QtGui

from openlp.core.lib import ThemeXML
from amendthemedialog import Ui_AmendThemeDialog

log = logging.getLogger(u'AmendThemeForm')

class AmendThemeForm(QtGui.QDialog, Ui_AmendThemeDialog):

    def __init__(self, thememanager, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.thememanager = thememanager
        self.path = None
        self.theme = ThemeXML()
        self.setupUi(self)
        #define signals
        #Buttons
        QtCore.QObject.connect(self.Color1PushButton,
            QtCore.SIGNAL(u'pressed()'), self.onColor1PushButtonClicked)
        QtCore.QObject.connect(self.Color2PushButton,
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
        QtCore.QObject.connect(self.FontMainLineSpacingSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontMainLineSpacingSpinBoxChanged)
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
        new_theme.new_document(theme_name.encode('unicode-escape'))
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
                save_to = os.path.join(self.path, theme_name, filename)
                save_from = self.theme.background_filename

        new_theme.add_font(unicode(self.theme.font_main_name),
                unicode(self.theme.font_main_color),
                unicode(self.theme.font_main_proportion),
                unicode(self.theme.font_main_override), u'main',
                unicode(self.theme.font_main_weight),
                unicode(self.theme.font_main_italics),
                unicode(self.theme.font_main_indentation),
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
                0,
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
        self.theme = self.thememanager.getThemeData(theme)
        # Stop the initial screen setup generating 1 preview per field!
        self.allowPreview = False
        self.paintUi(self.theme)
        self.allowPreview = True
        self.previewTheme(self.theme)

    def onImageToolButtonClicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(
            self, self.trUtf8('Open file'))
        if filename:
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
        if value == 0:
            self.theme.font_main_weight = u'Normal'
            self.theme.font_main_italics = False
        elif value == 1:
            self.theme.font_main_weight = u'Bold'
            self.theme.font_main_italics = False
        elif value == 2:
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

        if not self.theme.font_main_x and not self.theme.font_main_y and \
            not self.theme.font_main_width and not self.theme.font_main_height:
            self.theme.font_main_x = u'10'
            self.theme.font_main_y = u'10'
            self.theme.font_main_width = u'1024'
            self.theme.font_main_height = u'730'
            self.FontMainXSpinBox.setValue(self.theme.font_main_x)
            self.FontMainYSpinBox.setValue(self.theme.font_main_y)
            self.FontMainWidthSpinBox.setValue(self.theme.font_main_width)
            self.FontMainHeightSpinBox.setValue(self.theme.font_main_height)
            self.FontMainLineSpacingSpinBox.setValue(
                self.theme.font_main_indentation)
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

    def onFontMainLineSpacingSpinBoxChanged(self):
        if self.theme.font_main_indentation != \
            self.FontMainLineSpacingSpinBox.value():
            self.theme.font_main_indentation = \
                self.FontMainLineSpacingSpinBox.value()
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
        if value == 0:
            self.theme.font_footer_weight = u'Normal'
            self.theme.font_footer_italics = False
        elif value == 1:
            self.theme.font_footer_weight = u'Bold'
            self.theme.font_footer_italics = False
        elif value == 2:
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
        if not self.theme.font_footer_x and not self.theme.font_footer_y and \
            not self.theme.font_footer_width and \
            not self.theme.font_footer_height:
            self.theme.font_footer_x = u'10'
            self.theme.font_footer_y = u'730'
            self.theme.font_footer_width = u'1024'
            self.theme.font_footer_height = u'38'
            self.FontFooterXSpinBox.setValue(self.theme.font_footer_x)
            self.FontFooterYSpinBox.setValue(self.theme.font_footer_y)
            self.FontFooterWidthSpinBox.setValue(self.theme.font_footer_width)
            self.FontFooterHeightSpinBox.setValue(
                self.theme.font_footer_height)
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
            self.theme.font_footer_height = \
                self.FontFooterHeightSpinBox.value()
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
    def paintUi(self, theme):
        self.stateChanging(theme)
        self.ThemeNameEdit.setText(self.theme.theme_name)
        # Background Tab
        if self.theme.background_mode == u'opaque':
            self.BackgroundComboBox.setCurrentIndex(0)
        else:
            self.BackgroundComboBox.setCurrentIndex(1)
        self.ImageLineEdit.setText(u'')
        if theme.background_type == u'solid':
            self.BackgroundTypeComboBox.setCurrentIndex(0)
        elif theme.background_type == u'gradient':
            self.BackgroundTypeComboBox.setCurrentIndex(1)
        else:
            self.BackgroundTypeComboBox.setCurrentIndex(2)
            self.ImageLineEdit.setText(self.theme.background_filename)
        if self.theme.background_direction == u'horizontal':
            self.GradientComboBox.setCurrentIndex(0)
        elif self.theme.background_direction == u'vertical':
            self.GradientComboBox.setCurrentIndex(1)
        else:
            self.GradientComboBox.setCurrentIndex(2)
        # Font Main Tab
        self.FontMainComboBox.setCurrentFont(
            QtGui.QFont(self.theme.font_main_name))
        self.FontMainSizeSpinBox.setValue(self.theme.font_main_proportion)
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
        self.FontMainLineSpacingSpinBox.setValue(
            self.theme.font_main_indentation)
        self.FontMainXSpinBox.setValue(self.theme.font_main_x)
        self.FontMainYSpinBox.setValue(self.theme.font_main_y)
        self.FontMainWidthSpinBox.setValue(self.theme.font_main_width)
        self.FontMainHeightSpinBox.setValue(self.theme.font_main_height)
        # Font Footer Tab
        self.FontFooterComboBox.setCurrentFont(
            QtGui.QFont(self.theme.font_footer_name))
        self.FontFooterSizeSpinBox.setValue(
            self.theme.font_footer_proportion)
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
        self.FontFooterXSpinBox.setValue(self.theme.font_footer_x)
        self.FontFooterYSpinBox.setValue(self.theme.font_footer_y)
        self.FontFooterWidthSpinBox.setValue(self.theme.font_footer_width)
        self.FontFooterHeightSpinBox.setValue(self.theme.font_footer_height)
        self.FontMainColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(theme.font_main_color))
        self.FontFooterColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(theme.font_footer_color))

        if not self.theme.font_main_override:
            self.FontMainDefaultCheckBox.setChecked(True)
        else:
            self.FontMainDefaultCheckBox.setChecked(False)

        if not self.theme.font_footer_override:
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
            self.theme.display_horizontalAlign)
        self.VerticalComboBox.setCurrentIndex(self.theme.display_verticalAlign)

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
                self.Color1Label.setText(self.trUtf8(u'Background Color:'))
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
                self.Color1Label.setText(self.trUtf8(u'First  Color:'))
                self.Color2Label.setText(self.trUtf8(u'Second Color:'))
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

        if not theme.font_main_override:
            self.FontMainXSpinBox.setEnabled(False)
            self.FontMainYSpinBox.setEnabled(False)
            self.FontMainWidthSpinBox.setEnabled(False)
            self.FontMainHeightSpinBox.setEnabled(False)
        else:
            self.FontMainXSpinBox.setEnabled(True)
            self.FontMainYSpinBox.setEnabled(True)
            self.FontMainWidthSpinBox.setEnabled(True)
            self.FontMainHeightSpinBox.setEnabled(True)

        if not theme.font_footer_override:
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
            #calculate main number of rows
            main_weight = 50
            if self.theme.font_main_weight == u'Bold':
                main_weight = 75
            mainFont = QtGui.QFont(self.theme.font_main_name,
                         self.theme.font_main_proportion, # size
                         main_weight, # weight
                         self.theme.font_main_italics)# italic
            mainFont.setPixelSize(self.theme.font_main_proportion)
            metrics = QtGui.QFontMetrics(mainFont)
            page_length = \
                (self.FontMainHeightSpinBox.value() / metrics.height() - 2) - 1
            log.debug(u'Page Length area height %s, metrics %s, lines %s' %
                (self.FontMainHeightSpinBox.value(), metrics.height(),
                page_length))
            page_length_text = unicode(self.trUtf8(u'Slide Height is %s rows'))
            self.FontMainLinesPageLabel.setText(page_length_text % page_length)
            frame = self.thememanager.generateImage(theme)
            self.ThemePreview.setPixmap(QtGui.QPixmap.fromImage(frame))

