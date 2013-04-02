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
"""
The UI widgets for the rename dialog
"""
from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import create_button_box


class Ui_FileRenameDialog(object):
    """
    The UI widgets for the rename dialog
    """
    def setupUi(self, fileRenameDialog):
        """
        Set up the UI
        """
        fileRenameDialog.setObjectName(u'fileRenameDialog')
        fileRenameDialog.resize(300, 10)
        self.dialogLayout = QtGui.QGridLayout(fileRenameDialog)
        self.dialogLayout.setObjectName(u'dialog_layout')
        self.fileNameLabel = QtGui.QLabel(fileRenameDialog)
        self.fileNameLabel.setObjectName(u'fileNameLabel')
        self.dialogLayout.addWidget(self.fileNameLabel, 0, 0)
        self.fileNameEdit = QtGui.QLineEdit(fileRenameDialog)
        self.fileNameEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'[^/\\?*|<>\[\]":+%]+'), self))
        self.fileNameEdit.setObjectName(u'fileNameEdit')
        self.dialogLayout.addWidget(self.fileNameEdit, 0, 1)
        self.button_box = create_button_box(fileRenameDialog, u'button_box', [u'cancel', u'ok'])
        self.dialogLayout.addWidget(self.button_box, 1, 0, 1, 2)
        self.retranslateUi(fileRenameDialog)
        self.setMaximumHeight(self.sizeHint().height())

    def retranslateUi(self, fileRenameDialog):
        """
        Translate the UI on the fly.
        """
        self.fileNameLabel.setText(translate('OpenLP.FileRenameForm', 'New File Name:'))
