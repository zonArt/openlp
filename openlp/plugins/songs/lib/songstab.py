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

from openlp.core.lib import SettingsTab, translate

class SongsTab(SettingsTab):
    """
    SongsTab is the Songs settings tab in the settings dialog.
    """
    def __init__(self, title, visible_title):
        SettingsTab.__init__(self, title, visible_title)

    def setupUi(self):
        self.setObjectName(u'SongsTab')
        self.SongsLayout = QtGui.QHBoxLayout(self)
        self.SongsLayout.setObjectName(u'SongsLayout')
        self.LeftWidget = QtGui.QWidget(self)
        self.LeftWidget.setObjectName(u'LeftWidget')
        self.LeftLayout = QtGui.QVBoxLayout(self.LeftWidget)
        self.LeftLayout.setMargin(0)
        self.LeftLayout.setObjectName(u'LeftLayout')
        self.SongsModeGroupBox = QtGui.QGroupBox(self.LeftWidget)
        self.SongsModeGroupBox.setObjectName(u'SongsModeGroupBox')
        self.SongsModeLayout = QtGui.QVBoxLayout(self.SongsModeGroupBox)
        self.SongsModeLayout.setObjectName(u'SongsModeLayout')
        self.SearchAsTypeCheckBox = QtGui.QCheckBox(self.SongsModeGroupBox)
        self.SearchAsTypeCheckBox.setObjectName(u'SearchAsTypeCheckBox')
        self.SongsModeLayout.addWidget(self.SearchAsTypeCheckBox)
        self.SongBarActiveCheckBox = QtGui.QCheckBox(self.SongsModeGroupBox)
        self.SongBarActiveCheckBox.setObjectName(u'SongBarActiveCheckBox')
        self.SongsModeLayout.addWidget(self.SongBarActiveCheckBox)
        self.SongUpdateOnEditCheckBox = QtGui.QCheckBox(self.SongsModeGroupBox)
        self.SongUpdateOnEditCheckBox.setObjectName(u'SongUpdateOnEditCheckBox')
        self.SongsModeLayout.addWidget(self.SongUpdateOnEditCheckBox)
        self.SongAddFromServiceCheckBox = QtGui.QCheckBox(
            self.SongsModeGroupBox)
        self.SongAddFromServiceCheckBox.setObjectName(
            u'SongAddFromServiceCheckBox')
        self.SongsModeLayout.addWidget(self.SongAddFromServiceCheckBox)
        self.LeftLayout.addWidget(self.SongsModeGroupBox)
        self.LeftLayout.addStretch()
        self.SongsLayout.addWidget(self.LeftWidget)
        self.RightWidget = QtGui.QWidget(self)
        self.RightWidget.setObjectName(u'RightWidget')
        self.RightLayout = QtGui.QVBoxLayout(self.RightWidget)
        self.RightLayout.setMargin(0)
        self.RightLayout.setObjectName(u'RightLayout')
        self.RightLayout.addStretch()
        self.SongsLayout.addWidget(self.RightWidget)
        QtCore.QObject.connect(self.SearchAsTypeCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onSearchAsTypeCheckBoxChanged)
        QtCore.QObject.connect(self.SongBarActiveCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onSongBarActiveCheckBoxChanged)
        QtCore.QObject.connect(self.SongUpdateOnEditCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onSongUpdateOnEditCheckBoxChanged)
        QtCore.QObject.connect(self.SongAddFromServiceCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onSongAddFromServiceCheckBoxChanged)

    def retranslateUi(self):
        self.SongsModeGroupBox.setTitle(
            translate('SongsPlugin.SongsTab', 'Songs Mode'))
        self.SearchAsTypeCheckBox.setText(
            translate('SongsPlugin.SongsTab', 'Enable search as you type'))
        self.SongBarActiveCheckBox.setText(translate('SongsPlugin.SongsTab',
            'Display verses on live tool bar'))
        self.SongUpdateOnEditCheckBox.setText(
            translate('SongsPlugin.SongsTab', 'Update service from song edit'))
        self.SongAddFromServiceCheckBox.setText(
            translate('SongsPlugin.SongsTab',
            'Add missing songs when opening service'))

    def resizeEvent(self, event=None):
        """
        Resize the sides in two equal halves if the layout allows this.
        """
        if event:
            SettingsTab.resizeEvent(self, event)
        width = self.width() - self.SongsLayout.spacing() - \
            self.SongsLayout.contentsMargins().left() - \
            self.SongsLayout.contentsMargins().right()
        left_width = min(width - self.RightWidget.minimumSizeHint().width(),
            width / 2)
        left_width = max(left_width, self.LeftWidget.minimumSizeHint().width())
        self.LeftWidget.setMinimumWidth(left_width)

    def onSearchAsTypeCheckBoxChanged(self, check_state):
        self.song_search = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.song_search = True

    def onSongBarActiveCheckBoxChanged(self, check_state):
        self.song_bar = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.song_bar = True

    def onSongUpdateOnEditCheckBoxChanged(self, check_state):
        self.update_edit = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.update_edit = True

    def onSongAddFromServiceCheckBoxChanged(self, check_state):
        self.update_load = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.update_load = True

    def load(self):
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        self.song_search = settings.value(
            u'search as type', QtCore.QVariant(False)).toBool()
        self.song_bar = settings.value(
            u'display songbar', QtCore.QVariant(True)).toBool()
        self.update_edit = settings.value(
            u'update service on edit', QtCore.QVariant(False)).toBool()
        self.update_load = settings.value(
            u'add song from service', QtCore.QVariant(True)).toBool()
        self.SearchAsTypeCheckBox.setChecked(self.song_search)
        self.SongBarActiveCheckBox.setChecked(self.song_bar)
        self.SongUpdateOnEditCheckBox.setChecked(self.update_edit)
        self.SongAddFromServiceCheckBox.setChecked(self.update_load)
        settings.endGroup()

    def save(self):
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'search as type', QtCore.QVariant(self.song_search))
        settings.setValue(u'display songbar', QtCore.QVariant(self.song_bar))
        settings.setValue(u'update service on edit',
            QtCore.QVariant(self.update_edit))
        settings.setValue(u'add song from service',
            QtCore.QVariant(self.update_load))
        settings.endGroup()
