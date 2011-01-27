# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
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
"""
The :mod:`openlyricsexport` module provides the functionality for exporting
songs from the database to the OpenLyrics format.
"""
import logging
import os

from lxml import etree

from openlp.core.lib import Receiver, translate
from openlp.plugins.songs.lib import OpenLyrics

log = logging.getLogger(__name__)

class OpenLyricsExport(object):
    """
    This provides the Openlyrics export.
    """
    def __init__(self, parent, songs, save_path):
        """
        Initialise the export.
        """
        log.debug(u'initialise OpenLyricsExport')
        self.parent = parent
        self.manager = parent.plugin.manager
        self.songs = songs
        self.save_path = save_path
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

    def do_export(self):
        """
        Export the songs.
        """
        log.debug(u'started OpenLyricsExport')
        openLyrics = OpenLyrics(self.manager)
        self.parent.progressBar.setMaximum(len(self.songs))
        for song in self.songs:
            Receiver.send_message(u'openlp_process_events')
            if self.parent.stop_export_flag:
                return False
            self.parent.incrementProgressBar(unicode(translate(
                'SongsPlugin.OpenLyricsExport', 'Exporting "%s"...')) %
                song.title)
            xml = openLyrics.song_to_xml(song)
            tree = etree.ElementTree(etree.fromstring(xml))
            tree.write(os.path.join(self.save_path, song.title + u'.xml'),
                encoding=u'utf-8', xml_declaration=True, pretty_print=True)
        return True
