# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
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
from openlp.core.lib.ui import UiStrings

class MediaQCheckBox(QtGui.QCheckBox):
    """
    MediaQCheckBox adds an extra property, playerName to the QCheckBox class.
    """
    def setPlayerName(self, name):
        self.playerName = name


class MediaTab(SettingsTab):
    """
    MediaTab is the Media settings tab in the settings dialog.
    """
    def __init__(self, parent, title, visible_title, media_players, icon_path):
        self.mediaPlayers = media_players
        self.savedUsedPlayers = None
        SettingsTab.__init__(self, parent, title, visible_title, icon_path)

    def setupUi(self):
        self.setObjectName(u'MediaTab')
        SettingsTab.setupUi(self)
        self.mediaPlayerGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.mediaPlayerGroupBox.setObjectName(u'mediaPlayerGroupBox')
        self.mediaPlayerLayout = QtGui.QVBoxLayout(self.mediaPlayerGroupBox)
        self.mediaPlayerLayout.setObjectName(u'mediaPlayerLayout')
        self.playerCheckBoxes = {}
        for key, player in self.mediaPlayers.iteritems():
            player = self.mediaPlayers[key]
            checkbox = MediaQCheckBox(self.mediaPlayerGroupBox)
            checkbox.setEnabled(player.available)
            checkbox.setObjectName(player.name + u'CheckBox')
            self.playerCheckBoxes[player.name] = checkbox
            self.mediaPlayerLayout.addWidget(checkbox)
        self.leftLayout.addWidget(self.mediaPlayerGroupBox)
        self.playerOrderGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.playerOrderGroupBox.setObjectName(u'playerOrderGroupBox')
        self.playerOrderLayout = QtGui.QVBoxLayout(self.playerOrderGroupBox)
        self.playerOrderLayout.setObjectName(u'playerOrderLayout')
        self.playerOrderlistWidget = QtGui.QListWidget( \
            self.playerOrderGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playerOrderlistWidget. \
            sizePolicy().hasHeightForWidth())
        self.playerOrderlistWidget.setSizePolicy(sizePolicy)
        self.playerOrderlistWidget.setVerticalScrollBarPolicy( \
            QtCore.Qt.ScrollBarAsNeeded)
        self.playerOrderlistWidget.setHorizontalScrollBarPolicy( \
            QtCore.Qt.ScrollBarAlwaysOff)
        self.playerOrderlistWidget.setEditTriggers( \
            QtGui.QAbstractItemView.NoEditTriggers)
        self.playerOrderlistWidget.setObjectName(u'playerOrderlistWidget')
        self.playerOrderLayout.addWidget(self.playerOrderlistWidget)
        self.orderingButtonsWidget = QtGui.QWidget(self.playerOrderGroupBox)
        self.orderingButtonsWidget.setObjectName(u'orderingButtonsWidget')
        self.orderingButtonLayout = QtGui.QHBoxLayout( \
            self.orderingButtonsWidget)
        self.orderingButtonLayout.setObjectName(u'orderingButtonLayout')
        self.orderingDownButton = QtGui.QPushButton(self.orderingButtonsWidget)
        self.orderingDownButton.setObjectName(u'orderingDownButton')
        self.orderingButtonLayout.addWidget(self.orderingDownButton)
        self.orderingUpButton = QtGui.QPushButton(self.playerOrderGroupBox)
        self.orderingUpButton.setObjectName(u'orderingUpButton')
        self.orderingButtonLayout.addWidget(self.orderingUpButton)
        self.playerOrderLayout.addWidget(self.orderingButtonsWidget)
        self.leftLayout.addWidget(self.playerOrderGroupBox)
        self.advancedGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.advancedGroupBox.setObjectName(u'advancedGroupBox')
        self.advancedLayout = QtGui.QVBoxLayout(self.advancedGroupBox)
        self.advancedLayout.setObjectName(u'advancedLayout')
        self.overridePlayerCheckBox = QtGui.QCheckBox(self.advancedGroupBox)
        self.overridePlayerCheckBox.setObjectName(u'overridePlayerCheckBox')
        self.advancedLayout.addWidget(self.overridePlayerCheckBox)
        self.leftLayout.addWidget(self.advancedGroupBox)
        self.leftLayout.addStretch()
        self.rightLayout.addStretch()
        for key in self.mediaPlayers:
            player = self.mediaPlayers[key]
            checkbox = self.playerCheckBoxes[player.name]
            QtCore.QObject.connect(checkbox,
                QtCore.SIGNAL(u'stateChanged(int)'),
                self.onPlayerCheckBoxChanged)
        QtCore.QObject.connect(self.orderingUpButton,
            QtCore.SIGNAL(u'pressed()'), self.onOrderingUpButtonPressed)
        QtCore.QObject.connect(self.orderingDownButton,
            QtCore.SIGNAL(u'pressed()'), self.onOrderingDownButtonPressed)

    def retranslateUi(self):
        self.mediaPlayerGroupBox.setTitle(
            translate('MediaPlugin.MediaTab', 'Available Media Players'))
        for key in self.mediaPlayers:
            player = self.mediaPlayers[key]
            checkbox = self.playerCheckBoxes[player.name]
            checkbox.setPlayerName(key)
            if player.available:
                checkbox.setText(player.display_name)
            else:
                checkbox.setText(
                    unicode(translate('MediaPlugin.MediaTab',
                    '%s (unavailable)')) % player.display_name)
        self.playerOrderGroupBox.setTitle(
            translate('MediaPlugin.MediaTab', 'Player Order'))
        self.orderingDownButton.setText(
            translate('MediaPlugin.MediaTab', 'Down'))
        self.orderingUpButton.setText(
            translate('MediaPlugin.MediaTab', 'Up'))
        self.advancedGroupBox.setTitle(UiStrings().Advanced)
        self.overridePlayerCheckBox.setText(
            translate('MediaPlugin.MediaTab',
            'Allow media player to be overriden'))

    def onPlayerCheckBoxChanged(self, check_state):
        player = self.sender().playerName
        if check_state == QtCore.Qt.Checked:
            if player not in self.usedPlayers:
                self.usedPlayers.append(player)
        else:
            if player in self.usedPlayers:
                self.usedPlayers.takeAt(self.usedPlayers.indexOf(player))
        self.updatePlayerList()

    def updatePlayerList(self):
        self.playerOrderlistWidget.clear()
        for player in self.usedPlayers:
            if player in self.playerCheckBoxes.keys():
                if len(self.usedPlayers) == 1:
                    # At least one media player has to stay active
                    self.playerCheckBoxes[u'%s' % player].setEnabled(False)
                else:
                    self.playerCheckBoxes[u'%s' % player].setEnabled(True)
                self.playerOrderlistWidget.addItem(
                    self.mediaPlayers[unicode(player)].display_name)

    def onOrderingUpButtonPressed(self):
        currentRow = self.playerOrderlistWidget.currentRow()
        if currentRow > 0:
            item = self.playerOrderlistWidget.takeItem(currentRow)
            self.playerOrderlistWidget.insertItem(currentRow - 1, item)
            self.playerOrderlistWidget.setCurrentRow(currentRow - 1)
            self.usedPlayers.move(currentRow, currentRow - 1)

    def onOrderingDownButtonPressed(self):
        currentRow = self.playerOrderlistWidget.currentRow()
        if currentRow < self.playerOrderlistWidget.count() - 1:
            item = self.playerOrderlistWidget.takeItem(currentRow)
            self.playerOrderlistWidget.insertItem(currentRow + 1, item)
            self.playerOrderlistWidget.setCurrentRow(currentRow + 1)
            self.usedPlayers.move(currentRow, currentRow + 1)

    def load(self):
        self.usedPlayers = QtCore.QSettings().value(
            self.settingsSection + u'/players',
            QtCore.QVariant(u'webkit')).toString().split(u',')
        self.savedUsedPlayers = self.usedPlayers
        for key in self.mediaPlayers:
            player = self.mediaPlayers[key]
            checkbox = self.playerCheckBoxes[player.name]
            if player.available and player.name in self.usedPlayers:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
        self.updatePlayerList()
        self.overridePlayerCheckBox.setChecked(QtCore.QSettings().value(
            self.settingsSection + u'/override player',
            QtCore.QVariant(QtCore.Qt.Unchecked)).toInt()[0])

    def save(self):
        override_changed = False
        player_string_changed = False
        old_players = QtCore.QSettings().value(
            self.settingsSection + u'/players',
            QtCore.QVariant(u'webkit')).toString()
        new_players = self.usedPlayers.join(u',')
        if old_players != new_players:
            # clean old Media stuff
            QtCore.QSettings().setValue(self.settingsSection + u'/players',
                QtCore.QVariant(new_players))
            player_string_changed = True
            override_changed = True
        setting_key = self.settingsSection + u'/override player'
        if QtCore.QSettings().value(setting_key) != \
            self.overridePlayerCheckBox.checkState():
            QtCore.QSettings().setValue(setting_key,
                QtCore.QVariant(self.overridePlayerCheckBox.checkState()))
            override_changed = True
        if override_changed:
            Receiver.send_message(u'mediaitem_media_rebuild')
        if player_string_changed:
            Receiver.send_message(u'mediaitem_media_rebuild')
            Receiver.send_message(u'config_screen_changed')
