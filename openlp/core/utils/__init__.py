# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

import os
import sys
import logging
import urllib2
from datetime import datetime

log = logging.getLogger(__name__)

class AppLocation(object):
    """
    Retrieve a directory based on the directory type.
    """
    AppDir = 1
    ConfigDir = 2
    DataDir = 3
    PluginsDir = 4

    @staticmethod
    def get_directory(dir_type):
        if dir_type == AppLocation.AppDir:
           return os.path.abspath(os.path.split(sys.argv[0])[0])
        elif dir_type == AppLocation.ConfigDir:
            if os.getenv(u'PORTABLE')  is not None:
              path = os.path.split(os.path.abspath(sys.argv[0]))[0]
              path = os.path.join(path, os.getenv(u'PORTABLE'))
            elif sys.platform == u'win32':
                path = os.path.join(os.getenv(u'APPDATA'), u'openlp')
            elif sys.platform == u'darwin':
                path = os.path.join(os.getenv(u'HOME'), u'Library',
                    u'Application Support', u'openlp')
            else:
                try:
                    from xdg import BaseDirectory
                    path = os.path.join(BaseDirectory.xdg_config_home, u'openlp')
                except ImportError:
                    path = os.path.join(os.getenv(u'HOME'), u'.openlp')
            return path
        elif dir_type == AppLocation.DataDir:
            if os.getenv(u'PORTABLE')  is not None:
                path = os.path.split(os.path.abspath(sys.argv[0]))[0]
                path = os.path.join(path, os.getenv(u'PORTABLE'),  u'data')
            elif sys.platform == u'win32':
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
            app_path = os.path.abspath(os.path.split(sys.argv[0])[0])
            if hasattr(sys, u'frozen') and sys.frozen == 1:
                return os.path.join(app_path, u'plugins')
            else:
                return os.path.join(app_path, u'openlp', u'plugins')


def check_latest_version(config, current_version):
    version_string = current_version
    #set to prod in the distribution confif file.
    last_test = config.get_config(u'last version test', datetime.now().date())
    this_test = unicode(datetime.now().date())
    config.set_config(u'last version test', this_test)
    if last_test != this_test:
        version_string = u''
        req = urllib2.Request(u'http://www.openlp.org/files/version.txt')
        req.add_header(u'User-Agent', u'OpenLP/%s' % current_version)
        try:
            handle = urllib2.urlopen(req, None)
            html = handle.read()
            version_string = unicode(html).rstrip()
        except IOError, e:
            if hasattr(e, u'reason'):
                log.exception(u'Reason for failure: %s', e.reason)
    return version_string

from registry import Registry
from confighelper import ConfigHelper

__all__ = [u'Registry', u'ConfigHelper', u'AppLocation', u'check_latest_version']
