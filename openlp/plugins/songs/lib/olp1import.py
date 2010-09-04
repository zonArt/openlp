# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
The :mod:`olp1import` module provides the functionality for importing
openlp.org 1.x song databases into the current installation database.
"""
import logging
import sqlite

#from openlp.core.lib.db import BaseModel
from openlp.plugins.songs.lib.db import Author, Book, Song, Topic #, MediaFile
from songimport import SongImport

log = logging.getLogger(__name__)

class OpenLP1SongImport(SongImport):
    """
    The :class:`OpenLP1SongImport` class provides OpenLP with the ability to
    import song databases from installations of openlp.org 1.x.
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the import.

        ``manager``
            The song manager for the running OpenLP installation.

        ``filename``
            The database providing the data to import.
        """
        SongImport.__init__(self, manager)
        self.import_source = kwargs[u'filename']

    def do_import(self):
        """
        Run the import for an openlp.org 1.x song database.
        """
        connection = sqlite.connect(self.import_source)
        cursor = connection.cursor()
        cursor.execute(u'SELECT COUNT(authorid) FROM authors')
        count = int(cursor.fetchone()[0])
        cursor.execute(u'SELECT COUNT(songid) FROM songs')
        count = int(cursor.fetchone()[0])
        self.import_wizard.importProgressBar.setMaximum(count)

    old_cursor.execute(u'SELECT authorid AS id, authorname AS displayname FROM authors')
    rows = old_cursor.fetchall()
    if not debug and verbose:
        print 'done.'
    author_map = {}
    for row in rows:
        display_name = unicode(row[1], u'cp1252')
        names = display_name.split(u' ')
        first_name = names[0]
        last_name = u' '.join(names[1:])
        if last_name is None:
            last_name = u''
        sql_insert = u'INSERT INTO authors '\
            '(id, first_name, last_name, display_name) '\
            'VALUES (NULL, ?, ?, ?)'
        sql_params = (first_name, last_name, display_name)
        if debug:
            print '...', display_sql(sql_insert, sql_params)
        elif verbose:
            print '... importing "%s"' % display_name
        new_cursor.execute(sql_insert, sql_params)
        author_map[row[0]] = new_cursor.lastrowid
        if debug:
            print '    >>> authors.authorid =', row[0], 'authors.id =', author_map[row[0]]


        cursor.execute(u'SELECT songid AS id, songtitle AS title, '
            u'lyrics || \'\' AS lyrics, copyrightinfo AS copyright FROM songs')
        rows = cursor.fetchall()
