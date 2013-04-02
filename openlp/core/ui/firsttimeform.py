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
import io
import logging
import os
import sys
import time
import urllib
import urllib2
from tempfile import gettempdir
from ConfigParser import SafeConfigParser

from PyQt4 import QtCore, QtGui

from openlp.core.lib import PluginStatus, Receiver, Settings, Registry, build_icon, check_directory_exists, translate
from openlp.core.utils import AppLocation, get_web_page, get_filesystem_encoding
from firsttimewizard import Ui_FirstTimeWizard, FirstTimePage

log = logging.getLogger(__name__)


class ThemeScreenshotThread(QtCore.QThread):
    """
    This thread downloads the theme screenshots.
    """
    def run(self):
        """
        Overridden method to run the thread.
        """
        themes = self.parent().config.get(u'themes', u'files')
        themes = themes.split(u',')
        config = self.parent().config
        for theme in themes:
            # Stop if the wizard has been cancelled.
            if self.parent().downloadCancelled:
                return
            title = config.get(u'theme_%s' % theme, u'title')
            filename = config.get(u'theme_%s' % theme, u'filename')
            screenshot = config.get(u'theme_%s' % theme, u'screenshot')
            urllib.urlretrieve(u'%s%s' % (self.parent().web, screenshot),
                os.path.join(unicode(gettempdir(), get_filesystem_encoding()), u'openlp', screenshot))
            item = QtGui.QListWidgetItem(title, self.parent().themesListWidget)
            item.setData(QtCore.Qt.UserRole, filename)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)


class FirstTimeForm(QtGui.QWizard, Ui_FirstTimeWizard):
    """
    This is the Theme Import Wizard, which allows easy creation and editing of
    OpenLP themes.
    """
    log.info(u'ThemeWizardForm loaded')

    def __init__(self, screens, parent=None):
        """
        Create and set up the first time wizard.
        """
        super(FirstTimeForm, self).__init__(parent)
        self.setupUi(self)
        self.screens = screens
        # check to see if we have web access
        self.web = u'http://openlp.org/files/frw/'
        self.config = SafeConfigParser()
        self.webAccess = get_web_page(u'%s%s' % (self.web, u'download.cfg'))
        if self.webAccess:
            files = self.webAccess.read()
            self.config.readfp(io.BytesIO(files))
        self.updateScreenListCombo()
        self.was_download_cancelled = False
        self.downloading = translate('OpenLP.FirstTimeWizard', 'Downloading %s...')
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL('clicked()'),
            self.onCancelButtonClicked)
        QtCore.QObject.connect(self.noInternetFinishButton, QtCore.SIGNAL('clicked()'),
            self.onNoInternetFinishButtonClicked)
        QtCore.QObject.connect(self, QtCore.SIGNAL(u'currentIdChanged(int)'), self.onCurrentIdChanged)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'config_screen_changed'),
            self.updateScreenListCombo)

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
        check_directory_exists(os.path.join(
            unicode(gettempdir(), get_filesystem_encoding()), u'openlp'))
        self.noInternetFinishButton.setVisible(False)
        # Check if this is a re-run of the wizard.
        self.hasRunWizard = Settings().value(u'general/has run wizard')
        # Sort out internet access for downloads
        if self.webAccess:
            songs = self.config.get(u'songs', u'languages')
            songs = songs.split(u',')
            for song in songs:
                title = unicode(self.config.get(u'songs_%s' % song, u'title'), u'utf8')
                filename = unicode(self.config.get(u'songs_%s' % song, u'filename'), u'utf8')
                item = QtGui.QListWidgetItem(title, self.songsListWidget)
                item.setData(QtCore.Qt.UserRole, filename)
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            bible_languages = self.config.get(u'bibles', u'languages')
            bible_languages = bible_languages.split(u',')
            for lang in bible_languages:
                language = unicode(self.config.get(u'bibles_%s' % lang, u'title'), u'utf8')
                langItem = QtGui.QTreeWidgetItem(self.biblesTreeWidget, [language])
                bibles = self.config.get(u'bibles_%s' % lang, u'translations')
                bibles = bibles.split(u',')
                for bible in bibles:
                    title = unicode(self.config.get(u'bible_%s' % bible, u'title'), u'utf8')
                    filename = unicode(self.config.get(u'bible_%s' % bible, u'filename'))
                    item = QtGui.QTreeWidgetItem(langItem, [title])
                    item.setData(0, QtCore.Qt.UserRole, filename)
                    item.setCheckState(0, QtCore.Qt.Unchecked)
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            self.biblesTreeWidget.expandAll()
            # Download the theme screenshots.
            self.themeScreenshotThread = ThemeScreenshotThread(self)
            self.themeScreenshotThread.start()
        self.application.set_normal_cursor()

    def nextId(self):
        """
        Determine the next page in the Wizard to go to.
        """
        self.application.process_events()
        if self.currentId() == FirstTimePage.Plugins:
            if not self.webAccess:
                return FirstTimePage.NoInternet
            else:
                return FirstTimePage.Songs
        elif self.currentId() == FirstTimePage.Progress:
            return -1
        elif self.currentId() == FirstTimePage.NoInternet:
            return FirstTimePage.Progress
        elif self.currentId() == FirstTimePage.Themes:
            self.application.set_busy_cursor()
            while not self.themeScreenshotThread.isFinished():
                time.sleep(0.1)
                self.application.process_events()
            # Build the screenshot icons, as this can not be done in the thread.
            self._buildThemeScreenshots()
            self.application.set_normal_cursor()
            return FirstTimePage.Defaults
        else:
            return self.currentId() + 1

    def onCurrentIdChanged(self, pageId):
        """
        Detects Page changes and updates as appropriate.
        """
        # Keep track of the page we are at.  Triggering "Cancel" causes pageId
        # to be a -1.
        self.application.process_events()
        if pageId != -1:
            self.lastId = pageId
        if pageId == FirstTimePage.Plugins:
            # Set the no internet page text.
            if self.hasRunWizard:
                self.noInternetLabel.setText(self.noInternetText)
            else:
                self.noInternetLabel.setText(self.noInternetText + self.cancelWizardText)
        elif pageId == FirstTimePage.Defaults:
            self.themeComboBox.clear()
            for iter in xrange(self.themesListWidget.count()):
                item = self.themesListWidget.item(iter)
                if item.checkState() == QtCore.Qt.Checked:
                    self.themeComboBox.addItem(item.text())
            if self.hasRunWizard:
                # Add any existing themes to list.
                for theme in self.theme_manager.get_themes():
                    index = self.themeComboBox.findText(theme)
                    if index == -1:
                        self.themeComboBox.addItem(theme)
                default_theme = Settings().value(u'themes/global theme')
                # Pre-select the current default theme.
                index = self.themeComboBox.findText(default_theme)
                self.themeComboBox.setCurrentIndex(index)
        elif pageId == FirstTimePage.NoInternet:
            self.backButton.setVisible(False)
            self.nextButton.setVisible(False)
            self.noInternetFinishButton.setVisible(True)
            if self.hasRunWizard:
                self.cancelButton.setVisible(False)
        elif pageId == FirstTimePage.Progress:
            self.application.set_busy_cursor()
            self.repaint()
            self.application.process_events()
            # Try to give the wizard a chance to redraw itself
            time.sleep(0.2)
            self._preWizard()
            self._performWizard()
            self._postWizard()
            self.application.set_normal_cursor()

    def updateScreenListCombo(self):
        """
        The user changed screen resolution or enabled/disabled more screens, so
        we need to update the combo box.
        """
        self.displayComboBox.clear()
        self.displayComboBox.addItems(self.screens.get_screen_list())
        self.displayComboBox.setCurrentIndex(self.displayComboBox.count() - 1)

    def onCancelButtonClicked(self):
        """
        Process the triggering of the cancel button.
        """
        if self.lastId == FirstTimePage.NoInternet or \
                (self.lastId <= FirstTimePage.Plugins and not self.hasRunWizard):
            QtCore.QCoreApplication.exit()
            sys.exit()
        self.was_download_cancelled = True
        while self.themeScreenshotThread.isRunning():
            time.sleep(0.1)
        self.application.set_normal_cursor()

    def onNoInternetFinishButtonClicked(self):
        """
        Process the triggering of the "Finish" button on the No Internet page.
        """
        self.application.set_busy_cursor()
        self._performWizard()
        self.application.set_normal_cursor()
        Settings().setValue(u'general/has run wizard', True)
        self.close()

    def urlGetFile(self, url, fpath):
        """"
        Download a file given a URL.  The file is retrieved in chunks, giving
        the ability to cancel the download at any point.
        """
        block_count = 0
        block_size = 4096
        urlfile = urllib2.urlopen(url)
        filename = open(fpath, "wb")
        # Download until finished or canceled.
        while not self.was_download_cancelled:
            data = urlfile.read(block_size)
            if not data:
                break
            filename.write(data)
            block_count += 1
            self._downloadProgress(block_count, block_size)
        filename.close()
        # Delete file if cancelled, it may be a partial file.
        if self.was_download_cancelled:
            os.remove(fpath)

    def _buildThemeScreenshots(self):
        """
        This method builds the theme screenshots' icons for all items in the
        ``self.themesListWidget``.
        """
        themes = self.config.get(u'themes', u'files')
        themes = themes.split(u',')
        for theme in themes:
            filename = self.config.get(u'theme_%s' % theme, u'filename')
            screenshot = self.config.get(u'theme_%s' % theme, u'screenshot')
            for index in xrange(self.themesListWidget.count()):
                item = self.themesListWidget.item(index)
                if item.data(QtCore.Qt.UserRole) == filename:
                    break
            item.setIcon(build_icon(os.path.join(unicode(gettempdir(), get_filesystem_encoding()), u'openlp',
                screenshot)))

    def _getFileSize(self, url):
        """
        Get the size of a file.

        ``url``
            The URL of the file we want to download.
        """
        site = urllib.urlopen(url)
        meta = site.info()
        return int(meta.getheaders("Content-Length")[0])

    def _downloadProgress(self, count, block_size):
        """
        Calculate and display the download progress.
        """
        increment = (count * block_size) - self.previous_size
        self._incrementProgressBar(None, increment)
        self.previous_size = count * block_size

    def _incrementProgressBar(self, status_text, increment=1):
        """
        Update the wizard progress page.

        ``status_text``
            Current status information to display.

        ``increment``
            The value to increment the progress bar by.
        """
        if status_text:
            self.progressLabel.setText(status_text)
        if increment > 0:
            self.progressBar.setValue(self.progressBar.value() + increment)
        self.application.process_events()

    def _preWizard(self):
        """
        Prepare the UI for the process.
        """
        self.max_progress = 0
        self.finishButton.setVisible(False)
        self.application.process_events()
        # Loop through the songs list and increase for each selected item
        for i in xrange(self.songsListWidget.count()):
            self.application.process_events()
            item = self.songsListWidget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                filename = item.data(QtCore.Qt.UserRole)
                size = self._getFileSize(u'%s%s' % (self.web, filename))
                self.max_progress += size
        # Loop through the Bibles list and increase for each selected item
        iterator = QtGui.QTreeWidgetItemIterator(self.biblesTreeWidget)
        while iterator.value():
            self.application.process_events()
            item = iterator.value()
            if item.parent() and item.checkState(0) == QtCore.Qt.Checked:
                filename = item.data(0, QtCore.Qt.UserRole)
                size = self._getFileSize(u'%s%s' % (self.web, filename))
                self.max_progress += size
            iterator += 1
        # Loop through the themes list and increase for each selected item
        for i in xrange(self.themesListWidget.count()):
            self.application.process_events()
            item = self.themesListWidget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                filename = item.data(QtCore.Qt.UserRole)
                size = self._getFileSize(u'%s%s' % (self.web, filename))
                self.max_progress += size
        if self.max_progress:
            # Add on 2 for plugins status setting plus a "finished" point.
            self.max_progress += 2
            self.progressBar.setValue(0)
            self.progressBar.setMinimum(0)
            self.progressBar.setMaximum(self.max_progress)
            self.progressPage.setTitle(translate('OpenLP.FirstTimeWizard', 'Setting Up And Downloading'))
            self.progressPage.setSubTitle(
                translate('OpenLP.FirstTimeWizard', 'Please wait while OpenLP is set up and your data is downloaded.'))
        else:
            self.progressBar.setVisible(False)
            self.progressPage.setTitle(translate('OpenLP.FirstTimeWizard', 'Setting Up'))
            self.progressPage.setSubTitle(u'Setup complete.')
        self.repaint()
        self.application.process_events()
        # Try to give the wizard a chance to repaint itself
        time.sleep(0.1)

    def _postWizard(self):
        """
        Clean up the UI after the process has finished.
        """
        if self.max_progress:
            self.progressBar.setValue(self.progressBar.maximum())
            if self.hasRunWizard:
                self.progressLabel.setText(translate('OpenLP.FirstTimeWizard',
                    'Download complete. Click the finish button to return to OpenLP.'))
            else:
                self.progressLabel.setText(translate('OpenLP.FirstTimeWizard',
                    'Download complete. Click the finish button to start OpenLP.'))
        else:
            if self.hasRunWizard:
                self.progressLabel.setText(translate('OpenLP.FirstTimeWizard',
                    'Click the finish button to return to OpenLP.'))
            else:
                self.progressLabel.setText(translate('OpenLP.FirstTimeWizard',
                    'Click the finish button to start OpenLP.'))
        self.finishButton.setVisible(True)
        self.finishButton.setEnabled(True)
        self.cancelButton.setVisible(False)
        self.nextButton.setVisible(False)
        self.application.process_events()

    def _performWizard(self):
        """
        Run the tasks in the wizard.
        """
        # Set plugin states
        self._incrementProgressBar(translate('OpenLP.FirstTimeWizard', 'Enabling selected plugins...'))
        self._setPluginStatus(self.songsCheckBox, u'songs/status')
        self._setPluginStatus(self.bibleCheckBox, u'bibles/status')
        # TODO Presentation plugin is not yet working on Mac OS X.
        # For now just ignore it.
        if sys.platform != 'darwin':
            self._setPluginStatus(self.presentationCheckBox, u'presentations/status')
        self._setPluginStatus(self.imageCheckBox, u'images/status')
        self._setPluginStatus(self.mediaCheckBox, u'media/status')
        self._setPluginStatus(self.remoteCheckBox, u'remotes/status')
        self._setPluginStatus(self.customCheckBox, u'custom/status')
        self._setPluginStatus(self.songUsageCheckBox, u'songusage/status')
        self._setPluginStatus(self.alertCheckBox, u'alerts/status')
        if self.webAccess:
            # Build directories for downloads
            songs_destination = os.path.join(
                unicode(gettempdir(), get_filesystem_encoding()), u'openlp')
            bibles_destination = AppLocation.get_section_data_path(u'bibles')
            themes_destination = AppLocation.get_section_data_path(u'themes')
            # Download songs
            for i in xrange(self.songsListWidget.count()):
                item = self.songsListWidget.item(i)
                if item.checkState() == QtCore.Qt.Checked:
                    filename = item.data(QtCore.Qt.UserRole)
                    self._incrementProgressBar(self.downloading % filename, 0)
                    self.previous_size = 0
                    destination = os.path.join(songs_destination, unicode(filename))
                    self.urlGetFile(u'%s%s' % (self.web, filename), destination)
            # Download Bibles
            bibles_iterator = QtGui.QTreeWidgetItemIterator(
                self.biblesTreeWidget)
            while bibles_iterator.value():
                item = bibles_iterator.value()
                if item.parent() and item.checkState(0) == QtCore.Qt.Checked:
                    bible = item.data(0, QtCore.Qt.UserRole)
                    self._incrementProgressBar(self.downloading % bible, 0)
                    self.previous_size = 0
                    self.urlGetFile(u'%s%s' % (self.web, bible), os.path.join(bibles_destination, bible))
                bibles_iterator += 1
            # Download themes
            for i in xrange(self.themesListWidget.count()):
                item = self.themesListWidget.item(i)
                if item.checkState() == QtCore.Qt.Checked:
                    theme = item.data(QtCore.Qt.UserRole)
                    self._incrementProgressBar(self.downloading % theme, 0)
                    self.previous_size = 0
                    self.urlGetFile(u'%s%s' % (self.web, theme), os.path.join(themes_destination, theme))
        # Set Default Display
        if self.displayComboBox.currentIndex() != -1:
            Settings().setValue(u'General/monitor', self.displayComboBox.currentIndex())
            self.screens.set_current_display(self.displayComboBox.currentIndex())
        # Set Global Theme
        if self.themeComboBox.currentIndex() != -1:
            Settings().setValue(u'themes/global theme', self.themeComboBox.currentText())

    def _setPluginStatus(self, field, tag):
        """
        Set the status of a plugin.
        """
        status = PluginStatus.Active if field.checkState() == QtCore.Qt.Checked else PluginStatus.Inactive
        Settings().setValue(tag, status)

    def _get_theme_manager(self):
        """
        Adds the theme manager to the class dynamically
        """
        if not hasattr(self, u'_theme_manager'):
            self._theme_manager = Registry().get(u'theme_manager')
        return self._theme_manager

    theme_manager = property(_get_theme_manager)

    def _get_application(self):
        """
        Adds the openlp to the class dynamically
        """
        if not hasattr(self, u'_application'):
            self._application = Registry().get(u'application')
        return self._application

    application = property(_get_application)
