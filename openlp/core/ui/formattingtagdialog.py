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
The UI widgets for the formatting tags window.
"""
from PyQt4 import QtCore, QtGui

from openlp.core.lib import UiStrings, translate, build_icon
from openlp.core.lib.ui import create_button_box


class Ui_FormattingTagDialog(object):
    """
    The UI widgets for the formatting tags window.
    """
    def setupUi(self, formatting_tag_dialog):
        """
        Set up the UI
        """
        formatting_tag_dialog.setObjectName(u'formatting_tag_dialog')
        formatting_tag_dialog.resize(725, 548)
        self.list_data_grid_layout = QtGui.QVBoxLayout(formatting_tag_dialog)
        self.list_data_grid_layout.setMargin(8)
        self.list_data_grid_layout.setObjectName(u'list_data_grid_layout')
        self.tag_table_widget_read_label = QtGui.QLabel()
        self.list_data_grid_layout.addWidget(self.tag_table_widget_read_label)
        self.tag_table_widget_read = QtGui.QTableWidget(formatting_tag_dialog)
        self.tag_table_widget_read.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tag_table_widget_read.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tag_table_widget_read.setAlternatingRowColors(True)
        self.tag_table_widget_read.setCornerButtonEnabled(False)
        self.tag_table_widget_read.setObjectName(u'tag_table_widget_read')
        self.tag_table_widget_read.setColumnCount(4)
        self.tag_table_widget_read.setRowCount(0)
        self.tag_table_widget_read.horizontalHeader().setStretchLastSection(True)
        item = QtGui.QTableWidgetItem()
        self.tag_table_widget_read.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tag_table_widget_read.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tag_table_widget_read.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tag_table_widget_read.setHorizontalHeaderItem(3, item)
        self.list_data_grid_layout.addWidget(self.tag_table_widget_read)
        self.tag_table_widget_label = QtGui.QLabel()
        self.list_data_grid_layout.addWidget(self.tag_table_widget_label)
        self.tag_table_widget = QtGui.QTableWidget(formatting_tag_dialog)
        self.tag_table_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tag_table_widget.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.tag_table_widget.setAlternatingRowColors(True)
        self.tag_table_widget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tag_table_widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tag_table_widget.setCornerButtonEnabled(False)
        self.tag_table_widget.setObjectName(u'tag_table_widget')
        self.tag_table_widget.setColumnCount(4)
        self.tag_table_widget.setRowCount(0)
        self.tag_table_widget.horizontalHeader().setStretchLastSection(True)
        item = QtGui.QTableWidgetItem()
        self.tag_table_widget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tag_table_widget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tag_table_widget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tag_table_widget.setHorizontalHeaderItem(3, item)
        self.list_data_grid_layout.addWidget(self.tag_table_widget)


        #self.horizontal_layout = QtGui.QHBoxLayout()
        #self.horizontal_layout.setObjectName(u'horizontal_layout')
        #spacer_item = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        #self.horizontal_layout.addItem(spacer_item)
        #self.delete_push_button = QtGui.QPushButton(formatting_tag_dialog)
        #self.delete_push_button.setObjectName(u'delete_push_button')
        #self.horizontal_layout.addWidget(self.delete_push_button)
        #self.list_data_grid_layout.addLayout(self.horizontal_layout, 1, 0, 1, 1)
        #self.edit_group_box = QtGui.QGroupBox(formatting_tag_dialog)
        #self.edit_group_box.setObjectName(u'edit_group_box')
        #self.data_grid_layout = QtGui.QGridLayout(self.edit_group_box)
        #self.data_grid_layout.setObjectName(u'data_grid_layout')
        #self.description_label = QtGui.QLabel(self.edit_group_box)
        #self.description_label.setAlignment(QtCore.Qt.AlignCenter)
        #self.description_label.setObjectName(u'description_label')
        #self.data_grid_layout.addWidget(self.description_label, 0, 0, 1, 1)
        #self.description_line_edit = QtGui.QLineEdit(self.edit_group_box)
        #self.description_line_edit.setObjectName(u'description_line_edit')
        #self.data_grid_layout.addWidget(self.description_line_edit, 0, 1, 2, 1)
        #self.new_push_button = QtGui.QPushButton(self.edit_group_box)
        #self.new_push_button.setObjectName(u'new_push_button')
        #self.data_grid_layout.addWidget(self.new_push_button, 0, 2, 2, 1)
        #self.tag_label = QtGui.QLabel(self.edit_group_box)
        #self.tag_label.setAlignment(QtCore.Qt.AlignCenter)
        #self.tag_label.setObjectName(u'tag_label')
        #self.data_grid_layout.addWidget(self.tag_label, 2, 0, 1, 1)
        #self.tag_line_edit = QtGui.QLineEdit(self.edit_group_box)
        #self.tag_line_edit.setMaximumSize(QtCore.QSize(50, 16777215))
        #self.tag_line_edit.setMaxLength(5)
        #self.tag_line_edit.setObjectName(u'tag_line_edit')
        #self.data_grid_layout.addWidget(self.tag_line_edit, 2, 1, 1, 1)
        #self.start_tag_label = QtGui.QLabel(self.edit_group_box)
        #self.start_tag_label.setAlignment(QtCore.Qt.AlignCenter)
        #self.start_tag_label.setObjectName(u'start_tag_label')
        #self.data_grid_layout.addWidget(self.start_tag_label, 3, 0, 1, 1)
        #self.start_tag_line_edit = QtGui.QLineEdit(self.edit_group_box)
        #self.start_tag_line_edit.setObjectName(u'start_tag_line_edit')
        #self.data_grid_layout.addWidget(self.start_tag_line_edit, 3, 1, 1, 1)
        #self.end_tag_label = QtGui.QLabel(self.edit_group_box)
        #self.end_tag_label.setAlignment(QtCore.Qt.AlignCenter)
        #self.end_tag_label.setObjectName(u'end_tag_label')
        #self.data_grid_layout.addWidget(self.end_tag_label, 4, 0, 1, 1)
        #self.end_tag_line_edit = QtGui.QLineEdit(self.edit_group_box)
        #self.end_tag_line_edit.setObjectName(u'end_tag_line_edit')
        #self.data_grid_layout.addWidget(self.end_tag_line_edit, 4, 1, 1, 1)
        #self.save_push_button = QtGui.QPushButton(self.edit_group_box)
        #self.save_push_button.setObjectName(u'save_push_button')
        #self.data_grid_layout.addWidget(self.save_push_button, 4, 2, 1, 1)
        #self.list_data_grid_layout.addWidget(self.edit_group_box, 2, 0, 1, 1)


        self.edit_button_layout = QtGui.QHBoxLayout()
        self.new_button = QtGui.QPushButton(formatting_tag_dialog)
        self.new_button.setIcon(build_icon(u':/general/general_new.png'))
        self.new_button.setObjectName(u'new_button')
        self.edit_button_layout.addWidget(self.new_button)
        self.delete_button = QtGui.QPushButton(formatting_tag_dialog)
        self.delete_button.setIcon(build_icon(u':/general/general_delete.png'))
        self.delete_button.setObjectName(u'delete_button')
        self.edit_button_layout.addWidget(self.delete_button)
        self.edit_button_layout.addStretch()
        self.list_data_grid_layout.addLayout(self.edit_button_layout)
        self.button_box = create_button_box(formatting_tag_dialog, 'button_box',
            [u'cancel', u'save', u'defaults'])
        self.save_button = self.button_box.button(QtGui.QDialogButtonBox.Save)
        self.save_button.setObjectName(u'save_button')
        self.restore_button = self.button_box.button(QtGui.QDialogButtonBox.RestoreDefaults)
        self.restore_button.setIcon(build_icon(u':/general/general_revert.png'))
        self.restore_button.setObjectName(u'restore_button')
        self.list_data_grid_layout.addWidget(self.button_box)

        #self.button_box = create_button_box(formatting_tag_dialog, u'button_box', [u'close'])
        #self.list_data_grid_layout.addWidget(self.button_box, 5, 0, 1, 1)
        #self.delete_push_button = QtGui.QPushButton(formatting_tag_dialog)
        #self.delete_push_button.setObjectName(u'delete_push_button')
        #self.list_data_grid_layout.addWidget(self.delete_push_button, 5, 0, 1, 1)

        self.retranslateUi(formatting_tag_dialog)

    def retranslateUi(self, formatting_tag_dialog):
        """
        Translate the UI on the fly
        """
        formatting_tag_dialog.setWindowTitle(translate('OpenLP.FormattingTagDialog', 'Configure Formatting Tags'))
        #self.edit_group_box.setTitle(translate('OpenLP.FormattingTagDialog', 'Edit Selection'))
        #self.save_push_button.setText(translate('OpenLP.FormattingTagDialog', 'Save'))
        #self.description_label.setText(translate('OpenLP.FormattingTagDialog', 'Description'))
        #self.tag_label.setText(translate('OpenLP.FormattingTagDialog', 'Tag'))
        #self.start_tag_label.setText(translate('OpenLP.FormattingTagDialog', 'Start HTML'))
        #self.end_tag_label.setText(translate('OpenLP.FormattingTagDialog', 'End HTML'))
        self.delete_button.setText(UiStrings().Delete)
        self.new_button.setText(UiStrings().New)
        self.tag_table_widget_read_label.setText(translate('OpenLP.FormattingTagDialog', 'Static Formatting'))
        self.tag_table_widget_read.horizontalHeaderItem(0).\
            setText(translate('OpenLP.FormattingTagDialog', 'Description'))
        self.tag_table_widget_read.horizontalHeaderItem(1).setText(translate('OpenLP.FormattingTagDialog', 'Tag'))
        self.tag_table_widget_read.horizontalHeaderItem(2).\
            setText(translate('OpenLP.FormattingTagDialog', 'Start HTML'))
        self.tag_table_widget_read.horizontalHeaderItem(3).setText(translate('OpenLP.FormattingTagDialog', 'End HTML'))
        self.tag_table_widget_read.setColumnWidth(0, 120)
        self.tag_table_widget_read.setColumnWidth(1, 80)
        self.tag_table_widget_read.setColumnWidth(2, 330)
        self.tag_table_widget_label.setText(translate('OpenLP.FormattingTagDialog', 'Custom Formatting'))
        self.tag_table_widget.horizontalHeaderItem(0).setText(translate('OpenLP.FormattingTagDialog', 'Description'))
        self.tag_table_widget.horizontalHeaderItem(1).setText(translate('OpenLP.FormattingTagDialog', 'Tag'))
        self.tag_table_widget.horizontalHeaderItem(2).setText(translate('OpenLP.FormattingTagDialog', 'Start HTML'))
        self.tag_table_widget.horizontalHeaderItem(3).setText(translate('OpenLP.FormattingTagDialog', 'End HTML'))
        self.tag_table_widget.setColumnWidth(0, 120)
        self.tag_table_widget.setColumnWidth(1, 80)
        self.tag_table_widget.setColumnWidth(2, 330)
