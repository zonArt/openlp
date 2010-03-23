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
import sys

__ThisDir__ = os.path.dirname(__file__)
if "" == __ThisDir__ :
    __ThisDir__ = os.path.abspath(u'.')

sys.path.append(os.path.abspath(u'%s/../../../..'%__ThisDir__))

from openlp.plugins.songs.lib.songxml import *

class Test_Text(object):
    """Test cases for converting from text format to Song"""

    def test_file1(self):
        """OpenSong: parse CCLI example"""
        global __ThisDir__
        s = Song()
        s.from_ccli_text_file(u'%s/data_text/CCLI example.txt'%(__ThisDir__))
        assert(s.get_title() == 'Song Title Here')
        assert(s.get_author_list(True) == 'Author, artist name')
        assert(s.get_copyright() == '1996 Publisher Info')
        assert(s.get_song_cclino() == '1234567')
        assert(s.get_number_of_slides() == 4)

    def test_file2(self):
        """OpenSong: parse PåEnFjern (danish)"""
        global __ThisDir__
        s = Song()
        s.from_ccli_text_file(u'%s/data_text/PåEnFjern.txt'%(__ThisDir__))
        assert(s.get_title() == 'På en fjern ensom høj')
        assert(s.get_author_list(True) == 'Georg Bennard')
        assert(s.get_copyright() == '')
        assert(s.get_song_cclino() == '')
        assert(s.get_number_of_slides() == 8)

if '__main__' == __name__:
    # for local debugging
    r = Test_Text()
    r.test_file1()
    r.test_file2()
