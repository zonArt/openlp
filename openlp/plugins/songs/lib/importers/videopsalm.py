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
The :mod:`lyrix` module provides the functionality for importing songs which are
exproted from Lyrix."""

import logging
import json
import os

from openlp.core.common import translate
from openlp.plugins.songs.lib.importers.songimport import SongImport
from openlp.plugins.songs.lib.db import AuthorType

log = logging.getLogger(__name__)


class VideoPsalmImport(SongImport):
    """
    Import songs exported from Lyrix
    """

    def __init__(self, manager, **kwargs):
        """
        Initialise the class.
        """
        super(VideoPsalmImport, self).__init__(manager, **kwargs)

    def do_import(self):
        """
        Process the VideoPsalm file - pass in a file-like object, not a file path.
        """
        self.set_defaults()
        # Open SongBook file
        song_file = open(self.import_source, 'rt', encoding='utf-8-sig')
        try:
            file_content = song_file.read()
            processed_content = ''
            inside_quotes = False
            # The VideoPsalm format is not valid json, it uses illegal line breaks and unquoted keys, this must be fixed
            file_content_it = iter(file_content)
            for c in file_content_it:
                if c == '"':
                    inside_quotes = not inside_quotes
                # Detect invalid linebreak
                if c == '\n':
                    if inside_quotes:
                        processed_content += '\\n'
                # Put keys in quotes
                elif c.isalnum() and not inside_quotes:
                    processed_content += '"' + c
                    c = next(file_content_it)
                    while c.isalnum():
                        processed_content += c
                        c = next(file_content_it)
                    processed_content += '"' + c
                else:
                    processed_content += c
            songbook = json.loads(processed_content.strip())
            # Get song array
            songs = songbook['Songs']
            self.import_wizard.progress_bar.setMaximum(len(songs))
            songbook_name = songbook['Text']
            media_folder = os.path.normpath(os.path.join(os.path.dirname(song_file.name), '..', 'Audio'))
            for song in songs:
                self.song_book_name = songbook_name
                if 'Text' in song:
                    self.title = song['Text']
                composer = None
                author = None
                if 'Composer' in song:
                    composer = song['Composer']
                if 'Author' in song:
                    author = song['Author']
                if author and composer == author:
                    self.add_author(author, AuthorType.WordsAndMusic)
                else:
                    if author:
                        self.add_author(author, AuthorType.Words)
                    if composer:
                        self.add_author(composer, AuthorType.Music)
                if 'Copyright' in song:
                    self.add_copyright(song['Copyright'].replace('\n', ' ').strip())
                if 'CCLI' in song:
                    self.ccli_number = song['CCLI']
                if 'Theme' in song:
                    self.topics = song['Theme'].splitlines()
                if 'AudioFile' in song:
                    self.add_media_file(os.path.join(media_folder, song['AudioFile']))
                if 'Memo1' in song:
                    self.add_comment(song['Memo1'])
                if 'Memo2' in song:
                    self.add_comment(song['Memo2'])
                if 'Memo3' in song:
                    self.add_comment(song['Memo3'])
                for verse in song['Verses']:
                    self.add_verse(verse['Text'], 'v')
                if not self.finish():
                    self.log_error('Could not import %s' % self.title)
        except Exception as e:
            self.log_error(song_file.name, translate('SongsPlugin.VideoPsalmImport', 'Error: %s') % e)
        song_file.close()
