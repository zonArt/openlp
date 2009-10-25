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

    def initialise(self):
        self.FirstCheckBox.setCheckState(
            int(self.parent.config.get_config(u'first service', QtCore.Qt.Checked)))
        self.SecondCheckBox.setCheckState(
            int(self.parent.config.get_config(u'second service', QtCore.Qt.Checked)))
        self.ThirdCheckBox.setCheckState(
            int(self.parent.config.get_config(u'third service', QtCore.Qt.Checked)))
        year = QtCore.QDate().currentDate().year()
        if QtCore.QDate().currentDate().month() < 9:
            year -= 1
        toDate = QtCore.QDate(year, 8, 31)
        fromDate = QtCore.QDate(year - 1, 9, 1)
        self.FromDateEdit.setDate(fromDate)
        self.ToDateEdit.setDate(toDate)
        self.FileLineEdit.setText(self.parent.config.get_last_dir(1))
        self.resetWindow()

    def changeFirstService(self, value):
        self.parent.config.set_config(u'first service', value)
        self.resetWindow()

    def changeSecondService(self, value):
        self.parent.config.set_config(u'second service', value)
        self.resetWindow()

    def changeThirdService(self, value):
        self.parent.config.set_config(u'third service', value)
        self.resetWindow()

    def defineOutputLocation(self):
        path = QtGui.QFileDialog.getExistingDirectory(self,
            self.trUtf8(u'Output File Location'),
            self.parent.config.get_last_dir(1) )
        path = unicode(path)
        if path != u'':
            self.parent.config.set_last_dir(path, 1)
            self.FileLineEdit.setText(path)

    def resetWindow(self):
        if self.FirstCheckBox.checkState() == QtCore.Qt.Unchecked:
            self.FirstFromTimeEdit.setEnabled(False)
            self.FirstToTimeEdit.setEnabled(False)
        else:
            self.FirstFromTimeEdit.setEnabled(True)
            self.FirstToTimeEdit.setEnabled(True)
        if self.SecondCheckBox.checkState() == QtCore.Qt.Unchecked:
            self.SecondFromTimeEdit.setEnabled(False)
            self.SecondToTimeEdit.setEnabled(False)
        else:
            self.SecondFromTimeEdit.setEnabled(True)
            self.SecondToTimeEdit.setEnabled(True)
        if self.ThirdCheckBox.checkState() == QtCore.Qt.Unchecked:
            self.ThirdFromTimeEdit.setEnabled(False)
            self.ThirdToTimeEdit.setEnabled(False)
        else:
            self.ThirdFromTimeEdit.setEnabled(True)
            self.ThirdToTimeEdit.setEnabled(True)

    def accept(self):
        print self.DetailedReport.isChecked()
        print self.SummaryReport.isChecked()
        print self.FromDateEdit.date()
        print self.ToDateEdit.date()
        if self.DetailedReport.isChecked():
            self.detailedReport()
        else:
            self.summaryReport()
        self.close()

    def detailedReport(self):
        print "detailed"
        filename = u'audit_det_%s_%s.txt' % \
            (self.FromDateEdit.date().toString(u'ddMMyyyy'),
             self.ToDateEdit.date().toString(u'ddMMyyyy'))
        print filename

    def summaryReport(self):
        print "summary"
        filename = u'audit_sum_%s_%s.txt' % \
            (self.FromDateEdit.date().toString(u'ddMMyyyy'),
             self.ToDateEdit.date().toString(u'ddMMyyyy'))
        print filename
