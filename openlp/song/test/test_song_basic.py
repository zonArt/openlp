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
        #print r
        assert(len(l) == 21)
        
    def test_asString(self):
        """Init: Empty asString - initial values"""
        s = Song()
        r = s._get_as_string()
        flag = r.endswith("__None__None__None__None__None__None__1__1__1__1__None__None__None__None__BlankSong__None_")
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
        
    def test_Title2(self):
        """Set a titel with punctuation 1"""
        s = Song()
        t1 = "Hey! Come on, ya programmers*"
        t2 = "Hey Come on ya programmers"
        s.SetTitle(t1)
        assert(s.GetTitle() ==  t1)
        assert(s.GetSearchableTitle() ==  t2)
        
    def test_Title3(self):
        """Set a titel with punctuation 2"""
        s = Song()
        t1 = "??#Hey! Come on, ya programmers*"
        t2 = "Hey Come on ya programmers"
        s.SetTitle(t1)
        assert(s.GetTitle() ==  t1)
        assert(s.GetSearchableTitle() ==  t2)
        
    def test_Title4(self):
        """Set a title, where searchable title becomes empty - raises an exception"""
        s = Song()
        py.test.raises(SongTitleError, s.SetTitle, ",*")
        
