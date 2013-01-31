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
    def setupUi(self, editBibleDialog):
        editBibleDialog.setObjectName(u'editBibleDialog')
        editBibleDialog.resize(520, 400)
        editBibleDialog.setWindowIcon(build_icon(u':/icon/openlp-logo-16x16.png'))
        editBibleDialog.setModal(True)
        self.dialogLayout = QtGui.QVBoxLayout(editBibleDialog)
        self.dialogLayout.setSpacing(8)
        self.dialogLayout.setContentsMargins(8, 8, 8, 8)
        self.dialogLayout.setObjectName(u'dialog_layout')
        self.bibleTabWidget = QtGui.QTabWidget(editBibleDialog)
        self.bibleTabWidget.setObjectName(u'BibleTabWidget')
        # Meta tab
        self.metaTab = QtGui.QWidget()
        self.metaTab.setObjectName(u'metaTab')
        self.metaTabLayout = QtGui.QVBoxLayout(self.metaTab)
        self.metaTabLayout.setObjectName(u'metaTabLayout')
        self.licenseDetailsGroupBox = QtGui.QGroupBox(self.metaTab)
        self.licenseDetailsGroupBox.setObjectName(u'licenseDetailsGroupBox')
        self.licenseDetailsLayout = QtGui.QFormLayout(self.licenseDetailsGroupBox)
        self.licenseDetailsLayout.setObjectName(u'licenseDetailsLayout')
        self.versionNameLabel = QtGui.QLabel(self.licenseDetailsGroupBox)
        self.versionNameLabel.setObjectName(u'versionNameLabel')
        self.versionNameEdit = QtGui.QLineEdit(self.licenseDetailsGroupBox)
        self.versionNameEdit.setObjectName(u'versionNameEdit')
        self.versionNameLabel.setBuddy(self.versionNameEdit)
        self.licenseDetailsLayout.addRow(self.versionNameLabel, self.versionNameEdit)
        self.copyrightLabel = QtGui.QLabel(self.licenseDetailsGroupBox)
        self.copyrightLabel.setObjectName(u'copyrightLabel')
        self.copyrightEdit = QtGui.QLineEdit(self.licenseDetailsGroupBox)
        self.copyrightEdit.setObjectName(u'copyrightEdit')
        self.copyrightLabel.setBuddy(self.copyrightEdit)
        self.licenseDetailsLayout.addRow(self.copyrightLabel, self.copyrightEdit)
        self.permissionsLabel = QtGui.QLabel(self.licenseDetailsGroupBox)
        self.permissionsLabel.setObjectName(u'permissionsLabel')
        self.permissionsEdit = QtGui.QLineEdit(self.licenseDetailsGroupBox)
        self.permissionsEdit.setObjectName(u'permissionsEdit')
        self.permissionsLabel.setBuddy(self.permissionsEdit)
        self.licenseDetailsLayout.addRow(self.permissionsLabel, self.permissionsEdit)
        self.metaTabLayout.addWidget(self.licenseDetailsGroupBox)
        self.languageSelectionGroupBox = QtGui.QGroupBox(self.metaTab)
        self.languageSelectionGroupBox.setObjectName(u'languageSelectionGroupBox')
        self.languageSelectionLayout = QtGui.QVBoxLayout(self.languageSelectionGroupBox)
        self.languageSelectionLabel = QtGui.QLabel(self.languageSelectionGroupBox)
        self.languageSelectionLabel.setObjectName(u'languageSelectionLabel')
        self.languageSelectionComboBox = QtGui.QComboBox(self.languageSelectionGroupBox)
        self.languageSelectionComboBox.setObjectName(u'languageSelectionComboBox')
        self.languageSelectionComboBox.addItems([u'', u'', u'', u''])
        self.languageSelectionLayout.addWidget(self.languageSelectionLabel)
        self.languageSelectionLayout.addWidget(self.languageSelectionComboBox)
        self.metaTabLayout.addWidget(self.languageSelectionGroupBox)
        self.metaTabLayout.addStretch()
        self.bibleTabWidget.addTab(self.metaTab, u'')
        # Book name tab
        self.bookNameTab = QtGui.QWidget()
        self.bookNameTab.setObjectName(u'bookNameTab')
        self.bookNameTabLayout = QtGui.QVBoxLayout(self.bookNameTab)
        self.bookNameTabLayout.setObjectName(u'bookNameTabLayout')
        self.bookNameNotice = QtGui.QLabel(self.bookNameTab)
        self.bookNameNotice.setObjectName(u'bookNameNotice')
        self.bookNameNotice.setWordWrap(True)
        self.bookNameTabLayout.addWidget(self.bookNameNotice)
        self.scrollArea = QtGui.QScrollArea(self.bookNameTab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(u'scrollArea')
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.bookNameWidget = QtGui.QWidget(self.scrollArea)
        self.bookNameWidget.setObjectName(u'bookNameWidget')
        self.bookNameWidgetLayout = QtGui.QFormLayout(self.bookNameWidget)
        self.bookNameWidgetLayout.setObjectName(u'bookNameWidgetLayout')
        self.bookNameLabel = {}
        self.bookNameEdit= {}
        for book in BiblesResourcesDB.get_books():
            self.bookNameLabel[book[u'abbreviation']] = QtGui.QLabel(self.bookNameWidget)
            self.bookNameLabel[book[u'abbreviation']].setObjectName(u'bookNameLabel[%s]' % book[u'abbreviation'])
            self.bookNameEdit[book[u'abbreviation']] = QtGui.QLineEdit(self.bookNameWidget)
            self.bookNameEdit[book[u'abbreviation']].setObjectName(u'bookNameEdit[%s]' % book[u'abbreviation'])
            self.bookNameWidgetLayout.addRow(
                self.bookNameLabel[book[u'abbreviation']], 
                self.bookNameEdit[book[u'abbreviation']])
        self.scrollArea.setWidget(self.bookNameWidget)
        self.bookNameTabLayout.addWidget(self.scrollArea)
        self.bookNameTabLayout.addStretch()
        self.bibleTabWidget.addTab(self.bookNameTab, u'')
        # Last few bits
        self.dialogLayout.addWidget(self.bibleTabWidget)
        self.button_box = create_button_box(editBibleDialog, u'button_box', [u'cancel', u'save'])
        self.dialogLayout.addWidget(self.button_box)
        self.retranslateUi(editBibleDialog)
        QtCore.QMetaObject.connectSlotsByName(editBibleDialog)

    def retranslateUi(self, editBibleDialog):
        self.book_names = BibleStrings().BookNames
        editBibleDialog.setWindowTitle(translate('BiblesPlugin.EditBibleForm', 'Bible Editor'))
        # Meta tab
        self.bibleTabWidget.setTabText( self.bibleTabWidget.indexOf(self.metaTab),
            translate('SongsPlugin.EditBibleForm', 'Meta Data'))
        self.licenseDetailsGroupBox.setTitle(translate('BiblesPlugin.EditBibleForm', 'License Details'))
        self.versionNameLabel.setText(translate('BiblesPlugin.EditBibleForm', 'Version name:'))
        self.copyrightLabel.setText(translate('BiblesPlugin.EditBibleForm', 'Copyright:'))
        self.permissionsLabel.setText(translate('BiblesPlugin.EditBibleForm', 'Permissions:'))
        self.languageSelectionGroupBox.setTitle(translate('BiblesPlugin.EditBibleForm', 'Default Bible Language'))
        self.languageSelectionLabel.setText(translate('BiblesPlugin.EditBibleForm',
            'Book name language in search field, search results and on display:'))
        self.languageSelectionComboBox.setItemText(0, translate('BiblesPlugin.EditBibleForm', 'Global Settings'))
        self.languageSelectionComboBox.setItemText(LanguageSelection.Bible + 1,
            translate('BiblesPlugin.EditBibleForm', 'Bible Language'))
        self.languageSelectionComboBox.setItemText(LanguageSelection.Application + 1,
            translate('BiblesPlugin.EditBibleForm', 'Application Language'))
        self.languageSelectionComboBox.setItemText(LanguageSelection.English + 1,
            translate('BiblesPlugin.EditBibleForm', 'English'))
        # Book name tab
        self.bibleTabWidget.setTabText(self.bibleTabWidget.indexOf(self.bookNameTab),
            translate('SongsPlugin.EditBibleForm', 'Custom Book Names'))
        for book in BiblesResourcesDB.get_books():
            self.bookNameLabel[book[u'abbreviation']].setText(u'%s:' % unicode(self.book_names[book[u'abbreviation']]))
