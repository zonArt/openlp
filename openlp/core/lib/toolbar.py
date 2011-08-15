# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
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

    def addToolbarButton(self, title, icon, tooltip=None, slot=None,
        checkable=False, shortcuts=None, context=QtCore.Qt.WidgetShortcut):
        """
        A method to help developers easily add a button to the toolbar.

        ``title``
            The title of the button.

        ``icon``
            The icon of the button. This can be an instance of QIcon, or a
            string containing either the absolute path to the image, or an
            internal resource path starting with ':/'.

        ``tooltip``
            A hint or tooltip for this button.

        ``slot``
            The method to run when this button is clicked.

        ``checkable``
            If *True* the button has two, *off* and *on*, states. Default is
            *False*, which means the buttons has only one state.

        ``shortcuts``
            The list of shortcuts for this action

        ``context``
            Specify the context in which this shortcut is valid
        """
        if icon:
            actionIcon = build_icon(icon)
            if slot and not checkable:
                newAction = self.addAction(actionIcon, title, slot)
            else:
                newAction = self.addAction(actionIcon, title)
            self.icons[title] = actionIcon
        else:
            newAction = QtGui.QAction(title, self)
            self.addAction(newAction)
            QtCore.QObject.connect(newAction,
                QtCore.SIGNAL(u'triggered()'), slot)
        if tooltip:
            newAction.setToolTip(tooltip)
        if checkable:
            newAction.setCheckable(True)
            QtCore.QObject.connect(newAction,
                QtCore.SIGNAL(u'toggled(bool)'), slot)
        self.actions[title] = newAction
        if shortcuts is not None:
            newAction.setShortcuts(shortcuts)
            newAction.setShortcutContext(context)
        return newAction

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
