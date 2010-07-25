# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

import logging

from types import ListType

log = logging.getLogger(__name__)

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

class Song(object):
    """Handling song properties and methods

    handles all conversions between various input and output formats

    CCLI:
        from_ccli_text_file
        to_ccli_text_file
        from_ccli_text_buffer
        to_ccli_text_buffer

    presentation (screen):
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
        theme_name -- name of theme or blank
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
        self.theme_name = ""
        self.category_array = None
        self.song_book = ""
        self.song_number = ""
        self.comments = ""
        self.verse_order = ""
        self.set_lyrics(u'')
        return

    def _remove_punctuation(self, title):
        """Remove the puntuation chars from title

        chars are: .,:;!?&%#/\@`$'|"^~*-
        """
        punctuation = ".,:;!?&%#'\"/\\@`$|^~*-"
        string = title
        for char in punctuation:
            string = string.replace(char, '')
        return string

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
        lineCount = 0
        metMisc = False
        lyrics = []
        for line in textList:
            lineCount += 1
            if lastpart > 0:
                lastpart += 1
                if lastpart == 2:
                    sCopyright = line[1:].strip()
                if lastpart == 3:
                    sAuthor = line
            elif line.startswith(u'CCLI Song'):
                sCcli = line[13:].strip()
                lastpart = 1
            else:
                if metMisc:
                    metMisc = False
                    if line.upper().startswith(u'(BRIDGE)'):
                        lyrics.append(u'# Bridge')
                    # otherwise unknown misc keyword
                elif line.startswith(u'Misc'):
                    metMisc = True
                elif line.startswith(u'Verse') or line.startswith(u'Chorus'):
                    lyrics.append(u'# %s' % line)
                else:
                    # should we remove multiple blank lines?
                    if lineCount == 1:
                        sName = line
                    else:
                        lyrics.append(line)
        # split on known separators
        lst = sAuthor.split(u'/')
        if len(lst) < 2:
            lst = sAuthor.split(u'|')
        author_list = u', '.join(lst)
        self.set_title(sName)
        self.set_author_list(author_list)
        self.copyright = sCopyright
        self.ccli_number = sCcli
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
        except IOError:
            log.exception(u'Failed to load CCLI text file')
        finally:
            if ccli_file:
                ccli_file.close()

    def _assure_string(self, string_in):
        """Force a string is returned"""
        if string_in is None:
            string_out = ""
        else:
            string_out = unicode(string_in)
        return string_out

    def _split_to_list(self, aString):
        """Split a string into a list - comma separated"""
        if aString:
            list = aString.split(u',')
            res = [item.strip() for item in list]
            return res

    def _list_to_string(self, strOrList):
        """Force a possibly list into a string"""
        if isinstance(strOrList, basestring):
            lst = self._split_to_list(strOrList)
        elif isinstance(strOrList, ListType):
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

    def get_ccli_number(self):
        """Return the songCclino"""
        return self._assure_string(self.ccli_number)

    def get_theme_name(self):
        """Return the theme name for the song"""
        return self._assure_string(self.theme_name)

    def get_song_book(self):
        """Return the song_book (string)"""
        return self._assure_string(self.song_book)

    def get_song_number(self):
        """Return the song_number (string)"""
        return self._assure_string(self.song_number)

    def get_comments(self):
        """Return the comments (string)"""
        return self._assure_string(self.comments)

    def get_verse_order(self):
        """Get the verseOrder (string) - preferably space delimited"""
        return self._assure_string(self.verse_order)

    def get_author_list(self, asOneString = True):
        """Return the list of authors as a string

        asOneString
        True -- string:
          'John Newton, A Parker'
        False -- list of strings
          ['John Newton', u'A Parker']
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
          'Hymn, Gospel'
        False -- list of strings
          ['Hymn', u'Gospel']
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
        for lyric in self.lyrics:
            if lyric:
                metContent = True
                tmpSlide.append(lyric)
            else:
                if metContent:
                    metContent = False
                    self.slideList.append(tmpSlide)
                    tmpSlide = []
        if tmpSlide:
            self.slideList.append(tmpSlide)

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
        [theme_name (string),
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
            title = self.title
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
        if self.show_ccli_number:
            ccli = self.get_ccli_number()
        else:
            ccli = ""
        theme_name = self.get_theme_name()
        # examine the slide for a theme
        res.append(theme_name)
        res.append(title)
        res.append(author)
        res.append(cpright)
        res.append(ccli)
        # append the correct slide
        return res

__all__ = ['SongException', 'SongTitleError', 'SongSlideError', 'SongTypeError',
           'SongFeatureError', 'Song']