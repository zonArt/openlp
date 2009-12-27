# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Tim Bentley, Jonathan Corwin, Michael      #
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

import os
import os.path
import logging
import chardet
import codecs
from lxml import objectify

from PyQt4 import QtCore

from openlp.core.lib import Receiver

class OpenSongBible(object):
    """
    OSIS Bible format importer class.
    """
    global log
    log = logging.getLogger(__name__)
    log.info(u'BibleOpenSongImpl loaded')

    def __init__(self, biblepath, bibledb):
        """
        Constructor to create and set up an instance of the
        BibleOpenSongImpl class.

        ``biblepath``
            This does not seem to be used.

        ``bibledb``
            A reference to a Bible database object.
        """
        log.info(u'BibleOpenSongImpl Initialising')
        self.bibledb = bibledb
        self.loadbible = True
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlpstopimport'), self.stop_import)

    def stop_import(self):
        """
        Stops the import of the Bible.
        """
        self.loadbible = False

    def load_data(self, bible_file, dialogobject=None):
        """
        Loads a Bible from file.

        ``bible_file``
            The file to import from.

        ``dialogobject``
            The Import dialog, so that we can increase the counter on
            the progress bar.
        """
        log.info(u'Load data for %s' % bible_file)
        bible_file = unicode(bible_file)
        detect_file = None
        try:
            detect_file = open(bible_file, u'r')
            details = chardet.detect(detect_file.read(3000))
        except:
            log.exception(u'Failed to detect OpenSong file encoding')
            return False
        finally:
            if detect_file:
                detect_file.close()
        opensong_bible = None
        success = True
        try:
            opensong_bible = codecs.open(bible_file, u'r', details['encoding'])
            opensong = objectify.parse(opensong_bible)
            bible = opensong.getroot()
            for book in bible.b:
                if not self.loadbible:
                    break
                dbbook = self.bibledb.create_book(book.attrib[u'n'],
                    book.attrib[u'n'][:4])
                for chapter in book.c:
                    if not self.loadbible:
                        break
                    for verse in chapter.v:
                        if not self.loadbible:
                            break
                        self.bibledb.add_verse(dbbook.id, chapter.attrib[u'n'],
                            verse.attrib[u'n'], verse.text)
                        Receiver.send_message(u'process_events')
                    dialogobject.incrementProgressBar(u'Importing %s %s' % \
                        (dbbook.name, str(chapter.attrib[u'n'])))
                    self.bibledb.save_verses()
        except:
            log.exception(u'Loading bible from OpenSong file failed')
            success = False
        finally:
            if opensong_bible:
                opensong_bible.close()
        if not self.loadbible:
            dialogobject.incrementProgressBar(u'Import canceled!')
            dialogobject.ImportProgressBar.setValue(
                dialogobject.ImportProgressBar.maximum())
            return False
        else:
            return success

