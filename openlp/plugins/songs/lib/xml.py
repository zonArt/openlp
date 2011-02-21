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

The basic XML for storing the lyrics in the song database looks like this::

    <?xml version="1.0" encoding="UTF-8"?>
    <song version="1.0">
        <lyrics>
            <verse type="Chorus" label="1" lang="en">
                <![CDATA[ ... ]]>
            </verse>
        </lyrics>
    </song>


The XML of an `OpenLyrics <http://openlyrics.info/>`_  song looks like this::

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

import datetime
import logging
import re

from lxml import etree, objectify

from openlp.plugins.songs.lib import VerseType
from openlp.plugins.songs.lib.db import Author, Book, Song, Topic
from openlp.plugins.songs.lib.ui import SongStrings

log = logging.getLogger(__name__)

class SongXML(object):
    """
    This class builds and parses the XML used to describe songs.
    """
    log.info(u'SongXML Loaded')

    def __init__(self):
        """
        Set up the default variables.
        """
        self.song_xml = objectify.fromstring(u'<song version="1.0" />')
        self.lyrics = etree.SubElement(self.song_xml, u'lyrics')

    def add_verse_to_lyrics(self, type, number, content, lang=None):
        """
        Add a verse to the ``<lyrics>`` tag.

        ``type``
            A string denoting the type of verse. Possible values are *Verse*,
            *Chorus*, *Bridge*, *Pre-Chorus*, *Intro*, *Ending* and *Other*.
            Any other type is **not** allowed, this also includes translated
            types.

        ``number``
            An integer denoting the number of the item, for example: verse 1.

        ``content``
            The actual text of the verse to be stored.

        ``lang``
            The verse's language code (ISO-639). This is not required, but
            should be added if available.
        """
        verse = etree.Element(u'verse', type=unicode(type),
            label=unicode(number))
        if lang:
            verse.set(u'lang', lang)
        verse.text = etree.CDATA(content)
        self.lyrics.append(verse)

    def extract_xml(self):
        """
        Extract our newly created XML song.
        """
        return etree.tostring(self.song_xml, encoding=u'UTF-8',
            xml_declaration=True)

    def get_verses(self, xml):
        """
        Iterates through the verses in the XML and returns a list of verses
        and their attributes.

        ``xml``
            The XML of the song to be parsed.

        The returned list has the following format::

            [[{'lang': 'en', 'type': 'Verse', 'label': '1'}, u"English verse"],
            [{'lang': 'en', 'type': 'Chorus', 'label': '1'}, u"English chorus"]]
        """
        self.song_xml = None
        if xml[:5] == u'<?xml':
            xml = xml[38:]
        try:
            self.song_xml = objectify.fromstring(xml)
        except etree.XMLSyntaxError:
            log.exception(u'Invalid xml %s', xml)
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


class OpenLyrics(object):
    """
    This class represents the converter for OpenLyrics XML (version 0.7)
    to/from a song.

    As OpenLyrics has a rich set of different features, we cannot support them
    all. The following features are supported by the :class:`OpenLyrics` class:

    ``<authors>``
        OpenLP does not support the attribute *type* and *lang*.

    ``<chord>``
        This property is not supported.

    ``<comments>``
        The ``<comments>`` property is fully supported. But comments in lyrics
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
        The attribute *part* is not supported.

    ``<publisher>``
        This property is not supported.

    ``<songbooks>``
        As OpenLP does only support one songbook, we cannot consider more than
        one songbook.

    ``<tempo>``
        This property is not supported.

    ``<themes>``
        Topics, as they are called in OpenLP, are fully supported, whereby only
        the topic text (e. g. Grace) is considered, but neither the *id* nor
        *lang*.

    ``<transposition>``
        This property is not supported.

    ``<variant>``
        This property is not supported.

    ``<verse name="v1a" lang="he" translit="en">``
        The attribute *translit* is not supported. Note, the attribute *lang* is
        considered, but there is not further functionality implemented yet.

    ``<verseOrder>``
        OpenLP supports this property.

    """
    IMPLEMENTED_VERSION = u'0.7'
    def __init__(self, manager):
        self.manager = manager

    def song_to_xml(self, song):
        """
        Convert the song to OpenLyrics Format.
        """
        sxml = SongXML()
        verse_list = sxml.get_verses(song.lyrics)
        song_xml = objectify.fromstring(u'<song/>')
        # Append the necessary meta data to the song.
        song_xml.set(u'xmlns', u'http://openlyrics.info/namespace/2009/song')
        song_xml.set(u'version', OpenLyrics.IMPLEMENTED_VERSION)
        song_xml.set(u'createdIn', u'OpenLP 1.9.4')  # Use variable
        song_xml.set(u'modifiedIn', u'OpenLP 1.9.4')  # Use variable
        song_xml.set(u'modifiedDate',
            datetime.datetime.now().strftime(u'%Y-%m-%dT%H:%M:%S'))
        properties = etree.SubElement(song_xml, u'properties')
        titles = etree.SubElement(properties, u'titles')
        self._add_text_to_element(u'title', titles, song.title.strip())
        if song.alternate_title:
            self._add_text_to_element(
                u'title', titles, song.alternate_title.strip())
        if song.comments:
            comments = etree.SubElement(properties, u'comments')
            self._add_text_to_element(u'comment', comments, song.comments)
        if song.copyright:
            self._add_text_to_element(u'copyright', properties, song.copyright)
        if song.verse_order:
            self._add_text_to_element(
                u'verseOrder', properties, song.verse_order.lower())
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
            if song.song_number:
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
            if verse[0].has_key(u'lang'):
                element.set(u'lang', verse[0][u'lang'])
            element = self._add_text_to_element(u'lines', element)
            for line in unicode(verse[1]).split(u'\n'):
                self._add_text_to_element(u'line', element, line)
        return self._extract_xml(song_xml)

    def xml_to_song(self, xml):
        """
        Create and save a song from OpenLyrics format xml to the database. Since
        we also export XML from external sources (e. g. OpenLyrics import), we
        cannot ensure, that it completely conforms to the OpenLyrics standard.

        ``xml``
            The XML to parse (unicode).
        """
        # No xml get out of here.
        if not xml:
            return None
        if xml[:5] == u'<?xml':
            xml = xml[38:]
        # Remove chords from xml.
        xml = re.compile(u'<chord name=".*?"/>').sub(u'', xml)
        song_xml = objectify.fromstring(xml)
        if hasattr(song_xml, u'properties'):
            properties = song_xml.properties
        else:
            return None
        song = Song()
        self._process_copyright(properties, song)
        self._process_cclinumber(properties, song)
        self._process_titles(properties, song)
        # The verse order is processed with the lyrics!
        self._process_lyrics(properties, song_xml.lyrics, song)
        self._process_comments(properties, song)
        self._process_authors(properties, song)
        self._process_songbooks(properties, song)
        self._process_topics(properties, song)
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

    def _extract_xml(self, xml):
        """
        Extract our newly created XML song.
        """
        return etree.tostring(xml, encoding=u'UTF-8',
            xml_declaration=True)

    def _get(self, element, attribute):
        """
        This returns the element's attribute as unicode string.

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
        This returns the text of an element as unicode string.

        ``element``
            The element.
        """
        if element.text is not None:
            return unicode(element.text)
        return u''

    def _process_authors(self, properties, song):
        """
        Adds the authors specified in the XML to the song.

        ``properties``
            The property object (lxml.objectify.ObjectifiedElement).

        ``song``
            The song object.
        """
        authors = []
        if hasattr(properties, u'authors'):
            for author in properties.authors.author:
                display_name = self._text(author)
                if display_name:
                    authors.append(display_name)
        if not authors:
            authors.append(SongStrings.AuthorUnknownUnT)
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

    def _process_cclinumber(self, properties, song):
        """
        Adds the CCLI number to the song.

        ``properties``
            The property object (lxml.objectify.ObjectifiedElement).

        ``song``
            The song object.
        """
        if hasattr(properties, u'ccliNo'):
            song.ccli_number = self._text(properties.ccliNo)

    def _process_comments(self, properties, song):
        """
        Joins the comments specified in the XML and add it to the song.

        ``properties``
            The property object (lxml.objectify.ObjectifiedElement).

        ``song``
            The song object.
        """
        if hasattr(properties, u'comments'):
            comments_list = []  
            for comment in properties.comments.comment:
                commenttext = self._text(comment)
                if commenttext:
                    comments_list.append(commenttext)
            song.comments = u'\n'.join(comments_list)

    def _process_copyright(self, properties, song):
        """
        Adds the copyright to the song.

        ``properties``
            The property object (lxml.objectify.ObjectifiedElement).

        ``song``
            The song object.
        """
        if hasattr(properties, u'copyright'):
            song.copyright = self._text(properties.copyright)

    def _process_lyrics(self, properties, lyrics, song):
        """
        Processes the verses and search_lyrics for the song.

        ``properties``
            The properties object (lxml.objectify.ObjectifiedElement).

        ``lyrics``
            The lyrics object (lxml.objectify.ObjectifiedElement).

        ``song``
            The song object.
        """
        sxml = SongXML()
        search_text = u''
        temp_verse_order = []
        for verse in lyrics.verse:
            text = u''
            for lines in verse.lines:
                if text:
                    text += u'\n'
                text += u'\n'.join([unicode(line) for line in lines.line])
            verse_name = self._get(verse, u'name')
            verse_type_index = VerseType.from_tag(verse_name[0])
            verse_type = VerseType.Names[verse_type_index]
            verse_number = re.compile(u'[a-zA-Z]*').sub(u'', verse_name)
            verse_part = re.compile(u'[0-9]*').sub(u'', verse_name[1:])
            # OpenLyrics allows e. g. "c", but we need "c1".
            if not verse_number:
                verse_number = u'1'
            temp_verse_order.append((verse_type, verse_number, verse_part))
            lang = None
            if self._get(verse, u'lang'):
                lang = self._get(verse, u'lang')
            sxml.add_verse_to_lyrics(verse_type, verse_number, text, lang)
            search_text = search_text + text
        song.search_lyrics = search_text.lower()
        song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
        # Process verse order
        if hasattr(properties, u'verseOrder'):
            song.verse_order = self._text(properties.verseOrder)
        else:
            # We have to process the temp_verse_order, as the verseOrder
            # property is not present.
            previous_type = u''
            previous_number = u''
            previous_part = u''
            verse_order = []
            # Currently we do not support different "parts"!
            for name in temp_verse_order:
                if name[0] == previous_type:
                    if name[1] != previous_number:
                        verse_order.append(u''.join((name[0][0], name[1])))
                else:
                    verse_order.append(u''.join((name[0][0], name[1])))
                previous_type = name[0]
                previous_number = name[1]
                previous_part = name[2]
            song.verse_order = u' '.join(verse_order)

    def _process_songbooks(self, properties, song):
        """
        Adds the song book and song number specified in the XML to the song.

        ``properties``
            The property object (lxml.objectify.ObjectifiedElement).

        ``song``
            The song object.
        """
        song.song_book_id = 0
        song.song_number = u''
        if hasattr(properties, u'songbooks'):
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
                    if hasattr(songbook, u'entry'):
                        song.song_number = self._get(songbook, u'entry')
                    # We only support one song book, so take the first one.
                    break

    def _process_titles(self, properties, song):
        """
        Processes the titles specified in the song's XML.

        ``properties``
            The property object (lxml.objectify.ObjectifiedElement).

        ``song``
            The song object.
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
        Adds the topics to the song.

        ``properties``
            The property object (lxml.objectify.ObjectifiedElement).

        ``song``
            The song object.
        """
        if hasattr(properties, u'themes'):
            for topictext in properties.themes.theme:
                topictext = self._text(topictext)
                if topictext:
                    topic = self.manager.get_object_filtered(Topic,
                        Topic.name == topictext)
                    if topic is None:
                        # We need to create a topic, because it does not exist.
                        topic = Topic.populate(name=topictext)
                        self.manager.save_object(topic)
                    song.topics.append(topic)

    def _dump_xml(self, xml):
        """
        Debugging aid to dump XML so that we can see what we have.
        """
        return etree.tostring(xml, encoding=u'UTF-8',
            xml_declaration=True, pretty_print=True)
