# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
from openlp.core.lib.ui import UiStrings, create_accept_reject_button_box
from openlp.plugins.bibles.lib import LanguageSelection, BibleStrings
from openlp.plugins.bibles.lib.db import BiblesResourcesDB


class Ui_EditBibleDialog(object):
    def setupUi(self, editBibleDialog):
        editBibleDialog.setObjectName(u'editBibleDialog')
        editBibleDialog.resize(650, 400)
        editBibleDialog.setWindowIcon(
            build_icon(u':/icon/openlp-logo-16x16.png'))
        editBibleDialog.setModal(True)
        self.dialogLayout = QtGui.QVBoxLayout(editBibleDialog)
        self.dialogLayout.setSpacing(8)
        self.dialogLayout.setContentsMargins(8, 8, 8, 8)
        self.dialogLayout.setObjectName(u'dialogLayout')
        self.bibleTabWidget = QtGui.QTabWidget(editBibleDialog)
        self.bibleTabWidget.setObjectName(u'BibleTabWidget')
        # Meta tab
        self.metaTab = QtGui.QWidget()
        self.metaTab.setObjectName(u'metaTab')
        self.metaTabLayout = QtGui.QFormLayout(self.metaTab)
        self.metaTabLayout.setObjectName(u'metaTabLayout')
        self.versionNameLabel = QtGui.QLabel(self.metaTab)
        self.versionNameLabel.setObjectName(u'versionNameLabel')
        self.metaTabLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.versionNameLabel)
        self.versionNameEdit = QtGui.QLineEdit(self.metaTab)
        self.versionNameEdit.setObjectName(u'versionNameEdit')
        self.versionNameLabel.setBuddy(self.versionNameEdit)
        self.metaTabLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.versionNameEdit)
        self.copyrightLabel = QtGui.QLabel(self.metaTab)
        self.copyrightLabel.setObjectName(u'copyrightLabel')
        self.metaTabLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.copyrightLabel)
        self.copyrightEdit = QtGui.QLineEdit(self.metaTab)
        self.copyrightEdit.setObjectName(u'copyrightEdit')
        self.copyrightLabel.setBuddy(self.copyrightEdit)
        self.metaTabLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.copyrightEdit)
        self.permissionsLabel = QtGui.QLabel(self.metaTab)
        self.permissionsLabel.setObjectName(u'permissionsLabel')
        self.metaTabLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.permissionsLabel)
        self.permissionsEdit = QtGui.QLineEdit(self.metaTab)
        self.permissionsEdit.setObjectName(u'permissionsEdit')
        self.permissionsLabel.setBuddy(self.permissionsEdit)
        self.metaTabLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.permissionsEdit)
        self.languageSelectionLabel = QtGui.QLabel(self.metaTab)
        self.languageSelectionLabel.setObjectName(u'languageSelectionLabel')
        self.metaTabLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.languageSelectionLabel)
        self.languageSelectionComboBox = QtGui.QComboBox(self.metaTab)
        self.languageSelectionComboBox.setObjectName(
            u'languageSelectionComboBox')
        self.languageSelectionComboBox.addItems([u'', u'', u'', u''])
        self.metaTabLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.languageSelectionComboBox)
        self.bibleTabWidget.addTab(self.metaTab, u'')
        # Book name tab
        self.bookNameTab = QtGui.QWidget()
        self.bookNameTab.setObjectName(u'bookNameTab')
        self.bookNameTabLayout = QtGui.QVBoxLayout(self.bookNameTab)
        self.bookNameTabLayout.setObjectName(u'bookNameTabLayout')
        self.bookNameNotice = QtGui.QLabel(self.bookNameTab)
        self.bookNameNotice.setObjectName(u'bookNameNotice')
        self.bookNameTabLayout.addWidget(self.bookNameNotice)
        self.scrollArea = QtGui.QScrollArea(self.bookNameTab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(u'scrollArea')
        self.scrollArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.bookNameGroupBox = QtGui.QWidget(self.scrollArea)
        self.bookNameGroupBox.setObjectName(u'bookNameGroupBox')
        self.bookNameGroupBoxLayout = QtGui.QFormLayout(self.bookNameGroupBox)
        self.bookNameGroupBoxLayout.setObjectName(u'bookNameGroupBoxLayout')
        self.bookNameLabel = {}
        self.bookNameEdit= {}
        x = 0
        for book in BiblesResourcesDB.get_books():
            self.bookNameLabel[book[u'abbreviation']] = QtGui.QLabel(
                self.bookNameGroupBox)
            self.bookNameLabel[book[u'abbreviation']].setObjectName(
                u'bookNameLabel[%s]' % book[u'abbreviation'])
            self.bookNameGroupBoxLayout.setWidget(x,
                QtGui.QFormLayout.LabelRole,
                self.bookNameLabel[book[u'abbreviation']])
            self.bookNameEdit[book[u'abbreviation']] = QtGui.QLineEdit(
                self.bookNameGroupBox)
            self.bookNameEdit[book[u'abbreviation']].setObjectName(
                u'bookNameEdit[%s]' % book[u'abbreviation'])
            self.bookNameGroupBoxLayout.setWidget(x,
                QtGui.QFormLayout.FieldRole,
                self.bookNameEdit[book[u'abbreviation']])
            x = x+1
        self.scrollArea.setWidget(self.bookNameGroupBox)
        self.bookNameTabLayout.addWidget(self.scrollArea)
        self.spacer = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.bookNameTabLayout.addItem(self.spacer)
        self.bibleTabWidget.addTab(self.bookNameTab, u'')
        # Last few bits
        self.dialogLayout.addWidget(self.bibleTabWidget)
        self.buttonBox = create_accept_reject_button_box(editBibleDialog)
        self.dialogLayout.addWidget(self.buttonBox)
        self.retranslateUi(editBibleDialog)
        QtCore.QMetaObject.connectSlotsByName(editBibleDialog)

    def retranslateUi(self, editBibleDialog):
        self.booknames = BibleStrings().Booknames
        editBibleDialog.setWindowTitle(
            translate('BiblesPlugin.EditBibleForm', 'Song Editor'))
        self.bibleTabWidget.setTabText(
            self.bibleTabWidget.indexOf(self.metaTab),
            translate('SongsPlugin.EditBibleForm', 'License Details'))
        self.versionNameLabel.setText(
            translate('BiblesPlugin.EditBibleForm', 'Version name:'))
        self.copyrightLabel.setText(
            translate('BiblesPlugin.EditBibleForm', 'Copyright:'))
        self.permissionsLabel.setText(
            translate('BiblesPlugin.EditBibleForm', 'Permissions:'))
        self.bibleTabWidget.setTabText(
            self.bibleTabWidget.indexOf(self.bookNameTab),
            translate('SongsPlugin.EditBibleForm', 'Custom Book Names'))
        self.languageSelectionLabel.setText(
            translate('BiblesPlugin.EditBibleForm', 'Bookname language:'))
        self.languageSelectionComboBox.setItemText(0,
            translate('BiblesPlugin.EditBibleForm', 'General Settings'))
        self.languageSelectionComboBox.setItemText(LanguageSelection.Bible+1,
            translate('BiblesPlugin.EditBibleForm', 'Bible language'))
        self.languageSelectionComboBox.setItemText(
            LanguageSelection.Application+1,
            translate('BiblesPlugin.EditBibleForm', 'Application language'))
        self.languageSelectionComboBox.setItemText(LanguageSelection.English+1,
            translate('BiblesPlugin.EditBibleForm', 'English'))
        self.languageSelectionComboBox.setToolTip(
            translate('BiblesPlugin.EditBibleForm', 'Multiple options:\n '
            'General Settings - the option choosen in settings section\n'
            'Bible language - the language in which the Bible book names '
            'were imported\n Application language - the language you have '
            'chosen for OpenLP\n English - always use English book names'))
        for book in BiblesResourcesDB.get_books():
            self.bookNameLabel[book[u'abbreviation']].setText(
                u'%s:' % unicode(self.booknames[book[u'abbreviation']]))
