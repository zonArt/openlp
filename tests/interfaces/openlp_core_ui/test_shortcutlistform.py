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
Package to test the openlp.core.ui.shortcutform package.
"""
from unittest import TestCase

from PyQt5 import QtCore, QtGui, QtWidgets

from openlp.core.common import Registry
from openlp.core.ui.shortcutlistform import ShortcutListForm

from tests.interfaces import MagicMock, patch
from tests.helpers.testmixin import TestMixin


class TestShortcutform(TestCase, TestMixin):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.setup_application()
        self.main_window = QtWidgets.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.form = ShortcutListForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window

    def adjust_button_test(self):
        """
        Test the _adjust_button() method
        """
        # GIVEN: A button.
        button = QtWidgets.QPushButton()
        checked = True
        enabled = True
        text = 'new!'

        # WHEN: Call the method.
        with patch('PyQt5.QtWidgets.QPushButton.setChecked') as mocked_check_method:
            self.form._adjust_button(button, checked, enabled, text)

            # THEN: The button should be changed.
            self.assertEqual(button.text(), text, 'The text should match.')
            mocked_check_method.assert_called_once_with(True)
            self.assertEqual(button.isEnabled(), enabled, 'The button should be disabled.')

    def space_key_press_event_test(self):
        """
        Test the keyPressEvent when the spacebar was pressed
        """
        # GIVEN: A key event that is a space
        mocked_event = MagicMock()
        mocked_event.key.return_value = QtCore.Qt.Key_Space

        # WHEN: The event is handled
        with patch.object(self.form, 'keyReleaseEvent') as mocked_key_release_event:
            self.form.keyPressEvent(mocked_event)

            # THEN: The key should be released
            mocked_key_release_event.assert_called_with(mocked_event)
            self.assertEqual(0, mocked_event.accept.call_count)

    def primary_push_button_checked_key_press_event_test(self):
        """
        Test the keyPressEvent when the primary push button is checked
        """
        # GIVEN: The primary push button is checked
        with patch.object(self.form, 'keyReleaseEvent') as mocked_key_release_event, \
                patch.object(self.form.primary_push_button, 'isChecked') as mocked_is_checked:
            mocked_is_checked.return_value = True
            mocked_event = MagicMock()

            # WHEN: The event is handled
            self.form.keyPressEvent(mocked_event)

            # THEN: The key should be released
            mocked_key_release_event.assert_called_with(mocked_event)
            self.assertEqual(0, mocked_event.accept.call_count)

    def alternate_push_button_checked_key_press_event_test(self):
        """
        Test the keyPressEvent when the alternate push button is checked
        """
        # GIVEN: The primary push button is checked
        with patch.object(self.form, 'keyReleaseEvent') as mocked_key_release_event, \
                patch.object(self.form.alternate_push_button, 'isChecked') as mocked_is_checked:
            mocked_is_checked.return_value = True
            mocked_event = MagicMock()

            # WHEN: The event is handled
            self.form.keyPressEvent(mocked_event)

            # THEN: The key should be released
            mocked_key_release_event.assert_called_with(mocked_event)
            self.assertEqual(0, mocked_event.accept.call_count)

    def escape_key_press_event_test(self):
        """
        Test the keyPressEvent when the escape key was pressed
        """
        # GIVEN: A key event that is an escape
        mocked_event = MagicMock()
        mocked_event.key.return_value = QtCore.Qt.Key_Escape

        # WHEN: The event is handled
        with patch.object(self.form, 'close') as mocked_close:
            self.form.keyPressEvent(mocked_event)

            # THEN: The key should be released
            mocked_event.accept.assert_called_with()
            mocked_close.assert_called_with()

    def on_default_radio_button_not_toggled_test(self):
        """
        Test that the default radio button method exits early when the button is not toggled
        """
        # GIVEN: A not-toggled custom radio button
        with patch.object(self.form, '_current_item_action') as mocked_current_item_action:

            # WHEN: The clicked method is called
            self.form.on_default_radio_button_clicked(False)

            # THEN: The method should exit early (i.e. the rest of the methods are not called)
            self.assertEqual(0, mocked_current_item_action.call_count)

    def on_default_radio_button_clicked_no_action_test(self):
        """
        Test that nothing happens when an action hasn't been selected and you click the default radio button
        """
        # GIVEN: Some mocked out methods, a current action, and some shortcuts
        with patch.object(self.form, '_current_item_action') as mocked_current_item_action, \
                patch.object(self.form, '_action_shortcuts') as mocked_action_shortcuts:
            mocked_current_item_action.return_value = None

            # WHEN: The default radio button is clicked
            self.form.on_default_radio_button_clicked(True)

            # THEN: The method should exit early (i.e. the rest of the methods are not called)
            mocked_current_item_action.assert_called_with()
            self.assertEqual(0, mocked_action_shortcuts.call_count)

    def on_default_radio_button_clicked_test(self):
        """
        Test that the values are copied across correctly when the default radio button is selected
        """
        # GIVEN: Some mocked out methods, a current action, and some shortcuts
        with patch.object(self.form, '_current_item_action') as mocked_current_item_action, \
                patch.object(self.form, '_action_shortcuts') as mocked_action_shortcuts, \
                patch.object(self.form, 'refresh_shortcut_list') as mocked_refresh_shortcut_list, \
                patch.object(self.form, 'get_shortcut_string') as mocked_get_shortcut_string, \
                patch.object(self.form.primary_push_button, 'setText') as mocked_set_text:
            mocked_action = MagicMock()
            mocked_action.default_shortcuts = [QtCore.Qt.Key_Escape]
            mocked_current_item_action.return_value = mocked_action
            mocked_action_shortcuts.return_value = [QtCore.Qt.Key_Escape]
            mocked_get_shortcut_string.return_value = 'Esc'

            # WHEN: The default radio button is clicked
            self.form.on_default_radio_button_clicked(True)

            # THEN: The shorcuts should be copied across
            mocked_current_item_action.assert_called_with()
            mocked_action_shortcuts.assert_called_with(mocked_action)
            mocked_refresh_shortcut_list.assert_called_with()
            mocked_set_text.assert_called_with('Esc')

    def on_custom_radio_button_not_toggled_test(self):
        """
        Test that the custom radio button method exits early when the button is not toggled
        """
        # GIVEN: A not-toggled custom radio button
        with patch.object(self.form, '_current_item_action') as mocked_current_item_action:

            # WHEN: The clicked method is called
            self.form.on_custom_radio_button_clicked(False)

            # THEN: The method should exit early (i.e. the rest of the methods are not called)
            self.assertEqual(0, mocked_current_item_action.call_count)

    def on_custom_radio_button_clicked_test(self):
        """
        Test that the values are copied across correctly when the custom radio button is selected
        """
        # GIVEN: Some mocked out methods, a current action, and some shortcuts
        with patch.object(self.form, '_current_item_action') as mocked_current_item_action, \
                patch.object(self.form, '_action_shortcuts') as mocked_action_shortcuts, \
                patch.object(self.form, 'refresh_shortcut_list') as mocked_refresh_shortcut_list, \
                patch.object(self.form, 'get_shortcut_string') as mocked_get_shortcut_string, \
                patch.object(self.form.primary_push_button, 'setText') as mocked_set_text:
            mocked_action = MagicMock()
            mocked_current_item_action.return_value = mocked_action
            mocked_action_shortcuts.return_value = [QtCore.Qt.Key_Escape]
            mocked_get_shortcut_string.return_value = 'Esc'

            # WHEN: The custom radio button is clicked
            self.form.on_custom_radio_button_clicked(True)

            # THEN: The shorcuts should be copied across
            mocked_current_item_action.assert_called_with()
            mocked_action_shortcuts.assert_called_with(mocked_action)
            mocked_refresh_shortcut_list.assert_called_with()
            mocked_set_text.assert_called_with('Esc')
