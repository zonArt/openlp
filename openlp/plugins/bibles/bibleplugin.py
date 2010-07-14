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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin, build_icon, PluginStatus, translate
from openlp.plugins.bibles.lib import BibleManager, BiblesTab, BibleMediaItem

log = logging.getLogger(__name__)

class BiblePlugin(Plugin):
    log.info(u'Bible Plugin loaded')

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Bibles', u'1.9.2', plugin_helpers)
        self.weight = -9
        self.icon_path = u':/plugins/plugin_bibles.png'
        self.icon = build_icon(self.icon_path)
        #Register the bible Manager
        self.status = PluginStatus.Active
        self.manager = None

    def initialise(self):
        log.info(u'bibles Initialising')
        if self.manager is None:
            self.manager = BibleManager(self)
        Plugin.initialise(self)
        self.ImportBibleItem.setVisible(True)
        self.ExportBibleItem.setVisible(True)

    def finalise(self):
        log.info(u'Plugin Finalise')
        Plugin.finalise(self)
        self.ImportBibleItem.setVisible(False)
        self.ExportBibleItem.setVisible(False)

    def getSettingsTab(self):
        return BiblesTab(self.name)

    def getMediaManagerItem(self):
        # Create the BibleManagerItem object
        return BibleMediaItem(self, self.icon, self.name)

    def addImportMenuItem(self, import_menu):
        self.ImportBibleItem = QtGui.QAction(import_menu)
        self.ImportBibleItem.setObjectName(u'ImportBibleItem')
        import_menu.addAction(self.ImportBibleItem)
        self.ImportBibleItem.setText(
            translate('BiblePlugin', '&Bible'))
        # Signals and slots
        QtCore.QObject.connect(self.ImportBibleItem,
            QtCore.SIGNAL(u'triggered()'), self.onBibleImportClick)
        self.ImportBibleItem.setVisible(False)

    def addExportMenuItem(self, export_menu):
        self.ExportBibleItem = QtGui.QAction(export_menu)
        self.ExportBibleItem.setObjectName(u'ExportBibleItem')
        export_menu.addAction(self.ExportBibleItem)
        self.ExportBibleItem.setText(translate(
            'BiblePlugin', '&Bible'))
        self.ExportBibleItem.setVisible(False)

    def onBibleImportClick(self):
        if self.mediaItem:
            self.mediaItem.onImportClick()

    def about(self):
        about_text = translate('BiblePlugin',
            '<strong>Bible Plugin</strong><br />This '
            'plugin allows bible verses from different sources to be '
            'displayed on the screen during the service.')
        return about_text

    def usesTheme(self, theme):
        """
        Called to find out if the bible plugin is currently using a theme.

        Returns True if the theme is being used, otherwise returns False.
        """
        if self.settings_tab.bible_theme == theme:
            return True
        return False

    def renameTheme(self, oldTheme, newTheme):
        """
        Rename the theme the bible plugin is using making the plugin use the
        new name.

        ``oldTheme``
            The name of the theme the plugin should stop using. Unused for
            this particular plugin.

        ``newTheme``
            The new name the plugin should now use.
        """
        self.settings_tab.bible_theme = newTheme
