# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
Package to test for proper bzr tags.
"""
import os
import logging
from unittest import TestCase

from pylint import epylint as lint


class TestPylint(TestCase):

    def test_pylint(self):
        """
        Test for pylint errors
        """
        # GIVEN: The openlp base folder
        enabled_checks = 'missing-format-argument-key,unused-format-string-argument'
        disabled_checks = 'all'

        # WHEN: Running pylint
        (pylint_stdout, pylint_stderr) = \
            lint.py_run('{path} --disable={disabled} --enable={enabled} --reports=no'.format(path='openlp',
                                                                                             disabled=disabled_checks,
                                                                                             enabled=enabled_checks),
                        return_std=True)
        stdout = pylint_stdout.read()
        stderr = pylint_stderr.read()
        print(stdout)

        # THEN: The output should be empty
        self.assertTrue(stdout == '', 'PyLint should find no errors')
