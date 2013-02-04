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
Provide common toolbar handling for OpenLP
"""
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib.ui import create_widget_action

log = logging.getLogger(__name__)


class OpenLPToolbar(QtGui.QToolBar):
    """
    Lots of toolbars around the place, so it makes sense to have a common way
    to manage them. This is the base toolbar class.
    """
    def __init__(self, parent):
        """
        Initialise the toolbar.
        """
        QtGui.QToolBar.__init__(self, parent)
        # useful to be able to reuse button icons...
        self.setIconSize(QtCore.QSize(20, 20))
        self.actions = {}
        log.debug(u'Init done for %s' % parent.__class__.__name__)

    def addToolbarAction(self, name, **kwargs):
        """
        A method to help developers easily add a button to the toolbar.
        A new QAction is created by calling ``create_action()``. The action is
        added to the toolbar and the toolbar is set as parent.
        For more details please look at openlp.core.lib.ui.create_action()
        """
        action = create_widget_action(self, name, **kwargs)
        self.actions[name] = action
        return action

    def addToolbarWidget(self, widget):
        """
        Add a widget and store it's handle under the widgets object name.
        """
        action = self.addWidget(widget)
        self.actions[widget.objectName()] = action

    def setWidgetVisible(self, widgets, visible=True):
        """
        Set the visibitity for a widget or a list of widgets.

        ``widget``
            A list of string with widget object names.

        ``visible``
            The new state as bool.
        """
        for handle in widgets:
            if handle in self.actions:
                self.actions[handle].setVisible(visible)
            else:
                log.warn(u'No handle "%s" in actions list.', unicode(handle))
