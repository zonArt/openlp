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

from openlp.core.lib import Plugin, buildIcon
from openlp.plugins.images.lib import ImageMediaItem, ImageTab

class ImagePlugin(Plugin):
    global log
    log = logging.getLogger(u'ImagePlugin')
    log.info(u'Image Plugin loaded')

    def __init__(self, plugin_helpers):
        # Call the parent constructor
        Plugin.__init__(self, u'Images', u'1.9.0', plugin_helpers)
        self.weight = -7
        # Create the plugin icon
        self.icon = buildIcon(u':/media/media_image.png')

    def can_be_disabled(self):
        return True

    def initialise(self):
        log.info(u'Plugin Initialising')

    def finalise(self):
        log.info(u'Plugin Finalise')

    def get_settings_tab(self):
        self.ImageTab = ImageTab()
        return self.ImageTab

    def get_media_manager_item(self):
        # Create the MediaManagerItem object
        return ImageMediaItem(self, self.icon, u'Images')

    def about(self):
        return u'<b>Image Plugin</b><br>Allows images of all types to be displayed. If a number of images are selected together and presented on the live controller it is possible to turn them into a timed loop.<br> From the plugin if the <i>Override background</i> is chosen and an image is selected any somgs which are rendered will use the selected image from the background instead of the one provied by the theme.<br>'
