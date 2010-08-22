# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import build_icon, translate

class Ui_SongImportWizard(object):
    def setupUi(self, songImportWizard):
        openIcon = build_icon(u':/general/general_open.png')
        deleteIcon = build_icon(u':/general/general_delete.png')
        songImportWizard.setObjectName(u'songImportWizard')
        songImportWizard.resize(550, 386)
        songImportWizard.setModal(True)
        songImportWizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        songImportWizard.setOptions(
            QtGui.QWizard.IndependentPages |
            QtGui.QWizard.NoBackButtonOnStartPage |
            QtGui.QWizard.NoBackButtonOnLastPage)
        self.welcomePage = QtGui.QWizardPage()
        self.welcomePage.setObjectName(u'welcomePage')
        self.welcomePage.setPixmap(QtGui.QWizard.WatermarkPixmap,
            QtGui.QPixmap(u':/wizards/wizard_importsong.bmp'))
        self.welcomeLayout = QtGui.QHBoxLayout(self.welcomePage)
        self.welcomeLayout.setSpacing(8)
        self.welcomeLayout.setMargin(0)
        self.welcomeLayout.setObjectName(u'welcomeLayout')
        self.welcomeTextLayout = QtGui.QVBoxLayout()
        self.welcomeTextLayout.setSpacing(8)
        self.welcomeTextLayout.setObjectName(u'welcomeTextLayout')
        self.titleLabel = QtGui.QLabel(self.welcomePage)
        self.titleLabel.setObjectName(u'TitleLabel')
        self.welcomeTextLayout.addWidget(self.titleLabel)
        self.welcomeTopSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.welcomeTextLayout.addItem(self.welcomeTopSpacer)
        self.informationLabel = QtGui.QLabel(self.welcomePage)
        self.informationLabel.setWordWrap(True)
        self.informationLabel.setMargin(10)
        self.informationLabel.setObjectName(u'InformationLabel')
        self.welcomeTextLayout.addWidget(self.informationLabel)
        self.welcomeBottomSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.welcomeTextLayout.addItem(self.welcomeBottomSpacer)
        self.welcomeLayout.addLayout(self.welcomeTextLayout)
        songImportWizard.addPage(self.welcomePage)
        self.sourcePage = QtGui.QWizardPage()
        self.sourcePage.setObjectName(u'SourcePage')
        self.sourceLayout = QtGui.QVBoxLayout(self.sourcePage)
        self.sourceLayout.setSpacing(8)
        self.sourceLayout.setMargin(20)
        self.sourceLayout.setObjectName(u'SourceLayout')
        self.formatLayout = QtGui.QHBoxLayout()
        self.formatLayout.setSpacing(8)
        self.formatLayout.setObjectName(u'FormatLayout')
        self.formatLabel = QtGui.QLabel(self.sourcePage)
        self.formatLabel.setObjectName(u'FormatLabel')
        self.formatLayout.addWidget(self.formatLabel)
        self.formatComboBox = QtGui.QComboBox(self.sourcePage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.formatComboBox.sizePolicy().hasHeightForWidth())
        self.formatComboBox.setSizePolicy(sizePolicy)
        self.formatComboBox.setObjectName(u'formatComboBox')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
#        self.formatComboBox.addItem(u'')
        self.formatLayout.addWidget(self.formatComboBox)
        self.formatSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formatLayout.addItem(self.formatSpacer)
        self.sourceLayout.addLayout(self.formatLayout)
        self.formatStackedWidget = QtGui.QStackedWidget(self.sourcePage)
        self.formatStackedWidget.setObjectName(u'FormatStackedWidget')
        # OpenLP 2.0
        self.openLP2Page = QtGui.QWidget()
        self.openLP2Page.setObjectName(u'openLP2Page')
        self.openLP2Layout = QtGui.QFormLayout(self.openLP2Page)
        self.openLP2Layout.setMargin(0)
        self.openLP2Layout.setSpacing(8)
        self.openLP2Layout.setObjectName(u'openLP2Layout')
        self.openLP2FilenameLabel = QtGui.QLabel(self.openLP2Page)
        self.openLP2FilenameLabel.setObjectName(u'openLP2FilenameLabel')
        self.openLP2Layout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.openLP2FilenameLabel)
        self.openLP2FileLayout = QtGui.QHBoxLayout()
        self.openLP2FileLayout.setSpacing(8)
        self.openLP2FileLayout.setObjectName(u'openLP2FileLayout')
        self.openLP2FilenameEdit = QtGui.QLineEdit(self.openLP2Page)
        self.openLP2FilenameEdit.setObjectName(u'openLP2FilenameEdit')
        self.openLP2FileLayout.addWidget(self.openLP2FilenameEdit)
        self.openLP2BrowseButton = QtGui.QToolButton(self.openLP2Page)
        self.openLP2BrowseButton.setIcon(openIcon)
        self.openLP2BrowseButton.setObjectName(u'openLP2BrowseButton')
        self.openLP2FileLayout.addWidget(self.openLP2BrowseButton)
        self.openLP2Layout.setLayout(0, QtGui.QFormLayout.FieldRole,
            self.openLP2FileLayout)
        self.formatStackedWidget.addWidget(self.openLP2Page)
        # openlp.org 1.x
        self.openLP1Page = QtGui.QWidget()
        self.openLP1Page.setObjectName(u'openLP1Page')
        self.openLP1Layout = QtGui.QFormLayout(self.openLP1Page)
        self.openLP1Layout.setMargin(0)
        self.openLP1Layout.setSpacing(8)
        self.openLP1Layout.setObjectName(u'openLP1Layout')
        self.openLP1FilenameLabel = QtGui.QLabel(self.openLP1Page)
        self.openLP1FilenameLabel.setObjectName(u'openLP1FilenameLabel')
        self.openLP1Layout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.openLP1FilenameLabel)
        self.openLP1FileLayout = QtGui.QHBoxLayout()
        self.openLP1FileLayout.setSpacing(8)
        self.openLP1FileLayout.setObjectName(u'openLP1FileLayout')
        self.openLP1FilenameEdit = QtGui.QLineEdit(self.openLP1Page)
        self.openLP1FilenameEdit.setObjectName(u'openLP1FilenameEdit')
        self.openLP1FileLayout.addWidget(self.openLP1FilenameEdit)
        self.openLP1BrowseButton = QtGui.QToolButton(self.openLP1Page)
        self.openLP1BrowseButton.setIcon(openIcon)
        self.openLP1BrowseButton.setObjectName(u'openLP1BrowseButton')
        self.openLP1FileLayout.addWidget(self.openLP1BrowseButton)
        self.openLP1Layout.setLayout(0, QtGui.QFormLayout.FieldRole,
            self.openLP1FileLayout)
        self.formatStackedWidget.addWidget(self.openLP1Page)
        # OpenLyrics
        self.openLyricsPage = QtGui.QWidget()
        self.openLyricsPage.setObjectName(u'OpenLyricsPage')
        self.openLyricsLayout = QtGui.QVBoxLayout(self.openLyricsPage)
        self.openLyricsLayout.setSpacing(8)
        self.openLyricsLayout.setMargin(0)
        self.openLyricsLayout.setObjectName(u'OpenLyricsLayout')
        self.openLyricsFileListWidget = QtGui.QListWidget(self.openLyricsPage)
        self.openLyricsFileListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.openLyricsFileListWidget.setObjectName(u'OpenLyricsFileListWidget')
        self.openLyricsLayout.addWidget(self.openLyricsFileListWidget)
        self.openLyricsButtonLayout = QtGui.QHBoxLayout()
        self.openLyricsButtonLayout.setSpacing(8)
        self.openLyricsButtonLayout.setObjectName(u'OpenLyricsButtonLayout')
        self.openLyricsAddButton = QtGui.QPushButton(self.openLyricsPage)
        self.openLyricsAddButton.setIcon(openIcon)
        self.openLyricsAddButton.setObjectName(u'OpenLyricsAddButton')
        self.openLyricsButtonLayout.addWidget(self.openLyricsAddButton)
        self.openLyricsButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.openLyricsButtonLayout.addItem(self.openLyricsButtonSpacer)
        self.openLyricsRemoveButton = QtGui.QPushButton(self.openLyricsPage)
        self.openLyricsRemoveButton.setIcon(deleteIcon)
        self.openLyricsRemoveButton.setObjectName(u'OpenLyricsRemoveButton')
        self.openLyricsButtonLayout.addWidget(self.openLyricsRemoveButton)
        self.openLyricsLayout.addLayout(self.openLyricsButtonLayout)
        self.formatStackedWidget.addWidget(self.openLyricsPage)
        # Open Song
        self.openSongPage = QtGui.QWidget()
        self.openSongPage.setObjectName(u'OpenSongPage')
        self.openSongLayout = QtGui.QVBoxLayout(self.openSongPage)
        self.openSongLayout.setSpacing(8)
        self.openSongLayout.setMargin(0)
        self.openSongLayout.setObjectName(u'OpenSongLayout')
        self.openSongFileListWidget = QtGui.QListWidget(self.openSongPage)
        self.openSongFileListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.openSongFileListWidget.setObjectName(u'OpenSongFileListWidget')
        self.openSongLayout.addWidget(self.openSongFileListWidget)
        self.openSongButtonLayout = QtGui.QHBoxLayout()
        self.openSongButtonLayout.setSpacing(8)
        self.openSongButtonLayout.setObjectName(u'OpenSongButtonLayout')
        self.openSongAddButton = QtGui.QPushButton(self.openSongPage)
        self.openSongAddButton.setIcon(openIcon)
        self.openSongAddButton.setObjectName(u'OpenSongAddButton')
        self.openSongButtonLayout.addWidget(self.openSongAddButton)
        self.openSongButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.openSongButtonLayout.addItem(self.openSongButtonSpacer)
        self.openSongRemoveButton = QtGui.QPushButton(self.openSongPage)
        self.openSongRemoveButton.setIcon(deleteIcon)
        self.openSongRemoveButton.setObjectName(u'OpenSongRemoveButton')
        self.openSongButtonLayout.addWidget(self.openSongRemoveButton)
        self.openSongLayout.addLayout(self.openSongButtonLayout)
        self.formatStackedWidget.addWidget(self.openSongPage)
        # Words of Worship
        self.wordsOfWorshipPage = QtGui.QWidget()
        self.wordsOfWorshipPage.setObjectName(u'wordsOfWorshipPage')
        self.wordsOfWorshipLayout = QtGui.QVBoxLayout(self.wordsOfWorshipPage)
        self.wordsOfWorshipLayout.setSpacing(8)
        self.wordsOfWorshipLayout.setMargin(0)
        self.wordsOfWorshipLayout.setObjectName(u'wordsOfWorshipLayout')
        self.wordsOfWorshipFileListWidget = QtGui.QListWidget(self.wordsOfWorshipPage)
        self.wordsOfWorshipFileListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.wordsOfWorshipFileListWidget.setObjectName(u'wordsOfWorshipFileListWidget')
        self.wordsOfWorshipLayout.addWidget(self.wordsOfWorshipFileListWidget)
        self.wordsOfWorshipButtonLayout = QtGui.QHBoxLayout()
        self.wordsOfWorshipButtonLayout.setSpacing(8)
        self.wordsOfWorshipButtonLayout.setObjectName(u'wordsOfWorshipButtonLayout')
        self.wordsOfWorshipAddButton = QtGui.QPushButton(self.wordsOfWorshipPage)
        self.wordsOfWorshipAddButton.setIcon(openIcon)
        self.wordsOfWorshipAddButton.setObjectName(u'wordsOfWorshipAddButton')
        self.wordsOfWorshipButtonLayout.addWidget(self.wordsOfWorshipAddButton)
        self.wordsOfWorshipButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.wordsOfWorshipButtonLayout.addItem(self.wordsOfWorshipButtonSpacer)
        self.wordsOfWorshipRemoveButton = QtGui.QPushButton(self.wordsOfWorshipPage)
        self.wordsOfWorshipRemoveButton.setIcon(deleteIcon)
        self.wordsOfWorshipRemoveButton.setObjectName(u'wordsOfWorshipRemoveButton')
        self.wordsOfWorshipButtonLayout.addWidget(self.wordsOfWorshipRemoveButton)
        self.wordsOfWorshipLayout.addLayout(self.wordsOfWorshipButtonLayout)
        self.formatStackedWidget.addWidget(self.wordsOfWorshipPage)
        # CCLI File import
        self.ccliPage = QtGui.QWidget()
        self.ccliPage.setObjectName(u'CCLIPage')
        self.ccliLayout = QtGui.QVBoxLayout(self.ccliPage)
        self.ccliLayout.setSpacing(8)
        self.ccliLayout.setMargin(0)
        self.ccliLayout.setObjectName(u'CCLILayout')
        self.ccliFileListWidget = QtGui.QListWidget(self.ccliPage)
        self.ccliFileListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.ccliFileListWidget.setObjectName(u'CCLIFileListWidget')
        self.ccliLayout.addWidget(self.ccliFileListWidget)
        self.ccliButtonLayout = QtGui.QHBoxLayout()
        self.ccliButtonLayout.setSpacing(8)
        self.ccliButtonLayout.setObjectName(u'CCLIButtonLayout')
        self.ccliAddButton = QtGui.QPushButton(self.ccliPage)
        self.ccliAddButton.setIcon(openIcon)
        self.ccliAddButton.setObjectName(u'CCLIAddButton')
        self.ccliButtonLayout.addWidget(self.ccliAddButton)
        self.ccliButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ccliButtonLayout.addItem(self.ccliButtonSpacer)
        self.ccliRemoveButton = QtGui.QPushButton(self.ccliPage)
        self.ccliRemoveButton.setIcon(deleteIcon)
        self.ccliRemoveButton.setObjectName(u'CCLIRemoveButton')
        self.ccliButtonLayout.addWidget(self.ccliRemoveButton)
        self.ccliLayout.addLayout(self.ccliButtonLayout)
        self.formatStackedWidget.addWidget(self.ccliPage)
        # Songs of Fellowship
        self.songsOfFellowshipPage = QtGui.QWidget()
        self.songsOfFellowshipPage.setObjectName(u'songsOfFellowshipPage')
        self.songsOfFellowshipLayout = QtGui.QFormLayout(self.songsOfFellowshipPage)
        self.songsOfFellowshipLayout.setMargin(0)
        self.songsOfFellowshipLayout.setSpacing(8)
        self.songsOfFellowshipLayout.setObjectName(u'songsOfFellowshipLayout')
        self.songsOfFellowshipFilenameLabel = QtGui.QLabel(self.songsOfFellowshipPage)
        self.songsOfFellowshipFilenameLabel.setObjectName(u'songsOfFellowshipFilenameLabel')
        self.songsOfFellowshipLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.songsOfFellowshipFilenameLabel)
        self.songsOfFellowshipFileLayout = QtGui.QHBoxLayout()
        self.songsOfFellowshipFileLayout.setSpacing(8)
        self.songsOfFellowshipFileLayout.setObjectName(u'songsOfFellowshipFileLayout')
        self.songsOfFellowshipFilenameEdit = QtGui.QLineEdit(self.songsOfFellowshipPage)
        self.songsOfFellowshipFilenameEdit.setObjectName(u'songsOfFellowshipFilenameEdit')
        self.songsOfFellowshipFileLayout.addWidget(self.songsOfFellowshipFilenameEdit)
        self.songsOfFellowshipBrowseButton = QtGui.QToolButton(self.songsOfFellowshipPage)
        self.songsOfFellowshipBrowseButton.setIcon(openIcon)
        self.songsOfFellowshipBrowseButton.setObjectName(u'songsOfFellowshipBrowseButton')
        self.songsOfFellowshipFileLayout.addWidget(self.songsOfFellowshipBrowseButton)
        self.songsOfFellowshipLayout.setLayout(0, QtGui.QFormLayout.FieldRole,
            self.songsOfFellowshipFileLayout)
        self.formatStackedWidget.addWidget(self.songsOfFellowshipPage)
        # Generic Document/Presentation import
        self.genericPage = QtGui.QWidget()
        self.genericPage.setObjectName(u'genericPage')
        self.genericLayout = QtGui.QFormLayout(self.genericPage)
        self.genericLayout.setMargin(0)
        self.genericLayout.setSpacing(8)
        self.genericLayout.setObjectName(u'genericLayout')
        self.genericFilenameLabel = QtGui.QLabel(self.genericPage)
        self.genericFilenameLabel.setObjectName(u'genericFilenameLabel')
        self.genericLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.genericFilenameLabel)
        self.genericFileLayout = QtGui.QHBoxLayout()
        self.genericFileLayout.setSpacing(8)
        self.genericFileLayout.setObjectName(u'genericFileLayout')
        self.genericFilenameEdit = QtGui.QLineEdit(self.genericPage)
        self.genericFilenameEdit.setObjectName(u'genericFilenameEdit')
        self.genericFileLayout.addWidget(self.genericFilenameEdit)
        self.genericBrowseButton = QtGui.QToolButton(self.genericPage)
        self.genericBrowseButton.setIcon(openIcon)
        self.genericBrowseButton.setObjectName(u'genericBrowseButton')
        self.genericFileLayout.addWidget(self.genericBrowseButton)
        self.genericLayout.setLayout(0, QtGui.QFormLayout.FieldRole,
            self.genericFileLayout)
        self.formatStackedWidget.addWidget(self.genericPage)
#        Commented out for future use.
#        self.csvPage = QtGui.QWidget()
#        self.csvPage.setObjectName(u'CSVPage')
#        self.csvLayout = QtGui.QFormLayout(self.csvPage)
#        self.csvLayout.setMargin(0)
#        self.csvLayout.setSpacing(8)
#        self.csvLayout.setObjectName(u'CSVLayout')
#        self.csvFilenameLabel = QtGui.QLabel(self.csvPage)
#        self.csvFilenameLabel.setObjectName(u'CSVFilenameLabel')
#        self.csvLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
#            self.csvFilenameLabel)
#        self.csvFileLayout = QtGui.QHBoxLayout()
#        self.csvFileLayout.setSpacing(8)
#        self.csvFileLayout.setObjectName(u'CSVFileLayout')
#        self.csvFilenameEdit = QtGui.QLineEdit(self.csvPage)
#        self.csvFilenameEdit.setObjectName(u'CSVFilenameEdit')
#        self.csvFileLayout.addWidget(self.csvFilenameEdit)
#        self.csvBrowseButton = QtGui.QToolButton(self.csvPage)
#        self.csvBrowseButton.setIcon(openIcon)
#        self.csvBrowseButton.setObjectName(u'CSVBrowseButton')
#        self.csvFileLayout.addWidget(self.csvBrowseButton)
#        self.csvLayout.setLayout(0, QtGui.QFormLayout.FieldRole,
#            self.csvFileLayout)
#        self.formatStackedWidget.addWidget(self.csvPage)
        self.sourceLayout.addWidget(self.formatStackedWidget)
        songImportWizard.addPage(self.sourcePage)
        self.importPage = QtGui.QWizardPage()
        self.importPage.setObjectName(u'importPage')
        self.importLayout = QtGui.QVBoxLayout(self.importPage)
        self.importLayout.setSpacing(8)
        self.importLayout.setMargin(50)
        self.importLayout.setObjectName(u'importLayout')
        self.importProgressLabel = QtGui.QLabel(self.importPage)
        self.importProgressLabel.setObjectName(u'importProgressLabel')
        self.importLayout.addWidget(self.importProgressLabel)
        self.importProgressBar = QtGui.QProgressBar(self.importPage)
        self.importProgressBar.setProperty(u'value', 0)
        self.importProgressBar.setInvertedAppearance(False)
        self.importProgressBar.setObjectName(u'importProgressBar')
        self.importLayout.addWidget(self.importProgressBar)
        songImportWizard.addPage(self.importPage)
        self.retranslateUi(songImportWizard)
        self.formatStackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.formatComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.formatStackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(songImportWizard)

    def retranslateUi(self, songImportWizard):
        songImportWizard.setWindowTitle(
            translate('SongsPlugin.ImportWizardForm', 'Song import Wizard'))
        self.titleLabel.setText(
            u'<span style="font-size:14pt; font-weight:600;">%s</span>' % \
            translate('SongsPlugin.ImportWizardForm',
                'Welcome to the Song import Wizard'))
        self.informationLabel.setText(
            translate('SongsPlugin.ImportWizardForm',
                'This wizard will help you to import songs from a variety of '
                'formats. Click the next button below to start the process by '
                'selecting a format to import from.'))
        self.sourcePage.setTitle(
            translate('SongsPlugin.ImportWizardForm', 'Select import Source'))
        self.sourcePage.setSubTitle(
            translate('SongsPlugin.ImportWizardForm',
            'Select the import format, and where to import from.'))
        self.formatLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Format:'))
        self.formatComboBox.setItemText(0,
            translate('SongsPlugin.ImportWizardForm', 'OpenLP 2.0'))
        self.formatComboBox.setItemText(1,
            translate('SongsPlugin.ImportWizardForm', 'openlp.org 1.x'))
        self.formatComboBox.setItemText(2,
            translate('SongsPlugin.ImportWizardForm', 'OpenLyrics'))
        self.formatComboBox.setItemText(3,
            translate('SongsPlugin.ImportWizardForm', 'OpenSong'))
        self.formatComboBox.setItemText(4,
            translate('SongsPlugin.ImportWizardForm', 'Words of Worship'))
        self.formatComboBox.setItemText(5,
            translate('SongsPlugin.ImportWizardForm', 'CCLI'))
        self.formatComboBox.setItemText(6,
            translate('SongsPlugin.ImportWizardForm', 'Songs of Fellowship'))
        self.formatComboBox.setItemText(7,
            translate('SongsPlugin.ImportWizardForm',
            'Generic Document/Presentation'))
#        self.formatComboBox.setItemText(8,
#            translate('SongsPlugin.ImportWizardForm', 'CSV'))
        self.openLP2FilenameLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
        self.openLP2BrowseButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
        self.openLP1FilenameLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
        self.openLP1BrowseButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
        self.openLyricsAddButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        self.openLyricsRemoveButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
        self.openSongAddButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        self.openSongRemoveButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
        self.wordsOfWorshipAddButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        self.wordsOfWorshipRemoveButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
        self.ccliAddButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        self.ccliRemoveButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
        self.songsOfFellowshipFilenameLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
        self.songsOfFellowshipBrowseButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
        self.genericFilenameLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
        self.genericBrowseButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
#        self.csvFilenameLabel.setText(
#            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
#        self.csvBrowseButton.setText(
#            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
        self.importPage.setTitle(
            translate('SongsPlugin.ImportWizardForm', 'importing'))
        self.importPage.setSubTitle(
            translate('SongsPlugin.ImportWizardForm',
                'Please wait while your songs are imported.'))
        self.importProgressLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Ready.'))
        self.importProgressBar.setFormat(
            translate('SongsPlugin.ImportWizardForm', '%p%'))
