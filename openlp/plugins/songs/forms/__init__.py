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

from openlp.core.lib import translate

class VerseType(object):
    """
    VerseType provides an enumeration for the tags that may be associated
    with verses in songs.
    """
    Verse = 0
    Chorus = 1
    Bridge = 2
    PreChorus = 3
    Intro = 4
    Ending = 5
    Other = 6

    @staticmethod
    def to_string(verse_type):
        """
        Return a string for a given VerseType

        ``verse_type``
            The type to return a string for
        """
        if verse_type == VerseType.Verse:
            return translate(u'VerseType', u'Verse')
        elif verse_type == VerseType.Chorus:
            return translate(u'VerseType', u'Chorus')
        elif verse_type == VerseType.Bridge:
            return translate(u'VerseType', u'Bridge')
        elif verse_type == VerseType.PreChorus:
            return translate(u'VerseType', u'Pre-Chorus')
        elif verse_type == VerseType.Intro:
            return translate(u'VerseType', u'Intro')
        elif verse_type == VerseType.Ending:
            return translate(u'VerseType', u'Ending')
        elif verse_type == VerseType.Other:
            return translate(u'VerseType', u'Other')

    @staticmethod
    def from_string(verse_type):
        """
        Return the VerseType for a given string

        ``verse_type``
            The string to return a VerseType for
        """
        verse_type = verse_type.lower()
        if verse_type == unicode(VerseType.to_string(VerseType.Verse)).lower():
            return VerseType.Verse
        elif verse_type == \
            unicode(VerseType.to_string(VerseType.Chorus)).lower():
            return VerseType.Chorus
        elif verse_type == \
            unicode(VerseType.to_string(VerseType.Bridge)).lower():
            return VerseType.Bridge
        elif verse_type == \
            unicode(VerseType.to_string(VerseType.PreChorus)).lower():
            return VerseType.PreChorus
        elif verse_type == \
            unicode(VerseType.to_string(VerseType.Intro)).lower():
            return VerseType.Intro
        elif verse_type == \
            unicode(VerseType.to_string(VerseType.Ending)).lower():
            return VerseType.Ending
        elif verse_type == \
            unicode(VerseType.to_string(VerseType.Other)).lower():
            return VerseType.Other

from authorsform import AuthorsForm
from topicsform import TopicsForm
from songbookform import SongBookForm
from editverseform import EditVerseForm
from editsongform import EditSongForm
from songmaintenanceform import SongMaintenanceForm
from songimportform import ImportWizardForm
