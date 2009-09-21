# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab, str_to_bool, translate

class RemoteTab(SettingsTab):
    """
    RemoteTab is the Remotes settings tab in the settings dialog.
    """
    def __init__(self):
        SettingsTab.__init__(
            self, translate(u'RemoteTab', u'Remotes'), u'Remotes')

    def setupUi(self):
        self.setObjectName(u'RemoteTab')
        self.RemoteLayout = QtGui.QFormLayout(self)
        self.RemoteLayout.setObjectName(u'RemoteLayout')
        self.RemoteModeGroupBox = QtGui.QGroupBox(self)
        self.RemoteModeGroupBox.setObjectName(u'RemoteModeGroupBox')
        self.RemoteModeLayout = QtGui.QVBoxLayout(self.RemoteModeGroupBox)
        self.RemoteModeLayout.setSpacing(8)
        self.RemoteModeLayout.setMargin(8)
        self.RemoteModeLayout.setObjectName(u'RemoteModeLayout')
        self.RemotePortSpinBox = QtGui.QSpinBox(self.RemoteModeGroupBox)
        self.RemotePortSpinBox.setObjectName(u'RemotePortSpinBox')
        self.RemotePortSpinBox.setMaximum(32767)
        self.RemoteModeLayout.addWidget(self.RemotePortSpinBox)
        self.RemoteActive = QtGui.QCheckBox(self.RemoteModeGroupBox)
        self.RemoteActive.setObjectName(u'RemotePortSpinBox')
        self.RemoteModeLayout.addWidget(self.RemoteActive)
        self.WarningLabel = QtGui.QLabel(self.RemoteModeGroupBox)
        self.WarningLabel.setObjectName(u'WarningLabel')
        self.RemoteModeLayout.addWidget(self.WarningLabel)
        self.RemoteLayout.setWidget(
            0, QtGui.QFormLayout.LabelRole, self.RemoteModeGroupBox)

    def retranslateUi(self):
        self.RemoteModeGroupBox.setTitle(
            translate(u'RemoteTab', u'Remotes Receiver Port'))
        self.RemoteActive.setText(translate(u'RemoteTab', 'Remote available:'))
        self.WarningLabel.setText(translate(u'RemoteTab',
            u'A restart is needed for this change to become effective'))

    def load(self):
        self.RemotePortSpinBox.setValue(
            int(self.config.get_config(u'remote port', 4316)))
        self.RemoteActive.setChecked(int(
            self.config.get_config(u'startup', 0)))

    def save(self):
        self.config.set_config(
            u'remote port', unicode(self.RemotePortSpinBox.value()))
        self.config.set_config(
            u'startup', unicode(self.RemoteActive.checkState()))

