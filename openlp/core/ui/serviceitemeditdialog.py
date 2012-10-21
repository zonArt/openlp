# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Eric Ludin, Edwin Lunando, Brian T. Meyer,    #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Erode Woldsund                                                              #
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

from PyQt4 import QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import create_button_box, create_button

class Ui_ServiceItemEditDialog(object):
    def setupUi(self, serviceItemEditDialog):
        serviceItemEditDialog.setObjectName(u'serviceItemEditDialog')
        self.dialogLayout = QtGui.QGridLayout(serviceItemEditDialog)
        self.dialogLayout.setContentsMargins(8, 8, 8, 8)
        self.dialogLayout.setSpacing(8)
        self.dialogLayout.setObjectName(u'dialogLayout')
        self.listWidget = QtGui.QListWidget(serviceItemEditDialog)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName(u'listWidget')
        self.dialogLayout.addWidget(self.listWidget, 0, 0)
        self.buttonLayout = QtGui.QVBoxLayout()
        self.buttonLayout.setObjectName(u'buttonLayout')
        self.deleteButton = create_button(serviceItemEditDialog,
            u'deleteButton', role=u'delete',
            click=serviceItemEditDialog.onDeleteButtonClicked)
        self.buttonLayout.addWidget(self.deleteButton)
        self.buttonLayout.addStretch()
        self.upButton = create_button(serviceItemEditDialog, u'upButton',
            role=u'up', click=serviceItemEditDialog.onUpButtonClicked)
        self.downButton = create_button(serviceItemEditDialog, u'downButton',
            role=u'down', click=serviceItemEditDialog.onDownButtonClicked)
        self.buttonLayout.addWidget(self.upButton)
        self.buttonLayout.addWidget(self.downButton)
        self.dialogLayout.addLayout(self.buttonLayout, 0, 1)
        self.buttonBox = create_button_box(serviceItemEditDialog, u'buttonBox',
            [u'cancel', u'save'])
        self.dialogLayout.addWidget(self.buttonBox, 1, 0, 1, 2)
        self.retranslateUi(serviceItemEditDialog)

    def retranslateUi(self, serviceItemEditDialog):
        serviceItemEditDialog.setWindowTitle(
            translate('OpenLP.ServiceItemEditForm', 'Reorder Service Item'))
