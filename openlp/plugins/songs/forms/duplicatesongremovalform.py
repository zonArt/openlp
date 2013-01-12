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
The duplicate song removal logic for OpenLP.
"""
import codecs
import logging
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, Settings, SettingsManager, translate, build_icon
from openlp.core.lib.db import Manager
from openlp.core.lib.ui import UiStrings, critical_error_message_box
from openlp.core.ui.wizard import OpenLPWizard, WizardStrings
from openlp.plugins.songs.lib.db import Song
from openlp.plugins.songs.lib.importer import SongFormat, SongFormatSelect
from openlp.plugins.songs.lib.duplicatesongfinder import DuplicateSongFinder

log = logging.getLogger(__name__)

class DuplicateSongRemovalForm(OpenLPWizard):
    """
    This is the Duplicate Song Removal Wizard. It provides functionality to
    search for and remove duplicate songs in the database.
    """
    log.info(u'DuplicateSongRemovalForm loaded')

    def __init__(self, parent, plugin):
        """
        Instantiate the wizard, and run any extra setup we need to.

        ``parent``
            The QWidget-derived parent of the wizard.

        ``plugin``
            The songs plugin.
        """
        self.clipboard = plugin.formParent.clipboard
        OpenLPWizard.__init__(self, parent, plugin, u'duplicateSongRemovalWizard',
            u':/wizards/wizard_importsong.bmp', False)

    def customInit(self):
        """
        Song wizard specific initialisation.
        """
        self.duplicateSongList = []

    def customSignals(self):
        """
        Song wizard specific signals.
        """
        #QtCore.QObject.connect(self.addButton,
        #        QtCore.SIGNAL(u'clicked()'), self.onAddButtonClicked)
        #QtCore.QObject.connect(self.removeButton,
        #    QtCore.SIGNAL(u'clicked()'), self.onRemoveButtonClicked)

    def addCustomPages(self):
        """
        Add song wizard specific pages.
        """
        self.searchingPage = QtGui.QWizardPage()
        self.searchingPage.setObjectName('searchingPage')
        self.searchingVerticalLayout = QtGui.QVBoxLayout(self.searchingPage)
        self.searchingVerticalLayout.setObjectName('searchingVerticalLayout')
        self.duplicateSearchProgressBar = QtGui.QProgressBar(self.searchingPage)
        self.duplicateSearchProgressBar.setObjectName(u'duplicateSearchProgressBar')
        self.duplicateSearchProgressBar.setFormat(WizardStrings.PercentSymbolFormat)
        self.searchingVerticalLayout.addWidget(self.duplicateSearchProgressBar)
        self.foundDuplicatesEdit = QtGui.QPlainTextEdit(self.searchingPage)
        self.foundDuplicatesEdit.setUndoRedoEnabled(False)
        self.foundDuplicatesEdit.setReadOnly(True)
        self.foundDuplicatesEdit.setObjectName('foundDuplicatesEdit')
        self.searchingVerticalLayout.addWidget(self.foundDuplicatesEdit)
        self.addPage(self.searchingPage)
        self.reviewPage = QtGui.QWizardPage()
        self.reviewPage.setObjectName('reviewPage')
        self.headerVerticalLayout = QtGui.QVBoxLayout(self.reviewPage)
        self.headerVerticalLayout.setObjectName('headerVerticalLayout')
        self.reviewCounterLabel = QtGui.QLabel(self.reviewPage)
        self.reviewCounterLabel.setObjectName('reviewCounterLabel')
        self.headerVerticalLayout.addWidget(self.reviewCounterLabel)
        self.songsHorizontalLayout = QtGui.QHBoxLayout()
        self.songsHorizontalLayout.setObjectName('songsHorizontalLayout')
        self.headerVerticalLayout.addLayout(self.songsHorizontalLayout)
        self.addPage(self.reviewPage)

    def retranslateUi(self):
        """
        Song wizard localisation.
        """
        self.setWindowTitle(translate('Wizard', 'Wizard'))
        self.titleLabel.setText(WizardStrings.HeaderStyle % translate('OpenLP.Ui',
            'Welcome to the Duplicate Song Removal Wizard'))
        self.informationLabel.setText(translate("Wizard",
            'This wizard will help you to remove duplicate songs from the song database.'))
        self.searchingPage.setTitle(translate('Wizard', 'Searching for doubles'))
        self.searchingPage.setSubTitle(translate('Wizard', 'The song database is searched for double songs.'))
        self.reviewPage.setTitle(translate('Wizard', 'Review duplicate songs'))
        self.reviewPage.setSubTitle(translate('Wizard',
            'This page shows all duplicate songs to review which ones to remove and which ones to keep.'))

    def customPageChanged(self, pageId):
        """
        Called when changing to a page other than the progress page.
        """
        if self.page(pageId) == self.searchingPage:
            maxSongs = self.plugin.manager.get_object_count(Song)
            if maxSongs == 0 or maxSongs == 1:
                return
            # with x songs we have x*(x-1)/2 comparisons
            maxProgressCount = maxSongs*(maxSongs-1)/2
            self.duplicateSearchProgressBar.setMaximum(maxProgressCount)
            songs = self.plugin.manager.get_all_objects(Song)
            for outerSongCounter in range(maxSongs-1):
                for innerSongCounter in range(outerSongCounter+1, maxSongs):
                    doubleFinder = DuplicateSongFinder()
                    if doubleFinder.songsProbablyEqual(songs[outerSongCounter], songs[innerSongCounter]):
                        self.addDuplicatesToSongList(songs[outerSongCounter], songs[innerSongCounter])
                        self.foundDuplicatesEdit.appendPlainText(songs[outerSongCounter].title + "  =  " + songs[innerSongCounter].title)
                    self.duplicateSearchProgressBar.setValue(self.duplicateSearchProgressBar.value()+1)
        elif self.page(pageId) == self.reviewPage:
            for duplicates in self.duplicateSongList[0:1]:
                for duplicate in duplicates:
                    songReviewWidget = SongReviewWidget(self.reviewPage, duplicate)
                    self.songsHorizontalLayout.addWidget(songReviewWidget)

    def addDuplicatesToSongList(self, searchSong, duplicateSong):
        duplicateGroupFound = False
        for duplicates in self.duplicateSongList:
            #skip the first song in the duplicate lists, since the first one has to be an earlier song
            for duplicate in duplicates[1:]:
                if duplicate == searchSong:
                    duplicates.append(duplicateSong)
                    duplicateGroupFound = True
                    break
                elif duplicate == duplicateSong:
                    duplicates.appen(searchSong)
                    duplicateGroupFound = True
                    break
            if duplicateGroupFound:
                break
        if not duplicateGroupFound:
            self.duplicateSongList.append([searchSong, duplicateSong])

    def onAddButtonClicked(self):
        pass

    def onRemoveButtonClicked(self):
        pass

    def setDefaults(self):
        """
        Set default form values for the song import wizard.
        """
        self.restart()
        self.duplicateSearchProgressBar.setValue(0)
        self.foundDuplicatesEdit.clear()

    def performWizard(self):
        """
        Perform the actual import. This method pulls in the correct importer
        class, and then runs the ``doImport`` method of the importer to do
        the actual importing.
        """
        pass

class SongReviewWidget(QtGui.QWidget):
    def __init__(self, parent, song):
        QtGui.QWidget.__init__(self, parent)
        self.song = song
        self.setupUi()
        self.retranslateUi()

    def setupUi(self):
        self.songVerticalLayout = QtGui.QVBoxLayout(self)
        self.songVerticalLayout.setObjectName('songVerticalLayout')
        self.songGroupBox = QtGui.QGroupBox(self)
        self.songGroupBox.setObjectName('songGroupBox')
        self.songContentVerticalLayout = QtGui.QVBoxLayout(self.songGroupBox)
        self.songContentVerticalLayout.setObjectName('songContentVerticalLayout')
        self.songInfoFormLayout = QtGui.QFormLayout()
        self.songInfoFormLayout.setObjectName('songInfoFormLayout')
        #add ccli number, name, altname, authors, ... here
        self.songTitleLabel = QtGui.QLabel(self)
        self.songTitleLabel.setObjectName('songTitleLabel')
        self.songInfoFormLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.songTitleLabel)
        self.songTitleContent = QtGui.QLabel(self)
        self.songTitleContent.setObjectName('songTitleContent')
        self.songTitleContent.setText(self.song.title)
        self.songInfoFormLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.songTitleContent)
        self.songAlternateTitleLabel = QtGui.QLabel(self)
        self.songAlternateTitleLabel.setObjectName('songAlternateTitleLabel')
        self.songInfoFormLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.songAlternateTitleLabel)
        self.songAlternateTitleContent = QtGui.QLabel(self)
        self.songAlternateTitleContent.setObjectName('songAlternateTitleContent')
        self.songAlternateTitleContent.setText(self.song.alternate_title)
        self.songInfoFormLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.songAlternateTitleContent)
        self.songCCLINumberLabel = QtGui.QLabel(self)
        self.songCCLINumberLabel.setObjectName('songCCLINumberLabel')
        self.songInfoFormLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.songCCLINumberLabel)
        self.songCCLINumberContent = QtGui.QLabel(self)
        self.songCCLINumberContent.setObjectName('songCCLINumberContent')
        self.songCCLINumberContent.setText(self.song.ccli_number)
        self.songInfoFormLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.songCCLINumberContent)
        self.songVerseOrderLabel = QtGui.QLabel(self)
        self.songVerseOrderLabel.setObjectName('songVerseOrderLabel')
        self.songInfoFormLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.songVerseOrderLabel)
        self.songVerseOrderContent = QtGui.QLabel(self)
        self.songVerseOrderContent.setObjectName('songVerseOrderContent')
        self.songVerseOrderContent.setText(self.song.verse_order)
        self.songInfoFormLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.songVerseOrderContent)
        self.songCopyrightLabel = QtGui.QLabel(self)
        self.songCopyrightLabel.setObjectName('songCopyrightLabel')
        self.songInfoFormLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.songCopyrightLabel)
        self.songCopyrightContent = QtGui.QLabel(self)
        self.songCopyrightContent.setObjectName('songCopyrightContent')
        self.songCopyrightContent.setText(self.song.copyright)
        self.songInfoFormLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.songCopyrightContent)
        self.songCommentsLabel = QtGui.QLabel(self)
        self.songCommentsLabel.setObjectName('songCommentsLabel')
        self.songInfoFormLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.songCommentsLabel)
        self.songCommentsContent = QtGui.QLabel(self)
        self.songCommentsContent.setObjectName('songCommentsContent')
        self.songCommentsContent.setText(self.song.comments)
        self.songInfoFormLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.songCommentsContent)
        self.songAuthorsLabel = QtGui.QLabel(self)
        self.songAuthorsLabel.setObjectName('songAuthorsLabel')
        self.songInfoFormLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.songAuthorsLabel)
        self.songAuthorsContent = QtGui.QLabel(self)
        self.songAuthorsContent.setObjectName('songAuthorsContent')
        authorsText = u''
        for author in self.song.authors:
            authorsText += author.display_name + ', '
        if authorsText:
            authorsText = authorsText[:-2]
        self.songAuthorsContent.setText(authorsText)
        self.songInfoFormLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.songAuthorsContent)
        self.songContentVerticalLayout.addLayout(self.songInfoFormLayout)
        self.songVerseButton = QtGui.QPushButton(self)
        self.songVerseButton.setObjectName('songVerseButton')
        self.songContentVerticalLayout.addWidget(self.songVerseButton)
        self.songVerticalLayout.addWidget(self.songGroupBox)
        self.songRemoveButton = QtGui.QPushButton(self)
        self.songRemoveButton.setObjectName('songRemoveButton')
        self.songRemoveButton.setIcon(build_icon(u':/songs/song_delete.png'))
        self.songVerticalLayout.addWidget(self.songRemoveButton)

    def retranslateUi(self):
        self.songRemoveButton.setText(u'Remove')
        self.songTitleLabel.setText(u'Title:')
        self.songAlternateTitleLabel.setText(u'Alternate Title:')
        self.songCCLINumberLabel.setText(u'CCLI Number:')
        self.songVerseOrderLabel.setText(u'Verse Order:')
        self.songCopyrightLabel.setText(u'Copyright:')
        self.songCommentsLabel.setText(u'Comments:')
        self.songAuthorsLabel.setText(u'Authors:')

