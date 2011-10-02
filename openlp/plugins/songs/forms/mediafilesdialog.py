# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
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

from openlp.core.lib import translate, build_icon

class Ui_MediaFilesDialog(object):
    def setupUi(self, mediaFilesDialog):
        mediaFilesDialog.setObjectName(u'mediaFilesDialog')
        mediaFilesDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        mediaFilesDialog.resize(400, 300)
        mediaFilesDialog.setModal(True)
        mediaFilesDialog.setWindowIcon(
            build_icon(u':/icon/openlp-logo-16x16.png'))
        self.filesVerticalLayout = QtGui.QVBoxLayout(mediaFilesDialog)
        self.filesVerticalLayout.setSpacing(8)
        self.filesVerticalLayout.setMargin(8)
        self.filesVerticalLayout.setObjectName(u'filesVerticalLayout')
        self.selectLabel = QtGui.QLabel(mediaFilesDialog)
        self.selectLabel.setWordWrap(True)
        self.selectLabel.setObjectName(u'selectLabel')
        self.filesVerticalLayout.addWidget(self.selectLabel)
        self.fileListWidget = QtGui.QListWidget(mediaFilesDialog)
        self.fileListWidget.setAlternatingRowColors(True)
        self.fileListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.fileListWidget.setObjectName(u'fileListWidget')
        self.filesVerticalLayout.addWidget(self.fileListWidget)
        self.buttonBox = QtGui.QDialogButtonBox(mediaFilesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u'buttonBox')
        self.filesVerticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(mediaFilesDialog)
        QtCore.QObject.connect(self.buttonBox,
            QtCore.SIGNAL(u'accepted()'), mediaFilesDialog.accept)
        QtCore.QObject.connect(self.buttonBox,
            QtCore.SIGNAL(u'rejected()'), mediaFilesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(mediaFilesDialog)

    def retranslateUi(self, mediaFilesDialog):
        mediaFilesDialog.setWindowTitle(
            translate('SongsPlugin.MediaFilesForm', 'Select Media File(s)'))
        self.selectLabel.setText(
            translate('SongsPlugin.MediaFilesForm', u'Select one or more '
                'audio files from the list below, and click OK to import them '
                'into this song.'))
