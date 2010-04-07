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
        QtCore.QObject.connect(self.addIntro,
            QtCore.SIGNAL(u'clicked()'), self.onAddIntro)
        QtCore.QObject.connect(self.addOther,
            QtCore.SIGNAL(u'clicked()'), self.onAddOther)
        QtCore.QObject.connect(self.addPreChorus,
            QtCore.SIGNAL(u'clicked()'), self.onAddPreChorus)
        QtCore.QObject.connect(self.addEnding,
            QtCore.SIGNAL(u'clicked()'), self.onAddEnding)
        QtCore.QObject.connect(self.VerseListComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onVerseComboChanged)

    def startNewLine(self):
        if self.VerseTextEdit.textCursor().columnNumber() != 0:
            self.VerseTextEdit.insertPlainText(u'\n')

    def onAddIntro(self):
        self.startNewLine()
        self.VerseTextEdit.insertPlainText(u'---[Intro:1]---\n')
        self.VerseTextEdit.setFocus()

    def onAddEnding(self):
        self.startNewLine()
        self.VerseTextEdit.insertPlainText(u'---[Ending:1]---\n')
        self.VerseTextEdit.setFocus()

    def onAddOther(self):
        self.startNewLine()
        self.VerseTextEdit.insertPlainText(u'---[Other:1]---\n')
        self.VerseTextEdit.setFocus()

    def onAddPreChorus(self):
        self.startNewLine()
        self.VerseTextEdit.insertPlainText(u'---[Pre-Chorus:1]---\n')
        self.VerseTextEdit.setFocus()

    def onAddBridge(self):
        self.startNewLine()
        self.VerseTextEdit.insertPlainText(u'---[Bridge:1]---\n')
        self.VerseTextEdit.setFocus()

    def onAddChorus(self):
        self.startNewLine()
        count = self.VerseTextEdit.toPlainText().\
                        count(u'---[Chorus')
        self.VerseTextEdit.insertPlainText(u'---[Chorus:%s]---\n'
                                           % unicode(count + 1))
        self.VerseTextEdit.setFocus()

    def onAddVerse(self):
        self.startNewLine()
        count = self.VerseTextEdit.toPlainText().\
                        count(u'---[Verse')
        self.VerseTextEdit.insertPlainText(u'---[Verse:%s]---\n'
                                           % unicode(count + 1))
        self.VerseTextEdit.setFocus()

    def setVerse(self, text, verseCount=0, single=False, tag=u'Verse:1'):
        posVerse = 0
        posSub = 0
        if len(text) == 0 and not single:
            text = u'---[%s:1]---\n' % self.trUtf8('Verse')
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
            self.SubVerseListComboBox.clear()
            for i in range(1, verseCount + 1):
                self.SubVerseListComboBox.addItem(u'%s'% i)
            self.addBridge.setEnabled(False)
            self.addChorus.setEnabled(False)
            self.addVerse.setEnabled(False)
            self.addIntro.setEnabled(False)
            self.addPreChorus.setEnabled(False)
            self.addOther.setEnabled(False)
            self.addEnding.setEnabled(False)
        else:
            self.VerseListComboBox.setEnabled(False)
            self.SubVerseListComboBox.setEnabled(False)
            self.addBridge.setEnabled(True)
            self.addChorus.setEnabled(True)
            self.addVerse.setEnabled(True)
            self.addIntro.setEnabled(True)
            self.addPreChorus.setEnabled(True)
            self.addOther.setEnabled(True)
            self.addEnding.setEnabled(True)
        self.VerseListComboBox.setCurrentIndex(posVerse)
        self.SubVerseListComboBox.setCurrentIndex(posSub)
        self.VerseTextEdit.setPlainText(text)
        self.VerseTextEdit.setFocus(QtCore.Qt.OtherFocusReason)
        self.onVerseComboChanged(0)
        self.VerseTextEdit.moveCursor(QtGui.QTextCursor.Down)

    def getVerse(self):
       return self.VerseTextEdit.toPlainText(), \
            unicode(self.VerseListComboBox.currentText()), \
            unicode(self.SubVerseListComboBox.currentText())

    def getVerseAll(self):
        text = self.VerseTextEdit.toPlainText()
        if not text.startsWith(u'---['):
            text = u'---[%s:1]---\n%s' % (self.trUtf8('Verse'),  text)
        return text

    def onVerseComboChanged(self, id):
        if unicode(self.VerseListComboBox.currentText()) == self.trUtf8('Verse') or \
            unicode(self.VerseListComboBox.currentText()) == self.trUtf8('Chrous'):
            self.SubVerseListComboBox.setEnabled(True)
        else:
            self.SubVerseListComboBox.setEnabled(False)
            self.SubVerseListComboBox.setCurrentIndex(0)
