# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
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
"""
The :mod:`~openlp.plugins.songs.forms.songselectform` module contains the GUI for the SongSelect importer
"""

import logging
from http.cookiejar import CookieJar
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, HTTPError, build_opener
from html.parser import HTMLParser
from time import sleep

from PyQt4 import QtCore, QtGui
from bs4 import BeautifulSoup, NavigableString
from openlp.core import Settings

from openlp.core.common import Registry
from openlp.core.lib import translate
from openlp.plugins.songs.lib import VerseType, clean_song
from openlp.plugins.songs.forms.songselectdialog import Ui_SongSelectDialog
from openlp.plugins.songs.lib.db import Author, Song
from openlp.plugins.songs.lib.xml import SongXML

USER_AGENT = 'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; GT-I9000 ' \
    'Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 ' \
    'Mobile Safari/534.30'
BASE_URL = 'https://mobile.songselect.com'
LOGIN_URL = BASE_URL + '/account/login'
LOGOUT_URL = BASE_URL + '/account/logout'
SEARCH_URL = BASE_URL + '/search/results'

log = logging.getLogger(__name__)


class SearchWorker(QtCore.QObject):
    """
    Run the actual SongSelect search, and notify the GUI when we find each song.
    """
    show_info = QtCore.pyqtSignal(str, str)
    found_song = QtCore.pyqtSignal(dict)
    finished = QtCore.pyqtSignal(list)
    quit = QtCore.pyqtSignal()

    def __init__(self, opener, params):
        super().__init__()
        self.opener = opener
        self.params = params
        self.html_parser = HTMLParser()

    def _search_and_parse_results(self, params):
        params = urlencode(params)
        results_page = BeautifulSoup(self.opener.open(SEARCH_URL + '?' + params).read(), 'lxml')
        search_results = results_page.find_all('li', 'result pane')
        songs = []
        for result in search_results:
            song = {
                'title': self.html_parser.unescape(result.find('h3').string),
                'authors': [self.html_parser.unescape(author.string) for author in result.find_all('li')],
                'link': BASE_URL + result.find('a')['href']
            }
            self.found_song.emit(song)
            songs.append(song)
        return songs

    def start(self):
        """
        Run a search and then parse the results page of the search.
        """
        songs = self._search_and_parse_results(self.params)
        search_results = []
        self.params['page'] = 1
        total = 0
        while songs:
            search_results.extend(songs)
            self.params['page'] += 1
            total += len(songs)
            if total >= 1000:
                self.show_info.emit(
                    translate('SongsPlugin.SongSelectForm', 'More than 1000 results'),
                    translate('SongsPlugin.SongSelectForm', 'Your search has returned more than 1000 results, it has '
                                                            'been stopped. Please refine your search to fetch better '
                                                            'results.'))
                break
            songs = self._search_and_parse_results(self.params)
        self.finished.emit(search_results)
        self.quit.emit()


class SongSelectForm(QtGui.QDialog, Ui_SongSelectDialog):
    """
    The :class:`SongSelectForm` class is the SongSelect dialog.
    """

    def __init__(self, parent=None, plugin=None, db_manager=None):
        QtGui.QDialog.__init__(self, parent)
        self.setup_ui(self)
        self.thread = None
        self.worker = None
        self.song_count = 0
        self.song = None
        self.plugin = plugin
        self.db_manager = db_manager
        self.html_parser = HTMLParser()
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()))
        self.opener.addheaders = [('User-Agent', USER_AGENT)]
        self.save_password_checkbox.toggled.connect(self.on_save_password_checkbox_toggled)
        self.login_button.clicked.connect(self.on_login_button_clicked)
        self.search_button.clicked.connect(self.on_search_button_clicked)
        self.search_combobox.returnPressed.connect(self.on_search_button_clicked)
        self.logout_button.clicked.connect(self.done)
        self.search_results_widget.itemDoubleClicked.connect(self.on_search_results_widget_double_clicked)
        self.search_results_widget.itemSelectionChanged.connect(self.on_search_results_widget_selection_changed)
        self.view_button.clicked.connect(self.on_view_button_clicked)
        self.back_button.clicked.connect(self.on_back_button_clicked)
        self.import_button.clicked.connect(self.on_import_button_clicked)

    def exec_(self):
        """
        Execute the dialog. This method sets everything back to its initial
        values.
        """
        self.stacked_widget.setCurrentIndex(0)
        self.username_edit.setEnabled(True)
        self.password_edit.setEnabled(True)
        self.save_password_checkbox.setEnabled(True)
        self.search_combobox.clearEditText()
        self.search_combobox.clear()
        self.search_results_widget.clear()
        self.view_button.setEnabled(False)
        if Settings().contains(self.plugin.settings_section + '/songselect password'):
            self.username_edit.setText(Settings().value(self.plugin.settings_section + '/songselect username'))
            self.password_edit.setText(Settings().value(self.plugin.settings_section + '/songselect password'))
            self.save_password_checkbox.setChecked(True)
        if Settings().contains(self.plugin.settings_section + '/songselect searches'):
            self.search_combobox.addItems(
                Settings().value(self.plugin.settings_section + '/songselect searches').split('|'))
        self.username_edit.setFocus()
        return QtGui.QDialog.exec_(self)

    def done(self, r):
        """
        Log out of SongSelect.

        :param r: The result of the dialog.
        """
        log.debug('Closing SongSelectForm')
        if self.stacked_widget.currentIndex() > 0:
            progress_dialog = QtGui.QProgressDialog(
                translate('SongsPlugin.SongSelectForm', 'Logging out...'), '', 0, 2, self)
            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
            progress_dialog.setCancelButton(None)
            progress_dialog.setValue(1)
            progress_dialog.show()
            progress_dialog.setFocus()
            self.main_window.application.process_events()
            sleep(0.5)
            self.main_window.application.process_events()
            self.opener.open(LOGOUT_URL)
            self.main_window.application.process_events()
            progress_dialog.setValue(2)
        return QtGui.QDialog.done(self, r)

    def _get_main_window(self):
        if not hasattr(self, '_main_window'):
            self._main_window = Registry().get('main_window')
        return self._main_window

    main_window = property(_get_main_window)

    def _view_song(self, current_item):
        if not current_item:
            return
        else:
            current_item = current_item.data(QtCore.Qt.UserRole)
        self.song_progress_bar.setVisible(True)
        self.import_button.setEnabled(False)
        self.back_button.setEnabled(False)
        self.title_edit.setText('')
        self.title_edit.setEnabled(False)
        self.copyright_edit.setText('')
        self.copyright_edit.setEnabled(False)
        self.ccli_edit.setText('')
        self.ccli_edit.setEnabled(False)
        self.author_list_widget.clear()
        self.author_list_widget.setEnabled(False)
        self.lyrics_table_widget.clear()
        self.lyrics_table_widget.setRowCount(0)
        self.lyrics_table_widget.setEnabled(False)
        self.stacked_widget.setCurrentIndex(2)
        song = {}
        for key, value in current_item.items():
            song[key] = value
        self.song_progress_bar.setValue(1)
        self.main_window.application.process_events()
        song_page = BeautifulSoup(self.opener.open(song['link']).read(), 'lxml')
        self.song_progress_bar.setValue(2)
        self.main_window.application.process_events()
        try:
            lyrics_page = BeautifulSoup(self.opener.open(song['link'] + '/lyrics').read(), 'lxml')
        except HTTPError:
            lyrics_page = None
        self.song_progress_bar.setValue(3)
        self.main_window.application.process_events()
        song['copyright'] = '/'.join([li.string for li in song_page.find('ul', 'copyright').find_all('li')])
        song['copyright'] = self.html_parser.unescape(song['copyright'])
        song['ccli_number'] = song_page.find('ul', 'info').find('li').string.split(':')[1].strip()
        song['verses'] = []
        if lyrics_page:
            verses = lyrics_page.find('section', 'lyrics').find_all('p')
            verse_labels = lyrics_page.find('section', 'lyrics').find_all('h3')
            for counter in range(len(verses)):
                verse = {'label': verse_labels[counter].string, 'lyrics': ''}
                for v in verses[counter].contents:
                    if isinstance(v, NavigableString):
                        verse['lyrics'] = verse['lyrics'] + v.string
                    else:
                        verse['lyrics'] += '\n'
                verse['lyrics'] = verse['lyrics'].strip(' \n\r\t')
                song['verses'].append(self.html_parser.unescape(verse))
        self.title_edit.setText(song['title'])
        self.copyright_edit.setText(song['copyright'])
        self.ccli_edit.setText(song['ccli_number'])
        for author in song['authors']:
            QtGui.QListWidgetItem(self.html_parser.unescape(author), self.author_list_widget)
        for counter, verse in enumerate(song['verses']):
            log.debug('Verse type: %s', verse['label'])
            self.lyrics_table_widget.setRowCount(self.lyrics_table_widget.rowCount() + 1)
            item = QtGui.QTableWidgetItem(verse['lyrics'])
            item.setData(QtCore.Qt.UserRole, verse['label'])
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.lyrics_table_widget.setItem(counter, 0, item)
        self.lyrics_table_widget.setVerticalHeaderLabels([verse['label'] for verse in song['verses']])
        self.lyrics_table_widget.resizeRowsToContents()
        self.title_edit.setEnabled(True)
        self.copyright_edit.setEnabled(True)
        self.ccli_edit.setEnabled(True)
        self.author_list_widget.setEnabled(True)
        self.lyrics_table_widget.setEnabled(True)
        self.lyrics_table_widget.repaint()
        self.import_button.setEnabled(True)
        self.back_button.setEnabled(True)
        self.song_progress_bar.setVisible(False)
        self.song_progress_bar.setValue(0)
        self.song = song
        self.main_window.application.process_events()

    def on_save_password_checkbox_toggled(self, checked):
        """
        Show a warning dialog when the user toggles the save checkbox on or off.

        :param checked: If the combobox is checked or not
        """
        if checked and self.login_page.isVisible():
            answer = QtGui.QMessageBox.question(
                self, translate('SongsPlugin.SongSelectForm', 'Save Username and Password'),
                translate('SongsPlugin.SongSelectForm', 'WARNING: Saving your username and password is INSECURE, your '
                                                        'password is stored in PLAIN TEXT. Click Yes to save your '
                                                        'password or No to cancel this.'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No), QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.No:
                self.save_password_checkbox.setChecked(False)

    def on_login_button_clicked(self):
        """
        Log the user in to SongSelect.
        """
        self.username_edit.setEnabled(False)
        self.password_edit.setEnabled(False)
        self.save_password_checkbox.setEnabled(False)
        self.login_button.setEnabled(False)
        self.login_spacer.setVisible(False)
        self.login_progress_bar.setVisible(True)
        self.login_progress_bar.setValue(1)
        self.main_window.application.process_events()
        login_page = BeautifulSoup(self.opener.open(LOGIN_URL).read(), 'lxml')
        self.login_progress_bar.setValue(2)
        self.main_window.application.process_events()
        token_input = login_page.find('input', attrs={'name': '__RequestVerificationToken'})
        data = urlencode({
            '__RequestVerificationToken': token_input['value'],
            'UserName': self.username_edit.text(),
            'Password': self.password_edit.text(),
            'RememberMe': 'false'
        })
        posted_page = BeautifulSoup(self.opener.open(LOGIN_URL, data.encode('utf-8')).read(), 'lxml')
        self.login_progress_bar.setValue(3)
        self.main_window.application.process_events()
        if posted_page.find('input', attrs={'name': '__RequestVerificationToken'}):
            QtGui.QMessageBox.critical(
                self,
                translate('SongsPlugin.SongSelectForm', 'Error Logging In'),
                translate('SongsPlugin.SongSelectForm',
                          'There was a problem logging in, perhaps your username or password is incorrect?')
            )
        else:
            if self.save_password_checkbox.isChecked():
                Settings().setValue(self.plugin.settings_section + '/songselect username', self.username_edit.text())
                Settings().setValue(self.plugin.settings_section + '/songselect password', self.password_edit.text())
            else:
                Settings().remove(self.plugin.settings_section + '/songselect username')
                Settings().remove(self.plugin.settings_section + '/songselect password')
            self.stacked_widget.setCurrentIndex(1)
        self.login_progress_bar.setVisible(False)
        self.login_progress_bar.setValue(0)
        self.login_spacer.setVisible(True)
        self.login_button.setEnabled(True)
        self.search_combobox.setFocus()
        self.main_window.application.process_events()

    def on_search_button_clicked(self):
        """
        Run a search on SongSelect.
        """
        self.view_button.setEnabled(False)
        self.search_button.setEnabled(False)
        self.search_progress_bar.setVisible(True)
        self.search_progress_bar.setMinimum(0)
        self.search_progress_bar.setMaximum(0)
        self.search_progress_bar.setValue(0)
        self.search_results_widget.clear()
        self.result_count_label.setText(translate('SongsPlugin.SongSelectForm', 'Found %s song(s)') % self.song_count)
        self.main_window.application.process_events()
        self.song_count = 0
        search_history = self.search_combobox.getItems()
        Settings().setValue(self.plugin.settings_section + '/songselect searches', '|'.join(search_history))

        # Create thread and run search
        self.thread = QtCore.QThread()
        self.worker = SearchWorker(self.opener, {'SearchTerm': self.search_combobox.currentText(),
                                                 'allowredirect': 'false'})
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.start)
        self.worker.show_info.connect(self.on_search_show_info)
        self.worker.found_song.connect(self.on_search_found_song)
        self.worker.finished.connect(self.on_search_finished)
        self.worker.quit.connect(self.thread.quit)
        self.worker.quit.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def on_search_show_info(self, title, message):
        """
        Show an informational message from the search thread
        :param title:
        :param message:
        """
        QtGui.QMessageBox.information(self, title, message)

    def on_search_found_song(self, song):
        """
        Add a song to the list when one is found.
        :param song:
        """
        log.debug('SongSelect (title = "%s"), (link = "%s")', song['title'], song['link'])
        self.song_count += 1
        self.result_count_label.setText(translate('SongsPlugin.SongSelectForm', 'Found %s song(s)') % self.song_count)
        item_title = song['title'] + ' (' + ', '.join(song['authors']) + ')'
        song_item = QtGui.QListWidgetItem(item_title, self.search_results_widget)
        song_item.setData(QtCore.Qt.UserRole, song)

    def on_search_finished(self, songs):
        """
        Slot which is called when the search is completed.
        :param songs:
        """
        self.main_window.application.process_events()
        self.search_progress_bar.setVisible(False)
        self.search_button.setEnabled(True)
        self.main_window.application.process_events()

    def on_search_results_widget_selection_changed(self):
        """
        Enable or disable the view button when the selection changes.
        """
        self.view_button.setEnabled(len(self.search_results_widget.selectedItems()) > 0)

    def on_view_button_clicked(self):
        """
        View a song from SongSelect.
        """
        self._view_song(self.search_results_widget.currentItem())

    def on_search_results_widget_double_clicked(self, current_item):
        """
        View a song from SongSelect
        :param current_item:
        """
        self._view_song(current_item)

    def on_back_button_clicked(self):
        """
        Go back to the search page.
        """
        self.stacked_widget.setCurrentIndex(1)
        self.search_combobox.setFocus()

    def on_import_button_clicked(self):
        """
        Import a song from SongSelect.
        """
        song = Song.populate(
            title=self.song['title'],
            copyright=self.song['copyright'],
            ccli_number=self.song['ccli_number']
        )
        song_xml = SongXML()
        verse_order = []
        for verse in self.song['verses']:
            verse_type, verse_number = verse['label'].split(' ')[:2]
            verse_type = VerseType.from_loose_input(verse_type)
            verse_number = int(verse_number)
            song_xml.add_verse_to_lyrics(
                VerseType.tags[verse_type],
                verse_number,
                verse['lyrics']
            )
            verse_order.append('%s%s' % (VerseType.tags[verse_type], verse_number))
        song.verse_order = ' '.join(verse_order)
        song.lyrics = song_xml.extract_xml()
        clean_song(self.db_manager, song)
        self.db_manager.save_object(song)
        song.authors = []
        for author_name in self.song['authors']:
            #author_name = unicode(author_name)
            author = self.db_manager.get_object_filtered(Author, Author.display_name == author_name)
            if not author:
                author = Author.populate(
                    first_name=author_name.rsplit(' ', 1)[0],
                    last_name=author_name.rsplit(' ', 1)[1],
                    display_name=author_name
                )
            song.authors.append(author)
        self.db_manager.save_object(song)
        question_dialog = QtGui.QMessageBox()
        question_dialog.setWindowTitle(translate('SongsPlugin.SongSelectForm', 'Song Imported'))
        question_dialog.setText(translate('SongsPlugin.SongSelectForm', 'Your song has been imported, would you like '
                                                                        'to exit now, or import more songs?'))
        question_dialog.addButton(QtGui.QPushButton(translate('SongsPlugin.SongSelectForm', 'Import More Songs')),
                                  QtGui.QMessageBox.YesRole)
        question_dialog.addButton(QtGui.QPushButton(translate('SongsPlugin.SongSelectForm', 'Exit Now')),
                                  QtGui.QMessageBox.NoRole)
        if question_dialog.exec_() == QtGui.QMessageBox.Yes:
            self.on_back_button_clicked()
        else:
            self.main_window.application.process_events()
            self.done(QtGui.QDialog.Accepted)
