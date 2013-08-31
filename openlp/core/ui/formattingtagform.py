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

import cgi

from PyQt4 import QtGui, QtCore

from openlp.core.lib import FormattingTags, translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui.formattingtagdialog import Ui_FormattingTagDialog
from openlp.core.ui.formattingtagcontroller import FormattingTagController


class EDITCOLUMN(object):
    """
    Hides the magic numbers for the table columns
    """
    Description = 0
    Tag = 1
    StartHtml = 2
    EndHtml = 3


class FormattingTagForm(QtGui.QDialog, Ui_FormattingTagDialog, FormattingTagController):
    """
    The :class:`FormattingTagForm` manages the settings tab .
    """
    def __init__(self, parent):
        """
        Constructor
        """
        super(FormattingTagForm, self).__init__(parent)
        self.setupUi(self)
        self.services = FormattingTagController()
        self.tag_table_widget.itemSelectionChanged.connect(self.on_row_selected)
        self.new_button.clicked.connect(self.on_new_clicked)
        self.save_button.clicked.connect(self.on_saved_clicked)
        self.delete_button.clicked.connect(self.on_delete_clicked)
        self.tag_table_widget.currentCellChanged.connect(self.on_current_cell_changed)
        self.button_box.rejected.connect(self.close)
        # Forces reloading of tags from openlp configuration.
        FormattingTags.load_tags()

    def exec_(self):
        """
        Load Display and set field state.
        """
        # Create initial copy from master
        self._reloadTable()
        return QtGui.QDialog.exec_(self)

    def on_row_selected(self):
        """
        Table Row selected so display items and set field state.
        """
        self.delete_button.setEnabled(True)

    def on_new_clicked(self):
        """
        Add a new tag to edit list and select it for editing.
        """
        new_row = self.tag_table_widget.rowCount()
        self.tag_table_widget.insertRow(new_row)
        self.tag_table_widget.setItem(new_row, 0,
            QtGui.QTableWidgetItem(translate('OpenLP.FormattingTagForm', 'New Tag')))
        self.tag_table_widget.setItem(new_row, 1,
            QtGui.QTableWidgetItem('n%s' % unicode(new_row)))
        self.tag_table_widget.setItem(new_row, 2,
            QtGui.QTableWidgetItem(translate('OpenLP.FormattingTagForm', '<HTML here>')))
        self.tag_table_widget.setItem(new_row, 3, QtGui.QTableWidgetItem(u""))
        self.tag_table_widget.resizeRowsToContents()
        self.tag_table_widget.scrollToBottom()
        self.tag_table_widget.selectRow(new_row)

    def on_delete_clicked(self):
        """
        Delete selected custom row.
        """
        selected = self.tag_table_widget.currentRow()
        if selected != -1:
            self.tag_table_widget.removeRow(selected)

    def on_saved_clicked(self):
        """
        Update Custom Tag details if not duplicate and save the data.
        """
        count = 0
        self.services.pre_save()
        while count < self.tag_table_widget.rowCount():
            result = self.services.validate_for_save(self.tag_table_widget.item(count, 0).text(),
                self.tag_table_widget.item(count, 1).text(), self.tag_table_widget.item(count, 2).text(),
                self.tag_table_widget.item(count, 3).text())
            count += 1

        html_expands = FormattingTags.get_html_tags()
        #if self.selected != -1:
        #    html = html_expands[self.selected]
        #    tag = self.tag_line_edit.text()
        #    for linenumber, html1 in enumerate(html_expands):
        #        if self._strip(html1[u'start tag']) == tag and linenumber != self.selected:
        #            critical_error_message_box(
        #                translate('OpenLP.FormattingTagForm', 'Update Error'),
        #                translate('OpenLP.FormattingTagForm', 'Tag %s already defined.') % tag)
        #            return
        #    html[u'desc'] = self.description_line_edit.text()
        #    html[u'start html'] = self.start_tag_line_edit.text()
        #    html[u'end html'] = self.end_tag_line_edit.text()
        #    html[u'start tag'] = u'{%s}' % tag
        #    html[u'end tag'] = u'{/%s}' % tag
        #    # Keep temporary tags when the user changes one.
        #    html[u'temporary'] = False
        #    self.selected = -1
        #FormattingTags.save_html_tags()
        #self._reloadTable()

    def _reloadTable(self):
        """
        Reset List for loading.
        """
        self.tag_table_widget_read.clearContents()
        self.tag_table_widget_read.setRowCount(0)
        self.tag_table_widget.clearContents()
        self.tag_table_widget.setRowCount(0)
        self.new_button.setEnabled(True)
        self.delete_button.setEnabled(False)
        for linenumber, html in enumerate(FormattingTags.get_html_tags()):
            if html[u'protected']:
                line = self.tag_table_widget_read.rowCount()
                self.tag_table_widget_read.setRowCount(line + 1)
                print linenumber, self.tag_table_widget_read.rowCount()
                self.tag_table_widget_read.setItem(line, 0, QtGui.QTableWidgetItem(html[u'desc']))
                self.tag_table_widget_read.setItem(line, 1, QtGui.QTableWidgetItem(self._strip(html[u'start tag'])))
                self.tag_table_widget_read.setItem(line, 2, QtGui.QTableWidgetItem(html[u'start html']))
                self.tag_table_widget_read.setItem(line, 3, QtGui.QTableWidgetItem(html[u'end html']))
                self.tag_table_widget_read.resizeRowsToContents()
            else:
                print self.tag_table_widget.rowCount(), html
                line = self.tag_table_widget.rowCount()
                self.tag_table_widget.setRowCount(line + 1)
                self.tag_table_widget.setItem(line, 0, QtGui.QTableWidgetItem(html[u'desc']))
                self.tag_table_widget.setItem(line, 1, QtGui.QTableWidgetItem(self._strip(html[u'start tag'])))
                self.tag_table_widget.setItem(line, 2, QtGui.QTableWidgetItem(html[u'start html']))
                self.tag_table_widget.setItem(line, 3, QtGui.QTableWidgetItem(html[u'end html']))
                self.tag_table_widget.resizeRowsToContents()
                # Permanent (persistent) tags do not have this key
                html[u'temporary'] = False

    def on_current_cell_changed(self, cur_row, cur_col, pre_row, pre_col):
        """
        This function processes all user edits in the table. It is called on each cell change.
        """
        print cur_row, cur_col, pre_col, pre_col
        # only process for editable rows
        if self.tag_table_widget.item(pre_row, 0):
            item = self.tag_table_widget.item(pre_row, pre_col)
            text = item.text()
            errors = None
            if pre_col is EDITCOLUMN.StartHtml:
                # HTML edited
                item = self.tag_table_widget.item(pre_row, 3)
                end_html = item.text()
                errors, tag = self.services.start_tag_changed(text, end_html)
                if tag:
                    self.tag_table_widget.setItem(pre_row, 3, QtGui.QTableWidgetItem(tag))
                self.tag_table_widget.resizeRowsToContents()
            elif pre_col is EDITCOLUMN.EndHtml:
                # HTML edited
                item = self.tag_table_widget.item(pre_row, 2)
                start_html = item.text()
                errors, tag = self.services.end_tag_changed(start_html, text)
                if tag:
                    self.tag_table_widget.setItem(pre_row, 3, QtGui.QTableWidgetItem(tag))
            if errors:
                QtGui.QMessageBox.warning(self,
                    translate('OpenLP.FormattingTagForm', 'Validation Error'), errors,
                    QtGui.QMessageBox.Yes|QtGui.QMessageBox.Discard|QtGui.QMessageBox.Cancel)
            self.tag_table_widget.resizeRowsToContents()
