# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

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

from PyQt4 import QtCore, QtGui

from openlp.core.resources import *
from openlp.core.lib import Plugin, MediaManagerItem
from forms import EditSongForm, OpenLPImportForm, OpenSongImportForm, \
                  OpenLPExportForm, OpenSongExportForm
from openlp.plugins.songs.lib import SongManager                  

class SongsPlugin(Plugin):
    def __init__(self):
        # Call the parent constructor
        Plugin.__init__(self, 'Songs', '1.9.0')
        self.weight = -10
        self.edit_song_form = EditSongForm()
        self.openlp_import_form = OpenLPImportForm()
        self.opensong_import_form = OpenSongImportForm()
        self.openlp_export_form = OpenLPExportForm()
        self.opensong_export_form = OpenSongExportForm()
        # Create the plugin icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(':/media/media_song.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.songmanager = SongManager(self.config)
        self.searchresults = {} # place to store the search results            

    def get_media_manager_item(self):
        # Create the MediaManagerItem object
        self.MediaManagerItem = MediaManagerItem(self.icon, 'Songs')
        # Add a toolbar
        self.MediaManagerItem.addToolbar()
        # Create buttons for the toolbar
        ## New Song Button ##
        self.MediaManagerItem.addToolbarButton('New Song', 'Add a new song',
            ':/songs/song_new.png', self.onSongNewClick, 'SongNewItem')
        ## Edit Song Button ##
        self.MediaManagerItem.addToolbarButton('Edit Song', 'Edit the selected song',
            ':/songs/song_edit.png', self.onSongEditClick, 'SongEditItem')
        ## Delete Song Button ##
        self.MediaManagerItem.addToolbarButton('Delete Song', 'Delete the selected song',
            ':/songs/song_delete.png', self.onSongDeleteClick, 'SongDeleteItem')
        ## Separator Line ##
        self.MediaManagerItem.addToolbarSeparator()
        ## Preview Song Button ##
        self.MediaManagerItem.addToolbarButton('Preview Song', 'Preview the selected song',
            ':/system/system_preview.png', self.onSongPreviewClick, 'SongPreviewItem')
        ## Live Song Button ##
        self.MediaManagerItem.addToolbarButton('Go Live', 'Send the selected song live',
            ':/system/system_live.png', self.onSongLiveClick, 'SongLiveItem')
        ## Add Song Button ##
        self.MediaManagerItem.addToolbarButton('Add Song To Service',
            'Add the selected song(s) to the service', ':/system/system_add.png',
            self.onSongAddClick, 'SongAddItem')
        ## Add the songlist widget ##
        # Create the tab widget
        self.SongWidget = QtGui.QWidget(self.MediaManagerItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SongWidget.sizePolicy().hasHeightForWidth())
        self.SongWidget.setSizePolicy(sizePolicy)
        self.SongWidget.setObjectName('SongWidget')
        self.SearchLayout = QtGui.QGridLayout(self.SongWidget)
        self.SearchLayout.setObjectName('SearchLayout')
        self.SearchTypeComboBox = QtGui.QComboBox(self.SongWidget)
        self.SearchTypeComboBox.setObjectName('SearchTypeComboBox')
        self.SearchLayout.addWidget(self.SearchTypeComboBox, 0, 1, 1, 2)
        self.SearchTypeLabel = QtGui.QLabel(self.SongWidget)
        self.SearchTypeLabel.setObjectName('SearchTypeLabel')
        self.SearchTypeLabel.setText('Search Type:')
        self.SearchLayout.addWidget(self.SearchTypeLabel, 0, 0, 1, 1)
        self.SearchTextLabel = QtGui.QLabel(self.SongWidget)
        self.SearchTextLabel.setObjectName('SearchTextLabel')
        self.SearchTextLabel.setText('Search Text:')
        self.SearchLayout.addWidget(self.SearchTextLabel, 2, 0, 1, 1)
        self.SearchTextEdit = QtGui.QLineEdit(self.SongWidget)
        self.SearchTextEdit.setObjectName('SearchTextEdit')
        self.SearchLayout.addWidget(self.SearchTextEdit, 2, 1, 1, 2)
        self.ClearTextButton = QtGui.QPushButton(self.SongWidget)
        self.ClearTextButton.setObjectName('ClearTextButton')
        self.ClearTextButton.setText('Clear')
        self.SearchLayout.addWidget(self.ClearTextButton, 3, 1, 1, 1)        
        self.SearchTextButton = QtGui.QPushButton(self.SongWidget)
        self.SearchTextButton.setObjectName('SearchTextButton')
        self.SearchTextButton.setText('Search')
        self.SearchLayout.addWidget(self.SearchTextButton, 3, 2, 1, 1)
        # Add the song widget to the page layout
        self.MediaManagerItem.PageLayout.addWidget(self.SongWidget)
        self.SongListView = QtGui.QListWidget()
        self.SongListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.SongListView.setObjectName("listView")
        self.MediaManagerItem.PageLayout.addWidget(self.SongListView)
        
        QtCore.QObject.connect(self.SearchTextButton, QtCore.SIGNAL("pressed()"), self.onSearchTextButton)
        QtCore.QObject.connect(self.ClearTextButton, QtCore.SIGNAL("pressed()"), self.onClearTextButton)
        QtCore.QObject.connect(self.SearchTextEdit, QtCore.SIGNAL("textChanged(const QString&)"), self.onSearchTextEdit)        
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

    def initialise(self):
        self.SearchTypeComboBox.addItem("Lyrics")
        self.SearchTypeComboBox.addItem("Titles")
        self.SearchTypeComboBox.addItem("Authors")

    def onClearTextButton(self):
        print self.SearchTextEdit.clear()

    def onSearchTextEdit(self):
        if len(self.SearchTextEdit.displayText()) > 3:  # only search if > 3 characters
            self.onSearchTextButton() 

    def onSearchTextButton(self):
        searchtext = str(self.SearchTextEdit.displayText() )
        if str(self.SearchTypeComboBox.currentText=="Titles"):
            self.searchresults = self.songmanager.get_song_from_title(searchtext)
        elif str(self.SearchTypeComboBox.currentText=="Lyrics"):
            self.searchresults = self.songmanager.get_song_from_lyrics(searchtext)            
        self._display_results()

    def onSongNewClick(self):
        pass

    def onSongEditClick(self):
        self.edit_song_form.show()

    def onSongDeleteClick(self):
        pass

    def onSongPreviewClick(self):
        pass

    def onSongLiveClick(self):
        pass

    def onSongAddClick(self):
        pass

    def onImportOpenlp1ItemClick(self):
        self.openlp_import_form.show()

    def onImportOpenSongItemClick(self):
        self.opensong_import_form.show()

    def onExportOpenlp1ItemClicked(self):
        self.openlp_export_form.show()

    def onExportOpenSongItemClicked(self):
        self.opensong_export_form.show()
        
    def _display_results(self):
        self.SongListView.clear() # clear the results
        print self.searchresults
        for id,  txt in self.searchresults:
            self.SongListView.addItem(str(txt))        
