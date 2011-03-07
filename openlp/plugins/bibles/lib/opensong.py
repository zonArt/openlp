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
from lxml import objectify

from openlp.core.lib import Receiver, translate
from openlp.plugins.bibles.lib.db import BibleDB

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
        log.debug(self.__class__.__name__)
        BibleDB.__init__(self, parent, **kwargs)
        self.filename = kwargs['filename']

    def do_import(self):
        """
        Loads a Bible from file.
        """
        log.debug(u'Starting OpenSong import from "%s"' % self.filename)
        if not isinstance(self.filename, unicode):
            self.filename = unicode(self.filename, u'utf8')
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
                            int(chapter.attrib[u'n'].split()[-1]),
                            int(verse.attrib[u'n']),
                            unicode(verse.text))
                    self.wizard.incrementProgressBar(unicode(translate(
                        'BiblesPlugin.Opensong', 'Importing %s %s...',
                        'Importing <book name> <chapter>...')) %
                        (db_book.name, int(chapter.attrib[u'n'].split()[-1])))
                self.session.commit()
            Receiver.send_message(u'openlp_process_events')
        except (IOError, AttributeError):
            log.exception(u'Loading bible from OpenSong file failed')
            success = False
        finally:
            if file:
                file.close()
        if self.stop_import_flag:
            return False
        else:
            return success
