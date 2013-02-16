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
The :mod:`~openlp.plugins.songs.songsplugin` module contains the Plugin class
for the Songs plugin.
"""

import logging
import os
from tempfile import gettempdir
import sqlite3

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin, StringContent, UiStrings, build_icon, translate
from openlp.core.lib.db import Manager
from openlp.core.lib.ui import create_action
from openlp.core.utils import get_filesystem_encoding
from openlp.core.utils.actions import ActionList
from openlp.plugins.songs.lib import clean_song, upgrade, SongMediaItem, SongsTab
from openlp.plugins.songs.lib.db import init_schema, Song
from openlp.plugins.songs.lib.mediaitem import SongSearch
from openlp.plugins.songs.lib.importer import SongFormat
from openlp.plugins.songs.lib.olpimport import OpenLPSongImport

log = logging.getLogger(__name__)
__default_settings__ = {
        u'songs/db type': u'sqlite',
        u'songs/last search type': SongSearch.Entire,
        u'songs/last import type': SongFormat.OpenLyrics,
        u'songs/update service on edit': False,
        u'songs/search as type': False,
        u'songs/add song from service': True,
        u'songs/display songbar': True,
        u'songs/last directory import': u'',
        u'songs/last directory export': u''
    }


class SongsPlugin(Plugin):
    """
    This is the number 1 plugin, if importance were placed on any
    plugins. This plugin enables the user to create, edit and display
    songs. Songs are divided into verses, and the verse order can be
    specified. Authors, topics and song books can be assigned to songs
    as well.
    """
    log.info(u'Song Plugin loaded')

    def __init__(self):
        """
        Create and set up the Songs plugin.
        """
        Plugin.__init__(self, u'songs', __default_settings__, SongMediaItem, SongsTab)
        self.manager = Manager(u'songs', init_schema, upgrade_mod=upgrade)
        self.weight = -10
        self.iconPath = u':/plugins/plugin_songs.png'
        self.icon = build_icon(self.iconPath)

    def checkPreConditions(self):
        return self.manager.session is not None

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
        self.songImportItem = create_action(import_menu, u'songImportItem',
            text=translate('SongsPlugin', '&Song'),
            tooltip=translate('SongsPlugin', 'Import songs using the import wizard.'),
            triggers=self.onSongImportItemClicked)
        import_menu.addAction(self.songImportItem)

    def addExportMenuItem(self, export_menu):
        """
        Give the Songs plugin the opportunity to add items to the
        **Export** menu.

        ``export_menu``
            The actual **Export** menu item, so that your actions can
            use it as their parent.
        """
        # Main song import menu item - will eventually be the only one
        self.songExportItem = create_action(export_menu, u'songExportItem',
            text=translate('SongsPlugin', '&Song'),
            tooltip=translate('SongsPlugin', 'Exports songs using the export wizard.'),
            triggers=self.onSongExportItemClicked)
        export_menu.addAction(self.songExportItem)

    def addToolsMenuItem(self, tools_menu):
        """
        Give the alerts plugin the opportunity to add items to the
        **Tools** menu.

        ``tools_menu``
            The actual **Tools** menu item, so that your actions can
            use it as their parent.
        """
        log.info(u'add tools menu')
        self.toolsReindexItem = create_action(tools_menu, u'toolsReindexItem',
            text=translate('SongsPlugin', '&Re-index Songs'),
            icon=u':/plugins/plugin_songs.png',
            statustip=translate('SongsPlugin', 'Re-index the songs database to improve searching and ordering.'),
            visible=False, triggers=self.onToolsReindexItemTriggered)
        tools_menu.addAction(self.toolsReindexItem)

    def onToolsReindexItemTriggered(self):
        """
        Rebuild each song.
        """
        maxSongs = self.manager.get_object_count(Song)
        if maxSongs == 0:
            return
        progressDialog = QtGui.QProgressDialog(translate('SongsPlugin', 'Reindexing songs...'), UiStrings().Cancel,
            0, maxSongs, self.main_window)
        progressDialog.setWindowTitle(translate('SongsPlugin', 'Reindexing songs'))
        progressDialog.setWindowModality(QtCore.Qt.WindowModal)
        songs = self.manager.get_all_objects(Song)
        for number, song in enumerate(songs):
            clean_song(self.manager, song)
            progressDialog.setValue(number + 1)
        self.manager.save_objects(songs)
        self.mediaItem.onSearchTextButtonClicked()

    def onSongImportItemClicked(self):
        if self.mediaItem:
            self.mediaItem.onImportClick()

    def onSongExportItemClicked(self):
        if self.mediaItem:
            self.mediaItem.onExportClick()

    def about(self):
        return translate('SongsPlugin', '<strong>Songs Plugin</strong>'
            '<br />The songs plugin provides the ability to display and manage songs.')

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
        songsUsingTheme = self.manager.get_all_objects(Song, Song.theme_name == oldTheme)
        for song in songsUsingTheme:
            song.theme_name = newTheme
            self.manager.save_object(song)

    def importSongs(self, format, **kwargs):
        class_ = SongFormat.get(format, u'class')
        kwargs[u'plugin'] = self
        importer = class_(self.manager, **kwargs)
        importer.register(self.mediaItem.importWizard)
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
            u'new': translate('SongsPlugin', 'Add a new song.'),
            u'edit': translate('SongsPlugin', 'Edit the selected song.'),
            u'delete': translate('SongsPlugin', 'Delete the selected song.'),
            u'preview': translate('SongsPlugin', 'Preview the selected song.'),
            u'live': translate('SongsPlugin', 'Send the selected song live.'),
            u'service': translate('SongsPlugin',
                'Add the selected song to the service.')
        }
        self.setPluginUiTextStrings(tooltips)

    def first_time(self):
        """
        If the first time wizard has run, this function is run to import all the
        new songs into the database.
        """
        self.application.process_events()
        self.onToolsReindexItemTriggered()
        self.application.process_events()
        db_dir = unicode(os.path.join(unicode(gettempdir(), get_filesystem_encoding()), u'openlp'))
        if not os.path.exists(db_dir):
            return
        song_dbs = []
        song_count = 0
        for sfile in os.listdir(db_dir):
            if sfile.startswith(u'songs_') and sfile.endswith(u'.sqlite'):
                self.application.process_events()
                song_dbs.append(os.path.join(db_dir, sfile))
                song_count += self._countSongs(os.path.join(db_dir, sfile))
        if not song_dbs:
            return
        self.application.process_events()
        progress = QtGui.QProgressDialog(self.main_window)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setWindowTitle(translate('OpenLP.Ui', 'Importing Songs'))
        progress.setLabelText(translate('OpenLP.Ui', 'Starting import...'))
        progress.setCancelButton(None)
        progress.setRange(0, song_count)
        progress.setMinimumDuration(0)
        progress.forceShow()
        self.application.process_events()
        for db in song_dbs:
            importer = OpenLPSongImport(self.manager, filename=db)
            importer.doImport(progress)
            self.application.process_events()
        progress.setValue(song_count)
        self.mediaItem.onSearchTextButtonClicked()

    def finalise(self):
        """
        Time to tidy up on exit
        """
        log.info(u'Songs Finalising')
        self.new_service_created()
        # Clean up files and connections
        self.manager.finalise()
        self.songImportItem.setVisible(False)
        self.songExportItem.setVisible(False)
        self.toolsReindexItem.setVisible(False)
        action_list = ActionList.get_instance()
        action_list.remove_action(self.songImportItem, UiStrings().Import)
        action_list.remove_action(self.songExportItem, UiStrings().Export)
        action_list.remove_action(self.toolsReindexItem, UiStrings().Tools)
        Plugin.finalise(self)

    def new_service_created(self):
        """
        Remove temporary songs from the database
        """
        songs = self.manager.get_all_objects(Song, Song.temporary == True)
        for song in songs:
            self.manager.delete_object(Song, song.id)

    def _countSongs(self, db_file):
        """
        Provide a count of the songs in the database
        """
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute(u'SELECT COUNT(id) AS song_count FROM songs')
        song_count = cursor.fetchone()[0]
        connection.close()
        try:
            song_count = int(song_count)
        except (TypeError, ValueError):
            song_count = 0
        return song_count
