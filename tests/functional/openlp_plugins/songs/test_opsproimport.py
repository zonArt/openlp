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
This module contains tests for the WorshipCenter Pro song importer.
"""
import os
from unittest import TestCase, SkipTest

from tests.functional import patch, MagicMock

from openlp.core.common import Registry
from openlp.plugins.songs.lib.importers.opspro import OpsProImport


class TestRecord(object):
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

SONG_TEST_DATA1 = ('Refrein 2x:\r\n'
'Kom zing een nieuw lied\r\n'
'want dit is een nieuwe dag.\r\n'
'Zet de poorten open en zing je lied voor Hem.\r\n'
'[splits]\r\n'
'Kom zing een nieuw lied\r\n'
'Hij heeft je roep gehoord.\r\n'
'En de trouw en liefde van God zijn ook voor jou!\r\n'
' \r\n'
'Hij glimlacht en schijnt zijn licht op ons.\r\n'
'Hij redt ons en steunt ons liefdevol.\r\n'
'Mijn Redder, mijn sterkte is de Heer.\r\n'
'Deze dag leef ik voor Hem - en geef Hem eer!\r\n'
' \r\n'
'(refrein)\r\n'
'\r\n'
'Zijn goedheid rust elke dag op ons.\r\n'
'Zijn liefde verdrijft de angst in ons.\r\n'
'Mijn schuilplaats, mijn toevlucht is de Heer.\r\n'
'Deze dag leef ik voor Hem - en geef Hem eer!\r\n'
' \r\n'
'(refrein)\r\n'
'\r\n'
'Bridge 3x:\r\n'
'Breng dank aan de Heer jouw God.\r\n'
'Geef eer met een dankbaar hart,\r\n'
'Hij toont zijn liefde hier vandaag!\r\n'
'[splits]\r\n'
'Breng dank aan de Heer, jouw God.\r\n'
'Geef eer met een dankbaar hart.\r\n'
'Open je hart voor Hem vandaag!\r\n'
'\r\n'
'Ik zing een nieuw lied en breng Hem de hoogste eer\r\n'
'want de nieuwe dag is vol zegen van de Heer!\r\n'
'Ik zing een nieuw lied en breng Hem de hoogste eer.\r\n'
'Zet je hart wijd open en zing je lied voor Hem!\r\n')


SONG_TEST_DATA = [{'title': 'Amazing Grace',
                   'verses': [
                       ('Amazing grace! How\nsweet the sound\nThat saved a wretch like me!\nI once was lost,\n'
                        'but now am found;\nWas blind, but now I see.'),
                       ('\'Twas grace that\ntaught my heart to fear,\nAnd grace my fears relieved;\nHow precious did\n'
                        'that grace appear\nThe hour I first believed.'),
                       ('Through many dangers,\ntoils and snares,\nI have already come;\n\'Tis grace hath brought\n'
                        'me safe thus far,\nAnd grace will lead me home.'),
                       ('The Lord has\npromised good to me,\nHis Word my hope secures;\n'
                        'He will my Shield\nand Portion be,\nAs long as life endures.'),
                       ('Yea, when this flesh\nand heart shall fail,\nAnd mortal life shall cease,\nI shall possess,\n'
                        'within the veil,\nA life of joy and peace.'),
                       ('The earth shall soon\ndissolve like snow,\nThe sun forbear to shine;\nBut God, Who called\n'
                        'me here below,\nShall be forever mine.'),
                       ('When we\'ve been there\nten thousand years,\nBright shining as the sun,\n'
                        'We\'ve no less days to\nsing God\'s praise\nThan when we\'d first begun.')],
                   'author': 'John Newton',
                   'comments': 'The original version',
                   'copyright': 'Public Domain'},
                  {'title': 'Beautiful Garden Of Prayer, The',
                   'verses': [
                       ('There\'s a garden where\nJesus is waiting,\nThere\'s a place that\nis wondrously fair,\n'
                        'For it glows with the\nlight of His presence.\n\'Tis the beautiful\ngarden of prayer.'),
                       ('Oh, the beautiful garden,\nthe garden of prayer!\nOh, the beautiful\ngarden of prayer!\n'
                        'There my Savior awaits,\nand He opens the gates\nTo the beautiful\ngarden of prayer.'),
                       ('There\'s a garden where\nJesus is waiting,\nAnd I go with my\nburden and care,\n'
                        'Just to learn from His\nlips words of comfort\nIn the beautiful\ngarden of prayer.'),
                       ('There\'s a garden where\nJesus is waiting,\nAnd He bids you to come,\nmeet Him there;\n'
                        'Just to bow and\nreceive a new blessing\nIn the beautiful\ngarden of prayer.')]}]


class TestOpsProSongImport(TestCase):
    """
    Test the functions in the :mod:`opsproimport` module.
    """
    def setUp(self):
        """
        Create the registry
        """
        Registry.create()

    @patch('openlp.plugins.songs.lib.importers.opspro.SongImport')
    def create_importer_test(self, mocked_songimport):
        """
        Test creating an instance of the OPS Pro file importer
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        mocked_manager = MagicMock()

        # WHEN: An importer object is created
        importer = OpsProImport(mocked_manager, filenames=[])

        # THEN: The importer object should not be None
        self.assertIsNotNone(importer, 'Import should not be none')

    @patch('openlp.plugins.songs.lib.importers.opspro.SongImport')
    def detect_chorus_test(self, mocked_songimport):
        """
        Test importing lyrics with a chorus in OPS Pro
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        mocked_manager = MagicMock()
        importer = OpsProImport(mocked_manager, filenames=[])
        song = MagicMock()
        song.ID = 100
        song.SongNumber = 123
        song.SongBookName = 'The Song Book'
        song.Title = 'Song Title'
        song.CopyrightText = 'Music and text by me'
        song.Version = '1'
        song.Origin = '...'
        lyrics = MagicMock()
        lyrics.Lyrics = SONG_TEST_DATA1
        lyrics.Type = 1
        lyrics.IsDualLanguage = True
        importer.finish = MagicMock()

        # WHEN: An importer object is created
        importer.process_song(song, lyrics, [])

        # THEN: The importer object should not be None
        print(importer.verses)
        print(importer.verse_order_list)
        self.assertIsNone(importer, 'Import should not be none')