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

from openlp.core.lib import translate
from themewizard import Ui_ThemeWizard

log = logging.getLogger(__name__)

class BackgroundType(object):
    Solid = 0
    Gradient = 1
    Image = 3

    @staticmethod
    def to_string(type):
        if type == BackgroundType.Solid:
            return u'solid'
        elif type == BackgroundType.Gradient:
            return u'gradient'
        elif type == BackgroundType.Image:
            return u'image'

    @staticmethod
    def from_string(type_string):
        if type_string == u'solid':
            return BackgroundType.Solid
        elif type_string == u'gradient':
            return BackgroundType.Gradient
        elif type_string == u'image':
            return BackgroundType.Image

class BackgroundGradientType(object):
    Horizontal = 0
    Vertical = 1
    Circular = 3

    @staticmethod
    def to_string(type):
        if type == BackgroundType.Solid:
            return u'horizontal'
        elif type == BackgroundType.Gradient:
            return u'vertical'
        elif type == BackgroundType.Image:
            return u'circular'

    @staticmethod
    def from_string(type_string):
        if type_string == u'horizontal':
            return BackgroundType.Solid
        elif type_string == u'vertical':
            return BackgroundType.Gradient
        elif type_string == u'circular':
            return BackgroundType.Image

class ThemeWizardForm(QtGui.QWizard, Ui_ThemeWizard):
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

    def exec_(self):
        """
        Run the wizard.
        """
        self.setDefaults()
        return QtGui.QWizard.exec_(self)

    def validateCurrentPage(self):
        """
        Validate the current page before moving on to the next page.
        """
        print "CURRENT id", self.currentId()
        # Background Screen
        if self.currentId() == 0:
            print self.field(u'background_type').toString()
            self.setBackgroundTabValues()
        return True

    def setBackgroundTabValues(self):
        if self.theme.background_type == u'solid':
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
        elif self.theme.background_type == u'gradient':
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
        if self.theme.background_direction == u'horizontal':
           self.setField(u'gradient', QtCore.QVariant(0))
        elif self.theme.background_direction == u'vertical':
           self.setField(u'gradient', QtCore.QVariant(1))
        else:
           self.setField(u'gradient', QtCore.QVariant(2))

    def setDefaults(self):
        self.restart()
        self.setBackgroundTabValues()

    def registerFields(self):
        self.welcomePage.registerField(
            u'background_type', self.backgroundTypeComboBox)
        self.welcomePage.registerField(
            u'color_1', self.color1PushButton)
        self.welcomePage.registerField(
            u'color_2', self.color2PushButton)
        self.welcomePage.registerField(
            u'background_image', self.imageLineEdit)
        self.welcomePage.registerField(
            u'gradient', self.gradientComboBox)

    def onBackgroundComboBox(self, index):
        self.theme.background_type = self.backgrounds[index]
        self.setBackgroundTabValues()

    def onGradientComboBox(self, index):
        self.theme.background_direction = self.gradients[index]
        self.setBackgroundTabValues()

    def onColor1PushButtonClicked(self):
        if self.theme.background_type == u'solid':
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

    def _colorButton(self, field):
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(field), self)
        if new_color.isValid():
           field = new_color.name()
        return field
