# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

from openlp.core.lib import Receiver, SettingsTab, translate
from openlp.core.lib.ui import UiStrings

class PresentationTab(SettingsTab):
    """
    PresentationsTab is the Presentations settings tab in the settings dialog.
    """
    def __init__(self, parent, title, visible_title, controllers, icon_path):
        """
        Constructor
        """
        self.controllers = controllers
        SettingsTab.__init__(self, parent, title, visible_title, icon_path)
        self.activated = False

    def setupUi(self):
        """
        Create the controls for the settings tab
        """
        self.setObjectName(u'PresentationTab')
        SettingsTab.setupUi(self)
        self.ControllersGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.ControllersGroupBox.setObjectName(u'ControllersGroupBox')
        self.ControllersLayout = QtGui.QVBoxLayout(self.ControllersGroupBox)
        self.ControllersLayout.setObjectName(u'ControllersLayout')
        self.PresenterCheckboxes = {}
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = QtGui.QCheckBox(self.ControllersGroupBox)
            checkbox.setObjectName(controller.name + u'CheckBox')
            self.PresenterCheckboxes[controller.name] = checkbox
            self.ControllersLayout.addWidget(checkbox)
        self.leftLayout.addWidget(self.ControllersGroupBox)
        self.AdvancedGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.AdvancedGroupBox.setObjectName(u'AdvancedGroupBox')
        self.AdvancedLayout = QtGui.QVBoxLayout(self.AdvancedGroupBox)
        self.AdvancedLayout.setObjectName(u'AdvancedLayout')
        self.OverrideAppCheckBox = QtGui.QCheckBox(self.AdvancedGroupBox)
        self.OverrideAppCheckBox.setObjectName(u'OverrideAppCheckBox')
        self.AdvancedLayout.addWidget(self.OverrideAppCheckBox)
        self.leftLayout.addWidget(self.AdvancedGroupBox)
        self.leftLayout.addStretch()
        self.rightLayout.addStretch()

    def retranslateUi(self):
        """
        Make any translation changes
        """
        self.ControllersGroupBox.setTitle(
            translate('PresentationPlugin.PresentationTab',
            'Available Controllers'))
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = self.PresenterCheckboxes[controller.name]
            self.setControllerText(checkbox, controller)
        self.AdvancedGroupBox.setTitle(UiStrings().Advanced)
        self.OverrideAppCheckBox.setText(
            translate('PresentationPlugin.PresentationTab',
            'Allow presentation application to be overriden'))

    def setControllerText(self, checkbox, controller):
        if checkbox.isEnabled():
            checkbox.setText(controller.name)
        else:
            checkbox.setText(
                unicode(translate('PresentationPlugin.PresentationTab',
                '%s (unavailable)')) % controller.name)

    def load(self):
        """
        Load the settings.
        """
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = self.PresenterCheckboxes[controller.name]
            checkbox.setChecked(QtCore.QSettings().value(
                self.settingsSection + u'/' + controller.name,
                QtCore.QVariant(QtCore.Qt.Checked)).toInt()[0])
        self.OverrideAppCheckBox.setChecked(QtCore.QSettings().value(
            self.settingsSection + u'/override app',
            QtCore.QVariant(QtCore.Qt.Unchecked)).toInt()[0])

    def save(self):
        """
        Save the settings. If the tab hasn't been made visible to the user
        then there is nothing to do, so exit. This removes the need to
        start presentation applications unnecessarily.
        """
        if not self.activated:
            return
        changed = False
        for key in self.controllers:
            controller = self.controllers[key]
            if controller.is_available():
                checkbox = self.PresenterCheckboxes[controller.name]
                setting_key = self.settingsSection + u'/' + controller.name
                if QtCore.QSettings().value(setting_key) != \
                    checkbox.checkState():
                    changed = True
                    QtCore.QSettings().setValue(setting_key,
                        QtCore.QVariant(checkbox.checkState()))
                    if checkbox.isChecked():
                        controller.start_process()
                    else:
                        controller.kill()
        setting_key = self.settingsSection + u'/override app'
        if QtCore.QSettings().value(setting_key) != \
            self.OverrideAppCheckBox.checkState():
            QtCore.QSettings().setValue(setting_key,
                QtCore.QVariant(self.OverrideAppCheckBox.checkState()))
            changed = True
        if changed:
            Receiver.send_message(u'mediaitem_presentation_rebuild')

    def tabVisible(self):
        """
        Tab has just been made visible to the user
        """
        self.activated = True
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = self.PresenterCheckboxes[controller.name]
            checkbox.setEnabled(controller.is_available())
            self.setControllerText(checkbox, controller)
