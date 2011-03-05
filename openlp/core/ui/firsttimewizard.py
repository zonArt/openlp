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


class Ui_FirstTimeWizard(object):
    def setupUi(self, FirstTimeWizard):
        FirstTimeWizard.setObjectName(u'FirstTimeWizard')
        FirstTimeWizard.resize(550, 386)
        FirstTimeWizard.setModal(True)
        FirstTimeWizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        FirstTimeWizard.setOptions(QtGui.QWizard.IndependentPages|
            QtGui.QWizard.NoBackButtonOnStartPage)
        self.welcomePage = QtGui.QWizardPage()
        self.welcomePage.setTitle(u'')
        self.welcomePage.setSubTitle(u'')
        self.welcomePage.setObjectName(u'welcomePage')
        self.welcomeLayout = QtGui.QHBoxLayout(self.welcomePage)
        self.welcomeLayout.setSpacing(8)
        self.welcomeLayout.setMargin(0)
        self.welcomeLayout.setObjectName(u'welcomeLayout')
        self.importBibleImage = QtGui.QLabel(self.welcomePage)
        self.importBibleImage.setMinimumSize(QtCore.QSize(163, 0))
        self.importBibleImage.setMaximumSize(QtCore.QSize(163, 16777215))
        self.importBibleImage.setLineWidth(0)
        self.importBibleImage.setText(u'')
        self.importBibleImage.setPixmap(
            QtGui.QPixmap(u':/wizards/wizard_importbible.bmp'))
        self.importBibleImage.setIndent(0)
        self.importBibleImage.setObjectName(u'importBibleImage')
        self.welcomeLayout.addWidget(self.importBibleImage)
        self.welcomePageLayout = QtGui.QVBoxLayout()
        self.welcomePageLayout.setSpacing(8)
        self.welcomePageLayout.setObjectName(u'welcomePageLayout')
        self.titleLabel = QtGui.QLabel(self.welcomePage)
        self.titleLabel.setObjectName(u'titleLabel')
        self.welcomePageLayout.addWidget(self.titleLabel)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        self.welcomePageLayout.addItem(spacerItem)
        self.informationLabel = QtGui.QLabel(self.welcomePage)
        self.informationLabel.setWordWrap(True)
        self.informationLabel.setMargin(10)
        self.informationLabel.setObjectName(u'informationLabel')
        self.welcomePageLayout.addWidget(self.informationLabel)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.welcomePageLayout.addItem(spacerItem1)
        self.welcomeLayout.addLayout(self.welcomePageLayout)
        FirstTimeWizard.addPage(self.welcomePage)
        self.PluginPagePage = QtGui.QWizardPage()
        self.PluginPagePage.setObjectName(u'PluginPagePage')
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.PluginPagePage)
        self.verticalLayout_2.setObjectName(u'verticalLayout_2')
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.songsCheckBox = QtGui.QCheckBox(self.PluginPagePage)
        self.songsCheckBox.setChecked(True)
        self.songsCheckBox.setObjectName(u'songsCheckBox')
        self.verticalLayout.addWidget(self.songsCheckBox)
        self.customCheckBox = QtGui.QCheckBox(self.PluginPagePage)
        self.customCheckBox.setChecked(True)
        self.customCheckBox.setObjectName(u'customCheckBox')
        self.verticalLayout.addWidget(self.customCheckBox)
        self.bibleCheckBox = QtGui.QCheckBox(self.PluginPagePage)
        self.bibleCheckBox.setChecked(True)
        self.bibleCheckBox.setObjectName(u'bibleCheckBox')
        self.verticalLayout.addWidget(self.bibleCheckBox)
        self.imageCheckBox = QtGui.QCheckBox(self.PluginPagePage)
        self.imageCheckBox.setChecked(True)
        self.imageCheckBox.setObjectName(u'imageCheckBox')
        self.verticalLayout.addWidget(self.imageCheckBox)
        self.presentationCheckBox = QtGui.QCheckBox(self.PluginPagePage)
        self.presentationCheckBox.setChecked(True)
        self.presentationCheckBox.setObjectName(u'presentationCheckBox')
        self.verticalLayout.addWidget(self.presentationCheckBox)
        self.mediaCheckBox = QtGui.QCheckBox(self.PluginPagePage)
        self.mediaCheckBox.setChecked(True)
        self.mediaCheckBox.setObjectName(u'mediaCheckBox')
        self.verticalLayout.addWidget(self.mediaCheckBox)
        self.remoteCheckBox = QtGui.QCheckBox(self.PluginPagePage)
        self.remoteCheckBox.setObjectName(u'remoteCheckBox')
        self.verticalLayout.addWidget(self.remoteCheckBox)
        self.songUsageCheckBox = QtGui.QCheckBox(self.PluginPagePage)
        self.songUsageCheckBox.setChecked(True)
        self.songUsageCheckBox.setObjectName(u'songUsageCheckBox')
        self.verticalLayout.addWidget(self.songUsageCheckBox)
        self.alertCheckBox = QtGui.QCheckBox(self.PluginPagePage)
        self.alertCheckBox.setChecked(True)
        self.alertCheckBox.setObjectName(u'alertCheckBox')
        self.verticalLayout.addWidget(self.alertCheckBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        FirstTimeWizard.addPage(self.PluginPagePage)
        self.downloadDefaultsPage = QtGui.QWizardPage()
        self.downloadDefaultsPage.setObjectName(u'downloadDefaultsPage')
        self.noInternetLabel = QtGui.QLabel(self.downloadDefaultsPage)
        self.noInternetLabel.setGeometry(QtCore.QRect(20, 20, 461, 17))
        self.noInternetLabel.setObjectName(u'noInternetLabel')
        self.internetGroupBox = QtGui.QGroupBox(self.downloadDefaultsPage)
        self.internetGroupBox.setGeometry(QtCore.QRect(20, 10, 501, 271))
        self.internetGroupBox.setObjectName(u'internetGroupBox')
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.internetGroupBox)
        self.verticalLayout_4.setObjectName(u'verticalLayout_4')
        self.selectionTreeWidget = QtGui.QTreeWidget(self.internetGroupBox)
        self.selectionTreeWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.selectionTreeWidget.setProperty(u'showDropIndicator', False)
        self.selectionTreeWidget.setAlternatingRowColors(True)
        self.selectionTreeWidget.setObjectName(u'selectionTreeWidget')
        self.selectionTreeWidget.headerItem().setText(0, u'1')
        self.selectionTreeWidget.header().setVisible(False)
        self.verticalLayout_4.addWidget(self.selectionTreeWidget)
        FirstTimeWizard.addPage(self.downloadDefaultsPage)
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
        FirstTimeWizard.addPage(self.DefaultsPage)

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
        self.PluginPagePage.setTitle(translate('OpenLP.FirstTimeWizard',
            'Activate required Plugins'))
        self.PluginPagePage.setSubTitle(translate('OpenLP.FirstTimeWizard',
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
        self.downloadDefaultsPage.setTitle(translate('OpenLP.FirstTimeWizard',
            'Download Samples from OpenLP.org'))
        self.downloadDefaultsPage.setSubTitle(translate(
            'OpenLP.FirstTimeWizard',
            'Select samples to downlaod and install for use.'))
        self.noInternetLabel.setText(translate('OpenLP.FirstTimeWizard',
            'No Internet connection found so unable to download any default'
            ' files.'))
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
            'Press Finish to apply all you changes and start OpenLP'))
