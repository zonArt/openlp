# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

from PyQt4.phonon import Phonon

from openlp.core.lib import Plugin, build_icon, PluginStatus, translate
from openlp.plugins.media.lib import MediaMediaItem

log = logging.getLogger(__name__)

class MediaPlugin(Plugin):
    log.info(u'%s MediaPlugin loaded', __name__)

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Media', u'1.9.2', plugin_helpers)
        self.weight = -6
        self.icon = build_icon(u':/plugins/plugin_media.png')
        # passed with drag and drop messages
        self.dnd_id = u'Media'
        self.status = PluginStatus.Active
        self.audio_list = u''
        self.video_list = u''
        for mimetype in Phonon.BackendCapabilities.availableMimeTypes():
            mimetype = unicode(mimetype)
            type = mimetype.split(u'audio/x-')
            self.audio_list, mimetype = self._add_to_list(self.audio_list,
                type, mimetype)
            type = mimetype.split(u'audio/')
            self.audio_list, mimetype = self._add_to_list(self.audio_list,
                type, mimetype)
            type = mimetype.split(u'video/x-')
            self.video_list, mimetype = self._add_to_list(self.video_list,
                type, mimetype)
            type = mimetype.split(u'video/')
            self.video_list, mimetype = self._add_to_list(self.video_list,
                type, mimetype)

    def _add_to_list(self, list, value, type):
        if len(value) == 2:
            if list.find(value[1]) == -1:
                list += u'*.%s ' % value[1]
                self.serviceManager.supportedSuffixes(value[1])
            type = u''
        return list, type

    def getMediaManagerItem(self):
        # Create the MediaManagerItem object
        return MediaMediaItem(self, self.icon, self.name)

    def about(self):
        about_text = translate('MediaPlugin',
            '<b>Media Plugin</b><br>This plugin '
            'allows the playing of audio and video media')
        return about_text