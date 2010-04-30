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

class Ui_SongUsageDeleteDialog(object):
    def setupUi(self, AuditDeleteDialog):
        AuditDeleteDialog.setObjectName(u'AuditDeleteDialog')
        AuditDeleteDialog.resize(291, 243)
        self.layoutWidget = QtGui.QWidget(AuditDeleteDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 247, 181))
        self.layoutWidget.setObjectName(u'layoutWidget')
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.DeleteCalendar = QtGui.QCalendarWidget(self.layoutWidget)
        self.DeleteCalendar.setFirstDayOfWeek(QtCore.Qt.Sunday)
        self.DeleteCalendar.setGridVisible(True)
        self.DeleteCalendar.setVerticalHeaderFormat(
            QtGui.QCalendarWidget.NoVerticalHeader)
        self.DeleteCalendar.setObjectName(u'DeleteCalendar')
        self.verticalLayout.addWidget(self.DeleteCalendar)
        self.buttonBox = QtGui.QDialogButtonBox(AuditDeleteDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 210, 245, 25))
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u'buttonBox')

        self.retranslateUi(AuditDeleteDialog)
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL(u'accepted()'),
            AuditDeleteDialog.accept)
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL(u'rejected()'),
            AuditDeleteDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AuditDeleteDialog)

    def retranslateUi(self, AuditDeleteDialog):
        AuditDeleteDialog.setWindowTitle(translate('AuditDeleteDialog', 'Song Usage Delete'))
