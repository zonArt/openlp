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
The :mod:`openlp.core.utils` module provides the utility libraries for OpenLP.
"""
from datetime import datetime
from distutils.version import LooseVersion
import logging
import locale
import os
import re
from subprocess import Popen, PIPE
import sys
import urllib.request, urllib.error, urllib.parse

from PyQt4 import QtGui, QtCore

from openlp.core.lib import Registry, Settings


if sys.platform != 'win32' and sys.platform != 'darwin':
    try:
        from xdg import BaseDirectory
        XDG_BASE_AVAILABLE = True
    except ImportError:
        XDG_BASE_AVAILABLE = False

from openlp.core.lib import translate

log = logging.getLogger(__name__)
APPLICATION_VERSION = {}
IMAGES_FILTER = None
ICU_COLLATOR = None
UNO_CONNECTION_TYPE = 'pipe'
#UNO_CONNECTION_TYPE = u'socket'
CONTROL_CHARS = re.compile(r'[\x00-\x1F\x7F-\x9F]', re.UNICODE)
INVALID_FILE_CHARS = re.compile(r'[\\/:\*\?"<>\|\+\[\]%]', re.UNICODE)
DIGITS_OR_NONDIGITS = re.compile(r'\d+|\D+', re.UNICODE)


class VersionThread(QtCore.QThread):
    """
    A special Qt thread class to fetch the version of OpenLP from the website.
    This is threaded so that it doesn't affect the loading time of OpenLP.
    """
    def run(self):
        """
        Run the thread.
        """
        self.sleep(1)
        log.debug('Version thread - run')
        app_version = get_application_version()
        version = check_latest_version(app_version)
        if LooseVersion(str(version)) > LooseVersion(str(app_version['full'])):
            Registry().execute('openlp_version_check', '%s' % version)


def _get_frozen_path(frozen_option, non_frozen_option):
    """
    Return a path based on the system status.
    """
    if hasattr(sys, 'frozen') and sys.frozen == 1:
        return frozen_option
    return non_frozen_option


def get_application_version():
    """
    Returns the application version of the running instance of OpenLP::

        {u'full': u'1.9.4-bzr1249', u'version': u'1.9.4', u'build': u'bzr1249'}
    """
    global APPLICATION_VERSION
    if APPLICATION_VERSION:
        return APPLICATION_VERSION
    if '--dev-version' in sys.argv or '-d' in sys.argv:
        # NOTE: The following code is a duplicate of the code in setup.py. Any fix applied here should also be applied
        # there.

        # Get the revision of this tree.
        bzr = Popen(('bzr', 'revno'), stdout=PIPE)
        tree_revision, error = bzr.communicate()
        tree_revision = tree_revision.decode()
        code = bzr.wait()
        if code != 0:
            raise Exception('Error running bzr log')

        # Get all tags.
        bzr = Popen(('bzr', 'tags'), stdout=PIPE)
        output, error = bzr.communicate()
        code = bzr.wait()
        if code != 0:
            raise Exception('Error running bzr tags')
        tags = list(map(bytes.decode, output.splitlines()))
        if not tags:
            tag_version = '0.0.0'
            tag_revision = '0'
        else:
            # Remove any tag that has "?" as revision number. A "?" as revision number indicates, that this tag is from
            # another series.
            tags = [tag for tag in tags if tag.split()[-1].strip() != '?']
            # Get the last tag and split it in a revision and tag name.
            tag_version, tag_revision = tags[-1].split()
        # If they are equal, then this tree is tarball with the source for the release. We do not want the revision
        # number in the full version.
        if tree_revision == tag_revision:
            full_version =  tag_version
        else:
            full_version =  '%s-bzr%s' % (tag_version, tree_revision)
    else:
        # We're not running the development version, let's use the file.
        filepath = AppLocation.get_directory(AppLocation.VersionDir)
        filepath = os.path.join(filepath, '.version')
        fversion = None
        try:
            fversion = open(filepath, 'r')
            full_version = str(fversion.read()).rstrip()
        except IOError:
            log.exception('Error in version file.')
            full_version = '0.0.0-bzr000'
        finally:
            if fversion:
                fversion.close()
    bits = full_version.split('-')
    APPLICATION_VERSION = {
        'full': full_version,
        'version': bits[0],
        'build': bits[1] if len(bits) > 1 else None
    }
    if APPLICATION_VERSION['build']:
        log.info('Openlp version %s build %s', APPLICATION_VERSION['version'], APPLICATION_VERSION['build'])
    else:
        log.info('Openlp version %s' % APPLICATION_VERSION['version'])
    return APPLICATION_VERSION


def check_latest_version(current_version):
    """
    Check the latest version of OpenLP against the version file on the OpenLP
    site.

    ``current_version``
        The current version of OpenLP.

    **Rules around versions and version files:**

    * If a version number has a build (i.e. -bzr1234), then it is a nightly.
    * If a version number's minor version is an odd number, it is a development release.
    * If a version number's minor version is an even number, it is a stable release.
    """
    version_string = current_version['full']
    # set to prod in the distribution config file.
    settings = Settings()
    settings.beginGroup('core')
    last_test = settings.value('last version test')
    this_test = str(datetime.now().date())
    settings.setValue('last version test', this_test)
    settings.endGroup()
    # Tell the main window whether there will ever be data to display
    Registry().get('main_window').version_update_running = last_test != this_test
    if last_test != this_test:
        if current_version['build']:
            req = urllib.request.Request('http://www.openlp.org/files/nightly_version.txt')
        else:
            version_parts = current_version['version'].split('.')
            if int(version_parts[1]) % 2 != 0:
                req = urllib.request.Request('http://www.openlp.org/files/dev_version.txt')
            else:
                req = urllib.request.Request('http://www.openlp.org/files/version.txt')
        req.add_header('User-Agent', 'OpenLP/%s' % current_version['full'])
        remote_version = None
        try:
            remote_version = str(urllib.request.urlopen(req, None).read().decode()).strip()
        except IOError:
            log.exception('Failed to download the latest OpenLP version file')
        if remote_version:
            version_string = remote_version
    return version_string


def add_actions(target, actions):
    """
    Adds multiple actions to a menu or toolbar in one command.

    ``target``
        The menu or toolbar to add actions to.

    ``actions``
        The actions to be added. An action consisting of the keyword ``None``
        will result in a separator being inserted into the target.
    """
    for action in actions:
        if action is None:
            target.addSeparator()
        else:
            target.addAction(action)


def get_filesystem_encoding():
    """
    Returns the name of the encoding used to convert Unicode filenames into system file names.
    """
    encoding = sys.getfilesystemencoding()
    if encoding is None:
        encoding = sys.getdefaultencoding()
    return encoding


def get_images_filter():
    """
    Returns a filter string for a file dialog containing all the supported image formats.
    """
    global IMAGES_FILTER
    if not IMAGES_FILTER:
        log.debug('Generating images filter.')
        formats = list(map(bytes.decode, list(map(bytes, QtGui.QImageReader.supportedImageFormats()))))
        visible_formats = '(*.%s)' % '; *.'.join(formats)
        actual_formats = '(*.%s)' % ' *.'.join(formats)
        IMAGES_FILTER = '%s %s %s' % (translate('OpenLP', 'Image Files'), visible_formats, actual_formats)
    return IMAGES_FILTER


def is_not_image_file(file_name):
    """
    Validate that the file is not an image file.

    ``file_name``
        File name to be checked.
    """
    if not file_name:
        return True
    else:
        formats = [bytes(fmt).decode().lower() for fmt in QtGui.QImageReader.supportedImageFormats()]
        file_part, file_extension = os.path.splitext(str(file_name))
        if file_extension[1:].lower() in formats and os.path.exists(file_name):
            return False
        return True


def split_filename(path):
    """
    Return a list of the parts in a given path.
    """
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        return path, ''
    else:
        return os.path.split(path)


def clean_filename(filename):
    """
    Removes invalid characters from the given ``filename``.

    ``filename``
        The "dirty" file name to clean.
    """
    if not isinstance(filename, str):
        filename = str(filename, 'utf-8')
    return INVALID_FILE_CHARS.sub('_', CONTROL_CHARS.sub('', filename))


def delete_file(file_path_name):
    """
    Deletes a file from the system.

    ``file_path_name``
        The file, including path, to delete.
    """
    if not file_path_name:
        return False
    try:
        if os.path.exists(file_path_name):
            os.remove(file_path_name)
        return True
    except (IOError, OSError):
        log.exception("Unable to delete file %s" % file_path_name)
        return False


def get_web_page(url, header=None, update_openlp=False):
    """
    Attempts to download the webpage at url and returns that page or None.

    ``url``
        The URL to be downloaded.

    ``header``
        An optional HTTP header to pass in the request to the web server.

    ``update_openlp``
        Tells OpenLP to update itself if the page is successfully downloaded.
        Defaults to False.
    """
    # TODO: Add proxy usage. Get proxy info from OpenLP settings, add to a
    # proxy_handler, build into an opener and install the opener into urllib2.
    # http://docs.python.org/library/urllib2.html
    if not url:
        return None
    req = urllib.request.Request(url)
    if header:
        req.add_header(header[0], header[1])
    page = None
    log.debug('Downloading URL = %s' % url)
    try:
        page = urllib.request.urlopen(req)
        log.debug('Downloaded URL = %s' % page.geturl())
    except urllib.error.URLError:
        log.exception('The web page could not be downloaded')
    if not page:
        return None
    if update_openlp:
        Registry().get('application').process_events()
    log.debug(page)
    return page


def get_uno_command():
    """
    Returns the UNO command to launch an openoffice.org instance.
    """
    COMMAND = 'soffice'
    OPTIONS = '--nologo --norestore --minimized --nodefault --nofirststartwizard'
    if UNO_CONNECTION_TYPE == 'pipe':
        CONNECTION = '"--accept=pipe,name=openlp_pipe;urp;"'
    else:
        CONNECTION = '"--accept=socket,host=localhost,port=2002;urp;"'
    return '%s %s %s' % (COMMAND, OPTIONS, CONNECTION)


def get_uno_instance(resolver):
    """
    Returns a running openoffice.org instance.

    ``resolver``
        The UNO resolver to use to find a running instance.
    """
    log.debug('get UNO Desktop Openoffice - resolve')
    if UNO_CONNECTION_TYPE == 'pipe':
        return resolver.resolve('uno:pipe,name=openlp_pipe;urp;StarOffice.ComponentContext')
    else:
        return resolver.resolve('uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext')


def format_time(text, local_time):
    """
    Workaround for Python built-in time formatting function time.strftime().

    time.strftime() accepts only ascii characters. This function accepts
    unicode string and passes individual % placeholders to time.strftime().
    This ensures only ascii characters are passed to time.strftime().

    ``text``
        The text to be processed.

    ``local_time``
        The time to be used to add to the string.  This is a time object
    """
    def match_formatting(match):
        """
        Format the match
        """
        return local_time.strftime(match.group())
    return re.sub('\%[a-zA-Z]', match_formatting, text)


def get_locale_key(string):
    """
    Creates a key for case insensitive, locale aware string sorting.

    ``string``
        The corresponding string.
    """
    string = string.lower()
    # For Python 3 on platforms other than Windows ICU is not necessary. In those cases locale.strxfrm(str) can be used.
    if os.name == 'nt':
        global ICU_COLLATOR
        if ICU_COLLATOR is None:
            import icu
            from .languagemanager import LanguageManager
            language = LanguageManager.get_language()
            icu_locale = icu.Locale(language)
            ICU_COLLATOR = icu.Collator.createInstance(icu_locale)
        return ICU_COLLATOR.getSortKey(string)
    return locale.strxfrm(string).encode()


def get_natural_key(string):
    """
    Generate a key for locale aware natural string sorting.
    Returns a list of string compare keys and integers.
    """
    key = DIGITS_OR_NONDIGITS.findall(string)
    key = [int(part) if part.isdigit() else get_locale_key(part) for part in key]
    # Python 3 does not support comparision of different types anymore. So make sure, that we do not compare str
    # and int.
    if string[0].isdigit():
        return [b''] + key
    return key


from .applocation import AppLocation
from .languagemanager import LanguageManager
from .actions import ActionList


__all__ = ['AppLocation', 'ActionList', 'LanguageManager', 'get_application_version', 'check_latest_version',
    'add_actions', 'get_filesystem_encoding', 'get_web_page', 'get_uno_command', 'get_uno_instance',
    'delete_file', 'clean_filename', 'format_time', 'get_locale_key', 'get_natural_key']
