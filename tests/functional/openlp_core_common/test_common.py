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
Functional tests to test the AppLocation class and related methods.
"""

from unittest import TestCase

from openlp.core.common import de_hump, trace_error_handler
from tests.functional import MagicMock, patch


class TestCommonFunctions(TestCase):
    """
    A test suite to test out various functions in the openlp.core.common module.
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

    def trace_error_handler_test(self):
        """
        Test the trace_error_handler() method
        """
        # GIVEN: Mocked out objects
        with patch('openlp.core.common.traceback') as mocked_traceback:
            mocked_traceback.extract_stack.return_value = [('openlp.fake', 56, None, 'trace_error_handler_test')]
            mocked_logger = MagicMock()

            # WHEN: trace_error_handler() is called
            trace_error_handler(mocked_logger)

            # THEN: The mocked_logger.error() method should have been called with the correct parameters
            mocked_logger.error.assert_called_with(
                'OpenLP Error trace\n   File openlp.fake at line 56 \n\t called trace_error_handler_test')
