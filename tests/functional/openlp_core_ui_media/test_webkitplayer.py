# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
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
Package to test the openlp.core.ui.media.webkitplayer package.
"""
from unittest import TestCase

from openlp.core.ui.media.webkitplayer import WebkitPlayer
from openlp.core.common import is_macosx


class TestPhononPlayer(TestCase):
    """
    Test the functions in the :mod:`webkitplayer` module.
    """

    def check_available_test(self):
        """
        Simple test of webkitplayer availability
        """
        # GIVEN: A WebkitPlayer
        webkit_player = WebkitPlayer(None)

        # WHEN: An checking if the player is available
        available = webkit_player.check_available()

        # THEN: The player should be available, except on Mac OS X
        if is_macosx():
            self.assertEqual(False, available, 'The WebkitPlayer should not be available on Mac OS X.')
        else:
            self.assertEqual(True, available, 'The WebkitPlayer should be available on this platform.')
