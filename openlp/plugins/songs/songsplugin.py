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

from openlp.core.resources import *
from openlp.core.lib import Plugin
from openlp.plugins.songs.lib import SongManager, SongsTab, SongMediaItem
from openlp.plugins.songs.forms import OpenLPImportForm, OpenSongExportForm, \
    OpenSongImportForm, OpenLPExportForm

class SongsPlugin(Plugin):

    global log
    log=logging.getLogger(u'SongsPlugin')
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
        self.MediaManagerItem = SongMediaItem(self, self.icon, 'Songs')
        return self.MediaManagerItem

    def add_import_menu_item(self, import_menu):
        self.ImportSongMenu = QtGui.QMenu(import_menu)
        self.ImportSongMenu.setObjectName("ImportSongMenu")
        self.ImportOpenSongItem = QtGui.QAction(import_menu)
        self.ImportOpenSongItem.setObjectName("ImportOpenSongItem")
        self.ImportOpenlp1Item = QtGui.QAction(import_menu)
        self.ImportOpenlp1Item.setObjectName("ImportOpenlp1Item")
        self.ImportOpenlp2Item = QtGui.QAction(import_menu)
        self.ImportOpenlp2Item.setObjectName("ImportOpenlp2Item")
        # Add to menus
        self.ImportSongMenu.addAction(self.ImportOpenlp1Item)
        self.ImportSongMenu.addAction(self.ImportOpenlp2Item)
        self.ImportSongMenu.addAction(self.ImportOpenSongItem)
        import_menu.addAction(self.ImportSongMenu.menuAction())
        # Translations...
        self.ImportSongMenu.setTitle(QtGui.QApplication.translate("main_window", "&Song", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportOpenSongItem.setText(QtGui.QApplication.translate("main_window", "OpenSong", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportOpenlp1Item.setText(QtGui.QApplication.translate("main_window", "openlp.org 1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportOpenlp1Item.setToolTip(QtGui.QApplication.translate("main_window", "Export songs in openlp.org 1.0 format", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportOpenlp1Item.setStatusTip(QtGui.QApplication.translate("main_window", "Export songs in openlp.org 1.0 format", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportOpenlp2Item.setText(QtGui.QApplication.translate("main_window", "OpenLP 2.0", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportOpenlp2Item.setToolTip(QtGui.QApplication.translate("main_window", "Export songs in OpenLP 2.0 format", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportOpenlp2Item.setStatusTip(QtGui.QApplication.translate("main_window", "Export songs in OpenLP 2.0 format", None, QtGui.QApplication.UnicodeUTF8))
        # Signals and slots
        QtCore.QObject.connect(self.ImportOpenlp1Item, QtCore.SIGNAL("triggered()"), self.onImportOpenlp1ItemClick)
        QtCore.QObject.connect(self.ImportOpenlp2Item, QtCore.SIGNAL("triggered()"), self.onImportOpenlp1ItemClick)
        QtCore.QObject.connect(self.ImportOpenSongItem, QtCore.SIGNAL("triggered()"), self.onImportOpenSongItemClick)


    def add_export_menu_item(self, export_menu):
        self.ExportSongMenu = QtGui.QMenu(export_menu)
        self.ExportSongMenu.setObjectName("ExportSongMenu")
        self.ExportOpenSongItem = QtGui.QAction(export_menu)
        self.ExportOpenSongItem.setObjectName("ExportOpenSongItem")
        self.ExportOpenlp1Item = QtGui.QAction(export_menu)
        self.ExportOpenlp1Item.setObjectName("ExportOpenlp1Item")
        self.ExportOpenlp2Item = QtGui.QAction(export_menu)
        self.ExportOpenlp2Item.setObjectName("ExportOpenlp2Item")
        # Add to menus
        self.ExportSongMenu.addAction(self.ExportOpenlp1Item)
        self.ExportSongMenu.addAction(self.ExportOpenlp2Item)
        self.ExportSongMenu.addAction(self.ExportOpenSongItem)
        export_menu.addAction(self.ExportSongMenu.menuAction())
        # Translations...
        self.ExportSongMenu.setTitle(QtGui.QApplication.translate("main_window", "&Song", None, QtGui.QApplication.UnicodeUTF8))
        self.ExportOpenSongItem.setText(QtGui.QApplication.translate("main_window", "OpenSong", None, QtGui.QApplication.UnicodeUTF8))
        self.ExportOpenlp1Item.setText(QtGui.QApplication.translate("main_window", "openlp.org 1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.ExportOpenlp2Item.setText(QtGui.QApplication.translate("main_window", "OpenLP 2.0", None, QtGui.QApplication.UnicodeUTF8))
        # Signals and slots
        QtCore.QObject.connect(self.ExportOpenlp1Item, QtCore.SIGNAL("triggered()"), self.onExportOpenlp1ItemClicked)
        QtCore.QObject.connect(self.ExportOpenSongItem, QtCore.SIGNAL("triggered()"), self.onExportOpenSongItemClicked)

    def get_settings_tab(self):
        self.SongsTab = SongsTab()
        return self.SongsTab

    def initialise(self):
        pass

    def onImportOpenlp1ItemClick(self):
        self.openlp_import_form.show()

    def onImportOpenSongItemClick(self):
        self.opensong_import_form.show()

    def onExportOpenlp1ItemClicked(self):
        self.openlp_export_form.show()

    def onExportOpenSongItemClicked(self):
        self.opensong_export_form.show()
