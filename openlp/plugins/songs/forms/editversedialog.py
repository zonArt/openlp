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

from openlp.core.lib import SpellTextEdit, build_icon, translate
from openlp.core.lib.ui import UiStrings, create_button_box
from openlp.plugins.songs.lib import VerseType

class Ui_EditVerseDialog(object):
    def setupUi(self, editVerseDialog):
        editVerseDialog.setObjectName(u'editVerseDialog')
        editVerseDialog.resize(400, 400)
        editVerseDialog.setModal(True)
        self.dialogLayout = QtGui.QVBoxLayout(editVerseDialog)
        self.dialogLayout.setObjectName(u'dialog_layout')
        self.verseTextEdit = SpellTextEdit(editVerseDialog)
        self.verseTextEdit.setObjectName(u'verseTextEdit')
        self.dialogLayout.addWidget(self.verseTextEdit)
        self.verseTypeLayout = QtGui.QHBoxLayout()
        self.verseTypeLayout.setObjectName(u'verseTypeLayout')
        self.splitButton = QtGui.QPushButton(editVerseDialog)
        self.splitButton.setIcon(build_icon(u':/general/general_add.png'))
        self.splitButton.setObjectName(u'splitButton')
        self.verseTypeLayout.addWidget(self.splitButton)
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
        self.button_box = create_button_box(editVerseDialog, u'button_box', [u'cancel', u'ok'])
        self.dialogLayout.addWidget(self.button_box)
        self.retranslateUi(editVerseDialog)

    def retranslateUi(self, editVerseDialog):
        editVerseDialog.setWindowTitle(translate('SongsPlugin.EditVerseForm', 'Edit Verse'))
        self.verseTypeLabel.setText(translate('SongsPlugin.EditVerseForm', '&Verse type:'))
        self.verseTypeComboBox.setItemText(VerseType.Verse, VerseType.TranslatedNames[VerseType.Verse])
        self.verseTypeComboBox.setItemText(VerseType.Chorus, VerseType.TranslatedNames[VerseType.Chorus])
        self.verseTypeComboBox.setItemText(VerseType.Bridge, VerseType.TranslatedNames[VerseType.Bridge])
        self.verseTypeComboBox.setItemText(VerseType.PreChorus, VerseType.TranslatedNames[VerseType.PreChorus])
        self.verseTypeComboBox.setItemText(VerseType.Intro, VerseType.TranslatedNames[VerseType.Intro])
        self.verseTypeComboBox.setItemText(VerseType.Ending, VerseType.TranslatedNames[VerseType.Ending])
        self.verseTypeComboBox.setItemText(VerseType.Other, VerseType.TranslatedNames[VerseType.Other])
        self.splitButton.setText(UiStrings().Split)
        self.splitButton.setToolTip(UiStrings().SplitToolTip)
        self.insertButton.setText(translate('SongsPlugin.EditVerseForm', '&Insert'))
        self.insertButton.setToolTip(translate('SongsPlugin.EditVerseForm',
            'Split a slide into two by inserting a verse splitter.'))
