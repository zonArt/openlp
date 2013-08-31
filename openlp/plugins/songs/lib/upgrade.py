# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
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
The :mod:`upgrade` module provides a way for the database and schema that is the
backend for the Songs plugin
"""

from sqlalchemy import Column, types
from sqlalchemy.sql.expression import func, false, null, text

from openlp.core.lib.db import get_upgrade_op

__version__ = 3


def upgrade_1(session, metadata):
    """
    Version 1 upgrade.

    This upgrade removes the many-to-many relationship between songs and
    media_files and replaces it with a one-to-many, which is far more
    representative of the real relationship between the two entities.

    In order to facilitate this one-to-many relationship, a song_id column is
    added to the media_files table, and a weight column so that the media
    files can be ordered.
    """
    op = get_upgrade_op(session)
    op.drop_table('media_files_songs')
    op.add_column('media_files', Column('song_id', types.Integer(), server_default=null()))
    op.add_column('media_files', Column('weight', types.Integer(), server_default=text('0')))
    if metadata.bind.url.get_dialect().name != 'sqlite':
        # SQLite doesn't support ALTER TABLE ADD CONSTRAINT
        op.create_foreign_key('fk_media_files_song_id', 'media_files', 'songs', ['song_id', 'id'])


def upgrade_2(session, metadata):
    """
    Version 2 upgrade.

    This upgrade adds a create_date and last_modified date to the songs table
    """
    op = get_upgrade_op(session)
    op.add_column('songs', Column('create_date', types.DateTime(), default=func.now()))
    op.add_column('songs', Column('last_modified', types.DateTime(), default=func.now()))


def upgrade_3(session, metadata):
    """
    Version 3 upgrade.

    This upgrade adds a temporary song flag to the songs table
    """
    op = get_upgrade_op(session)
    if metadata.bind.url.get_dialect().name == 'sqlite':
        op.add_column('songs', Column('temporary', types.Boolean(create_constraint=False), server_default=false()))
    else:
        op.add_column('songs', Column('temporary', types.Boolean(), server_default=false()))

