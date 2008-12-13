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

from openlp.plugins.bibles.lib.biblemanager import BibleManager
from openlp.plugins.bibles.forms.bibleimportform import BibleImportForm

import logging

class BiblePlugin(Plugin):
    global log
    log=logging.getLogger("BiblePlugin")
    log.info("Bible Plugin loaded")    
    def __init__(self):
        # Call the parent constructor
        Plugin.__init__(self, 'Bible', '1.9.0')
        self.Weight = -9
        #Register the bible Manager
        self.biblemanager = BibleManager(self.config)
        self.searchresults = {} # place to store the search results

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

        self.listView = QtGui.QListWidget()
        self.listView.setGeometry(QtCore.QRect(10, 200, 256, 391))
        self.listView.setObjectName("listView")
        self.MediaManagerItem.PageLayout.addWidget(self.listView)
         
        #QtCore.QObject.connect(self.QuickTab, QtCore.SIGNAL("triggered()"), self.onQuickTabClick)
        QtCore.QObject.connect( self.SearchTabWidget, QtCore.SIGNAL("currentChanged ( QWidget * )" ), self.onQuickTabClick)
        QtCore.QObject.connect(self.AdvancedVersionComboBox, QtCore.SIGNAL("activated(int)"), self.onAdvancedVersionComboBox)
        QtCore.QObject.connect(self.AdvancedBookComboBox, QtCore.SIGNAL("activated(int)"), self.onAdvancedBookComboBox)      
        QtCore.QObject.connect(self.AdvancedFromChapter, QtCore.SIGNAL("activated(int)"), self.onAdvancedFromChapter)
        QtCore.QObject.connect(self.AdvancedFromVerse, QtCore.SIGNAL("activated(int)"), self.onAdvancedFromVerse)
        QtCore.QObject.connect(self.AdvancedToChapter, QtCore.SIGNAL("activated(int)"), self.onAdvancedToChapter)
        QtCore.QObject.connect(self.AdvancedSearchButton, QtCore.SIGNAL("pressed()"), self.onAdvancedSearchButton)
        QtCore.QObject.connect(self.QuickSearchButton, QtCore.SIGNAL("pressed()"), self.onQuickSearchButton) 
       
        return self.MediaManagerItem

    def initalise_ui(self):
        self._initialiseForm()

    def onAdvancedVersionComboBox(self):
        self._initialiseBibleAdvanced(str(self.AdvancedVersionComboBox.currentText())) # restet the bible info

    def onAdvancedBookComboBox(self):
        print self.AdvancedVersionComboBox.currentText()
        self._initialiseBibleAdvanced(str(self.AdvancedVersionComboBox.currentText())) # restet the bible info
        
    def onQuickTabClick(self):
        print "onQuickTabClick"
        print self.SearchTabWidget.currentIndex()
        print self.SearchTabWidget.tabText(self.SearchTabWidget.currentIndex())
        pass

    def onBibleNewClick(self):
        self.bibleimportform = BibleImportForm(self.biblemanager)
        self.bibleimportform.setModal(True)
        self.bibleimportform.show()
        pass

    def onBiblePreviewClick(self):
        pass

    def onBibleLiveClick(self):
        pass

    def onBibleAddClick(self):
        pass

    def _initialiseForm(self):
        bibles = self.biblemanager.getBibles()
        self.QuickSearchComboBox.addItem("Text Search")
        self.QuickSearchComboBox.addItem("Verse Search")        
        first = True
        for b in bibles:  # load bibles into the combo boxes
            self.QuickVersionComboBox.addItem(b)
            self.AdvancedVersionComboBox.addItem(b)            
            if first:
                first = False
                self._initialiseBible(b) # use the fist bible as the trigger


    def _initialiseBible(self, bible):
        log.debug("_initialiseBible %s ", bible)                
        self._initialiseBibleQuick(bible)
        self._initialiseBibleAdvanced(bible)

    def _initialiseBibleAdvanced(self, bible):
        log.debug("_initialiseBibleAdvanced %s ", bible)
        currentBook = str(self.AdvancedBookComboBox.currentText())
        cf = self.biblemanager.getBookChapterCount(bible, currentBook)[0]
        log.debug("Book change bible %s book %s ChapterCount %s", bible, currentBook, cf)
        if cf == None: # Only change the search details if the book is missing from the new bible
            books = self.biblemanager.getBibleBooks(str(self.AdvancedVersionComboBox.currentText())) 
            self.AdvancedBookComboBox.clear()
            first = True
            for b in books:
                self.AdvancedBookComboBox.addItem(b[0])            
                if first:
                    book = b
                    first = False
                    self._initialiseChapterVerse(bible, b[0])

    def _initialiseChapterVerse(self, bible, book):
        log.debug("_initialiseChapterVerse %s , %s", bible, book)
        self.chaptersfrom = self.biblemanager.getBookChapterCount(bible, book)[0]
        self.verses = self.biblemanager.getBookVerseCount(bible, book, 1)[0]
        self._adjustComboBox(1, self.chaptersfrom, self.AdvancedFromChapter)
        self._adjustComboBox(1, self.chaptersfrom, self.AdvancedToChapter) 
        self._adjustComboBox(1, self.verses, self.AdvancedFromVerse)
        self._adjustComboBox(1, self.verses, self.AdvancedToVerse) 
        
    def onAdvancedFromChapter(self):
        bible = str(self.AdvancedVersionComboBox.currentText())
        book = str(self.AdvancedBookComboBox.currentText())
        cf = self.AdvancedFromChapter.currentText()
        self._adjustComboBox(cf, self.chaptersfrom, self.AdvancedToChapter)
        vse = self.biblemanager.getBookVerseCount(bible, book, int(cf))[0] # get the verse count for new chapter
        self._adjustComboBox(1, vse, self.AdvancedFromVerse)        
        self._adjustComboBox(1, vse, self.AdvancedToVerse)        
        
    def _adjustComboBox(self, frm, to , combo):
        log.debug("_adjustComboBox %s , %s , %s", combo, frm,  to)        
        combo.clear()
        for i in range(int(frm), int(to) + 1):            
            combo.addItem(str(i))
        
    def onAdvancedFromVerse(self):
        frm = self.AdvancedFromVerse.currentText()
        self._adjustComboBox(frm, self.verses, self.AdvancedToVerse)
        
    def onAdvancedToChapter(self): 
        t1 =  self.AdvancedFromChapter.currentText()        
        t2 =  self.AdvancedToChapter.currentText()
        if t1 != t2:
            bible = str(self.AdvancedVersionComboBox.currentText())
            book = str(self.AdvancedBookComboBox.currentText())            
            vse = self.biblemanager.getBookVerseCount(bible, book, int(t2))[0] # get the verse count for new chapter
            self._adjustComboBox(1, vse, self.AdvancedToVerse)             
        
    def onAdvancedSearchButton(self):
        bible = str(self.AdvancedVersionComboBox.currentText())
        book = str(self.AdvancedBookComboBox.currentText()) 
        chapfrom =  int(self.AdvancedFromChapter.currentText())
        chapto =  int(self.AdvancedToChapter.currentText())
        versefrom =  int(self.AdvancedFromVerse.currentText())
        verseto =  int(self.AdvancedToVerse.currentText())
        self.searchresults = self.biblemanager.getVerseText(bible, book, chapfrom, versefrom, verseto) 
        self._displayResults()
                
    def onQuickSearchButton(self):
        bible = str(self.QuickVersionComboBox.currentText())
        text = str(self.QuickSearchEdit.displayText())
        
        if self.QuickSearchComboBox.currentText() == "Text Search":
            self._searchText(bible, text)
        else:
            self._verseSearch()
            
    def _searchText(self, bible, text):
        self.searchresults = self.biblemanager.getVersesFromText(bible,text) 
        self._displayResults()        

    def _verseSearch(self):
        self._displayResults()        
    
    def _displayResults(self):
        self.listView.clear() # clear the results
        for book, chap, vse , txt in self.searchresults:
            self.listView.addItem(book + " " +str(chap) + ":"+ str(vse))
        
    def _initialiseBibleQuick(self, bible): # not sure if needed yet!
        a=1
