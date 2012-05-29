# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
The :mod:`importer` modules provides the general song import functionality.
"""
import logging

from openlp.core.lib.ui import UiStrings
from openlp.core.ui.wizard import WizardStrings
from opensongimport import OpenSongImport
from easyslidesimport import EasySlidesImport
from olpimport import OpenLPSongImport
from openlyricsimport import OpenLyricsImport
from wowimport import WowImport
from cclifileimport import CCLIFileImport
from dreambeamimport import DreamBeamImport
from powersongimport import PowerSongImport
from ewimport import EasyWorshipSongImport
from songbeamerimport import SongBeamerImport
from songshowplusimport import SongShowPlusImport
from foilpresenterimport import FoilPresenterImport
# Imports that might fail
log = logging.getLogger(__name__)
try:
    from olp1import import OpenLP1SongImport
    HAS_OPENLP1 = True
except ImportError:
    log.exception('Error importing %s', 'OpenLP1SongImport')
    HAS_OPENLP1 = False
try:
    from sofimport import SofImport
    HAS_SOF = True
except ImportError:
    log.exception('Error importing %s', 'SofImport')
    HAS_SOF = False
try:
    from oooimport import OooImport
    HAS_OOO = True
except ImportError:
    log.exception('Error importing %s', 'OooImport')
    HAS_OOO = False

class SongFormat(object):
    """
    This is a special enumeration class that holds the various types of songs,
    plus a few helper functions to facilitate generic handling of song types
    for importing.
    """
    Unknown = -1
    OpenLyrics = 0
    OpenLP2 = 1
    OpenLP1 = 2
    Generic = 3
    CCLI = 4
    DreamBeam = 5
    EasySlides = 6
    EasyWorship = 7
    FoilPresenter = 8
    OpenSong = 9
    PowerSong = 10
    SongBeamer = 11
    SongShowPlus = 12
    SongsOfFellowship = 13
    WordsOfWorship = 14
    #CSV = 15

    @staticmethod
    def get_formats():
        """
        Return a list of the supported song formats.
        """
        return [
            SongFormat.OpenLyrics,
            SongFormat.OpenLP2,
            SongFormat.OpenLP1,
            SongFormat.Generic,
            SongFormat.CCLI,
            SongFormat.DreamBeam,
            SongFormat.EasySlides,
            SongFormat.EasyWorship,
            SongFormat.FoilPresenter,
            SongFormat.OpenSong,
            SongFormat.PowerSong,
            SongFormat.SongBeamer,
            SongFormat.SongShowPlus,
            SongFormat.SongsOfFellowship,
            SongFormat.WordsOfWorship
        ]

class SongFormatAttribute(object):
    # Required attributes:
    class_ = 0
    name = 1
    prefix = 2
    # Optional attributes:
    obj_prefix = 10
    can_disable = 11
    availability = 12
    select_mode = 13
    # Required widget Text:
    combo_box_text = 20
    # Optional widget Text
    disabled_label_text = 30
    filter = 31

    # Set attribute defaults (if not specified here, default is None)
    _defaults = {
        obj_prefix: None,
        can_disable: False,
        availability: True,
        select_mode: SongFormatSelect.MultipleFiles,
        disabled_label_text: u'',
        filter: u''
    }

    # Set attribute values
    _attributes = {
        SongFormat.OpenLyrics: {
            class_: OpenLyricsImport,
            name: WizardStrings.OL,
            prefix: u'openLyrics',
            obj_prefix: u'OpenLyrics',
            can_disable: True,
            combo_box_text: translate('SongsPlugin.ImportWizardForm',
                'OpenLyrics or OpenLP 2.0 Exported Song'),
            disabled_label_text: translate('SongsPlugin.ImportWizardForm',
                'The OpenLyrics importer has not yet been developed, but as '
                'you can see, we are still intending to do so. Hopefully it '
                'will be in the next release.'),
            filter: u'%s (*.xml)' % translate('SongsPlugin.ImportWizardForm',
                'OpenLyrics Files')
        },
        SongFormat.OpenLP2: {
            class_: OpenLPSongImport,
            name: UiStrings().OLPV2,
            prefix: u'openLP2',
            select_mode: SongFormatSelect.SingleFile,
            combo_box_text: UiStrings().OLPV2,
            filter: u'%s (*.sqlite)' % (translate(
                'SongsPlugin.ImportWizardForm', 'OpenLP 2.0 Databases'))
        },
        SongFormat.OpenLP1: {
            class_: OpenLP1SongImport,
            name: UiStrings().OLPV1,
            prefix: u'openLP1',
            can_disable: True,
            select_mode: SongFormatSelect.SingleFile,
            combo_box_text: UiStrings().OLPV1,
            disabled_label_text: WizardStrings.NoSqlite,
            filter: u'%s (*.olp)' % translate('SongsPlugin.ImportWizardForm',
                'openlp.org v1.x Databases')
        },
        SongFormat.Generic: {
            class_: OooImport,
#            name: ,
            prefix: u'generic',
            can_disable: True,
            combo_box_text: translate('SongsPlugin.ImportWizardForm',
                'Generic Document/Presentation'),
            disabled_label_text: translate('SongsPlugin.ImportWizardForm',
                'The generic document/presentation importer has been disabled '
                'because OpenLP cannot access OpenOffice or LibreOffice.')
        },
        SongFormat.CCLI: {
            class_: CCLIFileImport,
            name: WizardStrings.CCLI,
            prefix: u'ccli',
            combo_box_text: WizardStrings.CCLI,
            filter: u'%s (*.usr *.txt)' % translate(
                'SongsPlugin.ImportWizardForm', 'CCLI SongSelect Files')
        },
        SongFormat.DreamBeam: {
            class_: DreamBeamImport,
            name: WizardStrings.DB,
            prefix: u'dreamBeam',
            combo_box_text: WizardStrings.DB,
            filter: u'%s (*.xml)' % translate('SongsPlugin.ImportWizardForm',
                'DreamBeam Song Files')
        },
        SongFormat.EasySlides: {
            class_: EasySlidesImport,
            name: WizardStrings.ES,
            prefix: u'easySlides',
            select_mode: SongFormatSelect.SingleFile,
            combo_box_text: WizardStrings.ES,
            filter: u'%s (*.xml)' % translate('SongsPlugin.ImportWizardForm',
                'EasySlides XML File')
        },
        SongFormat.EasyWorship: {
            class_: EasyWorshipSongImport,
            name: WizardStrings.EW,
            prefix: u'ew',
            select_mode: SongFormatSelect.SingleFile,
            combo_box_text: WizardStrings.EW,
            filter: u'%s (*.db)' % translate('SongsPlugin.ImportWizardForm',
                'EasyWorship Song Database')
        },
        SongFormat.FoilPresenter: {
            class_: FoilPresenterImport,
            name: WizardStrings.FP,
            prefix: u'foilPresenter',
            combo_box_text: WizardStrings.FP,
            filter: u'%s (*.foil)' % translate('SongsPlugin.ImportWizardForm',
                'Foilpresenter Song Files')
        },
        SongFormat.OpenSong: {
            class_: OpenSongImport,
            name: WizardStrings.OS,
            prefix: u'openSong',
            obj_prefix: u'OpenSong',
            combo_box_text: WizardStrings.OS
        },
        SongFormat.PowerSong: {
            class_: PowerSongImport,
            name: WizardStrings.PS,
            prefix: u'powerSong',
            select_mode: SongFormatSelect.SingleFolder,
            combo_box_text: WizardStrings.PS
        },
        SongFormat.SongBeamer: {
            class_: SongBeamerImport,
            name: WizardStrings.SB,
            prefix: u'songBeamer',
            combo_box_text: WizardStrings.SB,
            filter: u'%s (*.sng)' % translate('SongsPlugin.ImportWizardForm',
                'SongBeamer Files')
        },
        SongFormat.SongShowPlus: {
            class_: SongShowPlusImport,
            name: WizardStrings.SSP,
            prefix: u'songShowPlus',
            combo_box_text: WizardStrings.SSP,
            filter: u'%s (*.sbsong)' % translate('SongsPlugin.ImportWizardForm',
                'SongShow Plus Song Files')
        },
        SongFormat.SongsOfFellowship: {
            class_: SofImport,
            name: WizardStrings.SoF,
            prefix: u'songsOfFellowship',
            can_disable: True,
            combo_box_text: WizardStrings.SoF,
            disabled_label_text: translate('SongsPlugin.ImportWizardForm',
                'The Songs of Fellowship importer has been disabled because '
                'OpenLP cannot access OpenOffice or LibreOffice.'),
            filter: u'%s (*.rtf)' % translate('SongsPlugin.ImportWizardForm',
                'Songs Of Fellowship Song Files')
        },
        SongFormat.WordsOfWorship: {
            class_: WowImport,
            name: WizardStrings.WoW,
            prefix: u'wordsOfWorship',
            combo_box_text: WizardStrings.WoW,
            filter: u'%s (*.wsg *.wow-song)' % translate(
                'SongsPlugin.ImportWizardForm', 'Words Of Worship Song Files')
#        },
#        SongFormat.CSV: {
#            class_: CSVImport,
#            name: WizardStrings.CSV,
#            prefix: u'csv',
#            obj_prefix: u'CSV',
#            select_mode: SongFormatSelect.SingleFile,
#            combo_box_text: WizardStrings.CSV
        }
    }

    @staticmethod
    def get(format, attribute):
        default = _defaults.get(attribute)
        return SongFormat._attributes[format].get(attribute, default)

    @staticmethod
    def set(format, attribute, value):
        SongFormat._attributes[format][attribute] = value

class SongFormatSelect(object):
    SingleFile = 0
    MultipleFiles = 1
    SingleFolder = 2

SongFormatAttribute.set(
    SongFormat.OpenLP1, SongFormatAttribute.availability, HAS_OPENLP1)
SongFormatAttribute.set(
    SongFormat.SongsOfFellowship, SongFormatAttribute.availability, HAS_SOF)
SongFormatAttribute.set(
    SongFormat.Generic, SongFormatAttribute.availability, HAS_OOO)

__all__ = [u'SongFormat']

