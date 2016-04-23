# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
The :mod:`common` module contains most of the components and libraries that make
OpenLP work.
"""
import hashlib
import logging
import os
import re
import sys
import traceback
from ipaddress import IPv4Address, IPv6Address, AddressValueError
from shutil import which

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QCryptographicHash as QHash

log = logging.getLogger(__name__ + '.__init__')


FIRST_CAMEL_REGEX = re.compile('(.)([A-Z][a-z]+)')
SECOND_CAMEL_REGEX = re.compile('([a-z0-9])([A-Z])')
CONTROL_CHARS = re.compile(r'[\x00-\x1F\x7F-\x9F]', re.UNICODE)
INVALID_FILE_CHARS = re.compile(r'[\\/:\*\?"<>\|\+\[\]%]', re.UNICODE)
IMAGES_FILTER = None


def trace_error_handler(logger):
    """
    Log the calling path of an exception

    :param logger: logger to use so traceback is logged to correct class
    """
    log_string = "OpenLP Error trace"
    for tb in traceback.extract_stack():
        log_string = '{text}\n   File {file} at line {line} \n\t called {data}'.format(text=log_string,
                                                                                       file=tb[0],
                                                                                       line=tb[1],
                                                                                       data=tb[3])
    logger.error(log_string)


def check_directory_exists(directory, do_not_log=False):
    """
    Check a theme directory exists and if not create it

    :param directory: The directory to make sure exists
    :param do_not_log: To not log anything. This is need for the start up, when the log isn't ready.
    """
    if not do_not_log:
        log.debug('check_directory_exists {text}'.format(text=directory))
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except IOError as e:
        if not do_not_log:
            log.exception('failed to check if directory exists or create directory')


def get_frozen_path(frozen_option, non_frozen_option):
    """
    Return a path based on the system status.

    :param frozen_option:
    :param non_frozen_option:
    """
    if hasattr(sys, 'frozen') and sys.frozen == 1:
        return frozen_option
    return non_frozen_option


class ThemeLevel(object):
    """
    Provides an enumeration for the level a theme applies to
    """
    Global = 1
    Service = 2
    Song = 3


def translate(context, text, comment=None, qt_translate=QtCore.QCoreApplication.translate):
    """
    A special shortcut method to wrap around the Qt5 translation functions. This abstracts the translation procedure so
    that we can change it if at a later date if necessary, without having to redo the whole of OpenLP.

    :param context: The translation context, used to give each string a context or a namespace.
    :param text: The text to put into the translation tables for translation.
    :param comment: An identifying string for when the same text is used in different roles within the same context.
    :param qt_translate:
    """
    return qt_translate(context, text, comment)


class SlideLimits(object):
    """
    Provides an enumeration for behaviour of OpenLP at the end limits of each service item when pressing the up/down
    arrow keys
    """
    End = 1
    Wrap = 2
    Next = 3


def de_hump(name):
    """
    Change any Camel Case string to python string
    """
    sub_name = FIRST_CAMEL_REGEX.sub(r'\1_\2', name)
    return SECOND_CAMEL_REGEX.sub(r'\1_\2', sub_name).lower()


def is_win():
    """
    Returns true if running on a system with a nt kernel e.g. Windows, Wine

    :return: True if system is running a nt kernel false otherwise
    """
    return os.name.startswith('nt')


def is_macosx():
    """
    Returns true if running on a system with a darwin kernel e.g. Mac OS X

    :return: True if system is running a darwin kernel false otherwise
    """
    return sys.platform.startswith('darwin')


def is_linux():
    """
    Returns true if running on a system with a linux kernel e.g. Ubuntu, Debian, etc

    :return: True if system is running a linux kernel false otherwise
    """
    return sys.platform.startswith('linux')


def verify_ipv4(addr):
    """
    Validate an IPv4 address

    :param addr: Address to validate
    :returns: bool
    """
    try:
        valid = IPv4Address(addr)
        return True
    except AddressValueError:
        return False


def verify_ipv6(addr):
    """
    Validate an IPv6 address

    :param addr: Address to validate
    :returns: bool
    """
    try:
        valid = IPv6Address(addr)
        return True
    except AddressValueError:
        return False


def verify_ip_address(addr):
    """
    Validate an IP address as either IPv4 or IPv6

    :param addr: Address to validate
    :returns: bool
    """
    return True if verify_ipv4(addr) else verify_ipv6(addr)


def md5_hash(salt, data=None):
    """
    Returns the hashed output of md5sum on salt,data
    using Python3 hashlib

    :param salt: Initial salt
    :param data: OPTIONAL Data to hash
    :returns: str
    """
    log.debug('md5_hash(salt="{text}")'.format(text=salt))
    hash_obj = hashlib.new('md5')
    hash_obj.update(salt)
    if data:
        hash_obj.update(data)
    hash_value = hash_obj.hexdigest()
    log.debug('md5_hash() returning "{text}"'.format(text=hash_value))
    return hash_value


def qmd5_hash(salt, data=None):
    """
    Returns the hashed output of MD5Sum on salt, data
    using PyQt5.QCryptographicHash.

    :param salt: Initial salt
    :param data: OPTIONAL Data to hash
    :returns: str
    """
    log.debug('qmd5_hash(salt="{text}"'.format(text=salt))
    hash_obj = QHash(QHash.Md5)
    hash_obj.addData(salt)
    hash_obj.addData(data)
    hash_value = hash_obj.result().toHex()
    log.debug('qmd5_hash() returning "{text}"'.format(text=hash_value))
    return hash_value.data()


def clean_button_text(button_text):
    """
    Clean the & and other characters out of button text

    :param button_text: The text to clean
    """
    return button_text.replace('&', '').replace('< ', '').replace(' >', '')


from .openlpmixin import OpenLPMixin
from .registry import Registry
from .registrymixin import RegistryMixin
from .registryproperties import RegistryProperties
from .uistrings import UiStrings
from .settings import Settings
from .applocation import AppLocation
from .actions import ActionList
from .languagemanager import LanguageManager


def add_actions(target, actions):
    """
    Adds multiple actions to a menu or toolbar in one command.

    :param target: The menu or toolbar to add actions to
    :param actions: The actions to be added. An action consisting of the keyword ``None``
        will result in a separator being inserted into the target.
    """
    for action in actions:
        if action is None:
            target.addSeparator()
        else:
            target.addAction(action)


def get_uno_command(connection_type='pipe'):
    """
    Returns the UNO command to launch an libreoffice.org instance.
    """
    for command in ['libreoffice', 'soffice']:
        if which(command):
            break
    else:
        raise FileNotFoundError('Command not found')

    OPTIONS = '--nologo --norestore --minimized --nodefault --nofirststartwizard'
    if connection_type == 'pipe':
        CONNECTION = '"--accept=pipe,name=openlp_pipe;urp;"'
    else:
        CONNECTION = '"--accept=socket,host=localhost,port=2002;urp;"'
    return '%s %s %s' % (command, OPTIONS, CONNECTION)


def get_uno_instance(resolver, connection_type='pipe'):
    """
    Returns a running libreoffice.org instance.

    :param resolver: The UNO resolver to use to find a running instance.
    """
    log.debug('get UNO Desktop Openoffice - resolve')
    if connection_type == 'pipe':
        return resolver.resolve('uno:pipe,name=openlp_pipe;urp;StarOffice.ComponentContext')
    else:
        return resolver.resolve('uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext')


def get_filesystem_encoding():
    """
    Returns the name of the encoding used to convert Unicode filenames into system file names.
    """
    encoding = sys.getfilesystemencoding()
    if encoding is None:
        encoding = sys.getdefaultencoding()
    return encoding


def split_filename(path):
    """
    Return a list of the parts in a given path.
    """
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        return path, ''
    else:
        return os.path.split(path)


def delete_file(file_path_name):
    """
    Deletes a file from the system.

    :param file_path_name: The file, including path, to delete.
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


def get_images_filter():
    """
    Returns a filter string for a file dialog containing all the supported image formats.
    """
    global IMAGES_FILTER
    if not IMAGES_FILTER:
        log.debug('Generating images filter.')
        formats = list(map(bytes.decode, list(map(bytes, QtGui.QImageReader.supportedImageFormats()))))
        visible_formats = '(*.{text})'.format(text='; *.'.join(formats))
        actual_formats = '(*.{text})'.format(text=' *.'.join(formats))
        IMAGES_FILTER = '{text} {visible} {actual}'.format(text=translate('OpenLP', 'Image Files'),
                                                           visible=visible_formats,
                                                           actual=actual_formats)
    return IMAGES_FILTER


def is_not_image_file(file_name):
    """
    Validate that the file is not an image file.

    :param file_name: File name to be checked.
    """
    if not file_name:
        return True
    else:
        formats = [bytes(fmt).decode().lower() for fmt in QtGui.QImageReader.supportedImageFormats()]
        file_part, file_extension = os.path.splitext(str(file_name))
        if file_extension[1:].lower() in formats and os.path.exists(file_name):
            return False
        return True


def clean_filename(filename):
    """
    Removes invalid characters from the given ``filename``.

    :param filename:  The "dirty" file name to clean.
    """
    if not isinstance(filename, str):
        filename = str(filename, 'utf-8')
    return INVALID_FILE_CHARS.sub('_', CONTROL_CHARS.sub('', filename))
