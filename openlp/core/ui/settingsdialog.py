# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(u'SettingsDialog')
        SettingsDialog.resize(724, 502)
        self.SettingsLayout = QtGui.QVBoxLayout(SettingsDialog)
        self.SettingsLayout.setSpacing(8)
        self.SettingsLayout.setMargin(8)
        self.SettingsLayout.setObjectName(u'SettingsLayout')
        self.SettingsTabWidget = QtGui.QTabWidget(SettingsDialog)
        self.SettingsTabWidget.setObjectName(u'SettingsTabWidget')
        self.SettingsLayout.addWidget(self.SettingsTabWidget)
        self.ButtonsBox = QtGui.QDialogButtonBox(SettingsDialog)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ButtonsBox.sizePolicy().hasHeightForWidth())
        self.ButtonsBox.setSizePolicy(sizePolicy)
        self.ButtonsBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.ButtonsBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonsBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.ButtonsBox.setObjectName(u'ButtonsBox')
        self.SettingsLayout.addWidget(self.ButtonsBox)
        self.retranslateUi(SettingsDialog)
        self.SettingsTabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.ButtonsBox,
            QtCore.SIGNAL(u'accepted()'), SettingsDialog.accept)
        QtCore.QObject.connect(self.ButtonsBox,
            QtCore.SIGNAL(u'rejected()'), SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(translate(u'SettingsForm', u'Settings'))
