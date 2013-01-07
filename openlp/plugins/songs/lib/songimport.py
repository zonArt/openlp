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

import logging
import re
import shutil
import os

from PyQt4 import QtCore

from openlp.core.lib import Receiver, translate, check_directory_exists
from openlp.core.ui.wizard import WizardStrings
from openlp.core.utils import AppLocation
from openlp.plugins.songs.lib import clean_song, VerseType
from openlp.plugins.songs.lib.db import Song, Author, Topic, Book, MediaFile
from openlp.plugins.songs.lib.ui import SongStrings
from openlp.plugins.songs.lib.xml import SongXML

log = logging.getLogger(__name__)

class SongImport(QtCore.QObject):
    """
    Helper class for import a song from a third party source into OpenLP

    This class just takes the raw strings, and will work out for itself
    whether the authors etc already exist and add them or refer to them
    as necessary
    """
    @staticmethod
    def isValidSource(import_source):
        """
        Override this method to validate the source prior to import.
        """
        return True

    def __init__(self, manager, **kwargs):
        """
        Initialise and create defaults for properties

        ``manager``
            An instance of a SongManager, through which all database access is
            performed.

        """
        self.manager = manager
        QtCore.QObject.__init__(self)
        if u'filename' in kwargs:
            self.importSource = kwargs[u'filename']
        elif u'filenames' in kwargs:
            self.importSource = kwargs[u'filenames']
        elif u'folder' in kwargs:
            self.importSource = kwargs[u'folder']
        else:
            raise KeyError(u'Keyword arguments "filename[s]" or "folder" not supplied.')
        log.debug(self.importSource)
        self.importWizard = None
        self.song = None
        self.stopImportFlag = False
        self.setDefaults()
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'openlp_stop_wizard'), self.stopImport)

    def setDefaults(self):
        """
        Create defaults for properties - call this before each song
        if importing many songs at once to ensure a clean beginning
        """
        self.title = u''
        self.songNumber = u''
        self.alternateTitle = u''
        self.copyright = u''
        self.comments = u''
        self.themeName = u''
        self.ccliNumber = u''
        self.authors = []
        self.topics = []
        self.mediaFiles = []
        self.songBookName = u''
        self.songBookPub = u''
        self.verseOrderListGeneratedUseful = False
        self.verseOrderListGenerated = []
        self.verseOrderList = []
        self.verses = []
        self.verseCounts = {}
        self.copyrightString = translate('SongsPlugin.SongImport', 'copyright')

    def logError(self, filepath, reason=SongStrings.SongIncomplete):
        """
        This should be called, when a song could not be imported.

        ``filepath``
            This should be the file path if ``self.importSource`` is a list
            with different files. If it is not a list, but a single file (for
            instance a database), then this should be the song's title.

        ``reason``
            The reason why the import failed. The string should be as
            informative as possible.
        """
        self.setDefaults()
        if self.importWizard is None:
            return
        if self.importWizard.errorReportTextEdit.isHidden():
            self.importWizard.errorReportTextEdit.setText(translate('SongsPlugin.SongImport',
                'The following songs could not be imported:'))
            self.importWizard.errorReportTextEdit.setVisible(True)
            self.importWizard.errorCopyToButton.setVisible(True)
            self.importWizard.errorSaveToButton.setVisible(True)
        self.importWizard.errorReportTextEdit.append(u'- %s (%s)' % (filepath, reason))

    def stopImport(self):
        """
        Sets the flag for importers to stop their import
        """
        log.debug(u'Stopping songs import')
        self.stopImportFlag = True

    def register(self, import_wizard):
        self.importWizard = import_wizard

    def tidyText(self, text):
        """
        Get rid of some dodgy unicode and formatting characters we're not
        interested in. Some can be converted to ascii.
        """
        text = text.replace(u'\u2018', u'\'')
        text = text.replace(u'\u2019', u'\'')
        text = text.replace(u'\u201c', u'"')
        text = text.replace(u'\u201d', u'"')
        text = text.replace(u'\u2026', u'...')
        text = text.replace(u'\u2013', u'-')
        text = text.replace(u'\u2014', u'-')
        # Remove surplus blank lines, spaces, trailing/leading spaces
        text = re.sub(r'[ \t\v]+', u' ', text)
        text = re.sub(r' ?(\r\n?|\n) ?', u'\n', text)
        text = re.sub(r' ?(\n{5}|\f)+ ?', u'\f', text)
        return text

    def processSongText(self, text):
        verse_texts = text.split(u'\n\n')
        for verse_text in verse_texts:
            if verse_text.strip() != u'':
                self.processVerseText(verse_text.strip())

    def processVerseText(self, text):
        lines = text.split(u'\n')
        if text.lower().find(self.copyrightString) >= 0 or text.find(unicode(SongStrings.CopyrightSymbol)) >= 0:
            copyright_found = False
            for line in lines:
                if (copyright_found or line.lower().find(self.copyrightString) >= 0 or
                        line.find(unicode(SongStrings.CopyrightSymbol)) >= 0):
                    copyright_found = True
                    self.addCopyright(line)
                else:
                    self.parseAuthor(line)
            return
        if len(lines) == 1:
            self.parseAuthor(lines[0])
            return
        if not self.title:
            self.title = lines[0]
        self.addVerse(text)

    def addCopyright(self, copyright):
        """
        Build the copyright field
        """
        if self.copyright.find(copyright) >= 0:
            return
        if self.copyright != u'':
            self.copyright += ' '
        self.copyright += copyright

    def parseAuthor(self, text):
        """
        Add the author. OpenLP stores them individually so split by 'and', '&'
        and comma. However need to check for 'Mr and Mrs Smith' and turn it to
        'Mr Smith' and 'Mrs Smith'.
        """
        for author in text.split(u','):
            authors = author.split(u'&')
            for i in range(len(authors)):
                author2 = authors[i].strip()
                if author2.find(u' ') == -1 and i < len(authors) - 1:
                    author2 = author2 + u' ' + authors[i + 1].strip().split(u' ')[-1]
                if author2.endswith(u'.'):
                    author2 = author2[:-1]
                if author2:
                    self.addAuthor(author2)

    def addAuthor(self, author):
        """
        Add an author to the list
        """
        if author in self.authors:
            return
        self.authors.append(author)

    def addMediaFile(self, filename, weight=0):
        """
        Add a media file to the list
        """
        if filename in map(lambda x: x[0], self.mediaFiles):
            return
        self.mediaFiles.append((filename, weight))

    def addVerse(self, verse_text, verse_def=u'v', lang=None):
        """
        Add a verse. This is the whole verse, lines split by \\n. It will also
        attempt to detect duplicates. In this case it will just add to the verse
        order.

        ``verse_text``
            The text of the verse.

        ``verse_def``
            The verse tag can be v1/c1/b etc, or 'v' and 'c' (will count the
            verses/choruses itself) or None, where it will assume verse.

        ``lang``
            The language code (ISO-639) of the verse, for example *en* or *de*.

        """
        for (old_verse_def, old_verse, old_lang) in self.verses:
            if old_verse.strip() == verse_text.strip():
                self.verseOrderListGenerated.append(old_verse_def)
                self.verseOrderListGeneratedUseful = True
                return
        if verse_def[0] in self.verseCounts:
            self.verseCounts[verse_def[0]] += 1
        else:
            self.verseCounts[verse_def[0]] = 1
        if len(verse_def) == 1:
            verse_def += unicode(self.verseCounts[verse_def[0]])
        elif int(verse_def[1:]) > self.verseCounts[verse_def[0]]:
            self.verseCounts[verse_def[0]] = int(verse_def[1:])
        self.verses.append([verse_def, verse_text.rstrip(), lang])
        self.verseOrderListGenerated.append(verse_def)

    def repeatVerse(self):
        """
        Repeat the previous verse in the verse order
        """
        if self.verseOrderListGenerated:
            self.verseOrderListGenerated.append(self.verseOrderListGenerated[-1])
            self.verseOrderListGeneratedUseful = True

    def checkComplete(self):
        """
        Check the mandatory fields are entered (i.e. title and a verse)
        Author not checked here, if no author then "Author unknown" is
        automatically added
        """
        if not self.title or not self.verses:
            return False
        else:
            return True

    def finish(self):
        """
        All fields have been set to this song. Write the song to disk.
        """
        if not self.checkComplete():
            self.setDefaults()
            return False
        log.info(u'committing song %s to database', self.title)
        song = Song()
        song.title = self.title
        if self.importWizard is not None:
            self.importWizard.incrementProgressBar(WizardStrings.ImportingType % song.title)
        song.alternate_title = self.alternateTitle
        # Values will be set when cleaning the song.
        song.search_title = u''
        song.search_lyrics = u''
        song.verse_order = u''
        song.song_number = self.songNumber
        verses_changed_to_other = {}
        sxml = SongXML()
        other_count = 1
        for (verse_def, verse_text, lang) in self.verses:
            if verse_def[0].lower() in VerseType.Tags:
                verse_tag = verse_def[0].lower()
            else:
                new_verse_def = u'%s%d' % (VerseType.Tags[VerseType.Other], other_count)
                verses_changed_to_other[verse_def] = new_verse_def
                other_count += 1
                verse_tag = VerseType.Tags[VerseType.Other]
                log.info(u'Versetype %s changing to %s', verse_def, new_verse_def)
                verse_def = new_verse_def
            sxml.add_verse_to_lyrics(verse_tag, verse_def[1:], verse_text, lang)
        song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
        if not self.verseOrderList and self.verseOrderListGeneratedUseful:
            self.verseOrderList = self.verseOrderListGenerated
        self.verseOrderList = map(lambda v: verses_changed_to_other.get(v, v), self.verseOrderList)
        song.verse_order = u' '.join(self.verseOrderList)
        song.copyright = self.copyright
        song.comments = self.comments
        song.theme_name = self.themeName
        song.ccli_number = self.ccliNumber
        for authortext in self.authors:
            author = self.manager.get_object_filtered(Author, Author.display_name == authortext)
            if not author:
                author = Author.populate(display_name=authortext,
                    last_name=authortext.split(u' ')[-1],
                    first_name=u' '.join(authortext.split(u' ')[:-1]))
            song.authors.append(author)
        if self.songBookName:
            song_book = self.manager.get_object_filtered(Book, Book.name == self.songBookName)
            if song_book is None:
                song_book = Book.populate(name=self.songBookName, publisher=self.songBookPub)
            song.book = song_book
        for topictext in self.topics:
            if not topictext:
                continue
            topic = self.manager.get_object_filtered(Topic, Topic.name == topictext)
            if topic is None:
                topic = Topic.populate(name=topictext)
            song.topics.append(topic)
        # We need to save the song now, before adding the media files, so that
        # we know where to save the media files to.
        clean_song(self.manager, song)
        self.manager.save_object(song)
        # Now loop through the media files, copy them to the correct location,
        # and save the song again.
        for filename, weight in self.mediaFiles:
            media_file = self.manager.get_object_filtered(MediaFile, MediaFile.file_name == filename)
            if not media_file:
                if os.path.dirname(filename):
                    filename = self.copyMediaFile(song.id, filename)
                song.media_files.append(MediaFile.populate(file_name=filename, weight=weight))
        self.manager.save_object(song)
        self.setDefaults()
        return True

    def copyMediaFile(self, song_id, filename):
        """
        This method copies the media file to the correct location and returns
        the new file location.

        ``filename``
            The file to copy.
        """
        if not hasattr(self, u'save_path'):
            self.save_path = os.path.join(AppLocation.get_section_data_path(self.importWizard.plugin.name),
                'audio', str(song_id))
        check_directory_exists(self.save_path)
        if not filename.startswith(self.save_path):
            oldfile, filename = filename, os.path.join(self.save_path, os.path.split(filename)[1])
            shutil.copyfile(oldfile, filename)
        return filename
