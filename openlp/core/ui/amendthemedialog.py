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

class Ui_AmendThemeDialog(object):
    def setupUi(self, amendThemeDialog):
        amendThemeDialog.setObjectName(u'amendThemeDialog')
        amendThemeDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        amendThemeDialog.resize(586, 651)
        icon = build_icon(u':/icon/openlp-logo-16x16.png')
        amendThemeDialog.setWindowIcon(icon)
        amendThemeDialog.setModal(True)
        self.amendThemeLayout = QtGui.QVBoxLayout(amendThemeDialog)
        self.amendThemeLayout.setSpacing(8)
        self.amendThemeLayout.setMargin(8)
        self.amendThemeLayout.setObjectName(u'amendThemeLayout')
        self.themeNameWidget = QtGui.QWidget(amendThemeDialog)
        self.themeNameWidget.setObjectName(u'themeNameWidget')
        self.themeNameLayout = QtGui.QHBoxLayout(self.themeNameWidget)
        self.themeNameLayout.setSpacing(8)
        self.themeNameLayout.setMargin(0)
        self.themeNameLayout.setObjectName(u'themeNameLayout')
        self.themeNameLabel = QtGui.QLabel(self.themeNameWidget)
        self.themeNameLabel.setObjectName(u'themeNameLabel')
        self.themeNameLayout.addWidget(self.themeNameLabel)
        self.themeNameEdit = QtGui.QLineEdit(self.themeNameWidget)
        self.themeNameEdit.setObjectName(u'themeNameEdit')
        self.themeNameLabel.setBuddy(self.themeNameEdit)
        self.themeNameLayout.addWidget(self.themeNameEdit)
        self.amendThemeLayout.addWidget(self.themeNameWidget)
        self.contentWidget = QtGui.QWidget(amendThemeDialog)
        self.contentWidget.setObjectName(u'contentWidget')
        self.contentLayout = QtGui.QHBoxLayout(self.contentWidget)
        self.contentLayout.setSpacing(8)
        self.contentLayout.setMargin(0)
        self.contentLayout.setObjectName(u'contentLayout')
        self.themeTabWidget = QtGui.QTabWidget(self.contentWidget)
        self.themeTabWidget.setObjectName(u'themeTabWidget')
        self.backgroundTab = QtGui.QWidget()
        self.backgroundTab.setObjectName(u'backgroundTab')
        self.backgroundLayout = QtGui.QFormLayout(self.backgroundTab)
        self.backgroundLayout.setMargin(8)
        self.backgroundLayout.setSpacing(8)
        self.backgroundLayout.setObjectName(u'backgroundLayout')
#        self.backgroundLabel = QtGui.QLabel(self.backgroundTab)
#        self.backgroundLabel.setObjectName(u'backgroundLabel')
#        self.backgroundLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
#            self.backgroundLabel)
#        self.backgroundComboBox = QtGui.QComboBox(self.backgroundTab)
#        self.backgroundComboBox.setObjectName(u'backgroundComboBox')
#        self.backgroundLabel.setBuddy(self.backgroundComboBox)
#        self.backgroundComboBox.addItem(QtCore.QString())
#        self.backgroundComboBox.addItem(QtCore.QString())
#        self.backgroundLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
#            self.backgroundComboBox)
        self.backgroundTypeLabel = QtGui.QLabel(self.backgroundTab)
        self.backgroundTypeLabel.setObjectName(u'backgroundTypeLabel')
        self.backgroundLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.backgroundTypeLabel)
        self.backgroundTypeComboBox = QtGui.QComboBox(self.backgroundTab)
        self.backgroundTypeComboBox.setObjectName(u'backgroundTypeComboBox')
        self.backgroundTypeComboBox.addItem(QtCore.QString())
        self.backgroundTypeComboBox.addItem(QtCore.QString())
        self.backgroundTypeComboBox.addItem(QtCore.QString())
        self.backgroundLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.backgroundTypeComboBox)
        self.color1Label = QtGui.QLabel(self.backgroundTab)
        self.color1Label.setObjectName(u'color1Label')
        self.backgroundLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.color1Label)
        self.color1PushButton = QtGui.QPushButton(self.backgroundTab)
        self.color1PushButton.setObjectName(u'color1PushButton')
        self.backgroundLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.color1PushButton)
        self.color2Label = QtGui.QLabel(self.backgroundTab)
        self.color2Label.setObjectName(u'color2Label')
        self.backgroundLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.color2Label)
        self.color2PushButton = QtGui.QPushButton(self.backgroundTab)
        self.color2PushButton.setObjectName(u'color2PushButton')
        self.backgroundLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.color2PushButton)
        self.imageLabel = QtGui.QLabel(self.backgroundTab)
        self.imageLabel.setObjectName(u'imageLabel')
        self.backgroundLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.imageLabel)
        self.gradientLabel = QtGui.QLabel(self.backgroundTab)
        self.gradientLabel.setObjectName(u'gradientLabel')
        self.backgroundLayout.setWidget(6, QtGui.QFormLayout.LabelRole,
            self.gradientLabel)
        self.gradientComboBox = QtGui.QComboBox(self.backgroundTab)
        self.gradientComboBox.setObjectName(u'gradientComboBox')
        self.gradientComboBox.addItem(QtCore.QString())
        self.gradientComboBox.addItem(QtCore.QString())
        self.gradientComboBox.addItem(QtCore.QString())
        self.backgroundLayout.setWidget(6, QtGui.QFormLayout.FieldRole,
            self.gradientComboBox)
        self.imageFilenameWidget = QtGui.QWidget(self.backgroundTab)
        self.imageFilenameWidget.setObjectName(u'imageFilenameWidget')
        self.horizontalLayout2 = QtGui.QHBoxLayout(self.imageFilenameWidget)
        self.horizontalLayout2.setSpacing(0)
        self.horizontalLayout2.setMargin(0)
        self.horizontalLayout2.setObjectName(u'horizontalLayout2')
        self.imageLineEdit = QtGui.QLineEdit(self.imageFilenameWidget)
        self.imageLineEdit.setObjectName(u'imageLineEdit')
        self.horizontalLayout2.addWidget(self.imageLineEdit)
        self.imageToolButton = QtGui.QToolButton(self.imageFilenameWidget)
        self.imageToolButton.setIcon(build_icon(u':/general/general_open.png'))
        self.imageToolButton.setObjectName(u'imageToolButton')
        self.imageToolButton.setAutoRaise(True)
        self.horizontalLayout2.addWidget(self.imageToolButton)
        self.backgroundLayout.setWidget(4, QtGui.QFormLayout.FieldRole,
            self.imageFilenameWidget)
        self.themeTabWidget.addTab(self.backgroundTab, u'')
        self.fontMainTab = QtGui.QWidget()
        self.fontMainTab.setObjectName(u'fontMainTab')
        self.fontMainLayout = QtGui.QHBoxLayout(self.fontMainTab)
        self.fontMainLayout.setSpacing(8)
        self.fontMainLayout.setMargin(8)
        self.fontMainLayout.setObjectName(u'fontMainLayout')
        self.mainLeftWidget = QtGui.QWidget(self.fontMainTab)
        self.mainLeftWidget.setObjectName(u'mainLeftWidget')
        self.mainLeftLayout = QtGui.QVBoxLayout(self.mainLeftWidget)
        self.mainLeftLayout.setSpacing(8)
        self.mainLeftLayout.setMargin(0)
        self.mainLeftLayout.setObjectName(u'mainLeftLayout')
        self.fontMainGroupBox = QtGui.QGroupBox(self.mainLeftWidget)
        self.fontMainGroupBox.setObjectName(u'fontMainGroupBox')
        self.mainFontLayout = QtGui.QFormLayout(self.fontMainGroupBox)
        self.mainFontLayout.setFormAlignment(QtCore.Qt.AlignLeading |
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.mainFontLayout.setMargin(8)
        self.mainFontLayout.setSpacing(8)
        self.mainFontLayout.setObjectName(u'mainFontLayout')
        self.fontMainlabel = QtGui.QLabel(self.fontMainGroupBox)
        self.fontMainlabel.setObjectName(u'fontMainlabel')
        self.mainFontLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.fontMainlabel)
        self.fontMainComboBox = QtGui.QFontComboBox(self.fontMainGroupBox)
        self.fontMainComboBox.setObjectName(u'fontMainComboBox')
        self.mainFontLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.fontMainComboBox)
        self.fontMainColorLabel = QtGui.QLabel(self.fontMainGroupBox)
        self.fontMainColorLabel.setObjectName(u'fontMainColorLabel')
        self.mainFontLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.fontMainColorLabel)
        self.fontMainColorPushButton = QtGui.QPushButton(self.fontMainGroupBox)
        self.fontMainColorPushButton.setObjectName(u'fontMainColorPushButton')
        self.mainFontLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.fontMainColorPushButton)
        self.fontMainSize = QtGui.QLabel(self.fontMainGroupBox)
        self.fontMainSize.setObjectName(u'fontMainSize')
        self.mainFontLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.fontMainSize)
        self.fontMainSizeSpinBox = QtGui.QSpinBox(self.fontMainGroupBox)
        defaultSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        defaultSizePolicy.setHeightForWidth(
            self.fontMainSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.fontMainSizeSpinBox.setSizePolicy(defaultSizePolicy)
        self.fontMainSizeSpinBox.setMinimumSize(QtCore.QSize(70, 0))
        self.fontMainSizeSpinBox.setProperty(u'value', QtCore.QVariant(16))
        self.fontMainSizeSpinBox.setMaximum(999)
        self.fontMainSizeSpinBox.setObjectName(u'fontMainSizeSpinBox')
        self.mainFontLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.fontMainSizeSpinBox)
        self.fontMainWeightComboBox = QtGui.QComboBox(self.fontMainGroupBox)
        self.fontMainWeightComboBox.setObjectName(u'fontMainWeightComboBox')
        self.fontMainWeightComboBox.addItem(QtCore.QString())
        self.fontMainWeightComboBox.addItem(QtCore.QString())
        self.fontMainWeightComboBox.addItem(QtCore.QString())
        self.fontMainWeightComboBox.addItem(QtCore.QString())
        self.mainFontLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.fontMainWeightComboBox)
        self.fontMainWeightLabel = QtGui.QLabel(self.fontMainGroupBox)
        self.fontMainWeightLabel.setObjectName(u'fontMainWeightLabel')
        self.mainFontLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.fontMainWeightLabel)
        self.mainLeftLayout.addWidget(self.fontMainGroupBox)
        self.fontMainWrapLineAdjustmentLabel = QtGui.QLabel(
            self.fontMainGroupBox)
        self.fontMainWrapLineAdjustmentLabel.setObjectName(
            u'fontMainWrapLineAdjustmentLabel')
        self.mainFontLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.fontMainWrapLineAdjustmentLabel)
        self.fontMainLineAdjustmentSpinBox = QtGui.QSpinBox(
            self.fontMainGroupBox)
        self.fontMainLineAdjustmentSpinBox.setObjectName(
            u'fontMainLineAdjustmentSpinBox')
        self.fontMainLineAdjustmentSpinBox.setMinimum(-99)
        self.mainFontLayout.setWidget(4, QtGui.QFormLayout.FieldRole,
            self.fontMainLineAdjustmentSpinBox)
        self.fontMainWrapIndentationLabel = QtGui.QLabel(self.fontMainGroupBox)
        self.fontMainWrapIndentationLabel.setObjectName(
            u'fontMainWrapIndentationLabel')
        self.mainFontLayout.setWidget(5, QtGui.QFormLayout.LabelRole,
            self.fontMainWrapIndentationLabel)
        self.fontMainLineSpacingSpinBox = QtGui.QSpinBox(self.fontMainGroupBox)
        self.fontMainLineSpacingSpinBox.setObjectName(
            u'fontMainLineSpacingSpinBox')
        self.fontMainLineSpacingSpinBox.setMaximum(10)
        self.mainFontLayout.setWidget(5, QtGui.QFormLayout.FieldRole,
            self.fontMainLineSpacingSpinBox)
        self.fontMainLinesPageLabel = QtGui.QLabel(self.fontMainGroupBox)
        self.fontMainLinesPageLabel.setObjectName(u'fontMainLinesPageLabel')
        self.mainFontLayout.addRow(self.fontMainLinesPageLabel)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.mainLeftLayout.addItem(spacerItem1)
        self.fontMainLayout.addWidget(self.mainLeftWidget)
        self.mainRightWidget = QtGui.QWidget(self.fontMainTab)
        self.mainRightWidget.setObjectName(u'mainRightWidget')
        self.mainRightLayout = QtGui.QVBoxLayout(self.mainRightWidget)
        self.mainRightLayout.setSpacing(8)
        self.mainRightLayout.setMargin(0)
        self.mainRightLayout.setObjectName(u'mainRightLayout')
        self.mainLocationGroupBox = QtGui.QGroupBox(self.mainRightWidget)
        self.mainLocationGroupBox.setObjectName(u'mainLocationGroupBox')
        self.mainLocationLayout = QtGui.QFormLayout(self.mainLocationGroupBox)
        self.mainLocationLayout.setMargin(8)
        self.mainLocationLayout.setSpacing(8)
        self.mainLocationLayout.setObjectName(u'mainLocationLayout')
        self.defaultLocationLabel = QtGui.QLabel(self.mainLocationGroupBox)
        self.defaultLocationLabel.setObjectName(u'defaultLocationLabel')
        self.mainLocationLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.defaultLocationLabel)
        self.fontMainDefaultCheckBox = QtGui.QCheckBox(
            self.mainLocationGroupBox)
        self.fontMainDefaultCheckBox.setTristate(False)
        self.fontMainDefaultCheckBox.setObjectName(u'fontMainDefaultCheckBox')
        self.mainLocationLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.fontMainDefaultCheckBox)
        self.fontMainXLabel = QtGui.QLabel(self.mainLocationGroupBox)
        self.fontMainXLabel.setObjectName(u'fontMainXLabel')
        self.mainLocationLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.fontMainXLabel)
        self.fontMainYLabel = QtGui.QLabel(self.mainLocationGroupBox)
        self.fontMainYLabel.setObjectName(u'fontMainYLabel')
        self.mainLocationLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.fontMainYLabel)
        self.fontMainWidthLabel = QtGui.QLabel(self.mainLocationGroupBox)
        self.fontMainWidthLabel.setObjectName(u'fontMainWidthLabel')
        self.mainLocationLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.fontMainWidthLabel)
        self.fontMainHeightLabel = QtGui.QLabel(self.mainLocationGroupBox)
        self.fontMainHeightLabel.setObjectName(u'fontMainHeightLabel')
        self.mainLocationLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.fontMainHeightLabel)
        self.fontMainXSpinBox = QtGui.QSpinBox(self.mainLocationGroupBox)
        defaultSizePolicy.setHeightForWidth(
            self.fontMainXSpinBox.sizePolicy().hasHeightForWidth())
        self.fontMainXSpinBox.setSizePolicy(defaultSizePolicy)
        self.fontMainXSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.fontMainXSpinBox.setProperty(u'value', QtCore.QVariant(0))
        self.fontMainXSpinBox.setMaximum(9999)
        self.fontMainXSpinBox.setObjectName(u'fontMainXSpinBox')
        self.mainLocationLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.fontMainXSpinBox)
        self.fontMainYSpinBox = QtGui.QSpinBox(self.mainLocationGroupBox)
        defaultSizePolicy.setHeightForWidth(
            self.fontMainYSpinBox.sizePolicy().hasHeightForWidth())
        self.fontMainYSpinBox.setSizePolicy(defaultSizePolicy)
        self.fontMainYSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.fontMainYSpinBox.setMaximum(9999)
        self.fontMainYSpinBox.setObjectName(u'fontMainYSpinBox')
        self.mainLocationLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.fontMainYSpinBox)
        self.fontMainWidthSpinBox = QtGui.QSpinBox(self.mainLocationGroupBox)
        defaultSizePolicy.setHeightForWidth(
            self.fontMainWidthSpinBox.sizePolicy().hasHeightForWidth())
        self.fontMainWidthSpinBox.setSizePolicy(defaultSizePolicy)
        self.fontMainWidthSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.fontMainWidthSpinBox.setMaximum(9999)
        self.fontMainWidthSpinBox.setObjectName(u'fontMainWidthSpinBox')
        self.mainLocationLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.fontMainWidthSpinBox)
        self.fontMainHeightSpinBox = QtGui.QSpinBox(self.mainLocationGroupBox)
        defaultSizePolicy.setHeightForWidth(
            self.fontMainHeightSpinBox.sizePolicy().hasHeightForWidth())
        self.fontMainHeightSpinBox.setSizePolicy(defaultSizePolicy)
        self.fontMainHeightSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.fontMainHeightSpinBox.setMaximum(9999)
        self.fontMainHeightSpinBox.setObjectName(u'fontMainHeightSpinBox')
        self.mainLocationLayout.setWidget(4, QtGui.QFormLayout.FieldRole,
            self.fontMainHeightSpinBox)
        self.mainRightLayout.addWidget(self.mainLocationGroupBox)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.mainRightLayout.addItem(spacerItem2)
        self.fontMainLayout.addWidget(self.mainRightWidget)
        self.themeTabWidget.addTab(self.fontMainTab, u'')
        self.fontFooterTab = QtGui.QWidget()
        self.fontFooterTab.setObjectName(u'fontFooterTab')
        self.fontFooterLayout = QtGui.QHBoxLayout(self.fontFooterTab)
        self.fontFooterLayout.setSpacing(8)
        self.fontFooterLayout.setMargin(8)
        self.fontFooterLayout.setObjectName(u'fontFooterLayout')
        self.footerLeftWidget = QtGui.QWidget(self.fontFooterTab)
        self.footerLeftWidget.setObjectName(u'footerLeftWidget')
        self.footerLeftLayout = QtGui.QVBoxLayout(self.footerLeftWidget)
        self.footerLeftLayout.setSpacing(8)
        self.footerLeftLayout.setMargin(0)
        self.footerLeftLayout.setObjectName(u'footerLeftLayout')
        self.footerFontGroupBox = QtGui.QGroupBox(self.footerLeftWidget)
        self.footerFontGroupBox.setObjectName(u'footerFontGroupBox')
        self.footerFontLayout = QtGui.QFormLayout(self.footerFontGroupBox)
        self.footerFontLayout.setFieldGrowthPolicy(
            QtGui.QFormLayout.ExpandingFieldsGrow)
        self.footerFontLayout.setFormAlignment(QtCore.Qt.AlignLeading |
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.footerFontLayout.setMargin(8)
        self.footerFontLayout.setSpacing(8)
        self.footerFontLayout.setObjectName(u'footerFontLayout')
        self.fontFooterLabel = QtGui.QLabel(self.footerFontGroupBox)
        self.fontFooterLabel.setObjectName(u'fontFooterLabel')
        self.footerFontLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.fontFooterLabel)
        self.fontFooterComboBox = QtGui.QFontComboBox(self.footerFontGroupBox)
        self.fontFooterComboBox.setObjectName(u'fontFooterComboBox')
        self.footerFontLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.fontFooterComboBox)
        self.fontFooterColorLabel = QtGui.QLabel(self.footerFontGroupBox)
        self.fontFooterColorLabel.setObjectName(u'fontFooterColorLabel')
        self.footerFontLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.fontFooterColorLabel)
        self.fontFooterColorPushButton = QtGui.QPushButton(
            self.footerFontGroupBox)
        self.fontFooterColorPushButton.setObjectName(
            u'fontFooterColorPushButton')
        self.footerFontLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.fontFooterColorPushButton)
        self.fontFooterSizeLabel = QtGui.QLabel(self.footerFontGroupBox)
        self.fontFooterSizeLabel.setObjectName(u'fontFooterSizeLabel')
        self.footerFontLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.fontFooterSizeLabel)
        self.fontFooterSizeSpinBox = QtGui.QSpinBox(self.footerFontGroupBox)
        defaultSizePolicy.setHeightForWidth(
            self.fontFooterSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.fontFooterSizeSpinBox.setSizePolicy(defaultSizePolicy)
        self.fontFooterSizeSpinBox.setMinimumSize(QtCore.QSize(70, 0))
        self.fontFooterSizeSpinBox.setProperty(u'value', QtCore.QVariant(10))
        self.fontFooterSizeSpinBox.setMaximum(999)
        self.fontFooterSizeSpinBox.setObjectName(u'fontFooterSizeSpinBox')
        self.footerFontLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.fontFooterSizeSpinBox)
        self.fontFooterWeightComboBox = QtGui.QComboBox(self.footerFontGroupBox)
        self.fontFooterWeightComboBox.setObjectName(u'fontFooterWeightComboBox')
        self.fontFooterWeightComboBox.addItem(QtCore.QString())
        self.fontFooterWeightComboBox.addItem(QtCore.QString())
        self.fontFooterWeightComboBox.addItem(QtCore.QString())
        self.fontFooterWeightComboBox.addItem(QtCore.QString())
        self.footerFontLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.fontFooterWeightComboBox)
        self.fontFooterWeightLabel = QtGui.QLabel(self.footerFontGroupBox)
        self.fontFooterWeightLabel.setObjectName(u'fontFooterWeightLabel')
        self.footerFontLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.fontFooterWeightLabel)
        self.footerLeftLayout.addWidget(self.footerFontGroupBox)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.footerLeftLayout.addItem(spacerItem3)
        self.fontFooterLayout.addWidget(self.footerLeftWidget)
        self.footerRightWidget = QtGui.QWidget(self.fontFooterTab)
        self.footerRightWidget.setObjectName(u'footerRightWidget')
        self.footerRightLayout = QtGui.QVBoxLayout(self.footerRightWidget)
        self.footerRightLayout.setSpacing(8)
        self.footerRightLayout.setMargin(0)
        self.footerRightLayout.setObjectName(u'footerRightLayout')
        self.locationFooterGroupBox = QtGui.QGroupBox(self.footerRightWidget)
        self.locationFooterGroupBox.setObjectName(u'locationFooterGroupBox')
        self.locationFooterLayout = QtGui.QFormLayout(
            self.locationFooterGroupBox)
        self.locationFooterLayout.setFieldGrowthPolicy(
            QtGui.QFormLayout.ExpandingFieldsGrow)
        self.locationFooterLayout.setFormAlignment(QtCore.Qt.AlignLeading |
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.locationFooterLayout.setMargin(8)
        self.locationFooterLayout.setSpacing(8)
        self.locationFooterLayout.setObjectName(u'locationFooterLayout')
        self.fontFooterDefaultLabel = QtGui.QLabel(self.locationFooterGroupBox)
        self.fontFooterDefaultLabel.setObjectName(u'fontFooterDefaultLabel')
        self.locationFooterLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.fontFooterDefaultLabel)
        self.fontFooterDefaultCheckBox = QtGui.QCheckBox(
            self.locationFooterGroupBox)
        self.fontFooterDefaultCheckBox.setTristate(False)
        self.fontFooterDefaultCheckBox.setObjectName(
            u'fontFooterDefaultCheckBox')
        self.locationFooterLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.fontFooterDefaultCheckBox)
        self.fontFooterXLabel = QtGui.QLabel(self.locationFooterGroupBox)
        self.fontFooterXLabel.setObjectName(u'fontFooterXLabel')
        self.locationFooterLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.fontFooterXLabel)
        self.fontFooterYLabel = QtGui.QLabel(self.locationFooterGroupBox)
        self.fontFooterYLabel.setObjectName(u'fontFooterYLabel')
        self.locationFooterLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.fontFooterYLabel)
        self.fontFooterWidthLabel = QtGui.QLabel(self.locationFooterGroupBox)
        self.fontFooterWidthLabel.setObjectName(u'fontFooterWidthLabel')
        self.locationFooterLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.fontFooterWidthLabel)
        self.fontFooterHeightLabel = QtGui.QLabel(self.locationFooterGroupBox)
        self.fontFooterHeightLabel.setObjectName(u'fontFooterHeightLabel')
        self.locationFooterLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.fontFooterHeightLabel)
        self.fontFooterXSpinBox = QtGui.QSpinBox(self.locationFooterGroupBox)
        defaultSizePolicy.setHeightForWidth(
            self.fontFooterXSpinBox.sizePolicy().hasHeightForWidth())
        self.fontFooterXSpinBox.setSizePolicy(defaultSizePolicy)
        self.fontFooterXSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.fontFooterXSpinBox.setProperty(u'value', QtCore.QVariant(0))
        self.fontFooterXSpinBox.setMaximum(9999)
        self.fontFooterXSpinBox.setObjectName(u'fontFooterXSpinBox')
        self.locationFooterLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.fontFooterXSpinBox)
        self.fontFooterYSpinBox = QtGui.QSpinBox(self.locationFooterGroupBox)
        defaultSizePolicy.setHeightForWidth(
            self.fontFooterXSpinBox.sizePolicy().hasHeightForWidth())
        self.fontFooterYSpinBox.setSizePolicy(defaultSizePolicy)
        self.fontFooterYSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.fontFooterYSpinBox.setProperty(u'value', QtCore.QVariant(0))
        self.fontFooterYSpinBox.setMaximum(9999)
        self.fontFooterYSpinBox.setObjectName(u'fontFooterYSpinBox')
        self.locationFooterLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.fontFooterYSpinBox)
        self.fontFooterWidthSpinBox = QtGui.QSpinBox(
            self.locationFooterGroupBox)
        self.fontFooterWidthSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.fontFooterWidthSpinBox.setMaximum(9999)
        self.fontFooterWidthSpinBox.setObjectName(u'fontFooterWidthSpinBox')
        self.locationFooterLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.fontFooterWidthSpinBox)
        self.fontFooterHeightSpinBox = QtGui.QSpinBox(
            self.locationFooterGroupBox)
        self.fontFooterHeightSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.fontFooterHeightSpinBox.setMaximum(9999)
        self.fontFooterHeightSpinBox.setObjectName(u'fontFooterHeightSpinBox')
        self.locationFooterLayout.setWidget(4, QtGui.QFormLayout.FieldRole,
            self.fontFooterHeightSpinBox)
        self.footerRightLayout.addWidget(self.locationFooterGroupBox)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.footerRightLayout.addItem(spacerItem4)
        self.fontFooterLayout.addWidget(self.footerRightWidget)
        self.themeTabWidget.addTab(self.fontFooterTab, u'')
        self.otherOptionsTab = QtGui.QWidget()
        self.otherOptionsTab.setObjectName(u'otherOptionsTab')
        self.otherOptionsLayout = QtGui.QHBoxLayout(self.otherOptionsTab)
        self.otherOptionsLayout.setSpacing(8)
        self.otherOptionsLayout.setMargin(8)
        self.otherOptionsLayout.setObjectName(u'otherOptionsLayout')
        self.optionsLeftWidget = QtGui.QWidget(self.otherOptionsTab)
        self.optionsLeftWidget.setObjectName(u'optionsLeftWidget')
        self.optionsLeftLayout = QtGui.QVBoxLayout(self.optionsLeftWidget)
        self.optionsLeftLayout.setSpacing(8)
        self.optionsLeftLayout.setMargin(0)
        self.optionsLeftLayout.setObjectName(u'optionsLeftLayout')
        self.outlineGroupBox = QtGui.QGroupBox(self.optionsLeftWidget)
        self.outlineGroupBox.setObjectName(u'outlineGroupBox')
        self.verticalLayout = QtGui.QVBoxLayout(self.outlineGroupBox)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setMargin(8)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.outlineWidget = QtGui.QWidget(self.outlineGroupBox)
        self.outlineWidget.setObjectName(u'outlineWidget')
        self.outlineLayout = QtGui.QFormLayout(self.outlineWidget)
        self.outlineLayout.setMargin(0)
        self.outlineLayout.setSpacing(8)
        self.outlineLayout.setObjectName(u'outlineLayout')
        self.outlineCheckBox = QtGui.QCheckBox(self.outlineWidget)
        self.outlineCheckBox.setObjectName(u'outlineCheckBox')
        self.outlineLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.outlineCheckBox)
        self.outlineSpinBox = QtGui.QSpinBox(self.outlineWidget)
        self.outlineSpinBox.setObjectName(u'outlineSpinBox')
        self.outlineSpinBox.setMaximum(10)
        self.outlineLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.outlineSpinBox)
        self.outlineSpinBoxLabel = QtGui.QLabel(self.outlineWidget)
        self.outlineSpinBoxLabel.setObjectName(u'outlineSpinBoxLabel')
        self.outlineLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.outlineSpinBoxLabel)
        self.outlineColorLabel = QtGui.QLabel(self.outlineWidget)
        self.outlineColorLabel.setObjectName(u'outlineColorLabel')
        self.outlineLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.outlineColorLabel)
        self.outlineColorPushButton = QtGui.QPushButton(self.outlineWidget)
        self.outlineColorPushButton.setObjectName(u'outlineColorPushButton')
        self.outlineLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.outlineColorPushButton)
        self.outlineEnabledLabel = QtGui.QLabel(self.outlineWidget)
        self.outlineEnabledLabel.setObjectName(u'outlineEnabledLabel')
        self.outlineLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.outlineEnabledLabel)
        self.verticalLayout.addWidget(self.outlineWidget)
        self.optionsLeftLayout.addWidget(self.outlineGroupBox)
        self.shadowGroupBox = QtGui.QGroupBox(self.optionsLeftWidget)
        self.shadowGroupBox.setObjectName(u'shadowGroupBox')
        self.verticalLayout = QtGui.QVBoxLayout(self.shadowGroupBox)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setMargin(8)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.shadowWidget = QtGui.QWidget(self.shadowGroupBox)
        self.shadowWidget.setObjectName(u'shadowWidget')
        self.shadowLayout = QtGui.QFormLayout(self.shadowWidget)
        self.shadowLayout.setMargin(0)
        self.shadowLayout.setSpacing(8)
        self.shadowLayout.setObjectName(u'shadowLayout')
        self.shadowCheckBox = QtGui.QCheckBox(self.shadowWidget)
        self.shadowCheckBox.setObjectName(u'shadowCheckBox')
        self.shadowLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.shadowCheckBox)
        self.shadowSpinBox = QtGui.QSpinBox(self.outlineWidget)
        self.shadowSpinBox.setObjectName(u'shadowSpinBox')
        self.shadowSpinBox.setMaximum(10)
        self.shadowLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.shadowSpinBox)
        self.shadowSpinBoxLabel = QtGui.QLabel(self.outlineWidget)
        self.shadowSpinBoxLabel.setObjectName(u'shadowSpinBoxLabel')
        self.shadowLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.shadowSpinBoxLabel)
        self.shadowColorLabel = QtGui.QLabel(self.shadowWidget)
        self.shadowColorLabel.setObjectName(u'shadowColorLabel')
        self.shadowLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.shadowColorLabel)
        self.shadowColorPushButton = QtGui.QPushButton(self.shadowWidget)
        self.shadowColorPushButton.setObjectName(u'shadowColorPushButton')
        self.shadowLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.shadowColorPushButton)
        self.shadowEnabledLabel = QtGui.QLabel(self.shadowWidget)
        self.shadowEnabledLabel.setObjectName(u'shadowEnabledLabel')
        self.shadowLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.shadowEnabledLabel)
        self.verticalLayout.addWidget(self.shadowWidget)
        self.optionsLeftLayout.addWidget(self.shadowGroupBox)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.optionsLeftLayout.addItem(spacerItem5)
        self.otherOptionsLayout.addWidget(self.optionsLeftWidget)
        self.optionsRightWidget = QtGui.QWidget(self.otherOptionsTab)
        self.optionsRightWidget.setObjectName(u'optionsRightWidget')
        self.optionsRightLayout = QtGui.QVBoxLayout(self.optionsRightWidget)
        self.optionsRightLayout.setSpacing(8)
        self.optionsRightLayout.setMargin(0)
        self.optionsRightLayout.setObjectName(u'optionsRightLayout')
        self.alignmentGroupBox = QtGui.QGroupBox(self.optionsRightWidget)
        self.alignmentGroupBox.setObjectName(u'alignmentGroupBox')
        self.gridLayout4 = QtGui.QGridLayout(self.alignmentGroupBox)
        self.gridLayout4.setObjectName(u'gridLayout4')
        self.horizontalLabel = QtGui.QLabel(self.alignmentGroupBox)
        self.horizontalLabel.setObjectName(u'horizontalLabel')
        self.gridLayout4.addWidget(self.horizontalLabel, 0, 0, 1, 1)
        self.horizontalComboBox = QtGui.QComboBox(self.alignmentGroupBox)
        self.horizontalComboBox.setObjectName(u'horizontalComboBox')
        self.horizontalComboBox.addItem(QtCore.QString())
        self.horizontalComboBox.addItem(QtCore.QString())
        self.horizontalComboBox.addItem(QtCore.QString())
        self.gridLayout4.addWidget(self.horizontalComboBox, 0, 1, 1, 1)
        self.verticalLabel = QtGui.QLabel(self.alignmentGroupBox)
        self.verticalLabel.setObjectName(u'verticalLabel')
        self.gridLayout4.addWidget(self.verticalLabel, 1, 0, 1, 1)
        self.verticalComboBox = QtGui.QComboBox(self.alignmentGroupBox)
        self.verticalComboBox.setObjectName(u'verticalComboBox')
        self.verticalComboBox.addItem(QtCore.QString())
        self.verticalComboBox.addItem(QtCore.QString())
        self.verticalComboBox.addItem(QtCore.QString())
        self.gridLayout4.addWidget(self.verticalComboBox, 1, 1, 1, 1)
        self.optionsRightLayout.addWidget(self.alignmentGroupBox)
        self.transitionGroupBox = QtGui.QGroupBox(self.optionsRightWidget)
        self.transitionGroupBox.setObjectName(u'transitionGroupBox')
        self.gridLayout5 = QtGui.QGridLayout(self.transitionGroupBox)
        self.gridLayout5.setObjectName(u'gridLayout5')
        self.slideTransitionCheckBoxLabel = QtGui.QLabel(
            self.transitionGroupBox)
        self.slideTransitionCheckBoxLabel.setObjectName(
            u'slideTransitionCheckBoxLabel')
        self.gridLayout5.addWidget(
            self.slideTransitionCheckBoxLabel, 0, 0, 1, 1)
        self.slideTransitionCheckBox = QtGui.QCheckBox(self.alignmentGroupBox)
        self.slideTransitionCheckBox.setTristate(False)
        self.gridLayout5.addWidget(self.slideTransitionCheckBox, 0, 1, 1, 1)
        self.optionsRightLayout.addWidget(self.transitionGroupBox)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.optionsRightLayout.addItem(spacerItem6)
        self.otherOptionsLayout.addWidget(self.optionsRightWidget)
        self.themeTabWidget.addTab(self.otherOptionsTab, u'')
        self.contentLayout.addWidget(self.themeTabWidget)
        self.amendThemeLayout.addWidget(self.contentWidget)
        self.previewGroupBox = QtGui.QGroupBox(amendThemeDialog)
        self.previewGroupBox.setObjectName(u'previewGroupBox')
        self.themePreviewLayout = QtGui.QHBoxLayout(self.previewGroupBox)
        self.themePreviewLayout.setSpacing(8)
        self.themePreviewLayout.setMargin(8)
        self.themePreviewLayout.setObjectName(u'themePreviewLayout')
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        self.themePreviewLayout.addItem(spacerItem7)
        self.themePreview = QtGui.QLabel(self.previewGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.themePreview.sizePolicy().hasHeightForWidth())
        self.themePreview.setSizePolicy(sizePolicy)
        self.themePreview.setMaximumSize(QtCore.QSize(300, 225))
        self.themePreview.setFrameShape(QtGui.QFrame.WinPanel)
        self.themePreview.setFrameShadow(QtGui.QFrame.Sunken)
        self.themePreview.setLineWidth(1)
        self.themePreview.setScaledContents(True)
        self.themePreview.setObjectName(u'themePreview')
        self.themePreviewLayout.addWidget(self.themePreview)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        self.themePreviewLayout.addItem(spacerItem8)
        self.amendThemeLayout.addWidget(self.previewGroupBox)
        self.themeButtonBox = QtGui.QDialogButtonBox(amendThemeDialog)
        self.themeButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Ok)
        self.themeButtonBox.setObjectName(u'themeButtonBox')
        self.amendThemeLayout.addWidget(self.themeButtonBox)

        self.retranslateUi(amendThemeDialog)
        self.themeTabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.themeButtonBox,
            QtCore.SIGNAL(u'accepted()'), amendThemeDialog.accept)
        QtCore.QObject.connect(self.themeButtonBox,
            QtCore.SIGNAL(u'rejected()'), amendThemeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(amendThemeDialog)

    def retranslateUi(self, amendThemeDialog):
        amendThemeDialog.setWindowTitle(
            translate('OpenLP.AmendThemeForm', 'Theme Maintenance'))
        self.themeNameLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Theme &name:'))
#        self.backgroundLabel.setText(
#            translate('OpenLP.AmendThemeForm', '&Visibility:'))
#        self.backgroundComboBox.setItemText(0,
#            translate('OpenLP.AmendThemeForm', 'Opaque'))
#        self.backgroundComboBox.setItemText(1,
#            translate('OpenLP.AmendThemeForm', 'Transparent'))
        self.backgroundTypeLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Type:'))
        self.backgroundTypeComboBox.setItemText(0,
            translate('OpenLP.AmendThemeForm', 'Solid Color'))
        self.backgroundTypeComboBox.setItemText(1,
            translate('OpenLP.AmendThemeForm', 'Gradient'))
        self.backgroundTypeComboBox.setItemText(2,
            translate('OpenLP.AmendThemeForm', 'Image'))
        self.color1Label.setText(u'<color1>:')
        self.color2Label.setText(u'<color2>:')
        self.imageLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Image:'))
        self.gradientLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Gradient:'))
        self.gradientComboBox.setItemText(0,
            translate('OpenLP.AmendThemeForm', 'Horizontal'))
        self.gradientComboBox.setItemText(1,
            translate('OpenLP.AmendThemeForm', 'Vertical'))
        self.gradientComboBox.setItemText(2,
            translate('OpenLP.AmendThemeForm', 'Circular'))
        self.themeTabWidget.setTabText(
            self.themeTabWidget.indexOf(self.backgroundTab),
            translate('OpenLP.AmendThemeForm', '&Background'))
        self.fontMainGroupBox.setTitle(
            translate('OpenLP.AmendThemeForm', 'Main Font'))
        self.fontMainlabel.setText(
            translate('OpenLP.AmendThemeForm', 'Font:'))
        self.fontMainColorLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Color:'))
        self.fontMainSize.setText(
            translate('OpenLP.AmendThemeForm', 'Size:'))
        self.fontMainSizeSpinBox.setSuffix(
            translate('OpenLP.AmendThemeForm', 'pt'))
        self.fontMainWrapIndentationLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Wrap indentation:'))
        self.fontMainWrapLineAdjustmentLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Adjust line spacing:'))
        self.fontMainWeightComboBox.setItemText(0,
            translate('OpenLP.AmendThemeForm', 'Normal'))
        self.fontMainWeightComboBox.setItemText(1,
            translate('OpenLP.AmendThemeForm', 'Bold'))
        self.fontMainWeightComboBox.setItemText(2,
            translate('OpenLP.AmendThemeForm', 'Italics'))
        self.fontMainWeightComboBox.setItemText(3,
            translate('OpenLP.AmendThemeForm', 'Bold/Italics'))
        self.fontMainWeightLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Style:'))
        self.mainLocationGroupBox.setTitle(
            translate('OpenLP.AmendThemeForm', 'Display Location'))
        self.defaultLocationLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Use default location'))
        self.fontMainXLabel.setText(
            translate('OpenLP.AmendThemeForm', 'X position:'))
        self.fontMainYLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Y position:'))
        self.fontMainWidthLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Width:'))
        self.fontMainHeightLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Height:'))
        self.fontMainXSpinBox.setSuffix(
            translate('OpenLP.AmendThemeForm', 'px'))
        self.fontMainYSpinBox.setSuffix(
            translate('OpenLP.AmendThemeForm', 'px'))
        self.fontMainWidthSpinBox.setSuffix(
            translate('OpenLP.AmendThemeForm', 'px'))
        self.fontMainHeightSpinBox.setSuffix(
            translate('OpenLP.AmendThemeForm', 'px'))
        self.themeTabWidget.setTabText(
            self.themeTabWidget.indexOf(self.fontMainTab),
            translate('OpenLP.AmendThemeForm', '&Main Font'))
        self.footerFontGroupBox.setTitle(
            translate('OpenLP.AmendThemeForm', 'Footer Font'))
        self.fontFooterLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Font:'))
        self.fontFooterColorLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Color:'))
        self.fontFooterSizeLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Size:'))
        self.fontFooterSizeSpinBox.setSuffix(
            translate('OpenLP.AmendThemeForm', 'pt'))
        self.fontFooterWeightComboBox.setItemText(0,
            translate('OpenLP.AmendThemeForm', 'Normal'))
        self.fontFooterWeightComboBox.setItemText(1,
            translate('OpenLP.AmendThemeForm', 'Bold'))
        self.fontFooterWeightComboBox.setItemText(2,
            translate('OpenLP.AmendThemeForm', 'Italics'))
        self.fontFooterWeightComboBox.setItemText(3,
            translate('OpenLP.AmendThemeForm', 'Bold/Italics'))
        self.fontFooterWeightLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Style:'))
        self.locationFooterGroupBox.setTitle(
            translate('OpenLP.AmendThemeForm', 'Display Location'))
        self.fontFooterDefaultLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Use default location'))
        self.fontFooterXLabel.setText(
            translate('OpenLP.AmendThemeForm', 'X position:'))
        self.fontFooterYLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Y position:'))
        self.fontFooterWidthLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Width:'))
        self.fontFooterHeightLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Height:'))
        self.fontFooterXSpinBox.setSuffix(
            translate('OpenLP.AmendThemeForm', 'px'))
        self.fontFooterYSpinBox.setSuffix(
            translate('OpenLP.AmendThemeForm', 'px'))
        self.fontFooterWidthSpinBox.setSuffix(
            translate('OpenLP.AmendThemeForm', 'px'))
        self.fontFooterHeightSpinBox.setSuffix(
            translate('OpenLP.AmendThemeForm', 'px'))
        self.themeTabWidget.setTabText(
            self.themeTabWidget.indexOf(self.fontFooterTab),
            translate('OpenLP.AmendThemeForm', '&Footer Font'))
        self.outlineGroupBox.setTitle(
            translate('OpenLP.AmendThemeForm', 'Outline'))
        self.outlineSpinBoxLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Outline size:'))
        self.outlineSpinBox.setSuffix(
            translate('OpenLP.AmendThemeForm', 'px'))
        self.outlineColorLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Outline color:'))
        self.outlineEnabledLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Show outline:'))
        self.shadowGroupBox.setTitle(
            translate('OpenLP.AmendThemeForm', 'Shadow'))
        self.shadowSpinBoxLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Shadow size:'))
        self.shadowSpinBox.setSuffix(
            translate('OpenLP.AmendThemeForm', 'px'))
        self.shadowColorLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Shadow color:'))
        self.shadowEnabledLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Show shadow:'))
        self.alignmentGroupBox.setTitle(
            translate('OpenLP.AmendThemeForm', 'Alignment'))
        self.horizontalLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Horizontal align:'))
        self.horizontalComboBox.setItemText(0,
            translate('OpenLP.AmendThemeForm', 'Left'))
        self.horizontalComboBox.setItemText(1,
            translate('OpenLP.AmendThemeForm', 'Right'))
        self.horizontalComboBox.setItemText(2,
            translate('OpenLP.AmendThemeForm', 'Center'))
        self.verticalLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Vertical align:'))
        self.verticalComboBox.setItemText(0,
            translate('OpenLP.AmendThemeForm', 'Top'))
        self.verticalComboBox.setItemText(1,
            translate('OpenLP.AmendThemeForm', 'Middle'))
        self.verticalComboBox.setItemText(2,
            translate('OpenLP.AmendThemeForm', 'Bottom'))
        self.transitionGroupBox.setTitle(
            translate('OpenLP.AmendThemeForm', 'Slide Transition'))
        self.slideTransitionCheckBoxLabel.setText(
            translate('OpenLP.AmendThemeForm', 'Transition active'))
        self.themeTabWidget.setTabText(
            self.themeTabWidget.indexOf(self.otherOptionsTab),
            translate('OpenLP.AmendThemeForm', '&Other Options'))
        self.previewGroupBox.setTitle(
            translate('OpenLP.AmendThemeForm', 'Preview'))
