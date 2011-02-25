# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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
from openlp.core.lib.ui import create_accept_reject_button_box
from openlp.plugins.songs.lib import VerseType

class Ui_EditVerseDialog(object):
    def setupUi(self, editVerseDialog):
        editVerseDialog.setObjectName(u'editVerseDialog')
        editVerseDialog.resize(400, 400)
        editVerseDialog.setModal(True)
        self.dialogLayout = QtGui.QVBoxLayout(editVerseDialog)
        self.dialogLayout.setObjectName(u'dialogLayout')
        self.verseTextEdit = SpellTextEdit(editVerseDialog)
        self.verseTextEdit.setObjectName(u'verseTextEdit')
        self.dialogLayout.addWidget(self.verseTextEdit)
        self.verseTypeLayout = QtGui.QHBoxLayout()
        self.verseTypeLayout.setObjectName(u'verseTypeLayout')
        self.verseTypeLabel = QtGui.QLabel(editVerseDialog)
        self.verseTypeLabel.setObjectName(u'verseTypeLabel')
        self.verseTypeLayout.addWidget(self.verseTypeLabel)
        self.verseTypeComboBox = QtGui.QComboBox(editVerseDialog)
        self.verseTypeComboBox.addItems([u'', u'', u'', u'', u'', u'', u''])
        self.verseTypeComboBox.setObjectName(u'verseTypeComboBox')
        self.verseTypeLabel.setBuddy(self.verseTypeComboBox)
        self.verseTypeLayout.addWidget(self.verseTypeComboBox)
        self.verseNumberBox = QtGui.QSpinBox(editVerseDialog)
        self.verseNumberBox.setMinimum(1)
        self.verseNumberBox.setObjectName(u'verseNumberBox')
        self.verseTypeLayout.addWidget(self.verseNumberBox)
        self.insertButton = QtGui.QPushButton(editVerseDialog)
        self.insertButton.setIcon(build_icon(u':/general/general_add.png'))
        self.insertButton.setObjectName(u'insertButton')
        self.verseTypeLayout.addWidget(self.insertButton)
        self.verseTypeLayout.addStretch()
        self.dialogLayout.addLayout(self.verseTypeLayout)
        self.dialogLayout.addWidget(
            create_accept_reject_button_box(editVerseDialog))
        self.retranslateUi(editVerseDialog)
        QtCore.QMetaObject.connectSlotsByName(editVerseDialog)

    def retranslateUi(self, editVerseDialog):
        editVerseDialog.setWindowTitle(
            translate('SongsPlugin.EditVerseForm', 'Edit Verse'))
        self.verseTypeLabel.setText(
            translate('SongsPlugin.EditVerseForm', '&Verse type:'))
        self.verseTypeComboBox.setItemText(VerseType.Verse,
            VerseType.TranslatedNames[VerseType.Verse])
        self.verseTypeComboBox.setItemText(VerseType.Chorus,
            VerseType.TranslatedNames[VerseType.Chorus])
        self.verseTypeComboBox.setItemText(VerseType.Bridge,
            VerseType.TranslatedNames[VerseType.Bridge])
        self.verseTypeComboBox.setItemText(VerseType.PreChorus,
            VerseType.TranslatedNames[VerseType.PreChorus])
        self.verseTypeComboBox.setItemText(VerseType.Intro,
            VerseType.TranslatedNames[VerseType.Intro])
        self.verseTypeComboBox.setItemText(VerseType.Ending,
            VerseType.TranslatedNames[VerseType.Ending])
        self.verseTypeComboBox.setItemText(VerseType.Other,
            VerseType.TranslatedNames[VerseType.Other])
        self.insertButton.setText(
            translate('SongsPlugin.EditVerseForm', '&Insert'))
