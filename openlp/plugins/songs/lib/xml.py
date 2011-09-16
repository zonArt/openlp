# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
            <verse type="c" label="1" lang="en">
                <![CDATA[Chorus virtual slide 1[---]Chorus  virtual slide 2]]>
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

import logging
import re

from lxml import etree, objectify

from openlp.core.lib import FormattingTags
from openlp.plugins.songs.lib import clean_song, VerseType
from openlp.plugins.songs.lib.db import Author, Book, Song, Topic
from openlp.core.utils import get_application_version

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
            A string denoting the type of verse. Possible values are *v*,
            *c*, *b*, *p*, *i*, *e* and *o*.
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

            [[{'type': 'v', 'label': '1'},
            u"virtual slide 1[---]virtual slide 2"],
            [{'lang': 'en', 'type': 'c', 'label': '1'}, u"English chorus"]]
        """
        self.song_xml = None
        verse_list = []
        if not xml.startswith(u'<?xml') and not xml.startswith(u'<song'):
            # This is an old style song, without XML. Let's handle it correctly
            # by iterating through the verses, and then recreating the internal
            # xml object as well.
            self.song_xml = objectify.fromstring(u'<song version="1.0" />')
            self.lyrics = etree.SubElement(self.song_xml, u'lyrics')
            verses = xml.split(u'\n\n')
            for count, verse in enumerate(verses):
                verse_list.append([{u'type': u'v', u'label': unicode(count)},
                    unicode(verse)])
                self.add_verse_to_lyrics(u'v', unicode(count), verse)
            return verse_list
        elif xml.startswith(u'<?xml'):
            xml = xml[38:]
        try:
            self.song_xml = objectify.fromstring(xml)
        except etree.XMLSyntaxError:
            log.exception(u'Invalid xml %s', xml)
        xml_iter = self.song_xml.getiterator()
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
    This class represents the converter for OpenLyrics XML (version 0.8)
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

    ``<format>``
        The custom formatting tags are fully supported.

    ``<keywords>``
        This property is not supported.

    ``<lines>``
        The attribute *part* is not supported. The *break* attribute is
        supported.

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
        considered, but there is not further functionality implemented yet. The
        following verse "types" are supported by OpenLP:

            * v
            * c
            * b
            * p
            * i
            * e
            * o

        The verse "types" stand for *Verse*, *Chorus*, *Bridge*, *Pre-Chorus*,
        *Intro*, *Ending* and *Other*. Any numeric value is allowed after the
        verse type. The complete verse name in OpenLP always consists of the
        verse type and the verse number. If not number is present *1* is
        assumed.
        OpenLP will merge verses which are split up by appending a letter to the
        verse name, such as *v1a*.

    ``<verseOrder>``
        OpenLP supports this property.

    """
    IMPLEMENTED_VERSION = u'0.8'

    def __init__(self, manager):
        self.manager = manager
        self.start_tags_regex = re.compile(r'\{\w+\}')  # {abc}
        self.end_tags_regex = re.compile(r'\{\/\w+\}')  # {/abc}

    def song_to_xml(self, song):
        """
        Convert the song to OpenLyrics Format.
        """
        sxml = SongXML()
        song_xml = objectify.fromstring(u'<song/>')
        # Append the necessary meta data to the song.
        song_xml.set(u'xmlns', u'http://openlyrics.info/namespace/2009/song')
        song_xml.set(u'version', OpenLyrics.IMPLEMENTED_VERSION)
        application_name = u'OpenLP ' + get_application_version()[u'version']
        song_xml.set(u'createdIn', application_name)
        song_xml.set(u'modifiedIn', application_name)
        # "Convert" 2011-08-27 11:49:15 to 2011-08-27T11:49:15.
        song_xml.set(u'modifiedDate',
            unicode(song.last_modified).replace(u' ', u'T'))
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
        # Process the formatting tags.
        # Have we any tags in song lyrics?
        tags_element = None
        match = re.search(u'\{/?\w+\}', song.lyrics, re.UNICODE)
        if match:
            # Reset available tags.
            FormattingTags.reset_html_tags()
            # Named 'formatting' - 'format' is built-in fuction in Python.
            formatting = etree.SubElement(song_xml, u'format')
            tags_element = etree.SubElement(formatting, u'tags')
            tags_element.set(u'application', u'OpenLP')
        # Process the song's lyrics.
        lyrics = etree.SubElement(song_xml, u'lyrics')
        verse_list = sxml.get_verses(song.lyrics)
        for verse in verse_list:
            verse_tag = verse[0][u'type'][0].lower()
            verse_number = verse[0][u'label']
            verse_def = verse_tag + verse_number
            verse_element = \
                self._add_text_to_element(u'verse', lyrics, None, verse_def)
            if u'lang' in verse[0]:
                verse_element.set(u'lang', verse[0][u'lang'])
            # Create a list with all "virtual" verses.
            virtual_verses = verse[1].split(u'[---]')
            for index, virtual_verse in enumerate(virtual_verses):
                lines_element = \
                    self._add_text_to_element(u'lines', verse_element)
                # Do not add the break attribute to the last lines element.
                if index < len(virtual_verses) - 1:
                    lines_element.set(u'break', u'optional')
                for line in virtual_verse.strip(u'\n').split(u'\n'):
                    # Process only lines containing formatting tags
                    if self.start_tags_regex.search(line):
                        # add formatting tags to text
                        self._add_line_with_tags_to_lines(lines_element, line,
                            tags_element)
                    else:
                        self._add_text_to_element(u'line', lines_element, line)
        return self._extract_xml(song_xml)

    def xml_to_song(self, xml, parse_and_not_save=False):
        """
        Create and save a song from OpenLyrics format xml to the database. Since
        we also export XML from external sources (e. g. OpenLyrics import), we
        cannot ensure, that it completely conforms to the OpenLyrics standard.

        ``xml``
            The XML to parse (unicode).

        ``parse_and_not_save``
            Switch to skip processing the whole song and to prevent storing the
            songs to the database. Defaults to ``False``.
        """
        # No xml get out of here.
        if not xml:
            return None
        if xml[:5] == u'<?xml':
            xml = xml[38:]
        song_xml = objectify.fromstring(xml)
        if hasattr(song_xml, u'properties'):
            properties = song_xml.properties
        else:
            return None
        if float(song_xml.get(u'version')) > 0.6:
            self._process_formatting_tags(song_xml, parse_and_not_save)
        if parse_and_not_save:
            return
        song = Song()
        # Values will be set when cleaning the song.
        song.search_lyrics = u''
        song.verse_order = u''
        song.search_title = u''
        self._process_copyright(properties, song)
        self._process_cclinumber(properties, song)
        self._process_titles(properties, song)
        # The verse order is processed with the lyrics!
        self._process_lyrics(properties, song_xml, song)
        self._process_comments(properties, song)
        self._process_authors(properties, song)
        self._process_songbooks(properties, song)
        self._process_topics(properties, song)
        clean_song(self.manager, song)
        self.manager.save_object(song)
        return song

    def _add_text_to_element(self, tag, parent, text=None, label=None):
        if label:
            element = etree.Element(tag, name=unicode(label))
        else:
            element = etree.Element(tag)
        if text:
            element.text = unicode(text)
        parent.append(element)
        return element

    def _add_tag_to_formatting(self, tag_name, tags_element):
        """
        Add new formatting tag to the element ``<format>``
        if the tag is not present yet.
        """
        available_tags = FormattingTags.get_html_tags()
        start_tag = '{%s}' % tag_name
        for t in available_tags:
            if t[u'start tag'] == start_tag:
                # Create new formatting tag in openlyrics xml.
                el = self._add_text_to_element(u'tag', tags_element)
                el.set(u'name', tag_name)
                el_open = self._add_text_to_element(u'open', el)
                el_close = self._add_text_to_element(u'close', el)
                el_open.text = etree.CDATA(t[u'start html'])
                el_close.text = etree.CDATA(t[u'end html'])

    def _add_line_with_tags_to_lines(self, parent, text, tags_element):
        """
        Convert text with formatting tags from OpenLP format to OpenLyrics
        format and append it to element ``<lines>``.
        """
        # Tags already converted to xml structure.
        xml_tags = tags_element.xpath(u'tag/attribute::name')
        start_tags = self.start_tags_regex.findall(text)
        end_tags = self.end_tags_regex.findall(text)
        # Replace start tags with xml syntax.
        for tag in start_tags:
            name = tag[1:-1]
            text = text.replace(tag, u'<tag name="%s">' % name)
            # Add tag to <format> element if tag not present.
            if name not in xml_tags:
                self._add_tag_to_formatting(name, tags_element)
        # Replace end tags.
        for t in end_tags:
            text = text.replace(t, u'</tag>')
        text = u'<line>' + text + u'</line>'
        element = etree.XML(text)
        parent.append(element)

    def _extract_xml(self, xml):
        """
        Extract our newly created XML song.
        """
        return etree.tostring(xml, encoding=u'UTF-8',
            xml_declaration=True)

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
        for display_name in authors:
            author = self.manager.get_object_filtered(Author,
                Author.display_name == display_name)
            if author is None:
                # We need to create a new author, as the author does not exist.
                author = Author.populate(display_name=display_name,
                    last_name=display_name.split(u' ')[-1],
                    first_name=u' '.join(display_name.split(u' ')[:-1]))
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

    def _process_formatting_tags(self, song_xml, temporary):
        """
        Process the formatting tags from the song and either add missing tags
        temporary or permanently to the formatting tag list.
        """
        if not hasattr(song_xml, u'format'):
            return
        found_tags = []
        for tag in song_xml.format.tags.getchildren():
            name = tag.get(u'name')
            if name is None:
                continue
            openlp_tag = {
                u'desc': name,
                u'start tag': u'{%s}' % name[:5],
                u'end tag': u'{/%s}' % name[:5],
                u'start html': tag.open.text,
                u'end html': tag.close.text,
                u'protected': False,
                u'temporary': temporary
            }
            found_tags.append(openlp_tag)
        existing_tag_ids = [tag[u'start tag']
            for tag in FormattingTags.get_html_tags()]
        FormattingTags.add_html_tags([tag for tag in found_tags
            if tag[u'start tag'] not in existing_tag_ids], True)

    def _process_lyrics(self, properties, song_xml, song_obj):
        """
        Processes the verses and search_lyrics for the song.

        ``properties``
            The properties object (lxml.objectify.ObjectifiedElement).

        ``song_xml``
            The objectified song (lxml.objectify.ObjectifiedElement).

        ``song_obj``
            The song object.
        """
        sxml = SongXML()
        verses = {}
        verse_def_list = []
        lyrics = song_xml.lyrics
        # Loop over the "verse" elements.
        for verse in lyrics.verse:
            text = u''
            # Loop over the "lines" elements.
            for lines in verse.lines:
                if text:
                    text += u'\n'
                # Loop over the "line" elements removing chords.
                for line in lines.line:
                    if text:
                        text += u'\n'
                    text += u''.join(map(unicode, line.itertext()))
                # Add a virtual split to the verse text.
                if lines.get(u'break') is not None:
                    text += u'\n[---]'
            verse_def = verse.get(u'name', u' ').lower()
            if verse_def[0] in VerseType.Tags:
                verse_tag = verse_def[0]
            else:
                verse_tag = VerseType.Tags[VerseType.Other]
            verse_number = re.compile(u'[a-zA-Z]*').sub(u'', verse_def)
            # OpenLyrics allows e. g. "c", but we need "c1". However, this does
            # not correct the verse order.
            if not verse_number:
                verse_number = u'1'
            lang = verse.get(u'lang')
            # In OpenLP 1.9.6 we used v1a, v1b ... to represent visual slide
            # breaks. In OpenLyrics 0.7 an attribute has been added.
            if song_xml.get(u'modifiedIn') in (u'1.9.6', u'OpenLP 1.9.6') and \
                song_xml.get(u'version') == u'0.7' and \
                (verse_tag, verse_number, lang) in verses:
                verses[(verse_tag, verse_number, lang)] += u'\n[---]\n' + text
            # Merge v1a, v1b, .... to v1.
            elif (verse_tag, verse_number, lang) in verses:
                verses[(verse_tag, verse_number, lang)] += u'\n' + text
            else:
                verses[(verse_tag, verse_number, lang)] = text
                verse_def_list.append((verse_tag, verse_number, lang))
        # We have to use a list to keep the order, as dicts are not sorted.
        for verse in verse_def_list:
            sxml.add_verse_to_lyrics(
                verse[0], verse[1], verses[verse], verse[2])
        song_obj.lyrics = unicode(sxml.extract_xml(), u'utf-8')
        # Process verse order
        if hasattr(properties, u'verseOrder'):
            song_obj.verse_order = self._text(properties.verseOrder)

    def _process_songbooks(self, properties, song):
        """
        Adds the song book and song number specified in the XML to the song.

        ``properties``
            The property object (lxml.objectify.ObjectifiedElement).

        ``song``
            The song object.
        """
        song.song_book_id = None
        song.song_number = u''
        if hasattr(properties, u'songbooks'):
            for songbook in properties.songbooks.songbook:
                bookname = songbook.get(u'name', u'')
                if bookname:
                    book = self.manager.get_object_filtered(Book,
                        Book.name == bookname)
                    if book is None:
                        # We need to create a book, because it does not exist.
                        book = Book.populate(name=bookname, publisher=u'')
                        self.manager.save_object(book)
                    song.song_book_id = book.id
                    song.song_number = songbook.get(u'entry', u'')
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
                song.alternate_title = u''
            else:
                song.alternate_title = self._text(title)

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
