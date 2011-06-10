# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Jeffrey Smith, Maikel            #
# Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund                    #
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

from openlp.core.lib import Receiver, translate
from openlp.core.utils import AppLocation
from openlp.plugins.bibles.lib.db import BibleDB, BiblesResourcesDB

log = logging.getLogger(__name__)

def replacement(match):
    return match.group(2).upper()

class OSISBible(BibleDB):
    """
    `OSIS <http://www.bibletechnologies.net/>`_ Bible format importer class.
    """
    log.info(u'BibleOSISImpl loaded')

    def __init__(self, parent, **kwargs):
        log.debug(self.__class__.__name__)
        BibleDB.__init__(self, parent, **kwargs)
        self.filename = kwargs[u'filename']
        fbibles = None
        self.books = {}
        self.verse_regex = re.compile(
            r'<verse osisID="([a-zA-Z0-9 ]*).([0-9]*).([0-9]*)">(.*?)</verse>')
        self.note_regex = re.compile(r'<note(.*?)>(.*?)</note>')
        self.title_regex = re.compile(r'<title(.*?)>(.*?)</title>')
        self.milestone_regex = re.compile(r'<milestone(.*?)/>')
        self.fi_regex = re.compile(r'<FI>(.*?)<Fi>')
        self.rf_regex = re.compile(r'<RF>(.*?)<Rf>')
        self.lb_regex = re.compile(r'<lb(.*?)>')
        self.lg_regex = re.compile(r'<lg(.*?)>')
        self.l_regex = re.compile(r'<l (.*?)>')
        self.w_regex = re.compile(r'<w (.*?)>')
        self.q_regex = re.compile(r'<q(.*?)>')
        self.q1_regex = re.compile(r'<q(.*?)level="1"(.*?)>')
        self.q2_regex = re.compile(r'<q(.*?)level="2"(.*?)>')
        self.trans_regex = re.compile(r'<transChange(.*?)>(.*?)</transChange>')
        self.divine_name_regex = re.compile(
            r'<divineName(.*?)>(.*?)</divineName>')
        self.spaces_regex = re.compile(r'([ ]{2,})')
        filepath = os.path.join(
            AppLocation.get_directory(AppLocation.PluginsDir), u'bibles',
            u'resources', u'osisbooks.csv')
        try:
            fbibles = open(filepath, u'r')
            for line in fbibles:
                book = line.split(u',')
                self.books[book[0]] = (book[1].lstrip().rstrip(),
                    book[2].lstrip().rstrip())
        except IOError:
            log.exception(u'OSIS bible import failed')
        finally:
            if fbibles:
                fbibles.close()

    def do_import(self, bible_name=None):
        """
        Loads a Bible from file.
        """
        log.debug(u'Starting OSIS import from "%s"' % self.filename)
        detect_file = None
        db_book = None
        osis = None
        success = True
        last_chapter = 0
        match_count = 0
        self.wizard.incrementProgressBar(translate('BiblesPlugin.OsisImport',
            'Detecting encoding (this may take a few minutes)...'))
        try:
            detect_file = open(self.filename, u'r')
            details = chardet.detect(detect_file.read(1048576))
        except IOError:
            log.exception(u'Failed to detect OSIS file encoding')
            return
        finally:
            if detect_file:
                detect_file.close()
        # Set meta language_id
        language_id = self.get_language(bible_name)
        if not language_id:
            log.exception(u'Importing books from "%s" failed' % self.filename)
            return False
        try:
            osis = codecs.open(self.filename, u'r', details['encoding'])
            repl = replacement
            for file_record in osis:
                if self.stop_import_flag:
                    break
                match = self.verse_regex.search(file_record)
                if match:
                    match_count += 1
                    book = match.group(1)
                    chapter = int(match.group(2))
                    verse = int(match.group(3))
                    verse_text = match.group(4)
                    if not db_book or db_book.name != self.books[book][0]:
                        log.debug(u'New book: "%s"' % self.books[book][0])
                        book_ref_id = self.get_book_ref_id_by_name(unicode(
                            self.books[book][0]), 67, language_id)
                        if not book_ref_id:
                            log.exception(u'Importing books from "%s" '\
                                'failed' % self.filename)
                            return False
                        book_details = BiblesResourcesDB.get_book_by_id(
                            book_ref_id)
                        db_book = self.create_book(
                            unicode(self.books[book][0]),
                            book_ref_id,
                            book_details[u'testament_id'])
                    if last_chapter == 0:
                        if book == u'Gen':
                            self.wizard.progressBar.setMaximum(1188)
                        else:
                            self.wizard.progressBar.setMaximum(260)
                    if last_chapter != chapter:
                        if last_chapter != 0:
                            self.session.commit()
                        self.wizard.incrementProgressBar(unicode(translate(
                            'BiblesPlugin.OsisImport', 'Importing %s %s...',
                            'Importing <book name> <chapter>...')) %
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
                    verse_text = self.lb_regex.sub(u' ', verse_text)
                    verse_text = self.lg_regex.sub(u'', verse_text)
                    verse_text = self.l_regex.sub(u' ', verse_text)
                    verse_text = self.w_regex.sub(u'', verse_text)
                    verse_text = self.q1_regex.sub(u'"', verse_text)
                    verse_text = self.q2_regex.sub(u'\'', verse_text)
                    verse_text = self.q_regex.sub(u'', verse_text)
                    verse_text = self.divine_name_regex.sub(repl, verse_text)
                    verse_text = self.trans_regex.sub(u'', verse_text)
                    verse_text = verse_text.replace(u'</lb>', u'')\
                        .replace(u'</l>', u'').replace(u'<lg>', u'')\
                        .replace(u'</lg>', u'').replace(u'</q>', u'')\
                        .replace(u'</div>', u'').replace(u'</w>', u'')
                    verse_text = self.spaces_regex.sub(u' ', verse_text)
                    self.create_verse(db_book.id, chapter, verse, verse_text)
                    Receiver.send_message(u'openlp_process_events')
            self.session.commit()
            if match_count == 0:
                success = False
        except (ValueError, IOError):
            log.exception(u'Loading bible from OSIS file failed')
            success = False
        finally:
            if osis:
                osis.close()
        if self.stop_import_flag:
            return False
        else:
            return success
