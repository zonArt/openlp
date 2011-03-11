# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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
    def __init__(self, title, visible_title):
        SettingsTab.__init__(self, title, visible_title)

    def setupUi(self):
        self.setObjectName(u'RemoteTab')
        SettingsTab.setupUi(self)
        self.serverSettingsGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.serverSettingsGroupBox.setObjectName(u'serverSettingsGroupBox')
        self.serverSettingsLayout = QtGui.QFormLayout(
            self.serverSettingsGroupBox)
        self.serverSettingsLayout.setObjectName(u'serverSettingsLayout')
        self.addressLabel = QtGui.QLabel(self.serverSettingsGroupBox)
        self.addressLabel.setObjectName(u'addressLabel')
        self.addressEdit = QtGui.QLineEdit(self.serverSettingsGroupBox)
        self.addressEdit.setSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.addressEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(
            u'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'), self))
        self.addressEdit.setObjectName(u'addressEdit')
        self.serverSettingsLayout.addRow(self.addressLabel, self.addressEdit)
        self.portLabel = QtGui.QLabel(self.serverSettingsGroupBox)
        self.portLabel.setObjectName(u'portLabel')
        self.portSpinBox = QtGui.QSpinBox(self.serverSettingsGroupBox)
        self.portSpinBox.setMaximum(32767)
        self.portSpinBox.setObjectName(u'portSpinBox')
        self.serverSettingsLayout.addRow(self.portLabel, self.portSpinBox)
        self.leftLayout.addWidget(self.serverSettingsGroupBox)
        self.leftLayout.addStretch()
        self.rightLayout.addStretch()

    def retranslateUi(self):
        self.serverSettingsGroupBox.setTitle(
            translate('RemotePlugin.RemoteTab', 'Server Settings'))
        self.addressLabel.setText(translate('RemotePlugin.RemoteTab',
            'Serve on IP address:'))
        self.portLabel.setText(translate('RemotePlugin.RemoteTab',
            'Port number:'))

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
