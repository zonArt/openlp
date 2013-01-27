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
from songproimport import SongProImport
from sundayplusimport import SundayPlusImport
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
HAS_MEDIASHOUT = False
if os.name == u'nt':
    try:
        from mediashoutimport import MediaShoutImport
        HAS_MEDIASHOUT = True
    except ImportError:
        log.exception('Error importing %s', 'MediaShoutImport')


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
    #   order used by formatComboBox.
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
    MediaShout = 9
    OpenSong = 10
    PowerSong = 11
    SongBeamer = 12
    SongPro = 13
    SongShowPlus = 14
    SongsOfFellowship = 15
    SundayPlus = 16
    WordsOfWorship = 17
    ZionWorx = 18

    # Set optional attribute defaults
    __defaults__ = {
        u'canDisable': False,
        u'availability': True,
        u'selectMode': SongFormatSelect.MultipleFiles,
        u'filter': u'',
        u'comboBoxText': None,
        u'disabledLabelText': translate('SongsPlugin.ImportWizardForm', 'This importer has been disabled.'),
        u'getFilesTitle': None,
        u'invalidSourceMsg': None,
        u'descriptionText': None
    }

    # Set attribute values for each Song Format
    __attributes__ = {
        OpenLyrics: {
            u'class': OpenLyricsImport,
            u'name': u'OpenLyrics',
            u'prefix': u'openLyrics',
            u'filter': u'%s (*.xml)' % translate('SongsPlugin.ImportWizardForm', 'OpenLyrics Files'),
            u'comboBoxText': translate('SongsPlugin.ImportWizardForm', 'OpenLyrics or OpenLP 2.0 Exported Song')
        },
        OpenLP2: {
            u'class': OpenLPSongImport,
            u'name': UiStrings().OLPV2,
            u'prefix': u'openLP2',
            u'selectMode': SongFormatSelect.SingleFile,
            u'filter': u'%s (*.sqlite)' % (translate('SongsPlugin.ImportWizardForm', 'OpenLP 2.0 Databases'))
        },
        OpenLP1: {
            u'name': UiStrings().OLPV1,
            u'prefix': u'openLP1',
            u'canDisable': True,
            u'selectMode': SongFormatSelect.SingleFile,
            u'filter': u'%s (*.olp)' % translate('SongsPlugin.ImportWizardForm', 'openlp.org v1.x Databases'),
            u'disabledLabelText': WizardStrings.NoSqlite
        },
        Generic: {
            u'name': translate('SongsPlugin.ImportWizardForm', 'Generic Document/Presentation'),
            u'prefix': u'generic',
            u'canDisable': True,
            u'disabledLabelText': translate('SongsPlugin.ImportWizardForm',
                'The generic document/presentation importer has been disabled '
                'because OpenLP cannot access OpenOffice or LibreOffice.'),
            u'getFilesTitle': translate('SongsPlugin.ImportWizardForm', 'Select Document/Presentation Files')
        },
        CCLI: {
            u'class': CCLIFileImport,
            u'name': u'CCLI/SongSelect',
            u'prefix': u'ccli',
            u'filter': u'%s (*.usr *.txt)' % translate('SongsPlugin.ImportWizardForm', 'CCLI SongSelect Files')
        },
        DreamBeam: {
            u'class': DreamBeamImport,
            u'name': u'DreamBeam',
            u'prefix': u'dreamBeam',
            u'filter': u'%s (*.xml)' % translate('SongsPlugin.ImportWizardForm', 'DreamBeam Song Files')
        },
        EasySlides: {
            u'class': EasySlidesImport,
            u'name': u'EasySlides',
            u'prefix': u'easySlides',
            u'selectMode': SongFormatSelect.SingleFile,
            u'filter': u'%s (*.xml)' % translate('SongsPlugin.ImportWizardForm', 'EasySlides XML File')
        },
        EasyWorship: {
            u'class': EasyWorshipSongImport,
            u'name': u'EasyWorship',
            u'prefix': u'ew',
            u'selectMode': SongFormatSelect.SingleFile,
            u'filter': u'%s (*.db)' % translate('SongsPlugin.ImportWizardForm', 'EasyWorship Song Database')
        },
        FoilPresenter: {
            u'class': FoilPresenterImport,
            u'name': u'Foilpresenter',
            u'prefix': u'foilPresenter',
            u'filter': u'%s (*.foil)' % translate('SongsPlugin.ImportWizardForm', 'Foilpresenter Song Files')
        },
        MediaShout: {
            u'name': u'MediaShout',
            u'prefix': u'mediaShout',
            u'canDisable': True,
            u'selectMode': SongFormatSelect.SingleFile,
            u'filter': u'%s (*.mdb)' % translate('SongsPlugin.ImportWizardForm',
                'MediaShout Database'),
            u'disabledLabelText': translate('SongsPlugin.ImportWizardForm',
                'The MediaShout importer is only supported on Windows. It has '
                'been disabled due to a missing Python module. If you want to '
                'use this importer, you will need to install the "pyodbc" '
                'module.')
        },
        OpenSong: {
            u'class': OpenSongImport,
            u'name': WizardStrings.OS,
            u'prefix': u'openSong'
        },
        PowerSong: {
            u'class': PowerSongImport,
            u'name': u'PowerSong 1.0',
            u'prefix': u'powerSong',
            u'selectMode': SongFormatSelect.SingleFolder,
            u'invalidSourceMsg': translate('SongsPlugin.ImportWizardForm',
                'You need to specify a valid PowerSong 1.0 database folder.')
        },
        SongBeamer: {
            u'class': SongBeamerImport,
            u'name': u'SongBeamer',
            u'prefix': u'songBeamer',
            u'filter': u'%s (*.sng)' % translate('SongsPlugin.ImportWizardForm',
                'SongBeamer Files')
        },
        SongPro: {
            u'class': SongProImport,
            u'name': u'SongPro',
            u'prefix': u'songPro',
            u'selectMode': SongFormatSelect.SingleFile,
            u'filter': u'%s (*.txt)' % translate('SongsPlugin.ImportWizardForm', 'SongPro Text Files'),
            u'comboBoxText': translate('SongsPlugin.ImportWizardForm', 'SongPro (Export File)'),
            u'descriptionText': translate('SongsPlugin.ImportWizardForm',
                'In SongPro, export your songs using the File -> Export menu')
        },
        SongShowPlus: {
            u'class': SongShowPlusImport,
            u'name': u'SongShow Plus',
            u'prefix': u'songShowPlus',
            u'filter': u'%s (*.sbsong)' % translate('SongsPlugin.ImportWizardForm', 'SongShow Plus Song Files')
        },
        SongsOfFellowship: {
            u'name': u'Songs of Fellowship',
            u'prefix': u'songsOfFellowship',
            u'canDisable': True,
            u'filter': u'%s (*.rtf)' % translate('SongsPlugin.ImportWizardForm', 'Songs Of Fellowship Song Files'),
            u'disabledLabelText': translate('SongsPlugin.ImportWizardForm',
                'The Songs of Fellowship importer has been disabled because '
                'OpenLP cannot access OpenOffice or LibreOffice.')
        },
        SundayPlus: {
            u'class': SundayPlusImport,
            u'name': u'SundayPlus',
            u'prefix': u'sundayPlus',
            u'filter': u'%s (*.ptf)' % translate('SongsPlugin.ImportWizardForm', 'SundayPlus Song Files')
        },
        WordsOfWorship: {
            u'class': WowImport,
            u'name': u'Words of Worship',
            u'prefix': u'wordsOfWorship',
            u'filter': u'%s (*.wsg *.wow-song)' %
                translate('SongsPlugin.ImportWizardForm', 'Words Of Worship Song Files')
        },
        ZionWorx: {
            u'class': ZionWorxImport,
            u'name': u'ZionWorx',
            u'prefix': u'zionWorx',
            u'selectMode': SongFormatSelect.SingleFile,
            u'comboBoxText': translate('SongsPlugin.ImportWizardForm', 'ZionWorx (CSV)'),
            u'descriptionText': translate('SongsPlugin.ImportWizardForm',
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
            SongFormat.OpenLP1,
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

SongFormat.set(SongFormat.OpenLP1, u'availability', HAS_OPENLP1)
if HAS_OPENLP1:
    SongFormat.set(SongFormat.OpenLP1, u'class', OpenLP1SongImport)
SongFormat.set(SongFormat.SongsOfFellowship, u'availability', HAS_SOF)
if HAS_SOF:
    SongFormat.set(SongFormat.SongsOfFellowship, u'class', SofImport)
SongFormat.set(SongFormat.Generic, u'availability', HAS_OOO)
if HAS_OOO:
    SongFormat.set(SongFormat.Generic, u'class', OooImport)
SongFormat.set(SongFormat.MediaShout, u'availability', HAS_MEDIASHOUT)
if HAS_MEDIASHOUT:
    SongFormat.set(SongFormat.MediaShout, u'class', MediaShoutImport)

__all__ = [u'SongFormat', u'SongFormatSelect']
