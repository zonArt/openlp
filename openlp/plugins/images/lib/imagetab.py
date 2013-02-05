# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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

from openlp.core.lib import SettingsTab, Receiver, Settings, UiStrings, translate

class ImageTab(SettingsTab):
    """
    ImageTab is the images settings tab in the settings dialog.
    """
    def __init__(self, parent, name, visible_title, icon_path):
        SettingsTab.__init__(self, parent, name, visible_title, icon_path)

    def setupUi(self):
        self.setObjectName(u'ImagesTab')
        SettingsTab.setupUi(self)
        self.bgColorGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.bgColorGroupBox.setObjectName(u'FontGroupBox')
        self.formLayout = QtGui.QFormLayout(self.bgColorGroupBox)
        self.formLayout.setObjectName(u'FormLayout')
        self.colorLayout = QtGui.QHBoxLayout()
        self.backgroundColorLabel = QtGui.QLabel(self.bgColorGroupBox)
        self.backgroundColorLabel.setObjectName(u'BackgroundColorLabel')
        self.colorLayout.addWidget(self.backgroundColorLabel)
        self.backgroundColorButton = QtGui.QPushButton(self.bgColorGroupBox)
        self.backgroundColorButton.setObjectName(u'BackgroundColorButton')
        self.colorLayout.addWidget(self.backgroundColorButton)
        self.formLayout.addRow(self.colorLayout)
        self.informationLabel = QtGui.QLabel(self.bgColorGroupBox)
        self.informationLabel.setObjectName(u'InformationLabel')
        self.informationLabel.setWordWrap(True)
        self.formLayout.addRow(self.informationLabel)
        self.leftLayout.addWidget(self.bgColorGroupBox)
        self.leftLayout.addStretch()
        self.rightColumn.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.rightLayout.addStretch()
        # Signals and slots
        QtCore.QObject.connect(self.backgroundColorButton, QtCore.SIGNAL(u'clicked()'),
            self.onbackgroundColorButtonClicked)

    def retranslateUi(self):
        self.bgColorGroupBox.setTitle(UiStrings().BackgroundColor)
        self.backgroundColorLabel.setText(UiStrings().DefaultColor)
        self.informationLabel.setText(
            translate('ImagesPlugin.ImageTab', 'Visible background for images with aspect ratio different to screen.'))

    def onbackgroundColorButtonClicked(self):
        new_color = QtGui.QColorDialog.getColor(QtGui.QColor(self.bg_color), self)
        if new_color.isValid():
            self.bg_color = new_color.name()
            self.backgroundColorButton.setStyleSheet(u'background-color: %s' % self.bg_color)

    def load(self):
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        self.bg_color = settings.value(u'background color')
        self.initial_color = self.bg_color
        settings.endGroup()
        self.backgroundColorButton.setStyleSheet(u'background-color: %s' % self.bg_color)

    def save(self):
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'background color', self.bg_color)
        settings.endGroup()
        if self.initial_color != self.bg_color:
            Receiver.send_message(u'image_updated')

