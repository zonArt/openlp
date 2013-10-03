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
The :mod:`openlp.core.utils.applocation` module provides an utility for OpenLP receiving the data path etc.
"""
import logging
import os
import sys

from openlp.core.lib import Settings
from openlp.core.utils import _get_frozen_path


if sys.platform != 'win32' and sys.platform != 'darwin':
    try:
        from xdg import BaseDirectory
        XDG_BASE_AVAILABLE = True
    except ImportError:
        XDG_BASE_AVAILABLE = False

import openlp
from openlp.core.lib import check_directory_exists


log = logging.getLogger(__name__)


class AppLocation(object):
    """
    The :class:`AppLocation` class is a static class which retrieves a directory based on the directory type.
    """
    AppDir = 1
    DataDir = 2
    PluginsDir = 3
    VersionDir = 4
    CacheDir = 5
    LanguageDir = 6

    # Base path where data/config/cache dir is located
    BaseDir = None

    @staticmethod
    def get_directory(dir_type=AppDir):
        """
        Return the appropriate directory according to the directory type.

        ``dir_type``
            The directory type you want, for instance the data directory. Default *AppLocation.AppDir*
        """
        if dir_type == AppLocation.AppDir:
            return _get_frozen_path(os.path.abspath(os.path.split(sys.argv[0])[0]), os.path.split(openlp.__file__)[0])
        elif dir_type == AppLocation.PluginsDir:
            app_path = os.path.abspath(os.path.split(sys.argv[0])[0])
            return _get_frozen_path(os.path.join(app_path, 'plugins'),
                os.path.join(os.path.split(openlp.__file__)[0], 'plugins'))
        elif dir_type == AppLocation.VersionDir:
            return _get_frozen_path(os.path.abspath(os.path.split(sys.argv[0])[0]), os.path.split(openlp.__file__)[0])
        elif dir_type == AppLocation.LanguageDir:
            app_path = _get_frozen_path(os.path.abspath(os.path.split(sys.argv[0])[0]), _get_os_dir_path(dir_type))
            return os.path.join(app_path, 'i18n')
        elif dir_type == AppLocation.DataDir and AppLocation.BaseDir:
            return os.path.join(AppLocation.BaseDir, 'data')
        else:
            return _get_os_dir_path(dir_type)

    @staticmethod
    def get_data_path():
        """
        Return the path OpenLP stores all its data under.
        """
        # Check if we have a different data location.
        if Settings().contains('advanced/data path'):
            path = Settings().value('advanced/data path')
        else:
            path = AppLocation.get_directory(AppLocation.DataDir)
            check_directory_exists(path)
        return os.path.normpath(path)

    @staticmethod
    def get_files(section=None, extension=None):
        """
        Get a list of files from the data files path.

        ``section``
            Defaults to *None*. The section of code getting the files - used to load from a section's data subdirectory.

        ``extension``
            Defaults to *None*. The extension to search for. For example::

                u'.png'
        """
        path = AppLocation.get_data_path()
        if section:
            path = os.path.join(path, section)
        try:
            files = os.listdir(path)
        except OSError:
            return []
        if extension:
            return [filename for filename in files if extension == os.path.splitext(filename)[1]]
        else:
            # no filtering required
            return files

    @staticmethod
    def get_section_data_path(section):
        """
        Return the path a particular module stores its data under.
        """
        data_path = AppLocation.get_data_path()
        path = os.path.join(data_path, section)
        check_directory_exists(path)
        return path


def _get_os_dir_path(dir_type):
    """
    Return a path based on which OS and environment we are running in.
    """
    if sys.platform == 'win32':
        if dir_type == AppLocation.DataDir:
            return os.path.join(str(os.getenv('APPDATA')), 'openlp', 'data')
        elif dir_type == AppLocation.LanguageDir:
            return os.path.split(openlp.__file__)[0]
        return os.path.join(str(os.getenv('APPDATA')), 'openlp')
    elif sys.platform == 'darwin':
        if dir_type == AppLocation.DataDir:
            return os.path.join(str(os.getenv('HOME')),
                                'Library', 'Application Support', 'openlp', 'Data')
        elif dir_type == AppLocation.LanguageDir:
            return os.path.split(openlp.__file__)[0]
        return os.path.join(str(os.getenv('HOME')), 'Library', 'Application Support', 'openlp')
    else:
        if dir_type == AppLocation.LanguageDir:
            for prefix in ['/usr/local', '/usr']:
                directory = os.path.join(prefix, 'share', 'openlp')
                if os.path.exists(directory):
                    return directory
            return os.path.join('/usr', 'share', 'openlp')
        if XDG_BASE_AVAILABLE:
            if dir_type == AppLocation.DataDir:
                return os.path.join(str(BaseDirectory.xdg_data_home), 'openlp')
            elif dir_type == AppLocation.CacheDir:
                return os.path.join(str(BaseDirectory.xdg_cache_home), 'openlp')
        if dir_type == AppLocation.DataDir:
            return os.path.join(str(os.getenv('HOME')), '.openlp', 'data')
        return os.path.join(str(os.getenv('HOME')), '.openlp')

