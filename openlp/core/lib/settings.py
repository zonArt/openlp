# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Eric Ludin, Edwin Lunando, Brian T. Meyer,    #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Erode Woldsund                                                              #
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
The :mod:``settings`` module provides a thin wrapper for QSettings, which OpenLP
uses to manage settings persistence.
"""

import logging

from PyQt4 import QtCore

log = logging.getLogger()

class Settings(QtCore.QSettings):
    """
    Class to wrap QSettings.

    * Exposes all the methods of QSettings.
    * Adds functionality for OpenLP Portable. If the ``defaultFormat`` is set to
      ``IniFormat``, and the path to the Ini file is set using ``setFilename``,
      then the Settings constructor (without any arguments) will create a Settings
      object for accessing settings stored in that Ini file.
    """

    __filePath = u''

    @staticmethod
    def setFilename(iniFile):
        """
        Sets the complete path to an Ini file to be used by Settings objects.

        Does not affect existing Settings objects.
        """
        Settings.__filePath = iniFile

    def __init__(self, *args):
        if not args and Settings.__filePath and (Settings.defaultFormat() ==
            Settings.IniFormat):
            QtCore.QSettings.__init__(self, Settings.__filePath,
                Settings.IniFormat)
        else:
            QtCore.QSettings.__init__(self, *args)
