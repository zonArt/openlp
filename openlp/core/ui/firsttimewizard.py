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
The UI widgets for the first time wizard.
"""
from PyQt4 import QtCore, QtGui

import sys

from openlp.core.lib import translate
from openlp.core.lib.ui import add_welcome_page


class FirstTimePage(object):
    """
    An enumeration class with each of the pages of the wizard.
    """
    Welcome = 0
    Plugins = 1
    NoInternet = 2
    Songs = 3
    Bibles = 4
    Themes = 5
    Defaults = 6
    Progress = 7


class Ui_FirstTimeWizard(object):
    """
    The UI widgets for the first time wizard.
    """
    def setupUi(self, FirstTimeWizard):
        """
        Set up the UI.
        """
        FirstTimeWizard.setObjectName(u'FirstTimeWizard')
        FirstTimeWizard.resize(550, 386)
        FirstTimeWizard.setModal(True)
        FirstTimeWizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        FirstTimeWizard.setOptions(QtGui.QWizard.IndependentPages | QtGui.QWizard.NoBackButtonOnStartPage |
            QtGui.QWizard.NoBackButtonOnLastPage | QtGui.QWizard.HaveCustomButton1)
        self.finishButton = self.button(QtGui.QWizard.FinishButton)
        self.noInternetFinishButton = self.button(QtGui.QWizard.CustomButton1)
        self.cancelButton = self.button(QtGui.QWizard.CancelButton)
        self.nextButton = self.button(QtGui.QWizard.NextButton)
        self.backButton = self.button(QtGui.QWizard.BackButton)
        add_welcome_page(FirstTimeWizard, u':/wizards/wizard_firsttime.bmp')
        # The plugins page
        self.pluginPage = QtGui.QWizardPage()
        self.pluginPage.setObjectName(u'pluginPage')
        self.pluginLayout = QtGui.QVBoxLayout(self.pluginPage)
        self.pluginLayout.setContentsMargins(40, 15, 40, 0)
        self.pluginLayout.setObjectName(u'pluginLayout')
        self.songsCheckBox = QtGui.QCheckBox(self.pluginPage)
        self.songsCheckBox.setChecked(True)
        self.songsCheckBox.setObjectName(u'songsCheckBox')
        self.pluginLayout.addWidget(self.songsCheckBox)
        self.customCheckBox = QtGui.QCheckBox(self.pluginPage)
        self.customCheckBox.setChecked(True)
        self.customCheckBox.setObjectName(u'customCheckBox')
        self.pluginLayout.addWidget(self.customCheckBox)
        self.bibleCheckBox = QtGui.QCheckBox(self.pluginPage)
        self.bibleCheckBox.setChecked(True)
        self.bibleCheckBox.setObjectName(u'bibleCheckBox')
        self.pluginLayout.addWidget(self.bibleCheckBox)
        self.imageCheckBox = QtGui.QCheckBox(self.pluginPage)
        self.imageCheckBox.setChecked(True)
        self.imageCheckBox.setObjectName(u'imageCheckBox')
        self.pluginLayout.addWidget(self.imageCheckBox)
        # TODO Presentation plugin is not yet working on Mac OS X.
        # For now just ignore it.
        if sys.platform != 'darwin':
            self.presentationCheckBox = QtGui.QCheckBox(self.pluginPage)
            self.presentationCheckBox.setChecked(True)
            self.presentationCheckBox.setObjectName(u'presentationCheckBox')
            self.pluginLayout.addWidget(self.presentationCheckBox)
        self.mediaCheckBox = QtGui.QCheckBox(self.pluginPage)
        self.mediaCheckBox.setChecked(True)
        self.mediaCheckBox.setObjectName(u'mediaCheckBox')
        self.pluginLayout.addWidget(self.mediaCheckBox)
        self.remoteCheckBox = QtGui.QCheckBox(self.pluginPage)
        self.remoteCheckBox.setObjectName(u'remoteCheckBox')
        self.pluginLayout.addWidget(self.remoteCheckBox)
        self.songUsageCheckBox = QtGui.QCheckBox(self.pluginPage)
        self.songUsageCheckBox.setChecked(True)
        self.songUsageCheckBox.setObjectName(u'songUsageCheckBox')
        self.pluginLayout.addWidget(self.songUsageCheckBox)
        self.alertCheckBox = QtGui.QCheckBox(self.pluginPage)
        self.alertCheckBox.setChecked(True)
        self.alertCheckBox.setObjectName(u'alertCheckBox')
        self.pluginLayout.addWidget(self.alertCheckBox)
        FirstTimeWizard.setPage(FirstTimePage.Plugins, self.pluginPage)
        # The "you don't have an internet connection" page.
        self.noInternetPage = QtGui.QWizardPage()
        self.noInternetPage.setObjectName(u'noInternetPage')
        self.noInternetLayout = QtGui.QVBoxLayout(self.noInternetPage)
        self.noInternetLayout.setContentsMargins(50, 30, 50, 40)
        self.noInternetLayout.setObjectName(u'noInternetLayout')
        self.noInternetLabel = QtGui.QLabel(self.noInternetPage)
        self.noInternetLabel.setWordWrap(True)
        self.noInternetLabel.setObjectName(u'noInternetLabel')
        self.noInternetLayout.addWidget(self.noInternetLabel)
        FirstTimeWizard.setPage(FirstTimePage.NoInternet, self.noInternetPage)
        # The song samples page
        self.songsPage = QtGui.QWizardPage()
        self.songsPage.setObjectName(u'songsPage')
        self.songsLayout = QtGui.QVBoxLayout(self.songsPage)
        self.songsLayout.setContentsMargins(50, 20, 50, 20)
        self.songsLayout.setObjectName(u'songsLayout')
        self.songsListWidget = QtGui.QListWidget(self.songsPage)
        self.songsListWidget.setAlternatingRowColors(True)
        self.songsListWidget.setObjectName(u'songsListWidget')
        self.songsLayout.addWidget(self.songsListWidget)
        FirstTimeWizard.setPage(FirstTimePage.Songs, self.songsPage)
        # The Bible samples page
        self.biblesPage = QtGui.QWizardPage()
        self.biblesPage.setObjectName(u'biblesPage')
        self.biblesLayout = QtGui.QVBoxLayout(self.biblesPage)
        self.biblesLayout.setContentsMargins(50, 20, 50, 20)
        self.biblesLayout.setObjectName(u'biblesLayout')
        self.biblesTreeWidget = QtGui.QTreeWidget(self.biblesPage)
        self.biblesTreeWidget.setAlternatingRowColors(True)
        self.biblesTreeWidget.header().setVisible(False)
        self.biblesTreeWidget.setObjectName(u'biblesTreeWidget')
        self.biblesLayout.addWidget(self.biblesTreeWidget)
        FirstTimeWizard.setPage(FirstTimePage.Bibles, self.biblesPage)
        # The theme samples page
        self.themesPage = QtGui.QWizardPage()
        self.themesPage.setObjectName(u'themesPage')
        self.themesLayout = QtGui.QVBoxLayout(self.themesPage)
        self.themesLayout.setContentsMargins(20, 50, 20, 60)
        self.themesLayout.setObjectName(u'themesLayout')
        self.themesListWidget = QtGui.QListWidget(self.themesPage)
        self.themesListWidget.setViewMode(QtGui.QListView.IconMode)
        self.themesListWidget.setMovement(QtGui.QListView.Static)
        self.themesListWidget.setFlow(QtGui.QListView.LeftToRight)
        self.themesListWidget.setSpacing(4)
        self.themesListWidget.setUniformItemSizes(True)
        self.themesListWidget.setIconSize(QtCore.QSize(133, 100))
        self.themesListWidget.setWrapping(False)
        self.themesListWidget.setObjectName(u'themesListWidget')
        self.themesLayout.addWidget(self.themesListWidget)
        FirstTimeWizard.setPage(FirstTimePage.Themes, self.themesPage)
        # the default settings page
        self.defaultsPage = QtGui.QWizardPage()
        self.defaultsPage.setObjectName(u'defaultsPage')
        self.defaultsLayout = QtGui.QFormLayout(self.defaultsPage)
        self.defaultsLayout.setContentsMargins(50, 20, 50, 20)
        self.defaultsLayout.setObjectName(u'defaultsLayout')
        self.displayLabel = QtGui.QLabel(self.defaultsPage)
        self.displayLabel.setObjectName(u'displayLabel')
        self.displayComboBox = QtGui.QComboBox(self.defaultsPage)
        self.displayComboBox.setEditable(False)
        self.displayComboBox.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.displayComboBox.setObjectName(u'displayComboBox')
        self.defaultsLayout.addRow(self.displayLabel, self.displayComboBox)
        self.themeLabel = QtGui.QLabel(self.defaultsPage)
        self.themeLabel.setObjectName(u'themeLabel')
        self.themeComboBox = QtGui.QComboBox(self.defaultsPage)
        self.themeComboBox.setEditable(False)
        self.themeComboBox.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.themeComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.themeComboBox.setObjectName(u'themeComboBox')
        self.defaultsLayout.addRow(self.themeLabel, self.themeComboBox)
        FirstTimeWizard.setPage(FirstTimePage.Defaults, self.defaultsPage)
        # Progress page
        self.progressPage = QtGui.QWizardPage()
        self.progressPage.setObjectName(u'progressPage')
        self.progressLayout = QtGui.QVBoxLayout(self.progressPage)
        self.progressLayout.setMargin(48)
        self.progressLayout.setObjectName(u'progressLayout')
        self.progressLabel = QtGui.QLabel(self.progressPage)
        self.progressLabel.setObjectName(u'progressLabel')
        self.progressLayout.addWidget(self.progressLabel)
        self.progressBar = QtGui.QProgressBar(self.progressPage)
        self.progressBar.setObjectName(u'progressBar')
        self.progressLayout.addWidget(self.progressBar)
        FirstTimeWizard.setPage(FirstTimePage.Progress, self.progressPage)
        self.retranslateUi(FirstTimeWizard)

    def retranslateUi(self, FirstTimeWizard):
        """
        Translate the UI on the fly
        """
        FirstTimeWizard.setWindowTitle(translate(
            'OpenLP.FirstTimeWizard', 'First Time Wizard'))
        self.titleLabel.setText(u'<span style="font-size:14pt; font-weight:600;">%s</span>' %
            translate('OpenLP.FirstTimeWizard', 'Welcome to the First Time Wizard'))
        self.informationLabel.setText(translate('OpenLP.FirstTimeWizard',
            'This wizard will help you to configure OpenLP for initial use.'
            ' Click the next button below to start.'))
        self.pluginPage.setTitle(translate('OpenLP.FirstTimeWizard', 'Activate required Plugins'))
        self.pluginPage.setSubTitle(translate('OpenLP.FirstTimeWizard', 'Select the Plugins you wish to use. '))
        self.songsCheckBox.setText(translate('OpenLP.FirstTimeWizard', 'Songs'))
        self.customCheckBox.setText(translate('OpenLP.FirstTimeWizard', 'Custom Slides'))
        self.bibleCheckBox.setText(translate('OpenLP.FirstTimeWizard', 'Bible'))
        self.imageCheckBox.setText(translate('OpenLP.FirstTimeWizard', 'Images'))
        # TODO Presentation plugin is not yet working on Mac OS X.
        # For now just ignore it.
        if sys.platform != 'darwin':
            self.presentationCheckBox.setText(translate('OpenLP.FirstTimeWizard', 'Presentations'))
        self.mediaCheckBox.setText(translate('OpenLP.FirstTimeWizard', 'Media (Audio and Video)'))
        self.remoteCheckBox.setText(translate('OpenLP.FirstTimeWizard', 'Allow remote access'))
        self.songUsageCheckBox.setText(translate('OpenLP.FirstTimeWizard', 'Monitor Song Usage'))
        self.alertCheckBox.setText(translate('OpenLP.FirstTimeWizard', 'Allow Alerts'))
        self.noInternetPage.setTitle(translate('OpenLP.FirstTimeWizard', 'No Internet Connection'))
        self.noInternetPage.setSubTitle(translate('OpenLP.FirstTimeWizard', 'Unable to detect an Internet connection.'))
        self.noInternetText = translate('OpenLP.FirstTimeWizard',
            'No Internet connection was found. The First Time Wizard needs an '
            'Internet connection in order to be able to download sample '
            'songs, Bibles and themes.  Click the Finish button now to start '
            'OpenLP with initial settings and no sample data.\n\nTo re-run the '
            'First Time Wizard and import this sample data at a later time, '
            'check your Internet connection and re-run this wizard by '
            'selecting "Tools/Re-run First Time Wizard" from OpenLP.')
        self.cancelWizardText = translate('OpenLP.FirstTimeWizard',
            '\n\nTo cancel the First Time Wizard completely (and not start '
            'OpenLP), click the Cancel button now.')
        self.songsPage.setTitle(translate('OpenLP.FirstTimeWizard', 'Sample Songs'))
        self.songsPage.setSubTitle(translate('OpenLP.FirstTimeWizard', 'Select and download public domain songs.'))
        self.biblesPage.setTitle(translate('OpenLP.FirstTimeWizard', 'Sample Bibles'))
        self.biblesPage.setSubTitle(translate('OpenLP.FirstTimeWizard', 'Select and download free Bibles.'))
        self.themesPage.setTitle(translate('OpenLP.FirstTimeWizard', 'Sample Themes'))
        self.themesPage.setSubTitle(translate('OpenLP.FirstTimeWizard', 'Select and download sample themes.'))
        self.defaultsPage.setTitle(translate('OpenLP.FirstTimeWizard', 'Default Settings'))
        self.defaultsPage.setSubTitle(translate('OpenLP.FirstTimeWizard',
            'Set up default settings to be used by OpenLP.'))
        self.displayLabel.setText(translate('OpenLP.FirstTimeWizard', 'Default output display:'))
        self.themeLabel.setText(translate('OpenLP.FirstTimeWizard', 'Select default theme:'))
        self.progressLabel.setText(translate('OpenLP.FirstTimeWizard', 'Starting configuration process...'))
        FirstTimeWizard.setButtonText(QtGui.QWizard.CustomButton1, translate('OpenLP.FirstTimeWizard', 'Finish'))
