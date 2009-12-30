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
import re

from PyQt4 import QtCore

from openlp.core.lib import Receiver
from db import BibleDB

class OSISBible(BibleDB):
    """
    OSIS Bible format importer class.
    """
    global log
    log = logging.getLogger(u'BibleOSISImpl')
    log.info(u'BibleOSISImpl loaded')

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
        self.verse_regex = re.compile(
            r'<verse osisID="([a-zA-Z0-9 ]*).([0-9]*).([0-9]*)">(.*?)</verse>')
        self.note_regex = re.compile(r'<note(.*?)>(.*?)</note>')
        self.title_regex = re.compile(r'<title(.*?)>(.*?)</title>')
        self.milestone_regex = re.compile(r'<milestone(.*?)/>')
        self.fi_regex = re.compile(r'<FI>(.*?)<Fi>')
        self.rf_regex = re.compile(r'<RF>(.*?)<Rf>')
        self.lb_regex = re.compile(r'<lb(.*?)>')
        self.l_regex = re.compile(r'<l (.*?)>')
        self.w_regex = re.compile(r'<w (.*?)>')
        self.q_regex = re.compile(r'<q (.*?)>')
        self.spaces_regex = re.compile(r'([ ]{2,})')
        self.books = {}
        filepath = os.path.split(os.path.abspath(__file__))[0]
        filepath = os.path.abspath(os.path.join(
            filepath, u'..', u'resources', u'osisbooks.csv'))
        fbibles = None
        try:
            fbibles = open(filepath, u'r')
            for line in fbibles:
                book = line.split(u',')
                self.books[book[0]] = (book[1].lstrip().rstrip(),
                    book[2].lstrip().rstrip())
        except:
            log.exception(u'OSIS bible import failed')
        finally:
            if fbibles:
                fbibles.close()

    def do_import(self):
        """
        Loads a Bible from file.
        """
        log.debug(u'Starting OSIS import from "%s"' % self.filename)
        detect_file = None
        try:
            detect_file = open(self.filename, u'r')
            details = chardet.detect(detect_file.read(3000))
        except:
            log.exception(u'Failed to detect OSIS file encoding')
            return
        finally:
            if detect_file:
                detect_file.close()
        osis = None
        success = True
        try:
            osis = codecs.open(self.filename, u'r', details['encoding'])
            last_chapter = 0
            testament = 1
            db_book = None
            for file_record in osis:
                if self.stop_import:
                    break
                match = self.verse_regex.search(file_record)
                if match:
                    book = match.group(1)
                    chapter = int(match.group(2))
                    verse = int(match.group(3))
                    verse_text = match.group(4)
                    if not db_book or db_book.name != self.books[book][0]:
                        log.debug('New book: "%s"', self.books[book][0])
                        if book == u'Matt':
                            testament += 1
                        db_book = self.bibledb.create_book(
                            unicode(self.books[book][0]),
                            unicode(self.books[book][1]),
                            testament)
                    if last_chapter == 0:
                        if book == u'Gen':
                            self.wizard.ImportProgressBar.setMaximum(1188)
                        else:
                            self.wizard.ImportProgressBar.setMaximum(260)
                    if last_chapter != chapter:
                        if last_chapter != 0:
                            self.bibledb.save_verses()
                        self.wizard.incrementProgressBar(
                            u'Importing %s %s...' % \
                            (self.books[match.group(1)][0], chapter))
                        last_chapter = chapter
                    # All of this rigmarol below is because the mod2osis
                    # tool from the Sword library embeds XML in the OSIS
                    # but neglects to enclose the verse text (with XML) in
                    # <[CDATA[ ]]> tags.
                    verse_text = self.note_regex.sub(u'', verse_text)
                    verse_text = self.title_regex.sub(u'', verse_text)
                    verse_text = self.milestone_regex.sub(u'', verse_text)
                    verse_text = self.fi_regex.sub(u'', verse_text)
                    verse_text = self.rf_regex.sub(u'', verse_text)
                    verse_text = self.lb_regex.sub(u'', verse_text)
                    verse_text = self.l_regex.sub(u'', verse_text)
                    verse_text = self.w_regex.sub(u'', verse_text)
                    verse_text = self.q_regex.sub(u'', verse_text)
                    verse_text = verse_text.replace(u'</lb>', u'')\
                        .replace(u'</l>', u'').replace(u'<lg>', u'')\
                        .replace(u'</lg>', u'').replace(u'</q>', u'')\
                        .replace(u'</div>', u'')
                    verse_text = self.spaces_regex.sub(u' ', verse_text)
                    self.add_verse(db_book.id, chapter, verse, verse_text)
                    Receiver.send_message(u'process_events')
            self.commit()
            self.wizard.incrementProgressBar(u'Finishing import...')
        except:
            log.exception(u'Loading bible from OSIS file failed')
            success = False
        finally:
            if osis:
                osis.close()
        if self.stop_import:
            self.wizard.incrementProgressBar(u'Import canceled!')
            return False
        else:
            return success
