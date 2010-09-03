# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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

from openlp.core.lib import Plugin, translate, build_icon
from openlp.plugins.remotes.lib import RemoteTab, HttpServer

log = logging.getLogger(__name__)

class RemotesPlugin(Plugin):
    log.info(u'Remote Plugin loaded')

    def __init__(self, plugin_helpers):
        """
        remotes constructor
        """
        self.set_plugin_translations()
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
        self.insertToolboxItem()
        self.server = HttpServer(self)

    def finalise(self):
        """
        Tidy up and close down the http server
        """
        log.debug(u'finalise')
        Plugin.finalise(self)
        if self.server:
            self.server.close()

    def getSettingsTab(self):
        """
        Create the settings Tab
        """
        return RemoteTab(self.name)

    def about(self):
        """
        Information about this plugin
        """
        about_text = translate('RemotePlugin', '<strong>Remote Plugin</strong>'
            '<br />The remote plugin provides the ability to send messages to '
            'a running version of OpenLP on a different computer via a web '
            'browser or through the remote API.')
        return about_text
    # rimach
    def set_plugin_translations(self):
        """
        Called to define all translatable texts of the plugin
        """
        self.name = u'Remotes'
        self.name_lower = u'remotes'
        self.text = {}
        #for context menu
#        self.text['context_edit'] = translate('RemotePlugin', '&Edit Remotes')
#        self.text['context_delete'] = translate('RemotePlugin', '&Delete Remotes')
#        self.text['context_preview'] = translate('RemotePlugin', '&Preview Remotes')
#        self.text['context_live'] = translate('RemotePlugin', '&Show Live')
#        # forHeaders in mediamanagerdock
#        self.text['import'] = translate('RemotePlugin', 'Import a Remotes')
#        self.text['file'] = translate('RemotePlugin', 'Load a new Remotes')
#        self.text['new'] = translate('RemotePlugin', 'Add a new Remotes')
#        self.text['edit'] = translate('RemotePlugin', 'Edit the selected Remotes')
#        self.text['delete'] = translate('RemotePlugin', 'Delete the selected Remotes')
#        self.text['delete_more'] = translate('RemotePlugin', 'Delete the selected Remotes')
#        self.text['preview'] = translate('RemotePlugin', 'Preview the selected Remotes')
#        self.text['preview_more'] = translate('RemotePlugin', 'Preview the selected Remotes')
#        self.text['live'] = translate('RemotePlugin', 'Send the selected Remotes live')
#        self.text['live_more'] = translate('RemotePlugin', 'Send the selected Remotes live')
#        self.text['service'] = translate('RemotePlugin', 'Add the selected Remotes to the service')
#        self.text['service_more'] = translate('RemotePlugin', 'Add the selected Remotes to the service')
#        # for names in mediamanagerdock and pluginlist
        self.text['name'] = translate('RemotePlugin', 'Remote')
        self.text['name_more'] = translate('RemotePlugin', 'Remotes')
