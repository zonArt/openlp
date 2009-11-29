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
from editversedialog import Ui_EditVerseDialog

class EditVerseForm(QtGui.QDialog, Ui_EditVerseDialog):
    """
    This is the form that is used to edit the verses of the song.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.addVerse,
            QtCore.SIGNAL(u'clicked()'), self.onAddVerse)
        QtCore.QObject.connect(self.addChorus,
            QtCore.SIGNAL(u'clicked()'), self.onAddChorus)
        QtCore.QObject.connect(self.addBridge,
            QtCore.SIGNAL(u'clicked()'), self.onAddBridge)

    def onAddBridge(self):
        self.VerseTextEdit.insertPlainText(u'---[Bridge:1]---\n')

    def onAddChorus(self):
        self.VerseTextEdit.insertPlainText(u'---[Chorus:1]---\n')

    def onAddVerse(self):
        self.VerseTextEdit.insertPlainText(u'---[Verse:1]---\n')

    def setVerse(self, text, single=False, tag=0):
        posVerse = 0
        posSub = 0
        if single:
            id = tag.split(u':')
            posVerse = self.VerseListComboBox.findText(id[0], QtCore.Qt.MatchExactly)
            posSub = self.SubVerseListComboBox.findText(id[1], QtCore.Qt.MatchExactly)
            if posVerse == -1:
                posVerse = 0
            if posSub == -1:
                posSub = 0
            self.VerseListComboBox.setEnabled(True)
            self.SubVerseListComboBox.setEnabled(True)
            self.addBridge.setEnabled(False)
            self.addChorus.setEnabled(False)
            self.addVerse.setEnabled(False)
        else:
            self.VerseListComboBox.setEnabled(False)
            self.SubVerseListComboBox.setEnabled(False)
            self.addBridge.setEnabled(True)
            self.addChorus.setEnabled(True)
            self.addVerse.setEnabled(True)
        self.VerseListComboBox.setCurrentIndex(posVerse)
        self.SubVerseListComboBox.setCurrentIndex(posSub)
        self.VerseTextEdit.setPlainText(text)
        self.VerseTextEdit.setFocus(QtCore.Qt.OtherFocusReason)

    def getVerse(self):
       return self.VerseTextEdit.toPlainText(), \
            unicode(self.VerseListComboBox.currentText()), \
            unicode(self.SubVerseListComboBox.currentText())

    def getVerseAll(self):
       return self.VerseTextEdit.toPlainText()
