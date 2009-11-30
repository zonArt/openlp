# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Tim Bentley, Jonathan Corwin, Michael      #
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

from types import StringType, ListType

sys.path.append(os.path.abspath(u'./../../../..'))

from openlp.core.lib import XmlRootClass

class SongException(Exception):
    pass

class SongTitleError(SongException):
    pass

class SongTypeError(SongException):
    pass

class SongSlideError(SongException):
    pass

class SongFeatureError(SongException):
    pass

# TODO: Song: Logging - not all, but enough
# TODO: Song: Handle OpenLP2 format
# TODO: Song: Import OpenLP1
# TODO: Song: Export OpenLP1
# TODO: Song: Export Song to CCLI
# TODO: Song: Export Song to OpenSong
# TODO: Song: Import ChangingSong
# TODO: Song: Export ChangingSong

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

    def __init__(self, xmlContent = None):
        """Initialize from given xml content"""
        super(_OpenSong, self).__init__()
        self.from_buffer(xmlContent)

    def _reset(self):
        """Reset all song attributes"""
        global _blankOpenSongXml
        self._setFromXml(_blankOpenSongXml, 'song')

    def from_buffer(self, xmlContent):
        """Initialize from buffer(string) with xml content"""
        self._reset()
        if xmlContent:
            self._setFromXml(xmlContent, 'song')

    def get_author_list(self):
        """Convert author field to an authorlist

        in OpenSong an author list may be separated by '/'
        return as a string
        """
        if self.author:
            list = self.author.split(u' and ')
            res = [item.strip() for item in list]
            return u', '.join(res)

    def get_category_array(self):
        """Convert theme and alttheme into category_array

        return as a string
        """
        res = []
        if self.theme:
            res.append(self.theme)
        if self.alttheme:
            res.append(self.alttheme)
        s = u', u'.join(res)
        return s

    def _reorder_verse(self, tag, tmpVerse):
        """
        Reorder the verse in case of first char is a number
        tag -- the tag of this verse / verse group
        tmpVerse -- list of strings
        """
        res = []
        for c in '1234567890 ':
            tagPending = True
            for l in tmpVerse:
                if l.startswith(c):
                    if tagPending:
                        tagPending = False
                        t = tag.strip(u'[]').lower()
                        if 'v' == t:
                            newtag = "Verse"
                        elif 'c' == t:
                            newtag = "Chorus"
                        elif 'b' == t:
                            newtag = "Bridge"
                        elif 'p' == t:
                            newtag = "Pre-chorus"
                        else:
                            newtag = t
                        s = (u'# %s %s'%(newtag, c)).rstrip()
                        res.append(s)
                    res.append(l[1:])
                if (len(l) == 0) and (not tagPending):
                    res.append(l)
        return res

    def get_lyrics(self):
        """
        Convert the lyrics to openlp lyrics format
        return as list of strings
        """
        lyrics = self.lyrics.split(u'\n')
        tmpVerse = []
        finalLyrics = []
        tag = ""
        for l in lyrics:
            line = l.rstrip()
            if not line.startswith(u'.'):
                # drop all chords
                tmpVerse.append(line)
                if len(line) > 0:
                    if line.startswith(u'['):
                        tag = line
                else:
                    r = self._reorder_verse(tag, tmpVerse)
                    finalLyrics.extend(r)
                    tag = ""
                    tmpVerse = []
        # catch up final verse
        r = self._reorder_verse(tag, tmpVerse)
        finalLyrics.extend(r)
        return finalLyrics


class Song(object):
    """Handling song properties and methods

    handles all conversions between various input and output formats

    CCLI:
        from_ccli_text_file
        to_ccli_text_file
        from_ccli_text_buffer
        to_ccli_text_buffer

    OpenSong:
        from_opensong_file
        to_opensong_file
        from_opensong_buffer
        to_opensong_buffer

    presentation (screen):
        get_number_of_slides
        get_preview_slide
        get_render_slide

    openlp1:
        from_openlp1_lyrics_buffer
        to_openlp1_lyrics_buffer
        set_author_list
        get_author_list

    editing and openlp2:
        set_*
        get_*
    """

    def __init__(self, songid = 0):
        """Initialize song object

        songid -- database id for this song
        title -- title of the song
        search_title -- title without punctuation chars
        author_list -- list of authors
        song_cclino -- CCLI number for this song
        copyright -- copyright string
        show_title -- 0: no show, 1: show
        show_author_list -- 0: no show, 1: show
        show_copyright -- 0: no show, 1: show
        show_song_cclino -- 0: no show, 1: show
        theme -- name of theme or blank
        category_array -- list of user defined properties (hymn, gospel)
        song_book -- name of originating book
        song_number -- number of the song, related to a songbook
        comments -- free comment
        verse_order -- presentation order of the slides
        lyrics -- text format
        search_lyrics -- lowercase lyrics without punctuation
        """
        self.songid = songid
        self._reset()

    def _reset(self):
        """Reset all song attributes"""
        self.slideList = []
        self.set_title(u'BlankSong')
        self.author_list = None
        self.song_cclino = ""
        self.copyright = ""
        self.show_author_list = 1
        self.show_copyright = 1
        self.show_song_cclino = 1
        self.show_title = 1
        self.theme = ""
        self.category_array = None
        self.song_book = ""
        self.song_number = ""
        self.comments = ""
        self.verse_order = ""
        self.set_lyrics(u'')
        return

    def set_songid(self, songid):
        """Set the songid for the database"""
        self.songid = songid

    def get_songid(self):
        """Return the songid for the database"""
        return self.songid

    def from_opensong_buffer(self, xmlcontent):
        """Initialize from buffer(string) of xml lines in opensong format"""
        self._reset()
        opensong = _OpenSong(xmlcontent)
        if opensong.title:
            self.set_title(opensong.title)
        if opensong.copyright:
            self.set_copyright(opensong.copyright)
        if opensong.presentation:
            self.set_verse_order(opensong.presentation)
        if opensong.ccli:
            self.set_song_cclino(opensong.ccli)
        self.set_author_list(opensong.get_author_list())
        self.set_category_array(opensong.get_category_array())
        self.set_lyrics(opensong.get_lyrics())

    def from_opensong_file(self, xmlfilename):
        """
        Initialize from file containing xml
        xmlfilename -- path to xml file
        """
        osfile = None
        try:
            osfile = open(xmlfilename, 'r')
            list = [line for line in osfile]
            osfile.close()
            xml = "".join(list)
            self.from_opensong_buffer(xml)
        except:
            log.exception(u'Failed to load opensong xml file')
        finally:
            if osfile:
                osfile.close()

    def _remove_punctuation(self, title):
        """Remove the puntuation chars from title

        chars are: .,:;!?&%#/\@`$'|"^~*-
        """
        punctuation = ".,:;!?&%#'\"/\\@`$|^~*-"
        s = title
        for c in punctuation:
            s = s.replace(c, '')
        return s

    def set_title(self, title):
        """Set the song title

        title (string)
        raises SongTitleError if the title is empty
        raises SongTitleError if the seach_title is empty
        """
        self.title = title.strip()
        self.search_title = self._remove_punctuation(title).strip()
        if len(self.title) < 1:
            raise SongTitleError(u'The title is empty')
        if len(self.search_title) < 1:
            raise SongTitleError(u'The searchable title is empty')

    def get_title(self):
        """Return title value"""
        return self.title

    def get_search_title(self):
        """Return search_title"""
        return self.search_title

    def from_ccli_text_buffer(self, textList):
        """
        Create song from a list of texts (strings) - CCLI text format expected

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
        for l in textList:
            n += 1
            if lastpart > 0:
                lastpart += 1
                if lastpart == 2:
                    sCopyright = l[1:].strip()
                if lastpart == 3:
                    sAuthor = l
            elif l.startswith(u'CCLI Song'):
                sCcli = l[13:].strip()
                lastpart = 1
            else:
                if metMisc:
                    metMisc = False
                    if l.upper().startswith(u'(BRIDGE)'):
                        lyrics.append(u'# Bridge')
                    # otherwise unknown misc keyword
                elif l.startswith(u'Misc'):
                    metMisc = True
                elif l.startswith(u'Verse') or l.startswith(u'Chorus'):
                    lyrics.append(u'# %s'%l)
                else:
                    # should we remove multiple blank lines?
                    if n == 1:
                        sName = l
                    else:
                        lyrics.append(l)
        # split on known separators
        lst = sAuthor.split(u'/')
        if len(lst) < 2:
            lst = sAuthor.split(u'|')
        author_list = u', '.join(lst)
        self.set_title(sName)
        self.set_author_list(author_list)
        self.set_copyright(sCopyright)
        self.set_song_cclino(sCcli)
        self.set_lyrics(lyrics)

    def from_ccli_text_file(self, textFileName):
        """
        Create song from a list of texts read from given file
        textFileName -- path to text file
        """
        ccli_file = None
        try:
            ccli_file = open(textFileName, 'r')
            lines = [orgline.rstrip() for orgline in ccli_file]
            self.from_ccli_text_buffer(lines)
        except:
            log.exception(u'Failed to load CCLI text file')
        finally:
            if ccli_file:
                ccli_file.close()

    def _assure_string(self, string_in):
        """Force a string is returned"""
        if string_in is None:
            string_out = ""
        else:
            string_out = unicode(s)
        return string_out

    def _split_to_list(self, aString):
        """Split a string into a list - comma separated"""
        if aString:
            list = aString.split(u',')
            res = [item.strip() for item in list]
            return res

    def _list_to_string(self, strOrList):
        """Force a possibly list into a string"""
        if type(strOrList) == StringType:
            lst = self._split_to_list(strOrList)
        elif type(strOrList) == ListType:
            lst = strOrList
        elif strOrList is None:
            lst = []
        else:
            raise SongTypeError(u'Variable not String or List')
        string = u', '.join(lst)
        return string

    def get_copyright(self):
        """Return copyright info string"""
        return self._assure_string(self.copyright)

    def set_copyright(self, copyright):
        """Set the copyright string"""
        self.copyright = copyright

    def get_song_cclino(self):
        """Return the songCclino"""
        return self._assure_string(self.song_cclino)

    def set_song_cclino(self, song_cclino):
        """Set the song_cclino"""
        self.song_cclino = song_cclino

    def get_theme(self):
        """Return the theme name for the song"""
        return self._assure_string(self.theme)

    def set_theme(self, theme):
        """Set the theme name (string)"""
        self.theme = theme

    def get_song_book(self):
        """Return the song_book (string)"""
        return self._assure_string(self.song_book)

    def set_song_book(self, song_book):
        """Set the song_book (string)"""
        self.song_book = song_book

    def get_song_number(self):
        """Return the song_number (string)"""
        return self._assure_string(self.song_number)

    def set_song_number(self, song_number):
        """Set the song_number (string)"""
        self.song_number = song_number

    def get_comments(self):
        """Return the comments (string)"""
        return self._assure_string(self.comments)

    def set_comments(self, comments):
        """Set the comments (string)"""
        self.comments = comments

    def get_verse_order(self):
        """Get the verseOrder (string) - preferably space delimited"""
        return self._assure_string(self.verse_order)

    def set_verse_order(self, verse_order):
        """Set the verse order (string) - space delimited"""
        self.verse_order = verse_order

    def get_author_list(self, asOneString = True):
        """Return the list of authors as a string

        asOneString
        True -- string:
          "John Newton, A Parker"
        False -- list of strings
          ["John Newton", u'A Parker"]
        """
        if asOneString:
            res = self._assure_string(self.author_list)
        else:
            res = self._split_to_list(self.author_list)
        return res

    def set_author_list(self, author_list):
        """Set the author_list

        author_list -- a string or list of strings
        """
        if author_list is None:
            self.author_list = None
        else:
            self.author_list = self._list_to_string(author_list)

    def get_category_array(self, asOneString = True):
        """Return the list of categories as a string

        asOneString
        True -- string:
          "Hymn, Gospel"
        False -- list of strings
          ["Hymn", u'Gospel"]
        """
        if asOneString:
            res = self._assure_string(self.category_array)
        else:
            res = self._split_to_list(self.category_array)
        return res

    def set_category_array(self, category_array):
        """Set the category_array

        category_array -- a string or list of strings
        """
        if category_array is None:
            self.category_array = None
        else:
            self.category_array = self._list_to_string(category_array)

    def get_show_title(self):
        """Return the show_title flag (bool)"""
        return self.show_title

    def set_show_title(self, show_title):
        """Set the show_title flag (bool)"""
        self.show_title = show_title

    def get_show_author_list(self):
        """Return the show_author_list flag"""
        return self.show_author_list

    def set_show_author_list(self, show_author_list):
        """Set the show_author_list flag (bool)"""
        self.show_author_list = show_author_list

    def get_show_copyright(self):
        """Return the show_copyright flag"""
        return self.show_copyright

    def set_show_copyright(self, show_copyright):
        """Set the show_copyright flag (bool)"""
        self.show_copyright = show_copyright

    def get_show_song_cclino(self):
        """Return the showSongCclino (string)"""
        return self.show_song_cclino

    def set_show_song_cclino(self, show_song_cclino):
        """Set the show_song_cclino flag (bool)"""
        self.show_song_cclino = show_song_cclino

    def get_lyrics(self):
        """Return the lyrics as a list of strings

        this will return all the strings in the song
        """
        return self.lyrics

    def set_lyrics(self, lyrics):
        """Set the lyrics as a list of strings"""
        self.lyrics = lyrics
        self._parse_lyrics()

    def _parse_lyrics(self):
        """Parse lyrics into the slidelist"""
        # TODO: check font formatting
        self.slideList = []
        tmpSlide = []
        metContent = False
        for l in self.lyrics:
            if len(l) > 0:
                metContent = True
                tmpSlide.append(l)
            else:
                if metContent:
                    metContent = False
                    self.slideList.append(tmpSlide)
                    tmpSlide = []
        #
        if len(tmpSlide) > 0:
            self.slideList.append(tmpSlide)

    def get_number_of_slides(self):
        """Return the number of slides in the song (int)"""
        numOfSlides = len(self.slideList)
        return numOfSlides

    def get_preview_slide(self, slideNumber):
        """Return the preview text for specified slide number

        slideNumber -- 0: all slides, 1..n: specific slide
        a list of strings are returned
        """
        num = len(self.slideList)
        if num < 1:
            raise SongSlideError(u'No slides in this song')
        elif slideNumber > num:
            raise SongSlideError(u'Slide number too high')
        if slideNumber > 0:
            # return this slide
            res = self.slideList[slideNumber-1]
            # find theme in this slide
        else:
            res = []
            for i in range(num):
                if i > 0:
                    res.append(u'')
                res.extend()
        # remove formattingincluding themes
        return res

    def get_render_slide(self, slideNumber):
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
        if num < 1:
            raise SongSlideError(u'No slides in this song')
        elif slideNumber > num:
            raise SongSlideError(u'Slide number too high')
        res = []
        if self.show_title:
            title = self.get_title()
        else:
            title = ""
        if self.show_author_list:
            author = self.get_author_list(True)
        else:
            author = ""
        if self.show_copyright:
            cpright = self.get_copyright()
        else:
            cpright = ""
        if self.show_song_cclino:
            ccli = self.get_song_cclino()
        else:
            ccli = ""
        theme = self.get_theme()
        # examine the slide for a theme
        res.append(theme)
        res.append(title)
        res.append(author)
        res.append(cpright)
        res.append(ccli)
        # append the correct slide
        return res

__all__ = ['SongException', 'SongTitleError', 'SongSlideError', 'SongTypeError',
           'SongFeatureError', 'Song']
