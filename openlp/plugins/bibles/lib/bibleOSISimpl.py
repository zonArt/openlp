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

import os
import os.path
import logging
import chardet
import codecs

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
        self.bibledb = bibledb
        # books of the bible linked to bibleid  {osis , name}
        self.booksOfBible = {}
        # books of the bible linked to bibleid  {osis ,Abbrev }
        self.abbrevOfBible = {}
        filepath = os.path.split(os.path.abspath(__file__))[0]
        filepath = os.path.abspath(os.path.join(
            filepath, u'..', u'resources',u'osisbooks.csv'))
        fbibles = None
        try:
            fbibles = open(filepath, u'r')
            for line in fbibles:
                p = line.split(u',')
                self.booksOfBible[p[0]] = p[1].replace(u'\n', u'')
                self.abbrevOfBible[p[0]] = p[2].replace(u'\n', u'')
            self.loadbible = True
        except:
            log.exception(u'OSIS bible import failed')
        finally:
            self.loadbible = False
            if fbibles:
                fbibles.close()
        QtCore.QObject.connect(Receiver().get_receiver(),
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
        detect_file = None
        try:
            detect_file = open(osisfile_record, u'r')
            details = chardet.detect(detect_file.read(2048))
        except:
            log.exception(u'Failed to detect OSIS file encoding')
            return
        finally:
            if detect_file:
                detect_file.close()
        osis = None
        try:
            osis = codecs.open(osisfile_record, u'r', details['encoding'])
            book_ptr = None
            count = 0
            verseText = u'<verse osisID='
            testament = 1
            for file_record in osis.readlines():
                # cancel pressed on UI
                if not self.loadbible:
                    break
                pos = file_record.find(verseText)
                # we have a verse
                if pos > -1:
                    epos = file_record.find(u'>', pos)
                    # Book Reference
                    ref = file_record[pos+15:epos-1]
                    #lets find the bible text only
                    # find start of text
                    pos = epos + 1
                    # end  of text
                    epos = file_record.find(u'</verse>', pos)
                    text = file_record[pos : epos]
                    #remove tags of extra information
                    text = self.remove_block(u'<title', u'</title>', text)
                    text = self.remove_block(u'<note', u'</note>', text)
                    text = self.remove_block(
                        u'<divineName', u'</divineName>', text)
                    text = self.remove_tag(u'<lb', text)
                    text = self.remove_tag(u'<q', text)
                    text = self.remove_tag(u'<l', text)
                    text = self.remove_tag(u'<lg', text)
                    # Strange tags where the end is not the same as the start
                    # The must be in this order as at least one bible has them
                    # crossing and the removal does not work.
                    pos = text.find(u'<FI>')
                    while pos > -1:
                        epos = text.find(u'<Fi>', pos)
                        if epos == -1: # TODO
                            pos = -1
                        else:
                            text = text[:pos] + text[epos + 4: ]
                            pos = text.find(u'<FI>')
                    pos = text.find(u'<RF>')
                    while pos > -1:
                        epos = text.find(u'<Rf>', pos)
                        text = text[:pos] + text[epos + 4: ]
                        pos = text.find(u'<RF>')
                    # split up the reference
                    p = ref.split(u'.', 3)
                    if book_ptr != p[0]:
                        # first time through
                        if book_ptr is None:
                            # set the max book size depending
                            # on the first book read
                            if p[0] == u'Gen':
                                dialogobject.setMax(65)
                            else:
                                dialogobject.setMax(27)
                        # First book of NT
                        if  p[0] == u'Matt':
                            testament += 1
                        book_ptr = p[0]
                        book = self.bibledb.create_book(
                            unicode(self.booksOfBible[p[0]]),
                            unicode(self.abbrevOfBible[p[0]]),
                            testament)
                        dialogobject.incrementProgressBar(
                            self.booksOfBible[p[0]])
                        Receiver().send_message(u'process_events')
                        count = 0
                    self.bibledb.add_verse(book.id, p[1], p[2], text)
                    count += 1
                    #Every 3 verses repaint the screen
                    if count % 3 == 0:
                        Receiver().send_message(u'process_events')
                        count = 0
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
