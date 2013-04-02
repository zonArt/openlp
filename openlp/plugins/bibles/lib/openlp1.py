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
import sqlite
import sys

from openlp.core.ui.wizard import WizardStrings
from openlp.plugins.bibles.lib.db import BibleDB, BiblesResourcesDB

log = logging.getLogger(__name__)

class OpenLP1Bible(BibleDB):
    """
    This class provides the OpenLPv1 bible importer.
    """
    def __init__(self, parent, **kwargs):
        """
        Constructor.
        """
        log.debug(self.__class__.__name__)
        BibleDB.__init__(self, parent, **kwargs)
        self.filename = kwargs[u'filename']

    def do_import(self, bible_name=None):
        """
        Imports an openlp.org v1 bible.
        """
        connection = None
        cursor = None
        try:
            connection = sqlite.connect(self.filename.encode(sys.getfilesystemencoding()))
            cursor = connection.cursor()
        except sqlite.DatabaseError:
            log.exception(u'File "%s" is encrypted or not a sqlite database, '
                'therefore not an openlp.org 1.x database either' % self.filename)
            # Please add an user error here!
            # This file is not an openlp.org 1.x bible database.
            return False
        #Create the bible language
        language_id = self.get_language(bible_name)
        if not language_id:
            log.exception(u'Importing books from "%s" failed' % self.filename)
            return False
        # Create all books.
        try:
            cursor.execute(u'SELECT id, testament_id, name, abbreviation FROM book')
        except sqlite.DatabaseError as error:
            log.exception(u'DatabaseError: %s' % error)
            # Please add an user error here!
            # This file is not an openlp.org 1.x bible database.
            return False
        books = cursor.fetchall()
        self.wizard.progressBar.setMaximum(len(books) + 1)
        for book in books:
            if self.stop_import_flag:
                connection.close()
                return False
            book_id = int(book[0])
            testament_id = int(book[1])
            name = unicode(book[2], u'cp1252')
            abbreviation = unicode(book[3], u'cp1252')
            book_ref_id = self.get_book_ref_id_by_name(name, len(books),
                language_id)
            if not book_ref_id:
                log.exception(u'Importing books from "%s" failed' % self.filename)
                return False
            book_details = BiblesResourcesDB.get_book_by_id(book_ref_id)
            db_book = self.create_book(name, book_ref_id, book_details[u'testament_id'])
            # Update the progess bar.
            self.wizard.incrementProgressBar(WizardStrings.ImportingType % name)
            # Import the verses for this book.
            cursor.execute(u'SELECT chapter, verse, text || \'\' AS text FROM '
                'verse WHERE book_id=%s' % book_id)
            verses = cursor.fetchall()
            for verse in verses:
                if self.stop_import_flag:
                    connection.close()
                    return False
                chapter = int(verse[0])
                verse_number = int(verse[1])
                text = unicode(verse[2], u'cp1252')
                self.create_verse(db_book.id, chapter, verse_number, text)
                self.application.process_events()
            self.session.commit()
        connection.close()
        return True
