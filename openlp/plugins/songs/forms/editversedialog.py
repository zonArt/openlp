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
from openlp.plugins.songs.lib import VerseType

class Ui_EditVerseDialog(object):
    def setupUi(self, EditVerseDialog):
        EditVerseDialog.setObjectName(u'EditVerseDialog')
        EditVerseDialog.resize(474, 442)
        EditVerseDialog.setModal(True)
        self.EditVerseLayout = QtGui.QVBoxLayout(EditVerseDialog)
        self.EditVerseLayout.setSpacing(8)
        self.EditVerseLayout.setMargin(8)
        self.EditVerseLayout.setObjectName(u'EditVerseLayout')
        self.VerseTextEdit = QtGui.QPlainTextEdit(EditVerseDialog)
        self.VerseTextEdit.setObjectName(u'VerseTextEdit')
        self.EditVerseLayout.addWidget(self.VerseTextEdit)
        self.VerseTypeLayout = QtGui.QHBoxLayout()
        self.VerseTypeLayout.setSpacing(8)
        self.VerseTypeLayout.setObjectName(u'VerseTypeLayout')
        self.VerseTypeLabel = QtGui.QLabel(EditVerseDialog)
        self.VerseTypeLabel.setObjectName(u'VerseTypeLabel')
        self.VerseTypeLayout.addWidget(self.VerseTypeLabel)
        self.VerseTypeComboBox = QtGui.QComboBox(EditVerseDialog)
        self.VerseTypeComboBox.setObjectName(u'VerseTypeComboBox')
        self.VerseTypeComboBox.addItem(u'')
        self.VerseTypeComboBox.addItem(u'')
        self.VerseTypeComboBox.addItem(u'')
        self.VerseTypeComboBox.addItem(u'')
        self.VerseTypeComboBox.addItem(u'')
        self.VerseTypeComboBox.addItem(u'')
        self.VerseTypeComboBox.addItem(u'')
        self.VerseTypeLayout.addWidget(self.VerseTypeComboBox)
        self.VerseNumberBox = QtGui.QSpinBox(EditVerseDialog)
        self.VerseNumberBox.setMinimum(1)
        self.VerseNumberBox.setObjectName(u'VerseNumberBox')
        self.VerseTypeLayout.addWidget(self.VerseNumberBox)
        self.InsertButton = QtGui.QPushButton(EditVerseDialog)
        self.AddIcon = QtGui.QIcon()
        self.AddIcon.addPixmap(QtGui.QPixmap(u':/general/general_add.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.InsertButton.setIcon(self.AddIcon)
        self.InsertButton.setObjectName(u'InsertButton')
        self.VerseTypeLayout.addWidget(self.InsertButton)
        self.VerseTypeSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.VerseTypeLayout.addItem(self.VerseTypeSpacer)
        self.EditVerseLayout.addLayout(self.VerseTypeLayout)
        self.EditButtonBox = QtGui.QDialogButtonBox(EditVerseDialog)
        self.EditButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.EditButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Save)
        self.EditButtonBox.setObjectName(u'EditButtonBox')
        self.EditVerseLayout.addWidget(self.EditButtonBox)

        self.retranslateUi(EditVerseDialog)
        QtCore.QObject.connect(self.EditButtonBox, QtCore.SIGNAL(u'accepted()'),
            EditVerseDialog.accept)
        QtCore.QObject.connect(self.EditButtonBox, QtCore.SIGNAL(u'rejected()'),
            EditVerseDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditVerseDialog)

    def retranslateUi(self, EditVerseDialog):
        EditVerseDialog.setWindowTitle(
            translate('SongsPlugin.EditVerseForm', 'Edit Verse'))
        self.VerseTypeLabel.setText(
            translate('SongsPlugin.EditVerseForm', '&Verse type:'))
        self.VerseTypeComboBox.setItemText(0,
            VerseType.to_string(VerseType.Verse))
        self.VerseTypeComboBox.setItemText(1,
            VerseType.to_string(VerseType.Chorus))
        self.VerseTypeComboBox.setItemText(2,
            VerseType.to_string(VerseType.Bridge))
        self.VerseTypeComboBox.setItemText(3,
            VerseType.to_string(VerseType.PreChorus))
        self.VerseTypeComboBox.setItemText(4,
            VerseType.to_string(VerseType.Intro))
        self.VerseTypeComboBox.setItemText(5,
            VerseType.to_string(VerseType.Ending))
        self.VerseTypeComboBox.setItemText(6,
            VerseType.to_string(VerseType.Other))
        self.InsertButton.setText(
            translate('SongsPlugin.EditVerseForm', '&Insert'))

