# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

from openlp.core.lib import Plugin, build_icon, Receiver, translate
from openlp.core.lib.db import Manager
from openlp.plugins.songs.lib import SongMediaItem, SongsTab
from openlp.plugins.songs.lib.db import init_schema, Song
from openlp.plugins.songs.lib.importer import SongFormat

#try:
#    from openlp.plugins.songs.lib import SofImport, OooImport
#    OOo_available = True
#except ImportError:
#    OOo_available = False
#from openlp.plugins.songs.lib import OpenSongImport

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
        self.icon_path = u':/plugins/plugin_songs.png'
        self.icon = build_icon(self.icon_path)

    def getSettingsTab(self):
        return SongsTab(self.name)

    def initialise(self):
        log.info(u'Songs Initialising')
        Plugin.initialise(self)
        self.mediaItem.displayResultsSong(
            self.manager.get_all_objects(Song, order_by_ref=Song.title))

    def getMediaManagerItem(self):
        """
        Create the MediaManagerItem object, which is displaed in the
        Media Manager.
        """
        return SongMediaItem(self, self.icon, self.name)

    def addImportMenuItem(self, import_menu):
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
#        if OOo_available:
#            # Songs of Fellowship import menu item - will be removed and the
#            # functionality will be contained within the import wizard
#            self.ImportSofItem = QtGui.QAction(import_menu)
#            self.ImportSofItem.setObjectName(u'ImportSofItem')
#            self.ImportSofItem.setText(
#                translate('SongsPlugin',
#                    'Songs of Fellowship (temp menu item)'))
#            self.ImportSofItem.setToolTip(
#                translate('SongsPlugin',
#                    'Import songs from the VOLS1_2.RTF, sof3words' \
#                    + '.rtf and sof4words.rtf supplied with the music books'))
#            self.ImportSofItem.setStatusTip(
#                translate('SongsPlugin',
#                    'Import songs from the VOLS1_2.RTF, sof3words' \
#                    + '.rtf and sof4words.rtf supplied with the music books'))
#            import_menu.addAction(self.ImportSofItem)
#            # OpenOffice.org import menu item - will be removed and the
#            # functionality will be contained within the import wizard
#            self.ImportOooItem = QtGui.QAction(import_menu)
#            self.ImportOooItem.setObjectName(u'ImportOooItem')
#            self.ImportOooItem.setText(
#                translate('SongsPlugin',
#                    'Generic Document/Presentation Import '
#                    '(temp menu item)'))
#            self.ImportOooItem.setToolTip(
#                translate('SongsPlugin',
#                    'Import songs from '
#                    'Word/Writer/Powerpoint/Impress'))
#            self.ImportOooItem.setStatusTip(
#                translate('SongsPlugin',
#                    'Import songs from '
#                    'Word/Writer/Powerpoint/Impress'))
#            import_menu.addAction(self.ImportOooItem)
#            # Signals and slots
#            QtCore.QObject.connect(self.ImportSofItem,
#                QtCore.SIGNAL(u'triggered()'), self.onImportSofItemClick)
#            QtCore.QObject.connect(self.ImportOooItem,
#                QtCore.SIGNAL(u'triggered()'), self.onImportOooItemClick)
#        # OpenSong import menu item - will be removed and the
#        # functionality will be contained within the import wizard
#        self.ImportOpenSongItem = QtGui.QAction(import_menu)
#        self.ImportOpenSongItem.setObjectName(u'ImportOpenSongItem')
#        self.ImportOpenSongItem.setText(
#            translate('SongsPlugin',
#                'OpenSong (temp menu item)'))
#        self.ImportOpenSongItem.setToolTip(
#            translate('SongsPlugin',
#                'Import songs from OpenSong files' +
#                '(either raw text or ZIPfiles)'))
#        self.ImportOpenSongItem.setStatusTip(
#            translate('SongsPlugin',
#                'Import songs from OpenSong files' +
#                '(either raw text or ZIPfiles)'))
#        import_menu.addAction(self.ImportOpenSongItem)
#        QtCore.QObject.connect(self.ImportOpenSongItem,
#                QtCore.SIGNAL(u'triggered()'), self.onImportOpenSongItemClick)
#        # OpenLP v2 import menu item - ditto above regarding refactoring into
#        # an import wizard
#        self.ImportOpenLPSongItem = QtGui.QAction(import_menu)
#        self.ImportOpenLPSongItem.setObjectName(u'ImportOpenLPSongItem')
#        self.ImportOpenLPSongItem.setText(translate('SongsPlugin',
#            'OpenLP v2 Songs (temporary)'))
#        self.ImportOpenLPSongItem.setToolTip(translate('SongsPlugin',
#            'Import an OpenLP v2 song database'))
#        self.ImportOpenLPSongItem.setStatusTip(translate('SongsPlugin',
#            'Import an OpenLP v2 song database'))
#        import_menu.addAction(self.ImportOpenLPSongItem)
#        QtCore.QObject.connect(self.ImportOpenLPSongItem,
#            QtCore.SIGNAL(u'triggered()'), self.onImportOpenLPSongItemClick)

    def addExportMenuItem(self, export_menu):
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
        if self.mediaItem:
            self.mediaItem.onImportClick()

#    def onImportSofItemClick(self):
#        filenames = QtGui.QFileDialog.getOpenFileNames(
#            None, translate('SongsPlugin',
#                'Open Songs of Fellowship file'),
#            u'', u'Songs of Fellowship file (*.rtf *.RTF)')
#        try:
#            for filename in filenames:
#                sofimport = SofImport(self.manager)
#                sofimport.import_sof(unicode(filename))
#        except:
#            log.exception('Could not import SoF file')
#            QtGui.QMessageBox.critical(None,
#                translate('SongsPlugin', 'Import Error'),
#                translate('SongsPlugin', 'Error importing Songs of '
#                    'Fellowship file.\nOpenOffice.org must be installed'
#                    ' and you must be using an unedited copy of the RTF'
#                    ' included with the Songs of Fellowship Music Editions'))
#        Receiver.send_message(u'songs_load_list')
#
#    def onImportOpenSongItemClick(self):
#        filenames = QtGui.QFileDialog.getOpenFileNames(
#            None, translate('SongsPlugin',
#                'Open OpenSong file'),
#            u'', u'All files (*.*)')
#        try:
#            for filename in filenames:
#                importer = OpenSongImport(self.manager)
#                importer.do_import(unicode(filename))
#        except:
#            log.exception('Could not import OpenSong file')
#            QtGui.QMessageBox.critical(None,
#                translate('SongsPlugin', 'Import Error'),
#                translate('SongsPlugin', 'Error importing OpenSong file'))
#        Receiver.send_message(u'songs_load_list')
#
#    def onImportOpenLPSongItemClick(self):
#        filenames = QtGui.QFileDialog.getOpenFileNames(None,
#            translate('SongsPlugin', 'Select OpenLP database(s) to import...'),
#            u'', u'OpenLP databases (*.sqlite);;All Files (*)')
#        try:
#            for filename in filenames:
#                db_url = u'sqlite:///%s' % filename
#                importer = OpenLPSongImport(self.manager, db_url)
#                importer.import_source_v2_db()
#            QtGui.QMessageBox.information(None, translate('SongsPlugin',
#                'Database(s) imported'), translate('SongsPlugin', 'Your '
#                'OpenLP v2 song databases have been successfully imported'))
#        except:
#            log.exception(u'Failed to import OpenLP v2 database(s)')
#            QtGui.QMessageBox.critical(None, translate('SongsPlugin',
#                'Import Error'), translate('SongsPlugin',
#                'Error importing OpenLP v2 database(s)'))
#        Receiver.send_message(u'songs_load_list')
#
#    def onImportOooItemClick(self):
#        filenames = QtGui.QFileDialog.getOpenFileNames(
#            None, translate('SongsPlugin', 'Open documents or presentations'),
#            '', u'All Files(*.*)')
#        oooimport = OooImport(self.manager)
#        oooimport.import_docs(filenames)
#        Receiver.send_message(u'songs_load_list')

    def about(self):
        about_text = translate('SongsPlugin', '<strong>Songs Plugin</strong>'
            '<br />The songs plugin provides the ability to display and '
            'manage songs.')
        return about_text

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
            self.custommanager.save_object(song)

    def importSongs(self, format, **kwargs):
        class_ = SongFormat.get_class(format)
        importer = class_(self.manager, **kwargs)
        importer.register(self.mediaItem.import_wizard)
        return importer
