# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

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

from bibleManager import BibleManager
from forms.bibleimportform import BibleImportForm

class BiblePlugin(Plugin):
    def __init__(self):
        # Call the parent constructor
        Plugin.__init__(self, 'Bible', '1.9.0')
        self.Weight = -9
        #Register the bible Manager
        self.biblemanager = BibleManager(self.config.get_data_path())
        self.textsearch = True

    def getMediaManagerItem(self):
        # Create the plugin icon
        self.Icon = QtGui.QIcon()
        self.Icon.addPixmap(QtGui.QPixmap(':/media/media_verse.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # Create the MediaManagerItem object
        self.MediaManagerItem = MediaManagerItem(self.Icon, 'Bible Verses')
        # Add a toolbar
        self.MediaManagerItem.addToolbar()
        # Create buttons for the toolbar
        ## New Bible Button ##
        self.MediaManagerItem.addToolbarButton('New Bible', 'Register a new Bible',
            ':/bibles/bible_new.png', self.onBibleNewClick, 'BibleNewItem')
        ## Separator Line ##
        self.MediaManagerItem.addToolbarSeparator()
        ## Preview Bible Button ##
        self.MediaManagerItem.addToolbarButton('Preview Bible', 'Preview the selected Bible Verse',
            ':/system/system_preview.png', self.onBiblePreviewClick, 'BiblePreviewItem')
        ## Live Bible Button ##
        self.MediaManagerItem.addToolbarButton('Go Live', 'Send the selected Bible Verse(s) live',
            ':/system/system_live.png', self.onBibleLiveClick, 'BibleLiveItem')
        ## Add Bible Button ##
        self.MediaManagerItem.addToolbarButton('Add Bible Verse(s) To Service',
            'Add the selected Bible(s) to the service', ':/system/system_add.png',
            self.onBibleAddClick, 'BibleAddItem')
        ## Separator Line ##
        #self.MediaManagerItem.addToolbarSeparator()
        ## Add Bible Button ##
        #self.MediaManagerItem.addToolbarButton('Change Search Style',
        #    'Swap between the Bible search styles', ':/system/system_add.png',
        #    self.onBibleSearchChangeClick, 'BibleSearchChange')
        # Add the Biblelist Tables

        # Create the tab widget
        self.SearchTabWidget = QtGui.QTabWidget(self.MediaManagerItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchTabWidget.sizePolicy().hasHeightForWidth())
        self.SearchTabWidget.setSizePolicy(sizePolicy)
        self.SearchTabWidget.setObjectName('SearchTabWidget')
        # Add the Quick Search tab
        self.QuickTab = QtGui.QWidget()
        self.QuickTab.setObjectName('QuickTab')
        self.QuickLayout = QtGui.QGridLayout(self.QuickTab)
        self.QuickLayout.setObjectName('QuickLayout')
        self.QuickVersionComboBox = QtGui.QComboBox(self.QuickTab)
        self.QuickVersionComboBox.setObjectName('VersionComboBox')
        self.QuickLayout.addWidget(self.QuickVersionComboBox, 0, 1, 1, 2)
        self.QuickVersionLabel = QtGui.QLabel(self.QuickTab)
        self.QuickVersionLabel.setObjectName('QuickVersionLabel')
        self.QuickVersionLabel.setText('Version:')
        self.QuickLayout.addWidget(self.QuickVersionLabel, 0, 0, 1, 1)
        self.QuickSearchLabel = QtGui.QLabel(self.QuickTab)
        self.QuickSearchLabel.setObjectName('QuickSearchLabel')
        self.QuickSearchLabel.setText('Find:')
        self.QuickLayout.addWidget(self.QuickSearchLabel, 2, 0, 1, 1)
        self.QuickSearchEdit = QtGui.QLineEdit(self.QuickTab)
        self.QuickSearchEdit.setObjectName('QuickSearchEdit')
        self.QuickLayout.addWidget(self.QuickSearchEdit, 2, 1, 1, 2)
        self.QuickSearchButton = QtGui.QPushButton(self.QuickTab)
        self.QuickSearchButton.setObjectName('QuickSearchButton')
        self.QuickSearchButton.setText('Search')
        self.QuickLayout.addWidget(self.QuickSearchButton, 3, 2, 1, 1)
        QuickSpacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.QuickLayout.addItem(QuickSpacerItem, 4, 2, 1, 1)
        self.SearchTabWidget.addTab(self.QuickTab, 'Quick Search')
        # Add the Advanced Search tab
        self.AdvancedTab = QtGui.QWidget()
        self.AdvancedTab.setObjectName('AdvancedTab')
        self.AdvancedLayout = QtGui.QGridLayout(self.AdvancedTab)
        self.AdvancedLayout.setObjectName('AdvancedLayout')
        self.AdvancedVersionLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedVersionLabel.setObjectName('AdvancedVersionLabel')
        self.AdvancedVersionLabel.setText('Version:')
        self.AdvancedLayout.addWidget(self.AdvancedVersionLabel, 0, 0, 1, 1)
        self.AdvancedVersionComboBox = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedVersionComboBox.setObjectName('AdvancedVersionComboBox')
        self.AdvancedLayout.addWidget(self.AdvancedVersionComboBox, 0, 2, 1, 2)
        self.AdvancedBookLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedBookLabel.setObjectName('AdvancedBookLabel')
        self.AdvancedBookLabel.setText('Book:')
        self.AdvancedLayout.addWidget(self.AdvancedBookLabel, 1, 0, 1, 1)
        self.AdvancedBookComboBox = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedBookComboBox.setObjectName('AdvancedBookComboBox')
        self.AdvancedLayout.addWidget(self.AdvancedBookComboBox, 1, 2, 1, 2)
        self.AdvancedChapterLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedChapterLabel.setObjectName('AdvancedChapterLabel')
        self.AdvancedChapterLabel.setText('Chapter:')
        self.AdvancedLayout.addWidget(self.AdvancedChapterLabel, 2, 2, 1, 1)
        self.AdvancedVerseLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedVerseLabel.setObjectName('AdvancedVerseLabel')
        self.AdvancedVerseLabel.setText('Verse:')
        self.AdvancedLayout.addWidget(self.AdvancedVerseLabel, 2, 3, 1, 1)
        self.AdvancedFromLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedFromLabel.setObjectName('AdvancedFromLabel')
        self.AdvancedFromLabel.setText('From:')
        self.AdvancedLayout.addWidget(self.AdvancedFromLabel, 3, 0, 1, 1)
        self.AdvancedToLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedToLabel.setObjectName('AdvancedToLabel')
        self.AdvancedToLabel.setText('To:')
        self.AdvancedLayout.addWidget(self.AdvancedToLabel, 4, 0, 1, 1)
        self.AdvancedFromChapter = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedFromChapter.setObjectName('AdvancedFromChapter')
        self.AdvancedLayout.addWidget(self.AdvancedFromChapter, 3, 3, 1, 1)
        self.AdvancedFromVerse = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedFromVerse.setObjectName('AdvancedFromVerse')
        self.AdvancedLayout.addWidget(self.AdvancedFromVerse, 3, 2, 1, 1)
        self.AdvancedToChapter = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedToChapter.setObjectName('AdvancedToChapter')
        self.AdvancedLayout.addWidget(self.AdvancedToChapter, 4, 2, 1, 1)
        self.AdvancedToVerse = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedToVerse.setObjectName('AdvancedToVerse')
        self.AdvancedLayout.addWidget(self.AdvancedToVerse, 4, 3, 1, 1)
        self.AdvancedSearchButton = QtGui.QPushButton(self.AdvancedTab)
        self.AdvancedSearchButton.setObjectName('AdvancedSearchButton')
        self.AdvancedSearchButton.setText('Search')
        self.AdvancedLayout.addWidget(self.AdvancedSearchButton, 5, 3, 1, 1)
        self.SearchTabWidget.addTab(self.AdvancedTab, 'Advanced Search')

        # Add the search tab widget to the page layout
        self.MediaManagerItem.PageLayout.addWidget(self.SearchTabWidget)

        """self.groupBox = QtGui.QGroupBox(self.MediaManagerItem)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 271, 391))
        self.groupBox.setMinimumSize(QtCore.QSize(0, 271))
        self.groupBox.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,  QtGui.QSizePolicy.Minimum))
        self.groupBox.setObjectName("groupBox")
        self.MediaManagerItem.PageLayout.addWidget(self.groupBox)

        self.biblelabel = QtGui.QLabel(self.groupBox)
        self.biblelabel.setGeometry(QtCore.QRect(10, 20, 80, 25))
        self.biblelabel.setObjectName("biblelabel")
        self.biblelabel.setText("Translation:")
        self.biblecomboBox = QtGui.QComboBox(self.groupBox)
        self.biblecomboBox.setGeometry(QtCore.QRect(120, 20, 150, 25))
        self.biblecomboBox.setObjectName("biblecomboBox")
        self.biblecomboBox.addItem("NIV")
        self.biblecomboBox.addItem("KJC")

        self.searchcomboBox = QtGui.QComboBox(self.groupBox)
        self.searchcomboBox.setGeometry(QtCore.QRect(10, 50, 105, 25))
        self.searchcomboBox.setObjectName("searchcomboBox")
        self.searchcomboBox.addItem("Verse Search")
        self.searchcomboBox.addItem("Text Search")
        self.searchEdit = QtGui.QLineEdit(self.groupBox)
        self.searchEdit.setGeometry(QtCore.QRect(120, 50, 150, 25))
        self.searchEdit.setObjectName("searchEdit")

        self.booklabel = QtGui.QLabel(self.groupBox)
        self.booklabel.setGeometry(QtCore.QRect(10, 50, 80, 25))
        self.booklabel.setObjectName("booklabel")
        self.booklabel.setText("Book:")
        self.bookcomboBox = QtGui.QComboBox(self.groupBox)
        self.bookcomboBox.setGeometry(QtCore.QRect(120, 50, 105, 25))
        self.bookcomboBox.setObjectName("bookcomboBox")
        self.bookcomboBox.addItem("Genesis")
        self.bookcomboBox.addItem("Matthew")
        self.bookcomboBox.addItem("Revelation")

        self.chapterlabel = QtGui.QLabel(self.groupBox)
        self.chapterlabel.setGeometry(QtCore.QRect(10, 110, 50, 25))
        self.chapterlabel.setObjectName("chapterlabel")
        self.chapterlabel.setText("Chapter:")
        self.verselabel = QtGui.QLabel(self.groupBox)
        self.verselabel.setGeometry(QtCore.QRect(10, 140, 50, 25))
        self.verselabel.setObjectName("verselabel")
        self.verselabel.setText("Verse:")
        self.fromlabel = QtGui.QLabel(self.groupBox)
        self.fromlabel.setGeometry(QtCore.QRect(120, 80, 50, 25))
        self.fromlabel.setObjectName("fromlabel")
        self.fromlabel.setText("From:")
        self.tolabel = QtGui.QLabel(self.groupBox)
        self.tolabel.setGeometry(QtCore.QRect(210, 80, 50, 25))
        self.tolabel.setObjectName("tolabel")
        self.tolabel.setText("To:")
        self.fromcomboBox_c = QtGui.QComboBox(self.groupBox)
        self.fromcomboBox_c.setGeometry(QtCore.QRect(120, 110, 45, 25))
        self.fromcomboBox_c.setObjectName("fromcomboBox_c")
        self.fromcomboBox_v = QtGui.QComboBox(self.groupBox)
        self.fromcomboBox_v.setGeometry(QtCore.QRect(200, 110, 45, 25))
        self.fromcomboBox_v.setObjectName("fromcomboBox_v")
        self.tocomboBox_c = QtGui.QComboBox(self.groupBox)
        self.tocomboBox_c.setGeometry(QtCore.QRect(120, 140, 45, 22))
        self.tocomboBox_c.setObjectName("tocomboBox_c")
        self.tocomboBox_v = QtGui.QComboBox(self.groupBox)
        self.tocomboBox_v.setGeometry(QtCore.QRect(200, 140, 45, 22))
        self.tocomboBox_v.setObjectName("tocomboBox_v")
        for i in range(1, 20):
            self.fromcomboBox_c.addItem(str(i))
            self.tocomboBox_c.addItem(str(i))
        for i in range(1, 10):
            self.fromcomboBox_v.addItem(str(i))
            self.tocomboBox_v.addItem(str(i))

        self.searchButton = QtGui.QPushButton(self.groupBox)
        self.searchButton.setGeometry(QtCore.QRect(170, 170, 75, 27))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setText("Search")
        QtCore.QObject.connect(self.searchButton, QtCore.SIGNAL("pressed()"), self.onBibleSearchClick)"""

        self.listView = QtGui.QListView()
        self.listView.setGeometry(QtCore.QRect(10, 200, 256, 391))
        self.listView.setObjectName("listView")
        self.MediaManagerItem.PageLayout.addWidget(self.listView)

        #self.textsearchmode()
        return self.MediaManagerItem

    def onBibleNewClick(self):
        self.bibleimportform = BibleImportForm(self.biblemanager)
        self.bibleimportform.show()
        pass

    def onBiblePreviewClick(self):
        pass

    def onBibleLiveClick(self):
        pass

    def onBibleAddClick(self):
        pass

    def onBibleSearchClick(self):
        #if self.textsearch == True:
        #    print "Text / Verse Search"
        #else:
        #    print "Combo Search"
        pass


    def onBibleSearchChangeClick(self):
        #self.textsearchmode()
        pass

    def  textsearchmode(self):
        """if self.textsearch == True:
            self.textsearch = False
            self.searchcomboBox.hide()
            self.searchEdit.hide()
            self.booklabel.show()
            self.bookcomboBox.show()
            self.fromcomboBox_c.show()
            self.fromcomboBox_v.show()
            self.tocomboBox_c.show()
            self.tocomboBox_v.show()
            self.chapterlabel.show()
            self.verselabel.show()
            self.fromlabel.show()
            self.tolabel.show()
        else:
            self.textsearch = True
            self.searchcomboBox.show()
            self.searchEdit.show()
            self.booklabel.hide()
            self.bookcomboBox.hide()
            self.fromcomboBox_c.hide()
            self.fromcomboBox_v.hide()
            self.tocomboBox_c.hide()
            self.tocomboBox_v.hide()
            self.chapterlabel.hide()
            self.verselabel.hide()
            self.fromlabel.hide()
            self.tolabel.hide()"""
        pass

