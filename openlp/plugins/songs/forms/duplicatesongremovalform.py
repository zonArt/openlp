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

from openlp.core.lib import Registry, translate, build_icon
from openlp.core.lib.db import Manager
from openlp.core.lib.ui import UiStrings, critical_error_message_box
from openlp.core.ui.wizard import OpenLPWizard, WizardStrings
from openlp.core.utils import AppLocation
from openlp.plugins.songs.lib.db import Song, MediaFile
from openlp.plugins.songs.lib.duplicatesongfinder import DuplicateSongFinder
from openlp.plugins.songs.forms.songreviewwidget import SongReviewWidget

log = logging.getLogger(__name__)

class DuplicateSongRemovalForm(OpenLPWizard):
    """
    This is the Duplicate Song Removal Wizard. It provides functionality to
    search for and remove duplicate songs in the database.
    """
    log.info(u'DuplicateSongRemovalForm loaded')

    def __init__(self, plugin):
        """
        Instantiate the wizard, and run any extra setup we need to.

        ``parent``
            The QWidget-derived parent of the wizard.

        ``plugin``
            The songs plugin.
        """
        self.duplicate_song_list = []
        self.review_current_count = 0
        self.review_total_count = 0
        OpenLPWizard.__init__(self, self.main_window, plugin, u'duplicateSongRemovalWizard',
            u':/wizards/wizard_duplicateremoval.bmp', False)

    def customSignals(self):
        """
        Song wizard specific signals.
        """
        QtCore.QObject.connect(self.finishButton, QtCore.SIGNAL(u'clicked()'), self.onWizardExit)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(u'clicked()'), self.onWizardExit)

    def addCustomPages(self):
        """
        Add song wizard specific pages.
        """
        #add custom pages
        self.searching_page = QtGui.QWizardPage()
        self.searching_page.setObjectName(u'searching_page')
        self.searching_vertical_layout = QtGui.QVBoxLayout(self.searching_page)
        self.searching_vertical_layout.setObjectName(u'searching_vertical_layout')
        self.duplicate_search_progress_bar = QtGui.QProgressBar(self.searching_page)
        self.duplicate_search_progress_bar.setObjectName(u'duplicate_search_progress_bar')
        self.duplicate_search_progress_bar.setFormat(WizardStrings.PercentSymbolFormat)
        self.searching_vertical_layout.addWidget(self.duplicate_search_progress_bar)
        self.found_duplicates_edit = QtGui.QPlainTextEdit(self.searching_page)
        self.found_duplicates_edit.setUndoRedoEnabled(False)
        self.found_duplicates_edit.setReadOnly(True)
        self.found_duplicates_edit.setObjectName(u'found_duplicates_edit')
        self.searching_vertical_layout.addWidget(self.found_duplicates_edit)
        self.searching_page_id = self.addPage(self.searching_page)
        self.review_page = QtGui.QWizardPage()
        self.review_page.setObjectName(u'review_page')
        self.review_layout = QtGui.QVBoxLayout(self.review_page)
        self.review_layout.setObjectName(u'review_layout')
        self.songs_horizontal_scroll_area = QtGui.QScrollArea(self.review_page)
        self.songs_horizontal_scroll_area.setObjectName(u'songs_horizontal_scroll_area')
        self.songs_horizontal_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.songs_horizontal_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.songs_horizontal_scroll_area.setFrameStyle(QtGui.QFrame.NoFrame)
        self.songs_horizontal_scroll_area.setWidgetResizable(True)
        self.songs_horizontal_scroll_area.setStyleSheet(
            u'QScrollArea#songs_horizontal_scroll_area {background-color:transparent;}')
        self.songs_horizontal_songs_widget = QtGui.QWidget(self.songs_horizontal_scroll_area)
        self.songs_horizontal_songs_widget.setObjectName(u'songs_horizontal_songs_widget')
        self.songs_horizontal_songs_widget.setStyleSheet(
            u'QWidget#songs_horizontal_songs_widget {background-color:transparent;}')
        self.songs_horizontal_layout = QtGui.QHBoxLayout(self.songs_horizontal_songs_widget)
        self.songs_horizontal_layout.setObjectName(u'songs_horizontal_layout')
        self.songs_horizontal_layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.songs_horizontal_scroll_area.setWidget(self.songs_horizontal_songs_widget)
        self.review_layout.addWidget(self.songs_horizontal_scroll_area)
        self.review_page_id = self.addPage(self.review_page)
        #add a dummy page to the end, to prevent the finish button to appear and the next button do disappear on the
        #review page
        self.dummy_page = QtGui.QWizardPage()
        self.dummy_page_id = self.addPage(self.dummy_page)

    def retranslateUi(self):
        """
        Song wizard localisation.
        """
        self.setWindowTitle(translate(u'Wizard', u'Wizard'))
        self.titleLabel.setText(WizardStrings.HeaderStyle % translate(u'OpenLP.Ui',
            u'Welcome to the Duplicate Song Removal Wizard'))
        self.informationLabel.setText(translate("Wizard",
            u'This wizard will help you to remove duplicate songs from the song database. You will have a chance to '
            u'review every potential duplicate song before it is deleted. So no songs will be deleted without your '
            u'explicit approval.'))
        self.searching_page.setTitle(translate(u'Wizard', u'Searching for duplicate songs.'))
        self.searching_page.setSubTitle(translate(u'Wizard', u'The song database is searched for double songs.'))
        self.updateReviewCounterText()
        self.review_page.setSubTitle(translate(u'Wizard',
            u'Here you can decide which songs to remove and which ones to keep.'))

    def updateReviewCounterText(self):
        """
        Set the wizard review page header text.
        """
        self.review_page.setTitle(translate(u'Wizard', u'Review duplicate songs (%s/%s)') % \
                (self.review_current_count, self.review_total_count))

    def customPageChanged(self, page_id):
        """
        Called when changing the wizard page.

        ``page_id``
            ID of the page the wizard changed to.
        """
        #hide back button
        self.button(QtGui.QWizard.BackButton).hide()
        if page_id == self.searching_page_id:
            #search duplicate songs
            max_songs = self.plugin.manager.get_object_count(Song)
            if max_songs == 0 or max_songs == 1:
                self.duplicate_search_progress_bar.setMaximum(1)
                self.duplicate_search_progress_bar.setValue(1)
                self.notifyNoDuplicates()
                return
            # with x songs we have x*(x - 1) / 2 comparisons
            max_progress_count = max_songs * (max_songs - 1) / 2
            self.duplicate_search_progress_bar.setMaximum(max_progress_count)
            songs = self.plugin.manager.get_all_objects(Song)
            for outer_song_counter in range(max_songs - 1):
                for inner_song_counter in range(outer_song_counter + 1, max_songs):
                    double_finder = DuplicateSongFinder()
                    if double_finder.songs_probably_equal(songs[outer_song_counter], songs[inner_song_counter]):
                        duplicate_added = self.addDuplicatesToSongList(songs[outer_song_counter],
                            songs[inner_song_counter])
                        if duplicate_added:
                            self.found_duplicates_edit.appendPlainText(songs[outer_song_counter].title + "  =  " +
                                songs[inner_song_counter].title)
                    self.duplicate_search_progress_bar.setValue(self.duplicate_search_progress_bar.value() + 1)
            self.review_total_count = len(self.duplicate_song_list)
            if self.review_total_count == 0:
                self.notifyNoDuplicates()
        elif page_id == self.review_page_id:
            self.processCurrentDuplicateEntry()

    def notifyNoDuplicates(self):
        """
        Notifies the user, that there were no duplicates found in the database.
        """
        self.button(QtGui.QWizard.FinishButton).show()
        self.button(QtGui.QWizard.FinishButton).setEnabled(True)
        self.button(QtGui.QWizard.NextButton).hide()
        QtGui.QMessageBox.information(self, translate(u'Wizard', u'Information'),
            translate(u'Wizard', u'No duplicate songs have been found in the database.'),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))


    def addDuplicatesToSongList(self, search_song, duplicate_song):
        """
        Inserts a song duplicate (two similar songs) to the duplicate song list.
        If one of the two songs is already part of the duplicate song list,
        don't add another duplicate group but add the other song to that group.
        Returns True if at least one of the songs was added, False if both were already
        member of a group.

        ``search_song``
            The song we searched the duplicate for.

        ``duplicate_song``
            The duplicate song.
        """
        duplicate_group_found = False
        duplicate_added = False
        for duplicate_group in self.duplicate_song_list:
            #skip the first song in the duplicate lists, since the first one has to be an earlier song
            if search_song in duplicate_group and not duplicate_song in duplicate_group:
                duplicate_group.append(duplicate_song)
                duplicate_group_found = True
                duplicate_added = True
                break
            elif not search_song in duplicate_group and duplicate_song in duplicate_group:
                duplicate_group.append(search_song)
                duplicate_group_found = True
                duplicate_added = True
                break
            elif search_song in duplicate_group and duplicate_song in duplicate_group:
                duplicate_group_found = True
                duplicate_added = False
                break
        if not duplicate_group_found:
            self.duplicate_song_list.append([search_song, duplicate_song])
            duplicate_added = True
        return duplicate_added

    def onWizardExit(self):
        """
        Once the wizard is finished, refresh the song list,
        since we potentially removed songs from it.
        """
        self.plugin.mediaItem.onSearchTextButtonClicked()

    def setDefaults(self):
        """
        Set default form values for the song import wizard.
        """
        self.restart()
        self.duplicate_search_progress_bar.setValue(0)
        self.found_duplicates_edit.clear()

    def validateCurrentPage(self):
        """
        Controls whether we should switch to the next wizard page. This method loops
        on the review page as long as there are more song duplicates to review.
        """
        if self.currentId() == self.review_page_id:
            #as long as it's not the last duplicate list entry we revisit the review page
            if len(self.duplicate_song_list) == 1:
                return True
            else:
                self.proceedToNextReview()
                return False
        return OpenLPWizard.validateCurrentPage(self)

    def removeButtonClicked(self, song_review_widget):
        """
        Removes a song from the database, removes the GUI element representing the
        song on the review page, and disable the remove button if only one duplicate
        is left.

        ``song_review_widget``
            The SongReviewWidget whose song we should delete.
        """
        #remove song from duplicate song list
        self.duplicate_song_list[-1].remove(song_review_widget.song)
        #remove song
        item_id = song_review_widget.song.id
        media_files = self.plugin.manager.get_all_objects(MediaFile,
            MediaFile.song_id == item_id)
        for media_file in media_files:
            try:
                os.remove(media_file.file_name)
            except:
                log.exception(u'Could not remove file: %s',
                    media_file.file_name)
        try:
            save_path = os.path.join(AppLocation.get_section_data_path(
                self.plugin.name), u'audio', str(item_id))
            if os.path.exists(save_path):
                os.rmdir(save_path)
        except OSError:
            log.exception(u'Could not remove directory: %s', save_path)
        self.plugin.manager.delete_object(Song, item_id)
        # remove GUI elements
        self.songs_horizontal_layout.removeWidget(song_review_widget)
        song_review_widget.setParent(None)
        # check if we only have one duplicate left
        # 4 stretches + 1 SongReviewWidget = 5
        # the SongReviewWidget is then at position 2
        if len(self.duplicate_song_list[-1]) == 1:
            self.songs_horizontal_layout.itemAt(2).widget().song_remove_button.setEnabled(False)

    def proceedToNextReview(self):
        """
        Removes the previous review UI elements and calls processCurrentDuplicateEntry.
        """
        #remove last duplicate group
        self.duplicate_song_list.pop()
        # remove all previous elements
        for i in reversed(range(self.songs_horizontal_layout.count())): 
            item = self.songs_horizontal_layout.itemAt(i)
            if isinstance(item, QtGui.QWidgetItem):
                # The order is important here, if the .setParent(None) call is done
                # before the .removeItem() call, a segfault occurs.
                widget = item.widget()
                self.songs_horizontal_layout.removeItem(item) 
                widget.setParent(None)
            else:
                self.songs_horizontal_layout.removeItem(item)
        #process next set of duplicates
        self.processCurrentDuplicateEntry()
    
    def processCurrentDuplicateEntry(self):
        """
        Update the review counter in the wizard header, add song widgets for
        the current duplicate group to review, if it's the last
        duplicate song group, hide the "next" button and show the "finish" button.
        """
        # update counter
        self.review_current_count = self.review_total_count - (len(self.duplicate_song_list) - 1)
        self.updateReviewCounterText()
        # add song elements to the UI
        if len(self.duplicate_song_list) > 0:
            # a stretch doesn't seem to stretch endlessly, so I add two to get enough stetch for 1400x1050
            self.songs_horizontal_layout.addStretch()
            self.songs_horizontal_layout.addStretch()
            for duplicate in self.duplicate_song_list[-1]:
                song_review_widget = SongReviewWidget(self.review_page, duplicate)
                QtCore.QObject.connect(song_review_widget,
                        QtCore.SIGNAL(u'songRemoveButtonClicked(PyQt_PyObject)'),
                        self.removeButtonClicked)
                self.songs_horizontal_layout.addWidget(song_review_widget)
            self.songs_horizontal_layout.addStretch()
            self.songs_horizontal_layout.addStretch()
        #change next button to finish button on last review
        if len(self.duplicate_song_list) == 1:
            self.button(QtGui.QWizard.FinishButton).show()
            self.button(QtGui.QWizard.FinishButton).setEnabled(True)
            self.button(QtGui.QWizard.NextButton).hide()
    
    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, u'_main_window'):
            self._main_window = Registry().get(u'main_window')
        return self._main_window

    main_window = property(_get_main_window)
