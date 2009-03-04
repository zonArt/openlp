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
import logging
from openlp.core.lib import ServiceItem
from listwithpreviews import ListWithPreviews

class ImageServiceItem(ServiceItem):
    """
    The service item is a base class for the plugins to use to interact with
    * the service manager (and hence the OOS disk files),
    * the slide controller(s - both preview and live)
    * and the renderer - which produces the
          main screen
          the preview preview and
          the live preview

    The image plugin passes one of these to the preview/live when requested
      The preview/live controllers keep hold of it
    The service manager has one in its service structure for each Image item in the OOS
    When something goes live/previews -
      it simply tells the slide controller to use it???

    It contains 1 or more images
          
    """
    global log
    log=logging.getLogger("ImageServiceItem")
    log.info("ImageServiceItem loaded")
    def __init__(self, controller):
        """
        Init Method
        """
        log.info("init")
        self.imgs=ListWithPreviews()
#         self.slide_controller=controller
#         self.slide_controller.ControllerContents=QtGui.QListView()
#         c=self.slide_controller.ControllerContents
#         c.uniformItemSizes=True
#         c.setModel(self.imgs)
#         c.setGeometry(0,0,200,200)
    
    def render(self):
        """
        The render method is what the plugin uses to render its meda to the
        screen.
        """
        # render the "image chooser first"
#         for f in self.imgs:
#             fl ,  nm = os.path.split(str(f))            
#             c = self.slide_controller.rowCount()
#             self.slide_controller.setRowCount(c+1)
#             twi = QtGui.QTableWidgetItem(str(f))
#             self.slide_controller.setItem(c , 0, twi)
#             twi = QtGui.QTableWidgetItem(str(nm))
#             self.slide_controller.setItem(c , 1, twi)
#             self.slide_controller.setRowHeight(c, 80)
            
        # render the preview screen here

    def get_parent_node(self):
        """
        This method returns a parent node to be inserted into the Service
        Manager.
        """
        pass
    def add(self, data):
        """
        append an image to the list
        """
        if type(data)==type("string"):
            log.info("add filename:"+data)
            self.imgs.addRow(data)
        else: # it's another service item to be merged in
            log.info("add Item..."+str(data))
            for filename in data.imgs.get_file_list():
                self.add(filename)
            

    def get_oos_text(self):
        """
        Turn the image list into a set of filenames for storage in the oos file
        """
        log.info("Get oos text")
        log.info(str(self.imgs))
        log.info(str(self.imgs.get_file_list()))
        return '\n'.join(self.imgs.get_file_list())

    def set_from_oos(self, text):
        """
        get text from the OOS file and setup the internal structure
        """
        log.info("Set from OOS:"+text)
        files=text.split('\n')
        for f in files:
            self.imgs.addRow(f)
        
