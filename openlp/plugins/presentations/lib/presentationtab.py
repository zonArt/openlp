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

from PyQt4 import QtGui

from openlp.core.lib import Settings, SettingsTab, UiStrings, translate


class PresentationTab(SettingsTab):
    """
    PresentationsTab is the Presentations settings tab in the settings dialog.
    """
    def __init__(self, parent, title, visible_title, controllers, icon_path):
        """
        Constructor
        """
        self.parent = parent
        self.controllers = controllers
        super(PresentationTab, self).__init__(parent, title, visible_title, icon_path)
        self.activated = False

    def setupUi(self):
        """
        Create the controls for the settings tab
        """
        self.setObjectName('PresentationTab')
        super(PresentationTab, self).setupUi()
        self.controllers_group_box = QtGui.QGroupBox(self.left_column)
        self.controllers_group_box.setObjectName('controllers_group_box')
        self.controllers_layout = QtGui.QVBoxLayout(self.controllers_group_box)
        self.controllers_layout.setObjectName('ccontrollers_layout')
        self.presenter_check_boxes = {}
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = QtGui.QCheckBox(self.controllers_group_box)
            checkbox.setObjectName(controller.name + 'CheckBox')
            self.presenter_check_boxes[controller.name] = checkbox
            self.controllers_layout.addWidget(checkbox)
        self.left_layout.addWidget(self.controllers_group_box)
        self.advanced_group_box = QtGui.QGroupBox(self.left_column)
        self.advanced_group_box.setObjectName('advanced_group_box')
        self.advanced_layout = QtGui.QVBoxLayout(self.advanced_group_box)
        self.advanced_layout.setObjectName('advanced_layout')
        self.override_app_check_box = QtGui.QCheckBox(self.advanced_group_box)
        self.override_app_check_box.setObjectName('override_app_check_box')
        self.advanced_layout.addWidget(self.override_app_check_box)
        self.left_layout.addWidget(self.advanced_group_box)
        self.left_layout.addStretch()
        self.right_layout.addStretch()

    def retranslateUi(self):
        """
        Make any translation changes
        """
        self.controllers_group_box.setTitle(translate('PresentationPlugin.PresentationTab', 'Available Controllers'))
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = self.presenter_check_boxes[controller.name]
            self.set_controller_text(checkbox, controller)
        self.advanced_group_box.setTitle(UiStrings().Advanced)
        self.override_app_check_box.setText(
            translate('PresentationPlugin.PresentationTab', 'Allow presentation application to be overridden'))

    def set_controller_text(self, checkbox, controller):
        if checkbox.isEnabled():
            checkbox.setText(controller.name)
        else:
            checkbox.setText(translate('PresentationPlugin.PresentationTab', '%s (unavailable)') % controller.name)

    def load(self):
        """
        Load the settings.
        """
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = self.presenter_check_boxes[controller.name]
            checkbox.setChecked(Settings().value(self.settings_section + '/' + controller.name))
        self.override_app_check_box.setChecked(Settings().value(self.settings_section + '/override app'))

    def save(self):
        """
        Save the settings. If the tab hasn't been made visible to the user then there is nothing to do, so exit. This
        removes the need to start presentation applications unnecessarily.
        """
        if not self.activated:
            return
        changed = False
        for key in self.controllers:
            controller = self.controllers[key]
            if controller.is_available():
                checkbox = self.presenter_check_boxes[controller.name]
                setting_key = self.settings_section + '/' + controller.name
                if Settings().value(setting_key) != checkbox.checkState():
                    changed = True
                    Settings().setValue(setting_key, checkbox.checkState())
                    if checkbox.isChecked():
                        controller.start_process()
                    else:
                        controller.kill()
        setting_key = self.settings_section + '/override app'
        if Settings().value(setting_key) != self.override_app_check_box.checkState():
            Settings().setValue(setting_key, self.override_app_check_box.checkState())
            changed = True
        if changed:
            self.settings_form.register_post_process('mediaitem_suffix_reset')
            self.settings_form.register_post_process('mediaitem_presentation_rebuild')
            self.settings_form.register_post_process('mediaitem_suffixes')

    def tab_visible(self):
        """
        Tab has just been made visible to the user
        """
        self.activated = True
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = self.presenter_check_boxes[controller.name]
            checkbox.setEnabled(controller.is_available())
            self.set_controller_text(checkbox, controller)
