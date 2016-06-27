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
import multiprocessing

log = logging.getLogger(__name__)


class TestPylint(TestCase):

    def test_pylint(self):
        """
        Test for pylint errors
        """
        # GIVEN: The openlp base folder
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'openlp'))

        # WHEN: Running pylint 
        (pylint_stdout, pylint_stderr) = lint.py_run('{path} --disable=all  --enable=missing-format-argument-key,unused-format-string-argument -r n -j {cpu_count}'.format(path='openlp', cpu_count=multiprocessing.cpu_count()), return_std=True)
        stdout = pylint_stdout.read()
        stderr = pylint_stderr.read()
        log.debug(stdout)
        log.debug(stderr)

        # THEN: The output should be empty
        self.assertEqual(stdout, '', 'PyLint should find no errors')
