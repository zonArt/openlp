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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, theme, BackgroundType, BackgroundGradientType

from themedialog import Ui_ThemeDialog

log = logging.getLogger(__name__)

class ThemeForm(QtGui.QWizard, Ui_ThemeDialog):
    """
    This is the Bible Import Wizard, which allows easy importing of Bibles
    into OpenLP from other formats like OSIS, CSV and OpenSong.
    """
    log.info(u'ThemeWizardForm loaded')

    def __init__(self, parent):
        """
        Instantiate the wizard, and run any extra setup we need to.

        ``parent``
            The QWidget-derived parent of the wizard.

        ``manager``
            The Bible manager.

        ``bibleplugin``
            The Bible plugin.
        """
        # Do not translate as internal
        QtGui.QWizard.__init__(self, parent)
        self.thememanager = parent
        self.setupUi(self)
        self.registerFields()
        self.finishButton = self.button(QtGui.QWizard.FinishButton)
        self.cancelButton = self.button(QtGui.QWizard.CancelButton)
        QtCore.QObject.connect(self.backgroundTypeComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onBackgroundComboBox)
        QtCore.QObject.connect(self.gradientComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onGradientComboBox)
        QtCore.QObject.connect(self.color1PushButton,
            QtCore.SIGNAL(u'pressed()'),
        self.onColor1PushButtonClicked)
        QtCore.QObject.connect(self.color2PushButton,
            QtCore.SIGNAL(u'pressed()'),
        self.onColor2PushButtonClicked)
        QtCore.QObject.connect(self.imageBrowseButton,
            QtCore.SIGNAL(u'pressed()'),
        self.onImageBrowseButtonClicked)
        QtCore.QObject.connect(self.mainColorPushButton,
            QtCore.SIGNAL(u'pressed()'),
        self.onMainColourPushButtonClicked)
        QtCore.QObject.connect(self.outlineColorPushButton,
            QtCore.SIGNAL(u'pressed()'),
        self.onOutlineColourPushButtonClicked)
        QtCore.QObject.connect(self.shadowColorPushButton,
            QtCore.SIGNAL(u'pressed()'),
        self.onShadowColourPushButtonClicked)
        QtCore.QObject.connect(self.outlineCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onOutlineCheckCheckBoxChanged)
        QtCore.QObject.connect(self.shadowCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onShadowCheckCheckBoxChanged)
        QtCore.QObject.connect(self.footerColorPushButton,
            QtCore.SIGNAL(u'pressed()'),
            self.onFooterColourPushButtonClicked)
        QtCore.QObject.connect(self.mainDefaultPositionCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onMainDefaultPositionCheckBox)
        QtCore.QObject.connect(self.footerDefaultPositionCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onFooterDefaultPositionCheckBox)

    def onOutlineCheckCheckBoxChanged(self, state):
        """
        Change state as Outline check box changed
        """
        self.outlineColorPushButton.setEnabled(state)
        self.outlineSizeSpinBox.setEnabled(state)

    def onShadowCheckCheckBoxChanged(self, state):
        """
        Change state as Shadow check box changed
        """
        self.shadowColorPushButton.setEnabled(state)
        self.shadowSizeSpinBox.setEnabled(state)

    def onMainDefaultPositionCheckBox(self, value):
        """
        Change state as Main Area Position check box changed
        """
        if value == QtCore.Qt.Checked:
            self.theme.font_main_override = False
        else:
            self.theme.font_main_override = True
        self.mainXSpinBox.setEnabled(self.theme.font_main_override)
        self.mainYSpinBox.setEnabled(self.theme.font_main_override)
        self.mainHeightSpinBox.setEnabled(self.theme.font_main_override)
        self.mainWidthSpinBox.setEnabled(self.theme.font_main_override)

    def onFooterDefaultPositionCheckBox(self, value):
        """
        Change state as Footer Area Position check box changed
        """
        if value == QtCore.Qt.Checked:
            self.theme.font_footer_override = False
        else:
            self.theme.font_footer_override = True
        self.footerXSpinBox.setEnabled(self.theme.font_footer_override)
        self.footerYSpinBox.setEnabled(self.theme.font_footer_override)
        self.footerHeightSpinBox.setEnabled(self.theme.font_footer_override)
        self.footerWidthSpinBox.setEnabled(self.theme.font_footer_override)

    def exec_(self):
        """
        Run the wizard.
        """
        self.setDefaults()
        return QtGui.QWizard.exec_(self)

    def validateCurrentPage(self):
        """
        Handle Tab specific code when moving between Tabs.
        """
        print "CURRENT id", self.currentId()
        # Preview Screen
        if self.currentId() == 5:
            self.updateTheme()
            frame = self.thememanager.generateImage(self.theme)
            self.previewBoxLabel.setPixmap(QtGui.QPixmap.fromImage(frame))
        return True

    def setBackgroundTabValues(self):
        """
        Handle the display and State of the background display tab.
        """
        if self.theme.background_type == \
            BackgroundType.to_string(BackgroundType.Solid):
            self.setField(u'background_type', QtCore.QVariant(0))
            self.color1PushButton.setVisible(True)
            self.color1Label.setVisible(True)
            self.color1PushButton.setStyleSheet(u'background-color: %s' %
                    self.theme.background_color)
            self.color1Label.setText(
                translate('OpenLP.AmendThemeForm', 'Color:'))
            self.color2PushButton.setVisible(False)
            self.color2Label.setVisible(False)
            self.gradientLabel.setVisible(False)
            self.gradientComboBox.setVisible(False)
            self.imageLabel.setVisible(False)
            self.imageLineEdit.setVisible(False)
            self.imageBrowseButton.setVisible(False)
            self.imageLineEdit.setText(u'')
        elif self.theme.background_type == \
            BackgroundType.to_string(BackgroundType.Gradient):
            self.setField(u'background_type', QtCore.QVariant(1))
            self.color1PushButton.setVisible(True)
            self.color1Label.setVisible(True)
            self.color1PushButton.setStyleSheet(u'background-color: %s' %
                    self.theme.background_start_color)
            self.color1Label.setText(
                translate('OpenLP.AmendThemeForm', 'First color:'))
            self.color2PushButton.setVisible(True)
            self.color2Label.setVisible(True)
            self.color2PushButton.setStyleSheet(u'background-color: %s' %
                    self.theme.background_end_color)
            self.color2Label.setText(
                translate('OpenLP.AmendThemeForm', 'Second color:'))
            self.gradientLabel.setVisible(True)
            self.gradientComboBox.setVisible(True)
            self.imageLabel.setVisible(False)
            self.imageLineEdit.setVisible(False)
            self.imageBrowseButton.setVisible(False)
            self.imageLineEdit.setText(u'')
        else:
            self.setField(u'background_type', QtCore.QVariant(2))
            self.color1PushButton.setVisible(False)
            self.color1Label.setVisible(False)
            self.color2PushButton.setVisible(False)
            self.color2Label.setVisible(False)
            self.gradientLabel.setVisible(False)
            self.gradientComboBox.setVisible(False)
            self.imageLineEdit.setVisible(True)
            self.imageLabel.setVisible(True)
            self.imageBrowseButton.setVisible(True)
            self.imageLineEdit.setText(self.theme.background_filename)
        if self.theme.background_direction == \
            BackgroundGradientType.to_string(BackgroundGradientType.Horizontal):
           self.setField(u'gradient', QtCore.QVariant(0))
        elif self.theme.background_direction == \
            BackgroundGradientType.to_string(BackgroundGradientType.Vertical):
           self.setField(u'gradient', QtCore.QVariant(1))
        elif self.theme.background_direction == \
            BackgroundGradientType.to_string(BackgroundGradientType.Circular):
           self.setField(u'gradient', QtCore.QVariant(2))
        elif self.theme.background_direction == \
            BackgroundGradientType.to_string(BackgroundGradientType.LeftTop):
           self.setField(u'gradient', QtCore.QVariant(3))
        else:
           self.setField(u'gradient', QtCore.QVariant(4))

    def setMainAreaTabValues(self):
        """
        Handle the display and State of the Main Area tab.
        """
        self.mainFontComboBox.setCurrentFont(
            QtGui.QFont(self.theme.font_main_name))
        self.mainColorPushButton.setStyleSheet(u'background-color: %s' %
            self.theme.font_main_color)
        self.setField(u'mainSizeSpinBox', \
            QtCore.QVariant(self.theme.font_main_size))
        self.setField(u'lineSpacingSpinBox', \
            QtCore.QVariant(self.theme.font_main_line_adjustment))
        self.setField(u'outlineCheckBox', \
            QtCore.QVariant(self.theme.font_main_outline))
        self.outlineColorPushButton.setStyleSheet(u'background-color: %s' %
            self.theme.font_main_outline_color)
        self.setField(u'outlineSizeSpinBox', \
            QtCore.QVariant(self.theme.font_main_outline_size))
        self.setField(u'shadowCheckBox', \
            QtCore.QVariant(self.theme.font_main_shadow))
        self.shadowColorPushButton.setStyleSheet(u'background-color: %s' %
            self.theme.font_main_shadow_color)
        self.setField(u'shadowSizeSpinBox', \
            QtCore.QVariant(self.theme.font_main_shadow_size))
        self.setField(u'boldCheckBox', \
            QtCore.QVariant(self.theme.font_main_bold))
        self.setField(u'italicsCheckBox', \
            QtCore.QVariant(self.theme.font_main_italics))

    def setFooterAreaTabValues(self):
        """
        Handle the display and State of the Footer Area tab.
        """
        self.footerFontComboBox.setCurrentFont(
            QtGui.QFont(self.theme.font_main_name))
        self.footerColorPushButton.setStyleSheet(u'background-color: %s' %
            self.theme.font_footer_color)
        self.setField(u'footerSizeSpinBox', \
            QtCore.QVariant(self.theme.font_footer_size))

    def setPositionTabValues(self):
        """
        Handle the display and State of the Position tab.
        """
        if self.theme.font_main_override:
            self.setField(u'mainDefaultPosition', QtCore.QVariant(False))
        else:
            self.setField(u'mainDefaultPosition', QtCore.QVariant(True))
        self.setField(u'mainPositionX', \
            QtCore.QVariant(self.theme.font_main_x))
        self.setField(u'mainPositionY', \
            QtCore.QVariant(self.theme.font_main_y))
        self.setField(u'mainPositionHeight', \
            QtCore.QVariant(self.theme.font_main_height))
        self.setField(u'mainPositionWidth', \
            QtCore.QVariant(self.theme.font_main_width))
        if self.theme.font_footer_override:
            self.setField(u'footerDefaultPosition', QtCore.QVariant(False))
        else:
            self.setField(u'footerDefaultPosition', QtCore.QVariant(True))
        self.setField(u'footerPositionX', \
            QtCore.QVariant(self.theme.font_footer_x))
        self.setField(u'footerPositionY', \
            QtCore.QVariant(self.theme.font_footer_y))
        self.setField(u'footerPositionHeight', \
            QtCore.QVariant(self.theme.font_footer_height))
        self.setField(u'footerPositionWidth', \
            QtCore.QVariant(self.theme.font_footer_width))

    def setAlignmentTabValues(self):
        self.setField(u'horizontal', \
            QtCore.QVariant(self.theme.display_horizontal_align))
        self.setField(u'vertical', \
            QtCore.QVariant(self.theme.display_vertical_align))
        if self.theme.display_slide_transition:
            self.setField(u'mainDefaultPosition', QtCore.QVariant(False))
        else:
            self.setField(u'mainDefaultPosition', QtCore.QVariant(True))

    def setPreviewTabValues(self):
        self.setField(u'name', QtCore.QVariant(self.theme.theme_name))
        if len(self.theme.theme_name) > 1:
            self.themeNameEdit.setEnabled(False)

    def setDefaults(self):
        """
        Set up display at start of theme edit.
        """
        self.restart()
        self.setBackgroundTabValues()
        self.setMainAreaTabValues()
        self.setFooterAreaTabValues()
        self.setAlignmentTabValues()
        self.setPositionTabValues()
        self.setPreviewTabValues()
        # Set up field states
        self.onOutlineCheckCheckBoxChanged(self.theme.font_main_outline)
        self.onShadowCheckCheckBoxChanged(self.theme.font_main_shadow)

    def registerFields(self):
        """
        Map field names to screen names,
        """
        self.backgroundPage.registerField(
            u'background_type', self.backgroundTypeComboBox)
        self.backgroundPage.registerField(
            u'color_1', self.color1PushButton)
        self.backgroundPage.registerField(
            u'color_2', self.color2PushButton)
        self.backgroundPage.registerField(
            u'background_image', self.imageLineEdit)
        self.backgroundPage.registerField(
            u'gradient', self.gradientComboBox)
        self.mainAreaPage.registerField(
            u'mainFontComboBox', self.mainFontComboBox)
        self.mainAreaPage.registerField(
            u'mainColorPushButton', self.mainColorPushButton)
        self.mainAreaPage.registerField(
            u'mainSizeSpinBox', self.mainSizeSpinBox)
        self.mainAreaPage.registerField(
            u'lineSpacingSpinBox', self.lineSpacingSpinBox)
        self.mainAreaPage.registerField(
            u'outlineCheckBox', self.outlineCheckBox)
        self.mainAreaPage.registerField(
            u'outlineColorPushButton', self.outlineColorPushButton)
        self.mainAreaPage.registerField(
            u'outlineSizeSpinBox', self.outlineSizeSpinBox)
        self.mainAreaPage.registerField(
            u'shadowCheckBox', self.shadowCheckBox)
        self.mainAreaPage.registerField(
            u'boldCheckBox', self.boldCheckBox)
        self.mainAreaPage.registerField(
            u'italicsCheckBox', self.italicsCheckBox)
        self.mainAreaPage.registerField(
            u'shadowColorPushButton', self.shadowColorPushButton)
        self.mainAreaPage.registerField(
            u'shadowSizeSpinBox', self.shadowSizeSpinBox)
        self.mainAreaPage.registerField(
            u'footerSizeSpinBox', self.footerSizeSpinBox)
        self.areaPositionPage.registerField(
            u'mainDefaultPosition', self.mainDefaultPositionCheckBox)
        self.areaPositionPage.registerField(
            u'mainPositionX', self.mainXSpinBox)
        self.areaPositionPage.registerField(
            u'mainPositionY', self.mainYSpinBox)
        self.areaPositionPage.registerField(
            u'mainPositionWidth', self.mainWidthSpinBox)
        self.areaPositionPage.registerField(
            u'mainPositionHeight', self.mainHeightSpinBox)
        self.areaPositionPage.registerField(
            u'footerDefaultPosition', self.footerDefaultPositionCheckBox)
        self.areaPositionPage.registerField(
            u'footerPositionX', self.footerXSpinBox)
        self.areaPositionPage.registerField(
            u'footerPositionY', self.footerYSpinBox)
        self.areaPositionPage.registerField(
            u'footerPositionWidth', self.footerWidthSpinBox)
        self.areaPositionPage.registerField(
            u'footerPositionHeight', self.footerHeightSpinBox)
        self.backgroundPage.registerField(
            u'horizontal', self.horizontalComboBox)
        self.backgroundPage.registerField(
            u'vertical', self.verticalComboBox)
        self.backgroundPage.registerField(
            u'slideTransition', self.transitionsCheckBox)
        self.backgroundPage.registerField(
            u'name', self.themeNameEdit)

    def onBackgroundComboBox(self, index):
        """
        Background style Combo box has changed.
        """
        self.theme.background_type = BackgroundType.to_string(index)
        self.setBackgroundTabValues()

    def onGradientComboBox(self, index):
        """
        Background gradient Combo box has changed.
        """
        self.theme.background_direction = \
            BackgroundGradientType.to_string(index)
        self.setBackgroundTabValues()

    def onColor1PushButtonClicked(self):
        if self.theme.background_type == \
            BackgroundType.to_string(BackgroundType.Solid):
            self.theme.background_color = \
                self._colorButton(self.theme.background_color)
        else:
            self.theme.background_start_color = \
                self._colorButton(self.theme.background_start_color)
        self.setBackgroundTabValues()

    def onColor2PushButtonClicked(self):
        self.theme.background_end_color = \
            self._colorButton(self.theme.background_end_color)
        self.setBackgroundTabValues()

    def onImageBrowseButtonClicked(self):
        images_filter = get_images_filter()
        images_filter = '%s;;%s (*.*) (*)' % (images_filter,
            translate('OpenLP.AmendThemeForm', 'All Files'))
        filename = QtGui.QFileDialog.getOpenFileName(self,
            translate('OpenLP.AmendThemeForm', 'Select Image'), u'',
            images_filter)
        if filename:
            self.theme.background_filename = filename
        self.setBackgroundTabValues()

    def onMainFontComboBox(self):
        self.theme.font_main_name = self.mainFontComboBox.currentFont().family()

    def onMainColourPushButtonClicked(self):
        self.theme.font_main_color = \
            self._colorButton(self.theme.font_main_color)
        self.setMainAreaTabValues()

    def onOutlineColourPushButtonClicked(self):
        self.theme.font_main_outline_color = \
            self._colorButton(self.theme.font_main_outline_color)
        self.setMainAreaTabValues()

    def onShadowColourPushButtonClicked(self):
        self.theme.font_main_shadow_color = \
            self._colorButton(self.theme.font_main_shadow_color)
        self.setMainAreaTabValues()

    def onFooterColourPushButtonClicked(self):
        self.theme.font_footer_color = \
            self._colorButton(self.theme.font_footer_color)
        self.setFooterAreaTabValues()

    def updateTheme(self):
        """
        Update the theme object from the UI for fields not already updated
        when the are changed.
        """
        # main page
        self.theme.font_main_name = \
            self.mainFontComboBox.currentFont().family()
        self.theme.font_footer_name = \
            self.footerFontComboBox.currentFont().family()
        self.theme.font_main_size = \
            self.field(u'mainSizeSpinBox').toInt()[0]
        self.theme.font_main_line_adjustment = \
            self.field(u'lineSpacingSpinBox').toInt()[0]
        self.theme.font_main_outline = \
            self.field(u'outlineSizeSpinBox').toInt()[0]
        self.theme.font_main_shadow_size = \
            self.field(u'shadowSizeSpinBox').toInt()[0]
        # footer page
        self.theme.font_footer_name = \
            self.footerFontComboBox.currentFont().family()
        self.theme.font_footer_size = \
            self.field(u'footerSizeSpinBox').toInt()[0]
        # position page
        self.theme.font_main_x = self.field(u'mainPositionX').toInt()[0]
        self.theme.font_main_y = self.field(u'mainPositionY').toInt()[0]
        self.theme.font_main_height = \
            self.field(u'mainPositionHeight').toInt()[0]
        self.theme.font_main_width = self.field(u'mainPositionWidth').toInt()[0]
        self.theme.font_footer_x = self.field(u'footerPositionX').toInt()[0]
        self.theme.font_footer_y = self.field(u'footerPositionY').toInt()[0]
        self.theme.font_footer_height = \
            self.field(u'footerPositionHeight').toInt()[0]
        self.theme.font_footer_width = \
            self.field(u'footerPositionWidth').toInt()[0]

    def _colorButton(self, field):
        """
        Handle Color buttons
        """
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(field), self)
        if new_color.isValid():
           field = new_color.name()
        return field
