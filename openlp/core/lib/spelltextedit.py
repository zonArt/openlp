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
"""
The :mod:`~openlp.core.lib.spelltextedit` module contains a classes to add spell checking to an edit widget.
"""

import logging
import re

try:
    import enchant
    from enchant import DictNotFoundError
    from enchant.errors import Error
    ENCHANT_AVAILABLE = True
except ImportError:
    ENCHANT_AVAILABLE = False

# based on code from
# http://john.nachtimwald.com/2009/08/22/qplaintextedit-with-in-line-spell-check

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, FormattingTags
from openlp.core.lib.ui import create_action

log = logging.getLogger(__name__)


class SpellTextEdit(QtGui.QPlainTextEdit):
    """
    Spell checking widget based on QPlanTextEdit.
    """
    def __init__(self, parent=None, formattingTagsAllowed=True):
        """
        Constructor.
        """
        global ENCHANT_AVAILABLE
        QtGui.QPlainTextEdit.__init__(self, parent)
        self.formattingTagsAllowed = formattingTagsAllowed
        # Default dictionary based on the current locale.
        if ENCHANT_AVAILABLE:
            try:
                self.dictionary = enchant.Dict()
                self.highlighter = Highlighter(self.document())
                self.highlighter.spellingDictionary = self.dictionary
            except (Error, DictNotFoundError):
                ENCHANT_AVAILABLE = False
                log.debug(u'Could not load default dictionary')

    def mousePressEvent(self, event):
        """
        Handle mouse clicks within the text edit region.
        """
        if event.button() == QtCore.Qt.RightButton:
            # Rewrite the mouse event to a left button event so the cursor is
            # moved to the location of the pointer.
            event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress,
                event.pos(), QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtGui.QPlainTextEdit.mousePressEvent(self, event)

    def contextMenuEvent(self, event):
        """
        Provide the context menu for the text edit region.
        """
        popupMenu = self.createStandardContextMenu()
        # Select the word under the cursor.
        cursor = self.textCursor()
        # only select text if not already selected
        if not cursor.hasSelection():
            cursor.select(QtGui.QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)
        # Add menu with available languages.
        if ENCHANT_AVAILABLE:
            lang_menu = QtGui.QMenu(
                translate('OpenLP.SpellTextEdit', 'Language:'))
            for lang in enchant.list_languages():
                action = create_action(lang_menu, lang, text=lang, checked=lang == self.dictionary.tag)
                lang_menu.addAction(action)
            popupMenu.insertSeparator(popupMenu.actions()[0])
            popupMenu.insertMenu(popupMenu.actions()[0], lang_menu)
            QtCore.QObject.connect(lang_menu, QtCore.SIGNAL(u'triggered(QAction*)'), self.setLanguage)
        # Check if the selected word is misspelled and offer spelling
        # suggestions if it is.
        if ENCHANT_AVAILABLE and self.textCursor().hasSelection():
            text = self.textCursor().selectedText()
            if not self.dictionary.check(text):
                spell_menu = QtGui.QMenu(translate('OpenLP.SpellTextEdit', 'Spelling Suggestions'))
                for word in self.dictionary.suggest(text):
                    action = SpellAction(word, spell_menu)
                    action.correct.connect(self.correctWord)
                    spell_menu.addAction(action)
                # Only add the spelling suggests to the menu if there are
                # suggestions.
                if spell_menu.actions():
                    popupMenu.insertMenu(popupMenu.actions()[0], spell_menu)
        tagMenu = QtGui.QMenu(translate('OpenLP.SpellTextEdit', 'Formatting Tags'))
        if self.formattingTagsAllowed:
            for html in FormattingTags.get_html_tags():
                action = SpellAction(html[u'desc'], tagMenu)
                action.correct.connect(self.htmlTag)
                tagMenu.addAction(action)
            popupMenu.insertSeparator(popupMenu.actions()[0])
            popupMenu.insertMenu(popupMenu.actions()[0], tagMenu)
        popupMenu.exec_(event.globalPos())

    def setLanguage(self, action):
        """
        Changes the language for this spelltextedit.

        ``action``
            The action.
        """
        self.dictionary = enchant.Dict(action.text())
        self.highlighter.spellingDictionary = self.dictionary
        self.highlighter.highlightBlock(self.toPlainText())
        self.highlighter.rehighlight()

    def correctWord(self, word):
        """
        Replaces the selected text with word.
        """
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.insertText(word)
        cursor.endEditBlock()

    def htmlTag(self, tag):
        """
        Replaces the selected text with word.
        """
        for html in FormattingTags.get_html_tags():
            if tag == html[u'desc']:
                cursor = self.textCursor()
                if self.textCursor().hasSelection():
                    text = cursor.selectedText()
                    cursor.beginEditBlock()
                    cursor.removeSelectedText()
                    cursor.insertText(html[u'start tag'])
                    cursor.insertText(text)
                    cursor.insertText(html[u'end tag'])
                    cursor.endEditBlock()
                else:
                    cursor = self.textCursor()
                    cursor.insertText(html[u'start tag'])
                    cursor.insertText(html[u'end tag'])


class Highlighter(QtGui.QSyntaxHighlighter):
    """
    Provides a text highlighter for pointing out spelling errors in text.
    """
    WORDS = u'(?iu)[\w\']+'

    def __init__(self, *args):
        """
        Constructor
        """
        QtGui.QSyntaxHighlighter.__init__(self, *args)
        self.spellingDictionary = None

    def highlightBlock(self, text):
        """
        Highlight misspelt words in a block of text
        """
        if not self.spellingDictionary:
            return
        text = unicode(text)
        charFormat = QtGui.QTextCharFormat()
        charFormat.setUnderlineColor(QtCore.Qt.red)
        charFormat.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)
        for word_object in re.finditer(self.WORDS, text):
            if not self.spellingDictionary.check(word_object.group()):
                self.setFormat(word_object.start(),
                    word_object.end() - word_object.start(), charFormat)


class SpellAction(QtGui.QAction):
    """
    A special QAction that returns the text in a signal.
    """
    correct = QtCore.pyqtSignal(unicode)

    def __init__(self, *args):
        """
        Constructor
        """
        QtGui.QAction.__init__(self, *args)
        self.triggered.connect(lambda x: self.correct.emit(self.text()))
