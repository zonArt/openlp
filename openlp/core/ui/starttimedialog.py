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
from openlp.core.lib.ui import UiStrings, create_accept_reject_button_box

class Ui_StartTimeDialog(object):
    def setupUi(self, StartTimeDialog):
        StartTimeDialog.setObjectName(u'StartTimeDialog')
        StartTimeDialog.resize(300, 10)
        self.dialogLayout = QtGui.QGridLayout(StartTimeDialog)
        self.dialogLayout.setObjectName(u'dialogLayout')
        self.hourLabel = QtGui.QLabel(StartTimeDialog)
        self.hourLabel.setObjectName("hourLabel")
        self.dialogLayout.addWidget(self.hourLabel, 0, 0, 1, 1)
        self.hourSpinBox = QtGui.QSpinBox(StartTimeDialog)
        self.hourSpinBox.setObjectName("hourSpinBox")
        self.dialogLayout.addWidget(self.hourSpinBox, 0, 1, 1, 1)
        self.minuteLabel = QtGui.QLabel(StartTimeDialog)
        self.minuteLabel.setObjectName("minuteLabel")
        self.dialogLayout.addWidget(self.minuteLabel, 1, 0, 1, 1)
        self.minuteSpinBox = QtGui.QSpinBox(StartTimeDialog)
        self.minuteSpinBox.setObjectName("minuteSpinBox")
        self.dialogLayout.addWidget(self.minuteSpinBox, 1, 1, 1, 1)
        self.secondLabel = QtGui.QLabel(StartTimeDialog)
        self.secondLabel.setObjectName("secondLabel")
        self.dialogLayout.addWidget(self.secondLabel, 2, 0, 1, 1)
        self.secondSpinBox = QtGui.QSpinBox(StartTimeDialog)
        self.secondSpinBox.setObjectName("secondSpinBox")
        self.dialogLayout.addWidget(self.secondSpinBox, 2, 1, 1, 1)
        self.buttonBox = create_accept_reject_button_box(StartTimeDialog, True)
        self.dialogLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.retranslateUi(StartTimeDialog)
        self.setMaximumHeight(self.sizeHint().height())
        QtCore.QMetaObject.connectSlotsByName(StartTimeDialog)

    def retranslateUi(self, StartTimeDialog):
        self.setWindowTitle(translate('OpenLP.StartTimeForm',
            'Item Start Time'))
        self.hourLabel.setText(translate('OpenLP.StartTimeForm', 'Hours:'))
        self.hourSpinBox.setSuffix(translate('OpenLP.StartTimeForm', 'h'))
        self.minuteSpinBox.setSuffix(translate('OpenLP.StartTimeForm', 'm'))
        self.secondSpinBox.setSuffix(UiStrings.S)
        self.minuteLabel.setText(translate('OpenLP.StartTimeForm', 'Minutes:'))
        self.secondLabel.setText(translate('OpenLP.StartTimeForm', 'Seconds:'))
