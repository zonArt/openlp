# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
The :mod:`zionworximport` module provides the functionality for importing
ZionWorx songs into the OpenLP database.
"""
import logging
import re

from lxml import etree

from openlp.core.lib import translate
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

class ZionWorxImport(SongImport):
    """
    The :class:`ZionWorxImport` class provides the ability to import...
    """

    def doImport(self):
        """
        Receive ... to import.
        """
        #open xml file
        with open(self.importSource, 'rb') as f:
            songs_xml = unicode(f.read(), u'utf-8')
            # check single xml file
            if not re.match(ur' *<\?xml[^<>]*\?>', songs_xml):
                # Error: invalid file (no XML declaration)
                print u'Error: invalid file (no XML declaration)'
            else:
                # clean invalid XML
                # remove DefaultStyle attribute if non-empty
                songs_xml = re.sub(ur'DefaultStyle=".+" />', u'/>', songs_xml)
                # replace & with &amp; (skip existing entities)
                songs_xml = re.sub(ur'&(?![a-zA-Z#][a-zA-Z0-9]*;)', u'&amp;',
                    songs_xml)
                # replace < with &lt; (skip known <tags>)
                songs_xml = re.sub(ur'<(?![?DMFR/])', u'&lt;', songs_xml)
                # replace " within Lyrics attribute with &quot;
                songs_xml = re.sub(ur'(?<=Lyrics=")([^<]*)(?=" Writer=)',
                    self._escapeQuotes, songs_xml)
                print songs_xml

                # parse XML
                tree = etree.fromstring(songs_xml.encode(u'utf-8'))
                for song in tree[1].iterchildren():
                    for attrib, value in song.attrib.items():
                        print attrib + ':', value
                    print ''

    def _escapeQuotes(self, m):
        return m.group(0).replace('"', '&quot;')