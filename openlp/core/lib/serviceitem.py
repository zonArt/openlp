# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import logging
import os
import time

from PyQt4 import QtCore, QtGui

from openlp.core.lib import buildIcon

class ServiceType(object):
    Text = 1
    Image = 2
    Command = 3

class ServiceItem(object):
    """
    The service item is a base class for the plugins to use to interact with
    the service manager, the slide controller, and the projection screen
    compositor.
    """
    global log
    log = logging.getLogger(u'ServiceItem')
    log.info(u'Service Item created')

    def __init__(self, hostplugin=None):
        """
        Set up the service item.

        ``hostplugin``
            The plugin that this service item belongs to.
        """
        self.plugin = hostplugin
        if hostplugin is not None:
            self.RenderManager = self.plugin.render_manager
            self.shortname = hostplugin.name
            self.name = self.plugin.name
        self.title = u''
        self.audit = u''
        self.items = []
        self.iconic_representation = None
        self.raw_slides = None
        self.frame_titles = []
        self.command_files = []
        self.frames = []
        self.raw_footer = None
        self.theme = None
        self.service_item_path = None
        self.service_item_type = None
        #log.debug(u'Service item created for %s ', self.shortname)
        self.service_frames = []

    def addIcon(self, icon):
        """
        Add an icon to the service item. This is used when displaying the
        service item in the service manager.

        ``icon``
            An instance of QIcon or a string to an icon in the resource or on
            disk.
        """
        self.icon = icon
        self.iconic_representation = buildIcon(icon)

    def render(self):
        """
        The render method is what renders the frames for the screen.
        """
        log.debug(u'Render called')
        self.frames = []
        if self.service_item_type == ServiceType.Text:
            log.debug(u'Formatting slides')
            if self.theme == None:
                self.RenderManager.set_override_theme(None)
            else:
                self.RenderManager.set_override_theme(self.theme)
            for slide in self.service_frames:
                formated = self.RenderManager.format_slide(slide[u'raw_slide'])
                for format in formated:
                    frame = self.RenderManager.generate_slide(format,
                        self.raw_footer)
                    self.frames.append({u'title': slide[u'title'],
                        u'image': frame})
        elif self.service_item_type == ServiceType.Command:
            self.frames = self.service_frames
        elif self.service_item_type == ServiceType.Image:
            for slide in self.service_frames:
                slide[u'image'] = \
                    self.RenderManager.resize_image(slide[u'image'])
            self.frames = self.service_frames
        else:
            log.error(u'Invalid value renderer :%s' % self.service_item_type)

    def add_from_image(self, path, frame_title, image):
        """
        Add an image slide to the service item.

        ``path``
            The directory in which the image file is located.

        ``frame_title``
            A title for the slide in the service item.

        ``image``
            The actual image file name.
        """
        self.service_item_type = ServiceType.Image
        self.service_item_path = path
        self.service_frames.append({u'title': frame_title, u'image': image})

    def add_from_text(self, frame_title, raw_slide):
        """
        Add a text slide to the service item.

        ``frame_title``
            The title of the slide in the service item.

        ``raw_slide``
            The raw text of the slide.
        """
        self.service_item_type = ServiceType.Text
        frame_title = frame_title.split(u'\n')[0]
        self.service_frames.append({u'title': frame_title,
            u'raw_slide': raw_slide})

    def add_from_command(self, path, frame_title):
        """
        Add a slide from a command.

        ``frame_title``
            The title of the slide in the service item.

        ``command``
            The command of/for the slide.
        """
        self.service_item_type = ServiceType.Command
        self.service_item_path = path
        self.service_frames.append({u'title': frame_title, u'command':  None})

    def get_oos_repr(self):
        """
        This method returns some text which can be saved into the OOS
        file to represent this item.
        """
        oos_header = {
            u'name': self.name.lower(),
            u'plugin': self.shortname,
            u'theme':self.theme,
            u'title':self.title,
            u'icon':self.icon,
            u'footer':self.raw_footer,
            u'type':self.service_item_type,
            u'audit':self.audit
        }
        oos_data = []
        if self.service_item_type == ServiceType.Text:
            for slide in self.service_frames:
                oos_data.append(slide)
        elif self.service_item_type == ServiceType.Image:
            for slide in self.service_frames:
                oos_data.append(slide[u'title'])
        elif self.service_item_type == ServiceType.Command:
            for slide in self.service_frames:
                oos_data.append(slide[u'title'])
        return {u'header': oos_header, u'data': oos_data}

    def set_from_oos(self, serviceitem, path=None):
        """
        This method takes a service item from a saved service file (passed
        from the ServiceManager) and extracts the data actually required.

        ``serviceitem``
            The item to extract data from.

        ``path``
            Defaults to *None*. Any path data, usually for images.
        """
        header = serviceitem[u'serviceitem'][u'header']
        self.title = header[u'title']
        self.name = header[u'name']
        self.service_item_type = header[u'type']
        self.shortname = header[u'plugin']
        self.theme = header[u'theme']
        self.addIcon(header[u'icon'])
        self.raw_footer = header[u'footer']
        self.audit = header[u'audit']
        if self.service_item_type == ServiceType.Text:
            for slide in serviceitem[u'serviceitem'][u'data']:
                self.service_frames.append(slide)
        elif self.service_item_type == ServiceType.Image:
            for text_image in serviceitem[u'serviceitem'][u'data']:
                filename = os.path.join(path, text_image)
                real_image = QtGui.QImage(unicode(filename))
                self.add_from_image(path, text_image, real_image)
        elif self.service_item_type == ServiceType.Command:
            for text_image in serviceitem[u'serviceitem'][u'data']:
                filename = os.path.join(path, text_image)
                self.add_from_command(path, text_image)
