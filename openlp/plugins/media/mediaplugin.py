# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Eric Ludin, Edwin Lunando, Brian T. Meyer,    #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky                                             #
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

from openlp.core.lib import Plugin, StringContent, build_icon, translate
from openlp.core.lib.settings import Settings
from openlp.plugins.media.lib import MediaMediaItem, MediaTab

log = logging.getLogger(__name__)

class MediaPlugin(Plugin):
    log.info(u'%s MediaPlugin loaded', __name__)

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'media', plugin_helpers,
            MediaMediaItem)
        self.weight = -6
        self.iconPath = u':/plugins/plugin_media.png'
        self.icon = build_icon(self.iconPath)
        # passed with drag and drop messages
        self.dnd_id = u'Media'
        self.audio_extensions_list = \
            self.mediaController.get_audio_extensions_list()
        for ext in self.audio_extensions_list:
            self.serviceManager.supportedSuffixes(ext[2:])
        self.video_extensions_list = \
            self.mediaController.get_video_extensions_list()
        for ext in self.video_extensions_list:
            self.serviceManager.supportedSuffixes(ext[2:])

    def createSettingsTab(self, parent):
        """
        Create the settings Tab
        """
        visible_name = self.getString(StringContent.VisibleName)
        self.settingsTab = MediaTab(parent, self.name, visible_name[u'title'],
            self.mediaController.mediaPlayers, self.iconPath)

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
        self.mediaController.finalise()
        Plugin.finalise(self)

    def getDisplayCss(self):
        """
        Add css style sheets to htmlbuilder
        """
        return self.mediaController.get_media_display_css()

    def getDisplayJavaScript(self):
        """
        Add javascript functions to htmlbuilder
        """
        return self.mediaController.get_media_display_javascript()

    def getDisplayHtml(self):
        """
        Add html code to htmlbuilder
        """
        return self.mediaController.get_media_display_html()

    def appStartup(self):
        """
        Do a couple of things when the app starts up. In this particular case
        we want to check if we have the old "Use Phonon" setting, and convert
        it to "enable Phonon" and "make it the first one in the list".
        """
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        if settings.contains(u'use phonon'):
            log.info(u'Found old Phonon setting')
            players = self.mediaController.mediaPlayers.keys()
            has_phonon = u'phonon' in players
            if settings.value(u'use phonon').toBool() and has_phonon:
                log.debug(u'Converting old setting to new setting')
                new_players = []
                if players:
                    new_players = [player for player in players \
                        if player != u'phonon']
                new_players.insert(0, u'phonon')
                self.mediaController.mediaPlayers[u'phonon'].isActive = True
                settings.setValue(u'players', \
                    QtCore.QVariant(u','.join(new_players)))
                self.settingsTab.load()
            settings.remove(u'use phonon')
        settings.endGroup()
