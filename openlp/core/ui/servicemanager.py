# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2009 Raoul Snyman
Portions copyright (c) 2009 Martin Thompson, Tim Bentley,

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
import os

from time import sleep
from PyQt4 import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
# from openlp.core.resources import *
# from openlp.core.ui import AboutForm, AlertForm, SettingsDialog, SlideController
from openlp.core.lib import OpenLPToolbar

# from openlp.core import PluginManager
import logging

class ServiceManager(QWidget):

    """Manages the orders of service.  Currently this involves taking
    text strings from plugins and adding them to an OOS file. In
    future, it will also handle zipping up all the resources used into
    one lump"""

    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent=parent
        self.Layout = QtGui.QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)
        self.Toolbar = OpenLPToolbar(self)
        self.Toolbar.addToolbarButton("Move to top", ":/services/service_top.png")
        self.Toolbar.addToolbarButton("Move up", ":/services/service_up.png")
        self.Toolbar.addToolbarButton("Move down", ":/services/service_down.png")
        self.Toolbar.addToolbarButton("Move to bottom", ":/services/service_bottom.png")
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton("New Service", ":/services/service_new.png")
        self.Toolbar.addToolbarButton("Save Service", ":/services/service_save.png")
        self.Toolbar.addSeparator()
        self.ThemeComboBox = QtGui.QComboBox(self.Toolbar)
        self.ThemeComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.ThemeComboBox.addItem(QtCore.QString())
        self.ThemeComboBox.addItem(QtCore.QString())
        self.ThemeComboBox.addItem(QtCore.QString())
        self.ThemeWidget = QtGui.QWidgetAction(self.Toolbar)
        self.ThemeWidget.setDefaultWidget(self.ThemeComboBox)
        self.Toolbar.addAction(self.ThemeWidget)
        self.Layout.addWidget(self.Toolbar)
        self.ListView = QtGui.QListView(self)
        self.Layout.addWidget(self.ListView)
