# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky                                             #
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
from openlp.core.lib.settings import Settings

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
        self.leftLayout.addWidget(self.customModeGroupBox)
        self.leftLayout.addStretch()
        self.rightLayout.addStretch()
        QtCore.QObject.connect(self.displayFooterCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onDisplayFooterCheckBoxChanged)

    def retranslateUi(self):
        self.customModeGroupBox.setTitle(translate('CustomPlugin.CustomTab',
            'Custom Display'))
        self.displayFooterCheckBox.setText(
            translate('CustomPlugin.CustomTab', 'Display footer'))

    def onDisplayFooterCheckBoxChanged(self, check_state):
        self.displayFooter = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.displayFooter = True

    def load(self):
        self.displayFooter = Settings().value(
            self.settingsSection + u'/display footer',
            QtCore.QVariant(True)).toBool()
        self.displayFooterCheckBox.setChecked(self.displayFooter)

    def save(self):
        Settings().setValue(self.settingsSection + u'/display footer',
            QtCore.QVariant(self.displayFooter))
