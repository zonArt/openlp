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

from PyQt4 import QtGui

from openlp.core.lib import Plugin
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
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(u':/media/media_presentation.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)

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
        dir = os.path.join(os.path.dirname(__file__), u'lib')
        for filename in os.listdir(dir):
            if filename.endswith(u'controller.py') and \
                not filename == 'presentationcontroller.py':
                path = os.path.join(dir, filename)
                if os.path.isfile(path):
                    modulename = u'openlp.plugins.presentations.lib.' + \
                        os.path.splitext(filename)[0]
                    log.debug(u'Importing controller %s', modulename)
                    try:
                        __import__(modulename, globals(), locals(), [])
                    except ImportError, e:
                        log.error(u'Failed to import %s on path %s for reason %s', modulename, path, e.args[0])
        controller_classes = PresentationController.__subclasses__()
        for controller_class in controller_classes:
            controller = controller_class(self)
            self.registerControllers(controller)
            if controller.enabled:
                controller.start_process()
        if len(self.controllers) > 0:
            return True
        else:
            return False

    def finalise(self):
        log.debug(u'Finalise')
        #Ask each controller to tidy up
        for key in self.controllers:
            controller = self.controllers[key]
            if controller.enabled:
                controller.kill()

    def about(self):
        return u'<b>Presentation Plugin</b> <br> Delivers the ability to show presentations using a number of different programs. The choice of available presentaion programs is available in a drop down.'
