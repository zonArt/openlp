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
import time

from PyQt4 import QtCore, QtGui

from openlp.core.lib import MediaManagerItem, Receiver, str_to_bool, \
    BaseListWithDnD
from openlp.plugins.bibles.forms import ImportWizardForm

log = logging.getLogger(__name__)

class BibleListView(BaseListWithDnD):
    """
    Drag and drop capable list for Bibles.
    """
    def __init__(self, parent=None):
        self.PluginName = u'Bibles'
        BaseListWithDnD.__init__(self, parent)

    def resizeEvent(self, event):
        self.parent.onListViewResize(event.size().width(), event.size().width())


class BibleMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Bibles.
    """
    log.info(u'Bible Media Item loaded')

    def __init__(self, parent, icon, title):
        self.PluginNameShort = u'Bible'
        self.ConfigSection = title
        self.IconPath = u'songs/song'
        self.ListViewWithDnD_class = BibleListView
        self.servicePath = None
        self.lastReference = []
        MediaManagerItem.__init__(self, parent, icon, title)
        # place to store the search results
        self.search_results = {}
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlpreloadbibles'), self.reloadBibles)

    def _decodeQtObject(self, listobj, key):
        obj = listobj[QtCore.QString(key)]
        if isinstance(obj, QtCore.QVariant):
            obj = obj.toPyObject()
        return unicode(obj)

    def initPluginNameVisible(self):
        self.PluginNameVisible = self.trUtf8('Bible')

    def requiredIcons(self):
        MediaManagerItem.requiredIcons(self)
        self.hasEditIcon = False
        self.hasDeleteIcon = False

    def addEndHeaderBar(self):
        self.SearchTabWidget = QtGui.QTabWidget(self)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.SearchTabWidget.sizePolicy().hasHeightForWidth())
        self.SearchTabWidget.setSizePolicy(sizePolicy)
        self.SearchTabWidget.setObjectName(u'SearchTabWidget')
        # Add the Quick Search tab
        self.QuickTab = QtGui.QWidget()
        self.QuickTab.setObjectName(u'QuickTab')
        self.QuickLayout = QtGui.QGridLayout(self.QuickTab)
        self.QuickLayout.setMargin(2)
        self.QuickLayout.setSpacing(4)
        self.QuickLayout.setVerticalSpacing(4)
        self.QuickLayout.setObjectName(u'QuickLayout')
        self.QuickVersionLabel = QtGui.QLabel(self.QuickTab)
        self.QuickVersionLabel.setObjectName(u'QuickVersionLabel')
        self.QuickLayout.addWidget(self.QuickVersionLabel, 0, 0, 1, 1)
        self.QuickVersionComboBox = QtGui.QComboBox(self.QuickTab)
        self.QuickVersionComboBox.setSizeAdjustPolicy(
            QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.QuickVersionComboBox.setObjectName(u'VersionComboBox')
        self.QuickLayout.addWidget(self.QuickVersionComboBox, 0, 1, 1, 2)
        self.QuickSecondVersionLabel = QtGui.QLabel(self.QuickTab)
        self.QuickSecondVersionLabel.setObjectName(u'QuickSecondVersionLabel')
        self.QuickLayout.addWidget(self.QuickSecondVersionLabel, 1, 0, 1, 1)
        self.QuickSecondBibleComboBox = QtGui.QComboBox(self.QuickTab)
        self.QuickSecondBibleComboBox.setSizeAdjustPolicy(
            QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.QuickSecondBibleComboBox.setObjectName(u'SecondBible')
        self.QuickLayout.addWidget(self.QuickSecondBibleComboBox, 1, 1, 1, 2)
        self.QuickSearchLabel = QtGui.QLabel(self.QuickTab)
        self.QuickSearchLabel.setObjectName(u'QuickSearchLabel')
        self.QuickLayout.addWidget(self.QuickSearchLabel, 2, 0, 1, 1)
        self.QuickSearchComboBox = QtGui.QComboBox(self.QuickTab)
        self.QuickSearchComboBox.setObjectName(u'SearchComboBox')
        self.QuickLayout.addWidget(self.QuickSearchComboBox, 2, 1, 1, 2)
        self.QuickSearchLabel = QtGui.QLabel(self.QuickTab)
        self.QuickSearchLabel.setObjectName(u'QuickSearchLabel')
        self.QuickLayout.addWidget(self.QuickSearchLabel, 3, 0, 1, 1)
        self.QuickSearchEdit = QtGui.QLineEdit(self.QuickTab)
        self.QuickSearchEdit.setObjectName(u'QuickSearchEdit')
        self.QuickLayout.addWidget(self.QuickSearchEdit, 3, 1, 1, 2)
        self.QuickClearLabel = QtGui.QLabel(self.QuickTab)
        self.QuickClearLabel.setObjectName(u'QuickSearchLabel')
        self.QuickLayout.addWidget(self.QuickClearLabel, 4, 0, 1, 1)
        self.ClearQuickSearchComboBox = QtGui.QComboBox(self.QuickTab)
        self.ClearQuickSearchComboBox.setObjectName(u'ClearQuickSearchComboBox')
        self.QuickLayout.addWidget(self.ClearQuickSearchComboBox, 4, 1, 1, 2)
        self.QuickSearchButtonLayout = QtGui.QHBoxLayout()
        self.QuickSearchButtonLayout.setMargin(0)
        self.QuickSearchButtonLayout.setSpacing(0)
        self.QuickSearchButtonLayout.setObjectName(u'QuickSearchButtonLayout')
        self.QuickSearchButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.QuickSearchButtonLayout.addItem(self.QuickSearchButtonSpacer)
        self.QuickSearchButton = QtGui.QPushButton(self.QuickTab)
        self.QuickSearchButton.setObjectName(u'QuickSearchButton')
        self.QuickSearchButtonLayout.addWidget(self.QuickSearchButton)
        self.QuickLayout.addLayout(self.QuickSearchButtonLayout, 5, 0, 1, 3)
        self.QuickMessage = QtGui.QLabel(self.QuickTab)
        self.QuickMessage.setObjectName(u'QuickMessage')
        self.QuickLayout.addWidget(self.QuickMessage, 6, 0, 1, 3)
        self.SearchTabWidget.addTab(self.QuickTab, self.trUtf8('Quick'))
        QuickSpacerItem = QtGui.QSpacerItem(20, 35, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.QuickLayout.addItem(QuickSpacerItem, 6, 2, 1, 1)
        # Add the Advanced Search tab
        self.AdvancedTab = QtGui.QWidget()
        self.AdvancedTab.setObjectName(u'AdvancedTab')
        self.AdvancedLayout = QtGui.QGridLayout(self.AdvancedTab)
        self.AdvancedLayout.setMargin(2)
        self.AdvancedLayout.setSpacing(4)
        self.AdvancedLayout.setVerticalSpacing(4)
        self.AdvancedLayout.setObjectName(u'AdvancedLayout')
        self.AdvancedVersionLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedVersionLabel.setObjectName(u'AdvancedVersionLabel')
        self.AdvancedLayout.addWidget(self.AdvancedVersionLabel, 0, 0, 1, 1)
        self.AdvancedVersionComboBox = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedVersionComboBox.setSizeAdjustPolicy(
            QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.AdvancedVersionComboBox.setObjectName(u'AdvancedVersionComboBox')
        self.AdvancedLayout.addWidget(self.AdvancedVersionComboBox, 0, 1, 1, 2)
        self.AdvancedSecondBibleLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedSecondBibleLabel.setObjectName(u'AdvancedSecondBibleLabel')
        self.AdvancedLayout.addWidget(self.AdvancedSecondBibleLabel, 1, 0, 1, 1)
        self.AdvancedSecondBibleComboBox = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedSecondBibleComboBox.setSizeAdjustPolicy(
            QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.AdvancedSecondBibleComboBox.setObjectName(
            u'AdvancedSecondBibleComboBox')
        self.AdvancedLayout.addWidget(
            self.AdvancedSecondBibleComboBox, 1, 1, 1, 2)
        self.AdvancedBookLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedBookLabel.setObjectName(u'AdvancedBookLabel')
        self.AdvancedLayout.addWidget(self.AdvancedBookLabel, 2, 0, 1, 1)
        self.AdvancedBookComboBox = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedBookComboBox.setObjectName(u'AdvancedBookComboBox')
        self.AdvancedLayout.addWidget(self.AdvancedBookComboBox, 2, 1, 1, 2)
        self.AdvancedChapterLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedChapterLabel.setObjectName(u'AdvancedChapterLabel')
        self.AdvancedLayout.addWidget(self.AdvancedChapterLabel, 3, 1, 1, 1)
        self.AdvancedVerseLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedVerseLabel.setObjectName(u'AdvancedVerseLabel')
        self.AdvancedLayout.addWidget(self.AdvancedVerseLabel, 3, 2, 1, 1)
        self.AdvancedFromLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedFromLabel.setObjectName(u'AdvancedFromLabel')
        self.AdvancedLayout.addWidget(self.AdvancedFromLabel, 4, 0, 1, 1)
        self.AdvancedFromChapter = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedFromChapter.setObjectName(u'AdvancedFromChapter')
        self.AdvancedLayout.addWidget(self.AdvancedFromChapter, 4, 1, 1, 1)
        self.AdvancedFromVerse = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedFromVerse.setObjectName(u'AdvancedFromVerse')
        self.AdvancedLayout.addWidget(self.AdvancedFromVerse, 4, 2, 1, 1)
        self.AdvancedToLabel = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedToLabel.setObjectName(u'AdvancedToLabel')
        self.AdvancedLayout.addWidget(self.AdvancedToLabel, 5, 0, 1, 1)
        self.AdvancedToChapter = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedToChapter.setObjectName(u'AdvancedToChapter')
        self.AdvancedLayout.addWidget(self.AdvancedToChapter, 5, 1, 1, 1)
        self.AdvancedToVerse = QtGui.QComboBox(self.AdvancedTab)
        self.AdvancedToVerse.setObjectName(u'AdvancedToVerse')
        self.AdvancedLayout.addWidget(self.AdvancedToVerse, 5, 2, 1, 1)
        self.AdvancedClearLabel = QtGui.QLabel(self.QuickTab)
        self.AdvancedClearLabel.setObjectName(u'QuickSearchLabel')
        self.AdvancedLayout.addWidget(self.AdvancedClearLabel, 6, 0, 1, 1)
        self.ClearAdvancedSearchComboBox = QtGui.QComboBox(self.QuickTab)
        self.ClearAdvancedSearchComboBox.setObjectName(
            u'ClearAdvancedSearchComboBox')
        self.AdvancedLayout.addWidget(
            self.ClearAdvancedSearchComboBox, 6, 1, 1, 2)
        self.AdvancedSearchButtonLayout = QtGui.QHBoxLayout()
        self.AdvancedSearchButtonLayout.setMargin(0)
        self.AdvancedSearchButtonLayout.setSpacing(0)
        self.AdvancedSearchButtonLayout.setObjectName(
            u'AdvancedSearchButtonLayout')
        self.AdvancedSearchButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.AdvancedSearchButtonLayout.addItem(self.AdvancedSearchButtonSpacer)
        self.AdvancedSearchButton = QtGui.QPushButton(self.AdvancedTab)
        self.AdvancedSearchButton.setObjectName(u'AdvancedSearchButton')
        self.AdvancedSearchButtonLayout.addWidget(self.AdvancedSearchButton)
        self.AdvancedLayout.addLayout(
            self.AdvancedSearchButtonLayout, 7, 0, 1, 3)
        self.AdvancedMessage = QtGui.QLabel(self.AdvancedTab)
        self.AdvancedMessage.setObjectName(u'AdvancedMessage')
        self.AdvancedLayout.addWidget(self.AdvancedMessage, 8, 0, 1, 3)
        self.SearchTabWidget.addTab(self.AdvancedTab, self.trUtf8('Advanced'))
        # Add the search tab widget to the page layout
        self.PageLayout.addWidget(self.SearchTabWidget)
        # Combo Boxes
        QtCore.QObject.connect(self.AdvancedVersionComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onAdvancedVersionComboBox)
        QtCore.QObject.connect(self.AdvancedBookComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onAdvancedBookComboBox)
        QtCore.QObject.connect(self.AdvancedFromChapter,
            QtCore.SIGNAL(u'activated(int)'), self.onAdvancedFromChapter)
        QtCore.QObject.connect(self.AdvancedFromVerse,
            QtCore.SIGNAL(u'activated(int)'), self.onAdvancedFromVerse)
        QtCore.QObject.connect(self.AdvancedToChapter,
            QtCore.SIGNAL(u'activated(int)'), self.onAdvancedToChapter)
        # Buttons
        QtCore.QObject.connect(self.AdvancedSearchButton,
            QtCore.SIGNAL(u'pressed()'), self.onAdvancedSearchButton)
        QtCore.QObject.connect(self.QuickSearchButton,
            QtCore.SIGNAL(u'pressed()'), self.onQuickSearchButton)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_updated'), self.configUpdated)
        # Other stuff
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'bible_showprogress'), self.onSearchProgressShow)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'bible_hideprogress'), self.onSearchProgressHide)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'bible_nobook'), self.onNoBookFound)

    def addListViewToToolBar(self):
        MediaManagerItem.addListViewToToolBar(self)
        # Progress Bar
        self.SearchProgress = QtGui.QProgressBar(self)
        self.SearchProgress.setFormat('%p%')
        self.SearchProgress.setMaximum(3)
        self.SearchProgress.setGeometry(self.ListView.geometry().left(),
            self.ListView.geometry().top(), 81, 23)
        self.SearchProgress.setVisible(False)
        self.SearchProgress.setObjectName(u'SearchProgress')

    def configUpdated(self):
        if str_to_bool(
            self.parent.config.get_config(u'dual bibles', u'False')):
            self.AdvancedSecondBibleLabel.setVisible(True)
            self.AdvancedSecondBibleComboBox.setVisible(True)
            self.QuickSecondVersionLabel.setVisible(True)
            self.QuickSecondBibleComboBox.setVisible(True)
        else:
            self.AdvancedSecondBibleLabel.setVisible(False)
            self.AdvancedSecondBibleComboBox.setVisible(False)
            self.QuickSecondVersionLabel.setVisible(False)
            self.QuickSecondBibleComboBox.setVisible(False)

    def retranslateUi(self):
        log.debug(u'retranslateUi')
        self.QuickVersionLabel.setText(self.trUtf8('Version:'))
        self.QuickSecondVersionLabel.setText(self.trUtf8('Dual:'))
        self.QuickSearchLabel.setText(self.trUtf8('Search Type:'))
        self.QuickSearchLabel.setText(self.trUtf8('Find:'))
        self.QuickSearchButton.setText(self.trUtf8('Search'))
        self.QuickClearLabel.setText(self.trUtf8('Results:'))
        self.AdvancedVersionLabel.setText(self.trUtf8('Version:'))
        self.AdvancedSecondBibleLabel.setText(self.trUtf8('Dual:'))
        self.AdvancedBookLabel.setText(self.trUtf8('Book:'))
        self.AdvancedChapterLabel.setText(self.trUtf8('Chapter:'))
        self.AdvancedVerseLabel.setText(self.trUtf8('Verse:'))
        self.AdvancedFromLabel.setText(self.trUtf8('From:'))
        self.AdvancedToLabel.setText(self.trUtf8('To:'))
        self.AdvancedClearLabel.setText(self.trUtf8('Results:'))
        self.AdvancedSearchButton.setText(self.trUtf8('Search'))
        self.QuickSearchComboBox.addItem(self.trUtf8('Verse Search'))
        self.QuickSearchComboBox.addItem(self.trUtf8('Text Search'))
        self.ClearQuickSearchComboBox.addItem(self.trUtf8('Clear'))
        self.ClearQuickSearchComboBox.addItem(self.trUtf8('Keep'))
        self.ClearAdvancedSearchComboBox.addItem(self.trUtf8('Clear'))
        self.ClearAdvancedSearchComboBox.addItem(self.trUtf8('Keep'))

    def initialise(self):
        log.debug(u'bible manager initialise')
        self.parent.manager.media = self
        self.loadBibles()
        self.configUpdated()
        log.debug(u'bible manager initialise complete')

    def setQuickMessage(self, text):
        self.QuickMessage.setText(text)
        self.AdvancedMessage.setText(text)
        Receiver.send_message(u'process_events')
        #minor delay to get the events processed
        time.sleep(0.1)

    def loadBibles(self):
        log.debug(u'Loading Bibles')
        self.QuickVersionComboBox.clear()
        self.QuickSecondBibleComboBox.clear()
        self.AdvancedVersionComboBox.clear()
        self.AdvancedSecondBibleComboBox.clear()
        self.QuickSecondBibleComboBox.addItem(u'')
        self.AdvancedSecondBibleComboBox.addItem(u'')
        bibles = self.parent.manager.get_bibles()
        # load bibles into the combo boxes
        first = True
        for bible in bibles:
            self.QuickVersionComboBox.addItem(bible)
            self.QuickSecondBibleComboBox.addItem(bible)
            self.AdvancedVersionComboBox.addItem(bible)
            self.AdvancedSecondBibleComboBox.addItem(bible)
            if first:
                first = False
                self.initialiseBible(bible)

    def onListViewResize(self, width, height):
        self.SearchProgress.setGeometry(self.ListView.geometry().x(),
            (self.ListView.geometry().y() + self.ListView.geometry().height())\
                - 23, 81, 23)

    def onSearchProgressShow(self):
        self.SearchProgress.setVisible(True)
        self.SearchProgress.setMinimum(0)
        self.SearchProgress.setMaximum(2)
        self.SearchProgress.setValue(1)

    def onSearchProgressHide(self):
        self.SearchProgress.setVisible(False)

    def onNoBookFound(self):
        QtGui.QMessageBox.critical(self,
            self.trUtf8('No Book Found'),
            self.trUtf8('No matching book could be found in this Bible.'),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok),
            QtGui.QMessageBox.Ok
        )

    def onAdvancedVersionComboBox(self):
        self.initialiseBible(
            unicode(self.AdvancedVersionComboBox.currentText()))

    def onAdvancedBookComboBox(self):
        item = int(self.AdvancedBookComboBox.currentIndex())
        self.initialiseChapterVerse(
            unicode(self.AdvancedVersionComboBox.currentText()),
            unicode(self.AdvancedBookComboBox.currentText()),
            self.AdvancedBookComboBox.itemData(item).toInt()[0])

    def onNewClick(self):
        self.bibleimportform = ImportWizardForm(self, self.parent.config,
            self.parent.manager, self.parent)
        self.bibleimportform.exec_()
        self.reloadBibles()

    def onAdvancedFromVerse(self):
        frm = self.AdvancedFromVerse.currentText()
        self.adjustComboBox(frm, self.verses, self.AdvancedToVerse)

    def onAdvancedToChapter(self):
        frm = unicode(self.AdvancedFromChapter.currentText())
        to = unicode(self.AdvancedToChapter.currentText())
        if frm != to:
            bible = unicode(self.AdvancedVersionComboBox.currentText())
            book = unicode(self.AdvancedBookComboBox.currentText())
            # get the verse count for new chapter
            verses = self.parent.manager.get_verse_count(bible, book, int(to))
            self.adjustComboBox(1, verses, self.AdvancedToVerse)

    def onAdvancedSearchButton(self):
        log.debug(u'Advanced Search Button pressed')
        bible = unicode(self.AdvancedVersionComboBox.currentText())
        book = unicode(self.AdvancedBookComboBox.currentText())
        chapter_from = int(self.AdvancedFromChapter.currentText())
        chapter_to = int(self.AdvancedToChapter.currentText())
        verse_from = int(self.AdvancedFromVerse.currentText())
        verse_to = int(self.AdvancedToVerse.currentText())
        versetext = u'%s %s:%s-%s:%s' % (book, chapter_from, verse_from, \
                                         chapter_to, verse_to)
        self.search_results = self.parent.manager.get_verses(bible, versetext)
        if self.ClearAdvancedSearchComboBox.currentIndex() == 0:
            self.ListView.clear()
            self.lastReference = []
        self.lastReference.append(versetext)
        self.displayResults(bible)

    def onAdvancedFromChapter(self):
        bible = unicode(self.AdvancedVersionComboBox.currentText())
        book = unicode(self.AdvancedBookComboBox.currentText())
        cf = int(self.AdvancedFromChapter.currentText())
        self.adjustComboBox(cf, self.chapters_from, self.AdvancedToChapter)
        # get the verse count for new chapter
        vse = self.parent.manager.get_verse_count(bible, book, cf)
        self.adjustComboBox(1, vse, self.AdvancedFromVerse)
        self.adjustComboBox(1, vse, self.AdvancedToVerse)

    def onQuickSearchButton(self):
        log.debug(u'Quick Search Button pressed')
        bible = unicode(self.QuickVersionComboBox.currentText())
        text = unicode(self.QuickSearchEdit.displayText())
        if self.ClearQuickSearchComboBox.currentIndex() == 0:
            self.ListView.clear()
            self.lastReference = []
        self.lastReference.append(text)
        self.search_results = self.parent.manager.get_verses(bible, text)
        if self.search_results:
            self.displayResults(bible)

    def generateSlideData(self, service_item):
        log.debug(u'generating slide data')
        items = self.ListView.selectedIndexes()
        if len(items) == 0:
            return False
        old_chapter = u''
        raw_slides = []
        raw_footer = []
        bible_text = u''
        service_item.autoPreviewAllowed = True
        #If we want to use a 2nd translation / version
        bible2 = u''
        if self.SearchTabWidget.currentIndex() == 0:
            bible2 = unicode(self.QuickSecondBibleComboBox.currentText())
        else:
            bible2 = unicode(self.AdvancedSecondBibleComboBox.currentText())
        if bible2:
            bible2_verses = []
            for scripture in self.lastReference:
                bible2_verses.extend(self.parent.manager.get_verses(bible2, scripture))
            bible2_version = self.parent.manager.get_meta_data(bible2, u'Version')
            bible2_copyright = self.parent.manager.get_meta_data(bible2, u'Copyright')
            bible2_permission = self.parent.manager.get_meta_data(bible2, u'Permission')
        # Let's loop through the main lot, and assemble our verses
        for item in items:
            bitem = self.ListView.item(item.row())
            reference = bitem.data(QtCore.Qt.UserRole)
            if isinstance(reference, QtCore.QVariant):
                reference = reference.toPyObject()
            bible = self._decodeQtObject(reference, 'bible')
            book = self._decodeQtObject(reference, 'book')
            chapter = self._decodeQtObject(reference, 'chapter')
            verse = self._decodeQtObject(reference, 'verse')
            text = self._decodeQtObject(reference, 'text')
            version = self._decodeQtObject(reference, 'version')
            copyright = self._decodeQtObject(reference, 'copyright')
            permission = self._decodeQtObject(reference, 'permission')
            if self.parent.settings_tab.display_style == 1:
                verse_text = self.formatVerse(old_chapter, chapter, verse, u'(u', u')')
            elif  self.parent.settings_tab.display_style == 2:
                verse_text = self.formatVerse(old_chapter, chapter, verse, u'{', u'}')
            elif  self.parent.settings_tab.display_style == 3:
                verse_text = self.formatVerse(old_chapter, chapter, verse, u'[', u']')
            else:
                verse_text = self.formatVerse(old_chapter, chapter, verse, u'', u'')
            old_chapter = chapter
            footer = u'%s (%s %s)' % (book, version, copyright)
            #If not found add to footer
            if footer not in raw_footer:
                raw_footer.append(footer)
            if bible2:
                footer = u'%s (%s %s)' % (book, version, copyright)
                #If not found add to footer
                if footer not in raw_footer:
                    raw_footer.append(footer)
                bible_text = u'%s %s \n\n %s %s' % \
                    (verse_text, text, verse_text, bible2_verses[item.row()].text)
                raw_slides.append(bible_text)
                bible_text = u''
            else:
                #Paragraph style force new line per verse
                if self.parent.settings_tab.layout_style == 1:
                    text = text + u'\n\n'
                bible_text = u'%s %s %s' % (bible_text, verse_text, text)
                #if we are verse per slide then create slide
                if self.parent.settings_tab.layout_style == 0:
                    raw_slides.append(bible_text)
                    bible_text = u''
            service_item.title = u'%s %s' % (book, verse_text)
        if  len(self.parent.settings_tab.bible_theme) == 0:
            service_item.theme = None
        else:
            service_item.theme = self.parent.settings_tab.bible_theme
        #if we are verse per slide we have already been added
        if self.parent.settings_tab.layout_style != 0:
            raw_slides.append(bible_text)
        for slide in raw_slides:
            service_item.add_from_text(slide[:30], slide)
        service_item.raw_footer = raw_footer
        return True

    def formatVerse(self, old_chapter, chapter, verse, opening, closing):
        verse_text = opening
        if old_chapter != chapter:
            verse_text += chapter + u':'
        elif not self.parent.settings_tab.show_new_chapters:
            verse_text += chapter + u':'
        verse_text += verse
        verse_text += closing
        return verse_text

    def reloadBibles(self):
        log.debug(u'Reloading Bibles')
        self.parent.manager.reload_bibles()
        self.loadBibles()

    def initialiseBible(self, bible):
        log.debug(u'initialiseBible %s', bible)
        book_data = self.parent.manager.get_books(bible)
        self.AdvancedBookComboBox.clear()
        first = True
        for book in book_data:
            row = self.AdvancedBookComboBox.count()
            self.AdvancedBookComboBox.addItem(book[u'name'])
            self.AdvancedBookComboBox.setItemData(
                row, QtCore.QVariant(book[u'chapters']))
            if first:
                first = False
                self.initialiseChapterVerse(
                    bible, book[u'name'], book[u'chapters'])

    def initialiseChapterVerse(self, bible, book, chapters):
        log.debug(u'initialiseChapterVerse %s, %s', bible, book)
        self.chapters_from = chapters
        self.verses = self.parent.manager.get_verse_count(bible, book, 1)
        if self.verses == 0:
            self.AdvancedSearchButton.setEnabled(False)
            self.AdvancedMessage.setText(self.trUtf8('Bible not fully loaded'))
        else:
            self.AdvancedSearchButton.setEnabled(True)
            self.AdvancedMessage.setText(u'')
            self.adjustComboBox(1, self.chapters_from, self.AdvancedFromChapter)
            self.adjustComboBox(1, self.chapters_from, self.AdvancedToChapter)
            self.adjustComboBox(1, self.verses, self.AdvancedFromVerse)
            self.adjustComboBox(1, self.verses, self.AdvancedToVerse)

    def adjustComboBox(self, range_from, range_to, combo):
        log.debug(u'adjustComboBox %s, %s, %s', combo, range_from, range_to)
        combo.clear()
        for i in range(int(range_from), int(range_to) + 1):
            combo.addItem(unicode(i))

    def displayResults(self, bible):
        version = self.parent.manager.get_meta_data(bible, u'Version')
        copyright = self.parent.manager.get_meta_data(bible, u'Copyright')
        permission = self.parent.manager.get_meta_data(bible, u'Permission')
        if not permission:
            permission = u''
        else:
            permission = permission.value
        for count, verse in enumerate(self.search_results):
            bible_text = u' %s %d:%d (%s)' % \
                (verse.book.name, verse.chapter, verse.verse, bible)
            bible_verse = QtGui.QListWidgetItem(bible_text)
            #bible_verse.setData(QtCore.Qt.UserRole,
            #    QtCore.QVariant(bible_text))
            vdict = {
                'bible': QtCore.QVariant(bible),
                'version': QtCore.QVariant(version.value),
                'copyright': QtCore.QVariant(copyright.value),
                'permission': QtCore.QVariant(permission),
                'book': QtCore.QVariant(verse.book.name),
                'chapter': QtCore.QVariant(verse.chapter),
                'verse': QtCore.QVariant(verse.verse),
                'text': QtCore.QVariant(verse.text)
            }
            bible_verse.setData(QtCore.Qt.UserRole, QtCore.QVariant(vdict))
            self.ListView.addItem(bible_verse)
            row = self.ListView.setCurrentRow(count)
            if row:
                row.setSelected(True)

    def searchByReference(self, bible, search):
        log.debug(u'searchByReference %s, %s', bible, search)
        self.search_results = self.parent.manager.get_verses(bible, search)
