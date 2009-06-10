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
import time
from openlp.core.lib import buildIcon
from PyQt4 import QtCore, QtGui

class ServiceItem():
    """
    The service item is a base class for the plugins to use to interact with
    the service manager, the slide controller, and the projection screen
    compositor.
    """
    global log
    log=logging.getLogger(u'ServiceItem')
    log.info(u'Service Item created')

    def __init__(self, hostplugin=None):
        """
        Init Method
        """
        self.plugin = hostplugin
        if hostplugin is not None:
            self.RenderManager = self.plugin.render_manager
            self.shortname = hostplugin.name
        self.title = u''
        self.items = []
        self.iconic_representation = None
        self.raw_slides = None
        self.frame_titles = []
        self.command_files = []
        self.frames = []
        self.raw_footer = None
        self.theme = None
        #log.debug(u'Service item created for %s ', self.shortname)
        self.service_frames = []

    def addIcon(self, icon):
        self.icon = icon
        self.iconic_representation = buildIcon(icon)

    def render(self):
        """
        The render method is what renders the frames for the screen.
        """
        log.debug(u'Render called')
        if self.theme == None:
            self.RenderManager.set_override_theme(None)
        else:
            self.RenderManager.set_override_theme(self.theme)
        log.debug(u'Formatting slides')
        self.frames = []
        if self.service_item_type == u'text':
            for slide in self.service_frames:
                formated = self.RenderManager.format_slide(slide[u'raw_slide'])
                for format in formated:
                    frame = self.RenderManager.generate_slide(format, self.raw_footer)
                    self.frames.append({u'title': slide[u'title'], u'image': frame})
        elif self.service_item_type == u'command':
            self.frames = self.service_frames
            self.service_frames = []
        elif self.service_item_type == u'image':
            self.frames = self.service_frames
            self.service_frames = []
        else:
            log.error(u'Invalid value renderer :%s' % self.service_item_type)

    def add_from_image(self, frame_title, image):
        self.service_item_type = u'image'
        self.service_frames.append({u'title': frame_title, u'image': image})

    def add_from_text(self, frame_title, raw_slide):
        self.service_item_type = u'text'
        frame_title = frame_title.split(u'\n')[0]
        self.service_frames.append({u'title': frame_title, u'raw_slide': raw_slide})

    def add_from_command(self, frame_title, command):
        self.service_item_type = u'command'
        self.service_frames.append({u'title': frame_title, u'command': command})

    def get_oos_repr(self):
        """
        This method returns some text which can be saved into the OOS
        file to represent this item
        """
        oos_header = {u'plugin': self.shortname,u'theme':self.theme, u'title':self.title,
            u'icon':self.icon, u'footer':self.raw_footer, u'type':self.service_item_type}
        oos_data = []
        if self.service_item_type == u'text':
            for slide in self.service_frames:
                oos_data.append(slide[u'raw_slide'])
        return {u'header': oos_header, u'data': self.service_frames}

    def set_from_oos(self, serviceitem):
        """
        This method takes some oostext (passed from the ServiceManager)
        and parses it into the data actually required
        """
        header = serviceitem[u'serviceitem'][u'header']
        self.title = header[u'title']
        self.service_item_type = header[u'type']
        self.shortname = header[u'plugin']
        self.theme = header[u'theme']
        self.addIcon(header[u'icon'])
        self.raw_footer = header[u'footer']
        self.service_frames = serviceitem[u'serviceitem'][u'data']
