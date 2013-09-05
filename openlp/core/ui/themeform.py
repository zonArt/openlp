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
"""
The Theme wizard
"""
import logging
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import UiStrings, Registry, translate
from openlp.core.lib.theme import BackgroundType, BackgroundGradientType
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui import ThemeLayoutForm
from openlp.core.utils import get_images_filter, is_not_image_file
from .themewizard import Ui_ThemeWizard

log = logging.getLogger(__name__)


class ThemeForm(QtGui.QWizard, Ui_ThemeWizard):
    """
    This is the Theme Import Wizard, which allows easy creation and editing of
    OpenLP themes.
    """
    log.info('ThemeWizardForm loaded')

    def __init__(self, parent):
        """
        Instantiate the wizard, and run any extra setup we need to.

        ``parent``
            The QWidget-derived parent of the wizard.
        """
        super(ThemeForm, self).__init__(parent)
        self.setupUi(self)
        self.registerFields()
        self.updateThemeAllowed = True
        self.temp_background_filename = ''
        self.themeLayoutForm = ThemeLayoutForm(self)
        self.backgroundComboBox.currentIndexChanged.connect(self.onBackgroundComboBoxCurrentIndexChanged)
        self.gradientComboBox.currentIndexChanged.connect(self.onGradientComboBoxCurrentIndexChanged)
        self.colorButton.clicked.connect(self.onColorButtonClicked)
        self.imageColorButton.clicked.connect(self.onImageColorButtonClicked)
        self.gradientStartButton.clicked.connect(self.onGradientStartButtonClicked)
        self.gradientEndButton.clicked.connect(self.onGradientEndButtonClicked)
        self.imageBrowseButton.clicked.connect(self.onImageBrowseButtonClicked)
        self.imageFileEdit.editingFinished.connect(self.onImageFileEditEditingFinished)
        self.mainColorButton.clicked.connect(self.onMainColorButtonClicked)
        self.outlineColorButton.clicked.connect(self.onOutlineColorButtonClicked)
        self.shadowColorButton.clicked.connect(self.onShadowColorButtonClicked)
        self.outlineCheckBox.stateChanged.connect(self.onOutlineCheckCheckBoxStateChanged)
        self.shadowCheckBox.stateChanged.connect(self.onShadowCheckCheckBoxStateChanged)
        self.footerColorButton.clicked.connect(self.onFooterColorButtonClicked)
        self.customButtonClicked.connect(self.onCustom1ButtonClicked)
        self.mainPositionCheckBox.stateChanged.connect(self.onMainPositionCheckBoxStateChanged)
        self.footerPositionCheckBox.stateChanged.connect(self.onFooterPositionCheckBoxStateChanged)
        self.currentIdChanged.connect(self.onCurrentIdChanged)
        Registry().register_function('theme_line_count', self.updateLinesText)
        self.mainSizeSpinBox.valueChanged.connect(self.calculateLines)
        self.lineSpacingSpinBox.valueChanged.connect(self.calculateLines)
        self.outlineSizeSpinBox.valueChanged.connect(self.calculateLines)
        self.shadowSizeSpinBox.valueChanged.connect(self.calculateLines)
        self.mainFontComboBox.activated.connect(self.calculateLines)
        self.footerFontComboBox.activated.connect(self.updateTheme)
        self.footerSizeSpinBox.valueChanged.connect(self.updateTheme)

    def setDefaults(self):
        """
        Set up display at start of theme edit.
        """
        self.restart()
        self.setBackgroundPageValues()
        self.setMainAreaPageValues()
        self.setFooterAreaPageValues()
        self.setAlignmentPageValues()
        self.setPositionPageValues()
        self.setPreviewPageValues()

    def registerFields(self):
        """
        Map field names to screen names,
        """
        self.backgroundPage.registerField('background_type', self.backgroundComboBox)
        self.backgroundPage.registerField('color', self.colorButton)
        self.backgroundPage.registerField('grandient_start', self.gradientStartButton)
        self.backgroundPage.registerField('grandient_end', self.gradientEndButton)
        self.backgroundPage.registerField('background_image', self.imageFileEdit)
        self.backgroundPage.registerField('gradient', self.gradientComboBox)
        self.mainAreaPage.registerField('mainColorButton', self.mainColorButton)
        self.mainAreaPage.registerField('mainSizeSpinBox', self.mainSizeSpinBox)
        self.mainAreaPage.registerField('lineSpacingSpinBox', self.lineSpacingSpinBox)
        self.mainAreaPage.registerField('outlineCheckBox', self.outlineCheckBox)
        self.mainAreaPage.registerField('outlineColorButton', self.outlineColorButton)
        self.mainAreaPage.registerField('outlineSizeSpinBox', self.outlineSizeSpinBox)
        self.mainAreaPage.registerField('shadowCheckBox', self.shadowCheckBox)
        self.mainAreaPage.registerField('mainBoldCheckBox', self.mainBoldCheckBox)
        self.mainAreaPage.registerField('mainItalicsCheckBox', self.mainItalicsCheckBox)
        self.mainAreaPage.registerField('shadowColorButton', self.shadowColorButton)
        self.mainAreaPage.registerField('shadowSizeSpinBox', self.shadowSizeSpinBox)
        self.mainAreaPage.registerField('footerSizeSpinBox', self.footerSizeSpinBox)
        self.areaPositionPage.registerField('mainPositionX', self.mainXSpinBox)
        self.areaPositionPage.registerField('mainPositionY', self.mainYSpinBox)
        self.areaPositionPage.registerField('mainPositionWidth', self.mainWidthSpinBox)
        self.areaPositionPage.registerField('mainPositionHeight', self.mainHeightSpinBox)
        self.areaPositionPage.registerField('footerPositionX', self.footerXSpinBox)
        self.areaPositionPage.registerField('footerPositionY', self.footerYSpinBox)
        self.areaPositionPage.registerField('footerPositionWidth', self.footerWidthSpinBox)
        self.areaPositionPage.registerField('footerPositionHeight', self.footerHeightSpinBox)
        self.backgroundPage.registerField('horizontal', self.horizontalComboBox)
        self.backgroundPage.registerField('vertical', self.verticalComboBox)
        self.backgroundPage.registerField('slideTransition', self.transitionsCheckBox)
        self.backgroundPage.registerField('name', self.themeNameEdit)

    def calculateLines(self):
        """
        Calculate the number of lines on a page by rendering text
        """
        # Do not trigger on start up
        if self.currentPage != self.welcome_page:
            self.updateTheme()
            self.theme_manager.generate_image(self.theme, True)

    def updateLinesText(self, lines):
        """
        Updates the lines on a page on the wizard
        """
        self.mainLineCountLabel.setText(
            translate('OpenLP.ThemeForm', '(approximately %d lines per slide)') % int(lines))

    def resizeEvent(self, event=None):
        """
        Rescale the theme preview thumbnail on resize events.
        """
        if not event:
            event = QtGui.QResizeEvent(self.size(), self.size())
        QtGui.QWizard.resizeEvent(self, event)
        if self.currentPage() == self.previewPage:
            frameWidth = self.previewBoxLabel.lineWidth()
            pixmapWidth = self.previewArea.width() - 2 * frameWidth
            pixmapHeight = self.previewArea.height() - 2 * frameWidth
            aspectRatio = float(pixmapWidth) / pixmapHeight
            if aspectRatio < self.displayAspectRatio:
                pixmapHeight = int(pixmapWidth / self.displayAspectRatio + 0.5)
            else:
                pixmapWidth = int(pixmapHeight * self.displayAspectRatio + 0.5)
            self.previewBoxLabel.setFixedSize(pixmapWidth + 2 * frameWidth,
                pixmapHeight + 2 * frameWidth)

    def validateCurrentPage(self):
        """
        Validate the current page
        """
        background_image = BackgroundType.to_string(BackgroundType.Image)
        if self.page(self.currentId()) == self.backgroundPage and \
                self.theme.background_type == background_image and is_not_image_file(self.theme.background_filename):
            QtGui.QMessageBox.critical(self, translate('OpenLP.ThemeWizard', 'Background Image Empty'),
                translate('OpenLP.ThemeWizard', 'You have not selected a '
                    'background image. Please select one before continuing.'))
            return False
        else:
            return True

    def onCurrentIdChanged(self, pageId):
        """
        Detects Page changes and updates as appropriate.
        """
        enabled = self.page(pageId) == self.areaPositionPage
        self.setOption(QtGui.QWizard.HaveCustomButton1, enabled)
        if self.page(pageId) == self.previewPage:
            self.updateTheme()
            frame = self.theme_manager.generate_image(self.theme)
            self.previewBoxLabel.setPixmap(frame)
            self.displayAspectRatio = float(frame.width()) / frame.height()
            self.resizeEvent()

    def onCustom1ButtonClicked(self, number):
        """
        Generate layout preview and display the form.
        """
        self.updateTheme()
        width = self.renderer.width
        height = self.renderer.height
        pixmap = QtGui.QPixmap(width, height)
        pixmap.fill(QtCore.Qt.white)
        paint = QtGui.QPainter(pixmap)
        paint.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
        paint.drawRect(self.renderer.get_main_rectangle(self.theme))
        paint.setPen(QtGui.QPen(QtCore.Qt.red, 2))
        paint.drawRect(self.renderer.get_footer_rectangle(self.theme))
        paint.end()
        self.themeLayoutForm.exec_(pixmap)

    def onOutlineCheckCheckBoxStateChanged(self, state):
        """
        Change state as Outline check box changed
        """
        if self.updateThemeAllowed:
            self.theme.font_main_outline = state == QtCore.Qt.Checked
            self.outlineColorButton.setEnabled(self.theme.font_main_outline)
            self.outlineSizeSpinBox.setEnabled(self.theme.font_main_outline)
            self.calculateLines()

    def onShadowCheckCheckBoxStateChanged(self, state):
        """
        Change state as Shadow check box changed
        """
        if self.updateThemeAllowed:
            if state == QtCore.Qt.Checked:
                self.theme.font_main_shadow = True
            else:
                self.theme.font_main_shadow = False
            self.shadowColorButton.setEnabled(self.theme.font_main_shadow)
            self.shadowSizeSpinBox.setEnabled(self.theme.font_main_shadow)
            self.calculateLines()

    def onMainPositionCheckBoxStateChanged(self, value):
        """
        Change state as Main Area Position check box changed
        NOTE the font_main_override is the inverse of the check box value
        """
        if self.updateThemeAllowed:
            self.theme.font_main_override = not (value == QtCore.Qt.Checked)

    def onFooterPositionCheckBoxStateChanged(self, value):
        """
        Change state as Footer Area Position check box changed
        NOTE the font_footer_override is the inverse of the check box value
        """
        if self.updateThemeAllowed:
            self.theme.font_footer_override = not (value == QtCore.Qt.Checked)

    def exec_(self, edit=False):
        """
        Run the wizard.
        """
        log.debug('Editing theme %s' % self.theme.theme_name)
        self.temp_background_filename = ''
        self.updateThemeAllowed = False
        self.setDefaults()
        self.updateThemeAllowed = True
        self.themeNameLabel.setVisible(not edit)
        self.themeNameEdit.setVisible(not edit)
        self.edit_mode = edit
        if edit:
            self.setWindowTitle(translate('OpenLP.ThemeWizard', 'Edit Theme - %s') % self.theme.theme_name)
            self.next()
        else:
            self.setWindowTitle(UiStrings().NewTheme)
        return QtGui.QWizard.exec_(self)

    def initializePage(self, page_id):
        """
        Set up the pages for Initial run through dialog
        """
        log.debug('initializePage %s' % page_id)
        wizardPage = self.page(page_id)
        if wizardPage == self.backgroundPage:
            self.setBackgroundPageValues()
        elif wizardPage == self.mainAreaPage:
            self.setMainAreaPageValues()
        elif wizardPage == self.footerAreaPage:
            self.setFooterAreaPageValues()
        elif wizardPage == self.alignmentPage:
            self.setAlignmentPageValues()
        elif wizardPage == self.areaPositionPage:
            self.setPositionPageValues()

    def setBackgroundPageValues(self):
        """
        Handle the display and state of the Background page.
        """
        if self.theme.background_type == \
            BackgroundType.to_string(BackgroundType.Solid):
            self.colorButton.setStyleSheet('background-color: %s' % self.theme.background_color)
            self.setField('background_type', 0)
        elif self.theme.background_type == BackgroundType.to_string(BackgroundType.Gradient):
            self.gradientStartButton.setStyleSheet('background-color: %s' % self.theme.background_start_color)
            self.gradientEndButton.setStyleSheet('background-color: %s' % self.theme.background_end_color)
            self.setField('background_type', 1)
        elif self.theme.background_type == BackgroundType.to_string(BackgroundType.Image):
            self.imageColorButton.setStyleSheet('background-color: %s' % self.theme.background_border_color)
            self.imageFileEdit.setText(self.theme.background_filename)
            self.setField('background_type', 2)
        elif self.theme.background_type == BackgroundType.to_string(BackgroundType.Transparent):
            self.setField('background_type', 3)
        if self.theme.background_direction == BackgroundGradientType.to_string(BackgroundGradientType.Horizontal):
            self.setField('gradient', 0)
        elif self.theme.background_direction == BackgroundGradientType.to_string(BackgroundGradientType.Vertical):
            self.setField('gradient', 1)
        elif self.theme.background_direction == BackgroundGradientType.to_string(BackgroundGradientType.Circular):
            self.setField('gradient', 2)
        elif self.theme.background_direction == BackgroundGradientType.to_string(BackgroundGradientType.LeftTop):
            self.setField('gradient', 3)
        else:
            self.setField('gradient', 4)

    def setMainAreaPageValues(self):
        """
        Handle the display and state of the Main Area page.
        """
        self.mainFontComboBox.setCurrentFont(QtGui.QFont(self.theme.font_main_name))
        self.mainColorButton.setStyleSheet('background-color: %s' % self.theme.font_main_color)
        self.setField('mainSizeSpinBox', self.theme.font_main_size)
        self.setField('lineSpacingSpinBox', self.theme.font_main_line_adjustment)
        self.setField('outlineCheckBox', self.theme.font_main_outline)
        self.outlineColorButton.setStyleSheet('background-color: %s' % self.theme.font_main_outline_color)
        self.setField('outlineSizeSpinBox', self.theme.font_main_outline_size)
        self.setField('shadowCheckBox', self.theme.font_main_shadow)
        self.shadowColorButton.setStyleSheet('background-color: %s' % self.theme.font_main_shadow_color)
        self.setField('shadowSizeSpinBox', self.theme.font_main_shadow_size)
        self.setField('mainBoldCheckBox', self.theme.font_main_bold)
        self.setField('mainItalicsCheckBox', self.theme.font_main_italics)

    def setFooterAreaPageValues(self):
        """
        Handle the display and state of the Footer Area page.
        """
        self.footerFontComboBox.setCurrentFont(QtGui.QFont(self.theme.font_footer_name))
        self.footerColorButton.setStyleSheet('background-color: %s' % self.theme.font_footer_color)
        self.setField('footerSizeSpinBox', self.theme.font_footer_size)

    def setPositionPageValues(self):
        """
        Handle the display and state of the Position page.
        """
        # Main Area
        self.mainPositionCheckBox.setChecked(not self.theme.font_main_override)
        self.setField('mainPositionX', self.theme.font_main_x)
        self.setField('mainPositionY', self.theme.font_main_y)
        self.setField('mainPositionHeight', self.theme.font_main_height)
        self.setField('mainPositionWidth', self.theme.font_main_width)
        # Footer
        self.footerPositionCheckBox.setChecked(not self.theme.font_footer_override)
        self.setField('footerPositionX', self.theme.font_footer_x)
        self.setField('footerPositionY', self.theme.font_footer_y)
        self.setField('footerPositionHeight', self.theme.font_footer_height)
        self.setField('footerPositionWidth', self.theme.font_footer_width)

    def setAlignmentPageValues(self):
        """
        Handle the display and state of the Alignments page.
        """
        self.setField('horizontal', self.theme.display_horizontal_align)
        self.setField('vertical', self.theme.display_vertical_align)
        self.setField('slideTransition', self.theme.display_slide_transition)

    def setPreviewPageValues(self):
        """
        Handle the display and state of the Preview page.
        """
        self.setField('name', self.theme.theme_name)

    def onBackgroundComboBoxCurrentIndexChanged(self, index):
        """
        Background style Combo box has changed.
        """
        # do not allow updates when screen is building for the first time.
        if self.updateThemeAllowed:
            self.theme.background_type = BackgroundType.to_string(index)
            if self.theme.background_type != BackgroundType.to_string(BackgroundType.Image) and \
                    self.temp_background_filename == '':
                self.temp_background_filename = self.theme.background_filename
                self.theme.background_filename = ''
            if self.theme.background_type == BackgroundType.to_string(BackgroundType.Image) and \
                    self.temp_background_filename != '':
                self.theme.background_filename = self.temp_background_filename
                self.temp_background_filename = ''
            self.setBackgroundPageValues()

    def onGradientComboBoxCurrentIndexChanged(self, index):
        """
        Background gradient Combo box has changed.
        """
        if self.updateThemeAllowed:
            self.theme.background_direction = BackgroundGradientType.to_string(index)
            self.setBackgroundPageValues()

    def onColorButtonClicked(self):
        """
        Background / Gradient 1 Color button pushed.
        """
        self.theme.background_color = self._colorButton(self.theme.background_color)
        self.setBackgroundPageValues()

    def onImageColorButtonClicked(self):
        """
        Background / Gradient 1 Color button pushed.
        """
        self.theme.background_border_color = self._colorButton(self.theme.background_border_color)
        self.setBackgroundPageValues()

    def onGradientStartButtonClicked(self):
        """
        Gradient 2 Color button pushed.
        """
        self.theme.background_start_color = self._colorButton(self.theme.background_start_color)
        self.setBackgroundPageValues()

    def onGradientEndButtonClicked(self):
        """
        Gradient 2 Color button pushed.
        """
        self.theme.background_end_color = self._colorButton(self.theme.background_end_color)
        self.setBackgroundPageValues()

    def onImageBrowseButtonClicked(self):
        """
        Background Image button pushed.
        """
        images_filter = get_images_filter()
        images_filter = '%s;;%s (*.*) (*)' % (images_filter, UiStrings().AllFiles)
        filename = QtGui.QFileDialog.getOpenFileName(self,
            translate('OpenLP.ThemeWizard', 'Select Image'), '', images_filter)
        if filename:
            self.theme.background_filename = str(filename)
        self.setBackgroundPageValues()

    def onImageFileEditEditingFinished(self):
        """
        Background image path edited
        """
        self.theme.background_filename = str(self.imageFileEdit.text())

    def onMainColorButtonClicked(self):
        """
        Set the main colour value
        """
        self.theme.font_main_color = self._colorButton(self.theme.font_main_color)
        self.setMainAreaPageValues()

    def onOutlineColorButtonClicked(self):
        """
        Set the outline colour value
        """
        self.theme.font_main_outline_color = self._colorButton(self.theme.font_main_outline_color)
        self.setMainAreaPageValues()

    def onShadowColorButtonClicked(self):
        """
        Set the shadow colour value
        """
        self.theme.font_main_shadow_color = self._colorButton(self.theme.font_main_shadow_color)
        self.setMainAreaPageValues()

    def onFooterColorButtonClicked(self):
        """
        Set the footer colour value
        """
        self.theme.font_footer_color = self._colorButton(self.theme.font_footer_color)
        self.setFooterAreaPageValues()

    def updateTheme(self):
        """
        Update the theme object from the UI for fields not already updated
        when the are changed.
        """
        if not self.updateThemeAllowed:
            return
        log.debug('updateTheme')
        # main page
        self.theme.font_main_name = self.mainFontComboBox.currentFont().family()
        self.theme.font_main_size = self.field('mainSizeSpinBox')
        self.theme.font_main_line_adjustment = self.field('lineSpacingSpinBox')
        self.theme.font_main_outline_size = self.field('outlineSizeSpinBox')
        self.theme.font_main_shadow_size = self.field('shadowSizeSpinBox')
        self.theme.font_main_bold = self.field('mainBoldCheckBox')
        self.theme.font_main_italics = self.field('mainItalicsCheckBox')
        # footer page
        self.theme.font_footer_name = self.footerFontComboBox.currentFont().family()
        self.theme.font_footer_size = self.field('footerSizeSpinBox')
        # position page
        self.theme.font_main_x = self.field('mainPositionX')
        self.theme.font_main_y = self.field('mainPositionY')
        self.theme.font_main_height = self.field('mainPositionHeight')
        self.theme.font_main_width = self.field('mainPositionWidth')
        self.theme.font_footer_x = self.field('footerPositionX')
        self.theme.font_footer_y = self.field('footerPositionY')
        self.theme.font_footer_height = self.field('footerPositionHeight')
        self.theme.font_footer_width = self.field('footerPositionWidth')
        # position page
        self.theme.display_horizontal_align = self.horizontalComboBox.currentIndex()
        self.theme.display_vertical_align = self.verticalComboBox.currentIndex()
        self.theme.display_slide_transition = self.field('slideTransition')

    def accept(self):
        """
        Lets save the theme as Finish has been triggered
        """
        # Save the theme name
        self.theme.theme_name = self.field('name')
        if not self.theme.theme_name:
            critical_error_message_box(
                translate('OpenLP.ThemeWizard', 'Theme Name Missing'),
                translate('OpenLP.ThemeWizard', 'There is no name for this theme. Please enter one.'))
            return
        if self.theme.theme_name == '-1' or self.theme.theme_name == 'None':
            critical_error_message_box(
                translate('OpenLP.ThemeWizard', 'Theme Name Invalid'),
                translate('OpenLP.ThemeWizard', 'Invalid theme name. Please enter one.'))
            return
        saveFrom = None
        saveTo = None
        if self.theme.background_type == BackgroundType.to_string(BackgroundType.Image):
            filename = os.path.split(str(self.theme.background_filename))[1]
            saveTo = os.path.join(self.path, self.theme.theme_name, filename)
            saveFrom = self.theme.background_filename
        if not self.edit_mode and not self.theme_manager.check_if_theme_exists(self.theme.theme_name):
            return
        self.theme_manager.save_theme(self.theme, saveFrom, saveTo)
        return QtGui.QDialog.accept(self)

    def _colorButton(self, field):
        """
        Handle Color buttons
        """
        new_color = QtGui.QColorDialog.getColor(QtGui.QColor(field), self)
        if new_color.isValid():
            field = new_color.name()
        return field

    def _get_renderer(self):
        """
        Adds the Renderer to the class dynamically
        """
        if not hasattr(self, '_renderer'):
            self._renderer = Registry().get('renderer')
        return self._renderer

    renderer = property(_get_renderer)

    def _get_theme_manager(self):
        """
        Adds the theme manager to the class dynamically
        """
        if not hasattr(self, '_theme_manager'):
            self._theme_manager = Registry().get('theme_manager')
        return self._theme_manager

    theme_manager = property(_get_theme_manager)
