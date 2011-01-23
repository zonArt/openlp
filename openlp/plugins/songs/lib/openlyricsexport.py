# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
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
"""
The :mod:`openlyricsexport` module provides the functionality for exporting
songs from the database.
"""
import datetime
import logging
import os

from lxml import etree

from openlp.core.lib import translate
from openlp.plugins.songs.lib import OpenLyrics

log = logging.getLogger(__name__)

class OpenLyricsExport(object):
    """
    This provides the Openlyrics export.
    """
    def __init__(self, master_manager, song_ids, save_path):
        """
        Initialise the export.
        """
        log.debug(u'initialise OpenLyricsExport')
        self.master_manager = master_manager
        self.song_ids = song_ids
        self.save_path = save_path

    def do_export(self):
        """
        Export the songs.
        """
        openLyrics = OpenLyrics(self.master_manager)
        self.export_wizard.exportProgressBar.setMaximum(len(songs))
        for song in self.songs:
            if self.stop_export_flag:
                return False
            self.export_wizard.incrementProgressBar(unicode(translate(
                'SongsPlugin.OpenLyricsExport', 'Exporting %s...')) %
                song.title)
            path = os.path.join(self.save_path, song.title + u'.xml')
            xml = openLyrics.song_to_xml(song)
            # Add "IMPLEMENTED_VERSION = u'0.7" to xml.py/OpenLyrics class!
            xml.set(u'version', OpenLyrics.IMPLEMENTED_VERSION)
            xml.set(u'createdIn', u'OpenLP 1.9.4')  # Use variable
            xml.set(u'modifiedIn', u'OpenLP 1.9.4')  # Use variable
            xml.set(u'modifiedDate',
                datetime.datetime.now().strftime(u'%Y-%m-%dT%H:%M:%S'))
            tree = etree.ElementTree(etree.fromstring(xml))
            tree.write(path, encoding=u'utf-8', xml_declaration=True,
                pretty_print=True)
        return True
