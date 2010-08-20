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
        self.WelcomePage = QtGui.QWizardPage()
        self.WelcomePage.setObjectName(u'WelcomePage')
        self.WelcomePage.setPixmap(QtGui.QWizard.WatermarkPixmap,
            QtGui.QPixmap(u':/wizards/wizard_importsong.bmp'))
        self.WelcomeLayout = QtGui.QHBoxLayout(self.WelcomePage)
        self.WelcomeLayout.setSpacing(8)
        self.WelcomeLayout.setMargin(0)
        self.WelcomeLayout.setObjectName(u'WelcomeLayout')
        self.WelcomeTextLayout = QtGui.QVBoxLayout()
        self.WelcomeTextLayout.setSpacing(8)
        self.WelcomeTextLayout.setObjectName(u'WelcomeTextLayout')
        self.TitleLabel = QtGui.QLabel(self.WelcomePage)
        self.TitleLabel.setObjectName(u'TitleLabel')
        self.WelcomeTextLayout.addWidget(self.TitleLabel)
        self.WelcomeTopSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.WelcomeTextLayout.addItem(self.WelcomeTopSpacer)
        self.InformationLabel = QtGui.QLabel(self.WelcomePage)
        self.InformationLabel.setWordWrap(True)
        self.InformationLabel.setMargin(10)
        self.InformationLabel.setObjectName(u'InformationLabel')
        self.WelcomeTextLayout.addWidget(self.InformationLabel)
        self.WelcomeBottomSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.WelcomeTextLayout.addItem(self.WelcomeBottomSpacer)
        self.WelcomeLayout.addLayout(self.WelcomeTextLayout)
        songImportWizard.addPage(self.WelcomePage)
        self.SourcePage = QtGui.QWizardPage()
        self.SourcePage.setObjectName(u'SourcePage')
        self.SourceLayout = QtGui.QVBoxLayout(self.SourcePage)
        self.SourceLayout.setSpacing(8)
        self.SourceLayout.setMargin(20)
        self.SourceLayout.setObjectName(u'SourceLayout')
        self.FormatLayout = QtGui.QHBoxLayout()
        self.FormatLayout.setSpacing(8)
        self.FormatLayout.setObjectName(u'FormatLayout')
        self.FormatLabel = QtGui.QLabel(self.SourcePage)
        self.FormatLabel.setObjectName(u'FormatLabel')
        self.FormatLayout.addWidget(self.FormatLabel)
        self.FormatComboBox = QtGui.QComboBox(self.SourcePage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.FormatComboBox.sizePolicy().hasHeightForWidth())
        self.FormatComboBox.setSizePolicy(sizePolicy)
        self.FormatComboBox.setObjectName(u'FormatComboBox')
        self.FormatComboBox.addItem(u'')
        self.FormatComboBox.addItem(u'')
        self.FormatComboBox.addItem(u'')
        self.FormatComboBox.addItem(u'')
        self.FormatComboBox.addItem(u'')
        self.FormatComboBox.addItem(u'')
        self.FormatComboBox.addItem(u'')
        self.FormatComboBox.addItem(u'')
#        self.FormatComboBox.addItem(u'')
        self.FormatLayout.addWidget(self.FormatComboBox)
        self.FormatSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.FormatLayout.addItem(self.FormatSpacer)
        self.SourceLayout.addLayout(self.FormatLayout)
        self.FormatStackedWidget = QtGui.QStackedWidget(self.SourcePage)
        self.FormatStackedWidget.setObjectName(u'FormatStackedWidget')
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
        self.FormatStackedWidget.addWidget(self.openLP2Page)
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
        self.FormatStackedWidget.addWidget(self.openLP1Page)
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
        self.FormatStackedWidget.addWidget(self.openLyricsPage)
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
        self.FormatStackedWidget.addWidget(self.openSongPage)
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
        self.FormatStackedWidget.addWidget(self.wordsOfWorshipPage)
        # CCLI File Import
        self.CCLIPage = QtGui.QWidget()
        self.CCLIPage.setObjectName(u'CCLIPage')
        self.CCLILayout = QtGui.QVBoxLayout(self.CCLIPage)
        self.CCLILayout.setSpacing(8)
        self.CCLILayout.setMargin(0)
        self.CCLILayout.setObjectName(u'CCLILayout')
        self.CCLIFileListWidget = QtGui.QListWidget(self.CCLIPage)
        self.CCLIFileListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.CCLIFileListWidget.setObjectName(u'CCLIFileListWidget')
        self.CCLILayout.addWidget(self.CCLIFileListWidget)
        self.CCLIButtonLayout = QtGui.QHBoxLayout()
        self.CCLIButtonLayout.setSpacing(8)
        self.CCLIButtonLayout.setObjectName(u'CCLIButtonLayout')
        self.CCLIAddButton = QtGui.QPushButton(self.CCLIPage)
        self.CCLIAddButton.setIcon(openIcon)
        self.CCLIAddButton.setObjectName(u'CCLIAddButton')
        self.CCLIButtonLayout.addWidget(self.CCLIAddButton)
        self.CCLIButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.CCLIButtonLayout.addItem(self.CCLIButtonSpacer)
        self.CCLIRemoveButton = QtGui.QPushButton(self.CCLIPage)
        self.CCLIRemoveButton.setIcon(deleteIcon)
        self.CCLIRemoveButton.setObjectName(u'CCLIRemoveButton')
        self.CCLIButtonLayout.addWidget(self.CCLIRemoveButton)
        self.CCLILayout.addLayout(self.CCLIButtonLayout)
        self.FormatStackedWidget.addWidget(self.CCLIPage)
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
        self.FormatStackedWidget.addWidget(self.songsOfFellowshipPage)
        # Generic Document/Presentation Import
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
        self.FormatStackedWidget.addWidget(self.genericPage)
#        Commented out for future use.
#        self.CSVPage = QtGui.QWidget()
#        self.CSVPage.setObjectName(u'CSVPage')
#        self.CSVLayout = QtGui.QFormLayout(self.CSVPage)
#        self.CSVLayout.setMargin(0)
#        self.CSVLayout.setSpacing(8)
#        self.CSVLayout.setObjectName(u'CSVLayout')
#        self.CSVFilenameLabel = QtGui.QLabel(self.CSVPage)
#        self.CSVFilenameLabel.setObjectName(u'CSVFilenameLabel')
#        self.CSVLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
#            self.CSVFilenameLabel)
#        self.CSVFileLayout = QtGui.QHBoxLayout()
#        self.CSVFileLayout.setSpacing(8)
#        self.CSVFileLayout.setObjectName(u'CSVFileLayout')
#        self.CSVFilenameEdit = QtGui.QLineEdit(self.CSVPage)
#        self.CSVFilenameEdit.setObjectName(u'CSVFilenameEdit')
#        self.CSVFileLayout.addWidget(self.CSVFilenameEdit)
#        self.CSVBrowseButton = QtGui.QToolButton(self.CSVPage)
#        self.CSVBrowseButton.setIcon(openIcon)
#        self.CSVBrowseButton.setObjectName(u'CSVBrowseButton')
#        self.CSVFileLayout.addWidget(self.CSVBrowseButton)
#        self.CSVLayout.setLayout(0, QtGui.QFormLayout.FieldRole,
#            self.CSVFileLayout)
#        self.FormatStackedWidget.addWidget(self.CSVPage)
        self.SourceLayout.addWidget(self.FormatStackedWidget)
        songImportWizard.addPage(self.SourcePage)
        self.ImportPage = QtGui.QWizardPage()
        self.ImportPage.setObjectName(u'ImportPage')
        self.ImportLayout = QtGui.QVBoxLayout(self.ImportPage)
        self.ImportLayout.setSpacing(8)
        self.ImportLayout.setMargin(50)
        self.ImportLayout.setObjectName(u'ImportLayout')
        self.ImportProgressLabel = QtGui.QLabel(self.ImportPage)
        self.ImportProgressLabel.setObjectName(u'ImportProgressLabel')
        self.ImportLayout.addWidget(self.ImportProgressLabel)
        self.ImportProgressBar = QtGui.QProgressBar(self.ImportPage)
        self.ImportProgressBar.setProperty(u'value', 0)
        self.ImportProgressBar.setInvertedAppearance(False)
        self.ImportProgressBar.setObjectName(u'ImportProgressBar')
        self.ImportLayout.addWidget(self.ImportProgressBar)
        songImportWizard.addPage(self.ImportPage)
        self.retranslateUi(songImportWizard)
        self.FormatStackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.FormatComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.FormatStackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(songImportWizard)

    def retranslateUi(self, songImportWizard):
        songImportWizard.setWindowTitle(
            translate('SongsPlugin.ImportWizardForm', 'Song Import Wizard'))
        self.TitleLabel.setText(
            u'<span style="font-size:14pt; font-weight:600;">%s</span>' % \
            translate('SongsPlugin.ImportWizardForm',
                'Welcome to the Song Import Wizard'))
        self.InformationLabel.setText(
            translate('SongsPlugin.ImportWizardForm',
                'This wizard will help you to import songs from a variety of '
                'formats. Click the next button below to start the process by '
                'selecting a format to import from.'))
        self.SourcePage.setTitle(
            translate('SongsPlugin.ImportWizardForm', 'Select Import Source'))
        self.SourcePage.setSubTitle(
            translate('SongsPlugin.ImportWizardForm',
            'Select the import format, and where to import from.'))
        self.FormatLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Format:'))
        self.FormatComboBox.setItemText(0,
            translate('SongsPlugin.ImportWizardForm', 'OpenLP 2.0'))
        self.FormatComboBox.setItemText(1,
            translate('SongsPlugin.ImportWizardForm', 'openlp.org 1.x'))
        self.FormatComboBox.setItemText(2,
            translate('SongsPlugin.ImportWizardForm', 'OpenLyrics'))
        self.FormatComboBox.setItemText(3,
            translate('SongsPlugin.ImportWizardForm', 'OpenSong'))
        self.FormatComboBox.setItemText(4,
            translate('SongsPlugin.ImportWizardForm', 'Words of Worship'))
        self.FormatComboBox.setItemText(5,
            translate('SongsPlugin.ImportWizardForm', 'CCLI'))
        self.FormatComboBox.setItemText(6,
            translate('SongsPlugin.ImportWizardForm', 'Songs of Fellowship'))
        self.FormatComboBox.setItemText(7,
            translate('SongsPlugin.ImportWizardForm',
            'Generic Document/Presentation'))
#        self.FormatComboBox.setItemText(8,
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
        self.CCLIAddButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        self.CCLIRemoveButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
        self.songsOfFellowshipFilenameLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
        self.songsOfFellowshipBrowseButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
        self.genericFilenameLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
        self.genericBrowseButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
#        self.CSVFilenameLabel.setText(
#            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
#        self.CSVBrowseButton.setText(
#            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
        self.ImportPage.setTitle(
            translate('SongsPlugin.ImportWizardForm', 'Importing'))
        self.ImportPage.setSubTitle(
            translate('SongsPlugin.ImportWizardForm',
                'Please wait while your songs are imported.'))
        self.ImportProgressLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Ready.'))
        self.ImportProgressBar.setFormat(
            translate('SongsPlugin.ImportWizardForm', '%p%'))
