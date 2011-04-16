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

from openlp.core.lib import translate
from openlp.core.lib.ui import create_accept_reject_button_box

class Ui_SongUsageDeleteDialog(object):
    def setupUi(self, songUsageDeleteDialog):
        songUsageDeleteDialog.setObjectName(u'songUsageDeleteDialog')
        songUsageDeleteDialog.resize(291, 243)
        self.layoutWidget = QtGui.QWidget(songUsageDeleteDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 247, 181))
        self.layoutWidget.setObjectName(u'layoutWidget')
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.deleteCalendar = QtGui.QCalendarWidget(self.layoutWidget)
        self.deleteCalendar.setFirstDayOfWeek(QtCore.Qt.Sunday)
        self.deleteCalendar.setGridVisible(True)
        self.deleteCalendar.setVerticalHeaderFormat(
            QtGui.QCalendarWidget.NoVerticalHeader)
        self.deleteCalendar.setObjectName(u'deleteCalendar')
        self.verticalLayout.addWidget(self.deleteCalendar)
        self.buttonBox = create_accept_reject_button_box(
            songUsageDeleteDialog, True)
        self.buttonBox.setGeometry(QtCore.QRect(30, 210, 245, 25))
        self.buttonBox.setObjectName(u'buttonBox')
        self.retranslateUi(songUsageDeleteDialog)
        QtCore.QMetaObject.connectSlotsByName(songUsageDeleteDialog)

    def retranslateUi(self, songUsageDeleteDialog):
        songUsageDeleteDialog.setWindowTitle(
            translate('SongUsagePlugin.SongUsageDeleteForm',
            'Delete Song Usage Data'))
