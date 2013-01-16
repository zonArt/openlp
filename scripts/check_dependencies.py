#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

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
This script is used to check dependencies of OpenLP. It checks availability
of required python modules and their version. To verify availability of Python
modules, simply run this script::

    @:~$ ./check_dependencies.py

"""
import os
import sys
from distutils.version import LooseVersion

is_win = sys.platform.startswith('win')

VERS = {
    'Python': '2.6',
    'PyQt4': '4.6',
    'Qt4': '4.6',
    'sqlalchemy': '0.5',
    # pyenchant 1.6 required on Windows
    'enchant': '1.6' if is_win else '1.3'
}

# pywin32
WIN32_MODULES = [
    'win32com',
    'win32ui',
    'pywintypes',
]

MODULES = [
    'PyQt4',
    'PyQt4.QtCore',
    'PyQt4.QtGui',
    'PyQt4.QtNetwork',
    'PyQt4.QtOpenGL',
    'PyQt4.QtSvg',
    'PyQt4.QtTest',
    'PyQt4.QtWebKit',
    'PyQt4.phonon',
    'sqlalchemy',
    'sqlite3',
    'lxml',
    'chardet',
    'enchant',
    'BeautifulSoup',
    'mako',
    'migrate',
    'uno',
]


OPTIONAL_MODULES = [
    ('sqlite', ' (SQLite 2 support)'),
    ('MySQLdb', ' (MySQL support)'),
    ('psycopg2', ' (PostgreSQL support)'),
    ('pytest', ' (testing framework)'),
]

w = sys.stdout.write

def check_vers(version, required, text):
    if type(version) is not str:
        version = '.'.join(map(str, version))
    if type(required) is not str:
        required = '.'.join(map(str, required))
    w('  %s >= %s ...    ' % (text, required))
    if LooseVersion(version) >= LooseVersion(required):
        w(version + os.linesep)
        return True
    else:
        w('FAIL' + os.linesep)
        return False

def print_vers_fail(required, text):
    print('  %s >= %s ...    FAIL' % (text, required))

def verify_python():
    if not check_vers(list(sys.version_info), VERS['Python'], text='Python'):
        exit(1)

def verify_versions():
    print('Verifying version of modules...')
    try:
        from PyQt4 import QtCore
        check_vers(QtCore.PYQT_VERSION_STR, VERS['PyQt4'], 'PyQt4')
        check_vers(QtCore.qVersion(), VERS['Qt4'], 'Qt4')
    except ImportError:
        print_vers_fail(VERS['PyQt4'], 'PyQt4')
        print_vers_fail(VERS['Qt4'], 'Qt4')
    try:
        import sqlalchemy
        check_vers(sqlalchemy.__version__, VERS['sqlalchemy'], 'sqlalchemy')
    except ImportError:
        print_vers_fail(VERS['sqlalchemy'], 'sqlalchemy')
    try:
        import enchant
        check_vers(enchant.__version__, VERS['enchant'], 'enchant')
    except ImportError:
        print_vers_fail(VERS['enchant'], 'enchant')

def check_module(mod, text='', indent='  '):
    space = (30 - len(mod) - len(text)) * ' '
    w(indent + '%s%s...  ' % (mod, text) + space)
    try:
        __import__(mod)
        w('OK')
    except ImportError:
        w('FAIL')
    w(os.linesep)

def verify_pyenchant():
    w('Enchant (spell checker)... ')
    try:
        import enchant
        w(os.linesep)
        backends = ', '.join([x.name for x in enchant.Broker().describe()])
        print('  available backends: %s' % backends)
        langs = ', '.join(enchant.list_languages())
        print('  available languages: %s' % langs)
    except ImportError:
        w('FAIL' + os.linesep)

def verify_pyqt():
    w('Qt4 image formats... ')
    try:
        from PyQt4 import QtGui
        read_f = ', '.join([unicode(format).lower()
           for format in QtGui.QImageReader.supportedImageFormats()])
        write_f = ', '.join([unicode(format).lower()
            for format in QtGui.QImageWriter.supportedImageFormats()])
        w(os.linesep)
        print('  read: %s' % read_f)
        print('  write: %s' % write_f)
    except ImportError:
        w('FAIL' + os.linesep)

def main():
    verify_python()

    print('Checking for modules...')
    for m in MODULES:
        check_module(m)

    print('Checking for optional modules...')
    for m in OPTIONAL_MODULES:
        check_module(m[0], text=m[1])

    if is_win:
        print('Checking for Windows specific modules...')
        for m in WIN32_MODULES:
            check_module(m)

    verify_versions()
    verify_pyqt()
    verify_pyenchant()

if __name__ == u'__main__':
    main()
