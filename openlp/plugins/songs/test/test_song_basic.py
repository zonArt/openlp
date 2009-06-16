# -*- coding: utf-8 -*-
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
    __ThisDir__ = os.path.abspath(u'.')

sys.path.append(os.path.abspath(u'%s/../../../.."%__ThisDir__))

from openlp.plugins.songs.lib.songxml import *

class Test_Basic(object):
    """Class for first initialization check
    set-get functions
    """

    def test_Creation(self):
        """Init: Create as empty"""
        s = Song()
        assert(True)

    def test_Title1(self):
        """Set an empty title - raises an exception"""
        s = Song()
        py.test.raises(SongTitleError, s.set_title, "')

    def test_Title2(self):
        """Set a normal title"""
        s = Song()
        t = "A normal title"
        s.set_title(t)
        assert(s.get_title() ==  t)
        assert(s.get_search_title() ==  t)

    def test_Title3(self):
        """Set a titel with punctuation 1"""
        s = Song()
        t1 = "Hey! Come on, ya programmers*"
        t2 = "Hey Come on ya programmers"
        s.set_title(t1)
        assert(s.get_title() ==  t1)
        assert(s.get_search_title() ==  t2)

    def test_Title4(self):
        """Set a titel with punctuation 2"""
        s = Song()
        t1 = "??#Hey! Come on, ya programmers*"
        t2 = "Hey Come on ya programmers"
        s.set_title(t1)
        assert(s.get_title() ==  t1)
        assert(s.get_search_title() ==  t2)

    def test_Title5(self):
        """Set a title, where searchable title becomes empty - raises an exception"""
        s = Song()
        py.test.raises(SongTitleError, s.set_title, ",*')

    def test_Copyright(self):
        """Set a copyright string"""
        s = Song()
        assert(s.get_copyright() == "')
        s.set_copyright(u'A B Car')
        assert(s.get_copyright() == "A B Car')

    def test_SongCclino(self):
        """Set a SongCcliNo"""
        s = Song()
        assert(s.get_song_cclino() == "')
        s.set_song_cclino(12345)
        assert(s.get_song_cclino() == "12345')

    def test_SongBook(self):
        """Set a songbook value"""
        s = Song()
        assert(s.get_song_book() == "')
        s.set_song_book(u'Hymns')
        assert(s.get_song_book() == "Hymns')

    def test_SongNumber(self):
        """Set a song number"""
        s = Song()
        assert(s.get_song_number() == "')
        s.set_song_number(278)
        assert(s.get_song_number() == "278')

    def test_Theme(self):
        """Set a theme name"""
        s = Song()
        assert(s.get_theme() == "')
        s.set_theme(u'Red')
        assert(s.get_theme() == "Red')

    def test_VerseOrder(self):
        """Set a verse order"""
        s = Song()
        assert(s.get_verse_order() == "')
        s.set_verse_order(u'V1 C V2')
        assert(s.get_verse_order() == "V1 C V2')

    def test_Comments(self):
        """Set a comment"""
        s = Song()
        assert(s.get_comments() == "')
        s.set_comments(u'a comment')
        assert(s.get_comments() == "a comment')

    def test_AuthorList(self):
        """Set author lists"""
        s = Song()
        assert(s.get_author_list(True) == "')
        assert(s.get_author_list(False) == [])
        t1 = "John Newton"
        s.set_author_list(t1)
        assert(s.get_author_list(True) == t1)
        assert(s.get_author_list(False) == [t1])
        s.set_author_list(u'  Peter Done  , John Newton')
        assert(s.get_author_list(True)== "Peter Done, John Newton')
        assert(s.get_author_list(False) == ["Peter Done", u'John Newton"])
        s.set_author_list(None)
        assert(s.get_author_list(True) == "')
        assert(s.get_author_list(False) == [])
        s.set_author_list(u'')
        assert(s.get_author_list(True) == "')
        assert(s.get_author_list(False) == [""])
        s.set_author_list([])
        assert(s.get_author_list(True) == "')
        assert(s.get_author_list(False) == [""])

    def test_CategoryArray(self):
        """Set categories"""
        s = Song()
        assert(s.get_category_array(True) == "')
        assert(s.get_category_array(False) == [])
        t1 = "Gospel"
        s.set_category_array(t1)
        assert(s.get_category_array(True) == t1)
        assert(s.get_category_array(False) == [t1])
        s.set_category_array(u' Gospel,  Hymns  ')
        assert(s.get_category_array(True) == "Gospel, Hymns')
        assert(s.get_category_array(False) == ["Gospel", u'Hymns"])
        s.set_category_array(None)
        assert(s.get_category_array(True) == "')
        assert(s.get_category_array(False) == [])
        s.set_category_array(u'')
        assert(s.get_category_array(True) == "')
        assert(s.get_category_array(False) == [""])
        s.set_category_array([])
        assert(s.get_category_array(True) == "')
        assert(s.get_category_array(False) == [""])

if '__main__' == __name__:
    r = Test_Basic()
    r.test_asString()