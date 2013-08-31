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

import logging
import os
import re

from PyQt4 import QtGui

from openlp.core.lib import Registry, UiStrings, translate
from openlp.core.lib.ui import critical_error_message_box
from .editbibledialog import Ui_EditBibleDialog
from openlp.plugins.bibles.lib import BibleStrings
from openlp.plugins.bibles.lib.db import BiblesResourcesDB

log = logging.getLogger(__name__)

class EditBibleForm(QtGui.QDialog, Ui_EditBibleDialog):
    """
    Class to manage the editing of a bible
    """
    log.info('%s EditBibleForm loaded', __name__)

    def __init__(self, media_item, parent, manager):
        """
        Constructor
        """
        super(EditBibleForm, self).__init__(parent)
        self.media_item = media_item
        self.book_names = BibleStrings().BookNames
        self.setupUi(self)
        self.manager = manager

    def loadBible(self, bible):
        """
        Loads a bible.

        ``bible``
            The name of the bible.
        """
        log.debug('Load Bible')
        self.bible = bible
        self.version_name_edit.setText(self.manager.get_meta_data(self.bible, 'name').value)
        self.copyright_edit.setText(self.manager.get_meta_data(self.bible, 'copyright').value)
        self.permissions_edit.setText(self.manager.get_meta_data(self.bible, 'permissions').value)
        book_name_language = self.manager.get_meta_data(self.bible, 'book_name_language')
        if book_name_language and book_name_language.value != 'None':
            self.language_selection_combo_box.setCurrentIndex(int(book_name_language.value) + 1)
        self.books = {}
        self.webbible = self.manager.get_meta_data(self.bible, 'download_source')
        if self.webbible:
            self.book_name_notice.setText(translate('BiblesPlugin.EditBibleForm',
                'This is a Web Download Bible.\nIt is not possible to customize the Book Names.'))
            self.scroll_area.hide()
        else:
            self.book_name_notice.setText(translate('BiblesPlugin.EditBibleForm',
                'To use the customized book names, "Bible language" must be selected on the Meta Data tab or, '
                'if "Global settings" is selected, on the Bible page in Configure OpenLP.'))
            for book in BiblesResourcesDB.get_books():
                self.books[book['abbreviation']] = self.manager.get_book_by_id(self.bible, book['id'])
                if self.books[book['abbreviation']] and not self.webbible:
                    self.book_name_edit[book['abbreviation']].setText(self.books[book['abbreviation']].name)
                else:
                    # It is necessary to remove the Widget otherwise there still
                    # exists the vertical spacing in QFormLayout
                    self.book_name_widget_layout.removeWidget(self.book_name_label[book['abbreviation']])
                    self.book_name_label[book['abbreviation']].hide()
                    self.book_name_widget_layout.removeWidget(self.book_name_edit[book['abbreviation']])
                    self.book_name_edit[book['abbreviation']].hide()

    def reject(self):
        """
        Exit Dialog and do not save
        """
        log.debug('BibleEditForm.reject')
        self.bible = None
        QtGui.QDialog.reject(self)

    def accept(self):
        """
        Exit Dialog and save data
        """
        log.debug('BibleEditForm.accept')
        version = self.version_name_edit.text()
        copyright = self.copyright_edit.text()
        permissions = self.permissions_edit.text()
        book_name_language = self.language_selection_combo_box.currentIndex() - 1
        if book_name_language == -1:
            book_name_language = None
        if not self.validateMeta(version, copyright):
            return
        if not self.webbible:
            custom_names = {}
            for abbr, book in self.books.items():
                if book:
                    custom_names[abbr] = self.book_name_edit[abbr].text()
                    if book.name != custom_names[abbr]:
                        if not self.validateBook(custom_names[abbr], abbr):
                            return
        self.application.set_busy_cursor()
        self.manager.save_meta_data(self.bible, version, copyright, permissions, book_name_language)
        if not self.webbible:
            for abbr, book in self.books.items():
                if book:
                    if book.name != custom_names[abbr]:
                        book.name = custom_names[abbr]
                        self.manager.update_book(self.bible, book)
        self.bible = None
        self.application.set_normal_cursor()
        QtGui.QDialog.accept(self)

    def validateMeta(self, name, copyright):
        """
        Validate the Meta before saving.
        """
        if not name:
            self.version_name_edit.setFocus()
            critical_error_message_box(UiStrings().EmptyField,
                translate('BiblesPlugin.BibleEditForm', 'You need to specify a version name for your Bible.'))
            return False
        elif not copyright:
            self.copyright_edit.setFocus()
            critical_error_message_box(UiStrings().EmptyField,
                translate('BiblesPlugin.BibleEditForm',
                'You need to set a copyright for your Bible. Bibles in the Public Domain need to be marked as such.'))
            return False
        elif self.manager.exists(name) and self.manager.get_meta_data(self.bible, 'name').value != \
            name:
            self.version_name_edit.setFocus()
            critical_error_message_box(translate('BiblesPlugin.BibleEditForm', 'Bible Exists'),
                translate('BiblesPlugin.BibleEditForm', 'This Bible already exists. Please import '
                'a different Bible or first delete the existing one.'))
            return False
        return True

    def validateBook(self, new_book_name, abbreviation):
        """
        Validate a book.
        """
        book_regex = re.compile('[\d]*[^\d]+$')
        if not new_book_name:
            self.book_name_edit[abbreviation].setFocus()
            critical_error_message_box(UiStrings().EmptyField,
                translate('BiblesPlugin.BibleEditForm', 'You need to specify a book name for "%s".') %
                    self.book_names[abbreviation])
            return False
        elif not book_regex.match(new_book_name):
            self.book_name_edit[abbreviation].setFocus()
            critical_error_message_box(UiStrings().EmptyField,
                translate('BiblesPlugin.BibleEditForm',
                    'The book name "%s" is not correct.\nNumbers can only be used at the beginning and must\nbe '
                    'followed by one or more non-numeric characters.') % new_book_name)
            return False
        for abbr, book in self.books.items():
            if book:
                if abbr == abbreviation:
                    continue
                if self.book_name_edit[abbr].text() == new_book_name:
                    self.book_name_edit[abbreviation].setFocus()
                    critical_error_message_box(
                        translate('BiblesPlugin.BibleEditForm', 'Duplicate Book Name'),
                        translate('BiblesPlugin.BibleEditForm', 'The Book Name "%s" has been entered more than once.')
                            % new_book_name)
                    return False
        return True

    def _get_application(self):
        """
        Adds the openlp to the class dynamically.
        Windows needs to access the application in a dynamic manner.
        """
        if os.name == 'nt':
            return Registry().get('application')
        else:
            if not hasattr(self, '_application'):
                self._application = Registry().get('application')
            return self._application

    application = property(_get_application)
