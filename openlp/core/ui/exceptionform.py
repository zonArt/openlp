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

import bs4
import sqlalchemy
from lxml import etree

from openlp.core.lib import Registry

from PyQt4 import Qt, QtCore, QtGui, QtWebKit

try:
    from PyQt4.phonon import Phonon
    PHONON_VERSION = Phonon.phononVersion()
except ImportError:
    PHONON_VERSION = '-'
try:
    import migrate
    MIGRATE_VERSION = getattr(migrate, '__version__', '< 0.7')
except ImportError:
    MIGRATE_VERSION = '-'
try:
    import chardet
    CHARDET_VERSION = chardet.__version__
except ImportError:
    CHARDET_VERSION = '-'
try:
    import enchant
    ENCHANT_VERSION = enchant.__version__
except ImportError:
    ENCHANT_VERSION = '-'
try:
    import mako
    MAKO_VERSION = mako.__version__
except ImportError:
    MAKO_VERSION = '-'
try:
    import icu
    try:
        ICU_VERSION = icu.VERSION
    except AttributeError:
        ICU_VERSION = 'OK'
except ImportError:
    ICU_VERSION = '-'
try:
    import cherrypy
    CHERRYPY_VERSION = cherrypy.__version__
except ImportError:
    CHERRYPY_VERSION = '-'

try:
    WEBKIT_VERSION = QtWebKit.qWebKitVersion()
except AttributeError:
    WEBKIT_VERSION = '-'
try:
    from openlp.core.ui.media.vlcplayer import VERSION
    VLC_VERSION = VERSION
except ImportError:
    VLC_VERSION = '-'

from openlp.core.lib import UiStrings, Settings, translate
from openlp.core.utils import get_application_version

from .exceptiondialog import Ui_ExceptionDialog

log = logging.getLogger(__name__)


class ExceptionForm(QtGui.QDialog, Ui_ExceptionDialog):
    """
    The exception dialog
    """
    def __init__(self):
        """
        Constructor.
        """
        super(ExceptionForm, self).__init__(self.main_window)
        self.setupUi(self)
        self.settings_section = 'crashreport'

    def exec_(self):
        """
        Show the dialog.
        """
        self.description_text_edit.setPlainText('')
        self.on_description_updated()
        self.file_attachment = None
        return QtGui.QDialog.exec_(self)

    def _create_report(self):
        """
        Create an exception report.
        """
        openlp_version = get_application_version()
        description = self.description_text_edit.toPlainText()
        traceback = self.exception_text_edit.toPlainText()
        system = translate('OpenLP.ExceptionForm', 'Platform: %s\n') % platform.platform()
        libraries = 'Python: %s\n' % platform.python_version() + \
            'Qt4: %s\n' % Qt.qVersion() + \
            'Phonon: %s\n' % PHONON_VERSION + \
            'PyQt4: %s\n' % Qt.PYQT_VERSION_STR + \
            'QtWebkit: %s\n' % WEBKIT_VERSION + \
            'SQLAlchemy: %s\n' % sqlalchemy.__version__ + \
            'SQLAlchemy Migrate: %s\n' % MIGRATE_VERSION + \
            'BeautifulSoup: %s\n' % bs4.__version__ + \
            'lxml: %s\n' % etree.__version__ + \
            'Chardet: %s\n' % CHARDET_VERSION + \
            'PyEnchant: %s\n' % ENCHANT_VERSION + \
            'Mako: %s\n' % MAKO_VERSION + \
            'CherryPy: %s\n' % CHERRYPY_VERSION + \
            'pyICU: %s\n' % ICU_VERSION + \
            'pyUNO bridge: %s\n' % self._pyuno_import() + \
            'VLC: %s\n' % VLC_VERSION
        if platform.system() == 'Linux':
            if os.environ.get('KDE_FULL_SESSION') == 'true':
                system += 'Desktop: KDE SC\n'
            elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                system += 'Desktop: GNOME\n'
            elif os.environ.get('DESKTOP_SESSION') == 'xfce':
                system += 'Desktop: Xfce\n'
        return (openlp_version, description, traceback, system, libraries)

    def on_save_report_button_clicked(self):
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
            Settings().value(self.settings_section + '/last directory'),
            translate('OpenLP.ExceptionForm', 'Text files (*.txt *.log *.text)'))
        if filename:
            filename = str(filename).replace('/', os.path.sep)
            Settings().setValue(self.settings_section + '/last directory', os.path.dirname(filename))
            report_text = report_text % self._create_report()
            try:
                report_file = open(filename, 'w')
                try:
                    report_file.write(report_text)
                except UnicodeError:
                    report_file.close()
                    report_file = open(filename, 'wb')
                    report_file.write(report_text.encode('utf-8'))
                finally:
                    report_file.close()
            except IOError:
                log.exception('Failed to write crash report')
            finally:
                report_file.close()

    def on_send_report_button_clicked(self):
        """
        Opening systems default email client and inserting exception log and system information.
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
        content = self._create_report()
        source = ''
        exception = ''
        for line in content[2].split('\n'):
            if re.search(r'[/\\]openlp[/\\]', line):
                source = re.sub(r'.*[/\\]openlp[/\\](.*)".*', r'\1', line)
            if ':' in line:
                exception = line.split('\n')[-1].split(':')[0]
        subject = 'Bug report: %s in %s' % (exception, source)
        mailto_url = QtCore.QUrl('mailto:bugs@openlp.org')
        mailto_url.addQueryItem('subject', subject)
        mailto_url.addQueryItem('body', body % content)
        if self.file_attachment:
            mailto_url.addQueryItem('attach', self.file_attachment)
        QtGui.QDesktopServices.openUrl(mailto_url)

    def on_description_updated(self):
        """
        Update the minimum number of characters needed in the description.
        """
        count = int(20 - len(self.description_text_edit.toPlainText()))
        if count < 0:
            count = 0
            self.__button_state(True)
        else:
            self.__button_state(False)
        self.description_word_count.setText(
            translate('OpenLP.ExceptionDialog', 'Description characters to enter : %s') % count)

    def on_attach_file_button_clicked(self):
        """
        Attache files to the bug report e-mail.
        """
        files = QtGui.QFileDialog.getOpenFileName(
            self, translate('ImagePlugin.ExceptionDialog', 'Select Attachment'),
                Settings().value(self.settings_section + '/last directory'), '%s (*.*) (*)' % UiStrings().AllFiles)
        log.info('New files(s) %s', str(files))
        if files:
            self.file_attachment = str(files)

    def __button_state(self, state):
        """
        Toggle the button state.
        """
        self.save_report_button.setEnabled(state)
        self.send_report_button.setEnabled(state)

    def _pyuno_import(self):
        """
        Added here to define only when the form is actioned. The uno interface spits out lots of exception messages
        if the import is at a file level.  If uno import is changed this could be reverted.
        This happens in other classes but there it is localised here it is across the whole system and hides real
        errors.
        """
        try:
            import uno
            arg = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
            arg.Name = 'nodepath'
            arg.Value = '/org.openoffice.Setup/Product'
            context = uno.getComponentContext()
            provider = context.ServiceManager.createInstance('com.sun.star.configuration.ConfigurationProvider')
            node = provider.createInstanceWithArguments('com.sun.star.configuration.ConfigurationAccess', (arg,))
            return node.getByName('ooSetupVersion')
        except ImportError:
            return '-'
        except:
            return '- (Possible non-standard UNO installation)'

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, '_main_window'):
            self._main_window = Registry().get('main_window')
        return self._main_window

    main_window = property(_get_main_window)
