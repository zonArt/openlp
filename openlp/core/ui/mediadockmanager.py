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

    def addDock(self, name,  media_item, icon):
        log.info(u'Adding %s dock' % name)
        id = self.mediaDock.addItem(
                        media_item, icon, media_item.title)

    def insertDock(self, name):
        log.debug(u'Inserting %s dock' % name)
        for tab_index in range(0, self.mediaDock.count()):
            #print self.mediaDock.widget(tab_index).ConfigSection,  name
            if self.mediaDock.widget(tab_index).ConfigSection == name.lower():
                self.mediaDock.setItemEnabled(tab_index, True)

    def removeDock(self, name):
        log.debug(u'remove %s dock' % name)
        for tab_index in range(0, self.mediaDock.count()):
            #print "rd", self.mediaDock.widget(tab_index).ConfigSection, name
            if self.mediaDock.widget(tab_index).ConfigSection == name.lower():
                self.mediaDock.setItemEnabled(tab_index, False)
