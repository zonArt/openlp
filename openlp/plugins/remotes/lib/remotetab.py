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

class RemoteTab(SettingsTab):
    """
    RemoteTab is the Remotes settings tab in the settings dialog.
    """
    def __init__(self, title):
        SettingsTab.__init__(self, title)

    def setupUi(self):
        self.setObjectName(u'RemoteTab')
        self.tabTitleVisible = translate('RemotePlugin.RemoteTab', 'Remotes')
        self.remoteLayout = QtGui.QFormLayout(self)
        self.remoteLayout.setObjectName(u'remoteLayout')
        self.serverSettingsGroupBox = QtGui.QGroupBox(self)
        self.serverSettingsGroupBox.setObjectName(u'serverSettingsGroupBox')
        self.serverSettingsLayout = QtGui.QFormLayout(self.serverSettingsGroupBox)
        self.serverSettingsLayout.setSpacing(8)
        self.serverSettingsLayout.setMargin(8)
        self.serverSettingsLayout.setObjectName(u'serverSettingsLayout')
        self.addressEdit = QtGui.QLineEdit(self.serverSettingsGroupBox)
        self.addressEdit.setObjectName(u'addressEdit')
        self.serverSettingsLayout.addRow(
            translate('RemotePlugin.RemoteTab', 'Serve on IP address:'),
            self.addressEdit)
        self.portSpinBox = QtGui.QSpinBox(self.serverSettingsGroupBox)
        self.portSpinBox.setObjectName(u'portSpinBox')
        self.portSpinBox.setMaximum(32767)
        self.serverSettingsLayout.addRow(
            translate('RemotePlugin.RemoteTab', 'Port number:'),
            self.portSpinBox)
        self.remoteLayout.setWidget(
            0, QtGui.QFormLayout.LabelRole, self.serverSettingsGroupBox)

    def retranslateUi(self):
        self.serverSettingsGroupBox.setTitle(
            translate('RemotePlugin.RemoteTab', 'Server Settings'))

    def load(self):
        self.portSpinBox.setValue(
            QtCore.QSettings().value(self.settingsSection + u'/port',
                QtCore.QVariant(4316)).toInt()[0])
        self.addressEdit.setText(
            QtCore.QSettings().value(self.settingsSection + u'/ip address',
                QtCore.QVariant(u'0.0.0.0')).toString())

    def save(self):
        QtCore.QSettings().setValue(self.settingsSection + u'/port',
            QtCore.QVariant(self.portSpinBox.value()))
        QtCore.QSettings().setValue(self.settingsSection + u'/ip address',
            QtCore.QVariant(self.addressEdit.text()))