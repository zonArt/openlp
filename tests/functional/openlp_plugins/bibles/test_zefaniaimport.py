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
This module contains tests for the Zefania Bible importer.
"""

import os
from unittest import TestCase

from tests.functional import MagicMock, patch
from openlp.plugins.bibles.lib.zefania import ZefaniaBible
from openlp.plugins.bibles.lib.db import BibleDB

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', '..', 'resources', 'bibles'))
ZEFANIA_TEST_DATA = {
    'zefania-dk1933.xml': {
        'book': 'Genesis',
        'chapter': 1,
        'verses': [
            ('1', 'I Begyndelsen skabte Gud Himmelen og Jorden.'),
            ('2', 'Og Jorden var øde og tom, og der var Mørke over Verdensdybet. '
             'Men Guds Ånd svævede over Vandene.'),
            ('3', 'Og Gud sagde: "Der blive Lys!" Og der blev Lys.'),
            ('4', 'Og Gud så, at Lyset var godt, og Gud satte Skel mellem Lyset og Mørket,'),
            ('5', 'og Gud kaldte Lyset Dag, og Mørket kaldte han Nat. Og det blev Aften, '
             'og det blev Morgen, første Dag.'),
            ('6', 'Derpå sagde Gud: "Der blive en Hvælving midt i Vandene til at skille Vandene ad!"'),
            ('7', 'Og således skete det: Gud gjorde Hvælvingen og skilte Vandet under Hvælvingen '
             'fra Vandet over Hvælvingen;'),
            ('8', 'og Gud kaldte Hvælvingen Himmel. Og det blev Aften, og det blev Morgen, anden Dag.'),
            ('9', 'Derpå sagde Gud: "Vandet under Himmelen samle sig på eet Sted, så det faste Land kommer til Syne!" '
             'Og således skete det;'),
            ('10', 'og Gud kaldte det faste Land Jord, og Stedet, hvor Vandet samlede sig, kaldte han Hav. Og Gud så, '
             'at det var godt.')
        ]
    }
}


class TestZefaniaImport(TestCase):
    """
    Test the functions in the :mod:`zefaniaimport` module.
    """

    def setUp(self):
        self.registry_patcher = patch('openlp.plugins.bibles.lib.db.Registry')
        self.registry_patcher.start()
        self.manager_patcher = patch('openlp.plugins.bibles.lib.db.Manager')
        self.manager_patcher.start()

    def tearDown(self):
        self.registry_patcher.stop()
        self.manager_patcher.stop()

    def create_importer_test(self):
        """
        Test creating an instance of the Zefania file importer
        """
        # GIVEN: A mocked out "manager"
        mocked_manager = MagicMock()

        # WHEN: An importer object is created
        importer = ZefaniaBible(mocked_manager, path='.', name='.', filename='')

        # THEN: The importer should be an instance of BibleDB
        self.assertIsInstance(importer, BibleDB)

    def file_import_test(self):
        """
        Test the actual import of real song files
        """
        # GIVEN: Test files with a mocked out "manager", "import_wizard", and mocked functions
        #        get_book_ref_id_by_name, create_verse, create_book, session and get_language.
        with patch('openlp.plugins.bibles.lib.zefania.ZefaniaBible.application'):
            for bible_file in ZEFANIA_TEST_DATA:
                mocked_manager = MagicMock()
                mocked_import_wizard = MagicMock()
                importer = ZefaniaBible(mocked_manager, path='.', name='.', filename='')
                importer.wizard = mocked_import_wizard
                importer.get_book_ref_id_by_name = MagicMock()
                importer.create_verse = MagicMock()
                importer.create_book = MagicMock()
                importer.session = MagicMock()
                importer.get_language = MagicMock()
                importer.get_language.return_value = 'Danish'

                # WHEN: Importing bible file
                importer.filename = os.path.join(TEST_PATH, bible_file)
                importer.do_import()

                # THEN: The create_verse() method should have been called with each verse in the file.
                self.assertTrue(importer.create_verse.called)
                for verse_tag, verse_text in ZEFANIA_TEST_DATA[bible_file]['verses']:
                    importer.create_verse.assert_any_call(importer.create_book().id, '1', verse_tag, verse_text)
