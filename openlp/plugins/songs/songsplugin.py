# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from openlp.core.lib import Plugin, buildIcon
from openlp.plugins.songs.lib import SongManager, SongMediaItem, SongsTab
from openlp.plugins.songs.forms import OpenLPImportForm, OpenSongExportForm, \
    OpenSongImportForm, OpenLPExportForm

class SongsPlugin(Plugin):
    """
    This is the number 1 plugin, if importance were placed on any
    plugins. This plugin enables the user to create, edit and display
    songs. Songs are divided into verses, and the verse order can be
    specified. Authors, topics and song books can be assigned to songs
    as well.
    """

    global log
    log = logging.getLogger(u'SongsPlugin')
    log.info(u'Song Plugin loaded')

    def __init__(self, plugin_helpers):
        """
        Create and set up the Songs plugin.
        """
        Plugin.__init__(self, u'Songs', u'1.9.0', plugin_helpers)
        self.weight = -10
        self.songmanager = SongManager(self.config)
        self.openlp_import_form = OpenLPImportForm()
        self.opensong_import_form = OpenSongImportForm()
        self.openlp_export_form = OpenLPExportForm()
        self.opensong_export_form = OpenSongExportForm()
        self.icon = buildIcon(u':/media/media_song.png')

    def can_be_disabled(self):
        return True

    def get_settings_tab(self):
        return SongsTab(self.name)

    def initialise(self):
        log.info(u'Songs Initialising')
        #if self.songmanager is None:
        #    self.songmanager = SongManager(self.config)
        Plugin.initialise(self)
        self.ImportSongMenu.menuAction().setVisible(True)
        self.ExportSongMenu.menuAction().setVisible(True)
        self.media_item.displayResultsSong(self.songmanager.get_songs())

    def finalise(self):
        log.info(u'Plugin Finalise')
        Plugin.finalise(self)
        self.remove_toolbox_item()
        self.ImportSongMenu.menuAction().setVisible(False)
        self.ExportSongMenu.menuAction().setVisible(False)

    def get_media_manager_item(self):
        """
        Create the MediaManagerItem object, which is displaed in the
        Media Manager.
        """
        return SongMediaItem(self, self.icon, self.name)

    def add_import_menu_item(self, import_menu):
        """
        Give the Songs plugin the opportunity to add items to the
        **Import** menu.

        ``import_menu``
            The actual **Import** menu item, so that your actions can
            use it as their parent.
        """
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
        self.ImportSongMenu.setTitle(import_menu.trUtf8(u'&Song'))
        self.ImportOpenSongItem.setText(import_menu.trUtf8(u'OpenSong'))
        self.ImportOpenlp1Item.setText(import_menu.trUtf8(u'openlp.org 1.0'))
        self.ImportOpenlp1Item.setToolTip(
            import_menu.trUtf8(u'Export songs in openlp.org 1.0 format'))
        self.ImportOpenlp1Item.setStatusTip(
            import_menu.trUtf8(u'Export songs in openlp.org 1.0 format'))
        self.ImportOpenlp2Item.setText(import_menu.trUtf8(u'OpenLP 2.0'))
        self.ImportOpenlp2Item.setToolTip(
            import_menu.trUtf8(u'Export songs in OpenLP 2.0 format'))
        self.ImportOpenlp2Item.setStatusTip(
            import_menu.trUtf8(u'Export songs in OpenLP 2.0 format'))
        # Signals and slots
        QtCore.QObject.connect(self.ImportOpenlp1Item,
            QtCore.SIGNAL(u'triggered()'), self.onImportOpenlp1ItemClick)
        QtCore.QObject.connect(self.ImportOpenlp2Item,
            QtCore.SIGNAL(u'triggered()'), self.onImportOpenlp1ItemClick)
        QtCore.QObject.connect(self.ImportOpenSongItem,
            QtCore.SIGNAL(u'triggered()'), self.onImportOpenSongItemClick)
        self.ImportSongMenu.menuAction().setVisible(False)

    def add_export_menu_item(self, export_menu):
        """
        Give the Songs plugin the opportunity to add items to the
        **Export** menu.

        ``export_menu``
            The actual **Export** menu item, so that your actions can
            use it as their parent.
        """
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
        self.ExportSongMenu.setTitle(export_menu.trUtf8(u'&Song'))
        self.ExportOpenSongItem.setText(export_menu.trUtf8(u'OpenSong'))
        self.ExportOpenlp1Item.setText(export_menu.trUtf8(u'openlp.org 1.0'))
        self.ExportOpenlp2Item.setText(export_menu.trUtf8(u'OpenLP 2.0'))
        # Signals and slots
        QtCore.QObject.connect(self.ExportOpenlp1Item,
            QtCore.SIGNAL(u'triggered()'), self.onExportOpenlp1ItemClicked)
        QtCore.QObject.connect(self.ExportOpenSongItem,
            QtCore.SIGNAL(u'triggered()'), self.onExportOpenSongItemClicked)
        self.ExportSongMenu.menuAction().setVisible(False)

    def onImportOpenlp1ItemClick(self):
        self.openlp_import_form.show()

    def onImportOpenSongItemClick(self):
        self.opensong_import_form.show()

    def onExportOpenlp1ItemClicked(self):
        self.openlp_export_form.show()

    def onExportOpenSongItemClicked(self):
        self.opensong_export_form.show()

    def about(self):
        about_text = self.trUtf8(u'<b>Song Plugin</b> <br>This plugin allows '
            u'Songs to be managed and displayed.<br>')
        return about_text
