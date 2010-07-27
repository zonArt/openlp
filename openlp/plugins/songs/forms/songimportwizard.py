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
    def setupUi(self, SongImportWizard):
        SongImportWizard.setObjectName(u'SongImportWizard')
        SongImportWizard.resize(550, 386)
        SongImportWizard.setModal(True)
        SongImportWizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        SongImportWizard.setOptions(
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
        SongImportWizard.addPage(self.WelcomePage)
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
        self.FormatLayout.addWidget(self.FormatComboBox)
        self.FormatSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.FormatLayout.addItem(self.FormatSpacer)
        self.SourceLayout.addLayout(self.FormatLayout)
        self.FormatStackedWidget = QtGui.QStackedWidget(self.SourcePage)
        self.FormatStackedWidget.setObjectName(u'FormatStackedWidget')
        self.OpenLyricsPage = QtGui.QWidget()
        self.OpenLyricsPage.setObjectName(u'OpenLyricsPage')
        self.OpenLyricsLayout = QtGui.QVBoxLayout(self.OpenLyricsPage)
        self.OpenLyricsLayout.setSpacing(8)
        self.OpenLyricsLayout.setMargin(0)
        self.OpenLyricsLayout.setObjectName(u'OpenLyricsLayout')
        self.OpenLyricsFileListWidget = QtGui.QListWidget(self.OpenLyricsPage)
        self.OpenLyricsFileListWidget.setObjectName(u'OpenLyricsFileListWidget')
        self.OpenLyricsLayout.addWidget(self.OpenLyricsFileListWidget)
        self.OpenLyricsButtonLayout = QtGui.QHBoxLayout()
        self.OpenLyricsButtonLayout.setSpacing(8)
        self.OpenLyricsButtonLayout.setObjectName(u'OpenLyricsButtonLayout')
        self.OpenLyricsAddButton = QtGui.QPushButton(self.OpenLyricsPage)
        openIcon = build_icon(u':/general/general_open.png')
        self.OpenLyricsAddButton.setIcon(openIcon)
        self.OpenLyricsAddButton.setObjectName(u'OpenLyricsAddButton')
        self.OpenLyricsButtonLayout.addWidget(self.OpenLyricsAddButton)
        self.OpenLyricsButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.OpenLyricsButtonLayout.addItem(self.OpenLyricsButtonSpacer)
        self.OpenLyricsRemoveButton = QtGui.QPushButton(self.OpenLyricsPage)
        deleteIcon = build_icon(u':/general/general_delete.png')
        self.OpenLyricsRemoveButton.setIcon(deleteIcon)
        self.OpenLyricsRemoveButton.setObjectName(u'OpenLyricsRemoveButton')
        self.OpenLyricsButtonLayout.addWidget(self.OpenLyricsRemoveButton)
        self.OpenLyricsLayout.addLayout(self.OpenLyricsButtonLayout)
        self.FormatStackedWidget.addWidget(self.OpenLyricsPage)
        self.OpenSongPage = QtGui.QWidget()
        self.OpenSongPage.setObjectName(u'OpenSongPage')
        self.OpenSongLayout = QtGui.QVBoxLayout(self.OpenSongPage)
        self.OpenSongLayout.setSpacing(8)
        self.OpenSongLayout.setMargin(0)
        self.OpenSongLayout.setObjectName(u'OpenSongLayout')
        self.OpenSongFileListWidget = QtGui.QListWidget(self.OpenSongPage)
        self.OpenSongFileListWidget.setObjectName(u'OpenSongFileListWidget')
        self.OpenSongLayout.addWidget(self.OpenSongFileListWidget)
        self.OpenSongButtonLayout = QtGui.QHBoxLayout()
        self.OpenSongButtonLayout.setSpacing(8)
        self.OpenSongButtonLayout.setObjectName(u'OpenSongButtonLayout')
        self.OpenSongAddButton = QtGui.QPushButton(self.OpenSongPage)
        self.OpenSongAddButton.setIcon(openIcon)
        self.OpenSongAddButton.setObjectName(u'OpenSongAddButton')
        self.OpenSongButtonLayout.addWidget(self.OpenSongAddButton)
        self.OpenSongButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.OpenSongButtonLayout.addItem(self.OpenSongButtonSpacer)
        self.OpenSongRemoveButton = QtGui.QPushButton(self.OpenSongPage)
        self.OpenSongRemoveButton.setIcon(deleteIcon)
        self.OpenSongRemoveButton.setObjectName(u'OpenSongRemoveButton')
        self.OpenSongButtonLayout.addWidget(self.OpenSongRemoveButton)
        self.OpenSongLayout.addLayout(self.OpenSongButtonLayout)
        self.FormatStackedWidget.addWidget(self.OpenSongPage)
        self.CCLIPage = QtGui.QWidget()
        self.CCLIPage.setObjectName(u'CCLIPage')
        self.CCLILayout = QtGui.QVBoxLayout(self.CCLIPage)
        self.CCLILayout.setSpacing(8)
        self.CCLILayout.setMargin(0)
        self.CCLILayout.setObjectName(u'CCLILayout')
        self.CCLIFileListWidget = QtGui.QListWidget(self.CCLIPage)
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
        self.CSVPage = QtGui.QWidget()
        self.CSVPage.setObjectName(u'CSVPage')
        self.CSVLayout = QtGui.QFormLayout(self.CSVPage)
        self.CSVLayout.setMargin(0)
        self.CSVLayout.setSpacing(8)
        self.CSVLayout.setObjectName(u'CSVLayout')
        self.CSVFilenameLabel = QtGui.QLabel(self.CSVPage)
        self.CSVFilenameLabel.setObjectName(u'CSVFilenameLabel')
        self.CSVLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.CSVFilenameLabel)
        self.CSVFileLayout = QtGui.QHBoxLayout()
        self.CSVFileLayout.setSpacing(8)
        self.CSVFileLayout.setObjectName(u'CSVFileLayout')
        self.CSVFilenameEdit = QtGui.QLineEdit(self.CSVPage)
        self.CSVFilenameEdit.setObjectName(u'CSVFilenameEdit')
        self.CSVFileLayout.addWidget(self.CSVFilenameEdit)
        self.CSVBrowseButton = QtGui.QToolButton(self.CSVPage)
        self.CSVBrowseButton.setIcon(openIcon)
        self.CSVBrowseButton.setObjectName(u'CSVBrowseButton')
        self.CSVFileLayout.addWidget(self.CSVBrowseButton)
        self.CSVLayout.setLayout(0, QtGui.QFormLayout.FieldRole,
            self.CSVFileLayout)
        self.FormatStackedWidget.addWidget(self.CSVPage)
        self.SourceLayout.addWidget(self.FormatStackedWidget)
        SongImportWizard.addPage(self.SourcePage)
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
        SongImportWizard.addPage(self.ImportPage)
        self.retranslateUi(SongImportWizard)
        self.FormatStackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.FormatComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.FormatStackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(SongImportWizard)

    def retranslateUi(self, SongImportWizard):
        SongImportWizard.setWindowTitle(
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
            translate('SongsPlugin.ImportWizardForm', 'OpenLyrics'))
        self.FormatComboBox.setItemText(1,
            translate('SongsPlugin.ImportWizardForm', 'OpenSong'))
        self.FormatComboBox.setItemText(2,
            translate('SongsPlugin.ImportWizardForm', 'CCLI'))
        self.FormatComboBox.setItemText(3,
            translate('SongsPlugin.ImportWizardForm', 'CSV'))
        self.OpenLyricsAddButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        self.OpenLyricsRemoveButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
        self.OpenSongAddButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        self.OpenSongRemoveButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
        self.CCLIAddButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        self.CCLIRemoveButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
        self.CSVFilenameLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
        self.CSVBrowseButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
        self.ImportPage.setTitle(
            translate('SongsPlugin.ImportWizardForm', 'Importing'))
        self.ImportPage.setSubTitle(
            translate('SongsPlugin.ImportWizardForm',
                'Please wait while your songs are imported.'))
        self.ImportProgressLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Ready.'))
        self.ImportProgressBar.setFormat(
            translate('SongsPlugin.ImportWizardForm', '%p%'))
