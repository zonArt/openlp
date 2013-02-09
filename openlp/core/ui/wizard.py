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
The :mod:``wizard`` module provides generic wizard tools for OpenLP.
"""
import logging
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, Registry, Settings, UiStrings, build_icon, translate
from openlp.core.lib.ui import add_welcome_page

log = logging.getLogger(__name__)


class WizardStrings(object):
    """
    Provide standard strings for wizards to use.
    """
    # Applications/Formats we import from or export to. These get used in
    # multiple places but do not need translating unless you find evidence of
    # the writers translating their own product name.
    CSV = u'CSV'
    OS = u'OpenSong'
    OSIS = u'OSIS'
    # These strings should need a good reason to be retranslated elsewhere.
    FinishedImport = translate('OpenLP.Ui', 'Finished import.')
    FormatLabel = translate('OpenLP.Ui', 'Format:')
    HeaderStyle = u'<span style="font-size:14pt; font-weight:600;">%s</span>'
    Importing = translate('OpenLP.Ui', 'Importing')
    ImportingType = translate('OpenLP.Ui', 'Importing "%s"...')
    ImportSelect = translate('OpenLP.Ui', 'Select Import Source')
    ImportSelectLong = translate('OpenLP.Ui',
        'Select the import format and the location to import from.')
    NoSqlite = translate('OpenLP.Ui', 'The openlp.org 1.x importer has been '
        'disabled due to a missing Python module. If you want to use this '
        'importer, you will need to install the "python-sqlite" module.')
    OpenTypeFile = translate('OpenLP.Ui', 'Open %s File')
    OpenTypeFolder = translate('OpenLP.Ui', 'Open %s Folder')
    PercentSymbolFormat = translate('OpenLP.Ui', '%p%')
    Ready = translate('OpenLP.Ui', 'Ready.')
    StartingImport = translate('OpenLP.Ui', 'Starting import...')
    YouSpecifyFile = translate('OpenLP.Ui', 'You need to specify one '
        '%s file to import from.', 'A file type e.g. OpenSong')
    YouSpecifyFiles = translate('OpenLP.Ui', 'You need to specify at '
        'least one %s file to import from.', 'A file type e.g. OpenSong')
    YouSpecifyFolder = translate('OpenLP.Ui', 'You need to specify one '
        '%s folder to import from.', 'A song format e.g. PowerSong')


class OpenLPWizard(QtGui.QWizard):
    """
    Generic OpenLP wizard to provide generic functionality and a unified look
    and feel.
    """
    def __init__(self, parent, plugin, name, image):
        """
        Constructor
        """
        QtGui.QWizard.__init__(self, parent)
        self.plugin = plugin
        self.setObjectName(name)
        self.openIcon = build_icon(u':/general/general_open.png')
        self.deleteIcon = build_icon(u':/general/general_delete.png')
        self.finishButton = self.button(QtGui.QWizard.FinishButton)
        self.cancelButton = self.button(QtGui.QWizard.CancelButton)
        self.setupUi(image)
        self.registerFields()
        self.customInit()
        self.customSignals()
        QtCore.QObject.connect(self, QtCore.SIGNAL(u'currentIdChanged(int)'), self.onCurrentIdChanged)
        QtCore.QObject.connect(self.errorCopyToButton, QtCore.SIGNAL(u'clicked()'), self.onErrorCopyToButtonClicked)
        QtCore.QObject.connect(self.errorSaveToButton, QtCore.SIGNAL(u'clicked()'), self.onErrorSaveToButtonClicked)

    def setupUi(self, image):
        """
        Set up the wizard UI.
        """
        self.setModal(True)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.setOptions(QtGui.QWizard.IndependentPages |
            QtGui.QWizard.NoBackButtonOnStartPage |
            QtGui.QWizard.NoBackButtonOnLastPage)
        add_welcome_page(self, image)
        self.addCustomPages()
        self.addProgressPage()
        self.retranslateUi()

    def registerFields(self):
        """
        Hook method for wizards to register any fields they need.
        """
        pass

    def addProgressPage(self):
        """
        Add the progress page for the wizard. This page informs the user how
        the wizard is progressing with its task.
        """
        self.progressPage = QtGui.QWizardPage()
        self.progressPage.setObjectName(u'progressPage')
        self.progressLayout = QtGui.QVBoxLayout(self.progressPage)
        self.progressLayout.setMargin(48)
        self.progressLayout.setObjectName(u'progressLayout')
        self.progressLabel = QtGui.QLabel(self.progressPage)
        self.progressLabel.setObjectName(u'progressLabel')
        self.progressLabel.setWordWrap(True)
        self.progressLayout.addWidget(self.progressLabel)
        self.progressBar = QtGui.QProgressBar(self.progressPage)
        self.progressBar.setObjectName(u'progressBar')
        self.progressLayout.addWidget(self.progressBar)
        # Add a QTextEdit and a copy to file and copy to clipboard button to be
        # able to provide feedback to the user. Hidden by default.
        self.errorReportTextEdit = QtGui.QTextEdit(self.progressPage)
        self.errorReportTextEdit.setObjectName(u'progresserrorReportTextEdit')
        self.errorReportTextEdit.setHidden(True)
        self.errorReportTextEdit.setReadOnly(True)
        self.progressLayout.addWidget(self.errorReportTextEdit)
        self.errorButtonLayout = QtGui.QHBoxLayout()
        self.errorButtonLayout.setObjectName(u'errorButtonLayout')
        spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.errorButtonLayout.addItem(spacer)
        self.errorCopyToButton = QtGui.QPushButton(self.progressPage)
        self.errorCopyToButton.setObjectName(u'errorCopyToButton')
        self.errorCopyToButton.setHidden(True)
        self.errorCopyToButton.setIcon(build_icon(u':/system/system_edit_copy.png'))
        self.errorButtonLayout.addWidget(self.errorCopyToButton)
        self.errorSaveToButton = QtGui.QPushButton(self.progressPage)
        self.errorSaveToButton.setObjectName(u'errorSaveToButton')
        self.errorSaveToButton.setHidden(True)
        self.errorSaveToButton.setIcon(build_icon(u':/general/general_save.png'))
        self.errorButtonLayout.addWidget(self.errorSaveToButton)
        self.progressLayout.addLayout(self.errorButtonLayout)
        self.addPage(self.progressPage)

    def exec_(self):
        """
        Run the wizard.
        """
        self.setDefaults()
        return QtGui.QWizard.exec_(self)

    def reject(self):
        """
        Stop the wizard on cancel button, close button or ESC key.
        """
        log.debug(u'Wizard cancelled by user.')
        if self.currentPage() == self.progressPage:
            Receiver.send_message(u'openlp_stop_wizard')
        self.done(QtGui.QDialog.Rejected)

    def onCurrentIdChanged(self, pageId):
        """
        Perform necessary functions depending on which wizard page is active.
        """
        if self.page(pageId) == self.progressPage:
            self.preWizard()
            self.performWizard()
            self.postWizard()
        else:
            self.customPageChanged(pageId)

    def customPageChanged(self, pageId):
        """
        Called when changing to a page other than the progress page
        """
        pass

    def onErrorCopyToButtonClicked(self):
        """
        Called when the ``onErrorCopyToButtonClicked`` has been clicked.
        """
        pass

    def onErrorSaveToButtonClicked(self):
        """
        Called when the ``onErrorSaveToButtonClicked`` has been clicked.
        """
        pass

    def incrementProgressBar(self, status_text, increment=1):
        """
        Update the wizard progress page.

        ``status_text``
            Current status information to display.

        ``increment``
            The value to increment the progress bar by.
        """
        log.debug(u'IncrementBar %s', status_text)
        self.progressLabel.setText(status_text)
        if increment > 0:
            self.progressBar.setValue(self.progressBar.value() + increment)
        self.application.process_events()

    def preWizard(self):
        """
        Prepare the UI for the import.
        """
        self.finishButton.setVisible(False)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(1188)
        self.progressBar.setValue(0)

    def postWizard(self):
        """
        Clean up the UI after the import has finished.
        """
        self.progressBar.setValue(self.progressBar.maximum())
        self.finishButton.setVisible(True)
        self.cancelButton.setVisible(False)
        self.application.process_events()

    def getFileName(self, title, editbox, setting_name, filters=u''):
        """
        Opens a QFileDialog and saves the filename to the given editbox.

        ``title``
            The title of the dialog (unicode).

        ``editbox``
            An editbox (QLineEdit).

        ``setting_name``
            The place where to save the last opened directory.

        ``filters``
            The file extension filters. It should contain the file description
            as well as the file extension. For example::

                u'OpenLP 2.0 Databases (*.sqlite)'
        """
        if filters:
            filters += u';;'
        filters += u'%s (*)' % UiStrings().AllFiles
        filename = QtGui.QFileDialog.getOpenFileName(self, title,
            os.path.dirname(Settings().value(self.plugin.settingsSection + u'/' + setting_name)), filters)
        if filename:
            editbox.setText(filename)
        Settings().setValue(self.plugin.settingsSection + u'/' + setting_name, filename)

    def getFolder(self, title, editbox, setting_name):
        """
        Opens a QFileDialog and saves the selected folder to the given editbox.

        ``title``
            The title of the dialog (unicode).

        ``editbox``
            An editbox (QLineEdit).

        ``setting_name``
            The place where to save the last opened directory.
        """
        folder = QtGui.QFileDialog.getExistingDirectory(self, title,
            Settings().value(self.plugin.settingsSection + u'/' + setting_name),
            QtGui.QFileDialog.ShowDirsOnly)
        if folder:
            editbox.setText(folder)
        Settings().setValue(self.plugin.settingsSection + u'/' + setting_name, folder)

    def _get_application(self):
        """
        Adds the openlp to the class dynamically
        """
        if not hasattr(self, u'_application'):
            self._application = Registry().get(u'application')
        return self._application

    application = property(_get_application)
