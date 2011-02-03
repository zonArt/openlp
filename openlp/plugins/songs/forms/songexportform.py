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

from openlp.core.lib import Receiver, SettingsManager, translate
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
        QtCore.QObject.connect(self.addButton,
            QtCore.SIGNAL(u'clicked()'), self.onAddSelectedClicked)
        QtCore.QObject.connect(self.removeButton,
            QtCore.SIGNAL(u'clicked()'), self.onRemoveSelectedClicked)
        QtCore.QObject.connect(self.availableListWidget,
            QtCore.SIGNAL(u'itemDoubleClicked(QListWidgetItem *)'),
            self.onAvailableListItemDoubleClicked)
        QtCore.QObject.connect(self.selectedListWidget,
            QtCore.SIGNAL(u'itemDoubleClicked(QListWidgetItem *)'),
            self.onSelectedListItemDoubleClicked)
        QtCore.QObject.connect(self.directoryButton,
            QtCore.SIGNAL(u'clicked()'), self.onDirectoryButtonClicked)
        QtCore.QObject.connect(self.allAvailableButton,
            QtCore.SIGNAL(u'clicked()'), self.onAllAvailableButtonClicked)
        QtCore.QObject.connect(self.allSelectedButton,
            QtCore.SIGNAL(u'clicked()'), self.onAllSelectedButtonClicked)

    def addCustomPages(self):
        """
        Add song wizard specific pages.
        """
        # Source Page
        self.sourcePage = QtGui.QWizardPage()
        self.sourcePage.setObjectName(u'sourcePage')
        self.horizontalLayout = QtGui.QHBoxLayout(self.sourcePage)
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(u'gridLayout')
        self.selectedListWidget = QtGui.QListWidget(self.sourcePage)
        self.selectedListWidget.setObjectName(u'selectedListWidget')
        self.selectedListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.selectedListWidget.setSortingEnabled(True)
        self.gridLayout.addWidget(self.selectedListWidget, 1, 2, 1, 1)
        self.gridLayout2 = QtGui.QGridLayout()
        self.gridLayout2.setObjectName(u'gridLayout2')
        self.addButton = QtGui.QToolButton(self.sourcePage)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/exports/export_move_to_list.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(icon)
        self.addButton.setObjectName(u'addButton')
        self.gridLayout2.addWidget(self.addButton, 1, 0, 1, 1)
        self.removeButton = QtGui.QToolButton(self.sourcePage)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/exports/export_remove.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeButton.setIcon(icon)
        self.removeButton.setObjectName(u'removeButton')
        self.gridLayout2.addWidget(self.removeButton, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout2.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout2.addItem(spacerItem, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout2, 1, 1, 1, 1)
        self.availableLabel = QtGui.QLabel(self.sourcePage)
        self.availableLabel.setObjectName(u'availableLabel')
        self.gridLayout.addWidget(self.availableLabel, 0, 0, 1, 1)
        self.selectedLabel = QtGui.QLabel(self.sourcePage)
        self.selectedLabel.setObjectName(u'selectedLabel')
        self.gridLayout.addWidget(self.selectedLabel, 0, 2, 1, 1)
        self.availableListWidget = QtGui.QListWidget(self.sourcePage)
        self.availableListWidget.setObjectName(u'availableListWidget')
        self.availableListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.availableListWidget.setSortingEnabled(True)
        self.gridLayout.addWidget(self.availableListWidget, 1, 0, 1, 1)
        # Button to select all songs in the "selectedListWidget".
        self.allSelectedButton = QtGui.QToolButton(self.sourcePage)
        self.allSelectedButton.setObjectName(u'allSelectedButton')
        self.gridLayout.addWidget(self.allSelectedButton, 3, 2, 1, 1)
        # Button to select all songs in the "availableListWidget".
        self.allAvailableButton = QtGui.QToolButton(self.sourcePage)
        self.allAvailableButton.setObjectName(u'allAvailableButton')
        self.gridLayout.addWidget(self.allAvailableButton, 3, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.gridLayout3 = QtGui.QGridLayout()
        self.gridLayout3.setObjectName(u'gridLayout3')
        self.directoryButton = QtGui.QToolButton(self.sourcePage)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/exports/export_load.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.directoryButton.setIcon(icon)
        self.directoryButton.setObjectName(u'directoryButton')
        self.gridLayout3.addWidget(self.directoryButton, 0, 2, 1, 1)
        self.directoryLineEdit = QtGui.QLineEdit(self.sourcePage)
        self.directoryLineEdit.setObjectName(u'directoryLineEdit')
        self.gridLayout3.addWidget(self.directoryLineEdit, 0, 1, 1, 1)
        self.directoryLabel = QtGui.QLabel(self.sourcePage)
        self.directoryLabel.setObjectName(u'directoryLabel')
        self.gridLayout3.addWidget(self.directoryLabel, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.addPage(self.sourcePage)

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
        self.sourcePage.setTitle(
            translate('SongsPlugin.ExportWizardForm', 'Select Songs'))
        self.sourcePage.setSubTitle(
            translate('SongsPlugin.ExportWizardForm',
            'Add the songs, you want to export to the list on the right hand '
            'side. You can use the buttons below or double click them.'))
        self.progressPage.setTitle(
            translate('SongsPlugin.ExportWizardForm', 'Exporting'))
        self.progressPage.setSubTitle(
            translate('SongsPlugin.ExportWizardForm',
            'Please wait while your songs are exported.'))
        self.progressLabel.setText(
            translate('SongsPlugin.ExportWizardForm', 'Ready.'))
        self.progressBar.setFormat(
            translate('SongsPlugin.ExportWizardForm', '%p%'))
        self.directoryLabel.setText(translate('SongsPlugin.ExportWizardForm',
            'Directory:'))
        self.availableLabel.setText(
            translate('SongsPlugin.ExportWizardForm', '<b>Available Songs</b>'))
        self.selectedLabel.setText(
            translate('SongsPlugin.ExportWizardForm', '<b>Selected Songs</b>'))
        self.allSelectedButton.setText(
            translate('SongsPlugin.ExportWizardForm', 'Select all'))
        self.allAvailableButton.setText(
            translate('SongsPlugin.ExportWizardForm', 'Select all'))

    def validateCurrentPage(self):
        """
        Validate the current page before moving on to the next page.
        """
        if self.currentPage() == self.welcomePage:
            return True
        elif self.currentPage() == self.sourcePage:
            if not self.selectedListWidget.count():
                critical_error_message_box(
                    translate('SongsPlugin.ExportWizardForm',
                    'No Song Selected'),
                    translate('SongsPlugin.ExportWizardForm',
                    'You need to add at least one Song to export.'))
                return False
            elif not self.directoryLineEdit.text():
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
            song_detail = u'%s (%s)' % (unicode(song.title), authors)
            song_name = QtGui.QListWidgetItem(song_detail)
            song_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(song))
            self.availableListWidget.addItem(song_name)
        self.availableListWidget.selectAll()
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
        self.selectedListWidget.selectAll()
        songs = [item.data(QtCore.Qt.UserRole).toPyObject()
            for item in self.selectedListWidget.selectedItems()]
        exporter = OpenLyricsExport(
            self, songs, unicode(self.directoryLineEdit.text()))
        if exporter.do_export():
            self.progressLabel.setText(
                translate('SongsPlugin.SongExportForm', 'Finished export.'))
        else:
            self.progressLabel.setText(
                translate('SongsPlugin.SongExportForm',
                'Your song export failed.'))

    def onAddSelectedClicked(self):
        """
        Removes the selected items from the list of available songs and add them
        to the list of selected songs.
        """
        items = self.availableListWidget.selectedItems()
        # Save a list with tuples which consist of the item row, and the item.
        items = [(self.availableListWidget.row(item), item) for item in items]
        items.sort(reverse=True)
        for item in items:
            self.availableListWidget.takeItem(item[0])
            self.selectedListWidget.addItem(item[1])

    def onRemoveSelectedClicked(self):
        """
        Removes the selected items from the list of selected songs and add them
        back to the list of available songs.
        """
        items = self.selectedListWidget.selectedItems()
        # Save a list with tuples which consist of the item row, and the item.
        items = [(self.selectedListWidget.row(item), item) for item in items]
        items.sort(reverse=True)
        for item in items:
            self.selectedListWidget.takeItem(item[0])
            self.availableListWidget.addItem(item[1])

    def onAvailableListItemDoubleClicked(self, item):
        """
        Adds the double clicked item to the list of selected songs and removes
        it from the list of availables songs.

        ``item``
            The *QListWidgetItem* which was double clicked.
        """
        self.availableListWidget.takeItem(self.availableListWidget.row(item))
        self.selectedListWidget.addItem(item)

    def onSelectedListItemDoubleClicked(self, item):
        """
        Adds the double clicked item back to the list of available songs and
        removes it from the list of selected songs.

        ``ìtem``
            The *QListWidgetItem* which was double clicked.
        """
        self.selectedListWidget.takeItem(self.selectedListWidget.row(item))
        self.availableListWidget.addItem(item)

    def onAllAvailableButtonClicked(self):
        """
        Selects all songs in the *availableListWidget*.
        """
        self.availableListWidget.selectAll()

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

    def onAllSelectedButtonClicked(self):
        """
        Selects all songs in the *selectedListWidget*.
        """
        self.selectedListWidget.selectAll()
