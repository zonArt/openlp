# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
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
The :mod:`formattingtagform` provides an Tag Edit facility. The Base set are protected and included each time loaded.
Custom tags can be defined and saved. The Custom Tag arrays are saved in a json string so QSettings works on them.
Base Tags cannot be changed.
"""
from PyQt4 import QtGui

from openlp.core.lib import FormattingTags, translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui.formattingtagdialog import Ui_FormattingTagDialog


class FormattingTagForm(QtGui.QDialog, Ui_FormattingTagDialog):
    """
    The :class:`FormattingTagForm` manages the settings tab .
    """
    def __init__(self, parent):
        """
        Constructor
        """
        super(FormattingTagForm, self).__init__(parent)
        self.setupUi(self)
        self.tag_table_widget.itemSelectionChanged.connect(self.on_row_selected)
        self.new_push_button.clicked.connect(self.on_new_clicked)
        self.save_push_button.clicked.connect(self.on_saved_clicked)
        self.delete_push_button.clicked.connect(self.on_delete_clicked)
        self.button_box.rejected.connect(self.close)
        self.description_line_edit.textEdited.connect(self.on_text_edited)
        self.tag_line_edit.textEdited.connect(self.on_text_edited)
        self.start_tag_line_edit.textEdited.connect(self.on_text_edited)
        self.end_tag_line_edit.textEdited.connect(self.on_text_edited)
        # Forces reloading of tags from openlp configuration.
        FormattingTags.load_tags()

    def exec_(self):
        """
        Load Display and set field state.
        """
        # Create initial copy from master
        self._reloadTable()
        self.selected = -1
        return QtGui.QDialog.exec_(self)

    def on_row_selected(self):
        """
        Table Row selected so display items and set field state.
        """
        self.save_push_button.setEnabled(False)
        self.selected = self.tag_table_widget.currentRow()
        html = FormattingTags.get_html_tags()[self.selected]
        self.description_line_edit.setText(html['desc'])
        self.tag_line_edit.setText(self._strip(html['start tag']))
        self.start_tag_line_edit.setText(html['start html'])
        self.end_tag_line_edit.setText(html['end html'])
        if html['protected']:
            self.description_line_edit.setEnabled(False)
            self.tag_line_edit.setEnabled(False)
            self.start_tag_line_edit.setEnabled(False)
            self.end_tag_line_edit.setEnabled(False)
            self.delete_push_button.setEnabled(False)
        else:
            self.description_line_edit.setEnabled(True)
            self.tag_line_edit.setEnabled(True)
            self.start_tag_line_edit.setEnabled(True)
            self.end_tag_line_edit.setEnabled(True)
            self.delete_push_button.setEnabled(True)

    def on_text_edited(self, text):
        """
        Enable the ``save_push_button`` when any of the selected tag's properties
        has been changed.
        """
        self.save_push_button.setEnabled(True)

    def on_new_clicked(self):
        """
        Add a new tag to list only if it is not a duplicate.
        """
        for html in FormattingTags.get_html_tags():
            if self._strip(html['start tag']) == 'n':
                critical_error_message_box(
                    translate('OpenLP.FormattingTagForm', 'Update Error'),
                    translate('OpenLP.FormattingTagForm', 'Tag "n" already defined.'))
                return
        # Add new tag to list
        tag = {
            'desc': translate('OpenLP.FormattingTagForm', 'New Tag'),
            'start tag': '{n}',
            'start html': translate('OpenLP.FormattingTagForm', '<HTML here>'),
            'end tag': '{/n}',
            'end html': translate('OpenLP.FormattingTagForm', '</and here>'),
            'protected': False,
            'temporary': False
        }
        FormattingTags.add_html_tags([tag])
        FormattingTags.save_html_tags()
        self._reloadTable()
        # Highlight new row
        self.tag_table_widget.selectRow(self.tag_table_widget.rowCount() - 1)
        self.on_row_selected()
        self.tag_table_widget.scrollToBottom()

    def on_delete_clicked(self):
        """
        Delete selected custom tag.
        """
        if self.selected != -1:
            FormattingTags.remove_html_tag(self.selected)
            # As the first items are protected we should not have to take care
            # of negative indexes causing tracebacks.
            self.tag_table_widget.selectRow(self.selected - 1)
            self.selected = -1
            FormattingTags.save_html_tags()
            self._reloadTable()

    def on_saved_clicked(self):
        """
        Update Custom Tag details if not duplicate and save the data.
        """
        html_expands = FormattingTags.get_html_tags()
        if self.selected != -1:
            html = html_expands[self.selected]
            tag = self.tag_line_edit.text()
            for linenumber, html1 in enumerate(html_expands):
                if self._strip(html1['start tag']) == tag and linenumber != self.selected:
                    critical_error_message_box(
                        translate('OpenLP.FormattingTagForm', 'Update Error'),
                        translate('OpenLP.FormattingTagForm', 'Tag %s already defined.') % tag)
                    return
            html['desc'] = self.description_line_edit.text()
            html['start html'] = self.start_tag_line_edit.text()
            html['end html'] = self.end_tag_line_edit.text()
            html['start tag'] = '{%s}' % tag
            html['end tag'] = '{/%s}' % tag
            # Keep temporary tags when the user changes one.
            html['temporary'] = False
            self.selected = -1
        FormattingTags.save_html_tags()
        self._reloadTable()

    def _reloadTable(self):
        """
        Reset List for loading.
        """
        self.tag_table_widget.clearContents()
        self.tag_table_widget.setRowCount(0)
        self.new_push_button.setEnabled(True)
        self.save_push_button.setEnabled(False)
        self.delete_push_button.setEnabled(False)
        for linenumber, html in enumerate(FormattingTags.get_html_tags()):
            self.tag_table_widget.setRowCount(self.tag_table_widget.rowCount() + 1)
            self.tag_table_widget.setItem(linenumber, 0, QtGui.QTableWidgetItem(html['desc']))
            self.tag_table_widget.setItem(linenumber, 1, QtGui.QTableWidgetItem(self._strip(html['start tag'])))
            self.tag_table_widget.setItem(linenumber, 2, QtGui.QTableWidgetItem(html['start html']))
            self.tag_table_widget.setItem(linenumber, 3, QtGui.QTableWidgetItem(html['end html']))
            # Permanent (persistent) tags do not have this key.
            if 'temporary' not in html:
                html['temporary'] = False
            self.tag_table_widget.resizeRowsToContents()
        self.description_line_edit.setText('')
        self.tag_line_edit.setText('')
        self.start_tag_line_edit.setText('')
        self.end_tag_line_edit.setText('')
        self.description_line_edit.setEnabled(False)
        self.tag_line_edit.setEnabled(False)
        self.start_tag_line_edit.setEnabled(False)
        self.end_tag_line_edit.setEnabled(False)

    def _strip(self, tag):
        """
        Remove tag wrappers for editing.
        """
        tag = tag.replace('{', '')
        tag = tag.replace('}', '')
        return tag
