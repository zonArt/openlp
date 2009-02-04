# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
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
from openlp.core.resources import *

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
        #self.ToolbarButtons = []

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
            self.Toolbar = QtGui.QToolBar(self)
            self.Toolbar.setObjectName('Toolbar')
            self.PageLayout.addWidget(self.Toolbar)

    def addToolbarButton(self, title, tooltip, icon, slot=None, objectname=None):
        """
        A method to help developers easily add a button to the toolbar.
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
        ToolbarButton = self.Toolbar.addAction(ButtonIcon, title)
        if tooltip is not None:
            ToolbarButton.setToolTip(tooltip)
        if slot is not None:
            QtCore.QObject.connect(ToolbarButton, QtCore.SIGNAL('triggered()'), slot)

    def addToolbarSeparator(self):
        """
        A very simple method to add a separator to the toolbar.
        """
        self.Toolbar.addSeparator()

    def getInputFile(self, dialogname, dialoglocation, dialogfilter):
        return QtGui.QFileDialog.getOpenFileName(self, dialogname,
                                                 dialoglocation, dialogfilter)

    def getInputFiles(self, dialogname, dialoglocation, dialogfilter):
        return QtGui.QFileDialog.getOpenFileNames(self, dialogname,
                                                  dialoglocation, dialogfilter)

    def refresh(self):
        self.update()

