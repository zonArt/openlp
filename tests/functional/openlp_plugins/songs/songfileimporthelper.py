"""
The :mod:`songfileimporthelper` modules provides a helper class and methods to easily enable testing the import of
song files from third party applications.
"""
import json
from unittest import TestCase
from mock import patch, MagicMock

class SongImportTestHelper(TestCase):
    """
    This class is designed to be a helper class to reduce repition when testing the import of song files.
    """
    def __init__(self, *args, **kwargs):
        self.importer_module = __import__(
            'openlp.plugins.songs.lib.%s' % self.importer_module_name, fromlist=[self.importer_class_name])
        self.importer_class = getattr(self.importer_module, self.importer_class_name)
        TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        """
        Patch and set up the mocks required.
        """
        self.add_copyright_patcher = patch(
            'openlp.plugins.songs.lib.%s.%s.addCopyright' % (self.importer_module_name, self.importer_class_name))
        self.add_verse_patcher = patch(
            'openlp.plugins.songs.lib.%s.%s.addVerse' % (self.importer_module_name, self.importer_class_name))
        self.finish_patcher = patch(
            'openlp.plugins.songs.lib.%s.%s.finish' % (self.importer_module_name, self.importer_class_name))
        self.parse_author_patcher = patch(
            'openlp.plugins.songs.lib.%s.%s.parse_author' % (self.importer_module_name, self.importer_class_name))
        self.song_import_patcher = patch('openlp.plugins.songs.lib.%s.SongImport' % self.importer_module_name)
        self.mocked_add_copyright = self.add_copyright_patcher.start()
        self.mocked_add_verse = self.add_verse_patcher.start()
        self.mocked_finish = self.finish_patcher.start()
        self.mocked_parse_author = self.parse_author_patcher.start()
        self.mocked_song_importer = self.song_import_patcher.start()
        self.mocked_manager = MagicMock()
        self.mocked_import_wizard = MagicMock()
        self.mocked_finish.return_value = True

    def tearDown(self):
        """
        Clean up
        """
        self.add_copyright_patcher.stop()
        self.add_verse_patcher.stop()
        self.finish_patcher.stop()
        self.parse_author_patcher.stop()
        self.song_import_patcher.stop()

    def load_external_result_data(self, file_name):
        """
        A method to load and return an object containing the song data from an external file.
        """
        result_file = open(file_name, 'rb')
        return json.loads(result_file.read())

    def file_import(self, source_file_name, result_data):
        """
        Import the given file and check that it has imported correctly
        """
        importer = self.importer_class(self.mocked_manager)
        importer.import_wizard = self.mocked_import_wizard
        importer.stop_import_flag = False
        importer.topics = []

        # WHEN: Importing the source file
        importer.import_source = [source_file_name]
        add_verse_calls = self.get_data(result_data, 'verses')
        author_calls = self.get_data(result_data, 'authors')
        ccli_number = self.get_data(result_data, 'ccli_number')
        comments = self.get_data(result_data, 'comments')
        song_book_name = self.get_data(result_data, 'song_book_name')
        song_copyright = self.get_data(result_data, 'copyright')
        song_number = self.get_data(result_data, 'song_number')
        title = self.get_data(result_data, 'title')
        topics = self.get_data(result_data, 'topics')
        verse_order_list = self.get_data(result_data, 'verse_order_list')

        # THEN: doImport should return none, the song data should be as expected, and finish should have been
        #       called.
        self.assertIsNone(importer.doImport(), 'doImport should return None when it has completed')
        self.assertEquals(importer.title, title, 'title for %s should be "%s"' % (source_file_name, title))
        for author in author_calls:
            self.mocked_parse_author.assert_any_call(author)
        if song_copyright:
            self.mocked_add_copyright.assert_called_with(song_copyright)
        if ccli_number:
            self.assertEquals(importer.ccliNumber, ccli_number, 'ccliNumber for %s should be %s'
                % (source_file_name, ccli_number))
        for verse_text, verse_tag in add_verse_calls:
            self.mocked_add_verse.assert_any_call(verse_text, verse_tag)
        if topics:
            self.assertEquals(importer.topics, topics, 'topics for %s should be %s' % (source_file_name, topics))
        if comments:
            self.assertEquals(importer.comments, comments, 'comments for %s should be "%s"'
                % (source_file_name, comments))
        if song_book_name:
            self.assertEquals(importer.songBookName, song_book_name, 'songBookName for %s should be "%s"'
                % (source_file_name, song_book_name))
        if song_number:
            self.assertEquals(importer.songNumber, song_number, 'songNumber for %s should be %s'
                % (source_file_name, song_number))
        if verse_order_list:
            self.assertEquals(importer.verseOrderList, [], 'verseOrderList for %s should be %s'
                % (source_file_name, verse_order_list))
        self.mocked_finish.assert_called_with()

    def get_data(self, data, key):
        if key in data:
            return data[key]
        return ''

