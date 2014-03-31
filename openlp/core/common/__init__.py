# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
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
The :mod:`common` module contains most of the components and libraries that make
OpenLP work.
"""
import re
import os
import logging
import sys
import traceback

from PyQt4 import QtCore

log = logging.getLogger(__name__+'.__init__')


FIRST_CAMEL_REGEX = re.compile('(.)([A-Z][a-z]+)')
SECOND_CAMEL_REGEX = re.compile('([a-z0-9])([A-Z])')


def trace_error_handler(logger):
    """
    Log the calling path of an exception

    :param logger: logger to use so traceback is logged to correct class
    """
    for tb in traceback.extract_stack():
        logger.error('Called by ' + tb[3] + ' at line ' + str(tb[1]) + ' in ' + tb[0])


def check_directory_exists(directory, do_not_log=False):
    """
    Check a theme directory exists and if not create it

    :param directory: The directory to make sure exists
    :param do_not_log: To not log anything. This is need for the start up, when the log isn't ready.
    """
    if not do_not_log:
        log.debug('check_directory_exists %s' % directory)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except IOError:
        pass


def get_frozen_path(frozen_option, non_frozen_option):
    """
    Return a path based on the system status.
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


def translate(context, text, comment=None, encoding=QtCore.QCoreApplication.CodecForTr, n=-1,
              qt_translate=QtCore.QCoreApplication.translate):
    """
    A special shortcut method to wrap around the Qt4 translation functions. This abstracts the translation procedure so
    that we can change it if at a later date if necessary, without having to redo the whole of OpenLP.

    :param context: The translation context, used to give each string a context or a namespace.
    :param text: The text to put into the translation tables for translation.
    :param comment: An identifying string for when the same text is used in different roles within the same context.
    :param encoding:
    :param n:
    :param qt_translate:
    """
    return qt_translate(context, text, comment, encoding, n)


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

from .openlpmixin import OpenLPMixin
from .registry import Registry
from .registrymixin import RegistryMixin
from .registryproperties import RegistryProperties
from .uistrings import UiStrings
from .settings import Settings
from .applocation import AppLocation
from .historycombobox import HistoryComboBox
