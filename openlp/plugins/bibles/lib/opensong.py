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

from lxml import objectify
from PyQt4 import QtCore

from openlp.core.lib import Receiver
from db import BibleDB

log = logging.getLogger(__name__)

class OpenSongBible(BibleDB):
    """
    OpenSong Bible format importer class.
    """

    def __init__(self, parent, **kwargs):
        """
        Constructor to create and set up an instance of the OpenSongBible
        class. This class is used to import Bibles from OpenSong's XML format.
        """
        log.debug(__name__)
        BibleDB.__init__(self, parent, **kwargs)
        if 'filename' not in kwargs:
            raise KeyError(u'You have to supply a file name to import from.')
        self.filename = kwargs['filename']
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlpstopimport'), self.stop_import)

    def stop_import(self):
        """
        Stops the import of the Bible.
        """
        log.debug('Stopping import!')
        self.stop_import_flag = True

    def do_import(self):
        """
        Loads a Bible from file.
        """
        log.debug(u'Starting OpenSong import from "%s"' % self.filename)
        if not isinstance(self.filename, unicode):
            self.filename = unicode(self.filename, u'utf8')
        self.wizard.incrementProgressBar(u'Preparing for import...')
        file = None
        success = True
        try:
            # NOTE: We don't need to do any of the normal encoding detection
            # here, because lxml does it's own encoding detection, and the two
            # mechanisms together interfere with each other.
            file = open(self.filename, u'r')
            opensong = objectify.parse(file)
            bible = opensong.getroot()
            for book in bible.b:
                if self.stop_import_flag:
                    break
                db_book = self.create_book(unicode(book.attrib[u'n']),
                    unicode(book.attrib[u'n'][:4]))
                for chapter in book.c:
                    if self.stop_import_flag:
                        break
                    for verse in chapter.v:
                        if self.stop_import_flag:
                            break
                        self.create_verse(
                            db_book.id,
                            int(chapter.attrib[u'n']),
                            int(verse.attrib[u'n']),
                            unicode(verse.text)
                        )
                        Receiver.send_message(u'process_events')
                    self.wizard.incrementProgressBar(
                        QtCore.QString('%s %s %s' % (self.trUtf8('Importing'),\
                            db_book.name, chapter.attrib[u'n'])))
                    self.commit()
        except:
            log.exception(u'Loading bible from OpenSong file failed')
            success = False
        finally:
            if file:
                file.close()
        if self.stop_import_flag:
            self.wizard.incrementProgressBar(u'Import canceled!')
            return False
        else:
            return success
