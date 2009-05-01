# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten Tinggaard

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
from xml.dom.minidom import  Document
from xml.etree.ElementTree import ElementTree, XML, dump

<?xml version="1.0" encoding="UTF-8"?>
<song version="1.0">
   <lyrics language="en">
       <verse type="chorus" label="1">
           <![CDATA[ ... ]]>
       </verse>
   </lyrics>
</song>

"""
from xml.dom.minidom import  Document
from xml.etree.ElementTree import ElementTree, XML, dump

class SongXMLBuilder():
    def __init__(self):
        # Create the minidom document
        self.song_xml = Document()

    def new_document(self):
        # Create the <song> base element
        self.song = self.song_xml.createElement(u'song')
        self.song_xml.appendChild(self.song)
        self.song.setAttribute(u'version', u'1.0')

    def add_lyrics_to_song(self):
        # Create the main <lyrics> element
        self.lyrics = self.song_xml.createElement(u'lyrics')
        self.lyrics.setAttribute(u'language', u'en')
        self.song.appendChild(self.lyrics)

    def add_verse_to_lyrics(self, type, number, content):
        """
        type - type of verse (Chorus, Verse , Bridge, Custom etc
        number - number of item eg verse 1
        content - the text to be stored
        """
        verse = self.song_xml.createElement(u'verse')
        verse.setAttribute(u'type', type)
        verse.setAttribute(u'label', number)
        self.lyrics.appendChild(verse)

        # add data as a CDATA section
        cds = self.song_xml.createCDATASection(content)
        verse.appendChild(cds)

    def dump_xml(self):
        # Debugging aid to see what we have
        print self.song_xml.toprettyxml(indent="  ")

    def extract_xml(self):
        # Print our newly created XML
        return self.song_xml.toxml()

class SongXMLParser():
    def __init__(self, xml):
        self.song_xml = ElementTree(element=XML(xml))

    def get_verses(self):
        #return a list of verse's and attributes
        iter=self.song_xml.getiterator()
        verse_list = []
        for element in iter:
            #print element.tag, element.attrib, element.text
            if element.tag == u'verse':
                verse_list.append([element.attrib, element.text])
        return verse_list

    def dump_xml(self):
        # Debugging aid to see what we have
        print dump(self.song_xml)
