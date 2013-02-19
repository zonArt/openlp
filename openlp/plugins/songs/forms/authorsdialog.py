# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
from openlp.core.lib.ui import create_button_box

class Ui_AuthorsDialog(object):
    def setupUi(self, authorsDialog):
        authorsDialog.setObjectName(u'AuthorsDialog')
        authorsDialog.resize(300, 10)
        self.dialogLayout = QtGui.QVBoxLayout(authorsDialog)
        self.dialogLayout.setObjectName(u'dialog_layout')
        self.authorLayout = QtGui.QFormLayout()
        self.authorLayout.setObjectName(u'authorLayout')
        self.firstNameLabel = QtGui.QLabel(authorsDialog)
        self.firstNameLabel.setObjectName(u'firstNameLabel')
        self.firstNameEdit = QtGui.QLineEdit(authorsDialog)
        self.firstNameEdit.setObjectName(u'firstNameEdit')
        self.firstNameLabel.setBuddy(self.firstNameEdit)
        self.authorLayout.addRow(self.firstNameLabel, self.firstNameEdit)
        self.lastNameLabel = QtGui.QLabel(authorsDialog)
        self.lastNameLabel.setObjectName(u'lastNameLabel')
        self.lastNameEdit = QtGui.QLineEdit(authorsDialog)
        self.lastNameEdit.setObjectName(u'lastNameEdit')
        self.lastNameLabel.setBuddy(self.lastNameEdit)
        self.authorLayout.addRow(self.lastNameLabel, self.lastNameEdit)
        self.displayLabel = QtGui.QLabel(authorsDialog)
        self.displayLabel.setObjectName(u'displayLabel')
        self.displayEdit = QtGui.QLineEdit(authorsDialog)
        self.displayEdit.setObjectName(u'displayEdit')
        self.displayLabel.setBuddy(self.displayEdit)
        self.authorLayout.addRow(self.displayLabel, self.displayEdit)
        self.dialogLayout.addLayout(self.authorLayout)
        self.button_box = create_button_box(authorsDialog, u'button_box', [u'cancel', u'save'])
        self.dialogLayout.addWidget(self.button_box)
        self.retranslateUi(authorsDialog)
        authorsDialog.setMaximumHeight(authorsDialog.sizeHint().height())

    def retranslateUi(self, authorsDialog):
        authorsDialog.setWindowTitle(translate('SongsPlugin.AuthorsForm', 'Author Maintenance'))
        self.displayLabel.setText(translate('SongsPlugin.AuthorsForm', 'Display name:'))
        self.firstNameLabel.setText(translate('SongsPlugin.AuthorsForm', 'First name:'))
        self.lastNameLabel.setText(translate('SongsPlugin.AuthorsForm', 'Last name:'))
