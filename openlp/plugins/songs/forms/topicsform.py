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
from openlp.core.lib import translate
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
        self.topic = None

        QtCore.QObject.connect(self.DeleteButton,
            QtCore.SIGNAL(u'pressed()'), self.onDeleteButtonClick)
        QtCore.QObject.connect(self.ClearButton,
            QtCore.SIGNAL(u'pressed()'), self.onClearButtonClick)
        QtCore.QObject.connect(self.AddUpdateButton,
            QtCore.SIGNAL(u'pressed()'), self.onAddUpdateButtonClick)
        QtCore.QObject.connect(self.TopicNameEdit,
            QtCore.SIGNAL(u'lostFocus()'), self.onTopicNameEditLostFocus)
        QtCore.QObject.connect(self.TopicsListWidget,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onTopicsListWidgetItemClicked)

    def load_form(self):
        """
        Refresh the screen and rest fields
        """
        self.TopicsListWidget.clear()
        # tidy up screen
        self.onClearButtonClick()
        topics = self.songmanager.get_topics()
        for topic in topics:
            topic_name = QtGui.QListWidgetItem(topic.name)
            topic_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(topic.id))
            self.TopicsListWidget.addItem(topic_name)
        if self.currentRow >= self.TopicsListWidget.count() :
            self.TopicsListWidget.setCurrentRow(self.TopicsListWidget.count() - 1)
        else:
            self.TopicsListWidget.setCurrentRow(self.currentRow)
        self._validate_form()

    def onDeleteButtonClick(self):
        """
        Delete the Topic is the Topic is not attached to any songs
        """
        self.songmanager.delete_topic(self.topic.id)
        self.load_form()

    def onTopicNameEditLostFocus(self):
        self._validate_form()

    def onAddUpdateButtonClick(self):
        """
        Sent New or update details to the database
        """
        if self._validate_form():
            if self.topic == None:
                self.topic = Topic()
            self.topic.name = unicode(self.TopicNameEdit.displayText())
            self.songmanager.save_topic(self.topic)
            self.onClearButtonClick()
            self.load_form()

    def onClearButtonClick(self):
        """
        Tidy up screen if clear button pressed
        """
        self.TopicNameEdit.setText(u'')
        self.MessageLabel.setText(u'')
        self.DeleteButton.setEnabled(False)
        self.topic = None
        self._validate_form()
        self.TopicNameEdit.setFocus()

    def onTopicsListWidgetItemClicked(self, index):
        """
        An Topic has been selected display it
        If the Topic is attached to a Song prevent delete
        """
        self.currentRow = self.TopicsListWidget.currentRow()
        item = self.TopicsListWidget.currentItem()
        item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        self.topic = self.songmanager.get_topic(item_id)
        self.TopicNameEdit.setText(self.topic.name)
        if len(self.topic.songs) > 0:
            self.MessageLabel.setText(translate(u'TopicForm', u'Topic in use "Delete" is disabled'))
            self.DeleteButton.setEnabled(False)
        else:
            self.MessageLabel.setText(translate(u'TopicForm', u'Topic in not used'))
            self.DeleteButton.setEnabled(True)
        self._validate_form()
        self.TopicNameEdit.setFocus()

    def _validate_form(self):
        # We need at lease a display name
        valid = True
        if len(self.TopicNameEdit.displayText()) == 0:
            valid = False
            self.TopicNameEdit.setStyleSheet(u'background-color: red; color: white')
        else:
            self.TopicNameEdit.setStyleSheet(u'')
        return valid
