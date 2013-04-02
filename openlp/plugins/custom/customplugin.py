# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
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
"""
The :mod:`~openlp.plugins.custom.customplugin` module contains the Plugin class
for the Custom Slides plugin.
"""

import logging

from openlp.core.lib import Plugin, StringContent, build_icon, translate
from openlp.core.lib.db import Manager
from openlp.plugins.custom.lib import CustomMediaItem, CustomTab
from openlp.plugins.custom.lib.db import CustomSlide, init_schema
from openlp.plugins.custom.lib.mediaitem import CustomSearch

log = logging.getLogger(__name__)

__default_settings__ = {
        u'custom/db type': u'sqlite',
        u'custom/last search type':  CustomSearch.Titles,
        u'custom/display footer': True,
        u'custom/add custom from service': True
    }


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

    def __init__(self):
        Plugin.__init__(self, u'custom', __default_settings__, CustomMediaItem, CustomTab)
        self.weight = -5
        self.manager = Manager(u'custom', init_schema)
        self.iconPath = u':/plugins/plugin_custom.png'
        self.icon = build_icon(self.iconPath)

    def about(self):
        about_text = translate('CustomPlugin', '<strong>Custom Slide Plugin </strong><br />The custom slide plugin '
            'provides the ability to set up custom text slides that can be displayed on the screen '
            'the same way songs are. This plugin provides greater freedom over the songs plugin.')
        return about_text

    def usesTheme(self, theme):
        """
        Called to find out if the custom plugin is currently using a theme.

        Returns True if the theme is being used, otherwise returns False.
        """
        if self.manager.get_all_objects(CustomSlide, CustomSlide.theme_name == theme):
            return True
        return False

    def renameTheme(self, oldTheme, newTheme):
        """
        Renames a theme the custom plugin is using making the plugin use the
        new name.

        ``oldTheme``
            The name of the theme the plugin should stop using.

        ``newTheme``
            The new name the plugin should now use.
        """
        customsUsingTheme = self.manager.get_all_objects(CustomSlide, CustomSlide.theme_name == oldTheme)
        for custom in customsUsingTheme:
            custom.theme_name = newTheme
            self.manager.save_object(custom)

    def setPluginTextStrings(self):
        """
        Called to define all translatable texts of the plugin
        """
        ## Name PluginList ##
        self.textStrings[StringContent.Name] = {
            u'singular': translate('CustomPlugin', 'Custom Slide', 'name singular'),
            u'plural': translate('CustomPlugin', 'Custom Slides', 'name plural')
        }
        ## Name for MediaDockManager, SettingsManager ##
        self.textStrings[StringContent.VisibleName] = {
            u'title': translate('CustomPlugin', 'Custom Slides', 'container title')
        }
        # Middle Header Bar
        tooltips = {
            u'load': translate('CustomPlugin', 'Load a new custom slide.'),
            u'import': translate('CustomPlugin', 'Import a custom slide.'),
            u'new': translate('CustomPlugin', 'Add a new custom slide.'),
            u'edit': translate('CustomPlugin', 'Edit the selected custom slide.'),
            u'delete': translate('CustomPlugin', 'Delete the selected custom slide.'),
            u'preview': translate('CustomPlugin', 'Preview the selected custom slide.'),
            u'live': translate('CustomPlugin', 'Send the selected custom slide live.'),
            u'service': translate('CustomPlugin', 'Add the selected custom slide to the service.')
        }
        self.setPluginUiTextStrings(tooltips)

    def finalise(self):
        """
        Time to tidy up on exit
        """
        log.info(u'Custom Finalising')
        self.manager.finalise()
        Plugin.finalise(self)
