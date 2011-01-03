# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
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

from openlp.core.lib import translate
from openlp.plugins.songs.lib import VerseType
from openlp.plugins.songs.lib.db import Author, Book, Song, Topic

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
        verse = etree.Element(u'verse', type=unicode(type),
            label=unicode(number))
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
        for counter, verse in enumerate(verses):
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
    This class represents the converter for Song to/from
    `OpenLyrics <http://openlyrics.info/>`_ XML.
    """
    # TODO: complete OpenLyrics standard implementation as fare as possible!
    def __init__(self, manager):
        self.manager = manager

    def song_to_xml(self, song):
        """
        Convert the song to OpenLyrics Format.
        """
        song_xml_parser = SongXMLParser(song.lyrics)
        verse_list = song_xml_parser.get_verses()
        song_xml = objectify.fromstring(
            u'<song version="0.7" createdIn="OpenLP 2.0"/>')
        properties = etree.SubElement(song_xml, u'properties')
        titles = etree.SubElement(properties, u'titles')
        self._add_text_to_element(u'title', titles, song.title)
        if song.alternate_title:
            self._add_text_to_element(u'title', titles, song.alternate_title)
        if song.comments:
            comments = etree.SubElement(properties, u'comments')
            self._add_text_to_element(u'comment', comments, song.comments)
        if song.copyright:
            self._add_text_to_element(u'copyright', properties, song.copyright)
        if song.verse_order:
            self._add_text_to_element(
                u'verseOrder', properties, song.verse_order)
        if song.ccli_number:
            self._add_text_to_element(u'ccliNo', properties, song.ccli_number)
        if song.authors:
            authors = etree.SubElement(properties, u'authors')
            for author in song.authors:
                self._add_text_to_element(
                    u'author', authors, author.display_name)
        book = self.manager.get_object_filtered(
            Book, Book.id == song.song_book_id)
        if book is not None:
            book = book.name
            songbooks = etree.SubElement(properties, u'songbooks')
            element = self._add_text_to_element(
                u'songbook', songbooks, None, book)
            element.set(u'entry', song.song_number)
        if song.topics:
            themes = etree.SubElement(properties, u'themes')
            for topic in song.topics:
                self._add_text_to_element(u'theme', themes, topic.name)
        lyrics = etree.SubElement(song_xml, u'lyrics')
        for verse in verse_list:
            verse_tag = u'%s%s' % (
                verse[0][u'type'][0].lower(), verse[0][u'label'])
            element = \
                self._add_text_to_element(u'verse', lyrics, None, verse_tag)
            # Note that the <verses> element will not be in OpenLyrics 0.8:
            # http://code.google.com/p/openlyrics/issues/detail?id=8
            element = self._add_text_to_element(u'lines', element)
            for line in unicode(verse[1]).split(u'\n'):
                self._add_text_to_element(u'line', element, line)
        return self._extract_xml(song_xml)

    def xml_to_song(self, xml):
        """
        Create and save a Song from OpenLyrics format xml.
        """
        # No xml get out of here.
        if not xml:
            return 0
        song = Song()
        if xml[:5] == u'<?xml':
            xml = xml[38:]
        song_xml = objectify.fromstring(xml)
        properties = song_xml.properties
        # Process Copyright
        try:
            song.copyright = unicode(properties.copyright.text)
            if song.copyright == u'None':
                song.copyright = u''
        except AttributeError:
            song.copyright = u''
        # Process CCLI number
        try:
            song.ccli_number = unicode(properties.ccliNo.text)
        except AttributeError:
            song.ccli_number = u''
        # Process Titles
        for title in properties.titles.title:
            if not song.title:
                song.title = unicode(title.text)
                song.search_title = unicode(song.title)
                song.alternate_title = u''
            else:
                song.alternate_title = unicode(title.text)
                song.search_title += u'@' + song.alternate_title
        song.search_title = re.sub(r'[\'"`,;:(){}?]+', u'',
            unicode(song.search_title)).lower()
        # Process Lyrics
        sxml = SongXMLBuilder()
        search_text = u''
        song.verse_order = u''
        for lyrics in song_xml.lyrics:
            for verse in lyrics.verse:
                text = u''
                # Note that the <verses> element will not be in OpenLyrics 0.8:
                # http://code.google.com/p/openlyrics/issues/detail?id=8
                for line in verse.lines:
                    for line in line.line:
                        line = unicode(line)
                        if not text:
                            text = line
                        else:
                            text += u'\n' + line
                type_ = VerseType.expand_string(verse.attrib[u'name'][0])
                # TODO: Here we need to create the verse order for the case that
                # the song does not have a verseOrder property.
                sxml.add_verse_to_lyrics(type_, verse.attrib[u'name'][1], text)
                search_text = search_text + text
        song.search_lyrics = search_text.lower()
        song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
        # Process verse order
        try:
            song.verse_order = unicode(properties.verseOrder.text)
        except AttributeError:
            # TODO: Do not allow empty verse order.
            pass
        if song.verse_order == u'None':
            song.verse_order = u''
        # Process Comments
        song.comments = u''
        try:
            for comment in properties.comments.comment:
                if not song.comments:
                    song.comments = unicode(comment.text)
                else:
                    song.comments += u'\n' + unicode(comment.text)
        except AttributeError:
            pass
        # Process Authors
        try:
            for author in properties.authors.author:
                self._process_author(author.text, song)
        except AttributeError:
            pass
        if not song.authors:
            # Add "Author unknown" (can be translated)
            self._process_author(translate('SongsPlugin.XML',
                'Author unknown'), song)
        # Process Song Book and Song Number
        song.song_book_id = 0
        song.song_number = u''
        try:
            for songbook in properties.songbooks.songbook:
                self._process_songbook(songbook.get(u'name'), song)
                if songbook.get(u'entry'):
                    song.song_number = unicode(songbook.get(u'entry'))
                # OpenLp does only support one song book, so take the first one.
                break
        except AttributeError:
            pass
        # Process Topcis
        try:
            for topic in properties.themes.theme:
                self._process_topic(topic.text, song)
        except AttributeError:
            pass
        # Properties not yet supported.
        song.theme_name = u''
        self.manager.save_object(song)
        return song.id

    def _add_text_to_element(self, tag, parent, text=None, label=None):
        if label:
            element = etree.Element(tag, name=unicode(label))
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
        Finds an existing Author or creates a new Author and adds it to the song
        object.

        ``name``
            The display_name of the song (string).

        ``song``
            The song the object.
        """
        if not name:
            # Wrong use of XML here, as no text has been supplied.
            return
        name = unicode(name)
        author = self.manager.get_object_filtered(Author,
            Author.display_name == name)
        if author is None:
            # We need to create a new author, as the author does not exist.
            author = Author.populate(first_name=name.rsplit(u' ', 1)[0],
                last_name=name.rsplit(u' ', 1)[1], display_name=name)
            self.manager.save_object(author)
        song.authors.append(author)

    def _process_topic(self, topictext, song):
        """
        Finds an existing topic or creates a new topic and adds it to the song
        object.

        ``topictext``
            The topictext of the topic (string).

        ``song``
            The song object.
        """
        if not topictext:
            # Wrong use of XML here, as no text has been supplied.
            return
        topictext = unicode(topictext)
        topic = self.manager.get_object_filtered(Topic, Topic.name == topictext)
        if topic is None:
            # We need to create a new topic, as the topic does not exist.
            topic = Topic.populate(name=topictext)
            self.manager.save_object(topic)
        song.topics.append(topic)

    def _process_songbook(self, bookname, song):
        """
        Finds an existing book or creates a new book and adds it to the song
        object.

        ``bookname``
            The name of the book (string).

        ``song``
            The song object.
        """
        if not bookname:
            # Wrong use of XML here, as no text has been supplied.
            return
        bookname = unicode(bookname)
        book = self.manager.get_object_filtered(Book, Book.name == bookname)
        if book is None:
            # We need to create a new book, as the book does not exist.
            book = Book.populate(name=bookname, publisher=u'')
            self.manager.save_object(book)
        song.song_book_id = book.id
