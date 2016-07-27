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
The :mod:`db` module provides helper functions for database related methods.
"""
import logging
from copy import deepcopy

import sqlalchemy


log = logging.getLogger(__name__)


def drop_column(op, tablename, columnname):
    drop_columns(op, tablename, [columnname])


def drop_columns(op, tablename, columns):
    """
    Column dropping functionality for SQLite, as there is no DROP COLUMN support in SQLite

    From https://github.com/klugjohannes/alembic-sqlite
    """

    # get the db engine and reflect database tables
    engine = op.get_bind()
    meta = sqlalchemy.MetaData(bind=engine)
    meta.reflect()

    # create a select statement from the old table
    old_table = meta.tables[tablename]
    select = sqlalchemy.sql.select([c for c in old_table.c if c.name not in columns])

    # get remaining columns without table attribute attached
    remaining_columns = [deepcopy(c) for c in old_table.columns if c.name not in columns]
    for column in remaining_columns:
        column.table = None

    # create a temporary new table
    new_tablename = '{0}_new'.format(tablename)
    op.create_table(new_tablename, *remaining_columns)
    meta.reflect()
    new_table = meta.tables[new_tablename]

    # copy data from old table
    insert = sqlalchemy.sql.insert(new_table).from_select([c.name for c in remaining_columns], select)
    engine.execute(insert)

    # drop the old table and rename the new table to take the old tables
    # position
    op.drop_table(tablename)
    op.rename_table(new_tablename, tablename)
