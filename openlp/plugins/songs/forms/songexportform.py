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
The song export function for OpenLP.
"""
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, translate
from openlp.core.ui import criticalErrorMessageBox
from openlp.core.ui.wizard import OpenLPWizard
from openlp.plugins.songs.lib.db import Song
from openlp.plugins.songs.lib.openlyricsexport import OpenLyricsExport

log = logging.getLogger(__name__)

class SongExportForm(OpenLPWizard):
    """
    This is the Song Export Wizard, which allows easy exporting of Songs to
    OpenLyrics.
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
            u':/wizards/wizard_importsong.bmp')
        self.stop_export_flag = False
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_stop_wizard'), self.stop_export)

    def stop_export(self):
        """
        Sets the flag for exporters to stop their export
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
        QtCore.QObject.connect(self.addSelected,
            QtCore.SIGNAL(u'clicked()'), self.onAddSelectedClicked)
        QtCore.QObject.connect(self.removeSelected,
            QtCore.SIGNAL(u'clicked()'), self.onRemoveSelectedClicked)
        QtCore.QObject.connect(self.availableListWidget,
            QtCore.SIGNAL(u'itemDoubleClicked(QListWidgetItem *)'),
            self.onAvailableListItemDoubleClicked)
        QtCore.QObject.connect(self.selectedListWidget,
            QtCore.SIGNAL(u'itemDoubleClicked(QListWidgetItem *)'),
            self.onSelectedListItemDoubleClicked)

    def addCustomPages(self):
        """
        Add song wizard specific pages.
        """
        # Source Page
        self.sourcePage = QtGui.QWizardPage()
        self.sourcePage.setObjectName(u'sourcePage')
        self.sourceLayout = QtGui.QHBoxLayout(self.sourcePage)
        self.sourceLayout.setObjectName(u'sourceLayout')
        self.availableGroupBox = QtGui.QGroupBox(self.sourcePage)
        self.availableGroupBox.setObjectName(u'availableGroupBox')
        self.verticalLayout = QtGui.QVBoxLayout(self.availableGroupBox)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.verticalLayout.setContentsMargins(0, -1, 0, 0)
        self.availableListWidget = QtGui.QListWidget(self.availableGroupBox)
        self.availableListWidget.setObjectName(u'availableListWidget')
        self.availableListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.availableListWidget.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.availableListWidget.setSortingEnabled(True)
        self.verticalLayout.addWidget(self.availableListWidget)
        self.sourceLayout.addWidget(self.availableGroupBox)
        self.selectionWidget = QtGui.QWidget(self.sourcePage)
        self.selectionWidget.setObjectName(u'selectionWidget')
        self.selectionLayout = QtGui.QVBoxLayout(self.selectionWidget)
        self.selectionLayout.setSpacing(0)
        self.selectionLayout.setMargin(0)
        self.selectionLayout.setObjectName(u'selectionLayout')
        self.addSelected = QtGui.QToolButton(self.selectionWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            u':/exports/export_move_to_list.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addSelected.setIcon(icon)
        self.addSelected.setIconSize(QtCore.QSize(20, 20))
        self.addSelected.setObjectName(u'addSelected')
        self.selectionLayout.addWidget(self.addSelected)
        self.removeSelected = QtGui.QToolButton(self.selectionWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            u':/imports/import_remove.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeSelected.setIcon(icon)
        self.removeSelected.setIconSize(QtCore.QSize(20, 20))
        self.removeSelected.setObjectName(u'removeSelected')
        self.selectionLayout.addWidget(self.removeSelected)
        self.sourceLayout.addWidget(self.selectionWidget)
        self.selectedGroupBox = QtGui.QGroupBox(self.sourcePage)
        self.selectedGroupBox.setObjectName(u'selectedGroupBox')
        self.verticalLayout = QtGui.QVBoxLayout(self.selectedGroupBox)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.verticalLayout.setContentsMargins(0, -1, 0, 0)
        self.selectedListWidget = QtGui.QListWidget(self.selectedGroupBox)
        self.selectedListWidget.setObjectName(u'selectedListWidget')
        self.selectedListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.selectedListWidget.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.selectedListWidget.setSortingEnabled(True)
        self.verticalLayout.addWidget(self.selectedListWidget)
        self.sourceLayout.addWidget(self.selectedGroupBox)
        self.addPage(self.sourcePage)
        #TODO: Add save dialog and maybe a search box.

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
            'export your songs to the free and open OpenLyrics worship song '
            'format. You can import these songs in all lyrics projection '
            'software, which supports OpenLyrics.'))
        self.sourcePage.setTitle(
            translate('SongsPlugin.ExportWizardForm', 'Select Songs'))
        self.sourcePage.setSubTitle(
            translate('SongsPlugin.ExportWizardForm',
            'Select the songs, you want to export.'))

        self.progressPage.setTitle(
            translate('SongsPlugin.ExportWizardForm', 'Exporting'))
        self.progressPage.setSubTitle(
            translate('SongsPlugin.ExportWizardForm',
            'Please wait while your songs are exported.'))
        self.progressLabel.setText(
            translate('SongsPlugin.ExportWizardForm', 'Ready.'))
        self.progressBar.setFormat(
            translate('SongsPlugin.ExportWizardForm', '%p%'))

        self.availableGroupBox.setTitle(
            translate('SongsPlugin.ExportWizardForm', 'Available Songs'))
        self.addSelected.setText(
            translate('SongsPlugin.ExportWizardForm', 'Select Songs'))
        self.removeSelected.setText(
            translate('SongsPlugin.ExportWizardForm', 'Select Songs'))
        self.selectedGroupBox.setTitle(
            translate('SongsPlugin.ExportWizardForm', 'Selected Songs'))

    def validateCurrentPage(self):
        """
        Validate the current page before moving on to the next page.
        """
        if self.currentPage() == self.welcomePage:
            Receiver.send_message(u'cursor_busy')
            songs = self.plugin.manager.get_all_objects(Song)
            for song in songs:
                author_list = u''
                for author in song.authors:
                    if author_list != u'':
                        author_list = author_list + u', '
                    author_list = author_list + author.display_name
                song_title = unicode(song.title)
                song_detail = u'%s (%s)' % (song_title, author_list)
                song_name = QtGui.QListWidgetItem(song_detail)
                song_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(song))
                self.availableListWidget.addItem(song_name)
            self.availableListWidget.selectAll()
            Receiver.send_message(u'cursor_normal')
            return True
        elif self.currentPage() == self.sourcePage:
            self.selectedListWidget.selectAll()
            if not self.selectedListWidget.selectedItems():
                criticalErrorMessageBox(
                    translate('SongsPlugin.ExportWizardForm',
                    'No Song Selected'),
                    translate('SongsPlugin.ImportWizardForm',
                    'You need to add at least one Song to export.'))
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

    def preWizard(self):
        """
        Perform pre export tasks
        """
        OpenLPWizard.preWizard(self)
        self.progressLabel.setText(
            translate('SongsPlugin.ExportWizardForm', 'Starting export...'))
        Receiver.send_message(u'openlp_process_events')

    def performWizard(self):
        """
        Perform the actual export. This method pulls in the correct exporter
        class, and then runs the ``do_export`` method of the exporter to do
        the actual exporting.
        """
        songs = [item.data(QtCore.Qt.UserRole).toPyObject()
            for item in self.selectedListWidget.selectedItems()]
        exporter = OpenLyricsExport(self, songs, u'/tmp/')
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
