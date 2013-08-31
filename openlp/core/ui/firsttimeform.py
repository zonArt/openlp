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
This module contains the first time wizard.
"""
import logging
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from tempfile import gettempdir
from configparser import SafeConfigParser

from PyQt4 import QtCore, QtGui

from openlp.core.lib import PluginStatus, Settings, Registry, build_icon, check_directory_exists, translate
from openlp.core.utils import AppLocation, get_web_page
from .firsttimewizard import Ui_FirstTimeWizard, FirstTimePage

log = logging.getLogger(__name__)


class ThemeScreenshotThread(QtCore.QThread):
    """
    This thread downloads the theme screenshots.
    """
    def run(self):
        """
        Overridden method to run the thread.
        """
        themes = self.parent().config.get('themes', 'files')
        themes = themes.split(',')
        config = self.parent().config
        for theme in themes:
            # Stop if the wizard has been cancelled.
            if self.parent().was_download_cancelled:
                return
            title = config.get('theme_%s' % theme, 'title')
            filename = config.get('theme_%s' % theme, 'filename')
            screenshot = config.get('theme_%s' % theme, 'screenshot')
            urllib.request.urlretrieve('%s%s' % (self.parent().web, screenshot),
                os.path.join(gettempdir(), 'openlp', screenshot))
            item = QtGui.QListWidgetItem(title, self.parent().themes_list_widget)
            item.setData(QtCore.Qt.UserRole, filename)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)


class FirstTimeForm(QtGui.QWizard, Ui_FirstTimeWizard):
    """
    This is the Theme Import Wizard, which allows easy creation and editing of OpenLP themes.
    """
    log.info('ThemeWizardForm loaded')

    def __init__(self, screens, parent=None):
        """
        Create and set up the first time wizard.
        """
        super(FirstTimeForm, self).__init__(parent)
        self.setupUi(self)
        self.screens = screens
        # check to see if we have web access
        self.web = 'http://openlp.org/files/frw/'
        self.config = SafeConfigParser()
        self.web_access = get_web_page('%s%s' % (self.web, 'download.cfg'))
        if self.web_access:
            files = self.web_access.read()
            self.config.read_string(files.decode())
        self.update_screen_list_combo()
        self.was_download_cancelled = False
        self.theme_screenshot_thread = None
        self.downloading = translate('OpenLP.FirstTimeWizard', 'Downloading %s...')
        self.cancel_button.clicked.connect(self.on_cancel_button_clicked)
        self.no_internet_finish_button.clicked.connect(self.on_no_internet_finish_button_clicked)
        self.currentIdChanged.connect(self.on_current_id_changed)
        Registry().register_function('config_screen_changed', self.update_screen_list_combo)

    def exec_(self):
        """
        Run the wizard.
        """
        self.setDefaults()
        return QtGui.QWizard.exec_(self)

    def setDefaults(self):
        """
        Set up display at start of theme edit.
        """
        self.restart()
        check_directory_exists(os.path.join(gettempdir(), 'openlp'))
        self.no_internet_finish_button.setVisible(False)
        # Check if this is a re-run of the wizard.
        self.has_run_wizard = Settings().value('core/has run wizard')
        # Sort out internet access for downloads
        if self.web_access:
            songs = self.config.get('songs', 'languages')
            songs = songs.split(',')
            for song in songs:
                title = self.config.get('songs_%s' % song, 'title')
                filename = self.config.get('songs_%s' % song, 'filename')
                item = QtGui.QListWidgetItem(title, self.songs_list_widget)
                item.setData(QtCore.Qt.UserRole, filename)
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            bible_languages = self.config.get('bibles', 'languages')
            bible_languages = bible_languages.split(',')
            for lang in bible_languages:
                language = self.config.get('bibles_%s' % lang, 'title')
                langItem = QtGui.QTreeWidgetItem(self.bibles_tree_widget, [language])
                bibles = self.config.get('bibles_%s' % lang, 'translations')
                bibles = bibles.split(',')
                for bible in bibles:
                    title = self.config.get('bible_%s' % bible, 'title')
                    filename = self.config.get('bible_%s' % bible, 'filename')
                    item = QtGui.QTreeWidgetItem(langItem, [title])
                    item.setData(0, QtCore.Qt.UserRole, filename)
                    item.setCheckState(0, QtCore.Qt.Unchecked)
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            self.bibles_tree_widget.expandAll()
            # Download the theme screenshots.
            self.theme_screenshot_thread = ThemeScreenshotThread(self)
            self.theme_screenshot_thread.start()
        self.application.set_normal_cursor()

    def nextId(self):
        """
        Determine the next page in the Wizard to go to.
        """
        self.application.process_events()
        if self.currentId() == FirstTimePage.Plugins:
            if not self.web_access:
                return FirstTimePage.NoInternet
            else:
                return FirstTimePage.Songs
        elif self.currentId() == FirstTimePage.Progress:
            return -1
        elif self.currentId() == FirstTimePage.NoInternet:
            return FirstTimePage.Progress
        elif self.currentId() == FirstTimePage.Themes:
            self.application.set_busy_cursor()
            while not self.theme_screenshot_thread.isFinished():
                time.sleep(0.1)
                self.application.process_events()
            # Build the screenshot icons, as this can not be done in the thread.
            self._build_theme_screenshots()
            self.application.set_normal_cursor()
            return FirstTimePage.Defaults
        else:
            return self.currentId() + 1

    def on_current_id_changed(self, page_id):
        """
        Detects Page changes and updates as appropriate.
        """
        # Keep track of the page we are at.  Triggering "Cancel" causes page_id to be a -1.
        self.application.process_events()
        if page_id != -1:
            self.last_id = page_id
        if page_id == FirstTimePage.Plugins:
            # Set the no internet page text.
            if self.has_run_wizard:
                self.no_internet_label.setText(self.no_internet_text)
            else:
                self.no_internet_label.setText(self.no_internet_text + self.cancelWizardText)
        elif page_id == FirstTimePage.Defaults:
            self.theme_combo_box.clear()
            for iter in range(self.themes_list_widget.count()):
                item = self.themes_list_widget.item(iter)
                if item.checkState() == QtCore.Qt.Checked:
                    self.theme_combo_box.addItem(item.text())
            if self.has_run_wizard:
                # Add any existing themes to list.
                for theme in self.theme_manager.get_themes():
                    index = self.theme_combo_box.findText(theme)
                    if index == -1:
                        self.theme_combo_box.addItem(theme)
                default_theme = Settings().value('themes/global theme')
                # Pre-select the current default theme.
                index = self.theme_combo_box.findText(default_theme)
                self.theme_combo_box.setCurrentIndex(index)
        elif page_id == FirstTimePage.NoInternet:
            self.back_button.setVisible(False)
            self.next_button.setVisible(False)
            self.no_internet_finish_button.setVisible(True)
            if self.has_run_wizard:
                self.cancel_button.setVisible(False)
        elif page_id == FirstTimePage.Progress:
            self.application.set_busy_cursor()
            self.repaint()
            self.application.process_events()
            # Try to give the wizard a chance to redraw itself
            time.sleep(0.2)
            self._pre_wizard()
            self._perform_wizard()
            self._post_wizard()
            self.application.set_normal_cursor()

    def update_screen_list_combo(self):
        """
        The user changed screen resolution or enabled/disabled more screens, so
        we need to update the combo box.
        """
        self.display_combo_box.clear()
        self.display_combo_box.addItems(self.screens.get_screen_list())
        self.display_combo_box.setCurrentIndex(self.display_combo_box.count() - 1)

    def on_cancel_button_clicked(self):
        """
        Process the triggering of the cancel button.
        """
        if self.last_id == FirstTimePage.NoInternet or (self.last_id <= FirstTimePage.Plugins and not self.has_run_wizard):
            QtCore.QCoreApplication.exit()
            sys.exit()
        self.was_download_cancelled = True
        # Was the thread created.
        if self.theme_screenshot_thread:
            while self.theme_screenshot_thread.isRunning():
                time.sleep(0.1)
        self.application.set_normal_cursor()

    def on_no_internet_finish_button_clicked(self):
        """
        Process the triggering of the "Finish" button on the No Internet page.
        """
        self.application.set_busy_cursor()
        self._perform_wizard()
        self.application.set_normal_cursor()
        Settings().setValue('core/has run wizard', True)
        self.close()

    def url_get_file(self, url, f_path):
        """"
        Download a file given a URL.  The file is retrieved in chunks, giving the ability to cancel the download at any
        point.
        """
        block_count = 0
        block_size = 4096
        url_file = urllib.request.urlopen(url)
        filename = open(f_path, "wb")
        # Download until finished or canceled.
        while not self.was_download_cancelled:
            data = url_file.read(block_size)
            if not data:
                break
            filename.write(data)
            block_count += 1
            self._download_progress(block_count, block_size)
        filename.close()
        # Delete file if cancelled, it may be a partial file.
        if self.was_download_cancelled:
            os.remove(f_path)

    def _build_theme_screenshots(self):
        """
        This method builds the theme screenshots' icons for all items in the
        ``self.themes_list_widget``.
        """
        themes = self.config.get('themes', 'files')
        themes = themes.split(',')
        for theme in themes:
            filename = self.config.get('theme_%s' % theme, 'filename')
            screenshot = self.config.get('theme_%s' % theme, 'screenshot')
            for index in range(self.themes_list_widget.count()):
                item = self.themes_list_widget.item(index)
                if item.data(QtCore.Qt.UserRole) == filename:
                    break
            item.setIcon(build_icon(os.path.join(gettempdir(), 'openlp', screenshot)))

    def _getFileSize(self, url):
        """
        Get the size of a file.

        ``url``
            The URL of the file we want to download.
        """
        site = urllib.request.urlopen(url)
        meta = site.info()
        return int(meta.get("Content-Length"))

    def _download_progress(self, count, block_size):
        """
        Calculate and display the download progress.
        """
        increment = (count * block_size) - self.previous_size
        self._increment_progress_bar(None, increment)
        self.previous_size = count * block_size

    def _increment_progress_bar(self, status_text, increment=1):
        """
        Update the wizard progress page.

        ``status_text``
            Current status information to display.

        ``increment``
            The value to increment the progress bar by.
        """
        if status_text:
            self.progress_label.setText(status_text)
        if increment > 0:
            self.progress_bar.setValue(self.progress_bar.value() + increment)
        self.application.process_events()

    def _pre_wizard(self):
        """
        Prepare the UI for the process.
        """
        self.max_progress = 0
        self.finish_button.setVisible(False)
        self.application.process_events()
        # Loop through the songs list and increase for each selected item
        for i in range(self.songs_list_widget.count()):
            self.application.process_events()
            item = self.songs_list_widget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                filename = item.data(QtCore.Qt.UserRole)
                size = self._getFileSize('%s%s' % (self.web, filename))
                self.max_progress += size
        # Loop through the Bibles list and increase for each selected item
        iterator = QtGui.QTreeWidgetItemIterator(self.bibles_tree_widget)
        while iterator.value():
            self.application.process_events()
            item = iterator.value()
            if item.parent() and item.checkState(0) == QtCore.Qt.Checked:
                filename = item.data(0, QtCore.Qt.UserRole)
                size = self._getFileSize('%s%s' % (self.web, filename))
                self.max_progress += size
            iterator += 1
        # Loop through the themes list and increase for each selected item
        for i in range(self.themes_list_widget.count()):
            self.application.process_events()
            item = self.themes_list_widget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                filename = item.data(QtCore.Qt.UserRole)
                size = self._getFileSize('%s%s' % (self.web, filename))
                self.max_progress += size
        if self.max_progress:
            # Add on 2 for plugins status setting plus a "finished" point.
            self.max_progress += 2
            self.progress_bar.setValue(0)
            self.progress_bar.setMinimum(0)
            self.progress_bar.setMaximum(self.max_progress)
            self.progress_page.setTitle(translate('OpenLP.FirstTimeWizard', 'Setting Up And Downloading'))
            self.progress_page.setSubTitle(
                translate('OpenLP.FirstTimeWizard', 'Please wait while OpenLP is set up and your data is downloaded.'))
        else:
            self.progress_bar.setVisible(False)
            self.progress_page.setTitle(translate('OpenLP.FirstTimeWizard', 'Setting Up'))
            self.progress_page.setSubTitle('Setup complete.')
        self.repaint()
        self.application.process_events()
        # Try to give the wizard a chance to repaint itself
        time.sleep(0.1)

    def _post_wizard(self):
        """
        Clean up the UI after the process has finished.
        """
        if self.max_progress:
            self.progress_bar.setValue(self.progress_bar.maximum())
            if self.has_run_wizard:
                self.progress_label.setText(translate('OpenLP.FirstTimeWizard',
                    'Download complete. Click the finish button to return to OpenLP.'))
            else:
                self.progress_label.setText(translate('OpenLP.FirstTimeWizard',
                    'Download complete. Click the finish button to start OpenLP.'))
        else:
            if self.has_run_wizard:
                self.progress_label.setText(translate('OpenLP.FirstTimeWizard',
                    'Click the finish button to return to OpenLP.'))
            else:
                self.progress_label.setText(translate('OpenLP.FirstTimeWizard',
                    'Click the finish button to start OpenLP.'))
        self.finish_button.setVisible(True)
        self.finish_button.setEnabled(True)
        self.cancel_button.setVisible(False)
        self.next_button.setVisible(False)
        self.application.process_events()

    def _perform_wizard(self):
        """
        Run the tasks in the wizard.
        """
        # Set plugin states
        self._increment_progress_bar(translate('OpenLP.FirstTimeWizard', 'Enabling selected plugins...'))
        self._set_plugin_status(self.songs_check_box, 'songs/status')
        self._set_plugin_status(self.bible_check_box, 'bibles/status')
        # TODO Presentation plugin is not yet working on Mac OS X.
        # For now just ignore it.
        if sys.platform != 'darwin':
            self._set_plugin_status(self.presentation_check_box, 'presentations/status')
        self._set_plugin_status(self.image_check_box, 'images/status')
        self._set_plugin_status(self.media_check_box, 'media/status')
        self._set_plugin_status(self.remote_check_box, 'remotes/status')
        self._set_plugin_status(self.custom_check_box, 'custom/status')
        self._set_plugin_status(self.song_usage_check_box, 'songusage/status')
        self._set_plugin_status(self.alert_check_box, 'alerts/status')
        if self.web_access:
            # Build directories for downloads
            songs_destination = os.path.join(gettempdir(), 'openlp')
            bibles_destination = AppLocation.get_section_data_path('bibles')
            themes_destination = AppLocation.get_section_data_path('themes')
            # Download songs
            for i in range(self.songs_list_widget.count()):
                item = self.songs_list_widget.item(i)
                if item.checkState() == QtCore.Qt.Checked:
                    filename = item.data(QtCore.Qt.UserRole)
                    self._increment_progress_bar(self.downloading % filename, 0)
                    self.previous_size = 0
                    destination = os.path.join(songs_destination, str(filename))
                    self.url_get_file('%s%s' % (self.web, filename), destination)
            # Download Bibles
            bibles_iterator = QtGui.QTreeWidgetItemIterator(
                self.bibles_tree_widget)
            while bibles_iterator.value():
                item = bibles_iterator.value()
                if item.parent() and item.checkState(0) == QtCore.Qt.Checked:
                    bible = item.data(0, QtCore.Qt.UserRole)
                    self._increment_progress_bar(self.downloading % bible, 0)
                    self.previous_size = 0
                    self.url_get_file('%s%s' % (self.web, bible), os.path.join(bibles_destination, bible))
                bibles_iterator += 1
            # Download themes
            for i in range(self.themes_list_widget.count()):
                item = self.themes_list_widget.item(i)
                if item.checkState() == QtCore.Qt.Checked:
                    theme = item.data(QtCore.Qt.UserRole)
                    self._increment_progress_bar(self.downloading % theme, 0)
                    self.previous_size = 0
                    self.url_get_file('%s%s' % (self.web, theme), os.path.join(themes_destination, theme))
        # Set Default Display
        if self.display_combo_box.currentIndex() != -1:
            Settings().setValue('core/monitor', self.display_combo_box.currentIndex())
            self.screens.set_current_display(self.display_combo_box.currentIndex())
        # Set Global Theme
        if self.theme_combo_box.currentIndex() != -1:
            Settings().setValue('themes/global theme', self.theme_combo_box.currentText())

    def _set_plugin_status(self, field, tag):
        """
        Set the status of a plugin.
        """
        status = PluginStatus.Active if field.checkState() == QtCore.Qt.Checked else PluginStatus.Inactive
        Settings().setValue(tag, status)

    def _get_theme_manager(self):
        """
        Adds the theme manager to the class dynamically
        """
        if not hasattr(self, '_theme_manager'):
            self._theme_manager = Registry().get('theme_manager')
        return self._theme_manager

    theme_manager = property(_get_theme_manager)

    def _get_application(self):
        """
        Adds the openlp to the class dynamically.
        Windows needs to access the application in a dynamic manner.
        """
        if os.name == 'nt':
            return Registry().get('application')
        else:
            if not hasattr(self, '_application'):
                self._application = Registry().get('application')
            return self._application

    application = property(_get_application)
