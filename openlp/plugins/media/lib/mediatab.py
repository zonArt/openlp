# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Edwin Lunando, Joshua Miller, Stevan Pettit,  #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Simon Scudder, Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon      #
# Tibble, Dave Warnock, Frode Woldsund                                        #
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
from openlp.core.lib.ui import UiStrings, create_button
from openlp.core.lib.settings import Settings
from openlp.core.ui.media import get_media_players, set_media_players
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
        self.playerOrderLayout = QtGui.QHBoxLayout(self.playerOrderGroupBox)
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
        self.orderingButtonLayout = QtGui.QVBoxLayout()
        self.orderingButtonLayout.setObjectName(u'orderingButtonLayout')
        self.orderingButtonLayout.addStretch(1)
        self.orderingUpButton = create_button(self, u'orderingUpButton',
            role=u'up', click=self.onUpButtonClicked)
        self.orderingDownButton = create_button(self, u'orderingDownButton',
            role=u'down', click=self.onDownButtonClicked)
        self.orderingButtonLayout.addWidget(self.orderingUpButton)
        self.orderingButtonLayout.addWidget(self.orderingDownButton)
        self.orderingButtonLayout.addStretch(1)
        self.playerOrderLayout.addLayout(self.orderingButtonLayout)
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

    def retranslateUi(self):
        self.mediaPlayerGroupBox.setTitle(
            translate('MediaPlugin.MediaTab', 'Available Media Players'))
        for key in self.mediaPlayers:
            player = self.mediaPlayers[key]
            checkbox = self.playerCheckBoxes[player.name]
            checkbox.setPlayerName(player.name)
            if player.available:
                checkbox.setText(player.display_name)
            else:
                checkbox.setText(
                    unicode(translate('MediaPlugin.MediaTab',
                    '%s (unavailable)')) % player.display_name)
        self.playerOrderGroupBox.setTitle(
            translate('MediaPlugin.MediaTab', 'Player Order'))
        self.advancedGroupBox.setTitle(UiStrings().Advanced)
        self.overridePlayerCheckBox.setText(
            translate('MediaPlugin.MediaTab',
            'Allow media player to be overridden'))

    def onPlayerCheckBoxChanged(self, check_state):
        player = self.sender().playerName
        if check_state == QtCore.Qt.Checked:
            if player not in self.usedPlayers:
                self.usedPlayers.append(player)
        else:
            if player in self.usedPlayers:
                self.usedPlayers.remove(player)
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
                    self.mediaPlayers[unicode(player)].original_name)

    def onUpButtonClicked(self):
        row = self.playerOrderlistWidget.currentRow()
        if row <= 0:
            return
        item = self.playerOrderlistWidget.takeItem(row)
        self.playerOrderlistWidget.insertItem(row - 1, item)
        self.playerOrderlistWidget.setCurrentRow(row - 1)
        self.usedPlayers.insert(row - 1, self.usedPlayers.pop(row))

    def onDownButtonClicked(self):
        row = self.playerOrderlistWidget.currentRow()
        if row == -1 or row > self.playerOrderlistWidget.count() - 1:
            return
        item = self.playerOrderlistWidget.takeItem(row)
        self.playerOrderlistWidget.insertItem(row + 1, item)
        self.playerOrderlistWidget.setCurrentRow(row + 1)
        self.usedPlayers.insert(row + 1, self.usedPlayers.pop(row))

    def load(self):
        if self.savedUsedPlayers:
            self.usedPlayers = self.savedUsedPlayers
        self.usedPlayers = get_media_players()[0]
        self.savedUsedPlayers = self.usedPlayers
        for key in self.mediaPlayers:
            player = self.mediaPlayers[key]
            checkbox = self.playerCheckBoxes[player.name]
            if player.available and player.name in self.usedPlayers:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
        self.updatePlayerList()
        self.overridePlayerCheckBox.setChecked(Settings().value(
            self.settingsSection + u'/override player',
            QtCore.QVariant(QtCore.Qt.Unchecked)).toInt()[0])

    def save(self):
        override_changed = False
        player_string_changed = False
        old_players, override_player = get_media_players()
        if self.usedPlayers != old_players:
            # clean old Media stuff
            set_media_players(self.usedPlayers, override_player)
            player_string_changed = True
            override_changed = True
        setting_key = self.settingsSection + u'/override player'
        if Settings().value(setting_key).toInt()[0] != \
            self.overridePlayerCheckBox.checkState():
            Settings().setValue(setting_key,
                QtCore.QVariant(self.overridePlayerCheckBox.checkState()))
            override_changed = True
        if override_changed:
            Receiver.send_message(u'mediaitem_media_rebuild')
        if player_string_changed:
            Receiver.send_message(u'mediaitem_media_rebuild')
            Receiver.send_message(u'config_screen_changed')
