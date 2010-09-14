# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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

from openlp.core.lib import build_icon, translate, SpellTextEdit
from openlp.plugins.songs.lib import VerseType

class Ui_EditVerseDialog(object):
    def setupUi(self, editVerseDialog):
        editVerseDialog.setObjectName(u'editVerseDialog')
        editVerseDialog.resize(474, 442)
        editVerseDialog.setModal(True)
        self.editVerseLayout = QtGui.QVBoxLayout(editVerseDialog)
        self.editVerseLayout.setSpacing(8)
        self.editVerseLayout.setMargin(8)
        self.editVerseLayout.setObjectName(u'editVerseLayout')
        self.verseTextEdit = SpellTextEdit(editVerseDialog)
        self.verseTextEdit.setObjectName(u'verseTextEdit')
        self.editVerseLayout.addWidget(self.verseTextEdit)
        self.verseTypeLayout = QtGui.QHBoxLayout()
        self.verseTypeLayout.setSpacing(8)
        self.verseTypeLayout.setObjectName(u'verseTypeLayout')
        self.verseTypeLabel = QtGui.QLabel(editVerseDialog)
        self.verseTypeLabel.setObjectName(u'verseTypeLabel')
        self.verseTypeLayout.addWidget(self.verseTypeLabel)
        self.verseTypeComboBox = QtGui.QComboBox(editVerseDialog)
        self.verseTypeComboBox.setObjectName(u'verseTypeComboBox')
        self.verseTypeLabel.setBuddy(self.verseTypeComboBox)
        self.verseTypeComboBox.addItem(u'')
        self.verseTypeComboBox.addItem(u'')
        self.verseTypeComboBox.addItem(u'')
        self.verseTypeComboBox.addItem(u'')
        self.verseTypeComboBox.addItem(u'')
        self.verseTypeComboBox.addItem(u'')
        self.verseTypeComboBox.addItem(u'')
        self.verseTypeLayout.addWidget(self.verseTypeComboBox)
        self.verseNumberBox = QtGui.QSpinBox(editVerseDialog)
        self.verseNumberBox.setMinimum(1)
        self.verseNumberBox.setObjectName(u'verseNumberBox')
        self.verseTypeLayout.addWidget(self.verseNumberBox)
        self.insertButton = QtGui.QPushButton(editVerseDialog)
        self.insertButton.setIcon(build_icon(u':/general/general_add.png'))
        self.insertButton.setObjectName(u'insertButton')
        self.verseTypeLayout.addWidget(self.insertButton)
        self.verseTypeSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verseTypeLayout.addItem(self.verseTypeSpacer)
        self.editVerseLayout.addLayout(self.verseTypeLayout)
        self.editButtonBox = QtGui.QDialogButtonBox(editVerseDialog)
        self.editButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.editButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Save)
        self.editButtonBox.setObjectName(u'editButtonBox')
        self.editVerseLayout.addWidget(self.editButtonBox)

        self.retranslateUi(editVerseDialog)
        QtCore.QObject.connect(self.editButtonBox, QtCore.SIGNAL(u'accepted()'),
            editVerseDialog.accept)
        QtCore.QObject.connect(self.editButtonBox, QtCore.SIGNAL(u'rejected()'),
            editVerseDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(editVerseDialog)

    def retranslateUi(self, editVerseDialog):
        editVerseDialog.setWindowTitle(
            translate('SongsPlugin.EditVerseForm', 'Edit Verse'))
        self.verseTypeLabel.setText(
            translate('SongsPlugin.EditVerseForm', '&Verse type:'))
        self.verseTypeComboBox.setItemText(0,
            VerseType.to_string(VerseType.Verse))
        self.verseTypeComboBox.setItemText(1,
            VerseType.to_string(VerseType.Chorus))
        self.verseTypeComboBox.setItemText(2,
            VerseType.to_string(VerseType.Bridge))
        self.verseTypeComboBox.setItemText(3,
            VerseType.to_string(VerseType.PreChorus))
        self.verseTypeComboBox.setItemText(4,
            VerseType.to_string(VerseType.Intro))
        self.verseTypeComboBox.setItemText(5,
            VerseType.to_string(VerseType.Ending))
        self.verseTypeComboBox.setItemText(6,
            VerseType.to_string(VerseType.Other))
        self.insertButton.setText(
            translate('SongsPlugin.EditVerseForm', '&Insert'))
