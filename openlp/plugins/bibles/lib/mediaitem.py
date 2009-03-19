# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley

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

from openlp.core import translate
from openlp.core.lib import MediaManagerItem, Receiver
from openlp.core.resources import *

from openlp.plugins.bibles.forms import BibleImportForm
from openlp.plugins.bibles.lib import TextListData

class BibleMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Bibles.
    """
    global log
    log=logging.getLogger(u'BibleMediaItem')
    log.info(u'Bible Media Item loaded')

    def __init__(self, parent, icon, title):
        MediaManagerItem.__init__(self, parent, icon, title)
        self.search_results = {} # place to store the search results
        QtCore.QObject.connect(Receiver().get_receiver(),
            QtCore.SIGNAL("openlpreloadbibles"), self.reloadBibles)

    def setupUi(self):
        # Add a toolbar
        self.addToolbar()
        # Create buttons for the toolbar
        ## New Bible Button ##
        self.addToolbarButton(
            translate(u'BibleMediaItem','New Bible'), 
            translate(u'BibleMediaItem','Register a new Bible'),
            ':/themes/theme_import.png', self.onBibleNewClick, 'BibleNewItem')
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview Bible Button ##
        self.addToolbarButton(
            translate(u'BibleMediaItem','Preview Bible'), 
            translate(u'BibleMediaItem','Preview the selected Bible Verse'),
            ':/system/system_preview.png', self.onBiblePreviewClick, 'BiblePreviewItem')
        ## Live Bible Button ##
        self.addToolbarButton(
            translate(u'BibleMediaItem','Go Live'), 
            translate(u'BibleMediaItem','Send the selected Bible Verse(s) live'),
            ':/system/system_live.png', self.onBibleLiveClick, 'BibleLiveItem')
        ## Add Bible Button ##
        self.addToolbarButton(
            translate(u'BibleMediaItem','Add Bible Verse(s) To Service'),
            translate(u'BibleMediaItem','Add the selected Bible(s) to the service'),
            ':/system/system_add.png',
            self.onBibleAddClick, 'BibleAddItem')

        # Create the tab widget
        self.SearchTabWidget = QtGui.QTabWidget(self)
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
        self.QuickLayout.setMargin(8)
        self.QuickLayout.setSpacing(8)
        self.QuickLayout.setObjectName('QuickLayout')
        self.QuickVersionLabel = QtGui.QLabel(self.QuickTab)
        self.QuickVersionLabel.setObjectName('QuickVersionLabel')
        self.QuickLayout.addWidget(self.QuickVersionLabel, 0, 0, 1, 1)
        self.QuickVersionComboBox = QtGui.QComboBox(self.QuickTab)
        self.QuickVersionComboBox.setObjectName('VersionComboBox')
        self.QuickLayout.addWidget(self.QuickVersionComboBox, 0, 1, 1, 2)
        self.QuickSearchLabel = QtGui.QLabel(self.QuickTab)
        self.QuickSearchLabel.setObjectName('QuickSearchLabel')
        self.QuickLayout.addWidget(self.QuickSearchLabel, 1, 0, 1, 1)
        self.QuickSearchComboBox = QtGui.QComboBox(self.QuickTab)
        self.QuickSearchComboBox.setObjectName('SearchComboBox')
        self.QuickLayout.addWidget(self.QuickSearchComboBox, 1, 1, 1, 2)
        self.QuickSearchLabel = QtGui.QLabel(self.QuickTab)
        self.QuickSearchLabel.setObjectName('QuickSearchLabel')
        self.QuickLayout.addWidget(self.QuickSearchLabel, 2, 0, 1, 1)
        self.QuickSearchEdit = QtGui.QLineEdit(self.QuickTab)
        self.QuickSearchEdit.setObjectName('QuickSearchEdit')
        self.QuickLayout.addWidget(self.QuickSearchEdit, 2, 1, 1, 2)
        self.QuickSearchButton = QtGui.QPushButton(self.QuickTab)
        self.QuickSearchButton.setObjectName('QuickSearchButton')
        self.QuickLayout.addWidget(self.QuickSearchButton, 3, 2, 1, 1)
        self.QuickClearLabel = QtGui.QLabel(self.QuickTab)
        self.QuickClearLabel.setObjectName('QuickSearchLabel')
        self.QuickLayout.addWidget(self.QuickClearLabel, 3, 0, 1, 1)
        self.ClearQuickSearchComboBox = QtGui.QComboBox(self.QuickTab)
        self.ClearQuickSearchComboBox.setObjectName('ClearQuickSearchComboBox')
        self.QuickLayout.addWidget(self.ClearQuickSearchComboBox, 3, 1, 1, 1)
        self.SearchTabWidget.addTab(self.QuickTab, 'Quick')
        QuickSpacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.QuickLayout.addItem(QuickSpacerItem, 4, 2, 1, 1)

        # Add the Advanced Search tab
        self.AdvancedTab = QtGui.QWidget()
        self.AdvancedTab.setObjectName('AdvancedTab')
        self.AdvancedLayout = QtGui.QGridLayout(self.AdvancedTab)
        self.AdvancedLayout.setMargin(8)
        self.AdvancedLayout.setSpacing(8)
        self.AdvancedLayout.setObjectName('AdvancedLayout')
        self.AdvancedVersionLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedVersionLabel.setObjectName('AdvancedVersionLabel')
        self.AdvancedLayout.addWidget(self.AdvancedVersionLabel, 0, 0, 1, 1)
        self.AdvancedVersionComboBox = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedVersionComboBox.setObjectName('AdvancedVersionComboBox')
        self.AdvancedLayout.addWidget(self.AdvancedVersionComboBox, 0, 2, 1, 2)
        self.AdvancedBookLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedBookLabel.setObjectName('AdvancedBookLabel')
        self.AdvancedLayout.addWidget(self.AdvancedBookLabel, 1, 0, 1, 1)
        self.AdvancedBookComboBox = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedBookComboBox.setObjectName('AdvancedBookComboBox')
        self.AdvancedLayout.addWidget(self.AdvancedBookComboBox, 1, 2, 1, 2)
        self.AdvancedChapterLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedChapterLabel.setObjectName('AdvancedChapterLabel')
        self.AdvancedLayout.addWidget(self.AdvancedChapterLabel, 2, 2, 1, 1)
        self.AdvancedVerseLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedVerseLabel.setObjectName('AdvancedVerseLabel')
        self.AdvancedLayout.addWidget(self.AdvancedVerseLabel, 2, 3, 1, 1)
        self.AdvancedFromLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedFromLabel.setObjectName('AdvancedFromLabel')
        self.AdvancedLayout.addWidget(self.AdvancedFromLabel, 3, 0, 1, 1)
        self.AdvancedToLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedToLabel.setObjectName('AdvancedToLabel')
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

        self.AdvancedClearLabel = QtGui.QLabel(self.QuickTab)
        self.AdvancedClearLabel.setObjectName('QuickSearchLabel')
        self.AdvancedLayout.addWidget(self.AdvancedClearLabel, 5, 0, 1, 1)
        self.ClearAdvancedSearchComboBox = QtGui.QComboBox(self.QuickTab)
        self.ClearAdvancedSearchComboBox.setObjectName('ClearAdvancedSearchComboBox')
        self.AdvancedLayout.addWidget(self.ClearAdvancedSearchComboBox, 5, 2, 1, 1)

        self.AdvancedSearchButton = QtGui.QPushButton(self.AdvancedTab)
        self.AdvancedSearchButton.setObjectName('AdvancedSearchButton')
        self.AdvancedLayout.addWidget(self.AdvancedSearchButton, 5, 3, 1, 1)
        self.SearchTabWidget.addTab(self.AdvancedTab, 'Advanced')

        # Add the search tab widget to the page layout
        self.PageLayout.addWidget(self.SearchTabWidget)

        self.BibleListView = QtGui.QListView()
        self.BibleListView.setAlternatingRowColors(True)
        self.BibleListData = TextListData()
        self.BibleListView.setModel(self.BibleListData)
        
        self.PageLayout.addWidget(self.BibleListView)
        
        # Combo Boxes
        QtCore.QObject.connect(self.AdvancedVersionComboBox,
            QtCore.SIGNAL("activated(int)"), self.onAdvancedVersionComboBox)
        QtCore.QObject.connect(self.AdvancedBookComboBox,
            QtCore.SIGNAL("activated(int)"), self.onAdvancedBookComboBox)
        QtCore.QObject.connect(self.AdvancedFromChapter,
            QtCore.SIGNAL("activated(int)"), self.onAdvancedFromChapter)
        QtCore.QObject.connect(self.AdvancedFromVerse,
            QtCore.SIGNAL("activated(int)"), self.onAdvancedFromVerse)
        QtCore.QObject.connect(self.AdvancedToChapter,
            QtCore.SIGNAL("activated(int)"), self.onAdvancedToChapter)
        # Buttons
        QtCore.QObject.connect(self.AdvancedSearchButton,
            QtCore.SIGNAL("pressed()"), self.onAdvancedSearchButton)
        QtCore.QObject.connect(self.QuickSearchButton,
            QtCore.SIGNAL("pressed()"), self.onQuickSearchButton)
        # Context Menus
        self.BibleListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.BibleListView.addAction(self.contextMenuAction(
            self.BibleListView, ':/system/system_preview.png',
            translate(u'BibleMediaItem',u'&Preview Verse'), self.onBiblePreviewClick))
        self.BibleListView.addAction(self.contextMenuAction(
            self.BibleListView, ':/system/system_live.png',
            translate(u'BibleMediaItem',u'&Show Live'), self.onBibleLiveClick))
        self.BibleListView.addAction(self.contextMenuAction(
            self.BibleListView, ':/system/system_add.png',
            translate(u'BibleMediaItem',u'&Add to Service'), self.onBibleAddClick))

    def retranslateUi(self):
        log.debug(u'retranslateUi')        
        self.QuickVersionLabel.setText(translate(u'BibleMediaItem', u'Version:'))
        self.QuickSearchLabel.setText(translate(u'BibleMediaItem', u'Search Type:'))
        self.QuickSearchLabel.setText(translate(u'BibleMediaItem', u'Find:'))
        self.QuickSearchButton.setText(translate(u'BibleMediaItem', u'Search'))
        self.QuickClearLabel.setText(translate(u'BibleMediaItem', u'Results:'))
        self.AdvancedVersionLabel.setText(translate(u'BibleMediaItem', u'Version:'))
        self.AdvancedBookLabel.setText(translate(u'BibleMediaItem', u'Book:'))
        self.AdvancedChapterLabel.setText(translate(u'BibleMediaItem', u'Chapter:'))
        self.AdvancedVerseLabel.setText(translate(u'BibleMediaItem', u'Verse:'))
        self.AdvancedFromLabel.setText(translate(u'BibleMediaItem', u'From:'))
        self.AdvancedToLabel.setText(translate(u'BibleMediaItem', u'To:'))
        self.AdvancedClearLabel.setText(translate(u'BibleMediaItem', u'Results:'))
        self.AdvancedSearchButton.setText(translate(u'BibleMediaItem', u'Search'))
        self.QuickSearchComboBox.addItem(translate(u'BibleMediaItem', u'Verse Search'))
        self.QuickSearchComboBox.addItem(translate(u'BibleMediaItem', u'Text Search'))
        self.ClearQuickSearchComboBox.addItem(translate(u'BibleMediaItem', u'Clear'))
        self.ClearQuickSearchComboBox.addItem(translate(u'BibleMediaItem', u'Keep'))
        self.ClearAdvancedSearchComboBox.addItem(translate(u'BibleMediaItem', u'Clear'))
        self.ClearAdvancedSearchComboBox.addItem(translate(u'BibleMediaItem', u'Keep'))

    def initialise(self):
        log.debug(u'initialise')
        self.loadBibles()

    def loadBibles(self):
        log.debug(u'Loading Bibles')  
        self.QuickVersionComboBox.clear()
        self.AdvancedVersionComboBox.clear()
        
        bibles = self.parent.biblemanager.get_bibles(u'full')
        
        for bible in bibles:  # load bibles into the combo boxes
            self.QuickVersionComboBox.addItem(bible)
            
        bibles = self.parent.biblemanager.get_bibles(u'partial') # Without HTTP
        first = True
        for bible in bibles:  # load bibles into the combo boxes
            self.AdvancedVersionComboBox.addItem(bible)
            if first:
                first = False
                self.initialiseBible(bible) # use the first bible as the trigger

    def onAdvancedVersionComboBox(self):
        self.initialiseBible(str(self.AdvancedVersionComboBox.currentText())) # restet the bible info

    def onAdvancedBookComboBox(self):
        self.initialiseBible(str(self.AdvancedVersionComboBox.currentText())) # reset the bible info

    def onBibleNewClick(self):
        self.bibleimportform = BibleImportForm(self.parent.config, self.parent.biblemanager, self)
        self.bibleimportform.exec_()
        pass

    def onBibleLiveClick(self):
        pass

    def onBibleAddClick(self):
        pass

    def onAdvancedFromVerse(self):
        frm = self.AdvancedFromVerse.currentText()
        self.adjustComboBox(frm, self.verses, self.AdvancedToVerse)

    def onAdvancedToChapter(self):
        t1 =  self.AdvancedFromChapter.currentText()
        t2 =  self.AdvancedToChapter.currentText()
        if t1 != t2:
            bible = str(self.AdvancedVersionComboBox.currentText())
            book = str(self.AdvancedBookComboBox.currentText())
            vse = self.parent.biblemanager.get_book_verse_count(bible, book, int(t2))[0] # get the verse count for new chapter
            self.adjustComboBox(1, vse, self.AdvancedToVerse)

    def onAdvancedSearchButton(self):
        log.debug(u'Advanced Search Button pressed')
        bible = str(self.AdvancedVersionComboBox.currentText())
        book = str(self.AdvancedBookComboBox.currentText())
        chapter_from =  int(self.AdvancedFromChapter.currentText())
        chapter_to =  int(self.AdvancedToChapter.currentText())
        verse_from =  int(self.AdvancedFromVerse.currentText())
        verse_to =  int(self.AdvancedToVerse.currentText())
        self.search_results = self.parent.biblemanager.get_verse_text(bible, book,
            chapter_from, chapter_to, verse_from, verse_to)
        if self.ClearAdvancedSearchComboBox.currentIndex() == 0:
            self.BibleListData.resetStore()
            self.displayResults(bible)

    def onAdvancedFromChapter(self):
        bible = str(self.AdvancedVersionComboBox.currentText())
        book = str(self.AdvancedBookComboBox.currentText())
        cf = self.AdvancedFromChapter.currentText()
        self._adjust_combobox(cf, self.chapters_from, self.AdvancedToChapter)
        vse = self.parent.biblemanager.get_book_verse_count(bible, book, int(cf))[0] # get the verse count for new chapter
        self._adjust_combobox(1, vse, self.AdvancedFromVerse)
        self._adjust_combobox(1, vse, self.AdvancedToVerse)

    def onQuickSearchButton(self):
        log.debug(u'Quick Search Button pressed')
        bible = str(self.QuickVersionComboBox.currentText())
        text = str(self.QuickSearchEdit.displayText())
        if self.ClearQuickSearchComboBox.currentIndex() == 0:
            self.BibleListData.resetStore()
        if self.QuickSearchComboBox.currentIndex() == 1:
            self.search_results = self.parent.biblemanager.get_verse_from_text(bible, text)
        else:
            self.searchByReference(bible, text)
        if not self.search_results == None:
            self.displayResults(bible)

    def onBiblePreviewClick(self):
        log.debug(u'Bible Preview Button pressed')
        items = self.BibleListView.selectedIndexes()
        old_chapter = ''
        for item in items:
            text = self.BibleListData.getValue(item)
            verse = text[:text.find("(")]
            bible = text[text.find("(") + 1:text.find(")")]
            self.searchByReference(bible, verse)
            book = self.search_results[0][0]
            chapter = str(self.search_results[0][1])
            verse = str(self.search_results[0][2])
            text = self.search_results[0][3]
            if self.parent.bibles_tab.paragraph_style: #Paragraph
                text = text + u'\n'
            if self.parent.bibles_tab.display_style == 1:
                loc = self.formatVerse(old_chapter, chapter, verse, u'(', u')')
            elif  self.parent.bibles_tab.display_style == 2:
                loc = self.formatVerse(old_chapter, chapter, verse, u'{', u'}')
            elif  self.parent.bibles_tab.display_style == 3:
                loc = self.formatVerse(old_chapter, chapter, verse, u'[', u']')
            else:
                loc = self.formatVerse(old_chapter, chapter, verse, u'', u'')
            old_chapter = chapter
            print book
            print loc
            print text

    def formatVerse(self, old_chapter, chapter, verse, opening, closing):
        loc = opening
        if old_chapter != chapter:
            loc += chapter + u':'
        elif not self.parent.bibles_tab.new_chapter_check:
            loc += chapter + u':'            
        loc += verse
        loc += closing
        return loc

    def reloadBibles(self):
        log.debug(u'Reloading Bibles')
        self.parent.biblemanager.reload_bibles()
        self.loadBibles()

    def initialiseBible(self, bible):
        log.debug(u"initialiseBible %s", bible)
        current_book = str(self.AdvancedBookComboBox.currentText())
        chapter_count = self.parent.biblemanager.get_book_chapter_count(bible,
            current_book)[0]
        log.debug(u'Book change bible %s book %s ChapterCount %s', bible,
            current_book, chapter_count)
        if chapter_count == None:
            # Only change the search details if the book is missing from the new bible
            books = self.parent.biblemanager.get_bible_books(str(
                self.AdvancedVersionComboBox.currentText()))
            self.AdvancedBookComboBox.clear()
            first = True
            for book in books:
                self.AdvancedBookComboBox.addItem(book.name)
                if first:
                    first = False
                    self.initialiseChapterVerse(bible, book.name)

    def initialiseChapterVerse(self, bible, book):
        log.debug(u"initialiseChapterVerse %s , %s", bible, book)
        self.chapters_from = self.parent.biblemanager.get_book_chapter_count(bible, book)[0]
        self.verses = self.parent.biblemanager.get_book_verse_count(bible, book, 1)[0]
        self.adjustComboBox(1, self.chapters_from, self.AdvancedFromChapter)
        self.adjustComboBox(1, self.chapters_from, self.AdvancedToChapter)
        self.adjustComboBox(1, self.verses, self.AdvancedFromVerse)
        self.adjustComboBox(1, self.verses, self.AdvancedToVerse)

    def adjustComboBox(self, frm, to , combo):
        log.debug(u"adjustComboBox %s , %s , %s", combo, frm,  to)
        combo.clear()
        for i in range(int(frm), int(to) + 1):
            combo.addItem(str(i))

    def displayResults(self, bible):
        for book, chap, vse , txt in self.search_results:
            text = str(u" %s %d:%d (%s)"%(book , chap,vse, bible))
            self.BibleListData.addRow(0,text)

    def searchByReference(self, bible,  search):
        log.debug(u"searchByReference %s ,%s", bible, search)
        book = ''
        start_chapter = ''
        end_chapter = ''
        start_verse = ''
        end_verse = ''
        search = search.replace('  ', ' ').strip()
        original = search
        message = None
        # Remove book
        for i in range (len(search)-1, 0, -1):   # 0 index arrays
            if search[i] == ' ':
                book = search[:i]
                search = search[i:] # remove book from string
                break
        search = search.replace('v', ':')  # allow V or v for verse instead of :
        search = search.replace('V', ':')  # allow V or v for verse instead of :
        search = search.strip()
        colon = search.find(':')
        if colon == -1:
            # number : found
            i = search.rfind(' ')
            if i == -1:
                chapter = ''
            else:
                chapter = search[i:len(search)]
            hyphen = chapter.find('-')
            if hyphen != -1:
                start_chapter= chapter[:hyphen]
                end_chapter= chapter[hyphen + 1:len(chapter)]
            else:
                start_chapter = chapter
        else:
            # more complex
            #print search
            sp = search.split('-') #find first
            #print sp, len(sp)
            sp1 = sp[0].split(':')
            #print sp1, len(sp1)
            if len(sp1) == 1:
                start_chapter = sp1[0]
                start_verse = 1
            else:
                start_chapter = sp1[0]
                start_verse = sp1[1]
            if len(sp)== 1:
                end_chapter = start_chapter
                end_verse = start_verse
            else:
                sp1 = sp[1].split(':')
                #print sp1, len(sp1)
                if len(sp1) == 1:
                    end_chapter = sp1[0]
                    end_verse = 1
                else:
                    end_chapter = sp1[0]
                    end_verse = sp1[1]
        if end_chapter == '':
            end_chapter = start_chapter.rstrip()
        if start_verse == '':
            if end_verse == '':
                start_verse = 1
            else:
                start_verse = end_verse
        if end_verse == '':
            end_verse = 99
        if start_chapter == '':
            message = u'No chapter found for search'
        #print "message = " + str(message)
        #print "search = " + str(original)
        #print "results = " + str(book) + " @ "+ str(start_chapter)+" @ "+ str(end_chapter)+" @ "+ str(start_verse)+ " @ "+ str(end_verse)

        if message == None:
            self.search_results = None
            self.search_results = self.parent.biblemanager.get_verse_text(bible, book,
                int(start_chapter), int(end_chapter), int(start_verse),
                int(end_verse))
        else:
            reply = QtGui.QMessageBox.information(self,
                translate(u'BibleMediaItem', u'Information'),
                translate(u'BibleMediaItem', message))
