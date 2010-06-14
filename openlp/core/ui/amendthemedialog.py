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

from openlp.core.lib import build_icon, translate

class Ui_AmendThemeDialog(object):
    def setupUi(self, AmendThemeDialog):
        AmendThemeDialog.setObjectName(u'AmendThemeDialog')
        AmendThemeDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AmendThemeDialog.resize(586, 651)
        icon = build_icon(u':/icon/openlp-logo-16x16.png')
        AmendThemeDialog.setWindowIcon(icon)
        AmendThemeDialog.setModal(True)
        self.AmendThemeLayout = QtGui.QVBoxLayout(AmendThemeDialog)
        self.AmendThemeLayout.setSpacing(8)
        self.AmendThemeLayout.setMargin(8)
        self.AmendThemeLayout.setObjectName(u'AmendThemeLayout')
        self.ThemeNameWidget = QtGui.QWidget(AmendThemeDialog)
        self.ThemeNameWidget.setObjectName(u'ThemeNameWidget')
        self.ThemeNameLayout = QtGui.QHBoxLayout(self.ThemeNameWidget)
        self.ThemeNameLayout.setSpacing(8)
        self.ThemeNameLayout.setMargin(0)
        self.ThemeNameLayout.setObjectName(u'ThemeNameLayout')
        self.ThemeNameLabel = QtGui.QLabel(self.ThemeNameWidget)
        self.ThemeNameLabel.setObjectName(u'ThemeNameLabel')
        self.ThemeNameLayout.addWidget(self.ThemeNameLabel)
        self.ThemeNameEdit = QtGui.QLineEdit(self.ThemeNameWidget)
        self.ThemeNameEdit.setObjectName(u'ThemeNameEdit')
        self.ThemeNameLayout.addWidget(self.ThemeNameEdit)
        self.AmendThemeLayout.addWidget(self.ThemeNameWidget)
        self.ContentWidget = QtGui.QWidget(AmendThemeDialog)
        self.ContentWidget.setObjectName(u'ContentWidget')
        self.ContentLayout = QtGui.QHBoxLayout(self.ContentWidget)
        self.ContentLayout.setSpacing(8)
        self.ContentLayout.setMargin(0)
        self.ContentLayout.setObjectName(u'ContentLayout')
        self.ThemeTabWidget = QtGui.QTabWidget(self.ContentWidget)
        self.ThemeTabWidget.setObjectName(u'ThemeTabWidget')
        self.BackgroundTab = QtGui.QWidget()
        self.BackgroundTab.setObjectName(u'BackgroundTab')
        self.BackgroundLayout = QtGui.QFormLayout(self.BackgroundTab)
        self.BackgroundLayout.setMargin(8)
        self.BackgroundLayout.setSpacing(8)
        self.BackgroundLayout.setObjectName(u'BackgroundLayout')
        self.BackgroundLabel = QtGui.QLabel(self.BackgroundTab)
        self.BackgroundLabel.setObjectName(u'BackgroundLabel')
        self.BackgroundLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.BackgroundLabel)
        self.BackgroundComboBox = QtGui.QComboBox(self.BackgroundTab)
        self.BackgroundComboBox.setObjectName(u'BackgroundComboBox')
        self.BackgroundComboBox.addItem(QtCore.QString())
        self.BackgroundComboBox.addItem(QtCore.QString())
        self.BackgroundLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.BackgroundComboBox)
        self.BackgroundTypeLabel = QtGui.QLabel(self.BackgroundTab)
        self.BackgroundTypeLabel.setObjectName(u'BackgroundTypeLabel')
        self.BackgroundLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.BackgroundTypeLabel)
        self.BackgroundTypeComboBox = QtGui.QComboBox(self.BackgroundTab)
        self.BackgroundTypeComboBox.setObjectName(u'BackgroundTypeComboBox')
        self.BackgroundTypeComboBox.addItem(QtCore.QString())
        self.BackgroundTypeComboBox.addItem(QtCore.QString())
        self.BackgroundTypeComboBox.addItem(QtCore.QString())
        self.BackgroundLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.BackgroundTypeComboBox)
        self.Color1Label = QtGui.QLabel(self.BackgroundTab)
        self.Color1Label.setObjectName(u'Color1Label')
        self.BackgroundLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.Color1Label)
        self.Color1PushButton = QtGui.QPushButton(self.BackgroundTab)
        self.Color1PushButton.setObjectName(u'Color1PushButton')
        self.BackgroundLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.Color1PushButton)
        self.Color2Label = QtGui.QLabel(self.BackgroundTab)
        self.Color2Label.setObjectName(u'Color2Label')
        self.BackgroundLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.Color2Label)
        self.Color2PushButton = QtGui.QPushButton(self.BackgroundTab)
        self.Color2PushButton.setObjectName(u'Color2PushButton')
        self.BackgroundLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.Color2PushButton)
        self.ImageLabel = QtGui.QLabel(self.BackgroundTab)
        self.ImageLabel.setObjectName(u'ImageLabel')
        self.BackgroundLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.ImageLabel)
        self.GradientLabel = QtGui.QLabel(self.BackgroundTab)
        self.GradientLabel.setObjectName(u'GradientLabel')
        self.BackgroundLayout.setWidget(6, QtGui.QFormLayout.LabelRole,
            self.GradientLabel)
        self.GradientComboBox = QtGui.QComboBox(self.BackgroundTab)
        self.GradientComboBox.setObjectName(u'GradientComboBox')
        self.GradientComboBox.addItem(QtCore.QString())
        self.GradientComboBox.addItem(QtCore.QString())
        self.GradientComboBox.addItem(QtCore.QString())
        self.BackgroundLayout.setWidget(6, QtGui.QFormLayout.FieldRole,
            self.GradientComboBox)
        self.ImageFilenameWidget = QtGui.QWidget(self.BackgroundTab)
        self.ImageFilenameWidget.setObjectName(u'ImageFilenameWidget')
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.ImageFilenameWidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(u'horizontalLayout_2')
        self.ImageLineEdit = QtGui.QLineEdit(self.ImageFilenameWidget)
        self.ImageLineEdit.setObjectName(u'ImageLineEdit')
        self.horizontalLayout_2.addWidget(self.ImageLineEdit)
        self.ImageToolButton = QtGui.QToolButton(self.ImageFilenameWidget)
        icon1 = build_icon(u':/general/general_open.png')
        self.ImageToolButton.setIcon(icon1)
        self.ImageToolButton.setObjectName(u'ImageToolButton')
        self.horizontalLayout_2.addWidget(self.ImageToolButton)
        self.BackgroundLayout.setWidget(4, QtGui.QFormLayout.FieldRole,
            self.ImageFilenameWidget)
        self.ThemeTabWidget.addTab(self.BackgroundTab, u'')
        self.FontMainTab = QtGui.QWidget()
        self.FontMainTab.setObjectName(u'FontMainTab')
        self.FontMainLayout = QtGui.QHBoxLayout(self.FontMainTab)
        self.FontMainLayout.setSpacing(8)
        self.FontMainLayout.setMargin(8)
        self.FontMainLayout.setObjectName(u'FontMainLayout')
        self.MainLeftWidget = QtGui.QWidget(self.FontMainTab)
        self.MainLeftWidget.setObjectName(u'MainLeftWidget')
        self.MainLeftLayout = QtGui.QVBoxLayout(self.MainLeftWidget)
        self.MainLeftLayout.setSpacing(8)
        self.MainLeftLayout.setMargin(0)
        self.MainLeftLayout.setObjectName(u'MainLeftLayout')
        self.FontMainGroupBox = QtGui.QGroupBox(self.MainLeftWidget)
        self.FontMainGroupBox.setObjectName(u'FontMainGroupBox')
        self.MainFontLayout = QtGui.QFormLayout(self.FontMainGroupBox)
        self.MainFontLayout.setFormAlignment(QtCore.Qt.AlignLeading |
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.MainFontLayout.setMargin(8)
        self.MainFontLayout.setSpacing(8)
        self.MainFontLayout.setObjectName(u'MainFontLayout')
        self.FontMainlabel = QtGui.QLabel(self.FontMainGroupBox)
        self.FontMainlabel.setObjectName(u'FontMainlabel')
        self.MainFontLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.FontMainlabel)
        self.FontMainComboBox = QtGui.QFontComboBox(self.FontMainGroupBox)
        self.FontMainComboBox.setObjectName(u'FontMainComboBox')
        self.MainFontLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.FontMainComboBox)
        self.FontMainColorLabel = QtGui.QLabel(self.FontMainGroupBox)
        self.FontMainColorLabel.setObjectName(u'FontMainColorLabel')
        self.MainFontLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.FontMainColorLabel)
        self.FontMainColorPushButton = QtGui.QPushButton(self.FontMainGroupBox)
        self.FontMainColorPushButton.setObjectName(u'FontMainColorPushButton')
        self.MainFontLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.FontMainColorPushButton)
        self.FontMainSize = QtGui.QLabel(self.FontMainGroupBox)
        self.FontMainSize.setObjectName(u'FontMainSize')
        self.MainFontLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.FontMainSize)
        self.FontMainSizeSpinBox = QtGui.QSpinBox(self.FontMainGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.FontMainSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.FontMainSizeSpinBox.setSizePolicy(sizePolicy)
        self.FontMainSizeSpinBox.setMinimumSize(QtCore.QSize(70, 0))
        self.FontMainSizeSpinBox.setProperty(u'value', QtCore.QVariant(16))
        self.FontMainSizeSpinBox.setMaximum(999)
        self.FontMainSizeSpinBox.setObjectName(u'FontMainSizeSpinBox')
        self.MainFontLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.FontMainSizeSpinBox)
        self.FontMainWeightComboBox = QtGui.QComboBox(self.FontMainGroupBox)
        self.FontMainWeightComboBox.setObjectName(u'FontMainWeightComboBox')
        self.FontMainWeightComboBox.addItem(QtCore.QString())
        self.FontMainWeightComboBox.addItem(QtCore.QString())
        self.FontMainWeightComboBox.addItem(QtCore.QString())
        self.FontMainWeightComboBox.addItem(QtCore.QString())
        self.MainFontLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.FontMainWeightComboBox)
        self.FontMainWeightLabel = QtGui.QLabel(self.FontMainGroupBox)
        self.FontMainWeightLabel.setObjectName(u'FontMainWeightLabel')
        self.MainFontLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.FontMainWeightLabel)
        self.MainLeftLayout.addWidget(self.FontMainGroupBox)
        self.FontMainWrapLineAdjustmentLabel = QtGui.QLabel(
            self.FontMainGroupBox)
        self.FontMainWrapLineAdjustmentLabel.setObjectName(
            u'FontMainWrapLineAdjustmentLabel')
        self.MainFontLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.FontMainWrapLineAdjustmentLabel)
        self.FontMainLineAdjustmentSpinBox = QtGui.QSpinBox(
            self.FontMainGroupBox)
        self.FontMainLineAdjustmentSpinBox.setObjectName(
            u'FontMainLineAdjustmentSpinBox')
        self.FontMainLineAdjustmentSpinBox.setMinimum(-99)
        self.MainFontLayout.setWidget(4, QtGui.QFormLayout.FieldRole,
            self.FontMainLineAdjustmentSpinBox)
        self.FontMainWrapIndentationLabel = QtGui.QLabel(self.FontMainGroupBox)
        self.FontMainWrapIndentationLabel.setObjectName(
            u'FontMainWrapIndentationLabel')
        self.MainFontLayout.setWidget(5, QtGui.QFormLayout.LabelRole,
            self.FontMainWrapIndentationLabel)
        self.FontMainLineSpacingSpinBox = QtGui.QSpinBox(self.FontMainGroupBox)
        self.FontMainLineSpacingSpinBox.setObjectName(
            u'FontMainLineSpacingSpinBox')
        self.FontMainLineSpacingSpinBox.setMaximum(10)
        self.MainFontLayout.setWidget(5, QtGui.QFormLayout.FieldRole,
            self.FontMainLineSpacingSpinBox)
        self.FontMainLinesPageLabel = QtGui.QLabel(self.FontMainGroupBox)
        self.FontMainLinesPageLabel.setObjectName(u'FontMainLinesPageLabel')
        self.MainFontLayout.setWidget(6, QtGui.QFormLayout.LabelRole,
            self.FontMainLinesPageLabel)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.MainLeftLayout.addItem(spacerItem1)
        self.FontMainLayout.addWidget(self.MainLeftWidget)
        self.MainRightWidget = QtGui.QWidget(self.FontMainTab)
        self.MainRightWidget.setObjectName(u'MainRightWidget')
        self.MainRightLayout = QtGui.QVBoxLayout(self.MainRightWidget)
        self.MainRightLayout.setSpacing(8)
        self.MainRightLayout.setMargin(0)
        self.MainRightLayout.setObjectName(u'MainRightLayout')
        self.MainLocationGroupBox = QtGui.QGroupBox(self.MainRightWidget)
        self.MainLocationGroupBox.setObjectName(u'MainLocationGroupBox')
        self.MainLocationLayout = QtGui.QFormLayout(self.MainLocationGroupBox)
        self.MainLocationLayout.setMargin(8)
        self.MainLocationLayout.setSpacing(8)
        self.MainLocationLayout.setObjectName(u'MainLocationLayout')
        self.DefaultLocationLabel = QtGui.QLabel(self.MainLocationGroupBox)
        self.DefaultLocationLabel.setObjectName(u'DefaultLocationLabel')
        self.MainLocationLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.DefaultLocationLabel)
        self.FontMainDefaultCheckBox = QtGui.QCheckBox(
            self.MainLocationGroupBox)
        self.FontMainDefaultCheckBox.setTristate(False)
        self.FontMainDefaultCheckBox.setObjectName(u'FontMainDefaultCheckBox')
        self.MainLocationLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.FontMainDefaultCheckBox)
        self.FontMainXLabel = QtGui.QLabel(self.MainLocationGroupBox)
        self.FontMainXLabel.setObjectName(u'FontMainXLabel')
        self.MainLocationLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.FontMainXLabel)
        self.FontMainYLabel = QtGui.QLabel(self.MainLocationGroupBox)
        self.FontMainYLabel.setObjectName(u'FontMainYLabel')
        self.MainLocationLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.FontMainYLabel)
        self.FontMainWidthLabel = QtGui.QLabel(self.MainLocationGroupBox)
        self.FontMainWidthLabel.setObjectName(u'FontMainWidthLabel')
        self.MainLocationLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.FontMainWidthLabel)
        self.FontMainHeightLabel = QtGui.QLabel(self.MainLocationGroupBox)
        self.FontMainHeightLabel.setObjectName(u'FontMainHeightLabel')
        self.MainLocationLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.FontMainHeightLabel)
        self.FontMainXSpinBox = QtGui.QSpinBox(self.MainLocationGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.FontMainXSpinBox.sizePolicy().hasHeightForWidth())
        self.FontMainXSpinBox.setSizePolicy(sizePolicy)
        self.FontMainXSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.FontMainXSpinBox.setProperty(u'value', QtCore.QVariant(0))
        self.FontMainXSpinBox.setMaximum(9999)
        self.FontMainXSpinBox.setObjectName(u'FontMainXSpinBox')
        self.MainLocationLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.FontMainXSpinBox)
        self.FontMainYSpinBox = QtGui.QSpinBox(self.MainLocationGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.FontMainYSpinBox.sizePolicy().hasHeightForWidth())
        self.FontMainYSpinBox.setSizePolicy(sizePolicy)
        self.FontMainYSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.FontMainYSpinBox.setMaximum(9999)
        self.FontMainYSpinBox.setObjectName(u'FontMainYSpinBox')
        self.MainLocationLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.FontMainYSpinBox)
        self.FontMainWidthSpinBox = QtGui.QSpinBox(self.MainLocationGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.FontMainWidthSpinBox.sizePolicy().hasHeightForWidth())
        self.FontMainWidthSpinBox.setSizePolicy(sizePolicy)
        self.FontMainWidthSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.FontMainWidthSpinBox.setMaximum(9999)
        self.FontMainWidthSpinBox.setObjectName(u'FontMainWidthSpinBox')
        self.MainLocationLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.FontMainWidthSpinBox)
        self.FontMainHeightSpinBox = QtGui.QSpinBox(self.MainLocationGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.FontMainHeightSpinBox.sizePolicy().hasHeightForWidth())
        self.FontMainHeightSpinBox.setSizePolicy(sizePolicy)
        self.FontMainHeightSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.FontMainHeightSpinBox.setMaximum(9999)
        self.FontMainHeightSpinBox.setObjectName(u'FontMainHeightSpinBox')
        self.MainLocationLayout.setWidget(4, QtGui.QFormLayout.FieldRole,
            self.FontMainHeightSpinBox)
        self.MainRightLayout.addWidget(self.MainLocationGroupBox)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.MainRightLayout.addItem(spacerItem2)
        self.FontMainLayout.addWidget(self.MainRightWidget)
        self.ThemeTabWidget.addTab(self.FontMainTab, u'')
        self.FontFooterTab = QtGui.QWidget()
        self.FontFooterTab.setObjectName(u'FontFooterTab')
        self.FontFooterLayout = QtGui.QHBoxLayout(self.FontFooterTab)
        self.FontFooterLayout.setSpacing(8)
        self.FontFooterLayout.setMargin(8)
        self.FontFooterLayout.setObjectName(u'FontFooterLayout')
        self.FooterLeftWidget = QtGui.QWidget(self.FontFooterTab)
        self.FooterLeftWidget.setObjectName(u'FooterLeftWidget')
        self.FooterLeftLayout = QtGui.QVBoxLayout(self.FooterLeftWidget)
        self.FooterLeftLayout.setSpacing(8)
        self.FooterLeftLayout.setMargin(0)
        self.FooterLeftLayout.setObjectName(u'FooterLeftLayout')
        self.FooterFontGroupBox = QtGui.QGroupBox(self.FooterLeftWidget)
        self.FooterFontGroupBox.setObjectName(u'FooterFontGroupBox')
        self.FooterFontLayout = QtGui.QFormLayout(self.FooterFontGroupBox)
        self.FooterFontLayout.setFieldGrowthPolicy(
            QtGui.QFormLayout.ExpandingFieldsGrow)
        self.FooterFontLayout.setFormAlignment(QtCore.Qt.AlignLeading |
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.FooterFontLayout.setMargin(8)
        self.FooterFontLayout.setSpacing(8)
        self.FooterFontLayout.setObjectName(u'FooterFontLayout')
        self.FontFooterLabel = QtGui.QLabel(self.FooterFontGroupBox)
        self.FontFooterLabel.setObjectName(u'FontFooterLabel')
        self.FooterFontLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.FontFooterLabel)
        self.FontFooterComboBox = QtGui.QFontComboBox(self.FooterFontGroupBox)
        self.FontFooterComboBox.setObjectName(u'FontFooterComboBox')
        self.FooterFontLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.FontFooterComboBox)
        self.FontFooterColorLabel = QtGui.QLabel(self.FooterFontGroupBox)
        self.FontFooterColorLabel.setObjectName(u'FontFooterColorLabel')
        self.FooterFontLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.FontFooterColorLabel)
        self.FontFooterColorPushButton = QtGui.QPushButton(
            self.FooterFontGroupBox)
        self.FontFooterColorPushButton.setObjectName(
            u'FontFooterColorPushButton')
        self.FooterFontLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.FontFooterColorPushButton)
        self.FontFooterSizeLabel = QtGui.QLabel(self.FooterFontGroupBox)
        self.FontFooterSizeLabel.setObjectName(u'FontFooterSizeLabel')
        self.FooterFontLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.FontFooterSizeLabel)
        self.FontFooterSizeSpinBox = QtGui.QSpinBox(self.FooterFontGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.FontFooterSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.FontFooterSizeSpinBox.setSizePolicy(sizePolicy)
        self.FontFooterSizeSpinBox.setMinimumSize(QtCore.QSize(70, 0))
        self.FontFooterSizeSpinBox.setProperty(u'value', QtCore.QVariant(10))
        self.FontFooterSizeSpinBox.setMaximum(999)
        self.FontFooterSizeSpinBox.setObjectName(u'FontFooterSizeSpinBox')
        self.FooterFontLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.FontFooterSizeSpinBox)
        self.FontFooterWeightComboBox = QtGui.QComboBox(self.FooterFontGroupBox)
        self.FontFooterWeightComboBox.setObjectName(u'FontFooterWeightComboBox')
        self.FontFooterWeightComboBox.addItem(QtCore.QString())
        self.FontFooterWeightComboBox.addItem(QtCore.QString())
        self.FontFooterWeightComboBox.addItem(QtCore.QString())
        self.FontFooterWeightComboBox.addItem(QtCore.QString())
        self.FooterFontLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.FontFooterWeightComboBox)
        self.FontFooterWeightLabel = QtGui.QLabel(self.FooterFontGroupBox)
        self.FontFooterWeightLabel.setObjectName(u'FontFooterWeightLabel')
        self.FooterFontLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.FontFooterWeightLabel)
        self.FooterLeftLayout.addWidget(self.FooterFontGroupBox)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.FooterLeftLayout.addItem(spacerItem3)
        self.FontFooterLayout.addWidget(self.FooterLeftWidget)
        self.FooterRightWidget = QtGui.QWidget(self.FontFooterTab)
        self.FooterRightWidget.setObjectName(u'FooterRightWidget')
        self.FooterRightLayout = QtGui.QVBoxLayout(self.FooterRightWidget)
        self.FooterRightLayout.setSpacing(8)
        self.FooterRightLayout.setMargin(0)
        self.FooterRightLayout.setObjectName(u'FooterRightLayout')
        self.LocationFooterGroupBox = QtGui.QGroupBox(self.FooterRightWidget)
        self.LocationFooterGroupBox.setObjectName(u'LocationFooterGroupBox')
        self.LocationFooterLayout = QtGui.QFormLayout(
            self.LocationFooterGroupBox)
        self.LocationFooterLayout.setFieldGrowthPolicy(
            QtGui.QFormLayout.ExpandingFieldsGrow)
        self.LocationFooterLayout.setFormAlignment(QtCore.Qt.AlignLeading |
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.LocationFooterLayout.setMargin(8)
        self.LocationFooterLayout.setSpacing(8)
        self.LocationFooterLayout.setObjectName(u'LocationFooterLayout')
        self.FontFooterDefaultLabel = QtGui.QLabel(self.LocationFooterGroupBox)
        self.FontFooterDefaultLabel.setObjectName(u'FontFooterDefaultLabel')
        self.LocationFooterLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.FontFooterDefaultLabel)
        self.FontFooterDefaultCheckBox = QtGui.QCheckBox(
            self.LocationFooterGroupBox)
        self.FontFooterDefaultCheckBox.setTristate(False)
        self.FontFooterDefaultCheckBox.setObjectName(
            u'FontFooterDefaultCheckBox')
        self.LocationFooterLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.FontFooterDefaultCheckBox)
        self.FontFooterXLabel = QtGui.QLabel(self.LocationFooterGroupBox)
        self.FontFooterXLabel.setObjectName(u'FontFooterXLabel')
        self.LocationFooterLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.FontFooterXLabel)
        self.FontFooterYLabel = QtGui.QLabel(self.LocationFooterGroupBox)
        self.FontFooterYLabel.setObjectName(u'FontFooterYLabel')
        self.LocationFooterLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.FontFooterYLabel)
        self.FontFooterWidthLabel = QtGui.QLabel(self.LocationFooterGroupBox)
        self.FontFooterWidthLabel.setObjectName(u'FontFooterWidthLabel')
        self.LocationFooterLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.FontFooterWidthLabel)
        self.FontFooterHeightLabel = QtGui.QLabel(self.LocationFooterGroupBox)
        self.FontFooterHeightLabel.setObjectName(u'FontFooterHeightLabel')
        self.LocationFooterLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.FontFooterHeightLabel)
        self.FontFooterXSpinBox = QtGui.QSpinBox(self.LocationFooterGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.FontFooterXSpinBox.sizePolicy().hasHeightForWidth())
        self.FontFooterXSpinBox.setSizePolicy(sizePolicy)
        self.FontFooterXSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.FontFooterXSpinBox.setProperty(u'value', QtCore.QVariant(0))
        self.FontFooterXSpinBox.setMaximum(9999)
        self.FontFooterXSpinBox.setObjectName(u'FontFooterXSpinBox')
        self.LocationFooterLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.FontFooterXSpinBox)
        self.FontFooterYSpinBox = QtGui.QSpinBox(self.LocationFooterGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.FontFooterYSpinBox.sizePolicy().hasHeightForWidth())
        self.FontFooterYSpinBox.setSizePolicy(sizePolicy)
        self.FontFooterYSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.FontFooterYSpinBox.setProperty(u'value', QtCore.QVariant(0))
        self.FontFooterYSpinBox.setMaximum(9999)
        self.FontFooterYSpinBox.setObjectName(u'FontFooterYSpinBox')
        self.LocationFooterLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.FontFooterYSpinBox)
        self.FontFooterWidthSpinBox = QtGui.QSpinBox(
            self.LocationFooterGroupBox)
        self.FontFooterWidthSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.FontFooterWidthSpinBox.setMaximum(9999)
        self.FontFooterWidthSpinBox.setObjectName(u'FontFooterWidthSpinBox')
        self.LocationFooterLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.FontFooterWidthSpinBox)
        self.FontFooterHeightSpinBox = QtGui.QSpinBox(
            self.LocationFooterGroupBox)
        self.FontFooterHeightSpinBox.setMinimumSize(QtCore.QSize(78, 0))
        self.FontFooterHeightSpinBox.setMaximum(9999)
        self.FontFooterHeightSpinBox.setObjectName(u'FontFooterHeightSpinBox')
        self.LocationFooterLayout.setWidget(4, QtGui.QFormLayout.FieldRole,
            self.FontFooterHeightSpinBox)
        self.FooterRightLayout.addWidget(self.LocationFooterGroupBox)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.FooterRightLayout.addItem(spacerItem4)
        self.FontFooterLayout.addWidget(self.FooterRightWidget)
        self.ThemeTabWidget.addTab(self.FontFooterTab, u'')
        self.OtherOptionsTab = QtGui.QWidget()
        self.OtherOptionsTab.setObjectName(u'OtherOptionsTab')
        self.OtherOptionsLayout = QtGui.QHBoxLayout(self.OtherOptionsTab)
        self.OtherOptionsLayout.setSpacing(8)
        self.OtherOptionsLayout.setMargin(8)
        self.OtherOptionsLayout.setObjectName(u'OtherOptionsLayout')
        self.OptionsLeftWidget = QtGui.QWidget(self.OtherOptionsTab)
        self.OptionsLeftWidget.setObjectName(u'OptionsLeftWidget')
        self.OptionsLeftLayout = QtGui.QVBoxLayout(self.OptionsLeftWidget)
        self.OptionsLeftLayout.setSpacing(8)
        self.OptionsLeftLayout.setMargin(0)
        self.OptionsLeftLayout.setObjectName(u'OptionsLeftLayout')
        self.OutlineGroupBox = QtGui.QGroupBox(self.OptionsLeftWidget)
        self.OutlineGroupBox.setObjectName(u'OutlineGroupBox')
        self.verticalLayout = QtGui.QVBoxLayout(self.OutlineGroupBox)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setMargin(8)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.OutlineWidget = QtGui.QWidget(self.OutlineGroupBox)
        self.OutlineWidget.setObjectName(u'OutlineWidget')
        self.OutlineLayout = QtGui.QFormLayout(self.OutlineWidget)
        self.OutlineLayout.setMargin(0)
        self.OutlineLayout.setSpacing(8)
        self.OutlineLayout.setObjectName(u'OutlineLayout')
        self.OutlineCheckBox = QtGui.QCheckBox(self.OutlineWidget)
        self.OutlineCheckBox.setObjectName(u'OutlineCheckBox')
        self.OutlineLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.OutlineCheckBox)
        self.OutlineSpinBox = QtGui.QSpinBox(self.OutlineWidget)
        self.OutlineSpinBox.setObjectName(u'OutlineSpinBox')
        self.OutlineSpinBox.setMaximum(10)
        self.OutlineLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.OutlineSpinBox)
        self.OutlineSpinBoxLabel = QtGui.QLabel(self.OutlineWidget)
        self.OutlineSpinBoxLabel.setObjectName(u'OutlineSpinBoxLabel')
        self.OutlineLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.OutlineSpinBoxLabel)
        self.OutlineColorLabel = QtGui.QLabel(self.OutlineWidget)
        self.OutlineColorLabel.setObjectName(u'OutlineColorLabel')
        self.OutlineLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.OutlineColorLabel)
        self.OutlineColorPushButton = QtGui.QPushButton(self.OutlineWidget)
        self.OutlineColorPushButton.setObjectName(u'OutlineColorPushButton')
        self.OutlineLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.OutlineColorPushButton)
        self.OutlineEnabledLabel = QtGui.QLabel(self.OutlineWidget)
        self.OutlineEnabledLabel.setObjectName(u'OutlineEnabledLabel')
        self.OutlineLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.OutlineEnabledLabel)
        self.verticalLayout.addWidget(self.OutlineWidget)
        self.OptionsLeftLayout.addWidget(self.OutlineGroupBox)
        self.ShadowGroupBox = QtGui.QGroupBox(self.OptionsLeftWidget)
        self.ShadowGroupBox.setObjectName(u'ShadowGroupBox')
        self.verticalLayout = QtGui.QVBoxLayout(self.ShadowGroupBox)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setMargin(8)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.ShadowWidget = QtGui.QWidget(self.ShadowGroupBox)
        self.ShadowWidget.setObjectName(u'ShadowWidget')
        self.ShadowLayout = QtGui.QFormLayout(self.ShadowWidget)
        self.ShadowLayout.setMargin(0)
        self.ShadowLayout.setSpacing(8)
        self.ShadowLayout.setObjectName(u'ShadowLayout')
        self.ShadowCheckBox = QtGui.QCheckBox(self.ShadowWidget)
        self.ShadowCheckBox.setObjectName(u'ShadowCheckBox')
        self.ShadowLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.ShadowCheckBox)
        self.ShadowSpinBox = QtGui.QSpinBox(self.OutlineWidget)
        self.ShadowSpinBox.setObjectName(u'ShadowSpinBox')
        self.ShadowSpinBox.setMaximum(10)
        self.ShadowLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.ShadowSpinBox)
        self.ShadowSpinBoxLabel = QtGui.QLabel(self.OutlineWidget)
        self.ShadowSpinBoxLabel.setObjectName(u'ShadowSpinBoxLabel')
        self.ShadowLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.ShadowSpinBoxLabel)
        self.ShadowColorLabel = QtGui.QLabel(self.ShadowWidget)
        self.ShadowColorLabel.setObjectName(u'ShadowColorLabel')
        self.ShadowLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.ShadowColorLabel)
        self.ShadowColorPushButton = QtGui.QPushButton(self.ShadowWidget)
        self.ShadowColorPushButton.setObjectName(u'ShadowColorPushButton')
        self.ShadowLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.ShadowColorPushButton)
        self.ShadowEnabledLabel = QtGui.QLabel(self.ShadowWidget)
        self.ShadowEnabledLabel.setObjectName(u'ShadowEnabledLabel')
        self.ShadowLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.ShadowEnabledLabel)
        self.verticalLayout.addWidget(self.ShadowWidget)
        self.OptionsLeftLayout.addWidget(self.ShadowGroupBox)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.OptionsLeftLayout.addItem(spacerItem5)
        self.OtherOptionsLayout.addWidget(self.OptionsLeftWidget)
        self.OptionsRightWidget = QtGui.QWidget(self.OtherOptionsTab)
        self.OptionsRightWidget.setObjectName(u'OptionsRightWidget')
        self.OptionsRightLayout = QtGui.QVBoxLayout(self.OptionsRightWidget)
        self.OptionsRightLayout.setSpacing(8)
        self.OptionsRightLayout.setMargin(0)
        self.OptionsRightLayout.setObjectName(u'OptionsRightLayout')
        self.AlignmentGroupBox = QtGui.QGroupBox(self.OptionsRightWidget)
        self.AlignmentGroupBox.setObjectName(u'AlignmentGroupBox')
        self.gridLayout_4 = QtGui.QGridLayout(self.AlignmentGroupBox)
        self.gridLayout_4.setObjectName(u'gridLayout_4')
        self.HorizontalLabel = QtGui.QLabel(self.AlignmentGroupBox)
        self.HorizontalLabel.setObjectName(u'HorizontalLabel')
        self.gridLayout_4.addWidget(self.HorizontalLabel, 0, 0, 1, 1)
        self.HorizontalComboBox = QtGui.QComboBox(self.AlignmentGroupBox)
        self.HorizontalComboBox.setObjectName(u'HorizontalComboBox')
        self.HorizontalComboBox.addItem(QtCore.QString())
        self.HorizontalComboBox.addItem(QtCore.QString())
        self.HorizontalComboBox.addItem(QtCore.QString())
        self.gridLayout_4.addWidget(self.HorizontalComboBox, 0, 1, 1, 1)
        self.VerticalLabel = QtGui.QLabel(self.AlignmentGroupBox)
        self.VerticalLabel.setObjectName(u'VerticalLabel')
        self.gridLayout_4.addWidget(self.VerticalLabel, 1, 0, 1, 1)
        self.VerticalComboBox = QtGui.QComboBox(self.AlignmentGroupBox)
        self.VerticalComboBox.setObjectName(u'VerticalComboBox')
        self.VerticalComboBox.addItem(QtCore.QString())
        self.VerticalComboBox.addItem(QtCore.QString())
        self.VerticalComboBox.addItem(QtCore.QString())
        self.gridLayout_4.addWidget(self.VerticalComboBox, 1, 1, 1, 1)
        self.OptionsRightLayout.addWidget(self.AlignmentGroupBox)
        self.TransitionGroupBox = QtGui.QGroupBox(self.OptionsRightWidget)
        self.TransitionGroupBox.setObjectName(u'TransitionGroupBox')
        self.gridLayout_5 = QtGui.QGridLayout(self.TransitionGroupBox)
        self.gridLayout_5.setObjectName(u'gridLayout_5')
        self.SlideTransitionCheckedBoxLabel = QtGui.QLabel(
            self.TransitionGroupBox)
        self.SlideTransitionCheckedBoxLabel.setObjectName(
            u'SlideTransitionCheckedBoxLabel')
        self.gridLayout_5.addWidget(
            self.SlideTransitionCheckedBoxLabel, 0, 0, 1, 1)
        self.SlideTransitionCheckedBox = QtGui.QCheckBox(self.AlignmentGroupBox)
        self.SlideTransitionCheckedBox.setTristate(False)
        self.gridLayout_5.addWidget(self.SlideTransitionCheckedBox, 0, 1, 1, 1)
        self.OptionsRightLayout.addWidget(self.TransitionGroupBox)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.OptionsRightLayout.addItem(spacerItem6)
        self.OtherOptionsLayout.addWidget(self.OptionsRightWidget)
        self.ThemeTabWidget.addTab(self.OtherOptionsTab, u'')
        self.ContentLayout.addWidget(self.ThemeTabWidget)
        self.AmendThemeLayout.addWidget(self.ContentWidget)
        self.PreviewGroupBox = QtGui.QGroupBox(AmendThemeDialog)
        self.PreviewGroupBox.setObjectName(u'PreviewGroupBox')
        self.ThemePreviewLayout = QtGui.QHBoxLayout(self.PreviewGroupBox)
        self.ThemePreviewLayout.setSpacing(8)
        self.ThemePreviewLayout.setMargin(8)
        self.ThemePreviewLayout.setObjectName(u'ThemePreviewLayout')
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        self.ThemePreviewLayout.addItem(spacerItem7)
        self.ThemePreview = QtGui.QLabel(self.PreviewGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ThemePreview.sizePolicy().hasHeightForWidth())
        self.ThemePreview.setSizePolicy(sizePolicy)
        self.ThemePreview.setMaximumSize(QtCore.QSize(300, 225))
        self.ThemePreview.setFrameShape(QtGui.QFrame.WinPanel)
        self.ThemePreview.setFrameShadow(QtGui.QFrame.Sunken)
        self.ThemePreview.setLineWidth(1)
        self.ThemePreview.setScaledContents(True)
        self.ThemePreview.setObjectName(u'ThemePreview')
        self.ThemePreviewLayout.addWidget(self.ThemePreview)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        self.ThemePreviewLayout.addItem(spacerItem8)
        self.AmendThemeLayout.addWidget(self.PreviewGroupBox)
        self.ThemeButtonBox = QtGui.QDialogButtonBox(AmendThemeDialog)
        self.ThemeButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Ok)
        self.ThemeButtonBox.setObjectName(u'ThemeButtonBox')
        self.AmendThemeLayout.addWidget(self.ThemeButtonBox)

        self.retranslateUi(AmendThemeDialog)
        self.ThemeTabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.ThemeButtonBox,
            QtCore.SIGNAL(u'accepted()'), AmendThemeDialog.accept)
        QtCore.QObject.connect(self.ThemeButtonBox,
            QtCore.SIGNAL(u'rejected()'), AmendThemeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AmendThemeDialog)
        AmendThemeDialog.setTabOrder(self.ThemeButtonBox, self.ThemeNameEdit)
        AmendThemeDialog.setTabOrder(self.ThemeNameEdit, self.ThemeTabWidget)
        AmendThemeDialog.setTabOrder(self.ThemeTabWidget,
            self.BackgroundComboBox)
        AmendThemeDialog.setTabOrder(self.BackgroundComboBox,
            self.BackgroundTypeComboBox)
        AmendThemeDialog.setTabOrder(self.BackgroundTypeComboBox,
            self.Color1PushButton)
        AmendThemeDialog.setTabOrder(self.Color1PushButton,
            self.Color2PushButton)
        AmendThemeDialog.setTabOrder(self.Color2PushButton, self.ImageLineEdit)
        AmendThemeDialog.setTabOrder(self.ImageLineEdit, self.ImageToolButton)
        AmendThemeDialog.setTabOrder(self.ImageToolButton,
            self.GradientComboBox)
        AmendThemeDialog.setTabOrder(self.GradientComboBox,
            self.FontMainComboBox)
        AmendThemeDialog.setTabOrder(self.FontMainComboBox,
            self.FontMainColorPushButton)
        AmendThemeDialog.setTabOrder(self.FontMainColorPushButton,
            self.FontMainSizeSpinBox)
        AmendThemeDialog.setTabOrder(self.FontMainSizeSpinBox,
            self.FontMainWeightComboBox)
        AmendThemeDialog.setTabOrder(self.FontMainWeightComboBox,
            self.FontMainLineSpacingSpinBox)
        AmendThemeDialog.setTabOrder(self.FontMainLineSpacingSpinBox,
            self.FontMainDefaultCheckBox)
        AmendThemeDialog.setTabOrder(self.FontMainDefaultCheckBox,
            self.FontMainXSpinBox)
        AmendThemeDialog.setTabOrder(self.FontMainXSpinBox,
            self.FontMainYSpinBox)
        AmendThemeDialog.setTabOrder(self.FontMainYSpinBox,
            self.FontMainWidthSpinBox)
        AmendThemeDialog.setTabOrder(self.FontMainWidthSpinBox,
            self.FontMainHeightSpinBox)
        AmendThemeDialog.setTabOrder(self.FontMainHeightSpinBox,
            self.FontFooterComboBox)
        AmendThemeDialog.setTabOrder(self.FontFooterComboBox,
            self.FontFooterColorPushButton)
        AmendThemeDialog.setTabOrder(self.FontFooterColorPushButton,
            self.FontFooterSizeSpinBox)
        AmendThemeDialog.setTabOrder(self.FontFooterSizeSpinBox,
            self.FontFooterWeightComboBox)
        AmendThemeDialog.setTabOrder(self.FontFooterWeightComboBox,
            self.FontFooterDefaultCheckBox)
        AmendThemeDialog.setTabOrder(self.FontFooterDefaultCheckBox,
            self.FontFooterXSpinBox)
        AmendThemeDialog.setTabOrder(self.FontFooterXSpinBox,
            self.FontFooterYSpinBox)
        AmendThemeDialog.setTabOrder(self.FontFooterYSpinBox,
            self.FontFooterWidthSpinBox)
        AmendThemeDialog.setTabOrder(self.FontFooterWidthSpinBox,
            self.FontFooterHeightSpinBox)
        AmendThemeDialog.setTabOrder(self.FontFooterHeightSpinBox,
            self.OutlineCheckBox)
        AmendThemeDialog.setTabOrder(self.OutlineCheckBox,
            self.OutlineColorPushButton)
        AmendThemeDialog.setTabOrder(self.OutlineColorPushButton,
            self.ShadowCheckBox)
        AmendThemeDialog.setTabOrder(self.ShadowCheckBox,
            self.ShadowColorPushButton)
        AmendThemeDialog.setTabOrder(self.ShadowColorPushButton,
            self.HorizontalComboBox)
        AmendThemeDialog.setTabOrder(self.HorizontalComboBox,
            self.VerticalComboBox)

    def retranslateUi(self, AmendThemeDialog):
        AmendThemeDialog.setWindowTitle(
            translate(u'AmendThemeForm', u'Theme Maintenance'))
        self.ThemeNameLabel.setText(
            translate(u'AmendThemeForm', u'Theme Name:'))
        self.BackgroundLabel.setText(
            translate(u'AmendThemeForm', u'Background:'))
        self.BackgroundComboBox.setItemText(0,
            translate(u'AmendThemeForm', u'Opaque'))
        self.BackgroundComboBox.setItemText(1,
            translate(u'AmendThemeForm', u'Transparent'))
        self.BackgroundTypeLabel.setText(
            translate(u'AmendThemeForm', u'Background Type:'))
        self.BackgroundTypeComboBox.setItemText(0,
            translate(u'AmendThemeForm', u'Solid Color'))
        self.BackgroundTypeComboBox.setItemText(1,
            translate(u'AmendThemeForm', u'Gradient'))
        self.BackgroundTypeComboBox.setItemText(2,
            translate(u'AmendThemeForm', u'Image'))
        self.Color1Label.setText(translate(u'AmendThemeForm', u'<Color1>'))
        self.Color2Label.setText(translate(u'AmendThemeForm', u'<Color2>'))
        self.ImageLabel.setText(translate(u'AmendThemeForm', u'Image:'))
        self.GradientLabel.setText(translate(u'AmendThemeForm', u'Gradient :'))
        self.GradientComboBox.setItemText(0,
            translate(u'AmendThemeForm', u'Horizontal'))
        self.GradientComboBox.setItemText(1,
            translate(u'AmendThemeForm', u'Vertical'))
        self.GradientComboBox.setItemText(2,
            translate(u'AmendThemeForm', u'Circular'))
        self.ThemeTabWidget.setTabText(
            self.ThemeTabWidget.indexOf(self.BackgroundTab),
            translate(u'AmendThemeForm', u'Background'))
        self.FontMainGroupBox.setTitle(
            translate(u'AmendThemeForm', u'Main Font'))
        self.FontMainlabel.setText(translate(u'AmendThemeForm', u'Font:'))
        self.FontMainColorLabel.setText(
            translate(u'AmendThemeForm', u'Font Color:'))
        self.FontMainSize.setText(translate(u'AmendThemeForm', u'Size:'))
        self.FontMainSizeSpinBox.setSuffix(translate(u'AmendThemeForm', u'pt'))
        self.FontMainWrapIndentationLabel.setText(
            translate(u'AmendThemeForm', u'Wrap Indentation'))
        self.FontMainWrapLineAdjustmentLabel.setText(
            translate(u'AmendThemeForm', u'Adjust Line Spacing'))
        self.FontMainWeightComboBox.setItemText(0,
            translate(u'AmendThemeForm', u'Normal'))
        self.FontMainWeightComboBox.setItemText(1,
            translate(u'AmendThemeForm', u'Bold'))
        self.FontMainWeightComboBox.setItemText(2,
            translate(u'AmendThemeForm', u'Italics'))
        self.FontMainWeightComboBox.setItemText(3,
            translate(u'AmendThemeForm', u'Bold/Italics'))
        self.FontMainWeightLabel.setText(
            translate(u'AmendThemeForm', u'Font Weight:'))
        self.MainLocationGroupBox.setTitle(
            translate(u'AmendThemeForm', u'Display Location'))
        self.DefaultLocationLabel.setText(
            translate(u'AmendThemeForm', u'Use Default Location:'))
        self.FontMainXLabel.setText(
            translate(u'AmendThemeForm', u'X Position:'))
        self.FontMainYLabel.setText(
            translate(u'AmendThemeForm', u'Y Position:'))
        self.FontMainWidthLabel.setText(
            translate(u'AmendThemeForm', u'Width:'))
        self.FontMainHeightLabel.setText(
            translate(u'AmendThemeForm', u'Height:'))
        self.FontMainXSpinBox.setSuffix(translate(u'AmendThemeForm', u'px'))
        self.FontMainYSpinBox.setSuffix(translate(u'AmendThemeForm', u'px'))
        self.FontMainWidthSpinBox.setSuffix(translate(u'AmendThemeForm', u'px'))
        self.FontMainHeightSpinBox.setSuffix(
            translate(u'AmendThemeForm', u'px'))
        self.ThemeTabWidget.setTabText(
            self.ThemeTabWidget.indexOf(self.FontMainTab),
            translate(u'AmendThemeForm', u'Font Main'))
        self.FooterFontGroupBox.setTitle(
            translate(u'AmendThemeForm', u'Footer Font'))
        self.FontFooterLabel.setText(translate(u'AmendThemeForm', u'Font:'))
        self.FontFooterColorLabel.setText(
            translate(u'AmendThemeForm', u'Font Color:'))
        self.FontFooterSizeLabel.setText(translate(u'AmendThemeForm', u'Size:'))
        self.FontFooterSizeSpinBox.setSuffix(
            translate(u'AmendThemeForm', u'pt'))
        self.FontFooterWeightComboBox.setItemText(0,
            translate(u'AmendThemeForm', u'Normal'))
        self.FontFooterWeightComboBox.setItemText(1,
            translate(u'AmendThemeForm', u'Bold'))
        self.FontFooterWeightComboBox.setItemText(2,
            translate(u'AmendThemeForm', u'Italics'))
        self.FontFooterWeightComboBox.setItemText(3,
            translate(u'AmendThemeForm', u'Bold/Italics'))
        self.FontFooterWeightLabel.setText(
            translate(u'AmendThemeForm', u'Font Weight:'))
        self.LocationFooterGroupBox.setTitle(
            translate(u'AmendThemeForm', u'Display Location'))
        self.FontFooterDefaultLabel.setText(
            translate(u'AmendThemeForm', u'Use Default Location:'))
        self.FontFooterXLabel.setText(
            translate(u'AmendThemeForm', u'X Position:'))
        self.FontFooterYLabel.setText(
            translate(u'AmendThemeForm', u'Y Position:'))
        self.FontFooterWidthLabel.setText(
            translate(u'AmendThemeForm', u'Width:'))
        self.FontFooterHeightLabel.setText(
            translate(u'AmendThemeForm', u'Height:'))
        self.FontFooterXSpinBox.setSuffix(
            translate(u'AmendThemeForm', u'px'))
        self.FontFooterYSpinBox.setSuffix(
            translate(u'AmendThemeForm', u'px'))
        self.FontFooterWidthSpinBox.setSuffix(
            translate(u'AmendThemeForm', u'px'))
        self.FontFooterHeightSpinBox.setSuffix(
            translate(u'AmendThemeForm', u'px'))
        self.ThemeTabWidget.setTabText(
            self.ThemeTabWidget.indexOf(self.FontFooterTab),
            translate(u'AmendThemeForm', u'Font Footer'))
        self.OutlineGroupBox.setTitle(translate(u'AmendThemeForm', u'Outline'))
        self.OutlineSpinBoxLabel.setText(
            translate(u'AmendThemeForm', u'Outline Size:'))
        self.OutlineSpinBox.setSuffix(translate(u'AmendThemeForm', u'px'))
        self.OutlineColorLabel.setText(
            translate(u'AmendThemeForm', u'Outline Color:'))
        self.OutlineEnabledLabel.setText(
            translate(u'AmendThemeForm', u'Show Outline:'))
        self.ShadowGroupBox.setTitle(translate(u'AmendThemeForm', u'Shadow'))
        self.ShadowSpinBoxLabel.setText(
            translate(u'AmendThemeForm', u'Shadow Size:'))
        self.ShadowSpinBox.setSuffix(translate(u'AmendThemeForm', u'px'))
        self.ShadowColorLabel.setText(
            translate(u'AmendThemeForm', u'Shadow Color:'))
        self.ShadowEnabledLabel.setText(
            translate(u'AmendThemeForm', u'Show Shadow:'))
        self.AlignmentGroupBox.setTitle(
            translate(u'AmendThemeForm', u'Alignment'))
        self.HorizontalLabel.setText(
            translate(u'AmendThemeForm', u'Horizontal Align:'))
        self.HorizontalComboBox.setItemText(0, 
            translate(u'AmendThemeForm', u'Left'))
        self.HorizontalComboBox.setItemText(1, 
            translate(u'AmendThemeForm', u'Right'))
        self.HorizontalComboBox.setItemText(2, 
            translate(u'AmendThemeForm', u'Center'))
        self.VerticalLabel.setText(
            translate(u'AmendThemeForm', u'Vertical Align:'))
        self.VerticalComboBox.setItemText(0, 
            translate(u'AmendThemeForm', u'Top'))
        self.VerticalComboBox.setItemText(1, 
            translate(u'AmendThemeForm', u'Middle'))
        self.VerticalComboBox.setItemText(2, 
            translate(u'AmendThemeForm', u'Bottom'))
        self.TransitionGroupBox.setTitle(
            translate(u'AmendThemeForm', u'Slide Transition'))
        self.SlideTransitionCheckedBoxLabel.setText(
            translate(u'AmendThemeForm', u'Transition Active:'))
        self.ThemeTabWidget.setTabText(
            self.ThemeTabWidget.indexOf(self.OtherOptionsTab),
            translate(u'AmendThemeForm', u'Other Options'))
        self.PreviewGroupBox.setTitle(translate(u'AmendThemeForm', u'Preview'))

