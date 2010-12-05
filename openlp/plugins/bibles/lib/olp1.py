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
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import logging
import sqlite

#from openlp.core.lib import Receiver, translate
from openlp.core.lib import translate
from db import BibleDB

log = logging.getLogger(__name__)

class OpenLP1Bible(BibleDB):
    """
    This class provides the OpenLPv1 bible importer.
    """
    def __init__(self, parent, **kwargs):
        """
        Constructor.
        """
        log.debug(__name__)
        BibleDB.__init__(self, parent, **kwargs)
        if 'filename' not in kwargs:
            raise KeyError(u'You have to supply a file name to import from.')
        self.filename = kwargs['filename']
#        QtCore.QObject.connect(Receiver.get_receiver(),
#            QtCore.SIGNAL(u'bibles_stop_import'), self.stop_import)

    def do_import(self):
        """
        Imports an openlp.org v1 bible.
        """
        # TODO: stop_import_flag
        # TODO: update progress bar
        connection = None
        cursor = None
        self.wizard.incrementProgressBar(u'Preparing for import...')
        try:
            connection = sqlite.connect(self.filename)
            cursor = connection.cursor()
        except:
            return False
        # Import books.
        cursor.execute(u'SELECT id, testament_id, name, abbreviation FROM book')
        books = cursor.fetchall()
        for book in books:
            testament_id = int(book[1])
            name = unicode(book[2], u'cp1252')
            abbreviation = unicode(book[3], u'cp1252')
            self.create_book(name, abbreviation, testament_id)
        self.session.commit()
        # Import chapters/verses.
        for book in books:
            print u'Importiere %s' % book
            cursor.execute(u'SELECT id, book_id, chapter, verse, text || \'\' '
                'AS text FROM verse WHERE book_id=%s' % book)
            verses = cursor.fetchall()
            for verse in verses:
                book_id = int(verse[1])
                chapter = int(verse[2])
                verse_number = int(verse[3])
                text = unicode(verse[4], u'cp1252')
                self.create_verse(book_id, chapter, verse_number, text)
            self.session.commit()
        return True

