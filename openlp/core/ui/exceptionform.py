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
import platform

import sqlalchemy
import BeautifulSoup
import enchant
import chardet
try:
    import sqlite
    sqlite_version = sqlite.version
except ImportError:
    sqlite_version = u'-'

from lxml import etree
from PyQt4 import Qt, QtCore, QtGui

from openlp.core.lib import translate, SettingsManager, mailto

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

    def _createReport(self):
        openlp_version = self.parent().applicationVersion[u'full']
        traceback = unicode(self.exceptionTextEdit.toPlainText()) 
        system = unicode(translate('OpenLP.ExceptionForm',
            'Platform: %s\n')) % (platform.platform())
        libraries = unicode(translate('OpenLP.ExceptionForm',
            'Python: %s\n'
            'PyQt4: %s\n'
            'Qt4: %s\n'
            'SQLAlchemy: %s\n'
            'lxml: %s\n'
            'BeautifulSoup: %s\n'
            'PyEnchant: %s\n'
            'Chardet: %s\n'
            'PySQLite: %s\n')) % (platform.python_version(),
             Qt.PYQT_VERSION_STR, Qt.qVersion(), sqlalchemy.__version__,
             etree.__version__, BeautifulSoup.__version__ , enchant.__version__,
             chardet.__version__, sqlite_version)
        return (openlp_version, traceback, system, libraries)
 
    def onSaveReportButtonPressed(self):
        """
        Saving exception log and system informations to a file.
        """
        report = unicode(translate('OpenLP.ExceptionForm',
            '**OpenLP Bug Report**\n'
            'Version: %s\n\n'
            '--- Exception Traceback ---\n%s\n'
            '--- System information ---\n%s\n'
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
            'Version: %s\n\n'
            '--- Please enter the report below this line. ---\n\n\n'
            '--- Exception Traceback ---\n%s\n'
            '--- System information ---\n%s\n'
            '--- Library Versions ---\n%s\n'))
        mailto.mailto(address=u'bugs@openlp.org', subject=u'OpenLP Bug Report',
            body=email_body % self._createReport())
