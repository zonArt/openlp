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
Provide common toolbar handling for OpenLP
"""
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import build_icon
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
        self.icons = {}
        self.setIconSize(QtCore.QSize(20, 20))
        self.actions = {}
        log.debug(u'Init done for %s' % parent.__class__.__name__)

    def addToolbarButton(self, name, **kwargs):
        """
        A method to help developers easily add a button to the toolbar. A new
        QAction is created by calling ``create_action()``. The action is added
        to the toolbar and the toolbar is set as parent. For more details please
        look at openlp.core.lib.ui.create_action()
        """
        action = create_widget_action(self, name, **kwargs)
        # The ObjectNames should be used as keys. So translators can't break
        # anything.
        title = kwargs.get(u'text', u'')
        self.actions[title] = action
        if u'icon' in kwargs:
            self.icons[title] = action.icon()
        return action

    def addToolbarSeparator(self, handle):
        """
        Add a Separator bar to the toolbar and store it's Handle
        """
        action = self.addSeparator()
        self.actions[handle] = action

    def addToolbarWidget(self, handle, widget):
        """
        Add a Widget to the toolbar and store it's Handle
        """
        action = self.addWidget(widget)
        self.actions[handle] = action

    def getIconFromTitle(self, title):
        """
        Search through the list of icons for an icon with a particular title,
        and return that icon.

        ``title``
            The title of the icon to search for.
        """
        title = QtCore.QString(title)
        try:
            if self.icons[title]:
                return self.icons[title]
        except KeyError:
            log.exception(u'getIconFromTitle - no icon for %s' % title)
            return QtGui.QIcon()

    def makeWidgetsInvisible(self, widgets):
        """
        Hide a set of widgets.

        ``widgets``
            The list of names of widgets to be hidden.
        """
        for widget in widgets:
            self.actions[widget].setVisible(False)

    def makeWidgetsVisible(self, widgets):
        """
        Show a set of widgets.

        ``widgets``
            The list of names of widgets to be shown.
        """
        for widget in widgets:
            self.actions[widget].setVisible(True)

    def addPushButton(self, image_file=None, text=u''):
        """
        Adds a push button to the toolbar.

        Returns the push button
        """
        push_button = QtGui.QPushButton(build_icon(image_file), text)
        push_button.setCheckable(True)
        push_button.setFlat(True)
        self.addWidget(push_button)
        return push_button
