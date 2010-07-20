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

from lxml import etree, objectify

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
