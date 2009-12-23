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

class BibleOSISImpl():
    """
    OSIS Bible format importer class.
    """
    global log
    log = logging.getLogger(u'BibleOSISImpl')
    log.info(u'BibleOSISImpl loaded')

    def __init__(self, biblepath, bibledb):
        """
        Constructor to create and set up an instance of the
        BibleOSISImpl class.

        ``biblepath``
            This does not seem to be used.

        ``bibledb``
            A reference to a Bible database object.
        """
        log.info(u'BibleOSISImpl Initialising')
        self.verse_regex = re.compile(r'<verse osisID="([a-zA-Z0-9 ]*).([0-9]*).([0-9]*)">(.*?)</verse>')
        self.note_regex = re.compile(r'<note(.*?)>(.*?)</note>')
        self.title_regex = re.compile(r'<title(.*?)>(.*?)</title>')
        self.milestone_regex = re.compile(r'<milestone(.*?)/>')
        self.lb_regex = re.compile(r'<lb(.*?)>')
        self.l_regex = re.compile(r'<l (.*?)>')
        self.w_regex = re.compile(r'<w (.*?)>')
        self.q_regex = re.compile(r'<q (.*?)>')
        self.spaces_regex = re.compile(r'([ ]{2,})')
        self.bibledb = bibledb
        # books of the bible linked to bibleid  {osis , name}
        self.booksOfBible = {}
        self.books = {}
        # books of the bible linked to bibleid  {osis ,Abbrev }
        self.abbrevOfBible = {}
        filepath = os.path.split(os.path.abspath(__file__))[0]
        filepath = os.path.abspath(os.path.join(
            filepath, u'..', u'resources', u'osisbooks.csv'))
        fbibles = None
        self.loadbible = True
        try:
            fbibles = open(filepath, u'r')
            for line in fbibles:
                p = line.split(u',')
                #self.booksOfBible[p[0]] = p[1].replace(u'\n', u'')
                self.books[p[0]] = (p[1].lstrip().rstrip(), p[2].lstrip().rstrip())
                #self.abbrevOfBible[p[0]] = p[2].replace(u'\n', u'')
        except:
            log.exception(u'OSIS bible import failed')
        finally:
            if fbibles:
                fbibles.close()
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlpstopimport'), self.stop_import)

    def stop_import(self):
        """
        Stops the import of the Bible.
        """
        self.loadbible = False

    def load_data(self, osisfile_record, dialogobject=None):
        """
        Loads a Bible from file.

        ``osisfile_record``
            The file to import from.

        ``dialogobject``
            The Import dialog, so that we can increase the counter on
            the progress bar.
        """
        log.info(u'Load data for %s' % osisfile_record)
        detect_file = None
        try:
            detect_file = open(osisfile_record, u'r')
            details = chardet.detect(detect_file.read(3000))
        except:
            log.exception(u'Failed to detect OSIS file encoding')
            return
        finally:
            if detect_file:
                detect_file.close()
        osis = None
        try:
            osis = codecs.open(osisfile_record, u'r', details['encoding'])
            last_chapter = 0
            testament = 1
            for file_record in osis:
                match = self.verse_regex.search(file_record)
                if match:
                    book = match.group(1)
                    chapter = int(match.group(2))
                    verse = int(match.group(3))
                    verse_text = match.group(4)
                    if last_chapter == 0:
                        if book == u'Gen':
                            dialogobject.ImportProgressBar.setMaximum(1188)
                        else:
                            dialogobject.ImportProgressBar.setMaximum(260)
                    if last_chapter != chapter:
                        if last_chapter != 0:
                            self.bibledb.save_verses()
                        dialogobject.incrementProgressBar(
                            u'Importing %s %s...' % \
                            (self.books[match.group(1)][0], chapter))
                        if book == u'Matt':
                            testament += 1
                        db_book = self.bibledb.create_book(
                            unicode(self.books[book][0]),
                            unicode(self.books[book][1]),
                            testament)
                        last_chapter = chapter
                    verse_text = self.note_regex.sub(u'', verse_text)
                    verse_text = self.title_regex.sub(u'', verse_text)
                    verse_text = self.milestone_regex.sub(u'', verse_text)
                    verse_text = self.lb_regex.sub(u'', verse_text)
                    verse_text = self.l_regex.sub(u'', verse_text)
                    verse_text = self.w_regex.sub(u'', verse_text)
                    verse_text = self.q_regex.sub(u'', verse_text)
                    verse_text = verse_text.replace(u'</lb>', u'')\
                        .replace(u'</l>', u'').replace(u'<lg>', u'')\
                        .replace(u'</lg>', u'').replace(u'</q>', u'')\
                        .replace(u'</div>', u'')
                    verse_text = self.spaces_regex.sub(u' ', verse_text)
                    self.bibledb.add_verse(db_book.id, chapter, verse, verse_text)
#                    # Strange tags where the end is not the same as the start
#                    # The must be in this order as at least one bible has them
#                    # crossing and the removal does not work.
#                    pos = text.find(u'<FI>')
#                    while pos > -1:
#                        epos = text.find(u'<Fi>', pos)
#                        if epos == -1: # TODO
#                            pos = -1
#                        else:
#                            text = text[:pos] + text[epos + 4: ]
#                            pos = text.find(u'<FI>')
#                    pos = text.find(u'<RF>')
#                    while pos > -1:
#                        epos = text.find(u'<Rf>', pos)
#                        text = text[:pos] + text[epos + 4: ]
#                        pos = text.find(u'<RF>')
            self.bibledb.save_verses()
            dialogobject.incrementProgressBar(u'Finishing import...')
        except:
            log.exception(u'Loading bible from OSIS file failed')
        finally:
            if osis:
                osis.close()

    def remove_block(self, start_tag, end_tag, text):
        """
        Removes a block of text between two tags::

            <tag attrib="xvf">Some not wanted text</tag>

        ``start_tag``
            The XML tag to look for.

        ``end_tag``
            The ending XML tag.

        ``text``
            The string of XML to search.
        """
        pos = text.find(start_tag)
        while pos > -1:
            epos = text.find(end_tag, pos)
            if epos == -1:
                pos = -1
            else:
                text = text[:pos] + text[epos + len(end_tag): ]
                pos = text.find(start_tag)
        return text

    def remove_tag(self, start_tag, text):
        """
        Removes a single tag::

            <tag attrib1="fajkdf" attrib2="fajkdf" attrib3="fajkdf" />

        ``start_tag``
            The XML tag to remove.

        ``text``
            The string of XML to search.
        """
        pos = text.find(start_tag)
        while pos > -1:
            epos = text.find(u'/>', pos)
            text = text[:pos] + text[epos + 2: ]
            pos = text.find(start_tag)
        return text
