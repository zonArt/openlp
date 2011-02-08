# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
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
"""
The :mod:`songexportform` module provides the wizard for exporting songs to the
OpenLyrics format.
"""
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import build_icon, Receiver, SettingsManager, translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui.wizard import OpenLPWizard
from openlp.plugins.songs.lib.db import Song
from openlp.plugins.songs.lib.openlyricsexport import OpenLyricsExport

log = logging.getLogger(__name__)

class SongExportForm(OpenLPWizard):
    """
    This is the Song Export Wizard, which allows easy exporting of Songs to the
    OpenLyrics format.
    """
    log.info(u'SongExportForm loaded')

    def __init__(self, parent, plugin):
        """
        Instantiate the wizard, and run any extra setup we need to.

        ``parent``
            The QWidget-derived parent of the wizard.

        ``plugin``
            The songs plugin.
        """
        self.plugin = plugin
        OpenLPWizard.__init__(self, parent, plugin, u'songExportWizard',
            u':/wizards/wizard_exportsong.bmp')
        self.stop_export_flag = False
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_stop_wizard'), self.stop_export)

    def stop_export(self):
        """
        Sets the flag for the exporter to stop the export.
        """
        log.debug(u'Stopping songs export')
        self.stop_export_flag = True

    def setupUi(self, image):
        """
        Set up the song wizard UI.
        """
        OpenLPWizard.setupUi(self, image)

    def customInit(self):
        """
        Song wizard specific initialisation.
        """
        pass

    def customSignals(self):
        """
        Song wizard specific signals.
        """
        QtCore.QObject.connect(self.directoryButton,
            QtCore.SIGNAL(u'clicked()'), self.onDirectoryButtonClicked)
#        QtCore.QObject.connect(self.searchLineEdit,
#            QtCore.SIGNAL(u'textEdited(const QString&)'),
#            self.onSearchLineEditChanged)

    def addCustomPages(self):
        """
        Add song wizard specific pages.
        """
        # The page with all available songs.
        self.availableSongsPage = QtGui.QWizardPage()
        self.availableSongsPage.setObjectName(u'availableSongsPage')
        self.availableSongsLayout = QtGui.QHBoxLayout(self.availableSongsPage)
        self.availableSongsLayout.setObjectName(u'availableSongsLayout')
#        self.gridLayout = QtGui.QGridLayout()
#        self.gridLayout.setObjectName(u'gridLayout')
        self.availableListWidget = QtGui.QListWidget(self.availableSongsPage)
        self.availableListWidget.setObjectName(u'availableListWidget')
#        self.gridLayout.addWidget(self.availableListWidget, 0, 0, 1, 1)
#        self.searchLineEdit = QtGui.QLineEdit(self.availableSongsPage)
#        self.searchLineEdit.setObjectName(u'searchLineEdit')
#        self.gridLayout.addWidget(self.searchLineEdit, 1, 0, 1, 1)
#        self.availableSongsLayout.addLayout(self.gridLayout)
        self.availableSongsLayout.addWidget(self.availableListWidget)
        self.addPage(self.availableSongsPage)
        # The page with the selected songs.
        self.exportSongPage = QtGui.QWizardPage()
        self.exportSongPage.setObjectName(u'availableSongsPage')
        self.exportSongLayout = QtGui.QHBoxLayout(self.exportSongPage)
        self.exportSongLayout.setObjectName(u'exportSongLayout')
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(u'gridLayout')
        self.selectedListWidget = QtGui.QListWidget(self.exportSongPage)
        self.selectedListWidget.setObjectName(u'selectedListWidget')
        self.gridLayout.addWidget(self.selectedListWidget, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.directoryLabel = QtGui.QLabel(self.exportSongPage)
        self.directoryLabel.setObjectName(u'directoryLabel')
        self.horizontalLayout.addWidget(self.directoryLabel)
        self.directoryLineEdit = QtGui.QLineEdit(self.exportSongPage)
        self.directoryLineEdit.setObjectName(u'directoryLineEdit')
        self.horizontalLayout.addWidget(self.directoryLineEdit)
        self.directoryButton = QtGui.QToolButton(self.exportSongPage)
        self.directoryButton.setIcon(build_icon(u':/exports/export_load.png'))
        self.directoryButton.setObjectName(u'directoryButton')
        self.horizontalLayout.addWidget(self.directoryButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.exportSongLayout.addLayout(self.gridLayout)
        self.addPage(self.exportSongPage)

    def retranslateUi(self):
        """
        Song wizard localisation.
        """
        self.setWindowTitle(
            translate('SongsPlugin.ExportWizardForm', 'Song Export Wizard'))
        self.titleLabel.setText(
            u'<span style="font-size:14pt; font-weight:600;">%s</span>' % \
            translate('SongsPlugin.ExportWizardForm',
            'Welcome to the Song Export Wizard'))
        self.informationLabel.setText(
            translate('SongsPlugin.ExportWizardForm', 'This wizard will help to '
            'export your songs to the open and free OpenLyrics worship song '
            'format.'))
        self.availableSongsPage.setTitle(
            translate('SongsPlugin.ExportWizardForm', 'Select Songs'))
        self.availableSongsPage.setSubTitle(
            translate('SongsPlugin.ExportWizardForm',
            'Check the songs, you want to export.'))
        self.exportSongPage.setTitle(
                translate('SongsPlugin.ExportWizardForm', 'Select Directory'))
        self.exportSongPage.setSubTitle(
                translate('SongsPlugin.ExportWizardForm',
                'Select the directory you want the songs to be saved.'))
        self.directoryLabel.setText(
            translate('SongsPlugin.ExportWizardForm', 'Directory:'))
        self.progressPage.setTitle(
            translate('SongsPlugin.ExportWizardForm', 'Exporting'))
        self.progressPage.setSubTitle(
            translate('SongsPlugin.ExportWizardForm',
            'Please wait while your songs are exported.'))
        self.progressLabel.setText(
            translate('SongsPlugin.ExportWizardForm', 'Ready.'))
        self.progressBar.setFormat(
            translate('SongsPlugin.ExportWizardForm', '%p%'))

    def validateCurrentPage(self):
        """
        Validate the current page before moving on to the next page.
        """
        if self.currentPage() == self.welcomePage:
            return True
        elif self.currentPage() == self.availableSongsPage:
            items = [item for item in self.availableListWidget.findItems(
                QtCore.QString(u''), QtCore.Qt.MatchContains)
                if item.checkState() == QtCore.Qt.Checked]
            if not items:
                critical_error_message_box(
                    translate('SongsPlugin.ExportWizardForm',
                    'No Song Selected'),
                    translate('SongsPlugin.ExportWizardForm',
                    'You need to add at least one Song to export.'))
                return False
            self.selectedListWidget.clear()
            # Add the songs to the list of selected songs.
            for item in items:
                song = QtGui.QListWidgetItem(item.text())
                song.setData(QtCore.Qt.UserRole,
                    QtCore.QVariant(item.data(QtCore.Qt.UserRole).toPyObject()))
                song.setFlags(QtCore.Qt.ItemIsEnabled)
                self.selectedListWidget.addItem(song)
            return True
        elif self.currentPage() == self.exportSongPage:
            if not self.directoryLineEdit.text():
                critical_error_message_box(
                    translate('SongsPlugin.ExportWizardForm',
                    'No Save Location specified'),
                    translate('SongsPlugin.ExportWizardForm',
                    'You need to specified a directory to save the songs in.'))
                return False
            return True
        elif self.currentPage() == self.progressPage:
            self.availableListWidget.clear()
            self.selectedListWidget.clear()
            return True

    def registerFields(self):
        """
        Register song export wizard fields.
        """
        pass

    def setDefaults(self):
        """
        Set default form values for the song export wizard.
        """
        self.restart()
        self.finishButton.setVisible(False)
        self.cancelButton.setVisible(True)
        self.availableListWidget.clear()
        self.selectedListWidget.clear()
        self.directoryLineEdit.clear()
        # Load the list of songs.
        Receiver.send_message(u'cursor_busy')
        songs = self.plugin.manager.get_all_objects(Song)
        for song in songs:
            authors = u', '.join([author.display_name
                for author in song.authors])
            title = u'%s (%s)' % (unicode(song.title), authors)
            item = QtGui.QListWidgetItem(title)
            item.setData(QtCore.Qt.UserRole, QtCore.QVariant(song))
            item.setFlags(QtCore.Qt.ItemIsSelectable|
                QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Checked)
            self.availableListWidget.addItem(item)
        Receiver.send_message(u'cursor_normal')

    def preWizard(self):
        """
        Perform pre export tasks.
        """
        OpenLPWizard.preWizard(self)
        self.progressLabel.setText(
            translate('SongsPlugin.ExportWizardForm', 'Starting export...'))
        Receiver.send_message(u'openlp_process_events')

    def performWizard(self):
        """
        Perform the actual export. This creates an *openlyricsexport* instance
        and calls the *do_export* method.
        """
        songs = [song.data(QtCore.Qt.UserRole).toPyObject()
            for song in self.selectedListWidget.findItems(
            QtCore.QString(u''), QtCore.Qt.MatchContains)]
        exporter = OpenLyricsExport(
            self, songs, unicode(self.directoryLineEdit.text()))
        if exporter.do_export():
            self.progressLabel.setText(
                translate('SongsPlugin.SongExportForm', 'Finished export.'))
        else:
            self.progressLabel.setText(
                translate('SongsPlugin.SongExportForm',
                'Your song export failed.'))

#    def onSearchLineEditChanged(self, text):
#        pass

    def onDirectoryButtonClicked(self):
        """
        Called when the *directoryButton* was clicked. Opens a dialog and writes
        the path to *directoryLineEdit*.
        """
        path = unicode(QtGui.QFileDialog.getExistingDirectory(self,
            translate('SongsPlugin.ExportWizardForm', 'Selecte to Folder'),
            SettingsManager.get_last_dir(self.plugin.settingsSection, 1),
            options=QtGui.QFileDialog.ShowDirsOnly))
        SettingsManager.set_last_dir(self.plugin.settingsSection, path, 1)
        self.directoryLineEdit.setText(path)
