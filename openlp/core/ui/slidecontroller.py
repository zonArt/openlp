# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

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

class SlideController(QtGui.QWidget):
    def __init__(self, control_splitter):
        QtGui.QWidget.__init__(self)
        self.Pane = QtGui.QWidget(control_splitter)
        self.Splitter = QtGui.QSplitter(self.Pane)
        self.Splitter.setOrientation(QtCore.Qt.Vertical)

        self.PaneLayout = QtGui.QVBoxLayout(self.Pane)
        self.PaneLayout.addWidget(self.Splitter)
        self.PaneLayout.setSpacing(50)
        self.PaneLayout.setMargin(0)

        #self.VerseListView = QtGui.QListWidget(customEditDialog)
        #self.VerseListView.setObjectName("VerseListView")
        #self.horizontalLayout_4.addWidget(self.VerseListView)

        self.Controller = QtGui.QScrollArea(self.Splitter)
        self.Controller.setWidgetResizable(True)

        self.ControllerContents = QtGui.QWidget(self.Controller)
        self.ControllerContents.setGeometry(QtCore.QRect(0, 0, 228, 536))
        self.Controller.setGeometry(QtCore.QRect(0, 0, 828, 536))

        self.Controller.setWidget(self.ControllerContents)

        self.SlidePreview = QtGui.QLabel(self.Splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SlidePreview.sizePolicy().hasHeightForWidth())
        self.SlidePreview.setSizePolicy(sizePolicy)
        self.SlidePreview.setMinimumSize(QtCore.QSize(250, 190))
        self.SlidePreview.setFrameShape(QtGui.QFrame.WinPanel)
        self.SlidePreview.setFrameShadow(QtGui.QFrame.Sunken)
        self.SlidePreview.setLineWidth(1)
        self.SlidePreview.setScaledContents(True)
        self.SlidePreview.setObjectName("SlidePreview")

    def previewFrame(self, frame):
        self.SlidePreview.setPixmap(frame)

        imageLabel = QtGui.QLabel()
        imageLabel.setPixmap(frame)
        self.Controller.setWidget(imageLabel)
