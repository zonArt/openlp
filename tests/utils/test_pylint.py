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
import platform
from unittest import TestCase, SkipTest

try:
    from pylint import epylint as lint
    from pylint.__pkginfo__ import version
except ImportError:
    raise SkipTest('pylint not installed - skipping tests using pylint.')

class TestPylint(TestCase):

    def test_pylint(self):
        """
        Test for pylint errors
        """
        # GIVEN: Some checks to disable and enable, and the pylint script
        disabled_checks = 'no-member,import-error,no-name-in-module'
        enabled_checks = 'missing-format-argument-key,unused-format-string-argument'
        if 'arch' in platform.dist()[0].lower():
            pylint_script = 'pylint'
        else:
            pylint_script = 'pylint3'

        # WHEN: Running pylint
        (pylint_stdout, pylint_stderr) = \
            lint.py_run('openlp --errors-only --disable={disabled} --enable={enabled} --reports=no --output-format=parseable'.format(
                                                                                        disabled=disabled_checks,
                                                                                        enabled=enabled_checks),
                        return_std=True, script=pylint_script)
        stdout = pylint_stdout.read()
        stderr = pylint_stderr.read()
        print(stdout)
        print(stderr)

        # THEN: The output should be empty
        self.assertTrue(stdout == 's', 'PyLint should find no errors')
