# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from openlp.core.lib import Plugin, buildIcon
from openlp.plugins.media.lib import MediaTab, MediaMediaItem

class MediaPlugin(Plugin):

    def __init__(self, plugin_helpers):
        # Call the parent constructor
        Plugin.__init__(self, u'Media', u'1.9.0', plugin_helpers)
        self.weight = -6
        # Create the plugin icon
        self.icon = buildIcon(u':/media/media_video.png')
        # passed with drag and drop messages
        self.dnd_id = u'Media'

    def get_settings_tab(self):
        self.MediaTab = MediaTab()
        return self.MediaTab

    def get_media_manager_item(self):
        # Create the MediaManagerItem object
        return MediaMediaItem(self, self.icon, u'Media')

    def about(self):
        return u'<b>Media Plugin</b> <br> One day this may provide access to video and audio clips'
