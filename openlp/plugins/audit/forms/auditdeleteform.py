# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from PyQt4 import QtCore, QtGui

from auditdeletedialog import Ui_AuditDeleteDialog
from openlp.core.lib import translate
from openlp.plugins.audit.lib import AuditManager

class AuditDeleteForm(QtGui.QDialog, Ui_AuditDeleteDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, auditmanager, parent = None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

    def accept(self):
        ret = QtGui.QMessageBox.question(None,
            translate(u'mainWindow', u'Delete Selected Audit Events?'),
            translate(u'mainWindow', u'Are you sure you want to delete selected Audit Data?'),
            QtGui.QMessageBox.StandardButtons(
                QtGui.QMessageBox.Ok |
                QtGui.QMessageBox.Cancel),
            QtGui.QMessageBox.Cancel)
        if ret == QtGui.QMessageBox.Ok:
            qDeleteDate = self.DeleteCalendar.selectedDate()
            print qDeleteDate
            deleteDate = date(qDeleteDate.year(), qDeleteDate.month(), qDeleteDate.day())
            print deleteDate
        self.close()
