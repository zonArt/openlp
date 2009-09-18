# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from openlp.core.lib import SettingsTab,  str_to_bool,  translate,  Receiver

class AuditTab(SettingsTab):
    """
    AuditTab is the Audit settings tab in the settings dialog.
    """
    def __init__(self):
        SettingsTab.__init__(self, translate(u'AuditTab', u'Audit'), u'Audit')

    def setupUi(self):
        self.setObjectName(u'AuditTab')
        self.AuditLayout = QtGui.QFormLayout(self)
        self.AuditLayout.setObjectName(u'AuditLayout')
        self.AuditModeGroupBox = QtGui.QGroupBox(self)
        self.AuditModeGroupBox.setObjectName(u'AuditModeGroupBox')
        self.AuditModeLayout = QtGui.QVBoxLayout(self.AuditModeGroupBox)
        self.AuditModeLayout.setSpacing(8)
        self.AuditModeLayout.setMargin(8)
        self.AuditModeLayout.setObjectName(u'AuditModeLayout')
        self.AuditPortSpinBox = QtGui.QSpinBox(self.AuditModeGroupBox)
        self.AuditPortSpinBox.setObjectName(u'AuditPortSpinBox')
        self.AuditPortSpinBox.setMaximum(32767)
        self.AuditModeLayout.addWidget(self.AuditPortSpinBox)
        self.AuditActive = QtGui.QCheckBox(self.AuditModeGroupBox)
        self.AuditActive.setObjectName(u'AuditPortSpinBox')
        self.AuditModeLayout.addWidget(self.AuditActive)
        self.WarningLabel = QtGui.QLabel(self.AuditModeGroupBox)
        self.WarningLabel.setObjectName(u'WarningLabel')
        self.AuditModeLayout.addWidget(self.WarningLabel)
        self.AuditLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.AuditModeGroupBox)

    def retranslateUi(self):
        self.AuditModeGroupBox.setTitle(translate(u'AuditTab', u'Audit File'))
        self.AuditActive.setText(translate(u'AuditTab', 'Audit available:'))
        self.WarningLabel.setText(translate(u'AuditTab', u'A restart is needed for this change to become effective'))

    def load(self):
        self.AuditPortSpinBox.setValue(int(self.config.get_config(u'Audit port', 4316)))
        self.AuditActive.setChecked(int(self.config.get_config(u'startup', 0)))

    def save(self):
        self.config.set_config(u'Audit port', unicode(self.AuditPortSpinBox.value()))
        self.config.set_config(u'startup', unicode(self.AuditActive.checkState()))

