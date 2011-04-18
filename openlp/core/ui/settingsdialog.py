# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
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
from openlp.core.lib.ui import create_accept_reject_button_box

class Ui_SettingsDialog(object):
    def setupUi(self, settingsDialog):
        settingsDialog.setObjectName(u'settingsDialog')
        settingsDialog.resize(800, 500)
        settingsDialog.setWindowIcon(
            build_icon(u':/system/system_settings.png'))
        self.dialogLayout = QtGui.QGridLayout(settingsDialog)
        self.dialogLayout.setObjectName(u'dialogLayout')
        self.dialogLayout.setMargin(8)
        self.settingListWidget = QtGui.QListWidget(settingsDialog)
        self.settingListWidget.setUniformItemSizes(True)
        self.settingListWidget.setMinimumSize(QtCore.QSize(150, 0))
        self.settingListWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.settingListWidget.setObjectName(u'settingListWidget')
        self.dialogLayout.addWidget(self.settingListWidget, 0, 0, 1, 1)
        self.stackedLayout = QtGui.QStackedLayout()
        self.stackedLayout.setObjectName(u'stackedLayout')
        self.dialogLayout.addLayout(self.stackedLayout, 0, 1, 1, 1)
        self.buttonBox = create_accept_reject_button_box(settingsDialog, True)
        self.dialogLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.retranslateUi(settingsDialog)
        QtCore.QMetaObject.connectSlotsByName(settingsDialog)
        QtCore.QObject.connect(self.settingListWidget,
            QtCore.SIGNAL(u'currentRowChanged(int)'),
            self.stackedLayout.setCurrentIndex)

    def retranslateUi(self, settingsDialog):
        settingsDialog.setWindowTitle(translate('OpenLP.SettingsForm',
            'Configure OpenLP'))
