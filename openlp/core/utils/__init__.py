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
"""
The :mod:`utils` module provides the utility libraries for OpenLP
"""

import os
import sys
import logging
import urllib2
from datetime import datetime

from PyQt4 import QtGui, QtCore

import openlp
from openlp.core.lib import translate

log = logging.getLogger(__name__)
images_filter = None

class AppLocation(object):
    """
    The :class:`AppLocation` class is a static class which retrieves a
    directory based on the directory type.
    """
    AppDir = 1
    ConfigDir = 2
    DataDir = 3
    PluginsDir = 4
    VersionDir = 5
    CacheDir = 6

    @staticmethod
    def get_directory(dir_type=1):
        """
        Return the appropriate directory according to the directory type.

        ``dir_type``
            The directory type you want, for instance the data directory.
        """
        if dir_type == AppLocation.AppDir:
            return os.path.abspath(os.path.split(sys.argv[0])[0])
        elif dir_type == AppLocation.ConfigDir:
            if sys.platform == u'win32':
                path = os.path.join(os.getenv(u'APPDATA'), u'openlp')
            elif sys.platform == u'darwin':
                path = os.path.join(os.getenv(u'HOME'), u'Library',
                    u'Application Support', u'openlp')
            else:
                try:
                    from xdg import BaseDirectory
                    path = os.path.join(
                        BaseDirectory.xdg_config_home, u'openlp')
                except ImportError:
                    path = os.path.join(os.getenv(u'HOME'), u'.openlp')
            return path
        elif dir_type == AppLocation.DataDir:
            if sys.platform == u'win32':
                path = os.path.join(os.getenv(u'APPDATA'), u'openlp', u'data')
            elif sys.platform == u'darwin':
                path = os.path.join(os.getenv(u'HOME'), u'Library',
                    u'Application Support', u'openlp', u'Data')
            else:
                try:
                    from xdg import BaseDirectory
                    path = os.path.join(BaseDirectory.xdg_data_home, u'openlp')
                except ImportError:
                    path = os.path.join(os.getenv(u'HOME'), u'.openlp', u'data')
            return path
        elif dir_type == AppLocation.PluginsDir:
            plugin_path = None
            app_path = os.path.abspath(os.path.split(sys.argv[0])[0])
            if hasattr(sys, u'frozen') and sys.frozen == 1:
                plugin_path = os.path.join(app_path, u'plugins')
            else:
                plugin_path = os.path.join(
                    os.path.split(openlp.__file__)[0], u'plugins')
            return plugin_path
        elif dir_type == AppLocation.VersionDir:
            if hasattr(sys, u'frozen') and sys.frozen == 1:
                plugin_path = os.path.abspath(os.path.split(sys.argv[0])[0])
            else:
                plugin_path = os.path.split(openlp.__file__)[0]
            return plugin_path
        elif dir_type == AppLocation.CacheDir:
            if sys.platform == u'win32':
                path = os.path.join(os.getenv(u'APPDATA'), u'openlp')
            elif sys.platform == u'darwin':
                path = os.path.join(os.getenv(u'HOME'), u'Library',
                    u'Application Support', u'openlp')
            else:
                try:
                    from xdg import BaseDirectory
                    path = os.path.join(
                        BaseDirectory.xdg_cache_home, u'openlp')
                except ImportError:
                    path = os.path.join(os.getenv(u'HOME'), u'.openlp')
            return path

    @staticmethod
    def get_data_path():
        path = AppLocation.get_directory(AppLocation.DataDir)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def get_section_data_path(section):
        data_path = AppLocation.get_data_path()
        path = os.path.join(data_path, section)
        if not os.path.exists(path):
            os.makedirs(path)
        return path


def check_latest_version(current_version):
    """
    Check the latest version of OpenLP against the version file on the OpenLP
    site.

    ``current_version``
        The current version of OpenLP.
    """
    version_string = current_version[u'full']
    #set to prod in the distribution config file.
    settings = QtCore.QSettings()
    settings.beginGroup(u'general')
    last_test = unicode(settings.value(u'last version test',
        QtCore.QVariant(datetime.now().date())).toString())
    this_test = unicode(datetime.now().date())
    settings.setValue(u'last version test', QtCore.QVariant(this_test))
    settings.endGroup()
    if last_test != this_test:
        if current_version[u'build']:
            req = urllib2.Request(
                u'http://www.openlp.org/files/dev_version.txt')
        else:
            req = urllib2.Request(u'http://www.openlp.org/files/version.txt')
        req.add_header(u'User-Agent', u'OpenLP/%s' % current_version[u'full'])
        try:
            version_string = unicode(urllib2.urlopen(req, None).read()).strip()
        except IOError, e:
            if hasattr(e, u'reason'):
                log.exception(u'Reason for failure: %s', e.reason)
    return version_string

def add_actions(target, actions):
    """
    Adds multiple actions to a menu or toolbar in one command.

    ``target``
        The menu or toolbar to add actions to.

    ``actions``
        The actions to be added.  An action consisting of the keyword 'None'
        will result in a separator being inserted into the target.
    """
    for action in actions:
        if action is None:
            target.addSeparator()
        else:
            target.addAction(action)

def get_filesystem_encoding():
    """
    Returns the name of the encoding used to convert Unicode filenames into
    system file names.
    """
    encoding = sys.getfilesystemencoding()
    if encoding is None:
        encoding = sys.getdefaultencoding()
    return encoding

def get_images_filter():
    """
    Returns a filter string for a file dialog containing all the supported
    image formats.
    """
    global images_filter
    if not images_filter:
        log.debug(u'Generating images filter.')
        formats = [unicode(fmt)
            for fmt in QtGui.QImageReader.supportedImageFormats()]
        visible_formats = u'(*.%s)' % u'; *.'.join(formats)
        actual_formats = u'(*.%s)' % u' *.'.join(formats)
        images_filter = u'%s %s %s' % (translate('OpenLP', 'Image Files'),
            visible_formats, actual_formats)
    return images_filter

from languagemanager import LanguageManager

__all__ = [u'AppLocation', u'check_latest_version', u'add_actions',
    u'get_filesystem_encoding', u'LanguageManager']
