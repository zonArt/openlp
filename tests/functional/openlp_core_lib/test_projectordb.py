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
Package to test the openlp.core.ui.projectordb  find, edit, delete
record functions.

PREREQUISITE: add_record() and get_all() functions validated.
"""
import os
from unittest import TestCase

from openlp.core.lib.projector.db import Manufacturer, Model, Projector, ProjectorDB, ProjectorSource, Source
from openlp.core.lib.projector.constants import PJLINK_PORT

from tests.functional import MagicMock, patch
from tests.resources.projector.data import TEST_DB, TEST1_DATA, TEST2_DATA, TEST3_DATA


def compare_data(one, two):
    """
    Verify two Projector() instances contain the same data
    """
    return one is not None and \
        two is not None and \
        one.ip == two.ip and \
        one.port == two.port and \
        one.name == two.name and \
        one.location == two.location and \
        one.notes == two.notes


def compare_source(one, two):
    """
    Verify two ProjectorSource instances contain the same data
    """
    return one is not None and \
        two is not None and \
        one.projector_id == two.projector_id and \
        one.code == two.code and \
        one.text == two.text


def add_records(projector_db, test):
    """
    Add record if not in database
    """
    record_list = projector_db.get_projector_all()
    if len(record_list) < 1:
        added = False
        for record in test:
            added = projector_db.add_projector(record) or added
        return added

    for new_record in test:
        added = None
        for record in record_list:
            if compare_data(record, new_record):
                break
            added = projector_db.add_projector(new_record)
    return added


class TestProjectorDB(TestCase):
    """
    Test case for ProjectorDB
    """
    @patch('openlp.core.lib.projector.db.init_url')
    def setUp(self, mocked_init_url):
        """
        Set up anything necessary for all tests
        """
        mocked_init_url.return_value = 'sqlite:///{db}'.format(db=TEST_DB)
        self.projector = ProjectorDB()

    def tearDown(self):
        """
        Clean up
        """
        self.projector.session.close()
        self.projector = None
        retries = 0
        while retries < 5:
            try:
                if os.path.exists(TEST_DB):
                    os.unlink(TEST_DB)
                break
            except:
                time.sleep(1)
                retries += 1

    def find_record_by_ip_test(self):
        """
        Test find record by IP
        """
        # GIVEN: Record entries in database
        add_records(self.projector, [Projector(**TEST1_DATA), Projector(**TEST2_DATA)])

        # WHEN: Search for record using IP
        record = self.projector.get_projector_by_ip(TEST2_DATA['ip'])

        # THEN: Verify proper record returned
        self.assertTrue(compare_data(Projector(**TEST2_DATA), record),
                        'Record found should have been test_2 data')

    def find_record_by_name_test(self):
        """
        Test find record by name
        """
        # GIVEN: Record entries in database
        add_records(self.projector, [Projector(**TEST1_DATA), Projector(**TEST2_DATA)])

        # WHEN: Search for record using name
        record = self.projector.get_projector_by_name(TEST2_DATA['name'])

        # THEN: Verify proper record returned
        self.assertTrue(compare_data(Projector(**TEST2_DATA), record),
                        'Record found should have been test_2 data')

    def record_delete_test(self):
        """
        Test record can be deleted
        """
        # GIVEN: Record in database
        add_records(self.projector, [Projector(**TEST3_DATA), ])
        record = self.projector.get_projector_by_ip(TEST3_DATA['ip'])

        # WHEN: Record deleted
        self.projector.delete_projector(record)

        # THEN: Verify record not retrievable
        found = self.projector.get_projector_by_ip(TEST3_DATA['ip'])
        self.assertFalse(found, 'test_3 record should have been deleted')

    def record_edit_test(self):
        """
        Test edited record returns the same record ID with different data
        """
        # GIVEN: Record entries in database
        add_records(self.projector, [Projector(**TEST1_DATA), Projector(**TEST2_DATA)])

        # WHEN: We retrieve a specific record
        record = self.projector.get_projector_by_ip(TEST1_DATA['ip'])
        record_id = record.id

        # WHEN: Data is changed
        record.ip = TEST3_DATA['ip']
        record.port = TEST3_DATA['port']
        record.pin = TEST3_DATA['pin']
        record.name = TEST3_DATA['name']
        record.location = TEST3_DATA['location']
        record.notes = TEST3_DATA['notes']
        updated = self.projector.update_projector(record)
        self.assertTrue(updated, 'Save updated record should have returned True')
        record = self.projector.get_projector_by_ip(TEST3_DATA['ip'])

        # THEN: Record ID should remain the same, but data should be changed
        self.assertEqual(record_id, record.id, 'Edited record should have the same ID')
        self.assertTrue(compare_data(Projector(**TEST3_DATA), record), 'Edited record should have new data')

    def source_add_test(self):
        """
        Test source entry for projector item
        """
        # GIVEN: Record entries in database
        projector1 = Projector(**TEST1_DATA)
        self.projector.add_projector(projector1)
        item = self.projector.get_projector_by_id(projector1.id)
        item_id = item.id

        # WHEN: A source entry is saved for item
        source = ProjectorSource(projector_id=item_id, code='11', text='First RGB source')
        self.projector.add_source(source)

        # THEN: Projector should have the same source entry
        item = self.projector.get_projector_by_id(item_id)
        self.assertTrue(compare_source(item.source_list[0], source))

    def manufacturer_repr_test(self):
        """
        Test Manufacturer.__repr__ text
        """
        # GIVEN: Test object
        manufacturer = Manufacturer()

        # WHEN: Name is set
        manufacturer.name = 'OpenLP Test'

        # THEN: __repr__ should return a proper string
        self.assertEqual(str(manufacturer), '<Manufacturer(name="OpenLP Test")>',
                         'Manufacturer.__repr__() should have returned a proper representation string')

    def model_repr_test(self):
        """
        Test Model.__repr__ text
        """
        # GIVEN: Test object
        model = Model()

        # WHEN: Name is set
        model.name = 'OpenLP Test'

        # THEN: __repr__ should return a proper string
        self.assertEqual(str(model), '<Model(name='"OpenLP Test"')>',
                         'Model.__repr__() should have returned a proper representation string')

    def source_repr_test(self):
        """
        Test Source.__repr__ text
        """
        # GIVEN: Test object
        source = Source()

        # WHEN: Source() information is set
        source.pjlink_name = 'Test object'
        source.pjlink_code = '11'
        source.text = 'Input text'

        # THEN: __repr__ should return a proper string
        self.assertEqual(str(source), '<Source(pjlink_name="Test object", pjlink_code="11", text="Input text")>',
                         'Source.__repr__() should have returned a proper representation string')

    def projector_repr_test(self):
        """
        Test Projector.__repr__() text
        """
        # GIVEN: Test object
        projector = Projector()

        # WHEN: projector() is populated
        # NOTE: projector.pin, projector.other, projector.sources should all return None
        #       projector.source_list should return an empty list
        projector.id = 0
        projector.ip = '127.0.0.1'
        projector.port = PJLINK_PORT
        projector.name = 'Test One'
        projector.location = 'Somewhere over the rainbow'
        projector.notes = 'Not again'
        projector.pjlink_name = 'TEST'
        projector.manufacturer = 'IN YOUR DREAMS'
        projector.model = 'OpenLP'

        # THEN: __repr__ should return a proper string
        self.assertEqual(str(projector),
                         '< Projector(id="0", ip="127.0.0.1", port="4352", pin="None", name="Test One", '
                         'location="Somewhere over the rainbow", notes="Not again", pjlink_name="TEST", '
                         'manufacturer="IN YOUR DREAMS", model="OpenLP", other="None", sources="None", '
                         'source_list="[]") >',
                         'Projector.__repr__() should have returned a proper representation string')
