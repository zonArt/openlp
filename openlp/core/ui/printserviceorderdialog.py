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
    def setupUi(self, printServiceOrderDialog):
        printServiceOrderDialog.setObjectName(u'printServiceOrderDialog')
        self.dialogLayout = QtGui.QGridLayout(printServiceOrderDialog)
        self.dialogLayout.setObjectName(u'dialogLayout')
        self.perviewLayout = QtGui.QVBoxLayout()
        self.perviewLayout.setObjectName(u'perviewLayout')
        self.previewLabel = QtGui.QLabel(printServiceOrderDialog)
        self.previewLabel.setSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.previewLabel.setObjectName(u'previewLabel')
        self.perviewLayout.addWidget(self.previewLabel)
        self.previewWidget = QtGui.QPrintPreviewWidget(
            self.printer, self, QtCore.Qt.Widget)
        self.previewWidget.setEnabled(True)
        self.previewWidget.setSizePolicy(
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        self.previewWidget.setObjectName(u'previewWidget')
        # Give the previewWidget a fixed size, to prevent resizing when clicking
        # the zoom buttons.
        self.previewWidget.setFixedWidth(350)
        self.perviewLayout.addWidget(self.previewWidget)
        self.dialogLayout.addLayout(self.perviewLayout, 0, 0, 1, 1)
        self.settingsLayout = QtGui.QVBoxLayout()
        self.settingsLayout.setObjectName(u'settingsLayout')
        self.serviceTitleLayout = QtGui.QGridLayout()
        self.serviceTitleLayout.setObjectName(u'serviceTitleLayout')
        self.serviceTitleLineEdit = QtGui.QLineEdit(printServiceOrderDialog)
        self.serviceTitleLineEdit.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.serviceTitleLineEdit.setObjectName(u'serviceTitleLineEdit')
        self.serviceTitleLayout.addWidget(self.serviceTitleLineEdit, 1, 1, 1, 1)
        self.serviceTitleLabel = QtGui.QLabel(printServiceOrderDialog)
        self.serviceTitleLabel.setSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.serviceTitleLabel.setObjectName(u'serviceTitleLabel')
        self.serviceTitleLayout.addWidget(self.serviceTitleLabel, 1, 0, 1, 1)
        self.settingsLayout.addLayout(self.serviceTitleLayout)
        self.printSlideTextCheckBox = QtGui.QCheckBox(printServiceOrderDialog)
        self.printSlideTextCheckBox.setObjectName(u'printSlideTextCheckBox')
        self.settingsLayout.addWidget(self.printSlideTextCheckBox)
        self.printNotesCheckBox = QtGui.QCheckBox(printServiceOrderDialog)
        self.printNotesCheckBox.setObjectName(u'printNotesCheckBox')
        self.settingsLayout.addWidget(self.printNotesCheckBox)
        self.printMetaDataCheckBox = QtGui.QCheckBox(printServiceOrderDialog)
        self.printMetaDataCheckBox.setObjectName(u'printMetaDataCheckBox')
        self.settingsLayout.addWidget(self.printMetaDataCheckBox)
        spacerItem = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.settingsLayout.addItem(spacerItem)
        self.customNotesLabel = QtGui.QLabel(self)
        self.customNotesLabel.setObjectName(u'customNotesLabel')
        self.settingsLayout.addWidget(self.customNotesLabel)
        self.customNoteEdit = SpellTextEdit(self)
        self.customNoteEdit.setObjectName(u'customNoteEdit')
        self.settingsLayout.addWidget(self.customNoteEdit)
        self.dialogLayout.addLayout(self.settingsLayout, 0, 3, 1, 1)
        self.buttonLayout = QtGui.QHBoxLayout()
        self.buttonLayout.setObjectName(u'buttonLayout')
        spacerItem = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.buttonLayout.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(printServiceOrderDialog)
        self.cancelButton.setObjectName(u'cancelButton')
        self.buttonLayout.addWidget(self.cancelButton)
        self.printButton = QtGui.QPushButton(printServiceOrderDialog)
        self.printButton.setObjectName(u'printButton')
        self.buttonLayout.addWidget(self.printButton)
        self.dialogLayout.addLayout(self.buttonLayout, 1, 3, 1, 1)
        self.zoomButtonLayout = QtGui.QHBoxLayout()
        self.zoomButtonLayout.setObjectName(u'zoomButtonLayout')
        spacerItem = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.zoomButtonLayout.addItem(spacerItem)
        self.zoomOutButton = QtGui.QToolButton(printServiceOrderDialog)
        self.zoomOutButton.setIcon(
            build_icon(u':/general/general_zoom_out.png'))
        self.zoomOutButton.setObjectName(u'zoomOutButton')
        self.zoomButtonLayout.addWidget(self.zoomOutButton)
        self.zoomInButton = QtGui.QToolButton(printServiceOrderDialog)
        self.zoomInButton.setIcon(build_icon(u':/general/general_zoom_in.png'))
        self.zoomInButton.setObjectName(u'zoomInButton')
        self.zoomButtonLayout.addWidget(self.zoomInButton)
        self.dialogLayout.addLayout(self.zoomButtonLayout, 1, 0, 1, 1)
        self.retranslateUi(printServiceOrderDialog)
        QtCore.QMetaObject.connectSlotsByName(printServiceOrderDialog)

    def retranslateUi(self, printServiceOrderDialog):
        printServiceOrderDialog.setWindowTitle(UiStrings.PrintServiceOrder)
        self.previewLabel.setText(
            translate('OpenLP.ServiceManager', '<b>Preview:</b>'))
        self.printSlideTextCheckBox.setText(translate(
            'OpenLP.PrintServiceOrderForm', 'Include slide text if available'))
        self.printNotesCheckBox.setText(translate(
            'OpenLP.PrintServiceOrderForm', 'Include service item notes'))
        self.printMetaDataCheckBox.setText(
            translate('OpenLP.PrintServiceOrderForm',
            'Include play length of media items'))
        self.serviceTitleLabel.setText(translate(
            'OpenLP.PrintServiceOrderForm', 'Title:'))
        self.serviceTitleLineEdit.setText(translate('OpenLP.ServiceManager',
            'Service Order Sheet'))
        self.printButton.setText(translate('OpenLP.ServiceManager', 'Print'))
        self.cancelButton.setText(UiStrings.Cancel)
        self.customNotesLabel.setText(
            translate('OpenLP.ServiceManager', '<b>Custom Service Notes:</b>'))
