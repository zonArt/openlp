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

import logging
import os

from openlp.core.lib import Plugin, StringContent, build_icon, translate
from openlp.plugins.media.lib import MediaMediaItem, MediaTab

log = logging.getLogger(__name__)

class MediaPlugin(Plugin):
    log.info(u'%s MediaPlugin loaded', __name__)

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Media', plugin_helpers,
            MediaMediaItem)
        self.weight = -6
        self.icon_path = u':/plugins/plugin_media.png'
        self.icon = build_icon(self.icon_path)
        # passed with drag and drop messages
        self.dnd_id = u'Media'
        self.audio_extensions_list = \
            self.mediaManager.get_audio_extensions_list()
        self.video_extensions_list = \
            self.mediaManager.get_video_extensions_list()

    def getSettingsTab(self, parent):
        """
        Create the settings Tab
        """
        visible_name = self.getString(StringContent.VisibleName)
        return MediaTab(parent, self.name, visible_name[u'title'],
            self.mediaManager.APIs, self.icon_path)

    def about(self):
        about_text = translate('MediaPlugin', '<strong>Media Plugin</strong>'
            '<br />The media plugin provides playback of audio and video.')
        return about_text

    def setPluginTextStrings(self):
        """
        Called to define all translatable texts of the plugin
        """
        ## Name PluginList ##
        self.textStrings[StringContent.Name] = {
            u'singular': translate('MediaPlugin', 'Media', 'name singular'),
            u'plural': translate('MediaPlugin', 'Media', 'name plural')
        }
        ## Name for MediaDockManager, SettingsManager ##
        self.textStrings[StringContent.VisibleName] = {
            u'title': translate('MediaPlugin', 'Media', 'container title')
        }
        # Middle Header Bar
        tooltips = {
            u'load': translate('MediaPlugin', 'Load new media.'),
            u'import': u'',
            u'new': translate('MediaPlugin', 'Add new media.'),
            u'edit': translate('MediaPlugin', 'Edit the selected media.'),
            u'delete': translate('MediaPlugin', 'Delete the selected media.'),
            u'preview': translate('MediaPlugin', 'Preview the selected media.'),
            u'live': translate('MediaPlugin', 'Send the selected media live.'),
            u'service': translate('MediaPlugin',
                'Add the selected media to the service.')
        }
        self.setPluginUiTextStrings(tooltips)

    def finalise(self):
        """
        Time to tidy up on exit
        """
        log.info(u'Media Finalising')
        self.mediaManager.finalise()

    def getDisplayCss(self):
        """
        Add css style sheets to htmlbuilder
        """
        return self.mediaManager.getDisplayCss()

    def getDisplayJavascript(self):
        """
        Add javascript functions to htmlbuilder
        """
        return self.mediaManager.getDisplayJavascript()

    def getDisplayHtml(self):
        """
        Add html code to htmlbuilder
        """
        return self.mediaManager.getDisplayHtml()
