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
Package to test the openlp.core.lib.ui package.
"""
from PyQt4 import QtGui
from unittest import TestCase

from openlp.core.lib.ui import *


class TestUi(TestCase):
    """
    Test the functions in the ui module
    """

    def test_add_welcome_page(self):
        """
        Test appending a welcome page to a wizard
        """
        # GIVEN: A wizard
        wizard = QtGui.QWizard()

        # WHEN: A welcome page has been added to the wizard
        add_welcome_page(wizard, ':/wizards/wizard_firsttime.bmp')

        # THEN: The wizard should have one page with a pixmap.
        self.assertEqual(1, len(wizard.pageIds()), 'The wizard should have one page.')
        self.assertIsInstance(wizard.page(0).pixmap(QtGui.QWizard.WatermarkPixmap), QtGui.QPixmap)

    def test_create_button_box(self):
        """
        Test creating a button box for a dialog
        """
        # GIVEN: A dialog
        dialog = QtGui.QDialog()

        # WHEN: We create the button box with five buttons
        btnbox = create_button_box(dialog, 'my_btns', ['ok', 'save', 'cancel', 'close', 'defaults'])

        # THEN: We should get a QDialogButtonBox with five buttons
        self.assertIsInstance(btnbox, QtGui.QDialogButtonBox)
        self.assertEqual(5, len(btnbox.buttons()))

        # WHEN: We create the button box with a custom button
        btnbox = create_button_box(dialog, 'my_btns', None, [QtGui.QPushButton('Custom')])
        # THEN: We should get a QDialogButtonBox with one button
        self.assertIsInstance(btnbox, QtGui.QDialogButtonBox)
        self.assertEqual(1, len(btnbox.buttons()))

        # WHEN: We create the button box with a custom button and a custom role
        btnbox = create_button_box(dialog, 'my_btns', None,
                                   [(QtGui.QPushButton('Help'), QtGui.QDialogButtonBox.HelpRole)])
        # THEN: We should get a QDialogButtonBox with one button with a certain role
        self.assertIsInstance(btnbox, QtGui.QDialogButtonBox)
        self.assertEqual(1, len(btnbox.buttons()))
        self.assertEqual(QtGui.QDialogButtonBox.HelpRole, btnbox.buttonRole(btnbox.buttons()[0]))

    def test_create_button(self):
        """
        Test creating a button
        """
        # GIVEN: A dialog
        dialog = QtGui.QDialog()
        
        # WHEN: We create the button
        btn = create_button(dialog, 'my_btn')

        # THEN: We should get a button with a name
        self.assertIsInstance(btn, QtGui.QPushButton)
        self.assertEqual('my_btn', btn.objectName())
        self.assertTrue(btn.isEnabled())

        # WHEN: We create a button with some attributes
        btn = create_button(dialog, 'my_btn', text='Hello', tooltip='How are you?', enabled=False)

        # THEN: We should get a button with those attributes
        self.assertIsInstance(btn, QtGui.QPushButton)
        self.assertEqual('Hello', btn.text())
        self.assertEqual('How are you?', btn.toolTip())
        self.assertFalse(btn.isEnabled())

        # WHEN: We create a toolbutton
        btn = create_button(dialog, 'my_btn', btn_class='toolbutton')

        # THEN: We should get a toolbutton
        self.assertIsInstance(btn, QtGui.QToolButton)
        self.assertEqual('my_btn', btn.objectName())
        self.assertTrue(btn.isEnabled())

    def test_create_valign_selection_widgets(self):
        """
        Test creating a combo box for valign selection
        """
        # GIVEN: A dialog
        dialog = QtGui.QDialog()
        
        # WHEN: We create the widgets
        label, combo = create_valign_selection_widgets(dialog)

        # THEN: We should get a label and a combobox.
        self.assertEqual(translate('OpenLP.Ui', '&Vertical Align:'), label.text())
        self.assertIsInstance(combo, QtGui.QComboBox)
        self.assertEqual(combo, label.buddy())
        for text in [UiStrings().Top, UiStrings().Middle, UiStrings().Bottom]:
            self.assertTrue(combo.findText(text) >= 0)

