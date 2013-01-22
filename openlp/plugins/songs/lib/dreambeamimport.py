# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
The :mod:`dreambeamimport` module provides the functionality for importing
DreamBeam songs into the OpenLP database.
"""
import logging

from lxml import etree, objectify

from openlp.core.lib import translate
from openlp.plugins.songs.lib.songimport import SongImport
from openlp.plugins.songs.lib.ui import SongStrings

log = logging.getLogger(__name__)

class DreamBeamImport(SongImport):
    """
    The :class:`DreamBeamImport` class provides the ability to import song files from
    DreamBeam.

    An example of DreamBeam xml mark-up::

        <?xml version="1.0"?>
        <DreamSong xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema">
          <WordWrap>false</WordWrap>
          <Version>0.80</Version>
          <Title>Amazing Grace</Title>
          <Author>John Newton</Author>
          <Collection />
          <Number />
          <Notes />
          <KeyRangeLow>F</KeyRangeLow>
          <KeyRangeHigh>G</KeyRangeHigh>
          <MinorKey>false</MinorKey>
          <DualLanguage>false</DualLanguage>
          <SongLyrics>
            <LyricsItem Type="Verse" Number="1">Amazing Grace, how sweet the sound,
            That saved a wretch like me.
            I once was lost but now am found,
            Was blind, but now, I see.</LyricsItem>
            <LyricsItem Type="Verse" Number="2">T’was Grace that taught my heart to fear.
            And Grace, my fears relieved.
            How precious did that Grace appear…
            the hour I first believed.</LyricsItem>
          </SongLyrics>
          <Sequence>
            <LyricsSequenceItem Type="Verse" Number="1" />
            <LyricsSequenceItem Type="Verse" Number="2" />
          </Sequence>
          <ShowRectangles>false</ShowRectangles>
        </DreamSong>

    Valid extensions for a DreamBeam song file are:

        * \*.xml
    """

    def doImport(self):
        """
        Receive a single file or a list of files to import.
        """
        if isinstance(self.importSource, list):
            self.importWizard.progressBar.setMaximum(len(self.importSource))
            for file in self.importSource:
                if self.stopImportFlag:
                    return
                self.setDefaults()
                parser = etree.XMLParser(remove_blank_text=True)
                try:
                    parsed_file = etree.parse(open(file, u'r'), parser)
                except etree.XMLSyntaxError:
                    log.exception(u'XML syntax error in file %s' % file)
                    self.logError(file, SongStrings.XMLSyntaxError)
                    continue
                xml = unicode(etree.tostring(parsed_file))
                song_xml = objectify.fromstring(xml)
                if song_xml.tag != u'DreamSong':
                    self.logError(file, unicode(
                        translate('SongsPlugin.DreamBeamImport',
                            ('Invalid DreamBeam song file. Missing DreamSong tag.'))))
                    continue
                if hasattr(song_xml, u'Version'):
                    self.version = float(song_xml.Version.text)
                else:
                    self.version = 0
                # Version numbers found in DreamBeam Source /FileTypes/Song.cs
                if self.version >= 0.5:
                    if hasattr(song_xml, u'Title'):
                        self.title = unicode(song_xml.Title.text)
                    if hasattr(song_xml, u'Author'):
                        author_copyright = song_xml.Author.text
                    if hasattr(song_xml, u'SongLyrics'):
                        for lyrics_item in song_xml.SongLyrics.iterchildren():
                            verse_type =  lyrics_item.get(u'Type')
                            verse_number = lyrics_item.get(u'Number')
                            verse_text = unicode(lyrics_item.text)
                            self.addVerse(verse_text, (u'%s%s' % (verse_type[:1], verse_number)))
                    if hasattr(song_xml, u'Collection'):
                        self.songBookName = unicode(song_xml.Collection.text)
                    if hasattr(song_xml, u'Number'):
                        self.songNumber = unicode(song_xml.Number.text)
                    if hasattr(song_xml, u'Sequence'):
                        for LyricsSequenceItem in (song_xml.Sequence.iterchildren()):
                            self.verseOrderList.append("%s%s" % (LyricsSequenceItem.get(u'Type')[:1],
                                LyricsSequenceItem.get(u'Number')))
                    if hasattr(song_xml, u'Notes'):
                        self.comments = unicode(song_xml.Notes.text)
                else:
                    if hasattr(song_xml.Text0, u'Text'):
                        self.title = unicode(song_xml.Text0.Text.text)
                    if hasattr(song_xml.Text1, u'Text'):
                        self.lyrics = unicode(song_xml.Text1.Text.text)
                        for verse in self.lyrics.split(u'\n\n\n'):
                            self.addVerse(verse)
                    if hasattr(song_xml.Text2, u'Text'):
                        author_copyright = song_xml.Text2.Text.text
                if author_copyright:
                    author_copyright = unicode(author_copyright)
                    if author_copyright.find(
                        unicode(SongStrings.CopyrightSymbol)) >= 0:
                        self.addCopyright(author_copyright)
                    else:
                        self.parseAuthor(author_copyright)
                if not self.finish():
                    self.logError(file)
