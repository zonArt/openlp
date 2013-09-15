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
The :mod:`upgrade` module provides a way for the database and schema that is the backend for the Bibles plugin.
"""
import logging

from sqlalchemy import Table, func, select, insert

__version__ = 1
log = logging.getLogger(__name__)


def upgrade_1(session, metadata):
    """
    Version 1 upgrade.

    This upgrade renames a number of keys to a single naming convention.
    """
    metadata_table = Table('metadata', metadata, autoload=True)
    # Copy "Version" to "name" ("version" used by upgrade system)
    # TODO: Clean up in a subsequent release of OpenLP (like 2.0 final)
    session.execute(insert(metadata_table).values(
        key='name',
        value=select(
            [metadata_table.c.value],
            metadata_table.c.key == 'Version'
        ).as_scalar()
    ))
    # Copy "Copyright" to "copyright"
    # TODO: Clean up in a subsequent release of OpenLP (like 2.0 final)
    session.execute(insert(metadata_table).values(
        key='copyright',
        value=select(
            [metadata_table.c.value],
            metadata_table.c.key == 'Copyright'
        ).as_scalar()
    ))
    # Copy "Permissions" to "permissions"
    # TODO: Clean up in a subsequent release of OpenLP (like 2.0 final)
    session.execute(insert(metadata_table).values(
        key='permissions',
        value=select(
            [metadata_table.c.value],
            metadata_table.c.key == 'Permissions'
        ).as_scalar()
    ))
    # Copy "Bookname language" to "book_name_language"
    # TODO: Clean up in a subsequent release of OpenLP (like 2.0 final)
    value_count = session.execute(
        select(
            [func.count(metadata_table.c.value)],
            metadata_table.c.key == 'Bookname language'
        )
    ).scalar()
    if value_count > 0:
        session.execute(insert(metadata_table).values(
            key='book_name_language',
            value=select(
                [metadata_table.c.value],
                metadata_table.c.key == 'Bookname language'
            ).as_scalar()
        ))
    # Copy "download source" to "download_source"
    # TODO: Clean up in a subsequent release of OpenLP (like 2.0 final)
    value_count = session.execute(
        select(
            [func.count(metadata_table.c.value)],
            metadata_table.c.key == 'download source'
        )
    ).scalar()
    log.debug('download source: %s', value_count)
    if value_count > 0:
        session.execute(insert(metadata_table).values(
            key='download_source',
            value=select(
                [metadata_table.c.value],
                metadata_table.c.key == 'download source'
            ).as_scalar()
        ))
    # Copy "download name" to "download_name"
    # TODO: Clean up in a subsequent release of OpenLP (like 2.0 final)
    value_count = session.execute(
        select(
            [func.count(metadata_table.c.value)],
            metadata_table.c.key == 'download name'
        )
    ).scalar()
    log.debug('download name: %s', value_count)
    if value_count > 0:
        session.execute(insert(metadata_table).values(
            key='download_name',
            value=select(
                [metadata_table.c.value],
                metadata_table.c.key == 'download name'
            ).as_scalar()
        ))
    # Copy "proxy server" to "proxy_server"
    # TODO: Clean up in a subsequent release of OpenLP (like 2.0 final)
    value_count = session.execute(
        select(
            [func.count(metadata_table.c.value)],
            metadata_table.c.key == 'proxy server'
        )
    ).scalar()
    log.debug('proxy server: %s', value_count)
    if value_count > 0:
        session.execute(insert(metadata_table).values(
            key='proxy_server',
            value=select(
                [metadata_table.c.value],
                metadata_table.c.key == 'proxy server'
            ).as_scalar()
        ))
    # Copy "proxy username" to "proxy_username"
    # TODO: Clean up in a subsequent release of OpenLP (like 2.0 final)
    value_count = session.execute(
        select(
            [func.count(metadata_table.c.value)],
            metadata_table.c.key == 'proxy username'
        )
    ).scalar()
    log.debug('proxy username: %s', value_count)
    if value_count > 0:
        session.execute(insert(metadata_table).values(
            key='proxy_username',
            value=select(
                [metadata_table.c.value],
                metadata_table.c.key == 'proxy username'
            ).as_scalar()
        ))
    # Copy "proxy password" to "proxy_password"
    # TODO: Clean up in a subsequent release of OpenLP (like 2.0 final)
    value_count = session.execute(
        select(
            [func.count(metadata_table.c.value)],
            metadata_table.c.key == 'proxy password'
        )
    ).scalar()
    log.debug('proxy password: %s', value_count)
    if value_count > 0:
        session.execute(insert(metadata_table).values(
            key='proxy_password',
            value=select(
                [metadata_table.c.value],
                metadata_table.c.key == 'proxy password'
            ).as_scalar()
        ))
    # TODO: Clean up in a subsequent release of OpenLP (like 2.0 final)
    #session.execute(delete(metadata_table)\
    #    .where(metadata_table.c.key == u'dbversion'))
    session.commit()
