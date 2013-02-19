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
Provide handling for persisting OpenLP settings.  OpenLP uses QSettings to manage settings persistence.  QSettings
provides a single API for saving and retrieving settings from the application but writes to disk in an OS dependant
format.
"""
import os

from openlp.core.utils import AppLocation


class SettingsManager(object):
    """
    Class to provide helper functions for the loading and saving of application settings.
    """

    @staticmethod
    def get_files(section=None, extension=None):
        """
        Get a list of files from the data files path.

        ``section``
            Defaults to *None*. The section of code getting the files - used to load from a section's data subdirectory.

        ``extension``
            Defaults to *None*. The extension to search for.
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
