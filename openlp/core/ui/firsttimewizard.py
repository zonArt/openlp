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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate
from openlp.core.lib.ui import add_welcome_page

class FirstTimePage(object):
    Welcome = 0
    Plugins = 1
    NoInternet = 2
    Songs = 3
    Bibles = 4
    Defaults = 5


class Ui_FirstTimeWizard(object):
    def setupUi(self, FirstTimeWizard):
        FirstTimeWizard.setObjectName(u'FirstTimeWizard')
        FirstTimeWizard.resize(550, 386)
        FirstTimeWizard.setModal(True)
        FirstTimeWizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        FirstTimeWizard.setOptions(QtGui.QWizard.IndependentPages|
            QtGui.QWizard.NoBackButtonOnStartPage)
        self.finishButton = self.button(QtGui.QWizard.FinishButton)
        self.cancelButton = self.button(QtGui.QWizard.CancelButton)
        self.nextButton = self.button(QtGui.QWizard.NextButton)
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
        self.noInternetLayout.setContentsMargins(50, 40, 50, 40)
        self.noInternetLayout.setObjectName(u'noInternetLayout')
        self.noInternetLabel = QtGui.QLabel(self.noInternetPage)
        self.noInternetLabel.setWordWrap(True)
        self.noInternetLabel.setObjectName(u'noInternetLabel')
        self.noInternetLayout.addWidget(self.noInternetLabel)
        FirstTimeWizard.setPage(FirstTimePage.NoInternet, self.noInternetPage)

        # The song samples page
        self.songsPage = QtGui.QWizardPage()
        self.songsPage.setObjectName(u'songsPage')
        FirstTimeWizard.setPage(FirstTimePage.Songs, self.songsPage)

        # download page
        self.biblesPage = QtGui.QWizardPage()
        self.biblesPage.setObjectName(u'biblesPage')
        self.internetGroupBox = QtGui.QGroupBox(self.biblesPage)
        self.internetGroupBox.setGeometry(QtCore.QRect(20, 10, 501, 271))
        self.internetGroupBox.setObjectName(u'internetGroupBox')
        self.pluginLayout_4 = QtGui.QVBoxLayout(self.internetGroupBox)
        self.pluginLayout_4.setObjectName(u'pluginLayout_4')
        self.selectionTreeWidget = QtGui.QTreeWidget(self.internetGroupBox)
        self.selectionTreeWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.selectionTreeWidget.setProperty(u'showDropIndicator', False)
        self.selectionTreeWidget.setAlternatingRowColors(True)
        self.selectionTreeWidget.setObjectName(u'selectionTreeWidget')
        self.selectionTreeWidget.headerItem().setText(0, u'1')
        self.selectionTreeWidget.header().setVisible(False)
        self.pluginLayout_4.addWidget(self.selectionTreeWidget)
        FirstTimeWizard.setPage(FirstTimePage.Bibles, self.biblesPage)

        self.DefaultsPage = QtGui.QWizardPage()
        self.DefaultsPage.setObjectName(u'DefaultsPage')
        self.layoutWidget = QtGui.QWidget(self.DefaultsPage)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 491, 113))
        self.layoutWidget.setObjectName(u'layoutWidget')
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(u'gridLayout')
        self.displaySelectionLabel = QtGui.QLabel(self.layoutWidget)
        self.displaySelectionLabel.setObjectName(u'displaySelectionLabel')
        self.gridLayout.addWidget(self.displaySelectionLabel, 0, 0, 1, 1)
        self.displaySelectionComboBox = QtGui.QComboBox(self.layoutWidget)
        self.displaySelectionComboBox.setEditable(False)
        self.displaySelectionComboBox.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.displaySelectionComboBox.setSizeAdjustPolicy(
            QtGui.QComboBox.AdjustToContents)
        self.displaySelectionComboBox.setObjectName(u'displaySelectionComboBox')
        self.gridLayout.addWidget(self.displaySelectionComboBox, 0, 1, 1, 1)
        self.themeSelectionLabel = QtGui.QLabel(self.layoutWidget)
        self.themeSelectionLabel.setObjectName(u'themeSelectionLabel')
        self.gridLayout.addWidget(self.themeSelectionLabel, 1, 0, 1, 1)
        self.themeSelectionComboBox = QtGui.QComboBox(self.layoutWidget)
        self.themeSelectionComboBox.setSizeAdjustPolicy(
            QtGui.QComboBox.AdjustToContents)
        self.themeSelectionComboBox.setObjectName(u'themeSelectionComboBox')
        self.gridLayout.addWidget(self.themeSelectionComboBox, 1, 1, 1, 1)
        self.messageLabel = QtGui.QLabel(self.DefaultsPage)
        self.messageLabel.setGeometry(QtCore.QRect(60, 160, 471, 17))
        self.messageLabel.setObjectName(u'messageLabel')
        self.updateLabel = QtGui.QLabel(self.DefaultsPage)
        self.updateLabel.setGeometry(QtCore.QRect(60, 220, 351, 17))
        self.updateLabel.setObjectName(u'updateLabel')
        FirstTimeWizard.setPage(FirstTimePage.Defaults, self.DefaultsPage)

        self.retranslateUi(FirstTimeWizard)
        QtCore.QMetaObject.connectSlotsByName(FirstTimeWizard)

    def retranslateUi(self, FirstTimeWizard):
        FirstTimeWizard.setWindowTitle(translate(
            'OpenLP.FirstTimeWizard', 'First Time Wizard'))
        self.titleLabel.setText(
            u'<span style="font-size:14pt; font-weight:600;">%s</span>' % \
            translate('OpenLP.FirstTimeWizard',
            'Welcome to the First Time Wizard'))
        self.informationLabel.setText(translate('OpenLP.FirstTimeWizard',
            'This wizard will help you to configure OpenLP for initial use .'
            ' Click the next button below to start the process of selection '
            'your initial options. '))
        self.pluginPage.setTitle(translate('OpenLP.FirstTimeWizard',
            'Activate required Plugins'))
        self.pluginPage.setSubTitle(translate('OpenLP.FirstTimeWizard',
            'Select the Plugins you wish to use. '))
        self.songsCheckBox.setText(translate('OpenLP.FirstTimeWizard', 'Songs'))
        self.customCheckBox.setText(translate('OpenLP.FirstTimeWizard',
            'Custom Text'))
        self.bibleCheckBox.setText(translate('OpenLP.FirstTimeWizard', 'Bible'))
        self.imageCheckBox.setText(translate('OpenLP.FirstTimeWizard',
            'Images'))
        self.presentationCheckBox.setText(translate('OpenLP.FirstTimeWizard',
            'Presentations'))
        self.mediaCheckBox.setText(translate('OpenLP.FirstTimeWizard',
            'Media (Audio and Video)'))
        self.remoteCheckBox.setText(translate('OpenLP.FirstTimeWizard',
            'Allow remote access'))
        self.songUsageCheckBox.setText(translate('OpenLP.FirstTimeWizard',
            'Monitor Song Usage'))
        self.alertCheckBox.setText(translate('OpenLP.FirstTimeWizard',
            'Allow Alerts'))
        self.noInternetPage.setTitle(translate('OpenLP.FirstTimeWizard',
            'No Internet Connection'))
        self.noInternetPage.setSubTitle(translate(
            'OpenLP.FirstTimeWizard',
            'Unable to detect an Internet connection.'))
        self.noInternetLabel.setText(translate('OpenLP.FirstTimeWizard',
            'No Internet connection was found. The First Time Wizard needs an '
            'Internet connection in order to be able to download sample '
            'songs, Bibles and themes.\n\nTo re-run the First Time Wizard and '
            'import this sample data at a later stage, press the cancel '
            'button now, check your Internet connection, and restart OpenLP.'
            '\n\nTo cancel the First Time Wizard completely, press the finish '
            'button now.'))
        self.songsPage.setTitle(translate('OpenLP.FirstTimeWizard',
            'Sample Songs'))
        self.songsPage.setSubTitle(translate(
            'OpenLP.FirstTimeWizard',
            'Select and download public domain songs.'))
        self.biblesPage.setTitle(translate('OpenLP.FirstTimeWizard',
            'Download Samples from OpenLP.org'))
        self.biblesPage.setSubTitle(translate(
            'OpenLP.FirstTimeWizard',
            'Select samples to downlaod and install for use.'))
        self.internetGroupBox.setTitle(translate('OpenLP.FirstTimeWizard',
            'Download Example Files'))
        self.DefaultsPage.setTitle(translate('OpenLP.FirstTimeWizard',
            'Default Settings'))
        self.DefaultsPage.setSubTitle(translate('OpenLP.FirstTimeWizard',
            'Set up default values to be used by OpenLP'))
        self.displaySelectionLabel.setText(translate('OpenLP.FirstTimeWizard',
            'Default output display'))
        self.themeSelectionLabel.setText(translate('OpenLP.FirstTimeWizard',
            'Select the default Theme'))
        self.messageLabel.setText(translate('OpenLP.FirstTimeWizard',
            'Press finish to apply all your changes and start OpenLP'))
