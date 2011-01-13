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
        
        # determines, if ENTIRELY UPPERCASE lines should be converted to lower
        self.toLower = True
        # determines, if title should be prepended to lyrics
        self.titleIsLyrics = True

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
                        'Importing %s, song %s...')) % 
                        (os.path.split(self.filename)[-1], self.title))
                if self.commit:
                    self.finish()
                data = {}
                
    def notCapsLock(self, string):
        if self.toLower and string.upper() == string:
            return string.lower()
        else:
            return string

    def notCapsLockTitle(self, string):
        if self.toLower and string.upper() == string:
            ret = string.lower()
            return u"%s%s" % (ret[0].upper(), ret[1:])
        else:
            return string
            
    def parse_song(self, data):
        # We should also check if the title is already used, if yes,
        # maybe user sould decide if we should import
        
        # set title
        self.title = self.notCapsLockTitle(data['title1'])
        
        # set alternate title, if present
        if data['title2'] != None:
            self.alternate_title = self.notCapsLockTitle(data['title2'])
        
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
        self.add_copyright(" ".join(copyright))

        # set topic data, I have seen no example, and should not use it,
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
        if data['bookreference']:
            for book in data['bookreference'].split(u','):
                self.books.append(book.strip())

        # don't know what to do with user
        # data['userreference'], this is simple text entry, no 
        # notable restrictions

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
        # nonsense: 10=2;5;0;0;1;0;»126;232;&gt;
        # data['settings']

        # LYRICS LYRICS LYRICS
        # the big and messy part to handle lyrics
        lyrics = data['contents']

        # we add title to first line, if supposed to do so
        if self.titleIsLyrics:
            lyrics = u"%s\n%s" % (self.title, lyrics)
        
        # we count the [region 2] and [whatever] separartors,  to be able
        # to tell how region data is used
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

        # data storage while importing
        verses = {}
        # keep track of a "default" verse order, in case none is specified
        our_verse_order = []

        lines = lyrics.split(u'\n')
        length = len(lines)        
        for i in range(length):
            thisline = lines[i].strip()
            if i < length-1:
                nextline = lines[i+1].strip()
            else:
                # there is no nextline at the last line
                nextline = False
                
            if len(thisline) is 0:
                if separators == 0:
                    # empty line starts a new verse or chorus
                    if nextline and nextline is nextline.upper():
                        # the next line is all uppercase, it must be chorus
                        versetype = u'C'
                    else:
                        # if the next line is not uppercase, it must be verse
                        versetype = u'V'
                    
                    if verses.has_key(versetype):
                        versenum = len(verses[versetype].keys())+1
                    else:
                        versenum = u'1'
                    
                    our_verse_order.append([versetype, versenum])
                else:
                    # separators are not used, something must be done
                    continue
                continue
            
            # verse/chorus/etc. marker, this line contains no other data
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
                    # versetype normally is one of the following:
                    # not set for verse (only number)
                    # prechorus (p), chorus (c), bridge (w), 
                    # ending, none of these is numbered in sequence
                    # empty line means split screen
                    versetype = match.group(1)
                    versenum = match.group(2)
                else:
                    # otherwise we assume number 1 and take the whole prefix as
                    # the versetype
                    versetype = content
                    versenum = u'1'
                our_verse_order.append([versetype, versenum])
                continue

            if i == 0:
                # this is the first line, but still no separator is found,
                # we say it's V1
                versetype = u'V'
                versenum = u'1'
                our_verse_order.append([versetype, versenum])
            
            # We have versetype/number data, if it was there, now
            # we parse text
            if not verses.has_key(versetype):
                verses[versetype] = {}
            if not verses[versetype].has_key(versenum):
                verses[versetype][versenum] = []
            
            # Tidy text and remove the ____s from extended words
            words = self.tidy_text(thisline)
            words = words.replace('_', '')
            words = self.notCapsLock(words)
            
            verses[versetype][versenum].append(words)
        # done parsing
        
        # we use our_verse_order to ensure, we insert lyrics in the same order
        # as these appeared originally in the file
        for tag in our_verse_order:
            versetype = tag[0]
            versenum = tag[1]
            
            if not versetype in verses:
                # something may have gone wrong
                continue
            if not versenum in verses[versetype]:
                # this most likely is caused by an extra empty line at the end,
                # to be debugged later
                continue
            versetag = u'%s%s' % (versetype, versenum)
            lines = u'\n'.join(verses[versetype][versenum])
            self.verses.append([versetag, lines])
        
        # Make use of Sequence data, determining the order of verses, choruses
        if data['sequence'] != None:
            order = data['sequence'].split(u',')
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
            for tag in our_verse_order:
                if not tag[0] in verses:
                    #log.info(u'Got order from our_verse_order %s but not in'
                    #    u'versetags, dropping this item from presentation order'
                    #    u'missing was versetag %s', tag, tag[0])
                    continue
                if not tag[1] in verses[tag[0]]:
                    #log.info(u'Got order from our_verse_order %s but not in'
                    #    u'versetags, dropping this item from presentation order'
                    #    u'missing was versenum %s for versetag %s',
                    #    tag, tag[1], tag[0])
                    continue
                self.verse_order_list.append(u'%s%s' % (tag[0], tag[1]))
