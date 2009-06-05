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
        self.frame_titles = []
        self.command_files = []
        self.frames = []
        self.raw_footer = None
        self.theme = None
        log.debug(u'Service item created for %s ', self.shortname)
        self.service_frames = []

    def addIcon(self, icon):
        self.iconic_representation = buildIcon(icon)

    def render(self):
        """
        The render method is what renders the frames for the screen.
        """
        log.debug(u'Render called')
        if self.theme == None:
            self.plugin.render_manager.set_override_theme(None)
        else:
            self.plugin.render_manager.set_override_theme(self.theme)
        log.debug(u'Formatting slides')
        if self.service_item_type == u'text':
            for slide in self.service_frames:
                formated = self.plugin.render_manager.format_slide(slide[u'raw_slide'])
                for format in formated:
                    frame = self.plugin.render_manager.generate_slide(format, self.raw_footer)
                    self.frames.append({u'title': slide[u'title'], u'image': frame})
        elif self.service_item_type == u'command':
            self.frames = self.service_frames
            self.service_frames = []
        elif self.service_item_type == u'image':
            self.frames = self.service_frames
            self.service_frames = []
        else:
            assert(0 , u'Invalid value rendere :%s' % self.service_item_type)

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
