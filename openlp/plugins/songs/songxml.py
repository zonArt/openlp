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
from types import StringType, ListType, NoneType

sys.path.append(os.path.abspath("./../../.."))

from openlp.core.lib import XmlRootClass

class SongException(Exception):
    pass

class SongTitleError(SongException):
    pass

class SongTypeError(SongException):
    pass

class SongSlideError(SongException):
    pass

# TODO: Song: Logging - not all, but enough
# TODO: Song: Handle OpenLP2 format
# TODO: Song: Import OpenLP1
# TODO: Song: Export OpenLP1
# TODO: Song: Export Song to CCLI
# TODO: Song: Export Song to OpenSong
# TODO: Song: Import ChangingSong
# TODO: Song: Export ChangingSong

_blankSongXml = \
'''<?xml version="1.0" encoding="iso-8859-1"?>
<Song>
  <title>BlankSong</title>
  <searchableTitle></searchableTitle>
  <authorList></authorList>
  <songCcliNo></songCcliNo>
  <copyright></copyright>
  <showTitle>1</showTitle>
  <showAuthorList>1</showAuthorList>
  <showSongCcliNo>1</showSongCcliNo>
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

_blankOpenSongXml = \
'''<?xml version="1.0" encoding="UTF-8"?>
<song>
  <title></title>
  <author></author>
  <copyright></copyright>
  <presentation></presentation>
  <ccli></ccli>
  <lyrics></lyrics>
  <theme></theme>
  <alttheme></alttheme>
</song>
'''

class _OpenSong(XmlRootClass):
    """Class for import of OpenSogn"""

    def __init__(self,  xmlContent = None):
        """Initialize from given xml content"""
        super(_OpenSong, self).__init__()
        self.FromBuffer(xmlContent)

    def _reset(self):
        """Reset all song attributes"""
        global _blankOpenSongXml
        self._setFromXml(_blankOpenSongXml, "song")

    def FromBuffer(self,  xmlContent):
        """Initialize from buffer(string) with xml content"""
        self._reset()
        if xmlContent != None :
            self._setFromXml(xmlContent, "song")

    def GetAuthorList(self):
        """Convert author field to an authorlist

        in OpenSong an author list may be separated by '/'
        return as a string
        """
        res = []
        if self.author != None :
            lst = self.author.split(' and ')
            for l in lst :
                res.append(l.strip())
        s = ", ".join(res)
        return s

    def GetCategoryArray(self):
        """Convert theme and alttheme into categoryArray

        return as a string
        """
        res = []
        if self.theme != None :
            res.append(self.theme)
        if self.alttheme != None :
            res.append(self.alttheme)
        s = ", ".join(res)
        return s

    def _reorderVerse(self, tag, tmpVerse):
        """Reorder the verse in case of first char is a number

        tag -- the tag of this verse / verse group
        tmpVerse -- list of strings
        """
        res = []
        for c in '1234567890 ':
            tagPending = True
            for l in tmpVerse :
                if l.startswith(c) :
                    if tagPending :
                        tagPending = False
                        t = tag.strip("[]").lower()
                        if 'v' == t :
                            newtag = "Verse"
                        elif 'c' == t :
                            newtag = "Chorus"
                        else :
                            #TODO: what is the tags for bridge, pre-chorus?
                            newtag = t
                        s = ("# %s %s"%(newtag, c)).rstrip()
                        res.append(s)
                    res.append(l[1:])
                if (len(l) == 0) and (not tagPending) :
                    res.append(l)
        return res

    def GetLyrics(self):
        """Convert the lyrics to openlp lyrics format

        return as list of strings
        """
        lyrics = self.lyrics.split("\n")
        tmpVerse = []
        finalLyrics = []
        tag = ""
        for l in lyrics:
            line = l.rstrip()
            if not line.startswith('.') :
                # drop all chords
                tmpVerse.append(line)
                if len(line) > 0 :
                    if line.startswith('['):
                        tag = line
                else :
                    r = self._reorderVerse(tag, tmpVerse)
                    finalLyrics.extend(r)
                    tag = ""
                    tmpVerse = []
        # catch up final verse
        r = self._reorderVerse(tag, tmpVerse)
        finalLyrics.extend(r)
        return finalLyrics


class Song(XmlRootClass) :
    """Class for handling song properties"""

    def __init__(self, xmlContent = None):
        """Initialize from given xml content

        xmlContent (string) -- xml formatted string

        title -- title of the song
        searchableTitle -- title without punctuation chars
        authorList -- list of authors
        songCcliNo -- CCLI number for this song
        copyright -- copyright string
        showTitle -- 0: no show, 1: show
        showAuthorList -- 0: no show, 1: show
        showCopyright -- 0: no show, 1: show
        showSongCcliNo -- 0: no show, 1: show
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
        if xmlContent != None :
            self._setFromXml(xmlContent, "Song")
            self._parseLyrics()

    def _reset(self):
        """Reset all song attributes"""
        global _blankSongXml
        self.slideList = []
        self._setFromXml(_blankSongXml, "Song")

    def FromOpenSongBuffer(self,  xmlcontent):
        """Initialize from buffer(string) of xml lines in opensong format"""
        self._reset()
        opensong = _OpenSong(xmlcontent)
        if opensong.title != None:
            self.SetTitle(opensong.title)
        if opensong.copyright != None :
            self.SetCopyright(opensong.copyright)
        if opensong.presentation != None:
            self.SetVerseOrder(opensong.presentation)
        if opensong.ccli != None:
            self.SetSongCcliNo(opensong.ccli)
        self.SetAuthorList(opensong.GetAuthorList())
        self.SetCategoryArray(opensong.GetCategoryArray())
        self.SetLyrics(opensong.GetLyrics())

    def FromOpenSongFile(self,  xmlfilename):
        """Initialize from file containing xml

        xmlfilename -- path to xml file
        """
        lst = []
        f = open(xmlfilename,  'r')
        for line in f :
            lst.append(line)
        f.close()
        xml = "".join(lst)
        self.FromOpenSongBuffer(xml)

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
        # extract the following fields
        # - name
        # - author
        # - CCLI no
        sName = ""
        sAuthor = ""
        sCopyright = ""
        sCcli = ""
        lastpart = 0
        n = 0
        metMisc = False
        lyrics = []
        for l in textList :
            n += 1
            if lastpart > 0 :
                lastpart += 1
                if lastpart == 2 :
                    sCopyright = l[1:].strip()
                if lastpart == 3 :
                    sAuthor = l
            elif l.startswith('CCLI Song') :
                sCcli = l[13:].strip()
                lastpart = 1
            else :
                if metMisc :
                    metMisc = False
                    if l.upper().startswith("(BRIDGE)") :
                        lyrics.append("# Bridge")
                    # otherwise unknown misc keyword
                elif l.startswith("Misc") :
                    metMisc = True
                elif l.startswith("Verse") or l.startswith("Chorus"):
                    lyrics.append("# %s"%l)
                else :
                    # should we remove multiple blank lines?
                    if n == 1 :
                        sName = l
                    else :
                        lyrics.append(l)
        # split on known separators
        lst = sAuthor.split('/')
        if len(lst) < 2:
            lst = sAuthor.split('|')
        authorList = ", ".join(lst)
        self.SetTitle(sName)
        self.SetAuthorList(authorList)
        self.SetCopyright(sCopyright)
        self.SetSongCcliNo(sCcli)
        self.SetLyrics(lyrics)

    def FromTextFile(self,  textFileName):
        """Create song from a list of texts read from given file

        textFileName -- path to text file
        """
        lines = []
        f = open(textFileName,  'r')
        for orgline in f:
            lines.append(orgline.rstrip())
        f.close()
        self.FromTextList(lines)

    def _assureString(self, s):
        """Force a string is returned"""
        if s == None :
            r = ""
        else :
            r = str(s)
        return r

    def _splitToList(self, aString):
        """Split a string into a list - comma separated"""
        res = []
        if aString != None :
            lst = aString.split(',')
            for l in lst :
                # remove whitespace
                res.append(l.strip())
        return res

    def _listToString(self, strOrList):
        """Force a possibly list into a string"""
        if type(strOrList) == StringType :
            lst = self._splitToList(strOrList)
        elif type(strOrList) == ListType :
            lst = strOrList
        elif type(strOrList) == NoneType :
            lst = []
        else :
            raise SongTypeError("Variable not String or List")
        s = ", ".join(lst)
        return s

    def GetCopyright(self):
        """Return copyright info string"""
        return self._assureString(self.copyright)

    def SetCopyright(self,  copyright):
        """Set the copyright string"""
        self.copyright = copyright

    def GetSongCcliNo(self):
        """Return the songCclino"""
        return self._assureString(self.songCcliNo)

    def SetSongCcliNo(self,  songCcliNo):
        """Set the songCcliNo"""
        self.songCcliNo = songCcliNo

    def GetTheme(self):
        """Return the theme name for the song"""
        return self._assureString(self.theme)

    def SetTheme(self,  theme):
        """Set the theme name (string)"""
        self.theme = theme

    def GetSongBook(self):
        """Return the songBook (string)"""
        return self._assureString(self.songBook)

    def SetSongBook(self,  songBook):
        """Set the songBook (string)"""
        self.songBook = songBook

    def GetSongNumber(self):
        """Return the songNumber (string)"""
        return self._assureString(self.songNumber)

    def SetSongNumber(self,  songNumber):
        """Set the songNumber (string)"""
        self.songNumber = songNumber

    def GetComments(self):
        """Return the comments (string)"""
        return self._assureString(self.comments)

    def SetComments(self,  comments):
        """Set the comments (string)"""
        self.comments = comments

    def GetVerseOrder(self):
        """Get the verseOrder (string) - preferably space delimited"""
        return self._assureString(self.verseOrder)

    def SetVerseOrder(self,  verseOrder):
        """Set the verseOrder (string) - space delimited"""
        self.verseOrder = verseOrder

    def GetAuthorList(self,  asOneString = True):
        """Return the list of authors as a string

        asOneString
        True -- string:
          "John Newton, A Parker"
        False -- list of strings
          ["John Newton", "A Parker"]
        """
        if asOneString :
            res = self._assureString(self.authorList)
        else :
            res = self._splitToList(self.authorList)
        return res

    def SetAuthorList(self,  authorList):
        """Set the authorList

        authorList -- a string or list of strings
        """
        if authorList == None :
            self.authorList = None
        else :
            self.authorList = self._listToString(authorList)

    def GetCategoryArray(self,  asOneString = True):
        """Return the list of categories as a string

        asOneString
        True -- string:
          "Hymn, Gospel"
        False -- list of strings
          ["Hymn", "Gospel"]
        """
        if asOneString :
            res = self._assureString(self.categoryArray)
        else :
            res = self._splitToList(self.categoryArray)
        return res

    def SetCategoryArray(self,  categoryArray):
        """Set the categoryArray

        categoryArray -- a string or list of strings
        """
        if categoryArray == None :
            self.categoryArray = None
        else :
            self.categoryArray = self._listToString(categoryArray)

    def GetShowTitle(self):
        """Return the showTitle flag (bool)"""
        return self.showTitle

    def SetShowTitle(self,  showTitle):
        """Set the showTitle flag (bool)"""
        self.showTitle = showTitle

    def GetShowAuthorList(self):
        """Return the showAuthorList flag"""
        return self.showAuthorList

    def SetShowAuthorList(self,  showAuthorList):
        """Set the showAuthorList flag (bool)"""
        self.showAuthorList = showAuthorList

    def GetShowCopyright(self):
        """Return the showCopyright flag"""
        return self.showCopyright

    def SetShowCopyright(self, showCopyright):
        """Set the showCopyright flag (bool)"""
        self.showCopyright = showCopyright

    def GetShowSongCcliNo(self):
        """Return the showSongCclino (string)"""
        return self.showSongCcliNo

    def SetShowSongCcliNo(self,  showSongCcliNo):
        """Set the showSongCcliNo flag (bool)"""
        self.showSongCcliNo = showSongCcliNo

    def GetLyrics(self):
        """Return the lyrics as a list of strings

        this will return all the strings in the song
        """
        return self.lyrics

    def SetLyrics(self,  lyrics):
        """Set the lyrics as a list of strings"""
        self.lyrics = lyrics
        self._parseLyrics()

    def _parseLyrics(self):
        """Parse lyrics into the slidelist"""
        # TODO: check font formatting
        self.slideList = []
        tmpSlide = []
        metContent = False
        for l in self.lyrics :
            if len(l) > 0 :
                metContent = True
                tmpSlide.append(l)
            else :
                if metContent :
                    metContent = False
                    self.slideList.append(tmpSlide)
                    tmpSlide = []
        #
        if len(tmpSlide) > 0:
            self.slideList.append(tmpSlide)

    def GetNumberOfSlides(self):
        """Return the number of slides in the song (int)"""
        numOfSlides = len(self.slideList)
        return numOfSlides

    def GetPreviewSlide(self,  slideNumber):
        """Return the preview text for specified slide number

        slideNumber -- 0: all slides, 1..n : specific slide
        a list of strings are returned
        """
        num = len(self.slideList)
        if num < 1 :
            raise SongSlideError("No slides in this song")
        elif slideNumber > num :
            raise SongSlideError("Slide number too high")
        if slideNumber > 0 :
            # return this slide
            res = self.slideList[slideNumber-1]
            # find theme in this slide
        else :
            res = []
            for i in range(num):
                if i > 0 :
                    res.append("")
                res.extend()
        # remove formattingincluding themes
        return res

    def GetRenderSlide(self,  slideNumber):
        """Return the slide to be rendered including the additional
        properties

        slideNumber -- 1 .. numberOfSlides
        Returns a list as:
        [theme (string),
         title (string),
         authorlist (string),
         copyright (string),
         cclino (string),
         lyric-part as a list of strings]
        """
        num = len(self.slideList)
        if num < 1 :
            raise SongSlideError("No slides in this song")
        elif slideNumber > num :
            raise SongSlideError("Slide number too high")
        res = []
        if self.showTitle :
            title = self.GetTitle()
        else :
            title = ""
        if self.showAuthorList :
            author = self.GetAuthorList(True)
        else :
            author = ""
        if self.showCopyright :
            cpright = self.GetCopyright()
        else :
            cpright = ""
        if self.showSongCcliNo :
            ccli = self.GetSongCcliNo()
        else :
            ccli = ""
        theme = self.GetTheme()
        # examine the slide for a theme
        res.append(theme)
        res.append(title)
        res.append(author)
        res.append(cpright)
        res.append(ccli)
        # append the correct slide
        return res

__all__ = ['SongException', 'SongTitleError', 'SongSlideError', 'SongTypeError',
           'Song']
