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
                'Importing %s...')) % os.path.split(self.filename)[-1])
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
        try:
            context = etree.iterparse(file)
        except (Error, LxmlError):
            log.exception(u'Error parsing XML')
            return
            
        song_dict = {}
        for action, elem in context:
            if not elem.text:
                text = None
            else:
                text = elem.text
            
            song_dict[elem.tag] = text
            
            if elem.tag.lower() == u"item":
                self.parse_song(song_dict)
                self.import_wizard.incrementProgressBar(
                    unicode(translate('SongsPlugin.ImportWizardForm',
                        'Importing %s, song %s...')) % 
                        (os.path.split(self.filename)[-1], self.title))
                if self.commit:
                    self.finish()
                song_dict = {}
                
    def notCapsLock(self, string):
        if string.upper() == string:
            return string.lower()
        else:
            return string

    def notCapsLockTitle(self, string):
        if string.upper() == string:
            ret = string.lower()
            return u"%s%s" % (ret[0].upper(), ret[1:])
        else:
            return string
            
    def parse_song(self, song_dict):
        #for i in song_dict:
            #if i != 'Contents' and song_dict[i] != None:
            #print u"%s = '%s'" % (i, song_dict[i])
        toLower = True
        
        title = unicode(song_dict['Title1'])
        if toLower:
            self.title = self.notCapsLockTitle(title)
        
        if song_dict['Title2'] != None:
            alttitle = unicode(song_dict['Title2'])
            if toLower:
                self.alternate_title = self.notCapsLockTitle(alttitle)
        
        if song_dict['SongNumber'] != None:
            self.song_number = int(song_dict['SongNumber'])
        else:
            self.song_number = 0

        #song_dict['Notations']
        if song_dict['Sequence'] != None:
            seq = song_dict['Sequence'].split(",")
            print seq
        
        if song_dict['Writer'] != None:
            self.authors.append(song_dict['Writer'])

        lyrics = unicode(song_dict['Contents'])
        
        titleIsFirstLine = True
        if titleIsFirstLine:
            lyrics = u"%s\n%s" % (self.title, lyrics)
            
            
        # data storage while importing
        verses = {}
        # keep track of a "default" verse order, in case none is specified
        our_verse_order = []
        verses_seen = {}
        # in the absence of any other indication, verses are the default,
        # erm, versetype!
        versetype = u'V'
        versenum = None
        seenorder = []
        
        lines = lyrics.split(u'\n')
        length = len(lines)
        
        regions = 0
        separators = 0
        if lyrics.find(u'[') != -1:
            match = -1
            while True:
                match = lyrics.find(u'[', match+1)
                if match == -1:
                    break
                if lyrics[match:match+7].lower() == u'[region':
                    regions = regions+1
                else:
                    separators = separators+1
        
        for i in range(length):
            thisline = lines[i].strip()
            if i < length-1:
                nextline = lines[i+1].strip()
                # we don't care about nextline at the last line
            else:
                nextline = False
                
                
            if len(thisline) is 0:
                if separators == 0:
                    # empty line starts a new verse or chorus
                    if nextline and nextline is nextline.upper():
                        # the next line is all uppercase, it is chorus
                        versetype = u'C'
                    else:
                        # if the next line is not uppercase, it must be verse
                        versetype = u'V'
                    
                    if verses.has_key(versetype):
                        keys = verses[versetype].keys()
                        #print keys
                        versenum = len(keys)+1
                    else:
                        versenum = u'1'
                    
                    seenorder.append([versetype, versenum])
                continue

            # verse/chorus/etc. marker
            if thisline[0] == u'[':
                if regions > 1:
                    # region markers are inside verse markers
                    if thisline[0:6] == u'[region':
                        # this is a region marker inside verse
                        # by now we do nothing
                        print 'region inside verse markers'
                        continue
                elif regions == 0:
                    # there is only one region marker
                    if thisline[0:6] == u'[region':
                        # we should restart verse count
                        # by now we do nothing
                        continue
                # this is to be handled as normal marker
                # drop the square brackets
                right_bracket = thisline.find(u']')
                content = thisline[1:right_bracket].upper()
                # have we got any digits?
                # If so, versenumber is everything from the digits
                # to the end (even if there are some alpha chars on the end)
                match = re.match(u'(.*)(\d+.*)', content)
                if match is not None:
                    versetype = match.group(1)
                    versenum = match.group(2)
                else:
                    # otherwise we assume number 1 and take the whole prefix as
                    # the versetype
                    versetype = content
                    versenum = u'1'
                seenorder.append([versetype, versenum])
                continue
            
            if i == 0:
                # this is the first line, but no separator is found,
                # let's say it's V1
                versetype = u'V'
                versenum = u'1'
                seenorder.append([versetype, versenum])
            
            words = None
            # number at start of line.. it's verse number
            if thisline[0].isdigit():
                versenum = thisline[0]
                words = thisline[1:].strip()
            if words is None:
                words = thisline
                if not versenum:
                    versenum = u'1'
            if versenum is not None:
                versetag = u'%s%s' % (versetype, versenum)
                if not verses.has_key(versetype):
                    verses[versetype] = {}
                if not verses[versetype].has_key(versenum):
                    # storage for lines in this verse
                    verses[versetype][versenum] = []
                if not verses_seen.has_key(versetag):
                    verses_seen[versetag] = 1
                    our_verse_order.append(versetag)
            if words:
                # Tidy text and remove the ____s from extended words
                words = self.tidy_text(words)
                words = words.replace('_', '')
                if toLower:
                    words = self.notCapsLock(words)
                    
                verses[versetype][versenum].append(words)
        # done parsing

        versetypes = verses.keys()
        versetags = {}

        for tag in seenorder:
            vtype = tag[0]
            vnum = tag[1]
            
            if not vtype in verses:
                # something may have gone wrong
                continue
            if not vnum in verses[vtype]:
                # this most likely is caused by an extra empty line at the end,
                # to be debugged later
                continue
            versetag = u'%s%s' % (vtype, vnum)
            lines = u'\n'.join(verses[vtype][vnum])
            self.verses.append([versetag, lines])
        
        if song_dict['Sequence'] != None:
            order = song_dict['Sequence'].split(u',')
            for tag in order:
                if tag[0].isdigit():
                    # Assume it's a verse if it has no prefix
                    tag = u'V' + tag
                elif not re.search('\d+', tag):
                    # Assume it's no.1 if there's no digits
                    tag = tag + u'1'
                if not versetags.has_key(tag):
                    log.info(u'Got order %s but not in versetags, dropping this'
                        u'item from presentation order', tag)
                else:
                    self.verse_order_list.append(tag)
        else:
            for tag in seenorder:
                self.verse_order_list.append(u'%s%s' % (tag[0], tag[1]))
