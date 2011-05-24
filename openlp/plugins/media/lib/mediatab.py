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
        self.mediaBackendsGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.mediaBackendsGroupBox.setObjectName(u'mediaBackendsGroupBox')
        self.mediaBackendLayout = QtGui.QVBoxLayout(self.mediaBackendsGroupBox)
        self.mediaBackendLayout.setObjectName(u'mediaBackendLayout')
        self.usePhononCheckBox = QtGui.QCheckBox(self.mediaBackendsGroupBox)
        self.usePhononCheckBox.setObjectName(u'usePhononCheckBox')
        self.mediaBackendLayout.addWidget(self.usePhononCheckBox)
        self.useVlcCheckBox = QtGui.QCheckBox(self.mediaBackendsGroupBox)
        self.useVlcCheckBox.setObjectName(u'useVlcCheckBox')
        self.mediaBackendLayout.addWidget(self.useVlcCheckBox)
        self.leftLayout.addWidget(self.mediaBackendsGroupBox)

        self.backendOrderGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.backendOrderGroupBox.setObjectName(u'backendOrderGroupBox')
        self.backendOrderLayout = QtGui.QVBoxLayout(self.backendOrderGroupBox)
        self.backendOrderLayout.setObjectName(u'backendOrderLayout')
        self.backendOrderlistWidget = QtGui.QListWidget( \
            self.backendOrderGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backendOrderlistWidget. \
            sizePolicy().hasHeightForWidth())
        self.backendOrderlistWidget.setSizePolicy(sizePolicy)

        self.backendOrderlistWidget.setVerticalScrollBarPolicy( \
            QtCore.Qt.ScrollBarAsNeeded)
        self.backendOrderlistWidget.setHorizontalScrollBarPolicy( \
            QtCore.Qt.ScrollBarAlwaysOff)
        self.backendOrderlistWidget.setEditTriggers( \
            QtGui.QAbstractItemView.NoEditTriggers)
        self.backendOrderlistWidget.setObjectName(u'backendOrderlistWidget')
        self.backendOrderLayout.addWidget(self.backendOrderlistWidget)
        self.orderingButtonsWidget = QtGui.QWidget(self.backendOrderGroupBox)
        self.orderingButtonsWidget.setObjectName(u'orderingButtonsWidget')
        self.orderingButtonLayout = QtGui.QHBoxLayout(self.orderingButtonsWidget)
        self.orderingButtonLayout.setObjectName(u'orderingButtonLayout')
        self.orderingDownButton = QtGui.QPushButton(self.orderingButtonsWidget)
        self.orderingDownButton.setObjectName(u'orderingDownButton')
        self.orderingButtonLayout.addWidget(self.orderingDownButton)
        self.orderingUpButton = QtGui.QPushButton(self.backendOrderGroupBox)
        self.orderingUpButton.setObjectName(u'orderingUpButton')
        self.orderingButtonLayout.addWidget(self.orderingUpButton)
        self.backendOrderLayout.addWidget(self.orderingButtonsWidget)
        self.leftLayout.addWidget(self.backendOrderGroupBox)
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
        self.mediaBackendsGroupBox.setTitle(
            translate('MediaPlugin.MediaTab', 'Media Backends'))
        self.usePhononCheckBox.setText(
            translate('MediaPlugin.MediaTab', 'use Phonon'))
        self.useVlcCheckBox.setText(
            translate('MediaPlugin.MediaTab', 'use Vlc'))
        self.backendOrderGroupBox.setTitle(
            translate('MediaPlugin.MediaTab', 'Backends Order'))
        self.orderingDownButton.setText(
            translate('MediaPlugin.MediaTab', 'Down'))
        self.orderingUpButton.setText(
            translate('MediaPlugin.MediaTab', 'Up'))

    def onUsePhononCheckBoxChanged(self, check_state):
        if check_state == QtCore.Qt.Checked:
            self.usePhonon = True
            if u'Phonon' not in self.usedBackends:
                self.usedBackends.append(u'Phonon')
        else:
            self.usePhonon = False
            self.usedBackends.takeAt(self.usedBackends.indexOf(u'Phonon'))
        self.updateBackendList()

    def onUseVlcCheckBoxChanged(self, check_state):
        if check_state == QtCore.Qt.Checked:
            self.useVlc = True
            if u'Vlc' not in self.usedBackends:
                self.usedBackends.append(u'Vlc')
        else:
            self.useVlc = False
            self.usedBackends.takeAt(self.usedBackends.indexOf(u'Vlc'))
        self.updateBackendList()

    def updateBackendList(self):
        self.backendOrderlistWidget.clear()
        for backend in self.usedBackends:
            self.backendOrderlistWidget.addItem(backend)

    def onOrderingUpButtonPressed(self):
        currentRow = self.backendOrderlistWidget.currentRow()
        if currentRow > 0:
            item = self.backendOrderlistWidget.takeItem(currentRow)
            self.backendOrderlistWidget.insertItem(currentRow-1, item)
            self.backendOrderlistWidget.setCurrentRow(currentRow-1)
            self.usedBackends.move(currentRow, currentRow-1)

    def onOrderingDownButtonPressed(self):
        currentRow = self.backendOrderlistWidget.currentRow()
        if currentRow < self.backendOrderlistWidget.count()-1:
            item = self.backendOrderlistWidget.takeItem(currentRow)
            self.backendOrderlistWidget.insertItem(currentRow+1, item)
            self.backendOrderlistWidget.setCurrentRow(currentRow+1)
            self.usedBackends.move(currentRow, currentRow+1)

    def load(self):
        self.usedBackends = QtCore.QSettings().value(
            self.settingsSection + u'/backends',
            QtCore.QVariant(u'Webkit')).toString().split(u',')
        self.useWebkit = u'Webkit' in self.usedBackends
        self.usePhonon = u'Phonon' in self.usedBackends
        self.useVlc = u'Vlc' in self.usedBackends
        self.usePhononCheckBox.setChecked(self.usePhonon)
        self.useVlcCheckBox.setChecked(self.useVlc)
        self.updateBackendList()

    def save(self):
        oldBackendString = QtCore.QSettings().value(
            self.settingsSection + u'/backends',
            QtCore.QVariant(u'Webkit')).toString()
        newBackendString = self.usedBackends.join(u',')
        if oldBackendString != newBackendString:
            QtCore.QSettings().setValue(self.settingsSection + u'/backends',
                QtCore.QVariant(newBackendString))
            Receiver.send_message(u'config_screen_changed')
