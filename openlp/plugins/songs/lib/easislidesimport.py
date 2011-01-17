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
from lxml import etree
from lxml.etree import Error, LxmlError
import re

from openlp.core.lib import translate
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

class EasiSlidesImportError(Exception):
    pass

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
        success = True
        
        self.import_wizard.importProgressBar.setMaximum(1)
        
        log.info(u'Direct import %s', self.filename)
        self.import_wizard.incrementProgressBar(
            unicode(translate('SongsPlugin.ImportWizardForm',
                u'Importing %s...')) % os.path.split(self.filename)[-1])
        file = open(self.filename)
        count = file.read().count('<Item>')
        file.seek(0)
        self.import_wizard.importProgressBar.setMaximum(count)
        self.do_import_file(file)
        
        return success

    def do_import_file(self, file):
        """
        Process the EasiSlides file - pass in a file-like object,
        not a filename
        """
        self.set_defaults()
        
        # determines, if ENTIRELY UPPERCASE lines should be converted to lower
        self.toLower = False
        # list of names, which have always to be Uppercase, like Jesus
        # only used, when self.toLower is True
        self.backToUpper = [u'Jesus', u'God']
        # determines, if title should be prepended to lyrics
        self.titleIsLyrics = False
        
        try:
            context = etree.iterparse(file)
        except (Error, LxmlError):
            log.exception(u'Error parsing XML')
            return
        
        data = {}
        for action, elem in context:
            if not elem.text:
                text = None
            else:
                text = unicode(elem.text)
            
            data[elem.tag.lower()] = text
            
            if elem.tag.lower() == u"item":
                self.parse_song(data)
                self.import_wizard.incrementProgressBar(
                    unicode(translate('SongsPlugin.ImportWizardForm',
                        u'Importing %s, song %s...')) % 
                        (os.path.split(self.filename)[-1], self.title))
                if self.commit:
                    self.finish()
                data = {}
        
    def notCapsLock(self, string):
        if self.toLower and string.upper() == string:
            ret = string.lower()
            if len(self.backToUpper) > 0:
                for repl in self.backToUpper:
                    if repl == u'':
                        continue
                    ret = ret.replace(repl.lower(), repl)
            return ret
        else:
            return string
        
    def notCapsLockTitle(self, string):
        if self.toLower and string.upper() == string:
            ret = string.lower()
            if len(self.backToUpper) > 0:
                for repl in self.backToUpper:
                    if repl == u'':
                        continue
                    ret = ret.replace(repl.lower(), repl)
            return u"%s%s" % (ret[0].upper(), ret[1:])
        else:
            return string
    
    def listHas(self, lst, subitems):
        for i in subitems:
            if type(lst) == type({}) and lst.has_key(i):
                lst = lst[i]
            elif type(lst) == type([]) and i in lst:
                lst = lst[i]
            else:
                return False
        return True
    
    def extractRegion(self, line):
        # this was true already: thisline[0:7] == u'[region':
        right_bracket = line.find(u']')
        return line[7:right_bracket].strip()
        
    def parse_song(self, data):
        # We should also check if the title is already used, if yes,
        # maybe user sould decide if we should import
        
        # set title
        self.title = self.notCapsLockTitle(data['title1'])
        
        # set alternate title, if present
        if data['title2'] != None:
            self.alternate_title = self.notCapsLockTitle(data['title2'])
            print self.alternate_title
            print data['title2']
            print "HERE HERE HERE"
        
        # folder name, we have no use for it, usually only one folder is 
        # used in easislides and this contains no actual data, easislides 
        # default database is named English, but usersmay not follow their
        # example
        # data['folder']
        
        # set song number, if present, 0 otherwise
        if data['songnumber'] != None:
            self.song_number = int(data['songnumber'])
        else:
            self.song_number = 0
        
        # Don't know how to use Notations
        # data['notations']
        
        # set song authors
        # we don't have to handle the no author case, it is done afterwards
        if data['writer'] != None:
            authors = data['writer'].split(u',')
            for author in authors:
                self.authors.append(author.strip())
        
        # set copyright data
        # licenceadmins may contain Public Domain or CCLI, as shown in examples
        # let's just concatenate these fields, it should be determined, if song
        # No is actually CCLI nr, if it is set
        copyright = []
        if data['copyright']:
            copyright.append(data['copyright'].strip())
        if data['licenceadmin1']:
            copyright.append(data['licenceadmin1'].strip())
        if data['licenceadmin2']:
            copyright.append(data['licenceadmin2'].strip())
        self.add_copyright(u' '.join(copyright))

        # set topic data, I have seen no example, and probably should not do it,
        # I even was not able to find place to set categories in easislides
        # but then again, it would not hurt either
        if data['category']:
            for topic in data['category'].split(u','):
                self.topics.append(topic.strip())

        # don't know what to do with timing data
        # may be either 3/4 or 4/4
        # data['timing']
        
        # don't know what to do with music key
        # data['musickey'], may be Db, C, G, F#, F#m
        # data['capo'], is a number from 0 to 11, determing where to
        # place a capo on guitar neck
        
        # set book data
        #if data['bookreference']:
        #    for book in data['bookreference'].split(u','):
        #        self.books.append(book.strip())
        # THIS NEEDS ATTENTION, DON'T KNOW HOW TO MAKE THIS WORK ↑ 
        
        # don't know what to do with user
        # data['userreference'], this is simple text entry, no 
        # notable restrictions, no idea what this is used for
        # U: I have seen one use of this as "searchable field" or similar,
        # still no use for us

        # there is nothing to do with formatdata, this for sure is a messy
        # thing, see an example: 
        # 21=1&gt;23=0&gt;22=2&gt;25=2&gt;26=-16777216&gt;
        # 27=-16777216&gt;28=11&gt;29=-1&gt;30=-256&gt;31=2&gt;32=2&gt;
        # 41=16&gt;42=16&gt;43=Microsoft Sans Serif&gt;
        # 44=Microsoft Sans Serif&gt;45=0&gt;46=45&gt;47=20&gt;48=40&gt;
        # 50=0&gt;51=&gt;52=50&gt;53=-1&gt;54=0&gt;55=1&gt;61=&gt;62=2&gt;
        # 63=1&gt;64=2&gt;65=2&gt;66=0&gt;71=0&gt;72=Fade&gt;73=Fade&gt;
        #
        # data['formatdata']

        # don't know what to do with settings data either, this is similar
        # nonsense as formatdata: 10=2;5;0;0;1;0;»126;232;&gt;
        # data['settings']
        
        # LYRICS LYRICS LYRICS
        # the big and messy part to handle lyrics
        lyrics = data['contents']

        # we add title to first line, if supposed to do so
        # we don't use self.title, because this may have changed case
        if self.titleIsLyrics:
            lyrics = u"%s\n%s" % (data['title1'], lyrics)

        #if lyrics.find(u'[') != -1:
        #    # this must have at least one separator
        #    match = -1
        #    while True:
        #        match = lyrics.find(u'[', match+1)
        #        if match == -1:
        #            break
        #        elif lyrics[match:match+7].lower() == u'[region':
        #            regions = regions+1
        #        else:
        #            separators = separators+1

        lines = lyrics.split(u'\n')
        length = len(lines)
        
        # we go over lines first, to determine some information,
        # which tells us how to parse verses later
        emptylines = 0
        regionlines = {}
        separatorlines = 0
        uppercaselines = 0
        notuppercaselines = 0
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
                    region = self.extractRegion(thisline)
                    if regionlines.has_key(region):
                        regionlines[region] = regionlines[region] + 1
                    else:
                        regionlines[region] = 1
                else:
                    separatorlines = separatorlines + 1
            elif thisline == thisline.upper():
                uppercaselines = uppercaselines + 1
            else:
                notuppercaselines = notuppercaselines + 1

        # if the whole song is entirely UPPERCASE
        allUpperCase = (notuppercaselines == 0)
        # if the song has separators
        separators = (separatorlines > 0)
        # the number of regions in song, conting the default as one
        regions = len(regionlines)+1
        if regions > 2:
            log.info(u'EasiSlidesImport: the file contained a song named "%s"'
                u'with more than two regions, but only two regions are',
                u'tested, all regions were: %s',
                self.title, u','.join(regionlines.keys()))
        # if the song has regions
        regions = (len(regionlines) > 1)
        # if the regions are inside verses (more than one )
        regionsInVerses = (len(regionlines) and \
                    regionlines[regionlines.keys()[0]] > 1)
        
        # data storage while importing
        verses = {}
        # keep track of a "default" verse order, in case none is specified
        # this list contains list as [region, versetype, versenum, instance]
        our_verse_order = []
        # default region
        defaultregion = u'1'
        reg = defaultregion
        verses[reg] = {}
        # instance
        inst = 1
        
        MarkTypes = {
            u'chorus': u'C',
            u'verse': u'V',
            u'intro': u'I',
            u'ending': u'E',
            u'bridge': u'B',
            u'prechorus': u'P',
            }

        for i in range(length):
            # we iterate once more over lines
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
                    if self.listHas(verses, [reg, vt, vn, inst]):
                        inst = inst + 1
                else:
                    # separators are not used, so empty line starts a new verse
                    if not allUpperCase and nextline and \
                        nextline is nextline.upper():
                        # the next line is all uppercase, it must be chorus
                        vt = u'C'
                    else:
                        # if the next line is not uppercase, 
                        # or whole song is uppercase, this must be verse
                        vt = u'V'
                    
                    # changing the region is not possible in this case

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
                reg = self.extractRegion(thisline)
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
                # If so, versenumber is everything from the digits
                # to the end (even if there are some alpha chars on the end)
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
                if self.listHas(verses, [reg, vt, vn, inst]):
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
            
            # Tidy text and remove the ____s from extended words
            words = self.tidy_text(thisline)
            words = self.notCapsLock(words)
            
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
            
            if not self.listHas(verses, [reg, vt, vn, inst]):
                continue
            versetag = u'%s%s' % (vt, vn)
            versetags.append(versetag)
            lines = u'\n'.join(verses[reg][vt][vn][inst])
            self.verses.append([versetag, lines])
        
        # Sequence keys:
        # numbers refer to verses
        # p = prechorus
        # q = prechorus 2
        # c = chorus
        # t = chorus 2
        # b = bridge
        # w = bridge 2
        # e = ending
        SeqTypes = {
            u'p': u'P1',
            u'q': u'P2',
            u'c': u'C1',
            u't': u'C2',
            u'b': u'B1',
            u'w': u'B2',
            u'e': u'E1'
            }
        # Make use of Sequence data, determining the order of verses, choruses
        # if this is not present, we don't need it either, since the
        # verses already are in the right order
        if data['sequence'] != None:
            order = data['sequence'].split(u',')
            for tag in order:
                if tag[0].isdigit():
                    # it's a verse if it has no prefix, but has a number
                    tag = u'V' + tag
                elif SeqTypes.has_key(tag.lower()):
                    tag = SeqTypes[tag.lower()]
                else:
                    # maybe we should continue here instead
                    tag = u'O1'
                
                if not tag in versetags:
                    log.info(u'Got order %s but not in versetags, dropping this'
                        u'item from presentation order', tag)
                else:
                    self.verse_order_list.append(tag)
