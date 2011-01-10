# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

import logging
import os
import re
import sys
import time
import urllib2
from datetime import datetime

from PyQt4 import QtGui, QtCore

import openlp
from openlp.core.lib import Receiver, translate

log = logging.getLogger(__name__)
images_filter = None

class VersionThread(QtCore.QThread):
    """
    A special Qt thread class to fetch the version of OpenLP from the website.
    This is threaded so that it doesn't affect the loading time of OpenLP.
    """
    def __init__(self, parent, app_version):
        QtCore.QThread.__init__(self, parent)
        self.app_version = app_version
        self.version_splitter = re.compile(
            r'([0-9]+).([0-9]+).([0-9]+)(?:-bzr([0-9]+))?')

    def run(self):
        """
        Run the thread.
        """
        time.sleep(1)
        Receiver.send_message(u'maindisplay_blank_check')
        version = check_latest_version(self.app_version)
        remote_version = {}
        local_version = {}
        match = self.version_splitter.match(version)
        if match:
            remote_version[u'major'] = int(match.group(1))
            remote_version[u'minor'] = int(match.group(2))
            remote_version[u'release'] = int(match.group(3))
            if len(match.groups()) > 3 and match.group(4):
                remote_version[u'revision'] = int(match.group(4))
        else:
            return
        match = self.version_splitter.match(self.app_version[u'full'])
        if match:
            local_version[u'major'] = int(match.group(1))
            local_version[u'minor'] = int(match.group(2))
            local_version[u'release'] = int(match.group(3))
            if len(match.groups()) > 3 and match.group(4):
                local_version[u'revision'] = int(match.group(4))
        else:
            return
        if remote_version[u'major'] > local_version[u'major'] or \
            remote_version[u'minor'] > local_version[u'minor'] or \
            remote_version[u'release'] > local_version[u'release']:
            Receiver.send_message(u'openlp_version_check', u'%s' % version)
        elif remote_version.get(u'revision') and \
            local_version.get(u'revision') and \
            remote_version[u'revision'] > local_version[u'revision']:
            Receiver.send_message(u'openlp_version_check', u'%s' % version)


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
    LanguageDir = 7

    @staticmethod
    def get_directory(dir_type=1):
        """
        Return the appropriate directory according to the directory type.

        ``dir_type``
            The directory type you want, for instance the data directory.
        """
        if dir_type == AppLocation.AppDir:
            if hasattr(sys, u'frozen') and sys.frozen == 1:
                app_path = os.path.abspath(os.path.split(sys.argv[0])[0])
            else:
                app_path = os.path.split(openlp.__file__)[0]
            return app_path
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
                version_path = os.path.abspath(os.path.split(sys.argv[0])[0])
            else:
                version_path = os.path.split(openlp.__file__)[0]
            return version_path
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
        if dir_type == AppLocation.LanguageDir:
            if hasattr(sys, u'frozen') and sys.frozen == 1:
                app_path = os.path.abspath(os.path.split(sys.argv[0])[0])
            else:
                app_path = os.path.split(openlp.__file__)[0]
            return os.path.join(app_path, u'i18n')


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
        remote_version = None
        try:
            remote_version = unicode(urllib2.urlopen(req, None).read()).strip()
        except IOError, e:
            if hasattr(e, u'reason'):
                log.exception(u'Reason for failure: %s', e.reason)
        if remote_version:
            version_string = remote_version
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

def split_filename(path):
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        return path, u''
    else:
        return os.path.split(path)

def get_web_page(url, update_openlp=False):
    """
    Attempts to download the webpage at url and returns that page or None.

    ``url``
        The URL to be downloaded.

    ``update_openlp``
        Tells OpenLP to update itself if the page is successfully downloaded.
        Defaults to False.
    """
    # TODO: Add proxy usage.  Get proxy info from OpenLP settings, add to a
    # proxy_handler, build into an opener and install the opener into urllib2.
    # http://docs.python.org/library/urllib2.html
    if not url:
        return None
    page = None
    log.debug(u'Downloading URL = %s' % url)
    try:
        page = urllib2.urlopen(url)
        log.debug(u'Downloaded URL = %s' % page.geturl())
    except urllib2.URLError:
        log.exception(u'The web page could not be downloaded')
    if not page:
        return None
    if update_openlp:
        Receiver.send_message(u'openlp_process_events')
    return page

from languagemanager import LanguageManager
from actions import ActionList

__all__ = [u'AppLocation', u'check_latest_version', u'add_actions',
    u'get_filesystem_encoding', u'LanguageManager', u'ActionList',
    u'get_web_page']
