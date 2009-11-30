# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

from openlp.core.lib import SettingsTab, str_to_bool

class SongsTab(SettingsTab):
    """
    SongsTab is the Songs settings tab in the settings dialog.
    """
    def __init__(self, title, section=None):
        SettingsTab.__init__(self, title, section)

    def setupUi(self):
        self.setObjectName(u'SongsTab')
        self.tabTitleVisible = self.trUtf8('Songs')
        self.SongsLayout = QtGui.QFormLayout(self)
        self.SongsLayout.setObjectName(u'SongsLayout')
        self.SongsModeGroupBox = QtGui.QGroupBox(self)
        self.SongsModeGroupBox.setObjectName(u'SongsModeGroupBox')
        self.SongsModeLayout = QtGui.QVBoxLayout(self.SongsModeGroupBox)
        self.SongsModeLayout.setSpacing(8)
        self.SongsModeLayout.setMargin(8)
        self.SongsModeLayout.setObjectName(u'SongsModeLayout')
        self.SearchAsTypeCheckBox = QtGui.QCheckBox(self.SongsModeGroupBox)
        self.SearchAsTypeCheckBox.setObjectName(u'SearchAsTypeCheckBox')
        self.SongsModeLayout.addWidget(self.SearchAsTypeCheckBox)
        self.SongBarActiveCheckBox = QtGui.QCheckBox(self.SongsModeGroupBox)
        self.SongBarActiveCheckBox.setObjectName(u'SearchAsTypeCheckBox')
        self.SongsModeLayout.addWidget(self.SongBarActiveCheckBox)
        self.SongsLayout.setWidget(
            0, QtGui.QFormLayout.LabelRole, self.SongsModeGroupBox)
        QtCore.QObject.connect(self.SearchAsTypeCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onSearchAsTypeCheckBoxChanged)
        QtCore.QObject.connect(self.SongBarActiveCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.SongBarActiveCheckBoxChanged)

    def retranslateUi(self):
        self.SongsModeGroupBox.setTitle(self.trUtf8('Songs Mode'))
        self.SearchAsTypeCheckBox.setText(
            self.trUtf8('Enable search as you type:'))
        self.SongBarActiveCheckBox.setText(
            self.trUtf8('Display Verses on Live Tool bar:'))

    def onSearchAsTypeCheckBoxChanged(self, check_state):
        self.song_search = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.song_search = True

    def SongBarActiveCheckBoxChanged(self, check_state):
        self.song_bar = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.song_bar = True

    def load(self):
        self.song_search = str_to_bool(
            self.config.get_config(u'search as type', False))
        self.song_bar = str_to_bool(
            self.config.get_config(u'display songbar', True))
        self.SearchAsTypeCheckBox.setChecked(self.song_search)
        self.SongBarActiveCheckBox.setChecked(self.song_bar)

    def save(self):
        self.config.set_config(u'search as type', unicode(self.song_search))
        self.config.set_config(u'display songbar', unicode(self.song_bar))
