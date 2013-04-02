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

from openlp.core.lib import UiStrings, build_icon, translate
from openlp.core.lib.ui import create_button_box, create_button
from openlp.plugins.songs.lib.ui import SongStrings

class Ui_EditSongDialog(object):
    def setupUi(self, editSongDialog):
        editSongDialog.setObjectName(u'editSongDialog')
        editSongDialog.resize(650, 400)
        editSongDialog.setWindowIcon(build_icon(u':/icon/openlp-logo-16x16.png'))
        editSongDialog.setModal(True)
        self.dialogLayout = QtGui.QVBoxLayout(editSongDialog)
        self.dialogLayout.setSpacing(8)
        self.dialogLayout.setContentsMargins(8, 8, 8, 8)
        self.dialogLayout.setObjectName(u'dialog_layout')
        self.songTabWidget = QtGui.QTabWidget(editSongDialog)
        self.songTabWidget.setObjectName(u'songTabWidget')
        # lyrics tab
        self.lyricsTab = QtGui.QWidget()
        self.lyricsTab.setObjectName(u'lyricsTab')
        self.lyricsTabLayout = QtGui.QGridLayout(self.lyricsTab)
        self.lyricsTabLayout.setObjectName(u'lyricsTabLayout')
        self.titleLabel = QtGui.QLabel(self.lyricsTab)
        self.titleLabel.setObjectName(u'titleLabel')
        self.lyricsTabLayout.addWidget(self.titleLabel, 0, 0)
        self.titleEdit = QtGui.QLineEdit(self.lyricsTab)
        self.titleEdit.setObjectName(u'titleEdit')
        self.titleLabel.setBuddy(self.titleEdit)
        self.lyricsTabLayout.addWidget(self.titleEdit, 0, 1, 1, 2)
        self.alternativeTitleLabel = QtGui.QLabel(self.lyricsTab)
        self.alternativeTitleLabel.setObjectName(u'alternativeTitleLabel')
        self.lyricsTabLayout.addWidget(self.alternativeTitleLabel, 1, 0)
        self.alternativeEdit = QtGui.QLineEdit(self.lyricsTab)
        self.alternativeEdit.setObjectName(u'alternativeEdit')
        self.alternativeTitleLabel.setBuddy(self.alternativeEdit)
        self.lyricsTabLayout.addWidget(self.alternativeEdit, 1, 1, 1, 2)
        self.lyricsLabel = QtGui.QLabel(self.lyricsTab)
        self.lyricsLabel.setFixedHeight(self.titleEdit.sizeHint().height())
        self.lyricsLabel.setObjectName(u'lyricsLabel')
        self.lyricsTabLayout.addWidget(self.lyricsLabel, 2, 0, QtCore.Qt.AlignTop)
        self.verseListWidget = SingleColumnTableWidget(self.lyricsTab)
        self.verseListWidget.setAlternatingRowColors(True)
        self.verseListWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.verseListWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.verseListWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.verseListWidget.setObjectName(u'verseListWidget')
        self.lyricsLabel.setBuddy(self.verseListWidget)
        self.lyricsTabLayout.addWidget(self.verseListWidget, 2, 1)
        self.verseOrderLabel = QtGui.QLabel(self.lyricsTab)
        self.verseOrderLabel.setObjectName(u'verseOrderLabel')
        self.lyricsTabLayout.addWidget(self.verseOrderLabel, 3, 0)
        self.verseOrderEdit = QtGui.QLineEdit(self.lyricsTab)
        self.verseOrderEdit.setObjectName(u'verseOrderEdit')
        self.verseOrderLabel.setBuddy(self.verseOrderEdit)
        self.lyricsTabLayout.addWidget(self.verseOrderEdit, 3, 1, 1, 2)
        self.verseButtonsLayout = QtGui.QVBoxLayout()
        self.verseButtonsLayout.setObjectName(u'verseButtonsLayout')
        self.verseAddButton = QtGui.QPushButton(self.lyricsTab)
        self.verseAddButton.setObjectName(u'verseAddButton')
        self.verseButtonsLayout.addWidget(self.verseAddButton)
        self.verseEditButton = QtGui.QPushButton(self.lyricsTab)
        self.verseEditButton.setObjectName(u'verseEditButton')
        self.verseButtonsLayout.addWidget(self.verseEditButton)
        self.verseEditAllButton = QtGui.QPushButton(self.lyricsTab)
        self.verseEditAllButton.setObjectName(u'verseEditAllButton')
        self.verseButtonsLayout.addWidget(self.verseEditAllButton)
        self.verseDeleteButton = QtGui.QPushButton(self.lyricsTab)
        self.verseDeleteButton.setObjectName(u'verseDeleteButton')
        self.verseButtonsLayout.addWidget(self.verseDeleteButton)
        self.verseButtonsLayout.addStretch()
        self.lyricsTabLayout.addLayout(self.verseButtonsLayout, 2, 2)
        self.songTabWidget.addTab(self.lyricsTab, u'')
        # authors tab
        self.authorsTab = QtGui.QWidget()
        self.authorsTab.setObjectName(u'authorsTab')
        self.authorsTabLayout = QtGui.QHBoxLayout(self.authorsTab)
        self.authorsTabLayout.setObjectName(u'authorsTabLayout')
        self.authorsLeftLayout = QtGui.QVBoxLayout()
        self.authorsLeftLayout.setObjectName(u'authorsLeftLayout')
        self.authorsGroupBox = QtGui.QGroupBox(self.authorsTab)
        self.authorsGroupBox.setObjectName(u'authorsGroupBox')
        self.authorsLayout = QtGui.QVBoxLayout(self.authorsGroupBox)
        self.authorsLayout.setObjectName(u'authorsLayout')
        self.authorAddLayout = QtGui.QHBoxLayout()
        self.authorAddLayout.setObjectName(u'authorAddLayout')
        self.authorsComboBox = editSongDialogComboBox(self.authorsGroupBox, u'authorsComboBox')
        self.authorAddLayout.addWidget(self.authorsComboBox)
        self.authorAddButton = QtGui.QPushButton(self.authorsGroupBox)
        self.authorAddButton.setObjectName(u'authorAddButton')
        self.authorAddLayout.addWidget(self.authorAddButton)
        self.authorsLayout.addLayout(self.authorAddLayout)
        self.authorsListView = QtGui.QListWidget(self.authorsGroupBox)
        self.authorsListView.setAlternatingRowColors(True)
        self.authorsListView.setObjectName(u'authorsListView')
        self.authorsLayout.addWidget(self.authorsListView)
        self.authorRemoveLayout = QtGui.QHBoxLayout()
        self.authorRemoveLayout.setObjectName(u'authorRemoveLayout')
        self.authorRemoveLayout.addStretch()
        self.authorRemoveButton = QtGui.QPushButton(self.authorsGroupBox)
        self.authorRemoveButton.setObjectName(u'authorRemoveButton')
        self.authorRemoveLayout.addWidget(self.authorRemoveButton)
        self.authorsLayout.addLayout(self.authorRemoveLayout)
        self.authorsLeftLayout.addWidget(self.authorsGroupBox)
        self.maintenanceLayout = QtGui.QHBoxLayout()
        self.maintenanceLayout.setObjectName(u'maintenanceLayout')
        self.maintenanceButton = QtGui.QPushButton(self.authorsTab)
        self.maintenanceButton.setObjectName(u'maintenanceButton')
        self.maintenanceLayout.addWidget(self.maintenanceButton)
        self.maintenanceLayout.addStretch()
        self.authorsLeftLayout.addLayout(self.maintenanceLayout)
        self.authorsTabLayout.addLayout(self.authorsLeftLayout)
        self.authorsRightLayout = QtGui.QVBoxLayout()
        self.authorsRightLayout.setObjectName(u'authorsRightLayout')
        self.topicsGroupBox = QtGui.QGroupBox(self.authorsTab)
        self.topicsGroupBox.setObjectName(u'topicsGroupBox')
        self.topicsLayout = QtGui.QVBoxLayout(self.topicsGroupBox)
        self.topicsLayout.setObjectName(u'topicsLayout')
        self.topicAddLayout = QtGui.QHBoxLayout()
        self.topicAddLayout.setObjectName(u'topicAddLayout')
        self.topicsComboBox = editSongDialogComboBox(self.topicsGroupBox, u'topicsComboBox')
        self.topicAddLayout.addWidget(self.topicsComboBox)
        self.topicAddButton = QtGui.QPushButton(self.topicsGroupBox)
        self.topicAddButton.setObjectName(u'topicAddButton')
        self.topicAddLayout.addWidget(self.topicAddButton)
        self.topicsLayout.addLayout(self.topicAddLayout)
        self.topicsListView = QtGui.QListWidget(self.topicsGroupBox)
        self.topicsListView.setAlternatingRowColors(True)
        self.topicsListView.setObjectName(u'topicsListView')
        self.topicsLayout.addWidget(self.topicsListView)
        self.topicRemoveLayout = QtGui.QHBoxLayout()
        self.topicRemoveLayout.setObjectName(u'topicRemoveLayout')
        self.topicRemoveLayout.addStretch()
        self.topicRemoveButton = QtGui.QPushButton(self.topicsGroupBox)
        self.topicRemoveButton.setObjectName(u'topicRemoveButton')
        self.topicRemoveLayout.addWidget(self.topicRemoveButton)
        self.topicsLayout.addLayout(self.topicRemoveLayout)
        self.authorsRightLayout.addWidget(self.topicsGroupBox)
        self.songBookGroupBox = QtGui.QGroupBox(self.authorsTab)
        self.songBookGroupBox.setObjectName(u'songBookGroupBox')
        self.songBookLayout = QtGui.QFormLayout(self.songBookGroupBox)
        self.songBookLayout.setObjectName(u'songBookLayout')
        self.songBookNameLabel = QtGui.QLabel(self.songBookGroupBox)
        self.songBookNameLabel.setObjectName(u'songBookNameLabel')
        self.songBookComboBox = editSongDialogComboBox(self.songBookGroupBox, u'songBookComboBox')
        self.songBookNameLabel.setBuddy(self.songBookComboBox)
        self.songBookLayout.addRow(self.songBookNameLabel, self.songBookComboBox)
        self.songBookNumberLabel = QtGui.QLabel(self.songBookGroupBox)
        self.songBookNumberLabel.setObjectName(u'songBookNumberLabel')
        self.songBookNumberEdit = QtGui.QLineEdit(self.songBookGroupBox)
        self.songBookNumberEdit.setObjectName(u'songBookNumberEdit')
        self.songBookNumberLabel.setBuddy(self.songBookNumberEdit)
        self.songBookLayout.addRow(self.songBookNumberLabel, self.songBookNumberEdit)
        self.authorsRightLayout.addWidget(self.songBookGroupBox)
        self.authorsTabLayout.addLayout(self.authorsRightLayout)
        self.songTabWidget.addTab(self.authorsTab, u'')
        # theme tab
        self.themeTab = QtGui.QWidget()
        self.themeTab.setObjectName(u'themeTab')
        self.themeTabLayout = QtGui.QHBoxLayout(self.themeTab)
        self.themeTabLayout.setObjectName(u'themeTabLayout')
        self.themeLeftLayout = QtGui.QVBoxLayout()
        self.themeLeftLayout.setObjectName(u'themeLeftLayout')
        self.themeGroupBox = QtGui.QGroupBox(self.themeTab)
        self.themeGroupBox.setObjectName(u'themeGroupBox')
        self.themeLayout = QtGui.QHBoxLayout(self.themeGroupBox)
        self.themeLayout.setObjectName(u'themeLayout')
        self.themeComboBox = editSongDialogComboBox(self.themeGroupBox, u'themeComboBox')
        self.themeLayout.addWidget(self.themeComboBox)
        self.themeAddButton = QtGui.QPushButton(self.themeGroupBox)
        self.themeAddButton.setObjectName(u'themeAddButton')
        self.themeLayout.addWidget(self.themeAddButton)
        self.themeLeftLayout.addWidget(self.themeGroupBox)
        self.rightsGroupBox = QtGui.QGroupBox(self.themeTab)
        self.rightsGroupBox.setObjectName(u'rightsGroupBox')
        self.rightsLayout = QtGui.QVBoxLayout(self.rightsGroupBox)
        self.rightsLayout.setObjectName(u'rightsLayout')
        self.copyrightLayout = QtGui.QHBoxLayout()
        self.copyrightLayout.setObjectName(u'copyrightLayout')
        self.copyrightEdit = QtGui.QLineEdit(self.rightsGroupBox)
        self.copyrightEdit.setObjectName(u'copyrightEdit')
        self.copyrightLayout.addWidget(self.copyrightEdit)
        self.copyrightInsertButton = QtGui.QToolButton(self.rightsGroupBox)
        self.copyrightInsertButton.setObjectName(u'copyrightInsertButton')
        self.copyrightLayout.addWidget(self.copyrightInsertButton)
        self.rightsLayout.addLayout(self.copyrightLayout)
        self.CCLILayout = QtGui.QHBoxLayout()
        self.CCLILayout.setObjectName(u'CCLILayout')
        self.CCLILabel = QtGui.QLabel(self.rightsGroupBox)
        self.CCLILabel.setObjectName(u'CCLILabel')
        self.CCLILayout.addWidget(self.CCLILabel)
        self.CCLNumberEdit = QtGui.QLineEdit(self.rightsGroupBox)
        self.CCLNumberEdit.setValidator(QtGui.QIntValidator())
        self.CCLNumberEdit.setObjectName(u'CCLNumberEdit')
        self.CCLILayout.addWidget(self.CCLNumberEdit)
        self.rightsLayout.addLayout(self.CCLILayout)
        self.themeLeftLayout.addWidget(self.rightsGroupBox)
        self.themeLeftLayout.addStretch()
        self.themeTabLayout.addLayout(self.themeLeftLayout)
        self.commentsGroupBox = QtGui.QGroupBox(self.themeTab)
        self.commentsGroupBox.setObjectName(u'commentsGroupBox')
        self.commentsLayout = QtGui.QVBoxLayout(self.commentsGroupBox)
        self.commentsLayout.setObjectName(u'commentsLayout')
        self.commentsEdit = QtGui.QTextEdit(self.commentsGroupBox)
        self.commentsEdit.setObjectName(u'commentsEdit')
        self.commentsLayout.addWidget(self.commentsEdit)
        self.themeTabLayout.addWidget(self.commentsGroupBox)
        self.songTabWidget.addTab(self.themeTab, u'')
        # audio tab
        self.audioTab = QtGui.QWidget()
        self.audioTab.setObjectName(u'audioTab')
        self.audioLayout = QtGui.QHBoxLayout(self.audioTab)
        self.audioLayout.setObjectName(u'audioLayout')
        self.audioListWidget = QtGui.QListWidget(self.audioTab)
        self.audioListWidget.setObjectName(u'audioListWidget')
        self.audioLayout.addWidget(self.audioListWidget)
        self.audioButtonsLayout = QtGui.QVBoxLayout()
        self.audioButtonsLayout.setObjectName(u'audioButtonsLayout')
        self.audioAddFromFileButton = QtGui.QPushButton(self.audioTab)
        self.audioAddFromFileButton.setObjectName(u'audioAddFromFileButton')
        self.audioButtonsLayout.addWidget(self.audioAddFromFileButton)
        self.audioAddFromMediaButton = QtGui.QPushButton(self.audioTab)
        self.audioAddFromMediaButton.setObjectName(u'audioAddFromMediaButton')
        self.audioButtonsLayout.addWidget(self.audioAddFromMediaButton)
        self.audioRemoveButton = QtGui.QPushButton(self.audioTab)
        self.audioRemoveButton.setObjectName(u'audioRemoveButton')
        self.audioButtonsLayout.addWidget(self.audioRemoveButton)
        self.audioRemoveAllButton = QtGui.QPushButton(self.audioTab)
        self.audioRemoveAllButton.setObjectName(u'audioRemoveAllButton')
        self.audioButtonsLayout.addWidget(self.audioRemoveAllButton)
        self.audioButtonsLayout.addStretch(1)
        self.upButton = create_button(self, u'upButton', role=u'up', click=self.onUpButtonClicked)
        self.downButton = create_button(self, u'downButton', role=u'down', click=self.onDownButtonClicked)
        self.audioButtonsLayout.addWidget(self.upButton)
        self.audioButtonsLayout.addWidget(self.downButton)
        self.audioLayout.addLayout(self.audioButtonsLayout)
        self.songTabWidget.addTab(self.audioTab, u'')
        # Last few bits
        self.dialogLayout.addWidget(self.songTabWidget)
        self.bottomLayout = QtGui.QHBoxLayout()
        self.bottomLayout.setObjectName(u'bottomLayout')
        self.warningLabel = QtGui.QLabel(editSongDialog)
        self.warningLabel.setObjectName(u'warningLabel')
        self.warningLabel.setVisible(False)
        self.bottomLayout.addWidget(self.warningLabel)
        self.button_box = create_button_box(editSongDialog, u'button_box', [u'cancel', u'save'])
        self.bottomLayout.addWidget(self.button_box)
        self.dialogLayout.addLayout(self.bottomLayout)
        self.retranslateUi(editSongDialog)

    def retranslateUi(self, editSongDialog):
        editSongDialog.setWindowTitle(translate('SongsPlugin.EditSongForm', 'Song Editor'))
        self.titleLabel.setText(translate('SongsPlugin.EditSongForm', '&Title:'))
        self.alternativeTitleLabel.setText(translate('SongsPlugin.EditSongForm', 'Alt&ernate title:'))
        self.lyricsLabel.setText(translate('SongsPlugin.EditSongForm', '&Lyrics:'))
        self.verseOrderLabel.setText(translate('SongsPlugin.EditSongForm', '&Verse order:'))
        self.verseAddButton.setText(UiStrings().Add)
        self.verseEditButton.setText(UiStrings().Edit)
        self.verseEditAllButton.setText(translate('SongsPlugin.EditSongForm', 'Ed&it All'))
        self.verseDeleteButton.setText(UiStrings().Delete)
        self.songTabWidget.setTabText(self.songTabWidget.indexOf(self.lyricsTab),
            translate('SongsPlugin.EditSongForm', 'Title && Lyrics'))
        self.authorsGroupBox.setTitle(SongStrings.Authors)
        self.authorAddButton.setText(translate('SongsPlugin.EditSongForm', '&Add to Song'))
        self.authorRemoveButton.setText(translate('SongsPlugin.EditSongForm', '&Remove'))
        self.maintenanceButton.setText(translate('SongsPlugin.EditSongForm', '&Manage Authors, Topics, Song Books'))
        self.topicsGroupBox.setTitle(SongStrings.Topic)
        self.topicAddButton.setText(translate('SongsPlugin.EditSongForm', 'A&dd to Song'))
        self.topicRemoveButton.setText(translate('SongsPlugin.EditSongForm', 'R&emove'))
        self.songBookGroupBox.setTitle(SongStrings.SongBook)
        self.songBookNameLabel.setText(translate('SongsPlugin.EditSongForm', 'Book:'))
        self.songBookNumberLabel.setText(translate('SongsPlugin.EditSongForm', 'Number:'))
        self.songTabWidget.setTabText(self.songTabWidget.indexOf(self.authorsTab),
            translate('SongsPlugin.EditSongForm', 'Authors, Topics && Song Book'))
        self.themeGroupBox.setTitle(UiStrings().Theme)
        self.themeAddButton.setText(translate('SongsPlugin.EditSongForm', 'New &Theme'))
        self.rightsGroupBox.setTitle(translate('SongsPlugin.EditSongForm', 'Copyright Information'))
        self.copyrightInsertButton.setText(SongStrings.CopyrightSymbol)
        self.CCLILabel.setText(UiStrings().CCLINumberLabel)
        self.commentsGroupBox.setTitle(translate('SongsPlugin.EditSongForm', 'Comments'))
        self.songTabWidget.setTabText(self.songTabWidget.indexOf(self.themeTab),
            translate('SongsPlugin.EditSongForm', 'Theme, Copyright Info && Comments'))
        self.songTabWidget.setTabText(self.songTabWidget.indexOf(self.audioTab),
            translate('SongsPlugin.EditSongForm', 'Linked Audio'))
        self.audioAddFromFileButton.setText(translate('SongsPlugin.EditSongForm', 'Add &File(s)'))
        self.audioAddFromMediaButton.setText(translate('SongsPlugin.EditSongForm', 'Add &Media'))
        self.audioRemoveButton.setText(translate('SongsPlugin.EditSongForm', '&Remove'))
        self.audioRemoveAllButton.setText(translate('SongsPlugin.EditSongForm', 'Remove &All'))
        self.warningLabel.setText(
            translate('SongsPlugin.EditSongForm', '<strong>Warning:</strong> Not all of the verses are in use.'))

def editSongDialogComboBox(parent, name):
    """
    Utility method to generate a standard combo box for this dialog.
    """
    comboBox = QtGui.QComboBox(parent)
    comboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
    comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    comboBox.setEditable(True)
    comboBox.setInsertPolicy(QtGui.QComboBox.NoInsert)
    comboBox.setObjectName(name)
    return comboBox

class SingleColumnTableWidget(QtGui.QTableWidget):
    """
    Class to for a single column table widget to use for the verse table widget.
    """
    def __init__(self, parent):
        """
        Constructor
        """
        QtGui.QTableWidget.__init__(self, parent)
        self.horizontalHeader().setVisible(False)
        self.setColumnCount(1)

    def resizeEvent(self, event):
        """
        Resize the first column together with the widget.
        """
        QtGui.QTableWidget.resizeEvent(self, event)
        if self.columnCount():
            self.setColumnWidth(0, event.size().width())
            self.resizeRowsToContents()
