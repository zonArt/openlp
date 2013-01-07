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
Module implementing BookNameForm.
"""
import logging
import re

from PyQt4.QtGui import QDialog
from PyQt4 import QtCore

from openlp.core.lib import translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.plugins.bibles.forms.booknamedialog import Ui_BookNameDialog
from openlp.plugins.bibles.lib import BibleStrings
from openlp.plugins.bibles.lib.db import BiblesResourcesDB

log = logging.getLogger(__name__)

class BookNameForm(QDialog, Ui_BookNameDialog):
    """
    Class to manage a dialog which help the user to refer a book name a
    to a english book name
    """
    log.info(u'BookNameForm loaded')

    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.customSignals()
        self.book_names = BibleStrings().BookNames
        self.book_id = False

    def customSignals(self):
        """
        Set up the signals used in the booknameform.
        """
        QtCore.QObject.connect(self.oldTestamentCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onCheckBoxIndexChanged)
        QtCore.QObject.connect(self.newTestamentCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onCheckBoxIndexChanged)
        QtCore.QObject.connect(self.apocryphaCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onCheckBoxIndexChanged)

    def onCheckBoxIndexChanged(self, index):
        """
        Reload Combobox if CheckBox state has changed
        """
        self.reloadComboBox()

    def reloadComboBox(self):
        """
        Reload the Combobox items
        """
        self.correspondingComboBox.clear()
        items = BiblesResourcesDB.get_books()
        for item in items:
            addBook = True
            for book in self.books:
                if book.book_reference_id == item[u'id']:
                    addBook = False
                    break
            if self.oldTestamentCheckBox.checkState() == QtCore.Qt.Unchecked and item[u'testament_id'] == 1:
                addBook = False
            elif self.newTestamentCheckBox.checkState() == QtCore.Qt.Unchecked and item[u'testament_id'] == 2:
                addBook = False
            elif self.apocryphaCheckBox.checkState() == QtCore.Qt.Unchecked and item[u'testament_id'] == 3:
                addBook = False
            if addBook:
                self.correspondingComboBox.addItem(self.book_names[item[u'abbreviation']])

    def exec_(self, name, books, maxbooks):
        self.books = books
        log.debug(maxbooks)
        if maxbooks <= 27:
            self.oldTestamentCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.apocryphaCheckBox.setCheckState(QtCore.Qt.Unchecked)
        elif maxbooks <= 66:
            self.apocryphaCheckBox.setCheckState(QtCore.Qt.Unchecked)
        self.reloadComboBox()
        self.currentBookLabel.setText(unicode(name))
        self.correspondingComboBox.setFocus()
        return QDialog.exec_(self)

    def accept(self):
        if self.correspondingComboBox.currentText() == u'':
            critical_error_message_box(message=translate('BiblesPlugin.BookNameForm', 'You need to select a book.'))
            self.correspondingComboBox.setFocus()
            return False
        else:
            cor_book = self.correspondingComboBox.currentText()
            for character in u'\\.^$*+?{}[]()':
                cor_book = cor_book.replace(character, u'\\' + character)
            books = filter(lambda key:
                re.match(cor_book, unicode(self.book_names[key]), re.UNICODE), self.book_names.keys())
            books = filter(None, map(BiblesResourcesDB.get_book, books))
            if books:
                self.book_id = books[0][u'id']
            return QDialog.accept(self)
