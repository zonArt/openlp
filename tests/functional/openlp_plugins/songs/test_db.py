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
This module contains tests for the db submodule of the Songs plugin.
"""
from unittest import TestCase

from openlp.plugins.songs.lib.db import Song, Author, AuthorType


class TestDB(TestCase):
    """
    Test the functions in the :mod:`db` module.
    """

    def test_add_author(self):
        """
        Test adding an author to a song
        """
        # GIVEN: A song and an author
        song = Song()
        song.authors_songs = []
        author = Author()
        author.first_name = "Max"
        author.last_name = "Mustermann"

        # WHEN: We add an author to the song
        song.add_author(author)

        # THEN: The author should have been added with author_type=None
        self.assertEqual(1, len(song.authors_songs))
        self.assertEqual("Max", song.authors_songs[0].author.first_name)
        self.assertEqual("Mustermann", song.authors_songs[0].author.last_name)
        self.assertIsNone(song.authors_songs[0].author_type)

    def test_add_author_with_type(self):
        """
        Test adding an author with a type specified to a song
        """
        # GIVEN: A song and an author
        song = Song()
        song.authors_songs = []
        author = Author()
        author.first_name = "Max"
        author.last_name = "Mustermann"

        # WHEN: We add an author to the song
        song.add_author(author, AuthorType.Words)

        # THEN: The author should have been added with author_type=None
        self.assertEqual(1, len(song.authors_songs))
        self.assertEqual("Max", song.authors_songs[0].author.first_name)
        self.assertEqual("Mustermann", song.authors_songs[0].author.last_name)
        self.assertEqual(AuthorType.Words, song.authors_songs[0].author_type)

    def test_remove_author(self):
        """
        Test removing an author from a song
        """
        # GIVEN: A song with an author
        song = Song()
        song.authors_songs = []
        author = Author()
        song.add_author(author)

        # WHEN: We remove the author
        song.remove_author(author)

        # THEN: It should have been removed
        self.assertEqual(0, len(song.authors_songs))

    def test_remove_author_with_type(self):
        """
        Test removing an author with a type specified from a song
        """
        # GIVEN: A song with two authors
        song = Song()
        song.authors_songs = []
        author = Author()
        song.add_author(author)
        song.add_author(author, AuthorType.Translation)

        # WHEN: We remove the author with a certain type
        song.remove_author(author, AuthorType.Translation)

        # THEN: It should have been removed and the other author should still be there
        self.assertEqual(1, len(song.authors_songs))
        self.assertEqual(None, song.authors_songs[0].author_type)

    def test_get_author_type_from_translated_text(self):
        """
        Test getting an author type from translated text
        """
        # GIVEN: A string with an author type
        author_type_name = AuthorType.Types[AuthorType.Words]

        # WHEN: We call the method
        author_type = AuthorType.from_translated_text(author_type_name)

        # THEN: The type should be correct
        self.assertEqual(author_type, AuthorType.Words)
