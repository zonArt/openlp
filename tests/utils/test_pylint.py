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
import platform
import sys
from unittest import TestCase, SkipTest

try:
    from pylint import epylint as lint
    from pylint.__pkginfo__ import version
except ImportError:
    raise SkipTest('pylint not installed - skipping tests using pylint.')

from openlp.core.common import is_win

in_argv = False
for arg in sys.argv:
    if arg.endswith('test_pylint.py'):
        in_argv = True
        break
if not in_argv:
    raise SkipTest('test_pylint.py not specified in arguments - skipping tests using pylint.')

TOLERATED_ERRORS = {'registryproperties.py': ['access-member-before-definition'],
                    'opensong.py': ['no-name-in-module'],
                    'maindisplay.py': ['no-name-in-module']}


class TestPylint(TestCase):

    def test_pylint(self):
        """
        Test for pylint errors
        """
        # GIVEN: Some checks to disable and enable, and the pylint script
        disabled_checks = 'import-error,no-member'
        enabled_checks = 'missing-format-argument-key,unused-format-string-argument,bad-format-string'
        if is_win() or 'arch' in platform.dist()[0].lower():
            pylint_script = 'pylint'
        else:
            pylint_script = 'pylint3'

        # WHEN: Running pylint
        (pylint_stdout, pylint_stderr) = \
            lint.py_run('openlp --errors-only --disable={disabled} --enable={enabled} '
                        '--reports=no --output-format=parseable'.format(disabled=disabled_checks,
                                                                        enabled=enabled_checks),
                        return_std=True, script=pylint_script)
        stdout = pylint_stdout.read()
        stderr = pylint_stderr.read()
        filtered_stdout = self._filter_tolerated_errors(stdout)
        print(filtered_stdout)
        print(stderr)

        # THEN: The output should be empty
        self.assertTrue(filtered_stdout == '', 'PyLint should find no errors')

    def _filter_tolerated_errors(self, pylint_output):
        """
        Filter out errors we tolerate.
        """
        filtered_output = ''
        for line in pylint_output.splitlines():
            # Filter out module info lines
            if line.startswith('**'):
                continue
            # Filter out undefined-variable error releated to WindowsError
            elif 'undefined-variable' in line and 'WindowsError' in line:
                continue
            # Filter out PyQt related errors
            elif ('no-name-in-module' in line or 'no-member' in line) and 'PyQt5' in line:
                continue
            elif self._is_line_tolerated(line):
                continue
            else:
                filtered_output += line + '\n'
        return filtered_output.strip()

    def _is_line_tolerated(self, line):
        """
        Check if line constains a tolerated error
        """
        for filename in TOLERATED_ERRORS:
            for tolerated_error in TOLERATED_ERRORS[filename]:
                if filename in line and tolerated_error in line:
                    return True
        return False
