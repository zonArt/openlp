# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
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

import logging
import re

from lxml import etree, objectify

from openlp.plugins.songs.lib import VerseType
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

class EasySlidesImport(SongImport):
    """
    Import songs exported from EasySlides

    The format example is here:
    http://wiki.openlp.org/Development:EasiSlides_-_Song_Data_Format
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the class.
        """
        SongImport.__init__(self, manager, **kwargs)
        self.commit = True

    def doImport(self):
        """
        Import either each of the files in self.importSources - each element of
        which can be either a single opensong file, or a zipfile containing
        multiple opensong files. If `self.commit` is set False, the
        import will not be committed to the database (useful for test scripts).
        """
        log.info(u'Importing EasySlides XML file %s', self.importSource)
        parser = etree.XMLParser(remove_blank_text=True)
        parsed_file = etree.parse(self.importSource, parser)
        xml = unicode(etree.tostring(parsed_file))
        song_xml = objectify.fromstring(xml)
        self.importWizard.progressBar.setMaximum(len(song_xml.Item))
        for song in song_xml.Item:
            if self.stopImportFlag:
                return
            self._parseSong(song)

    def _parseSong(self, song):
        self._success = True
        self._addUnicodeAttribute(u'title', song.Title1, True)
        if hasattr(song, u'Title2'):
            self._addUnicodeAttribute(u'alternateTitle', song.Title2)
        if hasattr(song, u'SongNumber'):
            self._addUnicodeAttribute(u'songNumber', song.SongNumber)
        if self.songNumber == u'0':
            self.songNumber = u''
        self._addAuthors(song)
        if hasattr(song, u'Copyright'):
            self._addCopyright(song.Copyright)
        if hasattr(song, u'LicenceAdmin1'):
            self._addCopyright(song.LicenceAdmin1)
        if hasattr(song, u'LicenceAdmin2'):
            self._addCopyright(song.LicenceAdmin2)
        if hasattr(song, u'BookReference'):
            self._addUnicodeAttribute(u'songBookName', song.BookReference)
        self._parseAndAddLyrics(song)
        if self._success:
            if not self.finish():
                self.logError(song.Title1 if song.Title1 else u'')
        else:
            self.setDefaults()

    def _addUnicodeAttribute(self, self_attribute, import_attribute,
        mandatory=False):
        """
        Add imported values to the song model converting them to unicode at the
        same time. If the unicode decode fails or a mandatory attribute is not
        present _success is set to False so the importer can react
        appropriately.

        ``self_attribute``
            The attribute in the song model to populate.

        ``import_attribute``
            The imported value to convert to unicode and save to the song.

        ``mandatory``
            Signals that this attribute must exist in a valid song.
        """
        try:
            setattr(self, self_attribute, unicode(import_attribute).strip())
        except UnicodeDecodeError:
            log.exception(u'UnicodeDecodeError decoding %s' % import_attribute)
            self._success = False
        except AttributeError:
            log.exception(u'No attribute %s' % import_attribute)
            if mandatory:
                self._success = False

    def _addAuthors(self, song):
        try:
            authors = unicode(song.Writer).split(u',')
            self.authors = \
                [author.strip() for author in authors if author.strip()]
        except UnicodeDecodeError:
            log.exception(u'Unicode decode error while decoding Writer')
            self._success = False
        except AttributeError:
            pass

    def _addCopyright(self, element):
        """
        Add a piece of copyright to the total copyright information for the
        song.

        ``element``
            The imported variable to get the data from.
        """
        try:
            self.addCopyright(unicode(element).strip())
        except UnicodeDecodeError:
            log.exception(u'Unicode error on decoding copyright: %s' % element)
            self._success = False
        except AttributeError:
            pass

    def _parseAndAddLyrics(self, song):
        try:
            lyrics = unicode(song.Contents).strip()
        except UnicodeDecodeError:
            log.exception(u'Unicode decode error while decoding Contents')
            self._success = False
        except AttributeError:
            log.exception(u'no Contents')
            self._success = False
        lines = lyrics.split(u'\n')
        # we go over all lines first, to determine information,
        # which tells us how to parse verses later
        regionlines = {}
        separatorlines = 0
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            elif line[1:7] == u'region':
                # this is region separator, probably [region 2]
                region = self._extractRegion(line)
                if regionlines.has_key(region):
                    regionlines[region] = regionlines[region] + 1
                else:
                    regionlines[region] = 1
            elif line[0] == u'[':
                separatorlines = separatorlines + 1
        # if the song has separators
        separators = (separatorlines > 0)
        # the number of different regions in song - 1
        if len(regionlines) > 1:
            log.info(u'EasySlidesImport: the file contained a song named "%s"'
                u'with more than two regions, but only two regions are',
                u'tested, encountered regions were: %s',
                self.title, u','.join(regionlines.keys()))
        # if the song has regions
        regions = (len(regionlines) > 0)
        # if the regions are inside verses
        regionsInVerses = (regions and regionlines[regionlines.keys()[0]] > 1)
        MarkTypes = {
            u'CHORUS': VerseType.Tags[VerseType.Chorus],
            u'VERSE': VerseType.Tags[VerseType.Verse],
            u'INTRO': VerseType.Tags[VerseType.Intro],
            u'ENDING': VerseType.Tags[VerseType.Ending],
            u'BRIDGE': VerseType.Tags[VerseType.Bridge],
            u'PRECHORUS': VerseType.Tags[VerseType.PreChorus]
        }
        verses = {}
        # list as [region, versetype, versenum, instance]
        our_verse_order = []
        defaultregion = u'1'
        reg = defaultregion
        verses[reg] = {}
        # instance differentiates occurrences of same verse tag
        vt = u'V'
        vn = u'1'
        inst = 1

        for line in lines:
            line = line.strip()
            if len(line) == 0:
                if separators:
                    # separators are used, so empty line means slide break
                    # inside verse
                    if self._listHas(verses, [reg, vt, vn, inst]):
                        inst = inst + 1
                else:
                    # separators are not used, so empty line starts a new verse
                    vt = u'V'
                    if verses[reg].has_key(vt):
                        vn = len(verses[reg][vt].keys())+1
                    else:
                        vn = u'1'
                    inst = 1
            elif line[0:7] == u'[region':
                reg = self._extractRegion(line)
                if not verses.has_key(reg):
                    verses[reg] = {}
                if not regionsInVerses:
                    vt = u'V'
                    vn = u'1'
                    inst = 1
            elif line[0] == u'[':
                # this is a normal section marker
                marker = line[1:line.find(u']')].upper()
                vn = u'1'
                # have we got any digits?
                # If so, versenumber is everything from the digits to the end
                match = re.match(u'(.*)(\d+.*)', marker)
                if match:
                    marker = match.group(1).strip()
                    vn = match.group(2)
                if len(marker) == 0:
                    vt = u'V'
                elif MarkTypes.has_key(marker):
                    vt = MarkTypes[marker]
                else:
                    vt = u'O'
                if regionsInVerses:
                    region = defaultregion
                inst = 1
                if self._listHas(verses, [reg, vt, vn, inst]):
                    inst = len(verses[reg][vt][vn])+1
            else:
                if not [reg, vt, vn, inst] in our_verse_order:
                    our_verse_order.append([reg, vt, vn, inst])
                if not verses[reg].has_key(vt):
                    verses[reg][vt] = {}
                if not verses[reg][vt].has_key(vn):
                    verses[reg][vt][vn] = {}
                if not verses[reg][vt][vn].has_key(inst):
                    verses[reg][vt][vn][inst] = []
                words = self.tidyText(line)
                verses[reg][vt][vn][inst].append(words)
        # done parsing

        versetags = []
        # we use our_verse_order to ensure, we insert lyrics in the same order
        # as these appeared originally in the file
        for [reg, vt, vn, inst] in our_verse_order:
            if self._listHas(verses, [reg, vt, vn, inst]):
                # this is false, but needs user input
                lang = None
                versetag = u'%s%s' % (vt, vn)
                versetags.append(versetag)
                lines = u'\n'.join(verses[reg][vt][vn][inst])
                self.verses.append([versetag, lines, lang])

        SeqTypes = {
            u'p': u'P1',
            u'q': u'P2',
            u'c': u'C1',
            u't': u'C2',
            u'b': u'B1',
            u'w': u'B2',
            u'e': u'E1'}
        # Make use of Sequence data, determining the order of verses
        try:
            order = unicode(song.Sequence).strip().split(u',')
            for tag in order:
                if len(tag) == 0:
                    continue
                elif tag[0].isdigit():
                    tag = u'V' + tag
                elif SeqTypes.has_key(tag.lower()):
                    tag = SeqTypes[tag.lower()]
                else:
                    continue
                if tag in versetags:
                    self.verseOrderList.append(tag)
                else:
                    log.info(u'Got order item %s, which is not in versetags,'
                        u'dropping item from presentation order', tag)
        except UnicodeDecodeError:
            log.exception(u'Unicode decode error while decoding Sequence')
            self._success = False
        except AttributeError:
            pass

    def _listHas(self, lst, subitems):
        for subitem in subitems:
            if isinstance(lst, dict) and lst.has_key(subitem):
                lst = lst[subitem]
            elif isinstance(lst, list) and subitem in lst:
                lst = lst[subitem]
            else:
                return False
        return True

    def _extractRegion(self, line):
        # this was true already: line[0:7] == u'[region':
        right_bracket = line.find(u']')
        return line[7:right_bracket].strip()
