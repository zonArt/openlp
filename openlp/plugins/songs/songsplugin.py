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
from openlp.core.lib.db import Manager
from openlp.plugins.songs.lib import SongMediaItem, SongsTab
from openlp.plugins.songs.lib.db import init_schema, Song

try:
    from openlp.plugins.songs.lib import SofImport, OooImport
    OOo_available = True
except ImportError:
    OOo_available = False

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
        Plugin.__init__(self, u'Songs', u'1.9.2', plugin_helpers)
        self.weight = -10
        self.manager = Manager(u'songs', init_schema)
        self.icon = build_icon(u':/plugins/plugin_songs.png')
        self.status = PluginStatus.Active

    def get_settings_tab(self):
        return SongsTab(self.name)

    def initialise(self):
        log.info(u'Songs Initialising')
        Plugin.initialise(self)
        self.mediaItem.displayResultsSong(
            self.manager.get_all_objects(Song, Song.title))

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
            'SongsPlugin', '&Song'))
        self.SongImportItem.setToolTip(translate('SongsPlugin',
            'Import songs using the import wizard.'))
        import_menu.addAction(self.SongImportItem)
        # Signals and slots
        QtCore.QObject.connect(self.SongImportItem,
            QtCore.SIGNAL(u'triggered()'), self.onSongImportItemClicked)
        if OOo_available:
            # Songs of Fellowship import menu item - will be removed and the
            # functionality will be contained within the import wizard
            self.ImportSofItem = QtGui.QAction(import_menu)
            self.ImportSofItem.setObjectName(u'ImportSofItem')
            self.ImportSofItem.setText(
                translate('SongsPlugin',
                    'Songs of Fellowship (temp menu item)'))
            self.ImportSofItem.setToolTip(
                translate('SongsPlugin',
                    'Import songs from the VOLS1_2.RTF, sof3words' \
                    + '.rtf and sof4words.rtf supplied with the music books'))
            self.ImportSofItem.setStatusTip(
                translate('SongsPlugin',
                    'Import songs from the VOLS1_2.RTF, sof3words' \
                    + '.rtf and sof4words.rtf supplied with the music books'))
            import_menu.addAction(self.ImportSofItem)
            # OpenOffice.org import menu item - will be removed and the
            # functionality will be contained within the import wizard
            self.ImportOooItem = QtGui.QAction(import_menu)
            self.ImportOooItem.setObjectName(u'ImportOooItem')
            self.ImportOooItem.setText(
                translate('SongsPlugin',
                    'Generic Document/Presentation Import '
                    '(temp menu item)'))
            self.ImportOooItem.setToolTip(
                translate('SongsPlugin',
                    'Import songs from '
                    'Word/Writer/Powerpoint/Impress'))
            self.ImportOooItem.setStatusTip(
                translate('SongsPlugin',
                    'Import songs from '
                    'Word/Writer/Powerpoint/Impress'))
            import_menu.addAction(self.ImportOooItem)
            # Signals and slots
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
            None, translate('SongsPlugin',
                'Open Songs of Fellowship file'),
            u'', u'Songs of Fellowship file (*.rtf *.RTF)')
        try:
            for filename in filenames:
                sofimport = SofImport(self.manager)
                sofimport.import_sof(unicode(filename))
        except:
            log.exception('Could not import SoF file')
            QtGui.QMessageBox.critical(None,
                translate('SongsPlugin',
                    'Import Error'),
                translate('SongsPlugin',
                    'Error importing Songs of '
                    'Fellowship file.\nOpenOffice.org must be installed'
                    ' and you must be using an unedited copy of the RTF'
                    ' included with the Songs of Fellowship Music Editions'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok),
                QtGui.QMessageBox.Ok)
        Receiver.send_message(u'songs_load_list')

    def onImportOooItemClick(self):
        filenames = QtGui.QFileDialog.getOpenFileNames(
            None, translate('SongsPlugin',
            'Open documents or presentations'),
            '', u'All Files(*.*)')
        oooimport = OooImport(self.manager)
        oooimport.import_docs(filenames)
        Receiver.send_message(u'songs_load_list')

    def about(self):
        about_text = translate('SongsPlugin',
            '<strong>Song Plugin</strong><br />'
            'This plugin allows songs to be managed and displayed.')
        return about_text

    def can_delete_theme(self, theme):
        if not self.manager.get_all_objects_filtered(Song,
            Song.theme_name == theme):
            return True
        return False
