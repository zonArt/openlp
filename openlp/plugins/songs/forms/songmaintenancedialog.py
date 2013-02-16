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

from openlp.core.lib import UiStrings, build_icon
from openlp.core.lib.ui import create_button_box
from openlp.plugins.songs.lib.ui import SongStrings

class Ui_SongMaintenanceDialog(object):
    def setupUi(self, songMaintenanceDialog):
        songMaintenanceDialog.setObjectName(u'songMaintenanceDialog')
        songMaintenanceDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        songMaintenanceDialog.resize(10, 350)
        self.dialogLayout = QtGui.QGridLayout(songMaintenanceDialog)
        self.dialogLayout.setObjectName(u'dialog_layout')
        self.typeListWidget = QtGui.QListWidget(songMaintenanceDialog)
        self.typeListWidget.setIconSize(QtCore.QSize(32, 32))
        self.typeListWidget.setUniformItemSizes(True)
        self.typeListWidget.setObjectName(u'typeListWidget')
        self.listItemAuthors = QtGui.QListWidgetItem(self.typeListWidget)
        self.listItemAuthors.setIcon(build_icon(u':/songs/author_maintenance.png'))
        self.listItemTopics = QtGui.QListWidgetItem(self.typeListWidget)
        self.listItemTopics.setIcon(build_icon(u':/songs/topic_maintenance.png'))
        self.listItemBooks = QtGui.QListWidgetItem(self.typeListWidget)
        self.listItemBooks.setIcon(build_icon(u':/songs/book_maintenance.png'))
        self.dialogLayout.addWidget(self.typeListWidget, 0, 0)
        self.stackedLayout = QtGui.QStackedLayout()
        self.stackedLayout.setObjectName(u'stackedLayout')
        # authors page
        self.authorsPage = QtGui.QWidget(songMaintenanceDialog)
        self.authorsPage.setObjectName(u'authorsPage')
        self.authorsLayout = QtGui.QVBoxLayout(self.authorsPage)
        self.authorsLayout.setObjectName(u'authorsLayout')
        self.authorsListWidget = QtGui.QListWidget(self.authorsPage)
        self.authorsListWidget.setObjectName(u'authorsListWidget')
        self.authorsLayout.addWidget(self.authorsListWidget)
        self.authorsButtonsLayout = QtGui.QHBoxLayout()
        self.authorsButtonsLayout.setObjectName(u'authorsButtonsLayout')
        self.authorsButtonsLayout.addStretch()
        self.authorsAddButton = QtGui.QPushButton(self.authorsPage)
        self.authorsAddButton.setIcon(build_icon(u':/songs/author_add.png'))
        self.authorsAddButton.setObjectName(u'authorsAddButton')
        self.authorsButtonsLayout.addWidget(self.authorsAddButton)
        self.authorsEditButton = QtGui.QPushButton(self.authorsPage)
        self.authorsEditButton.setIcon(build_icon(u':/songs/author_edit.png'))
        self.authorsEditButton.setObjectName(u'authorsEditButton')
        self.authorsButtonsLayout.addWidget(self.authorsEditButton)
        self.authorsDeleteButton = QtGui.QPushButton(self.authorsPage)
        self.authorsDeleteButton.setIcon(build_icon(u':/songs/author_delete.png'))
        self.authorsDeleteButton.setObjectName(u'authorsDeleteButton')
        self.authorsButtonsLayout.addWidget(self.authorsDeleteButton)
        self.authorsLayout.addLayout(self.authorsButtonsLayout)
        self.stackedLayout.addWidget(self.authorsPage)
        # topics page
        self.topicsPage = QtGui.QWidget(songMaintenanceDialog)
        self.topicsPage.setObjectName(u'topicsPage')
        self.topicsLayout = QtGui.QVBoxLayout(self.topicsPage)
        self.topicsLayout.setObjectName(u'topicsLayout')
        self.topicsListWidget = QtGui.QListWidget(self.topicsPage)
        self.topicsListWidget.setObjectName(u'topicsListWidget')
        self.topicsLayout.addWidget(self.topicsListWidget)
        self.topicsButtonsLayout = QtGui.QHBoxLayout()
        self.topicsButtonsLayout.setObjectName(u'topicsButtonLayout')
        self.topicsButtonsLayout.addStretch()
        self.topicsAddButton = QtGui.QPushButton(self.topicsPage)
        self.topicsAddButton.setIcon(build_icon(u':/songs/topic_add.png'))
        self.topicsAddButton.setObjectName(u'topicsAddButton')
        self.topicsButtonsLayout.addWidget(self.topicsAddButton)
        self.topicsEditButton = QtGui.QPushButton(self.topicsPage)
        self.topicsEditButton.setIcon(build_icon(u':/songs/topic_edit.png'))
        self.topicsEditButton.setObjectName(u'topicsEditButton')
        self.topicsButtonsLayout.addWidget(self.topicsEditButton)
        self.topicsDeleteButton = QtGui.QPushButton(self.topicsPage)
        self.topicsDeleteButton.setIcon(build_icon(u':/songs/topic_delete.png'))
        self.topicsDeleteButton.setObjectName(u'topicsDeleteButton')
        self.topicsButtonsLayout.addWidget(self.topicsDeleteButton)
        self.topicsLayout.addLayout(self.topicsButtonsLayout)
        self.stackedLayout.addWidget(self.topicsPage)
        # song books page
        self.booksPage = QtGui.QWidget(songMaintenanceDialog)
        self.booksPage.setObjectName(u'booksPage')
        self.booksLayout = QtGui.QVBoxLayout(self.booksPage)
        self.booksLayout.setObjectName(u'booksLayout')
        self.booksListWidget = QtGui.QListWidget(self.booksPage)
        self.booksListWidget.setObjectName(u'booksListWidget')
        self.booksLayout.addWidget(self.booksListWidget)
        self.booksButtonsLayout = QtGui.QHBoxLayout()
        self.booksButtonsLayout.setObjectName(u'booksButtonLayout')
        self.booksButtonsLayout.addStretch()
        self.booksAddButton = QtGui.QPushButton(self.booksPage)
        self.booksAddButton.setIcon(build_icon(u':/songs/book_add.png'))
        self.booksAddButton.setObjectName(u'booksAddButton')
        self.booksButtonsLayout.addWidget(self.booksAddButton)
        self.booksEditButton = QtGui.QPushButton(self.booksPage)
        self.booksEditButton.setIcon(build_icon(u':/songs/book_edit.png'))
        self.booksEditButton.setObjectName(u'booksEditButton')
        self.booksButtonsLayout.addWidget(self.booksEditButton)
        self.booksDeleteButton = QtGui.QPushButton(self.booksPage)
        self.booksDeleteButton.setIcon(build_icon(u':/songs/book_delete.png'))
        self.booksDeleteButton.setObjectName(u'booksDeleteButton')
        self.booksButtonsLayout.addWidget(self.booksDeleteButton)
        self.booksLayout.addLayout(self.booksButtonsLayout)
        self.stackedLayout.addWidget(self.booksPage)
        #
        self.dialogLayout.addLayout(self.stackedLayout, 0, 1)
        self.button_box = create_button_box(songMaintenanceDialog, u'button_box', [u'close'])
        self.dialogLayout.addWidget(self.button_box, 1, 0, 1, 2)
        self.retranslateUi(songMaintenanceDialog)
        self.stackedLayout.setCurrentIndex(0)
        QtCore.QObject.connect(self.typeListWidget, QtCore.SIGNAL(u'currentRowChanged(int)'),
            self.stackedLayout.setCurrentIndex)

    def retranslateUi(self, songMaintenanceDialog):
        songMaintenanceDialog.setWindowTitle(SongStrings.SongMaintenance)
        self.listItemAuthors.setText(SongStrings.Authors)
        self.listItemTopics.setText(SongStrings.Topics)
        self.listItemBooks.setText(SongStrings.SongBooks)
        self.authorsAddButton.setText(UiStrings().Add)
        self.authorsEditButton.setText(UiStrings().Edit)
        self.authorsDeleteButton.setText(UiStrings().Delete)
        self.topicsAddButton.setText(UiStrings().Add)
        self.topicsEditButton.setText(UiStrings().Edit)
        self.topicsDeleteButton.setText(UiStrings().Delete)
        self.booksAddButton.setText(UiStrings().Add)
        self.booksEditButton.setText(UiStrings().Edit)
        self.booksDeleteButton.setText(UiStrings().Delete)
        typeListWidth = max(self.fontMetrics().width(SongStrings.Authors),
            self.fontMetrics().width(SongStrings.Topics), self.fontMetrics().width(SongStrings.SongBooks))
        self.typeListWidget.setFixedWidth(typeListWidth + self.typeListWidget.iconSize().width() + 32)
