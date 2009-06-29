
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2009 Raoul Snyman
Portions copyright (c) 2009 Martin Thompson, Tim Bentley

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
import logging

class OpenLPToolbar(QtGui.QToolBar):
    """
    Lots of toolbars around the place, so it makes sense to have a common way to manage them
    """
    def __init__(self, parent):
        QtGui.QToolBar.__init__(self, None)
        # useful to be able to reuse button icons...
        self.icons = {}
        self.log = logging.getLogger(u'OpenLPToolbar')
        self.log.info(u'Init done')

    def addToolbarButton(self, title, icon, tooltip=None, slot=None, objectname=None):
        """
        A method to help developers easily add a button to the toolbar.
        """
        ButtonIcon = None
        if type(icon) is QtGui.QIcon:
            ButtonIcon = icon
        elif type(icon) is types.StringType or type(icon) is types.UnicodeType:
            ButtonIcon = QtGui.QIcon()
            if icon.startswith(u':/'):
                ButtonIcon.addPixmap(QtGui.QPixmap(icon), QtGui.QIcon.Normal,
                    QtGui.QIcon.Off)
            else:
                ButtonIcon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(icon)),
                    QtGui.QIcon.Normal, QtGui.QIcon.Off)
        if ButtonIcon is not None:
            ToolbarButton = self.addAction(ButtonIcon, title)
            if tooltip is not None:
                ToolbarButton.setToolTip(tooltip)
            if slot is not None:
                QtCore.QObject.connect(ToolbarButton, QtCore.SIGNAL(u'triggered()'), slot)
            self.icons[title] = ButtonIcon

    def getIconFromTitle(self, title):
        if self.icons.has_key(title):
            return self.icons[title]
        else:
            self.log.error(u'getIconFromTitle - no icon for %s' % title)
            return QtGui.QIcon()
