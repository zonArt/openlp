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

from lxml import objectify
from lxml.etree import XMLSyntaxError

class LyricsXML(object):
    """
    This class represents the XML in the ``lyrics`` field of a song.

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
        except XMLSyntaxError:
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
