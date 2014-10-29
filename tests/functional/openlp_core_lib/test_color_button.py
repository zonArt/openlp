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
This module contains tests for the openlp.core.lib.filedialog module
"""
from unittest import TestCase

from openlp.core.lib.colorbutton import ColorButton
from tests.functional import MagicMock, call, patch


class TestColorDialog(TestCase):
    """
    Test the :class:`~openlp.core.lib.colorbutton.ColorButton` class
    """
    def setUp(self):
        #self.qt_gui_patcher = patch('openlp.core.lib.colorbutton.QtGui')
        self.translate_patcher = patch('openlp.core.lib.colorbutton.translate')
        #self.mocked_qt_gui = self.qt_gui_patcher.start()
        self.mocked_translate = self.translate_patcher.start()
        self.mocked_parent = MagicMock()

    def tearDown(self):
        #self.qt_gui_patcher.stop()
        self.translate_patcher.stop()

    def constructor_test(self):
        """
        Test that constructing a basic ColorButton object works correctly
        """
        with patch.object(ColorButton, 'setToolTip') as mock_set_tool_tip:

            # GIVEN: The ColorButton class, a mocked out QtGui and mocked out parent
            self.mocked_translate.return_value = 'Tool Tip Text'

            # WHEN: An object is instantiated
            #ColorButton.setToolTip = MagicMock()
            #ColorButton.clicked = MagicMock()
            widget = ColorButton(self.mocked_parent)


            # THEN: The widget should have the correct properties
            self.assertEqual(widget.parent, self.mocked_parent,
                             'The parent should be the same as the one that the class was instianted with')
            self.assertEqual(widget._color, '#ffffff', 'The default value for _color should be #ffffff')
            b = mock_set_tool_tip.mock_calls
            mock_set_tool_tip.assert_called_once_with('Tool Tip Text')
            #d = widget.clicked.mock_calls
            #widget.clicked.connect.called_once_with(widget.on_clicked)
            #a = 1
            print(b)
