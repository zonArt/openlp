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

from openlp.core.lib import translate
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
    This is a special enumeration class that holds the various types of song
    importers and some helper functions to facilitate access.
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
    def get_format_list():
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

class SongFormatSelect(object):
    """
    This is a special enumeration class listing available file selection modes.
    """
    SingleFile = 0
    MultipleFiles = 1
    SingleFolder = 2

class SongFormatAttr(object):
    """
    This is a special static class that holds the attributes of each song format
    to aid the importing of each song type.

    The various definable attributes are enumerated as follows:

    Required attributes for each song format:
        * ``class_`` Import class, e.g. OpenLyricsImport
        * ``name`` Name of this format, e.g. u'OpenLyrics'
        * ``prefix`` Prefix for objects. Use camelCase, e.g. u'openLyrics'
          See ``SongImportForm.addFileSelectItem()``.

    Optional attributes for each song format:
        * ``obj_prefix`` Alternate prefix for objects.
          See ``SongImportForm.addFileSelectItem()``.
        * ``can_disable`` Whether song format is disablable.
        * ``availability`` Whether song format is available.
        * ``select_mode`` Whether format accepts single file, multiple files, or
          single folder.
        * ``filter`` File extension filter for QFileDialog.

    Optional/custom text values for SongImportForm widgets:
       * ``combo_box_text`` Combo box selector (default is format name).
       * ``disabled_label_text`` Required for disablable song formats.
       * ``get_files_title`` Title for QFileDialog (default includes format
         name).
       * ``invalid_source_msg`` Message shown when source does not validate with
         class_.isValidSource().
    """
    # Required attributes
    class_ = 0
    name = 1
    prefix = 2
    # Optional attributes
    obj_prefix = 10
    can_disable = 11
    availability = 12
    select_mode = 13
    filter = 14
    # Optional/custom text values
    combo_box_text = 20
    disabled_label_text = 21
    get_files_title = 22
    invalid_source_msg = 23

    # Set optional attribute defaults
    _defaults = {
        obj_prefix: None,
        can_disable: False,
        availability: True,
        select_mode: SongFormatSelect.MultipleFiles,
        filter: u'',
        combo_box_text: None,
        disabled_label_text: u'',
        get_files_title: None,
        invalid_source_msg: None
    }

    # Set attribute values
    _attributes = {
        SongFormat.OpenLyrics: {
            class_: OpenLyricsImport,
            name: u'OpenLyrics',
            prefix: u'openLyrics',
            obj_prefix: u'OpenLyrics',
            can_disable: True,
            filter: u'%s (*.xml)' % translate('SongsPlugin.ImportWizardForm',
                'OpenLyrics Files'),
            combo_box_text: translate('SongsPlugin.ImportWizardForm',
                'OpenLyrics or OpenLP 2.0 Exported Song'),
            disabled_label_text: translate('SongsPlugin.ImportWizardForm',
                'The OpenLyrics importer has not yet been developed, but as '
                'you can see, we are still intending to do so. Hopefully it '
                'will be in the next release.')
        },
        SongFormat.OpenLP2: {
            class_: OpenLPSongImport,
            name: UiStrings().OLPV2,
            prefix: u'openLP2',
            select_mode: SongFormatSelect.SingleFile,
            filter: u'%s (*.sqlite)' % (translate(
                'SongsPlugin.ImportWizardForm', 'OpenLP 2.0 Databases'))
        },
        SongFormat.OpenLP1: {
            name: UiStrings().OLPV1,
            prefix: u'openLP1',
            can_disable: True,
            select_mode: SongFormatSelect.SingleFile,
            filter: u'%s (*.olp)' % translate('SongsPlugin.ImportWizardForm',
                'openlp.org v1.x Databases'),
            disabled_label_text: WizardStrings.NoSqlite
        },
        SongFormat.Generic: {
            name: translate('SongsPlugin.ImportWizardForm',
                'Generic Document/Presentation'),
            prefix: u'generic',
            can_disable: True,
            disabled_label_text: translate('SongsPlugin.ImportWizardForm',
                'The generic document/presentation importer has been disabled '
                'because OpenLP cannot access OpenOffice or LibreOffice.'),
            get_files_title: translate('SongsPlugin.ImportWizardForm',
                'Select Document/Presentation Files')
        },
        SongFormat.CCLI: {
            class_: CCLIFileImport,
            name: u'CCLI/SongSelect',
            prefix: u'ccli',
            filter: u'%s (*.usr *.txt)' % translate(
                'SongsPlugin.ImportWizardForm', 'CCLI SongSelect Files')
        },
        SongFormat.DreamBeam: {
            class_: DreamBeamImport,
            name: u'DreamBeam',
            prefix: u'dreamBeam',
            filter: u'%s (*.xml)' % translate('SongsPlugin.ImportWizardForm',
                'DreamBeam Song Files')
        },
        SongFormat.EasySlides: {
            class_: EasySlidesImport,
            name: u'EasySlides',
            prefix: u'easySlides',
            select_mode: SongFormatSelect.SingleFile,
            filter: u'%s (*.xml)' % translate('SongsPlugin.ImportWizardForm',
                'EasySlides XML File')
        },
        SongFormat.EasyWorship: {
            class_: EasyWorshipSongImport,
            name: u'EasyWorship',
            prefix: u'ew',
            select_mode: SongFormatSelect.SingleFile,
            filter: u'%s (*.db)' % translate('SongsPlugin.ImportWizardForm',
                'EasyWorship Song Database')
        },
        SongFormat.FoilPresenter: {
            class_: FoilPresenterImport,
            name: u'Foilpresenter',
            prefix: u'foilPresenter',
            filter: u'%s (*.foil)' % translate('SongsPlugin.ImportWizardForm',
                'Foilpresenter Song Files')
        },
        SongFormat.OpenSong: {
            class_: OpenSongImport,
            name: WizardStrings.OS,
            prefix: u'openSong',
            obj_prefix: u'OpenSong'
        },
        SongFormat.PowerSong: {
            class_: PowerSongImport,
            name: u'PowerSong 1.0',
            prefix: u'powerSong',
            select_mode: SongFormatSelect.SingleFolder,
            invalid_source_msg: translate('SongsPlugin.ImportWizardForm',
                'You need to specify a valid PowerSong 1.0 database folder.')
        },
        SongFormat.SongBeamer: {
            class_: SongBeamerImport,
            name: u'SongBeamer',
            prefix: u'songBeamer',
            filter: u'%s (*.sng)' % translate('SongsPlugin.ImportWizardForm',
                'SongBeamer Files')
        },
        SongFormat.SongShowPlus: {
            class_: SongShowPlusImport,
            name: u'SongShow Plus',
            prefix: u'songShowPlus',
            filter: u'%s (*.sbsong)' % translate('SongsPlugin.ImportWizardForm',
                'SongShow Plus Song Files')
        },
        SongFormat.SongsOfFellowship: {
            name: u'Songs of Fellowship',
            prefix: u'songsOfFellowship',
            can_disable: True,
            filter: u'%s (*.rtf)' % translate('SongsPlugin.ImportWizardForm',
                'Songs Of Fellowship Song Files'),
            disabled_label_text: translate('SongsPlugin.ImportWizardForm',
                'The Songs of Fellowship importer has been disabled because '
                'OpenLP cannot access OpenOffice or LibreOffice.')
        },
        SongFormat.WordsOfWorship: {
            class_: WowImport,
            name: u'Words of Worship',
            prefix: u'wordsOfWorship',
            filter: u'%s (*.wsg *.wow-song)' % translate(
                'SongsPlugin.ImportWizardForm', 'Words Of Worship Song Files')
#        },
#        SongFormat.CSV: {
#            class_: CSVImport,
#            name: WizardStrings.CSV,
#            prefix: u'csv',
#            obj_prefix: u'CSV',
#            select_mode: SongFormatSelect.SingleFile
        }
    }

    @staticmethod
    def get(format, *attributes):
        """
        Return requested song format attribute(s).

        ``format``
            A song format from SongFormat.

        ``*attributes``
            Zero or more song format attributes from SongFormatAttr.

        Return type depends on number of supplied attributes:
            * 0 : Return dict containing all defined attributes for the format.
            * 1 : Return the attribute value.
            * >1 : Return tuple of requested attribute values.
        """
        if not attributes:
            return SongFormatAttr._attributes.get(format)
        elif len(attributes) == 1:
            default = SongFormatAttr._defaults.get(attributes[0])
            return SongFormatAttr._attributes[format].get(attributes[0],
                default)
        else:
            values = []
            for attr in attributes:
                default = SongFormatAttr._defaults.get(attr)
                values.append(SongFormatAttr._attributes[format].get(attr,
                    default))
            return tuple(values)

    @staticmethod
    def set(format, attribute, value):
        """
        Set specified song format attribute to the supplied value.
        """
        SongFormatAttr._attributes[format][attribute] = value

SongFormatAttr.set(SongFormat.OpenLP1, SongFormatAttr.availability, HAS_OPENLP1)
if HAS_OPENLP1:
    SongFormatAttr.set(SongFormat.OpenLP1, SongFormatAttr.class_,
        OpenLP1SongImport)
SongFormatAttr.set(SongFormat.SongsOfFellowship, SongFormatAttr.availability,
    HAS_SOF)
if HAS_SOF:
    SongFormatAttr.set(SongFormat.SongsOfFellowship, SongFormatAttr.class_,
        SofImport)
SongFormatAttr.set(SongFormat.Generic, SongFormatAttr.availability, HAS_OOO)
if HAS_OOO:
    SongFormatAttr.set(SongFormat.Generic, SongFormatAttr.class_,
        OooImport)

__all__ = [u'SongFormat', u'SongFormatSelect', u'SongFormatAttr']
