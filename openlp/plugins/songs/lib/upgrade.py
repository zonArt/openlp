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

from sqlalchemy import Column, Table, types
from sqlalchemy.sql.expression import func
from migrate.changeset.constraint import ForeignKeyConstraint

__version__ = 3

def upgrade_setup(metadata):
    """
    Set up the latest revision all tables, with reflection, needed for the
    upgrade process. If you want to drop a table, you need to remove it from
    here, and add it to your upgrade function.
    """
    tables = {
        u'authors': Table(u'authors', metadata, autoload=True),
        u'media_files': Table(u'media_files', metadata, autoload=True),
        u'song_books': Table(u'song_books', metadata, autoload=True),
        u'songs': Table(u'songs', metadata, autoload=True),
        u'topics': Table(u'topics', metadata, autoload=True),
        u'authors_songs': Table(u'authors_songs', metadata, autoload=True),
        u'songs_topics': Table(u'songs_topics', metadata, autoload=True)
    }
    return tables


def upgrade_1(session, metadata, tables):
    """
    Version 1 upgrade.

    This upgrade removes the many-to-many relationship between songs and
    media_files and replaces it with a one-to-many, which is far more
    representative of the real relationship between the two entities.

    In order to facilitate this one-to-many relationship, a song_id column is
    added to the media_files table, and a weight column so that the media
    files can be ordered.
    """
    Table(u'media_files_songs', metadata, autoload=True).drop(checkfirst=True)
    Column(u'song_id', types.Integer(), default=None).create(table=tables[u'media_files'])
    Column(u'weight', types.Integer(), default=0).create(table=tables[u'media_files'])
    if metadata.bind.url.get_dialect().name != 'sqlite':
        # SQLite doesn't support ALTER TABLE ADD CONSTRAINT
        ForeignKeyConstraint([u'song_id'], [u'songs.id'],
            table=tables[u'media_files']).create()


def upgrade_2(session, metadata, tables):
    """
    Version 2 upgrade.

    This upgrade adds a create_date and last_modified date to the songs table
    """
    Column(u'create_date', types.DateTime(), default=func.now()).create(table=tables[u'songs'])
    Column(u'last_modified', types.DateTime(), default=func.now()).create(table=tables[u'songs'])


def upgrade_3(session, metadata, tables):
    """
    Version 3 upgrade.

    This upgrade adds a temporary song flag to the songs table
    """
    Column(u'temporary', types.Boolean(), default=False).create(table=tables[u'songs'])

