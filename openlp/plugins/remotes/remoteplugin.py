# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
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

from PyQt4 import QtGui

from openlp.core.lib import Plugin, StringContent, translate, build_icon
from openlp.core.common import Registry
from openlp.plugins.remotes.lib import RemoteTab, OpenLPServer, WebSocketManager

log = logging.getLogger(__name__)

__default_settings__ = {
    'remotes/twelve hour': True,
    'remotes/port': 4316,
    'remotes/https port': 4317,
    'remotes/https enabled': False,
    'remotes/user id': 'openlp',
    'remotes/password': 'password',
    'remotes/authentication enabled': False,
    'remotes/ip address': '0.0.0.0'
}


class RemotesPlugin(Plugin):
    log.info('Remote Plugin loaded')

    def __init__(self):
        """
        remotes constructor
        """
        super(RemotesPlugin, self).__init__('remotes', __default_settings__, settings_tab_class=RemoteTab)
        self.icon_path = ':/plugins/plugin_remote.png'
        self.icon = build_icon(self.icon_path)
        self.weight = -1
        self.server = None
        self.websocketserver = None

    def initialise(self):
        """
        Initialise the remotes plugin, and start the http server
        """
        log.debug('initialise')
        super(RemotesPlugin, self).initialise()
        self.server = OpenLPServer()
        self.websocketserver = WebSocketManager()
        self.websocketserver.start()
        Registry().register_function('websock_send', self.websocketserver.send)
        if not hasattr(self, 'remote_server_icon'):
            self.remote_server_icon = QtGui.QLabel(self.main_window.status_bar)
            size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(self.remote_server_icon.sizePolicy().hasHeightForWidth())
            self.remote_server_icon.setSizePolicy(size_policy)
            self.remote_server_icon.setFrameShadow(QtGui.QFrame.Plain)
            self.remote_server_icon.setLineWidth(1)
            self.remote_server_icon.setScaledContents(True)
            self.remote_server_icon.setFixedSize(20, 20)
            self.remote_server_icon.setObjectName('remote_server_icon')
            self.main_window.status_bar.insertPermanentWidget(2, self.remote_server_icon)
            self.settings_tab.remote_server_icon = self.remote_server_icon
        self.settings_tab.generate_icon()

    def finalise(self):
        """
        Tidy up and close down the http server
        """
        log.debug('finalise')
        super(RemotesPlugin, self).finalise()
        if self.server:
            self.server.stop_server()
            self.server = None
        if self.websocketserver:
            self.websocketserver.stop()
            self.websocketserver = None

    def about(self):
        """
        Information about this plugin
        """
        about_text = translate('RemotePlugin', '<strong>Remote Plugin</strong>'
                               '<br />The remote plugin provides the ability to send messages to '
                               'a running version of OpenLP on a different computer via a web '
                               'browser or through the remote API.')
        return about_text

    def set_plugin_text_strings(self):
        """
        Called to define all translatable texts of the plugin
        """
        # Name PluginList
        self.text_strings[StringContent.Name] = {
            'singular': translate('RemotePlugin', 'Remote', 'name singular'),
            'plural': translate('RemotePlugin', 'Remotes', 'name plural')
        }
        # Name for MediaDockManager, SettingsManager
        self.text_strings[StringContent.VisibleName] = {
            'title': translate('RemotePlugin', 'Remote', 'container title')
        }

    def config_update(self):
        """
        Called when Config is changed to requests a restart with the server on new address or port
        """
        log.debug('remote config changed')
        QtGui.QMessageBox.information(self.main_window,
                                      translate('RemotePlugin', 'Server Config Change'),
                                      translate('RemotePlugin', 'Server configuration changes will require a restart '
                                                'to take effect.'),
                                      QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
