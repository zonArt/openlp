#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

import sys
import os
import sqlite
import sqlite3
import re
from optparse import OptionParser
from traceback import format_tb as get_traceback

# Some global options to be used throughout the import process
verbose = False
debug = False
old_cursor = None
new_cursor = None

# SQL create statments
create_statements = [
    (u'table "book"', u"""CREATE TABLE book (
        id INTEGER NOT NULL,
        testament_id INTEGER,
        name VARCHAR(30),
        abbreviation VARCHAR(5),
        PRIMARY KEY (id),
        FOREIGN KEY(testament_id) REFERENCES testament (id)
)"""),
    (u'table "metadata"', u"""CREATE TABLE metadata (
        "key" VARCHAR(255) NOT NULL,
        value VARCHAR(255),
        PRIMARY KEY ("key")
)"""),
    (u'table "testament"', u"""CREATE TABLE testament (
        id INTEGER NOT NULL,
        name VARCHAR(30),
        PRIMARY KEY (id)
)"""),
    (u'table "verse"', u"""CREATE TABLE verse (
        id INTEGER NOT NULL,
        book_id INTEGER,
        chapter INTEGER,
        verse INTEGER,
        text TEXT,
        PRIMARY KEY (id),
        FOREIGN KEY(book_id) REFERENCES book (id)
)"""),
    (u'index "idx_abbrev"',
        u"""CREATE INDEX idx_abbrev ON book (abbreviation, id)"""),
    (u'index "idx_chapter_verse_book',
        u"""CREATE INDEX idx_chapter_verse_book ON verse (chapter, verse, book_id, id)"""),
    (u'index "idx_chapter_verse_text"',
        u"""CREATE INDEX idx_chapter_verse_text ON verse (text, verse, book_id, id)"""),
    (u'index "idx_name"',
        u"""CREATE INDEX idx_name ON book (name, id)""")
]

def display_sql(sql, params):
    prepared_params = []
    for param in params:
        if isinstance(param, basestring):
            prepared_params.append(u'"%s"' % param)
        elif isinstance(param, (int, long)):
            prepared_params.append(u'%d' % param)
        elif isinstance(param, (float, complex)):
            prepared_params.append(u'%f' % param)
        else:
            prepared_params.append(u'"%s"' % str(param))
    for prepared_param in prepared_params:
        sql = sql.replace(u'?', prepared_param, 1)
    return sql

def create_database():
    global new_cursor, create_statements
    if debug or verbose:
        print 'Creating new database:'
    else:
        print 'Creating new database...',
    for statement_type, sql_create in create_statements:
        if debug:
            print '... ', sql_create.replace('\n', ' ').replace('         ', ' ')
        elif verbose:
            print '... creating %s...' % statement_type,
        new_cursor.execute(sql_create)
        if verbose and not debug:
            print 'done.'
    if not verbose and not debug:
        print 'done.'

def import_bible():
    global old_cursor, new_cursor, debug, verbose
    if debug or verbose:
        print 'Importing metadata:'
    else:
        print 'Importing metadata...',
    if debug:
        print '... SELECT "key", "value" FROM metadata'
    elif verbose:
        print '... fetching metadata from old database...',
    old_cursor.execute(u'SELECT "key", "value" FROM metadata')
    rows = old_cursor.fetchall()
    if not debug and verbose:
        print 'done.'
    for row in rows:
        key = unicode(row[0], u'cp1252')
        value = unicode(row[1], u'cp1252')
        sql_insert = u'INSERT INTO metadata '\
            '("key", "value") '\
            'VALUES (?, ?)'
        sql_params = (key, value)
        if debug:
            print '...', display_sql(sql_insert, sql_params)
        elif verbose:
            print '... importing "%s"' % key
        new_cursor.execute(sql_insert, sql_params)
    if not verbose and not debug:
        print 'done.'
    if debug or verbose:
        print 'Importing testaments:'
    else:
        print 'Importing testaments...',
    if debug:
        print '... SELECT id, name FROM testament'
    elif verbose:
        print '... fetching testaments from old database...',
    old_cursor.execute(u'SELECT id, name FROM testament')
    rows = old_cursor.fetchall()
    if not debug and verbose:
        print 'done.'
    for row in rows:
        id = int(row[0])
        name = unicode(row[1], u'cp1252')
        sql_insert = u'INSERT INTO testament '\
            '(id, name) '\
            'VALUES (?, ?)'
        sql_params = (id, name)
        if debug:
            print '...', display_sql(sql_insert, sql_params)
        elif verbose:
            print '... importing "%s"' % name
        new_cursor.execute(sql_insert, sql_params)
    if not verbose and not debug:
        print 'done.'
    if debug or verbose:
        print 'Importing books:'
    else:
        print 'Importing books...',
    if debug:
        print '... SELECT id, testament_id, name, abbreviation FROM book'
    elif verbose:
        print '... fetching books from old database...',
    old_cursor.execute(u'SELECT id, testament_id, name, abbreviation FROM book')
    rows = old_cursor.fetchall()
    if not debug and verbose:
        print 'done.'
    book_map = {}
    for row in rows:
        testament_id = int(row[1])
        name = unicode(row[2], u'cp1252')
        abbreviation = unicode(row[3], u'cp1252')
        sql_insert = u'INSERT INTO book '\
            '(id, testament_id, name, abbreviation) '\
            'VALUES (NULL, ?, ?, ?)'
        sql_params = (testament_id, name, abbreviation)
        if debug:
            print '...', display_sql(sql_insert, sql_params)
        elif verbose:
            print '... importing "%s"' % name
        new_cursor.execute(sql_insert, sql_params)
        book_map[row[0]] = new_cursor.lastrowid
        if debug:
            print '    >>> (old) books.id =', row[0], ' (new) books.id =', book_map[row[0]]
    if not verbose and not debug:
        print 'done.'
    if debug or verbose:
        print 'Importing verses:'
    else:
        print 'Importing verses...',
    if debug:
        print '... SELECT id, book_id, chapter, verse, text || \'\' AS text FROM verse...',
    elif verbose:
        print '... fetching verses from old database...',
    old_cursor.execute(u'SELECT id, book_id, chapter, verse, text || \'\' AS text FROM verse')
    rows = old_cursor.fetchall()
    if debug or verbose:
        print 'done.'
    song_map = {}
    for row in rows:
        book_id = int(row[1])
        chapter = int(row[2])
        verse = int(row[3])
        text = unicode(row[4], u'cp1252')
        sql_insert = u'INSERT INTO verse '\
            '(id, book_id, chapter, verse, text) '\
            'VALUES (NULL, ?, ?, ?, ?)'
        sql_params = (book_map[book_id], chapter, verse, text)
        if debug:
            print '...', display_sql(sql_insert, sql_params)
        elif verbose:
            print '... importing "%s..."' % text[:17]
        new_cursor.execute(sql_insert, sql_params)
    if not verbose and not debug:
        print 'done.'

def main(old_db, new_db):
    global old_cursor, new_cursor, debug
    old_connection = None
    new_connection = None
    try:
        old_connection = sqlite.connect(old_db)
    except:
        if debug:
            errormsg = '\n' + ''.join(get_traceback(sys.exc_info()[2]))\
                + str(sys.exc_info()[1])
        else:
            errormsg = sys.exc_info()[1]
        print 'There was a problem connecting to the old database:', errormsg
        return 1
    try:
        new_connection = sqlite3.connect(new_db)
    except:
        if debug:
            errormsg = '\n' + ''.join(get_traceback(sys.exc_info()[2]))\
                + str(sys.exc_info()[1])
        else:
            errormsg = sys.exc_info()[1]
        print 'There was a problem creating the new database:', errormsg
        return 1
    old_cursor = old_connection.cursor()
    new_cursor = new_connection.cursor()
    try:
        create_database()
    except:
        if debug:
            errormsg = '\n' + ''.join(get_traceback(sys.exc_info()[2]))\
                + str(sys.exc_info()[1])
        else:
            errormsg = sys.exc_info()[1]
        print 'There was a problem creating the database:', errormsg
        return 1
    try:
        import_bible()
        new_connection.commit()
    except:
        new_connection.rollback()
        if debug:
            errormsg = '\n' + ''.join(get_traceback(sys.exc_info()[2]))\
                + str(sys.exc_info()[1])
        else:
            errormsg = sys.exc_info()[1]
        print 'There was a problem importing songs:', errormsg
        return 1
    print 'Import complete.'

if __name__ == u'__main__':
    option_parser = OptionParser(usage='Usage: %prog [options] OLDDATABASE NEWDATABASE')
    option_parser.add_option('-o', '--overwrite', dest='overwrite', default=False,
        action=u'store_true', help='Overwrite database file if it already exists.')
    option_parser.add_option('-v', '--verbose', dest='verbose', default=False,
        action=u'store_true', help='Outputs additional progress data.')
    option_parser.add_option('-d', '--debug', dest='debug', default=False,
        action=u'store_true', help='Outputs raw SQL statements (overrides verbose).')
    options, arguments = option_parser.parse_args()
    if len(arguments) < 2:
        if len(arguments) == 0:
            option_parser.error('Please specify an old database and a new database.')
        else:
            option_parser.error('Please specify a new database.')
    old_db = os.path.abspath(arguments[0])
    new_db = os.path.abspath(arguments[1])
    if not os.path.isfile(old_db):
        option_parser.error('Old database file ("%s") is not a file.' % old_db)
    if not os.path.exists(old_db):
        option_parser.error('Old database file ("%s") does not exist.' % old_db)
    if os.path.exists(new_db):
        if not options.overwrite:
            option_parser.error('New database file ("%s") exists. If you want to overwrite it, specify the --overwrite option.' % new_db)
        else:
            if not os.path.isfile(new_db):
                option_parser.error('New database file ("%s") is not a file.' % new_db)
            os.unlink(new_db)
    verbose = options.verbose
    debug = options.debug
    main(old_db, new_db)
