# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

"""
This module contains tests for the WorshipCenter Pro song importer.
"""

from unittest import TestCase
from mock import patch, MagicMock
import pyodbc

from openlp.plugins.songs.lib.worshipcenterproimport import WorshipCenterProImport

class TestRecord:
    """
    Microsoft Access Driver is not available on non Microsoft Systems for this reason the :class:`TestRecord` is used
    to simulate a recordset that would be returned by pyobdc.
    """
    def __init__(self, id, field, value):
        # The case of the following instance variables is important as it needs to be the same as the ones in use in the
        # WorshipCenter Pro database.
        self.ID = id
        self.Field = field
        self.Value = value

class WorshipCenterProImportLogger(WorshipCenterProImport):
    """
    This class logs changes in the title instance variable
    """
    _title_assignment_list = []

    def __init__(self, manager):
        WorshipCenterProImport.__init__(self, manager)

    @property
    def title(self):
        return self._title_assignment_list[-1]

    @title.setter
    def title(self, title):
        self._title_assignment_list.append(title)


RECORDSET_TEST_DATA = [TestRecord(1, u'TITLE', u'Amazing Grace'),
                       TestRecord(1, u'LYRICS',
                            u'Amazing grace! How&crlf;sweet the sound&crlf;That saved a wretch like me!&crlf;'
                            u'I once was lost,&crlf;but now am found;&crlf;Was blind, but now I see.&crlf;&crlf;'
                            u'\'Twas grace that&crlf;taught my heart to fear,&crlf;And grace my fears relieved;&crlf;'
                            u'How precious did&crlf;that grace appear&crlf;The hour I first believed.&crlf;&crlf;'
                            u'Through many dangers,&crlf;toils and snares,&crlf;I have already come;&crlf;'
                            u'\'Tis grace hath brought&crlf;me safe thus far,&crlf;'
                            u'And grace will lead me home.&crlf;&crlf;The Lord has&crlf;promised good to me,&crlf;'
                            u'His Word my hope secures;&crlf;He will my Shield&crlf;and Portion be,&crlf;'
                            u'As long as life endures.&crlf;&crlf;Yea, when this flesh&crlf;and heart shall fail,&crlf;'
                            u'And mortal life shall cease,&crlf;I shall possess,&crlf;within the veil,&crlf;'
                            u'A life of joy and peace.&crlf;&crlf;The earth shall soon&crlf;dissolve like snow,&crlf;'
                            u'The sun forbear to shine;&crlf;But God, Who called&crlf;me here below,&crlf;'
                            u'Shall be forever mine.&crlf;&crlf;When we\'ve been there&crlf;ten thousand years,&crlf;'
                            u'Bright shining as the sun,&crlf;We\'ve no less days to&crlf;sing God\'s praise&crlf;'
                            u'Than when we\'d first begun.&crlf;&crlf;'),
                       TestRecord(2, u'TITLE', u'Beautiful Garden Of Prayer, The'),
                       TestRecord(2, u'LYRICS',
                            u'There\'s a garden where&crlf;Jesus is waiting,&crlf;'
                            u'There\'s a place that&crlf;is wondrously fair,&crlf;For it glows with the&crlf;'
                            u'light of His presence.&crlf;\'Tis the beautiful&crlf;garden of prayer.&crlf;&crlf;'
                            u'Oh, the beautiful garden,&crlf;the garden of prayer!&crlf;Oh, the beautiful&crlf;'
                            u'garden of prayer!&crlf;There my Savior awaits,&crlf;and He opens the gates&crlf;'
                            u'To the beautiful&crlf;garden of prayer.&crlf;&crlf;There\'s a garden where&crlf;'
                            u'Jesus is waiting,&crlf;And I go with my&crlf;burden and care,&crlf;'
                            u'Just to learn from His&crlf;lips words of comfort&crlf;In the beautiful&crlf;'
                            u'garden of prayer.&crlf;&crlf;There\'s a garden where&crlf;Jesus is waiting,&crlf;'
                            u'And He bids you to come,&crlf;meet Him there;&crlf;Just to bow and&crlf;'
                            u'receive a new blessing&crlf;In the beautiful&crlf;garden of prayer.&crlf;&crlf;')]
SONG_TEST_DATA = [{u'title': u'Amazing Grace',
                   u'verses': [
                       (u'Amazing grace! How\nsweet the sound\nThat saved a wretch like me!\nI once was lost,\n'
                        u'but now am found;\nWas blind, but now I see.'),
                       (u'\'Twas grace that\ntaught my heart to fear,\nAnd grace my fears relieved;\nHow precious did\n'
                        u'that grace appear\nThe hour I first believed.'),
                       (u'Through many dangers,\ntoils and snares,\nI have already come;\n\'Tis grace hath brought\n'
                        u'me safe thus far,\nAnd grace will lead me home.'),
                       (u'The Lord has\npromised good to me,\nHis Word my hope secures;\n'
                        u'He will my Shield\nand Portion be,\nAs long as life endures.'),
                       (u'Yea, when this flesh\nand heart shall fail,\nAnd mortal life shall cease,\nI shall possess,\n'
                        u'within the veil,\nA life of joy and peace.'),
                       (u'The earth shall soon\ndissolve like snow,\nThe sun forbear to shine;\nBut God, Who called\n'
                        u'me here below,\nShall be forever mine.'),
                       (u'When we\'ve been there\nten thousand years,\nBright shining as the sun,\n'
                        u'We\'ve no less days to\nsing God\'s praise\nThan when we\'d first begun.')]},
                   {u'title': u'Beautiful Garden Of Prayer, The',
                   u'verses': [
                       (u'There\'s a garden where\nJesus is waiting,\nThere\'s a place that\nis wondrously fair,\n'
                        u'For it glows with the\nlight of His presence.\n\'Tis the beautiful\ngarden of prayer.'),
                       (u'Oh, the beautiful garden,\nthe garden of prayer!\nOh, the beautiful\ngarden of prayer!\n'
                        u'There my Savior awaits,\nand He opens the gates\nTo the beautiful\ngarden of prayer.'),
                       (u'There\'s a garden where\nJesus is waiting,\nAnd I go with my\nburden and care,\n'
                        u'Just to learn from His\nlips words of comfort\nIn the beautiful\ngarden of prayer.'),
                       (u'There\'s a garden where\nJesus is waiting,\nAnd He bids you to come,\nmeet Him there;\n'
                        u'Just to bow and\nreceive a new blessing\nIn the beautiful\ngarden of prayer.')]}]

class TestWorshipCenterProSongImport(TestCase):
    """
    Test the functions in the :mod:`worshipcenterproimport` module.
    """
    def create_importer_test(self):
        """
        Test creating an instance of the WorshipCenter Pro file importer
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.worshipcenterproimport.SongImport'):
            mocked_manager = MagicMock()

            # WHEN: An importer object is created
            importer = WorshipCenterProImport(mocked_manager)

            # THEN: The importer object should not be None
            self.assertIsNotNone(importer, u'Import should not be none')

    def pyodbc_exception_test(self):
        """
        Test that exceptions raised by pyodbc are handled
        """
        # GIVEN: A mocked out SongImport class, a mocked out pyodbc module, a mocked out translate method,
        #       a mocked "manager" and a mocked out logError method.
        with patch(u'openlp.plugins.songs.lib.worshipcenterproimport.SongImport'), \
            patch(u'openlp.plugins.songs.lib.worshipcenterproimport.pyodbc.connect') as mocked_pyodbc_connect, \
            patch(u'openlp.plugins.songs.lib.worshipcenterproimport.translate') as mocked_translate:
            mocked_manager = MagicMock()
            mocked_log_error = MagicMock()
            mocked_translate.return_value = u'Translated Text'
            importer = WorshipCenterProImport(mocked_manager)
            importer.logError = mocked_log_error
            importer.import_source = u'import_source'
            pyodbc_errors = [pyodbc.DatabaseError, pyodbc.IntegrityError, pyodbc.InternalError, pyodbc.OperationalError]
            mocked_pyodbc_connect.side_effect = pyodbc_errors

            # WHEN: Calling the doImport method
            for effect in pyodbc_errors:
                return_value = importer.doImport()

                # THEN: doImport should return None, and pyodbc, translate & logError are called with known calls
                self.assertIsNone(return_value, u'doImport should return None when pyodbc raises an exception.')
                mocked_pyodbc_connect.assert_called_with( u'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=import_source')
                mocked_translate.assert_called_with('SongsPlugin.WorshipCenterProImport',
                    'Unable to connect the WorshipCenter Pro database.')
                mocked_log_error.assert_called_with(u'import_source', u'Translated Text')

    def song_import_test(self):
        """
        Test that a simulated WorshipCenter Pro recordset is imported correctly
        """
        # GIVEN: A mocked out SongImport class, a mocked out pyodbc module with a simulated recordset, a mocked out
        #       translate method,  a mocked "manager", addVerse method & mocked_finish method.
        with patch(u'openlp.plugins.songs.lib.worshipcenterproimport.SongImport'), \
            patch(u'openlp.plugins.songs.lib.worshipcenterproimport.pyodbc') as mocked_pyodbc, \
            patch(u'openlp.plugins.songs.lib.worshipcenterproimport.translate') as mocked_translate:
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            mocked_add_verse = MagicMock()
            mocked_finish = MagicMock()
            mocked_pyodbc.connect().cursor().fetchall.return_value = RECORDSET_TEST_DATA
            mocked_translate.return_value = u'Translated Text'
            importer = WorshipCenterProImportLogger(mocked_manager)
            importer.import_source = u'import_source'
            importer.import_wizard = mocked_import_wizard
            importer.addVerse = mocked_add_verse
            importer.stop_import_flag = False
            importer.finish = mocked_finish

            # WHEN: Calling the doImport method
            return_value = importer.doImport()


            # THEN: doImport should return None, and pyodbc, import_wizard, importer.title and addVerse are called with
            #       known calls
            self.assertIsNone(return_value, u'doImport should return None when pyodbc raises an exception.')
            mocked_pyodbc.connect.assert_called_with(u'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=import_source')
            mocked_pyodbc.connect().cursor.assert_any_call()
            mocked_pyodbc.connect().cursor().execute.assert_called_with(u'SELECT ID, Field, Value FROM __SONGDATA')
            mocked_pyodbc.connect().cursor().fetchall.assert_any_call()
            mocked_import_wizard.progress_bar.setMaximum.assert_called_with(2)
            add_verse_call_count = 0
            for song_data in SONG_TEST_DATA:
                title_value = song_data[u'title']
                self.assertIn(title_value, importer._title_assignment_list,
                    u'title should have been set to %s' % title_value)
                verse_calls = song_data[u'verses']
                add_verse_call_count += len(verse_calls)
                for call in verse_calls:
                    mocked_add_verse.assert_any_call(call)
            self.assertEqual(mocked_add_verse.call_count, add_verse_call_count,
                u'Incorrect number of calls made to addVerse')