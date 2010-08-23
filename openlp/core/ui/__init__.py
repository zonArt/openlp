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
# You should have received a copy of the GNU General Pu__init__.pyblic License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
The :mod:`ui` module provides the core user interface for OpenLP
"""

# http://john.nachtimwald.com/2009/08/22/qplaintextedit-with-in-line-spell-check/

import re
import sys
try:
    import enchant
    enchant_available = True
except ImportError:
    enchant_available = False

from PyQt4 import QtCore, QtGui
from openlp.core.lib import html_expands, translate, context_menu_action

class SpellTextEdit(QtGui.QPlainTextEdit):

    def __init__(self, *args):
        QtGui.QPlainTextEdit.__init__(self, *args)
        # Default dictionary based on the current locale.
        if enchant_available:
            self.dict = enchant.Dict()
            self.highlighter = Highlighter(self.document())
            self.highlighter.setDict(self.dict)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            # Rewrite the mouse event to a left button event so the cursor is
            # moved to the location of the pointer.
            event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress, event.pos(),
                QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtGui.QPlainTextEdit.mousePressEvent(self, event)

    def contextMenuEvent(self, event):
        popup_menu = self.createStandardContextMenu()

        # Select the word under the cursor.
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)

        # Check if the selected word is misspelled and offer spelling
        # suggestions if it is.
        if enchant_available and self.textCursor().hasSelection():
            text = unicode(self.textCursor().selectedText())
            if not self.dict.check(text):
                spell_menu = QtGui.QMenu(translate('OpenLP.SpellTextEdit',
                    'Spelling Suggestions'))
                for word in self.dict.suggest(text):
                    action = SpellAction(word, spell_menu)
                    action.correct.connect(self.correctWord)
                    spell_menu.addAction(action)
                # Only add the spelling suggests to the menu if there are
                # suggestions.
                if len(spell_menu.actions()) != 0:
                    popup_menu.insertSeparator(popup_menu.actions()[0])
                    popup_menu.insertMenu(popup_menu.actions()[0], spell_menu)
        tag_menu = QtGui.QMenu(translate('OpenLP.SpellTextEdit',
            'Formatting Tags'))
        for html in html_expands:
            action = SpellAction( html[u'desc'], tag_menu)
            action.correct.connect(self.htmlTag)
            tag_menu.addAction(action)
        popup_menu.insertSeparator(popup_menu.actions()[0])
        popup_menu.insertMenu(popup_menu.actions()[0], tag_menu)

        popup_menu.exec_(event.globalPos())

    def correctWord(self, word):
        '''
        Replaces the selected text with word.
        '''
        cursor = self.textCursor()
        cursor.beginEditBlock()

        cursor.removeSelectedText()
        cursor.insertText(word)

        cursor.endEditBlock()

    def htmlTag(self, tag):
        '''
        Replaces the selected text with word.
        '''
        for html in html_expands:
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

    WORDS = u'(?iu)[\w\']+'

    def __init__(self, *args):
        QtGui.QSyntaxHighlighter.__init__(self, *args)

        self.dict = None

    def setDict(self, dict):
        self.dict = dict

    def highlightBlock(self, text):
        if not self.dict:
            return

        text = unicode(text)

        format = QtGui.QTextCharFormat()
        format.setUnderlineColor(QtCore.Qt.red)
        format.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)

        for word_object in re.finditer(self.WORDS, text):
            if not self.dict.check(word_object.group()):
                self.setFormat(word_object.start(),
                    word_object.end() - word_object.start(), format)

class SpellAction(QtGui.QAction):
    '''
    A special QAction that returns the text in a signal.
    '''
    correct = QtCore.pyqtSignal(unicode)

    def __init__(self, *args):
        QtGui.QAction.__init__(self, *args)

        self.triggered.connect(lambda x: self.correct.emit(
            unicode(self.text())))

class HideMode(object):
    """
    This is basically an enumeration class which specifies the mode of a Bible.
    Mode refers to whether or not a Bible in OpenLP is a full Bible or needs to
    be downloaded from the Internet on an as-needed basis.
    """
    Blank = 1
    Theme = 2
    Screen = 3

from maindisplay import MainDisplay
from slidecontroller import HideMode
from servicenoteform import ServiceNoteForm
from serviceitemeditform import ServiceItemEditForm
from screen import ScreenList
from amendthemeform import AmendThemeForm
from slidecontroller import SlideController
from splashscreen import SplashScreen
from generaltab import GeneralTab
from themestab import ThemesTab
from advancedtab import AdvancedTab
from aboutform import AboutForm
from pluginform import PluginForm
from settingsform import SettingsForm
from mediadockmanager import MediaDockManager
from servicemanager import ServiceManager
from thememanager import ThemeManager

__all__ = ['SplashScreen', 'AboutForm', 'SettingsForm',
    'MainDisplay', 'SlideController', 'ServiceManager', 'ThemeManager',
    'AmendThemeForm', 'MediaDockManager', 'ServiceItemEditForm']
