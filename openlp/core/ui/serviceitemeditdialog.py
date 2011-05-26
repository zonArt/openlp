# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Millar, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Jeffrey Smith, Maikel            #
# Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund                    #
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

from openlp.core.lib import translate
from openlp.core.lib.ui import create_accept_reject_button_box, \
    create_delete_push_button, create_up_down_push_button_set

class Ui_ServiceItemEditDialog(object):
    def setupUi(self, serviceItemEditDialog):
        serviceItemEditDialog.setObjectName(u'serviceItemEditDialog')
        self.dialogLayout = QtGui.QGridLayout(serviceItemEditDialog)
        self.dialogLayout.setObjectName(u'dialogLayout')
        self.listWidget = QtGui.QListWidget(serviceItemEditDialog)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName(u'listWidget')
        self.dialogLayout.addWidget(self.listWidget, 0, 0)
        self.buttonLayout = QtGui.QVBoxLayout()
        self.buttonLayout.setObjectName(u'buttonLayout')
        self.deleteButton = create_delete_push_button(serviceItemEditDialog)
        self.buttonLayout.addWidget(self.deleteButton)
        self.buttonLayout.addStretch()
        self.upButton, self.downButton = create_up_down_push_button_set(
            serviceItemEditDialog)
        self.buttonLayout.addWidget(self.upButton)
        self.buttonLayout.addWidget(self.downButton)
        self.dialogLayout.addLayout(self.buttonLayout, 0, 1)
        self.dialogLayout.addWidget(
            create_accept_reject_button_box(serviceItemEditDialog), 1, 0, 1, 2)
        self.retranslateUi(serviceItemEditDialog)
        QtCore.QMetaObject.connectSlotsByName(serviceItemEditDialog)

    def retranslateUi(self, serviceItemEditDialog):
        serviceItemEditDialog.setWindowTitle(
            translate('OpenLP.ServiceItemEditForm', 'Reorder Service Item'))
