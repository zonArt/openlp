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
Mixin class with helpers
"""
import os
from tempfile import mkstemp

from PyQt4 import QtCore, QtGui
from openlp.core.common import Settings


class TestMixin(object):

    def get_application(self):
        """
        Build or reuse the Application object
        """
        old_app_instance = QtCore.QCoreApplication.instance()
        if old_app_instance is None:
            self.app = QtGui.QApplication([])
        else:
            self.app = old_app_instance

    def build_settings(self):
        """
        Build the settings Object and initialise it
        """
        Settings.setDefaultFormat(Settings.IniFormat)
        self.fd, self.ini_file = mkstemp('.ini')
        Settings().set_filename(self.ini_file)

    def destroy_settings(self):
        """
        Destroy the Settings Object
        """
        os.close(self.fd)
        os.unlink(Settings().fileName())





