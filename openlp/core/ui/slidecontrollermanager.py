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

class SlideControllerManager():
    """
    This class controls which SlideController is availabe to the
    main window
    """
    global log
    log = logging.getLogger(u'SlideControllerManager')

    def __init__(self, parent):
        """
        Set up the Slide Controller. Manager
        """
        self.parent = parent
        self.live = {}
        self.preview = {}

    def add_controllers(self, handle, preview, live):
        self.live[handle] = live
        self.preview[handle] = preview
        print self.live

    def getPreviewController(self, handle):
        return self.preview[handle]

    def getLiveController(self, handle):
        print "---"
        print self.live
        print handle
        print self.live[handle]
        return self.live[handle]
