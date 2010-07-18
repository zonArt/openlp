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

from zipfile import ZipFile

from lxml.etree import Element
from lxml import objectify

from openlp.plugins.songs.lib.songimport import SongImport

import logging
log = logging.getLogger(__name__)

class OpenSongImportError(Exception):
    pass

class OpenSongImport(object):
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

    Either or both forms can be used in one song.  The Number does not
    necessarily appear at the start of the line

    The [v1] labels can have either upper or lower case Vs
    Other labels can be used also:
      C - Chorus
      B - Bridge

    Guitar chords can be provided 'above' the lyrics (the line is
    preceeded by a'.') and _s can be used to signify long-drawn-out
    words:

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
        Initialise the class. Requires a songmanager class which 
        is passed to SongImport for writing song to disk
        """
        self.songmanager = songmanager
        self.song = None

    def do_import(self, filename, commit=True):
        """
        Import either a single opensong file, or a zipfile
        containing multiple opensong files If the commit parameter is
        set False, the import will not be committed to the database
        (useful for test scripts)
        """
        ext = os.path.splitext(filename)[1]
        if ext.lower() == ".zip":
            log.info('Zipfile found %s', filename)
            z = ZipFile(filename, u'r')
            for song in z.infolist():
                parts = os.path.split(song.filename)
                if parts[-1] == u'':
                    #No final part => directory
                    continue
                songfile = z.open(song)
                self.do_import_file(songfile)
                if commit:
                    self.finish()
        else:
            log.info('Direct import %s', filename)
            file = open(filename)
            self.do_import_file(file)
            if commit:
                self.finish()

   
    def do_import_file(self, file):
        """
        Process the OpenSong file - pass in a file-like object,
        not a filename
        """            
        self.song_import = SongImport(self.songmanager)
        tree = objectify.parse(file)
        root = tree.getroot()
        fields = dir(root)
        decode = {u'copyright':self.song_import.add_copyright,
                u'ccli':u'ccli_number',
                u'author':self.song_import.parse_author,
                u'title':u'title',
                u'aka':u'alternate_title',
                u'hymn_number':u'song_number'}
        for (attr, fn_or_string) in decode.items():
            if attr in fields:
                ustring = unicode(root.__getattr__(attr))
                if type(fn_or_string) == type(u''):
                    self.song_import.__setattr__(fn_or_string, ustring)
                else:
                    fn_or_string(ustring)

        res = []
        if u'theme' in fields:
            self.song_import.topics.append(unicode(root.theme))
        if u'alttheme' in fields:
            self.song_import.topics.append(unicode(root.alttheme))
        # data storage while importing
        verses = {}
        lyrics = unicode(root.lyrics)
        # keep track of a "default" verse order, in case none is specified
        our_verse_order = []
        verses_seen = {}
        # in the absence of any other indication, verses are the default,
        # erm, versetype!
        versetype = u'V'
        for thisline in lyrics.split(u'\n'):
            # remove comments
            semicolon = thisline.find(u';')
            if semicolon >= 0:
                thisline = thisline[:semicolon]
            thisline = thisline.strip()
            if len(thisline) == 0:
                continue
            # skip inthisline guitar chords and page and column breaks
            if thisline[0] == u'.' or thisline.startswith(u'---') \
                or thisline.startswith(u'-!!'):
                continue
            
            # verse/chorus/etc. marker
            if thisline[0] == u'[':
                versetype = thisline[1].upper()
                if versetype.isdigit():
                    versenum = versetype
                    versetype = u'V'
                elif thisline[2] != u']':
                    # there's a number to go with it - extract that as well
                    right_bracket = thisline.find(u']')
                    versenum = thisline[2:right_bracket]
                else:
                    # if there's no number, assume it's no.1
                    versenum = u'1'
                continue
            words = None

            # number at start of line.. it's verse number
            if thisline[0].isdigit():
                versenum = thisline[0]
                words = thisline[1:].strip()
            if words is None and \
                   versenum is not None and \
                   versetype is not None:
                words = thisline
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
                words = self.song_import.tidy_text(words)
                words = words.replace('_', '')
                verses[versetype][versenum].append(words)
        # done parsing
        versetypes = verses.keys()
        versetypes.sort()
        versetags = {}
        verse_renames = {}
        for versetype in versetypes:
            versenums = verses[versetype].keys()
            versenums.sort()
            for num in versenums:
                versetag = u'%s%s' %(versetype,num)
                lines = u'\n'.join(verses[versetype][num])
                self.song_import.verses.append([versetag, lines])
                versetags[versetag] = 1 # keep track of what we have for error checking later
        # now figure out the presentation order
        if u'presentation' in fields and root.presentation != u'':
            order = unicode(root.presentation)
            order = order.split()
        else:
            assert len(our_verse_order)>0
            order = our_verse_order
        for tag in order:
            if len(tag) == 1:
                tag = tag + u'1' # Assume it's no.1 if it's not there
            if not versetags.has_key(tag):
                log.warn(u'Got order %s but not in versetags, skipping', tag)
            else:
                self.song_import.verse_order_list.append(tag)
    def finish(self):
        """ Separate function, allows test suite to not pollute database"""
        self.song_import.finish()
