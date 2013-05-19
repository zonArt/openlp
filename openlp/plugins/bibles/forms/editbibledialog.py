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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import build_icon, translate
from openlp.core.lib.ui import create_button_box
from openlp.plugins.bibles.lib import LanguageSelection, BibleStrings
from openlp.plugins.bibles.lib.db import BiblesResourcesDB


class Ui_EditBibleDialog(object):
    def setupUi(self, edit_bible_dialog):
        edit_bible_dialog.setObjectName(u'edit_bible_dialog')
        edit_bible_dialog.resize(520, 400)
        edit_bible_dialog.setWindowIcon(build_icon(u':/icon/openlp-logo-16x16.png'))
        edit_bible_dialog.setModal(True)
        self.dialog_layout = QtGui.QVBoxLayout(edit_bible_dialog)
        self.dialog_layout.setSpacing(8)
        self.dialog_layout.setContentsMargins(8, 8, 8, 8)
        self.dialog_layout.setObjectName(u'dialog_layout')
        self.bible_tab_widget = QtGui.QTabWidget(edit_bible_dialog)
        self.bible_tab_widget.setObjectName(u'BibleTabWidget')
        # Meta tab
        self.meta_tab = QtGui.QWidget()
        self.meta_tab.setObjectName(u'meta_tab')
        self.meta_tab_layout = QtGui.QVBoxLayout(self.meta_tab)
        self.meta_tab_layout.setObjectName(u'meta_tab_layout')
        self.license_details_group_box = QtGui.QGroupBox(self.meta_tab)
        self.license_details_group_box.setObjectName(u'license_details_group_box')
        self.license_details_layout = QtGui.QFormLayout(self.license_details_group_box)
        self.license_details_layout.setObjectName(u'license_details_layout')
        self.version_name_label = QtGui.QLabel(self.license_details_group_box)
        self.version_name_label.setObjectName(u'version_name_label')
        self.version_name_edit = QtGui.QLineEdit(self.license_details_group_box)
        self.version_name_edit.setObjectName(u'version_name_edit')
        self.version_name_label.setBuddy(self.version_name_edit)
        self.license_details_layout.addRow(self.version_name_label, self.version_name_edit)
        self.copyright_label = QtGui.QLabel(self.license_details_group_box)
        self.copyright_label.setObjectName(u'copyright_label')
        self.copyright_edit = QtGui.QLineEdit(self.license_details_group_box)
        self.copyright_edit.setObjectName(u'copyright_edit')
        self.copyright_label.setBuddy(self.copyright_edit)
        self.license_details_layout.addRow(self.copyright_label, self.copyright_edit)
        self.permissions_label = QtGui.QLabel(self.license_details_group_box)
        self.permissions_label.setObjectName(u'permissions_label')
        self.permissions_edit = QtGui.QLineEdit(self.license_details_group_box)
        self.permissions_edit.setObjectName(u'permissions_edit')
        self.permissions_label.setBuddy(self.permissions_edit)
        self.license_details_layout.addRow(self.permissions_label, self.permissions_edit)
        self.meta_tab_layout.addWidget(self.license_details_group_box)
        self.language_selection_group_box = QtGui.QGroupBox(self.meta_tab)
        self.language_selection_group_box.setObjectName(u'language_selection_group_box')
        self.language_selection_layout = QtGui.QVBoxLayout(self.language_selection_group_box)
        self.language_selection_label = QtGui.QLabel(self.language_selection_group_box)
        self.language_selection_label.setObjectName(u'language_selection_label')
        self.language_selection_combo_box = QtGui.QComboBox(self.language_selection_group_box)
        self.language_selection_combo_box.setObjectName(u'language_selection_combo_box')
        self.language_selection_combo_box.addItems([u'', u'', u'', u''])
        self.language_selection_layout.addWidget(self.language_selection_label)
        self.language_selection_layout.addWidget(self.language_selection_combo_box)
        self.meta_tab_layout.addWidget(self.language_selection_group_box)
        self.meta_tab_layout.addStretch()
        self.bible_tab_widget.addTab(self.meta_tab, u'')
        # Book name tab
        self.book_name_tab = QtGui.QWidget()
        self.book_name_tab.setObjectName(u'book_name_tab')
        self.book_name_tab_layout = QtGui.QVBoxLayout(self.book_name_tab)
        self.book_name_tab_layout.setObjectName(u'book_name_tab_layout')
        self.book_name_notice = QtGui.QLabel(self.book_name_tab)
        self.book_name_notice.setObjectName(u'book_name_notice')
        self.book_name_notice.setWordWrap(True)
        self.book_name_tab_layout.addWidget(self.book_name_notice)
        self.scroll_area = QtGui.QScrollArea(self.book_name_tab)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName(u'scroll_area')
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.book_name_widget = QtGui.QWidget(self.scroll_area)
        self.book_name_widget.setObjectName(u'book_name_widget')
        self.book_name_widget_layout = QtGui.QFormLayout(self.book_name_widget)
        self.book_name_widget_layout.setObjectName(u'book_name_widget_layout')
        self.book_name_label = {}
        self.book_name_edit= {}
        for book in BiblesResourcesDB.get_books():
            self.book_name_label[book[u'abbreviation']] = QtGui.QLabel(self.book_name_widget)
            self.book_name_label[book[u'abbreviation']].setObjectName(u'book_name_label[%s]' % book[u'abbreviation'])
            self.book_name_edit[book[u'abbreviation']] = QtGui.QLineEdit(self.book_name_widget)
            self.book_name_edit[book[u'abbreviation']].setObjectName(u'book_name_edit[%s]' % book[u'abbreviation'])
            self.book_name_widget_layout.addRow(
                self.book_name_label[book[u'abbreviation']],
                self.book_name_edit[book[u'abbreviation']])
        self.scroll_area.setWidget(self.book_name_widget)
        self.book_name_tab_layout.addWidget(self.scroll_area)
        self.book_name_tab_layout.addStretch()
        self.bible_tab_widget.addTab(self.book_name_tab, u'')
        # Last few bits
        self.dialog_layout.addWidget(self.bible_tab_widget)
        self.button_box = create_button_box(edit_bible_dialog, u'button_box', [u'cancel', u'save'])
        self.dialog_layout.addWidget(self.button_box)
        self.retranslateUi(edit_bible_dialog)
        QtCore.QMetaObject.connectSlotsByName(edit_bible_dialog)

    def retranslateUi(self, edit_bible_dialog):
        self.book_names = BibleStrings().BookNames
        edit_bible_dialog.setWindowTitle(translate('BiblesPlugin.EditBibleForm', 'Bible Editor'))
        # Meta tab
        self.bible_tab_widget.setTabText( self.bible_tab_widget.indexOf(self.meta_tab),
            translate('SongsPlugin.EditBibleForm', 'Meta Data'))
        self.license_details_group_box.setTitle(translate('BiblesPlugin.EditBibleForm', 'License Details'))
        self.version_name_label.setText(translate('BiblesPlugin.EditBibleForm', 'Version name:'))
        self.copyright_label.setText(translate('BiblesPlugin.EditBibleForm', 'Copyright:'))
        self.permissions_label.setText(translate('BiblesPlugin.EditBibleForm', 'Permissions:'))
        self.language_selection_group_box.setTitle(translate('BiblesPlugin.EditBibleForm', 'Default Bible Language'))
        self.language_selection_label.setText(translate('BiblesPlugin.EditBibleForm',
            'Book name language in search field, search results and on display:'))
        self.language_selection_combo_box.setItemText(0, translate('BiblesPlugin.EditBibleForm', 'Global Settings'))
        self.language_selection_combo_box.setItemText(LanguageSelection.Bible + 1,
            translate('BiblesPlugin.EditBibleForm', 'Bible Language'))
        self.language_selection_combo_box.setItemText(LanguageSelection.Application + 1,
            translate('BiblesPlugin.EditBibleForm', 'Application Language'))
        self.language_selection_combo_box.setItemText(LanguageSelection.English + 1,
            translate('BiblesPlugin.EditBibleForm', 'English'))
        # Book name tab
        self.bible_tab_widget.setTabText(self.bible_tab_widget.indexOf(self.book_name_tab),
            translate('SongsPlugin.EditBibleForm', 'Custom Book Names'))
        for book in BiblesResourcesDB.get_books():
            self.book_name_label[book[u'abbreviation']].setText(u'%s:' % unicode(self.book_names[book[u'abbreviation']]))
