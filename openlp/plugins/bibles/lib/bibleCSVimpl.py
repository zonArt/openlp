# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from openlp.plugins.bibles.lib.common import BibleCommon
from openlp.core.lib import Receiver

class BibleCSVImpl(BibleCommon):
    global log
    log = logging.getLogger(u'BibleCSVImpl')
    log.info(u'BibleCVSImpl loaded')
    def __init__(self, bibledb):
        """
        Loads a Bible from a pair of CVS files passed in
        This class assumes the files contain all the information and
        a clean bible is being loaded.
        """
        self.bibledb = bibledb
        self.loadbible = True
        QtCore.QObject.connect(Receiver().get_receiver(),
            QtCore.SIGNAL(u'openlpstopimport'), self.stop_import)

    def stop_import(self):
        self.loadbible = False

    def load_data(self, booksfile, versesfile, dialogobject):
        #Populate the Tables
        fbooks = None
        try:
            fbooks = open(booksfile, 'r')
            count = 0
            for line in fbooks:
                # cancel pressed
                if not self.loadbible:
                    break
                details = chardet.detect(line)
                line = unicode(line, details['encoding'])
                p = line.split(u',')
                p1 = p[1].replace(u'"', u'')
                p2 = p[2].replace(u'"', u'')
                p3 = p[3].replace(u'"', u'')
                self.bibledb.create_book(p2, p3, int(p1))
                count += 1
                #Flush the screen events
                if count % 3 == 0:
                    Receiver().send_message(u'process_events')
                    count = 0
        except:
            log.exception(u'Loading books from file failed')
        finally:
            if fbooks:
                fbooks.close()

        fverse = None
        try:
            fverse = open(versesfile, 'r')
            count = 0
            book_ptr = None
            for line in fverse:
                if not self.loadbible:  # cancel pressed
                    break
                details = chardet.detect(line)
                line = unicode(line, details['encoding'])
                # split into 3 units and leave the rest as a single field
                p = line.split(u',', 3)
                p0 = p[0].replace(u'"', u'')
                p3 = p[3].replace(u'"',u'')
                if book_ptr is not p0:
                    book = self.bibledb.get_bible_book(p0)
                    book_ptr = book.name
                    # increament the progress bar
                    dialogobject.incrementProgressBar(book.name)
                self.bibledb.add_verse(book.id, p[1], p[2], p3)
                count += 1
                #Every x verses repaint the screen
                if count % 3 == 0:
                    Receiver().send_message(u'process_events')
                    count = 0
        except:
            log.exception(u'Loading verses from file failed')
        finally:
            if fverse:
                fverse.close()
