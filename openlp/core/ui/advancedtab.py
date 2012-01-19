# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
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
"""
The :mod:`advancedtab` provides an advanced settings facility.
"""
from PyQt4 import QtCore, QtGui

import os
import sys
from openlp.core.lib import SettingsTab, translate, build_icon,  Receiver
from openlp.core.lib.ui import UiStrings
from openlp.core.utils import get_images_filter, AppLocation

class AdvancedTab(SettingsTab):
    """
    The :class:`AdvancedTab` manages the advanced settings tab including the UI
    and the loading and saving of the displayed settings.
    """
    def __init__(self, parent):
        """
        Initialise the settings tab
        """
        self.display_changed = False
        advancedTranslated = translate('OpenLP.AdvancedTab', 'Advanced')
        self.default_image = u':/graphics/openlp-splash-screen.png'
        self.default_color = u'#ffffff'
        self.icon_path = u':/system/system_settings.png'
        SettingsTab.__init__(self, parent, u'Advanced', advancedTranslated)

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
        self.singleClickPreviewCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.singleClickPreviewCheckBox.setObjectName(
            u'singleClickPreviewCheckBox')
        self.uiLayout.addRow(self.singleClickPreviewCheckBox)
        self.expandServiceItemCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.expandServiceItemCheckBox.setObjectName(
            u'expandServiceItemCheckBox')
        self.uiLayout.addRow(self.expandServiceItemCheckBox)
        self.enableAutoCloseCheckBox = QtGui.QCheckBox(self.uiGroupBox)
        self.enableAutoCloseCheckBox.setObjectName(
            u'enableAutoCloseCheckBox')
        self.uiLayout.addRow(self.enableAutoCloseCheckBox)
        self.leftLayout.addWidget(self.uiGroupBox)
        self.dataDirectoryGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.dataDirectoryGroupBox.setObjectName(u'dataDirectoryGroupBox')
        self.dataDirectoryLabel= QtGui.QLabel(self.dataDirectoryGroupBox)
        self.dataDirectoryLabel.setObjectName(u'dataDirectoryLabel')
        self.newDataDirectoryEdit = QtGui.QLineEdit(self.dataDirectoryGroupBox)
        self.newDataDirectoryEdit.setObjectName(u'newDataDirectoryEdit')
        self.newDataDirectoryEdit.setReadOnly(True)
        self.newDataDirectoryHasFilesLabel= QtGui.QLabel(self.dataDirectoryGroupBox)
        self.newDataDirectoryHasFilesLabel.setObjectName(
            u'newDataDirectoryHasFilesLabel')
        self.newDataDirectoryHasFilesLabel.setWordWrap(True)
        self.dataDirectoryBrowseButton = QtGui.QPushButton(
            self.dataDirectoryGroupBox)
        self.dataDirectoryBrowseButton.setObjectName(
            u'dataDirectoryBrowseButton')
        self.dataDirectoryBrowseButton.setIcon(
            build_icon(u':/general/general_open.png'))
        self.dataDirectoryDefaultButton = QtGui.QPushButton(
            self.dataDirectoryGroupBox)
        self.dataDirectoryDefaultButton.setObjectName(
            u'dataDirectoryBrowseButton')
        self.dataDirectoryDefaultButton.setIcon(
            build_icon(u':/general/general_revert.png'))
        self.dataDirectoryCancelButton = QtGui.QPushButton(
            self.dataDirectoryGroupBox)
        self.dataDirectoryCancelButton.setObjectName(
            u'dataDirectoryCancelButton')
        self.dataDirectoryCancelButton.setIcon(
            build_icon(u':/general/general_revert.png'))
        self.dataDirectoryCopyCheckBox = QtGui.QCheckBox(
            self.dataDirectoryGroupBox)
        self.dataDirectoryCopyCheckBox.setObjectName(
            u'dataDirectoryCopyCheckBox')
        self.dataDirectoryCopyCheckBox.hide()
        self.newDataDirectoryHasFilesLabel.hide()
        self.dataDirectoryDefaultButton.hide()
        self.dataDirectoryCancelButton.hide()
        self.dataDirectoryLayout =QtGui.QFormLayout(self.dataDirectoryGroupBox)
        self.dataDirectoryLayout.setObjectName(u'dataDirectoryLayout')
        self.dataDirectoryLayout.addWidget(self.dataDirectoryLabel)
        self.dataDirectoryLayout.addWidget(self.dataDirectoryBrowseButton)
        self.dataDirectoryLayout.addWidget(self.newDataDirectoryEdit)
        self.dataDirectoryLayout.addWidget(self.dataDirectoryCopyCheckBox)
        self.dataDirectoryLayout.addWidget(self.newDataDirectoryHasFilesLabel)
        self.dataDirectoryLayout.addWidget(self.dataDirectoryDefaultButton)
        self.dataDirectoryLayout.addWidget(self.dataDirectoryCancelButton)
        self.leftLayout.addWidget(self.dataDirectoryGroupBox)
        self.leftLayout.addStretch()
        self.defaultImageGroupBox = QtGui.QGroupBox(self.rightColumn)
        self.defaultImageGroupBox.setObjectName(u'defaultImageGroupBox')
        self.defaultImageLayout = QtGui.QFormLayout(self.defaultImageGroupBox)
        self.defaultImageLayout.setObjectName(u'defaultImageLayout')
        self.defaultColorLabel = QtGui.QLabel(self.defaultImageGroupBox)
        self.defaultColorLabel.setObjectName(u'defaultColorLabel')
        self.defaultColorButton = QtGui.QPushButton(self.defaultImageGroupBox)
        self.defaultColorButton.setObjectName(u'defaultColorButton')
        self.defaultImageLayout.addRow(self.defaultColorLabel,
            self.defaultColorButton)
        self.defaultFileLabel = QtGui.QLabel(self.defaultImageGroupBox)
        self.defaultFileLabel.setObjectName(u'defaultFileLabel')
        self.defaultFileEdit = QtGui.QLineEdit(self.defaultImageGroupBox)
        self.defaultFileEdit.setObjectName(u'defaultFileEdit')
        self.defaultBrowseButton = QtGui.QToolButton(self.defaultImageGroupBox)
        self.defaultBrowseButton.setObjectName(u'defaultBrowseButton')
        self.defaultBrowseButton.setIcon(
            build_icon(u':/general/general_open.png'))
        self.defaultRevertButton = QtGui.QToolButton(self.defaultImageGroupBox)
        self.defaultRevertButton.setObjectName(u'defaultRevertButton')
        self.defaultRevertButton.setIcon(
            build_icon(u':/general/general_revert.png'))
        self.defaultFileLayout = QtGui.QHBoxLayout()
        self.defaultFileLayout.setObjectName(u'defaultFileLayout')
        self.defaultFileLayout.addWidget(self.defaultFileEdit)
        self.defaultFileLayout.addWidget(self.defaultBrowseButton)
        self.defaultFileLayout.addWidget(self.defaultRevertButton)
        self.defaultImageLayout.addRow(self.defaultFileLabel,
            self.defaultFileLayout)
        self.rightLayout.addWidget(self.defaultImageGroupBox)
        self.hideMouseGroupBox = QtGui.QGroupBox(self.leftColumn)
        self.hideMouseGroupBox.setObjectName(u'hideMouseGroupBox')
        self.hideMouseLayout = QtGui.QVBoxLayout(self.hideMouseGroupBox)
        self.hideMouseLayout.setObjectName(u'hideMouseLayout')
        self.hideMouseCheckBox = QtGui.QCheckBox(self.hideMouseGroupBox)
        self.hideMouseCheckBox.setObjectName(u'hideMouseCheckBox')
        self.hideMouseLayout.addWidget(self.hideMouseCheckBox)
        self.rightLayout.addWidget(self.hideMouseGroupBox)
        self.x11GroupBox = QtGui.QGroupBox(self.leftColumn)
        self.x11GroupBox.setObjectName(u'x11GroupBox')
        self.x11Layout = QtGui.QVBoxLayout(self.x11GroupBox)
        self.x11Layout.setObjectName(u'x11Layout')
        self.x11BypassCheckBox = QtGui.QCheckBox(self.x11GroupBox)
        self.x11BypassCheckBox.setObjectName(u'x11BypassCheckBox')
        self.x11Layout.addWidget(self.x11BypassCheckBox)
        self.rightLayout.addWidget(self.x11GroupBox)
        self.rightLayout.addStretch()

        QtCore.QObject.connect(self.defaultColorButton,
            QtCore.SIGNAL(u'pressed()'), self.onDefaultColorButtonPressed)
        QtCore.QObject.connect(self.defaultBrowseButton,
            QtCore.SIGNAL(u'pressed()'), self.onDefaultBrowseButtonPressed)
        QtCore.QObject.connect(self.defaultRevertButton,
            QtCore.SIGNAL(u'pressed()'), self.onDefaultRevertButtonPressed)
        QtCore.QObject.connect(self.x11BypassCheckBox,
            QtCore.SIGNAL(u'toggled(bool)'), self.onX11BypassCheckBoxToggled)
        QtCore.QObject.connect(self.dataDirectoryBrowseButton,
            QtCore.SIGNAL(u'pressed()'),
            self.onDataDirectoryBrowseButtonPressed)
        QtCore.QObject.connect(self.dataDirectoryDefaultButton,
            QtCore.SIGNAL(u'pressed()'),
            self.onDataDirectoryDefaultButtonPressed)
        QtCore.QObject.connect(self.dataDirectoryCancelButton,
            QtCore.SIGNAL(u'pressed()'),
            self.onDataDirectoryCancelButtonPressed)

    def retranslateUi(self):
        """
        Setup the interface translation strings.
        """
        self.tabTitleVisible = UiStrings().Advanced
        self.uiGroupBox.setTitle(
            translate('OpenLP.AdvancedTab', 'UI Settings'))
        self.dataDirectoryGroupBox.setTitle(
            translate('OpenLP.AdvancedTab', 'Data Location'))
        self.recentLabel.setText(
            translate('OpenLP.AdvancedTab',
                'Number of recent files to display:'))
        self.mediaPluginCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Remember active media manager tab on startup'))
        self.doubleClickLiveCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Double-click to send items straight to live'))
        self.singleClickPreviewCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Preview items when clicked in Media Manager'))
        self.expandServiceItemCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Expand new service items on creation'))
        self.enableAutoCloseCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Enable application exit confirmation'))
        self.hideMouseGroupBox.setTitle(translate('OpenLP.AdvancedTab',
            'Mouse Cursor'))
        self.hideMouseCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Hide mouse cursor when over display window'))
        self.defaultImageGroupBox.setTitle(translate('OpenLP.AdvancedTab',
            'Default Image'))
        self.defaultColorLabel.setText(translate('OpenLP.AdvancedTab',
            'Background color:'))
        self.defaultColorButton.setToolTip(translate('OpenLP.AdvancedTab',
            'Click to select a color.'))
        self.defaultFileLabel.setText(translate('OpenLP.AdvancedTab',
            'Image file:'))
        self.defaultBrowseButton.setToolTip(translate('OpenLP.AdvancedTab',
            'Browse for an image file to display.'))
        self.defaultRevertButton.setToolTip(translate('OpenLP.AdvancedTab',
            'Revert to the default OpenLP logo.'))
        self.dataDirectoryBrowseButton.setText(translate('OpenLP.AdvancedTab',
            'Select new location.'))
        self.dataDirectoryBrowseButton.setToolTip(
            translate('OpenLP.AdvancedTab',
            'Browse for new data file location.'))
        self.dataDirectoryDefaultButton.setText(
            translate('OpenLP.AdvancedTab',
            'Set to default location.'))
        self.dataDirectoryDefaultButton.setToolTip(
            translate('OpenLP.AdvancedTab',
            'Set the data location to the default.'))
        self.dataDirectoryCancelButton.setText(
            translate('OpenLP.AdvancedTab',
            'Cancel data directory change'))
        self.dataDirectoryCancelButton.setToolTip(
            translate('OpenLP.AdvancedTab',
            'Cancel OpenLP data directory location change.'))
        self.dataDirectoryCopyCheckBox.setText(
            translate('OpenLP.AdvancedTab',
            'Copy data to new location.'))
        self.dataDirectoryCopyCheckBox.setToolTip(
            translate('OpenLP.AdvancedTab',
            'Copy the OpenLP data files to the new location.'))
        self.newDataDirectoryHasFilesLabel.setText(
            translate('OpenLP.AdvancedTab',
            'Warning - New data directory location contains OpenLP '
            'data files.  These files WILL be replaced during a copy.'))
        self.x11GroupBox.setTitle(translate('OpenLP.AdvancedTab',
            'X11'))
        self.x11BypassCheckBox.setText(translate('OpenLP.AdvancedTab',
            'Bypass X11 Window Manager'))

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
        self.singleClickPreviewCheckBox.setChecked(
            settings.value(u'single click preview',
            QtCore.QVariant(False)).toBool())
        self.expandServiceItemCheckBox.setChecked(
            settings.value(u'expand service item',
            QtCore.QVariant(False)).toBool())
        self.enableAutoCloseCheckBox.setChecked(
            settings.value(u'enable exit confirmation',
            QtCore.QVariant(True)).toBool())
        self.hideMouseCheckBox.setChecked(
            settings.value(u'hide mouse', QtCore.QVariant(False)).toBool())
        self.x11BypassCheckBox.setChecked(
            settings.value(u'x11 bypass wm', QtCore.QVariant(True)).toBool())
        self.default_color = settings.value(u'default color',
            QtCore.QVariant(u'#ffffff')).toString()
        self.defaultFileEdit.setText(settings.value(u'default image',
            QtCore.QVariant(u':/graphics/openlp-splash-screen.png'))\
            .toString())
        settings.endGroup()
        # Since data location can be changed, make sure the path is present.
        data_path = AppLocation.get_data_path()
        if not os.path.exists(data_path):
            answer = QtGui.QMessageBox.critical(self,
                translate('OpenLP.AdvancedTab',
                'Data directory error - Reset to default?'),
                translate('OpenLP.AdvancedTab',
                'OpenLP data directory was not found \n\n %s \n\n'
                'This data directory was previously changed from the OpenLP '
                'default location.  If the new location was on removable '
                'media, that media needs to be made available.\n\n'
                'Click "No" to stop loading OpenLP. allowing you to fix '
                'the the problem.\n\n'
                'Click "Yes" to reset the data directory location to the '
                'default' % data_path),
                QtGui.QMessageBox.StandardButtons(
                QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No),
                QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.No:
                Receiver.send_message(u'cleanup')
                sys.exit()
            data_path = AppLocation.set_default_data_path()
            print AppLocation.IsDefaultDataPath
        if AppLocation.IsDefaultDataPath:
            self.dataDirectoryDefaultButton.hide()
        else:
             self.dataDirectoryDefaultButton.show()
        self.dataDirectoryLabel.setText(data_path)
        self.defaultColorButton.setStyleSheet(
            u'background-color: %s' % self.default_color)

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
        settings.setValue(u'single click preview',
            QtCore.QVariant(self.singleClickPreviewCheckBox.isChecked()))
        settings.setValue(u'expand service item',
            QtCore.QVariant(self.expandServiceItemCheckBox.isChecked()))
        settings.setValue(u'enable exit confirmation',
            QtCore.QVariant(self.enableAutoCloseCheckBox.isChecked()))
        settings.setValue(u'hide mouse',
            QtCore.QVariant(self.hideMouseCheckBox.isChecked()))
        settings.setValue(u'x11 bypass wm',
            QtCore.QVariant(self.x11BypassCheckBox.isChecked()))
        settings.setValue(u'default color', self.default_color)
        settings.setValue(u'default image', self.defaultFileEdit.text())
        if not AppLocation.IsDefaultDataPath:
            settings.setValue(u'data path', self.dataDirectoryLabel.text())
        settings.setValue(u'copy data',
            QtCore.QVariant(self.dataDirectoryCopyCheckBox.isChecked()))
        settings.endGroup()
        if self.display_changed:
            Receiver.send_message(u'config_screen_changed')
            self.display_changed = False

    def onDefaultColorButtonPressed(self):
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.default_color), self)
        if new_color.isValid():
            self.default_color = new_color.name()
            self.defaultColorButton.setStyleSheet(
                u'background-color: %s' % self.default_color)

    def onDefaultBrowseButtonPressed(self):
        file_filters = u'%s;;%s (*.*) (*)' % (get_images_filter(),
            UiStrings().AllFiles)
        filename = QtGui.QFileDialog.getOpenFileName(self,
            translate('OpenLP.AdvancedTab', 'Open File'), '',
            file_filters)
        if filename:
            self.defaultFileEdit.setText(filename)
        self.defaultFileEdit.setFocus()

    def onDataDirectoryBrowseButtonPressed(self):
        """
        Browse for a new data directory location.
        """
        old_data_path = str(self.dataDirectoryLabel.text())
        old_root_path = os.path.abspath(os.path.join(
            old_data_path, u'..', u'..'))
        # Get the new directory location.
        new_path = unicode(QtGui.QFileDialog.getExistingDirectory(self,
            translate('OpenLP.AdvancedTab',
            'Select Data Folder Root Directory'), old_root_path,
            options=QtGui.QFileDialog.ShowDirsOnly))
        # Set the new data path
        settings = QtCore.QSettings()
        new_data_path = os.path.join(new_path, 'OpenLP', 'Data')
        if new_path:
            if old_data_path.lower() == new_data_path.lower():
                self.onDataDirectoryCancelButtonPressed()
                return
        else:
            return
        # Make sure they want to change the data.
        answer = QtGui.QMessageBox.question(self,
            translate('OpenLP.AdvancedTab', 'Change data directory?'),
            translate('OpenLP.AdvancedTab',
            'Are you sure you want to change the location of the OpenLP data\n'
            'directory to:\n\n %s \n\n'
            'This is the root folder for the data.  The data will be stored '
            'in:\n\n %s \n\n '
            'The data directory will be changed when OpenLP is closed.'
            % (new_path,  new_data_path)),
            QtGui.QMessageBox.StandardButtons(
            QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No),
            QtGui.QMessageBox.No)
        if answer != QtGui.QMessageBox.Yes:
            return
        # Check  if data already exists here
        self.checkDataOverwrite(new_data_path)
        # Save the new location.
        settings.setValue(u'%s/new data path' % self.settingsSection,
            new_data_path)
        self.newDataDirectoryEdit.setText(new_data_path)
        self.dataDirectoryCancelButton.show()

    def onDataDirectoryDefaultButtonPressed(self):
        """
        Re-set the data directory location to the 'default' location.
        """
        # Make sure they want to change the data location back to the default.
        answer = QtGui.QMessageBox.question(self,
            translate('OpenLP.AdvancedTab', 'Reset data directory to default?'),
            translate('OpenLP.AdvancedTab',
            'Are you sure you want to change the location of the OpenLP data\n'
            'directory to the default locatiom?  \n\n'
            'This location will be used after OpenLP is closed.'), 
            QtGui.QMessageBox.StandardButtons(
            QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No),
            QtGui.QMessageBox.No)
        if answer != QtGui.QMessageBox.Yes:
            return
        old_data_path = str(self.dataDirectoryLabel.text())
        new_data_path = AppLocation.get_directory(AppLocation.DataDir)
        if old_data_path.lower() == new_data_path.lower():
            self.onDataDirectoryCancelButtonPressed()
            return
        self.checkDataOverwrite(new_data_path)
        # Save the new location.
        settings = QtCore.QSettings()
        settings.setValue(u'%s/new data path' % self.settingsSection,
            new_data_path)
        self.newDataDirectoryEdit.setText(new_data_path)
        self.dataDirectoryCancelButton.show()

    def checkDataOverwrite(self, data_path ):
        test_path = os.path.join(data_path, u'songs')
        self.dataDirectoryCopyCheckBox.show()
        if os.path.exists(test_path):
            # Check is they want to replace existing data
            answer = QtGui.QMessageBox.warning(self,
                translate('OpenLP.AdvancedTab', 'Replace existing data?'),
                translate('OpenLP.AdvancedTab',
                'WARNING \n\n'
                'The location you have selected \n\n %s \n\n'
                'appears to contain OpenLP data files.  Do you wish to replace '
                'these files with the current data files?' % data_path), 
                QtGui.QMessageBox.StandardButtons(
                QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No),
                QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes:
                self.dataDirectoryCopyCheckBox.setChecked(True)
            else:
                self.dataDirectoryCopyCheckBox.setChecked(False)
            self.newDataDirectoryHasFilesLabel.show()
        else:
            self.dataDirectoryCopyCheckBox.setChecked(True)
            self.newDataDirectoryHasFilesLabel.hide()

    def onDataDirectoryCancelButtonPressed(self):
        """
        Cancel the data directory location change
        """
        self.newDataDirectoryEdit.setText(u'')
        self.dataDirectoryCopyCheckBox.setChecked(False)
        settings = QtCore.QSettings()
        settings.remove(u'%s/new data path' % self.settingsSection)
        settings.remove(u'%s/copy data' % self.settingsSection)
        self.dataDirectoryCopyCheckBox.hide()
        self.dataDirectoryCancelButton.hide()
        self.newDataDirectoryHasFilesLabel.hide()
        print AppLocation.IsDefaultDataPath
        if AppLocation.IsDefaultDataPath:
            self.dataDirectoryDefaultButton.hide()
        else:
             self.dataDirectoryDefaultButton.show()

    def onDefaultRevertButtonPressed(self):
        self.defaultFileEdit.setText(u':/graphics/openlp-splash-screen.png')
        self.defaultFileEdit.setFocus()

    def onX11BypassCheckBoxToggled(self, checked):
        """
        Toggle X11 bypass flag on maindisplay depending on check box state.

        ``checked``
            The state of the check box (boolean).
        """
        self.display_changed = True
