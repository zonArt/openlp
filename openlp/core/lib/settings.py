# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
      then the Settings constructor will create a Settings object for accessing
      settings stored in that Ini file.
    """

    FilePath = u''

    @staticmethod
    def setFilename(filepath):
        """
        Sets the complete path to an Ini file to be used by Settings objects.

        Does not affect existing Settings objects.
        """
        Settings.FilePath = filepath
        log.info(u'Set Settings file: %s' % filepath)

    def __init__(self, *args):
        if Settings.FilePath and (Settings.defaultFormat() ==
                                  Settings.IniFormat):
            QtCore.QSettings.__init__(self, Settings.FilePath,
                Settings.IniFormat)
        else:
            QtCore.QSettings.__init__(self, *args)
