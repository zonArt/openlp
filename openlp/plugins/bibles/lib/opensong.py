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
from lxml import etree, objectify

from openlp.core.lib import translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.plugins.bibles.lib.db import BibleDB, BiblesResourcesDB

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

    def get_text(self, element):
        """
        Recursively get all text in an objectify element and its child elements.

        ``element``
            An objectify element to get the text from
        """
        verse_text = u''
        if element.text:
            verse_text = element.text
        for sub_element in element.iterchildren():
            verse_text += self.get_text(sub_element)
        if element.tail:
            verse_text += element.tail
        return verse_text

    def do_import(self, bible_name=None):
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
            language_id = self.get_language(bible_name)
            if not language_id:
                log.exception(u'Importing books from "%s" failed' % self.filename)
                return False
            for book in bible.b:
                if self.stop_import_flag:
                    break
                book_ref_id = self.get_book_ref_id_by_name(unicode(book.attrib[u'n']), len(bible.b), language_id)
                if not book_ref_id:
                    log.exception(u'Importing books from "%s" failed' % self.filename)
                    return False
                book_details = BiblesResourcesDB.get_book_by_id(book_ref_id)
                db_book = self.create_book(unicode(book.attrib[u'n']), book_ref_id, book_details[u'testament_id'])
                chapter_number = 0
                for chapter in book.c:
                    if self.stop_import_flag:
                        break
                    number = chapter.attrib[u'n']
                    if number:
                        chapter_number = int(number.split()[-1])
                    else:
                        chapter_number += 1
                    verse_number = 0
                    for verse in chapter.v:
                        if self.stop_import_flag:
                            break
                        number = verse.attrib[u'n']
                        if number:
                            try:
                                number = int(number)
                            except ValueError:
                                verse_parts = number.split(u'-')
                                if len(verse_parts) > 1:
                                    number = int(verse_parts[0])
                            except TypeError:
                                log.warn(u'Illegal verse number: %s',
                                    unicode(verse.attrib[u'n']))
                            verse_number = number
                        else:
                            verse_number += 1
                        self.create_verse(
                            db_book.id,
                            chapter_number,
                            verse_number,
                            self.get_text(verse))
                    self.wizard.incrementProgressBar(translate('BiblesPlugin.Opensong', 'Importing %s %s...',
                        'Importing <book name> <chapter>...')) % (db_book.name, chapter_number)
                self.session.commit()
            self.application.process_events()
        except etree.XMLSyntaxError as inst:
            critical_error_message_box(message=translate('BiblesPlugin.OpenSongImport',
                'Incorrect Bible file type supplied. OpenSong Bibles may be '
                'compressed. You must decompress them before import.'))
            log.exception(inst)
            success = False
        except (IOError, AttributeError):
            log.exception(u'Loading Bible from OpenSong file failed')
            success = False
        finally:
            if file:
                file.close()
        if self.stop_import_flag:
            return False
        else:
            return success
