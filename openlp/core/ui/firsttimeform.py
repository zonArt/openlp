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
from ConfigParser import SafeConfigParser

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, PluginStatus, check_directory_exists, \
    Receiver
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
        self.webAccess = get_web_page(u'%s%s' % (self.web, u'download.cfg?%s' % randint(0, 20)))
        if self.webAccess:
            files = self.webAccess.read()
            self.config.readfp(io.BytesIO(files))
        for screen in screens.get_screen_list():
            self.displayComboBox.addItem(screen)
        self.songsText = translate('OpenLP.FirstTimeWizard', 'Songs')
        self.biblesText = translate('OpenLP.FirstTimeWizard', 'Bibles')
        self.themesText = translate('OpenLP.FirstTimeWizard', 'Themes')
        self.startUpdates = translate('OpenLP.FirstTimeWizard',
            'Starting Updates')
        self.downloading = unicode(translate('OpenLP.FirstTimeWizard',
            'Downloading %s'))
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
                item = QtGui.QListWidgetItem(title, self.themesListWidget)
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(filename))
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
            listIterator = QtGui.QTreeWidgetItemIterator(
                self.selectionTreeWidget)
            while listIterator.value():
                parent = listIterator.value().parent()
                if parent and \
                    listIterator.value().checkState(0) == QtCore.Qt.Checked:
                    if unicode(parent.text(0)) == self.themesText:
                        self.themeComboBox.addItem(
                            listIterator.value().text(0))
                listIterator += 1

    def accept(self):
        Receiver.send_message(u'cursor_busy')
        self._updateMessage(self.startUpdates)
        # Set up the Plugin status's
        self._pluginStatus(self.songsCheckBox, u'songs/status')
        self._pluginStatus(self.bibleCheckBox, u'bibles/status')
        self._pluginStatus(self.presentationCheckBox, u'presentations/status')
        self._pluginStatus(self.imageCheckBox, u'images/status')
        self._pluginStatus(self.mediaCheckBox, u'media/status')
        self._pluginStatus(self.remoteCheckBox, u'remotes/status')
        self._pluginStatus(self.customCheckBox, u'custom/status')
        self._pluginStatus(self.songUsageCheckBox, u'songusage/status')
        self._pluginStatus(self.alertCheckBox, u'alerts/status')
        # Build directories for downloads
        destination = AppLocation.get_temp_path()
        check_directory_exists(destination)
        bibles_destination = AppLocation.get_section_data_path(u'bibles')
        check_directory_exists(bibles_destination)
        themes_destination = AppLocation.get_section_data_path(u'themes')
        check_directory_exists(destination)
        # Install songs
        songs_iterator = QtGui.QListWidgetItemIterator(self.songsListWidget)
        while songs_iterator.value():
            item = songs_iterator.value()
            if item.checkState() == QtCore.Qt.Checked:
                filename = item.data(QtCore.Qt.UserRole).toString()
                urllib.urlretrieve(u'%s%s' % (self.web, filename),
                    os.path.join(destination, filename))
                #importer = SongImporter()
            songs_iterator += 1
        # Install Bibles
        bibles_iterator = QtGui.QTreeWidgetItemIterator(self.biblesTreeWidget)
        while bibles_iterator.value():
            item = bibles_iterator.value()
            if item.parent() and item.checkState(0) == QtCore.Qt.Checked:
                bible = unicode(item.data(0, QtCore.Qt.UserRole).toString())
                urllib.urlretrieve(u'%s%s' % (self.web, bible),
                    os.path.join(bibles_destination, bible))
            bibles_iterator += 1
        themes_iterator = QtGui.QListWidgetItemIterator(self.themesListWidget)
        while themes_iterator.value():
            item = themes_iterator.value()
            if item.checkState() == QtCore.Qt.Checked:
                theme = unicode(item.data(QtCore.Qt.UserRole).toString())
                urllib.urlretrieve(u'%s%s' % (self.web, theme),
                    os.path.join(theme_destination, theme))
            themes_iterator += 1
        # Set Default Display
        if self.displayComboBox.currentIndex() != -1:
            QtCore.QSettings().setValue(u'General/monitor',
                QtCore.QVariant(self.displayComboBox.currentIndex()))
        # Set Global Theme
        if self.themeComboBox.currentIndex() != -1:
            QtCore.QSettings().setValue(u'themes/global theme',
                QtCore.QVariant(self.themeComboBox.currentText()))
        QtCore.QSettings().setValue(u'general/first time',
            QtCore.QVariant(False))
        Receiver.send_message(u'cursor_normal')
        return QtGui.QWizard.accept(self)

    def _pluginStatus(self, field, tag):
        status = PluginStatus.Active if field.checkState() \
            == QtCore.Qt.Checked else PluginStatus.Inactive
        QtCore.QSettings().setValue(tag, QtCore.QVariant(status))

    def _updateMessage(self, text):
        """
        Keep screen up to date
        """
        self.updateLabel.setText(text)
        Receiver.send_message(u'openlp_process_events')
