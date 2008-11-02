"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Carsten Tinggaard

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

import py.test
import os
import sys
sys.path.append(os.path.abspath("./../../.."))

from openlp.song import *

class Test_Verse(object):
    """Class for testing verses for preview and review"""
    
    def stdSong(self):
        """Definition of a standard song"""
        s = Song()
        self.title = "A song"
        self.author = "John Newton"
        self.copyright = "Peter Hamil"
        self.ccli = "123456"
        s.SetLyrics(["# verse","a single line"])
        s.SetTitle(self.title)
        s.SetCopyright(self.copyright)
        s.SetAuthorList(self.author)
        s.SetSongCcliNo(self.ccli)
        return s
    
    def check_allfields(self, r, isblank = 0):
        #[theme, title, author, cpright, ccli, lyrics]
        if isblank == 1 :
            assert(r[1] == "")
        else :
            assert(r[1] == self.title)
        if isblank == 2 :
            assert(r[2] == "")
        else :
            assert(r[2] == self.author)
        if isblank == 3 :
            assert(r[3] == "")
        else :
            assert(r[3] == self.copyright)
        if isblank == 4 :
            assert(r[4] == "")
        else :
            assert(r[4] == self.ccli)
        
    
    def test_title_show_noshow(self):
        """Test the show title flag"""
        s = self.stdSong()
        r = s.GetRenderVerse(1)
        self.check_allfields(r)
        s.SetShowTitle(False)
        r = s.GetRenderVerse(1)
        self.check_allfields(r, 1)
        s.SetShowTitle(True)
        r = s.GetRenderVerse(1)
        self.check_allfields(r)
    
    def test_author_show_noshow(self):
        """Test the show author flag"""
        s = self.stdSong()
        r = s.GetRenderVerse(1)
        self.check_allfields(r)
        s.SetShowAuthorList(False)
        r = s.GetRenderVerse(1)
        self.check_allfields(r, 2)
        s.SetShowAuthorList(True)
        r = s.GetRenderVerse(1)
        self.check_allfields(r)
    
    def test_copyright_show_noshow(self):
        """Test the show copyright flag"""
        s = self.stdSong()
        r = s.GetRenderVerse(1)
        self.check_allfields(r)
        s.SetShowCopyright(False)
        r = s.GetRenderVerse(1)
        self.check_allfields(r, 3)
        s.SetShowCopyright(True)
        r = s.GetRenderVerse(1)
        self.check_allfields(r)
    
    def test_ccli_show_noshow(self):
        """Test the show copyright flag"""
        s = self.stdSong()
        r = s.GetRenderVerse(1)
        self.check_allfields(r)
        s.SetShowSongCcliNo(False)
        r = s.GetRenderVerse(1)
        self.check_allfields(r, 4)
        s.SetShowSongCcliNo(True)
        r = s.GetRenderVerse(1)
        self.check_allfields(r)
        