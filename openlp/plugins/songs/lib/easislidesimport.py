# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
import os
from lxml import etree, objectify
from lxml.etree import Error, LxmlError
import re

from openlp.core.lib import translate
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

class EasiSlidesImport(SongImport):
    """
    Import songs exported from EasiSlides

    The format example is here: 
    http://wiki.openlp.org/Development:EasiSlides_-_Song_Data_Format
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the class.
        """
        SongImport.__init__(self, manager)
        self.filename = kwargs[u'filename']
        self.song = None
        self.commit = True

    def do_import(self):
        """
        Import either each of the files in self.filenames - each element of
        which can be either a single opensong file, or a zipfile containing
        multiple opensong files. If `self.commit` is set False, the
        import will not be committed to the database (useful for test scripts).
        """
        self.import_wizard.progressBar.setMaximum(1)
        
        log.info(u'Importing XML file %s', self.filename)
        parser = etree.XMLParser(remove_blank_text=True)
        file = etree.parse(self.filename, parser)
        xml = unicode(etree.tostring(file))
        song_xml = objectify.fromstring(xml)
        
        self.import_wizard.incrementProgressBar(
            unicode(translate('SongsPlugin.ImportWizardForm',
                u'Importing %s...')) % os.path.split(self.filename)[-1])
        self.import_wizard.progressBar.setMaximum(len(song_xml.Item))
        
        for song in song_xml.Item:
            self.import_wizard.incrementProgressBar(
                unicode(translate('SongsPlugin.ImportWizardForm',
                    u'Importing %s, song %s...')) % 
                    (os.path.split(self.filename)[-1], song.Title1))
            success = self._parse_song(song)
            if not success or self.stop_import_flag:
                return False
            if self.commit:
                self.finish()
        return True
    
    def _parse_song(self, song):
        self._success = True
        self._add_title(song)
        self._add_alttitle(song)
        self._add_number(song)
        self._add_authors(song)
        self._add_copyright(song)
        self._add_book(song)
        self._parse_and_add_lyrics(song)
        return self._success
        
    def _add_title(self, song):
        try:
            self.title = unicode(song.Title1).strip()
        except:
            log.info(u'no Title1')
            self._success = False
        
    def _add_alttitle(self, song):
        try:
            self.alternate_title = unicode(self.song.Title2).strip()
        except:
            pass
    
    def _add_number(self, song):
        try:
            number = int(song.SongNumber)
            if number != 0:
                self.song_number = number
                print number
        except:
            pass

    def _add_authors(self, song):
        try:
            authors = unicode(song.Writer).strip().split(u',')
            for author in authors:
                self.authors.append(author.strip())
        except:
            pass
            
    def _add_copyright(self, song):
        copyright = []
        try:
            copyright.append(unicode(song.Copyright).strip())
        except:
            pass
        try:
            copyright.append(unicode(song.LicenceAdmin1).strip())
        except:
            pass
        try:
            copyright.append(unicode(song.LicenceAdmin2).strip())
        except:
            pass
        self.add_copyright(u' '.join(copyright))
        
    def _add_book(self, song):
        try:
            self.song_book_name = unicode(song.BookReference).strip()
        except:
            pass
        
    def _parse_and_add_lyrics(self, song):
        try:
            lyrics = unicode(song.Contents).strip()
        except:
            log.info(u'no Contents')
            self._success = False
            
        lines = lyrics.split(u'\n')
        length = len(lines)
        
        # we go over all lines first, to determine information,
        # which tells us how to parse verses later
        emptylines = 0
        regionlines = {}
        separatorlines = 0
        for i in range(length):
            lines[i] = lines[i].strip()
            thisline = lines[i]
            if len(thisline) == 0:
                emptylines = emptylines + 1
            elif thisline[0] == u'[':
                if thisline[1:7] == u'region':
                    # this is region separator [region 2]
                    # Easislides song can have only one extra region zone,
                    # at least by now, but just in case the file happens 
                    # to have [region 3] or more, we add a possiblity to  
                    # count these separately, yeah, rather stupid, but 
                    # count this as a programming exercise
                    region = self._extractRegion(thisline)
                    if regionlines.has_key(region):
                        regionlines[region] = regionlines[region] + 1
                    else:
                        regionlines[region] = 1
                else:
                    separatorlines = separatorlines + 1
        
        # if the song has separators
        separators = (separatorlines > 0)
        # the number of different regions in song - 1
        if len(regionlines) > 1:
            log.info(u'EasiSlidesImport: the file contained a song named "%s"'
                u'with more than two regions, but only two regions are',
                u'tested, encountered regions were: %s',
                self.title, u','.join(regionlines.keys()))
        # if the song has regions
        regions = (len(regionlines) > 0)
        # if the regions are inside verses
        regionsInVerses = (regions and \
                    regionlines[regionlines.keys()[0]] > 1)
        
        verses = {}
        # list as [region, versetype, versenum, instance]
        our_verse_order = []
        defaultregion = u'1'
        reg = defaultregion
        verses[reg] = {}
        # instance differentiates occurrences of same verse tag
        inst = 1
        
        MarkTypes = {
            u'chorus': u'C',
            u'verse': u'V',
            u'intro': u'I',
            u'ending': u'E',
            u'bridge': u'B',
            u'prechorus': u'P'}

        for i in range(length):
            thisline = lines[i]
            if i < length-1:
                nextline = lines[i+1].strip()
            else:
                # there is no nextline at the last line
                nextline = False
            
            if len(thisline) == 0:
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
                    if not [reg, vt, vn, inst] in our_verse_order:
                        our_verse_order.append([reg, vt, vn, inst])
                    continue
                continue
            
            elif thisline[0:7] == u'[region':
                reg = self._extractRegion(thisline)
                if not verses.has_key(reg):
                    verses[reg] = {}
                if i == 0:
                    # the file started with [region 2]
                    vt = u'V'
                    vn = u'1'
                    our_verse_order.append([reg, vt, vn, inst])
                continue
                
            elif thisline[0] == u'[':
                # this is a normal section marker
                # drop the square brackets
                right_bracket = thisline.find(u']')
                marker = thisline[1:right_bracket].upper()
                # have we got any digits?
                # If so, versenumber is everything from the digits to the end
                match = re.match(u'(.*)(\d+.*)', marker)
                if match is not None:
                    vt = match.group(1).strip()
                    vn = match.group(2)
                    if vt == u'':
                        vt = u'V'
                    elif MarkTypes.has_key(vt.lower()):
                        vt = MarkTypes[vt.lower()]
                    else:
                        vt = u'O'
                else:
                    if marker == u'':
                        vt = u'V'
                    elif MarkTypes.has_key(marker.lower()):
                        vt = MarkTypes[marker.lower()]
                    else:
                        vt = u'O'
                    vn = u'1'
                    
                if regionsInVerses:
                    region = defaultregion
                
                inst = 1
                if self._listHas(verses, [reg, vt, vn, inst]):
                    inst = len(verses[reg][vt][vn])+1
                
                if not [reg, vt, vn, inst] in our_verse_order:
                    our_verse_order.append([reg, vt, vn, inst])
                continue
            
            if i == 0:
                # this is the first line, but no separator is found,
                # we say it's V1
                vt = u'V'
                vn = u'1'
                our_verse_order.append([reg, vt, vn, inst])
            
            # We have versetype/number data, if it was there, now
            # we parse text
            if not verses[reg].has_key(vt):
                verses[reg][vt] = {}
            if not verses[reg][vt].has_key(vn):
                verses[reg][vt][vn] = {}
            if not verses[reg][vt][vn].has_key(inst):
                verses[reg][vt][vn][inst] = []
            
            words = self.tidy_text(thisline)
            verses[reg][vt][vn][inst].append(words)
        # done parsing
        
        versetags = []
        
        # we use our_verse_order to ensure, we insert lyrics in the same order
        # as these appeared originally in the file
        
        for tag in our_verse_order:
            reg = tag[0]
            vt = tag[1]
            vn = tag[2]
            inst = tag[3]
            
            if not self._listHas(verses, [reg, vt, vn, inst]):
                continue
            versetag = u'%s%s' % (vt, vn)
            versetags.append(versetag)
            lines = u'\n'.join(verses[reg][vt][vn][inst])
            self.verses.append([versetag, lines])
        
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
                if tag[0].isdigit():
                    # it's a verse if it has no prefix, but has a number
                    tag = u'V' + tag
                elif SeqTypes.has_key(tag.lower()):
                    tag = SeqTypes[tag.lower()]
                else:
                    continue
                
                if not tag in versetags:
                    log.info(u'Got order item %s, which is not in versetags,'
                        u'dropping item from presentation order', tag)
                else:
                    self.verse_order_list.append(tag)
        except:
            pass
        
    def _listHas(self, lst, subitems):
        for i in subitems:
            if type(lst) == type({}) and lst.has_key(i):
                lst = lst[i]
            elif type(lst) == type([]) and i in lst:
                lst = lst[i]
            else:
                return False
        return True
    
    def _extractRegion(self, line):
        # this was true already: thisline[0:7] == u'[region':
        right_bracket = line.find(u']')
        return line[7:right_bracket].strip()
