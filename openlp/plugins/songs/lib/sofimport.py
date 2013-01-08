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

# OOo API documentation:
# http://wiki.services.openoffice.org/wiki/Documentation/BASIC_Guide/Structure_of_Text_Documents
# http://wiki.services.openoffice.org/wiki/Documentation/DevGuide/Text/Iterating_over_Text
# http://www.oooforum.org/forum/viewtopic.phtml?t=14409
# http://wiki.services.openoffice.org/wiki/Python

import logging
import os
import re

from oooimport import OooImport


log = logging.getLogger(__name__)

if os.name == u'nt':
    from oooimport import PAGE_BEFORE, PAGE_AFTER, PAGE_BOTH
    RuntimeException = Exception
else:
    try:
        from com.sun.star.style.BreakType import PAGE_BEFORE, PAGE_AFTER, \
            PAGE_BOTH
        from com.sun.star.uno import RuntimeException
    except ImportError:
        pass
try:
    from com.sun.star.awt.FontWeight import BOLD
except ImportError:
    BOLD = 150.0
try:
    from com.sun.star.awt.FontSlant import ITALIC
except ImportError:
    ITALIC = 2

class SofImport(OooImport):
    """
    Import songs provided on disks with the Songs of Fellowship music books
    VOLS1_2.RTF, sof3words.rtf and sof4words.rtf

    Use OpenOffice.org Writer for processing the rtf file

    The three books are not only inconsistant with each other, they are
    inconsistant in themselves too with their formatting. Not only this, but
    the 1+2 book does not space out verses correctly. This script attempts
    to sort it out, but doesn't get it 100% right. But better than having to
    type them all out!

    It attempts to detect italiced verses, and treats these as choruses in
    the verse ordering. Again not perfect, but a start.
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the class. Requires a songmanager class which is passed
        to SongImport for writing song to disk
        """
        OooImport.__init__(self, manager, **kwargs)
        self.song = False

    def processOooDocument(self):
        """
        Handle the import process for SoF files.
        """
        self.processSofFile()

    def processSofFile(self):
        """
        Process the RTF file, a paragraph at a time
        """
        self.blankLines = 0
        self.newSong()
        try:
            paragraphs = self.document.getText().createEnumeration()
            while paragraphs.hasMoreElements():
                if self.stopImportFlag:
                    return
                paragraph = paragraphs.nextElement()
                if paragraph.supportsService("com.sun.star.text.Paragraph"):
                    self.processParagraph(paragraph)
        except RuntimeException as exc:
            log.exception(u'Error processing file: %s', exc)
        if not self.finish():
            self.logError(self.filepath)

    def processParagraph(self, paragraph):
        """
        Process a paragraph.
        In the first book, a paragraph is a single line. In the latter ones
        they may contain multiple lines.
        Each paragraph contains textportions. Each textportion has it's own
        styling, e.g. italics, bold etc.
        Also check for page breaks, which indicates a new song in books 1+2.
        In later books, there may not be line breaks, so check for 3 or more
        newlines
        """
        text = u''
        textportions = paragraph.createEnumeration()
        while textportions.hasMoreElements():
            textportion = textportions.nextElement()
            if textportion.BreakType in (PAGE_BEFORE, PAGE_BOTH):
                self.processParagraphText(text)
                self.newSong()
                text = u''
            text += self.processTextPortion(textportion)
            if textportion.BreakType in (PAGE_AFTER, PAGE_BOTH):
                self.processParagraphText(text)
                self.newSong()
                text = u''
        self.processParagraphText(text)

    def processParagraphText(self, text):
        """
        Split the paragraph text into multiple lines and process
        """
        for line in text.split(u'\n'):
            self.processParagraphLine(line)
        if self.blankLines > 2:
            self.newSong()

    def processParagraphLine(self, text):
        """
        Process a single line. Throw away that text which isn't relevant, i.e.
        stuff that appears at the end of the song.
        Anything that is OK, append to the current verse
        """
        text = text.strip()
        if text == u'':
            self.blankLines += 1
            if self.blankLines > 1:
                return
            if self.title != u'':
                self.finishVerse()
            return
        self.blankLines = 0
        if self.skipToCloseBracket:
            if text.endswith(u')'):
                self.skipToCloseBracket = False
            return
        if text.startswith(u'CCL Licence'):
            self.italics = False
            return
        if text == u'A Songs of Fellowship Worship Resource':
            return
        if text.startswith(u'(NB.') or text.startswith(u'(Regrettably') or text.startswith(u'(From'):
            self.skipToCloseBracket = True
            return
        if text.startswith(u'Copyright'):
            self.addCopyright(text)
            return
        if text == u'(Repeat)':
            self.finishVerse()
            self.repeatVerse()
            return
        if self.title == u'':
            if self.copyright == u'':
                self.addSofAuthor(text)
            else:
                self.addCopyright(text)
            return
        self.addVerseLine(text)

    def processTextPortion(self, textportion):
        """
        Process a text portion. Here we just get the text and detect if
        it's bold or italics. If it's bold then its a song number or song title.
        Song titles are in all capitals, so we must bring the capitalization
        into line
        """
        text = textportion.getString()
        text = self.tidyText(text)
        if text.strip() == u'':
            return text
        if textportion.CharWeight == BOLD:
            boldtext = text.strip()
            if boldtext.isdigit() and self.songNumber == '':
                self.addSongNumber(boldtext)
                return u''
            text = self.uncapText(text)
            if self.title == u'':
                self.addTitle(text)
            return text
        if text.strip().startswith(u'('):
            return text
        self.italics = (textportion.CharPosture == ITALIC)
        return text

    def newSong(self):
        """
        A change of song. Store the old, create a new
        ... but only if the last song was complete. If not, stick with it
        """
        if self.song:
            self.finishVerse()
            if not self.checkComplete():
                return
            self.finish()
        self.song = True
        self.setDefaults()
        self.skipToCloseBracket = False
        self.isChorus = False
        self.italics = False
        self.currentVerse = u''

    def addSongNumber(self, song_no):
        """
        Add a song number, store as alternate title. Also use the song
        number to work out which songbook we're in
        """
        self.songNumber = song_no
        self.alternateTitle = song_no + u'.'
        self.songBook_pub = u'Kingsway Publications'
        if int(song_no) <= 640:
            self.songBook = u'Songs of Fellowship 1'
        elif int(song_no) <= 1150:
            self.songBook = u'Songs of Fellowship 2'
        elif int(song_no) <= 1690:
            self.songBook = u'Songs of Fellowship 3'
        elif int(song_no) <= 2200:
            self.songBook = u'Songs of Fellowship 4'
        elif int(song_no) <= 2710:
            self.songBook = u'Songs of Fellowship 5'
        else:
            self.songBook = u'Songs of Fellowship Other'

    def addTitle(self, text):
        """
        Add the title to the song. Strip some leading/trailing punctuation that
        we don't want in a title
        """
        title = text.strip()
        if title.startswith(u'\''):
            title = title[1:]
        if title.endswith(u','):
            title = title[:-1]
        self.title = title
        self.importWizard.incrementProgressBar(u'Processing song ' + title, 0)

    def addSofAuthor(self, text):
        """
        Add the author. OpenLP stores them individually so split by 'and', '&'
        and comma.
        However need to check for "Mr and Mrs Smith" and turn it to
        "Mr Smith" and "Mrs Smith".
        """
        text = text.replace(u' and ', u' & ')
        self.parseAuthor(text)

    def addVerseLine(self, text):
        """
        Add a line to the current verse. If the formatting has changed and
        we're beyond the second line of first verse, then this indicates
        a change of verse. Italics are a chorus
        """
        if self.italics != self.isChorus and ((len(self.verses) > 0) or
            (self.currentVerse.count(u'\n') > 1)):
            self.finishVerse()
        if self.italics:
            self.isChorus = True
        self.currentVerse += text + u'\n'

    def finishVerse(self):
        """
        Verse is finished, store it. Note in book 1+2, some songs are formatted
        incorrectly. Here we try and split songs with missing line breaks into
        the correct number of verses.
        """
        if self.currentVerse.strip() == u'':
            return
        if self.isChorus:
            versetag = u'C'
            splitat = None
        else:
            versetag = u'V'
            splitat = self.verseSplits(self.songNumber)
        if splitat:
            ln = 0
            verse = u''
            for line in self.currentVerse.split(u'\n'):
                ln += 1
                if line == u'' or ln > splitat:
                    self.addSofVerse(verse, versetag)
                    ln = 0
                    if line:
                        verse = line + u'\n'
                    else:
                        verse = u''
                else:
                    verse += line + u'\n'
            if verse:
                self.addSofVerse(verse, versetag)
        else:
            self.addSofVerse(self.currentVerse, versetag)
        self.currentVerse = u''
        self.isChorus = False

    def addSofVerse(self, lyrics, tag):
        self.addVerse(lyrics, tag)
        if not self.isChorus and u'C1' in self.verseOrderListGenerated:
            self.verseOrderListGenerated.append(u'C1')
            self.verseOrderListGenerated_useful = True

    def uncapText(self, text):
        """
        Words in the title are in all capitals, so we lowercase them.
        However some of these words, e.g. referring to God need a leading
        capital letter.

        There is a complicated word "One", which is sometimes lower and
        sometimes upper depending on context. Never mind, keep it lower.
        """
        textarr = re.split(u'(\W+)', text)
        textarr[0] = textarr[0].capitalize()
        for i in range(1, len(textarr)):
            # Do not translate these. Fixed strings in SOF song file
            if textarr[i] in (u'JESUS', u'CHRIST', u'KING', u'ALMIGHTY',
                u'REDEEMER', u'SHEPHERD', u'SON', u'GOD', u'LORD', u'FATHER',
                u'HOLY', u'SPIRIT', u'LAMB', u'YOU', u'YOUR', u'I', u'I\'VE',
                u'I\'M', u'I\'LL', u'SAVIOUR', u'O', u'YOU\'RE', u'HE', u'HIS',
                u'HIM', u'ZION', u'EMMANUEL', u'MAJESTY', u'JESUS\'', u'JIREH',
                u'JUDAH', u'LION', u'LORD\'S', u'ABRAHAM', u'GOD\'S',
                u'FATHER\'S', u'ELIJAH' u'MARTHA', u'CHRISTMAS', u'ALPHA',
                u'OMEGA'):
                textarr[i] = textarr[i].capitalize()
            else:
                textarr[i] = textarr[i].lower()
        text = u''.join(textarr)
        return text

    def verseSplits(self, song_number):
        """
        Because someone at Kingsway forgot to check the 1+2 RTF file,
        some verses were not formatted correctly.
        """
        if song_number == 11:
            return 8
        if song_number == 18:
            return 5
        if song_number == 21:
            return 6
        if song_number == 23:
            return 4
        if song_number == 24:
            return 7
        if song_number == 27:
            return 4
        if song_number == 31:
            return 6
        if song_number == 49:
            return 4
        if song_number == 50:
            return 8
        if song_number == 70:
            return 4
        if song_number == 75:
            return 8
        if song_number == 79:
            return 6
        if song_number == 97:
            return 7
        if song_number == 107:
            return 4
        if song_number == 109:
            return 4
        if song_number == 133:
            return 4
        if song_number == 155:
            return 10
        if song_number == 156:
            return 8
        if song_number == 171:
            return 4
        if song_number == 188:
            return 7
        if song_number == 192:
            return 4
        if song_number == 208:
            return 8
        if song_number == 215:
            return 8
        if song_number == 220:
            return 4
        if song_number == 247:
            return 6
        if song_number == 248:
            return 6
        if song_number == 251:
            return 8
        if song_number == 295:
            return 8
        if song_number == 307:
            return 5
        if song_number == 314:
            return 6
        if song_number == 325:
            return 8
        if song_number == 386:
            return 6
        if song_number == 415:
            return 4
        if song_number == 426:
            return 4
        if song_number == 434:
            return 5
        if song_number == 437:
            return 4
        if song_number == 438:
            return 6
        if song_number == 456:
            return 8
        if song_number == 461:
            return 4
        if song_number == 469:
            return 4
        if song_number == 470:
            return 5
        if song_number == 476:
            return 6
        if song_number == 477:
            return 7
        if song_number == 480:
            return 8
        if song_number == 482:
            return 4
        if song_number == 512:
            return 4
        if song_number == 513:
            return 8
        if song_number == 518:
            return 5
        if song_number == 520:
            return 4
        if song_number == 523:
            return 6
        if song_number == 526:
            return 8
        if song_number == 527:
            return 4
        if song_number == 529:
            return 4
        if song_number == 537:
            return 4
        if song_number == 555:
            return 6
        if song_number == 581:
            return 4
        if song_number == 589:
            return 6
        if song_number == 590:
            return 4
        if song_number == 593:
            return 8
        if song_number == 596:
            return 4
        if song_number == 610:
            return 6
        if song_number == 611:
            return 6
        if song_number == 619:
            return 8
        if song_number == 645:
            return 5
        if song_number == 653:
            return 6
        if song_number == 683:
            return 7
        if song_number == 686:
            return 4
        if song_number == 697:
            return 8
        if song_number == 698:
            return 4
        if song_number == 704:
            return 6
        if song_number == 716:
            return 4
        if song_number == 717:
            return 6
        if song_number == 730:
            return 4
        if song_number == 731:
            return 8
        if song_number == 732:
            return 8
        if song_number == 738:
            return 4
        if song_number == 756:
            return 9
        if song_number == 815:
            return 6
        if song_number == 830:
            return 8
        if song_number == 831:
            return 4
        if song_number == 876:
            return 6
        if song_number == 877:
            return 6
        if song_number == 892:
            return 4
        if song_number == 894:
            return 6
        if song_number == 902:
            return 8
        if song_number == 905:
            return 8
        if song_number == 921:
            return 6
        if song_number == 940:
            return 7
        if song_number == 955:
            return 9
        if song_number == 968:
            return 8
        if song_number == 972:
            return 7
        if song_number == 974:
            return 4
        if song_number == 988:
            return 6
        if song_number == 991:
            return 5
        if song_number == 1002:
            return 8
        if song_number == 1024:
            return 8
        if song_number == 1044:
            return 9
        if song_number == 1088:
            return 6
        if song_number == 1117:
            return 6
        if song_number == 1119:
            return 7
        return None
