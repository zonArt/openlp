# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
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
        self.openIcon = build_icon(u':/general/general_open.png')
        self.deleteIcon = build_icon(u':/general/general_delete.png')
        songImportWizard.setObjectName(u'songImportWizard')
        songImportWizard.setModal(True)
        songImportWizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        songImportWizard.setOptions(
            QtGui.QWizard.IndependentPages |
            QtGui.QWizard.NoBackButtonOnStartPage |
            QtGui.QWizard.NoBackButtonOnLastPage)
        # Welcome Page
        self.welcomePage = QtGui.QWizardPage()
        self.welcomePage.setPixmap(QtGui.QWizard.WatermarkPixmap,
            QtGui.QPixmap(u':/wizards/wizard_importsong.bmp'))
        self.welcomePage.setObjectName(u'WelcomePage')
        self.welcomeLayout = QtGui.QVBoxLayout(self.welcomePage)
        self.welcomeLayout.setObjectName(u'WelcomeLayout')
        self.titleLabel = QtGui.QLabel(self.welcomePage)
        self.titleLabel.setObjectName(u'TitleLabel')
        self.welcomeLayout.addWidget(self.titleLabel)
        self.welcomeLayout.addSpacing(40)
        self.informationLabel = QtGui.QLabel(self.welcomePage)
        self.informationLabel.setWordWrap(True)
        self.informationLabel.setObjectName(u'InformationLabel')
        self.welcomeLayout.addWidget(self.informationLabel)
        self.welcomeLayout.addStretch()
        songImportWizard.addPage(self.welcomePage)
        # Source Page
        self.sourcePage = QtGui.QWizardPage()
        self.sourcePage.setObjectName(u'SourcePage')
        self.sourceLayout = QtGui.QVBoxLayout(self.sourcePage)
        self.sourceLayout.setObjectName(u'SourceLayout')
        self.formatLayout = QtGui.QFormLayout()
        self.formatLayout.setObjectName(u'FormatLayout')
        self.formatLabel = QtGui.QLabel(self.sourcePage)
        self.formatLabel.setObjectName(u'FormatLabel')
        self.formatComboBox = QtGui.QComboBox(self.sourcePage)
        self.formatComboBox.setObjectName(u'FormatComboBox')
        self.formatLayout.addRow(self.formatLabel, self.formatComboBox)
        self.formatSpacer = QtGui.QSpacerItem(10, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Minimum)
        self.formatLayout.setItem(1, QtGui.QFormLayout.LabelRole,
            self.formatSpacer)
        self.sourceLayout.addLayout(self.formatLayout)
        self.formatStack = QtGui.QStackedLayout()
        self.formatStack.setObjectName(u'FormatStack')
        # OpenLP 2.0
        self.addSingleFileSelectItem(u'openLP2')
        # openlp.org 1.x
        self.addSingleFileSelectItem(u'openLP1', None, True)
        # OpenLyrics
        self.addMultiFileSelectItem(u'openLyrics', u'OpenLyrics', True)
        # Open Song
        self.addMultiFileSelectItem(u'openSong', u'OpenSong')
        # Words of Worship
        self.addMultiFileSelectItem(u'wordsOfWorship')
        # CCLI File import
        self.addMultiFileSelectItem(u'ccli')
        # Songs of Fellowship
        self.addMultiFileSelectItem(u'songsOfFellowship', None, True)
        # Generic Document/Presentation import
        self.addMultiFileSelectItem(u'generic', None, True)
        # EasyWorship
        self.addSingleFileSelectItem(u'easiSlides')
        # EasyWorship
        self.addSingleFileSelectItem(u'ew')
        # Words of Worship
        self.addMultiFileSelectItem(u'songBeamer')
#        Commented out for future use.
#        self.addSingleFileSelectItem(u'csv', u'CSV')
        self.sourceLayout.addLayout(self.formatStack)
        songImportWizard.addPage(self.sourcePage)
        # Import Page
        self.importPage = QtGui.QWizardPage()
        self.importPage.setObjectName(u'ImportPage')
        self.importLayout = QtGui.QVBoxLayout(self.importPage)
        self.importLayout.setMargin(48)
        self.importLayout.setObjectName(u'ImportLayout')
        self.importProgressLabel = QtGui.QLabel(self.importPage)
        self.importProgressLabel.setObjectName(u'ImportProgressLabel')
        self.importLayout.addWidget(self.importProgressLabel)
        self.importProgressBar = QtGui.QProgressBar(self.importPage)
        self.importProgressBar.setObjectName(u'ImportProgressBar')
        self.importLayout.addWidget(self.importProgressBar)
        songImportWizard.addPage(self.importPage)
        self.retranslateUi(songImportWizard)
        self.formatStack.setCurrentIndex(0)
        QtCore.QObject.connect(self.formatComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.formatStack.setCurrentIndex)
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
            translate('SongsPlugin.ImportWizardForm', 'EasiSlides'))
        self.formatComboBox.setItemText(9,
            translate('SongsPlugin.ImportWizardForm', 'EasyWorship'))
        self.formatComboBox.setItemText(10,
            translate('SongsPlugin.ImportWizardForm', 'SongBeamer'))
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
        self.openLyricsAddButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        self.openLyricsRemoveButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
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
        self.easiSlidesFilenameLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
        self.easiSlidesBrowseButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
        self.ewFilenameLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Filename:'))
        self.ewBrowseButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Browse...'))
        self.songBeamerAddButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Add Files...'))
        self.songBeamerRemoveButton.setText(
            translate('SongsPlugin.ImportWizardForm', 'Remove File(s)'))
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
        # Align all QFormLayouts towards each other.
        width = max(self.formatLabel.minimumSizeHint().width(),
            self.openLP2FilenameLabel.minimumSizeHint().width())
        self.formatSpacer.changeSize(width, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        self.openLP2FormLabelSpacer.changeSize(width, 0,
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.openLP1FormLabelSpacer.changeSize(width, 0,
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.easiSlidesFormLabelSpacer.changeSize(width, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        self.ewFormLabelSpacer.changeSize(width, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
#        self.csvFormLabelSpacer.changeSize(width, 0, QtGui.QSizePolicy.Fixed,
#            QtGui.QSizePolicy.Fixed)

    def addSingleFileSelectItem(self, prefix, obj_prefix=None,
        can_disable=False):
        if not obj_prefix:
            obj_prefix = prefix
        page = QtGui.QWidget()
        page.setObjectName(obj_prefix + u'Page')
        if can_disable:
            importWidget = self.disablableWidget(page, prefix, obj_prefix)
        else:
            importWidget = page
        importLayout = QtGui.QFormLayout(importWidget)
        importLayout.setMargin(0)
        if can_disable:
            importLayout.setObjectName(obj_prefix + u'ImportLayout')
        else:
            importLayout.setObjectName(obj_prefix + u'Layout')
        filenameLabel = QtGui.QLabel(importWidget)
        filenameLabel.setObjectName(obj_prefix + u'FilenameLabel')
        fileLayout = QtGui.QHBoxLayout()
        fileLayout.setObjectName(obj_prefix + u'FileLayout')
        filenameEdit = QtGui.QLineEdit(importWidget)
        filenameEdit.setObjectName(obj_prefix + u'FilenameEdit')
        fileLayout.addWidget(filenameEdit)
        browseButton = QtGui.QToolButton(importWidget)
        browseButton.setIcon(self.openIcon)
        browseButton.setObjectName(obj_prefix + u'BrowseButton')
        fileLayout.addWidget(browseButton)
        importLayout.addRow(filenameLabel, fileLayout)
        formSpacer = QtGui.QSpacerItem(10, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Minimum)
        importLayout.setItem(1, QtGui.QFormLayout.LabelRole, formSpacer)
        self.formatStack.addWidget(page)
        setattr(self, prefix + u'Page', page)
        setattr(self, prefix + u'FilenameLabel', filenameLabel)
        setattr(self, prefix + u'FormLabelSpacer', formSpacer)
        setattr(self, prefix + u'FileLayout', fileLayout)
        setattr(self, prefix + u'FilenameEdit', filenameEdit)
        setattr(self, prefix + u'BrowseButton', browseButton)
        if can_disable:
            setattr(self, prefix + u'ImportLayout', importLayout)
        else:
            setattr(self, prefix + u'Layout', importLayout)
        self.formatComboBox.addItem(u'')

    def addMultiFileSelectItem(self, prefix, obj_prefix=None,
        can_disable=False):
        if not obj_prefix:
            obj_prefix = prefix
        page = QtGui.QWidget()
        page.setObjectName(obj_prefix + u'Page')
        if can_disable:
            importWidget = self.disablableWidget(page, prefix, obj_prefix)
        else:
            importWidget = page
        importLayout = QtGui.QVBoxLayout(importWidget)
        importLayout.setMargin(0)
        if can_disable:
            importLayout.setObjectName(obj_prefix + u'ImportLayout')
        else:
            importLayout.setObjectName(obj_prefix + u'Layout')
        fileListWidget = QtGui.QListWidget(importWidget)
        fileListWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        fileListWidget.setObjectName(obj_prefix + u'FileListWidget')
        importLayout.addWidget(fileListWidget)
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.setObjectName(obj_prefix + u'ButtonLayout')
        addButton = QtGui.QPushButton(importWidget)
        addButton.setIcon(self.openIcon)
        addButton.setObjectName(obj_prefix + u'AddButton')
        buttonLayout.addWidget(addButton)
        buttonLayout.addStretch()
        removeButton = QtGui.QPushButton(importWidget)
        removeButton.setIcon(self.deleteIcon)
        removeButton.setObjectName(obj_prefix + u'RemoveButton')
        buttonLayout.addWidget(removeButton)
        importLayout.addLayout(buttonLayout)
        self.formatStack.addWidget(page)
        setattr(self, prefix + u'Page', page)
        setattr(self, prefix + u'FileListWidget', fileListWidget)
        setattr(self, prefix + u'ButtonLayout', buttonLayout)
        setattr(self, prefix + u'AddButton', addButton)
        setattr(self, prefix + u'RemoveButton', removeButton)
        if can_disable:
            setattr(self, prefix + u'ImportLayout', importLayout)
        else:
            setattr(self, prefix + u'Layout', importLayout)
        self.formatComboBox.addItem(u'')

    def disablableWidget(self, page, prefix, obj_prefix):
        layout = QtGui.QVBoxLayout(page)
        layout.setMargin(0)
        layout.setSpacing(0)
        layout.setObjectName(obj_prefix + u'Layout')
        disabledWidget = QtGui.QWidget(page)
        disabledWidget.setVisible(False)
        disabledWidget.setObjectName(obj_prefix + u'DisabledWidget')
        disabledLayout = QtGui.QVBoxLayout(disabledWidget)
        disabledLayout.setMargin(0)
        disabledLayout.setObjectName(obj_prefix + u'DisabledLayout')
        disabledLabel = QtGui.QLabel(disabledWidget)
        disabledLabel.setWordWrap(True)
        disabledLabel.setObjectName(obj_prefix + u'DisabledLabel')
        disabledLayout.addWidget(disabledLabel)
        layout.addWidget(disabledWidget)
        importWidget = QtGui.QWidget(page)
        importWidget.setObjectName(obj_prefix + u'ImportWidget')
        layout.addWidget(importWidget)
        setattr(self, prefix + u'Layout', layout)
        setattr(self, prefix + u'DisabledWidget', disabledWidget)
        setattr(self, prefix + u'DisabledLayout', disabledLayout)
        setattr(self, prefix + u'DisabledLabel', disabledLabel)
        setattr(self, prefix + u'ImportWidget', importWidget)
        return importWidget
