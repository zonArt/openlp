# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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

from openlp.core.lib import Receiver
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
        self.parent = parent
        self.filename = kwargs[u'filename']

    def do_import(self):
        """
        Imports an openlp.org v1 bible.
        """
        connection = None
        cursor = None
        try:
            connection = sqlite.connect(self.filename)
            cursor = connection.cursor()
        except:
            return False
        #Create the bible language
        language = self.parent.mediaItem.importRequest(u'language')
        if not language:
            log.exception(u'Importing books from %s   " '\
                'failed' % self.filename)
            return False
        language = BiblesResourcesDB.get_language(language)
        language_id = language[u'id']
        self.create_meta(u'language_id', language_id)
        # Create all books.
        cursor.execute(u'SELECT id, testament_id, name, abbreviation FROM book')
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
            book_ref_id = self.parent.manager.get_book_ref_id_by_name(name, 
                language_id)
            if not book_ref_id:
                log.exception(u'Importing books from %s " '\
                    'failed' % self.filename)
                return False
            book_details = BiblesResourcesDB.get_book_by_id(book_ref_id)
            self.create_book(name, book_ref_id, book_details[u'testament_id'])
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
                self.create_verse(book_id, chapter, verse_number, text)
                Receiver.send_message(u'openlp_process_events')
            self.session.commit()
        connection.close()
        return True
