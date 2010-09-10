# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

from openlp.core.lib import Plugin, StringType, build_icon, translate
from openlp.plugins.images.lib import ImageMediaItem

log = logging.getLogger(__name__)

class ImagePlugin(Plugin):
    log.info(u'Image Plugin loaded')

    def __init__(self, plugin_helpers):
        self.set_plugin_strings()
        Plugin.__init__(self, u'Images', u'1.9.2', plugin_helpers)
        self.weight = -7
        self.icon_path = u':/plugins/plugin_images.png'
        self.icon = build_icon(self.icon_path)

    def getMediaManagerItem(self):
        # Create the MediaManagerItem object
        return ImageMediaItem(self, self.icon, self.name)

    def about(self):
        about_text = translate('ImagePlugin', '<strong>Image Plugin</strong>'
            '<br />The image plugin provides displaying of images.<br />One '
            'of the distinguishing features of this plugin is the ability to '
            'group a number of images together in the service manager, making '
            'the displaying of multiple images easier. This plugin can also '
            'make use of OpenLP\'s "timed looping" feature to create a slide '
            'show that runs automatically. In addition to this, images from '
            'the plugin can be used to override the current theme\'s '
            'background, which renders text-based items like Images with the '
            'selected image as a background instead of the background '
            'provided by the theme.')
        return about_text
    # rimach
    def set_plugin_strings(self):
        """
        Called to define all translatable texts of the plugin
        """
        self.name = u'Images'
        self.name_lower = u'images'

        self.strings = {}
        # for names in mediamanagerdock and pluginlist
        self.strings[StringType.Name] = {
            u'singular': translate('ImagePlugin', 'Image'),
            u'plural': translate('ImagePlugin', 'Images')
        }

        # Middle Header Bar
        ## Load Button ##
        self.strings[StringType.Load] = {
            u'title': translate('ImagePlugin', 'Load'),
            u'tooltip': translate('ImagePlugin', 'Load a new Image')
        }
        ## New Button ##
        self.strings[StringType.New] = {
            u'title': translate('ImagePlugin', 'Add'),
            u'tooltip': translate('ImagePlugin', 'Add a new Image')
        }
        ## Edit Button ##
        self.strings[StringType.Edit] = {
            u'title': translate('ImagePlugin', 'Edit'),
            u'tooltip': translate('ImagePlugin', 'Edit the selected Image')
        }
        ## Delete Button ##
        self.strings[StringType.Delete] = {
            u'title': translate('ImagePlugin', 'Delete'),
            u'tooltip': translate('ImagePlugin', 'Delete the selected Image')
        }
        ## Preview ##
        self.strings[StringType.Preview] = {
            u'title': translate('ImagePlugin', 'Preview'),
            u'tooltip': translate('ImagePlugin', 'Preview the selected Image')
        }
        ## Live  Button ##
        self.strings[StringType.Live] = {
            u'title': translate('ImagePlugin', 'Live'),
            u'tooltip': translate('ImagePlugin', 'Send the selected Image live')
        }
        ## Add to service Button ##
        self.strings[StringType.Service] = {
            u'title': translate('ImagePlugin', 'Service'),
            u'tooltip': translate('ImagePlugin', 'Add the selected Image to the service')
        }
