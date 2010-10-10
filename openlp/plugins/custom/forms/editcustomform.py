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
from editcustomslideform import EditCustomSlideForm

log = logging.getLogger(__name__)

class EditCustomForm(QtGui.QDialog, Ui_CustomEditDialog):
    """
    Class documentation goes here.
    """
    log.info(u'Custom Editor loaded')
    def __init__(self, custommanager, parent=None):
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
        QtCore.QObject.connect(self.deleteButton,
            QtCore.SIGNAL(u'pressed()'), self.onDeleteButtonPressed)
        QtCore.QObject.connect(self.upButton,
            QtCore.SIGNAL(u'pressed()'), self.onUpButtonPressed)
        QtCore.QObject.connect(self.downButton,
            QtCore.SIGNAL(u'pressed()'), self.onDownButtonPressed)
        QtCore.QObject.connect(self.verseListView,
            QtCore.SIGNAL(u'itemClicked(QListWidgetItem*)'),
            self.onVerseListViewPressed)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_list'), self.loadThemes)
        # Create other objects and forms.
        self.custommanager = custommanager
        self.slide_form = EditCustomSlideForm(self)
        self.initialise()

    def onPreview(self, button):
        log.debug(u'onPreview')
        if button.text() == unicode(translate('CustomPlugin.EditCustomForm',
            'Save && Preview')) and self.saveCustom():
            Receiver.send_message(u'custom_preview')

    def initialise(self):
        self.addButton.setEnabled(True)
        self.deleteButton.setEnabled(False)
        self.editButton.setEnabled(False)
        self.editAllButton.setEnabled(True)
        self.titleEdit.setText(u'')
        self.creditEdit.setText(u'')
        self.verseListView.clear()
        # Make sure we have a new item.
        self.customSlide = CustomSlide()

    def loadThemes(self, themelist):
        self.themeComboBox.clear()
        self.themeComboBox.addItem(u'')
        for themename in themelist:
            self.themeComboBox.addItem(themename)

    def loadCustom(self, id, preview=False):
        """
        Called when editing or creating a new custom.

        ``id``
            The cutom's id. If zero, then a new custom is created.

        ``preview``
            States whether the custom is edited while being previewed in the
            preview panel.
        """
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
            self.editAllButton.setEnabled(False)
        # If not preview hide the preview button.
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
        """
        Saves the custom.
        """
        valid, message = self._validate()
        if not valid:
            QtGui.QMessageBox.critical(self,
                translate('CustomPlugin.EditCustomForm', 'Error'), message)
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

    def onVerseListViewPressed(self, item):
        self.deleteButton.setEnabled(True)
        self.editButton.setEnabled(True)

    def onAddButtonPressed(self):
        self.slide_form.setText(u'')
        if self.slide_form.exec_():
            for slide in self.slide_form.getText():
                self.verseListView.addItem(slide)
            self.editAllButton.setEnabled(True)

    def onEditButtonPressed(self):
        self.slide_form.setText(self.verseListView.currentItem().text())
        if self.slide_form.exec_():
            self.updateVerseList(self.slide_form.getText())

    def onEditAllButtonPressed(self):
        """
        Edits all slides.
        """
        if self.verseListView.count() > 0:
            verse_list = u''
            for row in range(0, self.verseListView.count()):
                item = self.verseListView.item(row)
                verse_list += item.text()
                if row != self.verseListView.count() - 1:
                    verse_list += u'\n[---]\n'
            self.slide_form.setText(verse_list)
            if self.slide_form.exec_():
                self.updateVerseList(self.slide_form.getText(), True)

    def updateVerseList(self, slides, edit_all=False):
        """
        Updates the verse list (self.verseListView) after editing slides.

        ``slides``
            A list of all slides which have been edited.

        ``edit_all``
            Indicates if all slides or only one slide has been edited.
        """
        if len(slides) == 1:
            self.verseListView.currentItem().setText(slides[0])
        else:
            if edit_all:
                self.verseListView.clear()
                for slide in slides:
                    self.verseListView.addItem(slide)
            else:
                old_slides = []
                old_row = self.verseListView.currentRow()
                # Create a list with all (old/unedited) slides.
                old_slides = [self.verseListView.item(row).text() for row in \
                    range(0, self.verseListView.count())]
                self.verseListView.clear()
                old_slides.pop(old_row)
                # Insert all slides in the old_slides list, to make the list complete.
                for slide in slides:
                    old_slides.insert(old_row, slide)
                for slide in old_slides:
                    self.verseListView.addItem(slide)
            self.verseListView.repaint()

    def onDeleteButtonPressed(self):
        self.verseListView.takeItem(self.verseListView.currentRow())
        self.editButton.setEnabled(True)
        self.editAllButton.setEnabled(True)
        if self.verseListView.count() == 0:
            self.deleteButton.setEnabled(False)
            self.editButton.setEnabled(False)
            self.editAllButton.setEnabled(False)

    def _validate(self):
        """
        Checks whether a custom is valid or not.
        """
        # We must have a title.
        if len(self.titleEdit.displayText()) == 0:
            self.titleEdit.setFocus()
            return False, translate('CustomPlugin.EditCustomForm',
                'You need to type in a title.')
        # We must have one slide.
        if self.verseListView.count() == 0:
            return False, translate('CustomPlugin.EditCustomForm',
                'You need to add at least one slide')
        return True, u''
