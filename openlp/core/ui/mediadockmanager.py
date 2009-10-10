# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expanddock textwidth=80 dockstop=4 softdockstop=4

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
# ANY WARRANTY; without even the implied warranty of MERCHANdockILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import logging

log = logging.getLogger(u'MediaDockManager')

class MediaDockManager(object):

    def __init__(self, mediaDock):
        self.mediaDock = mediaDock

    def addDock(self, media_item, icon, weight):
        log.info(u'Adding %s dock' % media_item.title)
        id = self.mediaDock.addItem(
            media_item, icon, media_item.title)

    def insertDock(self, media_item, icon, weight):
        """
        This should insert a dock item at a given location
        This does not work as it gives a Segmentation error.
        For now add at end of stack if not present
        """
        log.debug(u'Inserting %s dock' % media_item.title)
        match = False
        for dock_index in range(0, self.mediaDock.count()):
            if self.mediaDock.widget(dock_index).ConfigSection == media_item.title.lower():
                match = True
                break
        if not match:
            self.mediaDock.addItem(media_item, icon, media_item.title)


    def removeDock(self, name):
        log.debug(u'remove %s dock' % name)
        for dock_index in range(0, self.mediaDock.count()):
            if self.mediaDock.widget(dock_index) is not None:
                if self.mediaDock.widget(dock_index).ConfigSection == name.lower():
                    self.mediaDock.widget(dock_index).hide()
                    self.mediaDock.removeItem(dock_index)
