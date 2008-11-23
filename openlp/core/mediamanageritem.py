# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

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
from openlp.resources import *

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
            self.Icon = icon
        elif type(icon) is types.StringType:
            self.Icon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(icon)),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            self.Icon = None
        if title is not None:
            self.Title = title
        self.Toolbar = None

    def addToolbar(self):
        """
        A method to help developers easily add a toolbar to the media manager
        item.
        """
        if self.Toolbar is None:
            self.PageLayout = QtGui.QVBoxLayout(self)
            self.PageLayout.setSpacing(0)
            self.PageLayout.setMargin(0)
            self.PageLayout.setObjectName('PageLayout')
            self.Toolbar = QtGui.QWidget(self)
            self.Toolbar.setObjectName('Toolbar')
            self.ToolbarLayout = QtGui.QHBoxLayout(self.Toolbar)
            self.ToolbarLayout.setSpacing(0)
            self.ToolbarLayout.setMargin(0)
            self.ToolbarLayout.setObjectName('ToolbarLayout')

    def addToolbarItem(self, item):
        if self.Toolbar is None:
            self.addToolbar()
        self.ToolbarLayout.addWidget(item)
