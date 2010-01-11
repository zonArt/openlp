# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

from openlp.core.lib import Plugin, build_icon
from openlp.plugins.media.lib import MediaMediaItem

class MediaPlugin(Plugin):
    global log
    log = logging.getLogger(u'MediaPlugin')
    log.info(u'Media Plugin loaded')

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Media', u'1.9.0', plugin_helpers)
        self.weight = -6
        self.icon = build_icon(u':/media/media_video.png')
        # passed with drag and drop messages
        self.dnd_id = u'Media'

    def initialise(self):
        log.info(u'Plugin Initialising')
        Plugin.initialise(self)
        self.insert_toolbox_item()

    def finalise(self):
        log.info(u'Plugin Finalise')
        self.remove_toolbox_item()

    def get_media_manager_item(self):
        # Create the MediaManagerItem object
        return MediaMediaItem(self, self.icon, self.name)

    def about(self):
        about_text = self.trUtf8('<b>Media Plugin</b><br>This plugin '
            'allows the playing of audio and video media')
        return about_text