# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 - 2009 Martin Thompson, Tim Bentley

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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from openlp.core.resources import *
from openlp.core.lib import Plugin,PluginUtils,  MediaManagerItem, Receiver

from openlp.plugins.bibles.lib import BibleManager, BiblesTab
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
        self.search_results = {} # place to store the search results
        QtCore.QObject.connect(Receiver().get_receiver(),
            QtCore.SIGNAL("openlpreloadbibles"), self.reload_bibles)

    def get_settings_tab(self):
        self.BiblesTab = BiblesTab()
        """
        self.Bibles = QtGui.QWidget()
        self.Bibles.setObjectName("Bibles")
        self.formLayout_3 = QtGui.QFormLayout(self.Bibles)
        self.formLayout_3.setObjectName("formLayout_3")
        self.VerseDisplayGroupBox = QtGui.QGroupBox(self.Bibles)
        self.VerseDisplayGroupBox.setObjectName("VerseDisplayGroupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.VerseDisplayGroupBox)
        self.gridLayout_2.setMargin(8)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.VerseTypeWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.VerseTypeWidget.setObjectName("VerseTypeWidget")
        self.VerseTypeLayout = QtGui.QHBoxLayout(self.VerseTypeWidget)
        self.VerseTypeLayout.setSpacing(8)
        self.VerseTypeLayout.setMargin(0)
        self.VerseTypeLayout.setObjectName("VerseTypeLayout")
        self.VerseRadioButton = QtGui.QRadioButton(self.VerseTypeWidget)
        self.VerseRadioButton.setObjectName("VerseRadioButton")
        self.VerseTypeLayout.addWidget(self.VerseRadioButton)
        self.ParagraphRadioButton = QtGui.QRadioButton(self.VerseTypeWidget)
        self.ParagraphRadioButton.setChecked(True)
        self.ParagraphRadioButton.setObjectName("ParagraphRadioButton")
        self.VerseTypeLayout.addWidget(self.ParagraphRadioButton)
        self.gridLayout_2.addWidget(self.VerseTypeWidget, 0, 0, 1, 1)
        self.NewChaptersCheckBox = QtGui.QCheckBox(self.VerseDisplayGroupBox)
        self.NewChaptersCheckBox.setObjectName("NewChaptersCheckBox")
        self.gridLayout_2.addWidget(self.NewChaptersCheckBox, 1, 0, 1, 1)
        self.DisplayStyleWidget = QtGui.QWidget(self.VerseDisplayGroupBox)
        self.DisplayStyleWidget.setObjectName("DisplayStyleWidget")
        self.DisplayStyleLayout = QtGui.QHBoxLayout(self.DisplayStyleWidget)
        self.DisplayStyleLayout.setSpacing(8)
        self.DisplayStyleLayout.setMargin(0)
        self.DisplayStyleLayout.setObjectName("DisplayStyleLayout")
        self.DisplayStyleLabel = QtGui.QLabel(self.DisplayStyleWidget)
        self.DisplayStyleLabel.setObjectName("DisplayStyleLabel")
        self.DisplayStyleLayout.addWidget(self.DisplayStyleLabel)
        self.DisplayStyleComboBox = QtGui.QComboBox(self.DisplayStyleWidget)
        self.DisplayStyleComboBox.setObjectName("DisplayStyleComboBox")
        self.DisplayStyleComboBox.addItem(QtCore.QString())
        self.DisplayStyleComboBox.addItem(QtCore.QString())
        self.DisplayStyleComboBox.addItem(QtCore.QString())
        self.DisplayStyleComboBox.addItem(QtCore.QString())
        self.DisplayStyleLayout.addWidget(self.DisplayStyleComboBox)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.DisplayStyleLayout.addItem(spacerItem6)
        self.gridLayout_2.addWidget(self.DisplayStyleWidget, 2, 0, 1, 1)
        self.ChangeNoteLabel = QtGui.QLabel(self.VerseDisplayGroupBox)
        self.ChangeNoteLabel.setObjectName("ChangeNoteLabel")
        self.gridLayout_2.addWidget(self.ChangeNoteLabel, 3, 0, 1, 1)
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.VerseDisplayGroupBox)
        self.SearchGroupBox_2 = QtGui.QGroupBox(self.Bibles)
        self.SearchGroupBox_2.setObjectName("SearchGroupBox_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.SearchGroupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.SearchCheckBox_2 = QtGui.QCheckBox(self.SearchGroupBox_2)
        self.SearchCheckBox_2.setChecked(True)
        self.SearchCheckBox_2.setObjectName("SearchCheckBox_2")
        self.verticalLayout_2.addWidget(self.SearchCheckBox_2)
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.SearchGroupBox_2)

        self.VerseDisplayGroupBox.setTitle(QtGui.QApplication.translate("SettingsForm", "Verse Display", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseRadioButton.setText(QtGui.QApplication.translate("SettingsForm", "Verse style", None, QtGui.QApplication.UnicodeUTF8))
        self.ParagraphRadioButton.setText(QtGui.QApplication.translate("SettingsForm", "Paragraph style", None, QtGui.QApplication.UnicodeUTF8))
        self.NewChaptersCheckBox.setText(QtGui.QApplication.translate("SettingsForm", "Only show new chapter numbers", None, QtGui.QApplication.UnicodeUTF8))
        self.DisplayStyleLabel.setText(QtGui.QApplication.translate("SettingsForm", "Display Style:", None, QtGui.QApplication.UnicodeUTF8))
        self.DisplayStyleComboBox.setItemText(0, QtGui.QApplication.translate("SettingsForm", "No brackets", None, QtGui.QApplication.UnicodeUTF8))
        self.DisplayStyleComboBox.setItemText(1, QtGui.QApplication.translate("SettingsForm", "( and )", None, QtGui.QApplication.UnicodeUTF8))
        self.DisplayStyleComboBox.setItemText(2, QtGui.QApplication.translate("SettingsForm", "{ and }", None, QtGui.QApplication.UnicodeUTF8))
        self.DisplayStyleComboBox.setItemText(3, QtGui.QApplication.translate("SettingsForm", "[ and ]", None, QtGui.QApplication.UnicodeUTF8))
        self.ChangeNoteLabel.setText(QtGui.QApplication.translate("SettingsForm", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Changes don\'t affect verses already in the service</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.SearchGroupBox_2.setTitle(QtGui.QApplication.translate("SettingsForm", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.SearchCheckBox_2.setText(QtGui.QApplication.translate("SettingsForm", "Enabled search-as-you-type", None, QtGui.QApplication.UnicodeUTF8))

        self.SettingsTabItem.add_items(self.Bibles)
        self.SettingsTabItem.setTabText(QtGui.QApplication.translate("SettingsForm", "Bibles", None, QtGui.QApplication.UnicodeUTF8))
        """
        return self.BiblesTab

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

        self.QuickClearLabel = QtGui.QLabel(self.QuickTab)
        self.QuickClearLabel.setObjectName('QuickSearchLabel')
        self.QuickClearLabel.setText('Results:')
        self.QuickLayout.addWidget(self.QuickClearLabel, 3, 0, 1, 1)
        self.ClearQuickSearchComboBox = QtGui.QComboBox(self.QuickTab)
        self.ClearQuickSearchComboBox.setObjectName('ClearQuickSearchComboBox')
        self.QuickLayout.addWidget(self.ClearQuickSearchComboBox, 3, 1, 1, 1)
        self.SearchTabWidget.addTab(self.QuickTab, 'Quick')
        QuickSpacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.QuickLayout.addItem(QuickSpacerItem, 4, 2, 1, 1)

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

        self.AdvancedClearLabel = QtGui.QLabel(self.QuickTab)
        self.AdvancedClearLabel.setObjectName('QuickSearchLabel')
        self.AdvancedClearLabel.setText('Results:')
        self.AdvancedLayout.addWidget(self.AdvancedClearLabel, 5, 0, 1, 1)
        self.ClearAdvancedSearchComboBox = QtGui.QComboBox(self.QuickTab)
        self.ClearAdvancedSearchComboBox.setObjectName('ClearAdvancedSearchComboBox')
        self.AdvancedLayout.addWidget(self.ClearAdvancedSearchComboBox, 5, 2, 1, 1)

        self.AdvancedSearchButton = QtGui.QPushButton(self.AdvancedTab)
        self.AdvancedSearchButton.setObjectName('AdvancedSearchButton')
        self.AdvancedSearchButton.setText('Search')
        self.AdvancedLayout.addWidget(self.AdvancedSearchButton, 5, 3, 1, 1)
        self.SearchTabWidget.addTab(self.AdvancedTab, 'Advanced')

        # Add the search tab widget to the page layout
        self.MediaManagerItem.PageLayout.addWidget(self.SearchTabWidget)

        self.BibleListView = QtGui.QTableWidget()
        self.BibleListView.setColumnCount(2)
        self.BibleListView.setColumnHidden(0, True)
        self.BibleListView.setColumnWidth(1, 275)
        self.BibleListView.setShowGrid(False)
        self.BibleListView.setSortingEnabled(False)
        self.BibleListView.setAlternatingRowColors(True)
        self.BibleListView.verticalHeader().setVisible(False)
        self.BibleListView.horizontalHeader().setVisible(False)

        self.BibleListView.setGeometry(QtCore.QRect(10, 200, 256, 391))
        self.BibleListView.setObjectName("listView")
        self.BibleListView.setAlternatingRowColors(True)
        self.MediaManagerItem.PageLayout.addWidget(self.BibleListView)

        ##############Combo Boxes
        QtCore.QObject.connect(self.AdvancedVersionComboBox, QtCore.SIGNAL("activated(int)"), self.onAdvancedVersionComboBox)
        QtCore.QObject.connect(self.AdvancedBookComboBox, QtCore.SIGNAL("activated(int)"), self.onAdvancedBookComboBox)
        QtCore.QObject.connect(self.AdvancedFromChapter, QtCore.SIGNAL("activated(int)"), self.onAdvancedFromChapter)
        QtCore.QObject.connect(self.AdvancedFromVerse, QtCore.SIGNAL("activated(int)"), self.onAdvancedFromVerse)
        QtCore.QObject.connect(self.AdvancedToChapter, QtCore.SIGNAL("activated(int)"), self.onAdvancedToChapter)

        ##############Buttons
        QtCore.QObject.connect(self.AdvancedSearchButton, QtCore.SIGNAL("pressed()"), self.onAdvancedSearchButton)
        QtCore.QObject.connect(self.QuickSearchButton, QtCore.SIGNAL("pressed()"), self.onQuickSearchButton)

        ##############Context Menus
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
        self._initialise_form() # build the form

    def _initialise_form(self):
        log.debug("_initialise_form")
        self.QuickSearchComboBox.clear()
        self.QuickVersionComboBox.clear()
        self.AdvancedVersionComboBox.clear()
        self.ClearQuickSearchComboBox.clear()
        self.ClearAdvancedSearchComboBox.clear()

        self.QuickSearchComboBox.addItem(u"Verse Search")
        self.QuickSearchComboBox.addItem(u"Text Search")
        self.ClearQuickSearchComboBox.addItem(u"Clear")
        self.ClearQuickSearchComboBox.addItem(u"Keep")
        self.ClearAdvancedSearchComboBox.addItem(u"Clear")
        self.ClearAdvancedSearchComboBox.addItem(u"Keep")


        bibles = self.biblemanager.get_bibles("full")
        for b in bibles:  # load bibles into the combo boxes
            self.QuickVersionComboBox.addItem(b)

        bibles = self.biblemanager.get_bibles("partial") # Without HTTP
        first = True
        for b in bibles:  # load bibles into the combo boxes
            self.AdvancedVersionComboBox.addItem(b)
            if first:
                first = False
                self._initialise_bible_advanced(b) # use the first bible as the trigger

    def onAdvancedVersionComboBox(self):
        self._initialise_bible_advanced(str(self.AdvancedVersionComboBox.currentText())) # restet the bible info
        pass

    def onAdvancedBookComboBox(self):
        self._initialise_bible_advanced(str(self.AdvancedVersionComboBox.currentText())) # restet the bible info

    def onBibleNewClick(self):
        self.bibleimportform = BibleImportForm(self.config, self.biblemanager, self)
        self.bibleimportform.exec_()
        pass

    def onBibleLiveClick(self):
        pass

    def onBibleAddClick(self):
        pass

    def onSettingsSaveButton(self):
        self._save_settings()

    def onSettingsResetButton(self):
        self._load_reset_settings()

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
        chapter_from =  int(self.AdvancedFromChapter.currentText())
        chapter_to =  int(self.AdvancedToChapter.currentText())
        verse_from =  int(self.AdvancedFromVerse.currentText())
        verse_to =  int(self.AdvancedToVerse.currentText())
        self.search_results = self.biblemanager.get_verse_text(bible, book, chapter_from, chapter_to, verse_from, verse_to)
        if self.ClearAdvancedSearchComboBox.currentText() == u"Clear":
            self.BibleListView.clear() # clear the results
            self.BibleListView.setRowCount(0)
        self._display_results(bible)

    def onAdvancedFromChapter(self):
        bible = str(self.AdvancedVersionComboBox.currentText())
        book = str(self.AdvancedBookComboBox.currentText())
        cf = self.AdvancedFromChapter.currentText()
        self._adjust_combobox(cf, self.chapters_from, self.AdvancedToChapter)
        vse = self.biblemanager.get_book_verse_count(bible, book, int(cf))[0] # get the verse count for new chapter
        self._adjust_combobox(1, vse, self.AdvancedFromVerse)
        self._adjust_combobox(1, vse, self.AdvancedToVerse)

    def onQuickSearchButton(self):
        self.log.debug("onQuickSearchButton")
        bible = str(self.QuickVersionComboBox.currentText())
        text = str(self.QuickSearchEdit.displayText())

        if self.ClearQuickSearchComboBox.currentText() == u"Clear":
            self.BibleListView.clear() # clear the results
            self.BibleListView.setRowCount(0)

        if self.QuickSearchComboBox.currentText() == u"Text Search":
            self.search_results = self.biblemanager.get_verse_from_text(bible,text)
        else:
            self._search_using_bible_reference(bible, text)
        if not self.search_results == None:
            self._display_results(bible)

    def onBiblePreviewClick(self):
        items = self.BibleListView.selectedItems()
        for item in items:
            text = str(item.text())
            verse = text[:text.find("(")]
            bible = text[text.find("(")+1:text.find(")")]
            self._search_using_bible_reference(bible,  verse)
            book = self.search_results[0][0]
            chapter = str(self.search_results[0][1])
            verse = str(self.search_results[0][2])
            text = self.search_results[0][3]
            o = self.SettingsOutputStyleComboBox.currentIndex()
            v = self.SettingsVerseStyleComboBox.currentIndex()
            if o == 1: #Paragraph
                text = text + u"\n"
            if v == 1: #Paragraph
                loc = self._format_verse(chapter, verse, u"(", u")")
            elif v == 2: #Paragraph
                loc = self._format_verse(chapter, verse, u"{", u"}")
            elif v == 3: #Paragraph
                loc = self._format_verse(chapter, verse, u"[", u"]")
            else:
                loc = self._format_verse(chapter, verse, u"", u"")
            print book
            print loc
            print text

    def _format_verse(self, chapter, verse, opening, closing):
        loc = opening
        if self.SettingsNewChapterCheck.checkState() == 2:
            loc += chapter+u":"
        loc += verse
        loc += closing
        return loc

    def reload_bibles(self):
        self.biblemanager.reload_bibles()
        self._initialise_form()

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
        self.chapters_from = self.biblemanager.get_book_chapter_count(bible, book)[0]
        self.verses = self.biblemanager.get_book_verse_count(bible, book, 1)[0]
        self._adjust_combobox(1, self.chapters_from, self.AdvancedFromChapter)
        self._adjust_combobox(1, self.chapters_from, self.AdvancedToChapter)
        self._adjust_combobox(1, self.verses, self.AdvancedFromVerse)
        self._adjust_combobox(1, self.verses, self.AdvancedToVerse)

    def _adjust_combobox(self, frm, to , combo):
        log.debug("_adjust_combobox %s , %s , %s", combo, frm,  to)
        combo.clear()
        for i in range(int(frm), int(to) + 1):
            combo.addItem(str(i))

    def _display_results(self, bible):
        for book, chap, vse , txt in self.search_results:
            row_count = self.BibleListView.rowCount()
            self.BibleListView.setRowCount(row_count+1)
            table_data = QtGui.QTableWidgetItem(str(bible))
            self.BibleListView.setItem(row_count , 0, table_data)
            table_data = QtGui.QTableWidgetItem(str(book + " " +str(chap) + ":"+ str(vse)) + " ("+str(bible)+")")
            self.BibleListView.setItem(row_count , 1, table_data)
            self.BibleListView.setRowHeight(row_count, 20)

    def _search_using_bible_reference(self, bible,  search):
        book = ""
        start_chapter = ""
        end_chapter = ""
        start_verse=""
        end_verse=""
        search.replace("  ", " ")
        search = search.strip()
        original = search
        message = None
        # Remove book
        for i in range (len(search)-1, 0, -1):   # 0 index arrays
            if search[i] == " ":
                book = search[:i]
                search = search[i:] # remove book from string
                break
        search = search.replace("v", ":")  # allow V or v for verse instead of :
        search = search.replace("V", ":")  # allow V or v for verse instead of :
        search = search.strip()
        co = search.find(":")
        if co == -1: # no : found
            i = search.rfind(" ")
            if i == -1:
                chapter = ""
            else:
                chapter = search[i:len(search)]
            hi = chapter.find("-")
            if hi != -1:
                start_chapter= chapter[:hi]
                end_chapter= chapter[hi+1:len(chapter)]
            else:
                start_chapter = chapter
        else: # more complex
            #print search
            sp = search.split("-") #find first
            #print sp, len(sp)
            sp1 = sp[0].split(":")
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
                sp1 = sp[1].split(":")
                #print sp1, len(sp1)
                if len(sp1) == 1:
                    end_chapter = sp1[0]
                    end_verse = 1
                else:
                    end_chapter = sp1[0]
                    end_verse = sp1[1]
        if end_chapter == "":
            end_chapter = start_chapter.rstrip()
        if start_verse == "":
            if end_verse == "":
                start_verse = 1
            else:
                start_verse = end_verse
        if end_verse == "":
            end_verse = 99
        if start_chapter == "":
            message = "No chapter found for search"
        #print "message = " + str(message)
        #print "search = " + str(original)
        #print "results = " + str(book) + " @ "+ str(start_chapter)+" @ "+ str(end_chapter)+" @ "+ str(start_verse)+ " @ "+ str(end_verse)

        if message  == None:
            self.search_results = None
            self.search_results = self.biblemanager.get_verse_text(bible, book,int(start_chapter), int(end_chapter), int(start_verse), int(end_verse))
        else:
            reply = QtGui.QMessageBox.information(self.MediaManagerItem,"Information",message)

    def load_settings(self):
        pass
#        self.SettingsOutputStyleComboBox.setCurrentIndex(int(self.config.get_config("bible_output_style", 0)))
#        self.SettingsVerseStyleComboBox.setCurrentIndex(int(self.config.get_config("bible_verse_style", 0)))
#        try:
#            self.SettingsNewChapterCheck.setCheckState(int(self.config.get_config("bible_new_chapter", 0)))
#        except:
#            pass

    def save_settings(self):
        pass
#        self.config.set_config("bible_output_style", str(self.SettingsOutputStyleComboBox.currentIndex()))
#        self.config.set_config("bible_verse_style", str(self.SettingsVerseStyleComboBox.currentIndex()))
#        self.config.set_config("bible_new_chapter", str(self.SettingsNewChapterCheck.checkState()))

#        self.SettingsOutputStyleComboBox.clear()
#       self.SettingsVerseStyleComboBox.clear()

#        self.SettingsOutputStyleComboBox.addItem(u"Continuous")
#        self.SettingsOutputStyleComboBox.addItem(u"Paragraph")
#        self.SettingsVerseStyleComboBox.addItem(u"No Brackets")
#        self.SettingsVerseStyleComboBox.addItem(u"( and )")
#        self.SettingsVerseStyleComboBox.addItem(u"{ and }")
#        self.SettingsVerseStyleComboBox.addItem(u"[ and ]")


    def define_tab(self):
        pass
#        QtCore.QObject.connect(self.SettingsResetButton, QtCore.SIGNAL("pressed()"), self.onSettingsResetButton)
#        QtCore.QObject.connect(self.SettingsSaveButton, QtCore.SIGNAL("pressed()"), self.onSettingsSaveButton)
