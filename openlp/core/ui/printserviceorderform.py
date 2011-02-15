# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
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
import datetime

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import UiStrings
from openlp.core.ui.printserviceorderdialog import Ui_PrintServiceOrderDialog

class PrintServiceOrderForm(QtGui.QDialog, Ui_PrintServiceOrderDialog):

    def __init__(self, parent, serviceManager):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.serviceManager = serviceManager
        self.printer = QtGui.QPrinter()
        self.printDialog = QtGui.QPrintDialog(self.printer, self)
        self.document = QtGui.QTextDocument()
        self.setupUi(self)
        # Load the settings for the dialog.
        settings = QtCore.QSettings()
        settings.beginGroup(u'advanced')
        self.printSlideTextCheckBox.setChecked(settings.value(
            u'print slide text', QtCore.QVariant(False)).toBool())
        self.printMetaDataCheckBox.setChecked(settings.value(
            u'print file meta data', QtCore.QVariant(False)).toBool())
        self.printNotesCheckBox.setChecked(settings.value(
            u'print notes', QtCore.QVariant(False)).toBool())
        self.copyMetaDataCheckBox.setChecked(settings.value(
            u'html copy', QtCore.QVariant(False)).toBool())
        if self.copyMetaDataCheckBox.isChecked():
            self.copyTextButton.setText(UiStrings.CopyToHtml)
        settings.endGroup()
        # Signals
        QtCore.QObject.connect(self.printButton,
            QtCore.SIGNAL(u'clicked()'), self.printServiceOrder)
        QtCore.QObject.connect(self.zoomOutButton,
            QtCore.SIGNAL(u'clicked()'), self.zoomOut)
        QtCore.QObject.connect(self.zoomInButton,
            QtCore.SIGNAL(u'clicked()'), self.zoomIn)
        QtCore.QObject.connect(self.previewWidget,
            QtCore.SIGNAL(u'paintRequested(QPrinter *)'), self.paintRequested)
        QtCore.QObject.connect(self.serviceTitleLineEdit,
            QtCore.SIGNAL(u'textChanged(const QString)'),
            self.updatePreviewText)
        QtCore.QObject.connect(self.printSlideTextCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.updatePreviewText)
        QtCore.QObject.connect(self.printNotesCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.updatePreviewText)
        QtCore.QObject.connect(self.printMetaDataCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.updatePreviewText)
        QtCore.QObject.connect(self.customNoteEdit,
            QtCore.SIGNAL(u'textChanged()'), self.updatePreviewText)
        QtCore.QObject.connect(self.cancelButton,
            QtCore.SIGNAL(u'clicked()'), self.reject)
        QtCore.QObject.connect(self.copyTextButton,
            QtCore.SIGNAL(u'clicked()'), self.copyText)
        QtCore.QObject.connect(self.copyMetaDataCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'), self.updateTextFormat)
        self.updatePreviewText()

    def updatePreviewText(self):
        """
        Creates the html text and updates the html of *self.document*.
        """
        text = u''
        if self.serviceTitleLineEdit.text():
            text += u'<h2>%s</h2>' % unicode(self.serviceTitleLineEdit.text())
        for item in self.serviceManager.serviceItems:
            item = item[u'service_item']
            # Add the title of the service item.
            text += u'<h3><img src="%s" /> %s</h3>' % (item.icon,
                item.get_display_title())
            # Add slide text of the service item.
            if self.printSlideTextCheckBox.isChecked():
                if item.is_text():
                    # Add the text of the service item.
                    verse = None
                    for slide in item.get_frames():
                        if not verse:
                            text += u'<p>' + slide[u'html']
                            verse = slide[u'verseTag']
                        elif verse != slide[u'verseTag']:
                            text += u'<\p><p>' + slide[u'html']
                            verse = slide[u'verseTag']
                        else:
                            text += u'<br/>' + slide[u'html']
                    text += u'</p>'
                elif item.is_image():
                    # Add the image names of the service item.
                    text += u'<ol>'
                    for slide in range(len(item.get_frames())):
                        text += u'<li><p>%s</p></li>' % \
                            item.get_frame_title(slide)
                    text += u'</ol>'
                if item.foot_text:
                    # add footer
                    text += u'<p>%s</p>' % item.foot_text
            # Add service items' notes.
            if self.printNotesCheckBox.isChecked():
                if item.notes:
                    text += u'<p><b>%s</b></p>%s' % (translate(
                        'OpenLP.ServiceManager', 'Notes:'),
                        item.notes.replace(u'\n', u'<br />'))
            # Add play length of media files.
            if item.is_media() and self.printMetaDataCheckBox.isChecked():
                text += u'<p><b>%s</b> %s</p>' % (translate(
                    'OpenLP.ServiceManager', u'Playing time:'),
                    unicode(datetime.timedelta(seconds=item.media_length)))
        if self.customNoteEdit.toPlainText():
            text += u'<h4>%s</h4>%s' % (translate('OpenLP.ServiceManager',
                u'Custom Service Notes:'), self.customNoteEdit.toPlainText())
        self.document.setHtml(text)
        self.previewWidget.updatePreview()

    def paintRequested(self, printer):
        """
        Paint the preview of the *self.document*.

        ``printer``
            A *QPrinter* object.
        """
        self.document.print_(printer)

    def copyText(self):
        if self.copyMetaDataCheckBox.isChecked():
            self.parent.clipboard.setText(self.document.toHtml())
        else:
            self.parent.clipboard.setText(self.document.toPlainText())
        self.accept()

    def printServiceOrder(self):
        """
        Called, when the *printButton* is clicked. Opens the *printDialog*.
        """
        if not self.printDialog.exec_():
            return
        # Print the document.
        self.document.print_(self.printer)
        self.accept()

    def zoomIn(self):
        """
        Called when *zoomInButton* is clicked.
        """
        self.previewWidget.zoomIn()

    def zoomOut(self):
        """
        Called when *zoomOutButton* is clicked.
        """
        self.previewWidget.zoomOut()

    def updateTextFormat(self, value):
        """
        Called when html copy check box is selected.
        """
        if value == QtCore.Qt.Checked:
            self.copyTextButton.setText(UiStrings.CopyToHtml)
        else:
            self.copyTextButton.setText(UiStrings.CopyToText)

    def accept(self):
        """
        Save the settings and close the dialog.
        """
        # Save the settings for this dialog.
        settings = QtCore.QSettings()
        settings.beginGroup(u'advanced')
        settings.setValue(u'print slide text',
            QtCore.QVariant(self.printSlideTextCheckBox.isChecked()))
        settings.setValue(u'print file meta data',
            QtCore.QVariant(self.printMetaDataCheckBox.isChecked()))
        settings.setValue(u'print notes',
            QtCore.QVariant(self.printNotesCheckBox.isChecked()))
        settings.setValue(u'html copy',
            QtCore.QVariant(self.copyMetaDataCheckBox.isChecked()))
        settings.endGroup()
        # Close the dialog.
        return QtGui.QDialog.accept(self)

    def reject(self):
        """
        Close the dialog, do not print the service and do not save the settings.
        """
        return QtGui.QDialog.reject(self)
