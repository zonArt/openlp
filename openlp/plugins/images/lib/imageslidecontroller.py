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
from openlp.core.ui.slidecontroller import MasterToolbar

class ImageToolbar(MasterToolbar):

    def __init__(self, parent,  isLive):
        MasterToolbar.__init__(self, isLive)
        self.parent = parent
        self.Toolbar = None
        self.isLive = isLive
        self.defineToolbar()

    def defineToolbar(self):
        # Controller toolbar
        self.Toolbar = OpenLPToolbar(self)
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
        self.Toolbar.addToolbarButton(u'Previous Slide',
            u':/slides/slide_previous.png',
            translate(u'SlideController', u'Move to previous'),
            self.onSlideSelectedPrevious)
        self.Toolbar.addToolbarButton(u'Next Slide',
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
            u':/media/media_time.png',
            translate(u'SlideController', u'Start continuous loop'),
            self.onStartLoop)
        self.Toolbar.addToolbarButton(u'Stop Loop',
            u':/media/media_stop.png',
            translate(u'SlideController', u'Stop continuous loop'),
            self.onStopLoop)
        self.Toolbar.setSizePolicy(sizeToolbarPolicy)

    def onStartLoop(self):
        """
        Go to the last slide.
        """
        delay = self.parent.parent.ImageTab.loop_delay
        self.timer_id =  self.startTimer(delay * 1000)

    def onStopLoop(self):
        """
        Go to the last slide.
        """
        self.killTimer(self.timer_id)

    def timerEvent(self, event):
        if event.timerId() == self.timer_id:
            self.onSlideSelectedNext()

