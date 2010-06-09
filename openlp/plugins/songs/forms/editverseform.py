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

import re
import logging

from PyQt4 import QtCore, QtGui

from openlp.plugins.songs.forms import VerseType

from editversedialog import Ui_EditVerseDialog

log = logging.getLogger(__name__)

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
        QtCore.QObject.connect(
            self.InsertButton,
            QtCore.SIGNAL(u'clicked()'),
            self.onInsertButtonClicked
        )
        QtCore.QObject.connect(
            self.VerseTextEdit,
            QtCore.SIGNAL(u'cursorPositionChanged()'),
            self.onCursorPositionChanged
        )
        self.verse_regex = re.compile(r'---\[([-\w]+):([\d]+)\]---')

    def insertVerse(self, title, num=1):
        if self.VerseTextEdit.textCursor().columnNumber() != 0:
            self.VerseTextEdit.insertPlainText(u'\n')
        self.VerseTextEdit.insertPlainText(u'---[%s:%s]---\n' % (title, num))
        self.VerseTextEdit.setFocus()

    def onInsertButtonClicked(self):
        if self.VerseTextEdit.textCursor().columnNumber() != 0:
            self.VerseTextEdit.insertPlainText(u'\n')
        verse_type = self.VerseTypeComboBox.currentIndex()
        if verse_type == VerseType.Verse:
            self.insertVerse(VerseType.to_string(VerseType.Verse),
                self.VerseNumberBox.value())
        elif verse_type == VerseType.Chorus:
            self.insertVerse(VerseType.to_string(VerseType.Chorus),
                self.VerseNumberBox.value())
        elif verse_type == VerseType.Bridge:
            self.insertVerse(VerseType.to_string(VerseType.Bridge))
        elif verse_type == VerseType.PreChorus:
            self.insertVerse(VerseType.to_string(VerseType.PreChorus))
        elif verse_type == VerseType.Intro:
            self.insertVerse(VerseType.to_string(VerseType.Intro))
        elif verse_type == VerseType.Ending:
            self.insertVerse(VerseType.to_string(VerseType.Ending))
        elif verse_type == VerseType.Other:
            self.insertVerse(VerseType.to_string(VerseType.Other))

    def onCursorPositionChanged(self):
        position = self.VerseTextEdit.textCursor().position()
        text = unicode(self.VerseTextEdit.toPlainText())
        if not text:
            return
        if text.rfind(u'[', 0, position) > text.rfind(u']', 0, position) and \
           text.find(u']', position) < text.find(u'[', position):
            return
        position = text.rfind(u'---[', 0, position)
        if position == -1:
            return
        text = text[position:]
        position = text.find(u']---')
        if position == -1:
            return
        text = text[:position + 4]
        match = self.verse_regex.match(text)
        if match:
            verse_type = match.group(1)
            verse_number = int(match.group(2))
            verse_type_index = VerseType.from_string(verse_type)
            if verse_type_index >= 0:
                self.VerseTypeComboBox.setCurrentIndex(verse_type_index)
                self.VerseNumberBox.setValue(verse_number)

    def setVerse(self, text, single=False,
        tag=u'%s:1' % VerseType.to_string(VerseType.Verse)):
        if single:
            verse_type, verse_number = tag.split(u':')
            self.VerseTypeComboBox.setCurrentIndex(
                VerseType.from_string(verse_type))
            self.VerseNumberBox.setValue(int(verse_number))
            self.InsertButton.setVisible(False)
        else:
            if not text:
                text = u'---[%s:1]---\n' % VerseType.to_string(VerseType.Verse)
            self.VerseTypeComboBox.setCurrentIndex(0)
            self.VerseNumberBox.setValue(1)
            self.InsertButton.setVisible(True)
        self.VerseTextEdit.setPlainText(text)
        self.VerseTextEdit.setFocus(QtCore.Qt.OtherFocusReason)
        self.VerseTextEdit.moveCursor(QtGui.QTextCursor.End)

    def getVerse(self):
        return self.VerseTextEdit.toPlainText(), \
            VerseType.to_string(self.VerseTypeComboBox.currentIndex()), \
            unicode(self.VerseNumberBox.value())

    def getVerseAll(self):
        text = self.VerseTextEdit.toPlainText()
        if not text.startsWith(u'---['):
            text = u'---[%s:1]---\n%s' % (VerseType.to_string(VerseType.Verse),
                text)
        return text

