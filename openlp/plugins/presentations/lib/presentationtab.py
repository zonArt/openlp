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

from openlp.core.lib import SettingsTab, translate

class PresentationTab(SettingsTab):
    """
    PresentationsTab is the Presentations settings tab in the settings dialog.
    """
    def __init__(self, title, controllers):
        """
        Constructor
        """
        self.controllers = controllers
        SettingsTab.__init__(self, title)

    def setupUi(self):
        """
        Create the controls for the settings tab
        """
        self.setObjectName(u'PresentationTab')
        self.tabTitleVisible = translate('PresentationPlugin.PresentationTab',
            'Presentations')
        self.PresentationLayout = QtGui.QHBoxLayout(self)
        self.PresentationLayout.setSpacing(8)
        self.PresentationLayout.setMargin(8)
        self.PresentationLayout.setObjectName(u'PresentationLayout')
        self.PresentationLeftWidget = QtGui.QWidget(self)
        self.PresentationLeftWidget.setObjectName(u'PresentationLeftWidget')
        self.PresentationLeftLayout = QtGui.QVBoxLayout(
            self.PresentationLeftWidget)
        self.PresentationLeftLayout.setObjectName(u'PresentationLeftLayout')
        self.PresentationLeftLayout.setSpacing(8)
        self.PresentationLeftLayout.setMargin(0)
        self.VerseDisplayGroupBox = QtGui.QGroupBox(self)
        self.VerseDisplayGroupBox.setObjectName(u'VerseDisplayGroupBox')
        self.VerseDisplayLayout = QtGui.QVBoxLayout(self.VerseDisplayGroupBox)
        self.VerseDisplayLayout.setMargin(8)
        self.VerseDisplayLayout.setObjectName(u'VerseDisplayLayout')
        self.PresenterCheckboxes = {}
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = QtGui.QCheckBox(self.VerseDisplayGroupBox)
            checkbox.setTristate(False)
            checkbox.setEnabled(controller.available)
            checkbox.setObjectName(controller.name + u'CheckBox')
            self.PresenterCheckboxes[controller.name] = checkbox
            self.VerseDisplayLayout.addWidget(checkbox)
        self.PresentationThemeWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.PresentationThemeWidget.setObjectName(u'PresentationThemeWidget')
        self.PresentationThemeLayout = QtGui.QHBoxLayout(
            self.PresentationThemeWidget)
        self.PresentationThemeLayout.setSpacing(8)
        self.PresentationThemeLayout.setMargin(0)
        self.PresentationThemeLayout.setObjectName(u'PresentationThemeLayout')
        self.PresentationLeftLayout.addWidget(self.VerseDisplayGroupBox)
        self.PresentationLeftSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.PresentationLeftLayout.addItem(self.PresentationLeftSpacer)
        self.PresentationLayout.addWidget(self.PresentationLeftWidget)
        self.PresentationRightWidget = QtGui.QWidget(self)
        self.PresentationRightWidget.setObjectName(u'PresentationRightWidget')
        self.PresentationRightLayout = QtGui.QVBoxLayout(
            self.PresentationRightWidget)
        self.PresentationRightLayout.setObjectName(u'PresentationRightLayout')
        self.PresentationRightLayout.setSpacing(8)
        self.PresentationRightLayout.setMargin(0)
        self.PresentationRightSpacer = QtGui.QSpacerItem(50, 20,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.PresentationRightLayout.addItem(self.PresentationRightSpacer)
        self.PresentationLayout.addWidget(self.PresentationRightWidget)

    def retranslateUi(self):
        """
        Make any translation changes
        """
        self.VerseDisplayGroupBox.setTitle(
            translate('PresentationPlugin.PresentationTab',
            'Available Controllers'))
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = self.PresenterCheckboxes[controller.name]
            checkbox.setText(controller.name)

    def load(self):
        """
        Load the settings.
        """
        for key in self.controllers:
            controller = self.controllers[key]
            if controller.available:
                checkbox = self.PresenterCheckboxes[controller.name]
                checkbox.setChecked(QtCore.QSettings().value(
                    self.settingsSection + u'/' + controller.name,
                    QtCore.QVariant(0)).toInt()[0])

    def save(self):
        """
        Save the settings.
        """
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = self.PresenterCheckboxes[controller.name]
            QtCore.QSettings().setValue(
                self.settingsSection + u'/' + controller.name,
                QtCore.QVariant(checkbox.checkState()))
