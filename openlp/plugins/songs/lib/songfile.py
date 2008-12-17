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

import sys
import os
from songxml import *


class SongFile(object):
    """Class for handling the song file"""
    
    def __init__(self, fileUrl):
        """Initialize the song file
        
        fileUrl -- full path and name to the song file
        """
        self.filename = fileUrl


class SongFileVersion1(object):
    """Class for handling OpenLP 1.xx olp file
    
    The SQLite file contains these tables:
      authors(authorid, authorname)  # unique author list
      songauthors(authorid, songid)  # m-to-m relation 
      songs(songid, songtitle, lyrics, copyrightinfo, settingsid) # unique song list
    """
    
    def __init__(self, fileUrl):
        """Initialize the song file
        
        fileUrl -- full path and name to the song file
        """
        self.filename = fileUrl
       
