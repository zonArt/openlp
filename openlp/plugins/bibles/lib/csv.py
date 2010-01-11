# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

from openlp.core.lib import Receiver
from db import BibleDB

log = logging.getLogger(__name__)

class CSVBible(BibleDB):
    """
    This class provides a specialisation for importing of CSV Bibles.
    """

    def __init__(self, **kwargs):
        """
        Loads a Bible from a pair of CVS files passed in
        This class assumes the files contain all the information and
        a clean bible is being loaded.
        """
        log.info(__name__)
        BibleDB.__init__(self, **kwargs)
        if u'booksfile' not in kwargs:
            raise KeyError(u'You have to supply a file to import books from.')
        self.booksfile = kwargs[u'booksfile']
        if u'versesfile' not in kwargs:
            raise KeyError(u'You have to supply a file to import verses from.')
        self.versesfile = kwargs[u'versesfile']
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlpstopimport'), self.stop_import)

    def stop_import(self):
        """
        Stops the import of the Bible.
        """
        log.debug('Stopping import!')
        self.stop_import = True

    def do_import(self):
        #Populate the Tables
        success = True
        fbooks = None
        try:
            fbooks = open(self.booksfile, 'r')
            for line in fbooks:
                # cancel pressed
                if self.stop_import:
                    break
                details = chardet.detect(line)
                line = unicode(line, details['encoding'])
                p = line.split(u',')
                p1 = p[1].replace(u'"', u'')
                p2 = p[2].replace(u'"', u'')
                p3 = p[3].replace(u'"', u'')
                self.create_book(p2, p3, int(p1))
                Receiver.send_message(u'process_events')
        except:
            log.exception(u'Loading books from file failed')
            success = False
        finally:
            if fbooks:
                fbooks.close()
        if not success:
            return False
        fverse = None
        try:
            fverse = open(versesfile, 'r')
            book_ptr = None
            for line in fverse:
                if self.stop_import:  # cancel pressed
                    break
                details = chardet.detect(line)
                line = unicode(line, details['encoding'])
                # split into 3 units and leave the rest as a single field
                p = line.split(u',', 3)
                p0 = p[0].replace(u'"', u'')
                p3 = p[3].replace(u'"', u'')
                if book_ptr is not p0:
                    book = self.get_book(p0)
                    book_ptr = book.name
                    # increament the progress bar
                    self.wizard.incrementProgressBar(
                        u'Importing %s %s' % book.name)
                    self.commit()
                self.add_verse(book.id, p[1], p[2], p3)
                Receiver.send_message(u'process_events')
            self.commit()
        except:
            log.exception(u'Loading verses from file failed')
            success = False
        finally:
            if fverse:
                fverse.close()
        if self.stop_import:
            self.wizard.incrementProgressBar(u'Import canceled!')
            return False
        else:
            return success