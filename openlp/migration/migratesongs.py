# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

import os
import sys
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.exceptions import InvalidRequestError
from sqlalchemy.orm import scoped_session, sessionmaker, mapper, relation

from openlp.core.lib import BaseModel, SettingsManager
from openlp.core.utils import AppLocation
from openlp.plugins.songs.lib.models import metadata, songs_table, Song, \
    Author, Topic, Book
from openlp.plugins.songs.lib.tables import *
from openlp.plugins.songs.lib.classes import *

def init_models(url):
    engine = create_engine(url)
    metadata.bind = engine
    session = scoped_session(
        sessionmaker(autoflush=True, autocommit=False, bind=engine))
    mapper(Author, authors_table)
    mapper(TAuthor, temp_authors_table)
    mapper(Book, song_books_table)
    mapper(Song, songs_table,
        properties={'authors': relation(Author, backref='songs',
                                       secondary=authors_songs_table),
                   'book': relation(Book, backref='songs'),
                   'topics': relation(Topic, backref='songs',
                                      secondary=songs_topics_table)})
    mapper(TSong, temp_songs_table)
    mapper(TSongAuthor, temp_authors_songs_table)
    mapper(Topic, topics_table)
    return session

temp_authors_table = Table(u'authors_temp', metadata,
    Column(u'authorid', types.Integer, primary_key=True),
    Column(u'authorname', String(40))
)

temp_songs_table = Table(u'songs_temp', metadata,
    Column(u'songid', types.Integer, primary_key=True),
    Column(u'songtitle', String(60)),
    Column(u'lyrics', types.UnicodeText),
    Column(u'copyrightinfo', String(255)),
    Column(u'settingsid', types.Integer)
)

# Definition of the "authors_songs" table
temp_authors_songs_table = Table(u'songauthors_temp', metadata,
    Column(u'authorid', types.Integer, primary_key=True),
    Column(u'songid', types.Integer)
)

class TAuthor(BaseModel):
    """
    Author model
    """
    pass

class TSong(BaseModel):
    """
    Author model
    """
    pass

class TSongAuthor(BaseModel):
    """
    Author model
    """
    pass

class MigrateSongs(object):
    def __init__(self, display):
        self.display = display
        self.data_path = AppLocation.get_section_data_path(u'songs')
        self.database_files = SettingsManager.get_files(u'songs', u'.sqlite')
        print self.database_files

    def process(self):
        self.display.output(u'Songs processing started')
        for f in self.database_files:
            self.v_1_9_0(f)
        self.display.output(u'Songs processing finished')

    def v_1_9_0(self, database):
        self.display.output(u'Migration 1.9.0 Started for ' + database)
        self._v1_9_0_old(database)
        self._v1_9_0_new(database)
        self._v1_9_0_cleanup(database)
        self.display.output(u'Migration 1.9.0 Finished for ' + database)

    def _v1_9_0_old(self, database):
        self.display.sub_output(u'Rename Tables ' + database)
        conn = sqlite3.connect(self.data_path + os.sep + database)
        conn.execute(u'alter table authors rename to authors_temp;')
        conn.commit()
        conn.execute(u'alter table songs rename to songs_temp;')
        conn.commit()
        conn.execute(u'alter table songauthors rename to songauthors_temp;')
        conn.commit()

    def _v1_9_0_new(self, database):
        self.display.sub_output(u'Create new Tables ' + database)
        self.db_url = u'sqlite:///' + self.data_path + u'/songs.sqlite'
        print self.db_url
        self.session = init_models(self.db_url)
        metadata.create_all(checkfirst=True)
        results = self.session.query(TSong).order_by(TSong.songid).all()
        for songs_temp in results:
            song = Song()
            song.title = songs_temp.songtitle
            song.lyrics = songs_temp.lyrics.replace(u'\r\n', u'\n')
            song.copyright = songs_temp.copyrightinfo
            song.search_title = u''
            song.search_lyrics = u''
            print songs_temp.songtitle
            aa = self.session.execute(
                u'select * from songauthors_temp where songid =' + \
                unicode(songs_temp.songid))
            for row in aa:
                a = row['authorid']
                authors_temp = self.session.query(TAuthor).get(a)
                bb = self.session.execute(
                    u'select * from authors where display_name = \"%s\"' % \
                    unicode(authors_temp.authorname)).fetchone()
                if bb is None:
                    author = Author()
                    author.display_name = authors_temp.authorname
                    author.first_name = u''
                    author.last_name = u''
                else:
                    author = self.session.query(Author).get(bb[0])
                song.authors.append(author)
            try:
                self.session.add(song)
                self.session.commit()
            except InvalidRequestError:
                self.session.rollback()
                print u'Error thrown = ', sys.exc_info()[1]

    def _v1_9_0_cleanup(self, database):
        self.display.sub_output(u'Update Internal Data ' + database)
        conn = sqlite3.connect(self.data_path + os.sep + database)
        conn.execute("""update songs set search_title =
            replace(replace(replace(replace(replace(replace(replace(replace(
            replace(title, '&', 'and'), ',', ''), ';', ''), ':', ''),
            '(u', ''), ')', ''), '{', ''), '}',''),'?','');""")
        conn.execute("""update songs set search_lyrics =
            replace(replace(replace(replace(replace(replace(replace(replace(
            replace(lyrics, '&', 'and'), ',', ''), ';', ''), ':', ''),
            '(u', ''), ')', ''), '{', ''), '}',''),'?','')
            ;""")
        conn.commit()
        conn.execute(u'drop table authors_temp;')
        conn.commit()
        conn.execute(u'drop table songs_temp;')
        conn.commit()
        conn.execute(u'drop table songauthors_temp;')
        conn.commit()
        conn.execute(u'drop table settings;')
        conn.commit()
