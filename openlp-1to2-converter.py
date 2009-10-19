#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import sqlite
import sqlite3
import chardet
from optparse import OptionParser
from traceback import format_tb as get_traceback

# Some global options to be used throughout the import process
verbose = False
debug = False
old_cursor = None
new_cursor = None

# SQL create statments
create_statements = [
    u"""CREATE TABLE authors (
        id INTEGER NOT NULL,
        first_name VARCHAR(128),
        last_name VARCHAR(128),
        display_name VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
)""",
    u"""CREATE TABLE song_books (
        id INTEGER NOT NULL,
        name VARCHAR(128) NOT NULL,
        publisher VARCHAR(128),
        PRIMARY KEY (id)
)""",
    u"""CREATE TABLE songs (
        id INTEGER NOT NULL,
        song_book_id INTEGER,
        title VARCHAR(255) NOT NULL,
        lyrics TEXT NOT NULL,
        verse_order VARCHAR(128),
        copyright VARCHAR(255),
        comments TEXT,
        ccli_number VARCHAR(64),
        song_number VARCHAR(64),
        theme_name VARCHAR(128),
        search_title VARCHAR(255) NOT NULL,
        search_lyrics TEXT NOT NULL,
        PRIMARY KEY (id),
         FOREIGN KEY(song_book_id) REFERENCES song_books (id)
)""",
    u"""CREATE TABLE topics (
        id INTEGER NOT NULL,
        name VARCHAR(128) NOT NULL,
        PRIMARY KEY (id)
)""",
    u"""CREATE INDEX ix_songs_search_lyrics ON songs (search_lyrics)""",
    u"""CREATE INDEX ix_songs_search_title ON songs (search_title)""",
    u"""CREATE TABLE authors_songs (
        author_id INTEGER NOT NULL,
        song_id INTEGER NOT NULL,
        PRIMARY KEY (author_id, song_id),
         FOREIGN KEY(author_id) REFERENCES authors (id),
         FOREIGN KEY(song_id) REFERENCES songs (id)
)""",
    u"""CREATE TABLE songs_topics (
        song_id INTEGER NOT NULL,
        topic_id INTEGER NOT NULL,
        PRIMARY KEY (song_id, topic_id),
         FOREIGN KEY(song_id) REFERENCES songs (id),
         FOREIGN KEY(topic_id) REFERENCES topics (id)
)"""
]

def create_database():
    global new_cursor, create_statements
    if debug or verbose:
        print 'Creating new database:'
    else:
        print 'Creating new database...',
    for sql_create in create_statements:
        if debug:
            print '... ', sql_create.replace('\n', ' ').replace('         ', ' ')
        elif verbose:
            if sql_create[:12] == u'CREATE TABLE':
                print '... creating table "%s"...' % sql_create[13, sql_create.find(u'(') - 2],
            elif sql_create[:12] == u'CREATE INDEX':
                print '... creating index "%s"...' % sql_create[13, sql_create.find(u'ON') - 2],
        new_cursor.execute(sql_create)
        if verbose and not debug:
            print 'done.'
    if not verbose and not debug:
        print 'done.'

def import_songs():
    global old_cursor, new_cursor, debug, verbose
    if debug or verbose:
        print 'Importing authors:'
    else:
        print 'Importing authors...',
    if debug:
        print '... SELECT authorid AS id, authorname AS displayname FROM authors'
    elif verbose:
        print '... fetching authors from old database...',
    old_cursor.execute(u'SELECT authorid AS id, authorname AS displayname FROM authors')
    rows = old_cursor.fetchall()
    if not debug and verbose:
        print 'done.'
    author_map = {}
    for row in rows:
        names = row[1].split(u' ')
        first_name = names[0]
        last_name = u' '.join(names[1:])
        if last_name is None:
            last_name = u''
        sql_insert = u'INSERT INTO authors '\
            '(id, first_name, last_name, display_name) '\
            'VALUES (NULL, "%s", "%s", "%s")'\
            % (first_name, last_name, row['displayname'])
        if debug:
            print '...', str(sql_insert)
        elif verbose:
            print '... importing "%s"' % row['displayname']
        new_cursor.execute(sql_insert)
        author_map[row[0]] = new_cursor.lastrowid
        if debug:
            print '    >>> authors.authorid =', row[0], 'authors.id =', author_map[row[0]]
    if not verbose and not debug:
        print 'done.'
    if debug or verbose:
        print 'Importing songs:'
    else:
        print 'Importing songs...',
    if debug:
        print '... SELECT songid AS id, songtitle AS title, lyrics, copyrightinfo AS copyright FROM songs'
    elif verbose:
        print '... fetching songs from old database...',
    old_cursor.execute(u'SELECT songid AS id, songtitle AS title, lyrics, copyrightinfo AS copyright FROM songs')
    rows = old_cursor.fetchall()
    if not debug and verbose:
        print 'done.'
    song_map = {}
    xml_lyrics_template = u'<?xml version="1.0" encoding="utf-8"?><song version="1.0"><lyrics language="en">%s</lyrics></song>'
    xml_verse_template = u'<verse label="%d" type="Verse"><![CDATA[%s]]></verse>'
    for row in rows:
        print row[2].decode('iso-8859-1')
        text_lyrics = unicode(row[2], 'iso-8859-1').split(u'\n\n')
        xml_lyrics = u''
        for line, verse in enumerate(text_lyrics):
            if not verse:
                continue
            xml_lyrics += (xml_lyrics_template % (line, verse))
        xml_verse = xml_verse_template % xml_lyrics
        clean_title = row[1]
        clean_lyrics = row[2]
        sql_insert = u'INSERT INTO songs '\
            '(id, title, lyrics, copyright, search_title, search_lyrics) '\
            'VALUES (NULL, "%s", "%s", "%s", "%s", "%s")'\
            % (row[1], xml_lyrics, row[3], clean_title, clean_lyrics)
        if debug:
            print '...', str(sql_insert)
        elif verbose:
            print '... importing "%s"' % row[u'title']
        new_cursor.execute(sql_insert)
        song_map[row[0]] = new_cursor.lastrowid
    if not verbose and not debug:
        print 'done.'
    if debug or verbose:
        print 'Importing song-to-author mapping:'
    else:
        print 'Importing song-to-author mapping...',
    if debug:
        print '... SELECT authorid AS author_id, songid AS song_id FROM songauthors'
    elif verbose:
        print '... fetching song-to-author mapping from old database...',
    old_cursor.execute(u'SELECT songid AS id, songtitle AS title, lyrics, copyrightinfo AS copyright FROM songs')
    rows = old_cursor.fetchall()
    if not debug and verbose:
        print 'done.'
    for row in rows:
        sql_insert = u'INSERT INTO authors_songs '\
            '(author_id, song_id) '\
            'VALUES (%d, %d)'\
            % (author_map[row[u'author_id']], song_map[row[u'song_id']])
        if debug:
            print '... ', str(sql_insert)
        elif verbose:
            print '... Author %d (was %d) => Song %d (was %d)'\
                % (int(row[0]), author_map[row[0]],
                   int(row[1]), song_map[row[1]])
        new_cursor.execute(sql_insert)
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
        import_songs()
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
