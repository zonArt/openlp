# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Millar, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Jeffrey Smith, Maikel            #
# Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund                    #
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
import logging
import re
import os
import platform

import sqlalchemy
import BeautifulSoup
from lxml import etree
from PyQt4 import Qt, QtCore, QtGui

try:
    from PyQt4.phonon import Phonon
    PHONON_VERSION = Phonon.phononVersion()
except ImportError:
    PHONON_VERSION = u'-'
try:
    import chardet
    CHARDET_VERSION = chardet.__version__
except ImportError:
    CHARDET_VERSION = u'-'
try:
    import enchant
    ENCHANT_VERSION = enchant.__version__
except ImportError:
    ENCHANT_VERSION = u'-'
try:
    import sqlite
    SQLITE_VERSION = sqlite.version
except ImportError:
    SQLITE_VERSION = u'-'

from openlp.core.lib import translate, SettingsManager
from openlp.core.lib.mailto import mailto
from openlp.core.lib.ui import UiStrings
from openlp.core.utils import get_application_version

from exceptiondialog import Ui_ExceptionDialog

log = logging.getLogger(__name__)

class ExceptionForm(QtGui.QDialog, Ui_ExceptionDialog):
    """
    The exception dialog
    """
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.settingsSection = u'crashreport'

    def exec_(self):
        self.descriptionTextEdit.setPlainText(u'')
        self.onDescriptionUpdated()
        self.fileAttachment = None
        return QtGui.QDialog.exec_(self)

    def _createReport(self):
        openlp_version = get_application_version()
        description = unicode(self.descriptionTextEdit.toPlainText())
        traceback = unicode(self.exceptionTextEdit.toPlainText())
        system = unicode(translate('OpenLP.ExceptionForm',
            'Platform: %s\n')) % platform.platform()
        libraries = u'Python: %s\n' % platform.python_version() + \
            u'Qt4: %s\n' % Qt.qVersion() + \
            u'Phonon: %s\n' % PHONON_VERSION + \
            u'PyQt4: %s\n' % Qt.PYQT_VERSION_STR + \
            u'SQLAlchemy: %s\n' % sqlalchemy.__version__ + \
            u'BeautifulSoup: %s\n' % BeautifulSoup.__version__ + \
            u'lxml: %s\n' % etree.__version__ + \
            u'Chardet: %s\n' % CHARDET_VERSION + \
            u'PyEnchant: %s\n' % ENCHANT_VERSION + \
            u'PySQLite: %s\n' % SQLITE_VERSION
        if platform.system() == u'Linux':
            if os.environ.get(u'KDE_FULL_SESSION') == u'true':
                system = system + u'Desktop: KDE SC\n'
            elif os.environ.get(u'GNOME_DESKTOP_SESSION_ID'):
                system = system + u'Desktop: GNOME\n'
        return (openlp_version, description, traceback, system, libraries)

    def onSaveReportButtonPressed(self):
        """
        Saving exception log and system informations to a file.
        """
        report = unicode(translate('OpenLP.ExceptionForm',
            '**OpenLP Bug Report**\n'
            'Version: %s\n\n'
            '--- Details of the Exception. ---\n\n%s\n\n '
            '--- Exception Traceback ---\n%s\n'
            '--- System information ---\n%s\n'
            '--- Library Versions ---\n%s\n'))
        filename = QtGui.QFileDialog.getSaveFileName(self,
            translate('OpenLP.ExceptionForm', 'Save Crash Report'),
            SettingsManager.get_last_dir(self.settingsSection),
            translate('OpenLP.ExceptionForm',
            'Text files (*.txt *.log *.text)'))
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
                finally:
                    file.close()
            except IOError:
                log.exception(u'Failed to write crash report')
            finally:
                file.close()

    def onSendReportButtonPressed(self):
        """
        Opening systems default email client and inserting exception log and
        system informations.
        """
        body = unicode(translate('OpenLP.ExceptionForm',
            '*OpenLP Bug Report*\n'
            'Version: %s\n\n'
            '--- Details of the Exception. ---\n\n%s\n\n '
            '--- Exception Traceback ---\n%s\n'
            '--- System information ---\n%s\n'
            '--- Library Versions ---\n%s\n',
            'Please add the information that bug reports are favoured written '
            'in English.'))
        content = self._createReport()
        for line in content[2].split(u'\n'):
            if re.search(r'[/\\]openlp[/\\]', line):
                source = re.sub(r'.*[/\\]openlp[/\\](.*)".*', r'\1', line)
            if u':' in line:
                exception = line.split(u'\n')[-1].split(u':')[0]
        subject = u'Bug report: %s in %s' % (exception, source)
        if self.fileAttachment:
            mailto(address=u'bugs@openlp.org', subject=subject,
                body=body % content, attach=self.fileAttachment)
        else:
            mailto(address=u'bugs@openlp.org', subject=subject,
                body=body % content)

    def onDescriptionUpdated(self):
        count = int(20 - len(self.descriptionTextEdit.toPlainText()))
        if count < 0:
            count = 0
            self.__buttonState(True)
        else:
            self.__buttonState(False)
        self.descriptionWordCount.setText(
            unicode(translate('OpenLP.ExceptionDialog',
            'Description characters to enter : %s')) % count)

    def onAttachFileButtonPressed(self):
        files = QtGui.QFileDialog.getOpenFileName(
            self,translate('ImagePlugin.ExceptionDialog',
            'Select Attachment'),
            SettingsManager.get_last_dir(u'exceptions'),
            u'%s (*.*) (*)' % UiStrings().AllFiles)
        log.info(u'New files(s) %s', unicode(files))
        if files:
            self.fileAttachment = unicode(files)

    def __buttonState(self, state):
        self.saveReportButton.setEnabled(state)
        self.sendReportButton.setEnabled(state)

