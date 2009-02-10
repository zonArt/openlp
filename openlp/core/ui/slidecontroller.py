# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

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
from PyQt4 import QtCore, QtGui

class SlideController(object):
    def __init__(self, control_splitter):
        self.Pane = QtGui.QWidget(control_splitter)
#         self.Pane.setObjectName("Pane")
        self.PaneLayout = QtGui.QVBoxLayout(self.Pane)
        self.PaneLayout.setSpacing(0)
        self.PaneLayout.setMargin(0)
#         self.PaneLayout.setObjectName("PaneLayout")
        self.Splitter = QtGui.QSplitter(self.Pane)
        self.Splitter.setOrientation(QtCore.Qt.Vertical)
#         self.Splitter.setObjectName("Splitter")
        self.Controller = QtGui.QScrollArea(self.Splitter)
        self.Controller.setWidgetResizable(True)
#         self.Controller.setObjectName("Controller")
        self.ControllerContents = QtGui.QWidget(self.Controller)
        self.ControllerContents.setGeometry(QtCore.QRect(0, 0, 228, 536))
#         self.ControllerContents.setObjectName("ControllerContents")
        self.Controller.setWidget(self.ControllerContents)
        self.Screen = QtGui.QGraphicsView(self.Splitter)
        self.Screen.setMaximumSize(QtCore.QSize(16777215, 250))
#         self.Screen.setObjectName("Screen")
        self.PaneLayout.addWidget(self.Splitter)
