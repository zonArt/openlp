# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

from openlp.core.lib import MediaManagerItem, Receiver, ItemCapabilities, \
    translate
from openlp.core.lib.searchedit import SearchEdit
from openlp.core.lib.ui import UiStrings, add_widget_completer, \
    media_item_combo_box, critical_error_message_box, find_and_set_in_combo_box
from openlp.plugins.bibles.forms import BibleImportForm
from openlp.plugins.bibles.lib import LayoutStyle, DisplayStyle, \
    VerseReferenceList, get_reference_match

log = logging.getLogger(__name__)

class BibleSearch(object):
    """
    Enumeration class for the different search methods for the "quick search".
    """
    Reference = 1
    Text = 2


class BibleMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Bibles.
    """
    log.info(u'Bible Media Item loaded')

    def __init__(self, parent, plugin, icon):
        self.IconPath = u'songs/song'
        MediaManagerItem.__init__(self, parent, plugin, icon)
        # Place to store the search results for both bibles.
        self.settings = self.parent.settings_tab
        self.search_results = {}
        self.second_search_results = {}
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'bibles_load_list'), self.reloadBibles)

    def requiredIcons(self):
        MediaManagerItem.requiredIcons(self)
        self.hasImportIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False
        self.hasDeleteIcon = False
        self.addToServiceItem = False

    def addEndHeaderBar(self):
        self.searchTabWidget = QtGui.QTabWidget(self)
        self.searchTabWidget.setSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.searchTabWidget.setObjectName(u'SearchTabWidget')
        # Add the Quick Search tab.
        self.quickTab = QtGui.QWidget()
        self.quickTab.setObjectName(u'quickTab')
        self.quickLayout = QtGui.QFormLayout(self.quickTab)
        self.quickLayout.setObjectName(u'quickLayout')
        self.quickVersionLabel = QtGui.QLabel(self.quickTab)
        self.quickVersionLabel.setObjectName(u'quickVersionLabel')
        self.quickVersionComboBox = media_item_combo_box(self.quickTab,
            u'quickVersionComboBox')
        self.quickVersionLabel.setBuddy(self.quickVersionComboBox)
        self.quickLayout.addRow(self.quickVersionLabel,
            self.quickVersionComboBox)
        self.quickSecondLabel = QtGui.QLabel(self.quickTab)
        self.quickSecondLabel.setObjectName(u'quickSecondLabel')
        self.quickSecondComboBox = media_item_combo_box(self.quickTab,
            u'quickSecondComboBox')
        self.quickSecondLabel.setBuddy(self.quickSecondComboBox)
        self.quickLayout.addRow(self.quickSecondLabel, self.quickSecondComboBox)
        self.quickSearchLabel = QtGui.QLabel(self.quickTab)
        self.quickSearchLabel.setObjectName(u'quickSearchLabel')
        self.quickSearchEdit = SearchEdit(self.quickTab)
        self.quickSearchEdit.setObjectName(u'quickSearchEdit')
        self.quickSearchLabel.setBuddy(self.quickSearchEdit)
        self.quickSearchEdit.setSearchTypes([
            (BibleSearch.Reference, u':/bibles/bibles_search_reference.png',
            translate('BiblesPlugin.MediaItem', 'Scripture Reference')),
            (BibleSearch.Text, u':/bibles/bibles_search_text.png',
            translate('BiblesPlugin.MediaItem', 'Text Search'))
        ])
        self.quickLayout.addRow(self.quickSearchLabel, self.quickSearchEdit)
        self.quickLayoutLabel = QtGui.QLabel(self.quickTab)
        self.quickLayoutLabel.setObjectName(u'quickClearLabel')
        self.quickLayoutComboBox = media_item_combo_box(self.quickTab,
            u'quickLayoutComboBox')
        self.quickLayoutComboBox.addItems([u'', u'', u''])
        self.quickLayout.addRow(self.quickLayoutLabel, self.quickLayoutComboBox)
        self.quickClearLabel = QtGui.QLabel(self.quickTab)
        self.quickClearLabel.setObjectName(u'quickClearLabel')
        self.quickClearComboBox = media_item_combo_box(self.quickTab,
            u'quickClearComboBox')
        self.quickLayout.addRow(self.quickClearLabel, self.quickClearComboBox)
        self.quickSearchButtonLayout = QtGui.QHBoxLayout()
        self.quickSearchButtonLayout.setObjectName(u'quickSearchButtonLayout')
        self.quickSearchButtonLayout.addStretch()
        self.quickSearchButton = QtGui.QPushButton(self.quickTab)
        self.quickSearchButton.setObjectName(u'quickSearchButton')
        self.quickSearchButtonLayout.addWidget(self.quickSearchButton)
        self.quickLayout.addRow(self.quickSearchButtonLayout)
        self.searchTabWidget.addTab(self.quickTab,
            translate('BiblesPlugin.MediaItem', 'Quick'))
        # Add the Advanced Search tab.
        self.advancedTab = QtGui.QWidget()
        self.advancedTab.setObjectName(u'advancedTab')
        self.advancedLayout = QtGui.QGridLayout(self.advancedTab)
        self.advancedLayout.setObjectName(u'advancedLayout')
        self.advancedVersionLabel = QtGui.QLabel(self.advancedTab)
        self.advancedVersionLabel.setObjectName(u'advancedVersionLabel')
        self.advancedLayout.addWidget(self.advancedVersionLabel, 0, 0,
            QtCore.Qt.AlignRight)
        self.advancedVersionComboBox = media_item_combo_box(self.advancedTab,
            u'advancedVersionComboBox')
        self.advancedVersionLabel.setBuddy(self.advancedVersionComboBox)
        self.advancedLayout.addWidget(self.advancedVersionComboBox, 0, 1, 1, 2)
        self.advancedSecondLabel = QtGui.QLabel(self.advancedTab)
        self.advancedSecondLabel.setObjectName(u'advancedSecondLabel')
        self.advancedLayout.addWidget(self.advancedSecondLabel, 1, 0,
            QtCore.Qt.AlignRight)
        self.advancedSecondComboBox = media_item_combo_box(self.advancedTab,
            u'advancedSecondComboBox')
        self.advancedSecondLabel.setBuddy(self.advancedSecondComboBox)
        self.advancedLayout.addWidget(self.advancedSecondComboBox, 1, 1, 1, 2)
        self.advancedBookLabel = QtGui.QLabel(self.advancedTab)
        self.advancedBookLabel.setObjectName(u'advancedBookLabel')
        self.advancedLayout.addWidget(self.advancedBookLabel, 2, 0,
            QtCore.Qt.AlignRight)
        self.advancedBookComboBox = media_item_combo_box(self.advancedTab,
            u'advancedBookComboBox')
        self.advancedBookLabel.setBuddy(self.advancedBookComboBox)
        self.advancedLayout.addWidget(self.advancedBookComboBox, 2, 1, 1, 2)
        self.advancedChapterLabel = QtGui.QLabel(self.advancedTab)
        self.advancedChapterLabel.setObjectName(u'advancedChapterLabel')
        self.advancedLayout.addWidget(self.advancedChapterLabel, 3, 1)
        self.advancedVerseLabel = QtGui.QLabel(self.advancedTab)
        self.advancedVerseLabel.setObjectName(u'advancedVerseLabel')
        self.advancedLayout.addWidget(self.advancedVerseLabel, 3, 2)
        self.advancedFromLabel = QtGui.QLabel(self.advancedTab)
        self.advancedFromLabel.setObjectName(u'advancedFromLabel')
        self.advancedLayout.addWidget(self.advancedFromLabel, 4, 0,
            QtCore.Qt.AlignRight)
        self.advancedFromChapter = QtGui.QComboBox(self.advancedTab)
        self.advancedFromChapter.setObjectName(u'advancedFromChapter')
        self.advancedLayout.addWidget(self.advancedFromChapter, 4, 1)
        self.advancedFromVerse = QtGui.QComboBox(self.advancedTab)
        self.advancedFromVerse.setObjectName(u'advancedFromVerse')
        self.advancedLayout.addWidget(self.advancedFromVerse, 4, 2)
        self.advancedToLabel = QtGui.QLabel(self.advancedTab)
        self.advancedToLabel.setObjectName(u'advancedToLabel')
        self.advancedLayout.addWidget(self.advancedToLabel, 5, 0,
            QtCore.Qt.AlignRight)
        self.advancedToChapter = QtGui.QComboBox(self.advancedTab)
        self.advancedToChapter.setObjectName(u'advancedToChapter')
        self.advancedLayout.addWidget(self.advancedToChapter, 5, 1)
        self.advancedToVerse = QtGui.QComboBox(self.advancedTab)
        self.advancedToVerse.setObjectName(u'advancedToVerse')
        self.advancedLayout.addWidget(self.advancedToVerse, 5, 2)
        self.advancedClearLabel = QtGui.QLabel(self.quickTab)
        self.advancedClearLabel.setObjectName(u'advancedClearLabel')
        self.advancedLayout.addWidget(self.advancedClearLabel, 6, 0,
            QtCore.Qt.AlignRight)
        self.advancedClearComboBox = media_item_combo_box(self.quickTab,
            u'advancedClearComboBox')
        self.advancedClearLabel.setBuddy(self.advancedClearComboBox)
        self.advancedLayout.addWidget(self.advancedClearComboBox, 6, 1, 1, 2)
        self.advancedSearchButtonLayout = QtGui.QHBoxLayout()
        self.advancedSearchButtonLayout.setObjectName(
            u'advancedSearchButtonLayout')
        self.advancedSearchButtonLayout.addStretch()
        self.advancedSearchButton = QtGui.QPushButton(self.advancedTab)
        self.advancedSearchButton.setObjectName(u'advancedSearchButton')
        self.advancedSearchButtonLayout.addWidget(self.advancedSearchButton)
        self.advancedLayout.addLayout(
            self.advancedSearchButtonLayout, 7, 0, 1, 3)
        self.searchTabWidget.addTab(self.advancedTab, UiStrings.Advanced)
        # Add the search tab widget to the page layout.
        self.pageLayout.addWidget(self.searchTabWidget)
        # Combo Boxes
        QtCore.QObject.connect(self.advancedVersionComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onAdvancedVersionComboBox)
        QtCore.QObject.connect(self.advancedBookComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onAdvancedBookComboBox)
        QtCore.QObject.connect(self.advancedFromChapter,
            QtCore.SIGNAL(u'activated(int)'), self.onAdvancedFromChapter)
        QtCore.QObject.connect(self.advancedFromVerse,
            QtCore.SIGNAL(u'activated(int)'), self.onAdvancedFromVerse)
        QtCore.QObject.connect(self.advancedToChapter,
            QtCore.SIGNAL(u'activated(int)'), self.onAdvancedToChapter)
        QtCore.QObject.connect(self.quickSearchEdit,
            QtCore.SIGNAL(u'searchTypeChanged(int)'), self.updateAutoCompleter)
        QtCore.QObject.connect(self.quickVersionComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.updateAutoCompleter)
        QtCore.QObject.connect(
            self.quickLayoutComboBox, QtCore.SIGNAL(u'activated(int)'),
            self.onlayoutStyleComboBoxChanged)
        # Buttons
        QtCore.QObject.connect(self.advancedSearchButton,
            QtCore.SIGNAL(u'pressed()'), self.onAdvancedSearchButton)
        QtCore.QObject.connect(self.quickSearchButton,
            QtCore.SIGNAL(u'pressed()'), self.onQuickSearchButton)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_updated'), self.configUpdated)
        # Other stuff
        QtCore.QObject.connect(self.quickSearchEdit,
            QtCore.SIGNAL(u'returnPressed()'), self.onQuickSearchButton)

    def configUpdated(self):
        log.debug(u'configUpdated')
        if QtCore.QSettings().value(self.settingsSection + u'/second bibles',
            QtCore.QVariant(True)).toBool():
            self.advancedSecondLabel.setVisible(True)
            self.advancedSecondComboBox.setVisible(True)
            self.quickSecondLabel.setVisible(True)
            self.quickSecondComboBox.setVisible(True)
        else:
            self.advancedSecondLabel.setVisible(False)
            self.advancedSecondComboBox.setVisible(False)
            self.quickSecondLabel.setVisible(False)
            self.quickSecondComboBox.setVisible(False)
        self.quickLayoutComboBox.setCurrentIndex(self.settings.layout_style)

    def retranslateUi(self):
        log.debug(u'retranslateUi')
        self.quickVersionLabel.setText(u'%s:' % UiStrings.Version)
        self.quickSecondLabel.setText(
            translate('BiblesPlugin.MediaItem', 'Second:'))
        self.quickSearchLabel.setText(
            translate('BiblesPlugin.MediaItem', 'Find:'))
        self.quickSearchButton.setText(UiStrings.Search)
        self.quickClearLabel.setText(
            translate('BiblesPlugin.MediaItem', 'Results:'))
        self.advancedVersionLabel.setText(u'%s:' % UiStrings.Version)
        self.advancedSecondLabel.setText(
            translate('BiblesPlugin.MediaItem', 'Second:'))
        self.advancedBookLabel.setText(
            translate('BiblesPlugin.MediaItem', 'Book:'))
        self.advancedChapterLabel.setText(
            translate('BiblesPlugin.MediaItem', 'Chapter:'))
        self.advancedVerseLabel.setText(
            translate('BiblesPlugin.MediaItem', 'Verse:'))
        self.advancedFromLabel.setText(
            translate('BiblesPlugin.MediaItem', 'From:'))
        self.advancedToLabel.setText(
            translate('BiblesPlugin.MediaItem', 'To:'))
        self.advancedClearLabel.setText(
            translate('BiblesPlugin.MediaItem', 'Results:'))
        self.advancedSearchButton.setText(UiStrings.Search)
        self.quickClearComboBox.addItem(
            translate('BiblesPlugin.MediaItem', 'Clear'))
        self.quickClearComboBox.addItem(
            translate('BiblesPlugin.MediaItem', 'Keep'))
        self.advancedClearComboBox.addItem(
            translate('BiblesPlugin.MediaItem', 'Clear'))
        self.advancedClearComboBox.addItem(
            translate('BiblesPlugin.MediaItem', 'Keep'))
        self.quickLayoutLabel.setText(UiStrings.DisplayStyle)
        self.quickLayoutComboBox.setItemText(LayoutStyle.VersePerSlide,
            UiStrings.VersePerSlide)
        self.quickLayoutComboBox.setItemText(LayoutStyle.VersePerLine,
            UiStrings.VersePerLine)
        self.quickLayoutComboBox.setItemText(LayoutStyle.Continuous,
            UiStrings.Continuous)

    def initialise(self):
        log.debug(u'bible manager initialise')
        self.parent.manager.media = self
        self.loadBibles()
        bible = QtCore.QSettings().value(
            self.settingsSection + u'/quick bible', QtCore.QVariant(
            self.quickVersionComboBox.currentText())).toString()
        find_and_set_in_combo_box(self.quickVersionComboBox, bible)
        self.updateAutoCompleter()
        self.configUpdated()
        log.debug(u'bible manager initialise complete')

    def onImportClick(self):
        if not hasattr(self, u'import_wizard'):
            self.import_wizard = BibleImportForm(self, self.parent.manager,
                self.parent)
        # If the import was not cancelled then reload.
        if self.import_wizard.exec_():
            self.reloadBibles()

    def loadBibles(self):
        log.debug(u'Loading Bibles')
        self.quickVersionComboBox.clear()
        self.quickSecondComboBox.clear()
        self.advancedVersionComboBox.clear()
        self.advancedSecondComboBox.clear()
        self.quickSecondComboBox.addItem(u'')
        self.advancedSecondComboBox.addItem(u'')
        # Get all bibles and sort the list.
        bibles = self.parent.manager.get_bibles().keys()
        bibles.sort()
        # Load the bibles into the combo boxes.
        for bible in bibles:
            if bible:
                self.quickVersionComboBox.addItem(bible)
                self.quickSecondComboBox.addItem(bible)
                self.advancedVersionComboBox.addItem(bible)
                self.advancedSecondComboBox.addItem(bible)
        # set the default value
        bible = QtCore.QSettings().value(
            self.settingsSection + u'/advanced bible',
            QtCore.QVariant(u'')).toString()
        if bible in bibles:
            find_and_set_in_combo_box(self.advancedVersionComboBox, bible)
            self.initialiseAdvancedBible(unicode(bible))
        elif len(bibles):
            self.initialiseAdvancedBible(bibles[0])

    def reloadBibles(self):
        log.debug(u'Reloading Bibles')
        self.parent.manager.reload_bibles()
        self.loadBibles()

    def initialiseAdvancedBible(self, bible):
        """
        This initialises the given bible, which means that its book names and
        their chapter numbers is added to the combo boxes on the
        'Advanced Search' Tab. This is not of any importance of the
        'Quick Search' Tab.

        ``bible``
            The bible to initialise (unicode).
        """
        log.debug(u'initialiseAdvancedBible %s', bible)
        book_data = self.parent.manager.get_books(bible)
        self.advancedBookComboBox.clear()
        first = True
        for book in book_data:
            row = self.advancedBookComboBox.count()
            self.advancedBookComboBox.addItem(book[u'name'])
            self.advancedBookComboBox.setItemData(
                row, QtCore.QVariant(book[u'chapters']))
            if first:
                first = False
                self.initialiseChapterVerse(bible, book[u'name'],
                    book[u'chapters'])

    def initialiseChapterVerse(self, bible, book, chapter_count):
        log.debug(u'initialiseChapterVerse %s, %s', bible, book)
        self.chapter_count = chapter_count
        verse_count = self.parent.manager.get_verse_count(bible, book, 1)
        if verse_count == 0:
            self.advancedSearchButton.setEnabled(False)
            critical_error_message_box(
                message=translate('BiblePlugin.MediaItem',
                'Bible not fully loaded.'))
        else:
            self.advancedSearchButton.setEnabled(True)
            self.adjustComboBox(1, self.chapter_count, self.advancedFromChapter)
            self.adjustComboBox(1, self.chapter_count, self.advancedToChapter)
            self.adjustComboBox(1, verse_count, self.advancedFromVerse)
            self.adjustComboBox(1, verse_count, self.advancedToVerse)

    def updateAutoCompleter(self):
        """
        This updates the bible book completion list for the search field. The
        completion depends on the bible. It is only updated when we are doing a
        reference search, otherwise the auto completion list is removed.
        """
        QtCore.QSettings().setValue(self.settingsSection + u'/quick bible',
            QtCore.QVariant(self.quickVersionComboBox.currentText()))
        books = []
        # We have to do a 'Reference Search'.
        if self.quickSearchEdit.currentSearchType() == BibleSearch.Reference:
            bibles = self.parent.manager.get_bibles()
            bible = unicode(self.quickVersionComboBox.currentText())
            if bible:
                book_data = bibles[bible].get_books()
                books = [book.name + u' ' for book in book_data]
                books.sort()
        add_widget_completer(books, self.quickSearchEdit)

    def onAdvancedVersionComboBox(self):
        QtCore.QSettings().setValue(self.settingsSection + u'/advanced bible',
            QtCore.QVariant(self.advancedVersionComboBox.currentText()))
        self.initialiseAdvancedBible(
            unicode(self.advancedVersionComboBox.currentText()))

    def onAdvancedBookComboBox(self):
        item = int(self.advancedBookComboBox.currentIndex())
        self.initialiseChapterVerse(
            unicode(self.advancedVersionComboBox.currentText()),
            unicode(self.advancedBookComboBox.currentText()),
            self.advancedBookComboBox.itemData(item).toInt()[0])

    def onAdvancedFromVerse(self):
        chapter_from = int(self.advancedFromChapter.currentText())
        chapter_to = int(self.advancedToChapter.currentText())
        if chapter_from == chapter_to:
            bible = unicode(self.advancedVersionComboBox.currentText())
            book = unicode(self.advancedBookComboBox.currentText())
            verse_from = int(self.advancedFromVerse.currentText())
            verse_count = self.parent.manager.get_verse_count(bible, book,
                chapter_to)
            self.adjustComboBox(verse_from, verse_count,
                self.advancedToVerse, True)

    def onAdvancedToChapter(self):
        bible = unicode(self.advancedVersionComboBox.currentText())
        book = unicode(self.advancedBookComboBox.currentText())
        chapter_from = int(self.advancedFromChapter.currentText())
        chapter_to = int(self.advancedToChapter.currentText())
        verse_from = int(self.advancedFromVerse.currentText())
        verse_to = int(self.advancedToVerse.currentText())
        verse_count = self.parent.manager.get_verse_count(bible, book,
            chapter_to)
        if chapter_from == chapter_to and verse_from > verse_to:
            self.adjustComboBox(verse_from, verse_count, self.advancedToVerse)
        else:
            self.adjustComboBox(1, verse_count, self.advancedToVerse)

    def onAdvancedFromChapter(self):
        bible = unicode(self.advancedVersionComboBox.currentText())
        book = unicode(self.advancedBookComboBox.currentText())
        chapter_from = int(self.advancedFromChapter.currentText())
        chapter_to = int(self.advancedToChapter.currentText())
        verse_count = self.parent.manager.get_verse_count(bible, book,
            chapter_from)
        self.adjustComboBox(1, verse_count, self.advancedFromVerse)
        if chapter_from > chapter_to:
            self.adjustComboBox(1, verse_count, self.advancedToVerse)
            self.adjustComboBox(chapter_from, self.chapter_count,
                self.advancedToChapter)
        elif chapter_from == chapter_to:
            self.adjustComboBox(chapter_from, self.chapter_count,
                self.advancedToChapter)
            self.adjustComboBox(1, verse_count, self.advancedToVerse, True)
        else:
            self.adjustComboBox(chapter_from, self.chapter_count,
                self.advancedToChapter, True)

    def adjustComboBox(self, range_from, range_to, combo, restore=False):
        """
        Adjusts the given como box to the given values.

        ``range_from``
            The first number of the range (int).

        ``range_to``
            The last number of the range (int).

        ``combo``
            The combo box itself (QComboBox).

        ``restore``
            If True, then the combo's currentText will be restored after
            adjusting (if possible).
        """
        log.debug(u'adjustComboBox %s, %s, %s', combo, range_from, range_to)
        if restore:
            old_text = unicode(combo.currentText())
        combo.clear()
        combo.addItems([unicode(i) for i in range(range_from, range_to + 1)])
        if restore and combo.findText(old_text) != -1:
            combo.setCurrentIndex(combo.findText(old_text))

    def onAdvancedSearchButton(self):
        """
        Does an advanced search and saves the search results.
        """
        log.debug(u'Advanced Search Button pressed')
        self.advancedSearchButton.setEnabled(False)
        Receiver.send_message(u'openlp_process_events')
        bible = unicode(self.advancedVersionComboBox.currentText())
        second_bible = unicode(self.advancedSecondComboBox.currentText())
        book = unicode(self.advancedBookComboBox.currentText())
        chapter_from = self.advancedFromChapter.currentText()
        chapter_to = self.advancedToChapter.currentText()
        verse_from = self.advancedFromVerse.currentText()
        verse_to = self.advancedToVerse.currentText()
        verse_separator = get_reference_match(u'sep_v_display')
        range_separator = get_reference_match(u'sep_r_display')
        verse_range = chapter_from + verse_separator + verse_from + \
            range_separator + chapter_to + verse_separator + verse_to
        versetext = u'%s %s' % (book, verse_range)
        Receiver.send_message(u'cursor_busy')
        self.search_results = self.parent.manager.get_verses(bible, versetext)
        if second_bible:
            self.second_search_results = self.parent.manager.get_verses(
                second_bible, versetext)
        if self.advancedClearComboBox.currentIndex() == 0:
            self.listView.clear()
        if self.listView.count() != 0:
            self.__checkSecondBible(bible, second_bible)
        elif self.search_results:
            self.displayResults(bible, second_bible)
        Receiver.send_message(u'cursor_normal')
        self.advancedSearchButton.setEnabled(True)
        Receiver.send_message(u'openlp_process_events')

    def onQuickSearchButton(self):
        """
        Does a quick search and saves the search results. Quick search can
        either be "Reference Search" or "Text Search".
        """
        log.debug(u'Quick Search Button pressed')
        self.quickSearchButton.setEnabled(False)
        Receiver.send_message(u'openlp_process_events')
        bible = unicode(self.quickVersionComboBox.currentText())
        second_bible = unicode(self.quickSecondComboBox.currentText())
        text = unicode(self.quickSearchEdit.text())
        if self.quickSearchEdit.currentSearchType() == BibleSearch.Reference:
            # We are doing a 'Reference Search'.
            self.search_results = self.parent.manager.get_verses(bible, text)
            if second_bible and self.search_results:
                self.second_search_results = self.parent.manager.get_verses(
                    second_bible, text)
        else:
            # We are doing a 'Text Search'.
            Receiver.send_message(u'cursor_busy')
            bibles = self.parent.manager.get_bibles()
            self.search_results = self.parent.manager.verse_search(bible,
                second_bible, text)
            if second_bible and self.search_results:
                text = []
                for verse in self.search_results:
                    text.append((verse.book.name, verse.chapter, verse.verse,
                        verse.verse))
                self.second_search_results = \
                    bibles[second_bible].get_verses(text)
        if self.quickClearComboBox.currentIndex() == 0:
            self.listView.clear()
        if self.listView.count() != 0 and self.search_results:
            self.__checkSecondBible(bible, second_bible)
        elif self.search_results:
            self.displayResults(bible, second_bible)
        self.quickSearchButton.setEnabled(True)
        Receiver.send_message(u'cursor_normal')
        Receiver.send_message(u'openlp_process_events')

    def __checkSecondBible(self, bible, second_bible):
        """
        Check if the first item is a second bible item or not.
        """
        bitem = self.listView.item(0)
        item_second_bible = self._decodeQtObject(bitem, 'second_bible')
        if item_second_bible and second_bible or not item_second_bible and \
            not second_bible:
            self.displayResults(bible, second_bible)
        elif critical_error_message_box(
            message=translate('BiblePlugin.MediaItem',
            'You cannot combine single and dual Bible verse search results. '
            'Do you want to delete your search results and start a new '
            'search?'),
            parent=self, question=True) == QtGui.QMessageBox.Yes:
            self.listView.clear()
            self.displayResults(bible, second_bible)

    def displayResults(self, bible, second_bible=u''):
        """
        Displays the search results in the media manager. All data needed for
        further action is saved for/in each row.
        """
        verse_separator = get_reference_match(u'sep_v_display')
        version = self.parent.manager.get_meta_data(bible, u'Version').value
        copyright = self.parent.manager.get_meta_data(bible, u'Copyright').value
        permissions = \
            self.parent.manager.get_meta_data(bible, u'Permissions').value
        second_version = u''
        second_copyright = u''
        second_permissions = u''
        if second_bible:
            second_version = self.parent.manager.get_meta_data(
                second_bible, u'Version').value
            second_copyright = self.parent.manager.get_meta_data(
                second_bible, u'Copyright').value
            second_permissions = self.parent.manager.get_meta_data(
                second_bible, u'Permissions').value
        for count, verse in enumerate(self.search_results):
            data = {
                'book': QtCore.QVariant(verse.book.name),
                'chapter': QtCore.QVariant(verse.chapter),
                'verse': QtCore.QVariant(verse.verse),
                'bible': QtCore.QVariant(bible),
                'version': QtCore.QVariant(version),
                'copyright': QtCore.QVariant(copyright),
                'permissions': QtCore.QVariant(permissions),
                'text': QtCore.QVariant(verse.text),
                'second_bible': QtCore.QVariant(second_bible),
                'second_version': QtCore.QVariant(second_version),
                'second_copyright': QtCore.QVariant(second_copyright),
                'second_permissions': QtCore.QVariant(second_permissions),
                'second_text': QtCore.QVariant(u'')
            }
            if second_bible:
                try:
                    data[u'second_text'] = QtCore.QVariant(
                        self.second_search_results[count].text)
                except IndexError:
                    log.exception(u'The second_search_results does not have as '
                    'many verses as the search_results.')
                    break
                bible_text = u' %s %d%s%d (%s, %s)' % (verse.book.name,
                    verse.chapter, verse_separator, verse.verse, version,
                    second_version)
            else:
                bible_text = u'%s %d%s%d (%s)' % (verse.book.name,
                    verse.chapter, verse_separator, verse.verse, version)
            bible_verse = QtGui.QListWidgetItem(bible_text)
            bible_verse.setData(QtCore.Qt.UserRole, QtCore.QVariant(data))
            self.listView.addItem(bible_verse)
        self.listView.selectAll()
        self.search_results = {}
        self.second_search_results = {}

    def _decodeQtObject(self, bitem, key):
        reference = bitem.data(QtCore.Qt.UserRole)
        if isinstance(reference, QtCore.QVariant):
            reference = reference.toPyObject()
        obj = reference[QtCore.QString(key)]
        if isinstance(obj, QtCore.QVariant):
            obj = obj.toPyObject()
        return unicode(obj).strip()

    def generateSlideData(self, service_item, item=None, xmlVersion=False):
        """
        Generates and formats the slides for the service item as well as the
        service item's title.
        """
        log.debug(u'generating slide data')
        items = self.listView.selectedIndexes()
        if len(items) == 0:
            return False
        bible_text = u''
        old_item = None
        old_chapter = -1
        raw_slides = []
        raw_title = []
        verses = VerseReferenceList()
        for item in items:
            bitem = self.listView.item(item.row())
            book = self._decodeQtObject(bitem, 'book')
            chapter = int(self._decodeQtObject(bitem, 'chapter'))
            verse = int(self._decodeQtObject(bitem, 'verse'))
            bible = self._decodeQtObject(bitem, 'bible')
            version = self._decodeQtObject(bitem, 'version')
            copyright = self._decodeQtObject(bitem, 'copyright')
            permissions = self._decodeQtObject(bitem, 'permissions')
            text = self._decodeQtObject(bitem, 'text')
            second_bible = self._decodeQtObject(bitem, 'second_bible')
            second_version = self._decodeQtObject(bitem, 'second_version')
            second_copyright = self._decodeQtObject(bitem, 'second_copyright')
            second_permissions = \
                self._decodeQtObject(bitem, 'second_permissions')
            second_text = self._decodeQtObject(bitem, 'second_text')
            verses.add(book, chapter, verse, version, copyright, permissions)
            verse_text = self.formatVerse(old_chapter, chapter, verse)
            if second_bible:
                bible_text = u'%s&nbsp;%s\n\n%s&nbsp;%s' % (verse_text, text,
                    verse_text, second_text)
                raw_slides.append(bible_text.rstrip())
                bible_text = u''
            # If we are 'Verse Per Slide' then create a new slide.
            elif self.settings.layout_style == LayoutStyle.VersePerSlide:
                bible_text = u'%s&nbsp;%s' % (verse_text, text)
                raw_slides.append(bible_text.rstrip())
                bible_text = u''
            # If we are 'Verse Per Line' then force a new line.
            elif self.settings.layout_style == LayoutStyle.VersePerLine:
                bible_text = u'%s %s&nbsp;%s\n' % (bible_text, verse_text, text)
            # We have to be 'Continuous'.
            else:
                bible_text = u'%s %s&nbsp;%s\n' % (bible_text, verse_text, text)
            if not old_item:
                start_item = item
            elif self.checkTitle(item, old_item):
                raw_title.append(self.formatTitle(start_item, old_item))
                start_item = item
            old_item = item
            old_chapter = chapter
        # Add footer
        service_item.raw_footer.append(verses.format_verses())
        if second_bible:
            verses.add_version(second_version, second_copyright,
                second_permissions)
        service_item.raw_footer.append(verses.format_versions())
        raw_title.append(self.formatTitle(start_item, item))
        # If there are no more items we check whether we have to add bible_text.
        if bible_text:
            raw_slides.append(bible_text.lstrip())
            bible_text = u''
        # Service Item: Capabilities
        if self.settings.layout_style == LayoutStyle.Continuous and \
            not second_bible:
            # Split the line but do not replace line breaks in renderer.
            service_item.add_capability(ItemCapabilities.NoLineBreaks)
        service_item.add_capability(ItemCapabilities.AllowsPreview)
        service_item.add_capability(ItemCapabilities.AllowsLoop)
        # Service Item: Title
        service_item.title = u', '.join(raw_title)
        # Service Item: Theme
        if len(self.settings.bible_theme) == 0:
            service_item.theme = None
        else:
            service_item.theme = self.settings.bible_theme
        [service_item.add_from_text(slide[:30], slide) for slide in raw_slides]
        return True

    def formatTitle(self, start_item, old_item):
        """
        This methode is called, when we have to change the title, because
        we are at the end of a verse range. E. g. if we want to add
        Genesis 1:1-6 as well as Daniel 2:14.

        ``start_item``
            The first item of a range.

        ``old_item``
            The last item of a range.
        """
        verse_separator = get_reference_match(u'sep_v_display')
        range_separator = get_reference_match(u'sep_r_display')
        old_bitem = self.listView.item(old_item.row())
        old_chapter = self._decodeQtObject(old_bitem, 'chapter')
        old_verse = self._decodeQtObject(old_bitem, 'verse')
        start_bitem = self.listView.item(start_item.row())
        start_book = self._decodeQtObject(start_bitem, 'book')
        start_chapter = self._decodeQtObject(start_bitem, 'chapter')
        start_verse = self._decodeQtObject(start_bitem, 'verse')
        start_bible = self._decodeQtObject(start_bitem, 'bible')
        start_second_bible = self._decodeQtObject(start_bitem, 'second_bible')
        if start_second_bible:
            bibles = u'%s, %s' % (start_bible, start_second_bible)
        else:
            bibles = start_bible
        if start_chapter == old_chapter:
            if start_verse == old_verse:
                verse_range = start_chapter + verse_separator + start_verse
            else:
                verse_range = start_chapter + verse_separator + start_verse + \
                range_separator + old_verse
        else:
            verse_range = start_chapter + verse_separator + start_verse + \
                range_separator + old_chapter + verse_separator + old_verse
        return u'%s %s (%s)' % (start_book, verse_range, bibles)

    def checkTitle(self, item, old_item):
        """
        This methode checks if we are at the end of an verse range. If that is
        the case, we return True, otherwise False. E. g. if we added
        Genesis 1:1-6, but the next verse is Daniel 2:14, we return True.

        ``item``
            The item we are dealing with at the moment.

        ``old_item``
            The item we were previously dealing with.
        """
        # Get all the necessary meta data.
        bitem = self.listView.item(item.row())
        book = self._decodeQtObject(bitem, 'book')
        chapter = int(self._decodeQtObject(bitem, 'chapter'))
        verse = int(self._decodeQtObject(bitem, 'verse'))
        bible = self._decodeQtObject(bitem, 'bible')
        second_bible = self._decodeQtObject(bitem, 'second_bible')
        old_bitem = self.listView.item(old_item.row())
        old_book = self._decodeQtObject(old_bitem, 'book')
        old_chapter = int(self._decodeQtObject(old_bitem, 'chapter'))
        old_verse = int(self._decodeQtObject(old_bitem, 'verse'))
        old_bible = self._decodeQtObject(old_bitem, 'bible')
        old_second_bible = self._decodeQtObject(old_bitem, 'second_bible')
        if old_bible != bible or old_second_bible != second_bible or \
            old_book != book:
            # The bible, second bible or book has changed.
            return True
        elif old_verse + 1 != verse and old_chapter == chapter:
            # We are still in the same chapter, but a verse has been skipped.
            return True
        elif old_chapter + 1 == chapter and (verse != 1 or
            old_verse != self.parent.manager.get_verse_count(
            old_bible, old_book, old_chapter)):
            # We are in the following chapter, but the last verse was not the
            # last verse of the chapter or the current verse is not the
            # first one of the chapter.
            return True
        else:
            return False

    def formatVerse(self, old_chapter, chapter, verse):
        """
        Formats and returns the text, each verse starts with, for the given
        chapter and verse. The text is either surrounded by round, square,
        curly brackets or no brackets at all. For example::

            u'{su}1:1{/su}'

        ``old_chapter``
            The previous verse's chapter number (int).

        ``chapter``
            The chapter number (int).

        ``verse``
            The verse number (int).
        """
        verse_separator = get_reference_match(u'sep_v_display')
        if not self.settings.show_new_chapters or old_chapter != chapter:
            verse_text = unicode(chapter) + verse_separator + unicode(verse)
        else:
            verse_text = unicode(verse)
        if self.settings.display_style == DisplayStyle.Round:
            return u'{su}(%s){/su}' % verse_text
        if self.settings.display_style == DisplayStyle.Curly:
            return u'{su}{%s}{/su}' % verse_text
        if self.settings.display_style == DisplayStyle.Square:
            return u'{su}[%s]{/su}' % verse_text
        return u'{su}%s{/su}' % verse_text

    def onlayoutStyleComboBoxChanged(self):
        self.settings.layout_style = self.quickLayoutComboBox.currentIndex()
        self.settings.layoutStyleComboBox.setCurrentIndex(
            self.settings.layout_style)
        QtCore.QSettings().setValue(
            self.settingsSection + u'/verse layout style',
            QtCore.QVariant(self.settings.layout_style))
