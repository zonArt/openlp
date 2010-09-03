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

from openlp.core.lib import Plugin, build_icon, translate
from openlp.plugins.images.lib import ImageMediaItem

log = logging.getLogger(__name__)

class ImagePlugin(Plugin):
    log.info(u'Image Plugin loaded')

    def __init__(self, plugin_helpers):
        self.set_plugin_translations()
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
            'background, which renders text-based items like songs with the '
            'selected image as a background instead of the background '
            'provided by the theme.')
        return about_text
    # rimach
    def set_plugin_translations(self):
        """
        Called to define all translatable texts of the plugin
        """
        self.name = u'Images'
        self.name_lower = u'images'
        self.text = {}
        #for context menu
        self.text['context_edit'] = translate('ImagePlugin', '&Edit Image')
        self.text['context_delete'] = translate('ImagePlugin', '&Delete Image')
        self.text['context_preview'] = translate('ImagePlugin', '&Preview Image')
        self.text['context_live'] = translate('ImagePlugin', '&Show Live')
        # forHeaders in mediamanagerdock
        self.text['import'] = translate('ImagePlugin', 'Import a Image')
        self.text['load'] = translate('ImagePlugin', 'Load a new Image')
        self.text['new'] = translate('ImagePlugin', 'Add a new Image')
        self.text['edit'] = translate('ImagePlugin', 'Edit the selected Image')
        self.text['delete'] = translate('ImagePlugin', 'Delete the selected Image')
        self.text['delete_more'] = translate('ImagePlugin', 'Delete the selected Images')
        self.text['preview'] = translate('ImagePlugin', 'Preview the selected Image')
        self.text['preview_more'] = translate('ImagePlugin', 'Preview the selected Images')
        self.text['live'] = translate('ImagePlugin', 'Send the selected Image live')
        self.text['live_more'] = translate('ImagePlugin', 'Send the selected Images live')
        self.text['service'] = translate('ImagePlugin', 'Add the selected Image to the service')
        self.text['service_more'] = translate('ImagePlugin', 'Add the selected Images to the service')
        # for names in mediamanagerdock and pluginlist
        self.text['name'] = translate('ImagePlugin', 'Image')
        self.text['name_more'] = translate('ImagePlugin', 'Images')
