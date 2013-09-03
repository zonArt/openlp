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
The :mod:`importer` modules provides the general song import functionality.
"""
import os
import logging

from openlp.core.lib import translate, UiStrings
from openlp.core.ui.wizard import WizardStrings
from .opensongimport import OpenSongImport
from .easyslidesimport import EasySlidesImport
from .olpimport import OpenLPSongImport
from .openlyricsimport import OpenLyricsImport
from .wowimport import WowImport
from .cclifileimport import CCLIFileImport
from .dreambeamimport import DreamBeamImport
from .powersongimport import PowerSongImport
from .ewimport import EasyWorshipSongImport
from .songbeamerimport import SongBeamerImport
from .songshowplusimport import SongShowPlusImport
from .songproimport import SongProImport
from .sundayplusimport import SundayPlusImport
from .foilpresenterimport import FoilPresenterImport
from .zionworximport import ZionWorxImport
# Imports that might fail


log = logging.getLogger(__name__)


try:
    from .sofimport import SofImport
    HAS_SOF = True
except ImportError:
    log.exception('Error importing %s', 'SofImport')
    HAS_SOF = False
try:
    from .oooimport import OooImport
    HAS_OOO = True
except ImportError:
    log.exception('Error importing %s', 'OooImport')
    HAS_OOO = False
HAS_MEDIASHOUT = False
if os.name == 'nt':
    try:
        from .mediashoutimport import MediaShoutImport
        HAS_MEDIASHOUT = True
    except ImportError:
        log.exception('Error importing %s', 'MediaShoutImport')
HAS_WORSHIPCENTERPRO = False
if os.name == 'nt':
    try:
        from .worshipcenterproimport import WorshipCenterProImport
        HAS_WORSHIPCENTERPRO = True
    except ImportError:
        log.exception('Error importing %s', 'WorshipCenterProImport')

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

    ``u'class'``
        Import class, e.g. ``OpenLyricsImport``

    ``u'name'``
        Name of the format, e.g. ``u'OpenLyrics'``

    ``u'prefix'``
        Prefix for Qt objects. Use mixedCase, e.g. ``u'openLyrics'``
        See ``SongImportForm.addFileSelectItem()``

    Optional attributes for each song format:

    ``u'canDisable'``
        Whether song format importer is disablable.
        If ``True``, then ``u'disabledLabelText'`` must also be defined.

    ``u'availability'``
        Whether song format importer is available.

    ``u'selectMode'``
        Whether format accepts single file, multiple files, or single folder
        (as per ``SongFormatSelect`` options).

    ``u'filter'``
        File extension filter for ``QFileDialog``.

    Optional/custom text Strings for ``SongImportForm`` widgets:

    ``u'comboBoxText'``
        Combo box selector (default value is the format's ``u'name'``).

    ``u'disabledLabelText'``
        Required for disablable song formats.

    ``u'getFilesTitle'``
        Title for ``QFileDialog`` (default includes the format's ``u'name'``).

    ``u'invalidSourceMsg'``
        Message displayed if ``isValidSource()`` returns ``False``.

    ``u'descriptionText'``
        Short description (1-2 lines) about the song format.
    """
    # Song formats (ordered alphabetically after Generic)
    # * Numerical order of song formats is significant as it determines the
    #   order used by format_combo_box.
    Unknown = -1
    OpenLyrics = 0
    OpenLP2 = 1
    Generic = 2
    CCLI = 3
    DreamBeam = 4
    EasySlides = 5
    EasyWorship = 6
    FoilPresenter = 7
    MediaShout = 8
    OpenSong = 9
    PowerSong = 10
    SongBeamer = 11
    SongPro = 12
    SongShowPlus = 13
    SongsOfFellowship = 14
    SundayPlus = 15
    WordsOfWorship = 16
    WorshipCenterPro = 17
    ZionWorx = 18

    # Set optional attribute defaults
    __defaults__ = {
        'canDisable': False,
        'availability': True,
        'selectMode': SongFormatSelect.MultipleFiles,
        'filter': '',
        'comboBoxText': None,
        'disabledLabelText': translate('SongsPlugin.ImportWizardForm', 'This importer has been disabled.'),
        'getFilesTitle': None,
        'invalidSourceMsg': None,
        'descriptionText': None
    }

    # Set attribute values for each Song Format
    __attributes__ = {
        OpenLyrics: {
            'class': OpenLyricsImport,
            'name': 'OpenLyrics',
            'prefix': 'openLyrics',
            'filter': '%s (*.xml)' % translate('SongsPlugin.ImportWizardForm', 'OpenLyrics Files'),
            'comboBoxText': translate('SongsPlugin.ImportWizardForm', 'OpenLyrics or OpenLP 2.0 Exported Song')
        },
        OpenLP2: {
            'class': OpenLPSongImport,
            'name': UiStrings().OLPV2,
            'prefix': 'openLP2',
            'selectMode': SongFormatSelect.SingleFile,
            'filter': '%s (*.sqlite)' % (translate('SongsPlugin.ImportWizardForm', 'OpenLP 2.0 Databases'))
        },
        Generic: {
            'name': translate('SongsPlugin.ImportWizardForm', 'Generic Document/Presentation'),
            'prefix': 'generic',
            'canDisable': True,
            'disabledLabelText': translate('SongsPlugin.ImportWizardForm',
                'The generic document/presentation importer has been disabled '
                'because OpenLP cannot access OpenOffice or LibreOffice.'),
            'getFilesTitle': translate('SongsPlugin.ImportWizardForm', 'Select Document/Presentation Files')
        },
        CCLI: {
            'class': CCLIFileImport,
            'name': 'CCLI/SongSelect',
            'prefix': 'ccli',
            'filter': '%s (*.usr *.txt)' % translate('SongsPlugin.ImportWizardForm', 'CCLI SongSelect Files')
        },
        DreamBeam: {
            'class': DreamBeamImport,
            'name': 'DreamBeam',
            'prefix': 'dreamBeam',
            'filter': '%s (*.xml)' % translate('SongsPlugin.ImportWizardForm', 'DreamBeam Song Files')
        },
        EasySlides: {
            'class': EasySlidesImport,
            'name': 'EasySlides',
            'prefix': 'easySlides',
            'selectMode': SongFormatSelect.SingleFile,
            'filter': '%s (*.xml)' % translate('SongsPlugin.ImportWizardForm', 'EasySlides XML File')
        },
        EasyWorship: {
            'class': EasyWorshipSongImport,
            'name': 'EasyWorship',
            'prefix': 'ew',
            'selectMode': SongFormatSelect.SingleFile,
            'filter': '%s (*.db)' % translate('SongsPlugin.ImportWizardForm', 'EasyWorship Song Database')
        },
        FoilPresenter: {
            'class': FoilPresenterImport,
            'name': 'Foilpresenter',
            'prefix': 'foilPresenter',
            'filter': '%s (*.foil)' % translate('SongsPlugin.ImportWizardForm', 'Foilpresenter Song Files')
        },
        MediaShout: {
            'name': 'MediaShout',
            'prefix': 'mediaShout',
            'canDisable': True,
            'selectMode': SongFormatSelect.SingleFile,
            'filter': '%s (*.mdb)' % translate('SongsPlugin.ImportWizardForm',
                'MediaShout Database'),
            'disabledLabelText': translate('SongsPlugin.ImportWizardForm',
                'The MediaShout importer is only supported on Windows. It has '
                'been disabled due to a missing Python module. If you want to '
                'use this importer, you will need to install the "pyodbc" '
                'module.')
        },
        OpenSong: {
            'class': OpenSongImport,
            'name': WizardStrings.OS,
            'prefix': 'openSong'
        },
        PowerSong: {
            'class': PowerSongImport,
            'name': 'PowerSong 1.0',
            'prefix': 'powerSong',
            'selectMode': SongFormatSelect.SingleFolder,
            'invalidSourceMsg': translate('SongsPlugin.ImportWizardForm',
                'You need to specify a valid PowerSong 1.0 database folder.')
        },
        SongBeamer: {
            'class': SongBeamerImport,
            'name': 'SongBeamer',
            'prefix': 'songBeamer',
            'filter': '%s (*.sng)' % translate('SongsPlugin.ImportWizardForm',
                'SongBeamer Files')
        },
        SongPro: {
            'class': SongProImport,
            'name': 'SongPro',
            'prefix': 'songPro',
            'selectMode': SongFormatSelect.SingleFile,
            'filter': '%s (*.txt)' % translate('SongsPlugin.ImportWizardForm', 'SongPro Text Files'),
            'comboBoxText': translate('SongsPlugin.ImportWizardForm', 'SongPro (Export File)'),
            'descriptionText': translate('SongsPlugin.ImportWizardForm',
                'In SongPro, export your songs using the File -> Export menu')
        },
        SongShowPlus: {
            'class': SongShowPlusImport,
            'name': 'SongShow Plus',
            'prefix': 'songShowPlus',
            'filter': '%s (*.sbsong)' % translate('SongsPlugin.ImportWizardForm', 'SongShow Plus Song Files')
        },
        SongsOfFellowship: {
            'name': 'Songs of Fellowship',
            'prefix': 'songsOfFellowship',
            'canDisable': True,
            'filter': '%s (*.rtf)' % translate('SongsPlugin.ImportWizardForm', 'Songs Of Fellowship Song Files'),
            'disabledLabelText': translate('SongsPlugin.ImportWizardForm',
                'The Songs of Fellowship importer has been disabled because '
                'OpenLP cannot access OpenOffice or LibreOffice.')
        },
        SundayPlus: {
            'class': SundayPlusImport,
            'name': 'SundayPlus',
            'prefix': 'sundayPlus',
            'filter': '%s (*.ptf)' % translate('SongsPlugin.ImportWizardForm', 'SundayPlus Song Files')
        },
        WordsOfWorship: {
            'class': WowImport,
            'name': 'Words of Worship',
            'prefix': 'wordsOfWorship',
            'filter': '%s (*.wsg *.wow-song)' %
                translate('SongsPlugin.ImportWizardForm', 'Words Of Worship Song Files')
        },
        WorshipCenterPro: {
            'name': 'WorshipCenter Pro',
            'prefix': 'worshipCenterPro',
            'canDisable': True,
            'selectMode': SongFormatSelect.SingleFile,
            'filter': '%s (*.mdb)' % translate('SongsPlugin.ImportWizardForm', 'WorshipCenter Pro Song Files'),
            'disabledLabelText': translate('SongsPlugin.ImportWizardForm',
                'The WorshipCenter Pro importer is only supported on Windows. It has been disabled due to a missing '
                'Python module. If you want to use this importer, you will need to install the "pyodbc" module.')
        },
        ZionWorx: {
            'class': ZionWorxImport,
            'name': 'ZionWorx',
            'prefix': 'zionWorx',
            'selectMode': SongFormatSelect.SingleFile,
            'comboBoxText': translate('SongsPlugin.ImportWizardForm', 'ZionWorx (CSV)'),
            'descriptionText': translate('SongsPlugin.ImportWizardForm',
                'First convert your ZionWorx database to a CSV text file, as '
                'explained in the <a href="http://manual.openlp.org/songs.html'
                '#importing-from-zionworx">User Manual</a>.')
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
            SongFormat.Generic,
            SongFormat.CCLI,
            SongFormat.DreamBeam,
            SongFormat.EasySlides,
            SongFormat.EasyWorship,
            SongFormat.FoilPresenter,
            SongFormat.MediaShout,
            SongFormat.OpenSong,
            SongFormat.PowerSong,
            SongFormat.SongBeamer,
            SongFormat.SongPro,
            SongFormat.SongShowPlus,
            SongFormat.SongsOfFellowship,
            SongFormat.SundayPlus,
            SongFormat.WordsOfWorship,
            SongFormat.WorshipCenterPro,
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
            return SongFormat.__attributes__.get(format)
        elif len(attributes) == 1:
            default = SongFormat.__defaults__.get(attributes[0])
            return SongFormat.__attributes__[format].get(attributes[0], default)
        else:
            values = []
            for attr in attributes:
                default = SongFormat.__defaults__.get(attr)
                values.append(SongFormat.__attributes__[format].get(attr, default))
            return tuple(values)

    @staticmethod
    def set(format, attribute, value):
        """
        Set specified song format attribute to the supplied value.
        """
        SongFormat.__attributes__[format][attribute] = value


SongFormat.set(SongFormat.SongsOfFellowship, 'availability', HAS_SOF)
if HAS_SOF:
    SongFormat.set(SongFormat.SongsOfFellowship, 'class', SofImport)
SongFormat.set(SongFormat.Generic, 'availability', HAS_OOO)
if HAS_OOO:
    SongFormat.set(SongFormat.Generic, 'class', OooImport)
SongFormat.set(SongFormat.MediaShout, 'availability', HAS_MEDIASHOUT)
if HAS_MEDIASHOUT:
    SongFormat.set(SongFormat.MediaShout, 'class', MediaShoutImport)
SongFormat.set(SongFormat.WorshipCenterPro, 'availability', HAS_WORSHIPCENTERPRO)
if HAS_WORSHIPCENTERPRO:
    SongFormat.set(SongFormat.WorshipCenterPro, 'class', WorshipCenterProImport)


__all__ = ['SongFormat', 'SongFormatSelect']
