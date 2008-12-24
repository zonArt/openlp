# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

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

from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignature

from editsongdialog import Ui_EditSongDialog

class EditSongForm(QWidget, Ui_EditSongDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, songmanager, parent = None):
        """
        Constructor
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.songmanager = songmanager
        self.initialise()
    
    def initialise(self):
        list = self.songmanager.get_authors()
        self.AuthorsSelectionComboItem.clear()
        #print list
        for l in list:
            self.AuthorsSelectionComboItem.addItem(str(l[1]))

    def load_song(self, songid):
        self.songid = songid
        song = self.songmanager.get_song(songid)
        #print song
        self.TitleEditItem.setText(song[1])        
        self.LyricsTextEdit.setText(song[2])
        self.CopyrightEditItem.setText(song[3])

