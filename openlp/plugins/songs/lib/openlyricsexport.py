## -*- coding: utf-8 -*-
## vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
#
################################################################################
## OpenLP - Open Source Lyrics Projection                                      #
## --------------------------------------------------------------------------- #
## Copyright (c) 2008-2011 Raoul Snyman                                        #
## Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
## Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
## Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
## Carsten Tinggaard, Frode Woldsund                                           #
## --------------------------------------------------------------------------- #
## This program is free software; you can redistribute it and/or modify it     #
## under the terms of the GNU General Public License as published by the Free  #
## Software Foundation; version 2 of the License.                              #
##                                                                             #
## This program is distributed in the hope that it will be useful, but WITHOUT #
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
## FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
## more details.                                                               #
##                                                                             #
## You should have received a copy of the GNU General Public License along     #
## with this program; if not, write to the Free Software Foundation, Inc., 59  #
## Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
################################################################################
#"""
#The :mod:`openlyricsexport` module provides the functionality for exporting
#songs from the database.
#"""
#
#import logging
#import os
#
#from lxml import etree
#
#from openlp.core.lib import translate
#from openlp.plugins.songs.lib import OpenLyricsBuilder
#from openlp.plugins.songs.lib.songimport import SongImport
#
#log = logging.getLogger(__name__)
#
#class OpenLyricsExport(SongExport):
#    """
#    This provides the Openlyrics export.
#    """
#    def __init__(self, master_manager, songs=None, save_path=u''):
#        """
#        Initialise the export.
#        """
#        log.debug(u'initialise OpenLyricsExport')
#        SongExport.__init__(self, master_manager)
#        self.master_manager = master_manager
#        self.songs = songs
#        self.save_path = save_path
#
#    def do_export(self):
#        """
#        Exports the songs.
#        """
#        openLyricsBuilder = OpenLyricsBuilder(self.master_manager)
#        self.export_wizard.exportProgressBar.setMaximum(len(songs))
#        for song in self.songs:
#            if self.stop_export_flag:
#                return False
#            self.import_wizard.incrementProgressBar(unicode(translate(
#                'SongsPlugin.OpenLyricsExport', 'Importing %s...')) %
#                song.title)
#            xml = openLyricsBuilder.song_to_xml(song, True)
#            tree = etree.ElementTree(etree.fromstring(xml))
#            path = os.path.join(self.save_path, song.title)
#            tree.write(path)
#        return True
