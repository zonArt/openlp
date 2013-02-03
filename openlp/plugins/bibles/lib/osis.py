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

import os
import logging
import chardet
import codecs
import re

from openlp.core.lib import translate
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
        self.language_regex = re.compile(r'<language.*>(.*?)</language>')
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
            AppLocation.get_directory(AppLocation.PluginsDir), u'bibles', u'resources', u'osisbooks.csv')

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
            detect_file.seek(0)
            lines_in_file = int(len(detect_file.readlines()))
        except IOError:
            log.exception(u'Failed to detect OSIS file encoding')
            return
        finally:
            if detect_file:
                detect_file.close()
        try:
            osis = codecs.open(self.filename, u'r', details['encoding'])
            repl = replacement
            language_id = False
            # Decide if the bible propably contains only NT or AT and NT or
            # AT, NT and Apocrypha
            if lines_in_file < 11500:
                book_count = 27
                chapter_count = 260
            elif lines_in_file < 34200:
                book_count = 66
                chapter_count = 1188
            else:
                book_count = 67
                chapter_count = 1336
            for file_record in osis:
                if self.stop_import_flag:
                    break
                # Try to find the bible language
                if not language_id:
                    language_match = self.language_regex.search(file_record)
                    if language_match:
                        language = BiblesResourcesDB.get_language(
                            language_match.group(1))
                        if language:
                            language_id = language[u'id']
                            self.save_meta(u'language_id', language_id)
                        continue
                match = self.verse_regex.search(file_record)
                if match:
                    # Set meta language_id if not detected till now
                    if not language_id:
                        language_id = self.get_language(bible_name)
                        if not language_id:
                            log.exception(u'Importing books from "%s" failed' % self.filename)
                            return False
                    match_count += 1
                    book = unicode(match.group(1))
                    chapter = int(match.group(2))
                    verse = int(match.group(3))
                    verse_text = match.group(4)
                    book_ref_id = self.get_book_ref_id_by_name(book, book_count, language_id)
                    if not book_ref_id:
                        log.exception(u'Importing books from "%s" failed' % self.filename)
                        return False
                    book_details = BiblesResourcesDB.get_book_by_id(book_ref_id)
                    if not db_book or db_book.name != book_details[u'name']:
                        log.debug(u'New book: "%s"' % book_details[u'name'])
                        db_book = self.create_book(
                            book_details[u'name'],
                            book_ref_id,
                            book_details[u'testament_id'])
                    if last_chapter == 0:
                        self.wizard.progressBar.setMaximum(chapter_count)
                    if last_chapter != chapter:
                        if last_chapter != 0:
                            self.session.commit()
                        self.wizard.incrementProgressBar(translate('BiblesPlugin.OsisImport', 'Importing %s %s...',
                            'Importing <book name> <chapter>...') % (book_details[u'name'], chapter))
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
                    verse_text = verse_text.replace(u'</lb>', u'') \
                        .replace(u'</l>', u'').replace(u'<lg>', u'') \
                        .replace(u'</lg>', u'').replace(u'</q>', u'') \
                        .replace(u'</div>', u'').replace(u'</w>', u'')
                    verse_text = self.spaces_regex.sub(u' ', verse_text)
                    self.create_verse(db_book.id, chapter, verse, verse_text)
                    self.application.process_events()
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
