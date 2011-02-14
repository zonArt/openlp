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

import logging
import os
from zipfile import ZipFile
from lxml import objectify
from lxml.etree import Error, LxmlError
import re

from openlp.core.ui.wizard import WizardStrings
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

#TODO: Use lxml for parsing and make sure we use methods of "SongImport" .
class OpenSongImport(SongImport):
    """
    Import songs exported from OpenSong

    The format is described loosly on the `OpenSong File Format Specification
    <http://www.opensong.org/d/manual/song_file_format_specification>`_ page on
    the OpenSong web site. However, it doesn't describe the <lyrics> section,
    so here's an attempt:

    Verses can be expressed in one of 2 ways, either in complete verses, or by
    line grouping, i.e. grouping all line 1's of a verse together, all line 2's
    of a verse together, and so on.

    An example of complete verses::

        <lyrics>
        [v1]
         List of words
         Another Line

        [v2]
         Some words for the 2nd verse
         etc...
        </lyrics>

    The 'v' in the verse specifiers above can be left out, it is implied.

    An example of line grouping::

        <lyrics>
        [V]
        1List of words
        2Some words for the 2nd Verse

        1Another Line
        2etc...
        </lyrics>

    Either or both forms can be used in one song. The number does not
    necessarily appear at the start of the line. Additionally, the [v1] labels
    can have either upper or lower case Vs.

    Other labels can be used also:

    C
        Chorus

    B
        Bridge

    All verses are imported and tagged appropriately.

    Guitar chords can be provided "above" the lyrics (the line is preceeded by
    a period "."), and one or more "_" can be used to signify long-drawn-out
    words. Chords and "_" are removed by this importer. For example::

        . A7        Bm
        1 Some____ Words

    The <presentation> tag is used to populate the OpenLP verse display order
    field. The Author and Copyright tags are also imported to the appropriate
    places.

    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the class.
        """
        SongImport.__init__(self, manager)
        self.filenames = kwargs[u'filenames']
        self.song = None
        self.commit = True

    def do_import(self):
        """
        Import either each of the files in self.filenames - each element of
        which can be either a single opensong file, or a zipfile containing
        multiple opensong files. If `self.commit` is set False, the
        import will not be committed to the database (useful for test scripts).
        """
        success = True
        numfiles = 0
        for filename in self.filenames:
            ext = os.path.splitext(filename)[1]
            if ext.lower() == u'.zip':
                z = ZipFile(filename, u'r')
                numfiles += len(z.infolist())
            else:
                numfiles += 1
        log.debug(u'Total number of files: %d', numfiles)
        self.import_wizard.progressBar.setMaximum(numfiles)
        for filename in self.filenames:
            if self.stop_import_flag:
                success = False
                break
            ext = os.path.splitext(filename)[1]
            if ext.lower() == u'.zip':
                log.debug(u'Zipfile found %s', filename)
                z = ZipFile(filename, u'r')
                for song in z.infolist():
                    if self.stop_import_flag:
                        success = False
                        break
                    parts = os.path.split(song.filename)
                    if parts[-1] == u'':
                        #No final part => directory
                        continue
                    log.info(u'Zip importing %s', parts[-1])
                    self.import_wizard.incrementProgressBar(
                        WizardStrings.ImportingType % parts[-1])
                    songfile = z.open(song)
                    self.do_import_file(songfile)
                    if self.commit:
                        self.finish()
                if self.stop_import_flag:
                    success = False
                    break
            else:
                # not a zipfile
                log.info(u'Direct import %s', filename)
                self.import_wizard.incrementProgressBar(
                    WizardStrings.ImportingType % os.path.split(filename)[-1])
                file = open(filename)
                self.do_import_file(file)
                if self.commit:
                    self.finish()

        return success

    def do_import_file(self, file):
        """
        Process the OpenSong file - pass in a file-like object,
        not a filename
        """
        self.set_defaults()
        try:
            tree = objectify.parse(file)
        except (Error, LxmlError):
            log.exception(u'Error parsing XML')
            return
        root = tree.getroot()
        fields = dir(root)
        decode = {
            u'copyright': self.add_copyright,
            u'ccli': u'ccli_number',
            u'author': self.parse_author,
            u'title': u'title',
            u'aka': u'alternate_title',
            u'hymn_number': u'song_number'
        }
        for attr, fn_or_string in decode.items():
            if attr in fields:
                ustring = unicode(root.__getattr__(attr))
                if isinstance(fn_or_string, basestring):
                    setattr(self, fn_or_string, ustring)
                else:
                    fn_or_string(ustring)
        if u'theme' in fields and unicode(root.theme) not in self.topics:
            self.topics.append(unicode(root.theme))
        if u'alttheme' in fields and unicode(root.alttheme) not in self.topics:
            self.topics.append(unicode(root.alttheme))
        # data storage while importing
        verses = {}
        # keep track of a "default" verse order, in case none is specified
        our_verse_order = []
        verses_seen = {}
        # in the absence of any other indication, verses are the default,
        # erm, versetype!
        versetype = u'V'
        versenum = None
        lyrics = unicode(root.lyrics)
        for thisline in lyrics.split(u'\n'):
            # remove comments
            semicolon = thisline.find(u';')
            if semicolon >= 0:
                thisline = thisline[:semicolon]
            thisline = thisline.strip()
            if len(thisline) == 0:
                continue
            # skip inthisline guitar chords and page and column breaks
            if thisline[0] == u'.' or thisline.startswith(u'---') \
                or thisline.startswith(u'-!!'):
                continue
            # verse/chorus/etc. marker
            if thisline[0] == u'[':
                # drop the square brackets
                right_bracket = thisline.find(u']')
                content = thisline[1:right_bracket].upper()
                # have we got any digits?
                # If so, versenumber is everything from the digits
                # to the end (even if there are some alpha chars on the end)
                match = re.match(u'(.*)(\d+.*)', content)
                if match is not None:
                    versetype = match.group(1)
                    versenum = match.group(2)
                else:
                    # otherwise we assume number 1 and take the whole prefix as
                    # the versetype
                    versetype = content
                    versenum = u'1'
                continue
            words = None
            # number at start of line.. it's verse number
            if thisline[0].isdigit():
                versenum = thisline[0]
                words = thisline[1:].strip()
            if words is None:
                words = thisline
                if not versenum:
                    versenum = u'1'
            if versenum is not None:
                versetag = u'%s%s' % (versetype, versenum)
                if not verses.has_key(versetype):
                    verses[versetype] = {}
                if not verses[versetype].has_key(versenum):
                    # storage for lines in this verse
                    verses[versetype][versenum] = []
                if not verses_seen.has_key(versetag):
                    verses_seen[versetag] = 1
                    our_verse_order.append(versetag)
            if words:
                # Tidy text and remove the ____s from extended words
                words = self.tidy_text(words)
                words = words.replace('_', '')
                verses[versetype][versenum].append(words)
        # done parsing
        versetypes = verses.keys()
        versetypes.sort()
        versetags = {}
        for versetype in versetypes:
            our_verse_type = versetype
            if our_verse_type == u'':
                our_verse_type = u'V'
            versenums = verses[versetype].keys()
            versenums.sort()
            for num in versenums:
                versetag = u'%s%s' % (our_verse_type, num)
                lines = u'\n'.join(verses[versetype][num])
                self.add_verse(lines, versetag)
                # Keep track of what we have for error checking later
                versetags[versetag] = 1
        # now figure out the presentation order
        order = []
        if u'presentation' in fields and root.presentation != u'':
            order = unicode(root.presentation)
            # We make all the tags in the lyrics upper case, so match that here
            # and then split into a list on the whitespace
            order = order.upper().split()
        else:
            if len(our_verse_order) > 0:
                order = our_verse_order
            else:
                log.warn(u'No verse order available for %s, skipping.',
                    self.title)
        # TODO: make sure that the default order list will be overwritten, if
        # the songs provides its own order list.
        for tag in order:
            if tag[0].isdigit():
                # Assume it's a verse if it has no prefix
                tag = u'V' + tag
            elif not re.search('\d+', tag):
                # Assume it's no.1 if there's no digits
                tag = tag + u'1'
            if not versetags.has_key(tag):
                log.info(u'Got order %s but not in versetags, dropping this'
                    u'item from presentation order', tag)
            else:
                self.verse_order_list.append(tag)
