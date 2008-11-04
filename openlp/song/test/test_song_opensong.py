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


_sample1 = \
'''<?xml version="1.0" encoding="UTF-8"?>
<song>
  <title></title>
  <author></author>
  <copyright></copyright>
  <presentation></presentation>
  <ccli></ccli>
  <theme></theme>
  <lyrics>[V1]
. chord line 1
 verse 1 line 1
. chord line 2
 verse 1 line 2

[V2]
 verse 2 line 1
 verse 2 line 2

[V3]
 verse 3 line 1
 verse 3 line 2

[C]
. chorus chord line 1
 chorus line 1
. chorus chord line 2
 chorus line 2</lyrics>
</song>
'''

_sample2 = \
'''<?xml version="1.0" encoding="UTF-8"?>
<song>
  <title></title>
  <author></author>
  <copyright></copyright>
  <presentation></presentation>
  <ccli></ccli>
  <theme></theme>
  <lyrics>[V]
1verse 1 line 1
2verse 2 line 1
3verse 3 line 1
1verse 1 line 2
2verse 2 line 2
3verse 3 line 2

[C]
 chorus line 1
 chorus line 2</lyrics>
</song>
'''

class Test_OpenSong(object):
    """Test cases for converting from OpenSong xml format to Song"""
    
    def test_sample1(self):
        """OpenSong: handwritten sample1"""
        s = Song()
        s.FromOpenSongBuffer(_sample1)
        l = s.GetLyrics()
        assert(len(l) == (4*3+3))
        assert(s.GetNumberOfSlides() == 4)
        
    def test_sample2(self):
        """OpenSong: handwritten sample2"""
        s = Song()
        s.FromOpenSongBuffer(_sample2)
        l = s.GetLyrics()
        assert(len(l) == (4*3+3))
        assert(s.GetNumberOfSlides() == 4)
        
    def test_file1(self):
        """OpenSong: parse Amazing Grace"""
        global __ThisDir__
        s = Song()
        s.FromOpenSongFile("%s/data_opensong/Amazing Grace"%(__ThisDir__))
        assert(s.GetTitle() == "Amazing Grace")
        assert(s.GetCopyright() == "1982 Jubilate Hymns Limited")
        assert(s.GetSongCcliNo() == "1037882")
        assert(s.GetCategoryArray(True) == "God: Attributes")
        assert(s.GetAuthorList(True) == "John Newton")
        assert(s.GetVerseOrder() == "")
        assert(s.GetNumberOfSlides() == 4)
        
    def test_file2(self):
        """OpenSong: parse The Solid Rock"""
        s = Song()
        s.FromOpenSongFile("%s/data_opensong/The Solid Rock"%(__ThisDir__))
        assert(s.GetTitle() == "The Solid Rock")
        assert(s.GetCopyright() == "Public Domain")
        assert(s.GetSongCcliNo() == "101740")
        assert(s.GetCategoryArray(True) == "Christ: Victory, Fruit: Peace/Comfort")
        assert(s.GetAuthorList(True) == "Edward Mote, John B. Dykes")
        assert(s.GetVerseOrder() == "V1 C V2 C V3 C V4 C")
        assert(s.GetNumberOfSlides() == 5)
        
    def atest_file3(self):
        """OpenSong: parse 'På en fjern ensom høj' (danish)"""
        #FIXME: problem with XML convert and danish characters
        s = Song()
        s.FromOpenSongFile("%s/data_opensong/På en fjern ensom høj"%(__ThisDir__))
        assert(s.GetTitle() == "På en fjern ensom høj")
        assert(s.GetCopyright() == "")
        assert(s.GetSongCcliNo() == "")
        assert(s.GetCategoryArray(True) == "")
        assert(s.GetAuthorList(True) == "")
        assert(s.GetVerseOrder() == "V1 C1 V2 C2 V3 C3 V4 C4")
        assert(s.GetNumberOfSlides() == 8)
        
if '__main__' == __name__:
    r = Test_OpenSong()
    r.atest_file3()

