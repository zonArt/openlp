# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

from openlp.core.lib import translate, SpellTextEdit
from openlp.core.lib.ui import create_button_box

class ServiceNoteForm(QtGui.QDialog):
    """
    This is the form that is used to edit the verses of the song.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi()
        self.retranslateUi()

    def exec_(self):
        self.textEdit.setFocus()
        return QtGui.QDialog.exec_(self)

    def setupUi(self):
        self.setObjectName(u'serviceNoteEdit')
        self.dialogLayout = QtGui.QVBoxLayout(self)
        self.dialogLayout.setContentsMargins(8, 8, 8, 8)
        self.dialogLayout.setSpacing(8)
        self.dialogLayout.setObjectName(u'verticalLayout')
        self.textEdit = SpellTextEdit(self, False)
        self.textEdit.setObjectName(u'textEdit')
        self.dialogLayout.addWidget(self.textEdit)
        self.buttonBox = create_button_box(self, u'buttonBox',
            [u'cancel', u'save'])
        self.dialogLayout.addWidget(self.buttonBox)

    def retranslateUi(self):
        self.setWindowTitle(
            translate('OpenLP.ServiceNoteForm', 'Service Item Notes'))
