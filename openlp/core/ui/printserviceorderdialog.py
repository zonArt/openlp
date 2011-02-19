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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import build_icon, translate, SpellTextEdit
from openlp.core.lib.ui import UiStrings

class Ui_PrintServiceOrderDialog(object):
    def setupUi(self, printServiceDialog):
        printServiceDialog.setObjectName(u'printServiceDialog')
        printServiceDialog.resize(664, 594)
        self.mainLayout = QtGui.QVBoxLayout(printServiceDialog)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setMargin(0)
        self.mainLayout.setObjectName(u'mainLayout')
        self.toolbar = QtGui.QToolBar(printServiceDialog)
        self.toolbar.setIconSize(QtCore.QSize(22, 22))
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolbar.addAction(
            QtGui.QIcon(build_icon(u':/general/general_print.png')), 'Print')
        self.optionsButton = QtGui.QToolButton(self.toolbar)
        self.optionsButton.setText(u'Options')
        self.optionsButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.optionsButton.setIcon(QtGui.QIcon(
            build_icon(u':/system/system_configure.png')))
        self.optionsButton.setCheckable(True)
        self.toolbar.addWidget(self.optionsButton)
        self.toolbar.addAction(
            QtGui.QIcon(build_icon(u':/system/system_close.png')),
            'Close')
        self.toolbar.addSeparator()
        self.toolbar.addAction(
            QtGui.QIcon(build_icon(u':/system/system_edit_copy.png')),
            'Copy')
        self.toolbar.addAction(
            QtGui.QIcon(build_icon(u':/system/system_edit_copy.png')),
            'Copy as HTML')
        self.toolbar.addSeparator()
        self.zoomInButton = QtGui.QToolButton(self.toolbar)
        self.zoomInButton.setIcon(QtGui.QIcon(
            build_icon(u':/general/general_zoom_in.png')))
        self.zoomInButton.setToolTip(u'Zoom In')
        self.zoomInButton.setObjectName(u'zoomInButton')
        self.zoomInButton.setIconSize(QtCore.QSize(22, 22))
        self.toolbar.addWidget(self.zoomInButton)
        self.zoomOutButton = QtGui.QToolButton(self.toolbar)
        self.zoomOutButton.setIcon(QtGui.QIcon(
            build_icon(u':/general/general_zoom_out.png')))
        self.zoomOutButton.setToolTip(u'Zoom Out')
        self.zoomOutButton.setObjectName(u'zoomOutButton')
        self.zoomOutButton.setIconSize(QtCore.QSize(22, 22))
        self.toolbar.addWidget(self.zoomOutButton)
        self.zoomOriginalButton = QtGui.QToolButton(self.toolbar)
        self.zoomOriginalButton.setIcon(QtGui.QIcon(
            build_icon(u':/general/general_zoom_original.png')))
        self.zoomOriginalButton.setToolTip(u'Zoom Original')
        self.zoomOriginalButton.setObjectName(u'zoomOriginalButton')
        self.zoomOriginalButton.setIconSize(QtCore.QSize(22, 22))
        self.toolbar.addWidget(self.zoomOriginalButton)
        self.zoomComboBox = QtGui.QComboBox(printServiceDialog)
        self.zoomComboBox.setObjectName((u'zoomComboBox'))
        self.zoomComboBox.addItem(u'Fit Page')
        self.zoomComboBox.addItem(u'Fit Width')
        self.zoomComboBox.addItem(u'100%')
        self.zoomComboBox.addItem(u'75%')
        self.zoomComboBox.addItem(u'50%')
        self.zoomComboBox.addItem(u'25%')
        self.toolbar.addWidget(self.zoomComboBox)
        self.mainLayout.addWidget(self.toolbar)
        self.scrollArea = QtGui.QScrollArea(printServiceDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(u'scrollArea')
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 227, 473))
        self.scrollAreaWidgetContents.setObjectName(u'scrollAreaWidgetContents')
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.mainLayout.addWidget(self.scrollArea)
        self.optionsWidget = QtGui.QWidget(printServiceDialog)
        self.optionsWidget.hide()
        self.optionsWidget.resize(400, 300)
        self.optionsWidget.setAutoFillBackground(True)
        self.optionsLayout = QtGui.QVBoxLayout(self.optionsWidget)
        self.optionsLayout.setContentsMargins(8, 8, 8, 8)
        self.titleLabel = QtGui.QLabel(self.optionsWidget)
        self.titleLabel.setObjectName((u'titleLabel'))
        self.titleLabel.setText(u'Title:')
        self.optionsLayout.addWidget(self.titleLabel)
        self.titleLineEdit = QtGui.QLineEdit(self.optionsWidget)
        self.titleLineEdit.setObjectName(u'titleLineEdit')
        self.optionsLayout.addWidget(self.titleLineEdit)
        self.footerLabel = QtGui.QLabel(self.optionsWidget)
        self.footerLabel.setObjectName(u'footerLabel')
        self.footerLabel.setText(u'Custom Footer Text:')
        self.optionsLayout.addWidget(self.footerLabel)
        self.footerTextEdit = QtGui.QTextEdit(self.optionsWidget)
        self.footerTextEdit.setObjectName(u'footerTextEdit')
        self.optionsLayout.addWidget(self.footerTextEdit)
        self.optionsGroupBox = QtGui.QGroupBox(u'Other Options')
        self.groupLayout = QtGui.QVBoxLayout()
        self.slideTextCheckBox = QtGui.QCheckBox()
        self.groupLayout.addWidget(self.slideTextCheckBox)
        self.notesCheckBox = QtGui.QCheckBox('Include service item notes')
        self.groupLayout.addWidget(self.notesCheckBox)
        self.metaDataCheckBox = QtGui.QCheckBox()
        self.groupLayout.addWidget(self.metaDataCheckBox)
        self.groupLayout.addStretch(1)
        self.optionsGroupBox.setLayout(self.groupLayout)
        self.optionsLayout.addWidget(self.optionsGroupBox)

        self.retranslateUi(printServiceDialog)
        QtCore.QMetaObject.connectSlotsByName(printServiceDialog)
        QtCore.QObject.connect(self.optionsButton,
            QtCore.SIGNAL(u'toggled(bool)'), self.toggleOptions)

        self.retranslateUi(printServiceDialog)
        QtCore.QMetaObject.connectSlotsByName(printServiceDialog)

    def retranslateUi(self, printServiceDialog):
        printServiceDialog.setWindowTitle(
            translate('OpenLP.PrintServiceOrderForm', 'Print Service Order'))
#        self.previewLabel.setText(
#            translate('OpenLP.PrintServiceOrderForm', '<b>Preview:</b>'))
        self.slideTextCheckBox.setText(translate(
            'OpenLP.PrintServiceOrderForm', 'Include slide text if available'))
        self.notesCheckBox.setText(translate(
            'OpenLP.PrintServiceOrderForm', 'Include service item notes'))
        self.metaDataCheckBox.setText(
            translate('OpenLP.PrintServiceOrderForm',
            'Include play length of media items'))
#        self.serviceTitleLabel.setText(translate(
#            'OpenLP.PrintServiceOrderForm', 'Title:'))
#        self.serviceTitleLineEdit.setText(translate('OpenLP.ServiceManager',
#            'Service Order Sheet'))
#        self.copyTextButton.setText(translate('OpenLP.ServiceManager',
#            'Copy to Clipboard as Text'))
#        self.copyHtmlButton.setText(translate('OpenLP.ServiceManager',
#            'Copy to Clipboard as Html'))
#        self.printButton.setText(translate('OpenLP.ServiceManager', 'Print'))
#        self.cancelButton.setText(translate('OpenLP.ServiceManager', 'Cancel'))
#        self.customNotesLabel.setText(
#            translate('OpenLP.ServiceManager', '<b>Custom Service Notes:</b>'))
