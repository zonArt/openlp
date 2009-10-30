# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin, buildIcon
from openlp.plugins.bibles.lib import BibleManager, BiblesTab, BibleMediaItem

class BiblePlugin(Plugin):
    global log
    log = logging.getLogger(u'BiblePlugin')
    log.info(u'Bible Plugin loaded')

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Bibles', u'1.9.0', plugin_helpers)
        self.weight = -9
        self.icon = buildIcon(u':/media/media_bible.png')
        #Register the bible Manager
        self.biblemanager = None

    def can_be_disabled(self):
        return True

    def initialise(self):
        log.info(u'bibles Initialising')
        if self.biblemanager is None:
            self.biblemanager = BibleManager(self.config)
        Plugin.initialise(self)
        self.insert_toolbox_item()
        self.ImportBibleItem.setVisible(True)
        self.ExportBibleItem.setVisible(True)

    def finalise(self):
        log.info(u'Plugin Finalise')
        Plugin.finalise(self)
        self.remove_toolbox_item()
        self.ImportBibleItem.setVisible(False)
        self.ExportBibleItem.setVisible(False)

    def get_settings_tab(self):
        return BiblesTab(self.name)

    def get_media_manager_item(self):
        # Create the BibleManagerItem object
        return BibleMediaItem(self, self.icon, self.name)

    def add_import_menu_item(self, import_menu):
        self.ImportBibleItem = QtGui.QAction(import_menu)
        self.ImportBibleItem.setObjectName(u'ImportBibleItem')
        import_menu.addAction(self.ImportBibleItem)
        self.ImportBibleItem.setText(import_menu.trUtf8(u'&Bible'))
        # Signals and slots
        QtCore.QObject.connect(self.ImportBibleItem,
            QtCore.SIGNAL(u'triggered()'), self.onBibleNewClick)
        self.ImportBibleItem.setVisible(False)

    def add_export_menu_item(self, export_menu):
        self.ExportBibleItem = QtGui.QAction(export_menu)
        self.ExportBibleItem.setObjectName(u'ExportBibleItem')
        export_menu.addAction(self.ExportBibleItem)
        self.ExportBibleItem.setText(export_menu.trUtf8(u'&Bible'))
        self.ExportBibleItem.setVisible(False)

    def onBibleNewClick(self):
        if self.media_item is not None:
            self.media_item.onNewClick()

    def about(self):
        about_text = self.trUtf8(u'<strong>Bible Plugin</strong><br />This '
            u'plugin allows bible verses from different sources to be '
            u'displayed on the screen during the service.')
        return about_text
