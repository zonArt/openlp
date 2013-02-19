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

import re
import logging

from PyQt4 import QtCore, QtGui

from openlp.plugins.songs.lib import VerseType

from editversedialog import Ui_EditVerseDialog

log = logging.getLogger(__name__)

VERSE_REGEX = re.compile(r'---\[(.+):\D*(\d*)\D*.*\]---')

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
        QtCore.QObject.connect(self.verseTextEdit, QtCore.SIGNAL('customContextMenuRequested(QPoint)'),
            self.contextMenu)
        QtCore.QObject.connect(self.insertButton, QtCore.SIGNAL(u'clicked()'), self.onInsertButtonClicked)
        QtCore.QObject.connect(self.splitButton, QtCore.SIGNAL(u'clicked()'), self.onSplitButtonClicked)
        QtCore.QObject.connect(self.verseTextEdit, QtCore.SIGNAL(u'cursorPositionChanged()'),
            self.onCursorPositionChanged)
        QtCore.QObject.connect(self.verseTypeComboBox, QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onVerseTypeComboBoxChanged)

    def contextMenu(self, point):
        item = self.serviceManagerList.itemAt(point)

    def insertVerse(self, verse_tag, verse_num=1):
        if self.verseTextEdit.textCursor().columnNumber() != 0:
            self.verseTextEdit.insertPlainText(u'\n')
        verse_tag = VerseType.translated_name(verse_tag)
        self.verseTextEdit.insertPlainText(u'---[%s:%s]---\n' % (verse_tag, verse_num))
        self.verseTextEdit.setFocus()

    def onSplitButtonClicked(self):
        text = self.verseTextEdit.toPlainText()
        position = self.verseTextEdit.textCursor().position()
        insert_string = u'[---]'
        if position and text[position-1] != u'\n':
             insert_string = u'\n' + insert_string
        if position ==  len(text) or text[position] != u'\n':
             insert_string += u'\n'
        self.verseTextEdit.insertPlainText(insert_string)
        self.verseTextEdit.setFocus()

    def onInsertButtonClicked(self):
        verse_type_index = self.verseTypeComboBox.currentIndex()
        self.insertVerse(VerseType.Tags[verse_type_index],
            self.verseNumberBox.value())

    def onVerseTypeComboBoxChanged(self):
        self.updateSuggestedVerseNumber()

    def onCursorPositionChanged(self):
        self.updateSuggestedVerseNumber()

    def updateSuggestedVerseNumber(self):
        """
        Adjusts the verse number SpinBox in regard to the selected verse type
        and the cursor's position.
        """
        position = self.verseTextEdit.textCursor().position()
        text = self.verseTextEdit.toPlainText()
        verse_name = VerseType.TranslatedNames[
            self.verseTypeComboBox.currentIndex()]
        if not text:
            return
        position = text.rfind(u'---[%s' % verse_name, 0, position)
        if position == -1:
            self.verseNumberBox.setValue(1)
            return
        text = text[position:]
        position = text.find(u']---')
        if position == -1:
            return
        text = text[:position + 4]
        match = VERSE_REGEX.match(text)
        if match:
            verse_tag = match.group(1)
            try:
                verse_num = int(match.group(2)) + 1
            except ValueError:
                verse_num = 1
            self.verseNumberBox.setValue(verse_num)

    def setVerse(self, text, single=False,
        tag=u'%s1' % VerseType.Tags[VerseType.Verse]):
        self.hasSingleVerse = single
        if single:
            verse_type_index = VerseType.from_tag(tag[0], None)
            verse_number = tag[1:]
            if verse_type_index is not None:
                self.verseTypeComboBox.setCurrentIndex(verse_type_index)
            self.verseNumberBox.setValue(int(verse_number))
            self.insertButton.setVisible(False)
        else:
            if not text:
                text = u'---[%s:1]---\n' % VerseType.TranslatedNames[VerseType.Verse]
            self.verseTypeComboBox.setCurrentIndex(0)
            self.verseNumberBox.setValue(1)
            self.insertButton.setVisible(True)
        self.verseTextEdit.setPlainText(text)
        self.verseTextEdit.setFocus()
        self.verseTextEdit.moveCursor(QtGui.QTextCursor.End)

    def getVerse(self):
        return self.verseTextEdit.toPlainText(), VerseType.Tags[self.verseTypeComboBox.currentIndex()], \
            unicode(self.verseNumberBox.value())

    def getVerseAll(self):
        text = self.verseTextEdit.toPlainText()
        if not text.startswith(u'---['):
            text = u'---[%s:1]---\n%s' % (VerseType.TranslatedNames[VerseType.Verse], text)
        return text

