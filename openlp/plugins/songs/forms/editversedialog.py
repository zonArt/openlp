# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

class Ui_EditVerseDialog(object):
    def setupUi(self, EditVerseDialog):
        EditVerseDialog.setObjectName(u'EditVerseDialog')
        EditVerseDialog.resize(492, 373)
        EditVerseDialog.setModal(True)
        self.DialogLayout = QtGui.QVBoxLayout(EditVerseDialog)
        self.DialogLayout.setSpacing(8)
        self.DialogLayout.setMargin(8)
        self.DialogLayout.setObjectName(u'DialogLayout')
        self.VerseTextEdit = QtGui.QTextEdit(EditVerseDialog)
        self.VerseTextEdit.setAcceptRichText(False)
        self.VerseTextEdit.setObjectName(u'VerseTextEdit')
        self.DialogLayout.addWidget(self.VerseTextEdit)
        self.ButtonBox = QtGui.QDialogButtonBox(EditVerseDialog)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.ButtonBox.setObjectName(u'ButtonBox')
        self.DialogLayout.addWidget(self.ButtonBox)
        self.retranslateUi(EditVerseDialog)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL(u'accepted()'), EditVerseDialog.accept)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL(u'rejected()'), EditVerseDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditVerseDialog)
        self.VerseTextEdit.setFocus(QtCore.Qt.OtherFocusReason)

    def retranslateUi(self, EditVerseDialog):
        EditVerseDialog.setWindowTitle(self.trUtf8('Edit Verse'))
