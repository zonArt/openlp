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
"""
The :mod:`xml` module provides the XML functionality for songs

The basic XML is of the format::

    <?xml version="1.0" encoding="UTF-8"?>
    <song version="1.0">
        <lyrics language="en">
            <verse type="chorus" label="1">
                <![CDATA[ ... ]]>
            </verse>
        </lyrics>
    </song>
"""

import logging
import re

from lxml import etree, objectify
from openlp.plugins.songs.lib.db import Author, Song

log = logging.getLogger(__name__)

class SongXMLBuilder(object):
    """
    This class builds the XML used to describe songs.
    """
    log.info(u'SongXMLBuilder Loaded')

    def __init__(self, song_language=None):
        """
        Set up the song builder.

        ``song_language``
            The language used in this song
        """
        lang = u'en'
        if song_language:
            lang = song_language
        self.song_xml = objectify.fromstring(u'<song version="1.0" />')
        self.lyrics = etree.SubElement(self.song_xml, u'lyrics', language=lang)

    def add_verse_to_lyrics(self, type, number, content):
        """
        Add a verse to the ``<lyrics>`` tag.

        ``type``
            A string denoting the type of verse. Possible values are "Chorus",
            "Verse", "Bridge", and "Custom".

        ``number``
            An integer denoting the number of the item, for example: verse 1.

        ``content``
            The actual text of the verse to be stored.
        """
        # log.debug(u'add_verse_to_lyrics %s, %s\n%s' % (type, number, content))
        verse = etree.Element(u'verse', type = unicode(type),
            label = unicode(number))
        verse.text = etree.CDATA(content)
        self.lyrics.append(verse)

    def dump_xml(self):
        """
        Debugging aid to dump XML so that we can see what we have.
        """
        return etree.tostring(self.song_xml, encoding=u'UTF-8',
            xml_declaration=True, pretty_print=True)

    def extract_xml(self):
        """
        Extract our newly created XML song.
        """
        return etree.tostring(self.song_xml, encoding=u'UTF-8',
            xml_declaration=True)


class SongXMLParser(object):
    """
    A class to read in and parse a song's XML.
    """
    log.info(u'SongXMLParser Loaded')

    def __init__(self, xml):
        """
        Set up our song XML parser.

        ``xml``
            The XML of the song to be parsed.
        """
        self.song_xml = None
        if xml[:5] == u'<?xml':
            xml = xml[38:]
        try:
            self.song_xml = objectify.fromstring(xml)
        except etree.XMLSyntaxError:
            log.exception(u'Invalid xml %s', xml)

    def get_verses(self):
        """
        Iterates through the verses in the XML and returns a list of verses
        and their attributes.
        """
        xml_iter = self.song_xml.getiterator()
        verse_list = []
        for element in xml_iter:
            if element.tag == u'verse':
                if element.text is None:
                    element.text = u''
                verse_list.append([element.attrib, unicode(element.text)])
        return verse_list

    def dump_xml(self):
        """
        Debugging aid to dump XML so that we can see what we have.
        """
        return etree.dump(self.song_xml)


class LyricsXML(object):
    """
    This class represents the XML in the ``lyrics`` field of a song.
    """
    def __init__(self, song=None):
        if song:
            if song.lyrics.startswith(u'<?xml'):
                self.parse(song.lyrics)
            else:
                self.extract(song.lyrics)
        else:
            self.languages = []

    def parse(self, xml):
        """
        Parse XML from the ``lyrics`` field in the database, and set the list
        of verses from it.

        ``xml``
            The XML to parse.
        """
        try:
            self.languages = []
            song = objectify.fromstring(xml)
            for lyrics in song.lyrics:
                language = {
                    u'language': lyrics.attrib[u'language'],
                    u'verses': []
                }
                for verse in lyrics.verse:
                    language[u'verses'].append({
                        u'type': verse.attrib[u'type'],
                        u'label': verse.attrib[u'label'],
                        u'text': unicode(verse.text)
                    })
                self.lyrics.append(language)
            return True
        except etree.XMLSyntaxError:
            return False

    def extract(self, text):
        """
        If the ``lyrics`` field in the database is not XML, this method is
        called and used to construct the verse structure similar to the output
        of the ``parse`` function.

        ``text``
            The text to pull verses out of.
        """
        text = text.replace('\r\n', '\n')
        verses = text.split('\n\n')
        self.languages = [{u'language': u'en', u'verses': []}]
        counter = 0
        for verse in verses:
            counter = counter + 1
            self.languages[0][u'verses'].append({
                u'type': u'verse',
                u'label': unicode(counter),
                u'text': verse
            })
        return True

    def add_verse(self, type, label, text):
        """
        Add a verse to the list of verses.

        ``type``
            The type of list, one of "verse", "chorus", "bridge", "pre-chorus",
            "intro", "outtro".

        ``label``
            The number associated with this verse, like 1 or 2.

        ``text``
            The text of the verse.
        """
        self.verses.append({
            u'type': type,
            u'label': label,
            u'text': text
        })

    def export(self):
        """
        Build up the XML for the verse structure.
        """
        lyrics_output = u''
        for language in self.languages:
            verse_output = u''
            for verse in language[u'verses']:
                verse_output = verse_output + \
                    u'<verse type="%s" label="%s"><![CDATA[%s]]></verse>' % \
                    (verse[u'type'], verse[u'label'], verse[u'text'])
            lyrics_output = lyrics_output + \
                u'<lyrics language="%s">%s</lyrics>' % \
                (language[u'language'], verse_output)
        song_output = u'<?xml version="1.0" encoding="UTF-8"?>' + \
            u'<song version="1.0">%s</song>' % lyrics_output
        return song_output


class OpenLyricsParser(object):
    """
    This class represents the converter for Song to/from OpenLyrics XML.
    """
    def __init__(self, manager):
        self.manager = manager

    def song_to_xml(self, song):
        """
        Convert the song to OpenLyrics Format
        """
        songXML = SongXMLParser(song.lyrics)
        verseList = songXML.get_verses()
        song_xml = objectify.fromstring(
            u'<song version="0.7" createdIn="OpenLP 2.0"/>')
        properties = etree.SubElement(song_xml, u'properties')
        titles = etree.SubElement(properties, u'titles')
        self._add_text_to_element(u'title', titles, song.title)
        if song.alternate_title:
            self._add_text_to_element(u'title', titles, song.alternate_title)
        if song.theme_name:
            themes = etree.SubElement(properties, u'themes')
            self._add_text_to_element(u'theme', themes, song.theme_name)
        self._add_text_to_element(u'copyright', properties, song.copyright)
        self._add_text_to_element(u'verseOrder', properties, song.verse_order)
        if song.ccli_number:
            self._add_text_to_element(u'ccliNo', properties, song.ccli_number)
        authors = etree.SubElement(properties, u'authors')
        for author in song.authors:
            self._add_text_to_element(u'author', authors, author.display_name)
        lyrics = etree.SubElement(song_xml, u'lyrics')
        for verse in verseList:
            verseTag = u'%s%s' % (
                verse[0][u'type'][0].lower(), verse[0][u'label'])
            element = self._add_text_to_element(u'verse', lyrics, None, verseTag)
            element = self._add_text_to_element(u'lines', element)
            for line in unicode(verse[1]).split(u'\n'):
                self._add_text_to_element(u'line', element, line)
        print self._dump_xml(song_xml)
        self.xml_to_song(self._extract_xml(song_xml))
        return u'' #self.xml_to_song(self._extract_xml(song_xml))

    def xml_to_song(self, xml):
        """
        Create a Song from OpenLyrics format xml
        """
        song = Song()
        if xml[:5] == u'<?xml':
            xml = xml[38:]
        song_xml = objectify.fromstring(xml)
        print objectify.dump(song_xml)
        for properties in song_xml.properties:
            song.copyright = unicode(properties.copyright.text)
            song.verse_order = unicode(properties.verseOrder.text)
            try:
                song.ccli_number = unicode(properties.ccliNo.text)
            except:
                pass
            try:
                song.theme_name = unicode(properties.themes.theme)
            except:
                pass
            # Process Titles
            for title in properties.titles.title:
                if not song.title:
                    song.title = "aa" + title.text
                    song.search_title = unicode(song.title)
                else:
                    song.alternate_title = unicode(title.text)
                    song.search_title += u'@' + song.alternate_title
            song.search_title = re.sub(r'[\'"`,;:(){}?]+', u'',
                unicode(song.search_title)).lower()
            # Process Authors
            for author in properties.authors.author:
                self._process_author(author.text, song)
        # Process Lyrics
        sxml = SongXMLBuilder()
        search_text = u''
        for lyrics in song_xml.lyrics:
            for verse in song_xml.lyrics.verse:
                print "verse", verse.attrib
                text = u''
                for line in verse.lines.line:
                    line = unicode(line)
                    if not text:
                        text = line
                    else:
                        text += u'\n' + line
                sxml.add_verse_to_lyrics(u'V', verse.attrib[u'name'], text)
                search_text = search_text + text
        song.search_lyrics = search_text.lower()
        song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
        song.comments = u''
        song.song_number = u''
        self.manager.save_object(song)
        return 0

    def _add_text_to_element(self, tag, parent, text=None, label=None):
        if label:
            element = etree.Element(tag, name = unicode(label))
        else:
            element = etree.Element(tag)
        if text:
            element.text = unicode(text)
        parent.append(element)
        return element

    def _dump_xml(self, xml):
        """
        Debugging aid to dump XML so that we can see what we have.
        """
        return etree.tostring(xml, encoding=u'UTF-8',
            xml_declaration=True, pretty_print=True)

    def _extract_xml(self, xml):
        """
        Extract our newly created XML song.
        """
        return etree.tostring(xml, encoding=u'UTF-8',
            xml_declaration=True)

    def _process_author(self, name, song):
        """
        Find or create an Author from display_name.
        """
        print "name = ", name
        name = unicode(name)
        search_results = self.manager.get_all_objects(Author,
            Author.display_name == name)
        if search_results:
            # should only be one! so take the first
            song.authors.append(search_results[0])
        else:
            # Need a new author
            new_author = Author.populate(first_name=name.rsplit(u' ', 1)[0],
                        last_name=name.rsplit(u' ', 1)[1], display_name=name)
            self.manager.save_object(new_author)
            song.authors.append(new_author)
