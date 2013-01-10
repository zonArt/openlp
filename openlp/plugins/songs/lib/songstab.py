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

from openlp.core.lib import Settings, SettingsTab, translate


class SongsTab(SettingsTab):
    """
    SongsTab is the Songs settings tab in the settings dialog.
    """
    def setupUi(self):
        """
        Set up the configuration tab UI.
        """
        self.setObjectName(u'SongsTab')
        SettingsTab.setupUi(self)
        self.modeGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.modeGroupBox.setObjectName(u'modeGroupBox')
        self.modeLayout = QtGui.QVBoxLayout(self.modeGroupBox)
        self.modeLayout.setObjectName(u'modeLayout')
        self.searchAsTypeCheckBox = QtGui.QCheckBox(self.modeGroupBox)
        self.searchAsTypeCheckBox.setObjectName(u'SearchAsTypeCheckBox')
        self.modeLayout.addWidget(self.searchAsTypeCheckBox)
        self.toolBarActiveCheckBox = QtGui.QCheckBox(self.modeGroupBox)
        self.toolBarActiveCheckBox.setObjectName(u'toolBarActiveCheckBox')
        self.modeLayout.addWidget(self.toolBarActiveCheckBox)
        self.updateOnEditCheckBox = QtGui.QCheckBox(self.modeGroupBox)
        self.updateOnEditCheckBox.setObjectName(u'updateOnEditCheckBox')
        self.modeLayout.addWidget(self.updateOnEditCheckBox)
        self.addFromServiceCheckBox = QtGui.QCheckBox(self.modeGroupBox)
        self.addFromServiceCheckBox.setObjectName(u'addFromServiceCheckBox')
        self.modeLayout.addWidget(self.addFromServiceCheckBox)
        self.leftLayout.addWidget(self.modeGroupBox)
        self.leftLayout.addStretch()
        self.rightLayout.addStretch()
        QtCore.QObject.connect(self.searchAsTypeCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onSearchAsTypeCheckBoxChanged)
        QtCore.QObject.connect(self.toolBarActiveCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onToolBarActiveCheckBoxChanged)
        QtCore.QObject.connect(self.updateOnEditCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onUpdateOnEditCheckBoxChanged)
        QtCore.QObject.connect(self.addFromServiceCheckBox, QtCore.SIGNAL(u'stateChanged(int)'),
            self.onAddFromServiceCheckBoxChanged)

    def retranslateUi(self):
        self.modeGroupBox.setTitle(translate('SongsPlugin.SongsTab', 'Songs Mode'))
        self.searchAsTypeCheckBox.setText(translate('SongsPlugin.SongsTab', 'Enable search as you type'))
        self.toolBarActiveCheckBox.setText(translate('SongsPlugin.SongsTab',
            'Display verses on live tool bar'))
        self.updateOnEditCheckBox.setText(translate('SongsPlugin.SongsTab', 'Update service from song edit'))
        self.addFromServiceCheckBox.setText(translate('SongsPlugin.SongsTab',
            'Import missing songs from service files'))

    def onSearchAsTypeCheckBoxChanged(self, check_state):
        self.song_search = (check_state == QtCore.Qt.Checked)

    def onToolBarActiveCheckBoxChanged(self, check_state):
        self.tool_bar = (check_state == QtCore.Qt.Checked)

    def onUpdateOnEditCheckBoxChanged(self, check_state):
        self.update_edit = (check_state == QtCore.Qt.Checked)

    def onAddFromServiceCheckBoxChanged(self, check_state):
        self.update_load = (check_state == QtCore.Qt.Checked)

    def load(self):
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        self.song_search = settings.value(u'search as type')
        self.tool_bar = settings.value(u'display songbar')
        self.update_edit = settings.value(u'update service on edit')
        self.update_load = settings.value(u'add song from service')
        self.searchAsTypeCheckBox.setChecked(self.song_search)
        self.toolBarActiveCheckBox.setChecked(self.tool_bar)
        self.updateOnEditCheckBox.setChecked(self.update_edit)
        self.addFromServiceCheckBox.setChecked(self.update_load)
        settings.endGroup()

    def save(self):
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'search as type', self.song_search)
        settings.setValue(u'display songbar', self.tool_bar)
        settings.setValue(u'update service on edit', self.update_edit)
        settings.setValue(u'add song from service', self.update_load)
        settings.endGroup()
