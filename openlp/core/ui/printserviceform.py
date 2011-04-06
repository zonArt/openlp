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
import datetime

from PyQt4 import QtCore, QtGui
from lxml import html

from openlp.core.lib import translate
from openlp.core.lib.ui import UiStrings
from openlp.core.ui.printservicedialog import Ui_PrintServiceDialog, ZoomSize

class PrintServiceForm(QtGui.QDialog, Ui_PrintServiceDialog):

    def __init__(self, mainWindow, serviceManager):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, mainWindow)
        self.mainWindow = mainWindow
        self.serviceManager = serviceManager
        self.printer = QtGui.QPrinter()
        self.printDialog = QtGui.QPrintDialog(self.printer, self)
        self.document = QtGui.QTextDocument()
        self.zoom = 0
        self.setupUi(self)
        # Load the settings for the dialog.
        settings = QtCore.QSettings()
        settings.beginGroup(u'advanced')
        self.slideTextCheckBox.setChecked(settings.value(
            u'print slide text', QtCore.QVariant(False)).toBool())
        self.pageBreakAfterText.setChecked(settings.value(
            u'enable page break', QtCore.QVariant(False)).toBool())
        if not self.slideTextCheckBox.isChecked():
            self.pageBreakAfterText.setDisabled(True)
        self.metaDataCheckBox.setChecked(settings.value(
            u'print file meta data', QtCore.QVariant(False)).toBool())
        self.notesCheckBox.setChecked(settings.value(
            u'print notes', QtCore.QVariant(False)).toBool())
        self.zoomComboBox.setCurrentIndex(settings.value(
            u'display size', QtCore.QVariant(0)).toInt()[0])
        settings.endGroup()
        # Signals
        QtCore.QObject.connect(self.printButton,
            QtCore.SIGNAL(u'triggered()'), self.printServiceOrder)
        QtCore.QObject.connect(self.closeButton,
            QtCore.SIGNAL(u'triggered()'), self.accept)
        QtCore.QObject.connect(self.zoomOutButton,
            QtCore.SIGNAL(u'clicked()'), self.zoomOut)
        QtCore.QObject.connect(self.zoomInButton,
            QtCore.SIGNAL(u'clicked()'), self.zoomIn)
        QtCore.QObject.connect(self.zoomOriginalButton,
            QtCore.SIGNAL(u'clicked()'), self.zoomOriginal)
        QtCore.QObject.connect(self.previewWidget,
            QtCore.SIGNAL(u'paintRequested(QPrinter *)'), self.paintRequested)
        QtCore.QObject.connect(self.zoomComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'), self.displaySizeChanged)
        QtCore.QObject.connect(self.plainCopy,
            QtCore.SIGNAL(u'triggered()'), self.copyText)
        QtCore.QObject.connect(self.htmlCopy,
            QtCore.SIGNAL(u'triggered()'), self.copyHtmlText)
        QtCore.QObject.connect(self.slideTextCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onSlideTextCheckBoxChanged)
        self.updatePreviewText()

    def toggleOptions(self, checked):
        self.optionsWidget.setVisible(checked)
        if checked:
            left = self.optionsButton.pos().x()
            top = self.toolbar.height()
            self.optionsWidget.move(left, top)
            self.titleLineEdit.setFocus()
        else:
            self.saveOptions()
        self.updatePreviewText()

    def updatePreviewText(self):
        """
        Creates the html text and updates the html of *self.document*.
        """
        html_data = html.fromstring(
            u'<title>%s</title>' % unicode(self.titleLineEdit.text()))
        html_data.append(html.Element(u'body'))
        html_data.body.append(html.fromstring(
            u'<h2>%s</h2>' % unicode(self.titleLineEdit.text())))
        for index, item in enumerate(self.serviceManager.serviceItems):
            item = item[u'service_item']
            div = html.Element(u'div')
            # Add the title of the service item.
            item_title = html.Element(u'h3')
            icon = html.Element(u'img')
            icon.set(u'src', item.icon)
            item_title.append(icon)
            item_title.append(
                html.fromstring(u'<span> %s</span>' % item.get_display_title()))
            div.append(item_title)
            if self.slideTextCheckBox.isChecked():
                # Add the text of the service item.
                if item.is_text():
                    verse_def = None
                    for slide in item.get_frames():
                        if not verse_def or verse_def != slide[u'verseTag']:
                            p = html.Element(u'p')
                            div.append(p)
                        else:
                            p.append(html.Element(u'br'))
                        p.append(html.fromstring(
                            u'<span>%s</span>' % slide[u'html']))
                        verse_def = slide[u'verseTag']
                    # Break the page before the div element.
                    if index != 0 and self.pageBreakAfterText.isChecked():
                        div.set(u'style', u'page-break-before:always')
                # Add the image names of the service item.
                elif item.is_image():
                    ol = html.Element(u'ol')
                    for slide in range(len(item.get_frames())):
                        li = html.Element(u'li')
                        li.text = item.get_frame_title(slide)
                        ol.append(li)
                    div.append(ol)
                # add footer
                if item.foot_text:
                    div.append(html.fromstring(item.foot_text))
            # Add service items' notes.
            if self.notesCheckBox.isChecked():
                if item.notes:
                    p = html.Element(u'p')
                    strong = html.Element(u'strong')
                    strong.text = unicode(
                        translate('OpenLP.ServiceManager', 'Notes:'))
                    p.append(strong)
                    p.append(html.fromstring(u'<span>%s</span>' %
                        item.notes.replace(u'\n', u'<br />')))
                    div.append(p)
            # Add play length of media files.
            if item.is_media() and self.metaDataCheckBox.isChecked():
                tme = item.media_length
                if item.end_time > 0:
                    tme = item.end_time - item.start_time
                p = html.fromstring(u'<p><strong>%s</strong> </p>' % 
                    translate('OpenLP.ServiceManager', 'Playing time:'))
                p.append(html.fromstring(u'<span>%s</span>' %
                    unicode(datetime.timedelta(seconds=tme))))
                div.append(p)
            html_data.body.append(div)
        # Add the custom service notes:
        if self.footerTextEdit.toPlainText():            
            html_data.append(html.fromstring(u'<h4>%</h4>' %
                translate('OpenLP.ServiceManager', u'Custom Service Notes:')))
            html_data.append(html.fromstring(
                u'<span>%s</span>' % self.footerTextEdit.toPlainText()))
        for div in html_data.body:
            print len(div), html.tostring(div), u'\n'
        self.document.setHtml(html.tostring(html_data))
        self.previewWidget.updatePreview()

    def paintRequested(self, printer):
        """
        Paint the preview of the *self.document*.

        ``printer``
            A *QPrinter* object.
        """
        self.document.print_(printer)

    def displaySizeChanged(self, display):
        """
        The Zoom Combo box has changed so set up the size.
        """
        if display == ZoomSize.Page:
            self.previewWidget.fitInView()
        elif display == ZoomSize.Width:
            self.previewWidget.fitToWidth()
        elif display == ZoomSize.OneHundred:
            self.previewWidget.fitToWidth()
            self.previewWidget.zoomIn(1)
        elif display == ZoomSize.SeventyFive:
            self.previewWidget.fitToWidth()
            self.previewWidget.zoomIn(0.75)
        elif display == ZoomSize.Fifty:
            self.previewWidget.fitToWidth()
            self.previewWidget.zoomIn(0.5)
        elif display == ZoomSize.TwentyFive:
            self.previewWidget.fitToWidth()
            self.previewWidget.zoomIn(0.25)
        settings = QtCore.QSettings()
        settings.beginGroup(u'advanced')
        settings.setValue(u'display size', QtCore.QVariant(display))
        settings.endGroup()

    def copyText(self):
        """
        Copies the display text to the clipboard as plain text
        """
        self.mainWindow.clipboard.setText(
            self.document.toPlainText())

    def copyHtmlText(self):
        """
        Copies the display text to the clipboard as Html
        """
        self.mainWindow.clipboard.setText(self.document.toHtml())

    def printServiceOrder(self):
        """
        Called, when the *printButton* is clicked. Opens the *printDialog*.
        """
        if not self.printDialog.exec_():
            return
        # Print the document.
        self.document.print_(self.printer)

    def zoomIn(self):
        """
        Called when *zoomInButton* is clicked.
        """
        self.previewWidget.zoomIn()
        self.zoom -= 0.1

    def zoomOut(self):
        """
        Called when *zoomOutButton* is clicked.
        """
        self.previewWidget.zoomOut()
        self.zoom += 0.1

    def zoomOriginal(self):
        """
        Called when *zoomOutButton* is clicked.
        """
        self.previewWidget.zoomIn(1 + self.zoom)
        self.zoom = 0

    def updateTextFormat(self, value):
        """
        Called when html copy check box is selected.
        """
        if value == QtCore.Qt.Checked:
            self.copyTextButton.setText(UiStrings.CopyToHtml)
        else:
            self.copyTextButton.setText(UiStrings.CopyToText)

    def onSlideTextCheckBoxChanged(self, state):
        """
        The ``slideTextCheckBox`` checkbox was either checked or unchecked.
        """
        self.pageBreakAfterText.setDisabled(state == QtCore.Qt.Unchecked)

    def saveOptions(self):
        """
        Save the settings and close the dialog.
        """
        # Save the settings for this dialog.
        settings = QtCore.QSettings()
        settings.beginGroup(u'advanced')
        settings.setValue(u'print slide text',
            QtCore.QVariant(self.slideTextCheckBox.isChecked()))
        settings.setValue(u'enable page break',
            QtCore.QVariant(self.pageBreakAfterText.isChecked()))
        settings.setValue(u'print file meta data',
            QtCore.QVariant(self.metaDataCheckBox.isChecked()))
        settings.setValue(u'print notes',
            QtCore.QVariant(self.notesCheckBox.isChecked()))
        settings.endGroup()
