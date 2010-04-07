# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

from PyQt4 import QtGui

from openlp.core.lib import PluginConfig

class SettingsTab(QtGui.QWidget):
    """
    SettingsTab is a helper widget for plugins to define Tabs for the settings
    dialog.
    """
    def __init__(self, title, section=None):
        """
        Constructor to create the Settings tab item.

        ``title``
            Defaults to *None*. The title of the tab, which is usually
            displayed on the tab.

        ``section``
            Defaults to *None*. This is the section in the configuration file
            to write to when the ``save`` method is called.
        """
        QtGui.QWidget.__init__(self)
        self.tabTitle = title
        self.tabTitleVisible = None
        self.setupUi()
        self.retranslateUi()
        self.initialise()
        if section is None:
            self.config = PluginConfig(title)
        else:
            self.config = PluginConfig(section)
        self.preLoad()
        self.load()

    def setupUi(self):
        """
        Setup the tab's interface.
        """
        pass

    def preLoad(self):
        """
        Setup the tab's interface.
        """
        pass

    def retranslateUi(self):
        """
        Setup the interface translation strings.
        """
        pass

    def initialise(self):
        """
        Do any extra initialisation here.
        """
        pass

    def load(self):
        """
        Load settings from disk.
        """
        pass

    def save(self):
        """
        Save settings to disk.
        """
        pass

    def postSetUp(self):
        """
        Changes which need to be made after setup of application
        """
        pass
