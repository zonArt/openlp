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

from openlp.core.lib import translate
from openlp.core.lib.ui import create_accept_reject_button_box

class Ui_SongBookDialog(object):
    def setupUi(self, songBookDialog):
        songBookDialog.setObjectName(u'songBookDialog')
        songBookDialog.resize(300, 10)
        self.dialogLayout = QtGui.QVBoxLayout(songBookDialog)
        self.dialogLayout.setObjectName(u'dialogLayout')
        self.bookLayout = QtGui.QFormLayout()
        self.bookLayout.setObjectName(u'bookLayout')
        self.nameLabel = QtGui.QLabel(songBookDialog)
        self.nameLabel.setObjectName(u'nameLabel')
        self.nameEdit = QtGui.QLineEdit(songBookDialog)
        self.nameEdit.setObjectName(u'nameEdit')
        self.nameLabel.setBuddy(self.nameEdit)
        self.bookLayout.addRow(self.nameLabel, self.nameEdit)
        self.publisherLabel = QtGui.QLabel(songBookDialog)
        self.publisherLabel.setObjectName(u'publisherLabel')
        self.publisherEdit = QtGui.QLineEdit(songBookDialog)
        self.publisherEdit.setObjectName(u'publisherEdit')
        self.publisherLabel.setBuddy(self.publisherEdit)
        self.bookLayout.addRow(self.publisherLabel, self.publisherEdit)
        self.dialogLayout.addLayout(self.bookLayout)
        self.dialogLayout.addWidget(
            create_accept_reject_button_box(songBookDialog))
        self.retranslateUi(songBookDialog)
        songBookDialog.setMaximumHeight(songBookDialog.sizeHint().height())
        QtCore.QMetaObject.connectSlotsByName(songBookDialog)

    def retranslateUi(self, songBookDialog):
        songBookDialog.setWindowTitle(
            translate('SongsPlugin.SongBookForm', 'Song Book Maintenance'))
        self.nameLabel.setText(translate('SongsPlugin.SongBookForm', '&Name:'))
        self.publisherLabel.setText(
            translate('SongsPlugin.SongBookForm', '&Publisher:'))
