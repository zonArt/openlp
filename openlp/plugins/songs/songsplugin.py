# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin, Event,  EventType,  translate
from openlp.plugins.songs.lib import SongManager, SongsTab, SongMediaItem
from openlp.plugins.songs.forms import OpenLPImportForm, OpenSongExportForm, \
    OpenSongImportForm, OpenLPExportForm

class SongsPlugin(Plugin):

    global log
    log = logging.getLogger(u'SongsPlugin')
    log.info(u'Song Plugin loaded')

    def __init__(self, plugin_helpers):
        # Call the parent constructor
        Plugin.__init__(self, u'Songs', u'1.9.0', plugin_helpers)
        self.weight = -10
        self.songmanager = SongManager(self.config)
        self.openlp_import_form = OpenLPImportForm()
        self.opensong_import_form = OpenSongImportForm()
        self.openlp_export_form = OpenLPExportForm()
        self.opensong_export_form = OpenSongExportForm()
        # Create the plugin icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(':/media/media_song.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)

    def get_media_manager_item(self):
        # Create the MediaManagerItem object
        self.media_item = SongMediaItem(self, self.icon, 'Songs')
        return self.media_item

    def add_import_menu_item(self, import_menu):
        self.ImportSongMenu = QtGui.QMenu(import_menu)
        self.ImportSongMenu.setObjectName(u'ImportSongMenu')
        self.ImportOpenSongItem = QtGui.QAction(import_menu)
        self.ImportOpenSongItem.setObjectName(u'ImportOpenSongItem')
        self.ImportOpenlp1Item = QtGui.QAction(import_menu)
        self.ImportOpenlp1Item.setObjectName(u'ImportOpenlp1Item')
        self.ImportOpenlp2Item = QtGui.QAction(import_menu)
        self.ImportOpenlp2Item.setObjectName(u'ImportOpenlp2Item')
        # Add to menus
        self.ImportSongMenu.addAction(self.ImportOpenlp1Item)
        self.ImportSongMenu.addAction(self.ImportOpenlp2Item)
        self.ImportSongMenu.addAction(self.ImportOpenSongItem)
        import_menu.addAction(self.ImportSongMenu.menuAction())
        # Translations...
        self.ImportSongMenu.setTitle(translate(u'main_window', u'&Song'))
        self.ImportOpenSongItem.setText(translate(u'main_window', u'OpenSong'))
        self.ImportOpenlp1Item.setText(translate(u'main_window', u'openlp.org 1.0'))
        self.ImportOpenlp1Item.setToolTip(translate(u'main_window', u'Export songs in openlp.org 1.0 format'))
        self.ImportOpenlp1Item.setStatusTip(translate(u'main_window', u'Export songs in openlp.org 1.0 format'))
        self.ImportOpenlp2Item.setText(translate(u'main_window', u'OpenLP 2.0'))
        self.ImportOpenlp2Item.setToolTip(translate(u'main_window', u'Export songs in OpenLP 2.0 format'))
        self.ImportOpenlp2Item.setStatusTip(translate(u'main_window', u'Export songs in OpenLP 2.0 format'))
        # Signals and slots
        QtCore.QObject.connect(self.ImportOpenlp1Item, QtCore.SIGNAL(u'triggered()'), self.onImportOpenlp1ItemClick)
        QtCore.QObject.connect(self.ImportOpenlp2Item, QtCore.SIGNAL(u'triggered()'), self.onImportOpenlp1ItemClick)
        QtCore.QObject.connect(self.ImportOpenSongItem, QtCore.SIGNAL(u'triggered()'), self.onImportOpenSongItemClick)

    def add_export_menu_item(self, export_menu):
        self.ExportSongMenu = QtGui.QMenu(export_menu)
        self.ExportSongMenu.setObjectName(u'ExportSongMenu')
        self.ExportOpenSongItem = QtGui.QAction(export_menu)
        self.ExportOpenSongItem.setObjectName(u'ExportOpenSongItem')
        self.ExportOpenlp1Item = QtGui.QAction(export_menu)
        self.ExportOpenlp1Item.setObjectName(u'ExportOpenlp1Item')
        self.ExportOpenlp2Item = QtGui.QAction(export_menu)
        self.ExportOpenlp2Item.setObjectName(u'ExportOpenlp2Item')
        # Add to menus
        self.ExportSongMenu.addAction(self.ExportOpenlp1Item)
        self.ExportSongMenu.addAction(self.ExportOpenlp2Item)
        self.ExportSongMenu.addAction(self.ExportOpenSongItem)
        export_menu.addAction(self.ExportSongMenu.menuAction())
        # Translations...
        self.ExportSongMenu.setTitle(translate(u'main_window', u'&Song'))
        self.ExportOpenSongItem.setText(translate(u'main_window', u'OpenSong'))
        self.ExportOpenlp1Item.setText(translate(u'main_window', u'openlp.org 1.0'))
        self.ExportOpenlp2Item.setText(translate(u'main_window', u'OpenLP 2.0'))
        # Signals and slots
        QtCore.QObject.connect(self.ExportOpenlp1Item, QtCore.SIGNAL(u'triggered()'), self.onExportOpenlp1ItemClicked)
        QtCore.QObject.connect(self.ExportOpenSongItem, QtCore.SIGNAL(u'triggered()'), self.onExportOpenSongItemClicked)

    def initialise(self):
        self.media_item.displayResults(self.songmanager.get_songs())

    def onImportOpenlp1ItemClick(self):
        self.openlp_import_form.show()

    def onImportOpenSongItemClick(self):
        self.opensong_import_form.show()

    def onExportOpenlp1ItemClicked(self):
        self.openlp_export_form.show()

    def onExportOpenSongItemClicked(self):
        self.opensong_export_form.show()

    def handle_event(self, event):
        """
        Handle the event contained in the event object.
        """
        log.debug(u'Handle event called with event %s' % event.event_type)
        if event.event_type == EventType.ThemeListChanged:
            log.debug(u'New Theme request received')
            self.media_item.edit_song_form.loadThemes(self.theme_manager.getThemes())
        if event.event_type == EventType.LoadServiceItem and event.payload == 'Song':
            log.debug(u'Load Service Item received')
            self.media_item.onSongAddClick()
        if event.event_type == EventType.PreviewShow and event.payload == 'Song':
            log.debug(u'Load Preview Item received ')
            self.media_item.onSongPreviewClick()
        if event.event_type == EventType.LiveShow and event.payload == 'Song':
            log.debug(u'Load Live Show Item received')
            self.media_item.onSongLiveClick()
