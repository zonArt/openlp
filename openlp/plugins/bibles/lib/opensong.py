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

import os
import os.path
import logging
import chardet
import codecs
from lxml import objectify

from PyQt4 import QtCore

from openlp.core.lib import Receiver
from db import BibleDB

log = logging.getLogger(__name__)

class OpenSongBible(BibleDB):
    """
    OpenSong Bible format importer class.
    """

    def __init__(self, **kwargs):
        """
        Constructor to create and set up an instance of the OpenSongBible
        class. This class is used to import Bibles from OpenSong's XML format.
        """
        log.debug(__name__)
        BibleDB.__init__(self, **kwargs)
        if u'filename' not in kwargs:
            raise KeyError(u'You have to supply a file name to import from.')
        self.filename = kwargs[u'filename']
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlpstopimport'), self.stop_import)

    def stop_import(self):
        """
        Stops the import of the Bible.
        """
        log.debug('Stopping import!')
        self.stop_import = True

    def do_import(self):
        """
        Loads a Bible from file.
        """
        log.debug(u'Starting OpenSong import from "%s"' % self.filename)
        detect_file = None
        try:
            detect_file = open(self.filename, u'r')
            details = chardet.detect(detect_file.read(3000))
        except:
            log.exception(u'Failed to detect OpenSong file encoding')
            return False
        finally:
            if detect_file:
                detect_file.close()
        file = None
        success = True
        try:
            file = codecs.open(self.filename, u'r', details['encoding'])
            opensong = objectify.parse(file)
            bible = opensong.getroot()
            for book in bible.b:
                if self.stop_import:
                    break
                db_book = self.create_book(book.attrib[u'n'],
                                           book.attrib[u'n'][:4])
                for chapter in book.c:
                    if self.stop_import:
                        break
                    for verse in chapter.v:
                        if self.stop_import:
                            break
                        self.add_verse(db_book.id, chapter.attrib[u'n'],
                            verse.attrib[u'n'], verse.text)
                        Receiver.send_message(u'process_events')
                    self.wizard.incrementProgressBar(u'Importing %s %s' % \
                        (dbbook.name, str(chapter.attrib[u'n'])))
                    self.commit()
        except:
            log.exception(u'Loading bible from OpenSong file failed')
            success = False
        finally:
            if file:
                file.close()
        if self.stop_import:
            self.wizard.incrementProgressBar(u'Import canceled!')
            return False
        else:
            return success
