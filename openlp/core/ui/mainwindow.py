# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
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

import logging
import os
from tempfile import gettempdir

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Renderer, build_icon, OpenLPDockWidget, \
    PluginManager, Receiver, translate, ImageManager
from openlp.core.lib.ui import UiStrings, base_action, checkable_action, \
    icon_action, shortcut_action
from openlp.core.ui import AboutForm, SettingsForm, ServiceManager, \
    ThemeManager, SlideController, PluginForm, MediaDockManager, \
    ShortcutListForm, DisplayTagForm
from openlp.core.utils import AppLocation, add_actions, LanguageManager, \
    get_application_version, delete_file
from openlp.core.utils.actions import ActionList, CategoryOrder

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
        mainWindow.setWindowIcon(build_icon(u':/icon/openlp-logo-64x64.png'))
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
        self.previewController = SlideController(self)
        self.liveController = SlideController(self, True)
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
        self.statusBar = QtGui.QStatusBar(mainWindow)
        self.statusBar.setObjectName(u'statusBar')
        mainWindow.setStatusBar(self.statusBar)
        self.loadProgressBar = QtGui.QProgressBar(self.statusBar)
        self.loadProgressBar.setObjectName(u'loadProgressBar')
        self.statusBar.addPermanentWidget(self.loadProgressBar)
        self.loadProgressBar.hide()
        self.loadProgressBar.setValue(0)
        self.defaultThemeLabel = QtGui.QLabel(self.statusBar)
        self.defaultThemeLabel.setObjectName(u'defaultThemeLabel')
        self.statusBar.addPermanentWidget(self.defaultThemeLabel)
        # Create the MediaManager
        self.mediaManagerDock = OpenLPDockWidget(mainWindow,
            u'mediaManagerDock', u':/system/system_mediamanager.png')
        self.mediaManagerDock.setStyleSheet(MEDIA_MANAGER_STYLE)
        # Create the media toolbox
        self.MediaToolBox = QtGui.QToolBox(self.mediaManagerDock)
        self.MediaToolBox.setObjectName(u'MediaToolBox')
        self.mediaManagerDock.setWidget(self.MediaToolBox)
        mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
            self.mediaManagerDock)
        # Create the service manager
        self.serviceManagerDock = OpenLPDockWidget(mainWindow,
            u'serviceManagerDock', u':/system/system_servicemanager.png')
        self.ServiceManagerContents = ServiceManager(mainWindow,
            self.serviceManagerDock)
        self.serviceManagerDock.setWidget(self.ServiceManagerContents)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea,
            self.serviceManagerDock)
        # Create the theme manager
        self.themeManagerDock = OpenLPDockWidget(mainWindow,
            u'themeManagerDock', u':/system/system_thememanager.png')
        self.themeManagerContents = ThemeManager(mainWindow,
            self.themeManagerDock)
        self.themeManagerContents.setObjectName(u'themeManagerContents')
        self.themeManagerDock.setWidget(self.themeManagerContents)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea,
            self.themeManagerDock)
        # Create the menu items
        action_list = ActionList.get_instance()
        action_list.add_category(UiStrings().File, CategoryOrder.standardMenu)
        self.FileNewItem = shortcut_action(mainWindow, u'FileNewItem',
            [QtGui.QKeySequence(u'Ctrl+N')],
            self.ServiceManagerContents.onNewServiceClicked,
            u':/general/general_new.png', category=UiStrings().File)
        self.FileOpenItem = shortcut_action(mainWindow, u'FileOpenItem',
            [QtGui.QKeySequence(u'Ctrl+O')],
            self.ServiceManagerContents.onLoadServiceClicked,
            u':/general/general_open.png', category=UiStrings().File)
        self.FileSaveItem = shortcut_action(mainWindow, u'FileSaveItem',
            [QtGui.QKeySequence(u'Ctrl+S')],
            self.ServiceManagerContents.saveFile,
            u':/general/general_save.png', category=UiStrings().File)
        self.FileSaveAsItem = shortcut_action(mainWindow, u'FileSaveAsItem',
            [QtGui.QKeySequence(u'Ctrl+Shift+S')],
            self.ServiceManagerContents.saveFileAs, category=UiStrings().File)
        self.printServiceOrderItem = shortcut_action(mainWindow,
            u'printServiceItem', [QtGui.QKeySequence(u'Ctrl+P')],
            self.ServiceManagerContents.printServiceOrder,
            category=UiStrings().File)
        self.FileExitItem = shortcut_action(mainWindow, u'FileExitItem',
            [QtGui.QKeySequence(u'Alt+F4')], mainWindow.close,
            u':/system/system_exit.png', category=UiStrings().File)
        action_list.add_category(UiStrings().Import, CategoryOrder.standardMenu)
        self.ImportThemeItem = base_action(
            mainWindow, u'ImportThemeItem', UiStrings().Import)
        self.ImportLanguageItem = base_action(
            mainWindow, u'ImportLanguageItem')#, UiStrings().Import)
        action_list.add_category(UiStrings().Export, CategoryOrder.standardMenu)
        self.ExportThemeItem = base_action(
            mainWindow, u'ExportThemeItem', UiStrings().Export)
        self.ExportLanguageItem = base_action(
            mainWindow, u'ExportLanguageItem')#, UiStrings().Export)
        action_list.add_category(UiStrings().View, CategoryOrder.standardMenu)
        self.ViewMediaManagerItem = shortcut_action(mainWindow,
            u'ViewMediaManagerItem', [QtGui.QKeySequence(u'F8')],
            self.toggleMediaManager, u':/system/system_mediamanager.png',
            self.mediaManagerDock.isVisible(), UiStrings().View)
        self.ViewThemeManagerItem = shortcut_action(mainWindow,
            u'ViewThemeManagerItem', [QtGui.QKeySequence(u'F10')],
            self.toggleThemeManager,  u':/system/system_thememanager.png',
            self.themeManagerDock.isVisible(), UiStrings().View)
        self.ViewServiceManagerItem = shortcut_action(mainWindow,
            u'ViewServiceManagerItem', [QtGui.QKeySequence(u'F9')],
            self.toggleServiceManager, u':/system/system_servicemanager.png',
            self.serviceManagerDock.isVisible(), UiStrings().View)
        self.ViewPreviewPanel = shortcut_action(mainWindow,
            u'ViewPreviewPanel', [QtGui.QKeySequence(u'F11')],
            self.setPreviewPanelVisibility, checked=previewVisible,
            category=UiStrings().View)
        self.ViewLivePanel = shortcut_action(mainWindow, u'ViewLivePanel',
            [QtGui.QKeySequence(u'F12')], self.setLivePanelVisibility,
            checked=liveVisible, category=UiStrings().View)
        action_list.add_category(UiStrings().ViewMode, CategoryOrder.standardMenu)
        self.ModeDefaultItem = checkable_action(
            mainWindow, u'ModeDefaultItem', category=UiStrings().ViewMode)
        self.ModeSetupItem = checkable_action(
            mainWindow, u'ModeLiveItem', category=UiStrings().ViewMode)
        self.ModeLiveItem = checkable_action(
            mainWindow, u'ModeLiveItem', True, UiStrings().ViewMode)
        self.ModeGroup = QtGui.QActionGroup(mainWindow)
        self.ModeGroup.addAction(self.ModeDefaultItem)
        self.ModeGroup.addAction(self.ModeSetupItem)
        self.ModeGroup.addAction(self.ModeLiveItem)
        self.ModeDefaultItem.setChecked(True)
        action_list.add_category(UiStrings().Tools, CategoryOrder.standardMenu)
        self.ToolsAddToolItem = icon_action(mainWindow, u'ToolsAddToolItem',
            u':/tools/tools_add.png', category=UiStrings().Tools)
        self.ToolsOpenDataFolder = icon_action(mainWindow,
            u'ToolsOpenDataFolder', u':/general/general_open.png',
            category=UiStrings().Tools)
        action_list.add_category(UiStrings().Settings, CategoryOrder.standardMenu)
        self.settingsPluginListItem = shortcut_action(mainWindow,
            u'settingsPluginListItem', [QtGui.QKeySequence(u'Alt+F7')],
            self.onPluginItemClicked, u':/system/settings_plugin_list.png',
            category=UiStrings().Settings)
        # i18n Language Items
        self.AutoLanguageItem = checkable_action(mainWindow,
            u'AutoLanguageItem', LanguageManager.auto_language)
        self.LanguageGroup = QtGui.QActionGroup(mainWindow)
        self.LanguageGroup.setExclusive(True)
        self.LanguageGroup.setObjectName(u'LanguageGroup')
        add_actions(self.LanguageGroup, [self.AutoLanguageItem])
        qmList = LanguageManager.get_qm_list()
        savedLanguage = LanguageManager.get_language()
        for key in sorted(qmList.keys()):
            languageItem = checkable_action(
                mainWindow, key, qmList[key] == savedLanguage)
            add_actions(self.LanguageGroup, [languageItem])
        self.SettingsShortcutsItem = icon_action(mainWindow,
            u'SettingsShortcutsItem',
            u':/system/system_configure_shortcuts.png',
            category=UiStrings().Settings)
        self.DisplayTagItem = icon_action(mainWindow,
            u'DisplayTagItem', u':/system/tag_editor.png',
            category=UiStrings().Settings)
        self.SettingsConfigureItem = icon_action(mainWindow,
            u'SettingsConfigureItem', u':/system/system_settings.png',
            category=UiStrings().Settings)
        action_list.add_category(UiStrings().Help, CategoryOrder.standardMenu)
        self.HelpDocumentationItem = icon_action(mainWindow,
            u'HelpDocumentationItem', u':/system/system_help_contents.png',
            category=None)#UiStrings().Help)
        self.HelpDocumentationItem.setEnabled(False)
        self.HelpAboutItem = shortcut_action(mainWindow, u'HelpAboutItem',
            [QtGui.QKeySequence(u'Ctrl+F1')], self.onHelpAboutItemClicked,
            u':/system/system_about.png', category=UiStrings().Help)
        self.HelpOnlineHelpItem = base_action(
            mainWindow, u'HelpOnlineHelpItem', category=UiStrings().Help)
        self.helpWebSiteItem = base_action(
            mainWindow, u'helpWebSiteItem', category=UiStrings().Help)
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
        QtCore.QMetaObject.connectSlotsByName(mainWindow)
        # Hide the entry, as it does not have any functionality yet.
        self.ToolsAddToolItem.setVisible(False)
        self.ImportLanguageItem.setVisible(False)
        self.ExportLanguageItem.setVisible(False)
        self.HelpDocumentationItem.setVisible(False)

    def retranslateUi(self, mainWindow):
        """
        Set up the translation system
        """
        mainWindow.mainTitle = UiStrings().OLPV2
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
        self.FileNewItem.setToolTip(UiStrings().NewService)
        self.FileNewItem.setStatusTip(UiStrings().CreateService)
        self.FileOpenItem.setText(translate('OpenLP.MainWindow', '&Open'))
        self.FileOpenItem.setToolTip(UiStrings().OpenService)
        self.FileOpenItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Open an existing service.'))
        self.FileSaveItem.setText(translate('OpenLP.MainWindow', '&Save'))
        self.FileSaveItem.setToolTip(UiStrings().SaveService)
        self.FileSaveItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Save the current service to disk.'))
        self.FileSaveAsItem.setText(
            translate('OpenLP.MainWindow', 'Save &As...'))
        self.FileSaveAsItem.setToolTip(
            translate('OpenLP.MainWindow', 'Save Service As'))
        self.FileSaveAsItem.setStatusTip(translate('OpenLP.MainWindow',
            'Save the current service under a new name.'))
        self.printServiceOrderItem.setText(UiStrings().PrintServiceOrder)
        self.printServiceOrderItem.setStatusTip(translate('OpenLP.MainWindow',
            'Print the current Service Order.'))
        self.FileExitItem.setText(
            translate('OpenLP.MainWindow', 'E&xit'))
        self.FileExitItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Quit OpenLP'))
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
        self.ViewThemeManagerItem.setText(
            translate('OpenLP.MainWindow', '&Theme Manager'))
        self.ViewThemeManagerItem.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Theme Manager'))
        self.ViewThemeManagerItem.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the theme manager.'))
        self.ViewServiceManagerItem.setText(
            translate('OpenLP.MainWindow', '&Service Manager'))
        self.ViewServiceManagerItem.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Service Manager'))
        self.ViewServiceManagerItem.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the service manager.'))
        self.ViewPreviewPanel.setText(
            translate('OpenLP.MainWindow', '&Preview Panel'))
        self.ViewPreviewPanel.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Preview Panel'))
        self.ViewPreviewPanel.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the preview panel.'))
        self.ViewLivePanel.setText(
            translate('OpenLP.MainWindow', '&Live Panel'))
        self.ViewLivePanel.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Live Panel'))
        self.ViewLivePanel.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the live panel.'))
        self.settingsPluginListItem.setText(translate('OpenLP.MainWindow',
            '&Plugin List'))
        self.settingsPluginListItem.setStatusTip(
            translate('OpenLP.MainWindow', 'List the Plugins'))
        self.HelpDocumentationItem.setText(
            translate('OpenLP.MainWindow', '&User Guide'))
        self.HelpAboutItem.setText(translate('OpenLP.MainWindow', '&About'))
        self.HelpAboutItem.setStatusTip(
            translate('OpenLP.MainWindow', 'More information about OpenLP'))
        self.HelpOnlineHelpItem.setText(
            translate('OpenLP.MainWindow', '&Online Help'))
        # Uncomment after 1.9.5 beta string freeze
        #self.HelpOnlineHelpItem.setShortcut(
        #    translate('OpenLP.MainWindow', 'F1'))
        self.helpWebSiteItem.setText(
            translate('OpenLP.MainWindow', '&Web Site'))
        for item in self.LanguageGroup.actions():
            item.setText(item.objectName())
            item.setStatusTip(unicode(translate('OpenLP.MainWindow',
                'Set the interface language to %s')) % item.objectName())
        self.AutoLanguageItem.setText(
            translate('OpenLP.MainWindow', '&Autodetect'))
        self.AutoLanguageItem.setStatusTip(translate('OpenLP.MainWindow',
            'Use the system language, if available.'))
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

    def __init__(self, clipboard, arguments):
        """
        This constructor sets up the interface, the various managers, and the
        plugins.
        """
        QtGui.QMainWindow.__init__(self)
        self.clipboard = clipboard
        self.arguments = arguments
        # Set up settings sections for the main application
        # (not for use by plugins)
        self.uiSettingsSection = u'user interface'
        self.generalSettingsSection = u'general'
        self.serviceSettingsSection = u'servicemanager'
        self.songsSettingsSection = u'songs'
        self.serviceNotSaved = False
        self.aboutForm = AboutForm(self)
        self.settingsForm = SettingsForm(self, self)
        self.displayTagForm = DisplayTagForm(self)
        self.shortcutForm = ShortcutListForm(self)
        self.recentFiles = QtCore.QStringList()
        # Set up the path with plugins
        pluginpath = AppLocation.get_directory(AppLocation.PluginsDir)
        self.pluginManager = PluginManager(pluginpath)
        self.pluginHelpers = {}
        self.image_manager = ImageManager()
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
        QtCore.QObject.connect(self.HelpOnlineHelpItem,
            QtCore.SIGNAL(u'triggered()'), self.onHelpOnLineHelpClicked)
        QtCore.QObject.connect(self.ToolsOpenDataFolder,
            QtCore.SIGNAL(u'triggered()'), self.onToolsOpenDataFolderClicked)
        QtCore.QObject.connect(self.DisplayTagItem,
            QtCore.SIGNAL(u'triggered()'), self.onDisplayTagItemClicked)
        QtCore.QObject.connect(self.SettingsConfigureItem,
            QtCore.SIGNAL(u'triggered()'), self.onSettingsConfigureItemClicked)
        QtCore.QObject.connect(self.SettingsShortcutsItem,
            QtCore.SIGNAL(u'triggered()'), self.onSettingsShortcutsItemClicked)
        # i18n set signals for languages
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
        # renderer needs to call ThemeManager and
        # ThemeManager needs to call Renderer
        self.renderer = Renderer(self.image_manager, self.themeManagerContents)
        # Define the media Dock Manager
        self.mediaDockManager = MediaDockManager(self.MediaToolBox)
        log.info(u'Load Plugins')
        # make the controllers available to the plugins
        self.pluginHelpers[u'preview'] = self.previewController
        self.pluginHelpers[u'live'] = self.liveController
        self.pluginHelpers[u'renderer'] = self.renderer
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
        # Create the displays as all necessary components are loaded.
        self.previewController.screenSizeChanged()
        self.liveController.screenSizeChanged()
        log.info(u'Load data from Settings')
        if QtCore.QSettings().value(u'advanced/save current plugin',
            QtCore.QVariant(False)).toBool():
            savedPlugin = QtCore.QSettings().value(
                u'advanced/current media plugin', QtCore.QVariant()).toInt()[0]
            if savedPlugin != -1:
                self.MediaToolBox.setCurrentIndex(savedPlugin)
        self.settingsForm.postSetUp()
        # Once all components are initialised load the Themes
        log.info(u'Load Themes')
        self.themeManagerContents.loadThemes(True)
        Receiver.send_message(u'cursor_normal')

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
            version_text % (version, get_application_version()[u'full']))

    def show(self):
        """
        Show the main form, as well as the display form
        """
        QtGui.QWidget.show(self)
        if self.liveController.display.isVisible():
            self.liveController.display.setFocus()
        self.activateWindow()
        # On Windows, arguments contains the entire commandline
        # So args[0]=='python' args[1]=='openlp.pyw'
        # Therefore this approach is not going to work
        # Bypass for now.
        if len(self.arguments) and os.name != u'nt':
            args = []
            for a in self.arguments:
                args.extend([a])
            self.ServiceManagerContents.loadFile(unicode(args[0]))
        elif QtCore.QSettings().value(
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

    def firstTime(self):
        # Import themes if first time
        Receiver.send_message(u'openlp_process_events')
        for plugin in self.pluginManager.plugins:
            if hasattr(plugin, u'firstTime'):
                Receiver.send_message(u'openlp_process_events')
                plugin.firstTime()
        Receiver.send_message(u'openlp_process_events')
        temp_dir = os.path.join(unicode(gettempdir()), u'openlp')
        if not os.path.exists(temp_dir):
            return
        for filename in os.listdir(temp_dir):
            delete_file(os.path.join(temp_dir, filename))
        os.removedirs(temp_dir)

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

    def onHelpOnLineHelpClicked(self):
        """
        Load the online OpenLP manual
        """
        import webbrowser
        webbrowser.open_new(u'http://manual.openlp.org/')

    def onHelpAboutItemClicked(self):
        """
        Show the About form
        """
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
        if self.shortcutForm.exec_():
            self.shortcutForm.save()

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
        self.image_manager.update_display()
        self.renderer.update_display()
        self.liveController.screenSizeChanged()
        self.previewController.screenSizeChanged()
        self.themeManagerContents.updatePreviewImages()
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
        self.statusBar.showMessage(message)

    def defaultThemeChanged(self, theme):
        self.defaultThemeLabel.setText(
            unicode(translate('OpenLP.MainWindow', 'Default Theme: %s')) %
                theme)

    def toggleMediaManager(self):
        self.mediaManagerDock.setVisible(not self.mediaManagerDock.isVisible())

    def toggleServiceManager(self):
        self.serviceManagerDock.setVisible(not self.serviceManagerDock.isVisible())

    def toggleThemeManager(self):
        self.themeManagerDock.setVisible(not self.themeManagerDock.isVisible())

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
                action =  base_action(self, u'')
                action.setText(u'&%d %s' %
                    (fileId + 1, QtCore.QFileInfo(filename).fileName()))
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

    def displayProgressBar(self, size):
        """
        Make Progress bar visible and set size
        """
        self.loadProgressBar.show()
        self.loadProgressBar.setMaximum(size)
        self.loadProgressBar.setValue(0)
        Receiver.send_message(u'openlp_process_events')

    def incrementProgressBar(self):
        """
        Increase the Progress Bar value by 1
        """
        self.loadProgressBar.setValue(self.loadProgressBar.value() + 1)
        Receiver.send_message(u'openlp_process_events')

    def finishedProgressBar(self):
        """
        Trigger it's removal after 2.5 second
        """
        self.timer_id = self.startTimer(2500)

    def timerEvent(self, event):
        """
        Remove the Progress bar from view.
        """
        if event.timerId() == self.timer_id:
            self.timer_id = 0
            self.loadProgressBar.hide()
            Receiver.send_message(u'openlp_process_events')
