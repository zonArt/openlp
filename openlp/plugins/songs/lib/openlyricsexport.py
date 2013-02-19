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
The :mod:`openlyricsexport` module provides the functionality for exporting
songs from the database to the OpenLyrics format.
"""
import logging
import os

from lxml import etree

from openlp.core.lib import Registry, check_directory_exists, translate
from openlp.core.utils import clean_filename
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
        check_directory_exists(self.save_path)

    def do_export(self):
        """
        Export the songs.
        """
        log.debug(u'started OpenLyricsExport')
        openLyrics = OpenLyrics(self.manager)
        self.parent.progressBar.setMaximum(len(self.songs))
        for song in self.songs:
            self.application.process_events()
            if self.parent.stop_export_flag:
                return False
            self.parent.incrementProgressBar(translate('SongsPlugin.OpenLyricsExport', 'Exporting "%s"...') %
                song.title)
            xml = openLyrics.song_to_xml(song)
            tree = etree.ElementTree(etree.fromstring(xml))
            filename = u'%s (%s)' % (song.title, u', '.join([author.display_name for author in song.authors]))
            filename = clean_filename(filename)
            # Ensure the filename isn't too long for some filesystems
            filename = u'%s.xml' % filename[0:250 - len(self.save_path)]
            # Pass a file object, because lxml does not cope with some special
            # characters in the path (see lp:757673 and lp:744337).
            tree.write(open(os.path.join(self.save_path, filename), u'w'),
                encoding=u'utf-8', xml_declaration=True, pretty_print=True)
        return True

    def _get_application(self):
        """
        Adds the openlp to the class dynamically
        """
        if not hasattr(self, u'_application'):
            self._application = Registry().get(u'application')
        return self._application

    application = property(_get_application)
