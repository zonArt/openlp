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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import build_icon, translate, SpellTextEdit
from openlp.core.lib.ui import UiStrings

class ZoomSize(object):
    """
    Type enumeration for Combo Box sizes
    """
    Page = 0
    Width = 1
    OneHundred = 2
    SeventyFive = 3
    Fifty = 4
    TwentyFive = 5

    Sizes = [
        translate('OpenLP.PrintServiceDialog', 'Fit Page'),
        translate('OpenLP.PrintServiceDialog', 'Fit Width'),
        u'100%', u'75%', u'50%', u'25%']


class Ui_PrintServiceDialog(object):
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
        self.printButton = self.toolbar.addAction(
            build_icon(u':/general/general_print.png'), 'Print')
        self.optionsButton = QtGui.QToolButton(self.toolbar)
        self.optionsButton.setText(translate('OpenLP.PrintServiceForm',
            'Options'))
        self.optionsButton.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon)
        self.optionsButton.setIcon(build_icon(u':/system/system_configure.png'))
        self.optionsButton.setCheckable(True)
        self.toolbar.addWidget(self.optionsButton)
        self.closeButton = self.toolbar.addAction(
            build_icon(u':/system/system_close.png'),
            translate('OpenLP.PrintServiceForm', 'Close'))
        self.toolbar.addSeparator()
        self.plainCopy = self.toolbar.addAction(
            build_icon(u':/system/system_edit_copy.png'),
            translate('OpenLP.PrintServiceForm', 'Copy'))
        self.htmlCopy = self.toolbar.addAction(
            build_icon(u':/system/system_edit_copy.png'),
            translate('OpenLP.PrintServiceForm', 'Copy as HTML'))
        self.toolbar.addSeparator()
        self.zoomInButton = QtGui.QToolButton(self.toolbar)
        self.zoomInButton.setIcon(build_icon(u':/general/general_zoom_in.png'))
        self.zoomInButton.setToolTip(translate('OpenLP.PrintServiceForm',
            'Zoom In'))
        self.zoomInButton.setObjectName(u'zoomInButton')
        self.zoomInButton.setIconSize(QtCore.QSize(22, 22))
        self.toolbar.addWidget(self.zoomInButton)
        self.zoomOutButton = QtGui.QToolButton(self.toolbar)
        self.zoomOutButton.setIcon(
            build_icon(u':/general/general_zoom_out.png'))
        self.zoomOutButton.setToolTip(translate('OpenLP.PrintServiceForm',
            'Zoom Out'))
        self.zoomOutButton.setObjectName(u'zoomOutButton')
        self.zoomOutButton.setIconSize(QtCore.QSize(22, 22))
        self.toolbar.addWidget(self.zoomOutButton)
        self.zoomOriginalButton = QtGui.QToolButton(self.toolbar)
        self.zoomOriginalButton.setIcon(
            build_icon(u':/general/general_zoom_original.png'))
        self.zoomOriginalButton.setToolTip(translate('OpenLP.PrintServiceForm',
            'Zoom Original'))
        self.zoomOriginalButton.setObjectName(u'zoomOriginalButton')
        self.zoomOriginalButton.setIconSize(QtCore.QSize(22, 22))
        self.toolbar.addWidget(self.zoomOriginalButton)
        self.zoomComboBox = QtGui.QComboBox(printServiceDialog)
        self.zoomComboBox.setObjectName(u'zoomComboBox')
        self.toolbar.addWidget(self.zoomComboBox)
        self.mainLayout.addWidget(self.toolbar)
        self.previewWidget = QtGui.QPrintPreviewWidget(printServiceDialog)
        self.mainLayout.addWidget(self.previewWidget)
        self.optionsWidget = QtGui.QWidget(printServiceDialog)
        self.optionsWidget.hide()
        self.optionsWidget.resize(400, 300)
        self.optionsWidget.setAutoFillBackground(True)
        self.optionsLayout = QtGui.QVBoxLayout(self.optionsWidget)
        self.optionsLayout.setContentsMargins(8, 8, 8, 8)
        self.titleLabel = QtGui.QLabel(self.optionsWidget)
        self.titleLabel.setObjectName(u'titleLabel')
        self.titleLabel.setText(u'Title:')
        self.optionsLayout.addWidget(self.titleLabel)
        self.titleLineEdit = QtGui.QLineEdit(self.optionsWidget)
        self.titleLineEdit.setObjectName(u'titleLineEdit')
        self.optionsLayout.addWidget(self.titleLineEdit)
        self.footerLabel = QtGui.QLabel(self.optionsWidget)
        self.footerLabel.setObjectName(u'footerLabel')
        self.footerLabel.setText(u'Custom Footer Text:')
        self.optionsLayout.addWidget(self.footerLabel)
        self.footerTextEdit = SpellTextEdit(self.optionsWidget)
        self.footerTextEdit.setObjectName(u'footerTextEdit')
        self.optionsLayout.addWidget(self.footerTextEdit)
        self.optionsGroupBox = QtGui.QGroupBox(
            translate('OpenLP.PrintServiceForm','Other Options'))
        self.groupLayout = QtGui.QVBoxLayout()
        self.slideTextCheckBox = QtGui.QCheckBox()
        self.groupLayout.addWidget(self.slideTextCheckBox)
        self.pageBreakAfterText = QtGui.QCheckBox()
        self.groupLayout.addWidget(self.pageBreakAfterText)
        self.notesCheckBox = QtGui.QCheckBox()
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

    def retranslateUi(self, printServiceDialog):
        printServiceDialog.setWindowTitle(UiStrings().PrintServiceOrder)
        self.slideTextCheckBox.setText(translate('OpenLP.PrintServiceForm',
            'Include slide text if available'))
        self.pageBreakAfterText.setText(translate('OpenLP.PrintServiceForm',
            'Add page break before each text item'))
        self.notesCheckBox.setText(translate('OpenLP.PrintServiceForm',
            'Include service item notes'))
        self.metaDataCheckBox.setText(translate('OpenLP.PrintServiceForm',
            'Include play length of media items'))
        self.titleLineEdit.setText(translate('OpenLP.PrintServiceForm',
            'Service Order Sheet'))
        self.zoomComboBox.addItem(ZoomSize.Sizes[ZoomSize.Page])
        self.zoomComboBox.addItem(ZoomSize.Sizes[ZoomSize.Width])
        self.zoomComboBox.addItem(ZoomSize.Sizes[ZoomSize.OneHundred])
        self.zoomComboBox.addItem(ZoomSize.Sizes[ZoomSize.SeventyFive])
        self.zoomComboBox.addItem(ZoomSize.Sizes[ZoomSize.Fifty])
        self.zoomComboBox.addItem(ZoomSize.Sizes[ZoomSize.TwentyFive])

