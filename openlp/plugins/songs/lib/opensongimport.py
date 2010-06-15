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

    or:
    <lyrics>
    1List of words
    2Some words for the 2nd Verse

    1Another Line
    2etc...
    </lyrics>

    Either or both forms can be used in one song.

    The [v1] labels can have either upper or loewr case Vs
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
        self.songmanager=songmanager
        self.song = None
        
    def do_import(self, filename):
        """
        Process the OpenSong file
        """            
        self.song = SongImport(self.songmanager)
        f=open(filename)
        tree=objectify.parse(f)
        root=tree.getroot()
        # xxx this bit ought to be more "iterable"... esp. if song had attributes not getters and setters...
        if root.copyright:
            self.song.add_copyright(unicode(root.copyright))
        if root.author:
            self.song.parse_author(unicode(root.author))
        if root.title:
            self.song.set_title(unicode(root.title))
        if root.aka:
            self.song.set_alternate_title(unicode(root.aka))
        if root.hymn_number:
            self.song.set_song_number(unicode(root.hymn_number))
        
        # data storage while importing
        verses={}
        lyrics=str(root.lyrics)
        # xxx what to do if no presentation order - need to figure it out on the fly
        for l in lyrics.split('\n'):
            # remove comments
            semicolon = l.find(';')
            if semicolon >= 0:
                l=l[:semicolon]
            l=l.strip()
            if l=='':
                continue
            # skip inline guitar chords
            if l[0] == u'.':
                continue

            # verse/chorus/etc. marker
            if l[0] == u'[':
                versetype=l[1].upper()
                if not verses.has_key(versetype):
                    verses[versetype]={}
                if l[2] != u']':
                    # there's a number to go with it - extract that as well
                    right_bracket=l.find(u']')
                    versenum=int(l[2:right_bracket])
                else:
                    versenum = None # allow error trap
                continue
            words=None

            # number at start of line => verse number
            if l[0] >= u'0' and l[0] <= u'9':
                versenum=int(l[0])
                words=l[1:].strip()
            
            if words is None and \
                   versenum is not None and \
                   versetype is not None:
                words=l
            if versenum is not None and \
                   not verses[versetype].has_key(versenum):
                verses[versetype][versenum]=[] # storage for lines in this verse
            if words:
                # remove the ____s from extended words
                words=words.replace(u'_', u'')
                verses[versetype][versenum].append(words)
        # done parsing
        print u'Title:', root.title
        versetypes=verses.keys()
        versetypes.sort()
        versetags={}
        for v in versetypes:
            versenums=verses[v].keys()
            versenums.sort()
            for n in versenums:
                versetag= u'%s%s' %(v,n)
                lines=u'\n'.join(verses[v][n])
                self.song.verses.append([versetag, lines])
                versetags[versetag]=1 # keep track of what we have for error checking later
        # now figure out the presentation order
        if root.presentation:
            order=unicode(root.presentation).split(u' ')
            for tag in order:
                if not versetags.has_key(tag):
                    raise OpenSongImportError
                else:
                    self.song.verse_order_list.append(tag)
            
        
        self.song.print_song()

