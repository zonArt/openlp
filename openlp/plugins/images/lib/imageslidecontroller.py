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
import logging
import os

from PyQt4 import QtCore, QtGui
from openlp.core.lib import OpenLPToolbar, translate
from openlp.core.ui.slidecontroller import BaseToolbar

class ImageToolbar(BaseToolbar):

    def __init__(self, isLive):
        self.Toolbar = None
        self.PreviewListView = QtGui.QListWidget()
        self.PreviewListData = None
        self.isLive = isLive
        self.defineToolbar()

    def getToolbar(self):
        return self.Toolbar

    def defineToolbar(self):
        # Controller toolbar
        #self.Toolbar = OpenLPToolbar(self.Controller)
        sizeToolbarPolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        sizeToolbarPolicy.setHorizontalStretch(0)
        sizeToolbarPolicy.setVerticalStretch(0)
        sizeToolbarPolicy.setHeightForWidth(
            self.Toolbar.sizePolicy().hasHeightForWidth())
        if self.isLive:
            self.Toolbar.addToolbarButton(u'First Slide',
                u':/slides/slide_first.png',
                translate(u'SlideController', u'Move to first'),
                self.onSlideSelectedFirst)
        self.Toolbar.addToolbarButton(u'Last Slide',
            u':/slides/slide_previous.png',
            translate(u'SlideController', u'Move to previous'),
            self.onSlideSelectedPrevious)
        self.Toolbar.addToolbarButton(u'First Slide',
            u':/slides/slide_next.png',
            translate(u'SlideController', u'Move to next'),
            self.onSlideSelectedNext)
        if self.isLive:
            self.Toolbar.addToolbarButton(u'Last Slide',
                u':/slides/slide_last.png',
                translate(u'SlideController', u'Move to last'),
                self.onSlideSelectedLast)
            self.Toolbar.addSeparator()
            self.Toolbar.addToolbarButton(u'Close Screen',
                u':/slides/slide_close.png',
                translate(u'SlideController', u'Close Screen'),
                self.onBlankScreen)
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton(u'Start Loop',
            u':/slides/slide_last.png',
            translate(u'SlideController', u'Start continuous loop'),
            self.onStartLoop)
        self.Toolbar.addToolbarButton(u'Stop Loop',
            u':/slides/slide_last.png',
            translate(u'SlideController', u'Start continuous loop'),
            self.onStopLoop)
        self.Toolbar.setSizePolicy(sizeToolbarPolicy)
        self.ControllerLayout.addWidget(self.Toolbar)

    def onStartLoop(self):
        """
        Go to the last slide.
        """
        row = self.PreviewListData.createIndex(
            self.PreviewListData.rowCount() - 1, 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row,
                QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)

    def onStopLoop(self):
        """
        Go to the last slide.
        """
        row = self.PreviewListData.createIndex(
            self.PreviewListData.rowCount() - 1, 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row,
                QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)
