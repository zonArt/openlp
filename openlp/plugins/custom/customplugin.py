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

from forms import EditCustomForm
from openlp.core.lib import Plugin, build_icon, PluginStatus,  translate
from openlp.plugins.custom.lib import CustomManager, CustomMediaItem, CustomTab

log = logging.getLogger(__name__)

class CustomPlugin(Plugin):
    """
    This plugin enables the user to create, edit and display
    custom slide shows. Custom shows are divided into slides.
    Each show is able to have it's own theme.
    Custom shows are designed to replace the use of songs where
    the songs plugin has become restrictive. Examples could be
    Welcome slides, Bible Reading information, Orders of service.
    """
    log.info(u'Custom Plugin loaded')

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Custom', u'1.9.1', plugin_helpers)
        self.weight = -5
        self.custommanager = CustomManager()
        self.edit_custom_form = EditCustomForm(self.custommanager)
        self.icon = build_icon(u':/media/media_custom.png')
        self.status = PluginStatus.Active

    def get_settings_tab(self):
        return CustomTab(self.name)

    def get_media_manager_item(self):
        # Create the CustomManagerItem object
        return CustomMediaItem(self, self.icon, self.name)

    def initialise(self):
        log.info(u'Plugin Initialising')
        Plugin.initialise(self)
        self.insert_toolbox_item()

    def finalise(self):
        log.info(u'Plugin Finalise')
        self.remove_toolbox_item()

    def about(self):
        about_text = translate('CustomPlugin','<b>Custom Plugin</b><br>This plugin '
            'allows slides to be displayed on the screen in the same way '
            'songs are. This plugin provides greater freedom over the '
            'songs plugin.<br>')
        return about_text

    def can_delete_theme(self, theme):
        if len(self.custommanager.get_customs_for_theme(theme)) == 0:
            return True
        return False
