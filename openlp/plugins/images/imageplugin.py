# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

from PyQt4 import QtCore, QtGui

import logging

from openlp.core.lib import Plugin, StringContent, build_icon, translate, \
    Receiver
from openlp.plugins.images.lib import ImageMediaItem, ImageTab

log = logging.getLogger(__name__)

class ImagePlugin(Plugin):
    log.info(u'Image Plugin loaded')

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'images', plugin_helpers, ImageMediaItem,
            ImageTab)
        self.weight = -7
        self.icon_path = u':/plugins/plugin_images.png'
        self.icon = build_icon(self.icon_path)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'image_updated'), self.image_updated)

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

    def setPluginTextStrings(self):
        """
        Called to define all translatable texts of the plugin
        """
        ## Name PluginList ##
        self.textStrings[StringContent.Name] = {
            u'singular': translate('ImagePlugin', 'Image', 'name singular'),
            u'plural': translate('ImagePlugin', 'Images', 'name plural')
        }
        ## Name for MediaDockManager, SettingsManager ##
        self.textStrings[StringContent.VisibleName] = {
            u'title': translate('ImagePlugin', 'Images', 'container title')
        }
        # Middle Header Bar
        tooltips = {
            u'load': translate('ImagePlugin', 'Load a new image.'),
            u'import': u'',
            u'new': translate('ImagePlugin', 'Add a new image.'),
            u'edit': translate('ImagePlugin', 'Edit the selected image.'),
            u'delete': translate('ImagePlugin', 'Delete the selected image.'),
            u'preview': translate('ImagePlugin', 'Preview the selected image.'),
            u'live': translate('ImagePlugin', 'Send the selected image live.'),
            u'service': translate('ImagePlugin',
                'Add the selected image to the service.')
        }
        self.setPluginUiTextStrings(tooltips)

    def image_updated(self):
        background = QtGui.QColor(QtCore.QSettings().value(self.settingsSection
            + u'/background color', QtCore.QVariant(u'#000000')))
        self.liveController.imageManager.update_images(background)
