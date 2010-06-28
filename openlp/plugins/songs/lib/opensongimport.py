# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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
import re

from songimport import SongImport
from lxml.etree import Element
from lxml import objectify

class OpenSongImportError(Exception):
    pass

class OpenSongImport:
    """
    Import songs exported from OpenSong - the format is described loosly here:
    http://www.opensong.org/d/manual/song_file_format_specification

    However, it doesn't describe the <lyrics> section, so here's an attempt:

    Verses can be expressed in one of 2 ways:
    <lyrics>
    [v1]List of words
    Another Line

    [v2]Some words for the 2nd verse
    etc...
    </lyrics>

    The 'v' can be left out - it is implied
    or:
    <lyrics>
    [V]
    1List of words
    2Some words for the 2nd Verse

    1Another Line
    2etc...
    </lyrics>

    Either or both forms can be used in one song.  The Number does not necessarily appear at the start of the line

    The [v1] labels can have either upper or lower case Vs
    Other labels can be used also:
      C - Chorus
      B - Bridge

    Guitar chords can be provided 'above' the lyrics (the line is preceeded by a'.') and _s can be used to signify long-drawn-out words:

    . A7        Bm
    1 Some____ Words

    Chords and _s are removed by this importer.

    The verses etc. are imported and tagged appropriately.

    The <presentation> tag is used to populate the OpenLP verse
    display order field.  The Author and Copyright tags are also
    imported to the appropriate places.

    """
    def __init__(self, songmanager):
        """
        Initialise the class. Requires a songmanager class which is passed
        to SongImport for writing song to disk
        """
        self.songmanager = songmanager
        self.song = None

    def do_import(self, filename):
        file = open(filename)
        self.do_import_file(file)
        
    def do_import_file(self, file):
        """
        Process the OpenSong file
        """            
        self.song = SongImport(self.songmanager)
        tree = objectify.parse(file)
        root = tree.getroot()
        fields = dir(root)
        decode = {u'copyright':self.song.add_copyright,
                u'author':self.song.parse_author,
                u'title':self.song.set_title,
                u'aka':self.song.set_alternate_title,
                u'hymn_number':self.song.set_song_number}
        for (attr, fn) in decode.items():
            if attr in fields:
                fn(unicode(root.__getattr__(attr)))
        
        # data storage while importing
        verses = {}
        lyrics = unicode(root.lyrics)
        # keep track of a "default" verse order, in case none is specified
        our_verse_order = []
        verses_seen = {}
        # in the absence of any other indication, verses are the default, erm, versetype!
        versetype = u'V'
        for l in lyrics.split(u'\n'):
            # remove comments
            semicolon = l.find(u';')
            if semicolon >= 0:
                l = l[:semicolon]
            l = l.strip()
            if len(l) == 0:
                continue
            # skip inline guitar chords
            if l[0] == u'.':
                continue
            
            # verse/chorus/etc. marker
            if l[0] == u'[':
                versetype = l[1].upper()
                if versetype.isdigit():
                    versenum = versetype
                    versetype = u'V'
                elif l[2] != u']':
                    # there's a number to go with it - extract that as well
                    right_bracket = l.find(u']')
                    versenum = l[2:right_bracket]
                else:
                    versenum = u''
                continue
            words=None

            # number at start of line.. it's verse number
            if l[0].isdigit():
                versenum = l[0]
                words = l[1:].strip()
            if words is None and \
                   versenum is not None and \
                   versetype is not None:
                words=l
            if versenum is not None:
                versetag = u'%s%s'%(versetype,versenum)
                if not verses.has_key(versetype):
                    verses[versetype] = {}
                if not verses[versetype].has_key(versenum):
                    verses[versetype][versenum] = [] # storage for lines in this verse
                if not verses_seen.has_key(versetag):
                    verses_seen[versetag] = 1
                    our_verse_order.append(versetag)
            if words:
                # Tidy text and remove the ____s from extended words
                # words=self.song.tidy_text(words)
                words=words.replace('_', '')
                verses[versetype][versenum].append(words)
        # done parsing
        versetypes = verses.keys()
        versetypes.sort()
        versetags = {}
        for v in versetypes:
            versenums = verses[v].keys()
            versenums.sort()
            for n in versenums:
                versetag = u'%s%s' %(v,n)
                lines = u'\n'.join(verses[v][n])
                self.song.verses.append([versetag, lines])
                versetags[versetag] = 1 # keep track of what we have for error checking later
        # now figure out the presentation order
        if u'presentation' in fields and root.presentation != u'':
            order = unicode(root.presentation)
            order = order.split()
        else:
            assert len(our_verse_order)>0
            order = our_verse_order
        for tag in order:
            if not versetags.has_key(tag):
                print u'Got order', tag, u'but not in versetags, skipping'
                raise OpenSongImportError # xxx keep error, or just warn?
            else:
                self.song.verse_order_list.append(tag)
    def finish(self):
        """ Separate function, allows test suite to not pollute database"""
        self.song.finish()
