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

from openlp.core.lib import translate, build_icon

class Ui_SettingsDialog(object):
    def setupUi(self, settingsDialog):
        settingsDialog.setObjectName(u'settingsDialog')
        settingsDialog.resize(700, 500)
        settingsDialog.setWindowIcon(
            build_icon(u':/system/system_settings.png'))
        self.settingsLayout = QtGui.QVBoxLayout(settingsDialog)
        margins = self.settingsLayout.contentsMargins()
        self.settingsLayout.setObjectName(u'settingsLayout')
        self.settingsTabWidget = QtGui.QTabWidget(settingsDialog)
        self.settingsTabWidget.setObjectName(u'settingsTabWidget')
        self.settingsLayout.addWidget(self.settingsTabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(settingsDialog)
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u'buttonBox')
        self.settingsLayout.addWidget(self.buttonBox)
        self.retranslateUi(settingsDialog)
        QtCore.QObject.connect(self.buttonBox,
            QtCore.SIGNAL(u'accepted()'), settingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox,
            QtCore.SIGNAL(u'rejected()'), settingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(settingsDialog)

    def retranslateUi(self, settingsDialog):
        settingsDialog.setWindowTitle(translate('OpenLP.SettingsForm',
            'Configure OpenLP'))
