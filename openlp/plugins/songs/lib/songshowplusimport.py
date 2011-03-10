# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
"""
The :mod:`wowimport` module provides the functionality for importing Words of
Worship songs into the OpenLP database.
"""
import os
import logging
import struct

from openlp.core.ui.wizard import WizardStrings
from openlp.plugins.songs.lib.songimport import SongImport

TITLE = 1
AUTHOR = 2
COPYRIGHT = 3
CCLI_NO = 5
VERSE = 12
CHORUS = 20
TOPIC = 29
COMMENTS = 30
VERSE_ORDER = 31
SONG_BOOK = 35
SONG_NUMBER = 36
CUSTOM_VERSE = 37

log = logging.getLogger(__name__)

class SongShowPlusImport(SongImport):
    """
    The :class:`SongShowPlusImport` class provides the ability to import song
    files from SongShow Plus.

    **SongShow Plus Song File Format:**

    The SongShow Plus song file format is as follows:

    * Each piece of data in the song file has some information that precedes
    it.
    * The general format of this data is as follows:
    4 Bytes, forming a 32 bit number, a key if you will, this describes what
    the data is (see blockKey below)
    4 Bytes, forming a 32 bit number, which is the number of bytes until the
    next block starts
    1 Byte, which tells how namy bytes follows
    1 or 4 Bytes, describes how long the string is, if its 1 byte, the string
    is less than 255
    The next bytes are the actuall data.
    The next block of data follows on.

    This description does differ for verses. Which includes extra bytes
    stating the verse type or number. In some cases a "custom" verse is used,
    in that case, this block will in include 2 strings, with the associated
    string length descriptors. The first string is the name of the verse, the
    second is the verse content.

    The file is ended with four null bytes.

    Valid extensions for a SongShow Plus song file are:

    * .sbsong
    """
    otherList = {}
    otherCount = 0

    def __init__(self, manager, **kwargs):
        """
        Initialise the SongShow Plus importer.
        """
        SongImport.__init__(self, manager, **kwargs)

    def do_import(self):
        """
        Receive a single file or a list of files to import.
        """
        if isinstance(self.import_source, list):
            self.import_wizard.progressBar.setMaximum(len(self.import_source))
            for file in self.import_source:
                author = u''
                self.sspVerseOrderList = []
                otherCount = 0
                otherList = {}
                file_name = os.path.split(file)[1]
                self.import_wizard.incrementProgressBar(
                    WizardStrings.ImportingType % file_name, 0)
                songData = open(file, 'rb')
                while (1):
                    blockKey, = struct.unpack("I", songData.read(4))
                    # The file ends with 4 NUL's
                    if blockKey == 0:
                        break
                    nextBlockStarts, = struct.unpack("I", songData.read(4))
                    if blockKey == VERSE or blockKey == CHORUS:
                        null, verseNo,  = struct.unpack("BB", songData.read(2))
                    elif blockKey == CUSTOM_VERSE:
                        null, verseNameLength, = struct.unpack("BB",
                            songData.read(2))
                        verseName = songData.read(verseNameLength)
                    lengthDescriptorSize, = struct.unpack("B", songData.read(1))
                    # Detect if/how long the length descriptor is
                    if lengthDescriptorSize == 12:
                        lengthDescriptor, = struct.unpack("I", songData.read(4))
                    elif lengthDescriptorSize == 2:
                        lengthDescriptor = 1
                    elif lengthDescriptorSize == 9:
                        lengthDescriptor = 0
                    else:
                        lengthDescriptor, = struct.unpack("B", songData.read(1))
                    data = songData.read(lengthDescriptor)
                    if blockKey == TITLE:
                        self.title = unicode(data, u'cp1252')
                    elif blockKey == AUTHOR:
                        authors = data.split(" / ")
                        for author in authors:
                            if author.find(",") !=-1:
                                authorParts = author.split(", ")
                                author = authorParts[1] + " " + authorParts[0]
                            self.parse_author(unicode(author, u'cp1252'))
                    elif blockKey == COPYRIGHT:
                        self.add_copyright(unicode(data, u'cp1252'))
                    elif blockKey == CCLI_NO:
                        self.ccli_number = int(data)
                    elif blockKey == VERSE:
                        self.add_verse(unicode(data, u'cp1252'),
                            "V%s" % verseNo)
                    elif blockKey == CHORUS:
                        self.add_verse(unicode(data, u'cp1252'),
                            "C%s" % verseNo)
                    elif blockKey == TOPIC:
                        self.topics.append(unicode(data, u'cp1252'))
                    elif blockKey == COMMENTS:
                        self.comments = unicode(data, u'cp1252')
                    elif blockKey == VERSE_ORDER:
                        verseTag = self.toOpenLPVerseTag(data, True)
                        if verseTag:
                            self.sspVerseOrderList.append(unicode(verseTag,
                                u'cp1252'))
                    elif blockKey == SONG_BOOK:
                        self.song_book_name = unicode(data, u'cp1252')
                    elif blockKey == SONG_NUMBER:
                        self.song_number = ord(data)
                    elif blockKey == CUSTOM_VERSE:
                        verseTag = self.toOpenLPVerseTag(verseName)
                        self.add_verse(unicode(data, u'cp1252'), verseTag)
                    else:
                        log.debug("Unrecognised blockKey: %s, data: %s"
                            %(blockKey, data))
                self.verse_order_list = self.sspVerseOrderList
                songData.close()
                self.finish()
                self.import_wizard.incrementProgressBar(
                    WizardStrings.ImportingType % file_name)
            return True

    def toOpenLPVerseTag(self, verseName, ignoreUnique=False):
        if verseName.find(" ") != -1:
            verseParts = verseName.split(" ")
            verseType = verseParts[0]
            verseNumber = verseParts[1]
        else:
            verseType = verseName
            verseNumber = "1"
        verseType = verseType.lower()
        if verseType == "verse":
            verseTag = "V"
        elif verseType == "chorus":
            verseTag = "C"
        elif verseType == "bridge":
            verseTag = "B"
        elif verseType == "pre-chorus":
            verseTag = "P"
        elif verseType == "bridge":
            verseTag = "B"
        else:
            if not self.otherList.has_key(verseName):
                if ignoreUnique:
                    return None
                self.otherCount = self.otherCount + 1
                self.otherList[verseName] = str(self.otherCount)
            verseTag = "O"
            verseNumber = self.otherList[verseName]
        verseTag = verseTag + verseNumber
        return verseTag
