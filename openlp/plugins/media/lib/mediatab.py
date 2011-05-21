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
        self.mediaLayoutWidget = QtGui.QWidget(self.leftColumn)
        self.mediaBackendLayout = QtGui.QVBoxLayout(self.mediaLayoutWidget)
        self.mediaBackendLayout.setObjectName(u'mediaBackendLayout')
        self.mediaBackendsGroupBox = QtGui.QGroupBox(self.mediaLayoutWidget)
        self.mediaBackendsGroupBox.setObjectName(u'mediaBackendsGroupBox')
        self.mediaBackendsGroupLayout = QtGui.QVBoxLayout( \
            self.mediaBackendsGroupBox)
        self.mediaBackendsGroupLayout.setObjectName( \
            u'mediaBackendsGroupLayout')
        self.usePhononCheckBox = QtGui.QCheckBox(self.mediaBackendsGroupBox)
        self.usePhononCheckBox.setObjectName(u'usePhononCheckBox')
        self.mediaBackendsGroupLayout.addWidget(self.usePhononCheckBox)
        self.useVlcCheckBox = QtGui.QCheckBox(self.mediaBackendsGroupBox)
        self.useVlcCheckBox.setObjectName(u'useVlcCheckBox')
        self.mediaBackendsGroupLayout.addWidget(self.useVlcCheckBox)
        self.mediaBackendLayout.addWidget(self.mediaBackendsGroupBox)
        self.backendOrderLabel = QtGui.QLabel(self.mediaLayoutWidget)
        self.backendOrderLabel.setObjectName(u'backendOrderLabel')
        self.mediaBackendLayout.addWidget(self.backendOrderLabel)
        self.backendOrderlistWidget = QtGui.QListWidget(self.mediaLayoutWidget)
        self.backendOrderlistWidget.setVerticalScrollBarPolicy( \
            QtCore.Qt.ScrollBarAsNeeded)
        self.backendOrderlistWidget.setHorizontalScrollBarPolicy( \
            QtCore.Qt.ScrollBarAlwaysOff)
        self.backendOrderlistWidget.setEditTriggers( \
            QtGui.QAbstractItemView.NoEditTriggers)
        self.backendOrderlistWidget.setObjectName(u'backendOrderlistWidget')
        self.mediaBackendLayout.addWidget(self.backendOrderlistWidget)
        self.orderingButtonLayout = QtGui.QHBoxLayout()
        self.orderingButtonLayout.setObjectName(u'orderingButtonLayout')
        self.orderingDownButton = QtGui.QPushButton(self.mediaLayoutWidget)
        self.orderingDownButton.setObjectName(u'orderingDownButton')
        self.orderingButtonLayout.addWidget(self.orderingDownButton)
        self.orderingUpButton = QtGui.QPushButton(self.mediaLayoutWidget)
        self.orderingUpButton.setObjectName(u'orderingUpButton')
        self.orderingButtonLayout.addWidget(self.orderingUpButton)
        self.mediaBackendLayout.addLayout(self.orderingButtonLayout)

        self.leftLayout.addWidget(self.mediaLayoutWidget)
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
        self.usePhononCheckBox.setText(
            translate('MediaPlugin.MediaTab', 'use Phonon'))
        self.useVlcCheckBox.setText(
            translate('MediaPlugin.MediaTab', 'use Vlc'))
        self.backendOrderLabel.setText(
            translate('MediaPlugin.MediaTab', 'Backend Order'))
        self.orderingDownButton.setText(
            translate('MediaPlugin.MediaTab', 'Down'))
        self.orderingUpButton.setText(
            translate('MediaPlugin.MediaTab', 'Up'))

    def onUsePhononCheckBoxChanged(self, check_state):
        if check_state == QtCore.Qt.Checked:
            self.usePhonon = self.backendOrderlistWidget.count()
        else:
            self.usePhonon = -1
        self.updateBackendList()

    def onUseVlcCheckBoxChanged(self, check_state):
        if check_state == QtCore.Qt.Checked:
            self.useVlc = self.backendOrderlistWidget.count()
        else:
            self.useVlc = -1
        self.updateBackendList()

    def onOrderingUpButtonPressed(self):
        currentRow = self.backendOrderlistWidget.currentRow()
        if currentRow > 0:
            item = self.backendOrderlistWidget.takeItem(currentRow)
            self.backendOrderlistWidget.insertItem(currentRow-1, item)
            self.backendOrderlistWidget.setCurrentRow(currentRow-1)
            self.updateOrdering()

    def onOrderingDownButtonPressed(self):
        currentRow = self.backendOrderlistWidget.currentRow()
        if currentRow < self.backendOrderlistWidget.count()-1:
            item = self.backendOrderlistWidget.takeItem(currentRow)
            self.backendOrderlistWidget.insertItem(currentRow+1, item)
            self.backendOrderlistWidget.setCurrentRow(currentRow+1)
            self.updateOrdering()

    def updateOrdering(self):
        for num in range (0, self.backendOrderlistWidget.count()):
            item = self.backendOrderlistWidget.item(num)
            if item.text == u'Webkit':
                self.useWebkit = num
            elif item.text == u'Phonon':
                self.usePhonon = num
            elif item.text == u'Vlc':
                self.useVlc = num

    def updateBackendList(self):
        self.backendOrderlistWidget.clear()
        for num in range(0, 3):
            if self.useWebkit == num:
                self.backendOrderlistWidget.addItem(u'Webkit')
            elif self.usePhonon == num:
                self.backendOrderlistWidget.addItem(u'Phonon')
            elif self.useVlc == num:
                self.backendOrderlistWidget.addItem(u'Vlc')

    def load(self):
        self.useWebkit = QtCore.QSettings().value(
            self.settingsSection + u'/use webkit',
            QtCore.QVariant(True)).toInt()[0]
        self.usePhonon = QtCore.QSettings().value(
            self.settingsSection + u'/use phonon',
            QtCore.QVariant(True)).toInt()[0]
        self.useVlc = QtCore.QSettings().value(
            self.settingsSection + u'/use vlc',
            QtCore.QVariant(True)).toInt()[0]
        self.usePhononCheckBox.setChecked((self.usePhonon != -1))
        self.useVlcCheckBox.setChecked((self.useVlc != -1))

    def save(self):
        changedValues = False
        oldUseWebkit = QtCore.QSettings().value(
            u'media/use webkit', QtCore.QVariant(True)).toInt()[0]
        if oldUseWebkit != self.useWebkit:
            QtCore.QSettings().setValue(self.settingsSection + u'/use webkit',
                QtCore.QVariant(self.useWebkit))
            changedValues = True
        oldUsePhonon = QtCore.QSettings().value(
            u'media/use phonon', QtCore.QVariant(True)).toInt()[0]
        if oldUsePhonon != self.usePhonon:
            QtCore.QSettings().setValue(self.settingsSection + u'/use phonon',
                QtCore.QVariant(self.usePhonon))
            changedValues = True
        oldUseVlc = QtCore.QSettings().value(
            u'media/use vlc', QtCore.QVariant(True)).toInt()[0]
        if oldUseVlc != self.useVlc:
            QtCore.QSettings().setValue(self.settingsSection + u'/use vlc',
                QtCore.QVariant(self.useVlc))
            changedValues = True
        if changedValues:
            Receiver.send_message(u'config_screen_changed')
