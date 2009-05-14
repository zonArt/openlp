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
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.resources import *
from openlp.core.lib import Plugin, Event
from openlp.core.lib import EventType
from forms import EditCustomForm
from openlp.plugins.custom.lib import CustomManager, CustomTab, CustomMediaItem, CustomServiceItem


class CustomPlugin(Plugin):

    global log
    log=logging.getLogger(u'CustomPlugin')
    log.info(u'Custom Plugin loaded')

    def __init__(self, plugin_helpers):
        # Call the parent constructor
        Plugin.__init__(self, u'Custom', u'1.9.0', plugin_helpers)
        self.weight = -5
        self.custommanager = CustomManager(self.config)
        self.edit_custom_form = EditCustomForm(self.custommanager)
        # Create the plugin icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(':/media/media_custom.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.preview_service_item = CustomServiceItem(self.preview_controller)
        self.live_service_item = CustomServiceItem(self.live_controller)

    def get_media_manager_item(self):
        # Create the CustomManagerItem object
        self.media_item = CustomMediaItem(self, self.icon, u'Custom Slides')
        return self.media_item

    def handle_event(self, event):
        """
        Handle the event contained in the event object.
        """
        log.debug(u'Handle event called with event %s with payload %s'%(event.event_type, event.payload))
        if event.event_type == EventType.ThemeListChanged:
            log.debug(u'New Theme request received')
            self.edit_custom_form.loadThemes(self.theme_manager.getThemes())
        if event.event_type == EventType.LoadServiceItem and event.payload == 'Custom':
            log.debug(u'Load Service Item received')
            self.media_item.onCustomAddClick()
        if event.event_type == EventType.PreviewShow and event.payload == 'Custom':
            log.debug(u'Load Service Item received ')
            self.media_item.onCustomPreviewClick()
        if event.event_type == EventType.LiveShow and event.payload == 'Custom':
            log.debug(u'Load Service Item received')
            self.media_item.onCustomLiveClick()
