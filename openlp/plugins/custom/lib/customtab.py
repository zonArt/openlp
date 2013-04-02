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
The :mod:`~openlp.plugins.custom.lib.customtab` module contains the settings tab
for the Custom Slides plugin, which is inserted into the configuration dialog.
"""

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab, Settings, translate

class CustomTab(SettingsTab):
    """
    CustomTab is the Custom settings tab in the settings dialog.
    """
    def __init__(self, parent, title, visible_title, icon_path):
        SettingsTab.__init__(self, parent, title, visible_title, icon_path)

    def setupUi(self):
        self.setObjectName(u'CustomTab')
        SettingsTab.setupUi(self)
        self.customModeGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.customModeGroupBox.setObjectName(u'customModeGroupBox')
        self.customModeLayout = QtGui.QFormLayout(self.customModeGroupBox)
        self.customModeLayout.setObjectName(u'customModeLayout')
        self.displayFooterCheckBox = QtGui.QCheckBox(self.customModeGroupBox)
        self.displayFooterCheckBox.setObjectName(u'displayFooterCheckBox')
        self.customModeLayout.addRow(self.displayFooterCheckBox)
        self.add_from_service_checkbox = QtGui.QCheckBox(self.customModeGroupBox)
        self.add_from_service_checkbox.setObjectName(u'add_from_service_checkbox')
        self.customModeLayout.addRow(self.add_from_service_checkbox)
        self.leftLayout.addWidget(self.customModeGroupBox)
        self.leftLayout.addStretch()
        self.rightLayout.addStretch()
        QtCore.QObject.connect(self.displayFooterCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onDisplayFooterCheckBoxChanged)
        QtCore.QObject.connect(self.add_from_service_checkbox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.on_add_from_service_check_box_changed)

    def retranslateUi(self):
        self.customModeGroupBox.setTitle(translate('CustomPlugin.CustomTab', 'Custom Display'))
        self.displayFooterCheckBox.setText(translate('CustomPlugin.CustomTab', 'Display footer'))
        self.add_from_service_checkbox.setText(translate('CustomPlugin.CustomTab',
            'Import missing custom slides from service files'))

    def onDisplayFooterCheckBoxChanged(self, check_state):
        """
        Toggle the setting for displaying the footer.
        """
        self.displayFooter = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.displayFooter = True

    def on_add_from_service_check_box_changed(self, check_state):
        self.update_load = (check_state == QtCore.Qt.Checked)

    def load(self):
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        self.displayFooter = settings.value(u'display footer')
        self.update_load = settings.value(u'add custom from service')
        self.displayFooterCheckBox.setChecked(self.displayFooter)
        self.add_from_service_checkbox.setChecked(self.update_load)
        settings.endGroup()

    def save(self):
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'display footer', self.displayFooter)
        settings.setValue(u'add custom from service', self.update_load)
        settings.endGroup()
