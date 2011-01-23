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
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, SettingsManager, translate
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

    def setupUi(self, image):
        """
        Set up the song wizard UI.
        """
        OpenLPWizard.setupUi(self, image)

    def customInit(self):
        """
        Song wizard specific initialisation.
        """
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

    def customSignals(self):
        """
        Song wizard specific signals.
        """
        pass

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
        self.availableListWidget = QtGui.QListWidget(self.availableGroupBox)
        self.availableListWidget.setObjectName(u'availableListWidget')
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
        self.selectedListWidget = QtGui.QListWidget(self.selectedGroupBox)
        self.selectedListWidget.setObjectName(u'selectedListWidget')
        self.verticalLayout.addWidget(self.selectedListWidget)
        self.sourceLayout.addWidget(self.selectedGroupBox)
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
            'export your songs to the free and open OpenLyrics worship song '
            'format. You can import these songs in all lyrics projection '
            'software, which supports OpenLyrics.'))
        self.sourcePage.setTitle(
            translate('SongsPlugin.ExportWizardForm', 'Select Emport Source'))
        self.sourcePage.setSubTitle(
            translate('SongsPlugin.ExportWizardForm',
            'Select the export format, and where to export from.'))

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
            return True
        elif self.currentPage() == self.sourcePage:
            return True
        elif self.currentPage() == self.progressPage:
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
        exporter = OpenLyricsExport(self.plugin.manager,
            self.plugin.manager.get_all_objects(Song), u'/tmp/')
        if exporter.do_export():
            self.progressLabel.setText(
                translate('SongsPlugin.SongExportForm', 'Finished export.'))
        else:
            self.progressLabel.setText(
                translate('SongsPlugin.SongExportForm',
                'Your song export failed.'))
