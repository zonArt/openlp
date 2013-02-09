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

import logging

from PyQt4 import QtCore

from openlp.core.lib import Plugin, Registry, StringContent, Settings, build_icon, translate
from openlp.plugins.media.lib import MediaMediaItem, MediaTab

log = logging.getLogger(__name__)

# Some settings starting with "media" are in core, because they are needed for core functionality.
__default_settings__ = {
        u'media/media auto start': QtCore.Qt.Unchecked,
        u'media/media files': []
    }


class MediaPlugin(Plugin):
    log.info(u'%s MediaPlugin loaded', __name__)

    def __init__(self):
        Plugin.__init__(self, u'media', __default_settings__, MediaMediaItem)
        self.weight = -6
        self.iconPath = u':/plugins/plugin_media.png'
        self.icon = build_icon(self.iconPath)
        # passed with drag and drop messages
        self.dnd_id = u'Media'

    def createSettingsTab(self, parent):
        """
        Create the settings Tab
        """
        visible_name = self.getString(StringContent.VisibleName)
        self.settingsTab = MediaTab(parent, self.name, visible_name[u'title'], self.iconPath)

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
            u'service': translate('MediaPlugin', 'Add the selected media to the service.')
        }
        self.setPluginUiTextStrings(tooltips)

    def finalise(self):
        """
        Time to tidy up on exit
        """
        log.info(u'Media Finalising')
        self.media_controller.finalise()
        Plugin.finalise(self)

    def getDisplayCss(self):
        """
        Add css style sheets to htmlbuilder
        """
        return self.media_controller.get_media_display_css()

    def getDisplayJavaScript(self):
        """
        Add javascript functions to htmlbuilder
        """
        return self.media_controller.get_media_display_javascript()

    def getDisplayHtml(self):
        """
        Add html code to htmlbuilder
        """
        return self.media_controller.get_media_display_html()

    def app_startup(self):
        """
        Do a couple of things when the app starts up. In this particular case
        we want to check if we have the old "Use Phonon" setting, and convert
        it to "enable Phonon" and "make it the first one in the list".
        """
        Plugin.app_startup(self)
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        if settings.contains(u'use phonon'):
            log.info(u'Found old Phonon setting')
            players = self.media_controller.mediaPlayers.keys()
            has_phonon = u'phonon' in players
            if settings.value(u'use phonon')  and has_phonon:
                log.debug(u'Converting old setting to new setting')
                new_players = []
                if players:
                    new_players = [player for player in players if player != u'phonon']
                new_players.insert(0, u'phonon')
                self.media_controller.mediaPlayers[u'phonon'].isActive = True
                settings.setValue(u'players', u','.join(new_players))
                self.settingsTab.load()
            settings.remove(u'use phonon')
        settings.endGroup()

    def _get_media_controller(self):
        """
        Adds the media controller to the class dynamically
        """
        if not hasattr(self, u'_media_controller'):
            self._media_controller = Registry().get(u'media_controller')
        return self._media_controller

    media_controller = property(_get_media_controller)
