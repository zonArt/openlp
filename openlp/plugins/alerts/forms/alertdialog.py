# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

class Ui_AlertDialog(object):
    def setupUi(self, AlertForm):
        AlertForm.setObjectName(u'AlertDialog')
        AlertForm.resize(430, 320)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/icon/openlp.org-icon-32.bmp'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.AlertEntryWidget)
        self.verticalLayout_2.setObjectName(u'verticalLayout_2')
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.AlertEntryLabel = QtGui.QLabel(self.AlertEntryWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlertEntryLabel.sizePolicy().hasHeightForWidth())
        self.AlertEntryLabel.setSizePolicy(sizePolicy)
        self.AlertEntryLabel.setObjectName(u'AlertEntryLabel')
        self.verticalLayout.addWidget(self.AlertEntryLabel)
        self.AlertEntryEditItem = QtGui.QLineEdit(self.AlertEntryWidget)
        self.AlertEntryEditItem.setObjectName(u'AlertEntryEditItem')
        self.verticalLayout.addWidget(self.AlertEntryEditItem)
        self.AlertListWidget = QtGui.QListWidget(self.AlertEntryWidget)
        self.AlertListWidget.setAlternatingRowColors(True)
        self.AlertListWidget.setObjectName(u'AlertListWidget')
        self.verticalLayout.addWidget(self.AlertListWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        spacerItem = QtGui.QSpacerItem(181, 38, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.DisplayButton = QtGui.QPushButton(self.AlertEntryWidget)
        self.DisplayButton.setObjectName(u'DisplayButton')
        self.horizontalLayout.addWidget(self.DisplayButton)
        self.CancelButton = QtGui.QPushButton(self.AlertEntryWidget)
        self.CancelButton.setObjectName(u'CancelButton')
        self.horizontalLayout.addWidget(self.CancelButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.AlertFormLayout.addWidget(self.AlertEntryWidget)

        self.retranslateUi(AlertForm)
        QtCore.QObject.connect(self.CancelButton, QtCore.SIGNAL(u'clicked()'), self.close)
        QtCore.QMetaObject.connectSlotsByName(AlertForm)

    def retranslateUi(self, AlertForm):
        AlertForm.setWindowTitle(self.trUtf8('Alert Message'))
        self.AlertEntryLabel.setText(self.trUtf8('Alert Text:'))
        self.DisplayButton.setText(self.trUtf8('Display'))
        self.CancelButton.setText(self.trUtf8('Cancel'))
