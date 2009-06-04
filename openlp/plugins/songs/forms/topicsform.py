# -*- coding: utf-8 -*-
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten Tinggaard

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

from PyQt4 import QtGui, QtCore
from openlp.plugins.songs.lib import TextListData

from openlp.plugins.songs.forms.topicsdialog import Ui_TopicsDialog
from openlp.plugins.songs.lib.classes import Topic

class TopicsForm(QtGui.QDialog, Ui_TopicsDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, songmanager, parent = None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.songmanager = songmanager
        self.currentRow = 0
        self.songbook = None

        QtCore.QObject.connect(self.DeleteButton,
            QtCore.SIGNAL('pressed()'), self.onDeleteButtonClick)
        QtCore.QObject.connect(self.ClearButton,
            QtCore.SIGNAL('pressed()'), self.onClearButtonClick)
        QtCore.QObject.connect(self.AddUpdateButton,
            QtCore.SIGNAL('pressed()'), self.onAddUpdateButtonClick)
        QtCore.QObject.connect(self.TopicNameEdit,
            QtCore.SIGNAL('lostFocus()'), self.onTopicNameEditLostFocus)
        QtCore.QObject.connect(self.TopicsListView,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onTopicsListViewItemClicked)

    def load_form(self):
        """
        Refresh the screen and rest fields
        """
        self.TopicsListData.resetStore()
        self.onClearButtonClick() # tidy up screen
        Topics = self.songmanager.get_topics()
        for Topic in Topics:
            self.TopicsListData.addRow(Topic.id,Topic.name)
        row_count = self.TopicsListData.rowCount(None)
        if self.currentRow > row_count:
            # in case we have delete the last row of the table
            self.currentRow = row_count
        row = self.TopicsListData.createIndex(self.currentRow, 0)
        if row.isValid():
            self.TopicsListView.selectionModel().setCurrentIndex(row,
                QtGui.QItemSelectionModel.SelectCurrent)
        self._validate_form()

    def onDeleteButtonClick(self):
        """
        Delete the Topic is the Topic is not attached to any songs
        """
        self.songmanager.delete_topic(self.Topic.id)
        self.load_form()

    def onTopicNameEditLostFocus(self):
        self._validate_form()

    def onAddUpdateButtonClick(self):
        """
        Sent New or update details to the database
        """
        if self.Topic == None:
            self.Topic = Topic()
        self.Topic.name = unicode(self.TopicNameEdit.displayText())
        self.songmanager.save_topic(self.Topic)
        self.onClearButtonClick()
        self.load_form()

    def onClearButtonClick(self):
        """
        Tidy up screen if clear button pressed
        """
        self.TopicNameEdit.setText(u'')
        self.MessageLabel.setText(u'')
        self.DeleteButton.setEnabled(False)
        self.AddUpdateButton.setEnabled(True)
        self.Topic = None
        self._validate_form()

    def onTopicsListViewItemClicked(self, index):
        """
        An Topic has been selected display it
        If the Topic is attached to a Song prevent delete
        """
        self.currentRow = index.row()
        id = int(self.TopicsListData.getId(index))
        self.Topic = self.songmanager.get_topic(id)

        self.TopicNameEdit.setText(self.Topic.name)
        if len(self.Topic.songs) > 0:
            self.MessageLabel.setText("Topic in use 'Delete' is disabled")
            self.DeleteButton.setEnabled(False)
        else:
            self.MessageLabel.setText("Topic is not used")
            self.DeleteButton.setEnabled(True)
        self._validate_form()

    def _validate_form(self):
        if len(self.TopicNameEdit.displayText()) == 0: # We need at lease a display name
            self.AddUpdateButton.setEnabled(False)
        else:
            self.AddUpdateButton.setEnabled(True)
