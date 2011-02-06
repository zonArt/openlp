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
import mutagen
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import save_cancel_button_box


class PrintServiceOrderForm(QtGui.QDialog):
    def __init__(self, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.serviceManager = parent
        self.printer = QtGui.QPrinter()
        self.printDialog = QtGui.QPrintDialog(self.printer, self)
        self.document = QtGui.QTextDocument()
        self.setupUi()
        self.retranslateUi()
        # Load the settings for this dialog.
        settings = QtCore.QSettings()
        settings.beginGroup(u'advanced')
        self.printSlideTextCheckBox.setChecked(settings.value(
            u'print slide text', QtCore.QVariant(False)).toBool())
        self.printMetaDataCheckBox.setChecked(settings.value(
            u'print file meta data', QtCore.QVariant(False)).toBool())
        self.printNotesCheckBox.setChecked(settings.value(
            u'print notes', QtCore.QVariant(False)).toBool())
        settings.endGroup()
        # Signals
        QtCore.QObject.connect(self.printButton,
            QtCore.SIGNAL('clicked()'), self.printServiceOrder)
        QtCore.QObject.connect(self.zoomOutButton,
            QtCore.SIGNAL('clicked()'), self.zoomOut)
        QtCore.QObject.connect(self.zoomInButton,
            QtCore.SIGNAL('clicked()'), self.zoomIn)
        QtCore.QObject.connect(self.previewWidget,
            QtCore.SIGNAL('paintRequested(QPrinter *)'), self.paintRequested)
        QtCore.QObject.connect(self.serviceTitleLineEdit,
            QtCore.SIGNAL('textChanged(const QString)'), self.updatePreviewText)
        QtCore.QObject.connect(self.printSlideTextCheckBox,
            QtCore.SIGNAL('stateChanged(int)'), self.updatePreviewText)
        QtCore.QObject.connect(self.printNotesCheckBox,
            QtCore.SIGNAL('stateChanged(int)'), self.updatePreviewText)
        QtCore.QObject.connect(self.printMetaDataCheckBox,
            QtCore.SIGNAL('stateChanged(int)'), self.updatePreviewText)
        self.updatePreviewText()

    def setupUi(self):
        self.dialogLayout = QtGui.QHBoxLayout(self)
        self.dialogLayout.setObjectName(u'dialogLayout')
        self.perviewLayout = QtGui.QVBoxLayout()
        self.perviewLayout.setObjectName(u'perviewLayout')
        self.previewLabel = QtGui.QLabel(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewLabel.sizePolicy().hasHeightForWidth())
        self.previewLabel.setSizePolicy(sizePolicy)
        self.previewLabel.setObjectName(u'previewLabel')
        self.perviewLayout.addWidget(self.previewLabel)
        self.previewWidget = QtGui.QPrintPreviewWidget(self.printer, self, QtCore.Qt.Widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewWidget.sizePolicy().hasHeightForWidth())
        self.previewWidget.setSizePolicy(sizePolicy)
        self.previewWidget.setObjectName(u'previewWidget')
        self.previewWidget.fitToWidth()
        self.perviewLayout.addWidget(self.previewWidget)
        self.dialogLayout.addLayout(self.perviewLayout)
        self.settingsLayout = QtGui.QVBoxLayout()
        self.settingsLayout.setObjectName(u'settingsLayout')
        self.serviceTitleLayout = QtGui.QHBoxLayout()
        self.serviceTitleLayout.setObjectName(u'serviceTitleLayout')
        self.serviceTitleLabel = QtGui.QLabel(self)
        self.serviceTitleLabel.setObjectName(u'serviceTitleLabel')
        self.serviceTitleLayout.addWidget(self.serviceTitleLabel)
        self.serviceTitleLineEdit = QtGui.QLineEdit(self)
        self.serviceTitleLineEdit.setSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.serviceTitleLineEdit.setObjectName(u'serviceTitleLineEdit')
        self.serviceTitleLayout.addWidget(self.serviceTitleLineEdit)
        self.settingsLayout.addLayout(self.serviceTitleLayout)
        self.printSlideTextCheckBox = QtGui.QCheckBox(self)
        self.printSlideTextCheckBox.setObjectName(u'printSlideTextCheckBox')
        self.settingsLayout.addWidget(self.printSlideTextCheckBox)
        self.printNotesCheckBox = QtGui.QCheckBox(self)
        self.printNotesCheckBox.setObjectName(u'printNotesCheckBox')
        self.settingsLayout.addWidget(self.printNotesCheckBox)
        self.printMetaDataCheckBox = QtGui.QCheckBox(self)
        self.printMetaDataCheckBox.setObjectName(u'printMetaDataCheckBox')
        self.settingsLayout.addWidget(self.printMetaDataCheckBox)
        self.buttonLayout = QtGui.QHBoxLayout()
        self.zoomOutButton = QtGui.QToolButton(self)
        icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(u':/exports/export_move_to_list.png'),
        icon.addPixmap(QtGui.QPixmap(u'/home/andreas/zoom-out.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoomOutButton.setIcon(icon)
        self.zoomOutButton.setObjectName(u'zoomOutButton')
        self.buttonLayout.addWidget(self.zoomOutButton)
        self.zoomInButton = QtGui.QToolButton(self)
        icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(u':/exports/export_remove.png'),
        icon.addPixmap(QtGui.QPixmap(u'/home/andreas/zoom-in.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoomInButton.setIcon(icon)
        self.zoomInButton.setObjectName(u'toolButton')
        self.buttonLayout.addWidget(self.zoomInButton)
        spacerItem = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.settingsLayout.addItem(spacerItem)
        self.buttonLayout.setObjectName(u'buttonLayout')
        spacerItem = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.buttonLayout.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(self)
        self.cancelButton.setObjectName(u'cancelButton')
        self.buttonLayout.addWidget(self.cancelButton)
        self.printButton = QtGui.QPushButton(self)
        self.printButton.setObjectName(u'printButton')
        self.buttonLayout.addWidget(self.printButton)
        self.settingsLayout.addLayout(self.buttonLayout)
        self.dialogLayout.addLayout(self.settingsLayout)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(
            translate('OpenLP.PrintServiceOrderForm', 'Print Service Order'))
        self.previewLabel.setText(
            translate('OpenLP.ServiceManager', '<b>Preview:</b>'))
        self.printSlideTextCheckBox.setText(translate(
            'OpenLP.PrintServiceOrderForm', 'Include slide text if avaialbe'))
        self.printNotesCheckBox.setText(translate(
            'OpenLP.PrintServiceOrderForm', 'Include service item notes'))
        self.printMetaDataCheckBox.setText(
            translate('OpenLP.PrintServiceOrderForm',
            'Include play lenght of media items'))
        self.serviceTitleLabel.setText(translate(
            'OpenLP.PrintServiceOrderForm', 'Title:'))
        self.serviceTitleLineEdit.setText(translate('OpenLP.ServiceManager',
            'Service Order Sheet'))
        self.printButton.setText(translate('OpenLP.ServiceManager', 'Print'))
        self.cancelButton.setText(translate('OpenLP.ServiceManager', 'Cancel'))

    def updatePreviewText(self):
        """
        Creates the html text, to print the service items.
        """
        text = u''
        if self.serviceTitleLineEdit.text():
            text += u'<h2>%s</h2>' % unicode(self.serviceTitleLineEdit.text())
        for item in self.serviceManager.serviceItems:
            item = item[u'service_item']
            # Add the title of the service item.
            text += u'<h4><img src="%s" /> %s</h4>' % (item.icon,
                item.get_display_title())
            # Add slide text of the service item.
            if self.printSlideTextCheckBox.isChecked():
                if item.is_text():
                    # Add the text of the service item.
                    for slide in item.get_frames():
                        text += u'<p>' + slide[u'text'] + u'</p>'
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
                    text += u'<p><b>%s</b></p><br />%s' % (translate(
                        'OpenLP.ServiceManager', 'Notes:'),
                        item.notes.replace(u'\n', u'<br />'))
            # Add play length of media files.
            if item.is_media() and self.printMetaDataCheckBox.isChecked():
                path = os.path.join(item.get_frames()[0][u'path'],
                    item.get_frames()[0][u'title'])
                if not os.path.isfile(path):
                    continue
                file = mutagen.File(path)
                if file is not None:
                    length = int(file.info.length)
                    text += u'<p><b>%s</b> %s</p>' % (translate(
                        'OpenLP.ServiceManager', u'Playing time:'),
                        unicode(datetime.timedelta(seconds=length)))
        self.document.setHtml(text)
        self.previewWidget.updatePreview()

    def paintRequested(self, printer):
        """
        Paint the preview.
        """
        self.document.print_(printer)   

    def printServiceOrder(self):
        if not self.printDialog.exec_():
            return
        self.document.print_(self.printer)
        # Save the settings for this dialog.
        settings = QtCore.QSettings()
        settings.beginGroup(u'advanced')
        settings.setValue(u'print slide text',
            QtCore.QVariant(self.printSlideTextCheckBox.isChecked()))
        settings.setValue(u'print file meta data',
            QtCore.QVariant(self.printMetaDataCheckBox.isChecked()))
        settings.setValue(u'print notes',
            QtCore.QVariant(self.printNotesCheckBox.isChecked()))
        settings.endGroup()

    def zoomIn(self):
        self.previewWidget.zoomIn()
        
    def zoomOut(self):
        self.previewWidget.zoomOut()
