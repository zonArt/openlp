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

from lxml import etree, objectify
from zipfile import is_zipfile

from openlp.core.common import OpenLPMixin, Registry, RegistryProperties, languages, translate
from openlp.core.lib import ValidationError
from openlp.core.lib.ui import critical_error_message_box
from openlp.plugins.bibles.lib.db import AlternativeBookNamesDB, BibleDB, BiblesResourcesDB


class BibleImport(OpenLPMixin, RegistryProperties, BibleDB):
    """
    Helper class to import bibles from a third party source into OpenLP
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = kwargs['filename'] if 'filename' in kwargs else None
        self.wizard = None
        self.stop_import_flag = False
        Registry().register_function('openlp_stop_wizard', self.stop_import)

    @staticmethod
    def is_compressed(file):
        """
        Check if the supplied file is compressed

        :param file: A path to the file to check
        """
        if is_zipfile(file):
            critical_error_message_box(
                message=translate('BiblesPlugin.BibleImport',
                                  'The file "{file}" you supplied is compressed. You must decompress it before import.'
                                  ).format(file=file))
            return True
        return False

    def get_book_ref_id_by_name(self, book, maxbooks, language_id=None):
        self.log_debug('BibleDB.get_book_ref_id_by_name:("{book}", "{lang}")'.format(book=book, lang=language_id))
        book_id = None
        if BiblesResourcesDB.get_book(book, True):
            book_temp = BiblesResourcesDB.get_book(book, True)
            book_id = book_temp['id']
        elif BiblesResourcesDB.get_alternative_book_name(book):
            book_id = BiblesResourcesDB.get_alternative_book_name(book)
        elif AlternativeBookNamesDB.get_book_reference_id(book):
            book_id = AlternativeBookNamesDB.get_book_reference_id(book)
        else:
            from openlp.plugins.bibles.forms import BookNameForm
            book_name = BookNameForm(self.wizard)
            if book_name.exec(book, self.get_books(), maxbooks):
                book_id = book_name.book_id
            if book_id:
                AlternativeBookNamesDB.create_alternative_book_name(
                    book, book_id, language_id)
        return book_id

    def get_language(self, bible_name=None):
        """
        If no language is given it calls a dialog window where the user could  select the bible language.
        Return the language id of a bible.

        :param bible_name: The language the bible is.
        """
        self.log_debug('BibleImpoer.get_language()')
        from openlp.plugins.bibles.forms import LanguageForm
        language_id = None
        language_form = LanguageForm(self.wizard)
        if language_form.exec(bible_name):
            combo_box = language_form.language_combo_box
            language_id = combo_box.itemData(combo_box.currentIndex())
        if not language_id:
            return None
        self.save_meta('language_id', language_id)
        return language_id

    def get_language_id(self, file_language=None, bible_name=None):
        """
        Get the language_id for the language of the bible. Fallback to user input if we cannot do this pragmatically.

        :param file_language: Language of the bible. Possibly retrieved from the file being imported. Str
        :param bible_name: Name of the bible to display on the get_language dialog. Str
        :return: The id of a language Int or None
        """
        language_id = None
        if file_language:
            language = languages.get_language(file_language)
            if language and language.id:
                language_id = language.id
        if not language_id:
            # The language couldn't be detected, ask the user
            language_id = self.get_language(bible_name)
        if not language_id:
            # User cancelled get_language dialog
            self.log_error('Language detection failed when importing from "{name}". User aborted language selection.'
                           .format(name=bible_name))
            return None
        self.save_meta('language_id', language_id)
        return language_id

    def find_and_create_book(self, name, no_of_books, language_id, guess_id=None):
        """
        Find the OpenLP book id and then create the book in this bible db

        :param name: Name of the book. If None, then fall back to the guess_id Str
        :param no_of_books: The total number of books contained in this bible Int
        :param language_id: The OpenLP id of the language of this bible Int
        :param guess_id: The guessed id of the book, used if name is None Int
        :return:
        """
        if name:
            book_ref_id = self.get_book_ref_id_by_name(name, no_of_books, language_id)
        else:
            self.log_debug('No book name supplied. Falling back to guess_id')
            book_ref_id = guess_id
        if not book_ref_id:
            raise ValidationError(msg='Could not resolve book_ref_id in "{}"'.format(self.filename))
        book_details = BiblesResourcesDB.get_book_by_id(book_ref_id)
        if book_details is None:
            raise ValidationError(msg='book_ref_id: {book_ref} Could not be found in the BibleResourcesDB while '
                                      'importing {file}'.format(book_ref=book_ref_id, file=self.filename))
        return self.create_book(name, book_ref_id, book_details['testament_id'])

    def parse_xml(self, filename, use_objectify=False, elements=None, tags=None):
        """
        Parse and clean the supplied file by removing any elements or tags we don't use.
        :param filename: The filename of the xml file to parse. Str
        :param use_objectify: Use the objectify parser rather than the etree parser. (Bool)
        :param elements: A tuple of element names (Str) to remove along with their content.
        :param tags: A tuple of element names (Str) to remove, preserving their content.
        :return: The root element of the xml document
        """
        try:
            with open(filename, 'rb') as import_file:
                # NOTE: We don't need to do any of the normal encoding detection here, because lxml does it's own
                # encoding detection, and the two mechanisms together interfere with each other.
                if not use_objectify:
                    tree = etree.parse(import_file, parser=etree.XMLParser(recover=True))
                else:
                    tree = objectify.parse(import_file, parser=objectify.makeparser(recover=True))
                if elements or tags:
                    self.wizard.increment_progress_bar(
                        translate('BiblesPlugin.OsisImport', 'Removing unused tags (this may take a few minutes)...'))
                if elements:
                    # Strip tags we don't use - remove content
                    etree.strip_elements(tree, elements, with_tail=False)
                if tags:
                    # Strip tags we don't use - keep content
                    etree.strip_tags(tree, tags)
                return tree.getroot()
        except OSError as e:
            self.log_exception('Opening {file_name} failed.'.format(file_name=e.filename))
            critical_error_message_box(
                title='An Error Occured When Opening A File',
                message='The following error occurred when trying to open\n{file_name}:\n\n{error}'
                .format(file_name=e.filename, error=e.strerror))
        return None

    def register(self, wizard):
        """
        This method basically just initialises the database. It is called from the Bible Manager when a Bible is
        imported. Descendant classes may want to override this method to supply their own custom
        initialisation as well.

        :param wizard: The actual Qt wizard form.
        """
        self.wizard = wizard
        return self.name

    def set_current_chapter(self, book_name, chapter_name):
        self.wizard.increment_progress_bar(translate('BiblesPlugin.OsisImport', 'Importing {book} {chapter}...')
                                           .format(book=book_name, chapter=chapter_name))

    def stop_import(self):
        """
        Stops the import of the Bible.
        """
        self.log_debug('Stopping import')
        self.stop_import_flag = True

    def validate_xml_file(self, filename, tag):
        """
        Validate the supplied file

        :param filename: The supplied file
        :param tag: The expected root tag type
        :return: True if valid. ValidationError is raised otherwise.
        """
        if BibleImport.is_compressed(filename):
            raise ValidationError(msg='Compressed file')
        bible = self.parse_xml(filename, use_objectify=True)
        if bible is None:
            raise ValidationError(msg='Error when opening file')
        root_tag = bible.tag.lower()
        bible_type = translate('BiblesPlugin.BibleImport', 'unknown type of',
                               'This looks like an unknown type of XML bible.')
        if root_tag == tag:
            return True
        elif root_tag == 'bible':
            bible_type = "OpenSong"
        elif root_tag == '{http://www.bibletechnologies.net/2003/osis/namespace}osis':
            bible_type = 'OSIS'
        elif root_tag == 'xmlbible':
            bible_type = 'Zefania'
        critical_error_message_box(
            message=translate('BiblesPlugin.BibleImport',
                              'Incorrect Bible file type supplied. This looks like an {bible_type} XML bible.'
                              .format(bible_type=bible_type)))
        raise ValidationError(msg='Invalid xml.')
