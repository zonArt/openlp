# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

class SettingsTab(QtGui.QWidget):
    """
    SettingsTab is a helper widget for plugins to define Tabs for the settings
    dialog.
    """
    def __init__(self, title):
        """
        Constructor to create the Settings tab item.

        ``title``
            The title of the tab, which is usually displayed on the tab.
        """
        QtGui.QWidget.__init__(self)
        self.tabTitle = title
        self.tabTitleVisible = None
        self.settingsSection = self.tabTitle
        self.setupUi()
        self.retranslateUi()
        self.initialise()
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
