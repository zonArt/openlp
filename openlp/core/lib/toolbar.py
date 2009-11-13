# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import buildIcon

class OpenLPToolbar(QtGui.QToolBar):
    """
    Lots of toolbars around the place, so it makes sense to have a common way
    to manage them. This is the base toolbar class.
    """
    def __init__(self, parent):
        """
        Initialise the toolbar.
        """
        QtGui.QToolBar.__init__(self, None)
        # useful to be able to reuse button icons...
        self.icons = {}
        self.setIconSize(QtCore.QSize(20, 20))
        self.actions = {}
        self.log = logging.getLogger(u'OpenLPToolbar')
        self.log.debug(u'Init done')

    def addToolbarButton(self, title, icon, tooltip=None, slot=None,
        checkable=False):
        """
        A method to help developers easily add a button to the toolbar.

        ``title``
            The title of the button.

        ``icon``
            The icon of the button. This can be an instance of QIcon, or a
            string cotaining either the absolute path to the image, or an
            internal resource path starting with ':/'.

        ``tooltip``
            A hint or tooltip for this button.

        ``slot``
            The method to run when this button is clicked.

        ``objectname``
            The name of the object, as used in `<button>.setObjectName()`.
        """
        ButtonIcon = buildIcon(icon)
        if ButtonIcon:
            if slot and not checkable:
                ToolbarButton = self.addAction(ButtonIcon, title, slot)
            else:
                ToolbarButton = self.addAction(ButtonIcon, title)
            if tooltip:
                ToolbarButton.setToolTip(tooltip)
            if checkable:
                ToolbarButton.setCheckable(True)
                QtCore.QObject.connect(ToolbarButton,
                    QtCore.SIGNAL(u'toggled(bool)'), slot)
            self.icons[title] = ButtonIcon
            self.actions[title] = ToolbarButton
            return ToolbarButton

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
        if self.icons.has_key(title):
            return self.icons[title]
        else:
            self.log.error(u'getIconFromTitle - no icon for %s' % title)
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

    def addPushButton(self, imageFile=None, text=u''):
        """
        Adds a push button to the toolbar.

        Returns the push button
        """
        pushButton = QtGui.QPushButton(buildIcon(imageFile), text)
        pushButton.setCheckable(True)
        pushButton.setFlat(True)
        self.addWidget(pushButton)
        return pushButton
