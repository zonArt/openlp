# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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

from openlp.core.lib import RenderManager, build_icon, OpenLPDockWidget, \
    SettingsManager, PluginManager, Receiver, translate
from openlp.core.lib.ui import UiStrings, base_action, checkable_action, \
    icon_action
from openlp.core.ui import AboutForm, SettingsForm, ServiceManager, \
    ThemeManager, SlideController, PluginForm, MediaDockManager, \
    ShortcutListForm, DisplayTagForm
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
    def setupUi(self, mainWindow):
        """
        Set up the user interface
        """
        mainWindow.setObjectName(u'MainWindow')
        mainWindow.resize(self.settingsmanager.width,
            self.settingsmanager.height)
        mainWindow.setWindowIcon(build_icon(u':/icon/openlp-logo-16x16.png'))
        mainWindow.setDockNestingEnabled(True)
        # Set up the main container, which contains all the other form widgets.
        self.MainContent = QtGui.QWidget(mainWindow)
        self.MainContent.setObjectName(u'MainContent')
        self.mainContentLayout = QtGui.QHBoxLayout(self.MainContent)
        self.mainContentLayout.setSpacing(0)
        self.mainContentLayout.setMargin(0)
        self.mainContentLayout.setObjectName(u'mainContentLayout')
        mainWindow.setCentralWidget(self.MainContent)
        self.controlSplitter = QtGui.QSplitter(self.MainContent)
        self.controlSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.controlSplitter.setObjectName(u'controlSplitter')
        self.mainContentLayout.addWidget(self.controlSplitter)
        # Create slide controllers
        self.previewController = SlideController(self, self.settingsmanager,
            self.screens)
        self.liveController = SlideController(self, self.settingsmanager,
            self.screens, True)
        previewVisible = QtCore.QSettings().value(
            u'user interface/preview panel', QtCore.QVariant(True)).toBool()
        self.previewController.panel.setVisible(previewVisible)
        liveVisible = QtCore.QSettings().value(u'user interface/live panel',
            QtCore.QVariant(True)).toBool()
        self.liveController.panel.setVisible(liveVisible)
        # Create menu
        self.MenuBar = QtGui.QMenuBar(mainWindow)
        self.MenuBar.setObjectName(u'MenuBar')
        self.FileMenu = QtGui.QMenu(self.MenuBar)
        self.FileMenu.setObjectName(u'FileMenu')
        self.FileImportMenu = QtGui.QMenu(self.FileMenu)
        self.FileImportMenu.setObjectName(u'FileImportMenu')
        self.FileExportMenu = QtGui.QMenu(self.FileMenu)
        self.FileExportMenu.setObjectName(u'FileExportMenu')
        # View Menu
        self.viewMenu = QtGui.QMenu(self.MenuBar)
        self.viewMenu.setObjectName(u'viewMenu')
        self.ViewModeMenu = QtGui.QMenu(self.viewMenu)
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
        mainWindow.setMenuBar(self.MenuBar)
        self.StatusBar = QtGui.QStatusBar(mainWindow)
        self.StatusBar.setObjectName(u'StatusBar')
        mainWindow.setStatusBar(self.StatusBar)
        self.DefaultThemeLabel = QtGui.QLabel(self.StatusBar)
        self.DefaultThemeLabel.setObjectName(u'DefaultThemeLabel')
        self.StatusBar.addPermanentWidget(self.DefaultThemeLabel)
        # Create the MediaManager
        self.mediaManagerDock = OpenLPDockWidget(mainWindow,
            u'mediaManagerDock', u':/system/system_mediamanager.png')
        self.mediaManagerDock.setStyleSheet(MEDIA_MANAGER_STYLE)
        self.mediaManagerDock.setMinimumWidth(
            self.settingsmanager.mainwindow_left)
        # Create the media toolbox
        self.MediaToolBox = QtGui.QToolBox(self.mediaManagerDock)
        self.MediaToolBox.setObjectName(u'MediaToolBox')
        self.mediaManagerDock.setWidget(self.MediaToolBox)
        mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
            self.mediaManagerDock)
        # Create the service manager
        self.serviceManagerDock = OpenLPDockWidget(mainWindow,
            u'serviceManagerDock', u':/system/system_servicemanager.png')
        self.serviceManagerDock.setMinimumWidth(
            self.settingsmanager.mainwindow_right)
        self.ServiceManagerContents = ServiceManager(mainWindow,
            self.serviceManagerDock)
        self.serviceManagerDock.setWidget(self.ServiceManagerContents)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea,
            self.serviceManagerDock)
        # Create the theme manager
        self.themeManagerDock = OpenLPDockWidget(mainWindow,
            u'themeManagerDock', u':/system/system_thememanager.png')
        self.themeManagerDock.setMinimumWidth(
            self.settingsmanager.mainwindow_right)
        self.themeManagerContents = ThemeManager(mainWindow,
            self.themeManagerDock)
        self.themeManagerContents.setObjectName(u'themeManagerContents')
        self.themeManagerDock.setWidget(self.themeManagerContents)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea,
            self.themeManagerDock)
        # Create the menu items
        self.FileNewItem = icon_action(mainWindow, u'FileNewItem',
            u':/general/general_new.png')
        mainWindow.actionList.add_action(self.FileNewItem, u'File')
        self.FileOpenItem = icon_action(mainWindow, u'FileOpenItem',
            u':/general/general_open.png')
        mainWindow.actionList.add_action(self.FileOpenItem, u'File')
        self.FileSaveItem = icon_action(mainWindow, u'FileSaveItem',
            u':/general/general_save.png')
        mainWindow.actionList.add_action(self.FileSaveItem, u'File')
        self.FileSaveAsItem = base_action(mainWindow, u'FileSaveAsItem')
        mainWindow.actionList.add_action(self.FileSaveAsItem, u'File')
        self.printServiceOrderItem = base_action(
            mainWindow, u'printServiceItem')
        mainWindow.actionList.add_action(
            self.printServiceOrderItem, u'Print Service Order')
        self.FileExitItem = icon_action(mainWindow, u'FileExitItem',
            u':/system/system_exit.png')
        mainWindow.actionList.add_action(self.FileExitItem, u'File')
        self.ImportThemeItem = base_action(mainWindow, u'ImportThemeItem')
        mainWindow.actionList.add_action(self.ImportThemeItem, u'Import')
        self.ImportLanguageItem = base_action(mainWindow, u'ImportLanguageItem')
        mainWindow.actionList.add_action(self.ImportLanguageItem, u'Import')
        self.ExportThemeItem = base_action(mainWindow, u'ExportThemeItem')
        mainWindow.actionList.add_action(self.ExportThemeItem, u'Export')
        self.ExportLanguageItem = base_action(mainWindow, u'ExportLanguageItem')
        mainWindow.actionList.add_action(self.ExportLanguageItem, u'Export')
        self.ViewMediaManagerItem = icon_action(mainWindow,
            u'ViewMediaManagerItem', u':/system/system_mediamanager.png',
            self.mediaManagerDock.isVisible())
        self.ViewThemeManagerItem = icon_action(mainWindow,
            u'ViewThemeManagerItem', u':/system/system_thememanager.png',
            self.themeManagerDock.isVisible())
        mainWindow.actionList.add_action(self.ViewMediaManagerItem, u'View')
        self.ViewServiceManagerItem = icon_action(mainWindow,
            u'ViewServiceManagerItem', u':/system/system_servicemanager.png',
            self.serviceManagerDock.isVisible())
        mainWindow.actionList.add_action(self.ViewServiceManagerItem, u'View')
        self.ViewPreviewPanel = checkable_action(mainWindow,
            u'ViewPreviewPanel', previewVisible)
        mainWindow.actionList.add_action(self.ViewPreviewPanel, u'View')
        self.ViewLivePanel = checkable_action(mainWindow, u'ViewLivePanel',
            liveVisible)
        mainWindow.actionList.add_action(self.ViewLivePanel, u'View')
        self.ModeDefaultItem = checkable_action(mainWindow, u'ModeDefaultItem')
        mainWindow.actionList.add_action(self.ModeDefaultItem, u'View Mode')
        self.ModeSetupItem = checkable_action(mainWindow, u'ModeLiveItem')
        mainWindow.actionList.add_action(self.ModeSetupItem, u'View Mode')
        self.ModeLiveItem = checkable_action(mainWindow, u'ModeLiveItem', True)
        mainWindow.actionList.add_action(self.ModeLiveItem, u'View Mode')
        self.ModeGroup = QtGui.QActionGroup(mainWindow)
        self.ModeGroup.addAction(self.ModeDefaultItem)
        self.ModeGroup.addAction(self.ModeSetupItem)
        self.ModeGroup.addAction(self.ModeLiveItem)
        self.ModeDefaultItem.setChecked(True)
        self.ToolsAddToolItem = icon_action(mainWindow, u'ToolsAddToolItem',
            u':/tools/tools_add.png')
        # Hide the entry, as it does not have any functionality yet.
        self.ToolsAddToolItem.setVisible(False)
        mainWindow.actionList.add_action(self.ToolsAddToolItem, u'Tools')
        self.ToolsOpenDataFolder = icon_action(mainWindow,
            u'ToolsOpenDataFolder', u':/general/general_open.png')
        mainWindow.actionList.add_action(self.ToolsOpenDataFolder, u'Tools')
        self.settingsPluginListItem = icon_action(mainWindow,
            u'settingsPluginListItem', u':/system/settings_plugin_list.png')
        mainWindow.actionList.add_action(self.settingsPluginListItem,
            u'Settings')
        # i18n Language Items
        self.AutoLanguageItem = checkable_action(mainWindow,
            u'AutoLanguageItem', LanguageManager.auto_language)
        mainWindow.actionList.add_action(self.AutoLanguageItem, u'Settings')
        self.LanguageGroup = QtGui.QActionGroup(mainWindow)
        self.LanguageGroup.setExclusive(True)
        self.LanguageGroup.setObjectName(u'LanguageGroup')
        self.LanguageGroup.setDisabled(LanguageManager.auto_language)
        qmList = LanguageManager.get_qm_list()
        savedLanguage = LanguageManager.get_language()
        for key in sorted(qmList.keys()):
            languageItem = checkable_action(
                mainWindow, key, qmList[key] == savedLanguage)
            add_actions(self.LanguageGroup, [languageItem])
        self.SettingsShortcutsItem = icon_action(mainWindow,
            u'SettingsShortcutsItem',
            u':/system/system_configure_shortcuts.png')
        self.DisplayTagItem = icon_action(mainWindow,
            u'DisplayTagItem', u':/system/tag_editor.png')
        self.SettingsConfigureItem = icon_action(mainWindow,
            u'SettingsConfigureItem', u':/system/system_settings.png')
        mainWindow.actionList.add_action(self.SettingsShortcutsItem,
            u'Settings')
        self.HelpDocumentationItem = icon_action(mainWindow,
            u'HelpDocumentationItem', u':/system/system_help_contents.png')
        self.HelpDocumentationItem.setEnabled(False)
        mainWindow.actionList.add_action(self.HelpDocumentationItem, u'Help')
        self.HelpAboutItem = icon_action(mainWindow, u'HelpAboutItem',
            u':/system/system_about.png')
        mainWindow.actionList.add_action(self.HelpAboutItem, u'Help')
        self.HelpOnlineHelpItem = base_action(mainWindow, u'HelpOnlineHelpItem')
        self.HelpOnlineHelpItem.setEnabled(False)
        mainWindow.actionList.add_action(self.HelpOnlineHelpItem, u'Help')
        self.helpWebSiteItem = base_action(mainWindow, u'helpWebSiteItem')
        mainWindow.actionList.add_action(self.helpWebSiteItem, u'Help')
        add_actions(self.FileImportMenu,
            (self.ImportThemeItem, self.ImportLanguageItem))
        add_actions(self.FileExportMenu,
            (self.ExportThemeItem, self.ExportLanguageItem))
        self.FileMenuActions = (self.FileNewItem, self.FileOpenItem,
            self.FileSaveItem, self.FileSaveAsItem, None,
            self.printServiceOrderItem, None, self.FileImportMenu.menuAction(),
            self.FileExportMenu.menuAction(), self.FileExitItem)
        add_actions(self.ViewModeMenu, (self.ModeDefaultItem,
            self.ModeSetupItem, self.ModeLiveItem))
        add_actions(self.viewMenu, (self.ViewModeMenu.menuAction(),
            None, self.ViewMediaManagerItem, self.ViewServiceManagerItem,
            self.ViewThemeManagerItem, None, self.ViewPreviewPanel,
            self.ViewLivePanel))
        # i18n add Language Actions
        add_actions(self.SettingsLanguageMenu, (self.AutoLanguageItem, None))
        add_actions(self.SettingsLanguageMenu, self.LanguageGroup.actions())
        add_actions(self.SettingsMenu, (self.settingsPluginListItem,
            self.SettingsLanguageMenu.menuAction(), None,
            self.DisplayTagItem, self.SettingsShortcutsItem,
            self.SettingsConfigureItem))
        add_actions(self.ToolsMenu, (self.ToolsAddToolItem, None))
        add_actions(self.ToolsMenu, (self.ToolsOpenDataFolder, None))
        add_actions(self.HelpMenu, (self.HelpDocumentationItem,
            self.HelpOnlineHelpItem, None, self.helpWebSiteItem,
            self.HelpAboutItem))
        add_actions(self.MenuBar, (self.FileMenu.menuAction(),
            self.viewMenu.menuAction(), self.ToolsMenu.menuAction(),
            self.SettingsMenu.menuAction(), self.HelpMenu.menuAction()))
        # Initialise the translation
        self.retranslateUi(mainWindow)
        self.MediaToolBox.setCurrentIndex(0)
        # Connect up some signals and slots
        QtCore.QObject.connect(self.FileMenu,
            QtCore.SIGNAL(u'aboutToShow()'), self.updateFileMenu)
        QtCore.QObject.connect(self.FileExitItem,
            QtCore.SIGNAL(u'triggered()'), mainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        """
        Set up the translation system
        """
        mainWindow.mainTitle = UiStrings.OLPV2
        mainWindow.setWindowTitle(mainWindow.mainTitle)
        self.FileMenu.setTitle(translate('OpenLP.MainWindow', '&File'))
        self.FileImportMenu.setTitle(translate('OpenLP.MainWindow', '&Import'))
        self.FileExportMenu.setTitle(translate('OpenLP.MainWindow', '&Export'))
        self.viewMenu.setTitle(translate('OpenLP.MainWindow', '&View'))
        self.ViewModeMenu.setTitle(translate('OpenLP.MainWindow', 'M&ode'))
        self.ToolsMenu.setTitle(translate('OpenLP.MainWindow', '&Tools'))
        self.SettingsMenu.setTitle(translate('OpenLP.MainWindow', '&Settings'))
        self.SettingsLanguageMenu.setTitle(translate('OpenLP.MainWindow',
            '&Language'))
        self.HelpMenu.setTitle(translate('OpenLP.MainWindow', '&Help'))
        self.mediaManagerDock.setWindowTitle(
            translate('OpenLP.MainWindow', 'Media Manager'))
        self.serviceManagerDock.setWindowTitle(
            translate('OpenLP.MainWindow', 'Service Manager'))
        self.themeManagerDock.setWindowTitle(
            translate('OpenLP.MainWindow', 'Theme Manager'))
        self.FileNewItem.setText(translate('OpenLP.MainWindow', '&New'))
        self.FileNewItem.setToolTip(UiStrings.NewService)
        self.FileNewItem.setStatusTip(UiStrings.CreateService)
        self.FileNewItem.setShortcut(translate('OpenLP.MainWindow', 'Ctrl+N'))
        self.FileOpenItem.setText(translate('OpenLP.MainWindow', '&Open'))
        self.FileOpenItem.setToolTip(UiStrings.OpenService)
        self.FileOpenItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Open an existing service.'))
        self.FileOpenItem.setShortcut(translate('OpenLP.MainWindow', 'Ctrl+O'))
        self.FileSaveItem.setText(translate('OpenLP.MainWindow', '&Save'))
        self.FileSaveItem.setToolTip(UiStrings.SaveService)
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
        self.printServiceOrderItem.setText(UiStrings.PrintServiceOrder)
        self.printServiceOrderItem.setStatusTip(translate('OpenLP.MainWindow',
            'Print the current Service Order.'))
        self.printServiceOrderItem.setShortcut(
            translate('OpenLP.MainWindow', 'Ctrl+P'))
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
        self.DisplayTagItem.setText(
            translate('OpenLP.MainWindow', '&Configure Display Tags'))
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
        self.settingsPluginListItem.setText(translate('OpenLP.MainWindow',
            '&Plugin List'))
        self.settingsPluginListItem.setStatusTip(
            translate('OpenLP.MainWindow', 'List the Plugins'))
        self.settingsPluginListItem.setShortcut(
            translate('OpenLP.MainWindow', 'Alt+F7'))
        self.HelpDocumentationItem.setText(
            translate('OpenLP.MainWindow', '&User Guide'))
        self.HelpAboutItem.setText(translate('OpenLP.MainWindow', '&About'))
        self.HelpAboutItem.setStatusTip(
            translate('OpenLP.MainWindow', 'More information about OpenLP'))
        self.HelpAboutItem.setShortcut(
            translate('OpenLP.MainWindow', 'Ctrl+F1'))
        self.HelpOnlineHelpItem.setText(
            translate('OpenLP.MainWindow', '&Online Help'))
        self.helpWebSiteItem.setText(
            translate('OpenLP.MainWindow', '&Web Site'))
        self.AutoLanguageItem.setText(
            translate('OpenLP.MainWindow', '&Auto Detect'))
        self.AutoLanguageItem.setStatusTip(translate('OpenLP.MainWindow',
            'Use the system language, if available.'))
        for item in self.LanguageGroup.actions():
            item.setText(item.objectName())
            item.setStatusTip(unicode(translate('OpenLP.MainWindow',
                'Set the interface language to %s')) % item.objectName())
        self.ToolsAddToolItem.setText(
            translate('OpenLP.MainWindow', 'Add &Tool...'))
        self.ToolsAddToolItem.setStatusTip(translate('OpenLP.MainWindow',
            'Add an application to the list of tools.'))
        self.ToolsOpenDataFolder.setText(
            translate('OpenLP.MainWindow', 'Open &Data Folder...'))
        self.ToolsOpenDataFolder.setStatusTip(translate('OpenLP.MainWindow',
            'Open the folder where songs, bibles and other data resides.'))
        self.ModeDefaultItem.setText(
            translate('OpenLP.MainWindow', '&Default'))
        self.ModeDefaultItem.setStatusTip(translate('OpenLP.MainWindow',
            'Set the view mode back to the default.'))
        self.ModeSetupItem.setText(translate('OpenLP.MainWindow', '&Setup'))
        self.ModeSetupItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Set the view mode to Setup.'))
        self.ModeLiveItem.setText(translate('OpenLP.MainWindow', '&Live'))
        self.ModeLiveItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Set the view mode to Live.'))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    The main window.
    """
    log.info(u'MainWindow loaded')

    actionList = ActionList()

    def __init__(self, screens, applicationVersion, clipboard, firstTime):
        """
        This constructor sets up the interface, the various managers, and the
        plugins.
        """
        QtGui.QMainWindow.__init__(self)
        self.screens = screens
        self.actionList = ActionList()
        self.applicationVersion = applicationVersion
        self.clipboard = clipboard
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
        self.displayTagForm = DisplayTagForm(self)
        self.shortcutForm = ShortcutListForm(self)
        self.recentFiles = QtCore.QStringList()
        # Set up the path with plugins
        pluginpath = AppLocation.get_directory(AppLocation.PluginsDir)
        self.pluginManager = PluginManager(pluginpath)
        self.pluginHelpers = {}
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
            self.themeManagerContents.onImportTheme)
        QtCore.QObject.connect(self.ExportThemeItem,
            QtCore.SIGNAL(u'triggered()'),
            self.themeManagerContents.onExportTheme)
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
        QtCore.QObject.connect(self.mediaManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.ViewMediaManagerItem.setChecked)
        QtCore.QObject.connect(self.serviceManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.ViewServiceManagerItem.setChecked)
        QtCore.QObject.connect(self.themeManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.ViewThemeManagerItem.setChecked)
        QtCore.QObject.connect(self.helpWebSiteItem,
            QtCore.SIGNAL(u'triggered()'), self.onHelpWebSiteClicked)
        QtCore.QObject.connect(self.HelpAboutItem,
            QtCore.SIGNAL(u'triggered()'), self.onHelpAboutItemClicked)
        QtCore.QObject.connect(self.ToolsOpenDataFolder,
            QtCore.SIGNAL(u'triggered()'), self.onToolsOpenDataFolderClicked)
        QtCore.QObject.connect(self.settingsPluginListItem,
            QtCore.SIGNAL(u'triggered()'), self.onPluginItemClicked)
        QtCore.QObject.connect(self.DisplayTagItem,
            QtCore.SIGNAL(u'triggered()'), self.onDisplayTagItemClicked)
        QtCore.QObject.connect(self.SettingsConfigureItem,
            QtCore.SIGNAL(u'triggered()'), self.onSettingsConfigureItemClicked)
        QtCore.QObject.connect(self.SettingsShortcutsItem,
            QtCore.SIGNAL(u'triggered()'), self.onSettingsShortcutsItemClicked)
        QtCore.QObject.connect(self.FileNewItem, QtCore.SIGNAL(u'triggered()'),
            self.ServiceManagerContents.onNewServiceClicked)
        QtCore.QObject.connect(self.FileOpenItem,
            QtCore.SIGNAL(u'triggered()'),
            self.ServiceManagerContents.onLoadServiceClicked)
        QtCore.QObject.connect(self.FileSaveItem,
            QtCore.SIGNAL(u'triggered()'),
            self.ServiceManagerContents.saveFile)
        QtCore.QObject.connect(self.FileSaveAsItem,
            QtCore.SIGNAL(u'triggered()'),
            self.ServiceManagerContents.saveFileAs)
        QtCore.QObject.connect(self.printServiceOrderItem,
            QtCore.SIGNAL(u'triggered()'),
            self.ServiceManagerContents.printServiceOrder)
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
        Receiver.send_message(u'cursor_busy')
        # Simple message boxes
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_error_message'), self.onErrorMessage)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_warning_message'), self.onWarningMessage)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_information_message'),
            self.onInformationMessage)
        # warning cyclic dependency
        # RenderManager needs to call ThemeManager and
        # ThemeManager needs to call RenderManager
        self.renderManager = RenderManager(
            self.themeManagerContents, self.screens)
        # Define the media Dock Manager
        self.mediaDockManager = MediaDockManager(self.MediaToolBox)
        log.info(u'Load Plugins')
        # make the controllers available to the plugins
        self.pluginHelpers[u'preview'] = self.previewController
        self.pluginHelpers[u'live'] = self.liveController
        self.pluginHelpers[u'render'] = self.renderManager
        self.pluginHelpers[u'service'] = self.ServiceManagerContents
        self.pluginHelpers[u'settings form'] = self.settingsForm
        self.pluginHelpers[u'toolbox'] = self.mediaDockManager
        self.pluginHelpers[u'pluginmanager'] = self.pluginManager
        self.pluginHelpers[u'formparent'] = self
        self.pluginManager.find_plugins(pluginpath, self.pluginHelpers)
        # hook methods have to happen after find_plugins. Find plugins needs
        # the controllers hence the hooks have moved from setupUI() to here
        # Find and insert settings tabs
        log.info(u'hook settings')
        self.pluginManager.hook_settings_tabs(self.settingsForm)
        # Find and insert media manager items
        log.info(u'hook media')
        self.pluginManager.hook_media_manager(self.mediaDockManager)
        # Call the hook method to pull in import menus.
        log.info(u'hook menus')
        self.pluginManager.hook_import_menu(self.FileImportMenu)
        # Call the hook method to pull in export menus.
        self.pluginManager.hook_export_menu(self.FileExportMenu)
        # Call the hook method to pull in tools menus.
        self.pluginManager.hook_tools_menu(self.ToolsMenu)
        # Call the initialise method to setup plugins.
        log.info(u'initialise plugins')
        self.pluginManager.initialise_plugins()
        # Once all components are initialised load the Themes
        log.info(u'Load Themes')
        self.themeManagerContents.loadThemes()
        log.info(u'Load data from Settings')
        if QtCore.QSettings().value(u'advanced/save current plugin',
            QtCore.QVariant(False)).toBool():
            savedPlugin = QtCore.QSettings().value(
                u'advanced/current media plugin', QtCore.QVariant()).toInt()[0]
            if savedPlugin != -1:
                self.MediaToolBox.setCurrentIndex(savedPlugin)
        self.settingsForm.postSetUp()
        Receiver.send_message(u'cursor_normal')
        # Import themes if first time
        if firstTime:
            self.themeManagerContents.firstTime()


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
        if self.liveController.display.isVisible():
            self.liveController.display.setFocus()
        self.activateWindow()
        if QtCore.QSettings().value(
            self.generalSettingsSection + u'/auto open',
            QtCore.QVariant(False)).toBool():
            self.ServiceManagerContents.loadLastFile()
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
            self.liveController.mainDisplaySetBackground()
            if settings.value(u'blank warning',
                QtCore.QVariant(False)).toBool():
                QtGui.QMessageBox.question(self,
                    translate('OpenLP.MainWindow',
                        'OpenLP Main Display Blanked'),
                    translate('OpenLP.MainWindow',
                         'The Main Display has been blanked out'))

    def onErrorMessage(self, data):
        QtGui.QMessageBox.critical(self, data[u'title'], data[u'message'])

    def onWarningMessage(self, data):
        QtGui.QMessageBox.warning(self, data[u'title'], data[u'message'])

    def onInformationMessage(self, data):
        QtGui.QMessageBox.information(self, data[u'title'], data[u'message'])

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

    def onToolsOpenDataFolderClicked(self):
        """
        Open data folder
        """
        path = AppLocation.get_data_path()
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file:///" + path))

    def onDisplayTagItemClicked(self):
        """
        Show the Settings dialog
        """
        self.displayTagForm.exec_()

    def onSettingsConfigureItemClicked(self):
        """
        Show the Settings dialog
        """
        self.settingsForm.exec_()

    def paintEvent(self, event):
        """
        We need to make sure, that the SlidePreview's size is correct.
        """
        self.previewController.previewSizeChanged()
        self.liveController.previewSizeChanged()

    def onSettingsShortcutsItemClicked(self):
        """
        Show the shortcuts dialog
        """
        self.shortcutForm.exec_(self.actionList)

    def onModeDefaultItemClicked(self):
        """
        Put OpenLP into "Default" view mode.
        """
        self.setViewMode(True, True, True, True, True, u'default')

    def onModeSetupItemClicked(self):
        """
        Put OpenLP into "Setup" view mode.
        """
        self.setViewMode(True, True, False, True, False, u'setup')

    def onModeLiveItemClicked(self):
        """
        Put OpenLP into "Live" view mode.
        """
        self.setViewMode(False, True, False, False, True, u'live')

    def setViewMode(self, media=True, service=True, theme=True, preview=True,
        live=True, mode=u''):
        """
        Set OpenLP to a different view mode.
        """
        if mode:
            settings = QtCore.QSettings()
            settings.setValue(u'%s/view mode' % self.generalSettingsSection,
                mode)
        self.mediaManagerDock.setVisible(media)
        self.serviceManagerDock.setVisible(service)
        self.themeManagerDock.setVisible(theme)
        self.setPreviewPanelVisibility(preview)
        self.setLivePanelVisibility(live)

    def screenChanged(self):
        """
        The screen has changed to so tell the displays to update_display
        their locations
        """
        log.debug(u'screenChanged')
        self.renderManager.update_display()
        self.setFocus()
        self.activateWindow()

    def closeEvent(self, event):
        """
        Hook to close the main window and display windows on exit
        """
        if self.ServiceManagerContents.isModified():
            ret = self.ServiceManagerContents.saveModifiedService()
            if ret == QtGui.QMessageBox.Save:
                if self.ServiceManagerContents.saveFile():
                    self.cleanUp()
                    event.accept()
                else:
                    event.ignore()
            elif ret == QtGui.QMessageBox.Discard:
                self.cleanUp()
                event.accept()
            else:
                event.ignore()
        else:
            if QtCore.QSettings().value(u'advanced/enable exit confirmation',
                QtCore.QVariant(True)).toBool():
                ret = QtGui.QMessageBox.question(self,
                    translate('OpenLP.MainWindow', 'Close OpenLP'),
                    translate('OpenLP.MainWindow',
                        'Are you sure you want to close OpenLP?'),
                    QtGui.QMessageBox.StandardButtons(
                        QtGui.QMessageBox.Yes |
                        QtGui.QMessageBox.No),
                    QtGui.QMessageBox.Yes)
                if ret == QtGui.QMessageBox.Yes:
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
        self.pluginManager.finalise_plugins()
        # Save settings
        self.saveSettings()
        # Close down the display
        self.liveController.display.close()

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

    def setServiceModified(self, modified, fileName):
        """
        This method is called from the ServiceManager to set the title of the
        main window.

        ``modified``
            Whether or not this service has been modified.

        ``fileName``
            The file name of the service file.
        """
        if modified:
            title = u'%s - %s*' % (self.mainTitle, fileName)
        else:
            title = u'%s - %s' % (self.mainTitle, fileName)
        self.setWindowTitle(title)

    def showStatusMessage(self, message):
        self.StatusBar.showMessage(message)

    def defaultThemeChanged(self, theme):
        self.DefaultThemeLabel.setText(
            unicode(translate('OpenLP.MainWindow', 'Default Theme: %s')) %
                theme)

    def toggleMediaManager(self, visible):
        if self.mediaManagerDock.isVisible() != visible:
            self.mediaManagerDock.setVisible(visible)

    def toggleServiceManager(self, visible):
        if self.serviceManagerDock.isVisible() != visible:
            self.serviceManagerDock.setVisible(visible)

    def toggleThemeManager(self, visible):
        if self.themeManagerDock.isVisible() != visible:
            self.themeManagerDock.setVisible(visible)

    def setPreviewPanelVisibility(self, visible):
        """
        Sets the visibility of the preview panel including saving the setting
        and updating the menu.

        ``visible``
            A bool giving the state to set the panel to
                True - Visible
                False - Hidden
        """
        self.previewController.panel.setVisible(visible)
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
        self.liveController.panel.setVisible(visible)
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
        existingRecentFiles = [recentFile for recentFile in self.recentFiles
            if QtCore.QFile.exists(recentFile)]
        recentFilesToDisplay = existingRecentFiles[0:recentFileCount]
        if recentFilesToDisplay:
            self.FileMenu.addSeparator()
            for fileId, filename in enumerate(recentFilesToDisplay):
                log.debug('Recent file name: %s', filename)
                action = QtGui.QAction(u'&%d %s' % (fileId + 1,
                    QtCore.QFileInfo(filename).fileName()), self)
                action.setData(QtCore.QVariant(filename))
                self.connect(action, QtCore.SIGNAL(u'triggered()'),
                    self.ServiceManagerContents.onRecentServiceClicked)
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
        # actually stored in the settings therefore the default value of 20 will
        # always be used.
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
