# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

from openlp.core.lib import translate
from openlp.core.lib.ui import UiStrings

class Ui_MediaOpenDialog(object):
    def setupUi(self, mediaOpenDialog):
        mediaOpenDialog.setObjectName(u'mediaOpenDialog')
        mediaOpenDialog.resize(574, 431)
        self.verticalLayout = QtGui.QVBoxLayout(mediaOpenDialog)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.MediaOpenWidget = QtGui.QTabWidget(mediaOpenDialog)
        self.MediaOpenWidget.setTabPosition(QtGui.QTabWidget.North)
        self.MediaOpenWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.MediaOpenWidget.setTabsClosable(False)
        self.MediaOpenWidget.setObjectName(u'MediaOpenWidget')
        self.FileTab = QtGui.QWidget()
        self.FileTab.setObjectName(u'FileTab')
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.FileTab)
        self.verticalLayout_2.setObjectName(u'verticalLayout_2')
        self.FileSelectionGroupBox = QtGui.QGroupBox(self.FileTab)
        self.FileSelectionGroupBox.setObjectName(u'FileSelectionGroupBox')
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.FileSelectionGroupBox)
        self.verticalLayout_7.setObjectName(u'verticalLayout_7')
        self.ChooseFilesLabel = QtGui.QLabel(self.FileSelectionGroupBox)
        self.ChooseFilesLabel.setObjectName(u'ChooseFilesLabel')
        self.verticalLayout_7.addWidget(self.ChooseFilesLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.FilesListView = QtGui.QListWidget(self.FileSelectionGroupBox)
        self.FilesListView.setObjectName(u'FilesListView')
        self.horizontalLayout.addWidget(self.FilesListView)
        self.AddRemovelLayout = QtGui.QVBoxLayout()
        self.AddRemovelLayout.setObjectName(u'AddRemovelLayout')
        self.FileAddButton = QtGui.QPushButton(self.FileSelectionGroupBox)
        self.FileAddButton.setObjectName(u'FileAddButton')
        self.AddRemovelLayout.addWidget(self.FileAddButton)
        self.FileRemoveButton = QtGui.QPushButton(self.FileSelectionGroupBox)
        self.FileRemoveButton.setObjectName(u'FileRemoveButton')
        self.AddRemovelLayout.addWidget(self.FileRemoveButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.AddRemovelLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.AddRemovelLayout)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem1)
        self.verticalLayout_2.addWidget(self.FileSelectionGroupBox)
        self.MediaOpenWidget.addTab(self.FileTab, u'')
        self.MediaTab = QtGui.QWidget()
        self.MediaTab.setObjectName(u'MediaTab')
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.MediaTab)
        self.verticalLayout_3.setObjectName(u'verticalLayout_3')
        self.ChooseMediaGroupBox = QtGui.QGroupBox(self.MediaTab)
        self.ChooseMediaGroupBox.setObjectName(u'ChooseMediaGroupBox')
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.ChooseMediaGroupBox)
        self.verticalLayout_8.setObjectName(u'verticalLayout_8')
        self.MediaTypeWidget = QtGui.QWidget(self.ChooseMediaGroupBox)
        self.MediaTypeWidget.setObjectName(u'MediaTypeWidget')
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.MediaTypeWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(u'horizontalLayout_2')
        self.DvdRadioButton = QtGui.QRadioButton(self.MediaTypeWidget)
        self.DvdRadioButton.setObjectName(u'DvdRadioButton')
        self.horizontalLayout_2.addWidget(self.DvdRadioButton)
        self.AudioCdRadioButton = QtGui.QRadioButton(self.MediaTypeWidget)
        self.AudioCdRadioButton.setObjectName(u'AudioCdRadioButton')
        self.horizontalLayout_2.addWidget(self.AudioCdRadioButton)
        self.verticalLayout_8.addWidget(self.MediaTypeWidget)
        self.DeviceWidget = QtGui.QWidget(self.ChooseMediaGroupBox)
        self.DeviceWidget.setObjectName(u'DeviceWidget')
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.DeviceWidget)
        self.horizontalLayout_10.setMargin(0)
        self.horizontalLayout_10.setObjectName(u'horizontalLayout_10')
        self.DeviceLabel = QtGui.QLabel(self.DeviceWidget)
        self.DeviceLabel.setObjectName(u'DeviceLabel')
        self.horizontalLayout_10.addWidget(self.DeviceLabel)
        self.DeviceComboBox = QtGui.QComboBox(self.DeviceWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth( \
            self.DeviceComboBox.sizePolicy().hasHeightForWidth())
        self.DeviceComboBox.setSizePolicy(sizePolicy)
        self.DeviceComboBox.setObjectName(u'DeviceComboBox')
        self.horizontalLayout_10.addWidget(self.DeviceComboBox)
        self.DeviceEject = QtGui.QPushButton(self.DeviceWidget)
        sizePolicy = QtGui.QSizePolicy( \
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth( \
            self.DeviceEject.sizePolicy().hasHeightForWidth())
        self.DeviceEject.setSizePolicy(sizePolicy)
        self.DeviceEject.setObjectName(u'DeviceEject')
        self.horizontalLayout_10.addWidget(self.DeviceEject)
        self.DeviceSearchButton = QtGui.QPushButton(self.DeviceWidget)
        self.DeviceSearchButton.setObjectName(u'DeviceSearchButton')
        self.horizontalLayout_10.addWidget(self.DeviceSearchButton)
        self.verticalLayout_8.addWidget(self.DeviceWidget)
        self.verticalLayout_3.addWidget(self.ChooseMediaGroupBox)
        self.StartpositionGroupBox = QtGui.QGroupBox(self.MediaTab)
        self.StartpositionGroupBox.setObjectName(u'StartpositionGroupBox')
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.StartpositionGroupBox)
        self.horizontalLayout_4.setObjectName(u'horizontalLayout_4')
        self.TitleWidget = QtGui.QWidget(self.StartpositionGroupBox)
        self.TitleWidget.setObjectName(u'TitleWidget')
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.TitleWidget)
        self.horizontalLayout_7.setMargin(0)
        self.horizontalLayout_7.setObjectName(u'horizontalLayout_7')
        self.TitleLabel = QtGui.QLabel(self.TitleWidget)
        sizePolicy = QtGui.QSizePolicy( \
            QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth( \
            self.TitleLabel.sizePolicy().hasHeightForWidth())
        self.TitleLabel.setSizePolicy(sizePolicy)
        self.TitleLabel.setObjectName(u'TitleLabel')
        self.horizontalLayout_7.addWidget(self.TitleLabel)
        self.horizontalLayout_4.addWidget(self.TitleWidget)
        self.ChapterWidget = QtGui.QWidget(self.StartpositionGroupBox)
        self.ChapterWidget.setEnabled(True)
        self.ChapterWidget.setObjectName(u'ChapterWidget')
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.ChapterWidget)
        self.horizontalLayout_6.setMargin(0)
        self.horizontalLayout_6.setObjectName(u'horizontalLayout_6')
        self.ChapterLabel = QtGui.QLabel(self.ChapterWidget)
        sizePolicy = QtGui.QSizePolicy( \
            QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth( \
            self.ChapterLabel.sizePolicy().hasHeightForWidth())
        self.ChapterLabel.setSizePolicy(sizePolicy)
        self.ChapterLabel.setObjectName(u'ChapterLabel')
        self.horizontalLayout_6.addWidget(self.ChapterLabel)
        self.ChapterSpinBox = QtGui.QSpinBox(self.ChapterWidget)
        self.ChapterSpinBox.setObjectName(u'ChapterSpinBox')
        self.horizontalLayout_6.addWidget(self.ChapterSpinBox)
        self.horizontalLayout_4.addWidget(self.ChapterWidget)
        self.verticalLayout_3.addWidget(self.StartpositionGroupBox)
        self.AudioSubtitleGroupBox = QtGui.QGroupBox(self.MediaTab)
        self.AudioSubtitleGroupBox.setObjectName(u'AudioSubtitleGroupBox')
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.AudioSubtitleGroupBox)
        self.horizontalLayout_5.setObjectName(u'horizontalLayout_5')
        self.AudioTrackWidget = QtGui.QWidget(self.AudioSubtitleGroupBox)
        self.AudioTrackWidget.setObjectName(u'AudioTrackWidget')
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.AudioTrackWidget)
        self.horizontalLayout_9.setMargin(0)
        self.horizontalLayout_9.setObjectName(u'horizontalLayout_9')
        self.AudioTrackLabel_2 = QtGui.QLabel(self.AudioTrackWidget)
        sizePolicy = QtGui.QSizePolicy( \
            QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth( \
            self.AudioTrackLabel_2.sizePolicy().hasHeightForWidth())
        self.AudioTrackLabel_2.setSizePolicy(sizePolicy)
        self.AudioTrackLabel_2.setObjectName(u'AudioTrackLabel_2')
        self.horizontalLayout_9.addWidget(self.AudioTrackLabel_2)
        self.TitleSpinBox = QtGui.QSpinBox(self.AudioTrackWidget)
        self.TitleSpinBox.setObjectName(u'TitleSpinBox')
        self.horizontalLayout_9.addWidget(self.TitleSpinBox)
        self.horizontalLayout_5.addWidget(self.AudioTrackWidget)
        self.SubtitleTrackWidget = QtGui.QWidget(self.AudioSubtitleGroupBox)
        self.SubtitleTrackWidget.setObjectName(u'SubtitleTrackWidget')
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.SubtitleTrackWidget)
        self.horizontalLayout_8.setMargin(0)
        self.horizontalLayout_8.setObjectName(u'horizontalLayout_8')
        self.SubtitleTrackLabel = QtGui.QLabel(self.SubtitleTrackWidget)
        sizePolicy = QtGui.QSizePolicy( \
            QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth( \
            self.SubtitleTrackLabel.sizePolicy().hasHeightForWidth())
        self.SubtitleTrackLabel.setSizePolicy(sizePolicy)
        self.SubtitleTrackLabel.setObjectName(u'SubtitleTrackLabel')
        self.horizontalLayout_8.addWidget(self.SubtitleTrackLabel)
        self.SubtitleTrackSpinBox = QtGui.QSpinBox(self.SubtitleTrackWidget)
        self.SubtitleTrackSpinBox.setObjectName(u'SubtitleTrackSpinBox')
        self.horizontalLayout_8.addWidget(self.SubtitleTrackSpinBox)
        self.horizontalLayout_5.addWidget(self.SubtitleTrackWidget)
        self.verticalLayout_3.addWidget(self.AudioSubtitleGroupBox)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, \
            QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.MediaOpenWidget.addTab(self.MediaTab, u'')
        self.NetworkTab = QtGui.QWidget()
        self.NetworkTab.setObjectName(u'NetworkTab')
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.NetworkTab)
        self.verticalLayout_4.setObjectName(u'verticalLayout_4')
        self.NetworkprotocolGroupBox = QtGui.QGroupBox(self.NetworkTab)
        self.NetworkprotocolGroupBox.setObjectName(u'NetworkprotocolGroupBox')
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.NetworkprotocolGroupBox)
        self.verticalLayout_5.setObjectName(u'verticalLayout_5')
        self.NetworkAdressLabel = QtGui.QLabel(self.NetworkprotocolGroupBox)
        self.NetworkAdressLabel.setObjectName(u'NetworkAdressLabel')
        self.verticalLayout_5.addWidget(self.NetworkAdressLabel)
        self.NetworkAdressEdit = QtGui.QLineEdit(self.NetworkprotocolGroupBox)
        self.NetworkAdressEdit.setObjectName(u'NetworkAdressEdit')
        self.verticalLayout_5.addWidget(self.NetworkAdressEdit)
        spacerItem3 = QtGui.QSpacerItem(20, 259, QtGui.QSizePolicy.Minimum, \
            QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.verticalLayout_4.addWidget(self.NetworkprotocolGroupBox)
        self.MediaOpenWidget.addTab(self.NetworkTab, u'')
        self.verticalLayout.addWidget(self.MediaOpenWidget)
        self.ButtonBox = QtGui.QDialogButtonBox(mediaOpenDialog)
        self.ButtonBox.setStandardButtons( \
            QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.ButtonBox.setObjectName(u'ButtonBox')
        self.verticalLayout.addWidget(self.ButtonBox)

        self.retranslateUi(mediaOpenDialog)
        self.MediaOpenWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mediaOpenDialog)

    def retranslateUi(self, mediaOpenDialog):
        mediaOpenDialog.setWindowTitle(
            translate('MediaPlugin', 'mediaOpenForm'))
        self.FileSelectionGroupBox.setTitle(translate(
            'MediaPlugin', 'File Selection'))
        self.ChooseFilesLabel.setText(
            translate('MediaPlugin', 'Choose Files with the Buttons right.'))
        self.FileAddButton.setText(
            translate('MediaPlugin', 'Add ...'))
        self.FileRemoveButton.setText(
            translate('MediaPlugin', 'Remove'))
        self.MediaOpenWidget.setTabText(
            self.MediaOpenWidget.indexOf(self.FileTab),
            translate('MediaPlugin', 'File(s)'))
        self.ChooseMediaGroupBox.setTitle(
            translate('MediaPlugin', 'Choose Media'))
        self.DvdRadioButton.setText(
            translate('MediaPlugin', 'DVD'))
        self.AudioCdRadioButton.setText(
            translate('MediaPlugin', 'Audio-CD'))
        self.DeviceLabel.setText(
            translate('MediaPlugin', 'Device'))
        self.DeviceEject.setText(
            translate('MediaPlugin', 'Eject'))
        self.DeviceSearchButton.setText(
            translate('MediaPlugin', 'Search ...'))
        self.StartpositionGroupBox.setTitle(
            translate('MediaPlugin', 'Startposition'))
        self.TitleLabel.setText(
            translate('MediaPlugin', 'Title'))
        self.ChapterLabel.setText(
            translate('MediaPlugin', 'Chapter'))
        self.AudioSubtitleGroupBox.setTitle(
            translate('MediaPlugin', 'Audio and Subtitle'))
        self.AudioTrackLabel_2.setText(
            translate('MediaPlugin', 'Audiotrack'))
        self.SubtitleTrackLabel.setText(
            translate('MediaPlugin', 'Subtitletrack'))
        self.MediaOpenWidget.setTabText(
            self.MediaOpenWidget.indexOf(self.MediaTab),
            translate('MediaPlugin', 'Location'))
        self.NetworkprotocolGroupBox.setTitle(
            translate('MediaPlugin', 'Networkprotocol'))
        self.NetworkAdressLabel.setText(
            translate('MediaPlugin', 'Network adress:'))
        self.MediaOpenWidget.setTabText(
            self.MediaOpenWidget.indexOf(self.NetworkTab),
            translate('MediaPlugin', 'Network'))

