# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
The actual exception dialog form.
"""
import logging
import re
import os
import platform

import sqlalchemy
import BeautifulSoup
from lxml import etree
from PyQt4 import Qt, QtCore, QtGui, QtWebKit

try:
    from PyQt4.phonon import Phonon
    PHONON_VERSION = Phonon.phononVersion()
except ImportError:
    PHONON_VERSION = u'-'
try:
    import migrate
    MIGRATE_VERSION = getattr(migrate, u'__version__', u'< 0.7')
except ImportError:
    MIGRATE_VERSION = u'-'
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
try:
    import mako
    MAKO_VERSION = mako.__version__
except ImportError:
    MAKO_VERSION = u'-'
try:
    import uno
    arg = uno.createUnoStruct(u'com.sun.star.beans.PropertyValue')
    arg.Name = u'nodepath'
    arg.Value = u'/org.openoffice.Setup/Product'
    context = uno.getComponentContext()
    provider = context.ServiceManager.createInstance(u'com.sun.star.configuration.ConfigurationProvider')
    node = provider.createInstanceWithArguments(u'com.sun.star.configuration.ConfigurationAccess', (arg,))
    UNO_VERSION = node.getByName(u'ooSetupVersion')
except ImportError:
    UNO_VERSION = u'-'
except:
    UNO_VERSION = u'- (Possible non-standard UNO installation)'
try:
    WEBKIT_VERSION = QtWebKit.qWebKitVersion()
except AttributeError:
    WEBKIT_VERSION = u'-'


from openlp.core.lib import UiStrings, Settings, translate
from openlp.core.utils import get_application_version

from exceptiondialog import Ui_ExceptionDialog

log = logging.getLogger(__name__)


class ExceptionForm(QtGui.QDialog, Ui_ExceptionDialog):
    """
    The exception dialog
    """
    def __init__(self, parent):
        """
        Constructor.
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.settingsSection = u'crashreport'

    def exec_(self):
        """
        Show the dialog.
        """
        self.descriptionTextEdit.setPlainText(u'')
        self.onDescriptionUpdated()
        self.fileAttachment = None
        return QtGui.QDialog.exec_(self)

    def _createReport(self):
        """
        Create an exception report.
        """
        openlp_version = get_application_version()
        description = self.descriptionTextEdit.toPlainText()
        traceback = self.exceptionTextEdit.toPlainText()
        system = translate('OpenLP.ExceptionForm', 'Platform: %s\n') % platform.platform()
        libraries = u'Python: %s\n' % platform.python_version() + \
            u'Qt4: %s\n' % Qt.qVersion() + \
            u'Phonon: %s\n' % PHONON_VERSION + \
            u'PyQt4: %s\n' % Qt.PYQT_VERSION_STR + \
            u'QtWebkit: %s\n' % WEBKIT_VERSION + \
            u'SQLAlchemy: %s\n' % sqlalchemy.__version__ + \
            u'SQLAlchemy Migrate: %s\n' % MIGRATE_VERSION + \
            u'BeautifulSoup: %s\n' % BeautifulSoup.__version__ + \
            u'lxml: %s\n' % etree.__version__ + \
            u'Chardet: %s\n' % CHARDET_VERSION + \
            u'PyEnchant: %s\n' % ENCHANT_VERSION + \
            u'PySQLite: %s\n' % SQLITE_VERSION + \
            u'Mako: %s\n' % MAKO_VERSION + \
            u'pyUNO bridge: %s\n' % UNO_VERSION
        if platform.system() == u'Linux':
            if os.environ.get(u'KDE_FULL_SESSION') == u'true':
                system += u'Desktop: KDE SC\n'
            elif os.environ.get(u'GNOME_DESKTOP_SESSION_ID'):
                system += u'Desktop: GNOME\n'
        return (openlp_version, description, traceback, system, libraries)

    def onSaveReportButtonClicked(self):
        """
        Saving exception log and system information to a file.
        """
        report_text = translate('OpenLP.ExceptionForm',
            '**OpenLP Bug Report**\n'
            'Version: %s\n\n'
            '--- Details of the Exception. ---\n\n%s\n\n '
            '--- Exception Traceback ---\n%s\n'
            '--- System information ---\n%s\n'
            '--- Library Versions ---\n%s\n')
        filename = QtGui.QFileDialog.getSaveFileName(self,
            translate('OpenLP.ExceptionForm', 'Save Crash Report'),
            Settings().value(self.settingsSection + u'/last directory'),
            translate('OpenLP.ExceptionForm',
            'Text files (*.txt *.log *.text)'))
        if filename:
            filename = unicode(filename).replace(u'/', os.path.sep)
            Settings().setValue(self.settingsSection + u'/last directory', os.path.dirname(filename))
            report_text = report_text % self._createReport()
            try:
                report_file = open(filename, u'w')
                try:
                    report_file.write(report_text)
                except UnicodeError:
                    report_file.close()
                    report_file = open(filename, u'wb')
                    report_file.write(report_text.encode(u'utf-8'))
                finally:
                    report_file.close()
            except IOError:
                log.exception(u'Failed to write crash report')
            finally:
                report_file.close()

    def onSendReportButtonClicked(self):
        """
        Opening systems default email client and inserting exception log and
        system informations.
        """
        body = translate('OpenLP.ExceptionForm',
            '*OpenLP Bug Report*\n'
            'Version: %s\n\n'
            '--- Details of the Exception. ---\n\n%s\n\n '
            '--- Exception Traceback ---\n%s\n'
            '--- System information ---\n%s\n'
            '--- Library Versions ---\n%s\n',
            'Please add the information that bug reports are favoured written '
            'in English.')
        content = self._createReport()
        source = u''
        exception = u''
        for line in content[2].split(u'\n'):
            if re.search(r'[/\\]openlp[/\\]', line):
                source = re.sub(r'.*[/\\]openlp[/\\](.*)".*', r'\1', line)
            if u':' in line:
                exception = line.split(u'\n')[-1].split(u':')[0]
        subject = u'Bug report: %s in %s' % (exception, source)
        mailto_url = QtCore.QUrl(u'mailto:bugs@openlp.org')
        mailto_url.addQueryItem(u'subject', subject)
        mailto_url.addQueryItem(u'body', body % content)
        if self.fileAttachment:
            mailto_url.addQueryItem(u'attach', self.fileAttachment)
        QtGui.QDesktopServices.openUrl(mailto_url)

    def onDescriptionUpdated(self):
        """
        Update the minimum number of characters needed in the description.
        """
        count = int(20 - len(self.descriptionTextEdit.toPlainText()))
        if count < 0:
            count = 0
            self.__buttonState(True)
        else:
            self.__buttonState(False)
        self.descriptionWordCount.setText(
            translate('OpenLP.ExceptionDialog', 'Description characters to enter : %s') % count)

    def onAttachFileButtonClicked(self):
        """
        Attache files to the bug report e-mail.
        """
        files = QtGui.QFileDialog.getOpenFileName(
            self, translate('ImagePlugin.ExceptionDialog', 'Select Attachment'),
                Settings().value(self.settingsSection + u'/last directory'), u'%s (*.*) (*)' % UiStrings().AllFiles)
        log.info(u'New files(s) %s', unicode(files))
        if files:
            self.fileAttachment = unicode(files)

    def __buttonState(self, state):
        """
        Toggle the button state.
        """
        self.saveReportButton.setEnabled(state)
        self.sendReportButton.setEnabled(state)
