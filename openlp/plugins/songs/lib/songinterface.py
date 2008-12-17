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
from songfile import SongFile

class SongInterface(object):
    """Handle the interface functionality between UI, SongFile and Songs"""
    
    def __init__(self, fileUrl):
        """Initialize with needed paths, files and forms
        
        fileUrl -- full path and name to the song file
        """
        self.songfile = SongFile(fileUrl)
        
