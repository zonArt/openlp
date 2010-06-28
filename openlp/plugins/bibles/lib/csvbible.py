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

import logging
import chardet
import csv

from PyQt4 import QtCore

from openlp.core.lib import Receiver
from db import BibleDB

log = logging.getLogger(__name__)

class CSVBible(BibleDB):
    """
    This class provides a specialisation for importing of CSV Bibles.
    """

    def __init__(self, parent, **kwargs):
        """
        Loads a Bible from a pair of CVS files passed in
        This class assumes the files contain all the information and
        a clean bible is being loaded.
        """
        BibleDB.__init__(self, parent, **kwargs)
        log.info(self.__class__.__name__)
        if u'booksfile' not in kwargs:
            raise KeyError(u'You have to supply a file to import books from.')
        self.booksfile = kwargs[u'booksfile']
        if u'versesfile' not in kwargs:
            raise KeyError(u'You have to supply a file to import verses from.')
        self.versesfile = kwargs[u'versesfile']
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'bibles_stop_import'), self.stop_import)

    def do_import(self):
        #Populate the Tables
        success = True
        books_file = None
        try:
            books_file = open(self.booksfile, 'r')
            dialect = csv.Sniffer().sniff(books_file.read(1024))
            books_file.seek(0)
            books_reader = csv.reader(books_file, dialect)
            for line in books_reader:
                # cancel pressed
                if self.stop_import_flag:
                    break
                details = chardet.detect(line[1])
                self.create_book(unicode(line[1], details['encoding']),
                    line[2], int(line[0]))
                Receiver.send_message(u'openlp_process_events')
        except IOError:
            log.exception(u'Loading books from file failed')
            success = False
        finally:
            if books_file:
                books_file.close()
        if not success:
            return False
        verse_file = None
        try:
            book_ptr = None
            verse_file = open(self.versesfile, 'r')
            dialect = csv.Sniffer().sniff(verse_file.read(1024))
            verse_file.seek(0)
            verse_reader = csv.reader(verse_file, dialect)
            for line in verse_reader:
                if self.stop_import_flag:  # cancel pressed
                    break
                details = chardet.detect(line[3])
                if book_ptr != line[0]:
                    book = self.get_book(line[0])
                    book_ptr = book.name
                    self.wizard.incrementProgressBar(
                        u'Importing %s %s' % (book.name, line[1]))
                    self.session.commit()
                self.create_verse(book.id, line[1], line[2],
                                  unicode(line[3], details['encoding']))
                Receiver.send_message(u'openlp_process_events')
            self.session.commit()
        except IOError:
            log.exception(u'Loading verses from file failed')
            success = False
        finally:
            if verse_file:
                verse_file.close()
        if self.stop_import_flag:
            self.wizard.incrementProgressBar(u'Import canceled!')
            return False
        else:
            return success
