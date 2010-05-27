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

import logging
from xml.dom.minidom import Document
from xml.etree.ElementTree import ElementTree, XML, dump

log = logging.getLogger(__name__)

class SongXMLBuilder(object):
    """
    This class builds the XML used to describe songs.

    The basic XML looks like this::

        <?xml version="1.0" encoding="UTF-8"?>
        <song version="1.0">
          <lyrics language="en">
            <verse type="chorus" label="1">
              <![CDATA[ ... ]]>
            </verse>
          </lyrics>
        </song>
    """
    log.info(u'SongXMLBuilder Loaded')

    def __init__(self):
        """
        Set up the song builder.
        """
        # Create the minidom document
        self.song_xml = Document()

    def new_document(self):
        """
        Create a new song XML document.
        """
        # Create the <song> base element
        self.song = self.song_xml.createElement(u'song')
        self.song_xml.appendChild(self.song)
        self.song.setAttribute(u'version', u'1.0')

    def add_lyrics_to_song(self):
        """
        Set up and add a ``<lyrics>`` tag which contains the lyrics of the
        song.
        """
        # Create the main <lyrics> element
        self.lyrics = self.song_xml.createElement(u'lyrics')
        self.lyrics.setAttribute(u'language', u'en')
        self.song.appendChild(self.lyrics)

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
        #log.debug(u'add_verse_to_lyrics %s, %s\n%s' % (type, number, content))
        verse = self.song_xml.createElement(u'verse')
        verse.setAttribute(u'type', type)
        verse.setAttribute(u'label', number)
        self.lyrics.appendChild(verse)
        # add data as a CDATA section to protect the XML from special chars
        cds = self.song_xml.createCDATASection(content)
        verse.appendChild(cds)

    def dump_xml(self):
        """
        Debugging aid to dump XML so that we can see what we have.
        """
        return self.song_xml.toprettyxml(indent=u'  ')

    def extract_xml(self):
        """
        Extract our newly created XML song.
        """
        return self.song_xml.toxml(u'utf-8')


class SongXMLParser(object):
    """
    A class to read in and parse a song's XML.

    The basic XML looks like this::

        <?xml version="1.0" encoding="UTF-8"?>
        <song version="1.0">
          <lyrics language="en">
            <verse type="chorus" label="1">
              <![CDATA[ ... ]]>
            </verse>
          </lyrics>
        </song>
    """
    log.info(u'SongXMLParser Loaded')

    def __init__(self, xml):
        """
        Set up our song XML parser.

        ``xml``
            The XML of the song to be parsed.
        """
        self.song_xml = None
        try:
            self.song_xml = ElementTree(
                element=XML(unicode(xml).encode('unicode-escape')))
        except ExpatError:
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
                verse_list.append([element.attrib,
                    unicode(element.text).decode('unicode-escape')])
        return verse_list

    def dump_xml(self):
        """
        Debugging aid to dump XML so that we can see what we have.
        """
        return dump(self.song_xml)
