# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
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
    def __init__(self, parent, title, visible_title, icon_path):
        self.parent = parent
        SettingsTab.__init__(self, parent, title, visible_title, icon_path)

    def setupUi(self):
        self.setObjectName(u'MediaTab')
        SettingsTab.setupUi(self)
        self.advancedGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.advancedGroupBox.setObjectName(u'advancedGroupBox')
        self.advancedLayout = QtGui.QVBoxLayout(self.advancedGroupBox)
        self.advancedLayout.setObjectName(u'advancedLayout')
        self.overridePlayerCheckBox = QtGui.QCheckBox(self.advancedGroupBox)
        self.overridePlayerCheckBox.setObjectName(u'overridePlayerCheckBox')
        self.advancedLayout.addWidget(self.overridePlayerCheckBox)
        self.autoStartCheckBox = QtGui.QCheckBox(self.advancedGroupBox)
        self.autoStartCheckBox.setObjectName(u'autoStartCheckBox')
        self.advancedLayout.addWidget(self.autoStartCheckBox)
        self.leftLayout.addWidget(self.advancedGroupBox)
        self.leftLayout.addStretch()
        self.rightLayout.addStretch()

    def retranslateUi(self):
        self.advancedGroupBox.setTitle(UiStrings().Advanced)
        self.overridePlayerCheckBox.setText(translate('MediaPlugin.MediaTab', 'Allow media player to be overridden'))
        self.autoStartCheckBox.setText(translate('MediaPlugin.MediaTab', 'Start Live items automatically'))

    def load(self):
        self.overridePlayerCheckBox.setChecked(Settings().value(self.settingsSection + u'/override player',
            QtCore.QVariant(QtCore.Qt.Unchecked)).toInt()[0])
        self.autoStartCheckBox.setChecked(Settings().value(self.settingsSection + u'/media auto start',
            QtCore.QVariant(QtCore.Qt.Unchecked)).toInt()[0])

    def save(self):
        override_changed = False
        setting_key = self.settingsSection + u'/override player'
        if Settings().value(setting_key).toInt()[0] != self.overridePlayerCheckBox.checkState():
            Settings().setValue(setting_key, QtCore.QVariant(self.overridePlayerCheckBox.checkState()))
            override_changed = True
        setting_key = self.settingsSection + u'/media auto start'
        if Settings().value(setting_key).toInt()[0] != self.autoStartCheckBox.checkState():
            Settings().setValue(setting_key, QtCore.QVariant(self.autoStartCheckBox.checkState()))
        if override_changed:
            self.parent.resetSupportedSuffixes()
            Receiver.send_message(u'mediaitem_media_rebuild')
            Receiver.send_message(u'mediaitem_suffixes')