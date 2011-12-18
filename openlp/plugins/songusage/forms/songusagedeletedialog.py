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

from openlp.core.lib import translate

class Ui_SongUsageDeleteDialog(object):
    def setupUi(self, songUsageDeleteDialog):
        songUsageDeleteDialog.setObjectName(u'songUsageDeleteDialog')
        songUsageDeleteDialog.resize(291, 243)
        self.verticalLayout = QtGui.QVBoxLayout(songUsageDeleteDialog)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.deleteLabel = QtGui.QLabel(songUsageDeleteDialog)
        self.deleteLabel.setObjectName(u'deleteLabel')
        self.verticalLayout.addWidget(self.deleteLabel)
        self.deleteCalendar = QtGui.QCalendarWidget(songUsageDeleteDialog)
        self.deleteCalendar.setFirstDayOfWeek(QtCore.Qt.Sunday)
        self.deleteCalendar.setGridVisible(True)
        self.deleteCalendar.setVerticalHeaderFormat(
            QtGui.QCalendarWidget.NoVerticalHeader)
        self.deleteCalendar.setObjectName(u'deleteCalendar')
        self.verticalLayout.addWidget(self.deleteCalendar)
        self.buttonBox = QtGui.QDialogButtonBox(songUsageDeleteDialog)
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(u'buttonBox')
        self.verticalLayout.addWidget(self.buttonBox)
        self.retranslateUi(songUsageDeleteDialog)

    def retranslateUi(self, songUsageDeleteDialog):
        songUsageDeleteDialog.setWindowTitle(
            translate('SongUsagePlugin.SongUsageDeleteForm',
                'Delete Song Usage Data'))
        self.deleteLabel.setText(
            translate('SongUsagePlugin.SongUsageDeleteForm',
                'Select the date up to which the song usage data should be '
                'deleted. All data recorded before this date will be '
                'permanently deleted.'))
