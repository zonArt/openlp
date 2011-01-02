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
"""
The :mod:`advancedtab` provides an advanced settings facility.
"""
from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab, translate

class AdvancedTab(SettingsTab):
    """
    The :class:`AdvancedTab` manages the advanced settings tab including the UI
    and the loading and saving of the displayed settings.
    """
    def __init__(self):
        """
        Initialise the settings tab
        """
        SettingsTab.__init__(self, u'Advanced')

    def setupUi(self):
        """
        Configure the UI elements for the tab.
        """
        self.setObjectName(u'AdvancedTab')
        self.tabTitleVisible = translate('OpenLP.AdvancedTab', 'Advanced')
        self.advancedTabLayout = QtGui.QHBoxLayout(self)
        self.advancedTabLayout.setSpacing(8)
        self.advancedTabLayout.setMargin(8)
        self.leftWidget = QtGui.QWidget(self)
        self.leftLayout = QtGui.QVBoxLayout(self.leftWidget)
        self.leftLayout.setSpacing(8)
        self.leftLayout.setMargin(0)
        self.uiGroupBox = QtGui.QGroupBox(self.leftWidget)
        self.uiGroupBox.setObjectName(u'uiGroupBox')
        self.uiLayout = QtGui.QVBoxLayout(self.uiGroupBox)
        self.uiLayout.setSpacing(8)
        self.uiLayout.setMargin(6)
        self.uiLayout.setObjectName(u'uiLayout')
        self.recentLayout = QtGui.QHBoxLayout()
        self.recentLayout.setSpacing(8)
        self.recentLayout.setMargin(0)
        self.recentLayout.setObjectName(u'recentLayout')
        self.recentLabel = QtGui.QLabel(self.uiGroupBox)
        self.recentLabel.setObjectName(u'recentLabel')
        self.recentLayout.addWidget(self.recentLabel)
        self.recentSpinBox = QtGui.QSpinBox(self.uiGroupBox)
        self.recentSpinBox.setObjectName(u'recentSpinBox')
        self.recentSpinBox.setMinimum(0)
        self.recentLayout.addWidget(self.recentSpinBox)
        self.recentSpacer = QtGui.QSpacerItem(50, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.recentLayout.addItem(self.recentSpacer)
        self.uiLayout.addLayout(self.recentLayout)
        self.mediaPluginCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.mediaPluginCheckBox.setObjectName(u'mediaPluginCheckBox')
        self.uiLayout.addWidget(self.mediaPluginCheckBox)
        self.doubleClickLiveCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.doubleClickLiveCheckBox.setObjectName(u'doubleClickLiveCheckBox')
        self.uiLayout.addWidget(self.doubleClickLiveCheckBox)
#        self.expandServiceItemCheckBox = QtGui.QCheckBox(self.uiGroupBox)
#        self.expandServiceItemCheckBox.setObjectName(
#            u'expandServiceItemCheckBox')
#        self.uiLayout.addWidget(self.expandServiceItemCheckBox)
        self.leftLayout.addWidget(self.uiGroupBox)
        self.expandServiceItemCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.expandServiceItemCheckBox.setObjectName(
            u'expandServiceItemCheckBox')
        self.uiLayout.addWidget(self.expandServiceItemCheckBox)
        self.enableAutoCloseCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.enableAutoCloseCheckBox.setObjectName(
            u'enableAutoCloseCheckBox')
        self.uiLayout.addWidget(self.enableAutoCloseCheckBox)
#        self.sharedDirGroupBox = QtGui.QGroupBox(self.leftWidget)
#        self.sharedDirGroupBox.setObjectName(u'sharedDirGroupBox')
#        self.sharedDirGroupBox.setGeometry(QtCore.QRect(0, 65, 500, 85))
#        self.sharedDirGroupBox.setMaximumSize(QtCore.QSize(500, 85))
#        self.sharedDirLayout = QtGui.QVBoxLayout(self.sharedDirGroupBox)
#        self.sharedDirLayout.setSpacing(8)
#        self.sharedDirLayout.setMargin(8)
#        self.sharedCheckBox = QtGui.QCheckBox(self.sharedDirGroupBox)
#        self.sharedCheckBox.setObjectName(u'sharedCheckBox')
#        self.sharedDirLayout.addWidget(self.sharedCheckBox)
#        self.sharedSubLayout = QtGui.QHBoxLayout()
#        self.sharedSubLayout.setSpacing(8)
#        self.sharedSubLayout.setMargin(0)
#        self.sharedLabel = QtGui.QLabel(self.sharedDirGroupBox)
#        self.sharedLabel.setObjectName(u'sharedLabel')
#        self.sharedSubLayout.addWidget(self.sharedLabel)
#        self.sharedLineEdit = QtGui.QLineEdit(self.sharedDirGroupBox)
#        self.sharedLineEdit.setObjectName(u'sharedLineEdit')
#        self.sharedSubLayout.addWidget(self.sharedLineEdit)
#        self.sharedPushButton = QtGui.QPushButton(self.sharedDirGroupBox)
#        self.sharedPushButton.setObjectName(u'sharedPushButton')
#        self.sharedSubLayout.addWidget(self.sharedPushButton)
#        self.sharedDirLayout.addLayout(self.sharedSubLayout)
#        self.leftLayout.addWidget(self.sharedDirGroupBox)
        self.leftSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.leftLayout.addItem(self.leftSpacer)
        self.advancedTabLayout.addWidget(self.leftWidget)
        self.rightWidget = QtGui.QWidget(self)
        self.rightLayout = QtGui.QVBoxLayout(self.rightWidget)
        self.rightLayout.setSpacing(8)
        self.rightLayout.setMargin(0)
#        self.databaseGroupBox = QtGui.QGroupBox(self.rightWidget)
#        self.databaseGroupBox.setObjectName(u'databaseGroupBox')
#        self.databaseGroupBox.setEnabled(False)
#        self.databaseLayout = QtGui.QVBoxLayout(self.databaseGroupBox)
#        self.databaseLayout.setSpacing(8)
#        self.databaseLayout.setMargin(8)
#        self.rightLayout.addWidget(self.databaseGroupBox)
        self.rightSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.rightLayout.addItem(self.rightSpacer)
        self.advancedTabLayout.addWidget(self.rightWidget)
#        QtCore.QObject.connect(self.sharedCheckBox,
#            QtCore.SIGNAL(u'stateChanged(int)'), self.onSharedCheckBoxChanged)

    def retranslateUi(self):
        """
        Setup the interface translation strings.
        """
        self.uiGroupBox.setTitle(translate('OpenLP.AdvancedTab', 'UI Settings'))
        self.recentLabel.setText(
            translate('OpenLP.AdvancedTab',
                'Number of recent files to display:'))
        self.mediaPluginCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Remember active media manager tab on startup'))
        self.doubleClickLiveCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Double-click to send items straight to live'))
        self.expandServiceItemCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Expand new service items on creation'))
        self.enableAutoCloseCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Enable confirm on closure'))
#        self.sharedDirGroupBox.setTitle(
#            translate('AdvancedTab', 'Central Data Store'))
#        self.sharedCheckBox.setText(
#            translate('AdvancedTab', 'Enable a shared data location'))
#        self.sharedLabel.setText(translate('AdvancedTab', 'Store location:'))
#        self.sharedPushButton.setText(translate('AdvancedTab', 'Browse...'))
#        self.databaseGroupBox.setTitle(translate('AdvancedTab', 'Databases'))

    def load(self):
        """
        Load settings from disk.
        """
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        # The max recent files value does not have an interface and so never
        # gets actually stored in the settings therefore the default value of
        # 20 will always be used.
        self.recentSpinBox.setMaximum(QtCore.QSettings().value(
            u'max recent files', QtCore.QVariant(20)).toInt()[0])
        self.recentSpinBox.setValue(settings.value(u'recent file count',
            QtCore.QVariant(4)).toInt()[0])
        self.mediaPluginCheckBox.setChecked(
            settings.value(u'save current plugin',
            QtCore.QVariant(False)).toBool())
        self.doubleClickLiveCheckBox.setChecked(
            settings.value(u'double click live',
            QtCore.QVariant(False)).toBool())
        self.expandServiceItemCheckBox.setChecked(
            settings.value(u'expand service item',
            QtCore.QVariant(False)).toBool())
        self.enableAutoCloseCheckBox.setChecked(
            settings.value(u'enable auto close',
            QtCore.QVariant(True)).toBool())
        settings.endGroup()

    def save(self):
        """
        Save settings to disk.
        """
        settings = QtCore.QSettings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'recent file count',
            QtCore.QVariant(self.recentSpinBox.value()))
        settings.setValue(u'save current plugin',
            QtCore.QVariant(self.mediaPluginCheckBox.isChecked()))
        settings.setValue(u'double click live',
            QtCore.QVariant(self.doubleClickLiveCheckBox.isChecked()))
        settings.setValue(u'expand service item',
            QtCore.QVariant(self.expandServiceItemCheckBox.isChecked()))
        settings.setValue(u'enable auto close',
            QtCore.QVariant(self.enableAutoCloseCheckBox.isChecked()))
        settings.endGroup()

#    def onSharedCheckBoxChanged(self, checked):
#        """
#        Enables the widgets to allow a shared data location
#        """
#        self.sharedLabel.setEnabled(checked)
#        self.sharedTextEdit.setEnabled(checked)
#        self.sharedPushButton.setEnabled(checked)
