"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Carsten Tinggaard

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

import sys
import os
sys.path.append(os.path.abspath("./../.."))

from openlp.core.xmlrootclass import XmlRootClass

class SongException(Exception):
    pass

class SongTitleError(SongException):
    pass
    
blankSongXml = \
'''<?xml version="1.0" encoding="iso-8859-1"?>
<Song>
  <title>BlankSong</title>
  <searchableTitle></searchableTitle>
  <authorList></authorList>
  <songCcliNo></songCcliNo>
  <copyright></copyright>
  <showTitle>1</showTitle>
  <showAuthorList>1</showAuthorList>
  <showSongCcli>1</showSongCcli>
  <showCopyright>1</showCopyright>
  <theme></theme>
  <categoryArray></categoryArray>
  <songBook></songBook>
  <songNumber></songNumber>
  <comments></comments>
  <verseOrder></verseOrder>
  <lyrics></lyrics>
</Song>
'''

class Song(XmlRootClass) :
    """Class for handling song properties"""
    
    def __init__(self, xmlContent = None):
        """Initialize from given xml content
        
        xmlContent (string) -- xml formatted string
        
        attributes
            title -- title of the song
            searchableTitle -- title without punctuation chars
            authorList -- list of authors
            songCcliNo -- CCLI number for this song
            copyright -- copyright string
            showTitle -- 0: no show, 1: show
            showAuthorList -- 0: no show, 1: show
            showCopyright -- 0: no show, 1: show
            showCcliNo -- 0: no show, 1: show
            theme -- name of theme or blank
            categoryArray -- list of user defined properties (hymn, gospel)
            songBook -- name of originating book
            songNumber -- number of the song, related to a songbook
            comments -- free comment
            verseOrder -- presentation order of the slides
            lyrics -- simple or formatted (tbd)
        """
        super(Song, self).__init__()
        self._reset()
        
    def _reset(self):
        """Reset all song attributes"""
        global blankSongXml
        self._setFromXml(blankSongXml, "Song")
        
    def _RemovePunctuation(self,  title):
        """Remove the puntuation chars from title
        
        chars are: .,:;!?&%#/\@`$'|"^~*
        """
        punctuation = ".,:;!?&%#'\"/\\@`$|^~*"
        s = title
        for c in punctuation :
            s = s.replace(c,  '')
        return s
        
    def SetTitle(self, title):
        """Set the song title
        
        title (string)
        """
        self.title = title.strip()
        self.searchableTitle = self._RemovePunctuation(title).strip()
        if len(self.title) < 1 :
            raise SongTitleError("The title is empty")
        if len(self.searchableTitle) < 1 :
            raise SongTitleError("The searchable title is empty")
        
    def GetTitle(self):
        """Return title value"""
        return self.title
    
    def GetSearchableTitle(self):
        """Return searchableTitle"""
        return self.searchableTitle
    
    def FromTextList(self, textList):
        """Create song from a list of texts (strings) - CCLI text format expected
        
        textList (list of strings) -- the song
        """
        self._reset()
        # TODO: Implement CCLI text parse
        
    def FromTextFile(self,  textFileName):
        """Create song from a list of texts read from given file
        
        textFileName -- path to text file
        """
        textList = []
        f = open(textFileName,  'r')
        for line in f :
            textList.append(line)
        f.close()
        self.FromText(textList)
        
    
