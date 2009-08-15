# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

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
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin,  MediaManagerItem
from openlp.plugins.presentations.lib import PresentationMediaItem, PresentationTab,  impressController

class PresentationPlugin(Plugin):

    global log
    log = logging.getLogger(u'PresentationPlugin')

    def __init__(self, plugin_helpers):
        # Call the parent constructor
        log.debug('Initialised')
        self.controllers = {}
        Plugin.__init__(self, u'Presentations', u'1.9.0', plugin_helpers)
        self.weight = -8
        # Create the plugin icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(u':/media/media_presentation.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dnd_id = u'Presentations'

    def get_settings_tab(self):
        """
        Create the settings Tab
        """
        self.presentation_tab = PresentationTab()
        return self.presentation_tab

    def get_media_manager_item(self):
        """
        Create the Media Manager List
        """
        self.media_item = PresentationMediaItem(self, self.icon, u'Presentations', self.controllers)
        return self.media_item

    def registerControllers(self, handle, controller):
        self.controllers[handle] = controller

    def check_pre_conditions(self):
        """
        Check to see if we have any presentation software available
        If Not do not install the plugin.
        """
        log.debug('check_pre_conditions')

        if int(self.config.get_config(u'Powerpoint', 0)) == 2:
            try:
                #Check to see if we have uno installed
                import uno
                #openoffice = impressController()
                self.registerControllers(u'Impress', None)
            except:
                pass
        #If we have no controllers disable plugin
        if len(self.controllers) > 0:
            return True
        else:
            return False
