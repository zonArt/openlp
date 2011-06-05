# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
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

from openlp.core.lib import Plugin, StringContent, build_icon, translate
from openlp.plugins.media.lib import MediaMediaItem, MediaTab, MediaManager

log = logging.getLogger(__name__)

class MediaPlugin(Plugin):
    log.info(u'%s MediaPlugin loaded', __name__)

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Media', plugin_helpers,
            MediaMediaItem, MediaTab)
        self.weight = -6
        self.icon_path = u':/plugins/plugin_media.png'
        self.icon = build_icon(self.icon_path)
        # passed with drag and drop messages
        self.dnd_id = u'Media'
        self.mediaManager = MediaManager(self)
        self.audio_extensions_list = \
            self.mediaManager.get_audio_extensions_list()
        self.video_extensions_list = \
            self.mediaManager.get_video_extensions_list()

    def about(self):
        about_text = translate('MediaPlugin', '<strong>Media Plugin</strong>'
            '<br />The media plugin provides playback of audio and video.')
        return about_text

    def addControllerItems(self, controller, control_panel):
        self.mediaManager.addControllerItems(controller, control_panel)

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
            u'load': translate('MediaPlugin', 'Load a new Media.'),
            u'import': u'',
            u'new': translate('MediaPlugin', 'Add a new Media.'),
            u'edit': translate('MediaPlugin', 'Edit the selected Media.'),
            u'delete': translate('MediaPlugin', 'Delete the selected Media.'),
            u'preview': translate('MediaPlugin', 'Preview the selected Media.'),
            u'live': translate('MediaPlugin', 'Send the selected Media live.'),
            u'service': translate('MediaPlugin',
                'Add the selected Media to the service.')
        }
        self.setPluginUiTextStrings(tooltips)

    def finalise(self):
        """
        Time to tidy up on exit
        """
        log.info(u'Media Finalising')
        self.mediaManager.Timer.stop()
        self.mediaManager.video_reset(self.previewController)
        self.mediaManager.video_reset(self.liveController)
