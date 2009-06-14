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
from openlp.plugins.songs.forms.authorsdialog import Ui_AuthorsDialog
from openlp.plugins.songs.lib.classes import Author

class AuthorsForm(QtGui.QDialog, Ui_AuthorsDialog):
    """
    Class to control the Maintenance of Authors Dialog
    """
    def __init__(self, songmanager, parent = None):
        """
        Set up the screen and common data
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.songmanager = songmanager
        self.currentRow = 0
        self.author = None

        QtCore.QObject.connect(self.DeleteButton,
            QtCore.SIGNAL(u'pressed()'), self.onDeleteButtonClick)
        QtCore.QObject.connect(self.ClearButton,
            QtCore.SIGNAL(u'pressed()'), self.onClearButtonClick)
        QtCore.QObject.connect(self.AddUpdateButton,
            QtCore.SIGNAL(u'pressed()'), self.onAddUpdateButtonClick)
        QtCore.QObject.connect(self.DisplayEdit,
            QtCore.SIGNAL(u'lostFocus()'), self.onDisplayEditLostFocus)
        QtCore.QObject.connect(self.AuthorListWidget,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onAuthorListWidgetItemClicked)

    def load_form(self):
        """
        Refresh the screen and rest fields
        """
        self.AuthorListWidget.clear()
        self.onClearButtonClick() # tidy up screen
        authors = self.songmanager.get_authors()
        for author in authors:
            author_name = QtGui.QListWidgetItem(author.display_name)
            author_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(author.id))
            self.AuthorListWidget.addItem(author_name)
        if self.currentRow >= self.AuthorListWidget.count() :
            self.AuthorListWidget.setCurrentRow(self.AuthorListWidget.count() - 1)
        else:
            self.AuthorListWidget.setCurrentRow(self.currentRow)
        self._validate_form()

    def onDeleteButtonClick(self):
        """
        Delete the author is the Author is not attached to any songs
        """
        self.songmanager.delete_author(self.author.id)
        self.load_form()

    def onDisplayEditLostFocus(self):
        self._validate_form()

    def onAddUpdateButtonClick(self):
        """
        Sent New or update details to the database
        """
        if self.author == None:
            self.author = Author()
        self.author.display_name = unicode(self.DisplayEdit.displayText())
        self.author.first_name = unicode(self.FirstNameEdit.displayText())
        self.author.last_name = unicode(self.LastNameEdit.displayText())
        self.songmanager.save_author(self.author)
        self.onClearButtonClick()
        self.load_form()

    def onClearButtonClick(self):
        """
        Tidy up screen if clear button pressed
        """
        self.DisplayEdit.setText(u'')
        self.FirstNameEdit.setText(u'')
        self.LastNameEdit.setText(u'')
        self.MessageLabel.setText(u'')
        self.DeleteButton.setEnabled(False)
        self.author = None
        self._validate_form()

    def onAuthorListWidgetItemClicked(self, index):
        """
        An Author has been selected display it
        If the author is attached to a Song prevent delete
        """
        self.currentRow = self.AuthorListWidget.currentRow()
        item = self.AuthorListWidget.currentItem()
        item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        self.author = self.songmanager.get_author(item_id)
        self.DisplayEdit.setText(self.author.display_name)
        self.FirstNameEdit.setText(self.author.first_name)
        self.LastNameEdit.setText(self.author.last_name)
        if len(self.author.songs) > 0:
            self.MessageLabel.setText(translate(u'AuthorForm', u'Author in use "Delete" is disabled'))
            self.DeleteButton.setEnabled(False)
        else:
            self.MessageLabel.setText(translate(u'AuthorForm', u'Author in not used'))
            self.DeleteButton.setEnabled(True)
        self._validate_form()

    def _validate_form(self):
        # We need at lease a display name
        if len(self.DisplayEdit.displayText()) == 0:
            self.AddUpdateButton.setEnabled(False)
        else:
            self.AddUpdateButton.setEnabled(True)
