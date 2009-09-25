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

import os
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin
from openlp.plugins.presentations.lib import PresentationMediaItem, \
    PresentationTab, ImpressController
if os.name == u'nt':
    try:
        from openlp.plugins.presentations.lib import PowerpointController
    except:
        pass
    from openlp.plugins.presentations.lib import PptviewController

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
        log.debug('check_pre_conditions')
        #Lets see if Impress is required (Default is Not wanted)
        if int(self.config.get_config(
            u'Impress', QtCore.Qt.Unchecked)) == QtCore.Qt.Checked:
            try:
                if os.name == u'nt':
                    #Check to see if we are Win32
                    from win32com.client import Dispatch
                else:
                    #Check to see if we have uno installed
                    import uno
                openoffice = ImpressController()
                openoffice.name = u'Impress'    # until controller updated
                self.registerControllers(openoffice)
            except:
                log.exception(u'Failed to set up plugin for Impress')
        if os.name == u'nt':
            #Lets see if Powerpoint is required (Default is Not wanted)
            if int(self.config.get_config(
                u'Powerpoint', QtCore.Qt.Unchecked)) == QtCore.Qt.Checked:
                try:
                    #Check to see if we are Win32
                    from win32com.client import Dispatch
                    powerpoint = PowerpointController()
                    powerpoint.name = u'Powerpoint' # until controller updated
                    self.registerControllers(powerpoint)
                except:
                    log.exception(u'Failed to set up plugin for Powerpoint')
            #Lets see if Powerpoint Viewer is required (Default is Not wanted)
            if int(self.config.get_config(
                u'Powerpoint Viewer', QtCore.Qt.Unchecked)) == QtCore.Qt.Checked:
                try:
                    pptview = PptviewController(self)
                    self.registerControllers(pptview)
                except:
                    log.exception(u'Failed to set up plugin for Powerpoint Viewer')
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
