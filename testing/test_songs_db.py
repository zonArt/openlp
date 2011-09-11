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
Songs database tests
"""

import pytest
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import UnmappedInstanceError

from openlp.plugins.songs.lib.db import Author, Book, MediaFile, Song, Topic


def test_empty_songdb(openlp_runner):
    db = openlp_runner.get_songs_db(empty=True)
    g = db.get_all_objects
    assert g(Author) == []
    assert g(Book) == []
    assert g(MediaFile) == []
    assert g(Song) == []
    assert g(Topic) == []
    c = db.get_object_count
    assert c(Author) == 0
    assert c(Book) == 0
    assert c(MediaFile) == 0
    assert c(Song) == 0
    assert c(Topic) == 0


def test_unmapped_class(openlp_runner):
    # test class not mapped to any sqlalchemy table
    class A(object):
        pass
    db = openlp_runner.get_songs_db(empty=True)
    assert db.save_object(A()) == False
    assert db.save_objects([A(), A()]) == False
    # no key - new object instance is created from supplied class
    assert type(db.get_object(A, key=None)) == A

    with pytest.raises(InvalidRequestError):
        db.get_object(A, key=1)
    with pytest.raises(InvalidRequestError):
        db.get_object_filtered(A, filter_clause=None)
    with pytest.raises(InvalidRequestError):
        db.get_all_objects(A)
    with pytest.raises(InvalidRequestError):
        db.get_object_count(A)

    assert db.delete_object(A, key=None) == False
    assert db.delete_all_objects(A) == False
