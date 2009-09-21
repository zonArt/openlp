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

from openlp.core.lib import SettingsTab, str_to_bool, translate, Receiver

class AuditTab(SettingsTab):
    """
    AuditTab is the Audit settings tab in the settings dialog.
    """
    def __init__(self):
        SettingsTab.__init__(self, translate(u'AuditTab', u'Audit'), u'Audit')

    def setupUi(self):
        self.setObjectName(u'AuditTab')
        self.AuditModeGroupBox = QtGui.QGroupBox(self)
        self.AuditModeGroupBox.setObjectName(u'AuditModeGroupBox')
        self.verticalLayout = QtGui.QVBoxLayout(self.AuditModeGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AuditFileName = QtGui.QLineEdit(self)
        self.AuditFileName.setObjectName("AuditFileName")
        self.horizontalLayout.addWidget(self.AuditFileName)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(u':/imports/import_load.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AuditFileButton = QtGui.QPushButton(self)
        self.AuditFileButton.setObjectName("AuditFileButton")
        self.AuditFileButton.setIcon(icon1)
        self.horizontalLayout.addWidget(self.AuditFileButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.AuditActive = QtGui.QCheckBox(self)
        self.AuditActive.setObjectName("AuditActive")
        self.verticalLayout.addWidget(self.AuditActive)
        self.WarningLabel = QtGui.QLabel(self)
        self.WarningLabel.setObjectName("WarningLabel")
        self.verticalLayout.addWidget(self.WarningLabel)
        QtCore.QObject.connect(self.AuditFileButton,
            QtCore.SIGNAL(u'pressed()'), self.onAuditFileButtonClicked)

    def retranslateUi(self):
        self.AuditModeGroupBox.setTitle(translate(u'AuditTab', u'Audit File'))
        self.AuditActive.setText(translate(u'AuditTab', 'Audit available:'))
        self.WarningLabel.setText(translate(u'AuditTab',
            u'A restart is needed for this change to become effective'))

    def load(self):
        self.AuditFileName.setText(self.config.get_config(u'Audit file', u''))
        self.AuditActive.setChecked(int(self.config.get_config(u'startup', 0)))

    def onAuditFileButtonClicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(
            self, u'Audit File',self.AuditFileName.text())
        if filename != u'':
            filename = unicode(filename)
            self.AuditFileName.setText(filename)

    def save(self):
        self.config.set_config(
            u'Audit file', unicode(self.AuditFileName.text()))
        self.config.set_config(
            u'startup', unicode(self.AuditActive.checkState()))
        Receiver().send_message(u'audit_changed')
