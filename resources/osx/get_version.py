#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode       #
# Woldsund                                                                    #
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
import sys
import os
from bzrlib.branch import Branch

def get_version(path):
    b = Branch.open_containing(path)[0]
    b.lock_read()
    result = '0.0.0'
    try:
        # Get the branch's latest revision number.
        revno = b.revno()
        # Convert said revision number into a bzr revision id.
        revision_id = b.dotted_revno_to_revision_id((revno,))
        # Get a dict of tags, with the revision id as the key.
        tags = b.tags.get_reverse_tag_dict()
        # Check if the latest
        if revision_id in tags:
            result = tags[revision_id][0]
        else:
            result = '%s-bzr%s' % (sorted(b.tags.get_tag_dict().keys())[-1], revno)
    finally:
        b.unlock()
        return result

def get_path():
    if len(sys.argv) > 1:
        return os.path.abspath(sys.argv[1])
    else:
        return os.path.abspath('.')

if __name__ == u'__main__':
    path = get_path()
    print get_version(path)

