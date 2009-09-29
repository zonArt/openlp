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

from PyQt4 import QtCore

from openlp.core.lib import Plugin, buildIcon
from openlp.plugins.presentations.lib import *

class PresentationPlugin(Plugin):

    global log
    log = logging.getLogger(u'PresentationPlugin')

    def __init__(self, plugin_helpers):
        # Call the parent constructor
        log.debug(u'Initialised')
        self.controllers = {}
        Plugin.__init__(self, u'Presentations', u'1.9.0', plugin_helpers)
        self.weight = -8
        # Create the plugin icon
        self.icon = buildIcon(u':/media/media_presentation.png')

    def get_settings_tab(self):
        """
        Create the settings Tab
        """
        self.presentation_tab = PresentationTab(self.controllers)
        return self.presentation_tab

    def get_media_manager_item(self):
        """
        Create the Media Manager List
        """
        self.media_item = PresentationMediaItem(
            self, self.icon, u'Presentations', self.controllers)
        return self.media_item

    def registerControllers(self, controller):
        self.controllers[controller.name] = controller

    def check_pre_conditions(self):
        """
        Check to see if we have any presentation software available
        If Not do not install the plugin.
        """
        log.debug(u'check_pre_conditions')
        #Lets see if Powerpoint is required (Default is Not wanted)
        controller = PowerpointController(self)
        if int(self.config.get_config(
            controller.name, QtCore.Qt.Unchecked)) == QtCore.Qt.Checked:
            if controller.is_available():
                self.registerControllers(controller)
        #Lets see if Impress is required (Default is Not wanted)
        controller = ImpressController(self)
        if int(self.config.get_config(
            controller.name, QtCore.Qt.Unchecked)) == QtCore.Qt.Checked:
            if controller.is_available():
                self.registerControllers(controller)
        #Lets see if Powerpoint Viewer is required (Default is Not wanted)
        controller = PptviewController(self)
        if int(self.config.get_config(
            controller.name, QtCore.Qt.Unchecked)) == QtCore.Qt.Checked:
            if controller.is_available():
                self.registerControllers(controller)
        #If we have no available controllers disable plugin
        if len(self.controllers) > 0:
            return True
        else:
            return False

    def finalise(self):
        log.debug(u'Finalise')
        #Ask each controller to tidy up
        for controller in self.controllers:
            self.controllers[controller].kill()
