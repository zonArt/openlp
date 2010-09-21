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
        self.openLP1Layout = QtGui.QVBoxLayout(self.openLP1Page)
        self.openLP1Layout.setMargin(0)
        self.openLP1Layout.setSpacing(0)
        self.openLP1Layout.setObjectName(u'openLP1Layout')
        self.openLP1DisabledWidget = QtGui.QWidget(self.openLP1Page)
        self.openLP1DisabledLayout = QtGui.QVBoxLayout(self.openLP1DisabledWidget)
        self.openLP1DisabledLayout.setMargin(0)
        self.openLP1DisabledLayout.setSpacing(8)
        self.openLP1DisabledLayout.setObjectName(u'openLP1DisabledLayout')
        self.openLP1DisabledLabel = QtGui.QLabel(self.openLP1DisabledWidget)
        self.openLP1DisabledLabel.setWordWrap(True)
        self.openLP1DisabledLabel.setObjectName(u'openLP1DisabledLabel')
        self.openLP1DisabledLayout.addWidget(self.openLP1DisabledLabel)
        self.openLP1DisabledWidget.setVisible(False)
        self.openLP1Layout.addWidget(self.openLP1DisabledWidget)
        self.openLP1ImportWidget = QtGui.QWidget(self.openLP1Page)
        self.openLP1ImportLayout = QtGui.QFormLayout(self.openLP1ImportWidget)
        self.openLP1ImportLayout.setMargin(0)
        self.openLP1ImportLayout.setSpacing(8)
        self.openLP1ImportLayout.setObjectName(u'openLP1ImportLayout')
        self.openLP1FilenameLabel = QtGui.QLabel(self.openLP1ImportWidget)
        self.openLP1FilenameLabel.setObjectName(u'openLP1FilenameLabel')
        self.openLP1ImportLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.openLP1FilenameLabel)
        self.openLP1FileLayout = QtGui.QHBoxLayout()
        self.openLP1FileLayout.setSpacing(8)
        self.openLP1FileLayout.setObjectName(u'openLP1FileLayout')
        self.openLP1FilenameEdit = QtGui.QLineEdit(self.openLP1ImportWidget)
        self.openLP1FilenameEdit.setObjectName(u'openLP1FilenameEdit')
        self.openLP1FileLayout.addWidget(self.openLP1FilenameEdit)
        self.openLP1BrowseButton = QtGui.QToolButton(self.openLP1ImportWidget)
        self.openLP1BrowseButton.setIcon(openIcon)
        self.openLP1BrowseButton.setObjectName(u'openLP1BrowseButton')
        self.openLP1FileLayout.addWidget(self.openLP1BrowseButton)
        self.openLP1ImportLayout.setLayout(0, QtGui.QFormLayout.FieldRole,
            self.openLP1FileLayout)
        self.openLP1Layout.addWidget(self.openLP1ImportWidget)
        self.formatStackedWidget.addWidget(self.openLP1Page)
        # OpenLyrics
        self.openLyricsPage = QtGui.QWidget()
        self.openLyricsPage.setObjectName(u'OpenLyricsPage')
        self.openLyricsLayout = QtGui.QVBoxLayout(self.openLyricsPage)
        self.openLyricsLayout.setSpacing(8)
        self.openLyricsLayout.setMargin(0)
        self.openLyricsLayout.setObjectName(u'OpenLyricsLayout')
        self.openLyricsDisabledLabel = QtGui.QLabel(self.openLyricsPage)
        self.openLyricsDisabledLabel.setWordWrap(True)
        self.openLyricsDisabledLabel.setObjectName(u'openLyricsDisabledLabel')
        self.openLyricsLayout.addWidget(self.openLyricsDisabledLabel)
        # Commented out for future use.
        #self.openLyricsFileListWidget = QtGui.QListWidget(self.openLyricsPage)
        #self.openLyricsFileListWidget.setSelectionMode(
        #    QtGui.QAbstractItemView.ExtendedSelection)
        #self.openLyricsFileListWidget.setObjectName(u'OpenLyricsFileListWidget')
        #self.openLyricsLayout.addWidget(self.openLyricsFileListWidget)
        #self.openLyricsButtonLayout = QtGui.QHBoxLayout()
        #self.openLyricsButtonLayout.setSpacing(8)
        #self.openLyricsButtonLayout.setObjectName(u'OpenLyricsButtonLayout')
        #self.openLyricsAddButton = QtGui.QPushButton(self.openLyricsPage)
        #self.openLyricsAddButton.setIcon(openIcon)
        #self.openLyricsAddButton.setObjectName(u'OpenLyricsAddButton')
        #self.openLyricsButtonLayout.addWidget(self.openLyricsAddButton)
        #self.openLyricsButtonSpacer = QtGui.QSpacerItem(40, 20,
        #    QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        #self.openLyricsButtonLayout.addItem(self.openLyricsButtonSpacer)
        #self.openLyricsRemoveButton = QtGui.QPushButton(self.openLyricsPage)
        #self.openLyricsRemoveButton.setIcon(deleteIcon)
        #self.openLyricsRemoveButton.setObjectName(u'OpenLyricsRemoveButton')
        #self.openLyricsButtonLayout.addWidget(self.openLyricsRemoveButton)
        #self.openLyricsLayout.addLayout(self.openLyricsButtonLayout)
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
        self.wordsOfWorshipFileListWidget = QtGui.QListWidget(
            self.wordsOfWorshipPage)
        self.wordsOfWorshipFileListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.wordsOfWorshipFileListWidget.setObjectName(
            u'wordsOfWorshipFileListWidget')
        self.wordsOfWorshipLayout.addWidget(self.wordsOfWorshipFileListWidget)
        self.wordsOfWorshipButtonLayout = QtGui.QHBoxLayout()
        self.wordsOfWorshipButtonLayout.setSpacing(8)
        self.wordsOfWorshipButtonLayout.setObjectName(
            u'wordsOfWorshipButtonLayout')
        self.wordsOfWorshipAddButton = QtGui.QPushButton(
            self.wordsOfWorshipPage)
        self.wordsOfWorshipAddButton.setIcon(openIcon)
        self.wordsOfWorshipAddButton.setObjectName(u'wordsOfWorshipAddButton')
        self.wordsOfWorshipButtonLayout.addWidget(self.wordsOfWorshipAddButton)
        self.wordsOfWorshipButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.wordsOfWorshipButtonLayout.addItem(self.wordsOfWorshipButtonSpacer)
        self.wordsOfWorshipRemoveButton = QtGui.QPushButton(
            self.wordsOfWorshipPage)
        self.wordsOfWorshipRemoveButton.setIcon(deleteIcon)
        self.wordsOfWorshipRemoveButton.setObjectName(
            u'wordsOfWorshipRemoveButton')
        self.wordsOfWorshipButtonLayout.addWidget(
            self.wordsOfWorshipRemoveButton)
        self.wordsOfWorshipLayout.addLayout(self.wordsOfWorshipButtonLayout)
        self.formatStackedWidget.addWidget(self.wordsOfWorshipPage)
        # CCLI File import
        self.ccliPage = QtGui.QWidget()
        self.ccliPage.setObjectName(u'ccliPage')
        self.ccliLayout = QtGui.QVBoxLayout(self.ccliPage)
        self.ccliLayout.setSpacing(8)
        self.ccliLayout.setMargin(0)
        self.ccliLayout.setObjectName(u'ccliLayout')
        self.ccliFileListWidget = QtGui.QListWidget(self.ccliPage)
        self.ccliFileListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.ccliFileListWidget.setObjectName(u'ccliFileListWidget')
        self.ccliLayout.addWidget(self.ccliFileListWidget)
        self.ccliButtonLayout = QtGui.QHBoxLayout()
        self.ccliButtonLayout.setSpacing(8)
        self.ccliButtonLayout.setObjectName(u'ccliButtonLayout')
        self.ccliAddButton = QtGui.QPushButton(self.ccliPage)
        self.ccliAddButton.setIcon(openIcon)
        self.ccliAddButton.setObjectName(u'ccliAddButton')
        self.ccliButtonLayout.addWidget(self.ccliAddButton)
        self.ccliButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ccliButtonLayout.addItem(self.ccliButtonSpacer)
        self.ccliRemoveButton = QtGui.QPushButton(self.ccliPage)
        self.ccliRemoveButton.setIcon(deleteIcon)
        self.ccliRemoveButton.setObjectName(u'ccliRemoveButton')
        self.ccliButtonLayout.addWidget(self.ccliRemoveButton)
        self.ccliLayout.addLayout(self.ccliButtonLayout)
        self.formatStackedWidget.addWidget(self.ccliPage)
        # Songs of Fellowship
        self.songsOfFellowshipPage = QtGui.QWidget()
        self.songsOfFellowshipPage.setObjectName(u'songsOfFellowshipPage')
        self.songsOfFellowshipLayout = QtGui.QVBoxLayout(
            self.songsOfFellowshipPage)
        self.songsOfFellowshipLayout.setMargin(0)
        self.songsOfFellowshipLayout.setSpacing(0)
        self.songsOfFellowshipLayout.setObjectName(u'songsOfFellowshipLayout')
        self.songsOfFellowshipDisabledWidget = QtGui.QWidget(
            self.songsOfFellowshipPage)
        self.songsOfFellowshipDisabledWidget.setVisible(False)
        self.songsOfFellowshipDisabledWidget.setObjectName(
            u'songsOfFellowshipDisabledWidget')
        self.songsOfFellowshipDisabledLayout = QtGui.QVBoxLayout(
            self.songsOfFellowshipDisabledWidget)
        self.songsOfFellowshipDisabledLayout.setMargin(0)
        self.songsOfFellowshipDisabledLayout.setSpacing(8)
        self.songsOfFellowshipDisabledLayout.setObjectName(
            u'songsOfFellowshipDisabledLayout')
        self.songsOfFellowshipDisabledLabel = QtGui.QLabel(
            self.songsOfFellowshipDisabledWidget)
        self.songsOfFellowshipDisabledLabel.setWordWrap(True)
        self.songsOfFellowshipDisabledLabel.setObjectName(
            u'songsOfFellowshipDisabledLabel')
        self.songsOfFellowshipDisabledLayout.addWidget(
            self.songsOfFellowshipDisabledLabel)
        self.songsOfFellowshipLayout.addWidget(
            self.songsOfFellowshipDisabledWidget)
        self.songsOfFellowshipImportWidget = QtGui.QWidget(
            self.songsOfFellowshipPage)
        self.songsOfFellowshipImportWidget.setObjectName(
            u'songsOfFellowshipImportWidget')
        self.songsOfFellowshipImportLayout = QtGui.QVBoxLayout(
            self.songsOfFellowshipImportWidget)
        self.songsOfFellowshipImportLayout.setMargin(0)
        self.songsOfFellowshipImportLayout.setSpacing(8)
        self.songsOfFellowshipImportLayout.setObjectName(
            u'songsOfFellowshipImportLayout')
        self.songsOfFellowshipFileListWidget = QtGui.QListWidget(
            self.songsOfFellowshipImportWidget)
        self.songsOfFellowshipFileListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.songsOfFellowshipFileListWidget.setObjectName(
            u'songsOfFellowshipFileListWidget')
        self.songsOfFellowshipImportLayout.addWidget(
            self.songsOfFellowshipFileListWidget)
        self.songsOfFellowshipButtonLayout = QtGui.QHBoxLayout()
        self.songsOfFellowshipButtonLayout.setSpacing(8)
        self.songsOfFellowshipButtonLayout.setObjectName(
            u'songsOfFellowshipButtonLayout')
        self.songsOfFellowshipAddButton = QtGui.QPushButton(
            self.songsOfFellowshipImportWidget)
        self.songsOfFellowshipAddButton.setIcon(openIcon)
        self.songsOfFellowshipAddButton.setObjectName(
            u'songsOfFellowshipAddButton')
        self.songsOfFellowshipButtonLayout.addWidget(
            self.songsOfFellowshipAddButton)
        self.songsOfFellowshipButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.songsOfFellowshipButtonLayout.addItem(
            self.songsOfFellowshipButtonSpacer)
        self.songsOfFellowshipRemoveButton = QtGui.QPushButton(
            self.songsOfFellowshipImportWidget)
        self.songsOfFellowshipRemoveButton.setIcon(deleteIcon)
        self.songsOfFellowshipRemoveButton.setObjectName(
            u'songsOfFellowshipRemoveButton')
        self.songsOfFellowshipButtonLayout.addWidget(
            self.songsOfFellowshipRemoveButton)
        self.songsOfFellowshipImportLayout.addLayout(
            self.songsOfFellowshipButtonLayout)
        self.songsOfFellowshipLayout.addWidget(
            self.songsOfFellowshipImportWidget)
        self.formatStackedWidget.addWidget(self.songsOfFellowshipPage)
        # Generic Document/Presentation import
        self.genericPage = QtGui.QWidget()
        self.genericPage.setObjectName(u'genericPage')
        self.genericLayout = QtGui.QVBoxLayout(self.genericPage)
        self.genericLayout.setMargin(0)
        self.genericLayout.setSpacing(0)
        self.genericLayout.setObjectName(u'genericLayout')
        self.genericDisabledWidget = QtGui.QWidget(self.genericPage)
        self.genericDisabledWidget.setObjectName(u'genericDisabledWidget')
        self.genericDisabledLayout = QtGui.QVBoxLayout(self.genericDisabledWidget)
        self.genericDisabledLayout.setMargin(0)
        self.genericDisabledLayout.setSpacing(8)
        self.genericDisabledLayout.setObjectName(u'genericDisabledLayout')
        self.genericDisabledLabel = QtGui.QLabel(self.genericDisabledWidget)
        self.genericDisabledLabel.setWordWrap(True)
        self.genericDisabledLabel.setObjectName(u'genericDisabledLabel')
        self.genericDisabledWidget.setVisible(False)
        self.genericDisabledLayout.addWidget(self.genericDisabledLabel)
        self.genericLayout.addWidget(self.genericDisabledWidget)
        self.genericImportWidget = QtGui.QWidget(self.genericPage)
        self.genericImportWidget.setObjectName(u'genericImportWidget')
        self.genericImportLayout = QtGui.QVBoxLayout(self.genericImportWidget)
        self.genericImportLayout.setMargin(0)
        self.genericImportLayout.setSpacing(8)
        self.genericImportLayout.setObjectName(u'genericImportLayout')
        self.genericFileListWidget = QtGui.QListWidget(self.genericImportWidget)
        self.genericFileListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.genericFileListWidget.setObjectName(u'genericFileListWidget')
        self.genericImportLayout.addWidget(self.genericFileListWidget)
        self.genericButtonLayout = QtGui.QHBoxLayout()
        self.genericButtonLayout.setSpacing(8)
        self.genericButtonLayout.setObjectName(u'genericButtonLayout')
        self.genericAddButton = QtGui.QPushButton(self.genericImportWidget)
        self.genericAddButton.setIcon(openIcon)
        self.genericAddButton.setObjectName(u'genericAddButton')
        self.genericButtonLayout.addWidget(self.genericAddButton)
        self.genericButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.genericButtonLayout.addItem(self.genericButtonSpacer)
        self.genericRemoveButton = QtGui.QPushButton(self.genericImportWidget)
        self.genericRemoveButton.setIcon(deleteIcon)
        self.genericRemoveButton.setObjectName(u'genericRemoveButton')
        self.genericButtonLayout.addWidget(self.genericRemoveButton)
        self.genericImportLayout.addLayout(self.genericButtonLayout)
        self.genericLayout.addWidget(self.genericImportWidget)
        self.formatStackedWidget.addWidget(self.genericPage)
        # EasyWorship
        self.ewPage = QtGui.QWidget()
        self.ewPage.setObjectName(u'ewPage')
        self.ewLayout = QtGui.QFormLayout(self.ewPage)
        self.ewLayout.setMargin(0)
        self.ewLayout.setSpacing(8)
        self.ewLayout.setObjectName(u'ewLayout')
        self.ewFilenameLabel = QtGui.QLabel(self.ewPage)
        self.ewFilenameLabel.setObjectName(u'ewFilenameLabel')
        self.ewLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.ewFilenameLabel)
        self.ewFileLayout = QtGui.QHBoxLayout()
        self.ewFileLayout.setSpacing(8)
        self.ewFileLayout.setObjectName(u'ewFileLayout')
        self.ewFilenameEdit = QtGui.QLineEdit(self.ewPage)
        self.ewFilenameEdit.setObjectName(u'ewFilenameEdit')
        self.ewFileLayout.addWidget(self.ewFilenameEdit)
        self.ewBrowseButton = QtGui.QToolButton(self.ewPage)
        self.ewBrowseButton.setIcon(openIcon)
        self.ewBrowseButton.setObjectName(u'ewBrowseButton')
        self.ewFileLayout.addWidget(self.ewBrowseButton)
        self.ewLayout.setLayout(0, QtGui.QFormLayout.FieldRole,
            self.ewFileLayout)
        self.formatStackedWidget.addWidget(self.ewPage)
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
            translate('SongsPlugin.ImportWizardForm', 'Song Import Wizard'))
        self.titleLabel.setText(
            u'<span style="font-size:14pt; font-weight:600;">%s</span>' % \
            translate('SongsPlugin.ImportWizardForm',
                'Welcome to the Song Import Wizard'))
        self.informationLabel.setText(
            translate('SongsPlugin.ImportWizardForm',
                'This wizard will help you to import songs from a variety of '
                'formats. Click the next button below to start the process by '
                'selecting a format to import from.'))
        self.sourcePage.setTitle(
            translate('SongsPlugin.ImportWizardForm', 'Select Import Source'))
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
            translate('SongsPlugin.ImportWizardForm', 'CCLI/SongSelect'))
        self.formatComboBox.setItemText(6,
            translate('SongsPlugin.ImportWizardForm', 'Songs of Fellowship'))
        self.formatComboBox.setItemText(7,
            translate('SongsPlugin.ImportWizardForm',
            'Generic Document/Presentation'))
        self.formatComboBox.setItemText(8,
            translate('SongsPlugin.ImportWizardForm', 'EasyWorship'))
#        self.formatComboBox.setItemText(9,
#            translate('SongsPlugin.ImportWizardForm', 'CSV'))
        self.openLP2FilenameLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
        self.openLP2BrowseButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
        self.openLP1FilenameLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
        self.openLP1BrowseButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
        self.openLP1DisabledLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'The openlp.org 1.x '
            'importer has been disabled due to a missing Python module. If '
            'you want to use this importer, you will need to install the '
            '"python-sqlite" module.'))
        #self.openLyricsAddButton.setText(
        #    translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        #self.openLyricsRemoveButton.setText(
        #    translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
        self.openLyricsDisabledLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'The OpenLyrics '
            'importer has not yet been developed, but as you can see, we are '
            'still intending to do so. Hopefully it will be in the next '
            'release.'))
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
        self.songsOfFellowshipAddButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        self.songsOfFellowshipRemoveButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
        self.songsOfFellowshipDisabledLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'The Songs of '
            'Fellowship importer has been disabled because OpenLP cannot '
            'find OpenOffice.org on your computer.'))
        self.genericAddButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        self.genericRemoveButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
        self.genericDisabledLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'The generic document/'
            'presentation importer has been disabled because OpenLP cannot '
            'find OpenOffice.org on your computer.'))
        self.ewFilenameLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
        self.ewBrowseButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
#        self.csvFilenameLabel.setText(
#            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
#        self.csvBrowseButton.setText(
#            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
        self.importPage.setTitle(
            translate('SongsPlugin.ImportWizardForm', 'Importing'))
        self.importPage.setSubTitle(
            translate('SongsPlugin.ImportWizardForm',
                'Please wait while your songs are imported.'))
        self.importProgressLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Ready.'))
        self.importProgressBar.setFormat(
            translate('SongsPlugin.ImportWizardForm', '%p%'))
