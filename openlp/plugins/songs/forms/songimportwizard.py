# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

class Ui_SongImportWizard(object):
    def setupUi(self, SongImportWizard):
        SongImportWizard.setObjectName(u'SongImportWizard')
        SongImportWizard.resize(550, 386)
        SongImportWizard.setMinimumSize(QtCore.QSize(166, 386))
        SongImportWizard.setModal(True)
        SongImportWizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        SongImportWizard.setOptions(QtGui.QWizard.NoBackButtonOnLastPage |
            QtGui.QWizard.NoBackButtonOnStartPage)
        self.WelcomePage = QtGui.QWizardPage()
        self.WelcomePage.setObjectName(u'WelcomePage')
        self.WelcomeLayout = QtGui.QHBoxLayout(self.WelcomePage)
        self.WelcomeLayout.setSpacing(8)
        self.WelcomeLayout.setMargin(0)
        self.WelcomeLayout.setObjectName(u'WelcomeLayout')
        self.ImportSongImage = QtGui.QLabel(self.WelcomePage)
        self.ImportSongImage.setMinimumSize(QtCore.QSize(163, 0))
        self.ImportSongImage.setMaximumSize(QtCore.QSize(163, 16777215))
        self.ImportSongImage.setPixmap(
            QtGui.QPixmap(u':/wizards/wizard_importsong.bmp'))
        self.ImportSongImage.setObjectName(u'ImportSongImage')
        self.WelcomeLayout.addWidget(self.ImportSongImage)
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
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FormatComboBox.sizePolicy().hasHeightForWidth())
        self.FormatComboBox.setSizePolicy(sizePolicy)
        self.FormatComboBox.setObjectName(u'FormatComboBox')
        self.FormatComboBox.addItem(u'')
        self.FormatComboBox.addItem(u'')
        self.FormatLayout.addWidget(self.FormatComboBox)
        self.FormatSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.FormatLayout.addItem(self.FormatSpacer)
        self.SourceLayout.addLayout(self.FormatLayout)
        self.FormatStackedWidget = QtGui.QStackedWidget(self.SourcePage)
        self.FormatStackedWidget.setObjectName(u'FormatStackedWidget')
        self.OpenSongFilePage = QtGui.QWidget()
        self.OpenSongFilePage.setObjectName(u'OpenSongFilePage')
        self.OpenSongFileLayout = QtGui.QFormLayout(self.OpenSongFilePage)
        self.OpenSongFileLayout.setMargin(0)
        self.OpenSongFileLayout.setSpacing(8)
        self.OpenSongFileLayout.setObjectName(u'OpenSongFileLayout')
        self.OpenSongFileLabel = QtGui.QLabel(self.OpenSongFilePage)
        self.OpenSongFileLabel.setObjectName(u'OpenSongFileLabel')
        self.OpenSongFileLayout.setWidget(0,
            QtGui.QFormLayout.LabelRole, self.OpenSongFileLabel)
        self.OpenSongFilenameLayout = QtGui.QHBoxLayout()
        self.OpenSongFilenameLayout.setSpacing(8)
        self.OpenSongFilenameLayout.setObjectName(u'OpenSongFilenameLayout')
        self.OpenSongFilenameLineEdit = QtGui.QLineEdit(self.OpenSongFilePage)
        self.OpenSongFilenameLineEdit.setObjectName(u'OpenSongFilenameLineEdit')
        self.OpenSongFilenameLayout.addWidget(self.OpenSongFilenameLineEdit)
        self.OpenSongFilenameButton = QtGui.QToolButton(self.OpenSongFilePage)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/imports/import_load.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.OpenSongFilenameButton.setIcon(icon)
        self.OpenSongFilenameButton.setObjectName(u'OpenSongFilenameButton')
        self.OpenSongFilenameLayout.addWidget(self.OpenSongFilenameButton)
        self.OpenSongFileLayout.setLayout(0,
            QtGui.QFormLayout.FieldRole, self.OpenSongFilenameLayout)
        self.FormatStackedWidget.addWidget(self.OpenSongFilePage)
        self.OpenSongDirectoryPage = QtGui.QWidget()
        self.OpenSongDirectoryPage.setObjectName(u'OpenSongDirectoryPage')
        self.OpenSongDirectoryLayout = QtGui.QFormLayout(self.OpenSongDirectoryPage)
        self.OpenSongDirectoryLayout.setMargin(0)
        self.OpenSongDirectoryLayout.setSpacing(8)
        self.OpenSongDirectoryLayout.setObjectName(u'OpenSongDirectoryLayout')
        self.OpenSongDirectoryLabel = QtGui.QLabel(self.OpenSongDirectoryPage)
        self.OpenSongDirectoryLabel.setObjectName(u'OpenSongDirectoryLabel')
        self.OpenSongDirectoryLayout.setWidget(0,
            QtGui.QFormLayout.LabelRole, self.OpenSongDirectoryLabel)
        self.OpenSongDirLayout = QtGui.QHBoxLayout()
        self.OpenSongDirLayout.setSpacing(8)
        self.OpenSongDirLayout.setObjectName(u'OpenSongDirLayout')
        self.OpenSongDirectoryLineEdit = QtGui.QLineEdit(self.OpenSongDirectoryPage)
        self.OpenSongDirectoryLineEdit.setObjectName(u'OpenSongDirectoryLineEdit')
        self.OpenSongDirLayout.addWidget(self.OpenSongDirectoryLineEdit)
        self.OpenSongDirectoryButton = QtGui.QToolButton(self.OpenSongDirectoryPage)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(u':/exports/export_load.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.OpenSongDirectoryButton.setIcon(icon1)
        self.OpenSongDirectoryButton.setObjectName(u'OpenSongDirectoryButton')
        self.OpenSongDirLayout.addWidget(self.OpenSongDirectoryButton)
        self.OpenSongDirectoryLayout.setLayout(0,
            QtGui.QFormLayout.FieldRole, self.OpenSongDirLayout)
        self.FormatStackedWidget.addWidget(self.OpenSongDirectoryPage)
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
        self.OpenSongFileLabel.setBuddy(self.OpenSongFilenameLineEdit)

        self.retranslateUi(SongImportWizard)
        self.FormatStackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(
            self.FormatComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.FormatStackedWidget.setCurrentIndex
        )
        QtCore.QMetaObject.connectSlotsByName(SongImportWizard)

    def retranslateUi(self, SongImportWizard):
        SongImportWizard.setWindowTitle(self.trUtf8('Song Import Wizard'))
        self.TitleLabel.setText(self.trUtf8(
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" \n'
            '          "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
            '<html>\n'
            '  <head>\n'
            '    <meta name="qrichtext" content="1" />\n'
            '    <style type="text/css">p, li { white-space: pre-wrap; }</style>\n'
            '  </head>\n'
            '  <body style="font-family: Lucida Grande; font-size:10pt; font-weight:400; font-style:normal;">\n'
            '    <p style="margin: 0; -qt-block-indent:0; text-indent:0px;">\n'
            '     <span style="font-size:14pt; font-weight:600;">\n'
            '       Welcome to the Song Import Wizard\n'
            '     </span>\n'
            '   </p>\n'
            '  </body>\n'
            '</html>'
        ))
        self.InformationLabel.setText(self.trUtf8('This wizard will help you '
            'to import songs from a variety of formats. Click the next button '
            'below to start the process by selecting a format to import from.'))
        self.SourcePage.setTitle(self.trUtf8('Select Import Source'))
        self.SourcePage.setSubTitle(self.trUtf8('Select the import format, '
            'and where to import from.'))
        self.FormatLabel.setText(self.trUtf8('Format:'))
        self.FormatComboBox.setItemText(0, self.trUtf8('OpenSong (Single File)'))
        self.FormatComboBox.setItemText(1, self.trUtf8('OpenSong (Directory of Files)'))
        self.OpenSongFileLabel.setText(self.trUtf8('Filename:'))
        self.OpenSongDirectoryLabel.setText(self.trUtf8('Directory:'))
        self.ImportPage.setTitle(self.trUtf8('Importing'))
        self.ImportPage.setSubTitle(self.trUtf8('Please wait while your songs '
            'are imported.'))
        self.ImportProgressLabel.setText(self.trUtf8('Ready.'))
        self.ImportProgressBar.setFormat(self.trUtf8('%p%'))

