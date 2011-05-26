# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Millar, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Jeffrey Smith, Maikel            #
# Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund                    #
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
Provide handling for persisting OpenLP settings.  OpenLP uses QSettings to
manage settings persistence.  QSettings provides a single API for saving and
retrieving settings from the application but writes to disk in an OS dependant
format.
"""
import os

from PyQt4 import QtCore

from openlp.core.utils import AppLocation

class SettingsManager(object):
    """
    Class to provide helper functions for the loading and saving of application
    settings.
    """

    @staticmethod
    def get_last_dir(section, num=None):
        """
        Read the last directory used for plugin.

        ``section``
            The section of code calling the method. This is used in the
            settings key.

        ``num``
            Defaults to *None*. A further qualifier.
        """
        if num:
            name = u'last directory %d' % num
        else:
            name = u'last directory'
        last_dir = unicode(QtCore.QSettings().value(
            section + u'/' + name, QtCore.QVariant(u'')).toString())
        return last_dir

    @staticmethod
    def set_last_dir(section, directory, num=None):
        """
        Save the last directory used for plugin.

        ``section``
            The section of code calling the method. This is used in the
            settings key.

        ``directory``
            The directory being stored in the settings.

        ``num``
            Defaults to *None*. A further qualifier.
        """
        if num:
            name = u'last directory %d' % num
        else:
            name = u'last directory'
        QtCore.QSettings().setValue(
            section + u'/' + name, QtCore.QVariant(directory))

    @staticmethod
    def set_list(section, name, list):
        """
        Save a list to application settings.

        ``section``
            The section of the settings to store this list.

        ``name``
            The name of the list to save.

        ``list``
            The list of values to save.
        """
        settings = QtCore.QSettings()
        settings.beginGroup(section)
        old_count = settings.value(
            u'%s count' % name, QtCore.QVariant(0)).toInt()[0]
        new_count = len(list)
        settings.setValue(u'%s count' % name, QtCore.QVariant(new_count))
        for counter in range (0, new_count):
            settings.setValue(
                u'%s %d' % (name, counter), QtCore.QVariant(list[counter-1]))
        if old_count > new_count:
            # Tidy up any old list items
            for counter in range(new_count, old_count):
                settings.remove(u'%s %d' % (name, counter))
        settings.endGroup()

    @staticmethod
    def load_list(section, name):
        """
        Load a list from the config file.

        ``section``
            The section of the settings to load the list from.

        ``name``
            The name of the list.
        """
        settings = QtCore.QSettings()
        settings.beginGroup(section)
        list_count = settings.value(
            u'%s count' % name, QtCore.QVariant(0)).toInt()[0]
        list = []
        if list_count:
            for counter in range(0, list_count):
                item = unicode(
                    settings.value(u'%s %d' % (name, counter)).toString())
                if item:
                    list.append(item)
        settings.endGroup()
        return list

    @staticmethod
    def get_files(section=None, extension=None):
        """
        Get a list of files from the data files path.

        ``section``
            Defaults to *None*. The section of code getting the files - used
            to load from a section's data subdirectory.

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
            return [filename for filename in files
                if extension == os.path.splitext(filename)[1]]
        else:
            # no filtering required
            return files
