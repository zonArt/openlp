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

import logging

from PyQt4 import QtCore, QtGui

from openlp.core.resources import *
from openlp.core.lib import Plugin,PluginUtils,  MediaManagerItem

from openlp.plugins.bibles.lib import BibleManager
from openlp.plugins.bibles.forms import BibleImportForm

from openlp.plugins.bibles.lib.tables import *
from openlp.plugins.bibles.lib.classes import *

class BiblePlugin(Plugin, PluginUtils):
    global log
    log=logging.getLogger("BiblePlugin")
    log.info("Bible Plugin loaded")
    def __init__(self):
        # Call the parent constructor
        Plugin.__init__(self, 'Bible', '1.9.0')
        self.weight = -9
        # Create the plugin icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(':/media/media_verse.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #Register the bible Manager
        self.biblemanager = BibleManager(self.config)
        self.searchresults = {} # place to store the search results

    def get_media_manager_item(self):
        # Create the MediaManagerItem object
        self.MediaManagerItem = MediaManagerItem(self.icon, 'Bible Verses')
        # Add a toolbar
        self.MediaManagerItem.addToolbar()
        # Create buttons for the toolbar
        ## New Bible Button ##
        self.MediaManagerItem.addToolbarButton('New Bible', 'Register a new Bible',
            ':/themes/theme_import.png', self.onBibleNewClick, 'BibleNewItem')
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

        self.QuickSearchComboBox = QtGui.QComboBox(self.QuickTab)
        self.QuickSearchComboBox.setObjectName('SearchComboBox')
        self.QuickLayout.addWidget(self.QuickSearchComboBox, 1, 1, 1, 2)
        self.QuickSearchLabel = QtGui.QLabel(self.QuickTab)
        self.QuickSearchLabel .setObjectName('QuickSearchLabel')
        self.QuickSearchLabel .setText('Search Type:')
        self.QuickLayout.addWidget(self.QuickSearchLabel, 1, 0, 1, 1)

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
        self.AdvancedLayout.addWidget(self.AdvancedFromChapter, 3, 2, 1, 1)
        self.AdvancedFromVerse = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedFromVerse.setObjectName('AdvancedFromVerse')
        self.AdvancedLayout.addWidget(self.AdvancedFromVerse, 3, 3, 1, 1)

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

        self.BibleListView = QtGui.QTableWidget()
        self.BibleListView.setColumnCount(2)
        self.BibleListView.setColumnHidden(0, True)
        self.BibleListView.setColumnWidth(1, 275)
        self.BibleListView.setShowGrid(False)
        self.BibleListView.setSortingEnabled(False)        
        self.BibleListView.setAlternatingRowColors(True)
        self.BibleListView.setHorizontalHeaderLabels(QtCore.QStringList(["","Bible Verses"]))        

        self.BibleListView.setGeometry(QtCore.QRect(10, 200, 256, 391))
        self.BibleListView.setObjectName("listView")
        self.BibleListView.setAlternatingRowColors(True)        
        self.MediaManagerItem.PageLayout.addWidget(self.BibleListView)

        #QtCore.QObject.connect(self.QuickTab, QtCore.SIGNAL("triggered()"), self.onQuickTabClick)
        QtCore.QObject.connect( self.SearchTabWidget, QtCore.SIGNAL("currentChanged ( QWidget * )" ), self.onQuickTabClick)
        QtCore.QObject.connect(self.AdvancedVersionComboBox, QtCore.SIGNAL("activated(int)"), self.onAdvancedVersionComboBox)
        QtCore.QObject.connect(self.AdvancedBookComboBox, QtCore.SIGNAL("activated(int)"), self.onAdvancedBookComboBox)
        QtCore.QObject.connect(self.AdvancedFromChapter, QtCore.SIGNAL("activated(int)"), self.onAdvancedFromChapter)
        QtCore.QObject.connect(self.AdvancedFromVerse, QtCore.SIGNAL("activated(int)"), self.onAdvancedFromVerse)
        QtCore.QObject.connect(self.AdvancedToChapter, QtCore.SIGNAL("activated(int)"), self.onAdvancedToChapter)

        QtCore.QObject.connect(self.AdvancedSearchButton, QtCore.SIGNAL("pressed()"), self.onAdvancedSearchButton)
        QtCore.QObject.connect(self.QuickSearchButton, QtCore.SIGNAL("pressed()"), self.onQuickSearchButton)
        
        #define and add the context menu
        self.BibleListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.BibleListView.addAction(self.add_to_context_menu(self.BibleListView, ':/system/system_preview.png', "&Preview Verse", self.onBiblePreviewClick))      
        self.BibleListView.addAction(self.add_to_context_menu(self.BibleListView, ':/system/system_live.png', "&Show Live", self.onBibleLiveClick))        
        self.BibleListView.addAction(self.add_to_context_menu(self.BibleListView, ':/system/system_add.png', "&Add to Service", self.onBibleAddClick))
        return self.MediaManagerItem

    def add_import_menu_item(self, import_menu):
        self.ImportBibleItem = QtGui.QAction(import_menu)
        self.ImportBibleItem.setObjectName("ImportBibleItem")
        import_menu.addAction(self.ImportBibleItem)
        self.ImportBibleItem.setText(QtGui.QApplication.translate("main_window", "&Bible", None, QtGui.QApplication.UnicodeUTF8))
        # Signals and slots
        QtCore.QObject.connect(self.ImportBibleItem, QtCore.SIGNAL("triggered()"),  self.onBibleNewClick)
        
    def add_export_menu_item(self, export_menu):
        self.ExportBibleItem = QtGui.QAction(export_menu)
        self.ExportBibleItem.setObjectName("ExportBibleItem")
        export_menu.addAction(self.ExportBibleItem)
        self.ExportBibleItem.setText(QtGui.QApplication.translate("main_window", "&Bible", None, QtGui.QApplication.UnicodeUTF8))

    def initialise(self):
        self._initialise_form()

    def onAdvancedVersionComboBox(self):
        self._initialise_bible_advanced(str(self.AdvancedVersionComboBox.currentText())) # restet the bible info

    def onAdvancedBookComboBox(self):
        print self.AdvancedVersionComboBox.currentText()
        self._initialise_bible_advanced(str(self.AdvancedVersionComboBox.currentText())) # restet the bible info

    def onQuickTabClick(self):
        print "onQuickTabClick"
        print self.SearchTabWidget.currentIndex()
        print self.SearchTabWidget.tabText(self.SearchTabWidget.currentIndex())
        pass

    def onBibleNewClick(self):
        self.bibleimportform = BibleImportForm(self.config, self.biblemanager)
        self.bibleimportform.setModal(True)
        self.bibleimportform.show()
        pass

    def onBiblePreviewClick(self):
        pass

    def onBibleLiveClick(self):
        pass

    def onBibleAddClick(self):
        pass

    def _initialise_form(self):
        bibles = self.biblemanager.get_bibles("full")
        self.QuickSearchComboBox.addItem("Text Search")
        self.QuickSearchComboBox.addItem("Verse Search")
        for b in bibles:  # load bibles into the combo boxes
            self.QuickVersionComboBox.addItem(b)
                
        bibles = self.biblemanager.get_bibles("partial") # Without HTTP
        first = True
        for b in bibles:  # load bibles into the combo boxes
            self.AdvancedVersionComboBox.addItem(b) 
            if first:
                first = False
                self._initialise_bible_advanced(b) # use the first bible as the trigger                

    def _initialise_bible_advanced(self, bible):
        log.debug("_initialise_bible_advanced %s ", bible)
        currentBook = str(self.AdvancedBookComboBox.currentText())
        cf = self.biblemanager.get_book_chapter_count(bible, currentBook)[0]
        log.debug("Book change bible %s book %s ChapterCount %s", bible, currentBook, cf)
        if cf == None: # Only change the search details if the book is missing from the new bible
            books = self.biblemanager.get_bible_books(str(self.AdvancedVersionComboBox.currentText()))
            self.AdvancedBookComboBox.clear()
            first = True
            for book in books:
                self.AdvancedBookComboBox.addItem(book.name)
                if first:
                    first = False
                    self._initialise_chapter_verse(bible, book.name)

    def _initialise_chapter_verse(self, bible, book):
        log.debug("_initialise_chapter_verse %s , %s", bible, book)
        self.chaptersfrom = self.biblemanager.get_book_chapter_count(bible, book)[0]
        self.verses = self.biblemanager.get_book_verse_count(bible, book, 1)[0]
        self._adjust_combobox(1, self.chaptersfrom, self.AdvancedFromChapter)
        self._adjust_combobox(1, self.chaptersfrom, self.AdvancedToChapter)
        self._adjust_combobox(1, self.verses, self.AdvancedFromVerse)
        self._adjust_combobox(1, self.verses, self.AdvancedToVerse)

    def onAdvancedFromChapter(self):
        bible = str(self.AdvancedVersionComboBox.currentText())
        book = str(self.AdvancedBookComboBox.currentText())
        cf = self.AdvancedFromChapter.currentText()
        self._adjust_combobox(cf, self.chaptersfrom, self.AdvancedToChapter)
        vse = self.biblemanager.get_book_verse_count(bible, book, int(cf))[0] # get the verse count for new chapter
        self._adjust_combobox(1, vse, self.AdvancedFromVerse)
        self._adjust_combobox(1, vse, self.AdvancedToVerse)

    def _adjust_combobox(self, frm, to , combo):
        log.debug("_adjust_combobox %s , %s , %s", combo, frm,  to)
        combo.clear()
        for i in range(int(frm), int(to) + 1):
            combo.addItem(str(i))

    def onAdvancedFromVerse(self):
        frm = self.AdvancedFromVerse.currentText()
        self._adjust_combobox(frm, self.verses, self.AdvancedToVerse)

    def onAdvancedToChapter(self):
        t1 =  self.AdvancedFromChapter.currentText()
        t2 =  self.AdvancedToChapter.currentText()
        if t1 != t2:
            bible = str(self.AdvancedVersionComboBox.currentText())
            book = str(self.AdvancedBookComboBox.currentText())
            vse = self.biblemanager.get_book_verse_count(bible, book, int(t2))[0] # get the verse count for new chapter
            self._adjust_combobox(1, vse, self.AdvancedToVerse)

    def onAdvancedSearchButton(self):
        bible = str(self.AdvancedVersionComboBox.currentText())
        book = str(self.AdvancedBookComboBox.currentText())
        chapfrom =  int(self.AdvancedFromChapter.currentText())
        chapto =  int(self.AdvancedToChapter.currentText())
        versefrom =  int(self.AdvancedFromVerse.currentText())
        verseto =  int(self.AdvancedToVerse.currentText())
        self.searchresults = self.biblemanager.get_verse_text(bible, book, chapfrom, chapto, versefrom, verseto)
        self._display_results(bible)

    def onQuickSearchButton(self):
        self.log.debug("onQuickSearchButton")
        bible = str(self.QuickVersionComboBox.currentText())
        text = str(self.QuickSearchEdit.displayText())

        if self.QuickSearchComboBox.currentText() == "Text Search":
            self._search_text(bible, text)
        else:
            self.translate(bible, text)

    def _search_text(self, bible, text):
        self.log.debug("_search Text %s,%s", bible, text)
        self.searchresults = self.biblemanager.get_verse_from_text(bible,text)
        self._display_results(bible)

#    def _verse_search(self):
#        self._display_results()

    def _display_results(self, bible):
        self.BibleListView.clear() # clear the results
        self.BibleListView.setRowCount(0)        
        self.BibleListView.setHorizontalHeaderLabels(QtCore.QStringList(["","Bible Verses"]))          
        for book, chap, vse , txt in self.searchresults:
            c = self.BibleListView.rowCount()
            self.BibleListView.setRowCount(c+1)
            twi = QtGui.QTableWidgetItem(str(bible))
            self.BibleListView.setItem(c , 0, twi)
            twi = QtGui.QTableWidgetItem(str(book + " " +str(chap) + ":"+ str(vse)))
            self.BibleListView.setItem(c , 1, twi)
            self.BibleListView.setRowHeight(c, 20)             


    def _initialise_bible_quick(self, bible): # not sure if needed yet!
        a=1
        
    def translate(self, bible,  search):
        print "------"
        print search
        book, rest = self._split_book_from_verses(search)
        book = book.rstrip()
        chapters, verses = self._split_chapters_and_verses(rest)
        print verses
        chapters = self._split_chapters(chapters)
        #v = self._split_verses(verses)
        print "book = " + book
        print "chapters =" + str(chapters)
        #print "from =" + str(v)
        print "to ="
        self.searchresults = self.biblemanager.get_verse_text(bible, book,int(chapters[0]), int(chapters[1]), 1, 99)
        self._display_results()    
            
    def _split_chapters(self, text):
        txt = text.split("-")  # split in to parts
        print  txt  ,  len(txt)
        if len(txt) == 1:
            return  [text, text]
        return txt
        
    def _split_verses(self, text):
        print text
        txt = text.split("-")  # split in to parts
        print  txt  ,  len(txt)
        if len(txt) == 1:
            return [text, text]
        return txt        

    def _split_book_from_verses(self, search):
        v = search.split(" ")  # split in to parts
        book = ""
        for i in range (0, len(v) - 1 ): # Join the books back together except last word
            book += v[i] + " "
        verse = v[len(v)-1]
        return book, verse

    def _split_chapters_and_verses(self, verse):
        verse = verse.lower().replace("v", ":")  # allow V or v for verse instead of :
        c = verse.split(":")
        if len(c) == 1:
            return c[0], []
        return c[0], c[1]
