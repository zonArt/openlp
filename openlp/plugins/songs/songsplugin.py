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

from openlp.core.lib import Plugin, build_icon, PluginStatus, Receiver, \
    translate
from openlp.plugins.songs.lib import SongManager, SongMediaItem, SongsTab, \
    SofImport, OooImport

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
        Plugin.__init__(self, u'Songs', u'1.9.1', plugin_helpers)
        self.weight = -10
        self.manager = SongManager()
        self.icon = build_icon(u':/media/media_song.png')
        self.status = PluginStatus.Active

    def get_settings_tab(self):
        return SongsTab(self.name)

    def initialise(self):
        log.info(u'Songs Initialising')
        #if self.songmanager is None:
        #    self.songmanager = SongManager()
        Plugin.initialise(self)
        self.insert_toolbox_item()
        #self.ImportSongMenu.menuAction().setVisible(True)
        #self.ExportSongMenu.menuAction().setVisible(True)
        self.media_item.displayResultsSong(self.manager.get_songs())

    def finalise(self):
        log.info(u'Plugin Finalise')
        Plugin.finalise(self)
        self.remove_toolbox_item()
        #self.ImportSongMenu.menuAction().setVisible(False)
        #self.ExportSongMenu.menuAction().setVisible(False)

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
        # Main song import menu item - will eventually be the only one
        self.SongImportItem = QtGui.QAction(import_menu)
        self.SongImportItem.setObjectName(u'SongImportItem')
        self.SongImportItem.setText(translate(
            u'SongsPlugin', u'&Song'))
        self.SongImportItem.setToolTip(
            translate(u'SongsPlugin', 
                u'Import songs using the import wizard.'))
        import_menu.addAction(self.SongImportItem)
        # Songs of Fellowship import menu item - will be removed and the
        # functionality will be contained within the import wizard
        self.ImportSofItem = QtGui.QAction(import_menu)
        self.ImportSofItem.setObjectName(u'ImportSofItem')
        self.ImportSofItem.setText(
            translate(u'SongsPlugin', 
                u'Songs of Fellowship (temp menu item)'))
        self.ImportSofItem.setToolTip(
            translate(u'SongsPlugin', 
                u'Import songs from the VOLS1_2.RTF, sof3words' \
                + u'.rtf and sof4words.rtf supplied with the music books'))
        self.ImportSofItem.setStatusTip(
            translate(u'SongsPlugin', 
                u'Import songs from the VOLS1_2.RTF, sof3words' \
                + u'.rtf and sof4words.rtf supplied with the music books'))
        import_menu.addAction(self.ImportSofItem)
        # OpenOffice.org import menu item - will be removed and the
        # functionality will be contained within the import wizard
        self.ImportOooItem = QtGui.QAction(import_menu)
        self.ImportOooItem.setObjectName(u'ImportOooItem')
        self.ImportOooItem.setText(
            translate(u'SongsPlugin', 
                u'Generic Document/Presentation Import '
                u'(temp menu item)'))
        self.ImportOooItem.setToolTip(
            translate(u'SongsPlugin', 
                u'Import songs from '
                u'Word/Writer/Powerpoint/Impress'))
        self.ImportOooItem.setStatusTip(
            translate(u'SongsPlugin', 
                u'Import songs from '
                u'Word/Writer/Powerpoint/Impress'))
        import_menu.addAction(self.ImportOooItem)
        # Signals and slots
        QtCore.QObject.connect(self.SongImportItem,
            QtCore.SIGNAL(u'triggered()'), self.onSongImportItemClicked)
        QtCore.QObject.connect(self.ImportSofItem,
            QtCore.SIGNAL(u'triggered()'), self.onImportSofItemClick)
        QtCore.QObject.connect(self.ImportOooItem,
            QtCore.SIGNAL(u'triggered()'), self.onImportOooItemClick)

    def add_export_menu_item(self, export_menu):
        """
        Give the Songs plugin the opportunity to add items to the
        **Export** menu.

        ``export_menu``
            The actual **Export** menu item, so that your actions can
            use it as their parent.
        """
        # No menu items for now.
        pass

    def onSongImportItemClicked(self):
        if self.media_item:
            self.media_item.onImportClick()

    def onImportSofItemClick(self):
        filenames = QtGui.QFileDialog.getOpenFileNames(
            None, translate(u'SongsPlugin',
                u'Open Songs of Fellowship file'),
            u'', u'Songs of Fellowship file (*.rtf *.RTF)')
        try:
            for filename in filenames:
                sofimport = SofImport(self.manager)
                sofimport.import_sof(unicode(filename))
        except:
            log.exception('Could not import SoF file')
            QtGui.QMessageBox.critical(None,
                translate(u'SongsPlugin', 
                    u'Import Error'),
                translate(u'SongsPlugin', 
                    u'Error importing Songs of ' 
                    u'Fellowship file.\nOpenOffice.org must be installed' 
                    u' and you must be using an unedited copy of the RTF'
                    u' included with the Songs of Fellowship Music Editions'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok),
                QtGui.QMessageBox.Ok)
        Receiver.send_message(u'songs_load_list')

    def onImportOooItemClick(self):
        filenames = QtGui.QFileDialog.getOpenFileNames(
            None, translate(u'SongsPlugin',
            u'Open documents or presentations'),
            u'', u'All Files(*.*)')
        oooimport = OooImport(self.manager)        
        oooimport.import_docs(filenames)
        Receiver.send_message(u'songs_load_list')

    def about(self):
        about_text = translate(u'SongsPlugin',
            u'<strong>Song Plugin</strong><br />'
            u'This plugin allows songs to be managed and displayed.')
        return about_text

    def can_delete_theme(self, theme):
        if len(self.manager.get_songs_for_theme(theme)) == 0:
            return True
        return False

