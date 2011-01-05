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
The :mod:`xml` module provides the XML functionality.

The basic XML for storing the lyrics in the song database is of the format::

    <?xml version="1.0" encoding="UTF-8"?>
    <song version="1.0">
        <lyrics language="en">
            <verse type="chorus" label="1">
                <![CDATA[ ... ]]>
            </verse>
        </lyrics>
    </song>


The XML of `OpenLyrics <http://openlyrics.info/>`_  songs is of the format::

    <song xmlns="http://openlyrics.info/namespace/2009/song"
        version="0.7"
        createdIn="OpenLP 1.9.0"
        modifiedIn="ChangingSong 0.0.1"
        modifiedDate="2010-01-28T13:15:30+01:00">
    <properties>
        <titles>
            <title>Amazing Grace</title>
        </titles>
    </properties>
        <lyrics>
            <verse name="v1">
                <lines>
                    <line>Amazing grace how sweet the sound</line>
                </lines>
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


#class LyricsXML(object):
#    """
#    This class represents the XML in the ``lyrics`` field of a song.
#    """
#    def __init__(self, song=None):
#        if song:
#            if song.lyrics.startswith(u'<?xml'):
#                self.parse(song.lyrics)
#            else:
#                self.extract(song.lyrics)
#        else:
#            self.languages = []
#
#    def parse(self, xml):
#        """
#        Parse XML from the ``lyrics`` field in the database, and set the list
#        of verses from it.
#
#        ``xml``
#            The XML to parse.
#        """
#        try:
#            self.languages = []
#            song = objectify.fromstring(xml)
#            for lyrics in song.lyrics:
#                language = {
#                    u'language': lyrics.attrib[u'language'],
#                    u'verses': []
#                }
#                for verse in lyrics.verse:
#                    language[u'verses'].append({
#                        u'type': verse.attrib[u'type'],
#                        u'label': verse.attrib[u'label'],
#                        u'text': unicode(verse.text)
#                    })
#                self.lyrics.append(language)
#            return True
#        except etree.XMLSyntaxError:
#            return False
#
#    def extract(self, text):
#        """
#        If the ``lyrics`` field in the database is not XML, this method is
#        called and used to construct the verse structure similar to the output
#        of the ``parse`` function.
#
#        ``text``
#            The text to pull verses out of.
#        """
#        text = text.replace('\r\n', '\n')
#        verses = text.split('\n\n')
#        self.languages = [{u'language': u'en', u'verses': []}]
#        for counter, verse in enumerate(verses):
#            self.languages[0][u'verses'].append({
#                u'type': u'verse',
#                u'label': unicode(counter),
#                u'text': verse
#            })
#        return True
#
#    def add_verse(self, type, label, text):
#        """
#        Add a verse to the list of verses.
#
#        ``type``
#            The type of list, one of "verse", "chorus", "bridge", "pre-chorus",
#            "intro", "outtro".
#
#        ``label``
#            The number associated with this verse, like 1 or 2.
#
#        ``text``
#            The text of the verse.
#        """
#        self.verses.append({
#            u'type': type,
#            u'label': label,
#            u'text': text
#        })
#
#    def export(self):
#        """
#        Build up the XML for the verse structure.
#        """
#        lyrics_output = u''
#        for language in self.languages:
#            verse_output = u''
#            for verse in language[u'verses']:
#                verse_output = verse_output + \
#                    u'<verse type="%s" label="%s"><![CDATA[%s]]></verse>' % \
#                    (verse[u'type'], verse[u'label'], verse[u'text'])
#            lyrics_output = lyrics_output + \
#                u'<lyrics language="%s">%s</lyrics>' % \
#                (language[u'language'], verse_output)
#        song_output = u'<?xml version="1.0" encoding="UTF-8"?>' + \
#            u'<song version="1.0">%s</song>' % lyrics_output
#        return song_output


class OpenLyricsBuilder(object):
    """
    This class represents the converter for song to OpenLyrics XML.
    """
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
            element = self._add_text_to_element(u'lines', element)
            for line in unicode(verse[1]).split(u'\n'):
                self._add_text_to_element(u'line', element, line)
        return self._extract_xml(song_xml)

    def _add_text_to_element(self, tag, parent, text=None, label=None):
        if label:
            element = etree.Element(tag, name=unicode(label))
        else:
            element = etree.Element(tag)
        if text:
            element.text = unicode(text)
        parent.append(element)
        return element

    def _extract_xml(self, xml):
        """
        Extract our newly created XML song.
        """
        return etree.tostring(xml, encoding=u'UTF-8',
            xml_declaration=True)

    def _dump_xml(self, xml):
        """
        Debugging aid to dump XML so that we can see what we have.
        """
        return etree.tostring(xml, encoding=u'UTF-8',
            xml_declaration=True, pretty_print=True)


class OpenLyricsParser(object):
    """
    This class represents the converter for OpenLyrics XML to a song.

    As OpenLyrics has a rich set of different features, we cannot support them
    all. The following features are supported by the :class:`OpenLyricsParser`::

    ``<authors>``
        OpenLP does not support the author ``type`` and consequently not 
        ``lang`` for the author of the type ``translation``.

    ``<chord>``
        This property is not supported. 

    ``<comments>``
        The ``<comments>`` property  is fully supported. But comments in lyrics
        are not supported.

    ``<copyright>``
        This property is fully supported.

    ``<customVersion>``
        This property is not supported.

    ``<key>``
        This property is not supported. 

    ``<keywords>``
        This property is not supported. 

    ``<lines>``
        The attribute ``part`` is not supported.

    ``<publisher>``
        This property is not supported. 

    ``<songbooks>``
        As OpenLP does only support one songbook, we cannot consider more than
        one songbook.

    ``<tempo>``
        This property is not supported. 

    ``<themes>``
        Topics, as they are called in OpenLP, are fully supported, whereby only
        the topic text (e. g. Grace) is considered, but neither the ``id`` nor
        ``lang``.

    ``<transposition>``
        This property is not supported.

    ``<variant>``
        This property is not supported. 

    ``<verse name="v1a"  lang="he" translit="en">``
        The attribute ``translit`` and ``lang`` are not supported.
        This class support verse names of the format ``<type>`` and
        ``<type><number>``. Whereas this class does not support verse names of
        the format ``<type><number><part>`` as OpenLP does not support splitting
        verses into different parts.

    ``<verseOrder>``
        OpenLP supports this property.
    """
    def __init__(self, manager):
        self.manager = manager

    def xml_to_song(self, xml):
        """
        Create and save a song from OpenLyrics format xml to the database. Since
        we also export XML from external sources (e. g. OpenLyrics import), we
        cannot ensure, that it completely conforms to the OpenLyrics standard.
        """
        # No xml get out of here.
        if not xml:
            return 0
        song = Song()
        if xml[:5] == u'<?xml':
            xml = xml[38:]
        # Remove chords
        xml = re.compile(u'<chord name=".*?"/>').sub(u'', xml)
        song_xml = objectify.fromstring(xml)
        properties = song_xml.properties
        # Process Copyright
        try:
            song.copyright = self._text(properties.copyright)
        except AttributeError:
            song.copyright = u''
        # Process CCLI number
        try:
            song.ccli_number = self._text(properties.ccliNo)
        except AttributeError:
            song.ccli_number = u''
        self._process_titles(properties, song)
        song.verse_order = u''
        self._process_lyrics(song_xml, song)
        # Process verse order
        song.verse_order = song.verse_order.strip()
        try:
            song.verse_order = self._text(properties.verseOrder)
        except AttributeError:
            # Do not worry, as the verse order has cautionary already been
            # saved while creating the verses.
            pass
        self._process_comments(properties, song)
        self._process_authors(properties, song)
        self._process_songbooks(properties, song)
        self._process_topics(properties, song)
        self.manager.save_object(song)
        return song.id

    def _get(self, element, attribute):
        """
        This takes care of empty attributes. It returns the element's attribute.

        ``element``
            The element.

        ``attribute``
            The element's attribute (unicode).
        """
        if element.get(attribute) is not None:
            return unicode(element.get(attribute))
        return u''

    def _text(self, element):
        """
        This takes care of empty texts. It returns the element's text. 

        ``element``
            The element.
        """
        if element.text is not None:
            return unicode(element.text)
        return u''

    def _process_authors(self, properties, song):
        """
        Finds an existing Author or creates a new Author and adds it to the song
        object.
        """
        authors = []
        try:
            for author in properties.authors.author:
                display_name = self._text(author)
                if display_name:
                    authors.append(display_name)
        except AttributeError:
            pass
        if not authors:
            # Add "Author unknown" (can be translated).
            authors.append((unicode(translate('SongsPlugin.XML',
                'Author unknown'))))
        for display_name in authors:
            author = self.manager.get_object_filtered(Author,
                Author.display_name == display_name)
            if author is None:
                # We need to create a new author, as the author does not exist.
                author = Author.populate(display_name=display_name,
                    last_name=display_name.split(u' ')[-1],
                    first_name=u' '.join(display_name.split(u' ')[:-1]))
            self.manager.save_object(author)
            song.authors.append(author)

    def _process_comments(self, properties, song):
        """
        """
        try:
            song.comments = u'\n'.join(
                [self._text(comment) for comment in properties.comments.comment]
                )
        except AttributeError:
            song.comments = u''

    def _process_lyrics(self, song_xml, song):
        """
        """
        sxml = SongXMLBuilder()
        search_text = u''
        for verse in song_xml.lyrics.verse:
            text = u''
            for lines in verse.lines:
                if text:
                    text += u'\n'
                text += u'\n'.join([unicode(line) for line in lines.line])
            # OpenLyrics allows e. g. "c", but we need "c1".
            if self._get(verse, u'name').isalpha():
                verse.set(u'name', self._get(verse, u'name') + u'1')
            type = VerseType.expand_string(self._get(verse, u'name')[0])
            sxml.add_verse_to_lyrics(type, self._get(verse, u'name')[1], text)
            song.verse_order += u'%s%s ' % (type[0],
                self._get(verse, u'name')[1])
            search_text = search_text + text
        song.search_lyrics = search_text.lower()
        song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
        #TODO: make sure "c" becomes "c1"

    def _process_songbooks(self, properties, song):
        """
        Finds an existing book or creates a new book and adds it to the song
        object.
        """
        song.song_book_id = 0
        song.song_number = u''
        try:
            for songbook in properties.songbooks.songbook:
                bookname = self._get(songbook, u'name')
                if bookname:
                    book = self.manager.get_object_filtered(Book,
                        Book.name == bookname)
                    if book is None:
                        # We need to create a book, because it does not exist.
                        book = Book.populate(name=bookname, publisher=u'')
                        self.manager.save_object(book)
                    song.song_book_id = book.id
                    if self._get(songbook, u'entry'):
                        song.song_number = self._get(songbook, u'entry')
                    # We does only support one song book, so take the first one.
                    break
        except AttributeError:
            pass

    def _process_titles(self, properties, song):
        """
        """
        for title in properties.titles.title:
            if not song.title:
                song.title = self._text(title)
                song.search_title = unicode(song.title)
                song.alternate_title = u''
            else:
                song.alternate_title = self._text(title)
                song.search_title += u'@' + song.alternate_title
        song.search_title = re.sub(r'[\'"`,;:(){}?]+', u'',
            unicode(song.search_title)).lower()

    def _process_topics(self, properties, song):
        """
        Finds an existing topic or creates a new topic and adds it to the song
        object.
        """
        try:
            for topictext in properties.themes.theme:
                topictext = self._text(topictext)
                if not topictext:
                    # Wrong use of XML here, as no text has been supplied.
                    return
                topic = self.manager.get_object_filtered(Topic,
                    Topic.name == topictext)
                if topic is None:
                    # We need to create a new topic, as the topic does not exist.
                    topic = Topic.populate(name=topictext)
                    self.manager.save_object(topic)
                song.topics.append(topic)
        except AttributeError:
            pass
