# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from PyQt4 import Qt, QtCore, QtGui

from editcustomdialog import Ui_customEditDialog
from openlp.core.lib import SongXMLBuilder, SongXMLParser, Receiver, translate
from openlp.plugins.custom.lib.models import CustomSlide

class EditCustomForm(QtGui.QDialog, Ui_customEditDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, custommanager, parent = None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        #self.parent = parent
        self.setupUi(self)
        # Connecting signals and slots
        QtCore.QObject.connect(self.buttonBox,
            QtCore.SIGNAL(u'rejected()'), self.rejected)
        QtCore.QObject.connect(self.buttonBox,
            QtCore.SIGNAL(u'accepted()'), self.accept)
        QtCore.QObject.connect(self.AddButton,
            QtCore.SIGNAL(u'pressed()'), self.onAddButtonPressed)
        QtCore.QObject.connect(self.EditButton,
            QtCore.SIGNAL(u'pressed()'), self.onEditButtonPressed)
        QtCore.QObject.connect(self.EditAllButton,
            QtCore.SIGNAL(u'pressed()'), self.onEditAllButtonPressed)
        QtCore.QObject.connect(self.SaveButton,
            QtCore.SIGNAL(u'pressed()'), self.onSaveButtonPressed)
        QtCore.QObject.connect(self.DeleteButton,
            QtCore.SIGNAL(u'pressed()'), self.onDeleteButtonPressed)
        QtCore.QObject.connect(self.ClearButton,
            QtCore.SIGNAL(u'pressed()'), self.onClearButtonPressed)
        QtCore.QObject.connect(self.UpButton,
            QtCore.SIGNAL(u'pressed()'), self.onUpButtonPressed)
        QtCore.QObject.connect(self.DownButton,
            QtCore.SIGNAL(u'pressed()'), self.onDownButtonPressed)

        QtCore.QObject.connect(self.VerseListView,
            QtCore.SIGNAL(u'itemDoubleClicked(QListWidgetItem*)'),
            self.onVerseListViewSelected)
        QtCore.QObject.connect(self.VerseListView,
            QtCore.SIGNAL(u'itemClicked(QListWidgetItem*)'),
            self.onVerseListViewPressed)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'update_themes'), self.loadThemes)
        # Create other objects and forms
        self.custommanager = custommanager
        self.initialise()

    def initialise(self):
        self.editAll = False
        self.DeleteButton.setEnabled(False)
        self.EditButton.setEnabled(False)
        self.EditAllButton.setEnabled(True)
        self.SaveButton.setEnabled(False)
        self.ClearButton.setEnabled(False)
        self.TitleEdit.setText(u'')
        self.CreditEdit.setText(u'')
        self.VerseTextEdit.clear()
        self.VerseListView.clear()
        #make sure we have a new item
        self.customSlide = CustomSlide()
        self.ThemeComboBox.addItem(u'')

    def loadThemes(self, themelist):
        self.ThemeComboBox.clear()
        self.ThemeComboBox.addItem(u'')
        for themename in themelist:
            self.ThemeComboBox.addItem(themename)

    def loadCustom(self, id):
        self.customSlide = CustomSlide()
        self.initialise()
        if id != 0:
            self.customSlide = self.custommanager.get_custom(id)
            self.TitleEdit.setText(self.customSlide.title)
            self.CreditEdit.setText(self.customSlide.credits)

            songXML=SongXMLParser(self.customSlide.text)
            verseList = songXML.get_verses()
            for verse in verseList:
                self.VerseListView.addItem(verse[1])
            theme = unicode(self.customSlide.theme_name)
            id = self.ThemeComboBox.findText(theme, QtCore.Qt.MatchExactly)
            if id == -1:
                id = 0 # Not Found
            self.ThemeComboBox.setCurrentIndex(id)
        else:
            self.ThemeComboBox.setCurrentIndex(0)

    def accept(self):
        valid , message = self._validate()
        if not valid:
            QtGui.QMessageBox.critical(self,
            translate(u'customEditDialog', u'Error'), message,
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
            return
        sxml=SongXMLBuilder()
        sxml.new_document()
        sxml.add_lyrics_to_song()
        count = 1
        for i in range (0, self.VerseListView.count()):
            sxml.add_verse_to_lyrics(u'custom', unicode(count),
                unicode(self.VerseListView.item(i).text()))
            count += 1
        self.customSlide.title = unicode(self.TitleEdit.displayText())
        self.customSlide.text = unicode(sxml.extract_xml())
        self.customSlide.credits = unicode(self.CreditEdit.displayText())
        self.customSlide.theme_name = unicode(self.ThemeComboBox.currentText())
        self.custommanager.save_slide(self.customSlide)
        self.close()

    def rejected(self):
        self.close()

    def onUpButtonPressed(self):
        selectedRow = self.VerseListView.currentRow()
        if selectedRow != 0:
            qw = self.VerseListView.takeItem(selectedRow)
            self.VerseListView.insertItem(selectedRow - 1, qw)
            self.VerseListView.setCurrentRow(selectedRow - 1)

    def onDownButtonPressed(self):
        selectedRow = self.VerseListView.currentRow()
        # zero base arrays
        if selectedRow != self.VerseListView.count() - 1:
            qw = self.VerseListView.takeItem(selectedRow)
            self.VerseListView.insertItem(selectedRow + 1, qw)
            self.VerseListView.setCurrentRow(selectedRow + 1)

    def onClearButtonPressed(self):
        self.VerseTextEdit.clear()
        self.editAll = False
        self.AddButton.setEnabled(True)
        self.EditAllButton.setEnabled(True)
        self.SaveButton.setEnabled(False)

    def onVerseListViewPressed(self, item):
        self.DeleteButton.setEnabled(True)
        self.EditButton.setEnabled(True)

    def onVerseListViewSelected(self, item):
        self.editText(item.text())

    def onAddButtonPressed(self):
        self.VerseListView.addItem(self.VerseTextEdit.toPlainText())
        self.DeleteButton.setEnabled(False)
        self.VerseTextEdit.clear()

    def onEditButtonPressed(self):
        self.editText(self.VerseListView.currentItem().text())

    def onEditAllButtonPressed(self):
        self.editAll = True
        self.AddButton.setEnabled(False)
        if self.VerseListView.count() > 0:
            verse_list = u''
            for row in range(0, self.VerseListView.count()):
                item = self.VerseListView.item(row)
                verse_list += item.text()
                verse_list += u'\n---\n'
            self.editText(verse_list)

    def editText(self, text):
        self.beforeText = text
        self.VerseTextEdit.setPlainText(text)
        self.DeleteButton.setEnabled(False)
        self.EditButton.setEnabled(False)
        self.EditAllButton.setEnabled(False)
        self.SaveButton.setEnabled(True)
        self.ClearButton.setEnabled(True)

    def onSaveButtonPressed(self):
        if self.editAll:
            self.VerseListView.clear()
            for row in unicode(self.VerseTextEdit.toPlainText()).split(u'---'):
                self.VerseListView.addItem(row)
        else:
            self.VerseListView.currentItem().setText(
                self.VerseTextEdit.toPlainText())
            #number of lines has change
            if len(self.beforeText.split(u'\n')) != \
                len(self.VerseTextEdit.toPlainText().split(u'\n')):
                tempList = {}
                for row in range(0, self.VerseListView.count()):
                    tempList[row] = self.VerseListView.item(row).text()
                self.VerseListView.clear()
                for row in range (0, len(tempList)):
                    self.VerseListView.addItem(tempList[row])
                self.VerseListView.repaint()
        self.AddButton.setEnabled(True)
        self.SaveButton.setEnabled(False)
        self.EditButton.setEnabled(False)
        self.EditAllButton.setEnabled(True)
        self.VerseTextEdit.clear()

    def onDeleteButtonPressed(self):
        self.VerseListView.takeItem(self.VerseListView.currentRow())
        self.EditButton.setEnabled(False)
        self.EditAllButton.setEnabled(True)

    def _validate(self):
        valid = True
        message = u''
        if len(self.TitleEdit.displayText()) == 0:
            valid = False
            message = translate(
                u'customEditDialog', u'You need to enter a title \n')
        # must have 1 slide
        if self.VerseListView.count() == 0:
            valid = False
            message += translate(
                u'customEditDialog', u'You need to enter a slide \n')
        return valid, message
