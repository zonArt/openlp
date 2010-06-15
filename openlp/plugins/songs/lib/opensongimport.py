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

# from songimport import SongImport

class opensongimport:
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
        
    def osimport(self, filename):
        """
        Process the OpenSong file
        """            
        self.new_song()
        f=open(filename)
        tree=objectify.parse(f)
        root=tree.getroot()
        print "Title", zroot.title
        # data storage while importing
        self.verses=[]
        

        # xxx this is common with SOF
    def new_song(self):
        """
        A change of song. Store the old, create a new
        ... but only if the last song was complete. If not, stick with it
        """
        if self.song:
            self.finish_verse()
            if not self.song.check_complete():
                return
            self.song.finish()

        self.song = SongImport(self.manager)
        self.skip_to_close_bracket = False
        self.is_chorus = False
        self.italics = False
        self.currentverse = u''
        

