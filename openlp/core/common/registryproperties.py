# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
Provide Registry values for adding to classes
"""
import os

from openlp.core.common import Registry


class RegistryProperties(object):
    """
    This adds registry components to classes to use at run time.
    """

    @property
    def application(self):
        """
        Adds the openlp to the class dynamically.
        Windows needs to access the application in a dynamic manner.
        """
        if os.name == 'nt':
            return Registry().get('application')
        else:
            if not hasattr(self, '_application') or not self._application:
                self._application = Registry().get('application')
            return self._application

    @property
    def plugin_manager(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, '_plugin_manager') or not self._plugin_manager:
            self._plugin_manager = Registry().get('plugin_manager')
        return self._plugin_manager

    @property
    def image_manager(self):
        """
        Adds the image manager to the class dynamically
        """
        if not hasattr(self, '_image_manager') or not self._image_manager:
            self._image_manager = Registry().get('image_manager')
        return self._image_manager

    @property
    def media_controller(self):
        """
        Adds the media controller to the class dynamically
        """
        if not hasattr(self, '_media_controller') or not self._media_controller:
            self._media_controller = Registry().get('media_controller')
        return self._media_controller

    @property
    def service_manager(self):
        """
        Adds the service manager to the class dynamically
        """
        if not hasattr(self, '_service_manager') or not self._service_manager:
            self._service_manager = Registry().get('service_manager')
        return self._service_manager

    @property
    def preview_controller(self):
        """
        Adds the preview controller to the class dynamically
        """
        if not hasattr(self, '_preview_controller') or not self._preview_controller:
            self._preview_controller = Registry().get('preview_controller')
        return self._preview_controller

    @property
    def live_controller(self):
        """
        Adds the live controller to the class dynamically
        """
        if not hasattr(self, '_live_controller') or not self._live_controller:
            self._live_controller = Registry().get('live_controller')
        return self._live_controller

    @property
    def main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, '_main_window') or not self._main_window:
            self._main_window = Registry().get('main_window')
        return self._main_window

