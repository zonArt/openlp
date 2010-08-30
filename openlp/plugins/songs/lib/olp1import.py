# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
The :mod:`olp1import` module provides the functionality for importing
openlp.org 1.x song databases into the current installation database.
"""
import logging
import sqlite

#from openlp.core.lib.db import BaseModel
from openlp.plugins.songs.lib.db import Author, Book, Song, Topic #, MediaFile
from songimport import SongImport

log = logging.getLogger(__name__)

class OpenLP1SongImport(SongImport):
    """
    The :class:`OpenLP1SongImport` class provides OpenLP with the ability to
    import song databases from installations of openlp.org 1.x.
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the import.

        ``manager``
            The song manager for the running OpenLP installation.

        ``filename``
            The database providing the data to import.
        """
        SongImport.__init__(self, manager)
        self.manager = manager
        self.import_source = kwargs[u'filename']

    def do_import(self):
        """
        Run the import for an openlp.org 1.x song database.
        """
        connection = sqlite.connect(self.import_source)
        cursor = connection.cursor()

#        for song in source_songs:
#            new_song = Song()
#            new_song.title = song.title
#            if has_media_files:
#                new_song.alternate_title = song.alternate_title
#            else:
#                old_titles = song.search_title.split(u'@')
#                if len(old_titles) > 1:
#                    new_song.alternate_title = old_titles[1]
#                else:
#                    new_song.alternate_title = u''
#            new_song.search_title = song.search_title
#            new_song.song_number = song.song_number
#            new_song.lyrics = song.lyrics
#            new_song.search_lyrics = song.search_lyrics
#            new_song.verse_order = song.verse_order
#            new_song.copyright = song.copyright
#            new_song.comments = song.comments
#            new_song.theme_name = song.theme_name
#            new_song.ccli_number = song.ccli_number
#            if song.authors:
#                for author in song.authors:
#                    existing_author = self.master_manager.get_object_filtered(
#                        Author, Author.display_name == author.display_name)
#                    if existing_author:
#                        new_song.authors.append(existing_author)
#                    else:
#                        new_song.authors.append(Author.populate(
#                            first_name=author.first_name,
#                            last_name=author.last_name,
#                            display_name=author.display_name))
#            else:
#                au = self.master_manager.get_object_filtered(Author,
#                    Author.display_name == u'Author Unknown')
#                if au:
#                    new_song.authors.append(au)
#                else:
#                    new_song.authors.append(Author.populate(
#                        display_name=u'Author Unknown'))
#            if song.book:
#                existing_song_book = self.master_manager.get_object_filtered(
#                    Book, Book.name == song.book.name)
#                if existing_song_book:
#                    new_song.book = existing_song_book
#                else:
#                    new_song.book = Book.populate(name=song.book.name,
#                        publisher=song.book.publisher)
#            if song.topics:
#                for topic in song.topics:
#                    existing_topic = self.master_manager.get_object_filtered(
#                        Topic, Topic.name == topic.name)
#                    if existing_topic:
#                        new_song.topics.append(existing_topic)
#                    else:
#                        new_song.topics.append(Topic.populate(name=topic.name))
##            if has_media_files:
##                if song.media_files:
##                    for media_file in song.media_files:
##                        existing_media_file = \
##                            self.master_manager.get_object_filtered(MediaFile,
##                                MediaFile.file_name == media_file.file_name)
##                        if existing_media_file:
##                            new_song.media_files.append(existing_media_file)
##                        else:
##                            new_song.media_files.append(MediaFile.populate(
##                                file_name=media_file.file_name))
#            self.master_manager.save_object(new_song)
