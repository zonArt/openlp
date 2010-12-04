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
        ThemeWizard.setObjectName(u'ThemeWizard')
        ThemeWizard.resize(550, 386)
        ThemeWizard.setModal(True)
        ThemeWizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        ThemeWizard.setOptions(QtGui.QWizard.IndependentPages|
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
        self.importBibleImage.setPixmap(QtGui.QPixmap
            (u':/wizards/wizard_importbible.bmp'))
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
        ThemeWizard.addPage(self.welcomePage)
        self.backgroundPage = QtGui.QWizardPage()
        self.backgroundPage.setObjectName(u'backgroundPage')
        self.backgroundLayout = QtGui.QFormLayout(self.backgroundPage)
        self.backgroundLayout.setFieldGrowthPolicy(
            QtGui.QFormLayout.ExpandingFieldsGrow)
        self.backgroundLayout.setLabelAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.backgroundLayout.setMargin(20)
        self.backgroundLayout.setSpacing(8)
        self.backgroundLayout.setObjectName(u'backgroundLayout')
        self.backgroundTypeLabel = QtGui.QLabel(self.backgroundPage)
        self.backgroundTypeLabel.setObjectName(u'backgroundTypeLabel')
        self.backgroundLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.backgroundTypeLabel)
        self.backgroundTypeComboBox = QtGui.QComboBox(self.backgroundPage)
        self.backgroundTypeComboBox.setObjectName(u'backgroundTypeComboBox')
        self.backgroundTypeComboBox.addItem(u'')
        self.backgroundTypeComboBox.addItem(u'')
        self.backgroundTypeComboBox.addItem(u'')
        self.backgroundLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.backgroundTypeComboBox)
        self.color1Label = QtGui.QLabel(self.backgroundPage)
        self.color1Label.setObjectName(u'color1Label')
        self.backgroundLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.color1Label)
        self.color1PushButton = QtGui.QPushButton(self.backgroundPage)
        self.color1PushButton.setText(u'')
        self.color1PushButton.setObjectName(u'color1PushButton')
        self.backgroundLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.color1PushButton)
        self.color2Label = QtGui.QLabel(self.backgroundPage)
        self.color2Label.setObjectName(u'color2Label')
        self.backgroundLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.color2Label)
        self.color2PushButton = QtGui.QPushButton(self.backgroundPage)
        self.color2PushButton.setText(u'')
        self.color2PushButton.setObjectName(u'color2PushButton')
        self.backgroundLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.color2PushButton)
        self.imageLabel = QtGui.QLabel(self.backgroundPage)
        self.imageLabel.setObjectName(u'imageLabel')
        self.backgroundLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.imageLabel)
        self.imageLayout = QtGui.QHBoxLayout()
        self.imageLayout.setSpacing(8)
        self.imageLayout.setObjectName(u'imageLayout')
        self.imageLineEdit = QtGui.QLineEdit(self.backgroundPage)
        self.imageLineEdit.setObjectName(u'imageLineEdit')
        self.imageLayout.addWidget(self.imageLineEdit)
        self.imageBrowseButton = QtGui.QToolButton(self.backgroundPage)
        self.imageBrowseButton.setText(u'')
        self.imageBrowseButton.setIcon(build_icon
            (u':/general/general_open.png'))
        self.imageBrowseButton.setObjectName(u'imageBrowseButton')
        self.imageLayout.addWidget(self.imageBrowseButton)
        self.backgroundLayout.setLayout(3, QtGui.QFormLayout.FieldRole,
            self.imageLayout)
        self.gradientLabel = QtGui.QLabel(self.backgroundPage)
        self.gradientLabel.setObjectName(u'gradientLabel')
        self.backgroundLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.gradientLabel)
        self.gradientComboBox = QtGui.QComboBox(self.backgroundPage)
        self.gradientComboBox.setObjectName(u'gradientComboBox')
        self.gradientComboBox.addItem(u'')
        self.gradientComboBox.addItem(u'')
        self.gradientComboBox.addItem(u'')
        self.gradientComboBox.addItem(u'')
        self.gradientComboBox.addItem(u'')
        self.backgroundLayout.setWidget(4, QtGui.QFormLayout.FieldRole,
            self.gradientComboBox)
        ThemeWizard.addPage(self.backgroundPage)
        self.mainAreaPage = QtGui.QWizardPage()
        self.mainAreaPage.setObjectName(u'mainAreaPage')
        self.formLayout = QtGui.QFormLayout(self.mainAreaPage)
        self.formLayout.setFormAlignment(
            QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout.setContentsMargins(-1, 20, 20, 20)
        self.formLayout.setSpacing(8)
        self.formLayout.setObjectName(u'formLayout')
        self.mainFontLabel = QtGui.QLabel(self.mainAreaPage)
        self.mainFontLabel.setObjectName(u'mainFontLabel')
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.mainFontLabel)
        self.mainFontComboBox = QtGui.QFontComboBox(self.mainAreaPage)
        self.mainFontComboBox.setObjectName(u'mainFontComboBox')
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.mainFontComboBox)
        self.mainColorLabel = QtGui.QLabel(self.mainAreaPage)
        self.mainColorLabel.setObjectName(u'mainColorLabel')
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.mainColorLabel)
        self.mainColorPushButton = QtGui.QPushButton(self.mainAreaPage)
        self.mainColorPushButton.setText(u'')
        self.mainColorPushButton.setObjectName(u'mainColorPushButton')
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.mainColorPushButton)
        self.mainSizeLabel = QtGui.QLabel(self.mainAreaPage)
        self.mainSizeLabel.setObjectName(u'mainSizeLabel')
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.mainSizeLabel)
        self.mainSizeLayout = QtGui.QHBoxLayout()
        self.mainSizeLayout.setSpacing(8)
        self.mainSizeLayout.setMargin(0)
        self.mainSizeLayout.setObjectName(u'mainSizeLayout')
        self.mainSizeSpinBox = QtGui.QSpinBox(self.mainAreaPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
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
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole,
            self.mainSizeLayout)
        self.lineSpacingLabel = QtGui.QLabel(self.mainAreaPage)
        self.lineSpacingLabel.setObjectName(u'lineSpacingLabel')
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.lineSpacingLabel)
        self.lineSpacingSpinBox = QtGui.QSpinBox(self.mainAreaPage)
        self.lineSpacingSpinBox.setMinimum(-50)
        self.lineSpacingSpinBox.setMaximum(50)
        self.lineSpacingSpinBox.setObjectName(u'lineSpacingSpinBox')
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.lineSpacingSpinBox)
        self.outlineCheckBox = QtGui.QCheckBox(self.mainAreaPage)
        self.outlineCheckBox.setObjectName(u'outlineCheckBox')
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.outlineCheckBox)
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
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole,
            self.outlineLayout)
        self.shadowCheckBox = QtGui.QCheckBox(self.mainAreaPage)
        self.shadowCheckBox.setObjectName(u'shadowCheckBox')
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole,
            self.shadowCheckBox)
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
        self.formLayout.setLayout(5, QtGui.QFormLayout.FieldRole,
            self.shadowLayout)
        self.boldCheckBox = QtGui.QCheckBox(self.mainAreaPage)
        self.boldCheckBox.setObjectName(u'boldCheckBox')
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole,
            self.boldCheckBox)
        self.italicsCheckBox = QtGui.QCheckBox(self.mainAreaPage)
        self.italicsCheckBox.setObjectName(u'italicsCheckBox')
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole,
            self.italicsCheckBox)
        ThemeWizard.addPage(self.mainAreaPage)
        self.footerAreaPage = QtGui.QWizardPage()
        self.footerAreaPage.setObjectName(u'footerAreaPage')
        self.footerLayout = QtGui.QFormLayout(self.footerAreaPage)
        self.footerLayout.setFieldGrowthPolicy(
            QtGui.QFormLayout.ExpandingFieldsGrow)
        self.footerLayout.setContentsMargins(50, 20, 20, 20)
        self.footerLayout.setSpacing(8)
        self.footerLayout.setObjectName(u'footerLayout')
        self.footerFontLabel = QtGui.QLabel(self.footerAreaPage)
        self.footerFontLabel.setObjectName(u'footerFontLabel')
        self.footerLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.footerFontLabel)
        self.footerFontComboBox = QtGui.QFontComboBox(self.footerAreaPage)
        self.footerFontComboBox.setObjectName(u'footerFontComboBox')
        self.footerLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.footerFontComboBox)
        self.footerColorLabel = QtGui.QLabel(self.footerAreaPage)
        self.footerColorLabel.setObjectName(u'footerColorLabel')
        self.footerLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.footerColorLabel)
        self.footerColorPushButton = QtGui.QPushButton(self.footerAreaPage)
        self.footerColorPushButton.setText(u'')
        self.footerColorPushButton.setObjectName(u'footerColorPushButton')
        self.footerLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.footerColorPushButton)
        self.footerSizeLabel = QtGui.QLabel(self.footerAreaPage)
        self.footerSizeLabel.setObjectName(u'footerSizeLabel')
        self.footerLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.footerSizeLabel)
        self.footerSizeSpinBox = QtGui.QSpinBox(self.footerAreaPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.footerSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.footerSizeSpinBox.setSizePolicy(sizePolicy)
        self.footerSizeSpinBox.setMinimumSize(QtCore.QSize(70, 0))
        self.footerSizeSpinBox.setMaximum(999)
        self.footerSizeSpinBox.setProperty(u'value', 10)
        self.footerSizeSpinBox.setObjectName(u'footerSizeSpinBox')
        self.footerLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.footerSizeSpinBox)
        ThemeWizard.addPage(self.footerAreaPage)
        self.alignmentPage = QtGui.QWizardPage()
        self.alignmentPage.setObjectName(u'alignmentPage')
        self.formLayout_2 = QtGui.QFormLayout(self.alignmentPage)
        self.formLayout_2.setMargin(20)
        self.formLayout_2.setObjectName(u'formLayout_2')
        self.horizontalLabel = QtGui.QLabel(self.alignmentPage)
        self.horizontalLabel.setObjectName(u'horizontalLabel')
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.horizontalLabel)
        self.horizontalComboBox = QtGui.QComboBox(self.alignmentPage)
        self.horizontalComboBox.setEditable(False)
        self.horizontalComboBox.setObjectName(u'horizontalComboBox')
        self.horizontalComboBox.addItem(u'')
        self.horizontalComboBox.addItem(u'')
        self.horizontalComboBox.addItem(u'')
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.horizontalComboBox)
        self.verticalLabel = QtGui.QLabel(self.alignmentPage)
        self.verticalLabel.setObjectName(u'verticalLabel')
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.verticalLabel)
        self.verticalComboBox = QtGui.QComboBox(self.alignmentPage)
        self.verticalComboBox.setObjectName(u'verticalComboBox')
        self.verticalComboBox.addItem(u'')
        self.verticalComboBox.addItem(u'')
        self.verticalComboBox.addItem(u'')
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.verticalComboBox)
        self.transitionsCheckBox = QtGui.QCheckBox(self.alignmentPage)
        self.transitionsCheckBox.setObjectName(u'transitionsCheckBox')
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.transitionsCheckBox)
        ThemeWizard.addPage(self.alignmentPage)
        self.areaPositionPage = QtGui.QWizardPage()
        self.areaPositionPage.setObjectName(u'areaPositionPage')
        self.gridLayout_2 = QtGui.QGridLayout(self.areaPositionPage)
        self.gridLayout_2.setMargin(20)
        self.gridLayout_2.setSpacing(8)
        self.gridLayout_2.setObjectName(u'gridLayout_2')
        self.mainPositionGroupBox = QtGui.QGroupBox(self.areaPositionPage)
        self.mainPositionGroupBox.setMinimumSize(QtCore.QSize(248, 0))
        self.mainPositionGroupBox.setObjectName(u'mainPositionGroupBox')
        self.mainPositionLayout = QtGui.QFormLayout(self.mainPositionGroupBox)
        self.mainPositionLayout.setMargin(8)
        self.mainPositionLayout.setSpacing(8)
        self.mainPositionLayout.setObjectName(u'mainPositionLayout')
        self.mainDefaultPositionCheckBox = \
            QtGui.QCheckBox(self.mainPositionGroupBox)
        self.mainDefaultPositionCheckBox.setChecked(True)
        self.mainDefaultPositionCheckBox.setTristate(False)
        self.mainDefaultPositionCheckBox.setObjectName(
            u'mainDefaultPositionCheckBox')
        self.mainPositionLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.mainDefaultPositionCheckBox)
        self.nainXLabel = QtGui.QLabel(self.mainPositionGroupBox)
        self.nainXLabel.setObjectName(u'nainXLabel')
        self.mainPositionLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.nainXLabel)
        self.mainXSpinBox = QtGui.QSpinBox(self.mainPositionGroupBox)
        self.mainXSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainXSpinBox.sizePolicy().hasHeightForWidth())
        self.mainXSpinBox.setSizePolicy(sizePolicy)
        self.mainXSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.mainXSpinBox.setMaximum(9999)
        self.mainXSpinBox.setProperty(u'value', 0)
        self.mainXSpinBox.setObjectName(u'mainXSpinBox')
        self.mainPositionLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.mainXSpinBox)
        self.mainYSpinBox = QtGui.QSpinBox(self.mainPositionGroupBox)
        self.mainYSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainYSpinBox.sizePolicy().hasHeightForWidth())
        self.mainYSpinBox.setSizePolicy(sizePolicy)
        self.mainYSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.mainYSpinBox.setMaximum(9999)
        self.mainYSpinBox.setObjectName(u'mainYSpinBox')
        self.mainPositionLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.mainYSpinBox)
        self.mainYLabel = QtGui.QLabel(self.mainPositionGroupBox)
        self.mainYLabel.setObjectName(u'mainYLabel')
        self.mainPositionLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.mainYLabel)
        self.mainWidthSpinBox = QtGui.QSpinBox(self.mainPositionGroupBox)
        self.mainWidthSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainWidthSpinBox.sizePolicy().hasHeightForWidth())
        self.mainWidthSpinBox.setSizePolicy(sizePolicy)
        self.mainWidthSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.mainWidthSpinBox.setMaximum(9999)
        self.mainWidthSpinBox.setObjectName(u'mainWidthSpinBox')
        self.mainPositionLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.mainWidthSpinBox)
        self.mainWidthLabel = QtGui.QLabel(self.mainPositionGroupBox)
        self.mainWidthLabel.setObjectName(u'mainWidthLabel')
        self.mainPositionLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.mainWidthLabel)
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
        self.mainPositionLayout.setWidget(4, QtGui.QFormLayout.FieldRole,
            self.mainHeightSpinBox)
        self.mainHeightLabel = QtGui.QLabel(self.mainPositionGroupBox)
        self.mainHeightLabel.setObjectName(u'mainHeightLabel')
        self.mainPositionLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.mainHeightLabel)
        self.gridLayout_2.addWidget(self.mainPositionGroupBox, 1, 0, 1, 1)
        self.footerPositionGroupBox = QtGui.QGroupBox(self.areaPositionPage)
        self.footerPositionGroupBox.setMinimumSize(QtCore.QSize(248, 0))
        self.footerPositionGroupBox.setObjectName(u'footerPositionGroupBox')
        self.footerPositionLayout = \
            QtGui.QFormLayout(self.footerPositionGroupBox)
        self.footerPositionLayout.setMargin(8)
        self.footerPositionLayout.setSpacing(8)
        self.footerPositionLayout.setObjectName(u'footerPositionLayout')
        self.footerXLabel = QtGui.QLabel(self.footerPositionGroupBox)
        self.footerXLabel.setObjectName(u'footerXLabel')
        self.footerPositionLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.footerXLabel)
        self.footerXSpinBox = QtGui.QSpinBox(self.footerPositionGroupBox)
        self.footerXSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.footerXSpinBox.sizePolicy().hasHeightForWidth())
        self.footerXSpinBox.setSizePolicy(sizePolicy)
        self.footerXSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.footerXSpinBox.setMaximum(9999)
        self.footerXSpinBox.setProperty(u'value', 0)
        self.footerXSpinBox.setObjectName(u'footerXSpinBox')
        self.footerPositionLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.footerXSpinBox)
        self.footerYLabel = QtGui.QLabel(self.footerPositionGroupBox)
        self.footerYLabel.setObjectName(u'footerYLabel')
        self.footerPositionLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.footerYLabel)
        self.footerYSpinBox = QtGui.QSpinBox(self.footerPositionGroupBox)
        self.footerYSpinBox.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.footerYSpinBox.sizePolicy().hasHeightForWidth())
        self.footerYSpinBox.setSizePolicy(sizePolicy)
        self.footerYSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.footerYSpinBox.setMaximum(9999)
        self.footerYSpinBox.setProperty(u'value', 0)
        self.footerYSpinBox.setObjectName(u'footerYSpinBox')
        self.footerPositionLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.footerYSpinBox)
        self.footerWidthLabel = QtGui.QLabel(self.footerPositionGroupBox)
        self.footerWidthLabel.setObjectName(u'footerWidthLabel')
        self.footerPositionLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.footerWidthLabel)
        self.footerWidthSpinBox = QtGui.QSpinBox(self.footerPositionGroupBox)
        self.footerWidthSpinBox.setEnabled(False)
        self.footerWidthSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.footerWidthSpinBox.setMaximum(9999)
        self.footerWidthSpinBox.setObjectName(u'footerWidthSpinBox')
        self.footerPositionLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.footerWidthSpinBox)
        self.footerHeightLabel = QtGui.QLabel(self.footerPositionGroupBox)
        self.footerHeightLabel.setObjectName(u'footerHeightLabel')
        self.footerPositionLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.footerHeightLabel)
        self.footerHeightSpinBox = QtGui.QSpinBox(self.footerPositionGroupBox)
        self.footerHeightSpinBox.setEnabled(False)
        self.footerHeightSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.footerHeightSpinBox.setMaximum(9999)
        self.footerHeightSpinBox.setObjectName(u'footerHeightSpinBox')
        self.footerPositionLayout.setWidget(4, QtGui.QFormLayout.FieldRole,
            self.footerHeightSpinBox)
        self.footerDefaultPositionCheckBox = \
            QtGui.QCheckBox(self.footerPositionGroupBox)
        self.footerDefaultPositionCheckBox.setChecked(True)
        self.footerDefaultPositionCheckBox.setObjectName(
            u'footerDefaultPositionCheckBox')
        self.footerPositionLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.footerDefaultPositionCheckBox)
        self.gridLayout_2.addWidget(self.footerPositionGroupBox, 1, 1, 1, 1)
        ThemeWizard.addPage(self.areaPositionPage)
        self.previewPage = QtGui.QWizardPage()
        self.previewPage.setObjectName(u'previewPage')
        self.themeNameLabel = QtGui.QLabel(self.previewPage)
        self.themeNameLabel.setGeometry(QtCore.QRect(20, 10, 82, 16))
        self.themeNameLabel.setTextFormat(QtCore.Qt.PlainText)
        self.themeNameLabel.setObjectName(u'themeNameLabel')
        self.previewLabel = QtGui.QLabel(self.previewPage)
        self.previewLabel.setGeometry(QtCore.QRect(250, 60, 48, 16))
        self.previewLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.previewLabel.setObjectName(u'previewLabel')
        self.themeNameEdit = QtGui.QLineEdit(self.previewPage)
        self.themeNameEdit.setGeometry(QtCore.QRect(117, 4, 351, 23))
        self.themeNameEdit.setObjectName(u'themeNameEdit')
        self.groupBox = QtGui.QGroupBox(self.previewPage)
        self.groupBox.setGeometry(QtCore.QRect(40, 80, 464, 214))
        self.groupBox.setTitle(u'')
        self.groupBox.setObjectName(u'groupBox')
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        spacerItem2 = QtGui.QSpacerItem(58, 20, QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.previewBoxLabel = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.previewBoxLabel.sizePolicy().hasHeightForWidth())
        self.previewBoxLabel.setSizePolicy(sizePolicy)
        self.previewBoxLabel.setMinimumSize(QtCore.QSize(300, 200))
        self.previewBoxLabel.setFrameShape(QtGui.QFrame.WinPanel)
        self.previewBoxLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.previewBoxLabel.setLineWidth(1)
        self.previewBoxLabel.setText(u'')
        self.previewBoxLabel.setScaledContents(True)
        self.previewBoxLabel.setObjectName(u'previewBoxLabel')
        self.horizontalLayout.addWidget(self.previewBoxLabel)
        spacerItem3 = QtGui.QSpacerItem(78, 20, QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        ThemeWizard.addPage(self.previewPage)
        self.themeNameLabel.setBuddy(self.themeNameEdit)

        self.retranslateUi(ThemeWizard)
        QtCore.QObject.connect(ThemeWizard, QtCore.SIGNAL(u'accepted()'),
            ThemeWizard.accept)
        QtCore.QMetaObject.connectSlotsByName(ThemeWizard)

    def retranslateUi(self, ThemeWizard):
        ThemeWizard.setWindowTitle(translate('OpenLP.ThemeForm',
            'Theme Wizard'))
        self.titleLabel.setText(translate('OpenLP.ThemeForm',
            '<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" '
            '\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n'
            '<html><head><meta name=\"qrichtext\" content=\"1\" '
            '/><style type=\"text/css\">\n'
            'p, li { white-space: pre-wrap; }\n'
            '</style></head><body style=\" font-family:\'Sans Serif\'; '
            'font-size:9pt; font-weight:400; font-style:normal;\">\n'
            '<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; '
            'margin-right:0px; -qt-block-indent:0; text-indent:0px;'
            '\"><span style=\" font-size:14pt; font-weight:600;\">'
            'Welcome to the Theme Wizard</span></p></body></html>'))
        self.informationLabel.setText(translate('OpenLP.ThemeForm',
            'This wizard will help you to maintain Themes . Click the next '
            'button below to start the process by setting up your background.'))
        self.backgroundPage.setTitle(translate('OpenLP.ThemeForm',
            'Set Up Background'))
        self.backgroundPage.setSubTitle(translate('OpenLP.ThemeForm',
            'Set up your theme\'s background according to the parameters '
            'below.'))
        self.backgroundTypeLabel.setText(translate('OpenLP.ThemeForm',
            'Background type:'))
        self.backgroundTypeComboBox.setItemText(0, translate('OpenLP.ThemeForm',
            'Solid Color'))
        self.backgroundTypeComboBox.setItemText(1, translate('OpenLP.ThemeForm',
            'Gradient'))
        self.backgroundTypeComboBox.setItemText(2, translate('OpenLP.ThemeForm',
            'Image'))
        self.color1Label.setText(translate('OpenLP.ThemeForm', '<Color1>'))
        self.color2Label.setText(translate('OpenLP.ThemeForm', '<Color2>'))
        self.imageLabel.setText(translate('OpenLP.ThemeForm', 'Image:'))
        self.gradientLabel.setText(translate('OpenLP.ThemeForm', 'Gradient:'))
        self.gradientComboBox.setItemText(0, translate('OpenLP.ThemeForm',
            'Horizontal'))
        self.gradientComboBox.setItemText(1, translate('OpenLP.ThemeForm',
            'Vertical'))
        self.gradientComboBox.setItemText(2, translate('OpenLP.ThemeForm',
            'Circular'))
        self.gradientComboBox.setItemText(3, translate('OpenLP.ThemeForm',
            'Top Left - Bottom Right'))
        self.gradientComboBox.setItemText(4, translate('OpenLP.ThemeForm',
            'Bottom Left - Top Right'))
        self.mainAreaPage.setTitle(translate('OpenLP.ThemeForm',
            'Main Area Font Details'))
        self.mainAreaPage.setSubTitle(translate('OpenLP.ThemeForm',
            'Define the font and display characteristics for the Display text'))
        self.mainFontLabel.setText(translate('OpenLP.ThemeForm', 'Font:'))
        self.mainColorLabel.setText(translate('OpenLP.ThemeForm', 'Color:'))
        self.mainSizeLabel.setText(translate('OpenLP.ThemeForm', 'Size:'))
        self.mainSizeSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'pt'))
        self.mainLineCountLabel.setText(translate('OpenLP.ThemeForm',
            '(%d lines per slide)'))
        self.lineSpacingLabel.setText(translate('OpenLP.ThemeForm',
            'Line Spacing:'))
        self.lineSpacingSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'pt'))
        self.outlineCheckBox.setText(translate('OpenLP.ThemeForm', '&Outline:'))
        self.outlineSizeLabel.setText(translate('OpenLP.ThemeForm', 'Size:'))
        self.outlineSizeSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'pt'))
        self.shadowCheckBox.setText(translate('OpenLP.ThemeForm', '&Shadow:'))
        self.shadowSizeLabel.setText(translate('OpenLP.ThemeForm', 'Size:'))
        self.shadowSizeSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'pt'))
        self.boldCheckBox.setText(translate('OpenLP.ThemeForm', 'Bold Display'))
        self.italicsCheckBox.setText(translate('OpenLP.ThemeForm',
            'Italic Display'))
        self.footerAreaPage.setTitle(translate('OpenLP.ThemeForm',
            'Footer Area Font Details'))
        self.footerAreaPage.setSubTitle(translate('OpenLP.ThemeForm',
            'Define the font and display characteristics for the Footer text'))
        self.footerFontLabel.setText(translate('OpenLP.ThemeForm', 'Font:'))
        self.footerColorLabel.setText(translate('OpenLP.ThemeForm', 'Color:'))
        self.footerSizeLabel.setText(translate('OpenLP.ThemeForm', 'Size:'))
        self.footerSizeSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'pt'))
        self.alignmentPage.setTitle(translate('OpenLP.ThemeForm',
            'Text Formatting Details'))
        self.alignmentPage.setSubTitle(translate('OpenLP.ThemeForm',
            'Allows additional display formatting information to be defined'))
        self.horizontalLabel.setText(translate('OpenLP.ThemeForm',
            'Horizontal Align:'))
        self.horizontalComboBox.setItemText(0, translate('OpenLP.ThemeForm',
            'Left'))
        self.horizontalComboBox.setItemText(1, translate('OpenLP.ThemeForm',
            'Right'))
        self.horizontalComboBox.setItemText(2, translate('OpenLP.ThemeForm',
            'Center'))
        self.verticalLabel.setText(translate('OpenLP.ThemeForm',
            'Vertcal Align:'))
        self.verticalComboBox.setItemText(0, translate('OpenLP.ThemeForm',
            'Top'))
        self.verticalComboBox.setItemText(1, translate('OpenLP.ThemeForm',
            'Middle'))
        self.verticalComboBox.setItemText(2, translate('OpenLP.ThemeForm',
            'Bottom'))
        self.transitionsCheckBox.setText(translate('OpenLP.ThemeForm',
            'Transitions'))
        self.areaPositionPage.setTitle(translate('OpenLP.ThemeForm',
            'Output Area Locations'))
        self.areaPositionPage.setSubTitle(translate('OpenLP.ThemeForm',
            'Allows you to change and move the Main and Footer areas.'))
        self.mainPositionGroupBox.setTitle(translate('OpenLP.ThemeForm',
            '&Main Area'))
        self.mainDefaultPositionCheckBox.setText(translate('OpenLP.ThemeForm',
            '&Use default location'))
        self.nainXLabel.setText(translate('OpenLP.ThemeForm', 'X position:'))
        self.mainXSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'px'))
        self.mainYSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'px'))
        self.mainYLabel.setText(translate('OpenLP.ThemeForm', 'Y position:'))
        self.mainWidthSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'px'))
        self.mainWidthLabel.setText(translate('OpenLP.ThemeForm', 'Width:'))
        self.mainHeightSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'px'))
        self.mainHeightLabel.setText(translate('OpenLP.ThemeForm', 'Height:'))
        self.footerPositionGroupBox.setTitle(translate('OpenLP.ThemeForm',
            'Footer Area'))
        self.footerXLabel.setText(translate('OpenLP.ThemeForm', 'X position:'))
        self.footerXSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'px'))
        self.footerYLabel.setText(translate('OpenLP.ThemeForm', 'Y position:'))
        self.footerYSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'px'))
        self.footerWidthLabel.setText(translate('OpenLP.ThemeForm', 'Width:'))
        self.footerWidthSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'px'))
        self.footerHeightLabel.setText(translate('OpenLP.ThemeForm', 'Height:'))
        self.footerHeightSpinBox.setSuffix(translate('OpenLP.ThemeForm', 'px'))
        self.footerDefaultPositionCheckBox.setText(translate('OpenLP.ThemeForm',
            'Use default location'))
        self.previewPage.setTitle(translate('OpenLP.ThemeForm',
            'Save and Preview'))
        self.previewPage.setSubTitle(translate('OpenLP.ThemeForm',
            'View the theme and save it replacing the current one or change '
            'the name to create a new theme'))
        self.themeNameLabel.setText(translate('OpenLP.ThemeForm',
            'Theme name:'))
        self.previewLabel.setText(translate('OpenLP.ThemeForm', 'Preview'))
