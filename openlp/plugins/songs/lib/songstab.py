# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from openlp.core.lib import SettingsTab, str_to_bool, translate

class SongsTab(SettingsTab):
    """
    SongsTab is the Songs settings tab in the settings dialog.
    """
    def __init__(self):
        SettingsTab.__init__(self, u'Songs', u'Songs')

    def setupUi(self):
        self.setObjectName(u'SongsTab')
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
        self.SongsLayout.setWidget(
            0, QtGui.QFormLayout.LabelRole, self.SongsModeGroupBox)
        QtCore.QObject.connect(self.SearchAsTypeCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.onSearchAsTypeCheckBoxChanged)

    def retranslateUi(self):
        self.SongsModeGroupBox.setTitle(self.trUtf8(u'Songs Mode'))
        self.SearchAsTypeCheckBox.setText(self.trUtf8(u'Enable search as you type:'))

    def onSearchAsTypeCheckBoxChanged(self, check_state):
        self.bible_search = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.bible_search = True

    def load(self):
        self.bible_search = str_to_bool(
            self.config.get_config(u'search as type', u'False'))
        self.SearchAsTypeCheckBox.setChecked(self.bible_search)

    def save(self):
        self.config.set_config(u'search as type', unicode(self.bible_search))
