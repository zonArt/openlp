# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

log = logging.getLogger(__name__)

class MediaDockManager(object):
    """
    Provide a repository for MediaManagerItems
    """
    def __init__(self, media_dock):
        """
        Initialise the media dock
        """
        self.media_dock = media_dock

    def add_dock(self, media_item, icon, weight):
        """
        Add a MediaManagerItem to the dock

        ``media_item``
            The item to add to the dock

        ``icon``
            An icon for this dock item
        """
        log.info(u'Adding %s dock' % media_item.title)
        self.media_dock.addItem(media_item, icon, media_item.title)

    def insert_dock(self, media_item, icon, weight):
        """
        This should insert a dock item at a given location
        This does not work as it gives a Segmentation error.
        For now add at end of stack if not present
        """
        log.debug(u'Inserting %s dock' % media_item.title)
        match = False
        for dock_index in range(0, self.media_dock.count()):
            if self.media_dock.widget(dock_index).settingsSection == \
                media_item.parent.get_text('name_lower'):
                match = True
                break
        if not match:
            self.media_dock.addItem(media_item, icon, media_item.title)

    def remove_dock(self, name):
        """
        Removes a MediaManagerItem from the dock

        ``name``
            The item to remove
        """
        log.debug(u'remove %s dock' % name)
        for dock_index in range(0, self.media_dock.count()):
            if self.media_dock.widget(dock_index):
                log.debug(u'%s %s' % (name,  self.media_dock.widget(dock_index).settingsSection))
                if self.media_dock.widget(dock_index).settingsSection == \
                    name:
                    self.media_dock.widget(dock_index).hide()
                    self.media_dock.removeItem(dock_index)
