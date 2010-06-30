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

from openlp.core.lib import Plugin, translate, build_icon
from openlp.plugins.remotes.lib import RemoteTab, HttpServer

log = logging.getLogger(__name__)

class RemotesPlugin(Plugin):
    log.info(u'Remote Plugin loaded')

    def __init__(self, plugin_helpers):
        """
        remotes constructor
        """
        Plugin.__init__(self, u'Remotes', u'1.9.2', plugin_helpers)
        self.icon = build_icon(u':/plugins/plugin_remote.png')
        self.weight = -1
        self.server = None

    def initialise(self):
        """
        Initialise the remotes plugin, and start the http server
        """
        log.debug(u'initialise')
        Plugin.initialise(self)
        self.insert_toolbox_item()
        self.server = HttpServer(self)

    def finalise(self):
        """
        Tidy up and close down the http server
        """
        log.debug(u'finalise')
        self.remove_toolbox_item()
        if self.server:
            self.server.close()

    def get_settings_tab(self):
        """
        Create the settings Tab
        """
        return RemoteTab(self.name)

    def about(self):
        """
        Information about this plugin
        """
        about_text = translate('RemotePlugin',
            '<b>Remote Plugin</b><br>This plugin '
            'provides the ability to send messages to a running version of '
            'openlp on a different computer via a web browser or other app<br>'
            'The Primary use for this would be to send alerts from a creche')
        return about_text
