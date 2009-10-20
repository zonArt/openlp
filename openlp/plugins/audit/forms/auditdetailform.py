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

from PyQt4 import QtCore, QtGui

from auditdetaildialog import Ui_AuditDetailDialog

class AuditDetailForm(QtGui.QDialog, Ui_AuditDetailDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, None)
        self.parent = parent
        self.setupUi(self)
        self.initialise()

    def initialise(self):
        self.firstService = \
            int(self.parent.config.get_config(u'first service', QtCore.Qt.Checked))
        self.secondService = \
            int(self.parent.config.get_config(u'second service', QtCore.Qt.Checked))
        self.resetWindow()

    def changeFirstService(self, value):
        self.firstService = value
        self.parent.config.set_config(u'first service', value)
        self.resetWindow()

    def changeSecondService(self, value):
        self.secondService = value
        self.parent.config.set_config(u'second service', value)
        self.resetWindow()

    def changeThirdService(self, value):
        pass

    def defineOutputLocation(self):
        pass

    def resetWindow(self):
        if self.firstService == QtCore.Qt.Unchecked:
            self.FirstFromTimeEdit.setEnabled(False)
            self.FirstToTimeEdit.setEnabled(False)
        else:
            self.FirstFromTimeEdit.setEnabled(True)
            self.FirstToTimeEdit.setEnabled(True)
        if self.secondService == QtCore.Qt.Unchecked:
            self.SecondFromTimeEdit.setEnabled(False)
            self.SecondToTimeEdit.setEnabled(False)
        else:
            self.SecondFromTimeEdit.setEnabled(True)
            self.SecondToTimeEdit.setEnabled(True)
