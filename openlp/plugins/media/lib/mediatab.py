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

from openlp.core.lib import SettingsTab, translate, Receiver

class MediaTab(SettingsTab):
    """
    MediaTab is the Media settings tab in the settings dialog.
    """
    def __init__(self, parent, title, visible_title, icon_path):
        SettingsTab.__init__(self, parent, title, visible_title, icon_path)

    def setupUi(self):
        self.setObjectName(u'MediaTab')
        SettingsTab.setupUi(self)
        self.mediaAPIsGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.mediaAPIsGroupBox.setObjectName(u'mediaAPIsGroupBox')
        self.mediaApiLayout = QtGui.QVBoxLayout(self.mediaAPIsGroupBox)
        self.mediaApiLayout.setObjectName(u'mediaApiLayout')
        self.usePhononCheckBox = QtGui.QCheckBox(self.mediaAPIsGroupBox)
        self.usePhononCheckBox.setObjectName(u'usePhononCheckBox')
        self.mediaApiLayout.addWidget(self.usePhononCheckBox)
        self.useVlcCheckBox = QtGui.QCheckBox(self.mediaAPIsGroupBox)
        self.useVlcCheckBox.setObjectName(u'useVlcCheckBox')
        self.mediaApiLayout.addWidget(self.useVlcCheckBox)
        self.leftLayout.addWidget(self.mediaAPIsGroupBox)

        self.apiOrderGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.apiOrderGroupBox.setObjectName(u'apiOrderGroupBox')
        self.apiOrderLayout = QtGui.QVBoxLayout(self.apiOrderGroupBox)
        self.apiOrderLayout.setObjectName(u'apiOrderLayout')
        self.apiOrderlistWidget = QtGui.QListWidget( \
            self.apiOrderGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apiOrderlistWidget. \
            sizePolicy().hasHeightForWidth())
        self.apiOrderlistWidget.setSizePolicy(sizePolicy)

        self.apiOrderlistWidget.setVerticalScrollBarPolicy( \
            QtCore.Qt.ScrollBarAsNeeded)
        self.apiOrderlistWidget.setHorizontalScrollBarPolicy( \
            QtCore.Qt.ScrollBarAlwaysOff)
        self.apiOrderlistWidget.setEditTriggers( \
            QtGui.QAbstractItemView.NoEditTriggers)
        self.apiOrderlistWidget.setObjectName(u'apiOrderlistWidget')
        self.apiOrderLayout.addWidget(self.apiOrderlistWidget)
        self.orderingButtonsWidget = QtGui.QWidget(self.apiOrderGroupBox)
        self.orderingButtonsWidget.setObjectName(u'orderingButtonsWidget')
        self.orderingButtonLayout = QtGui.QHBoxLayout(self.orderingButtonsWidget)
        self.orderingButtonLayout.setObjectName(u'orderingButtonLayout')
        self.orderingDownButton = QtGui.QPushButton(self.orderingButtonsWidget)
        self.orderingDownButton.setObjectName(u'orderingDownButton')
        self.orderingButtonLayout.addWidget(self.orderingDownButton)
        self.orderingUpButton = QtGui.QPushButton(self.apiOrderGroupBox)
        self.orderingUpButton.setObjectName(u'orderingUpButton')
        self.orderingButtonLayout.addWidget(self.orderingUpButton)
        self.apiOrderLayout.addWidget(self.orderingButtonsWidget)
        self.leftLayout.addWidget(self.apiOrderGroupBox)
        self.leftLayout.addStretch()
        self.rightLayout.addStretch()
        QtCore.QObject.connect(self.usePhononCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onUsePhononCheckBoxChanged)
        QtCore.QObject.connect(self.useVlcCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onUseVlcCheckBoxChanged)
        QtCore.QObject.connect(self.orderingUpButton,
            QtCore.SIGNAL(u'pressed()'), self.onOrderingUpButtonPressed)
        QtCore.QObject.connect(self.orderingDownButton,
            QtCore.SIGNAL(u'pressed()'), self.onOrderingDownButtonPressed)

    def retranslateUi(self):
        self.mediaAPIsGroupBox.setTitle(
            translate('MediaPlugin.MediaTab', 'Media APIs'))
        self.usePhononCheckBox.setText(
            translate('MediaPlugin.MediaTab', 'use Phonon'))
        self.useVlcCheckBox.setText(
            translate('MediaPlugin.MediaTab', 'use Vlc'))
        self.apiOrderGroupBox.setTitle(
            translate('MediaPlugin.MediaTab', 'API Order'))
        self.orderingDownButton.setText(
            translate('MediaPlugin.MediaTab', 'Down'))
        self.orderingUpButton.setText(
            translate('MediaPlugin.MediaTab', 'Up'))

    def onUsePhononCheckBoxChanged(self, check_state):
        if check_state == QtCore.Qt.Checked:
            self.usePhonon = True
            if u'Phonon' not in self.usedAPIs:
                self.usedAPIs.append(u'Phonon')
        else:
            self.usePhonon = False
            self.usedAPIs.takeAt(self.usedAPIs.indexOf(u'Phonon'))
        self.updateApiList()

    def onUseVlcCheckBoxChanged(self, check_state):
        if check_state == QtCore.Qt.Checked:
            self.useVlc = True
            if u'Vlc' not in self.usedAPIs:
                self.usedAPIs.append(u'Vlc')
        else:
            self.useVlc = False
            self.usedAPIs.takeAt(self.usedAPIs.indexOf(u'Vlc'))
        self.updateApiList()

    def updateApiList(self):
        self.apiOrderlistWidget.clear()
        for api in self.usedAPIs:
            self.apiOrderlistWidget.addItem(api)

    def onOrderingUpButtonPressed(self):
        currentRow = self.apiOrderlistWidget.currentRow()
        if currentRow > 0:
            item = self.apiOrderlistWidget.takeItem(currentRow)
            self.apiOrderlistWidget.insertItem(currentRow-1, item)
            self.apiOrderlistWidget.setCurrentRow(currentRow-1)
            self.usedAPIs.move(currentRow, currentRow-1)

    def onOrderingDownButtonPressed(self):
        currentRow = self.apiOrderlistWidget.currentRow()
        if currentRow < self.apiOrderlistWidget.count()-1:
            item = self.apiOrderlistWidget.takeItem(currentRow)
            self.apiOrderlistWidget.insertItem(currentRow+1, item)
            self.apiOrderlistWidget.setCurrentRow(currentRow+1)
            self.usedAPIs.move(currentRow, currentRow+1)

    def load(self):
        self.usedAPIs = QtCore.QSettings().value(
            self.settingsSection + u'/apis',
            QtCore.QVariant(u'Webkit')).toString().split(u',')
        self.useWebkit = u'Webkit' in self.usedAPIs
        self.usePhonon = u'Phonon' in self.usedAPIs
        self.useVlc = u'Vlc' in self.usedAPIs
        self.usePhononCheckBox.setChecked(self.usePhonon)
        self.useVlcCheckBox.setChecked(self.useVlc)
        self.updateApiList()

    def save(self):
        oldApiString = QtCore.QSettings().value(
            self.settingsSection + u'/apis',
            QtCore.QVariant(u'Webkit')).toString()
        newApiString = self.usedAPIs.join(u',')
        if oldApiString != newApiString:
            QtCore.QSettings().setValue(self.settingsSection + u'/apis',
                QtCore.QVariant(newApiString))
            Receiver.send_message(u'config_screen_changed')
