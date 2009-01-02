# -*- coding: utf-8 -*-
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

from openlp.core.resources import *

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature
from songbookdialog import Ui_SongBookDialog

class SongBookForm(QDialog, Ui_SongBookDialog):
    """
    Class documentation goes here.
    """
    def __init__(self,songmanager,  parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.songmanager = songmanager
        
    def load_form(self):
        A = 1   

    @pyqtSignature("QTableWidgetItem*")
    def on_BookSongListView_itemClicked(self, item):
        """
        Slot documentation goes here.
        """
        print "bslv ic " + str(item)
    
    @pyqtSignature("")
    def on_DeleteButton_clicked(self):
        """
        Slot documentation goes here.
        """
        print "db c "
    
    @pyqtSignature("")
    def on_AddUpdateButton_clicked(self):
        """
        Slot documentation goes here.
        """
        print "au c "
