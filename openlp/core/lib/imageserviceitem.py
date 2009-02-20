# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

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
from PyQt4 import QtCore, QtGui

class ImageServiceItem():
    """
    The service item is a base class for the plugins to use to interact with
    the service manager, the slide controller, and the renderer.
    """

    def __init__(self, controller):
        """
        Init Method
        """
        self.imgs=[]
        self.slide_controller=controller
        self.slide_controller.ControllerContents=QtGui.QTableWidget()
        c=self.slide_controller.ControllerContents
        c.setColumnCount(2)
        c.setColumnHidden(0, True)
        c.setColumnWidth(1, 275)
        c.setShowGrid(False)
        c.setSortingEnabled(False)        
        c.setAlternatingRowColors(True)
        c.setHorizontalHeaderLabels(QtCore.QStringList(["","Name"]))  
        c.setAlternatingRowColors(True)                 
        c.setGeometry(QtCore.QRect(10, 100, 256, 591))
        pass
    
    def render(self):
        """
        The render method is what the plugin uses to render its meda to the
        screen.
        """
        # render the "image chooser first"
        for f in self.imgs:
            fl ,  nm = os.path.split(str(f))            
            c = self.slide_controller.rowCount()
            self.slide_controller.setRowCount(c+1)
            twi = QtGui.QTableWidgetItem(str(f))
            self.slide_controller.setItem(c , 0, twi)
            twi = QtGui.QTableWidgetItem(str(nm))
            self.slide_controller.setItem(c , 1, twi)
            self.slide_controller.setRowHeight(c, 20)        

    def get_parent_node(self):
        """
        This method returns a parent node to be inserted into the Service
        Manager.
        """
        pass
    def add(self, img_filename):
        """
        append an image to the list
        """
        self.imgs.append(img_filename)

    def get_oos_text(self):
        """
        Turn the image list into a set of filenames for storage in the oos file
        """
        return str(self.imgs)

    def set_from_oos(self, text):
        """
        get text from the OOS file and setup the internal structure
        """
        self.imgs=eval(text)
        
