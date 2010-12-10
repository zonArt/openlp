# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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

import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, build_icon, SettingsManager
from openlp.core.ui.mailto import mailto

from exceptiondialog import Ui_ExceptionDialog

class ExceptionForm(QtGui.QDialog, Ui_ExceptionDialog):
    """
    The exception dialog
    """
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.settingsSection = u'crashreport'
        #TODO: Icons
        self.saveReportButton = QtGui.QPushButton(self)
        self.saveReportButton.setIcon(build_icon(u':/icon/openlp-logo-16x16.png'))
        self.saveReportButton.setText(translate('OpenLP.ExceptionForm', 'Save Report to File'))
        self.saveReportButton.setObjectName(u'saveReportButton')
        self.sendReportButton = QtGui.QPushButton(self)
        self.sendReportButton.setIcon(build_icon(u':/icon/openlp-logo-16x16.png'))
        self.sendReportButton.setText(translate('OpenLP.ExceptionForm', 'Send Report Mail'))
        self.sendReportButton.setObjectName(u'sendReportButton')
        self.exceptionButtonBox.addButton(self.saveReportButton,
            QtGui.QDialogButtonBox.ActionRole)
        self.exceptionButtonBox.addButton(self.sendReportButton,
            QtGui.QDialogButtonBox.ActionRole)
        QtCore.QObject.connect(self.saveReportButton,
            QtCore.SIGNAL(u'pressed()'), self.onSaveReportButtonPressed)
        QtCore.QObject.connect(self.sendReportButton,
            QtCore.SIGNAL(u'pressed()'), self.onSendReportButtonPressed)

    def _createReport(self):
        system = unicode(translate('OpenLP.ExceptionForm',
            'Operating System: %s\n'
            'Desktop Envoirnment: %s'))
        libraries = unicode(translate('OpenLP.ExceptionForm',
            'Python: %s\n'
            'PyQt: %s\n'
            'SQLAlchemy: %s\n'
            'lxml: %s\n'
            'BeautifulSoup: %s\n'
            'PyEnchant: %s\n'
            'Chardet: %s\n'
            'pysqlite: %s'))
        #TODO: collect the informations
        version = self.parent().applicationVersion[u'full']
        return (version, system, libraries)
 
    def onSaveReportButtonPressed(self):
        """
        Saving exception log and system informations to a file.
        """
        report = unicode(translate('OpenLP.ExceptionForm',
            '*OpenLP Bug Report*\n'
            'Version: %s\n'
            '--- System information. ---\n%s\n'
            '--- Library Versions ---\n%s\n'))
        filename = QtGui.QFileDialog.getSaveFileName(self,
            translate('OpenLP.ExceptionForm', 'Save Crash Report'),
            SettingsManager.get_last_dir(self.settingsSection),
            translate('OpenLP.ExceptionForm', 'Text files (*.txt *.log *.text)'))
        if filename:
            filename = unicode(QtCore.QDir.toNativeSeparators(filename))
            SettingsManager.set_last_dir(self.settingsSection, os.path.dirname(
                filename))
            report = report % self._createReport()
            try:
                file = open(filename, u'w')
                try:
                    file.write(report)
                except UnicodeError:
                    file.close()
                    file = open(filename, u'wb')
                    file.write(report.encode(u'utf-8'))
                file.close()
            except IOError:
                log.exception(u'Failed to write crash report')

    def onSendReportButtonPressed(self):
        """
        Opening systems default email client and inserting exception log and
        system informations.
        """
        email_body = unicode(translate('OpenLP.ExceptionForm',
            '*OpenLP Bug Report*\n'
            'Version: %s\n'
            '--- Please enter the report below this line. ---\n\n\n'
            '--- System information. ---\n%s\n'
            '--- Library Versions ---\n%s\n'))
        mailto(address=u'bugs@openlp.org', subject=u'OpenLP Bug Report',
            body=email_body % self._createReport())
