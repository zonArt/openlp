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

from PyQt4 import QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import create_button_box

class Ui_SongBookDialog(object):
    def setupUi(self, songBookDialog):
        songBookDialog.setObjectName(u'songBookDialog')
        songBookDialog.resize(300, 10)
        self.dialogLayout = QtGui.QVBoxLayout(songBookDialog)
        self.dialogLayout.setObjectName(u'dialog_layout')
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
        self.button_box = create_button_box(songBookDialog, u'button_box', [u'cancel', u'save'])
        self.dialogLayout.addWidget(self.button_box)
        self.retranslateUi(songBookDialog)
        songBookDialog.setMaximumHeight(songBookDialog.sizeHint().height())

    def retranslateUi(self, songBookDialog):
        songBookDialog.setWindowTitle(translate('SongsPlugin.SongBookForm', 'Song Book Maintenance'))
        self.nameLabel.setText(translate('SongsPlugin.SongBookForm', '&Name:'))
        self.publisherLabel.setText(translate('SongsPlugin.SongBookForm', '&Publisher:'))
