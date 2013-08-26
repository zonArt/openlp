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
Custom tags can be defined and saved. The Custom Tag arrays are saved in a pickle so QSettings works on them. Base Tags
cannot be changed.
"""

import re
import cgi

from PyQt4 import QtGui, QtCore

from openlp.core.lib import FormattingTags, translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui.formattingtagdialog import Ui_FormattingTagDialog


class EDITCOLUMN(object):
    """
    Hides the magic numbers for the table columns
    """
    Description = 0
    Tag = 1
    StartHtml = 2
    EndHtml = 3


class FormattingTagForm(QtGui.QDialog, Ui_FormattingTagDialog):
    """
    The :class:`FormattingTagForm` manages the settings tab .
    """
    def __init__(self, parent):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.html_tag_regex = re.compile(r'<(?:(?P<close>/(?=[^\s/>]+>))?'
            r'(?P<tag>[^\s/!\?>]+)(?:\s+[^\s=]+="[^"]*")*\s*(?P<empty>/)?'
            r'|(?P<cdata>!\[CDATA\[(?:(?!\]\]>).)*\]\])'
            r'|(?P<procinst>\?(?:(?!\?>).)*\?)'
            r'|(?P<comment>!--(?:(?!-->).)*--))>', re.UNICODE)
        self.html_regex = re.compile(r'^(?:[^<>]*%s)*[^<>]*$' % self.html_tag_regex.pattern)
        self.tag_table_widget.itemSelectionChanged.connect(self.on_row_selected)
        self.new_button.clicked.connect(self.on_new_clicked)
        #self.save_push_button.clicked.connect(self.on_saved_clicked)
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
        self.tag_table_widget.setItem(new_row, 3,
            QtGui.QTableWidgetItem(translate('OpenLP.FormattingTagForm', '</and here>')))
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
        html_expands = FormattingTags.get_html_tags()
        if self.selected != -1:
            html = html_expands[self.selected]
            tag = self.tag_line_edit.text()
            for linenumber, html1 in enumerate(html_expands):
                if self._strip(html1[u'start tag']) == tag and linenumber != self.selected:
                    critical_error_message_box(
                        translate('OpenLP.FormattingTagForm', 'Update Error'),
                        translate('OpenLP.FormattingTagForm', 'Tag %s already defined.') % tag)
                    return
            html[u'desc'] = self.description_line_edit.text()
            html[u'start html'] = self.start_tag_line_edit.text()
            html[u'end html'] = self.end_tag_line_edit.text()
            html[u'start tag'] = u'{%s}' % tag
            html[u'end tag'] = u'{/%s}' % tag
            # Keep temporary tags when the user changes one.
            html[u'temporary'] = False
            self.selected = -1
        FormattingTags.save_html_tags()
        self._reloadTable()

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
                self.tag_table_widget.setRowCount(self.tag_table_widget.rowCount() + 1)
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
        pre_row_item = self.tag_table_widget.item(pre_row, 0)
        edit_item = None
        if pre_row_item and (pre_row_item.flags() & QtCore.Qt.ItemIsEditable):
            item = self.tag_table_widget.item(pre_row, pre_col)
            text = unicode(item.text())
            if pre_col is EDITCOLUMN.Tag:
                if text:
                    for row in range(self.tag_table_widget.rowCount()):
                        counting_item = self.tag_table_widget.item(row, 0)
                        if row != pre_row and counting_item and counting_item.text() == text:
                            answer = QtGui.QMessageBox.warning(self,
                                translate('OpenLP.FormattingTagForm', 'Validation Error'),
                                translate('OpenLP.FormattingTagForm',
                                    'Tag %s is already defined. Please pick a different one.' % text),
                                QtGui.QMessageBox.Discard|QtGui.QMessageBox.Ok)
                            if answer == QtGui.QMessageBox.Discard:
                                break
                            else:
                                edit_item = item
                                break
                else:
                    answer = None
                    if self.tag_table_widget.item(pre_row, 1).text() or self.tag_table_widget.item(pre_row, 2).text():
                        answer = QtGui.QMessageBox.warning(self,
                            translate('OpenLP.FormattingTagForm', 'Validation Error'),
                            translate('OpenLP.FormattingTagForm',
                                'No tag name defined. Do you want to delete the whole tag?'),
                            QtGui.QMessageBox.Yes|QtGui.QMessageBox.Discard|QtGui.QMessageBox.Cancel)
                    #if answer == QtGui.QMessageBox.Discard:
                    #    item.setText(data.get(u'tag'))
                    #if answer == QtGui.QMessageBox.Cancel:
                    #    edit_item = item
                    elif pre_row < self.tag_table_widget.rowCount() - 1:
                        self.tag_table_widget.removeRow(pre_row)
            #elif pre_col is EDITCOLUMN.StartHtml:
                # HTML edited
                #end_html = self.start_html_to_end_html(text)
                #if end_html is not None:
                #    item.setToolTip(cgi.escape(text))
                ##    if self.tag_table_widget.item(pre_row, 3) is None:
                #        self.tag_table_widget.setItem(pre_row, 3, QtGui.QTableWidgetItem(end_html))
                #   else:
                #        self.tag_table_widget.item(pre_row, 3).setText(end_html)
                #    self.tag_table_widget.item(pre_row, 3).setToolTip(cgi.escape(end_html))
                #    #data[u'html'] = text
                #    #pre_row_item.setData(QtCore.Qt.UserRole, data)
                # #   self.tag_table_widget.resizeRowsToContents()
        #if not edit_item:
        #    # select the tag cell in a empty row
        #    cur_row_item = self.tag_table_widget.item(cur_row, 0)
        #    if cur_row_item and (cur_row_item.flags() & QtCore.Qt.ItemIsEditable) and cur_row_item.text().isEmpty():
        #        edit_item = cur_row_item
        #if edit_item:
        #    self.tag_table_widget.setCurrentItem(edit_item)
        # enable delete_button for editable rows
        cur_row = self.tag_table_widget.currentRow()
        cur_row_item = self.tag_table_widget.item(cur_row, 0)
        delete_enabled = bool(cur_row_item) and bool(cur_row_item.flags() & QtCore.Qt.ItemIsEditable)
        delete_enabled &= cur_row < self.tag_table_widget.rowCount() - 1
        self.delete_button.setEnabled(delete_enabled)

    def _strip(self, tag):
        """
        Remove tag wrappers for editing.
        """
        tag = tag.replace(u'{', u'')
        tag = tag.replace(u'}', u'')
        return tag
