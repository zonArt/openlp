# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, translate
from openlp.plugins.custom.lib import CustomXMLBuilder, CustomXMLParser
from openlp.plugins.custom.lib.db import CustomSlide
from editcustomdialog import Ui_CustomEditDialog

log = logging.getLogger(__name__)

class EditCustomForm(QtGui.QDialog, Ui_CustomEditDialog):
    """
    Class documentation goes here.
    """
    log.info(u'Custom Editor loaded')
    def __init__(self, custommanager, parent = None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        #self.parent = parent
        self.setupUi(self)
        # Connecting signals and slots
        self.previewButton = QtGui.QPushButton()
        self.previewButton.setText(
            translate('CustomPlugin.EditCustomForm', 'Save && Preview'))
        self.buttonBox.addButton(
            self.previewButton, QtGui.QDialogButtonBox.ActionRole)
        QtCore.QObject.connect(self.buttonBox,
            QtCore.SIGNAL(u'clicked(QAbstractButton*)'), self.onPreview)
        QtCore.QObject.connect(self.addButton,
            QtCore.SIGNAL(u'pressed()'), self.onAddButtonPressed)
        QtCore.QObject.connect(self.editButton,
            QtCore.SIGNAL(u'pressed()'), self.onEditButtonPressed)
        QtCore.QObject.connect(self.editAllButton,
            QtCore.SIGNAL(u'pressed()'), self.onEditAllButtonPressed)
        QtCore.QObject.connect(self.saveButton,
            QtCore.SIGNAL(u'pressed()'), self.onSaveButtonPressed)
        QtCore.QObject.connect(self.deleteButton,
            QtCore.SIGNAL(u'pressed()'), self.onDeleteButtonPressed)
        QtCore.QObject.connect(self.clearButton,
            QtCore.SIGNAL(u'pressed()'), self.onClearButtonPressed)
        QtCore.QObject.connect(self.upButton,
            QtCore.SIGNAL(u'pressed()'), self.onUpButtonPressed)
        QtCore.QObject.connect(self.downButton,
            QtCore.SIGNAL(u'pressed()'), self.onDownButtonPressed)
        QtCore.QObject.connect(self.splitButton,
            QtCore.SIGNAL(u'pressed()'), self.onSplitButtonPressed)
        QtCore.QObject.connect(self.verseListView,
            QtCore.SIGNAL(u'itemDoubleClicked(QListWidgetItem*)'),
            self.onVerseListViewSelected)
        QtCore.QObject.connect(self.verseListView,
            QtCore.SIGNAL(u'itemClicked(QListWidgetItem*)'),
            self.onVerseListViewPressed)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_list'), self.loadThemes)
        # Create other objects and forms
        self.custommanager = custommanager
        self.initialise()

    def onPreview(self, button):
        log.debug(u'onPreview')
        if button.text() == unicode(translate('CustomPlugin.EditCustomForm',
            'Save && Preview')) and self.saveCustom():
            Receiver.send_message(u'custom_preview')

    def initialise(self):
        self.editAll = False
        self.addButton.setEnabled(True)
        self.deleteButton.setEnabled(False)
        self.editButton.setEnabled(False)
        self.editAllButton.setEnabled(True)
        self.saveButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.splitButton.setEnabled(False)
        self.titleEdit.setText(u'')
        self.creditEdit.setText(u'')
        self.verseTextEdit.clear()
        self.verseListView.clear()
        #make sure we have a new item
        self.customSlide = CustomSlide()
        self.themeComboBox.addItem(u'')

    def loadThemes(self, themelist):
        self.themeComboBox.clear()
        self.themeComboBox.addItem(u'')
        for themename in themelist:
            self.themeComboBox.addItem(themename)

    def loadCustom(self, id, preview=False):
        self.customSlide = CustomSlide()
        self.initialise()
        if id != 0:
            self.customSlide = self.custommanager.get_object(CustomSlide, id)
            self.titleEdit.setText(self.customSlide.title)
            self.creditEdit.setText(self.customSlide.credits)
            customXML = CustomXMLParser(self.customSlide.text)
            verseList = customXML.get_verses()
            for verse in verseList:
                self.verseListView.addItem(verse[1])
            theme = self.customSlide.theme_name
            id = self.themeComboBox.findText(theme, QtCore.Qt.MatchExactly)
            if id == -1:
                id = 0 # Not Found
            self.themeComboBox.setCurrentIndex(id)
        else:
            self.themeComboBox.setCurrentIndex(0)
        #if not preview hide the preview button
        self.previewButton.setVisible(False)
        if preview:
            self.previewButton.setVisible(True)

    def closePressed(self):
        Receiver.send_message(u'custom_edit_clear')
        self.close()

    def accept(self):
        log.debug(u'accept')
        if self.saveCustom():
            Receiver.send_message(u'custom_load_list')
            self.close()

    def saveCustom(self):
        valid, message = self._validate()
        if not valid:
            QtGui.QMessageBox.critical(self,
                translate('CustomPlugin.EditCustomForm', 'Error'), message,
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
            return False
        sxml = CustomXMLBuilder()
        sxml.new_document()
        sxml.add_lyrics_to_song()
        count = 1
        for i in range(0, self.verseListView.count()):
            sxml.add_verse_to_lyrics(u'custom', unicode(count),
                unicode(self.verseListView.item(i).text()))
            count += 1
        self.customSlide.title = unicode(self.titleEdit.displayText(), u'utf-8')
        self.customSlide.text = unicode(sxml.extract_xml(), u'utf-8')
        self.customSlide.credits = unicode(self.creditEdit.displayText(),
            u'utf-8')
        self.customSlide.theme_name = unicode(self.themeComboBox.currentText(),
            u'utf-8')
        return self.custommanager.save_object(self.customSlide)

    def onUpButtonPressed(self):
        selectedRow = self.verseListView.currentRow()
        if selectedRow != 0:
            qw = self.verseListView.takeItem(selectedRow)
            self.verseListView.insertItem(selectedRow - 1, qw)
            self.verseListView.setCurrentRow(selectedRow - 1)

    def onDownButtonPressed(self):
        selectedRow = self.verseListView.currentRow()
        # zero base arrays
        if selectedRow != self.verseListView.count() - 1:
            qw = self.verseListView.takeItem(selectedRow)
            self.verseListView.insertItem(selectedRow + 1, qw)
            self.verseListView.setCurrentRow(selectedRow + 1)

    def onClearButtonPressed(self):
        self.verseTextEdit.clear()
        self.editAll = False
        self.addButton.setEnabled(True)
        self.editAllButton.setEnabled(True)
        self.saveButton.setEnabled(False)

    def onVerseListViewPressed(self, item):
        self.deleteButton.setEnabled(True)
        self.editButton.setEnabled(True)

    def onVerseListViewSelected(self, item):
        self.editText(item.text())

    def onAddButtonPressed(self):
        self.verseListView.addItem(self.verseTextEdit.toPlainText())
        self.deleteButton.setEnabled(False)
        self.verseTextEdit.clear()

    def onEditButtonPressed(self):
        self.editText(self.verseListView.currentItem().text())

    def onEditAllButtonPressed(self):
        self.editAll = True
        self.addButton.setEnabled(False)
        self.splitButton.setEnabled(True)
        if self.verseListView.count() > 0:
            verse_list = u''
            for row in range(0, self.verseListView.count()):
                item = self.verseListView.item(row)
                verse_list += item.text()
                if row != self.verseListView.count() - 1:
                    verse_list += u'\n[---]\n'
            self.editText(verse_list)

    def editText(self, text):
        self.beforeText = text
        self.verseTextEdit.setPlainText(text)
        self.deleteButton.setEnabled(False)
        self.editButton.setEnabled(False)
        self.editAllButton.setEnabled(False)
        self.saveButton.setEnabled(True)
        self.clearButton.setEnabled(True)

    def onSaveButtonPressed(self):
        if self.editAll:
            self.verseListView.clear()
            for row in unicode(self.verseTextEdit.toPlainText()).split(
                u'\n[---]\n'):
                self.verseListView.addItem(row)
        else:
            self.verseListView.currentItem().setText(
                self.verseTextEdit.toPlainText())
            #number of lines has change
            if len(self.beforeText.split(u'\n')) != \
                len(self.verseTextEdit.toPlainText().split(u'\n')):
                tempList = {}
                for row in range(0, self.verseListView.count()):
                    tempList[row] = self.verseListView.item(row).text()
                self.verseListView.clear()
                for row in range (0, len(tempList)):
                    self.verseListView.addItem(tempList[row])
                self.verseListView.repaint()
        self.addButton.setEnabled(True)
        self.saveButton.setEnabled(False)
        self.editButton.setEnabled(False)
        self.editAllButton.setEnabled(True)
        self.splitButton.setEnabled(False)
        self.verseTextEdit.clear()

    def onSplitButtonPressed(self):
        if self.verseTextEdit.textCursor().columnNumber() != 0:
            self.verseTextEdit.insertPlainText(u'\n')
        self.verseTextEdit.insertPlainText(u'[---]\n' )
        self.verseTextEdit.setFocus()

    def onDeleteButtonPressed(self):
        self.verseListView.takeItem(self.verseListView.currentRow())
        self.editButton.setEnabled(False)
        self.editAllButton.setEnabled(True)

    def _validate(self):
        if len(self.titleEdit.displayText()) == 0:
            self.titleEdit.setFocus()
            return False, translate('CustomPlugin.EditCustomForm',
                'You need to type in a title.')
        # must have 1 slide
        if self.verseListView.count() == 0:
            self.verseTextEdit.setFocus()
            return False, translate('CustomPlugin.EditCustomForm',
                'You need to add at least one slide')
        if self.verseTextEdit.toPlainText():
            self.verseTextEdit.setFocus()
            return False, translate('CustomPlugin.EditCustomForm',
                'You have one or more unsaved slides, please either save your '
                'slide(s) or clear your changes.')
        return True, u''
