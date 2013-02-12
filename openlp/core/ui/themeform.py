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

from openlp.core.lib import Receiver, UiStrings, Registry, translate
from openlp.core.lib.theme import BackgroundType, BackgroundGradientType
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui import ThemeLayoutForm
from openlp.core.utils import get_images_filter
from themewizard import Ui_ThemeWizard

log = logging.getLogger(__name__)


class ThemeForm(QtGui.QWizard, Ui_ThemeWizard):
    """
    This is the Theme Import Wizard, which allows easy creation and editing of
    OpenLP themes.
    """
    log.info(u'ThemeWizardForm loaded')

    def __init__(self, parent):
        """
        Instantiate the wizard, and run any extra setup we need to.

        ``parent``
            The QWidget-derived parent of the wizard.
        """
        QtGui.QWizard.__init__(self, parent)
        self.setupUi(self)
        self.registerFields()
        self.updateThemeAllowed = True
        self.temp_background_filename = u''
        self.themeLayoutForm = ThemeLayoutForm(self)
        QtCore.QObject.connect(self.backgroundComboBox, QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onBackgroundComboBoxCurrentIndexChanged)
        QtCore.QObject.connect(self.gradientComboBox, QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onGradientComboBoxCurrentIndexChanged)
        QtCore.QObject.connect(self.colorButton, QtCore.SIGNAL(u'clicked()'), self.onColorButtonClicked)
        QtCore.QObject.connect(self.imageColorButton, QtCore.SIGNAL(u'clicked()'), self.onImageColorButtonClicked)
        QtCore.QObject.connect(self.gradientStartButton, QtCore.SIGNAL(u'clicked()'),
            self.onGradientStartButtonClicked)
        QtCore.QObject.connect(self.gradientEndButton, QtCore.SIGNAL(u'clicked()'), self.onGradientEndButtonClicked)
        QtCore.QObject.connect(self.imageBrowseButton, QtCore.SIGNAL(u'clicked()'), self.onImageBrowseButtonClicked)
        QtCore.QObject.connect(self.mainColorButton, QtCore.SIGNAL(u'clicked()'), self.onMainColorButtonClicked)
        QtCore.QObject.connect(self.outlineColorButton, QtCore.SIGNAL(u'clicked()'), self.onOutlineColorButtonClicked)
        QtCore.QObject.connect(self.shadowColorButton, QtCore.SIGNAL(u'clicked()'), self.onShadowColorButtonClicked)
        QtCore.QObject.connect(self.outlineCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onOutlineCheckCheckBoxStateChanged)
        QtCore.QObject.connect(self.shadowCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onShadowCheckCheckBoxStateChanged)
        QtCore.QObject.connect(self.footerColorButton, QtCore.SIGNAL(u'clicked()'), self.onFooterColorButtonClicked)
        QtCore.QObject.connect(self, QtCore.SIGNAL(u'customButtonClicked(int)'), self.onCustom1ButtonClicked)
        QtCore.QObject.connect(self.mainPositionCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onMainPositionCheckBoxStateChanged)
        QtCore.QObject.connect(self.footerPositionCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onFooterPositionCheckBoxStateChanged)
        QtCore.QObject.connect(self, QtCore.SIGNAL(u'currentIdChanged(int)'), self.onCurrentIdChanged)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'theme_line_count'), self.updateLinesText)
        QtCore.QObject.connect(self.mainSizeSpinBox, QtCore.SIGNAL(u'valueChanged(int)'), self.calculateLines)
        QtCore.QObject.connect(self.lineSpacingSpinBox, QtCore.SIGNAL(u'valueChanged(int)'), self.calculateLines)
        QtCore.QObject.connect(self.outlineSizeSpinBox, QtCore.SIGNAL(u'valueChanged(int)'), self.calculateLines)
        QtCore.QObject.connect(self.shadowSizeSpinBox, QtCore.SIGNAL(u'valueChanged(int)'), self.calculateLines)
        QtCore.QObject.connect(self.mainFontComboBox, QtCore.SIGNAL(u'activated(int)'), self.calculateLines)
        QtCore.QObject.connect(self.footerFontComboBox, QtCore.SIGNAL(u'activated(int)'), self.updateTheme)
        QtCore.QObject.connect(self.footerSizeSpinBox, QtCore.SIGNAL(u'valueChanged(int)'), self.updateTheme)

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
        self.backgroundPage.registerField(u'background_type', self.backgroundComboBox)
        self.backgroundPage.registerField(u'color', self.colorButton)
        self.backgroundPage.registerField(u'grandient_start', self.gradientStartButton)
        self.backgroundPage.registerField(u'grandient_end', self.gradientEndButton)
        self.backgroundPage.registerField(u'background_image', self.imageFileEdit)
        self.backgroundPage.registerField(u'gradient', self.gradientComboBox)
        self.mainAreaPage.registerField(u'mainColorButton', self.mainColorButton)
        self.mainAreaPage.registerField(u'mainSizeSpinBox', self.mainSizeSpinBox)
        self.mainAreaPage.registerField(u'lineSpacingSpinBox', self.lineSpacingSpinBox)
        self.mainAreaPage.registerField(u'outlineCheckBox', self.outlineCheckBox)
        self.mainAreaPage.registerField(u'outlineColorButton', self.outlineColorButton)
        self.mainAreaPage.registerField(u'outlineSizeSpinBox', self.outlineSizeSpinBox)
        self.mainAreaPage.registerField(u'shadowCheckBox', self.shadowCheckBox)
        self.mainAreaPage.registerField(u'mainBoldCheckBox', self.mainBoldCheckBox)
        self.mainAreaPage.registerField(u'mainItalicsCheckBox', self.mainItalicsCheckBox)
        self.mainAreaPage.registerField(u'shadowColorButton', self.shadowColorButton)
        self.mainAreaPage.registerField(u'shadowSizeSpinBox', self.shadowSizeSpinBox)
        self.mainAreaPage.registerField(u'footerSizeSpinBox', self.footerSizeSpinBox)
        self.areaPositionPage.registerField(u'mainPositionX', self.mainXSpinBox)
        self.areaPositionPage.registerField(u'mainPositionY', self.mainYSpinBox)
        self.areaPositionPage.registerField(u'mainPositionWidth', self.mainWidthSpinBox)
        self.areaPositionPage.registerField(u'mainPositionHeight', self.mainHeightSpinBox)
        self.areaPositionPage.registerField(u'footerPositionX', self.footerXSpinBox)
        self.areaPositionPage.registerField(u'footerPositionY', self.footerYSpinBox)
        self.areaPositionPage.registerField(u'footerPositionWidth', self.footerWidthSpinBox)
        self.areaPositionPage.registerField(u'footerPositionHeight', self.footerHeightSpinBox)
        self.backgroundPage.registerField(u'horizontal', self.horizontalComboBox)
        self.backgroundPage.registerField(u'vertical', self.verticalComboBox)
        self.backgroundPage.registerField(u'slideTransition', self.transitionsCheckBox)
        self.backgroundPage.registerField(u'name', self.themeNameEdit)

    def calculateLines(self):
        """
        Calculate the number of lines on a page by rendering text
        """
        # Do not trigger on start up
        if self.currentPage != self.welcomePage:
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
                self.theme.background_type == background_image and not self.imageFileEdit.text():
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
        log.debug(u'Editing theme %s' % self.theme.theme_name)
        self.temp_background_filename = u''
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

    def initializePage(self, id):
        """
        Set up the pages for Initial run through dialog
        """
        log.debug(u'initializePage %s' % id)
        wizardPage = self.page(id)
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
            self.colorButton.setStyleSheet(u'background-color: %s' % self.theme.background_color)
            self.setField(u'background_type', 0)
        elif self.theme.background_type == BackgroundType.to_string(BackgroundType.Gradient):
            self.gradientStartButton.setStyleSheet(u'background-color: %s' % self.theme.background_start_color)
            self.gradientEndButton.setStyleSheet(u'background-color: %s' % self.theme.background_end_color)
            self.setField(u'background_type', 1)
        elif self.theme.background_type == BackgroundType.to_string(BackgroundType.Image):
            self.imageColorButton.setStyleSheet(u'background-color: %s' % self.theme.background_border_color)
            self.imageFileEdit.setText(self.theme.background_filename)
            self.setField(u'background_type', 2)
        elif self.theme.background_type == BackgroundType.to_string(BackgroundType.Transparent):
            self.setField(u'background_type', 3)
        if self.theme.background_direction == BackgroundGradientType.to_string(BackgroundGradientType.Horizontal):
            self.setField(u'gradient', 0)
        elif self.theme.background_direction == BackgroundGradientType.to_string(BackgroundGradientType.Vertical):
            self.setField(u'gradient', 1)
        elif self.theme.background_direction == BackgroundGradientType.to_string(BackgroundGradientType.Circular):
            self.setField(u'gradient', 2)
        elif self.theme.background_direction == BackgroundGradientType.to_string(BackgroundGradientType.LeftTop):
            self.setField(u'gradient', 3)
        else:
            self.setField(u'gradient', 4)

    def setMainAreaPageValues(self):
        """
        Handle the display and state of the Main Area page.
        """
        self.mainFontComboBox.setCurrentFont(QtGui.QFont(self.theme.font_main_name))
        self.mainColorButton.setStyleSheet(u'background-color: %s' % self.theme.font_main_color)
        self.setField(u'mainSizeSpinBox', self.theme.font_main_size)
        self.setField(u'lineSpacingSpinBox', self.theme.font_main_line_adjustment)
        self.setField(u'outlineCheckBox', self.theme.font_main_outline)
        self.outlineColorButton.setStyleSheet(u'background-color: %s' % self.theme.font_main_outline_color)
        self.setField(u'outlineSizeSpinBox', self.theme.font_main_outline_size)
        self.setField(u'shadowCheckBox', self.theme.font_main_shadow)
        self.shadowColorButton.setStyleSheet(u'background-color: %s' % self.theme.font_main_shadow_color)
        self.setField(u'shadowSizeSpinBox', self.theme.font_main_shadow_size)
        self.setField(u'mainBoldCheckBox', self.theme.font_main_bold)
        self.setField(u'mainItalicsCheckBox', self.theme.font_main_italics)

    def setFooterAreaPageValues(self):
        """
        Handle the display and state of the Footer Area page.
        """
        self.footerFontComboBox.setCurrentFont(QtGui.QFont(self.theme.font_footer_name))
        self.footerColorButton.setStyleSheet(u'background-color: %s' % self.theme.font_footer_color)
        self.setField(u'footerSizeSpinBox', self.theme.font_footer_size)

    def setPositionPageValues(self):
        """
        Handle the display and state of the Position page.
        """
        # Main Area
        self.mainPositionCheckBox.setChecked(not self.theme.font_main_override)
        self.setField(u'mainPositionX', self.theme.font_main_x)
        self.setField(u'mainPositionY', self.theme.font_main_y)
        self.setField(u'mainPositionHeight', self.theme.font_main_height)
        self.setField(u'mainPositionWidth', self.theme.font_main_width)
        # Footer
        self.footerPositionCheckBox.setChecked(not self.theme.font_footer_override)
        self.setField(u'footerPositionX', self.theme.font_footer_x)
        self.setField(u'footerPositionY', self.theme.font_footer_y)
        self.setField(u'footerPositionHeight', self.theme.font_footer_height)
        self.setField(u'footerPositionWidth', self.theme.font_footer_width)

    def setAlignmentPageValues(self):
        """
        Handle the display and state of the Alignments page.
        """
        self.setField(u'horizontal', self.theme.display_horizontal_align)
        self.setField(u'vertical', self.theme.display_vertical_align)
        self.setField(u'slideTransition', self.theme.display_slide_transition)

    def setPreviewPageValues(self):
        """
        Handle the display and state of the Preview page.
        """
        self.setField(u'name', self.theme.theme_name)

    def onBackgroundComboBoxCurrentIndexChanged(self, index):
        """
        Background style Combo box has changed.
        """
        # do not allow updates when screen is building for the first time.
        if self.updateThemeAllowed:
            self.theme.background_type = BackgroundType.to_string(index)
            if self.theme.background_type != BackgroundType.to_string(BackgroundType.Image) and \
                    self.temp_background_filename == u'':
                self.temp_background_filename = self.theme.background_filename
                self.theme.background_filename = u''
            if self.theme.background_type == BackgroundType.to_string(BackgroundType.Image) and \
                    self.temp_background_filename != u'':
                self.theme.background_filename = self.temp_background_filename
                self.temp_background_filename = u''
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
        images_filter = u'%s;;%s (*.*) (*)' % (images_filter, UiStrings().AllFiles)
        filename = QtGui.QFileDialog.getOpenFileName(self,
            translate('OpenLP.ThemeWizard', 'Select Image'), u'', images_filter)
        if filename:
            self.theme.background_filename = unicode(filename)
        self.setBackgroundPageValues()

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
        log.debug(u'updateTheme')
        # main page
        self.theme.font_main_name = self.mainFontComboBox.currentFont().family()
        self.theme.font_main_size = self.field(u'mainSizeSpinBox')
        self.theme.font_main_line_adjustment = self.field(u'lineSpacingSpinBox')
        self.theme.font_main_outline_size = self.field(u'outlineSizeSpinBox')
        self.theme.font_main_shadow_size = self.field(u'shadowSizeSpinBox')
        self.theme.font_main_bold = self.field(u'mainBoldCheckBox')
        self.theme.font_main_italics = self.field(u'mainItalicsCheckBox')
        # footer page
        self.theme.font_footer_name = self.footerFontComboBox.currentFont().family()
        self.theme.font_footer_size = self.field(u'footerSizeSpinBox')
        # position page
        self.theme.font_main_x = self.field(u'mainPositionX')
        self.theme.font_main_y = self.field(u'mainPositionY')
        self.theme.font_main_height = self.field(u'mainPositionHeight')
        self.theme.font_main_width = self.field(u'mainPositionWidth')
        self.theme.font_footer_x = self.field(u'footerPositionX')
        self.theme.font_footer_y = self.field(u'footerPositionY')
        self.theme.font_footer_height = self.field(u'footerPositionHeight')
        self.theme.font_footer_width = self.field(u'footerPositionWidth')
        # position page
        self.theme.display_horizontal_align = self.horizontalComboBox.currentIndex()
        self.theme.display_vertical_align = self.verticalComboBox.currentIndex()
        self.theme.display_slide_transition = self.field(u'slideTransition')

    def accept(self):
        """
        Lets save the theme as Finish has been triggered
        """
        # Save the theme name
        self.theme.theme_name = self.field(u'name')
        if not self.theme.theme_name:
            critical_error_message_box(
                translate('OpenLP.ThemeWizard', 'Theme Name Missing'),
                translate('OpenLP.ThemeWizard', 'There is no name for this theme. Please enter one.'))
            return
        if self.theme.theme_name == u'-1' or self.theme.theme_name == u'None':
            critical_error_message_box(
                translate('OpenLP.ThemeWizard', 'Theme Name Invalid'),
                translate('OpenLP.ThemeWizard', 'Invalid theme name. Please enter one.'))
            return
        saveFrom = None
        saveTo = None
        if self.theme.background_type == BackgroundType.to_string(BackgroundType.Image):
            filename = os.path.split(unicode(self.theme.background_filename))[1]
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
        if not hasattr(self, u'_renderer'):
            self._renderer = Registry().get(u'renderer')
        return self._renderer

    renderer = property(_get_renderer)

    def _get_theme_manager(self):
        """
        Adds the theme manager to the class dynamically
        """
        if not hasattr(self, u'_theme_manager'):
            self._theme_manager = Registry().get(u'theme_manager')
        return self._theme_manager

    theme_manager = property(_get_theme_manager)
