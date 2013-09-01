# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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

from openlp.core.lib import Registry, MediaManagerItem, ItemCapabilities, ServiceItemContext, Settings, UiStrings, \
    create_separated_list, translate
from openlp.core.lib.searchedit import SearchEdit
from openlp.core.lib.ui import set_case_insensitive_completer, create_horizontal_adjusting_combo_box, \
    critical_error_message_box, find_and_set_in_combo_box, build_icon
from openlp.core.utils import get_locale_key
from openlp.plugins.bibles.forms import BibleImportForm, EditBibleForm
from openlp.plugins.bibles.lib import LayoutStyle, DisplayStyle, VerseReferenceList, get_reference_separator, \
    LanguageSelection, BibleStrings
from openlp.plugins.bibles.lib.db import BiblesResourcesDB

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
    log.info('Bible Media Item loaded')

    def __init__(self, parent, plugin):
        self.icon_path = 'songs/song'
        self.lock_icon = build_icon(':/bibles/bibles_search_lock.png')
        self.unlock_icon = build_icon(':/bibles/bibles_search_unlock.png')
        MediaManagerItem.__init__(self, parent, plugin)
        # Place to store the search results for both bibles.
        self.settings = self.plugin.settings_tab
        self.quick_preview_allowed = True
        self.has_search = True
        self.search_results = {}
        self.second_search_results = {}
        self.check_search_result()
        Registry().register_function('bibles_load_list', self.reload_bibles)

    def __check_second_bible(self, bible, second_bible):
        """
        Check if the first item is a second bible item or not.
        """
        bitem = self.list_view.item(0)
        if not bitem.flags() & QtCore.Qt.ItemIsSelectable:
            # The item is the "No Search Results" item.
            self.list_view.clear()
            self.displayResults(bible, second_bible)
            return
        else:
            item_second_bible = self._decode_qt_object(bitem, 'second_bible')
        if item_second_bible and second_bible or not item_second_bible and not second_bible:
            self.displayResults(bible, second_bible)
        elif critical_error_message_box(
            message=translate('BiblesPlugin.MediaItem',
                'You cannot combine single and dual Bible verse search results. '
                'Do you want to delete your search results and start a new search?'),
            parent=self, question=True) == QtGui.QMessageBox.Yes:
            self.list_view.clear()
            self.displayResults(bible, second_bible)

    def _decode_qt_object(self, bitem, key):
        reference = bitem.data(QtCore.Qt.UserRole)
        obj = reference[str(key)]
        return str(obj).strip()

    def required_icons(self):
        """
        Set which icons the media manager tab should show
        """
        MediaManagerItem.required_icons(self)
        self.has_import_icon = True
        self.has_new_icon = False
        self.has_edit_icon = True
        self.has_delete_icon = True
        self.add_to_service_item = False

    def addSearchTab(self, prefix, name):
        self.searchTabBar.addTab(name)
        tab = QtGui.QWidget()
        tab.setObjectName(prefix + 'Tab')
        tab.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        layout = QtGui.QGridLayout(tab)
        layout.setObjectName(prefix + 'Layout')
        setattr(self, prefix + 'Tab', tab)
        setattr(self, prefix + 'Layout', layout)

    def addSearchFields(self, prefix, name):
        """
        Creates and adds generic search tab.

        ``prefix``
            The prefix of the tab, this is either ``quick`` or ``advanced``.

        ``name``
            The translated string to display.
        """
        if prefix == 'quick':
            idx = 2
        else:
            idx = 5
        tab = getattr(self, prefix + 'Tab')
        layout = getattr(self, prefix + 'Layout')
        versionLabel = QtGui.QLabel(tab)
        versionLabel.setObjectName(prefix + 'VersionLabel')
        layout.addWidget(versionLabel, idx, 0, QtCore.Qt.AlignRight)
        versionComboBox = create_horizontal_adjusting_combo_box(tab, prefix + 'VersionComboBox')
        versionLabel.setBuddy(versionComboBox)
        layout.addWidget(versionComboBox, idx, 1, 1, 2)
        secondLabel = QtGui.QLabel(tab)
        secondLabel.setObjectName(prefix + 'SecondLabel')
        layout.addWidget(secondLabel, idx + 1, 0, QtCore.Qt.AlignRight)
        secondComboBox = create_horizontal_adjusting_combo_box(tab, prefix + 'SecondComboBox')
        versionLabel.setBuddy(secondComboBox)
        layout.addWidget(secondComboBox, idx + 1, 1, 1, 2)
        styleLabel = QtGui.QLabel(tab)
        styleLabel.setObjectName(prefix + 'StyleLabel')
        layout.addWidget(styleLabel, idx + 2, 0, QtCore.Qt.AlignRight)
        styleComboBox = create_horizontal_adjusting_combo_box(tab, prefix + 'StyleComboBox')
        styleComboBox.addItems(['', '', ''])
        layout.addWidget(styleComboBox, idx + 2, 1, 1, 2)
        search_button_layout = QtGui.QHBoxLayout()
        search_button_layout.setObjectName(prefix + 'search_button_layout')
        search_button_layout.addStretch()
        lockButton = QtGui.QToolButton(tab)
        lockButton.setIcon(self.unlock_icon)
        lockButton.setCheckable(True)
        lockButton.setObjectName(prefix + 'LockButton')
        search_button_layout.addWidget(lockButton)
        searchButton = QtGui.QPushButton(tab)
        searchButton.setObjectName(prefix + 'SearchButton')
        search_button_layout.addWidget(searchButton)
        layout.addLayout(search_button_layout, idx + 3, 1, 1, 2)
        self.page_layout.addWidget(tab)
        tab.setVisible(False)
        lockButton.toggled.connect(self.onLockButtonToggled)
        setattr(self, prefix + 'VersionLabel', versionLabel)
        setattr(self, prefix + 'VersionComboBox', versionComboBox)
        setattr(self, prefix + 'SecondLabel', secondLabel)
        setattr(self, prefix + 'SecondComboBox', secondComboBox)
        setattr(self, prefix + 'StyleLabel', styleLabel)
        setattr(self, prefix + 'StyleComboBox', styleComboBox)
        setattr(self, prefix + 'LockButton', lockButton)
        setattr(self, prefix + 'SearchButtonLayout', search_button_layout)
        setattr(self, prefix + 'SearchButton', searchButton)

    def add_end_header_bar(self):
        self.searchTabBar = QtGui.QTabBar(self)
        self.searchTabBar.setExpanding(False)
        self.searchTabBar.setObjectName('searchTabBar')
        self.page_layout.addWidget(self.searchTabBar)
        # Add the Quick Search tab.
        self.addSearchTab('quick', translate('BiblesPlugin.MediaItem', 'Quick'))
        self.quickSearchLabel = QtGui.QLabel(self.quickTab)
        self.quickSearchLabel.setObjectName('quickSearchLabel')
        self.quickLayout.addWidget(self.quickSearchLabel, 0, 0, QtCore.Qt.AlignRight)
        self.quickSearchEdit = SearchEdit(self.quickTab)
        self.quickSearchEdit.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        self.quickSearchEdit.setObjectName('quickSearchEdit')
        self.quickSearchLabel.setBuddy(self.quickSearchEdit)
        self.quickLayout.addWidget(self.quickSearchEdit, 0, 1, 1, 2)
        self.addSearchFields('quick', translate('BiblesPlugin.MediaItem', 'Quick'))
        self.quickTab.setVisible(True)
        # Add the Advanced Search tab.
        self.addSearchTab('advanced', UiStrings().Advanced)
        self.advancedBookLabel = QtGui.QLabel(self.advancedTab)
        self.advancedBookLabel.setObjectName('advancedBookLabel')
        self.advancedLayout.addWidget(self.advancedBookLabel, 0, 0, QtCore.Qt.AlignRight)
        self.advancedBookComboBox = create_horizontal_adjusting_combo_box(self.advancedTab, 'advancedBookComboBox')
        self.advancedBookLabel.setBuddy(self.advancedBookComboBox)
        self.advancedLayout.addWidget(self.advancedBookComboBox, 0, 1, 1, 2)
        self.advancedChapterLabel = QtGui.QLabel(self.advancedTab)
        self.advancedChapterLabel.setObjectName('advancedChapterLabel')
        self.advancedLayout.addWidget(self.advancedChapterLabel, 1, 1, 1, 2)
        self.advancedVerseLabel = QtGui.QLabel(self.advancedTab)
        self.advancedVerseLabel.setObjectName('advancedVerseLabel')
        self.advancedLayout.addWidget(self.advancedVerseLabel, 1, 2)
        self.advancedFromLabel = QtGui.QLabel(self.advancedTab)
        self.advancedFromLabel.setObjectName('advancedFromLabel')
        self.advancedLayout.addWidget(self.advancedFromLabel, 3, 0, QtCore.Qt.AlignRight)
        self.advancedFromChapter = QtGui.QComboBox(self.advancedTab)
        self.advancedFromChapter.setObjectName('advancedFromChapter')
        self.advancedLayout.addWidget(self.advancedFromChapter, 3, 1)
        self.advancedFromVerse = QtGui.QComboBox(self.advancedTab)
        self.advancedFromVerse.setObjectName('advancedFromVerse')
        self.advancedLayout.addWidget(self.advancedFromVerse, 3, 2)
        self.advancedToLabel = QtGui.QLabel(self.advancedTab)
        self.advancedToLabel.setObjectName('advancedToLabel')
        self.advancedLayout.addWidget(self.advancedToLabel, 4, 0, QtCore.Qt.AlignRight)
        self.advancedToChapter = QtGui.QComboBox(self.advancedTab)
        self.advancedToChapter.setObjectName('advancedToChapter')
        self.advancedLayout.addWidget(self.advancedToChapter, 4, 1)
        self.advancedToVerse = QtGui.QComboBox(self.advancedTab)
        self.advancedToVerse.setObjectName('advancedToVerse')
        self.advancedLayout.addWidget(self.advancedToVerse, 4, 2)
        self.addSearchFields('advanced', UiStrings().Advanced)
        # Combo Boxes
        self.quickVersionComboBox.activated.connect(self.updateAutoCompleter)
        self.quickSecondComboBox.activated.connect(self.updateAutoCompleter)
        self.advancedVersionComboBox.activated.connect(self.onAdvancedVersionComboBox)
        self.advancedSecondComboBox.activated.connect(self.onAdvancedSecondComboBox)
        self.advancedBookComboBox.activated.connect(self.onAdvancedBookComboBox)
        self.advancedFromChapter.activated.connect(self.onAdvancedFromChapter)
        self.advancedFromVerse.activated.connect(self.onAdvancedFromVerse)
        self.advancedToChapter.activated.connect(self.onAdvancedToChapter)
        QtCore.QObject.connect(self.quickSearchEdit, QtCore.SIGNAL('searchTypeChanged(int)'), self.updateAutoCompleter)
        self.quickVersionComboBox.activated.connect(self.updateAutoCompleter)
        self.quickStyleComboBox.activated.connect(self.onQuickStyleComboBoxChanged)
        self.advancedStyleComboBox.activated.connect(self.onAdvancedStyleComboBoxChanged)
        # Buttons
        self.advancedSearchButton.clicked.connect(self.onAdvancedSearchButton)
        self.quickSearchButton.clicked.connect(self.onQuickSearchButton)
        # Other stuff
        self.quickSearchEdit.returnPressed.connect(self.onQuickSearchButton)
        self.searchTabBar.currentChanged.connect(self.onSearchTabBarCurrentChanged)

    def on_focus(self):
        if self.quickTab.isVisible():
            self.quickSearchEdit.setFocus()
        else:
            self.advancedBookComboBox.setFocus()

    def config_update(self):
        log.debug('config_update')
        if Settings().value(self.settings_section + '/second bibles'):
            self.advancedSecondLabel.setVisible(True)
            self.advancedSecondComboBox.setVisible(True)
            self.quickSecondLabel.setVisible(True)
            self.quickSecondComboBox.setVisible(True)
        else:
            self.advancedSecondLabel.setVisible(False)
            self.advancedSecondComboBox.setVisible(False)
            self.quickSecondLabel.setVisible(False)
            self.quickSecondComboBox.setVisible(False)
        self.quickStyleComboBox.setCurrentIndex(self.settings.layout_style)
        self.advancedStyleComboBox.setCurrentIndex(self.settings.layout_style)

    def retranslateUi(self):
        log.debug('retranslateUi')
        self.quickSearchLabel.setText(translate('BiblesPlugin.MediaItem', 'Find:'))
        self.quickVersionLabel.setText('%s:' % UiStrings().Version)
        self.quickSecondLabel.setText(translate('BiblesPlugin.MediaItem', 'Second:'))
        self.quickStyleLabel.setText(UiStrings().LayoutStyle)
        self.quickStyleComboBox.setItemText(LayoutStyle.VersePerSlide, UiStrings().VersePerSlide)
        self.quickStyleComboBox.setItemText(LayoutStyle.VersePerLine, UiStrings().VersePerLine)
        self.quickStyleComboBox.setItemText(LayoutStyle.Continuous, UiStrings().Continuous)
        self.quickLockButton.setToolTip(translate('BiblesPlugin.MediaItem',
            'Toggle to keep or clear the previous results.'))
        self.quickSearchButton.setText(UiStrings().Search)
        self.advancedBookLabel.setText(translate('BiblesPlugin.MediaItem', 'Book:'))
        self.advancedChapterLabel.setText(translate('BiblesPlugin.MediaItem', 'Chapter:'))
        self.advancedVerseLabel.setText(translate('BiblesPlugin.MediaItem', 'Verse:'))
        self.advancedFromLabel.setText(translate('BiblesPlugin.MediaItem', 'From:'))
        self.advancedToLabel.setText(translate('BiblesPlugin.MediaItem', 'To:'))
        self.advancedVersionLabel.setText('%s:' % UiStrings().Version)
        self.advancedSecondLabel.setText(translate('BiblesPlugin.MediaItem', 'Second:'))
        self.advancedStyleLabel.setText(UiStrings().LayoutStyle)
        self.advancedStyleComboBox.setItemText(LayoutStyle.VersePerSlide, UiStrings().VersePerSlide)
        self.advancedStyleComboBox.setItemText(LayoutStyle.VersePerLine, UiStrings().VersePerLine)
        self.advancedStyleComboBox.setItemText(LayoutStyle.Continuous, UiStrings().Continuous)
        self.advancedLockButton.setToolTip(translate('BiblesPlugin.MediaItem',
            'Toggle to keep or clear the previous results.'))
        self.advancedSearchButton.setText(UiStrings().Search)

    def initialise(self):
        log.debug('bible manager initialise')
        self.plugin.manager.media = self
        self.loadBibles()
        self.quickSearchEdit.set_search_types([
            (BibleSearch.Reference, ':/bibles/bibles_search_reference.png',
                translate('BiblesPlugin.MediaItem', 'Scripture Reference'),
                translate('BiblesPlugin.MediaItem', 'Search Scripture Reference...')),
            (BibleSearch.Text, ':/bibles/bibles_search_text.png',
                translate('BiblesPlugin.MediaItem', 'Text Search'),
                translate('BiblesPlugin.MediaItem', 'Search Text...'))
        ])
        self.quickSearchEdit.set_current_search_type(Settings().value('%s/last search type' % self.settings_section))
        self.config_update()
        log.debug('bible manager initialise complete')

    def loadBibles(self):
        log.debug('Loading Bibles')
        self.quickVersionComboBox.clear()
        self.quickSecondComboBox.clear()
        self.advancedVersionComboBox.clear()
        self.advancedSecondComboBox.clear()
        self.quickSecondComboBox.addItem('')
        self.advancedSecondComboBox.addItem('')
        # Get all bibles and sort the list.
        bibles = list(self.plugin.manager.get_bibles().keys())
        bibles = [_f for _f in bibles if _f]
        bibles.sort(key=get_locale_key)
        # Load the bibles into the combo boxes.
        self.quickVersionComboBox.addItems(bibles)
        self.quickSecondComboBox.addItems(bibles)
        self.advancedVersionComboBox.addItems(bibles)
        self.advancedSecondComboBox.addItems(bibles)
        # set the default value
        bible = Settings().value(self.settings_section + '/advanced bible')
        if bible in bibles:
            find_and_set_in_combo_box(self.advancedVersionComboBox, bible)
            self.initialiseAdvancedBible(str(bible))
        elif bibles:
            self.initialiseAdvancedBible(bibles[0])
        bible = Settings().value(self.settings_section + '/quick bible')
        find_and_set_in_combo_box(self.quickVersionComboBox, bible)

    def reload_bibles(self, process=False):
        log.debug('Reloading Bibles')
        self.plugin.manager.reload_bibles()
        self.loadBibles()
        # If called from first time wizard re-run, process any new bibles.
        if process:
            self.plugin.app_startup()
        self.updateAutoCompleter()

    def initialiseAdvancedBible(self, bible, last_book_id=None):
        """
        This initialises the given bible, which means that its book names and
        their chapter numbers is added to the combo boxes on the
        'Advanced Search' Tab. This is not of any importance of the
        'Quick Search' Tab.

        ``bible``
            The bible to initialise (unicode).

        ``last_book_id``
            The "book reference id" of the book which is choosen at the moment.
            (int)
        """
        log.debug('initialiseAdvancedBible %s, %s', bible, last_book_id)
        book_data = self.plugin.manager.get_books(bible)
        secondbible = self.advancedSecondComboBox.currentText()
        if secondbible != '':
            secondbook_data = self.plugin.manager.get_books(secondbible)
            book_data_temp = []
            for book in book_data:
                for secondbook in secondbook_data:
                    if book['book_reference_id'] == \
                        secondbook['book_reference_id']:
                        book_data_temp.append(book)
            book_data = book_data_temp
        self.advancedBookComboBox.clear()
        first = True
        initialise_chapter_verse = False
        language_selection = self.plugin.manager.get_language_selection(bible)
        book_names = BibleStrings().BookNames
        for book in book_data:
            row = self.advancedBookComboBox.count()
            if language_selection == LanguageSelection.Bible:
                self.advancedBookComboBox.addItem(book['name'])
            elif language_selection == LanguageSelection.Application:
                data = BiblesResourcesDB.get_book_by_id(book['book_reference_id'])
                self.advancedBookComboBox.addItem(book_names[data['abbreviation']])
            elif language_selection == LanguageSelection.English:
                data = BiblesResourcesDB.get_book_by_id(book['book_reference_id'])
                self.advancedBookComboBox.addItem(data['name'])
            self.advancedBookComboBox.setItemData(row, book['book_reference_id'])
            if first:
                first = False
                first_book = book
                initialise_chapter_verse = True
            if last_book_id and last_book_id == int(book['book_reference_id']):
                index = self.advancedBookComboBox.findData(book['book_reference_id'])
                if index == -1:
                    # Not Found.
                    index = 0
                self.advancedBookComboBox.setCurrentIndex(index)
                initialise_chapter_verse = False
        if initialise_chapter_verse:
            self.initialiseChapterVerse(bible, first_book['name'],
                first_book['book_reference_id'])

    def initialiseChapterVerse(self, bible, book, book_ref_id):
        log.debug('initialiseChapterVerse %s, %s, %s', bible, book, book_ref_id)
        book = self.plugin.manager.get_book_by_id(bible, book_ref_id)
        self.chapter_count = self.plugin.manager.get_chapter_count(bible, book)
        verse_count = self.plugin.manager.get_verse_count_by_book_ref_id(bible, book_ref_id, 1)
        if verse_count == 0:
            self.advancedSearchButton.setEnabled(False)
            critical_error_message_box(message=translate('BiblesPlugin.MediaItem', 'Bible not fully loaded.'))
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
        log.debug('updateAutoCompleter')
        # Save the current search type to the configuration.
        Settings().setValue('%s/last search type' % self.settings_section, self.quickSearchEdit.current_search_type())
        # Save the current bible to the configuration.
        Settings().setValue(self.settings_section + '/quick bible', self.quickVersionComboBox.currentText())
        books = []
        # We have to do a 'Reference Search'.
        if self.quickSearchEdit.current_search_type() == BibleSearch.Reference:
            bibles = self.plugin.manager.get_bibles()
            bible = self.quickVersionComboBox.currentText()
            if bible:
                book_data = bibles[bible].get_books()
                secondbible = self.quickSecondComboBox.currentText()
                if secondbible != '':
                    secondbook_data = bibles[secondbible].get_books()
                    book_data_temp = []
                    for book in book_data:
                        for secondbook in secondbook_data:
                            if book.book_reference_id == secondbook.book_reference_id:
                                book_data_temp.append(book)
                    book_data = book_data_temp
                language_selection = self.plugin.manager.get_language_selection(bible)
                if language_selection == LanguageSelection.Bible:
                    books = [book.name + ' ' for book in book_data]
                elif language_selection == LanguageSelection.Application:
                    book_names = BibleStrings().BookNames
                    for book in book_data:
                        data = BiblesResourcesDB.get_book_by_id(book.book_reference_id)
                        books.append(str(book_names[data['abbreviation']]) + ' ')
                elif language_selection == LanguageSelection.English:
                    for book in book_data:
                        data = BiblesResourcesDB.get_book_by_id(book.book_reference_id)
                        books.append(data['name'] + ' ')
                books.sort(key=get_locale_key)
        set_case_insensitive_completer(books, self.quickSearchEdit)

    def on_import_click(self):
        if not hasattr(self, 'import_wizard'):
            self.import_wizard = BibleImportForm(self, self.plugin.manager, self.plugin)
        # If the import was not cancelled then reload.
        if self.import_wizard.exec_():
            self.reload_bibles()

    def on_edit_click(self):
        if self.quickTab.isVisible():
            bible = self.quickVersionComboBox.currentText()
        elif self.advancedTab.isVisible():
            bible = self.advancedVersionComboBox.currentText()
        if bible:
            self.editBibleForm = EditBibleForm(self, self.main_window, self.plugin.manager)
            self.editBibleForm.loadBible(bible)
            if self.editBibleForm.exec_():
                self.reload_bibles()

    def on_delete_click(self):
        if self.quickTab.isVisible():
            bible = self.quickVersionComboBox.currentText()
        elif self.advancedTab.isVisible():
            bible = self.advancedVersionComboBox.currentText()
        if bible:
            if QtGui.QMessageBox.question(self, UiStrings().ConfirmDelete,
                translate('BiblesPlugin.MediaItem', 'Are you sure you want to completely delete "%s" Bible from '
                    'OpenLP?\n\nYou will need to re-import this Bible to use it again.') % bible,
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
                QtGui.QMessageBox.Yes) == QtGui.QMessageBox.No:
                return
            self.plugin.manager.delete_bible(bible)
            self.reload_bibles()

    def onSearchTabBarCurrentChanged(self, index):
        if index == 0:
            self.advancedTab.setVisible(False)
            self.quickTab.setVisible(True)
            self.quickSearchEdit.setFocus()
        else:
            self.quickTab.setVisible(False)
            self.advancedTab.setVisible(True)
            self.advancedBookComboBox.setFocus()

    def onLockButtonToggled(self, checked):
        if checked:
            self.sender().setIcon(self.lock_icon)
        else:
            self.sender().setIcon(self.unlock_icon)

    def onQuickStyleComboBoxChanged(self):
        self.settings.layout_style = self.quickStyleComboBox.currentIndex()
        self.advancedStyleComboBox.setCurrentIndex(self.settings.layout_style)
        self.settings.layout_style_combo_box.setCurrentIndex(self.settings.layout_style)
        Settings().setValue(self.settings_section + '/verse layout style', self.settings.layout_style)

    def onAdvancedStyleComboBoxChanged(self):
        self.settings.layout_style = self.advancedStyleComboBox.currentIndex()
        self.quickStyleComboBox.setCurrentIndex(self.settings.layout_style)
        self.settings.layout_style_combo_box.setCurrentIndex(self.settings.layout_style)
        Settings().setValue(self.settings_section + '/verse layout style', self.settings.layout_style)

    def onAdvancedVersionComboBox(self):
        Settings().setValue(self.settings_section + '/advanced bible', self.advancedVersionComboBox.currentText())
        self.initialiseAdvancedBible(self.advancedVersionComboBox.currentText(),
            self.advancedBookComboBox.itemData(int(self.advancedBookComboBox.currentIndex())))

    def onAdvancedSecondComboBox(self):
        self.initialiseAdvancedBible(self.advancedVersionComboBox.currentText(),
            self.advancedBookComboBox.itemData(int(self.advancedBookComboBox.currentIndex())))

    def onAdvancedBookComboBox(self):
        item = int(self.advancedBookComboBox.currentIndex())
        self.initialiseChapterVerse(
            self.advancedVersionComboBox.currentText(),
            self.advancedBookComboBox.currentText(),
            self.advancedBookComboBox.itemData(item))

    def onAdvancedFromVerse(self):
        chapter_from = int(self.advancedFromChapter.currentText())
        chapter_to = int(self.advancedToChapter.currentText())
        if chapter_from == chapter_to:
            bible = self.advancedVersionComboBox.currentText()
            book_ref_id = self.advancedBookComboBox.itemData(int(self.advancedBookComboBox.currentIndex()))
            verse_from = int(self.advancedFromVerse.currentText())
            verse_count = self.plugin.manager.get_verse_count_by_book_ref_id(bible, book_ref_id, chapter_to)
            self.adjustComboBox(verse_from, verse_count, self.advancedToVerse, True)

    def onAdvancedToChapter(self):
        bible = self.advancedVersionComboBox.currentText()
        book_ref_id = self.advancedBookComboBox.itemData(int(self.advancedBookComboBox.currentIndex()))
        chapter_from = int(self.advancedFromChapter.currentText())
        chapter_to = int(self.advancedToChapter.currentText())
        verse_from = int(self.advancedFromVerse.currentText())
        verse_to = int(self.advancedToVerse.currentText())
        verse_count = self.plugin.manager.get_verse_count_by_book_ref_id(bible, book_ref_id, chapter_to)
        if chapter_from == chapter_to and verse_from > verse_to:
            self.adjustComboBox(verse_from, verse_count, self.advancedToVerse)
        else:
            self.adjustComboBox(1, verse_count, self.advancedToVerse)

    def onAdvancedFromChapter(self):
        bible = self.advancedVersionComboBox.currentText()
        book_ref_id = self.advancedBookComboBox.itemData(
            int(self.advancedBookComboBox.currentIndex()))
        chapter_from = int(self.advancedFromChapter.currentText())
        chapter_to = int(self.advancedToChapter.currentText())
        verse_count = self.plugin.manager.get_verse_count_by_book_ref_id(bible, book_ref_id, chapter_from)
        self.adjustComboBox(1, verse_count, self.advancedFromVerse)
        if chapter_from > chapter_to:
            self.adjustComboBox(1, verse_count, self.advancedToVerse)
            self.adjustComboBox(chapter_from, self.chapter_count, self.advancedToChapter)
        elif chapter_from == chapter_to:
            self.adjustComboBox(chapter_from, self.chapter_count, self.advancedToChapter)
            self.adjustComboBox(1, verse_count, self.advancedToVerse, True)
        else:
            self.adjustComboBox(chapter_from, self.chapter_count, self.advancedToChapter, True)

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
        log.debug('adjustComboBox %s, %s, %s', combo, range_from, range_to)
        if restore:
            old_text = combo.currentText()
        combo.clear()
        combo.addItems(list(map(str, list(range(range_from, range_to + 1)))))
        if restore and combo.findText(old_text) != -1:
            combo.setCurrentIndex(combo.findText(old_text))

    def onAdvancedSearchButton(self):
        """
        Does an advanced search and saves the search results.
        """
        log.debug('Advanced Search Button clicked')
        self.advancedSearchButton.setEnabled(False)
        self.application.process_events()
        bible = self.advancedVersionComboBox.currentText()
        second_bible = self.advancedSecondComboBox.currentText()
        book = self.advancedBookComboBox.currentText()
        book_ref_id = self.advancedBookComboBox.itemData(int(self.advancedBookComboBox.currentIndex()))
        chapter_from = self.advancedFromChapter.currentText()
        chapter_to = self.advancedToChapter.currentText()
        verse_from = self.advancedFromVerse.currentText()
        verse_to = self.advancedToVerse.currentText()
        verse_separator = get_reference_separator('sep_v_display')
        range_separator = get_reference_separator('sep_r_display')
        verse_range = chapter_from + verse_separator + verse_from + range_separator + chapter_to + \
            verse_separator + verse_to
        versetext = '%s %s' % (book, verse_range)
        self.application.set_busy_cursor()
        self.search_results = self.plugin.manager.get_verses(bible, versetext, book_ref_id)
        if second_bible:
            self.second_search_results = self.plugin.manager.get_verses(second_bible, versetext, book_ref_id)
        if not self.advancedLockButton.isChecked():
            self.list_view.clear()
        if self.list_view.count() != 0:
            self.__check_second_bible(bible, second_bible)
        elif self.search_results:
            self.displayResults(bible, second_bible)
        self.advancedSearchButton.setEnabled(True)
        self.check_search_result()
        self.application.set_normal_cursor()

    def onQuickSearchButton(self):
        """
        Does a quick search and saves the search results. Quick search can
        either be "Reference Search" or "Text Search".
        """
        log.debug('Quick Search Button clicked')
        self.quickSearchButton.setEnabled(False)
        self.application.process_events()
        bible = self.quickVersionComboBox.currentText()
        second_bible = self.quickSecondComboBox.currentText()
        text = self.quickSearchEdit.text()
        if self.quickSearchEdit.current_search_type() == BibleSearch.Reference:
            # We are doing a 'Reference Search'.
            self.search_results = self.plugin.manager.get_verses(bible, text)
            if second_bible and self.search_results:
                self.second_search_results = self.plugin.manager.get_verses(second_bible, text,
                    self.search_results[0].book.book_reference_id)
        else:
            # We are doing a 'Text Search'.
            self.application.set_busy_cursor()
            bibles = self.plugin.manager.get_bibles()
            self.search_results = self.plugin.manager.verse_search(bible, second_bible, text)
            if second_bible and self.search_results:
                text = []
                new_search_results = []
                count = 0
                passage_not_found = False
                for verse in self.search_results:
                    db_book = bibles[second_bible].get_book_by_book_ref_id(verse.book.book_reference_id)
                    if not db_book:
                        log.debug('Passage "%s %d:%d" not found in Second Bible' %
                            (verse.book.name, verse.chapter, verse.verse))
                        passage_not_found = True
                        count += 1
                        continue
                    new_search_results.append(verse)
                    text.append((verse.book.book_reference_id, verse.chapter,
                        verse.verse, verse.verse))
                if passage_not_found:
                    QtGui.QMessageBox.information(self, translate('BiblesPlugin.MediaItem', 'Information'),
                        translate('BiblesPlugin.MediaItem', 'The second Bible does not contain all the verses '
                            'that are in the main Bible. Only verses found in both Bibles will be shown. %d verses '
                            'have not been included in the results.') % count,
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                self.search_results = new_search_results
                self.second_search_results = bibles[second_bible].get_verses(text)
        if not self.quickLockButton.isChecked():
            self.list_view.clear()
        if self.list_view.count() != 0 and self.search_results:
            self.__check_second_bible(bible, second_bible)
        elif self.search_results:
            self.displayResults(bible, second_bible)
        self.quickSearchButton.setEnabled(True)
        self.check_search_result()
        self.application.set_normal_cursor()

    def displayResults(self, bible, second_bible=''):
        """
        Displays the search results in the media manager. All data needed for
        further action is saved for/in each row.
        """
        items = self.buildDisplayResults(bible, second_bible, self.search_results)
        for bible_verse in items:
            self.list_view.addItem(bible_verse)
        self.list_view.selectAll()
        self.search_results = {}
        self.second_search_results = {}

    def buildDisplayResults(self, bible, second_bible, search_results):
        """
        Displays the search results in the media manager. All data needed for
        further action is saved for/in each row.
        """
        verse_separator = get_reference_separator('sep_v_display')
        version = self.plugin.manager.get_meta_data(bible, 'name').value
        copyright = self.plugin.manager.get_meta_data(bible, 'copyright').value
        permissions = self.plugin.manager.get_meta_data(bible, 'permissions').value
        second_version = ''
        second_copyright = ''
        second_permissions = ''
        if second_bible:
            second_version = self.plugin.manager.get_meta_data(second_bible, 'name').value
            second_copyright = self.plugin.manager.get_meta_data(second_bible, 'copyright').value
            second_permissions = self.plugin.manager.get_meta_data(second_bible, 'permissions').value
        items = []
        language_selection = self.plugin.manager.get_language_selection(bible)
        for count, verse in enumerate(search_results):
            book = None
            if language_selection == LanguageSelection.Bible:
                book = verse.book.name
            elif language_selection == LanguageSelection.Application:
                book_names = BibleStrings().BookNames
                data = BiblesResourcesDB.get_book_by_id(verse.book.book_reference_id)
                book = str(book_names[data['abbreviation']])
            elif language_selection == LanguageSelection.English:
                data = BiblesResourcesDB.get_book_by_id(verse.book.book_reference_id)
                book = data['name']
            data = {
                'book': book,
                'chapter': verse.chapter,
                'verse': verse.verse,
                'bible': bible,
                'version': version,
                'copyright': copyright,
                'permissions': permissions,
                'text': verse.text,
                'second_bible': second_bible,
                'second_version': second_version,
                'second_copyright': second_copyright,
                'second_permissions': second_permissions,
                'second_text': ''
            }
            if second_bible:
                try:
                    data['second_text'] = self.second_search_results[count].text
                except IndexError:
                    log.exception('The second_search_results does not have as many verses as the search_results.')
                    break
                bible_text = '%s %d%s%d (%s, %s)' % (book, verse.chapter, verse_separator, verse.verse, version,
                    second_version)
            else:
                bible_text = '%s %d%s%d (%s)' % (book, verse.chapter, verse_separator, verse.verse, version)
            bible_verse = QtGui.QListWidgetItem(bible_text)
            bible_verse.setData(QtCore.Qt.UserRole, data)
            items.append(bible_verse)
        return items

    def generate_slide_data(self, service_item, item=None, xmlVersion=False,
        remote=False, context=ServiceItemContext.Service):
        """
        Generates and formats the slides for the service item as well as the
        service item's title.
        """
        log.debug('generating slide data')
        if item:
            items = item
        else:
            items = self.list_view.selectedItems()
        if not items:
            return False
        bible_text = ''
        old_item = None
        old_chapter = -1
        raw_slides = []
        raw_title = []
        verses = VerseReferenceList()
        for bitem in items:
            book = self._decode_qt_object(bitem, 'book')
            chapter = int(self._decode_qt_object(bitem, 'chapter'))
            verse = int(self._decode_qt_object(bitem, 'verse'))
            bible = self._decode_qt_object(bitem, 'bible')
            version = self._decode_qt_object(bitem, 'version')
            copyright = self._decode_qt_object(bitem, 'copyright')
            permissions = self._decode_qt_object(bitem, 'permissions')
            text = self._decode_qt_object(bitem, 'text')
            second_bible = self._decode_qt_object(bitem, 'second_bible')
            second_version = self._decode_qt_object(bitem, 'second_version')
            second_copyright = self._decode_qt_object(bitem, 'second_copyright')
            second_permissions = self._decode_qt_object(bitem, 'second_permissions')
            second_text = self._decode_qt_object(bitem, 'second_text')
            verses.add(book, chapter, verse, version, copyright, permissions)
            verse_text = self.formatVerse(old_chapter, chapter, verse)
            if second_bible:
                bible_text = '%s&nbsp;%s\n\n%s&nbsp;%s' % (verse_text, text, verse_text, second_text)
                raw_slides.append(bible_text.rstrip())
                bible_text = ''
            # If we are 'Verse Per Slide' then create a new slide.
            elif self.settings.layout_style == LayoutStyle.VersePerSlide:
                bible_text = '%s&nbsp;%s' % (verse_text, text)
                raw_slides.append(bible_text.rstrip())
                bible_text = ''
            # If we are 'Verse Per Line' then force a new line.
            elif self.settings.layout_style == LayoutStyle.VersePerLine:
                bible_text = '%s%s&nbsp;%s\n' % (bible_text, verse_text, text)
            # We have to be 'Continuous'.
            else:
                bible_text = '%s %s&nbsp;%s\n' % (bible_text, verse_text, text)
            bible_text = bible_text.strip(' ')
            if not old_item:
                start_item = bitem
            elif self.checkTitle(bitem, old_item):
                raw_title.append(self.formatTitle(start_item, old_item))
                start_item = bitem
            old_item = bitem
            old_chapter = chapter
        # Add footer
        service_item.raw_footer.append(verses.format_verses())
        if second_bible:
            verses.add_version(second_version, second_copyright, second_permissions)
        service_item.raw_footer.append(verses.format_versions())
        raw_title.append(self.formatTitle(start_item, bitem))
        # If there are no more items we check whether we have to add bible_text.
        if bible_text:
            raw_slides.append(bible_text.lstrip())
            bible_text = ''
        # Service Item: Capabilities
        if self.settings.layout_style == LayoutStyle.Continuous and not second_bible:
            # Split the line but do not replace line breaks in renderer.
            service_item.add_capability(ItemCapabilities.NoLineBreaks)
        service_item.add_capability(ItemCapabilities.CanPreview)
        service_item.add_capability(ItemCapabilities.CanLoop)
        service_item.add_capability(ItemCapabilities.CanWordSplit)
        # Service Item: Title
        service_item.title = create_separated_list(raw_title)
        # Service Item: Theme
        if not self.settings.bible_theme:
            service_item.theme = None
        else:
            service_item.theme = self.settings.bible_theme
        for slide in raw_slides:
            service_item.add_from_text(slide)
        return True

    def formatTitle(self, start_bitem, old_bitem):
        """
        This method is called, when we have to change the title, because
        we are at the end of a verse range. E. g. if we want to add
        Genesis 1:1-6 as well as Daniel 2:14.

        ``start_item``
            The first item of a range.

        ``old_item``
            The last item of a range.
        """
        verse_separator = get_reference_separator('sep_v_display')
        range_separator = get_reference_separator('sep_r_display')
        old_chapter = self._decode_qt_object(old_bitem, 'chapter')
        old_verse = self._decode_qt_object(old_bitem, 'verse')
        start_book = self._decode_qt_object(start_bitem, 'book')
        start_chapter = self._decode_qt_object(start_bitem, 'chapter')
        start_verse = self._decode_qt_object(start_bitem, 'verse')
        start_bible = self._decode_qt_object(start_bitem, 'bible')
        start_second_bible = self._decode_qt_object(start_bitem, 'second_bible')
        if start_second_bible:
            bibles = '%s, %s' % (start_bible, start_second_bible)
        else:
            bibles = start_bible
        if start_chapter == old_chapter:
            if start_verse == old_verse:
                verse_range = start_chapter + verse_separator + start_verse
            else:
                verse_range = start_chapter + verse_separator + start_verse + range_separator + old_verse
        else:
            verse_range = start_chapter + verse_separator + start_verse + \
                range_separator + old_chapter + verse_separator + old_verse
        return '%s %s (%s)' % (start_book, verse_range, bibles)

    def checkTitle(self, bitem, old_bitem):
        """
        This method checks if we are at the end of an verse range. If that is
        the case, we return True, otherwise False. E. g. if we added
        Genesis 1:1-6, but the next verse is Daniel 2:14, we return True.

        ``item``
            The item we are dealing with at the moment.

        ``old_item``
            The item we were previously dealing with.
        """
        # Get all the necessary meta data.
        book = self._decode_qt_object(bitem, 'book')
        chapter = int(self._decode_qt_object(bitem, 'chapter'))
        verse = int(self._decode_qt_object(bitem, 'verse'))
        bible = self._decode_qt_object(bitem, 'bible')
        second_bible = self._decode_qt_object(bitem, 'second_bible')
        old_book = self._decode_qt_object(old_bitem, 'book')
        old_chapter = int(self._decode_qt_object(old_bitem, 'chapter'))
        old_verse = int(self._decode_qt_object(old_bitem, 'verse'))
        old_bible = self._decode_qt_object(old_bitem, 'bible')
        old_second_bible = self._decode_qt_object(old_bitem, 'second_bible')
        if old_bible != bible or old_second_bible != second_bible or old_book != book:
            # The bible, second bible or book has changed.
            return True
        elif old_verse + 1 != verse and old_chapter == chapter:
            # We are still in the same chapter, but a verse has been skipped.
            return True
        elif old_chapter + 1 == chapter and (verse != 1 or
            old_verse != self.plugin.manager.get_verse_count(old_bible, old_book, old_chapter)):
            # We are in the following chapter, but the last verse was not the
            # last verse of the chapter or the current verse is not the
            # first one of the chapter.
            return True
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
        verse_separator = get_reference_separator('sep_v_display')
        if not self.settings.show_new_chapters or old_chapter != chapter:
            verse_text = str(chapter) + verse_separator + str(verse)
        else:
            verse_text = str(verse)
        if self.settings.display_style == DisplayStyle.Round:
            return '{su}(%s){/su}' % verse_text
        if self.settings.display_style == DisplayStyle.Curly:
            return '{su}{%s}{/su}' % verse_text
        if self.settings.display_style == DisplayStyle.Square:
            return '{su}[%s]{/su}' % verse_text
        return '{su}%s{/su}' % verse_text

    def search(self, string, showError):
        """
        Search for some Bible verses (by reference).
        """
        bible = self.quickVersionComboBox.currentText()
        search_results = self.plugin.manager.get_verses(bible, string, False, showError)
        if search_results:
            versetext = ' '.join([verse.text for verse in search_results])
            return [[string, versetext]]
        return []

    def create_item_from_id(self, item_id):
        """
        Create a media item from an item id.
        """
        item = QtGui.QListWidgetItem()
        bible = self.quickVersionComboBox.currentText()
        search_results = self.plugin.manager.get_verses(bible, item_id, False)
        items = self.buildDisplayResults(bible, '', search_results)
        return items
