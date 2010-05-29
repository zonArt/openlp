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
from openlp.core.lib import translate

class Ui_ServiceNoteEdit(object):
    def setupUi(self, ServiceNoteEdit):
        ServiceNoteEdit.setObjectName(u'ServiceNoteEdit')
        ServiceNoteEdit.resize(400, 243)
        self.widget = QtGui.QWidget(ServiceNoteEdit)
        self.widget.setGeometry(QtCore.QRect(20, 10, 361, 223))
        self.widget.setObjectName(u'widget')
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.textEdit = QtGui.QTextEdit(self.widget)
        self.textEdit.setObjectName(u'textEdit')
        self.verticalLayout.addWidget(self.textEdit)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(u'buttonBox')
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ServiceNoteEdit)
        QtCore.QMetaObject.connectSlotsByName(ServiceNoteEdit)

    def retranslateUi(self, ServiceNoteEdit):
        ServiceNoteEdit.setWindowTitle(
            translate('ServiceNoteForm', 'Service Item Notes'))

