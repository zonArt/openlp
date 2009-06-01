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
import os
from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin, MediaManagerItem, SettingsTab
from openlp.plugins.media.lib import MediaTab,MediaMediaItem

class MediaPlugin(Plugin):

    def __init__(self, plugin_helpers):
        # Call the parent constructor
        Plugin.__init__(self, u'Media', u'1.9.0', plugin_helpers)
        self.weight = -6
        # Create the plugin icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(':/media/media_video.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)

    def get_settings_tab(self):
        self.MediaTab = MediaTab()
        return self.MediaTab

    def get_media_manager_item(self):
        # Create the MediaManagerItem object
        self.media_item = MediaMediaItem(self, self.icon, u'Media')
        return self.media_item

