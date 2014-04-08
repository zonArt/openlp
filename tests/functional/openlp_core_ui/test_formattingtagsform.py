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
Package to test the openlp.core.ui.formattingtagsform package.
"""
from unittest import TestCase

from tests.functional import MagicMock, patch

from openlp.core.ui.formattingtagform import FormattingTagForm

# TODO: Tests Still TODO
# __init__
# exec_
# on_new_clicked
# on_delete_clicked
# on_saved_clicked
# _reloadTable


class TestFormattingTagForm(TestCase):

    def setUp(self):
        self.init_patcher = patch('openlp.core.ui.formattingtagform.FormattingTagForm.__init__')
        self.qdialog_patcher = patch('openlp.core.ui.formattingtagform.QtGui.QDialog')
        self.ui_formatting_tag_dialog_patcher = patch('openlp.core.ui.formattingtagform.Ui_FormattingTagDialog')
        self.mocked_init = self.init_patcher.start()
        self.mocked_qdialog = self.qdialog_patcher.start()
        self.mocked_ui_formatting_tag_dialog = self.ui_formatting_tag_dialog_patcher.start()
        self.mocked_init.return_value = None

    def tearDown(self):
        self.init_patcher.stop()
        self.qdialog_patcher.stop()
        self.ui_formatting_tag_dialog_patcher.stop()

    def test_on_text_edited(self):
        """
        Test that the appropriate actions are preformed when on_text_edited is called
        """

        # GIVEN: An instance of the Formatting Tag Form and a mocked save_push_button
        form = FormattingTagForm()
        form.save_button = MagicMock()

        # WHEN: on_text_edited is called with an arbitrary value
        #form.on_text_edited('text')

        # THEN: setEnabled and setDefault should have been called on save_push_button
        #form.save_button.setEnabled.assert_called_with(True)
