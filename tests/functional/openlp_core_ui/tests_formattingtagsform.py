"""
Package to test the openlp.core.ui.formattingtagsform package.
"""
from unittest import TestCase

from mock import MagicMock, patch

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

