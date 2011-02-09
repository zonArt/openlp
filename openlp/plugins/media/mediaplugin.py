# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
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
import mimetypes

from PyQt4.phonon import Phonon

from openlp.core.lib import Plugin, StringContent, build_icon, translate
from openlp.core.lib.ui import UiStrings
from openlp.plugins.media.lib import MediaMediaItem, MediaTab

log = logging.getLogger(__name__)

class MediaPlugin(Plugin):
    log.info(u'%s MediaPlugin loaded', __name__)

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Media', u'1.9.4', plugin_helpers)
        self.weight = -6
        self.icon_path = u':/plugins/plugin_media.png'
        self.icon = build_icon(self.icon_path)
        # passed with drag and drop messages
        self.dnd_id = u'Media'
        self.audio_list = u''
        self.video_list = u''
        mimetypes.init()
        for mimetype in Phonon.BackendCapabilities.availableMimeTypes():
            mimetype = unicode(mimetype)
            type = mimetype.split(u'audio/x-')
            self.audio_list, mimetype = self._addToList(self.audio_list,
                type, mimetype)
            type = mimetype.split(u'audio/')
            self.audio_list, mimetype = self._addToList(self.audio_list,
                type, mimetype)
            type = mimetype.split(u'video/x-')
            self.video_list, mimetype = self._addToList(self.video_list,
                type, mimetype)
            type = mimetype.split(u'video/')
            self.video_list, mimetype = self._addToList(self.video_list,
                type, mimetype)

    def _addToList(self, list, value, mimetype):
        # Is it a media type
        if len(value) == 2:
            extensions = mimetypes.guess_all_extensions(unicode(mimetype))
            # we have an extension
            if extensions:
                for extension in extensions:
                    if list.find(extension) == -1:
                        list += u'*%s ' % extension
                        self.serviceManager.supportedSuffixes(extension[1:])
                mimetype = u''
        return list, mimetype

    def getSettingsTab(self):
        return MediaTab(self.name)

    def getMediaManagerItem(self):
        # Create the MediaManagerItem object.
        return MediaMediaItem(self, self, self.icon)

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
        ## Load Action ##
        self.textStrings[StringContent.Load] = {
            u'title': UiStrings.Load,
            u'tooltip': translate('MediaPlugin',
                'Load a new Media')
        }
        ## New Action ##
        self.textStrings[StringContent.New] = {
            u'title': UiStrings.Add,
            u'tooltip': translate('MediaPlugin',
                'Add a new Media')
        }
        ## Edit Action ##
        self.textStrings[StringContent.Edit] = {
            u'title': UiStrings.Edit,
            u'tooltip': translate('MediaPlugin',
                'Edit the selected Media')
        }
        ## Delete Action ##
        self.textStrings[StringContent.Delete] = {
            u'title': UiStrings.Delete,
            u'tooltip': translate('MediaPlugin',
                'Delete the selected Media')
        }
        ## Preview Action ##
        self.textStrings[StringContent.Preview] = {
            u'title': UiStrings.Preview,
            u'tooltip': translate('MediaPlugin',
                'Preview the selected Media')
        }
        ## Send Live Action ##
        self.textStrings[StringContent.Live] = {
            u'title': UiStrings.Live,
            u'tooltip': translate('MediaPlugin',
                'Send the selected Media live')
        }
        ## Add to Service Action ##
        self.textStrings[StringContent.Service] = {
            u'title': UiStrings.Service,
            u'tooltip': translate('MediaPlugin',
                'Add the selected Media to the service')
        }
