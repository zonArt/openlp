# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

import logging
from PyQt4 import QtCore, QtGui
from openlp.core.lib import build_icon

class AlertForm(QtGui.QDialog):
    global log
    log = logging.getLogger(u'AlertForm')

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        log.debug(u'Defined')

    def setupUi(self, AlertForm):
        AlertForm.setObjectName(u'AlertForm')
        AlertForm.resize(370, 110)
        icon = build_icon(u':/icon/openlp-logo-16x16.png')
        AlertForm.setWindowIcon(icon)
        self.AlertFormLayout = QtGui.QVBoxLayout(AlertForm)
        self.AlertFormLayout.setSpacing(8)
        self.AlertFormLayout.setMargin(8)
        self.AlertFormLayout.setObjectName(u'AlertFormLayout')
        self.AlertEntryWidget = QtGui.QWidget(AlertForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlertEntryWidget.sizePolicy().hasHeightForWidth())
        self.AlertEntryWidget.setSizePolicy(sizePolicy)
        self.AlertEntryWidget.setObjectName(u'AlertEntryWidget')
        self.AlertEntryLabel = QtGui.QLabel(self.AlertEntryWidget)
        self.AlertEntryLabel.setGeometry(QtCore.QRect(0, 0, 353, 16))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlertEntryLabel.sizePolicy().hasHeightForWidth())
        self.AlertEntryLabel.setSizePolicy(sizePolicy)
        self.AlertEntryLabel.setObjectName(u'AlertEntryLabel')
        self.AlertEntryEditItem = QtGui.QLineEdit(self.AlertEntryWidget)
        self.AlertEntryEditItem.setGeometry(QtCore.QRect(0, 20, 353, 26))
        self.AlertEntryEditItem.setObjectName(u'AlertEntryEditItem')
        self.AlertFormLayout.addWidget(self.AlertEntryWidget)
        self.ButtonBoxWidget = QtGui.QWidget(AlertForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonBoxWidget.sizePolicy().hasHeightForWidth())
        self.ButtonBoxWidget.setSizePolicy(sizePolicy)
        self.ButtonBoxWidget.setObjectName(u'ButtonBoxWidget')
        self.horizontalLayout = QtGui.QHBoxLayout(self.ButtonBoxWidget)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        spacerItem = QtGui.QSpacerItem(267, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.DisplayButton = QtGui.QPushButton(self.ButtonBoxWidget)
        self.DisplayButton.setObjectName(u'DisplayButton')
        self.horizontalLayout.addWidget(self.DisplayButton)
        self.CancelButton = QtGui.QPushButton(self.ButtonBoxWidget)
        self.CancelButton.setObjectName(u'CancelButton')
        self.horizontalLayout.addWidget(self.CancelButton)
        self.AlertFormLayout.addWidget(self.ButtonBoxWidget)

        self.retranslateUi(AlertForm)

        QtCore.QObject.connect(self.CancelButton, QtCore.SIGNAL(u'clicked()'), AlertForm.close)
        QtCore.QObject.connect(self.DisplayButton, QtCore.SIGNAL(u'clicked()'), self.onDisplayClicked)
        QtCore.QMetaObject.connectSlotsByName(AlertForm)

    def retranslateUi(self, AlertForm):
        AlertForm.setWindowTitle(self.trUtf8('Alert Message'))
        self.AlertEntryLabel.setText(self.trUtf8('Alert Text:'))
        self.DisplayButton.setText(self.trUtf8('Display'))
        self.CancelButton.setText(self.trUtf8('Cancel'))

    def onDisplayClicked(self):
        self.parent.mainDisplay.displayAlert(self.AlertEntryEditItem.text())
