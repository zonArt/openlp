# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 - 2009 Martin Thompson, Tim Bentley

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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

from openlp.core.lib import Plugin, Event,  EventType,  translate

from openlp.plugins.bibles.lib import BibleManager, BiblesTab, BibleMediaItem

class BiblePlugin(Plugin):
    global log
    log=logging.getLogger(u'BiblePlugin')
    log.info(u'Bible Plugin loaded')

    def __init__(self, plugin_helpers):
        # Call the parent constructor
        Plugin.__init__(self, u'Bibles', u'1.9.0', plugin_helpers)
        self.weight = -9
        # Create the plugin icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(u':/media/media_bible.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #Register the bible Manager
        self.biblemanager = BibleManager(self.config)

    def get_settings_tab(self):
        self.bibles_tab = BiblesTab()
        return self.bibles_tab

    def get_media_manager_item(self):
        # Create the BibleManagerItem object
        self.media_item = BibleMediaItem(self, self.icon, u'Bible Verses')
        return self.media_item

    def add_import_menu_item(self, import_menu):
        self.ImportBibleItem = QtGui.QAction(import_menu)
        self.ImportBibleItem.setObjectName(u'ImportBibleItem')
        import_menu.addAction(self.ImportBibleItem)
        self.ImportBibleItem.setText(translate(u'BiblePlugin', u'&Bible'))
        # Signals and slots
        QtCore.QObject.connect(self.ImportBibleItem, QtCore.SIGNAL(u'triggered()'),  self.onBibleNewClick)

    def add_export_menu_item(self, export_menu):
        self.ExportBibleItem = QtGui.QAction(export_menu)
        self.ExportBibleItem.setObjectName(u'ExportBibleItem')
        export_menu.addAction(self.ExportBibleItem)
        self.ExportBibleItem.setText(translate(u'BiblePlugin', u'&Bible'))

    def initialise(self):
        pass

    def onBibleNewClick(self):
        self.media_item.onBibleNewClick()

    def handle_event(self, event):
        """
        Handle the event contained in the event object.
        """
        log.debug(u'Handle event called with event %s with payload %s'%(event.event_type, event.payload))
        if event.event_type == EventType.ThemeListChanged:
            log.debug(u'New Theme request received')
            self.bibles_tab.updateThemeList(event.payload)
        return Plugin.handle_event(self, event)
