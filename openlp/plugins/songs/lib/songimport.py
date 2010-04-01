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

import string
from openlp.core.lib import SongXMLBuilder
from openlp.plugins.songs.lib.models import Song
        
class SongImport(object):
    """
    Helper class for import a song from a third party source into OpenLP

    This class just takes the raw strings, and will work out for itself
    whether the authors etc already exist and add them or refer to them 
    as necessary
    """

    def __init__(self, song_manager):
        """
        Initialise and create defaults for properties
        
        song_manager is an instance of a SongManager, through which all
        database access is performed
        """
        self.song_manager = song_manager
        self.title = u''
        self.song_number = u''
        self.copyright = u''
        self.comment = u''
        self.theme_name = u''
        self.ccli_number = u''    
        self.authors = []           
        self.topics = []            
        self.song_book_name = u''   
        self.song_book_pub = u''   
        self.verse_order_list = []  
        self.verses = []            
        self.versecount = 0
        self.choruscount = 0
       
    def get_title(self):
        """
        Return the title
        """
        return self.title
        
    def get_copyright(self):
        """
        Return the copyright
        """
        return self.copyright
        
    def get_song_number(self):
        """ 
        Return the song number (also known as alternate title)
        """
        return self.song_number
        
    def set_title(self, title):
        """
        Set the title
        """
        self.title = title
 
    def set_song_number(self, song_number):
        """ 
        Set the song number/alternate title
        """
        self.song_number = song_number
        
    def set_song_book(self, song_book, publisher):
        """
        Set the song book name and publisher
        """
        self.song_book_name = song_book
        self.song_book_pub = publisher

    def add_copyright(self, copyright):
        """ 
        Build the copyright field
        """
        if self.copyright != u'':
            self.copyright += ' '
        self.copyright += copyright

    def add_author(self, text):
        """ 
        Add an author to the list
        """
        self.authors.append(text)
        
    def add_verse(self, verse, versetag):
        """
        Add a verse. This is the whole verse, lines split by \n
        Verse tag can be V1/C1/B1 etc, or 'V' and 'C' (will count the verses/
        choruses itself) or None, where it will assume verse
        It will also attempt to detect duplicates. In this case it will just
        add to the verse order
        """        
        for (oldversetag, oldverse) in self.verses:
            if oldverse.strip() == verse.strip():
                self.verse_order_list.append(oldversetag)
                return
        if versetag == u'C':
            self.choruscount += 1
            versetag += unicode(self.choruscount)
        if versetag == u'V' or not versetag:
            self.versecount += 1
            versetag = u'V' + unicode(self.versecount)
        self.verses.append([versetag, verse])
        self.verse_order_list.append(versetag)
        if self.choruscount > 0 and not versetag.startswith(u'C'):
            self.verse_order_list.append(u'C1')

    def repeat_verse(self):
        """
        Repeat the previous verse in the verse order
        """
        self.verse_order_list.append(self.verse_order_list[-1])
    
    def check_complete(self):
        """
        Check the mandatory fields are entered (i.e. title and a verse)
        Author not checked here, if no author then "Author unknown" is 
        automatically added
        """
        if self.title == u'' or len(self.verses) == 0:
            return False
        else:
            return True
            
    def remove_punctuation(self, text):	
        """
        Remove punctuation from the string for searchable fields
        """
        return text.translate(string.maketrans(u'',u''), string.punctuation)
            
    def finish(self):
        """
        All fields have been set to this song. Write it away
        """
        if len(self.authors) == 0:
            self.authors.append(u'Author unknown')
        #self.commit_song()
        self.print_song()
        
    def commit_song():
        """
        Write the song and it's fields to disk
        """
        song = Song()
        song.title = self.title
        song.search_title = self.remove_punctuation(self.title)
        song.song_number = self.song_number
        song.search_lyrics = u''
        sxml = SongXMLBuilder()
        sxml.new_document()
        sxml.add_lyrics_to_song()
        for (versetag, versetext) in self.verses:
            if versetag[0] == u'C':
                versetype = u'Chorus'
            elif versetag[0] == u'V':
                versetype = u'Verse'
            elif versetag[0] == u'B':
                versetype = u'Bridge'
            elif versetag[0] == u'I':
                versetype = u'Intro'
            elif versetag[0] == u'P':
                versetype = u'Prechorus'
            elif versetag[0] == u'E':
                versetype = u'Ending'
            else:
                versetype = u'Other'
            sxml.add_verse_to_lyrics(versetype, versetag[1:], versetext)
            song.search_lyrics += u' ' + self.remove_punctuation(versetext)
        song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
        song.verse_order = u' '.join(self.verse_order_list)
        song.copyright = self.copyright
        song.comment = self.comment 
        song.theme_name = self.theme_name 
        song.ccli_number = self.ccli_number 
        for authortext in self.authors:
            author = None
            # read the author here
            if author is None:
                author = Author()
                author.display_name = authortext
                author.last_name = authortext.split(u' ')[-1]
                author.first_name = u' '.join(authortext.split(u' ')[:-1])
                # write the author here
            song.authors.append(author)
        if self.song_book_name:
            song_book = None
            # read the book here
            if song_book is None:
                song_book = Book()
                song_book.name = self.song_book_name
                song_book.publisher = self.song_book_pub
                # write the song book here
            song.song_book_id = song_book.id
        for topictext in self.topics:
            topic = None
            # read the topic here 
            if topic is None:
                topic = Topic()
                topic.name = topictext
                # write the topic here
            song.topics.append(topictext)
        # write the song here
        
    def print_song(self):
        """ 
        For debugging 
        """
        print u'========================================'   \
            + u'========================================'
        print u'TITLE: ' + self.title 
        for (versetag, versetext) in self.verses:
            print u'VERSE ' + versetag + u': ' + versetext
        print u'ORDER: ' + u' '.join(self.verse_order_list)
        for author in self.authors:
            print u'AUTHOR: ' + author
        if self.copyright:
            print u'COPYRIGHT: ' + self.copyright
        if self.song_book_name:
            print u'BOOK: ' + self.song_book_name
        if self.song_number:
            print u'NUMBER: ' + self.song_number
        for topictext in self.topics:        
            print u'TOPIC: ' + topictext
        if self.comment:
            print u'COMMENT: ' + self.comment
        if self.theme_name:
            print u'THEME: ' + self.theme_name
        if self.ccli_number:
            print u'CCLI: ' + self.ccli_number
            

