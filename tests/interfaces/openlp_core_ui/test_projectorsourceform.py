#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2015 OpenLP Developers                                   #
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
    :mod: `tests.interfaces.openlp_core_ui.test_projectorsourceform` module

    Tests for the Projector Source Select form.
"""
import logging
log = logging.getLogger(__name__)
log.debug('test_projectorsourceform loaded')

from unittest import TestCase

from tests.helpers.testmixin import TestMixin
from openlp.core.lib.projector.constants import PJLINK_DEFAULT_CODES, PJLINK_DEFAULT_SOURCES

from openlp.core.ui.projector.sourceselectform import source_group


def build_source_dict():
    """
    Builds a source dictionary to verify source_group returns a valid dictionary of dictionary items

    :returns: dictionary of valid PJLink source codes grouped by PJLink source group
    """
    test_group = {}
    for group in PJLINK_DEFAULT_SOURCES.keys():
        test_group[group] = {}
    for key in PJLINK_DEFAULT_CODES:
        test_group[key[0]][key] = PJLINK_DEFAULT_CODES[key]
    return test_group


class ProjectorSourceFormTest(TestCase, TestMixin):
    """
    Test class for the Projector Source Select form module
    """
    def source_dict_test(self):
        """
        Test that source list dict returned from sourceselectform module is a valid dict with proper entries
        """
        # GIVEN: A list of inputs
        codes = []
        for item in PJLINK_DEFAULT_CODES.keys():
            codes.append(item)
        codes.sort()

        # WHEN: projector.sourceselectform.source_select() is called
        check = source_group(codes, PJLINK_DEFAULT_CODES)

        # THEN: return dictionary should match test dictionary
        self.assertEquals(check, build_source_dict(),
                          "Source group dictionary should match test dictionary")
