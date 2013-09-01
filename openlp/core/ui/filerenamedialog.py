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
    def setupUi(self, file_rename_dialog):
        """
        Set up the UI
        """
        file_rename_dialog.setObjectName('file_rename_dialog')
        file_rename_dialog.resize(300, 10)
        self.dialog_layout = QtGui.QGridLayout(file_rename_dialog)
        self.dialog_layout.setObjectName('dialog_layout')
        self.file_name_label = QtGui.QLabel(file_rename_dialog)
        self.file_name_label.setObjectName('file_name_label')
        self.dialog_layout.addWidget(self.file_name_label, 0, 0)
        self.file_name_edit = QtGui.QLineEdit(file_rename_dialog)
        self.file_name_edit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'[^/\\?*|<>\[\]":+%]+'), self))
        self.file_name_edit.setObjectName('file_name_edit')
        self.dialog_layout.addWidget(self.file_name_edit, 0, 1)
        self.button_box = create_button_box(file_rename_dialog, 'button_box', ['cancel', 'ok'])
        self.dialog_layout.addWidget(self.button_box, 1, 0, 1, 2)
        self.retranslateUi(file_rename_dialog)
        self.setMaximumHeight(self.sizeHint().height())

    def retranslateUi(self, file_rename_dialog):
        """
        Translate the UI on the fly.
        """
        self.file_name_label.setText(translate('OpenLP.FileRenameForm', 'New File Name:'))
