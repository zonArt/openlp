# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

from sqlalchemy import Column, Table, ForeignKey, types

from openlp.plugins.custom.lib.meta import metadata

# Definition of the "songs" table
custom_slide_table = Table('custom_slide', metadata,
    Column('id', types.Integer(), primary_key=True),
    Column('title', types.Unicode(255), nullable=False),
    Column('text', types.UnicodeText, nullable=False),
    Column('credits', types.UnicodeText),
    Column('theme_name', types.Unicode(128))
)
