# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
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
from openlp.core.lib import translate

class Ui_ServiceNoteEdit(object):
    def setupUi(self, serviceNoteEdit):
        serviceNoteEdit.setObjectName(u'serviceNoteEdit')
        self.dialogLayout = QtGui.QVBoxLayout(serviceNoteEdit)
        self.dialogLayout.setObjectName(u'verticalLayout')
        self.textEdit = QtGui.QTextEdit(serviceNoteEdit)
        self.textEdit.setObjectName(u'textEdit')
        self.dialogLayout.addWidget(self.textEdit)
        self.buttonBox = QtGui.QDialogButtonBox(serviceNoteEdit)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(u'buttonBox')
        self.dialogLayout.addWidget(self.buttonBox)
        self.retranslateUi(serviceNoteEdit)
        QtCore.QMetaObject.connectSlotsByName(serviceNoteEdit)

    def retranslateUi(self, serviceNoteEdit):
        serviceNoteEdit.setWindowTitle(
            translate('OpenLP.ServiceNoteForm', 'Service Item Notes'))
