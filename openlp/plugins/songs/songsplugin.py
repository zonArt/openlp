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
from openlp.core.utils.actions import ActionList
from openlp.plugins.songs.lib import clean_song, upgrade
from openlp.plugins.songs.lib.db import init_schema, Song
from openlp.plugins.songs.lib.mediaitem import SongSearch
from openlp.plugins.songs.lib.importer import SongFormat
from openlp.plugins.songs.lib.olpimport import OpenLPSongImport
from openlp.plugins.songs.lib.mediaitem import SongMediaItem
from openlp.plugins.songs.lib.songstab import SongsTab
from openlp.plugins.songs.forms.duplicatesongremovalform import DuplicateSongRemovalForm


log = logging.getLogger(__name__)
__default_settings__ = {
        'songs/db type': 'sqlite',
        'songs/last search type': SongSearch.Entire,
        'songs/last import type': SongFormat.OpenLyrics,
        'songs/update service on edit': False,
        'songs/search as type': False,
        'songs/add song from service': True,
        'songs/display songbar': True,
        'songs/last directory import': '',
        'songs/last directory export': ''
    }


class SongsPlugin(Plugin):
    """
    This is the number 1 plugin, if importance were placed on any
    plugins. This plugin enables the user to create, edit and display
    songs. Songs are divided into verses, and the verse order can be
    specified. Authors, topics and song books can be assigned to songs
    as well.
    """
    log.info('Song Plugin loaded')

    def __init__(self):
        """
        Create and set up the Songs plugin.
        """
        super(SongsPlugin, self).__init__('songs', __default_settings__, SongMediaItem, SongsTab)
        self.manager = Manager('songs', init_schema, upgrade_mod=upgrade)
        self.weight = -10
        self.icon_path = ':/plugins/plugin_songs.png'
        self.icon = build_icon(self.icon_path)

    def check_pre_conditions(self):
        """
        Check the plugin can run.
        """
        return self.manager.session is not None

    def initialise(self):
        log.info('Songs Initialising')
        super(SongsPlugin, self).initialise()
        self.song_import_item.setVisible(True)
        self.song_export_item.setVisible(True)
        self.tools_reindex_item.setVisible(True)
        self.tools_find_duplicates.setVisible(True)
        action_list = ActionList.get_instance()
        action_list.add_action(self.song_import_item, UiStrings().Import)
        action_list.add_action(self.song_export_item, UiStrings().Export)
        action_list.add_action(self.tools_reindex_item, UiStrings().Tools)
        action_list.add_action(self.tools_find_duplicates, UiStrings().Tools)

    def add_import_menu_item(self, import_menu):
        """
        Give the Songs plugin the opportunity to add items to the
        **Import** menu.

        ``import_menu``
            The actual **Import** menu item, so that your actions can
            use it as their parent.
        """
        # Main song import menu item - will eventually be the only one
        self.song_import_item = create_action(import_menu, 'songImportItem',
            text=translate('SongsPlugin', '&Song'),
            tooltip=translate('SongsPlugin', 'Import songs using the import wizard.'),
            triggers=self.on_song_import_item_clicked)
        import_menu.addAction(self.song_import_item)

    def add_export_menu_Item(self, export_menu):
        """
        Give the Songs plugin the opportunity to add items to the
        **Export** menu.

        ``export_menu``
            The actual **Export** menu item, so that your actions can
            use it as their parent.
        """
        # Main song import menu item - will eventually be the only one
        self.song_export_item = create_action(export_menu, 'songExportItem',
            text=translate('SongsPlugin', '&Song'),
            tooltip=translate('SongsPlugin', 'Exports songs using the export wizard.'),
            triggers=self.on_song_export_item_clicked)
        export_menu.addAction(self.song_export_item)

    def add_tools_menu_item(self, tools_menu):
        """
        Give the Songs plugin the opportunity to add items to the
        **Tools** menu.

        ``tools_menu``
            The actual **Tools** menu item, so that your actions can
            use it as their parent.
        """
        log.info('add tools menu')
        self.tools_reindex_item = create_action(tools_menu, 'toolsReindexItem',
            text=translate('SongsPlugin', '&Re-index Songs'),
            icon=':/plugins/plugin_songs.png',
            statustip=translate('SongsPlugin', 'Re-index the songs database to improve searching and ordering.'),
            visible=False, triggers=self.on_tools_reindex_item_triggered)
        tools_menu.addAction(self.tools_reindex_item)
        self.tools_find_duplicates = create_action(tools_menu, 'toolsFindDuplicates',
            text=translate('SongsPlugin', 'Find &Duplicate Songs'),
            statustip=translate('SongsPlugin',
            'Find and remove duplicate songs in the song database.'),
            visible=False, triggers=self.on_tools_find_duplicates_triggered, can_shortcuts=True)
        tools_menu.addAction(self.tools_find_duplicates)

    def on_tools_reindex_item_triggered(self):
        """
        Rebuild each song.
        """
        maxSongs = self.manager.get_object_count(Song)
        if maxSongs == 0:
            return
        progress_dialog = QtGui.QProgressDialog(translate('SongsPlugin', 'Reindexing songs...'), UiStrings().Cancel,
            0, maxSongs, self.main_window)
        progress_dialog.setWindowTitle(translate('SongsPlugin', 'Reindexing songs'))
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        songs = self.manager.get_all_objects(Song)
        for number, song in enumerate(songs):
            clean_song(self.manager, song)
            progress_dialog.setValue(number + 1)
        self.manager.save_objects(songs)
        self.media_item.on_search_text_button_clicked()

    def on_tools_find_duplicates_triggered(self):
        """
        Search for duplicates in the song database.
        """
        DuplicateSongRemovalForm(self).exec_()

    def on_song_import_item_clicked(self):
        if self.media_item:
            self.media_item.on_import_click()

    def on_song_export_item_clicked(self):
        if self.media_item:
            self.media_item.on_export_click()

    def about(self):
        return translate('SongsPlugin', '<strong>Songs Plugin</strong>'
            '<br />The songs plugin provides the ability to display and manage songs.')

    def uses_theme(self, theme):
        """
        Called to find out if the song plugin is currently using a theme.

        Returns True if the theme is being used, otherwise returns False.
        """
        if self.manager.get_all_objects(Song, Song.theme_name == theme):
            return True
        return False

    def rename_theme(self, oldTheme, newTheme):
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
        class_ = SongFormat.get(format, 'class')
        importer = class_(self.manager, **kwargs)
        importer.register(self.media_item.import_wizard)
        return importer

    def set_plugin_text_strings(self):
        """
        Called to define all translatable texts of the plugin
        """
        ## Name PluginList ##
        self.text_strings[StringContent.Name] = {
            'singular': translate('SongsPlugin', 'Song', 'name singular'),
            'plural': translate('SongsPlugin', 'Songs', 'name plural')
        }
        ## Name for MediaDockManager, SettingsManager ##
        self.text_strings[StringContent.VisibleName] = {
            'title': translate('SongsPlugin', 'Songs', 'container title')
        }
        # Middle Header Bar
        tooltips = {
            'load': '',
            'import': '',
            'new': translate('SongsPlugin', 'Add a new song.'),
            'edit': translate('SongsPlugin', 'Edit the selected song.'),
            'delete': translate('SongsPlugin', 'Delete the selected song.'),
            'preview': translate('SongsPlugin', 'Preview the selected song.'),
            'live': translate('SongsPlugin', 'Send the selected song live.'),
            'service': translate('SongsPlugin', 'Add the selected song to the service.')
        }
        self.set_plugin_ui_text_strings(tooltips)

    def first_time(self):
        """
        If the first time wizard has run, this function is run to import all the
        new songs into the database.
        """
        self.application.process_events()
        self.on_tools_reindex_item_triggered()
        self.application.process_events()
        db_dir = os.path.join(gettempdir(), 'openlp')
        if not os.path.exists(db_dir):
            return
        song_dbs = []
        song_count = 0
        for sfile in os.listdir(db_dir):
            if sfile.startswith('songs_') and sfile.endswith('.sqlite'):
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
        self.media_item.on_search_text_button_clicked()

    def finalise(self):
        """
        Time to tidy up on exit
        """
        log.info('Songs Finalising')
        self.new_service_created()
        # Clean up files and connections
        self.manager.finalise()
        self.song_import_item.setVisible(False)
        self.song_export_item.setVisible(False)
        self.tools_reindex_item.setVisible(False)
        self.tools_find_duplicates.setVisible(False)
        action_list = ActionList.get_instance()
        action_list.remove_action(self.song_import_item, UiStrings().Import)
        action_list.remove_action(self.song_export_item, UiStrings().Export)
        action_list.remove_action(self.tools_reindex_item, UiStrings().Tools)
        action_list.remove_action(self.tools_find_duplicates, UiStrings().Tools)
        super(SongsPlugin, self).finalise()

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
        cursor.execute('SELECT COUNT(id) AS song_count FROM songs')
        song_count = cursor.fetchone()[0]
        connection.close()
        try:
            song_count = int(song_count)
        except (TypeError, ValueError):
            song_count = 0
        return song_count
