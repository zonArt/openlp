# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
import os
from tempfile import gettempdir

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin, StringContent, build_icon, translate, \
    Receiver
from openlp.core.lib.db import Manager
from openlp.core.lib.ui import UiStrings, base_action, icon_action
from openlp.core.utils.actions import ActionList
from openlp.plugins.songs.lib import clean_song, SongMediaItem, SongsTab
from openlp.plugins.songs.lib.db import init_schema, Song
from openlp.plugins.songs.lib.importer import SongFormat
from openlp.plugins.songs.lib.olpimport import OpenLPSongImport

log = logging.getLogger(__name__)

class SongsPlugin(Plugin):
    """
    This is the number 1 plugin, if importance were placed on any
    plugins. This plugin enables the user to create, edit and display
    songs. Songs are divided into verses, and the verse order can be
    specified. Authors, topics and song books can be assigned to songs
    as well.
    """
    log.info(u'Song Plugin loaded')

    def __init__(self, plugin_helpers):
        """
        Create and set up the Songs plugin.
        """
        Plugin.__init__(self, u'Songs', plugin_helpers, SongMediaItem, SongsTab)
        self.weight = -10
        self.manager = Manager(u'songs', init_schema)
        self.icon_path = u':/plugins/plugin_songs.png'
        self.icon = build_icon(self.icon_path)

    def initialise(self):
        log.info(u'Songs Initialising')
        Plugin.initialise(self)
        self.songImportItem.setVisible(True)
        self.songExportItem.setVisible(True)
        self.toolsReindexItem.setVisible(True)
        action_list = ActionList.get_instance()
        action_list.add_action(self.songImportItem, UiStrings().Import)
        action_list.add_action(self.songExportItem, UiStrings().Export)
        action_list.add_action(self.toolsReindexItem, UiStrings().Tools)

    def addImportMenuItem(self, import_menu):
        """
        Give the Songs plugin the opportunity to add items to the
        **Import** menu.

        ``import_menu``
            The actual **Import** menu item, so that your actions can
            use it as their parent.
        """
        # Main song import menu item - will eventually be the only one
        self.songImportItem = base_action(import_menu, u'songImportItem')
        self.songImportItem.setText(translate('SongsPlugin', '&Song'))
        self.songImportItem.setToolTip(translate('SongsPlugin',
            'Import songs using the import wizard.'))
        import_menu.addAction(self.songImportItem)
        # Signals and slots
        QtCore.QObject.connect(self.songImportItem,
            QtCore.SIGNAL(u'triggered()'), self.onSongImportItemClicked)

    def addExportMenuItem(self, export_menu):
        """
        Give the Songs plugin the opportunity to add items to the
        **Export** menu.

        ``export_menu``
            The actual **Export** menu item, so that your actions can
            use it as their parent.
        """
        # Main song import menu item - will eventually be the only one
        self.songExportItem = base_action(export_menu, u'songExportItem')
        self.songExportItem.setText(translate('SongsPlugin', '&Song'))
        self.songExportItem.setToolTip(translate('SongsPlugin',
            'Exports songs using the export wizard.'))
        export_menu.addAction(self.songExportItem)
        # Signals and slots
        QtCore.QObject.connect(self.songExportItem,
            QtCore.SIGNAL(u'triggered()'), self.onSongExportItemClicked)

    def addToolsMenuItem(self, tools_menu):
        """
        Give the alerts plugin the opportunity to add items to the
        **Tools** menu.

        ``tools_menu``
            The actual **Tools** menu item, so that your actions can
            use it as their parent.
        """
        log.info(u'add tools menu')
        self.toolsReindexItem = icon_action(tools_menu, u'toolsReindexItem',
            u':/plugins/plugin_songs.png')
        self.toolsReindexItem.setText(
            translate('SongsPlugin', '&Re-index Songs'))
        self.toolsReindexItem.setStatusTip(
            translate('SongsPlugin', 'Re-index the songs database to improve '
            'searching and ordering.'))
        tools_menu.addAction(self.toolsReindexItem)
        QtCore.QObject.connect(self.toolsReindexItem,
            QtCore.SIGNAL(u'triggered()'), self.onToolsReindexItemTriggered)
        self.toolsReindexItem.setVisible(False)

    def onToolsReindexItemTriggered(self):
        """
        Rebuild each song.
        """
        maxSongs = self.manager.get_object_count(Song)
        if maxSongs == 0:
            return
        progressDialog = QtGui.QProgressDialog(
            translate('SongsPlugin', 'Reindexing songs...'), UiStrings().Cancel,
            0, maxSongs, self.formparent)
        progressDialog.setWindowModality(QtCore.Qt.WindowModal)
        songs = self.manager.get_all_objects(Song)
        for number, song in enumerate(songs):
            clean_song(self.manager, song)
            progressDialog.setValue(number + 1)
        self.manager.save_objects(songs)
        self.mediaItem.onSearchTextButtonClick()

    def onSongImportItemClicked(self):
        if self.mediaItem:
            self.mediaItem.onImportClick()

    def onSongExportItemClicked(self):
        if self.mediaItem:
            self.mediaItem.onExportClick()

    def about(self):
        return translate('SongsPlugin', '<strong>Songs Plugin</strong>'
            '<br />The songs plugin provides the ability to display and '
            'manage songs.')

    def usesTheme(self, theme):
        """
        Called to find out if the song plugin is currently using a theme.

        Returns True if the theme is being used, otherwise returns False.
        """
        if self.manager.get_all_objects(Song, Song.theme_name == theme):
            return True
        return False

    def renameTheme(self, oldTheme, newTheme):
        """
        Renames a theme the song plugin is using making the plugin use the new
        name.

        ``oldTheme``
            The name of the theme the plugin should stop using.

        ``newTheme``
            The new name the plugin should now use.
        """
        songsUsingTheme = self.manager.get_all_objects(Song,
            Song.theme_name == oldTheme)
        for song in songsUsingTheme:
            song.theme_name = newTheme
            self.manager.save_object(song)

    def importSongs(self, format, **kwargs):
        class_ = SongFormat.get_class(format)
        importer = class_(self.manager, **kwargs)
        importer.register(self.mediaItem.import_wizard)
        return importer

    def setPluginTextStrings(self):
        """
        Called to define all translatable texts of the plugin
        """
        ## Name PluginList ##
        self.textStrings[StringContent.Name] = {
            u'singular': translate('SongsPlugin', 'Song', 'name singular'),
            u'plural': translate('SongsPlugin', 'Songs', 'name plural')
        }
        ## Name for MediaDockManager, SettingsManager ##
        self.textStrings[StringContent.VisibleName] = {
            u'title': translate('SongsPlugin', 'Songs', 'container title')
        }
        # Middle Header Bar
        tooltips = {
            u'load': u'',
            u'import': u'',
            u'new': translate('SongsPlugin', 'Add a new Song.'),
            u'edit': translate('SongsPlugin', 'Edit the selected Song.'),
            u'delete': translate('SongsPlugin', 'Delete the selected Song.'),
            u'preview': translate('SongsPlugin', 'Preview the selected Song.'),
            u'live': translate('SongsPlugin', 'Send the selected Song live.'),
            u'service': translate('SongsPlugin',
                'Add the selected Song to the service.')
        }
        self.setPluginUiTextStrings(tooltips)

    def firstTime(self):
        """
        If the first time wizard has run, this function is run to import all the
        new songs into the database.
        """
        db_dir = unicode(os.path.join(gettempdir(), u'openlp'))
        song_dbs = []
        for sfile in os.listdir(db_dir):
            if sfile.startswith(u'songs_') and sfile.endswith(u'.sqlite'):
                song_dbs.append(os.path.join(db_dir, sfile))
        self.onToolsReindexItemTriggered()
        if len(song_dbs) == 0:
            return
        progress = QtGui.QProgressDialog(self.formparent)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setLabelText(translate('OpenLP.Ui', 'Starting import...'))
        progress.setCancelButton(None)
        progress.setRange(0, len(song_dbs))
        progress.setMinimumDuration(0)
        progress.forceShow()
        for idx, db in enumerate(song_dbs):
            progress.setValue(idx)
            Receiver.send_message(u'openlp_process_events')
            importer = OpenLPSongImport(self.manager, filename=db)
            importer.do_import()
        progress.setValue(len(song_dbs))
        self.mediaItem.onSearchTextButtonClick()

    def finalise(self):
        """
        Time to tidy up on exit
        """
        log.info(u'Songs Finalising')
        self.manager.finalise()
        self.songImportItem.setVisible(False)
        self.songExportItem.setVisible(False)
        self.toolsReindexItem.setVisible(False)
        action_list = ActionList.get_instance()
        action_list.remove_action(self.songImportItem, UiStrings().Import)
        action_list.remove_action(self.songExportItem, UiStrings().Export)
        action_list.remove_action(self.toolsReindexItem, UiStrings().Tools)
        Plugin.finalise(self)

