# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008-2009 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import types

from PyQt4 import QtCore, QtGui
from openlp.core.resources import *
from openlp.core.lib.toolbar import *

class MediaManagerItem(QtGui.QWidget):
    """
    MediaManagerItem is a helper widget for plugins.
    """
    def __init__(self, icon=None, title=None):
        """
        Constructor to create the media manager item.
        """
        QtGui.QWidget.__init__(self)
        if type(icon) is QtGui.QIcon:
            self.icon = icon
        elif type(icon) is types.StringType:
            self.icon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(icon)),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            self.icon = None
        if title is not None:
            self.title = title
        self.Toolbar = None
        self.PageLayout = QtGui.QVBoxLayout(self)
        self.PageLayout.setSpacing(0)
        self.PageLayout.setMargin(0)
        self.setupUi()
        self.retranslateUi()
        self.initialise()

    def setupUi(self):
        pass

    def retranslateUi(self):
        pass

    def initialise(self):
        pass

    def addToolbar(self):
        """
        A method to help developers easily add a toolbar to the media manager
        item.
        """
        if self.Toolbar is None:
            self.Toolbar=OpenLPToolbar(self)
            self.PageLayout.addWidget(self.Toolbar)

    def addToolbarButton(self, title, tooltip, icon, slot=None, objectname=None):
        """
        A method to help developers easily add a button to the toolbar.
        """
        # NB different order (when I broke this out, I wanted to not break compatability)
        # but it makes sense for the icon to come before the tooltip (as you have to have an icon, but not neccesarily a tooltip)
        self.Toolbar.addToolbarButton(title, icon, tooltip, slot, objectname)

    def addToolbarSeparator(self):
        """
        A very simple method to add a separator to the toolbar.
        """
        self.Toolbar.addSeparator()

    def contextMenuSeparator(self, base):
        action = QtGui.QAction("", base)
        action.setSeparator(True)
        return action

    def contextMenuAction(self, base, icon, text, slot):
        """
        Utility method to help build context menus for plugins
        """
        if type(icon) is QtGui.QIcon:
            ButtonIcon = icon
        elif type(icon) is types.StringType:
            ButtonIcon = QtGui.QIcon()
            if icon.startswith(':/'):
                ButtonIcon.addPixmap(QtGui.QPixmap(icon), QtGui.QIcon.Normal,
                    QtGui.QIcon.Off)
            else:
                ButtonIcon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(icon)),
                    QtGui.QIcon.Normal, QtGui.QIcon.Off)

        action = QtGui.QAction(text, base)
        action .setIcon(ButtonIcon)
        QtCore.QObject.connect(action, QtCore.SIGNAL("triggered()"), slot)
        return action

