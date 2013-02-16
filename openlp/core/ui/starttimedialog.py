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
"""
The UI widgets for the time dialog
"""
from PyQt4 import QtCore, QtGui

from openlp.core.lib import UiStrings, translate
from openlp.core.lib.ui import create_button_box


class Ui_StartTimeDialog(object):
    """
    The UI widgets for the time dialog
    """
    def setupUi(self, StartTimeDialog):
        """
        Set up the UI
        """
        StartTimeDialog.setObjectName(u'StartTimeDialog')
        StartTimeDialog.resize(350, 10)
        self.dialogLayout = QtGui.QGridLayout(StartTimeDialog)
        self.dialogLayout.setObjectName(u'dialog_layout')
        self.startLabel = QtGui.QLabel(StartTimeDialog)
        self.startLabel.setObjectName(u'startLabel')
        self.startLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.dialogLayout.addWidget(self.startLabel, 0, 1, 1, 1)
        self.finishLabel = QtGui.QLabel(StartTimeDialog)
        self.finishLabel.setObjectName(u'finishLabel')
        self.finishLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.dialogLayout.addWidget(self.finishLabel, 0, 2, 1, 1)
        self.lengthLabel = QtGui.QLabel(StartTimeDialog)
        self.lengthLabel.setObjectName(u'startLabel')
        self.lengthLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.dialogLayout.addWidget(self.lengthLabel, 0, 3, 1, 1)
        self.hourLabel = QtGui.QLabel(StartTimeDialog)
        self.hourLabel.setObjectName(u'hourLabel')
        self.dialogLayout.addWidget(self.hourLabel, 1, 0, 1, 1)
        self.hourSpinBox = QtGui.QSpinBox(StartTimeDialog)
        self.hourSpinBox.setObjectName(u'hourSpinBox')
        self.hourSpinBox.setMinimum(0)
        self.hourSpinBox.setMaximum(4)
        self.dialogLayout.addWidget(self.hourSpinBox, 1, 1, 1, 1)
        self.hourFinishSpinBox = QtGui.QSpinBox(StartTimeDialog)
        self.hourFinishSpinBox.setObjectName(u'hourFinishSpinBox')
        self.hourFinishSpinBox.setMinimum(0)
        self.hourFinishSpinBox.setMaximum(4)
        self.dialogLayout.addWidget(self.hourFinishSpinBox, 1, 2, 1, 1)
        self.hourFinishLabel = QtGui.QLabel(StartTimeDialog)
        self.hourFinishLabel.setObjectName(u'hourLabel')
        self.hourFinishLabel.setAlignment(QtCore.Qt.AlignRight)
        self.dialogLayout.addWidget(self.hourFinishLabel, 1, 3, 1, 1)
        self.minuteLabel = QtGui.QLabel(StartTimeDialog)
        self.minuteLabel.setObjectName(u'minuteLabel')
        self.dialogLayout.addWidget(self.minuteLabel, 2, 0, 1, 1)
        self.minuteSpinBox = QtGui.QSpinBox(StartTimeDialog)
        self.minuteSpinBox.setObjectName(u'minuteSpinBox')
        self.minuteSpinBox.setMinimum(0)
        self.minuteSpinBox.setMaximum(59)
        self.dialogLayout.addWidget(self.minuteSpinBox, 2, 1, 1, 1)
        self.minuteFinishSpinBox = QtGui.QSpinBox(StartTimeDialog)
        self.minuteFinishSpinBox.setObjectName(u'minuteFinishSpinBox')
        self.minuteFinishSpinBox.setMinimum(0)
        self.minuteFinishSpinBox.setMaximum(59)
        self.dialogLayout.addWidget(self.minuteFinishSpinBox, 2, 2, 1, 1)
        self.minuteFinishLabel = QtGui.QLabel(StartTimeDialog)
        self.minuteFinishLabel.setObjectName(u'minuteLabel')
        self.minuteFinishLabel.setAlignment(QtCore.Qt.AlignRight)
        self.dialogLayout.addWidget(self.minuteFinishLabel, 2, 3, 1, 1)
        self.secondLabel = QtGui.QLabel(StartTimeDialog)
        self.secondLabel.setObjectName(u'secondLabel')
        self.dialogLayout.addWidget(self.secondLabel, 3, 0, 1, 1)
        self.secondSpinBox = QtGui.QSpinBox(StartTimeDialog)
        self.secondSpinBox.setObjectName(u'secondSpinBox')
        self.secondSpinBox.setMinimum(0)
        self.secondSpinBox.setMaximum(59)
        self.secondFinishSpinBox = QtGui.QSpinBox(StartTimeDialog)
        self.secondFinishSpinBox.setObjectName(u'secondFinishSpinBox')
        self.secondFinishSpinBox.setMinimum(0)
        self.secondFinishSpinBox.setMaximum(59)
        self.dialogLayout.addWidget(self.secondFinishSpinBox, 3, 2, 1, 1)
        self.secondFinishLabel = QtGui.QLabel(StartTimeDialog)
        self.secondFinishLabel.setObjectName(u'secondLabel')
        self.secondFinishLabel.setAlignment(QtCore.Qt.AlignRight)
        self.dialogLayout.addWidget(self.secondFinishLabel, 3, 3, 1, 1)
        self.dialogLayout.addWidget(self.secondSpinBox, 3, 1, 1, 1)
        self.button_box = create_button_box(StartTimeDialog, u'button_box', [u'cancel', u'ok'])
        self.dialogLayout.addWidget(self.button_box, 5, 2, 1, 2)
        self.retranslateUi(StartTimeDialog)
        self.setMaximumHeight(self.sizeHint().height())

    def retranslateUi(self, StartTimeDialog):
        """
        Update the translations on the fly
        """
        self.setWindowTitle(translate('OpenLP.StartTimeForm', 'Item Start and Finish Time'))
        self.hourSpinBox.setSuffix(UiStrings().Hours)
        self.minuteSpinBox.setSuffix(UiStrings().Minutes)
        self.secondSpinBox.setSuffix(UiStrings().Seconds)
        self.hourFinishSpinBox.setSuffix(UiStrings().Hours)
        self.minuteFinishSpinBox.setSuffix(UiStrings().Minutes)
        self.secondFinishSpinBox.setSuffix(UiStrings().Seconds)
        self.hourLabel.setText(translate('OpenLP.StartTimeForm', 'Hours:'))
        self.minuteLabel.setText(translate('OpenLP.StartTimeForm', 'Minutes:'))
        self.secondLabel.setText(translate('OpenLP.StartTimeForm', 'Seconds:'))
        self.startLabel.setText(translate('OpenLP.StartTimeForm', 'Start'))
        self.finishLabel.setText(translate('OpenLP.StartTimeForm', 'Finish'))
        self.lengthLabel.setText(translate('OpenLP.StartTimeForm', 'Length'))
