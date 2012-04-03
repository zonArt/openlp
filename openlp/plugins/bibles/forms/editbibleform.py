# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

import logging
import re

from PyQt4 import QtGui

from openlp.core.lib import Receiver, translate
from openlp.core.lib.ui import UiStrings, critical_error_message_box
from editbibledialog import Ui_EditBibleDialog
from openlp.plugins.bibles.lib import BibleStrings
from openlp.plugins.bibles.lib.db import BiblesResourcesDB

log = logging.getLogger(__name__)

class EditBibleForm(QtGui.QDialog, Ui_EditBibleDialog):
    """
    Class to manage the editing of a bible
    """
    log.info(u'%s EditBibleForm loaded', __name__)

    def __init__(self, mediaitem, parent, manager):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.mediaitem = mediaitem
        self.validate_error = []
        self.booknames = BibleStrings().Booknames
        # can this be automated?
        self.width = 400
        self.setupUi(self)
        self.manager = manager

    def loadBible(self, bible):
        """
        Loads a bible.

        ``bible``
            The name of the bible.
        """
        log.debug(u'Load Bible')
        self.bible = bible
        self.versionNameEdit.setText(
            self.manager.get_meta_data(self.bible, u'Version').value)
        self.copyrightEdit.setText(
            self.manager.get_meta_data(self.bible, u'Copyright').value)
        self.permissionsEdit.setText(
            self.manager.get_meta_data(self.bible, u'Permissions').value)
        self.bookname_language = self.manager.get_meta_data(
            self.bible, u'Bookname language')
        if self.bookname_language:
            self.languageSelectionComboBox.setCurrentIndex(
                int(self.bookname_language.value)+1)
        self.books = {}
        self.webbible = self.manager.get_meta_data(self.bible,
            u'download source')
        if self.webbible:
            self.bookNameNotice.setText(translate('BiblesPlugin.EditBibleForm',
                'This is a webbible.\nIt is not possible to customize the Book '
                'Names.'))
            self.bookNameTabLayout.removeWidget(self.scrollArea)
            self.scrollArea.setParent(None)
        else:
            self.bookNameNotice.setText(translate('BiblesPlugin.EditBibleForm',
                'To use the customized Book Names, choose the option "Bible '
                'language"\nin general settings or explicit for this Bible.'))
            for book in BiblesResourcesDB.get_books():
                self.books[book[u'abbreviation']] = self.manager.get_book_by_id(
                    self.bible, book[u'id'])
                if self.books[book[u'abbreviation']] and not self.webbible:
                    self.bookNameEdit[book[u'abbreviation']].setText(
                        self.books[book[u'abbreviation']].name)
                else:
                    self.bookNameGroupBoxLayout.removeWidget(
                        self.bookNameLabel[book[u'abbreviation']])
                    self.bookNameLabel[book[u'abbreviation']].setParent(None)
                    self.bookNameGroupBoxLayout.removeWidget(
                        self.bookNameEdit[book[u'abbreviation']])
                    self.bookNameEdit[book[u'abbreviation']].setParent(None)

    def reject(self):
        """
        Exit Dialog and do not save
        """
        log.debug (u'BibleEditForm.reject')
        self.bible = None
        QtGui.QDialog.reject(self)

    def accept(self):
        """
        Exit Dialog and save data
        """
        log.debug(u'BibleEditForm.accept')
        save = True
        self.version = unicode(self.versionNameEdit.text())
        self.copyright = unicode(self.copyrightEdit.text())
        self.permissions = unicode(self.permissionsEdit.text())
        self.bookname_language = \
            self.languageSelectionComboBox.currentIndex()-1
        for error in self.validate_error:
            self.changeBackgroundColor(error, 'white')
        if not self.validateMeta():
            save = False
        if not self.webbible and save:
            custom_names = {}
            for abbr, book in self.books.iteritems():
                if book:
                    custom_names[abbr] = unicode(self.bookNameEdit[abbr].text())
                    if book.name != custom_names[abbr]:
                        if not self.validateBook(custom_names[abbr], abbr):
                            save = False
                            break
        if save:
            Receiver.send_message(u'openlp_process_events')
            Receiver.send_message(u'cursor_busy')
            self.manager.save_meta_data(self.bible, self.version,
                self.copyright, self.permissions, self.bookname_language)
            if not self.webbible:
                for abbr, book in self.books.iteritems():
                    if book:
                        if book.name != custom_names[abbr]:
                            book.name = custom_names[abbr]
                            self.manager.update_book(self.bible, book)
            self.bible = None
            Receiver.send_message(u'cursor_normal')
            QtGui.QDialog.accept(self)

    def validateMeta(self):
        """
        Validate the Meta before saving.
        """
        if not self.version:
            self.changeBackgroundColor(self.versionNameEdit, 'red')
            self.validate_error = [self.versionNameEdit]
            self.versionNameEdit.setFocus()
            critical_error_message_box(UiStrings().EmptyField,
                translate('BiblesPlugin.BibleEditForm',
                'You need to specify a version name for your Bible.'))
            return False
        elif not self.copyright:
            self.changeBackgroundColor(self.copyrightEdit, 'red')
            self.validate_error = [self.copyrightEdit]
            self.copyrightEdit.setFocus()
            critical_error_message_box(UiStrings().EmptyField,
                translate('BiblesPlugin.BibleEditForm',
                'You need to set a copyright for your Bible. '
                'Bibles in the Public Domain need to be marked as such.'))
            return False
        elif self.manager.exists(self.version) and \
            self.manager.get_meta_data(self.bible, u'Version').value != \
            self.version:
            self.changeBackgroundColor(self.versionNameEdit, 'red')
            self.validate_error = [self.versionNameEdit]
            self.versionNameEdit.setFocus()
            critical_error_message_box(
                translate('BiblesPlugin.BibleEditForm', 'Bible Exists'),
                translate('BiblesPlugin.BibleEditForm',
                'This Bible already exists. Please import '
                'a different Bible or first delete the existing one.'))
            return False
        return True

    def validateBook(self, new_bookname, abbreviation):
        """
        Validate a book.
        """
        book_regex = re.compile(u'[\d]*[^\d]+$')
        if not new_bookname:
            self.changeBackgroundColor(self.bookNameEdit[abbreviation], 'red')
            self.validate_error = [self.bookNameEdit[abbreviation]]
            self.bookNameEdit[abbreviation].setFocus()
            critical_error_message_box(UiStrings().EmptyField,
                unicode(translate('BiblesPlugin.BibleEditForm',
                'You need to specify a book name for "%s".')) %
                self.booknames[abbreviation])
            return False
        elif not book_regex.match(new_bookname):
            self.changeBackgroundColor(self.bookNameEdit[abbreviation], 'red')
            self.validate_error = [self.bookNameEdit[abbreviation]]
            self.bookNameEdit[abbreviation].setFocus()
            critical_error_message_box(UiStrings().EmptyField,
                unicode(translate('BiblesPlugin.BibleEditForm',
                'The book name "%s" is not correct.\nDecimal digits only could '
                'be used at the beginning and\nmust be followed by one or more '
                'non-digit characters')) % new_bookname)
            return False
        for abbr, book in self.books.iteritems():
            if book:
                if abbr == abbreviation:
                    continue
                if unicode(self.bookNameEdit[abbr].text()) == new_bookname:
                    self.changeBackgroundColor(self.bookNameEdit[abbreviation],
                        'red')
                    self.bookNameEdit[abbreviation].setFocus()
                    self.changeBackgroundColor(self.bookNameEdit[abbr], 'red')
                    self.validate_error = [self.bookNameEdit[abbr],
                        self.bookNameEdit[abbreviation]]
                    critical_error_message_box(
                        translate('BiblesPlugin.BibleEditForm',
                        'Book Name Exists Twice'),
                        unicode(translate('BiblesPlugin.BibleEditForm',
                        'The Book Name "%s" exists twice. Please change one.'))
                        % new_bookname)
                    return False
        return True

    def changeBackgroundColor(self, lineedit, color):
        """
        Change the Background Color of the given LineEdit
        """
        pal = QtGui.QPalette(lineedit.palette())
        pal.setColor(QtGui.QPalette.Base,QtGui.QColor(color))
        lineedit.setPalette(pal)
