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

import logging

from PyQt4 import QtGui

from openlp.core.lib import Plugin, StringContent, build_icon, translate
from openlp.core.lib.ui import UiStrings, create_action
from openlp.core.utils.actions import ActionList
from openlp.plugins.bibles.lib import BibleManager, BiblesTab, BibleMediaItem, LayoutStyle, DisplayStyle, \
    LanguageSelection
from openlp.plugins.bibles.lib.mediaitem import BibleSearch
from openlp.plugins.bibles.forms import BibleUpgradeForm

log = logging.getLogger(__name__)


__default_settings__ = {
        u'bibles/db type': u'sqlite',
        u'bibles/last search type': BibleSearch.Reference,
        u'bibles/verse layout style': LayoutStyle.VersePerSlide,
        u'bibles/book name language': LanguageSelection.Bible,
        u'bibles/display brackets': DisplayStyle.NoBrackets,
        u'bibles/display new chapter': False,
        u'bibles/second bibles': True,
        u'bibles/advanced bible': u'',
        u'bibles/quick bible': u'',
        u'bibles/proxy name': u'',
        u'bibles/proxy address': u'',
        u'bibles/proxy username': u'',
        u'bibles/proxy password': u'',
        u'bibles/bible theme': u'',
        u'bibles/verse separator': u'',
        u'bibles/range separator': u'',
        u'bibles/list separator': u'',
        u'bibles/end separator': u'',
        u'bibles/last directory import': u''
    }


class BiblePlugin(Plugin):
    log.info(u'Bible Plugin loaded')

    def __init__(self):
        Plugin.__init__(self, u'bibles', __default_settings__, BibleMediaItem, BiblesTab)
        self.weight = -9
        self.iconPath = u':/plugins/plugin_bibles.png'
        self.icon = build_icon(self.iconPath)
        self.manager = None

    def initialise(self):
        log.info(u'bibles Initialising')
        if self.manager is None:
            self.manager = BibleManager(self)
        Plugin.initialise(self)
        self.importBibleItem.setVisible(True)
        action_list = ActionList.get_instance()
        action_list.add_action(self.importBibleItem, UiStrings().Import)
        # Do not add the action to the list yet.
        #action_list.add_action(self.exportBibleItem, UiStrings().Export)
        # Set to invisible until we can export bibles
        self.exportBibleItem.setVisible(False)
        self.toolsUpgradeItem.setVisible(bool(self.manager.old_bible_databases))

    def finalise(self):
        """
        Tidy up on exit
        """
        log.info(u'Plugin Finalise')
        self.manager.finalise()
        Plugin.finalise(self)
        action_list = ActionList.get_instance()
        action_list.remove_action(self.importBibleItem, UiStrings().Import)
        self.importBibleItem.setVisible(False)
        #action_list.remove_action(self.exportBibleItem, UiStrings().Export)
        self.exportBibleItem.setVisible(False)

    def app_startup(self):
        """
        Perform tasks on application startup
        """
        Plugin.app_startup(self)
        if self.manager.old_bible_databases:
            if QtGui.QMessageBox.information(self.main_window,
                translate('OpenLP', 'Information'),
                translate('OpenLP', 'Bible format has changed.\nYou have to upgrade your existing Bibles.\n'
                    'Should OpenLP upgrade now?'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)) == \
                    QtGui.QMessageBox.Yes:
                self.onToolsUpgradeItemTriggered()

    def addImportMenuItem(self, import_menu):
        self.importBibleItem = create_action(import_menu, u'importBibleItem',
            text=translate('BiblesPlugin', '&Bible'), visible=False,
            triggers=self.onBibleImportClick)
        import_menu.addAction(self.importBibleItem)

    def addExportMenuItem(self, export_menu):
        self.exportBibleItem = create_action(export_menu, u'exportBibleItem',
            text=translate('BiblesPlugin', '&Bible'),
            visible=False)
        export_menu.addAction(self.exportBibleItem)

    def addToolsMenuItem(self, tools_menu):
        """
        Give the bible plugin the opportunity to add items to the
        **Tools** menu.

        ``tools_menu``
            The actual **Tools** menu item, so that your actions can
            use it as their parent.
        """
        log.debug(u'add tools menu')
        self.toolsUpgradeItem = create_action(tools_menu, u'toolsUpgradeItem',
            text=translate('BiblesPlugin', '&Upgrade older Bibles'),
            statustip=translate('BiblesPlugin', 'Upgrade the Bible databases to the latest format.'),
            visible=False, triggers=self.onToolsUpgradeItemTriggered)
        tools_menu.addAction(self.toolsUpgradeItem)

    def onToolsUpgradeItemTriggered(self):
        """
        Upgrade older bible databases.
        """
        if not hasattr(self, u'upgrade_wizard'):
            self.upgrade_wizard = BibleUpgradeForm(self.main_window, self.manager, self)
        # If the import was not cancelled then reload.
        if self.upgrade_wizard.exec_():
            self.mediaItem.reloadBibles()

    def onBibleImportClick(self):
        if self.mediaItem:
            self.mediaItem.onImportClick()

    def about(self):
        about_text = translate('BiblesPlugin', '<strong>Bible Plugin</strong>'
            '<br />The Bible plugin provides the ability to display Bible '
            'verses from different sources during the service.')
        return about_text

    def usesTheme(self, theme):
        """
        Called to find out if the bible plugin is currently using a theme.
        Returns ``True`` if the theme is being used, otherwise returns
        ``False``.
        """
        return unicode(self.settingsTab.bible_theme) == theme

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
        self.settingsTab.bible_theme = newTheme
        self.settingsTab.save()

    def setPluginTextStrings(self):
        """
        Called to define all translatable texts of the plugin
        """
        ## Name PluginList ##
        self.textStrings[StringContent.Name] = {
            u'singular': translate('BiblesPlugin', 'Bible', 'name singular'),
            u'plural': translate('BiblesPlugin', 'Bibles', 'name plural')
        }
        ## Name for MediaDockManager, SettingsManager ##
        self.textStrings[StringContent.VisibleName] = {
            u'title': translate('BiblesPlugin', 'Bibles', 'container title')
        }
        # Middle Header Bar
        tooltips = {
            u'load': u'',
            u'import': translate('BiblesPlugin', 'Import a Bible.'),
            u'new': translate('BiblesPlugin', 'Add a new Bible.'),
            u'edit': translate('BiblesPlugin', 'Edit the selected Bible.'),
            u'delete': translate('BiblesPlugin', 'Delete the selected Bible.'),
            u'preview': translate('BiblesPlugin',
                'Preview the selected Bible.'),
            u'live': translate('BiblesPlugin', 'Send the selected Bible live.'),
            u'service': translate('BiblesPlugin', 'Add the selected Bible to the service.')
        }
        self.setPluginUiTextStrings(tooltips)
