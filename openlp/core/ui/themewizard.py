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

from openlp.core.lib import translate, build_icon

class Ui_ThemeWizard(object):
    def setupUi(self, ThemeWizard):
        ThemeWizard.setObjectName(u'OpenLP.ThemeWizard')
        ThemeWizard.resize(550, 386)
        ThemeWizard.setModal(True)
        ThemeWizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        ThemeWizard.setOptions(
            QtGui.QWizard.IndependentPages |
            QtGui.QWizard.NoBackButtonOnStartPage)
        self.welcomePage = QtGui.QWizardPage()
        self.welcomePage.setTitle(u'')
        self.welcomePage.setSubTitle(u'')
        self.welcomePage.setObjectName(u'welcomePage')
        self.welcomePage.setPixmap(QtGui.QWizard.WatermarkPixmap,
            QtGui.QPixmap(u':/wizards/wizard_createtheme.bmp'))
        self.welcomeLayout = QtGui.QHBoxLayout(self.welcomePage)
        self.welcomeLayout.setSpacing(8)
        self.welcomeLayout.setMargin(0)
        self.welcomeLayout.setObjectName(u'welcomeLayout')
        self.welcomePageLayout = QtGui.QVBoxLayout()
        self.welcomePageLayout.setSpacing(8)
        self.welcomePageLayout.setObjectName(u'welcomePageLayout')
        self.titleLabel = QtGui.QLabel(self.welcomePage)
        self.titleLabel.setObjectName(u'titleLabel')
        self.welcomePageLayout.addWidget(self.titleLabel)
        self.welcomeTopSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.welcomePageLayout.addItem(self.welcomeTopSpacer)
        self.informationLabel = QtGui.QLabel(self.welcomePage)
        self.informationLabel.setWordWrap(True)
        self.informationLabel.setMargin(10)
        self.informationLabel.setObjectName(u'informationLabel')
        self.welcomePageLayout.addWidget(self.informationLabel)
        self.welcomeBottomSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.welcomePageLayout.addItem(self.welcomeBottomSpacer)
        self.welcomeLayout.addLayout(self.welcomePageLayout)
        ThemeWizard.addPage(self.welcomePage)
        self.backgroundPage = QtGui.QWizardPage()
        self.backgroundPage.setObjectName(u'backgroundPage')
        self.backgroundLayout = QtGui.QVBoxLayout(self.backgroundPage)
        self.backgroundLayout.setSpacing(8)
        self.backgroundLayout.setMargin(20)
        self.backgroundLayout.setObjectName(u'backgroundLayout')
        self.backgroundTypeLayout = QtGui.QHBoxLayout()
        self.backgroundTypeLayout.setSpacing(8)
        self.backgroundTypeLayout.setObjectName(u'backgroundTypeLayout')
        self.backgroundTypeLabel = QtGui.QLabel(self.backgroundPage)
        self.backgroundTypeLabel.setObjectName(u'backgroundTypeLabel')
        self.backgroundTypeLayout.addWidget(self.backgroundTypeLabel)
        self.backgroundTypeComboBox = QtGui.QComboBox(self.backgroundPage)
        self.backgroundTypeComboBox.setObjectName(u'backgroundTypeComboBox')
        self.backgroundTypeComboBox.addItem(u'')
        self.backgroundTypeComboBox.addItem(u'')
        self.backgroundTypeComboBox.addItem(u'')
        self.backgroundTypeLayout.addWidget(self.backgroundTypeComboBox)
        self.backgroundTypeSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.backgroundTypeLayout.addItem(self.backgroundTypeSpacer)
        self.backgroundLayout.addLayout(self.backgroundTypeLayout)
        self.backgroundStackedWidget = QtGui.QStackedWidget(
            self.backgroundPage)
        self.backgroundStackedWidget.setObjectName(u'backgroundStackedWidget')
        self.colorPage = QtGui.QWidget()
        self.colorPage.setObjectName(u'colorPage')
        self.colorLayout = QtGui.QFormLayout(self.colorPage)
        self.colorLayout.setMargin(0)
        self.colorLayout.setSpacing(8)
        self.colorLayout.setObjectName(u'colorLayout')
        self.colorLabel = QtGui.QLabel(self.colorPage)
        self.colorLabel.setMinimumSize(QtCore.QSize(103, 0))
        self.colorLabel.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.colorLabel.setObjectName(u'colorLabel')
        self.colorLayout.setWidget(0,
            QtGui.QFormLayout.LabelRole, self.colorLabel)
        self.colorButton = QtGui.QPushButton(self.colorPage)
        self.colorButton.setText(u'')
        self.colorButton.setObjectName(u'colorButton')
        self.colorLayout.setWidget(0,
            QtGui.QFormLayout.FieldRole, self.colorButton)
        self.backgroundStackedWidget.addWidget(self.colorPage)
        self.gradientPage = QtGui.QWidget()
        self.gradientPage.setObjectName(u'gradientPage')
        self.gradientLayout = QtGui.QFormLayout(self.gradientPage)
        self.gradientLayout.setMargin(0)
        self.gradientLayout.setSpacing(8)
        self.gradientLayout.setObjectName(u'gradientLayout')
        self.gradientStartLabel = QtGui.QLabel(self.gradientPage)
        self.gradientStartLabel.setMinimumSize(QtCore.QSize(103, 0))
        self.gradientStartLabel.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.gradientStartLabel.setObjectName(u'gradientStartLabel')
        self.gradientLayout.setWidget(0,
            QtGui.QFormLayout.LabelRole, self.gradientStartLabel)
        self.gradientStartButton = QtGui.QPushButton(self.gradientPage)
        self.gradientStartButton.setText(u'')
        self.gradientStartButton.setObjectName(u'gradientStartButton')
        self.gradientLayout.setWidget(0,
            QtGui.QFormLayout.FieldRole, self.gradientStartButton)
        self.gradientEndLabel = QtGui.QLabel(self.gradientPage)
        self.gradientEndLabel.setMinimumSize(QtCore.QSize(103, 0))
        self.gradientEndLabel.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.gradientEndLabel.setObjectName(u'gradientEndLabel')
        self.gradientLayout.setWidget(1,
            QtGui.QFormLayout.LabelRole, self.gradientEndLabel)
        self.gradientEndButton = QtGui.QPushButton(self.gradientPage)
        self.gradientEndButton.setText(u'')
        self.gradientEndButton.setObjectName(u'gradientEndButton')
        self.gradientLayout.setWidget(1,
            QtGui.QFormLayout.FieldRole, self.gradientEndButton)
        self.gradientTypeLabel = QtGui.QLabel(self.gradientPage)
        self.gradientTypeLabel.setMinimumSize(QtCore.QSize(103, 0))
        self.gradientTypeLabel.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.gradientTypeLabel.setObjectName(u'gradientTypeLabel')
        self.gradientLayout.setWidget(2,
            QtGui.QFormLayout.LabelRole, self.gradientTypeLabel)
        self.gradientComboBox = QtGui.QComboBox(self.gradientPage)
        self.gradientComboBox.setObjectName(u'gradientComboBox')
        self.gradientComboBox.addItem(u'')
        self.gradientComboBox.addItem(u'')
        self.gradientComboBox.addItem(u'')
        self.gradientComboBox.addItem(u'')
        self.gradientComboBox.addItem(u'')
        self.gradientLayout.setWidget(2,
            QtGui.QFormLayout.FieldRole, self.gradientComboBox)
        self.backgroundStackedWidget.addWidget(self.gradientPage)
        self.imagePage = QtGui.QWidget()
        self.imagePage.setObjectName(u'imagePage')
        self.imageLayout = QtGui.QFormLayout(self.imagePage)
        self.imageLayout.setMargin(0)
        self.imageLayout.setSpacing(8)
        self.imageLayout.setObjectName(u'imageLayout')
        self.imageLabel = QtGui.QLabel(self.imagePage)
        self.imageLabel.setMinimumSize(QtCore.QSize(103, 0))
        self.imageLabel.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.imageLabel.setObjectName(u'imageLabel')
        self.imageLayout.setWidget(0,
            QtGui.QFormLayout.LabelRole, self.imageLabel)
        self.imageFileLayout = QtGui.QHBoxLayout()
        self.imageFileLayout.setSpacing(8)
        self.imageFileLayout.setObjectName(u'imageFileLayout')
        self.imageLineEdit = QtGui.QLineEdit(self.imagePage)
        self.imageLineEdit.setObjectName(u'imageLineEdit')
        self.imageFileLayout.addWidget(self.imageLineEdit)
        self.imageBrowseButton = QtGui.QToolButton(self.imagePage)
        self.imageBrowseButton.setText(u'')
        self.imageBrowseButton.setIcon(
            build_icon(u':/general/general_open.png'))
        self.imageBrowseButton.setObjectName(u'imageBrowseButton')
        self.imageFileLayout.addWidget(self.imageBrowseButton)
        self.imageLayout.setLayout(0,
            QtGui.QFormLayout.FieldRole, self.imageFileLayout)
        self.backgroundStackedWidget.addWidget(self.imagePage)
        self.backgroundLayout.addWidget(self.backgroundStackedWidget)
        ThemeWizard.addPage(self.backgroundPage)
        self.mainAreaPage = QtGui.QWizardPage()
        self.mainAreaPage.setObjectName(u'mainAreaPage')
        self.mainAreaLayout = QtGui.QFormLayout(self.mainAreaPage)
        self.mainAreaLayout.setFormAlignment(QtCore.Qt.AlignLeading |
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.mainAreaLayout.setMargin(20)
        self.mainAreaLayout.setSpacing(8)
        self.mainAreaLayout.setObjectName(u'mainAreaLayout')
        self.mainFontLabel = QtGui.QLabel(self.mainAreaPage)
        self.mainFontLabel.setMinimumSize(QtCore.QSize(103, 0))
        self.mainFontLabel.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.mainFontLabel.setObjectName(u'mainFontLabel')
        self.mainAreaLayout.setWidget(0,
            QtGui.QFormLayout.LabelRole, self.mainFontLabel)
        self.mainFontComboBox = QtGui.QFontComboBox(self.mainAreaPage)
        self.mainFontComboBox.setObjectName(u'mainFontComboBox')
        self.mainAreaLayout.setWidget(0,
            QtGui.QFormLayout.FieldRole, self.mainFontComboBox)
        self.mainColorLabel = QtGui.QLabel(self.mainAreaPage)
        self.mainColorLabel.setObjectName(u'mainColorLabel')
        self.mainAreaLayout.setWidget(1,
            QtGui.QFormLayout.LabelRole, self.mainColorLabel)
        self.fontPropertiesLayout = QtGui.QHBoxLayout()
        self.fontPropertiesLayout.setSpacing(24)
        self.fontPropertiesLayout.setObjectName(u'fontPropertiesLayout')
        self.mainColorPushButton = QtGui.QPushButton(self.mainAreaPage)
        self.mainColorPushButton.setText(u'')
        self.mainColorPushButton.setObjectName(u'mainColorPushButton')
        self.fontPropertiesLayout.addWidget(self.mainColorPushButton)
        self.boldCheckBox = QtGui.QCheckBox(self.mainAreaPage)
        self.boldCheckBox.setObjectName(u'boldCheckBox')
        self.fontPropertiesLayout.addWidget(self.boldCheckBox)
        self.italicsCheckBox = QtGui.QCheckBox(self.mainAreaPage)
        self.italicsCheckBox.setObjectName(u'italicsCheckBox')
        self.fontPropertiesLayout.addWidget(self.italicsCheckBox)
        self.mainAreaLayout.setLayout(1,
            QtGui.QFormLayout.FieldRole, self.fontPropertiesLayout)
        self.mainSizeLabel = QtGui.QLabel(self.mainAreaPage)
        self.mainSizeLabel.setObjectName(u'mainSizeLabel')
        self.mainAreaLayout.setWidget(2,
            QtGui.QFormLayout.LabelRole, self.mainSizeLabel)
        self.mainSizeLayout = QtGui.QHBoxLayout()
        self.mainSizeLayout.setSpacing(8)
        self.mainSizeLayout.setMargin(0)
        self.mainSizeLayout.setObjectName(u'mainSizeLayout')
        self.mainSizeSpinBox = QtGui.QSpinBox(self.mainAreaPage)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.mainSizeSpinBox.setSizePolicy(sizePolicy)
        self.mainSizeSpinBox.setMinimumSize(QtCore.QSize(70, 0))
        self.mainSizeSpinBox.setMaximum(999)
        self.mainSizeSpinBox.setProperty(u'value', 16)
        self.mainSizeSpinBox.setObjectName(u'mainSizeSpinBox')
        self.mainSizeLayout.addWidget(self.mainSizeSpinBox)
        self.mainLineCountLabel = QtGui.QLabel(self.mainAreaPage)
        self.mainLineCountLabel.setObjectName(u'mainLineCountLabel')
        self.mainSizeLayout.addWidget(self.mainLineCountLabel)
        self.mainAreaLayout.setLayout(2,
            QtGui.QFormLayout.FieldRole, self.mainSizeLayout)
        self.lineSpacingLabel = QtGui.QLabel(self.mainAreaPage)
        self.lineSpacingLabel.setObjectName(u'lineSpacingLabel')
        self.mainAreaLayout.setWidget(3,
            QtGui.QFormLayout.LabelRole, self.lineSpacingLabel)
        self.lineSpacingSpinBox = QtGui.QSpinBox(self.mainAreaPage)
        self.lineSpacingSpinBox.setMinimum(-50)
        self.lineSpacingSpinBox.setMaximum(50)
        self.lineSpacingSpinBox.setObjectName(u'lineSpacingSpinBox')
        self.mainAreaLayout.setWidget(3,
            QtGui.QFormLayout.FieldRole, self.lineSpacingSpinBox)
        self.outlineCheckBox = QtGui.QCheckBox(self.mainAreaPage)
        self.outlineCheckBox.setObjectName(u'outlineCheckBox')
        self.mainAreaLayout.setWidget(4,
            QtGui.QFormLayout.LabelRole, self.outlineCheckBox)
        self.outlineLayout = QtGui.QHBoxLayout()
        self.outlineLayout.setObjectName(u'outlineLayout')
        self.outlineColorPushButton = QtGui.QPushButton(self.mainAreaPage)
        self.outlineColorPushButton.setEnabled(True)
        self.outlineColorPushButton.setText(u'')
        self.outlineColorPushButton.setObjectName(u'outlineColorPushButton')
        self.outlineLayout.addWidget(self.outlineColorPushButton)
        self.outlineSizeLabel = QtGui.QLabel(self.mainAreaPage)
        self.outlineSizeLabel.setObjectName(u'outlineSizeLabel')
        self.outlineLayout.addWidget(self.outlineSizeLabel)
        self.outlineSizeSpinBox = QtGui.QSpinBox(self.mainAreaPage)
        self.outlineSizeSpinBox.setObjectName(u'outlineSizeSpinBox')
        self.outlineLayout.addWidget(self.outlineSizeSpinBox)
        self.mainAreaLayout.setLayout(4,
            QtGui.QFormLayout.FieldRole, self.outlineLayout)
        self.shadowCheckBox = QtGui.QCheckBox(self.mainAreaPage)
        self.shadowCheckBox.setObjectName(u'shadowCheckBox')
        self.mainAreaLayout.setWidget(5,
            QtGui.QFormLayout.LabelRole, self.shadowCheckBox)
        self.shadowLayout = QtGui.QHBoxLayout()
        self.shadowLayout.setObjectName(u'shadowLayout')
        self.shadowColorPushButton = QtGui.QPushButton(self.mainAreaPage)
        self.shadowColorPushButton.setEnabled(True)
        self.shadowColorPushButton.setText(u'')
        self.shadowColorPushButton.setObjectName(u'shadowColorPushButton')
        self.shadowLayout.addWidget(self.shadowColorPushButton)
        self.shadowSizeLabel = QtGui.QLabel(self.mainAreaPage)
        self.shadowSizeLabel.setObjectName(u'shadowSizeLabel')
        self.shadowLayout.addWidget(self.shadowSizeLabel)
        self.shadowSizeSpinBox = QtGui.QSpinBox(self.mainAreaPage)
        self.shadowSizeSpinBox.setObjectName(u'shadowSizeSpinBox')
        self.shadowLayout.addWidget(self.shadowSizeSpinBox)
        self.mainAreaLayout.setLayout(5,
            QtGui.QFormLayout.FieldRole, self.shadowLayout)
        ThemeWizard.addPage(self.mainAreaPage)
        self.footerAreaPage = QtGui.QWizardPage()
        self.footerAreaPage.setObjectName(u'footerAreaPage')
        self.footerLayout = QtGui.QFormLayout(self.footerAreaPage)
        self.footerLayout.setFieldGrowthPolicy(
            QtGui.QFormLayout.ExpandingFieldsGrow)
        self.footerLayout.setMargin(20)
        self.footerLayout.setSpacing(8)
        self.footerLayout.setObjectName(u'footerLayout')
        self.footerFontLabel = QtGui.QLabel(self.footerAreaPage)
        self.footerFontLabel.setMinimumSize(QtCore.QSize(103, 0))
        self.footerFontLabel.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.footerFontLabel.setObjectName(u'footerFontLabel')
        self.footerLayout.setWidget(0,
            QtGui.QFormLayout.LabelRole, self.footerFontLabel)
        self.footerFontComboBox = QtGui.QFontComboBox(self.footerAreaPage)
        self.footerFontComboBox.setObjectName(u'footerFontComboBox')
        self.footerLayout.setWidget(0,
            QtGui.QFormLayout.FieldRole, self.footerFontComboBox)
        self.footerColorLabel = QtGui.QLabel(self.footerAreaPage)
        self.footerColorLabel.setObjectName(u'footerColorLabel')
        self.footerLayout.setWidget(1,
            QtGui.QFormLayout.LabelRole, self.footerColorLabel)
        self.footerColorPushButton = QtGui.QPushButton(self.footerAreaPage)
        self.footerColorPushButton.setText(u'')
        self.footerColorPushButton.setObjectName(u'footerColorPushButton')
        self.footerLayout.setWidget(1,
            QtGui.QFormLayout.FieldRole, self.footerColorPushButton)
        self.footerSizeLabel = QtGui.QLabel(self.footerAreaPage)
        self.footerSizeLabel.setObjectName(u'footerSizeLabel')
        self.footerLayout.setWidget(2,
            QtGui.QFormLayout.LabelRole, self.footerSizeLabel)
        self.footerSizeSpinBox = QtGui.QSpinBox(self.footerAreaPage)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.footerSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.footerSizeSpinBox.setSizePolicy(sizePolicy)
        self.footerSizeSpinBox.setMinimumSize(QtCore.QSize(70, 0))
        self.footerSizeSpinBox.setMaximum(999)
        self.footerSizeSpinBox.setProperty(u'value', 10)
        self.footerSizeSpinBox.setObjectName(u'footerSizeSpinBox')
        self.footerLayout.setWidget(2,
            QtGui.QFormLayout.FieldRole, self.footerSizeSpinBox)
        ThemeWizard.addPage(self.footerAreaPage)
        self.alignmentPage = QtGui.QWizardPage()
        self.alignmentPage.setObjectName(u'alignmentPage')
        self.alignmentLayout = QtGui.QFormLayout(self.alignmentPage)
        self.alignmentLayout.setMargin(20)
        self.alignmentLayout.setSpacing(8)
        self.alignmentLayout.setObjectName(u'alignmentLayout')
        self.horizontalLabel = QtGui.QLabel(self.alignmentPage)
        self.horizontalLabel.setMinimumSize(QtCore.QSize(103, 0))
        self.horizontalLabel.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.horizontalLabel.setObjectName(u'horizontalLabel')
        self.alignmentLayout.setWidget(0,
            QtGui.QFormLayout.LabelRole, self.horizontalLabel)
        self.horizontalComboBox = QtGui.QComboBox(self.alignmentPage)
        self.horizontalComboBox.setEditable(False)
        self.horizontalComboBox.setObjectName(u'horizontalComboBox')
        self.horizontalComboBox.addItem(u'')
        self.horizontalComboBox.addItem(u'')
        self.horizontalComboBox.addItem(u'')
        self.alignmentLayout.setWidget(0,
            QtGui.QFormLayout.FieldRole, self.horizontalComboBox)
        self.verticalLabel = QtGui.QLabel(self.alignmentPage)
        self.verticalLabel.setObjectName(u'verticalLabel')
        self.alignmentLayout.setWidget(1,
            QtGui.QFormLayout.LabelRole, self.verticalLabel)
        self.verticalComboBox = QtGui.QComboBox(self.alignmentPage)
        self.verticalComboBox.setObjectName(u'verticalComboBox')
        self.verticalComboBox.addItem(u'')
        self.verticalComboBox.addItem(u'')
        self.verticalComboBox.addItem(u'')
        self.alignmentLayout.setWidget(1,
            QtGui.QFormLayout.FieldRole, self.verticalComboBox)
        self.transitionsCheckBox = QtGui.QCheckBox(self.alignmentPage)
        self.transitionsCheckBox.setObjectName(u'transitionsCheckBox')
        self.alignmentLayout.setWidget(2,
            QtGui.QFormLayout.FieldRole, self.transitionsCheckBox)
        ThemeWizard.addPage(self.alignmentPage)
        self.areaPositionPage = QtGui.QWizardPage()
        self.areaPositionPage.setObjectName(u'areaPositionPage')
        self.areaPositionLayout = QtGui.QGridLayout(self.areaPositionPage)
        self.areaPositionLayout.setMargin(20)
        self.areaPositionLayout.setSpacing(8)
        self.areaPositionLayout.setObjectName(u'areaPositionLayout')
        self.mainPositionGroupBox = QtGui.QGroupBox(self.areaPositionPage)
        self.mainPositionGroupBox.setMinimumSize(QtCore.QSize(248, 0))
        self.mainPositionGroupBox.setObjectName(u'mainPositionGroupBox')
        self.mainPositionLayout = QtGui.QFormLayout(self.mainPositionGroupBox)
        self.mainPositionLayout.setMargin(8)
        self.mainPositionLayout.setSpacing(8)
        self.mainPositionLayout.setObjectName(u'mainPositionLayout')
        self.mainDefaultPositionCheckBox = QtGui.QCheckBox(
            self.mainPositionGroupBox)
        self.mainDefaultPositionCheckBox.setChecked(True)
        self.mainDefaultPositionCheckBox.setTristate(False)
        self.mainDefaultPositionCheckBox.setObjectName(
            u'mainDefaultPositionCheckBox')
        self.mainPositionLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.mainDefaultPositionCheckBox)
        self.nainXLabel = QtGui.QLabel(self.mainPositionGroupBox)
        self.nainXLabel.setObjectName(u'nainXLabel')
        self.mainPositionLayout.setWidget(1,
            QtGui.QFormLayout.LabelRole, self.nainXLabel)
        self.mainXSpinBox = QtGui.QSpinBox(self.mainPositionGroupBox)
        self.mainXSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainXSpinBox.sizePolicy().hasHeightForWidth())
        self.mainXSpinBox.setSizePolicy(sizePolicy)
        self.mainXSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.mainXSpinBox.setMaximum(9999)
        self.mainXSpinBox.setProperty(u'value', 0)
        self.mainXSpinBox.setObjectName(u'mainXSpinBox')
        self.mainPositionLayout.setWidget(1,
            QtGui.QFormLayout.FieldRole, self.mainXSpinBox)
        self.mainYSpinBox = QtGui.QSpinBox(self.mainPositionGroupBox)
        self.mainYSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainYSpinBox.sizePolicy().hasHeightForWidth())
        self.mainYSpinBox.setSizePolicy(sizePolicy)
        self.mainYSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.mainYSpinBox.setMaximum(9999)
        self.mainYSpinBox.setObjectName(u'mainYSpinBox')
        self.mainPositionLayout.setWidget(2,
            QtGui.QFormLayout.FieldRole, self.mainYSpinBox)
        self.mainYLabel = QtGui.QLabel(self.mainPositionGroupBox)
        self.mainYLabel.setObjectName(u'mainYLabel')
        self.mainPositionLayout.setWidget(2,
            QtGui.QFormLayout.LabelRole, self.mainYLabel)
        self.mainWidthSpinBox = QtGui.QSpinBox(self.mainPositionGroupBox)
        self.mainWidthSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainWidthSpinBox.sizePolicy().hasHeightForWidth())
        self.mainWidthSpinBox.setSizePolicy(sizePolicy)
        self.mainWidthSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.mainWidthSpinBox.setMaximum(9999)
        self.mainWidthSpinBox.setObjectName(u'mainWidthSpinBox')
        self.mainPositionLayout.setWidget(3,
            QtGui.QFormLayout.FieldRole, self.mainWidthSpinBox)
        self.mainWidthLabel = QtGui.QLabel(self.mainPositionGroupBox)
        self.mainWidthLabel.setObjectName(u'mainWidthLabel')
        self.mainPositionLayout.setWidget(3,
            QtGui.QFormLayout.LabelRole, self.mainWidthLabel)
        self.mainHeightSpinBox = QtGui.QSpinBox(self.mainPositionGroupBox)
        self.mainHeightSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainHeightSpinBox.sizePolicy().hasHeightForWidth())
        self.mainHeightSpinBox.setSizePolicy(sizePolicy)
        self.mainHeightSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.mainHeightSpinBox.setMaximum(9999)
        self.mainHeightSpinBox.setObjectName(u'mainHeightSpinBox')
        self.mainPositionLayout.setWidget(4,
            QtGui.QFormLayout.FieldRole, self.mainHeightSpinBox)
        self.mainHeightLabel = QtGui.QLabel(self.mainPositionGroupBox)
        self.mainHeightLabel.setObjectName(u'mainHeightLabel')
        self.mainPositionLayout.setWidget(4,
            QtGui.QFormLayout.LabelRole, self.mainHeightLabel)
        self.areaPositionLayout.addWidget(
            self.mainPositionGroupBox, 1, 0, 1, 1)
        self.footerPositionGroupBox = QtGui.QGroupBox(self.areaPositionPage)
        self.footerPositionGroupBox.setMinimumSize(QtCore.QSize(248, 0))
        self.footerPositionGroupBox.setObjectName(u'footerPositionGroupBox')
        self.footerPositionLayout = QtGui.QFormLayout(
            self.footerPositionGroupBox)
        self.footerPositionLayout.setMargin(8)
        self.footerPositionLayout.setSpacing(8)
        self.footerPositionLayout.setObjectName(u'footerPositionLayout')
        self.footerXLabel = QtGui.QLabel(self.footerPositionGroupBox)
        self.footerXLabel.setObjectName(u'footerXLabel')
        self.footerPositionLayout.setWidget(1,
            QtGui.QFormLayout.LabelRole, self.footerXLabel)
        self.footerXSpinBox = QtGui.QSpinBox(self.footerPositionGroupBox)
        self.footerXSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.footerXSpinBox.sizePolicy().hasHeightForWidth())
        self.footerXSpinBox.setSizePolicy(sizePolicy)
        self.footerXSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.footerXSpinBox.setMaximum(9999)
        self.footerXSpinBox.setProperty(u'value', 0)
        self.footerXSpinBox.setObjectName(u'footerXSpinBox')
        self.footerPositionLayout.setWidget(1,
            QtGui.QFormLayout.FieldRole, self.footerXSpinBox)
        self.footerYLabel = QtGui.QLabel(self.footerPositionGroupBox)
        self.footerYLabel.setObjectName(u'footerYLabel')
        self.footerPositionLayout.setWidget(2,
            QtGui.QFormLayout.LabelRole, self.footerYLabel)
        self.footerYSpinBox = QtGui.QSpinBox(self.footerPositionGroupBox)
        self.footerYSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.footerYSpinBox.sizePolicy().hasHeightForWidth())
        self.footerYSpinBox.setSizePolicy(sizePolicy)
        self.footerYSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.footerYSpinBox.setMaximum(9999)
        self.footerYSpinBox.setProperty(u'value', 0)
        self.footerYSpinBox.setObjectName(u'footerYSpinBox')
        self.footerPositionLayout.setWidget(2,
            QtGui.QFormLayout.FieldRole, self.footerYSpinBox)
        self.footerWidthLabel = QtGui.QLabel(self.footerPositionGroupBox)
        self.footerWidthLabel.setObjectName(u'footerWidthLabel')
        self.footerPositionLayout.setWidget(3,
            QtGui.QFormLayout.LabelRole, self.footerWidthLabel)
        self.footerWidthSpinBox = QtGui.QSpinBox(self.footerPositionGroupBox)
        self.footerWidthSpinBox.setEnabled(False)
        self.footerWidthSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.footerWidthSpinBox.setMaximum(9999)
        self.footerWidthSpinBox.setObjectName(u'footerWidthSpinBox')
        self.footerPositionLayout.setWidget(3,
            QtGui.QFormLayout.FieldRole, self.footerWidthSpinBox)
        self.footerHeightLabel = QtGui.QLabel(self.footerPositionGroupBox)
        self.footerHeightLabel.setObjectName(u'footerHeightLabel')
        self.footerPositionLayout.setWidget(4,
            QtGui.QFormLayout.LabelRole, self.footerHeightLabel)
        self.footerHeightSpinBox = QtGui.QSpinBox(self.footerPositionGroupBox)
        self.footerHeightSpinBox.setEnabled(False)
        self.footerHeightSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.footerHeightSpinBox.setMaximum(9999)
        self.footerHeightSpinBox.setObjectName(u'footerHeightSpinBox')
        self.footerPositionLayout.setWidget(4,
            QtGui.QFormLayout.FieldRole, self.footerHeightSpinBox)
        self.footerDefaultPositionCheckBox = QtGui.QCheckBox(
            self.footerPositionGroupBox)
        self.footerDefaultPositionCheckBox.setChecked(True)
        self.footerDefaultPositionCheckBox.setObjectName(
            u'footerDefaultPositionCheckBox')
        self.footerPositionLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.footerDefaultPositionCheckBox)
        self.areaPositionLayout.addWidget(
            self.footerPositionGroupBox, 1, 1, 1, 1)
        ThemeWizard.addPage(self.areaPositionPage)
        self.previewPage = QtGui.QWizardPage()
        self.previewPage.setObjectName(u'previewPage')
        self.previewLayout = QtGui.QVBoxLayout(self.previewPage)
        self.previewLayout.setSpacing(8)
        self.previewLayout.setMargin(20)
        self.previewLayout.setObjectName(u'previewLayout')
        self.themeNameLayout = QtGui.QHBoxLayout()
        self.themeNameLayout.setSpacing(8)
        self.themeNameLayout.setObjectName(u'themeNameLayout')
        self.themeNameLabel = QtGui.QLabel(self.previewPage)
        self.themeNameLabel.setMinimumSize(QtCore.QSize(103, 0))
        self.themeNameLabel.setTextFormat(QtCore.Qt.PlainText)
        self.themeNameLabel.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.themeNameLabel.setObjectName(u'themeNameLabel')
        self.themeNameLayout.addWidget(self.themeNameLabel)
        self.themeNameEdit = QtGui.QLineEdit(self.previewPage)
        self.themeNameEdit.setObjectName(u'themeNameEdit')
        self.themeNameLayout.addWidget(self.themeNameEdit)
        self.previewLayout.addLayout(self.themeNameLayout)
        self.previewPaneLayout = QtGui.QHBoxLayout()
        self.previewPaneLayout.setSpacing(0)
        self.previewPaneLayout.setObjectName(u'previewPaneLayout')
        self.previewLeftSpacer = QtGui.QSpacerItem(58, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.previewPaneLayout.addItem(self.previewLeftSpacer)
        self.previewBoxLabel = QtGui.QLabel(self.previewPage)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.previewBoxLabel.sizePolicy().hasHeightForWidth())
        self.previewBoxLabel.setSizePolicy(sizePolicy)
        self.previewBoxLabel.setMinimumSize(QtCore.QSize(100, 150))
        self.previewBoxLabel.setFrameShape(QtGui.QFrame.WinPanel)
        self.previewBoxLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.previewBoxLabel.setLineWidth(1)
        self.previewBoxLabel.setText(u'')
        self.previewBoxLabel.setScaledContents(True)
        self.previewBoxLabel.setObjectName(u'previewBoxLabel')
        self.previewPaneLayout.addWidget(self.previewBoxLabel)
        self.previewRightSpacer = QtGui.QSpacerItem(78, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.previewPaneLayout.addItem(self.previewRightSpacer)
        self.previewLayout.addLayout(self.previewPaneLayout)
        ThemeWizard.addPage(self.previewPage)
        self.themeNameLabel.setBuddy(self.themeNameEdit)

        self.retranslateUi(ThemeWizard)
        self.backgroundStackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(
            ThemeWizard,
            QtCore.SIGNAL(u'accepted()'),
            ThemeWizard.accept)
        QtCore.QObject.connect(
            self.backgroundTypeComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.backgroundStackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(ThemeWizard)

    def retranslateUi(self, ThemeWizard):
        ThemeWizard.setWindowTitle(
            translate('OpenLP.ThemeWizard', 'Theme Wizard'))
        self.titleLabel.setText(
            u'<span style="font-size:14pt; font-weight:600;">%s</span>' % \
            translate('OpenLP.ThemeWizard', 'Welcome to the Theme Wizard'))
        self.informationLabel.setText(
            translate('OpenLP.ThemeWizard', 'This wizard will help you to '
                'create and edit your themes . Click the next button below to '
                'start the process by setting up your background.'))
        self.backgroundPage.setTitle(
            translate('OpenLP.ThemeWizard', 'Set Up Background'))
        self.backgroundPage.setSubTitle(
            translate('OpenLP.ThemeWizard', 'Set up your theme\'s background '
                'according to the parameters below.'))
        self.backgroundTypeLabel.setText(
            translate('OpenLP.ThemeWizard', 'Background type:'))
        self.backgroundTypeComboBox.setItemText(0,
            translate('OpenLP.ThemeWizard', 'Solid Color'))
        self.backgroundTypeComboBox.setItemText(1,
            translate('OpenLP.ThemeWizard', 'Gradient'))
        self.backgroundTypeComboBox.setItemText(2,
            translate('OpenLP.ThemeWizard', 'Image'))
        self.colorLabel.setText(translate('OpenLP.ThemeWizard', 'Color:'))
        self.gradientStartLabel.setText(
            translate(u'OpenLP.ThemeWizard', 'Starting color:'))
        self.gradientEndLabel.setText(
            translate(u'OpenLP.ThemeWizard', 'Ending color:'))
        self.gradientTypeLabel.setText(
            translate('OpenLP.ThemeWizard', 'Gradient:'))
        self.gradientComboBox.setItemText(0,
            translate('OpenLP.ThemeWizard', 'Horizontal'))
        self.gradientComboBox.setItemText(1,
            translate('OpenLP.ThemeWizard', 'Vertical'))
        self.gradientComboBox.setItemText(2,
            translate('OpenLP.ThemeWizard', 'Circular'))
        self.gradientComboBox.setItemText(3,
            translate('OpenLP.ThemeWizard', 'Top Left - Bottom Right'))
        self.gradientComboBox.setItemText(4,
            translate('OpenLP.ThemeWizard', 'Bottom Left - Top Right'))
        self.imageLabel.setText(translate('OpenLP.ThemeWizard', 'Image:'))
        self.mainAreaPage.setTitle(
            translate('OpenLP.ThemeWizard', 'Main Area Font Details'))
        self.mainAreaPage.setSubTitle(
            translate('OpenLP.ThemeWizard', 'Define the font and display '
                'characteristics for the Display text'))
        self.mainFontLabel.setText(
            translate('OpenLP.ThemeWizard', 'Font:'))
        self.mainColorLabel.setText(translate('OpenLP.ThemeWizard', 'Color:'))
        self.mainSizeLabel.setText(translate('OpenLP.ThemeWizard', 'Size:'))
        self.mainSizeSpinBox.setSuffix(translate('OpenLP.ThemeWizard', 'pt'))
        self.mainLineCountLabel.setText(
            translate('OpenLP.ThemeWizard', '(%d lines per slide)'))
        self.lineSpacingLabel.setText(
            translate('OpenLP.ThemeWizard', 'Line Spacing:'))
        self.lineSpacingSpinBox.setSuffix(translate('OpenLP.ThemeWizard', 'pt'))
        self.outlineCheckBox.setText(
            translate('OpenLP.ThemeWizard', '&Outline:'))
        self.outlineSizeLabel.setText(translate('OpenLP.ThemeWizard', 'Size:'))
        self.outlineSizeSpinBox.setSuffix(translate('OpenLP.ThemeWizard', 'pt'))
        self.shadowCheckBox.setText(translate('OpenLP.ThemeWizard', '&Shadow:'))
        self.shadowSizeLabel.setText(translate('OpenLP.ThemeWizard', 'Size:'))
        self.shadowSizeSpinBox.setSuffix(translate('OpenLP.ThemeWizard', 'pt'))
        self.boldCheckBox.setText(
            translate('OpenLP.ThemeWizard', 'Bold'))
        self.italicsCheckBox.setText(
            translate('OpenLP.ThemeWizard', 'Italic'))
        self.footerAreaPage.setTitle(
            translate('OpenLP.ThemeWizard', 'Footer Area Font Details'))
        self.footerAreaPage.setSubTitle(
            translate('OpenLP.ThemeWizard', 'Define the font and display '
                'characteristics for the Footer text'))
        self.footerFontLabel.setText(translate('OpenLP.ThemeWizard', 'Font:'))
        self.footerColorLabel.setText(translate('OpenLP.ThemeWizard', 'Color:'))
        self.footerSizeLabel.setText(translate('OpenLP.ThemeWizard', 'Size:'))
        self.footerSizeSpinBox.setSuffix(translate('OpenLP.ThemeWizard', 'pt'))
        self.alignmentPage.setTitle(
            translate('OpenLP.ThemeWizard', 'Text Formatting Details'))
        self.alignmentPage.setSubTitle(
            translate('OpenLP.ThemeWizard', 'Allows additional display '
                'formatting information to be defined'))
        self.horizontalLabel.setText(
            translate('OpenLP.ThemeWizard', 'Horizontal Align:'))
        self.horizontalComboBox.setItemText(0,
            translate('OpenLP.ThemeWizard', 'Left'))
        self.horizontalComboBox.setItemText(1,
            translate('OpenLP.ThemeWizard', 'Right'))
        self.horizontalComboBox.setItemText(2,
            translate('OpenLP.ThemeWizard', 'Center'))
        self.verticalLabel.setText(
            translate('OpenLP.ThemeWizard', 'Vertical Align:'))
        self.verticalComboBox.setItemText(0,
            translate('OpenLP.ThemeWizard', 'Top'))
        self.verticalComboBox.setItemText(1,
            translate('OpenLP.ThemeWizard', 'Middle'))
        self.verticalComboBox.setItemText(2,
            translate('OpenLP.ThemeWizard', 'Bottom'))
        self.transitionsCheckBox.setText(
            translate('OpenLP.ThemeWizard', 'Transitions'))
        self.areaPositionPage.setTitle(
            translate('OpenLP.ThemeWizard', 'Output Area Locations'))
        self.areaPositionPage.setSubTitle(
            translate('OpenLP.ThemeWizard', 'Allows you to change and move the'
                ' main and footer areas.'))
        self.mainPositionGroupBox.setTitle(
            translate('OpenLP.ThemeWizard', '&Main Area'))
        self.mainDefaultPositionCheckBox.setText(
            translate('OpenLP.ThemeWizard', '&Use default location'))
        self.nainXLabel.setText(translate('OpenLP.ThemeWizard', 'X position:'))
        self.mainXSpinBox.setSuffix(translate('OpenLP.ThemeWizard', 'px'))
        self.mainYSpinBox.setSuffix(translate('OpenLP.ThemeWizard', 'px'))
        self.mainYLabel.setText(translate('OpenLP.ThemeWizard', 'Y position:'))
        self.mainWidthSpinBox.setSuffix(translate('OpenLP.ThemeWizard', 'px'))
        self.mainWidthLabel.setText(translate('OpenLP.ThemeWizard', 'Width:'))
        self.mainHeightSpinBox.setSuffix(translate('OpenLP.ThemeWizard', 'px'))
        self.mainHeightLabel.setText(
            translate('OpenLP.ThemeWizard', 'Height:'))
        self.footerPositionGroupBox.setTitle(
            translate('OpenLP.ThemeWizard', 'Footer Area'))
        self.footerXLabel.setText(
            translate('OpenLP.ThemeWizard', 'X position:'))
        self.footerXSpinBox.setSuffix(translate('OpenLP.ThemeWizard', 'px'))
        self.footerYLabel.setText(
            translate('OpenLP.ThemeWizard', 'Y position:'))
        self.footerYSpinBox.setSuffix(translate('OpenLP.ThemeWizard', 'px'))
        self.footerWidthLabel.setText(
            translate('OpenLP.ThemeWizard', 'Width:'))
        self.footerWidthSpinBox.setSuffix(
            translate('OpenLP.ThemeWizard', 'px'))
        self.footerHeightLabel.setText(
            translate('OpenLP.ThemeWizard', 'Height:'))
        self.footerHeightSpinBox.setSuffix(
            translate('OpenLP.ThemeWizard', 'px'))
        self.footerDefaultPositionCheckBox.setText(
            translate('OpenLP.ThemeWizard', 'Use default location'))
        self.previewPage.setTitle(
            translate('OpenLP.ThemeWizard', 'Save and Preview'))
        self.previewPage.setSubTitle(
            translate('OpenLP.ThemeWizard', 'View the theme and save it '
                'replacing the current one or change the name to create a '
                'new theme'))
        self.themeNameLabel.setText(
            translate('OpenLP.ThemeWizard', 'Theme name:'))
