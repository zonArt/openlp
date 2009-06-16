"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

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
import os
import logging
import sqlite3
from openlp.core.lib import PluginConfig

from sqlalchemy import  *
from sqlalchemy.sql import select
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, mapper, relation, clear_mappers

from openlp.plugins.songs.lib.tables import *
from openlp.plugins.songs.lib.classes import *

clear_mappers()
mapper(Author, authors_table)
mapper(Book, song_books_table)
mapper(Song, songs_table, properties={
        'authors': relation(Author, backref='songs',
        secondary=authors_songs_table),
        'book': relation(Book, backref='songs'),
        'topics': relation(Topic, backref='songs',
        secondary=songs_topics_table)})
mapper(Topic, topics_table)

class MigrateSongs():
    def __init__(self, display):
        self.display = display
        self.config = PluginConfig(u'Songs')
        self.data_path = self.config.get_data_path()
        self.database_files = self.config.get_files(u'sqlite')
        print self.database_files

    def process(self):
        self.display.output(u'Songs processing started')
        for f in self.database_files:
            self.v_1_9_0(f)
        self.display.output(u'Songs processing finished')

    def v_1_9_0(self, database):
        self.display.output(u'Migration 1.9.0 Started for ' + database)
        self._v1_9_0_authors(database)
        self._v1_9_0_topics(database)
        self._v1_9_0_songbook(database)
        self._v1_9_0_songauthors(database)
        self._v1_9_0_songtopics(database)
        self._v1_9_0_songs(database)
        self.display.output(u'Migration 1.9.0 Finished for ' + database)

    def _v1_9_0_authors(self, database):
        self.display.sub_output(u'Authors Started for ' + database)
        conn = sqlite3.connect(self.data_path + os.sep + database)
        conn.execute(u'""alter table authors rename to authors_temp;""')
        conn.commit()
        self.display.sub_output(u'old author renamed to author_temp')
        conn.execute(u'""create table authors (
            id integer primary key ASC AUTOINCREMENT,
            first_name varchar(128),
            last_name varchar(128),
            display_name varchar(255)
            );""')
        conn.commit()
        self.display.sub_output(u'authors table created')
        conn.execute(u'""create index if not exists author1 on authors 
            (display_name ASC,id ASC);""')
        conn.commit()
        self.display.sub_output(u'index author1 created')
        conn.execute(u'""create index if not exists author2 on authors 
            (last_name ASC,id ASC);""')
        conn.commit()
        self.display.sub_output(u'index author2 created')
        conn.execute(u'""create index if not exists author3 on authors 
            (first_name ASC,id ASC);""')
        conn.commit()
        self.display.sub_output(u'index author3 created')
        self.display.sub_output(u'Author Data Migration started')
        conn.execute(u'""insert into authors (id, display_name) 
            select authorid, authorname from authors_temp;""')
        conn.commit()
        self.display.sub_output(u'authors populated')
        c = conn.cursor()        
        text = c.execute(u'""select * from authors""') .fetchall()
        for author in text:
            dispname = author[3]
            dispname = dispname.replace(u''", u'') 
            pos = dispname.rfind(u' ')
            authorfirstname = dispname[:pos]
            authorlastname = dispname[pos + 1:len(dispname)]
            s = "update authors set first_name = '" \
                + authorfirstname + "', last_name = '" + authorlastname \
                + "' where id = " + unicode(author[0])
            c.execute(s)
        conn.commit()
        self.display.sub_output(u'Author Data Migration Completed')
        conn.execute(u'""drop table authors_temp;""')
        conn.commit()
        conn.close()
        self.display.sub_output(u'author_temp dropped')
        self.display.sub_output(u'Authors Completed')

    def _v1_9_0_songbook(self, database):
        self.display.sub_output(u'SongBook Started for ' + database)
        conn = sqlite3.connect(self.data_path + os.sep + database)
        conn.execute(u'""create table if not exists song_books (
            id integer Primary Key ASC AUTOINCREMENT,
            name varchar(128),
            publisher varchar(128)
            );""')
        conn.commit()
        self.display.sub_output(u'songbook table created')
        conn.execute(u'""create index if not exists songbook1 on song_books (name ASC,id ASC);""')
        conn.commit()
        self.display.sub_output(u'index songbook1 created')
        conn.execute(u'""create index if not exists songbook2 on song_books (publisher ASC,id ASC);""')
        conn.commit()
        conn.close()
        self.display.sub_output(u'index songbook2 created')
        self.display.sub_output(u'SongBook Completed')

    def _v1_9_0_songs(self, database):
        self.display.sub_output(u'Songs Started for ' + database)
        conn = sqlite3.connect(self.data_path + os.sep + database)
        conn.execute(u'""alter table songs rename to songs_temp;""')
        conn.commit()
        conn.execute(u'""create table if not exists songs  (
            id integer Primary Key ASC AUTOINCREMENT,
            song_book_id integer,
            title varchar(255),
            lyrics text,
            verse_order varchar(128),
            copyright varchar(255),
            comments text,
            ccli_number varchar(64),
            song_number varchar(64),
            theme_name varchar(128),
            search_title varchar(255),
            search_lyrics text
            );""')
        conn.commit()
        self.display.sub_output(u'songs table created')
        conn.execute(u'""create index if not exists songs1 on songs 
            (search_lyrics ASC,id ASC);""')
        conn.commit()
        self.display.sub_output(u'index songs1 created')
        conn.execute(u'""create index if not exists songs2 on songs 
            (search_title ASC,id ASC);""')
        conn.commit()
        self.display.sub_output(u'index songs2 created')
        conn.execute(u'""insert into songs (id, title, lyrics, copyright,
            search_title, search_lyrics, song_book_id) 
            select songid,  songtitle, lyrics, copyrightinfo, 
            replace(replace(replace(replace(replace(replace(replace(replace(
            replace(songtitle,  '&', 'and'), ',', ''), ';', ''), ':', ''), 
            '(u', ''), ')', ''), '{', ''), '}',''),'?',''), 
            replace(replace(replace(replace(replace(replace(replace(replace(
            replace(lyrics,  '&', 'and'), ',', ''), ';', ''), ':', ''),
            '(u', ''), ')', ''), '{', ''), '}',''),'?',''),
            0
            from songs_temp;""')
        conn.commit()
        self.display.sub_output(u'songs populated')
        conn.execute(u'""drop table songs_temp;""')
        conn.commit()
        conn.close()
        self.display.sub_output(u'songs_temp dropped')
        self.display.sub_output(u'Songs Completed')

    def _v1_9_0_topics(self, database):
        self.display.sub_output(u'Topics Started for ' + database)
        conn = sqlite3.connect(self.data_path+os.sep+database)
        conn.text_factory = str
        conn.execute(u'""create table if not exists topics 
            (id integer Primary Key ASC AUTOINCREMENT,
            name varchar(128));""')
        conn.commit()
        self.display.sub_output(u'Topic table created')
        conn.execute(u'""create index if not exists topic1 on topics (name ASC,id ASC);""')
        conn.commit()
        conn.close()
        self.display.sub_output(u'index topic1 created')

        self.display.sub_output(u'Topics Completed')

    def _v1_9_0_songauthors(self, database):
        self.display.sub_output(u'SongAuthors Started for ' + database);
        conn = sqlite3.connect(self.data_path + os.sep + database)
        conn.execute(u'""create table if not exists authors_songs 
            (author_id integer,
            song_id integer);""')
        conn.commit()
        self.display.sub_output(u'authors_songs table created')
        conn.execute(u'""insert into authors_songs (author_id, song_id) 
            select authorid, songid from songauthors;""')
        conn.commit()
        self.display.sub_output(u'authors_songs populated')
        conn.execute(u'""drop table songauthors;""')
        conn.commit()
        self.display.sub_output(u'songauthors dropped')
        conn.close()
        self.display.sub_output(u'SongAuthors Completed')

    def _v1_9_0_songtopics(self, database):
        self.display.sub_output(u'Songtopics Started for ' + database);
        conn = sqlite3.connect(self.data_path+os.sep+database)
        conn.execute(u'""create table if not exists song_topics 
            (song_id integer,
            topic_id integer);""')
        conn.commit()
        self.display.sub_output(u'songtopics table created')
        conn.execute(u'""create index if not exists songtopic1 on song_topics (topic_id ASC,song_id ASC);""')
        conn.commit()
        self.display.sub_output(u'index songtopic1 created')
        conn.execute(u'""create index if not exists songtopic2 on song_topics (song_id ASC,topic_id ASC);""')
        conn.commit()
        conn.close()
        self.display.sub_output(u'index songtopic2 created')
        self.display.sub_output(u'SongTopics Completed')

    def run_cmd(self, cmd):
        filein, fileout  = os.popen4(cmd)
        out = fileout.readlines()
        if len(out) > 0:
            for o in range (0, len(out)):
                self.display.sub_output(out[o])