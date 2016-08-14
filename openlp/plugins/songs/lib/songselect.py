# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
The :mod:`~openlp.plugins.songs.lib.songselect` module contains the SongSelect importer itself.
"""
import logging
import random
import re
from http.cookiejar import CookieJar
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, URLError, build_opener
from html.parser import HTMLParser
from html import unescape

from bs4 import BeautifulSoup, NavigableString

from openlp.plugins.songs.lib import Song, Author, Topic, VerseType, clean_song
from openlp.plugins.songs.lib.openlyricsxml import SongXML

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/52.0.2743.116 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
]
BASE_URL = 'https://songselect.ccli.com'
LOGIN_PAGE = 'https://profile.ccli.com/account/signin?appContext=SongSelect&returnUrl='\
    'https%3a%2f%2fsongselect.ccli.com%2f'
LOGIN_URL = 'https://profile.ccli.com/'
LOGOUT_URL = BASE_URL + '/account/logout'
SEARCH_URL = BASE_URL + '/search/results'

log = logging.getLogger(__name__)


class SongSelectImport(object):
    """
    The :class:`~openlp.plugins.songs.lib.songselect.SongSelectImport` class contains all the code which interfaces
    with CCLI's SongSelect service and downloads the songs.
    """
    def __init__(self, db_manager):
        """
        Set up the song select importer

        :param db_manager: The song database manager
        """
        self.db_manager = db_manager
        self.html_parser = HTMLParser()
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()))
        self.opener.addheaders = [('User-Agent', random.choice(USER_AGENTS))]
        self.run_search = True

    def login(self, username, password, callback=None):
        """
        Log the user into SongSelect. This method takes a username and password, and runs ``callback()`` at various
        points which can be used to give the user some form of feedback.

        :param username: SongSelect username
        :param password: SongSelect password
        :param callback: Method to notify of progress.
        :return: True on success, False on failure.
        """
        if callback:
            callback()
        try:
            login_page = BeautifulSoup(self.opener.open(LOGIN_PAGE).read(), 'lxml')
        except (TypeError, URLError) as error:
            log.exception('Could not login to SongSelect, {error}'.format(error=error))
            return False
        if callback:
            callback()
        token_input = login_page.find('input', attrs={'name': '__RequestVerificationToken'})
        data = urlencode({
            '__RequestVerificationToken': token_input['value'],
            'emailAddress': username,
            'password': password,
            'RememberMe': 'false'
        })
        try:
            posted_page = BeautifulSoup(self.opener.open(LOGIN_URL, data.encode('utf-8')).read(), 'lxml')
        except (TypeError, URLError) as error:
            log.exception('Could not login to SongSelect, {error}'.format(error=error))
            return False
        if callback:
            callback()
        return posted_page.find('input', id='SearchText') is not None

    def logout(self):
        """
        Log the user out of SongSelect
        """
        try:
            self.opener.open(LOGOUT_URL)
        except (TypeError, URLError) as error:
            log.exception('Could not log of SongSelect, {error}'.format(error=error))

    def search(self, search_text, max_results, callback=None):
        """
        Set up a search.

        :param search_text: The text to search for.
        :param max_results: Maximum number of results to fetch.
        :param callback: A method which is called when each song is found, with the song as a parameter.
        :return: List of songs
        """
        self.run_search = True
        params = {
            'SongContent': '',
            'PrimaryLanguage': '',
            'Keys': '',
            'Themes': '',
            'List': '',
            'Sort': '',
            'SearchText': search_text
        }
        current_page = 1
        songs = []
        while self.run_search:
            if current_page > 1:
                params['page'] = current_page
            try:
                results_page = BeautifulSoup(self.opener.open(SEARCH_URL + '?' + urlencode(params)).read(), 'lxml')
                search_results = results_page.find_all('div', 'song-result')
            except (TypeError, URLError) as error:
                log.exception('Could not search SongSelect, {error}'.format(error=error))
                search_results = None
            if not search_results:
                break
            for result in search_results:
                song = {
                    'title': unescape(result.find('p', 'song-result-title').find('a').string).strip(),
                    'authors': unescape(result.find('p', 'song-result-subtitle').string).strip().split(', '),
                    'link': BASE_URL + result.find('p', 'song-result-title').find('a')['href']
                }
                if callback:
                    callback(song)
                songs.append(song)
                if len(songs) >= max_results:
                    break
            current_page += 1
        return songs

    def get_song(self, song, callback=None):
        """
        Get the full song from SongSelect

        :param song: The song dictionary to update
        :param callback: A callback which can be used to indicate progress
        :return: The updated song dictionary
        """
        if callback:
            callback()
        try:
            song_page = BeautifulSoup(self.opener.open(song['link']).read(), 'lxml')
        except (TypeError, URLError) as error:
            log.exception('Could not get song from SongSelect, {error}'.format(error=error))
            return None
        if callback:
            callback()
        try:
            lyrics_page = BeautifulSoup(self.opener.open(song['link'] + '/viewlyrics').read(), 'lxml')
        except (TypeError, URLError):
            log.exception('Could not get lyrics from SongSelect')
            return None
        if callback:
            callback()
        copyright_elements = []
        theme_elements = []
        copyrights_regex = re.compile(r'\bCopyrights\b')
        themes_regex = re.compile(r'\bThemes\b')
        for ul in song_page.find_all('ul', 'song-meta-list'):
            if ul.find('li', string=copyrights_regex):
                copyright_elements.extend(ul.find_all('li')[1:])
            if ul.find('li', string=themes_regex):
                theme_elements.extend(ul.find_all('li')[1:])
        song['copyright'] = '/'.join([unescape(li.string).strip() for li in copyright_elements])
        song['topics'] = [unescape(li.string).strip() for li in theme_elements]
        song['ccli_number'] = song_page.find('div', 'song-content-data').find('ul').find('li')\
            .find('strong').string.strip()
        song['verses'] = []
        verses = lyrics_page.find('div', 'song-viewer lyrics').find_all('p')
        verse_labels = lyrics_page.find('div', 'song-viewer lyrics').find_all('h3')
        for verse, label in zip(verses, verse_labels):
            song_verse = {'label': unescape(label.string).strip(), 'lyrics': ''}
            for v in verse.contents:
                if isinstance(v, NavigableString):
                    song_verse['lyrics'] += unescape(v.string).strip()
                else:
                    song_verse['lyrics'] += '\n'
            song_verse['lyrics'] = song_verse['lyrics'].strip(' \n\r\t')
            song['verses'].append(song_verse)
        for counter, author in enumerate(song['authors']):
            song['authors'][counter] = unescape(author)
        return song

    def save_song(self, song):
        """
        Save a song to the database, using the db_manager

        :param song:
        :return:
        """
        db_song = Song.populate(title=song['title'], copyright=song['copyright'], ccli_number=song['ccli_number'])
        song_xml = SongXML()
        verse_order = []
        for verse in song['verses']:
            if ' ' in verse['label']:
                verse_type, verse_number = verse['label'].split(' ', 1)
            else:
                verse_type = verse['label']
                verse_number = 1
            verse_type = VerseType.from_loose_input(verse_type)
            verse_number = int(verse_number)
            song_xml.add_verse_to_lyrics(VerseType.tags[verse_type], verse_number, verse['lyrics'])
            verse_order.append('{tag}{number}'.format(tag=VerseType.tags[verse_type], number=verse_number))
        db_song.verse_order = ' '.join(verse_order)
        db_song.lyrics = song_xml.extract_xml()
        clean_song(self.db_manager, db_song)
        self.db_manager.save_object(db_song)
        db_song.authors_songs = []
        for author_name in song['authors']:
            author = self.db_manager.get_object_filtered(Author, Author.display_name == author_name)
            if not author:
                name_parts = author_name.rsplit(' ', 1)
                first_name = name_parts[0]
                if len(name_parts) == 1:
                    last_name = ''
                else:
                    last_name = name_parts[1]
                author = Author.populate(first_name=first_name, last_name=last_name, display_name=author_name)
            db_song.add_author(author)
        for topic_name in song.get('topics', []):
            topic = self.db_manager.get_object_filtered(Topic, Topic.name == topic_name)
            if not topic:
                topic = Topic.populate(name=topic_name)
            db_song.topics.append(topic)
        self.db_manager.save_object(db_song)
        return db_song

    def stop(self):
        """
        Stop the search.
        """
        self.run_search = False
