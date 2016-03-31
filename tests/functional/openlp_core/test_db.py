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
Package to test the openlp.core.utils.db package.
"""
import gc
import os
import shutil
import time
from tempfile import mkdtemp
from unittest import TestCase

import sqlalchemy

from openlp.core.common.db import drop_column, drop_columns
from openlp.core.lib.db import init_db, get_upgrade_op
from tests.utils.constants import TEST_RESOURCES_PATH


class TestUtilsDBFunctions(TestCase):

    def setUp(self):
        """
        Create temp folder for keeping db file
        """
        self.tmp_folder = mkdtemp()
        db_path = os.path.join(TEST_RESOURCES_PATH, 'songs', 'songs-1.9.7.sqlite')
        self.db_tmp_path = os.path.join(self.tmp_folder, 'songs-1.9.7.sqlite')
        shutil.copyfile(db_path, self.db_tmp_path)
        db_url = 'sqlite:///' + self.db_tmp_path
        self.session, metadata = init_db(db_url)
        self.op = get_upgrade_op(self.session)

    def tearDown(self):
        """
        Clean up
        """
        self.session.close()
        self.session = None
        gc.collect()
        retries = 0
        while retries < 5:
            try:
                if os.path.exists(self.tmp_folder):
                    shutil.rmtree(self.tmp_folder)
                break
            except:
                time.sleep(1)
                retries += 1

    def delete_column_test(self):
        """
        Test deleting a single column in a table
        """
        # GIVEN: A temporary song db

        # WHEN: Deleting a columns in a table
        drop_column(self.op, 'songs', 'song_book_id')

        # THEN: The column should have been deleted
        meta = sqlalchemy.MetaData(bind=self.op.get_bind())
        meta.reflect()
        columns = meta.tables['songs'].columns

        for column in columns:
            if column.name == 'song_book_id':
                self.fail("The column 'song_book_id' should have been deleted.")

    def delete_columns_test(self):
        """
        Test deleting multiple columns in a table
        """
        # GIVEN: A temporary song db

        # WHEN: Deleting a columns in a table
        drop_columns(self.op, 'songs', ['song_book_id', 'song_number'])

        # THEN: The columns should have been deleted
        meta = sqlalchemy.MetaData(bind=self.op.get_bind())
        meta.reflect()
        columns = meta.tables['songs'].columns

        for column in columns:
            if column.name == 'song_book_id' or column.name == 'song_number':
                self.fail("The column '%s' should have been deleted." % column.name)
