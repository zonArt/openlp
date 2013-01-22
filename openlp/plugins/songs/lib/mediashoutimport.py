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
The :mod:`mediashoutimport` module provides the functionality for importing
a MediaShout database into the OpenLP database.
"""
import pyodbc

from openlp.core.lib import translate
from openlp.plugins.songs.lib.songimport import SongImport

VERSE_TAGS = [u'V', u'C', u'B', u'O', u'P', u'I', u'E']

class MediaShoutImport(SongImport):
    """
    The :class:`MediaShoutImport` class provides the ability to import the
    MediaShout Access Database
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the MediaShout importer.
        """
        SongImport.__init__(self, manager, **kwargs)

    def doImport(self):
        """
        Receive a single file to import.
        """
        try:
           conn = pyodbc.connect(u'DRIVER={Microsoft Access Driver (*.mdb)};'
            u'DBQ=%s;PWD=6NOZ4eHK7k' % self.importSource)
        except:
            # Unfortunately no specific exception type
            self.logError(self.importSource,
                translate('SongsPlugin.MediaShoutImport', 'Unable to open the MediaShout database.'))
            return
        cursor = conn.cursor()
        cursor.execute(u'SELECT Record, Title, Author, Copyright, '
                       u'SongID, CCLI, Notes FROM Songs ORDER BY Title')
        songs = cursor.fetchall()
        self.importWizard.progressBar.setMaximum(len(songs))
        for song in songs:
            if self.stopImportFlag:
                break
            cursor.execute(u'SELECT Type, Number, Text FROM Verses '
                u'WHERE Record = %s ORDER BY Type, Number' % song.Record)
            verses = cursor.fetchall()
            cursor.execute(u'SELECT Type, Number, POrder FROM PlayOrder '
                u'WHERE Record = %s ORDER BY POrder' % song.Record)
            verse_order = cursor.fetchall()
            cursor.execute(u'SELECT Name FROM Themes INNER JOIN SongThemes '
                u'ON SongThemes.ThemeId = Themes.ThemeId '
                u'WHERE SongThemes.Record = %s' % song.Record)
            topics = cursor.fetchall()
            cursor.execute(u'SELECT Name FROM Groups INNER JOIN SongGroups '
                u'ON SongGroups.GroupId = Groups.GroupId '
                u'WHERE SongGroups.Record = %s' % song.Record)
            topics += cursor.fetchall()
            self.processSong(song, verses, verse_order, topics)

    def processSong(self, song, verses, verse_order, topics):
        """
        Create the song, i.e. title, verse etc.
        """
        self.setDefaults()
        self.title = song.Title
        self.parseAuthor(song.Author)
        self.addCopyright(song.Copyright)
        self.comments = song.Notes
        for topic in topics:
            self.topics.append(topic.Name)
        if u'-' in song.SongID:
            self.songBookName, self.songNumber = song.SongID.split(u'-', 1)
        else:
            self.songBookName = song.SongID
        for verse in verses:
            tag = VERSE_TAGS[verse.Type] + unicode(verse.Number) if verse.Type < len(VERSE_TAGS) else u'O'
            self.addVerse(verse.Text, tag)
        for order in verse_order:
            if order.Type < len(VERSE_TAGS):
                self.verseOrderList.append(VERSE_TAGS[order.Type] + unicode(order.Number))
        self.finish()
