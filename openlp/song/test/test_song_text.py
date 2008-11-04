# -*- coding:iso-8859-1 -*-
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

import os
import sys
sys.path.append(os.path.abspath("./../../.."))
from openlp.song import *

__ThisDir__ = os.path.abspath(".")

class Test_Text(object):
    """Test cases for converting from text format to Song"""
    
    def test_file1(self):
        """OpenSong: parse CCLI example"""
        global __ThisDir__
        s = Song()
        s.FromTextFile("%s/data_text/CCLI example.txt"%(__ThisDir__))
        assert(s.GetTitle() == "Song Title Here")
        assert(s.GetAuthorList(True) == "Author, artist name")
        assert(s.GetCopyright() == "1996 Publisher Info")
        assert(s.GetSongCcliNo() == "1234567")
        assert(s.GetNumberOfSlides() == 4)
        
    def test_file2(self):
        """OpenSong: parse PåEnFjern (danish)"""
        global __ThisDir__
        s = Song()
        s.FromTextFile("%s/data_text/PåEnFjern.txt"%(__ThisDir__))
        assert(s.GetTitle() == "På en fjern ensom høj")
        assert(s.GetAuthorList(True) == "Georg Bennard")
        assert(s.GetCopyright() == "")
        assert(s.GetSongCcliNo() == "")
        assert(s.GetNumberOfSlides() == 8)

if '__main__' == __name__:
    # for local debugging
    r = Test_Text()
    r.test_file1()
    r.test_file2()

