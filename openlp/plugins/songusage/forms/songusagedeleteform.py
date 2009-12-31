# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

from datetime import date

from PyQt4 import QtGui

from songusagedeletedialog import Ui_SongUsageDeleteDialog

class SongUsageDeleteForm(QtGui.QDialog, Ui_SongUsageDeleteDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, auditmanager, parent=None):
        """
        Constructor
        """
        self.auditmanager = auditmanager
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

    def accept(self):
        ret = QtGui.QMessageBox.question(self,
            self.trUtf8('Delete Selected Audit Events?'),
            self.trUtf8('Are you sure you want to delete selected Audit Data?'),
            QtGui.QMessageBox.StandardButtons(
                QtGui.QMessageBox.Ok |
                QtGui.QMessageBox.Cancel),
            QtGui.QMessageBox.Cancel)
        if ret == QtGui.QMessageBox.Ok:
            qDeleteDate = self.DeleteCalendar.selectedDate()
            deleteDate = date(qDeleteDate.year(), qDeleteDate.month(), qDeleteDate.day())
            self.auditmanager.delete_to_date(deleteDate)
        self.close()