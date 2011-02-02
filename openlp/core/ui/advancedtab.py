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
        SettingsTab.setupUi(self)
        self.uiGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.uiGroupBox.setObjectName(u'uiGroupBox')
        self.uiLayout = QtGui.QFormLayout(self.uiGroupBox)
        self.uiLayout.setObjectName(u'uiLayout')
        self.recentLabel = QtGui.QLabel(self.uiGroupBox)
        self.recentLabel.setObjectName(u'recentLabel')
        self.recentSpinBox = QtGui.QSpinBox(self.uiGroupBox)
        self.recentSpinBox.setObjectName(u'recentSpinBox')
        self.recentSpinBox.setMinimum(0)
        self.uiLayout.addRow(self.recentLabel, self.recentSpinBox)
        self.mediaPluginCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.mediaPluginCheckBox.setObjectName(u'mediaPluginCheckBox')
        self.uiLayout.addRow(self.mediaPluginCheckBox)
        self.doubleClickLiveCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.doubleClickLiveCheckBox.setObjectName(u'doubleClickLiveCheckBox')
        self.uiLayout.addRow(self.doubleClickLiveCheckBox)
        self.expandServiceItemCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.expandServiceItemCheckBox.setObjectName(
            u'expandServiceItemCheckBox')
        self.uiLayout.addRow(self.expandServiceItemCheckBox)
        self.enableAutoCloseCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.enableAutoCloseCheckBox.setObjectName(
            u'enableAutoCloseCheckBox')
        self.uiLayout.addRow(self.enableAutoCloseCheckBox)
        self.leftLayout.addWidget(self.uiGroupBox)
        self.hideMouseGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.hideMouseGroupBox.setObjectName(u'hideMouseGroupBox')
        self.hideMouseLayout = QtGui.QVBoxLayout(self.hideMouseGroupBox)
        self.hideMouseLayout.setObjectName(u'hideMouseLayout')
        self.hideMouseCheckBox = QtGui.QCheckBox(self.hideMouseGroupBox)
        self.hideMouseCheckBox.setObjectName(u'hideMouseCheckBox')
        self.hideMouseLayout.addWidget(self.hideMouseCheckBox)
        self.leftLayout.addWidget(self.hideMouseGroupBox)
        self.serviceOrderGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.serviceOrderGroupBox.setObjectName(u'serviceOrderGroupBox')
        self.serviceOrderLayout = QtGui.QVBoxLayout(self.serviceOrderGroupBox)
        self.serviceOrderLayout.setObjectName(u'serviceOrderLayout')
        self.detailedServicePrintCheckBox = QtGui.QCheckBox(
            self.serviceOrderGroupBox)
        self.detailedServicePrintCheckBox.setObjectName(
            u'detailedServicePrintCheckBox')
        self.serviceOrderLayout.addWidget(self.detailedServicePrintCheckBox)
        self.leftLayout.addWidget(self.serviceOrderGroupBox)
#        self.sharedDirGroupBox = QtGui.QGroupBox(self.leftColumn)
#        self.sharedDirGroupBox.setObjectName(u'sharedDirGroupBox')
#        self.sharedDirLayout = QtGui.QFormLayout(self.sharedDirGroupBox)
#        self.sharedCheckBox = QtGui.QCheckBox(self.sharedDirGroupBox)
#        self.sharedCheckBox.setObjectName(u'sharedCheckBox')
#        self.sharedDirLayout.addRow(self.sharedCheckBox)
#        self.sharedLabel = QtGui.QLabel(self.sharedDirGroupBox)
#        self.sharedLabel.setObjectName(u'sharedLabel')
#        self.sharedSubLayout = QtGui.QHBoxLayout()
#        self.sharedSubLayout.setObjectName(u'sharedSubLayout')
#        self.sharedLineEdit = QtGui.QLineEdit(self.sharedDirGroupBox)
#        self.sharedLineEdit.setObjectName(u'sharedLineEdit')
#        self.sharedSubLayout.addWidget(self.sharedLineEdit)
#        self.sharedPushButton = QtGui.QPushButton(self.sharedDirGroupBox)
#        self.sharedPushButton.setObjectName(u'sharedPushButton')
#        self.sharedSubLayout.addWidget(self.sharedPushButton)
#        self.sharedDirLayout.addRow(self.sharedLabel, self.sharedSubLayout)
#        self.leftLayout.addWidget(self.sharedDirGroupBox)
        self.leftLayout.addStretch()
#        self.databaseGroupBox = QtGui.QGroupBox(self.rightColumn)
#        self.databaseGroupBox.setObjectName(u'databaseGroupBox')
#        self.databaseGroupBox.setEnabled(False)
#        self.databaseLayout = QtGui.QVBoxLayout(self.databaseGroupBox)
#        self.rightLayout.addWidget(self.databaseGroupBox)
        self.rightLayout.addStretch()
#        QtCore.QObject.connect(self.sharedCheckBox,
#            QtCore.SIGNAL(u'stateChanged(int)'), self.onSharedCheckBoxChanged)

    def retranslateUi(self):
        """
        Setup the interface translation strings.
        """
        self.tabTitleVisible = translate('OpenLP.AdvancedTab', 'Advanced')
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
            'Enable application exit confirmation'))
        self.hideMouseGroupBox.setTitle(translate('OpenLP.AdvancedTab',
            'Mouse Cursor'))
        self.hideMouseCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Hide the mouse cursor when moved over the display window'))
        self.serviceOrderGroupBox.setTitle(translate('OpenLP.AdvancedTab',
            'Service Order Print'))
        self.detailedServicePrintCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Print slide texts and service item notes as well'))
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
            settings.value(u'enable exit confirmation',
            QtCore.QVariant(True)).toBool())
        self.hideMouseCheckBox.setChecked(
            settings.value(u'hide mouse', QtCore.QVariant(False)).toBool())
        self.detailedServicePrintCheckBox.setChecked(settings.value(
            u'detailed service print', QtCore.QVariant(False)).toBool())
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
        settings.setValue(u'enable exit confirmation',
            QtCore.QVariant(self.enableAutoCloseCheckBox.isChecked()))
        settings.setValue(u'hide mouse',
            QtCore.QVariant(self.hideMouseCheckBox.isChecked()))
        settings.setValue(u'detailed service print',
            QtCore.QVariant(self.detailedServicePrintCheckBox.isChecked()))
        settings.endGroup()

#    def onSharedCheckBoxChanged(self, checked):
#        """
#        Enables the widgets to allow a shared data location
#        """
#        self.sharedLabel.setEnabled(checked)
#        self.sharedTextEdit.setEnabled(checked)
#        self.sharedPushButton.setEnabled(checked)
