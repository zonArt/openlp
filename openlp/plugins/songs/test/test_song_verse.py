# -*- coding:iso-8859-1 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley, Carsten Tinggaard

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

__ThisDir__ = os.path.dirname(__file__)
if "" == __ThisDir__ :
    __ThisDir__ = os.path.abspath(".")

sys.path.append(os.path.abspath("%s/../../../.."%__ThisDir__))

from openlp.plugins.songs.lib.songxml import *

class Test_Verse(object):
    """Class for testing verses for preview and review"""
    
    def stdSong(self):
        """Definition of a standard song"""
        s = Song()
        self.title = "A song"
        self.author = "John Newton"
        self.copyright = "Peter Hamil"
        self.ccli = "123456"
        s.set_lyrics(["# verse","a single line"])
        s.set_title(self.title)
        s.set_copyright(self.copyright)
        s.set_author_list(self.author)
        s.set_song_cclino(self.ccli)
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
        r = s.get_render_slide(1)
        self.check_allfields(r)
        s.set_show_title(False)
        r = s.get_render_slide(1)
        self.check_allfields(r, 1)
        s.set_show_title(True)
        r = s.get_render_slide(1)
        self.check_allfields(r)
    
    def test_author_show_noshow(self):
        """Test the show author flag"""
        s = self.stdSong()
        r = s.get_render_slide(1)
        self.check_allfields(r)
        s.set_show_author_list(False)
        r = s.get_render_slide(1)
        self.check_allfields(r, 2)
        s.set_show_author_list(True)
        r = s.get_render_slide(1)
        self.check_allfields(r)
    
    def test_copyright_show_noshow(self):
        """Test the show copyright flag"""
        s = self.stdSong()
        r = s.get_render_slide(1)
        self.check_allfields(r)
        s.set_show_copyright(False)
        r = s.get_render_slide(1)
        self.check_allfields(r, 3)
        s.set_show_copyright(True)
        r = s.get_render_slide(1)
        self.check_allfields(r)
    
    def test_ccli_show_noshow(self):
        """Test the show copyright flag"""
        s = self.stdSong()
        r = s.get_render_slide(1)
        self.check_allfields(r)
        s.set_show_song_cclino(False)
        r = s.get_render_slide(1)
        self.check_allfields(r, 4)
        s.set_show_song_cclino(True)
        r = s.get_render_slide(1)
        self.check_allfields(r)
        
    def test_verse1(self):
        """Test an empty verse list"""
        s = Song()
        s.set_lyrics([])
        assert(s.get_number_of_slides() == 0)
        
    def test_verse2(self):
        """Test a list with an empty string"""
        s = Song()
        s.set_lyrics([""])
        assert(s.get_number_of_slides() == 0)
        
    def test_verse3a(self):
        """Test a one liner song"""
        s = Song()
        s.set_lyrics(["Single verse"])
        assert(s.get_number_of_slides() == 1)
        
    def test_verse3b(self):
        """Test a one liner song"""
        s = Song()
        s.set_lyrics(["", "Single verse"])
        assert(s.get_number_of_slides() == 1)
        
    def test_verse3c(self):
        """Test a one liner song"""
        s = Song()
        s.set_lyrics(["", "Single verse", "", ""])
        assert(s.get_number_of_slides() == 1)

    def test_verse3d(self):
        """Test a one liner song"""
        s = Song()
        s.set_lyrics(["", "# Verse", "", ""])
        assert(s.get_number_of_slides() == 1)
        