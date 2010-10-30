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

import logging

from PyQt4 import QtCore, QtGui

from openlp.core.ui import AboutForm, SettingsForm, ServiceManager, \
    ThemeManager, SlideController, PluginForm, MediaDockManager, \
    ShortcutListForm
from openlp.core.lib import RenderManager, build_icon, OpenLPDockWidget, \
    SettingsManager, PluginManager, Receiver, translate
from openlp.core.utils import AppLocation, add_actions, LanguageManager, \
    ActionList

log = logging.getLogger(__name__)

MEDIA_MANAGER_STYLE = """
  QToolBox {
    padding-bottom: 2px;
  }
  QToolBox::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 palette(button), stop: 0.5 palette(button),
        stop: 1.0 palette(mid));
    border: 1px groove palette(mid);
    border-radius: 5px;
  }
  QToolBox::tab:selected {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 palette(light), stop: 0.5 palette(midlight),
        stop: 1.0 palette(dark));
    border: 1px groove palette(dark);
    font-weight: bold;
  }
"""

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        """
        Set up the user interface
        """
        MainWindow.setObjectName(u'MainWindow')
        MainWindow.resize(self.settingsmanager.width,
            self.settingsmanager.height)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainIcon = build_icon(u':/icon/openlp-logo-16x16.png')
        MainWindow.setWindowIcon(MainIcon)
        self.setDockNestingEnabled(True)
        # Set up the main container, which contains all the other form widgets
        self.MainContent = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MainContent.sizePolicy().hasHeightForWidth())
        self.MainContent.setSizePolicy(sizePolicy)
        self.MainContent.setObjectName(u'MainContent')
        self.MainContentLayout = QtGui.QHBoxLayout(self.MainContent)
        self.MainContentLayout.setSpacing(0)
        self.MainContentLayout.setMargin(0)
        self.MainContentLayout.setObjectName(u'MainContentLayout')
        MainWindow.setCentralWidget(self.MainContent)
        self.ControlSplitter = QtGui.QSplitter(self.MainContent)
        self.ControlSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.ControlSplitter.setOpaqueResize(False)
        self.ControlSplitter.setObjectName(u'ControlSplitter')
        self.MainContentLayout.addWidget(self.ControlSplitter)
        # Create slide controllers
        self.PreviewController = SlideController(self, self.settingsmanager,
            self.screens)
        self.LiveController = SlideController(self, self.settingsmanager,
            self.screens, True)
        previewVisible = QtCore.QSettings().value(
            u'user interface/preview panel', QtCore.QVariant(True)).toBool()
        self.PreviewController.Panel.setVisible(previewVisible)
        liveVisible = QtCore.QSettings().value(u'user interface/live panel',
            QtCore.QVariant(True)).toBool()
        self.LiveController.Panel.setVisible(liveVisible)
        # Create menu
        self.MenuBar = QtGui.QMenuBar(MainWindow)
        self.MenuBar.setGeometry(QtCore.QRect(0, 0, 1087, 27))
        self.MenuBar.setObjectName(u'MenuBar')
        self.FileMenu = QtGui.QMenu(self.MenuBar)
        self.FileMenu.setObjectName(u'FileMenu')
        self.FileImportMenu = QtGui.QMenu(self.FileMenu)
        self.FileImportMenu.setObjectName(u'FileImportMenu')
        self.FileExportMenu = QtGui.QMenu(self.FileMenu)
        self.FileExportMenu.setObjectName(u'FileExportMenu')
        # View Menu
        self.ViewMenu = QtGui.QMenu(self.MenuBar)
        self.ViewMenu.setObjectName(u'ViewMenu')
        self.ViewModeMenu = QtGui.QMenu(self.ViewMenu)
        self.ViewModeMenu.setObjectName(u'ViewModeMenu')
        # Tools Menu
        self.ToolsMenu = QtGui.QMenu(self.MenuBar)
        self.ToolsMenu.setObjectName(u'ToolsMenu')
        # Settings Menu
        self.SettingsMenu = QtGui.QMenu(self.MenuBar)
        self.SettingsMenu.setObjectName(u'SettingsMenu')
        self.SettingsLanguageMenu = QtGui.QMenu(self.SettingsMenu)
        self.SettingsLanguageMenu.setObjectName(u'SettingsLanguageMenu')
        # Help Menu
        self.HelpMenu = QtGui.QMenu(self.MenuBar)
        self.HelpMenu.setObjectName(u'HelpMenu')
        MainWindow.setMenuBar(self.MenuBar)
        self.StatusBar = QtGui.QStatusBar(MainWindow)
        self.StatusBar.setObjectName(u'StatusBar')
        MainWindow.setStatusBar(self.StatusBar)
        self.DefaultThemeLabel = QtGui.QLabel(self.StatusBar)
        self.DefaultThemeLabel.setObjectName(u'DefaultThemeLabel')
        self.StatusBar.addPermanentWidget(self.DefaultThemeLabel)
        # Create the MediaManager
        self.MediaManagerDock = OpenLPDockWidget(MainWindow)
        self.MediaManagerDock.setWindowIcon(
            build_icon(u':/system/system_mediamanager.png'))
        self.MediaManagerDock.setStyleSheet(MEDIA_MANAGER_STYLE)
        self.MediaManagerDock.setMinimumWidth(
            self.settingsmanager.mainwindow_left)
        self.MediaManagerDock.setObjectName(u'MediaManagerDock')
        self.MediaManagerContents = QtGui.QWidget()
        self.MediaManagerContents.setObjectName(u'MediaManagerContents')
        self.MediaManagerLayout = QtGui.QHBoxLayout(self.MediaManagerContents)
        self.MediaManagerLayout.setContentsMargins(0, 2, 0, 0)
        self.MediaManagerLayout.setObjectName(u'MediaManagerLayout')
        # Create the media toolbox
        self.MediaToolBox = QtGui.QToolBox(self.MediaManagerContents)
        self.MediaToolBox.setObjectName(u'MediaToolBox')
        self.MediaManagerLayout.addWidget(self.MediaToolBox)
        self.MediaManagerDock.setWidget(self.MediaManagerContents)
        MainWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(1), self.MediaManagerDock)
        # Create the service manager
        self.ServiceManagerDock = OpenLPDockWidget(MainWindow)
        self.ServiceManagerDock.setWindowIcon(
            build_icon(u':/system/system_servicemanager.png'))
        self.ServiceManagerDock.setObjectName(u'ServiceManagerDock')
        self.ServiceManagerDock.setMinimumWidth(
            self.settingsmanager.mainwindow_right)
        self.ServiceManagerContents = ServiceManager(self)
        self.ServiceManagerDock.setWidget(self.ServiceManagerContents)
        MainWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(2), self.ServiceManagerDock)
        # Create the theme manager
        self.ThemeManagerDock = OpenLPDockWidget(MainWindow)
        self.ThemeManagerDock.setWindowIcon(
            build_icon(u':/system/system_thememanager.png'))
        self.ThemeManagerDock.setObjectName(u'ThemeManagerDock')
        self.ThemeManagerDock.setMinimumWidth(
            self.settingsmanager.mainwindow_right)
        self.ThemeManagerContents = ThemeManager(self)
        self.ThemeManagerDock.setWidget(self.ThemeManagerContents)
        MainWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(2), self.ThemeManagerDock)
        # Create the menu items
        self.FileNewItem = QtGui.QAction(MainWindow)
        self.FileNewItem.setIcon(build_icon(u':/general/general_new.png'))
        self.FileNewItem.setObjectName(u'FileNewItem')
        MainWindow.actionList.add_action(self.FileNewItem, u'File')
        self.FileOpenItem = QtGui.QAction(MainWindow)
        self.FileOpenItem.setIcon(build_icon(u':/general/general_open.png'))
        self.FileOpenItem.setObjectName(u'FileOpenItem')
        MainWindow.actionList.add_action(self.FileOpenItem, u'File')
        self.FileSaveItem = QtGui.QAction(MainWindow)
        self.FileSaveItem.setIcon(build_icon(u':/general/general_save.png'))
        self.FileSaveItem.setObjectName(u'FileSaveItem')
        MainWindow.actionList.add_action(self.FileSaveItem, u'File')
        self.FileSaveAsItem = QtGui.QAction(MainWindow)
        self.FileSaveAsItem.setObjectName(u'FileSaveAsItem')
        MainWindow.actionList.add_action(self.FileSaveAsItem, u'File')
        self.FileExitItem = QtGui.QAction(MainWindow)
        self.FileExitItem.setIcon(build_icon(u':/system/system_exit.png'))
        self.FileExitItem.setObjectName(u'FileExitItem')
        MainWindow.actionList.add_action(self.FileExitItem, u'File')
        self.ImportThemeItem = QtGui.QAction(MainWindow)
        self.ImportThemeItem.setObjectName(u'ImportThemeItem')
        MainWindow.actionList.add_action(self.ImportThemeItem, u'Import')
        self.ImportLanguageItem = QtGui.QAction(MainWindow)
        self.ImportLanguageItem.setObjectName(u'ImportLanguageItem')
        MainWindow.actionList.add_action(self.ImportLanguageItem, u'Import')
        self.ExportThemeItem = QtGui.QAction(MainWindow)
        self.ExportThemeItem.setObjectName(u'ExportThemeItem')
        MainWindow.actionList.add_action(self.ExportThemeItem, u'Export')
        self.ExportLanguageItem = QtGui.QAction(MainWindow)
        self.ExportLanguageItem.setObjectName(u'ExportLanguageItem')
        MainWindow.actionList.add_action(self.ExportLanguageItem, u'Export')
        self.ViewMediaManagerItem = QtGui.QAction(MainWindow)
        self.ViewMediaManagerItem.setCheckable(True)
        self.ViewMediaManagerItem.setChecked(self.MediaManagerDock.isVisible())
        self.ViewMediaManagerItem.setIcon(
            build_icon(u':/system/system_mediamanager.png'))
        self.ViewMediaManagerItem.setObjectName(u'ViewMediaManagerItem')
        self.ViewThemeManagerItem = QtGui.QAction(MainWindow)
        self.ViewThemeManagerItem.setCheckable(True)
        self.ViewThemeManagerItem.setChecked(self.ThemeManagerDock.isVisible())
        self.ViewThemeManagerItem.setIcon(
            build_icon(u':/system/system_thememanager.png'))
        self.ViewThemeManagerItem.setObjectName(u'ViewThemeManagerItem')
        MainWindow.actionList.add_action(self.ViewMediaManagerItem, u'View')
        self.ViewServiceManagerItem = QtGui.QAction(MainWindow)
        self.ViewServiceManagerItem.setCheckable(True)
        self.ViewServiceManagerItem.setChecked(
            self.ServiceManagerDock.isVisible())
        self.ViewServiceManagerItem.setIcon(
            build_icon(u':/system/system_servicemanager.png'))
        self.ViewServiceManagerItem.setObjectName(u'ViewServiceManagerItem')
        MainWindow.actionList.add_action(self.ViewServiceManagerItem, u'View')
        self.ViewPreviewPanel = QtGui.QAction(MainWindow)
        self.ViewPreviewPanel.setCheckable(True)
        self.ViewPreviewPanel.setChecked(previewVisible)
        self.ViewPreviewPanel.setObjectName(u'ViewPreviewPanel')
        MainWindow.actionList.add_action(self.ViewPreviewPanel, u'View')
        self.ViewLivePanel = QtGui.QAction(MainWindow)
        self.ViewLivePanel.setCheckable(True)
        self.ViewLivePanel.setChecked(liveVisible)
        self.ViewLivePanel.setObjectName(u'ViewLivePanel')
        MainWindow.actionList.add_action(self.ViewLivePanel, u'View')
        self.ModeDefaultItem = QtGui.QAction(MainWindow)
        self.ModeDefaultItem.setCheckable(True)
        self.ModeDefaultItem.setObjectName(u'ModeDefaultItem')
        MainWindow.actionList.add_action(self.ModeDefaultItem, u'View Mode')
        self.ModeSetupItem = QtGui.QAction(MainWindow)
        self.ModeSetupItem.setCheckable(True)
        self.ModeSetupItem.setObjectName(u'ModeLiveItem')
        MainWindow.actionList.add_action(self.ModeSetupItem, u'View Mode')
        self.ModeLiveItem = QtGui.QAction(MainWindow)
        self.ModeLiveItem.setCheckable(True)
        self.ModeLiveItem.setObjectName(u'ModeLiveItem')
        MainWindow.actionList.add_action(self.ModeLiveItem, u'View Mode')
        self.ModeGroup = QtGui.QActionGroup(MainWindow)
        self.ModeGroup.addAction(self.ModeDefaultItem)
        self.ModeGroup.addAction(self.ModeSetupItem)
        self.ModeGroup.addAction(self.ModeLiveItem)
        self.ModeDefaultItem.setChecked(True)
        self.ToolsAddToolItem = QtGui.QAction(MainWindow)
        self.ToolsAddToolItem.setIcon(build_icon(u':/tools/tools_add.png'))
        self.ToolsAddToolItem.setObjectName(u'ToolsAddToolItem')
        MainWindow.actionList.add_action(self.ToolsAddToolItem, u'Tools')
        self.SettingsPluginListItem = QtGui.QAction(MainWindow)
        self.SettingsPluginListItem.setIcon(
            build_icon(u':/system/settings_plugin_list.png'))
        self.SettingsPluginListItem.setObjectName(u'SettingsPluginListItem')
        MainWindow.actionList.add_action(self.SettingsPluginListItem, u'Settings')
        #i18n Language Items
        self.AutoLanguageItem = QtGui.QAction(MainWindow)
        self.AutoLanguageItem.setObjectName(u'AutoLanguageItem')
        self.AutoLanguageItem.setCheckable(True)
        MainWindow.actionList.add_action(self.AutoLanguageItem, u'Settings')
        self.LanguageGroup = QtGui.QActionGroup(MainWindow)
        qmList = LanguageManager.get_qm_list()
        savedLanguage = LanguageManager.get_language()
        self.AutoLanguageItem.setChecked(LanguageManager.auto_language)
        for key in sorted(qmList.keys()):
            languageItem = QtGui.QAction(MainWindow)
            languageItem.setObjectName(key)
            languageItem.setCheckable(True)
            if qmList[key] == savedLanguage:
                languageItem.setChecked(True)
            add_actions(self.LanguageGroup, [languageItem])
        self.LanguageGroup.setDisabled(LanguageManager.auto_language)
        self.SettingsShortcutsItem = QtGui.QAction(MainWindow)
        self.SettingsShortcutsItem.setIcon(
            build_icon(u':/system/system_configure_shortcuts.png'))
        self.SettingsShortcutsItem.setObjectName(u'SettingsShortcutsItem')
        self.SettingsConfigureItem = QtGui.QAction(MainWindow)
        self.SettingsConfigureItem.setIcon(
            build_icon(u':/system/system_settings.png'))
        self.SettingsConfigureItem.setObjectName(u'SettingsConfigureItem')
        MainWindow.actionList.add_action(self.SettingsShortcutsItem, u'Settings')
        self.HelpDocumentationItem = QtGui.QAction(MainWindow)
        self.HelpDocumentationItem.setIcon(
            build_icon(u':/system/system_help_contents.png'))
        self.HelpDocumentationItem.setObjectName(u'HelpDocumentationItem')
        self.HelpDocumentationItem.setEnabled(False)
        MainWindow.actionList.add_action(self.HelpDocumentationItem, u'Help')
        self.HelpAboutItem = QtGui.QAction(MainWindow)
        self.HelpAboutItem.setIcon(
            build_icon(u':/system/system_about.png'))
        self.HelpAboutItem.setObjectName(u'HelpAboutItem')
        MainWindow.actionList.add_action(self.HelpAboutItem, u'Help')
        self.HelpOnlineHelpItem = QtGui.QAction(MainWindow)
        self.HelpOnlineHelpItem.setObjectName(u'HelpOnlineHelpItem')
        self.HelpOnlineHelpItem.setEnabled(False)
        MainWindow.actionList.add_action(self.HelpOnlineHelpItem, u'Help')
        self.HelpWebSiteItem = QtGui.QAction(MainWindow)
        self.HelpWebSiteItem.setObjectName(u'HelpWebSiteItem')
        MainWindow.actionList.add_action(self.HelpWebSiteItem, u'Help')
        add_actions(self.FileImportMenu,
            (self.ImportThemeItem, self.ImportLanguageItem))
        add_actions(self.FileExportMenu,
            (self.ExportThemeItem, self.ExportLanguageItem))
        self.FileMenuActions = (self.FileNewItem, self.FileOpenItem,
            self.FileSaveItem, self.FileSaveAsItem, None,
            self.FileImportMenu.menuAction(), self.FileExportMenu.menuAction(),
            self.FileExitItem)
        add_actions(self.ViewModeMenu, (self.ModeDefaultItem,
            self.ModeSetupItem, self.ModeLiveItem))
        add_actions(self.ViewMenu, (self.ViewModeMenu.menuAction(),
            None, self.ViewMediaManagerItem, self.ViewServiceManagerItem,
            self.ViewThemeManagerItem, None, self.ViewPreviewPanel,
            self.ViewLivePanel))
        #i18n add Language Actions
        add_actions(self.SettingsLanguageMenu, (self.AutoLanguageItem, None))
        add_actions(self.SettingsLanguageMenu, self.LanguageGroup.actions())
        add_actions(self.SettingsMenu, (self.SettingsPluginListItem,
            self.SettingsLanguageMenu.menuAction(), None,
            self.SettingsShortcutsItem, self.SettingsConfigureItem))
        add_actions(self.ToolsMenu,
            (self.ToolsAddToolItem, None))
        add_actions(self.HelpMenu,
            (self.HelpDocumentationItem, self.HelpOnlineHelpItem, None,
            self.HelpWebSiteItem, self.HelpAboutItem))
        add_actions(self.MenuBar,
            (self.FileMenu.menuAction(), self.ViewMenu.menuAction(),
            self.ToolsMenu.menuAction(), self.SettingsMenu.menuAction(),
            self.HelpMenu.menuAction()))
        # Initialise the translation
        self.retranslateUi(MainWindow)
        self.MediaToolBox.setCurrentIndex(0)
        # Connect up some signals and slots
        QtCore.QObject.connect(self.FileMenu,
            QtCore.SIGNAL(u'aboutToShow()'), self.updateFileMenu)
        QtCore.QObject.connect(self.FileExitItem,
            QtCore.SIGNAL(u'triggered()'), MainWindow.close)
        QtCore.QObject.connect(self.ControlSplitter,
            QtCore.SIGNAL(u'splitterMoved(int, int)'), self.trackSplitter)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def trackSplitter(self, tab, pos):
        """
        Splitter between the Preview and Live Controllers.
        """
        self.LiveController.widthChanged()
        self.PreviewController.widthChanged()

    def retranslateUi(self, MainWindow):
        """
        Set up the translation system
        """
        MainWindow.mainTitle = translate('OpenLP.MainWindow', 'OpenLP 2.0')
        MainWindow.setWindowTitle(MainWindow.mainTitle)
        self.FileMenu.setTitle(translate('OpenLP.MainWindow', '&File'))
        self.FileImportMenu.setTitle(translate('OpenLP.MainWindow', '&Import'))
        self.FileExportMenu.setTitle(translate('OpenLP.MainWindow', '&Export'))
        self.ViewMenu.setTitle(translate('OpenLP.MainWindow', '&View'))
        self.ViewModeMenu.setTitle(translate('OpenLP.MainWindow', 'M&ode'))
        self.ToolsMenu.setTitle(translate('OpenLP.MainWindow', '&Tools'))
        self.SettingsMenu.setTitle(translate('OpenLP.MainWindow', '&Settings'))
        self.SettingsLanguageMenu.setTitle(translate('OpenLP.MainWindow',
            '&Language'))
        self.HelpMenu.setTitle(translate('OpenLP.MainWindow', '&Help'))
        self.MediaManagerDock.setWindowTitle(
            translate('OpenLP.MainWindow', 'Media Manager'))
        self.ServiceManagerDock.setWindowTitle(
            translate('OpenLP.MainWindow', 'Service Manager'))
        self.ThemeManagerDock.setWindowTitle(
            translate('OpenLP.MainWindow', 'Theme Manager'))
        self.FileNewItem.setText(translate('OpenLP.MainWindow', '&New'))
        self.FileNewItem.setToolTip(
            translate('OpenLP.MainWindow', 'New Service'))
        self.FileNewItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Create a new service.'))
        self.FileNewItem.setShortcut(translate('OpenLP.MainWindow', 'Ctrl+N'))
        self.FileOpenItem.setText(translate('OpenLP.MainWindow', '&Open'))
        self.FileOpenItem.setToolTip(
            translate('OpenLP.MainWindow', 'Open Service'))
        self.FileOpenItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Open an existing service.'))
        self.FileOpenItem.setShortcut(translate('OpenLP.MainWindow', 'Ctrl+O'))
        self.FileSaveItem.setText(translate('OpenLP.MainWindow', '&Save'))
        self.FileSaveItem.setToolTip(
            translate('OpenLP.MainWindow', 'Save Service'))
        self.FileSaveItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Save the current service to disk.'))
        self.FileSaveItem.setShortcut(translate('OpenLP.MainWindow', 'Ctrl+S'))
        self.FileSaveAsItem.setText(
            translate('OpenLP.MainWindow', 'Save &As...'))
        self.FileSaveAsItem.setToolTip(
            translate('OpenLP.MainWindow', 'Save Service As'))
        self.FileSaveAsItem.setStatusTip(translate('OpenLP.MainWindow',
            'Save the current service under a new name.'))
        self.FileSaveAsItem.setShortcut(
            translate('OpenLP.MainWindow', 'Ctrl+Shift+S'))
        self.FileExitItem.setText(
            translate('OpenLP.MainWindow', 'E&xit'))
        self.FileExitItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Quit OpenLP'))
        self.FileExitItem.setShortcut(
            translate('OpenLP.MainWindow', 'Alt+F4'))
        self.ImportThemeItem.setText(
            translate('OpenLP.MainWindow', '&Theme'))
        self.ImportLanguageItem.setText(
            translate('OpenLP.MainWindow', '&Language'))
        self.ExportThemeItem.setText(
            translate('OpenLP.MainWindow', '&Theme'))
        self.ExportLanguageItem.setText(
            translate('OpenLP.MainWindow', '&Language'))
        self.SettingsShortcutsItem.setText(
            translate('OpenLP.MainWindow', 'Configure &Shortcuts...'))
        self.SettingsConfigureItem.setText(
            translate('OpenLP.MainWindow', '&Configure OpenLP...'))
        self.ViewMediaManagerItem.setText(
            translate('OpenLP.MainWindow', '&Media Manager'))
        self.ViewMediaManagerItem.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Media Manager'))
        self.ViewMediaManagerItem.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the media manager.'))
        self.ViewMediaManagerItem.setShortcut(
            translate('OpenLP.MainWindow', 'F8'))
        self.ViewThemeManagerItem.setText(
            translate('OpenLP.MainWindow', '&Theme Manager'))
        self.ViewThemeManagerItem.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Theme Manager'))
        self.ViewThemeManagerItem.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the theme manager.'))
        self.ViewThemeManagerItem.setShortcut(
            translate('OpenLP.MainWindow', 'F10'))
        self.ViewServiceManagerItem.setText(
            translate('OpenLP.MainWindow', '&Service Manager'))
        self.ViewServiceManagerItem.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Service Manager'))
        self.ViewServiceManagerItem.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the service manager.'))
        self.ViewServiceManagerItem.setShortcut(
            translate('OpenLP.MainWindow', 'F9'))
        self.ViewPreviewPanel.setText(
            translate('OpenLP.MainWindow', '&Preview Panel'))
        self.ViewPreviewPanel.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Preview Panel'))
        self.ViewPreviewPanel.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the preview panel.'))
        self.ViewPreviewPanel.setShortcut(
            translate('OpenLP.MainWindow', 'F11'))
        self.ViewLivePanel.setText(
            translate('OpenLP.MainWindow', '&Live Panel'))
        self.ViewLivePanel.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Live Panel'))
        self.ViewLivePanel.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the live panel.'))
        self.ViewLivePanel.setShortcut(
            translate('OpenLP.MainWindow', 'F12'))
        self.SettingsPluginListItem.setText(translate('OpenLP.MainWindow',
            '&Plugin List'))
        self.SettingsPluginListItem.setStatusTip(
            translate('OpenLP.MainWindow', 'List the Plugins'))
        self.SettingsPluginListItem.setShortcut(
            translate('OpenLP.MainWindow', 'Alt+F7'))
        self.HelpDocumentationItem.setText(
            translate('OpenLP.MainWindow', '&User Guide'))
        self.HelpAboutItem.setText(translate('OpenLP.MainWindow', '&About'))
        self.HelpAboutItem.setStatusTip(
            translate('OpenLP.MainWindow', 'More information about OpenLP'))
        self.HelpAboutItem.setShortcut(translate('OpenLP.MainWindow',
            'Ctrl+F1'))
        self.HelpOnlineHelpItem.setText(
            translate('OpenLP.MainWindow', '&Online Help'))
        self.HelpWebSiteItem.setText(
            translate('OpenLP.MainWindow', '&Web Site'))
        self.AutoLanguageItem.setText(
            translate('OpenLP.MainWindow', '&Auto Detect'))
        self.AutoLanguageItem.setStatusTip(
            translate('OpenLP.MainWindow',
                'Use the system language, if available.'))
        for item in self.LanguageGroup.actions():
            item.setText(item.objectName())
            item.setStatusTip(unicode(translate('OpenLP.MainWindow',
                'Set the interface language to %s')) % item.objectName())
        self.ToolsAddToolItem.setText(
            translate('OpenLP.MainWindow', 'Add &Tool...'))
        self.ToolsAddToolItem.setStatusTip(
            translate('OpenLP.MainWindow',
                'Add an application to the list of tools.'))
        self.ModeDefaultItem.setText(
            translate('OpenLP.MainWindow', '&Default'))
        self.ModeDefaultItem.setStatusTip(
            translate('OpenLP.MainWindow',
                'Set the view mode back to the default.'))
        self.ModeSetupItem.setText(translate('OpenLP.MainWindow', '&Setup'))
        self.ModeSetupItem.setStatusTip(
            translate('OpenLP.MainWindow',
                'Set the view mode to Setup.'))
        self.ModeLiveItem.setText(translate('OpenLP.MainWindow', '&Live'))
        self.ModeLiveItem.setStatusTip(
            translate('OpenLP.MainWindow',
                'Set the view mode to Live.'))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    The main window.
    """
    log.info(u'MainWindow loaded')

    actionList = ActionList()

    def __init__(self, screens, applicationVersion):
        """
        This constructor sets up the interface, the various managers, and the
        plugins.
        """
        QtGui.QMainWindow.__init__(self)
        self.screens = screens
        self.actionList = ActionList()
        self.applicationVersion = applicationVersion
        # Set up settings sections for the main application
        # (not for use by plugins)
        self.uiSettingsSection = u'user interface'
        self.generalSettingsSection = u'general'
        self.serviceSettingsSection = u'servicemanager'
        self.songsSettingsSection = u'songs'
        self.serviceNotSaved = False
        self.settingsmanager = SettingsManager(screens)
        self.aboutForm = AboutForm(self, applicationVersion)
        self.settingsForm = SettingsForm(self.screens, self, self)
        self.shortcutForm = ShortcutListForm(self)
        self.recentFiles = QtCore.QStringList()
        # Set up the path with plugins
        pluginpath = AppLocation.get_directory(AppLocation.PluginsDir)
        self.plugin_manager = PluginManager(pluginpath)
        self.plugin_helpers = {}
        # Set up the interface
        self.setupUi(self)
        # Load settings after setupUi so default UI sizes are overwritten
        self.loadSettings()
        # Once settings are loaded update FileMenu with recentFiles
        self.updateFileMenu()
        self.pluginForm = PluginForm(self)
        # Set up signals and slots
        QtCore.QObject.connect(self.ImportThemeItem,
            QtCore.SIGNAL(u'triggered()'),
            self.ThemeManagerContents.onImportTheme)
        QtCore.QObject.connect(self.ExportThemeItem,
            QtCore.SIGNAL(u'triggered()'),
            self.ThemeManagerContents.onExportTheme)
        QtCore.QObject.connect(self.ViewMediaManagerItem,
            QtCore.SIGNAL(u'triggered(bool)'), self.toggleMediaManager)
        QtCore.QObject.connect(self.ViewServiceManagerItem,
            QtCore.SIGNAL(u'triggered(bool)'), self.toggleServiceManager)
        QtCore.QObject.connect(self.ViewThemeManagerItem,
            QtCore.SIGNAL(u'triggered(bool)'), self.toggleThemeManager)
        QtCore.QObject.connect(self.ViewPreviewPanel,
            QtCore.SIGNAL(u'toggled(bool)'), self.setPreviewPanelVisibility)
        QtCore.QObject.connect(self.ViewLivePanel,
            QtCore.SIGNAL(u'toggled(bool)'), self.setLivePanelVisibility)
        QtCore.QObject.connect(self.MediaManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.ViewMediaManagerItem.setChecked)
        QtCore.QObject.connect(self.ServiceManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.ViewServiceManagerItem.setChecked)
        QtCore.QObject.connect(self.ThemeManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.ViewThemeManagerItem.setChecked)
        QtCore.QObject.connect(self.HelpWebSiteItem,
            QtCore.SIGNAL(u'triggered()'), self.onHelpWebSiteClicked)
        QtCore.QObject.connect(self.HelpAboutItem,
            QtCore.SIGNAL(u'triggered()'), self.onHelpAboutItemClicked)
        QtCore.QObject.connect(self.SettingsPluginListItem,
            QtCore.SIGNAL(u'triggered()'), self.onPluginItemClicked)
        QtCore.QObject.connect(self.SettingsConfigureItem,
            QtCore.SIGNAL(u'triggered()'), self.onSettingsConfigureItemClicked)
        QtCore.QObject.connect(self.SettingsShortcutsItem,
            QtCore.SIGNAL(u'triggered()'), self.onSettingsShortcutsItemClicked)
        QtCore.QObject.connect(self.FileNewItem, QtCore.SIGNAL(u'triggered()'),
            self.ServiceManagerContents.onNewService)
        QtCore.QObject.connect(self.FileOpenItem,
            QtCore.SIGNAL(u'triggered()'),
            self.ServiceManagerContents.onLoadService)
        QtCore.QObject.connect(self.FileSaveItem,
            QtCore.SIGNAL(u'triggered()'),
            self.ServiceManagerContents.onQuickSaveService)
        QtCore.QObject.connect(self.FileSaveAsItem,
            QtCore.SIGNAL(u'triggered()'),
            self.ServiceManagerContents.onSaveService)
        # i18n set signals for languages
        QtCore.QObject.connect(self.AutoLanguageItem,
            QtCore.SIGNAL(u'toggled(bool)'), self.setAutoLanguage)
        self.LanguageGroup.triggered.connect(LanguageManager.set_language)
        QtCore.QObject.connect(self.ModeDefaultItem,
            QtCore.SIGNAL(u'triggered()'), self.onModeDefaultItemClicked)
        QtCore.QObject.connect(self.ModeSetupItem,
            QtCore.SIGNAL(u'triggered()'), self.onModeSetupItemClicked)
        QtCore.QObject.connect(self.ModeLiveItem,
            QtCore.SIGNAL(u'triggered()'), self.onModeLiveItemClicked)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_global'), self.defaultThemeChanged)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_version_check'), self.versionNotice)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'maindisplay_blank_check'), self.blankCheck)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_screen_changed'), self.screenChanged)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'maindisplay_status_text'), self.showStatusMessage)
        # warning cyclic dependency
        # RenderManager needs to call ThemeManager and
        # ThemeManager needs to call RenderManager
        self.RenderManager = RenderManager(
            self.ThemeManagerContents, self.screens)
        # Define the media Dock Manager
        self.mediaDockManager = MediaDockManager(self.MediaToolBox)
        log.info(u'Load Plugins')
        # make the controllers available to the plugins
        self.plugin_helpers[u'preview'] = self.PreviewController
        self.plugin_helpers[u'live'] = self.LiveController
        self.plugin_helpers[u'render'] = self.RenderManager
        self.plugin_helpers[u'service'] = self.ServiceManagerContents
        self.plugin_helpers[u'settings form'] = self.settingsForm
        self.plugin_helpers[u'toolbox'] = self.mediaDockManager
        self.plugin_helpers[u'pluginmanager'] = self.plugin_manager
        self.plugin_helpers[u'formparent'] = self
        self.plugin_manager.find_plugins(pluginpath, self.plugin_helpers)
        # hook methods have to happen after find_plugins. Find plugins needs
        # the controllers hence the hooks have moved from setupUI() to here
        # Find and insert settings tabs
        log.info(u'hook settings')
        self.plugin_manager.hook_settings_tabs(self.settingsForm)
        # Find and insert media manager items
        log.info(u'hook media')
        self.plugin_manager.hook_media_manager(self.mediaDockManager)
        # Call the hook method to pull in import menus.
        log.info(u'hook menus')
        self.plugin_manager.hook_import_menu(self.FileImportMenu)
        # Call the hook method to pull in export menus.
        self.plugin_manager.hook_export_menu(self.FileExportMenu)
        # Call the hook method to pull in tools menus.
        self.plugin_manager.hook_tools_menu(self.ToolsMenu)
        # Call the initialise method to setup plugins.
        log.info(u'initialise plugins')
        self.plugin_manager.initialise_plugins()
        # Once all components are initialised load the Themes
        log.info(u'Load Themes')
        self.ThemeManagerContents.loadThemes()
        log.info(u'Load data from Settings')
        if QtCore.QSettings().value(u'advanced/save current plugin',
            QtCore.QVariant(False)).toBool():
            savedPlugin = QtCore.QSettings().value(
                u'advanced/current media plugin', QtCore.QVariant()).toInt()[0]
            if savedPlugin != -1:
                self.MediaToolBox.setCurrentIndex(savedPlugin)
        self.settingsForm.postSetUp()

    def setAutoLanguage(self, value):
        self.LanguageGroup.setDisabled(value)
        LanguageManager.auto_language = value
        LanguageManager.set_language(self.LanguageGroup.checkedAction())

    def versionNotice(self, version):
        """
        Notifies the user that a newer version of OpenLP is available.
        Triggered by delay thread.
        """
        version_text = unicode(translate('OpenLP.MainWindow',
            'Version %s of OpenLP is now available for download (you are '
            'currently running version %s). \n\nYou can download the latest '
            'version from http://openlp.org/.'))
        QtGui.QMessageBox.question(self,
            translate('OpenLP.MainWindow', 'OpenLP Version Updated'),
            version_text % (version, self.applicationVersion[u'full']))

    def show(self):
        """
        Show the main form, as well as the display form
        """
        QtGui.QWidget.show(self)
        self.LiveController.display.setup()
        self.PreviewController.display.setup()
        if self.LiveController.display.isVisible():
            self.LiveController.display.setFocus()
        self.activateWindow()
        if QtCore.QSettings().value(
            self.generalSettingsSection + u'/auto open',
            QtCore.QVariant(False)).toBool():
            self.ServiceManagerContents.onLoadService(True)
        view_mode = QtCore.QSettings().value(u'%s/view mode' % \
            self.generalSettingsSection, u'default')
        if view_mode == u'default':
            self.ModeDefaultItem.setChecked(True)
        elif view_mode == u'setup':
            self.setViewMode(True, True, False, True, False)
            self.ModeSetupItem.setChecked(True)
        elif view_mode == u'live':
            self.setViewMode(False, True, False, False, True)
            self.ModeLiveItem.setChecked(True)

    def blankCheck(self):
        """
        Check and display message if screen blank on setup.
        Triggered by delay thread.
        """
        settings = QtCore.QSettings()
        if settings.value(u'%s/screen blank' % self.generalSettingsSection,
            QtCore.QVariant(False)).toBool():
            self.LiveController.mainDisplaySetBackground()
            if settings.value(u'blank warning',
                QtCore.QVariant(False)).toBool():
                QtGui.QMessageBox.question(self,
                    translate('OpenLP.MainWindow',
                        'OpenLP Main Display Blanked'),
                    translate('OpenLP.MainWindow',
                         'The Main Display has been blanked out'))

    def onHelpWebSiteClicked(self):
        """
        Load the OpenLP website
        """
        import webbrowser
        webbrowser.open_new(u'http://openlp.org/')

    def onHelpAboutItemClicked(self):
        """
        Show the About form
        """
        self.aboutForm.applicationVersion = self.applicationVersion
        self.aboutForm.exec_()

    def onPluginItemClicked(self):
        """
        Show the Plugin form
        """
        self.pluginForm.load()
        self.pluginForm.exec_()

    def onSettingsConfigureItemClicked(self):
        """
        Show the Settings dialog
        """
        self.settingsForm.exec_()

    def onSettingsShortcutsItemClicked(self):
        """
        Show the shortcuts dialog
        """
        self.shortcutForm.exec_(self.actionList)

    def onModeDefaultItemClicked(self):
        """
        Put OpenLP into "Default" view mode.
        """
        settings = QtCore.QSettings()
        settings.setValue(u'%s/view mode' % self.generalSettingsSection,
            u'default')
        self.setViewMode(True, True, True, True, True)

    def onModeSetupItemClicked(self):
        """
        Put OpenLP into "Setup" view mode.
        """
        settings = QtCore.QSettings()
        settings.setValue(u'%s/view mode' % self.generalSettingsSection,
            u'setup')
        self.setViewMode(True, True, False, True, False)

    def onModeLiveItemClicked(self):
        """
        Put OpenLP into "Live" view mode.
        """
        settings = QtCore.QSettings()
        settings.setValue(u'%s/view mode' % self.generalSettingsSection,
            u'live')
        self.setViewMode(False, True, False, False, True)

    def setViewMode(self, media=True, service=True, theme=True, preview=True,
        live=True):
        """
        Set OpenLP to a different view mode.
        """
        self.MediaManagerDock.setVisible(media)
        self.ServiceManagerDock.setVisible(service)
        self.ThemeManagerDock.setVisible(theme)
        self.setPreviewPanelVisibility(preview)
        self.setLivePanelVisibility(live)

    def screenChanged(self):
        """
        The screen has changed to so tell the displays to update_display
        their locations
        """
        log.debug(u'screenChanged')
        self.RenderManager.update_display()
        self.setFocus()
        self.activateWindow()

    def closeEvent(self, event):
        """
        Hook to close the main window and display windows on exit
        """
        if self.serviceNotSaved:
            ret = QtGui.QMessageBox.question(self,
                translate('OpenLP.MainWindow', 'Save Changes to Service?'),
                translate('OpenLP.MainWindow', 'Your service has changed. '
                    'Do you want to save those changes?'),
                QtGui.QMessageBox.StandardButtons(
                    QtGui.QMessageBox.Cancel |
                    QtGui.QMessageBox.Discard |
                    QtGui.QMessageBox.Save),
                QtGui.QMessageBox.Save)
            if ret == QtGui.QMessageBox.Save:
                self.ServiceManagerContents.onSaveService(True)
                self.cleanUp()
                event.accept()
            elif ret == QtGui.QMessageBox.Discard:
                self.cleanUp()
                event.accept()
            else:
                event.ignore()
        else:
            self.cleanUp()
            event.accept()

    def cleanUp(self):
        """
        Runs all the cleanup code before OpenLP shuts down
        """
        # Clean temporary files used by services
        self.ServiceManagerContents.cleanUp()
        if QtCore.QSettings().value(u'advanced/save current plugin',
            QtCore.QVariant(False)).toBool():
            QtCore.QSettings().setValue(u'advanced/current media plugin',
                QtCore.QVariant(self.MediaToolBox.currentIndex()))
        # Call the cleanup method to shutdown plugins.
        log.info(u'cleanup plugins')
        self.plugin_manager.finalise_plugins()
        # Save settings
        self.saveSettings()
        #Close down the display
        self.LiveController.display.close()

    def serviceChanged(self, reset=False, serviceName=None):
        """
        Hook to change the main window title when the service changes

        ``reset``
            Shows if the service has been cleared or saved

        ``serviceName``
            The name of the service (if it has one)
        """
        if not serviceName:
            service_name = u'(unsaved service)'
        else:
            service_name = serviceName
        if reset:
            self.serviceNotSaved = False
            title = u'%s - %s' % (self.mainTitle, service_name)
        else:
            self.serviceNotSaved = True
            title = u'%s - %s*' % (self.mainTitle, service_name)
        self.setWindowTitle(title)

    def showStatusMessage(self, message):
        self.StatusBar.showMessage(message)

    def defaultThemeChanged(self, theme):
        self.DefaultThemeLabel.setText(
            unicode(translate('OpenLP.MainWindow', 'Default Theme: %s')) %
                theme)

    def toggleMediaManager(self, visible):
        if self.MediaManagerDock.isVisible() != visible:
            self.MediaManagerDock.setVisible(visible)

    def toggleServiceManager(self, visible):
        if self.ServiceManagerDock.isVisible() != visible:
            self.ServiceManagerDock.setVisible(visible)

    def toggleThemeManager(self, visible):
        if self.ThemeManagerDock.isVisible() != visible:
            self.ThemeManagerDock.setVisible(visible)

    def setPreviewPanelVisibility(self, visible):
        """
        Sets the visibility of the preview panel including saving the setting
        and updating the menu.

        ``visible``
            A bool giving the state to set the panel to
                True - Visible
                False - Hidden
        """
        self.PreviewController.Panel.setVisible(visible)
        QtCore.QSettings().setValue(u'user interface/preview panel',
            QtCore.QVariant(visible))
        self.ViewPreviewPanel.setChecked(visible)

    def setLivePanelVisibility(self, visible):
        """
        Sets the visibility of the live panel including saving the setting and
        updating the menu.

        ``visible``
            A bool giving the state to set the panel to
                True - Visible
                False - Hidden
        """
        self.LiveController.Panel.setVisible(visible)
        QtCore.QSettings().setValue(u'user interface/live panel',
            QtCore.QVariant(visible))
        self.ViewLivePanel.setChecked(visible)

    def loadSettings(self):
        """
        Load the main window settings.
        """
        log.debug(u'Loading QSettings')
        settings = QtCore.QSettings()
        settings.beginGroup(self.generalSettingsSection)
        self.recentFiles = settings.value(u'recent files').toStringList()
        settings.endGroup()
        settings.beginGroup(self.uiSettingsSection)
        self.move(settings.value(u'main window position',
            QtCore.QVariant(QtCore.QPoint(0, 0))).toPoint())
        self.restoreGeometry(
            settings.value(u'main window geometry').toByteArray())
        self.restoreState(settings.value(u'main window state').toByteArray())
        settings.endGroup()

    def saveSettings(self):
        """
        Save the main window settings.
        """
        log.debug(u'Saving QSettings')
        settings = QtCore.QSettings()
        settings.beginGroup(self.generalSettingsSection)
        recentFiles = QtCore.QVariant(self.recentFiles) \
            if self.recentFiles else QtCore.QVariant()
        settings.setValue(u'recent files', recentFiles)
        settings.endGroup()
        settings.beginGroup(self.uiSettingsSection)
        settings.setValue(u'main window position',
            QtCore.QVariant(self.pos()))
        settings.setValue(u'main window state',
            QtCore.QVariant(self.saveState()))
        settings.setValue(u'main window geometry',
            QtCore.QVariant(self.saveGeometry()))
        settings.endGroup()

    def updateFileMenu(self):
        """
        Updates the file menu with the latest list of service files accessed.
        """
        recentFileCount = QtCore.QSettings().value(
            u'advanced/recent file count', QtCore.QVariant(4)).toInt()[0]
        self.FileMenu.clear()
        add_actions(self.FileMenu, self.FileMenuActions[:-1])
        existingRecentFiles = [file for file in self.recentFiles
            if QtCore.QFile.exists(file)]
        recentFilesToDisplay = existingRecentFiles[0:recentFileCount]
        if recentFilesToDisplay:
            self.FileMenu.addSeparator()
            for fileId, filename in enumerate(recentFilesToDisplay):
                action = QtGui.QAction(u'&%d %s' % (fileId +1,
                    QtCore.QFileInfo(filename).fileName()), self)
                action.setData(QtCore.QVariant(filename))
                self.connect(action, QtCore.SIGNAL(u'triggered()'),
                    self.ServiceManagerContents.loadService)
                self.FileMenu.addAction(action)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.FileMenuActions[-1])

    def addRecentFile(self, filename):
        """
        Adds a service to the list of recently used files.

        ``filename``
            The service filename to add
        """
        # The maxRecentFiles value does not have an interface and so never gets
        # actually stored in the settings therefore the default value of 20
        # will always be used.
        maxRecentFiles = QtCore.QSettings().value(u'advanced/max recent files',
            QtCore.QVariant(20)).toInt()[0]
        if filename:
            position = self.recentFiles.indexOf(filename)
            if position != -1:
                self.recentFiles.removeAt(position)
            self.recentFiles.insert(0, QtCore.QString(filename))
            while self.recentFiles.count() > maxRecentFiles:
                # Don't care what API says takeLast works, removeLast doesn't!
                self.recentFiles.takeLast()
