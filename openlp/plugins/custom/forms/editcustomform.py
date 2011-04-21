# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
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

import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, translate
from openlp.core.lib.ui import critical_error_message_box, find_and_set_in_combo_box
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
    def __init__(self, parent):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.manager = self.parent.manager
        self.setupUi(self)
        # Create other objects and forms.
        self.editSlideForm = EditCustomSlideForm(self)
        # Connecting signals and slots
        QtCore.QObject.connect(self.previewButton,
            QtCore.SIGNAL(u'pressed()'), self.onPreviewButtonPressed)
        QtCore.QObject.connect(self.addButton,
            QtCore.SIGNAL(u'pressed()'), self.onAddButtonPressed)
        QtCore.QObject.connect(self.editButton,
            QtCore.SIGNAL(u'pressed()'), self.onEditButtonPressed)
        QtCore.QObject.connect(self.editAllButton,
            QtCore.SIGNAL(u'pressed()'), self.onEditAllButtonPressed)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_list'), self.loadThemes)
        QtCore.QObject.connect(self.slideListView,
            QtCore.SIGNAL(u'currentRowChanged(int)'), self.onCurrentRowChanged)

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
        self.slideListView.clear()
        if id == 0:
            self.customSlide = CustomSlide()
            self.titleEdit.setText(u'')
            self.creditEdit.setText(u'')
            self.themeComboBox.setCurrentIndex(0)
        else:
            self.customSlide = self.manager.get_object(CustomSlide, id)
            self.titleEdit.setText(self.customSlide.title)
            self.creditEdit.setText(self.customSlide.credits)
            customXML = CustomXMLParser(self.customSlide.text)
            slideList = customXML.get_verses()
            for slide in slideList:
                self.slideListView.addItem(slide[1])
            theme = self.customSlide.theme_name
            find_and_set_in_combo_box(self.themeComboBox, theme)
        # If not preview hide the preview button.
        self.previewButton.setVisible(False)
        if preview:
            self.previewButton.setVisible(True)

    def reject(self):
        Receiver.send_message(u'custom_edit_clear')
        QtGui.QDialog.reject(self)

    def accept(self):
        log.debug(u'accept')
        if self.saveCustom():
            Receiver.send_message(u'custom_load_list')
            QtGui.QDialog.accept(self)

    def saveCustom(self):
        """
        Saves the custom.
        """
        if not self._validate():
            return False
        sxml = CustomXMLBuilder()
        sxml.new_document()
        sxml.add_lyrics_to_song()
        count = 1
        for i in range(0, self.slideListView.count()):
            sxml.add_verse_to_lyrics(u'custom', unicode(count),
                unicode(self.slideListView.item(i).text()))
            count += 1
        self.customSlide.title = unicode(self.titleEdit.text())
        self.customSlide.text = unicode(sxml.extract_xml(), u'utf-8')
        self.customSlide.credits = unicode(self.creditEdit.text())
        self.customSlide.theme_name = unicode(self.themeComboBox.currentText())
        return self.manager.save_object(self.customSlide)

    def onUpButtonClicked(self):
        selectedRow = self.slideListView.currentRow()
        if selectedRow != 0:
            qw = self.slideListView.takeItem(selectedRow)
            self.slideListView.insertItem(selectedRow - 1, qw)
            self.slideListView.setCurrentRow(selectedRow - 1)

    def onDownButtonClicked(self):
        selectedRow = self.slideListView.currentRow()
        # zero base arrays
        if selectedRow != self.slideListView.count() - 1:
            qw = self.slideListView.takeItem(selectedRow)
            self.slideListView.insertItem(selectedRow + 1, qw)
            self.slideListView.setCurrentRow(selectedRow + 1)

    def onAddButtonPressed(self):
        self.editSlideForm.setText(u'')
        if self.editSlideForm.exec_():
            for slide in self.editSlideForm.getText():
                self.slideListView.addItem(slide)

    def onEditButtonPressed(self):
        self.editSlideForm.setText(self.slideListView.currentItem().text())
        if self.editSlideForm.exec_():
            self.updateSlideList(self.editSlideForm.getText())

    def onEditAllButtonPressed(self):
        """
        Edits all slides.
        """
        slide_list = u''
        for row in range(0, self.slideListView.count()):
            item = self.slideListView.item(row)
            slide_list += item.text()
            if row != self.slideListView.count() - 1:
                slide_list += u'\n[---]\n'
        self.editSlideForm.setText(slide_list)
        if self.editSlideForm.exec_():
            self.updateSlideList(self.editSlideForm.getText(), True)

    def onPreviewButtonPressed(self):
        """
        Save the custom item and preview it.
        """
        log.debug(u'onPreview')
        if self.saveCustom():
            Receiver.send_message(u'custom_preview')

    def updateSlideList(self, slides, edit_all=False):
        """
        Updates the slide list after editing slides.

        ``slides``
            A list of all slides which have been edited.

        ``edit_all``
            Indicates if all slides or only one slide has been edited.
        """
        if edit_all:
            self.slideListView.clear()
            for slide in slides:
                self.slideListView.addItem(slide)
        else:
            old_slides = []
            old_row = self.slideListView.currentRow()
            # Create a list with all (old/unedited) slides.
            old_slides = [self.slideListView.item(row).text() for row in \
                range(0, self.slideListView.count())]
            self.slideListView.clear()
            old_slides.pop(old_row)
            # Insert all slides to make the old_slides list complete.
            for slide in slides:
                old_slides.insert(old_row, slide)
            for slide in old_slides:
                self.slideListView.addItem(slide)
        self.slideListView.repaint()

    def onDeleteButtonClicked(self):
        """
        Removes the current row from the list.
        """
        self.slideListView.takeItem(self.slideListView.currentRow())
        self.onCurrentRowChanged(self.slideListView.currentRow())

    def onCurrentRowChanged(self, row):
        """
        Called when the *slideListView*'s current row has been changed. This
        enables or disables buttons which require an slide to act on.

        ``row``
            The row (int). If there is no current row, the value is -1.
        """
        if row == -1:
            self.deleteButton.setEnabled(False)
            self.editButton.setEnabled(False)
            self.upButton.setEnabled(False)
            self.downButton.setEnabled(False)
        else:
            self.deleteButton.setEnabled(True)
            self.editButton.setEnabled(True)
            # Decide if the up/down buttons should be enabled or not.
            if self.slideListView.count() - 1 == row:
                self.downButton.setEnabled(False)
            else:
                self.downButton.setEnabled(True)
            if row == 0:
                self.upButton.setEnabled(False)
            else:
                self.upButton.setEnabled(True)

    def _validate(self):
        """
        Checks whether a custom is valid or not.
        """
        # We must have a title.
        if len(self.titleEdit.displayText()) == 0:
            self.titleEdit.setFocus()
            critical_error_message_box(
                message=translate('CustomPlugin.EditCustomForm',
                'You need to type in a title.'))
            return False
        # We must have at least one slide.
        if self.slideListView.count() == 0:
            critical_error_message_box(
                message=translate('CustomPlugin.EditCustomForm',
                'You need to add at least one slide'))
            return False
        return True