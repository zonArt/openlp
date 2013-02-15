"""
    Package to test the openlp.plugins.songs.lib package.
"""
import os

from unittest import TestCase
from mock import MagicMock, patch
from openlp.plugins.songs.lib import songshowplusimport

TESTPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'..', u'..', u'resources'))


class TestSongShowPlusImport(TestCase):

    def default_test(self):
        """
        Test the defaults of songshowplusimport
        """
        # Given: The songshowplusimport module as imported

        # When: Imported the module should have defaults set
        constants = {u'TITLE' : 1, u'AUTHOR' : 2, u'COPYRIGHT' : 3, u'CCLI_NO' : 5, u'VERSE' : 12, u'CHORUS' : 20,
            u'BRIDGE' : 24, u'TOPIC' : 29, u'COMMENTS' : 30, u'VERSE_ORDER' : 31, u'SONG_BOOK' : 35,
            u'SONG_NUMBER' : 36, u'CUSTOM_VERSE' : 37, u'SongShowPlusImport.otherList' : {},
            u'SongShowPlusImport.otherCount' : 0}

        # Then: The constants should not have changed.
        for constant in constants:
            value = constants[constant]
            self.assertEquals(eval(u'songshowplusimport.%s' % constant), value,
                u'%s should be set as %s' % (constant, value))


    def do_import_test(self):
        mocked_manager = MagicMock()
        songshowplusimport.SongImport = MagicMock()

        with patch(u'openlp.plugins.songs.lib.songshowplusimport.SongImport') as mocked_song_import:
            ssp_import_class = songshowplusimport.SongShowPlusImport(mocked_manager)

            songshowplusimport.SongShowPlusImport.importSource = ''

            self.assertEquals(ssp_import_class.SongShowPlusImport().doImport(), False)
