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

class Ui_FileRenameDialog(object):
    def setupUi(self, FileRenameDialog):
        FileRenameDialog.setObjectName(u'FileRenameDialog')
        FileRenameDialog.resize(400, 87)
        self.buttonBox = QtGui.QDialogButtonBox(FileRenameDialog)
        self.buttonBox.setGeometry(QtCore.QRect(210, 50, 171, 25))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u'buttonBox')
        self.widget = QtGui.QWidget(FileRenameDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 381, 35))
        self.widget.setObjectName(u'widget')
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.fileRenameLabel = QtGui.QLabel(self.widget)
        self.fileRenameLabel.setObjectName(u'fileRenameLabel')
        self.horizontalLayout.addWidget(self.fileRenameLabel)
        self.fileNameEdit = QtGui.QLineEdit(self.widget)
        self.fileNameEdit.setObjectName(u'fileNameEdit')
        self.horizontalLayout.addWidget(self.fileNameEdit)

        self.retranslateUi(FileRenameDialog)
        QtCore.QMetaObject.connectSlotsByName(FileRenameDialog)

    def retranslateUi(self, FileRenameDialog):
        self.fileRenameLabel.setText(translate('OpenLP.FileRenameForm',
            'New File Name:'))