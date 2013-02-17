"""
    Package to test the openlp.plugins.songs.lib package.
"""
import os

from unittest import TestCase
from mock import MagicMock, patch
from openlp.plugins.songs.lib import songshowplusimport

TESTPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'..', u'..', u'resources'))


class TestSongShowPlusImport(TestCase):

#test do import
    # set self.import source to non list type. Do import should return None or False?
    # set self.import source to a list of files
    # importWizard.progressBar should be set to the number of files in the list
    # set self.stop_import_flag to true. Do import should return None or False?



    def do_import_test(self):
        mocked_manager = MagicMock()

        with patch(u'openlp.plugins.songs.lib.songshowplusimport.SongImport') as mocked_song_import:
            ssp_import_class = songshowplusimport.SongShowPlusImport(mocked_manager)

            songshowplusimport.SongShowPlusImport.importSource = ''

            self.assertEquals(ssp_import_class.SongShowPlusImport().doImport(), False)
