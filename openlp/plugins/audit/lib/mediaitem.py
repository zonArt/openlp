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
import os

from PyQt4 import QtCore, QtGui
from openlp.core.lib import MediaManagerItem, translate, buildIcon

class AuditMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Audits.
    """
    global log
    log = logging.getLogger(u'AuditMediaItem')
    log.info(u'Audit Media Item loaded')

    def __init__(self, parent, icon, title):
        self.TranslationContext = u'AuditPlugin'
        self.PluginTextShort = u'Audit'
        self.ConfigSection = u'Audits'
        self.IconPath = u'Audit/Audit'
        self.hasFileIcon = False
        self.hasNewIcon = False
        self.hasEditIcon = False
        MediaManagerItem.__init__(self, parent, icon, title)

    def initialise(self):
        pass

    def addStartHeaderBar(self):
        self.startMessage = translate(self.TranslationContext, u'Start Collecting')
        self.addToolbarButton(self.startMessage,
        translate(self.TranslationContext, u'Start collecting alert messages '),
        u':audit/audit_start.png', self.onStartClick, u'AuditStartItem')
        self.stopMessage = translate(self.TranslationContext, u'Stop Collecting')
        self.addToolbarButton(self.stopMessage,
        translate(self.TranslationContext, u'Stop collecting alert messages '),
        u':audit/audit_stop.png', self.onStopClick, u'AuditStopItem')

    def addMiddleHeaderBar(self):
        pass

    def addListViewToToolBar(self):
        self.ListView = QtGui.QListWidget()
        self.ListView.uniformItemSizes = True
        self.ListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.ListView.setSpacing(1)
        self.ListView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.ListView.setAlternatingRowColors(True)
        self.ListView.setDragEnabled(True)
        self.ListView.setObjectName(u'AlertListView')
        #Add tp PageLayout
        self.PageLayout.addWidget(self.ListView)

    def onStartClick(self):
        self.Toolbar.actions[self.startMessage].setVisible(False)
        self.Toolbar.actions[self.stopMessage].setVisible(True)

    def onStopClick(self):
        self.Toolbar.actions[self.startMessage].setVisible(True)
        self.Toolbar.actions[self.stopMessage].setVisible(False)
