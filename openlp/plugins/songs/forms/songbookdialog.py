# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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

class Ui_SongBookDialog(object):
    def setupUi(self, SongBookDialog):
        SongBookDialog.setObjectName(u'SongBookDialog')
        SongBookDialog.resize(367, 120)
        self.SongBookLayout = QtGui.QFormLayout(SongBookDialog)
        self.SongBookLayout.setMargin(8)
        self.SongBookLayout.setSpacing(8)
        self.SongBookLayout.setObjectName(u'SongBookLayout')
        self.NameLabel = QtGui.QLabel(SongBookDialog)
        self.NameLabel.setObjectName(u'NameLabel')
        self.SongBookLayout.setWidget(0,
            QtGui.QFormLayout.LabelRole, self.NameLabel)
        self.NameEdit = QtGui.QLineEdit(SongBookDialog)
        self.NameEdit.setObjectName(u'NameEdit')
        self.NameLabel.setBuddy(self.NameEdit)
        self.SongBookLayout.setWidget(0,
            QtGui.QFormLayout.FieldRole, self.NameEdit)
        self.PublisherLabel = QtGui.QLabel(SongBookDialog)
        self.PublisherLabel.setObjectName(u'PublisherLabel')
        self.SongBookLayout.setWidget(1,
            QtGui.QFormLayout.LabelRole, self.PublisherLabel)
        self.PublisherEdit = QtGui.QLineEdit(SongBookDialog)
        self.PublisherEdit.setObjectName(u'PublisherEdit')
        self.PublisherLabel.setBuddy(self.PublisherEdit)
        self.SongBookLayout.setWidget(1,
            QtGui.QFormLayout.FieldRole, self.PublisherEdit)
        self.ButtonBox = QtGui.QDialogButtonBox(SongBookDialog)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Save | QtGui.QDialogButtonBox.Cancel)
        self.ButtonBox.setObjectName(u'ButtonBox')
        self.SongBookLayout.setWidget(2,
            QtGui.QFormLayout.FieldRole, self.ButtonBox)

        self.retranslateUi(SongBookDialog)
        QtCore.QObject.connect(self.ButtonBox,
            QtCore.SIGNAL(u'accepted()'), SongBookDialog.accept)
        QtCore.QObject.connect(self.ButtonBox,
            QtCore.SIGNAL(u'rejected()'), SongBookDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SongBookDialog)

    def retranslateUi(self, SongBookDialog):
        SongBookDialog.setWindowTitle(
            translate('SongsPlugin.SongBookForm', 'Song Book Maintenance'))
        self.NameLabel.setText(translate('SongsPlugin.SongBookForm', '&Name:'))
        self.PublisherLabel.setText(
            translate('SongsPlugin.SongBookForm', '&Publisher:'))
