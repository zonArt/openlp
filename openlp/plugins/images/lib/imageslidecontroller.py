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
from openlp.core.lib import OpenLPToolbar, translate,  Receiver
from openlp.core.ui.slidecontroller import MasterToolbar

class ImageToolbar(MasterToolbar):

    def __init__(self, parent,  isLive):
        MasterToolbar.__init__(self, isLive)
        self.parent = parent
        self.Toolbar = None
        self.isLive = isLive

    def defineZone5(self):
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton(u'Start Loop',
            u':/media/media_time.png',
            translate(u'SlideController', u'Start continuous loop'),
            self.onStartLoop)
        self.Toolbar.addToolbarButton(u'Stop Loop',
            u':/media/media_stop.png',
            translate(u'SlideController', u'Stop continuous loop'),
            self.onStopLoop)
        self.Toolbar.addSeparator()
        self.DelaySpinBox = QtGui.QSpinBox(self.Toolbar)
        self.SpinWidget = QtGui.QWidgetAction(self.Toolbar)
        self.SpinWidget.setDefaultWidget(self.DelaySpinBox)
        self.Toolbar.addAction(self.SpinWidget)
        self.DelaySpinBox.setValue(self.parent.parent.ImageTab.loop_delay)
        self.DelaySpinBox.setSuffix(translate(u'ImageSlideController', u's'))

    def onStartLoop(self):
        """
        Trigger the slide controller to start to loop passing the delay
        """
        Receiver().send_message(u'%sslide_start_loop' % self.prefix,  self.DelaySpinBox.value())

    def onStopLoop(self):
        """
        Trigger the slide controller to stop the loop
        """
        Receiver().send_message(u'%sslide_stop_loop' % self.prefix)
