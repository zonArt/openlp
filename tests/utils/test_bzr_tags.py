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
from unittest import TestCase

from subprocess import Popen, PIPE

TAGS1 = {'1.9.0', '1.9.1', '1.9.2', '1.9.3', '1.9.4', '1.9.5', '1.9.6', '1.9.7', '1.9.8', '1.9.9', '1.9.10',
         '1.9.11', '1.9.12', '2.0', '2.1.0', '2.1.1', '2.1.2', '2.1.3', '2.1.4', '2.1.5', '2.1.6', '2.2'
         }


class TestBzrTags(TestCase):

    def bzr_tags_test(self):
        """
        Test for proper bzr tags
        """
        # GIVEN: A bzr branch
        path = os.path.dirname(__file__)

        # WHEN getting the branches tags
        bzr = Popen(('bzr', 'tags', '--directory=' + path), stdout=PIPE)
        std_out = bzr.communicate()[0]
        count = len(TAGS1)
        tags = [line.decode('utf-8').split()[0] for line in std_out.splitlines()]
        count1 = 0
        for t in tags:
            if t in TAGS1:
                count1 += 1

        # THEN the tags should match the accepted tags
        self.assertEqual(count, count1, 'List of tags should match')
