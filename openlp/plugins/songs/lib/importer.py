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
from zionworximport import ZionWorxImport
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

class SongFormatSelect(object):
    """
    This is a special enumeration class listing available file selection modes.
    """
    SingleFile = 0
    MultipleFiles = 1
    SingleFolder = 2

class SongFormat(object):
    """
    This is a special static class that holds an enumeration of the various
    song formats handled by the importer, the attributes of each song format,
    and a few helper functions.

    Required attributes for each song format:

    ``Class``
        Import class, e.g. ``OpenLyricsImport``
    ``Name``
        Name of the format, e.g. ``u'OpenLyrics'``
    ``Prefix``
        Prefix for Qt objects. Use mixedCase, e.g. ``u'openLyrics'``
        See ``SongImportForm.addFileSelectItem()``

    Optional attributes for each song format:

    ``CanDisable``
        Whether song format importer is disablable.
    ``Availability``
        Whether song format importer is available.
    ``SelectMode``
        Whether format accepts single file, multiple files, or single folder
        (as per ``SongFormatSelect`` options).
    ``Filter``
        File extension filter for ``QFileDialog``.

    Optional/custom text Strings for ``SongImportForm`` widgets:

    ``ComboBoxText``
        Combo box selector (default value is the format's ``Name``).
    ``DisabledLabelText``
        Required for disablable song formats.
    ``GetFilesTitle``
        Title for ``QFileDialog`` (default includes the format's ``Name``).
    ``InvalidSourceMsg``
        Message displayed if ``Class.isValidSource()`` returns ``False``.
    ``DescriptionText``
        Short description (1-2 lines) about the song format.
    """
    # Enumeration of song formats and their attributes
    # * Numerical order of song formats is significant as it determines the
    #   order used by formatComboBox.
    # * Attribute ints are negative so they don't clash with song format ints.
    # * Each group of attribute values increments by 10 to facilitate addition
    #   of more attributes in future.

    # Song formats (ordered alphabetically after Generic)
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
    ZionWorx = 15
    #CSV = 16

    # Required attributes
    Class = -10
    Name = -11
    Prefix = -12
    # Optional attributes
    CanDisable = -20
    Availability = -21
    SelectMode = -22
    Filter = -23
    # Optional/custom text values
    ComboBoxText = -30
    DisabledLabelText = -31
    GetFilesTitle = -32
    InvalidSourceMsg = -33
    DescriptionText = -34

    # Set optional attribute defaults
    _defaults = {
        CanDisable: False,
        Availability: True,
        SelectMode: SongFormatSelect.MultipleFiles,
        Filter: u'',
        ComboBoxText: None,
        DisabledLabelText: u'',
        GetFilesTitle: None,
        InvalidSourceMsg: None,
        DescriptionText: None
    }

    # Set attribute values for each Song Format
    _attributes = {
        OpenLyrics: {
            Class: OpenLyricsImport,
            Name: u'OpenLyrics',
            Prefix: u'openLyrics',
            Filter: u'%s (*.xml)' % translate('SongsPlugin.ImportWizardForm',
                'OpenLyrics Files'),
            ComboBoxText: translate('SongsPlugin.ImportWizardForm',
                'OpenLyrics or OpenLP 2.0 Exported Song')
        },
        OpenLP2: {
            Class: OpenLPSongImport,
            Name: UiStrings().OLPV2,
            Prefix: u'openLP2',
            SelectMode: SongFormatSelect.SingleFile,
            Filter: u'%s (*.sqlite)' % (translate(
                'SongsPlugin.ImportWizardForm', 'OpenLP 2.0 Databases'))
        },
        OpenLP1: {
            Name: UiStrings().OLPV1,
            Prefix: u'openLP1',
            CanDisable: True,
            SelectMode: SongFormatSelect.SingleFile,
            Filter: u'%s (*.olp)' % translate('SongsPlugin.ImportWizardForm',
                'openlp.org v1.x Databases'),
            DisabledLabelText: WizardStrings.NoSqlite
        },
        Generic: {
            Name: translate('SongsPlugin.ImportWizardForm',
                'Generic Document/Presentation'),
            Prefix: u'generic',
            CanDisable: True,
            DisabledLabelText: translate('SongsPlugin.ImportWizardForm',
                'The generic document/presentation importer has been disabled '
                'because OpenLP cannot access OpenOffice or LibreOffice.'),
            GetFilesTitle: translate('SongsPlugin.ImportWizardForm',
                'Select Document/Presentation Files')
        },
        CCLI: {
            Class: CCLIFileImport,
            Name: u'CCLI/SongSelect',
            Prefix: u'ccli',
            Filter: u'%s (*.usr *.txt)' % translate(
                'SongsPlugin.ImportWizardForm', 'CCLI SongSelect Files')
        },
        DreamBeam: {
            Class: DreamBeamImport,
            Name: u'DreamBeam',
            Prefix: u'dreamBeam',
            Filter: u'%s (*.xml)' % translate('SongsPlugin.ImportWizardForm',
                'DreamBeam Song Files')
        },
        EasySlides: {
            Class: EasySlidesImport,
            Name: u'EasySlides',
            Prefix: u'easySlides',
            SelectMode: SongFormatSelect.SingleFile,
            Filter: u'%s (*.xml)' % translate('SongsPlugin.ImportWizardForm',
                'EasySlides XML File')
        },
        EasyWorship: {
            Class: EasyWorshipSongImport,
            Name: u'EasyWorship',
            Prefix: u'ew',
            SelectMode: SongFormatSelect.SingleFile,
            Filter: u'%s (*.db)' % translate('SongsPlugin.ImportWizardForm',
                'EasyWorship Song Database')
        },
        FoilPresenter: {
            Class: FoilPresenterImport,
            Name: u'Foilpresenter',
            Prefix: u'foilPresenter',
            Filter: u'%s (*.foil)' % translate('SongsPlugin.ImportWizardForm',
                'Foilpresenter Song Files')
        },
        OpenSong: {
            Class: OpenSongImport,
            Name: WizardStrings.OS,
            Prefix: u'openSong'
        },
        PowerSong: {
            Class: PowerSongImport,
            Name: u'PowerSong 1.0',
            Prefix: u'powerSong',
            SelectMode: SongFormatSelect.SingleFolder,
            InvalidSourceMsg: translate('SongsPlugin.ImportWizardForm',
                'You need to specify a valid PowerSong 1.0 database folder.')
        },
        SongBeamer: {
            Class: SongBeamerImport,
            Name: u'SongBeamer',
            Prefix: u'songBeamer',
            Filter: u'%s (*.sng)' % translate('SongsPlugin.ImportWizardForm',
                'SongBeamer Files')
        },
        SongShowPlus: {
            Class: SongShowPlusImport,
            Name: u'SongShow Plus',
            Prefix: u'songShowPlus',
            Filter: u'%s (*.sbsong)' % translate('SongsPlugin.ImportWizardForm',
                'SongShow Plus Song Files')
        },
        SongsOfFellowship: {
            Name: u'Songs of Fellowship',
            Prefix: u'songsOfFellowship',
            CanDisable: True,
            Filter: u'%s (*.rtf)' % translate('SongsPlugin.ImportWizardForm',
                'Songs Of Fellowship Song Files'),
            DisabledLabelText: translate('SongsPlugin.ImportWizardForm',
                'The Songs of Fellowship importer has been disabled because '
                'OpenLP cannot access OpenOffice or LibreOffice.')
        },
        WordsOfWorship: {
            Class: WowImport,
            Name: u'Words of Worship',
            Prefix: u'wordsOfWorship',
            Filter: u'%s (*.wsg *.wow-song)' % translate(
                'SongsPlugin.ImportWizardForm', 'Words Of Worship Song Files')
        },
        ZionWorx: {
            Class: ZionWorxImport,
            Name: u'ZionWorx',
            Prefix: u'zionWorx',
            SelectMode: SongFormatSelect.SingleFile,
            ComboBoxText: translate('SongsPlugin.ImportWizardForm',
                'ZionWorx (CSV)'),
            DescriptionText: translate('SongsPlugin.ImportWizardForm',
                'First dump your ZionWorx database to a CSV text file, using '
                'freeware tool TdbDataX "TurboDB Data Exchange" from dataWeb '
                '(see the User Manual).')
#        },
#        CSV: {
#            class_: CSVImport,
#            name: WizardStrings.CSV,
#            prefix: u'csv',
#            select_mode: SongFormatSelect.SingleFile
        }
    }

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
            SongFormat.WordsOfWorship,
            SongFormat.ZionWorx
        ]
    
    @staticmethod
    def get(format, *attributes):
        """
        Return requested song format attribute(s).

        ``format``
            A song format from SongFormat.

        ``*attributes``
            Zero or more song format attributes from SongFormat.

        Return type depends on number of supplied attributes:
        :0: Return dict containing all defined attributes for the format.
        :1: Return the attribute value.
        :>1: Return tuple of requested attribute values.
        """
        if not attributes:
            return SongFormat._attributes.get(format)
        elif len(attributes) == 1:
            default = SongFormat._defaults.get(attributes[0])
            return SongFormat._attributes[format].get(attributes[0],
                default)
        else:
            values = []
            for attr in attributes:
                default = SongFormat._defaults.get(attr)
                values.append(SongFormat._attributes[format].get(attr,
                    default))
            return tuple(values)

    @staticmethod
    def set(format, attribute, value):
        """
        Set specified song format attribute to the supplied value.
        """
        SongFormat._attributes[format][attribute] = value

SongFormat.set(SongFormat.OpenLP1, SongFormat.Availability, HAS_OPENLP1)
if HAS_OPENLP1:
    SongFormat.set(SongFormat.OpenLP1, SongFormat.Class, OpenLP1SongImport)
SongFormat.set(SongFormat.SongsOfFellowship, SongFormat.Availability, HAS_SOF)
if HAS_SOF:
    SongFormat.set(SongFormat.SongsOfFellowship, SongFormat.Class, SofImport)
SongFormat.set(SongFormat.Generic, SongFormat.Availability, HAS_OOO)
if HAS_OOO:
    SongFormat.set(SongFormat.Generic, SongFormat.Class, OooImport)

__all__ = [u'SongFormat', u'SongFormatSelect']
