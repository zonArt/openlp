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
Provide additional functionality required by OpenLP from the inherited
QDockWidget.
"""
import logging

from PyQt4 import QtGui

from openlp.core.lib import ScreenList, build_icon

log = logging.getLogger(__name__)


class OpenLPDockWidget(QtGui.QDockWidget):
    """
    Custom DockWidget class to handle events
    """
    def __init__(self, parent=None, name=None, icon=None):
        """
        Initialise the DockWidget
        """
        log.debug(u'Initialise the %s widget' % name)
        QtGui.QDockWidget.__init__(self, parent)
        if name:
            self.setObjectName(name)
        if icon:
            self.setWindowIcon(build_icon(icon))
        # Sort out the minimum width.
        screens = ScreenList()
        mainwindow_docbars = screens.current[u'size'].width() / 5
        if mainwindow_docbars > 300:
            self.setMinimumWidth(300)
        else:
            self.setMinimumWidth(mainwindow_docbars)
