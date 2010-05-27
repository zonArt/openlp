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
from sqlalchemy.orm import scoped_session, sessionmaker, mapper

from openlp.core.lib import SettingsManager
from openlp.core.utils import AppLocation
from openlp.plugins.bibles.lib.models import *
    
class TBibleMeta(BaseModel):
    """
    Bible Meta Data
    """
    pass

class TTestament(BaseModel):
    """
    Bible Testaments
    """
    pass

class TBook(BaseModel):
    """
    Song model
    """
    pass

class TVerse(BaseModel):
    """
    Topic model
    """
    pass
    
temp_meta_table = Table(u'metadata_temp', metadata,
    Column(u'key', types.Unicode(255), primary_key=True),
    Column(u'value', types.Unicode(255)),
)
temp_testament_table = Table(u'testament_temp', metadata,
    Column(u'id', types.Integer, primary_key=True),
    Column(u'name', types.Unicode(30)),
)
temp_book_table = Table(u'book_temp', metadata,
    Column(u'id', types.Integer, primary_key=True),
    Column(u'testament_id', types.Integer),
    Column(u'name', types.Unicode(30)),
    Column(u'abbreviation', types.Unicode(5)),
)
temp_verse_table = Table(u'verse_temp', metadata,
    Column(u'id', types.Integer, primary_key=True),
    Column(u'book_id', types.Integer),
    Column(u'chapter', types.Integer),
    Column(u'verse', types.Integer),
    Column(u'text', types.UnicodeText),
)

mapper(TBibleMeta, temp_meta_table)
mapper(TTestament, temp_testament_table)
mapper(TBook, temp_book_table)
mapper(TVerse, temp_verse_table)

def init_models(url):
    engine = create_engine(url)
    metadata.bind = engine
    session = scoped_session(sessionmaker(autoflush=False,
        autocommit=False, bind=engine))
    return session

class MigrateBibles(object):
    def __init__(self, display):
        self.display = display
        self.data_path = AppLocation.get_section_data_path(u'bibles')
        self.database_files = SettingsManager.get_files(u'bibles', u'.sqlite')
        print self.database_files

    def progress(self, text):
        print text
        self.display.output(text)

    def process(self):
        self.progress(u'Bibles processing started')
        for f in self.database_files:
            self.v_1_9_0(f)
        self.progress(u'Bibles processing finished')

    def v_1_9_0(self, database):
        self.progress(u'Migration 1.9.0 Started for ' + database)
        self._v1_9_0_old(database)
        self._v1_9_0_new(database)
        self._v1_9_0_cleanup(database)
        self.progress(u'Migration 1.9.0 Finished for ' + database)

    def _v1_9_0_old(self, database):
        self.progress(u'Rename Tables ' + database)
        conn = sqlite3.connect(os.path.join(self.data_path, database))
        conn.execute(u'alter table book rename to book_temp;')
        conn.commit()
        conn.execute(u'alter table testament rename to testament_temp;')
        conn.commit()
        conn.execute(u'alter table verse rename to verse_temp;')
        conn.commit()
        conn.execute(u'alter table metadata rename to metadata_temp;')
        conn.commit()

    def _v1_9_0_new(self, database):
        self.progress(u'Create new Tables ' + database)
        self.db_url = u'sqlite:///' + self.data_path + u'/' + database 
        print self.db_url
        self.session = init_models(self.db_url)
        metadata.create_all(checkfirst=True)
        self.progress(u'Create testament table')
        results = self.session.query(TTestament).order_by(TTestament.id).all()
        for testament_temp in results:
            testament = Testament()
            testament.id = testament_temp.id
            testament.name = testament_temp.name
            try:
                self.session.add(testament)
                self.session.commit()
            except InvalidRequestError:
                self.session.rollback()
                print u'Error thrown = ', sys.exc_info()[1]
        self.progress(u'Create book table')
        results = self.session.query(TBook).order_by(TBook.id).all()
        for book_temp in results:
            book = Book()
            book.id = book_temp.id
            book.testament_id = book_temp.testament_id
            book.name = book_temp.name
            book.abbreviation = book_temp.abbreviation
            try:
                self.session.add(book)
                self.session.commit()
            except InvalidRequestError:
                self.session.rollback()
                print u'Error thrown = ', sys.exc_info()[1]
        self.progress(u'Create verse table')
        results = self.session.query(TVerse).order_by(TVerse.id).all()
        for verse_temp in results:
            verse = Verse()
            verse.id = verse_temp.id
            verse.book_id = verse_temp.book_id
            verse.chapter = verse_temp.chapter
            verse.verse = verse_temp.verse
            verse.text = verse_temp.text
            try:
                self.session.add(verse)
                self.session.commit()
            except InvalidRequestError:
                self.session.rollback()
                print u'Error thrown = ', sys.exc_info()[1]
        self.progress(u'Create metadata table')
        results = self.session.query(TBibleMeta).order_by(TBibleMeta.key).all()
        for biblemeta_temp in results:
            biblemeta = BibleMeta()
            biblemeta.key = biblemeta_temp.key
            biblemeta.value = biblemeta_temp.value
            try:
                self.session.add(biblemeta)
                self.session.commit()
            except InvalidRequestError:
                self.session.rollback()
                print u'Error thrown = ', sys.exc_info()[1]

    def _v1_9_0_cleanup(self, database):
        self.progress(u'Update Internal Data ' + database)
        conn = sqlite3.connect(os.path.join(self.data_path, database))
        conn.commit()
        conn.execute(u'drop table book_temp;')
        conn.commit()
        conn.execute(u'drop table testament_temp;')
        conn.commit()
        conn.execute(u'drop table verse_temp;')
        conn.commit()
        conn.execute(u'drop table metadata_temp;')
        conn.commit()
        conn.execute(u'vacuum;')
        conn.commit()

