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
The :mod:`cvsbible` modules provides a facility to import bibles from a set of CSV files.

The module expects two mandatory files containing the books and the verses.

The format of the books file is:

    <book_id>,<testament_id>,<book_name>,<book_abbreviation>

    For example

        1,1,Genesis,Gen
        2,1,Exodus,Exod
        ...
        40,2,Matthew,Matt

There are two acceptable formats of the verses file.  They are:

    <book_id>,<chapter_number>,<verse_number>,<verse_text>
    or
    <book_name>,<chapter_number>,<verse_number>,<verse_text>

    For example:

        1,1,1,"In the beginning God created the heaven and the earth."
        or
        "Genesis",1,2,"And the earth was without form, and void; and...."

All CSV files are expected to use a comma (',') as the delimiter and double quotes ('"') as the quote symbol.
"""
import csv
from collections import namedtuple

from openlp.core.common import get_file_encoding, translate
from openlp.core.lib.exceptions import ValidationError
from openlp.plugins.bibles.lib.bibleimport import BibleImport


Book = namedtuple('Book', 'id, testament_id, name, abbreviation')
Verse = namedtuple('Verse', 'book_id_name, chapter_number, number, text')


class CSVBible(BibleImport):
    """
    This class provides a specialisation for importing of CSV Bibles.
    """
    def __init__(self, *args, **kwargs):
        """
        Loads a Bible from a set of CSV files. This class assumes the files contain all the information and a clean
        bible is being loaded.
        """
        super().__init__(*args, **kwargs)
        self.log_info(self.__class__.__name__)
        self.books_file = kwargs['booksfile']
        self.verses_file = kwargs['versefile']

    @staticmethod
    def get_book_name(name, books):
        """
        Normalize a book name or id.

        :param name: The name, or id of a book. Str
        :param books: A dict of books parsed from the books file.
        :return: The normalized name. Str
        """
        try:
            book_name = books[int(name)]
        except ValueError:
            book_name = name
        return book_name

    @staticmethod
    def parse_csv_file(filename, results_tuple):
        """
        Parse the supplied CSV file.

        :param filename: The name of the file to parse. Str
        :param results_tuple: The namedtuple to use to store the results. namedtuple
        :return: An iterable yielding namedtuples of type results_tuple
        """
        try:
            encoding = get_file_encoding(filename)['encoding']
            with open(filename, 'r', encoding=encoding, newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
                return [results_tuple(*line) for line in csv_reader]
        except (OSError, csv.Error):
            raise ValidationError(msg='Parsing "{file}" failed'.format(file=filename))

    def process_books(self, books):
        """
        Process the books parsed from the books file.

        :param books: An a list Book namedtuples
        :return: A dict of books or None
        """
        book_list = {}
        number_of_books = len(books)
        for book in books:
            if self.stop_import_flag:
                break
            self.wizard.increment_progress_bar(
                translate('BiblesPlugin.CSVBible', 'Importing books... {book}').format(book=book.name))
            self.find_and_create_book(book.name, number_of_books, self.language_id)
            book_list.update({int(book.id): book.name})
        return book_list

    def process_verses(self, verses, books):
        """
        Process the verses parsed from the verses file.

        :param verses: A list of Verse namedtuples
        :param books: A dict of books
        :return: None
        """
        book_ptr = None
        for verse in verses:
            if self.stop_import_flag:
                break
            verse_book = self.get_book_name(verse.book_id_name, books)
            if book_ptr != verse_book:
                book = self.get_book(verse_book)
                book_ptr = book.name
                self.wizard.increment_progress_bar(
                    translate('BiblesPlugin.CSVBible', 'Importing verses from {book}...',
                              'Importing verses from <book name>...').format(book=book.name))
                self.session.commit()
            self.create_verse(book.id, int(verse.chapter_number), int(verse.number), verse.text)
        self.session.commit()

    def do_import(self, bible_name=None):
        """
        Import a bible from the CSV files.

        :param bible_name: Optional name of the bible being imported. Str or None
        :return: True if the import was successful, False if it failed or was cancelled
        """
        self.language_id = self.get_language(bible_name)
        if not self.language_id:
            return False
        books = self.parse_csv_file(self.books_file, Book)
        self.wizard.progress_bar.setValue(0)
        self.wizard.progress_bar.setMinimum(0)
        self.wizard.progress_bar.setMaximum(len(books))
        book_list = self.process_books(books)
        verses = self.parse_csv_file(self.verses_file, Verse)
        self.wizard.progress_bar.setValue(0)
        self.wizard.progress_bar.setMaximum(len(books) + 1)
        self.process_verses(verses, book_list)
        return True
