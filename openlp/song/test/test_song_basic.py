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

class Test_Basic(object):
    """Class for first initialization check
    set-get functions
    """
    
    def test_Creation(self):
        """Init: Create as empty"""
        s = Song()
        assert(True)
        
    def test_str(self):
        """Init: Empty, use __str__ to count public attributes & methods"""
        s = Song()
        r = s.__str__()
        l = r.split("\n")
        assert(len(l) == 55)
        
    def test_asString(self):
        """Init: Empty asString - initial values"""
        s = Song()
        r = s._get_as_string()
        #print r
        flag = r.endswith("__None__None__None__None__None__None__1__1__1__1__[]__None__None__None__None__BlankSong__None_")
        assert(flag)
        
    def test_Title1(self):
        """Set an empty title - raises an exception"""
        s = Song()
        py.test.raises(SongTitleError, s.SetTitle, "")
        
    def test_Title2(self):
        """Set a normal title"""
        s = Song()
        t = "A normal title"
        s.SetTitle(t)
        assert(s.GetTitle() ==  t)
        assert(s.GetSearchableTitle() ==  t)
        
    def test_Title3(self):
        """Set a titel with punctuation 1"""
        s = Song()
        t1 = "Hey! Come on, ya programmers*"
        t2 = "Hey Come on ya programmers"
        s.SetTitle(t1)
        assert(s.GetTitle() ==  t1)
        assert(s.GetSearchableTitle() ==  t2)
        
    def test_Title4(self):
        """Set a titel with punctuation 2"""
        s = Song()
        t1 = "??#Hey! Come on, ya programmers*"
        t2 = "Hey Come on ya programmers"
        s.SetTitle(t1)
        assert(s.GetTitle() ==  t1)
        assert(s.GetSearchableTitle() ==  t2)
        
    def test_Title5(self):
        """Set a title, where searchable title becomes empty - raises an exception"""
        s = Song()
        py.test.raises(SongTitleError, s.SetTitle, ",*")
        
    def test_Copyright(self):
        """Set a copyright string"""
        s = Song()
        assert(s.GetCopyright() == "")
        s.SetCopyright("A B Car")
        assert(s.GetCopyright() == "A B Car")
        
    def test_SongCclino(self):
        """Set a SongCcliNo"""
        s = Song()
        assert(s.GetSongCcliNo() == "")
        s.SetSongCcliNo(12345)
        assert(s.GetSongCcliNo() == "12345")
        
    def test_SongBook(self):
        """Set a songbook value"""
        s = Song()
        assert(s.GetSongBook() == "")
        s.SetSongBook("Hymns")
        assert(s.GetSongBook() == "Hymns")
        
    def test_SongNumber(self):
        """Set a song number"""
        s = Song()
        assert(s.GetSongNumber() == "")
        s.SetSongNumber(278)
        assert(s.GetSongNumber() == "278")
        
    def test_Theme(self):
        """Set a theme name"""
        s = Song()
        assert(s.GetTheme() == "")
        s.SetTheme("Red")
        assert(s.GetTheme() == "Red")
        
    def test_VerseOrder(self):
        """Set a verse order"""
        s = Song()
        assert(s.GetVerseOrder() == "")
        s.SetVerseOrder("V1 C V2")
        assert(s.GetVerseOrder() == "V1 C V2")
        
    def test_Comments(self):
        """Set a comment"""
        s = Song()
        assert(s.GetComments() == "")
        s.SetComments("a comment")
        assert(s.GetComments() == "a comment")
        
    def test_AuthorList(self):
        """Set author lists"""
        s = Song()
        assert(s.GetAuthorList(True) == "")
        assert(s.GetAuthorList(False) == [])
        t1 = "John Newton"
        s.SetAuthorList(t1)
        assert(s.GetAuthorList(True) == t1)
        assert(s.GetAuthorList(False) == [t1])
        s.SetAuthorList("  Peter Done  , John Newton")
        assert(s.GetAuthorList(True)== "Peter Done, John Newton")
        assert(s.GetAuthorList(False) == ["Peter Done", "John Newton"])
        s.SetAuthorList(None)
        assert(s.GetAuthorList(True) == "")
        assert(s.GetAuthorList(False) == [])
        s.SetAuthorList("")
        assert(s.GetAuthorList(True) == "")
        assert(s.GetAuthorList(False) == [""])
        s.SetAuthorList([])
        assert(s.GetAuthorList(True) == "")
        assert(s.GetAuthorList(False) == [""])
        
    def test_CategoryArray(self):
        """Set categories"""
        s = Song()
        assert(s.GetCategoryArray(True) == "")
        assert(s.GetCategoryArray(False) == [])
        t1 = "Gospel"
        s.SetCategoryArray(t1)
        assert(s.GetCategoryArray(True) == t1)
        assert(s.GetCategoryArray(False) == [t1])
        s.SetCategoryArray(" Gospel,  Hymns  ")
        assert(s.GetCategoryArray(True) == "Gospel, Hymns")
        assert(s.GetCategoryArray(False) == ["Gospel", "Hymns"])
        s.SetCategoryArray(None)
        assert(s.GetCategoryArray(True) == "")
        assert(s.GetCategoryArray(False) == [])
        s.SetCategoryArray("")
        assert(s.GetCategoryArray(True) == "")
        assert(s.GetCategoryArray(False) == [""])
        s.SetCategoryArray([])
        assert(s.GetCategoryArray(True) == "")
        assert(s.GetCategoryArray(False) == [""])
        
if '__main__' == __name__:
    r = Test_Basic()
    r.test_asString()
