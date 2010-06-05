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
    Verse = 0
    Chorus = 1
    Bridge = 2
    PreChorus = 3
    Intro = 4
    Ending = 5
    Other = 6

    @staticmethod
    def to_string(verse_type):
        if verse_type == VerseType.Verse:
            return translate('SongTags', 'Verse')
        elif verse_type == VerseType.Chorus:
            return translate('SongTags', 'Chorus')
        elif verse_type == VerseType.Bridge:
            return translate('SongTags', 'Bridge')
        elif verse_type == VerseType.PreChorus:
            return u'Pre-Chorus'
        elif verse_type == VerseType.Intro:
            return u'Intro'
        elif verse_type == VerseType.Ending:
            return u'Ending'
        elif verse_type == VerseType.Other:
            return u'Other'

    @staticmethod
    def from_string(verse_type):
        verse_type = verse_type.lower()
        if verse_type == translate('SongTags', 'verse'):
            return VerseType.Verse
        elif verse_type == translate('SongTags', 'chorus'):
            return VerseType.Chorus
        elif verse_type == translate('SongTags', 'bridge'):
            return VerseType.Bridge
        elif verse_type == u'pre-chorus':
            return VerseType.PreChorus
        elif verse_type == u'intro':
            return VerseType.Intro
        elif verse_type == u'ending':
            return VerseType.Ending
        elif verse_type == u'other':
            return VerseType.Other

from authorsform import AuthorsForm
from topicsform import TopicsForm
from songbookform import SongBookForm
from editverseform import EditVerseForm
from editsongform import EditSongForm
from songmaintenanceform import SongMaintenanceForm

#from openlpexportform import OpenLPExportForm
#from openlpimportform import OpenLPImportForm
#from opensongexportform import OpenSongExportForm
#from opensongimportform import OpenSongImportForm

from songimportform import ImportWizardForm
