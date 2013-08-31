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
The :mod:`openlyricsimport` module provides the functionality for importing
songs which are saved as OpenLyrics files.
"""

import logging
import os

from lxml import etree

from openlp.core.ui.wizard import WizardStrings
from openlp.plugins.songs.lib.songimport import SongImport
from openlp.plugins.songs.lib.ui import SongStrings
from openlp.plugins.songs.lib.xml import OpenLyrics, OpenLyricsError

log = logging.getLogger(__name__)


class OpenLyricsImport(SongImport):
    """
    This provides the Openlyrics import.
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the Open Lyrics importer.
        """
        log.debug('initialise OpenLyricsImport')
        SongImport.__init__(self, manager, **kwargs)
        self.openLyrics = OpenLyrics(self.manager)

    def doImport(self):
        """
        Imports the songs.
        """
        self.import_wizard.progress_bar.setMaximum(len(self.import_source))
        parser = etree.XMLParser(remove_blank_text=True)
        for file_path in self.import_source:
            if self.stop_import_flag:
                return
            self.import_wizard.increment_progress_bar(WizardStrings.ImportingType % os.path.basename(file_path))
            try:
                # Pass a file object, because lxml does not cope with some
                # special characters in the path (see lp:757673 and lp:744337).
                parsed_file = etree.parse(open(file_path, 'r'), parser)
                xml = etree.tostring(parsed_file).decode()
                self.openLyrics.xml_to_song(xml)
            except etree.XMLSyntaxError:
                log.exception('XML syntax error in file %s' % file_path)
                self.logError(file_path, SongStrings.XMLSyntaxError)
            except OpenLyricsError as exception:
                log.exception('OpenLyricsException %d in file %s: %s'
                    % (exception.type, file_path, exception.log_message))
                self.logError(file_path, exception.display_message)
