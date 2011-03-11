# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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

import io
import logging
import os
import urllib
from random import randint
from tempfile import gettempdir
from ConfigParser import SafeConfigParser

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, PluginStatus, check_directory_exists, \
    Receiver, build_icon
from openlp.core.utils import get_web_page, AppLocation
from firsttimewizard import Ui_FirstTimeWizard, FirstTimePage

log = logging.getLogger(__name__)

class FirstTimeForm(QtGui.QWizard, Ui_FirstTimeWizard):
    """
    This is the Theme Import Wizard, which allows easy creation and editing of
    OpenLP themes.
    """
    log.info(u'ThemeWizardForm loaded')

    def __init__(self, screens, parent=None):
        QtGui.QWizard.__init__(self, parent)
        self.setupUi(self)
        # check to see if we have web access
        self.web = u'http://openlp.org/files/frw/'
        self.config = SafeConfigParser()
        self.webAccess = get_web_page(u'%s%s' % (self.web, u'download.cfg'))
        if self.webAccess:
            files = self.webAccess.read()
            self.config.readfp(io.BytesIO(files))
        for screen in screens.get_screen_list():
            self.displayComboBox.addItem(screen)
        self.downloading = unicode(translate('OpenLP.FirstTimeWizard',
            'Downloading %s...'))
        QtCore.QObject.connect(self,
            QtCore.SIGNAL(u'currentIdChanged(int)'),
            self.onCurrentIdChanged)

    def exec_(self, edit=False):
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
        # Sort out internet access for downloads
        if self.webAccess:
            songs = self.config.get(u'songs', u'languages')
            songs = songs.split(u',')
            for song in songs:
                title = unicode(self.config.get(
                    u'songs_%s' % song, u'title'), u'utf8')
                filename = unicode(self.config.get(
                    u'songs_%s' % song, u'filename'), u'utf8')
                item = QtGui.QListWidgetItem(title, self.songsListWidget)
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(filename))
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            bible_languages = self.config.get(u'bibles', u'languages')
            bible_languages = bible_languages.split(u',')
            for lang in bible_languages:
                language = unicode(self.config.get(
                    u'bibles_%s' % lang, u'title'), u'utf8')
                langItem = QtGui.QTreeWidgetItem(
                   self.biblesTreeWidget, QtCore.QStringList(language))
                bibles = self.config.get(u'bibles_%s' % lang, u'translations')
                bibles = bibles.split(u',')
                for bible in bibles:
                    title = unicode(self.config.get(
                        u'bible_%s' % bible, u'title'), u'utf8')
                    filename = unicode(self.config.get(
                        u'bible_%s' % bible, u'filename'))
                    item = QtGui.QTreeWidgetItem(
                       langItem, QtCore.QStringList(title))
                    item.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(filename))
                    item.setCheckState(0, QtCore.Qt.Unchecked)
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            self.biblesTreeWidget.expandAll()
            themes = self.config.get(u'themes', u'files')
            themes = themes.split(u',')
            for theme in themes:
                title = self.config.get(u'theme_%s' % theme, u'title')
                filename = self.config.get(u'theme_%s' % theme, u'filename')
                screenshot = self.config.get(u'theme_%s' % theme, u'screenshot')
                urllib.urlretrieve(u'%s/%s' % (self.web, screenshot),
                    os.path.join(gettempdir(), screenshot))
                item = QtGui.QListWidgetItem(title, self.themesListWidget)
                item.setData(QtCore.Qt.UserRole,
                    QtCore.QVariant(filename))
                item.setIcon(build_icon(
                    os.path.join(gettempdir(), screenshot)))
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)

    def nextId(self):
        """
        Determine the next page in the Wizard to go to.
        """
        if self.currentId() == FirstTimePage.Plugins:
            if not self.webAccess:
                return FirstTimePage.NoInternet
            else:
                return FirstTimePage.Songs
        elif self.currentId() == FirstTimePage.Progress:
            return -1
        else:
            return self.currentId() + 1

    def onCurrentIdChanged(self, pageId):
        """
        Detects Page changes and updates as approprate.
        """
        if pageId == FirstTimePage.NoInternet:
            self.finishButton.setVisible(True)
            self.finishButton.setEnabled(True)
            self.nextButton.setVisible(False)
        elif pageId == FirstTimePage.Defaults:
            self.themeComboBox.clear()
            for iter in xrange(self.themesListWidget.count()):
                item = self.themesListWidget.item(iter)
                if item.checkState() == QtCore.Qt.Checked:
                    self.themeComboBox.addItem(item.text())
        elif pageId == FirstTimePage.Progress:
            self._preWizard()
            self._performWizard()
            self._postWizard()

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
        Receiver.send_message(u'openlp_process_events')

    def _preWizard(self):
        """
        Prepare the UI for the process.
        """
        # We start on 9 for the 9 plugins
        max_progress = 9
        # Loop through the songs list and increase for each selected item
        for i in xrange(self.songsListWidget.count()):
            if self.songsListWidget.item(i).checkState() == QtCore.Qt.Checked:
                max_progress += 1
        # Loop through the Bibles list and increase for each selected item
        iterator = QtGui.QTreeWidgetItemIterator(self.biblesTreeWidget)
        while iterator.value():
            item = iterator.value()
            if item.parent() and item.checkState(0) == QtCore.Qt.Checked:
                max_progress += 1
            iterator += 1
        # Loop through the themes list and increase for each selected item
        for i in xrange(self.themesListWidget.count()):
            if self.themesListWidget.item(i).checkState() == QtCore.Qt.Checked:
                max_progress += 1
        self.finishButton.setVisible(False)
        self.progressBar.setValue(0)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(max_progress)

    def _postWizard(self):
        """
        Clean up the UI after the process has finished.
        """
        self.progressBar.setValue(self.progressBar.maximum())
        self.finishButton.setVisible(True)
        self.finishButton.setEnabled(True)
        self.cancelButton.setVisible(False)
        self.nextButton.setVisible(False)
        Receiver.send_message(u'openlp_process_events')

    def _performWizard(self):
        """
        Run the tasks in the wizard.
        """
        # Set plugin states
        self._incrementProgressBar(translate('OpenLP.FirstTimeWizard',
            'Enabling selected plugins...'))
        self._setPluginStatus(self.songsCheckBox, u'songs/status')
        self._incrementProgressBar(None)
        self._setPluginStatus(self.bibleCheckBox, u'bibles/status')
        self._incrementProgressBar(None)
        self._setPluginStatus(self.presentationCheckBox, u'presentations/status')
        self._incrementProgressBar(None)
        self._setPluginStatus(self.imageCheckBox, u'images/status')
        self._incrementProgressBar(None)
        self._setPluginStatus(self.mediaCheckBox, u'media/status')
        self._incrementProgressBar(None)
        self._setPluginStatus(self.remoteCheckBox, u'remotes/status')
        self._incrementProgressBar(None)
        self._setPluginStatus(self.customCheckBox, u'custom/status')
        self._incrementProgressBar(None)
        self._setPluginStatus(self.songUsageCheckBox, u'songusage/status')
        self._incrementProgressBar(None)
        self._setPluginStatus(self.alertCheckBox, u'alerts/status')
        # Build directories for downloads
        songs_destination = AppLocation.get_section_data_path(u'songs')
        bibles_destination = AppLocation.get_section_data_path(u'bibles')
        themes_destination = AppLocation.get_section_data_path(u'themes')
        # Install songs
        for i in xrange(self.songsListWidget.count()):
            item = self.songsListWidget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                filename = item.data(QtCore.Qt.UserRole).toString()
                self._incrementProgressBar(self.downloading % filename)
                destination = os.path.join(songs_destination, u'songs.sqlite')
                if os.path.exists(destination):
                    if QtGui.QMessageBox.question(self,
                        translate('OpenLP.FirstTimeWizard',
                        'Overwrite Existing Songs?'),
                        translate('OpenLP.FirstTimeWizard', 'Your songs '
                        'database already exists and your current songs will '
                        'be permanently lost, are you sure you want to '
                        'replace it ?'),
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                        QtGui.QMessageBox.No) != QtGui.QMessageBox.Yes:
                        continue
                urllib.urlretrieve(u'%s%s' % (self.web, filename), destination)
        # Install Bibles
        bibles_iterator = QtGui.QTreeWidgetItemIterator(self.biblesTreeWidget)
        while bibles_iterator.value():
            item = bibles_iterator.value()
            if item.parent() and item.checkState(0) == QtCore.Qt.Checked:
                bible = unicode(item.data(0, QtCore.Qt.UserRole).toString())
                self._incrementProgressBar(self.downloading % bible)
                urllib.urlretrieve(u'%s%s' % (self.web, bible),
                    os.path.join(bibles_destination, bible))
            bibles_iterator += 1
        # Install themes
        for i in xrange(self.themesListWidget.count()):
            item = self.themesListWidget.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                theme = unicode(item.data(QtCore.Qt.UserRole).toString())
                self._incrementProgressBar(self.downloading % theme)
                urllib.urlretrieve(u'%s%s' % (self.web, theme),
                    os.path.join(themes_destination, theme))
        # Set Default Display
        if self.displayComboBox.currentIndex() != -1:
            QtCore.QSettings().setValue(u'General/monitor',
                QtCore.QVariant(self.displayComboBox.currentIndex()))
        # Set Global Theme
        if self.themeComboBox.currentIndex() != -1:
            QtCore.QSettings().setValue(u'themes/global theme',
                QtCore.QVariant(self.themeComboBox.currentText()))
        QtCore.QSettings().setValue(u'general/has run wizard',
            QtCore.QVariant(True))

    def _setPluginStatus(self, field, tag):
        status = PluginStatus.Active if field.checkState() \
            == QtCore.Qt.Checked else PluginStatus.Inactive
        QtCore.QSettings().setValue(tag, QtCore.QVariant(status))

