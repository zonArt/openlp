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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab, translate

class CustomTab(SettingsTab):
    """
    CustomTab is the Custom settings tab in the settings dialog.
    """
    def __init__(self, title):
        SettingsTab.__init__(self, title)

    def setupUi(self):
        self.setObjectName(u'CustomTab')
        self.tabTitleVisible = translate('CustomPlugin.CustomTab', 'Custom')
        self.customLayout = QtGui.QFormLayout(self)
        self.customLayout.setSpacing(8)
        self.customLayout.setMargin(8)
        self.customLayout.setObjectName(u'customLayout')
        self.customModeGroupBox = QtGui.QGroupBox(self)
        self.customModeGroupBox.setObjectName(u'customModeGroupBox')
        self.customModeLayout = QtGui.QVBoxLayout(self.customModeGroupBox)
        self.customModeLayout.setSpacing(8)
        self.customModeLayout.setMargin(8)
        self.customModeLayout.setObjectName(u'customModeLayout')
        self.displayFooterCheckBox = QtGui.QCheckBox(self.customModeGroupBox)
        self.displayFooterCheckBox.setObjectName(u'displayFooterCheckBox')
        self.customModeLayout.addWidget(self.displayFooterCheckBox)
        self.customLayout.setWidget(
            0, QtGui.QFormLayout.LabelRole, self.customModeGroupBox)
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
        self.displayFooter = QtCore.QSettings().value(
            self.settingsSection + u'/display footer',
            QtCore.QVariant(True)).toBool()
        self.displayFooterCheckBox.setChecked(self.displayFooter)

    def save(self):
        QtCore.QSettings().setValue(self.settingsSection + u'/display footer',
            QtCore.QVariant(self.displayFooter))
