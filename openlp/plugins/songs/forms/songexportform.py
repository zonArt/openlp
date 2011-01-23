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
            self.availableListWidget.addItem(unicode(song.id))

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
        self.sourcePage.setObjectName(u'SourcePage')
        self.sourceLayout = QtGui.QVBoxLayout(self.sourcePage)
        self.sourceLayout.setObjectName(u'SourceLayout')

        self.songListsWidget = QtGui.QWidget(self.sourcePage)
        self.songListsWidget.setGeometry(QtCore.QRect(8, 10, 541, 291))
        self.songListsWidget.setObjectName("songListsWidget")
        self.SongListsLayout = QtGui.QHBoxLayout(self.songListsWidget)
        self.SongListsLayout.setSpacing(0)
        self.SongListsLayout.setMargin(0)
        self.SongListsLayout.setObjectName("SongListsLayout")
        self.availableGroupBox = QtGui.QGroupBox(self.songListsWidget)
        self.availableGroupBox.setObjectName("availableGroupBox")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.availableGroupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.availableListWidget = QtGui.QListWidget(self.availableGroupBox)
        self.availableListWidget.setObjectName("availableListWidget")
        self.verticalLayout_5.addWidget(self.availableListWidget)
        self.SongListsLayout.addWidget(self.availableGroupBox)
        self.selectionWidget = QtGui.QWidget(self.songListsWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectionWidget.sizePolicy().hasHeightForWidth())
        self.selectionWidget.setSizePolicy(sizePolicy)
        self.selectionWidget.setMaximumSize(QtCore.QSize(30, 16777215))
        self.selectionWidget.setObjectName("selectionWidget")
        self.SelectionLayout = QtGui.QVBoxLayout(self.selectionWidget)
        self.SelectionLayout.setSpacing(0)
        self.SelectionLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.SelectionLayout.setMargin(0)
        self.SelectionLayout.setObjectName("SelectionLayout")
        self.addSelected = QtGui.QToolButton(self.selectionWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/exports/export_move_to_list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addSelected.setIcon(icon)
        self.addSelected.setIconSize(QtCore.QSize(20, 20))
        self.addSelected.setObjectName("addSelected")
        self.SelectionLayout.addWidget(self.addSelected)
        self.removeSelected = QtGui.QToolButton(self.selectionWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/imports/import_remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeSelected.setIcon(icon1)
        self.removeSelected.setIconSize(QtCore.QSize(20, 20))
        self.removeSelected.setObjectName("removeSelected")
        self.SelectionLayout.addWidget(self.removeSelected)
        self.SongListsLayout.addWidget(self.selectionWidget)
        self.selectedGroupBox = QtGui.QGroupBox(self.songListsWidget)
        self.selectedGroupBox.setObjectName("selectedGroupBox")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.selectedGroupBox)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.selectedListWidget = QtGui.QListWidget(self.selectedGroupBox)
        self.selectedListWidget.setObjectName("selectedListWidget")
        self.verticalLayout_6.addWidget(self.selectedListWidget)
        self.SongListsLayout.addWidget(self.selectedGroupBox)


        self.formatStack = QtGui.QStackedLayout()
        self.formatStack.setObjectName(u'FormatStack')
        self.sourceLayout.addLayout(self.formatStack)
        self.addPage(self.sourcePage)

    def retranslateUi(self):
        """
        Song wizard localisation.
        """
        self.setWindowTitle(
            translate('SongsPlugin.ImportWizardForm', 'Song Import Wizard'))
        self.titleLabel.setText(
            u'<span style="font-size:14pt; font-weight:600;">%s</span>' % \
            translate('SongsPlugin.ImportWizardForm',
                'Welcome to the Song Import Wizard'))
        self.informationLabel.setText(
            translate('SongsPlugin.ImportWizardForm',
                'This wizard will help you to export songs from a variety of '
                'formats. Click the next button below to start the process by '
                'selecting a format to export from.'))
        self.sourcePage.setTitle(
            translate('SongsPlugin.ImportWizardForm', 'Select Import Source'))
        self.sourcePage.setSubTitle(
            translate('SongsPlugin.ImportWizardForm',
            'Select the export format, and where to export from.'))

        self.progressPage.setTitle(
            translate('SongsPlugin.ImportWizardForm', 'Importing'))
        self.progressPage.setSubTitle(
            translate('SongsPlugin.ImportWizardForm',
                'Please wait while your songs are exported.'))
        self.progressLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Ready.'))
        self.progressBar.setFormat(
            translate('SongsPlugin.ImportWizardForm', '%p%'))

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
            translate('SongsPlugin.ImportWizardForm', 'Starting export...'))
        Receiver.send_message(u'openlp_process_events')

    def performWizard(self):
        """
        Perform the actual export. This method pulls in the correct exporter
        class, and then runs the ``do_export`` method of the exporter to do
        the actual exporting.
        """
        exporter = OpenLyricsExport()
        if exporter.do_export():
            self.progressLabel.setText(
                translate('SongsPlugin.SongImportForm', 'Finished export.'))
        else:
            self.progressLabel.setText(
                translate('SongsPlugin.SongImportForm',
                'Your song export failed.'))
