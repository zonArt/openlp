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
import os.path
import sys
import time
import datetime
import logging
import string

from sqlalchemy import  *
from sqlalchemy.sql import select
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from openlp.plugins.songs.lib.songtables import *
from openlp.plugins.songs.lib.songclasses import *

from openlp.core.utils import ConfigHelper

class SongDBException(Exception):
    pass
class SongInvalidDatabaseError(Exception):
    pass
    
class SongDBImpl():
    global log     
    log=logging.getLogger("SongDBImpl")
    log.info("SongDBImpl loaded")   
    def __init__(self, songpath , songname, suffix, btype = 'sqlite'):   
        # Connect to database 
        self.songfile = os.path.join(songpath, songname)
        log.debug( "Load Song on path %s", self.songfile)

        if btype == 'sqlite': 
            self.db = create_engine("sqlite:///"+self.songfile, encoding='utf-8' , convert_unicode=False, assert_unicode=False)
        elif btype == 'mysql': 
            self.db = create_engine("mysql://tim:@192.168.0.100:3306/openlp_song")
        else:
            raise SongInvalidDatabaseError("Database not mysql or sqlite")
        self.db.echo = True
        metadata.bind = self.db
        metadata.bind.echo = False
        self.Session = scoped_session(sessionmaker(autoflush=True, autocommit=False))
        self.Session.configure(bind=self.db)
        
    def save_author(self, author):
        log.debug( "add_author %s,%s,%s", author.display_name, author.first_name, author.last_name)
        metadata.bind.echo = True
        session = self.Session()
        session.save_or_update(author)
        session.commit()
      
    def save_meta(self, key, value):
        metadata.bind.echo = False                
        session = self.Session()
        bmeta= BibleMeta(key, value)
        session.add(bmeta)
        session.commit()

    def get_meta(self, key):
        s = text (""" select value FROM metadata where key == :k """)
        return self.db.execute(s, k=key).fetchone()

    def delete_meta(self, key):
        metadata.bind.echo = False
        s = text (""" delete FROM meta where key == :k """)
        self.db.execute(s, k=key)

    def get_song(self, songid):
        log.debug( "get_song ") 
#        metadata.bind.echo = True
#        s = text (""" select * FROM songs where songid = :c """)
#        return self.db.execute(s, c=songid).fetchone()
        metadata.bind.echo = False
        session = self.Session()
        return session.query(Song).get(songid)
        
    def get_authors(self):
        log.debug( "get_authors ") 
        metadata.bind.echo = False
        session = self.Session()
        return session.query(Author).order_by(Author.display_name).all()
        
    def get_author(self, authorid):
        log.debug( "get_author %s" ,  authorid) 
#        metadata.bind.echo = True
#        s = text (""" select * FROM authors where authorid = :i """)
#        return self.db.execute(s, i=authorid).fetchone()
        session = self.Session()
        return session.query(Author).get(authorid)

        
    def delete_author(self, authorid):
        log.debug( "delete_author %s" ,  authorid) 
        metadata.bind.echo = True
#        s = text (""" delete FROM authors where authorid = :i """)
#        return self.db.execute(s, i=authorid)
        session = self.Session()
        author = session.query(Author).get(authorid)
        session.delete(author)
        session.commit()
 
        
    def update_author(self, authorid, author_name, first_name, last_name):
        log.debug( "update_author %s,%s,%s,%s" ,  authorid, author_name, first_name, last_name) 
        metadata.bind.echo = True
        s = text (""" update authors set authorname= :an ,first_name = :fn,last_name = :ln where authorid = :i """)
        return self.db.execute(s, an=author_name, fn=first_name, ln=last_name,  i=authorid)        

    def get_song_authors_for_author(self, authorid):
        log.debug( "get_song_authors for author %s ", authorid) 
        metadata.bind.echo = False        
        s = text (""" select * FROM authors_songs where author_id = :c """)
        return self.db.execute(s, c=authorid).fetchall()

    def get_song_authors_for_song(self, songid):
        log.debug( "get_song_authors for song %s ", songid) 
        metadata.bind.echo = False        
        s = text (""" select * FROM songauthors where songid = :c """)
        return self.db.execute(s, c=songid).fetchall()
 
    def get_song_from_lyrics(self,searchtext):
        log.debug( "get_song_from_lyrics %s",searchtext)
        metadata.bind.echo = False
        searchtext = unicode("%"+searchtext+"%")
#        s = text (""" SELECT s.songid AS songid, s.songtitle AS songtitle, a.authorname AS authorname FROM songs s OUTER JOIN songauthors sa ON s.songid = sa.songid OUTER JOIN authors a ON sa.authorid = a.authorid WHERE s.lyrics LIKE :t ORDER BY s.songtitle ASC """)
#        log.debug("Records returned from search %s", len(self.db.execute(s, t=searchtext).fetchall()))        
#        return self.db.execute(s, t=searchtext).fetchall()
        metadata.bind.echo = False
        session = self.Session()
        return session.query(Song).filter(Song.search_lyrics.like(searchtext)).order_by(Song.title).all()
        
    def get_song_from_title(self,searchtext):
        log.debug( "get_song_from_title %s",searchtext)
#        metadata.bind.echo = False
        searchtext = unicode("%"+searchtext+"%")
#        s = text (""" SELECT s.songid AS songid, s.songtitle AS songtitle, a.authorname AS authorname FROM songs s OUTER JOIN songauthors sa ON s.songid = sa.songid OUTER JOIN authors a ON sa.authorid = a.authorid WHERE s.songtitle LIKE :t ORDER BY s.songtitle ASC """)
#        log.debug("Records returned from search %s", len(self.db.execute(s, t=searchtext).fetchall()))        
#        return self.db.execute(s, t=searchtext).fetchall()
        metadata.bind.echo = False
        session = self.Session()
        return session.query(Song).filter(Song.search_title.like(searchtext)).order_by(Song.title).all()
    
    def get_song_from_author(self,searchtext):
        log.debug( "get_song_from_author %s",searchtext)
        metadata.bind.echo = False
        searchtext = "%"+searchtext+"%"
        s = text (""" SELECT s.songid AS songid, s.songtitle AS songtitle, a.authorname AS authorname FROM songs s OUTER JOIN songauthors sa ON s.songid = sa.songid OUTER JOIN authors a ON sa.authorid = a.authorid WHERE a.authorname LIKE :t ORDER BY s.songtitle ASC """)
        log.debug("Records returned from search %s", len(self.db.execute(s, t=searchtext).fetchall()))
        return self.db.execute(s, t=searchtext).fetchall()         
        
        
    def dump_songs(self):
        log.debug( ".........Dumping Songs Database")
        log.debug( "...............................Books ")     
        s = text (""" select * FROM authors """)
        log.debug( self.db.execute(s).fetchall())
