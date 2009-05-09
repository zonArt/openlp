# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley

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
import logging
import types
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ServiceItem():
    """
    The service item is a base class for the plugins to use to interact with
    the service manager, the slide controller, and the projection screen
    compositor.
    """
    global log
    log=logging.getLogger(u'ServiceItem')
    log.info(u'Service Item created')

    def __init__(self, hostplugin):
        """
        Init Method
        """
        self.plugin = hostplugin
        self.shortname = hostplugin.name
        self.title = u''
        self.items = []
        self.iconic_representation = None
        self.raw_slides = None
        self.frames = []
        self.raw_footer = None
        self.theme = None
        log.debug(u'Service item created for %s', self.shortname)

    def addIcon(self, icon):
        ButtonIcon = None
        if type(icon) is QIcon:
            ButtonIcon = icon
        elif type(icon) is types.StringType or type(icon) is types.UnicodeType:
            ButtonIcon = QIcon()
            if icon.startswith(u':/'):
                ButtonIcon.addPixmap(QPixmap(icon), QIcon.Normal,
                    QIcon.Off)
            else:
                ButtonIcon.addPixmap(QPixmap.fromImage(QImage(icon)),
                    QIcon.Normal, QIcon.Off)
        self.iconic_representation = ButtonIcon

    def render(self):
        """
        The render method is what renders the frames for the screen.
        """
        log.debug(u'Render called')
        if self.theme == None:
            self.render_manager.set_override_theme(None)
        else:
            self.render_manager.set_override_theme(self.theme)
        log.debug(u'Formatting slides')
        if len(self.frames) == 0 :
            for slide in self.raw_slides:
                formated = self.render_manager.format_slide(slide, False)
                frame = self.render_manager.generate_slide(slide, self.raw_footer)
                self.frames.append({u'formatted': formated, u'image': frame})


    def get_parent_node(self):
        """
        This method returns a parent node to be inserted into the Service
        Manager. At the moment this has to be a QAbstractListModel based class
        """
        pass

    def get_oos_repr(self):
        """
        This method returns some text which can be saved into the OOS
        file to represent this item
        """
        pass

    def set_from_oos(self, oostext):
        """
        This method takes some oostext (passed from the ServiceManager)
        and parses it into the data actually required
        """
        pass

    def set_from_plugin(self):
        """
        Takes data from the plugin media chooser
        """
        pass
