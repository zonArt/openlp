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
Functional tests to test the AppLocation class and related methods.
"""

from unittest import TestCase

from openlp.core.common import de_hump


class TestInitFunctions(TestCase):
    """
    A test suite to test out various functions in the __init__ class.
    """
    def de_hump_conversion_test(self):
        """
        Test the de_hump function with a class name
        """
        # GIVEN: a Class name in Camel Case
        string = "MyClass"

        # WHEN: we call de_hump
        new_string = de_hump(string)

        # THEN: the new string should be converted to python format
        self.assertTrue(new_string == "my_class", 'The class name should have been converted')

    def de_hump_static_test(self):
        """
        Test the de_hump function with a python string
        """
        # GIVEN: a Class name in Camel Case
        string = "my_class"

        # WHEN: we call de_hump
        new_string = de_hump(string)

        # THEN: the new string should be converted to python format
        self.assertTrue(new_string == "my_class", 'The class name should have been preserved')
