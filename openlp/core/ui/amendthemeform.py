# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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

import logging
import os
import os.path

from PyQt4 import QtCore, QtGui

from openlp.core.lib import ThemeXML, translate
from openlp.core.utils import get_images_filter
from amendthemedialog import Ui_AmendThemeDialog

log = logging.getLogger(u'AmendThemeForm')

class AmendThemeForm(QtGui.QDialog, Ui_AmendThemeDialog):
    """
    The :class:`AmendThemeForm` class provides the user interface to set up
    new and edit existing themes.
    """
    def __init__(self, parent):
        """
        Initialise the theme editor user interface
        """
        QtGui.QDialog.__init__(self, parent)
        self.thememanager = parent
        self.path = None
        self.theme = ThemeXML()
        self.setupUi(self)
        # Buttons
        QtCore.QObject.connect(self.color1PushButton,
            QtCore.SIGNAL(u'pressed()'), self.onColor1PushButtonClicked)
        QtCore.QObject.connect(self.color2PushButton,
            QtCore.SIGNAL(u'pressed()'), self.onColor2PushButtonClicked)
        QtCore.QObject.connect(self.fontMainColorPushButton,
            QtCore.SIGNAL(u'pressed()'), self.onFontMainColorPushButtonClicked)
        QtCore.QObject.connect(self.fontFooterColorPushButton,
            QtCore.SIGNAL(u'pressed()'),
            self.onFontFooterColorPushButtonClicked)
        QtCore.QObject.connect(self.outlineColorPushButton,
            QtCore.SIGNAL(u'pressed()'), self.onOutlineColorPushButtonClicked)
        QtCore.QObject.connect(self.shadowColorPushButton,
            QtCore.SIGNAL(u'pressed()'), self.onShadowColorPushButtonClicked)
        QtCore.QObject.connect(self.imageToolButton,
            QtCore.SIGNAL(u'clicked()'), self.onImageToolButtonClicked)
        # Combo boxes
        QtCore.QObject.connect(self.backgroundTypeComboBox,
            QtCore.SIGNAL(u'activated(int)'),
            self.onBackgroundTypeComboBoxSelected)
        QtCore.QObject.connect(self.gradientComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onGradientComboBoxSelected)
        QtCore.QObject.connect(self.fontMainComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onFontMainComboBoxSelected)
        QtCore.QObject.connect(self.fontMainWeightComboBox,
            QtCore.SIGNAL(u'activated(int)'),
            self.onFontMainWeightComboBoxSelected)
        QtCore.QObject.connect(self.fontFooterComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onFontFooterComboBoxSelected)
        QtCore.QObject.connect(self.fontFooterWeightComboBox,
            QtCore.SIGNAL(u'activated(int)'),
            self.onFontFooterWeightComboBoxSelected)
        QtCore.QObject.connect(self.horizontalComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onHorizontalComboBoxSelected)
        QtCore.QObject.connect(self.verticalComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onVerticalComboBoxSelected)
        # Spin boxes
        QtCore.QObject.connect(self.fontMainSizeSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontMainSizeSpinBoxChanged)
        QtCore.QObject.connect(self.fontMainLineAdjustmentSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontMainLineAdjustmentSpinBoxChanged)
        QtCore.QObject.connect(self.shadowSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onShadowSpinBoxChanged)
        QtCore.QObject.connect(self.outlineSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onOutlineSpinBoxChanged)

        QtCore.QObject.connect(self.fontFooterSizeSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontFooterSizeSpinBoxChanged)
        QtCore.QObject.connect(self.fontMainXSpinBox,
            QtCore.SIGNAL(u'editingFinished()'), self.onFontMainXSpinBoxChanged)
        QtCore.QObject.connect(self.fontMainYSpinBox,
            QtCore.SIGNAL(u'editingFinished()'), self.onFontMainYSpinBoxChanged)
        QtCore.QObject.connect(self.fontMainWidthSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontMainWidthSpinBoxChanged)
        QtCore.QObject.connect(self.fontMainHeightSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontMainHeightSpinBoxChanged)
        QtCore.QObject.connect(self.fontMainLineAdjustmentSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontMainLineAdjustmentSpinBoxChanged)
        QtCore.QObject.connect(self.fontFooterXSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontFooterXSpinBoxChanged)
        QtCore.QObject.connect(self.fontFooterYSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontFooterYSpinBoxChanged)
        QtCore.QObject.connect(self.fontFooterWidthSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontFooterWidthSpinBoxChanged)
        QtCore.QObject.connect(self.fontFooterHeightSpinBox,
            QtCore.SIGNAL(u'editingFinished()'),
            self.onFontFooterHeightSpinBoxChanged)

        # CheckBoxes
        QtCore.QObject.connect(self.fontMainDefaultCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onFontMainDefaultCheckBoxChanged)
        QtCore.QObject.connect(self.fontFooterDefaultCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onFontFooterDefaultCheckBoxChanged)
        QtCore.QObject.connect(self.outlineCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.onOutlineCheckBoxChanged)
        QtCore.QObject.connect(self.shadowCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.onShadowCheckBoxChanged)
        QtCore.QObject.connect(self.slideTransitionCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onSlideTransitionCheckBoxChanged)

    def accept(self):
        new_theme = ThemeXML()
        theme_name = unicode(self.themeNameEdit.text())
        new_theme.new_document(theme_name)
        save_from = None
        save_to = None
        if self.theme.background_type == u'solid':
            new_theme.add_background_solid(
                unicode(self.theme.background_color))
        elif self.theme.background_type == u'gradient':
            new_theme.add_background_gradient(
                unicode(self.theme.background_start_color),
                unicode(self.theme.background_end_color),
                self.theme.background_direction)
        else:
            filename = \
                os.path.split(unicode(self.theme.background_filename))[1]
            new_theme.add_background_image(filename)
            save_to = os.path.join(self.path, theme_name, filename)
            save_from = self.theme.background_filename
        new_theme.add_font(unicode(self.theme.font_main_name),
                unicode(self.theme.font_main_color),
                unicode(self.theme.font_main_proportion),
                unicode(self.theme.font_main_override), u'main',
                unicode(self.theme.font_main_weight),
                unicode(self.theme.font_main_italics),
                unicode(self.theme.font_main_line_adjustment),
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
                0, # line adjustment
                unicode(self.theme.font_footer_x),
                unicode(self.theme.font_footer_y),
                unicode(self.theme.font_footer_width),
                unicode(self.theme.font_footer_height))
        new_theme.add_display(unicode(self.theme.display_shadow),
                unicode(self.theme.display_shadow_color),
                unicode(self.theme.display_outline),
                unicode(self.theme.display_outline_color),
                unicode(self.theme.display_horizontal_align),
                unicode(self.theme.display_vertical_align),
                unicode(self.theme.display_wrap_style),
                unicode(self.theme.display_slide_transition),
                unicode(self.theme.display_shadow_size),
                unicode(self.theme.display_outline_size))
        theme = new_theme.extract_xml()
        pretty_theme = new_theme.extract_formatted_xml()
        if self.thememanager.saveTheme(theme_name, theme, pretty_theme,
            save_from, save_to) is not False:
            return QtGui.QDialog.accept(self)

    def loadTheme(self, theme):
        log.debug(u'LoadTheme %s', theme)
        self.theme = theme
        # Stop the initial screen setup generating 1 preview per field!
        self.allowPreview = False
        self.paintUi(self.theme)
        self.allowPreview = True
        self.previewTheme()

    def onImageToolButtonClicked(self):
        images_filter = get_images_filter()
        images_filter = '%s;;%s (*.*) (*)' % (images_filter,
            translate('OpenLP.AmendThemeForm', 'All Files'))
        filename = QtGui.QFileDialog.getOpenFileName(self,
            translate('OpenLP.AmendThemeForm', 'Select Image'), u'',
            images_filter)
        if filename:
            self.imageLineEdit.setText(filename)
            self.theme.background_filename = filename
            self.previewTheme()
    #
    # Main Font Tab
    #
    def onFontMainComboBoxSelected(self):
        self.theme.font_main_name = self.fontMainComboBox.currentFont().family()
        self.previewTheme()

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
        self.previewTheme()

    def onFontMainColorPushButtonClicked(self):
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.theme.font_main_color), self)
        if new_color.isValid():
            self.theme.font_main_color = new_color.name()
            self.fontMainColorPushButton.setStyleSheet(
                u'background-color: %s' % unicode(self.theme.font_main_color))
            self.previewTheme()

    def onFontMainSizeSpinBoxChanged(self):
        if self.theme.font_main_proportion != self.fontMainSizeSpinBox.value():
            self.theme.font_main_proportion = self.fontMainSizeSpinBox.value()
            self.previewTheme()

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
            self.fontMainXSpinBox.setValue(self.theme.font_main_x)
            self.fontMainYSpinBox.setValue(self.theme.font_main_y)
            self.fontMainWidthSpinBox.setValue(self.theme.font_main_width)
            self.fontMainHeightSpinBox.setValue(self.theme.font_main_height)
            self.fontMainLineAdjustmentSpinBox.setValue(
                self.theme.font_main_line_adjustment)
        self.stateChanging(self.theme)
        self.previewTheme()

    def onFontMainXSpinBoxChanged(self):
        if self.theme.font_main_x != self.fontMainXSpinBox.value():
            self.theme.font_main_x = self.fontMainXSpinBox.value()
            self.previewTheme()

    def onFontMainYSpinBoxChanged(self):
        if self.theme.font_main_y != self.fontMainYSpinBox.value():
            self.theme.font_main_y = self.fontMainYSpinBox.value()
            self.previewTheme()

    def onFontMainWidthSpinBoxChanged(self):
        if self.theme.font_main_width != self.fontMainWidthSpinBox.value():
            self.theme.font_main_width = self.fontMainWidthSpinBox.value()
            self.previewTheme()

    def onFontMainLineAdjustmentSpinBoxChanged(self):
        if self.theme.font_main_line_adjustment != \
            self.fontMainLineAdjustmentSpinBox.value():
            self.theme.font_main_line_adjustment = \
                self.fontMainLineAdjustmentSpinBox.value()
            self.previewTheme()

    def onFontMainHeightSpinBoxChanged(self):
        if self.theme.font_main_height != self.fontMainHeightSpinBox.value():
            self.theme.font_main_height = self.fontMainHeightSpinBox.value()
            self.previewTheme()
    #
    # Footer Font Tab
    #
    def onFontFooterComboBoxSelected(self):
        self.theme.font_footer_name = \
            self.fontFooterComboBox.currentFont().family()
        self.previewTheme()

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
        self.previewTheme()

    def onFontFooterColorPushButtonClicked(self):
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.theme.font_footer_color), self)
        if new_color.isValid():
            self.theme.font_footer_color = new_color.name()
            self.fontFooterColorPushButton.setStyleSheet(
                u'background-color: %s' % unicode(self.theme.font_footer_color))
            self.previewTheme()

    def onFontFooterSizeSpinBoxChanged(self):
        if self.theme.font_footer_proportion != \
            self.fontFooterSizeSpinBox.value():
            self.theme.font_footer_proportion = \
                self.fontFooterSizeSpinBox.value()
            self.previewTheme()

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
            self.fontFooterXSpinBox.setValue(self.theme.font_footer_x)
            self.fontFooterYSpinBox.setValue(self.theme.font_footer_y)
            self.fontFooterWidthSpinBox.setValue(self.theme.font_footer_width)
            self.fontFooterHeightSpinBox.setValue(
                self.theme.font_footer_height)
        self.stateChanging(self.theme)
        self.previewTheme()

    def onFontFooterXSpinBoxChanged(self):
        if self.theme.font_footer_x != self.fontFooterXSpinBox.value():
            self.theme.font_footer_x = self.fontFooterXSpinBox.value()
            self.previewTheme()

    def onFontFooterYSpinBoxChanged(self):
        if self.theme.font_footer_y != self.fontFooterYSpinBox.value():
            self.theme.font_footer_y = self.fontFooterYSpinBox.value()
            self.previewTheme()

    def onFontFooterWidthSpinBoxChanged(self):
        if self.theme.font_footer_width != self.fontFooterWidthSpinBox.value():
            self.theme.font_footer_width = self.fontFooterWidthSpinBox.value()
            self.previewTheme()

    def onFontFooterHeightSpinBoxChanged(self):
        if self.theme.font_footer_height != \
            self.fontFooterHeightSpinBox.value():
            self.theme.font_footer_height = \
                self.fontFooterHeightSpinBox.value()
            self.previewTheme()
    #
    # Background Tab
    #
    def onGradientComboBoxSelected(self, currentIndex):
        self.setBackground(self.backgroundTypeComboBox.currentIndex(),
            currentIndex)

    def onBackgroundTypeComboBoxSelected(self, currentIndex):
        self.setBackground(currentIndex, self.gradientComboBox.currentIndex())

    def setBackground(self, background, gradient):
        if background == 0: # Solid
            self.theme.background_type = u'solid'
            if self.theme.background_color is None:
                self.theme.background_color = u'#000000'
            self.imageLineEdit.setText(u'')
        elif background == 1: # Gradient
            self.theme.background_type = u'gradient'
            if gradient == 0: # Horizontal
                self.theme.background_direction = u'horizontal'
            elif gradient == 1: # vertical
                self.theme.background_direction = u'vertical'
            else:
                self.theme.background_direction = u'circular'
            if self.theme.background_start_color is None:
                self.theme.background_start_color = u'#000000'
            if self.theme.background_end_color is None:
                self.theme.background_end_color = u'#ff0000'
            self.imageLineEdit.setText(u'')
        else:
            self.theme.background_type = u'image'
        self.stateChanging(self.theme)
        self.previewTheme()

    def onColor1PushButtonClicked(self):
        if self.theme.background_type == u'solid':
            new_color = QtGui.QColorDialog.getColor(
                QtGui.QColor(self.theme.background_color), self)
            if new_color.isValid():
                self.theme.background_color = new_color.name()
                self.color1PushButton.setStyleSheet(u'background-color: %s' %
                    unicode(self.theme.background_color))
        else:
            new_color = QtGui.QColorDialog.getColor(
                QtGui.QColor(self.theme.background_start_color), self)
            if new_color.isValid():
                self.theme.background_start_color = new_color.name()
                self.color1PushButton.setStyleSheet(u'background-color: %s' %
                    unicode(self.theme.background_start_color))
        self.previewTheme()

    def onColor2PushButtonClicked(self):
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.theme.background_end_color), self)
        if new_color.isValid():
            self.theme.background_end_color = new_color.name()
            self.color2PushButton.setStyleSheet(u'background-color: %s' %
                unicode(self.theme.background_end_color))
            self.previewTheme()
    #
    # Other Tab
    #
    def onOutlineCheckBoxChanged(self, value):
        if value == 2:  # checked
            self.theme.display_outline = True
        else:
            self.theme.display_outline = False
        self.stateChanging(self.theme)
        self.previewTheme()

    def onOutlineSpinBoxChanged(self):
        if self.theme.display_outline_size != self.outlineSpinBox.value():
            self.theme.display_outline_size = self.outlineSpinBox.value()
            self.previewTheme()

    def onShadowSpinBoxChanged(self):
        if self.theme.display_shadow_size != self.shadowSpinBox.value():
            self.theme.display_shadow_size = self.shadowSpinBox.value()
            self.previewTheme()

    def onOutlineColorPushButtonClicked(self):
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.theme.display_outline_color), self)
        if new_color.isValid():
            self.theme.display_outline_color = new_color.name()
            self.outlineColorPushButton.setStyleSheet(u'background-color: %s' %
                unicode(self.theme.display_outline_color))
            self.previewTheme()

    def onShadowCheckBoxChanged(self, value):
        if value == 2:  # checked
            self.theme.display_shadow = True
        else:
            self.theme.display_shadow = False
        self.stateChanging(self.theme)
        self.previewTheme()

    def onSlideTransitionCheckBoxChanged(self, value):
        if value == 2:  # checked
            self.theme.display_slide_transition = True
        else:
            self.theme.display_slide_transition = False
        self.stateChanging(self.theme)
        self.previewTheme()

    def onShadowColorPushButtonClicked(self):
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.theme.display_shadow_color), self)
        if new_color.isValid():
            self.theme.display_shadow_color = new_color.name()
            self.shadowColorPushButton.setStyleSheet(u'background-color: %s' %
                unicode(self.theme.display_shadow_color))
            self.previewTheme()

    def onHorizontalComboBoxSelected(self, currentIndex):
        self.theme.display_horizontal_align = currentIndex
        self.stateChanging(self.theme)
        self.previewTheme()

    def onVerticalComboBoxSelected(self, currentIndex):
        self.theme.display_vertical_align = currentIndex
        self.stateChanging(self.theme)
        self.previewTheme()
    #
    # Local Methods
    #
    def paintUi(self, theme):
        self.stateChanging(theme)
        self.themeNameEdit.setText(self.theme.theme_name)
        # Background Tab
        self.imageLineEdit.setText(u'')
        if theme.background_type == u'solid':
            self.backgroundTypeComboBox.setCurrentIndex(0)
        elif theme.background_type == u'gradient':
            self.backgroundTypeComboBox.setCurrentIndex(1)
        else:
            self.backgroundTypeComboBox.setCurrentIndex(2)
            self.imageLineEdit.setText(self.theme.background_filename)
        if self.theme.background_direction == u'horizontal':
            self.gradientComboBox.setCurrentIndex(0)
        elif self.theme.background_direction == u'vertical':
            self.gradientComboBox.setCurrentIndex(1)
        else:
            self.gradientComboBox.setCurrentIndex(2)
        # Font Main Tab
        self.fontMainComboBox.setCurrentFont(
            QtGui.QFont(self.theme.font_main_name))
        self.fontMainSizeSpinBox.setValue(self.theme.font_main_proportion)
        if not self.theme.font_main_italics and \
            self.theme.font_main_weight == u'Normal':
            self.fontMainWeightComboBox.setCurrentIndex(0)
        elif not self.theme.font_main_italics and \
            self.theme.font_main_weight == u'Bold':
            self.fontMainWeightComboBox.setCurrentIndex(1)
        elif self.theme.font_main_italics and \
            self.theme.font_main_weight == u'Normal':
            self.fontMainWeightComboBox.setCurrentIndex(2)
        else:
            self.fontMainWeightComboBox.setCurrentIndex(3)
        self.fontMainXSpinBox.setValue(self.theme.font_main_x)
        self.fontMainYSpinBox.setValue(self.theme.font_main_y)
        self.fontMainWidthSpinBox.setValue(self.theme.font_main_width)
        self.fontMainHeightSpinBox.setValue(self.theme.font_main_height)
        # Font Footer Tab
        self.fontFooterComboBox.setCurrentFont(
            QtGui.QFont(self.theme.font_footer_name))
        self.fontFooterSizeSpinBox.setValue(
            self.theme.font_footer_proportion)
        if not self.theme.font_footer_italics and \
            self.theme.font_footer_weight == u'Normal':
            self.fontFooterWeightComboBox.setCurrentIndex(0)
        elif not self.theme.font_footer_italics and \
            self.theme.font_footer_weight == u'Bold':
            self.fontFooterWeightComboBox.setCurrentIndex(1)
        elif self.theme.font_footer_italics and \
            self.theme.font_footer_weight == u'Normal':
            self.fontFooterWeightComboBox.setCurrentIndex(2)
        else:
            self.fontFooterWeightComboBox.setCurrentIndex(3)
        self.fontFooterXSpinBox.setValue(self.theme.font_footer_x)
        self.fontFooterYSpinBox.setValue(self.theme.font_footer_y)
        self.fontFooterWidthSpinBox.setValue(self.theme.font_footer_width)
        self.fontFooterHeightSpinBox.setValue(self.theme.font_footer_height)
        self.fontMainColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(theme.font_main_color))
        self.fontFooterColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(theme.font_footer_color))
        if not self.theme.font_main_override:
            self.fontMainDefaultCheckBox.setChecked(True)
        else:
            self.fontMainDefaultCheckBox.setChecked(False)
        if not self.theme.font_footer_override:
            self.fontFooterDefaultCheckBox.setChecked(True)
        else:
            self.fontFooterDefaultCheckBox.setChecked(False)
        self.outlineColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(theme.display_outline_color))
        self.shadowColorPushButton.setStyleSheet(
            u'background-color: %s' % unicode(theme.display_shadow_color))
        if self.theme.display_outline:
            self.outlineCheckBox.setChecked(True)
            self.outlineColorPushButton.setEnabled(True)
        else:
            self.outlineCheckBox.setChecked(False)
            self.outlineColorPushButton.setEnabled(False)
        self.outlineSpinBox.setValue(int(self.theme.display_outline_size))
        if self.theme.display_shadow:
            self.shadowCheckBox.setChecked(True)
            self.shadowColorPushButton.setEnabled(True)
        else:
            self.shadowCheckBox.setChecked(False)
            self.shadowColorPushButton.setEnabled(False)
        self.shadowSpinBox.setValue(int(self.theme.display_shadow_size))
        if self.theme.display_slide_transition:
            self.slideTransitionCheckBox.setCheckState(QtCore.Qt.Checked)
        else:
            self.slideTransitionCheckBox.setCheckState(QtCore.Qt.Unchecked)
        self.horizontalComboBox.setCurrentIndex(
            self.theme.display_horizontal_align)
        self.verticalComboBox.setCurrentIndex(self.theme.display_vertical_align)

    def stateChanging(self, theme):
        self.backgroundTypeComboBox.setVisible(True)
        self.backgroundTypeLabel.setVisible(True)
        if theme.background_type == u'solid':
            self.color1PushButton.setStyleSheet(
                u'background-color: %s' % unicode(theme.background_color))
            self.color1Label.setText(
                translate('OpenLP.AmendThemeForm', 'Color:'))
            self.color1Label.setVisible(True)
            self.color1PushButton.setVisible(True)
            self.color2Label.setVisible(False)
            self.color2PushButton.setVisible(False)
            self.imageLabel.setVisible(False)
            self.imageLineEdit.setVisible(False)
            self.imageFilenameWidget.setVisible(False)
            self.gradientLabel.setVisible(False)
            self.gradientComboBox.setVisible(False)
        elif theme.background_type == u'gradient':
            self.color1PushButton.setStyleSheet(u'background-color: %s' \
                % unicode(theme.background_start_color))
            self.color2PushButton.setStyleSheet(u'background-color: %s' \
                % unicode(theme.background_end_color))
            self.color1Label.setText(
                translate('OpenLP.AmendThemeForm', 'First color:'))
            self.color2Label.setText(
                translate('OpenLP.AmendThemeForm', 'Second color:'))
            self.color1Label.setVisible(True)
            self.color1PushButton.setVisible(True)
            self.color2Label.setVisible(True)
            self.color2PushButton.setVisible(True)
            self.imageLabel.setVisible(False)
            self.imageLineEdit.setVisible(False)
            self.imageFilenameWidget.setVisible(False)
            self.gradientLabel.setVisible(True)
            self.gradientComboBox.setVisible(True)
        else: # must be image
            self.color1Label.setVisible(False)
            self.color1PushButton.setVisible(False)
            self.color2Label.setVisible(False)
            self.color2PushButton.setVisible(False)
            self.imageLabel.setVisible(True)
            self.imageLineEdit.setVisible(True)
            self.imageFilenameWidget.setVisible(True)
            self.gradientLabel.setVisible(False)
            self.gradientComboBox.setVisible(False)
        if not theme.font_main_override:
            self.fontMainXSpinBox.setEnabled(False)
            self.fontMainYSpinBox.setEnabled(False)
            self.fontMainWidthSpinBox.setEnabled(False)
            self.fontMainHeightSpinBox.setEnabled(False)
        else:
            self.fontMainXSpinBox.setEnabled(True)
            self.fontMainYSpinBox.setEnabled(True)
            self.fontMainWidthSpinBox.setEnabled(True)
            self.fontMainHeightSpinBox.setEnabled(True)

        if not theme.font_footer_override:
            self.fontFooterXSpinBox.setEnabled(False)
            self.fontFooterYSpinBox.setEnabled(False)
            self.fontFooterWidthSpinBox.setEnabled(False)
            self.fontFooterHeightSpinBox.setEnabled(False)
        else:
            self.fontFooterXSpinBox.setEnabled(True)
            self.fontFooterYSpinBox.setEnabled(True)
            self.fontFooterWidthSpinBox.setEnabled(True)
            self.fontFooterHeightSpinBox.setEnabled(True)

        if self.theme.display_outline:
            self.outlineColorPushButton.setEnabled(True)
        else:
            self.outlineColorPushButton.setEnabled(False)

        if self.theme.display_shadow:
            self.shadowColorPushButton.setEnabled(True)
        else:
            self.shadowColorPushButton.setEnabled(False)

    def previewTheme(self):
        if self.allowPreview:
            #calculate main number of rows
            metrics = self._getThemeMetrics()
            line_height = metrics.height() \
                + int(self.theme.font_main_line_adjustment)
            if self.theme.display_shadow:
                line_height += int(self.theme.display_shadow_size)
            if self.theme.display_outline:
                #  pixels top/bottom
                line_height += 2 * int(self.theme.display_outline_size)
            page_length = \
                ((self.fontMainHeightSpinBox.value()) / line_height )
            log.debug(u'Page Length area height %s, metrics %s, lines %s' %
                (self.fontMainHeightSpinBox.value(), metrics.height(),
                page_length))
            page_length_text = unicode(
                translate('OpenLP.AmendThemeForm', 'Slide height is %s rows.'))
            self.fontMainLinesPageLabel.setText(page_length_text % page_length)
            frame = self.thememanager.generateImage(self.theme)
            self.themePreview.setPixmap(QtGui.QPixmap.fromImage(frame))

    def _getThemeMetrics(self):
        main_weight = 50
        if self.theme.font_main_weight == u'Bold':
            main_weight = 75
        mainFont = QtGui.QFont(self.theme.font_main_name,
                     self.theme.font_main_proportion, # size
                     main_weight, # weight
                     self.theme.font_main_italics)# italic
        mainFont.setPixelSize(self.theme.font_main_proportion)
        metrics = QtGui.QFontMetrics(mainFont)
        # Validate that the screen width is big enough to display the text
        if self.theme.font_main_width < metrics.maxWidth() * 2 + 64:
            self.theme.font_main_width = metrics.maxWidth() * 2 + 64
            self.fontMainWidthSpinBox.setValue(self.theme.font_main_width)
        return metrics
