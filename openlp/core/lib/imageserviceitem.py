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

class ImageServiceItem():
    """
    The service item is a base class for the plugins to use to interact with
    the service manager, the slide controller, and the renderer.
    """

    def __init__(self):
        """
        Init Method
        """
        self.imgs=[]
        pass
    
    def render(self):
        """
        The render method is what the plugin uses to render its meda to the
        screen.
        """
        pass

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
    
