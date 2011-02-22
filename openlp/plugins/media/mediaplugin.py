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
from openlp.plugins.media.lib import MediaMediaItem, MediaTab

log = logging.getLogger(__name__)

class MediaPlugin(Plugin):
    log.info(u'%s MediaPlugin loaded', __name__)

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Media', u'1.9.4', plugin_helpers,
            MediaMediaItem, MediaTab)
        self.weight = -6
        self.icon_path = u':/plugins/plugin_media.png'
        self.icon = build_icon(self.icon_path)
        # passed with drag and drop messages
        self.dnd_id = u'Media'
        self.additional_extensions = {}
        #   'video/msvideo': ['.avi']} This is an example line.
        self.audio_extensions_list = []
        self.video_extensions_list = []
        mimetypes.init()
        for mimetype in Phonon.BackendCapabilities.availableMimeTypes():
            mimetype = unicode(mimetype)
            if mimetype.startswith(u'audio/'):
                self._addToList(self.audio_extensions_list, mimetype)
            elif mimetype.startswith(u'video/'):
                self._addToList(self.video_extensions_list, mimetype)

    def _addToList(self, list, mimetype):
        # Add all extensions which mimetypes provides us for supported types.
        extensions = mimetypes.guess_all_extensions(unicode(mimetype))
        for extension in extensions:
            ext = u'*%s' % extension
            if ext not in list:
                list.append(ext)
                self.serviceManager.supportedSuffixes(extension[1:])
        log.info(u'MediaPlugin: %s extensions: %s' % (mimetype,
            u' '.join(extensions)))
        # Add all extensions listed in self.additional_extensions, which
        # have this mimetype, previously claimed to be supported by Phonon,
        # to hack away mimetypes' shortcomings in providing some extensions.
        if mimetype in self.additional_extensions.keys():
            for extension in self.additional_extensions[mimetype]:
                ext = u'*%s' % extensions
                if ext not in list:
                    list.append(ext)
                    self.serviceManager.supportedSuffixes(extension[1:])
            log.info(u'MediaPlugin: %s additional extensions: %s' % (mimetype,
                u' '.join(self.additional_extensions[mimetype])))

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
            u'load': translate('MediaPlugin', 'Load a new Media'),
            u'import': u'',
            u'new': translate('MediaPlugin', 'Add a new Media'),
            u'edit': translate('MediaPlugin', 'Edit the selected Media'),
            u'delete': translate('MediaPlugin', 'Delete the selected Media'),
            u'preview': translate('MediaPlugin', 'Preview the selected Media'),
            u'live': translate('MediaPlugin', 'Send the selected Media live'),
            u'service': translate('MediaPlugin',
                'Add the selected Media to the service')
        }
        self.setPluginUiTextStrings(tooltips)
