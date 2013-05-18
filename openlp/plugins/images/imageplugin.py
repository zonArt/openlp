# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
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

from PyQt4 import QtGui

import logging

from openlp.core.lib import Plugin, StringContent, Registry, ImageSource, Settings, build_icon, translate
from openlp.core.lib.db import Manager
from openlp.plugins.images.lib import ImageMediaItem, ImageTab
from openlp.plugins.images.lib.db import init_schema, ImageFilenames

log = logging.getLogger(__name__)

__default_settings__ = {
    u'images/db type': u'sqlite',
    u'images/background color': u'#000000',
}


class ImagePlugin(Plugin):
    log.info(u'Image Plugin loaded')

    def __init__(self):
        Plugin.__init__(self, u'images', __default_settings__, ImageMediaItem, ImageTab)
        self.manager = Manager(u'images', init_schema)
        self.weight = -7
        self.icon_path = u':/plugins/plugin_images.png'
        self.icon = build_icon(self.icon_path)

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

    def app_startup(self):
        """
        Perform tasks on application startup.
        """
        Plugin.app_startup(self)
        # Convert old settings-based image list to the database.
        files_from_config = Settings().get_files_from_config(self)
        if files_from_config:
            log.debug(u'Importing images list from old config: %s' % files_from_config)
            self.media_item.save_new_images_list(files_from_config)

    def upgrade_settings(self, settings):
        """
        Upgrade the settings of this plugin.

        ``settings``
            The Settings object containing the old settings.
        """
        files_from_config = settings.get_files_from_config(self)
        if files_from_config:
            log.debug(u'Importing images list from old config: %s' % files_from_config)
            self.media_item.save_new_images_list(files_from_config)

    def set_plugin_text_strings(self):
        """
        Called to define all translatable texts of the plugin.
        """
        ## Name PluginList ##
        self.text_strings[StringContent.Name] = {
            u'singular': translate('ImagePlugin', 'Image', 'name singular'),
            u'plural': translate('ImagePlugin', 'Images', 'name plural')
        }
        ## Name for MediaDockManager, SettingsManager ##
        self.text_strings[StringContent.VisibleName] = {u'title': translate('ImagePlugin', 'Images', 'container title')}
        # Middle Header Bar
        tooltips = {
            u'load': translate('ImagePlugin', 'Load a new image.'),
            u'import': u'',
            u'new': translate('ImagePlugin', 'Add a new image.'),
            u'edit': translate('ImagePlugin', 'Edit the selected image.'),
            u'delete': translate('ImagePlugin', 'Delete the selected image.'),
            u'preview': translate('ImagePlugin', 'Preview the selected image.'),
            u'live': translate('ImagePlugin', 'Send the selected image live.'),
            u'service': translate('ImagePlugin', 'Add the selected image to the service.')
        }
        self.set_plugin_ui_text_strings(tooltips)

    def config_update(self):
        """
        Triggered by saving and changing the image border.  Sets the images in image manager to require updates. Actual
        update is triggered by the last part of saving the config.
        """
        log.info(u'Images config_update')
        background = QtGui.QColor(Settings().value(self.settings_section + u'/background color'))
        self.image_manager.update_images_border(ImageSource.ImagePlugin, background)

    def _get_image_manager(self):
        """
        Adds the image manager to the class dynamically
        """
        if not hasattr(self, u'_image_manager'):
            self._image_manager = Registry().get(u'image_manager')
        return self._image_manager

    image_manager = property(_get_image_manager)
