# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
The media manager dock.
"""
import logging

from openlp.core.lib import StringContent

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
        visible_title = media_item.plugin.getString(StringContent.VisibleName)
        log.info(u'Adding %s dock' % visible_title)
        self.media_dock.addItem(media_item, icon, visible_title[u'title'])

    def insert_dock(self, media_item, icon, weight):
        """
        This should insert a dock item at a given location
        This does not work as it gives a Segmentation error.
        For now add at end of stack if not present
        """
        visible_title = media_item.plugin.getString(StringContent.VisibleName)
        log.debug(u'Inserting %s dock' % visible_title[u'title'])
        match = False
        for dock_index in range(self.media_dock.count()):
            if self.media_dock.widget(dock_index).settingsSection == media_item.plugin.name:
                match = True
                break
        if not match:
            self.media_dock.addItem(media_item, icon, visible_title[u'title'])

    def remove_dock(self, media_item):
        """
        Removes a MediaManagerItem from the dock

        ``media_item``
            The item to add to the dock
        """
        visible_title = media_item.plugin.getString(StringContent.VisibleName)
        log.debug(u'remove %s dock' % visible_title[u'title'])
        for dock_index in range(self.media_dock.count()):
            if self.media_dock.widget(dock_index):
                if self.media_dock.widget(dock_index).settingsSection == media_item.plugin.name:
                    self.media_dock.widget(dock_index).setVisible(False)
                    self.media_dock.removeItem(dock_index)
