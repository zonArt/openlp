#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Millar, Stevan Pettit, Andreas Preikschat, Mattias     #
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
OpenLyrics import/export tests
"""

from lxml import etree

from openlp.plugins.songs.lib.db import Song
from openlp.plugins.songs.lib import OpenLyrics


def test_openlyrics_export(openlp_runner, openlyrics_validator, pth, tmpdir):
    # export song to file
    f = tmpdir.join('out.xml')
    db = openlp_runner.get_songs_db()
    s = db.get_all_objects(Song)[0]
    o = OpenLyrics(db)
    xml = o.song_to_xml(s)
    tree = etree.ElementTree(etree.fromstring(xml))
    tree.write(open(f.strpath, u'w'), encoding=u'utf-8', xml_declaration=True,
        pretty_print=True)
    # validate file
    assert openlyrics_validator.validate(f.strpath) == True
    # string comparison with original file line by line
    f_orig = pth.songs.join('openlyrics_test_1.xml')
    for l, l_orig in zip(f.readlines(), f_orig.readlines()):
        # skip line with item modifiedDate - it is unique everytime
        if l.startswith('<song xmlns='):
            continue
        assert l == l_orig
