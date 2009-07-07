# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 - 2009 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import os
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.ui import AboutForm, SettingsForm, AlertForm, ServiceManager, \
    ThemeManager, MainDisplay, SlideController
from openlp.core.lib import translate, Plugin, MediaManagerItem, SettingsTab, \
    EventManager, RenderManager, PluginConfig
from openlp.core import PluginManager

class MainWindow(object):
    """
    The main window.
    """
    global log
    log = logging.getLogger(u'MainWindow')
    log.info(u'MainWindow loaded')

    def __init__(self, screens):
        """
        This constructor sets up the interface, the various managers, and the
        plugins.
        """
        self.oosNotSaved = False
        self.mainWindow = QtGui.QMainWindow()
        self.mainWindow.__class__.closeEvent = self.onCloseEvent
        self.mainDisplay = MainDisplay(None, screens)
        self.screenList = screens
        self.EventManager = EventManager()
        self.generalConfig = PluginConfig(u'General')
        self.alertForm = AlertForm(self)
        self.aboutForm = AboutForm()
        self.settingsForm = SettingsForm(self.screenList, self)
        # Set up the path with plugins
        pluginpath = os.path.split(os.path.abspath(__file__))[0]
        pluginpath = os.path.abspath(
            os.path.join(pluginpath, u'..', u'..', u'plugins'))
        self.plugin_manager = PluginManager(pluginpath)
        self.plugin_helpers = {}
        # Set up the interface
        self.setupUi()
        #warning cyclic dependency
        #RenderManager needs to call ThemeManager and
        #ThemeManager needs to call RenderManager
        self.RenderManager = RenderManager(self.ThemeManagerContents,
            self.screenList, int(self.generalConfig.get_config(u'Monitor', 0)))
        log.info(u'Load Plugins')
        #make the controllers available to the plugins
        self.plugin_helpers[u'preview'] = self.PreviewController
        self.plugin_helpers[u'live'] = self.LiveController
        self.plugin_helpers[u'event'] = self.EventManager
        self.plugin_helpers[u'theme'] = self.ThemeManagerContents
        self.plugin_helpers[u'render'] = self.RenderManager
        self.plugin_helpers[u'service'] = self.ServiceManagerContents
        self.plugin_helpers[u'settings'] = self.settingsForm
        self.plugin_manager.find_plugins(pluginpath, self.plugin_helpers,
            self.EventManager)
        # hook methods have to happen after find_plugins. Find plugins needs the
        # controllers hence the hooks have moved from setupUI() to here

        # Find and insert settings tabs
        log.info(u'hook settings')
        self.plugin_manager.hook_settings_tabs(self.settingsForm)
        # Find and insert media manager items
        log.info(u'hook media')
        self.plugin_manager.hook_media_manager(self.MediaToolBox)
        # Call the hook method to pull in import menus.
        log.info(u'hook menus')
        self.plugin_manager.hook_import_menu(self.FileImportMenu)
        # Call the hook method to pull in export menus.
        self.plugin_manager.hook_export_menu(self.FileExportMenu)
        # Call the initialise method to setup plugins.
        log.info(u'initialise plugins')
        self.plugin_manager.initialise_plugins()
        # Once all components are initialised load the Themes
        log.info(u'Load Themes')
        self.ThemeManagerContents.loadThemes()

    def show(self):
        """
        Show the main form, as well as the display form
        """
        self.mainWindow.showMaximized()
        self.mainDisplay.setup(self.settingsForm.GeneralTab.MonitorNumber)

    def onHelpAboutItemClicked(self):
        """
        Show the About form
        """
        self.aboutForm.exec_()

    def onToolsAlertItemClicked(self):
        """
        Show the Alert form
        """
        self.alertForm.exec_()

    def onOptionsSettingsItemClicked(self):
        """
        Show the Settings dialog
        """
        self.settingsForm.exec_()
        screen_number = int(self.generalConfig.get_config(u'Monitor', 0))
        self.RenderManager.update_display(screen_number)
        self.mainDisplay.setup(screen_number)

    def onCloseEvent(self, event):
        """
        Hook to close the main window and display windows on exit
        """
        if self.oosNotSaved == True:
            box = QtGui.QMessageBox()
            box.setWindowTitle(translate(u'mainWindow', u'Question?'))
            box.setText(translate(u'mainWindow', u'Save changes to Order of Service?'))
            box.setIcon(QtGui.QMessageBox.Question)
            box.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel);
            box.setDefaultButton(QtGui.QMessageBox.Save);
            ret = box.exec_()
            if ret == QtGui.QMessageBox.Save:
                self.ServiceManagerContents.onSaveService()
                self.mainDisplay.close()
                event.accept()
            elif ret == QtGui.QMessageBox.Discard:
                self.mainDisplay.close()
                event.accept()
            else:
                event.ignore()
        else:
            self.mainDisplay.close()
            event.accept()

    def OosChanged(self, reset = False, oosName = None):
        """
        Hook to change the title if the OOS has been changed
        reset - tells if the OOS has been cleared or saved
        oosName - is the name of the OOS (if it has one)
        """
        if reset == True:
            self.oosNotSaved = False
            if oosName is None:
                title = self.mainTitle
            else:
                title = self.mainTitle + u' - (' + oosName + u')'
        else:
            self.oosNotSaved = True
            if oosName is None:
                title = self.mainTitle + u' - *'
            else:
                title = self.mainTitle + u' - *(' + oosName + u')'
        self.mainWindow.setWindowTitle(title)

    def setupUi(self):
        """
        Set up the user interface
        """
        self.mainWindow.setObjectName(u'mainWindow')
        self.mainWindow.resize(1087, 847)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainWindow.sizePolicy().hasHeightForWidth())
        self.mainWindow.setSizePolicy(sizePolicy)
        main_icon = QtGui.QIcon()
        main_icon.addPixmap(QtGui.QPixmap(u':/icon/openlp-logo-16x16.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainWindow.setWindowIcon(main_icon)
        # Set up the main container, which contains all the other form widgets
        self.MainContent = QtGui.QWidget(self.mainWindow)
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
        self.mainWindow.setCentralWidget(self.MainContent)
        self.ControlSplitter = QtGui.QSplitter(self.MainContent)
        self.ControlSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.ControlSplitter.setObjectName(u'ControlSplitter')
        self.MainContentLayout.addWidget(self.ControlSplitter)
        # Create slide controllers
        self.PreviewController = SlideController(self)
        self.LiveController = SlideController(self, True)
        # Create menu
        self.MenuBar = QtGui.QMenuBar(self.mainWindow)
        self.MenuBar.setGeometry(QtCore.QRect(0, 0, 1087, 27))
        self.MenuBar.setObjectName(u'MenuBar')
        self.FileMenu = QtGui.QMenu(self.MenuBar)
        self.FileMenu.setObjectName(u'FileMenu')
        self.FileImportMenu = QtGui.QMenu(self.FileMenu)
        self.FileImportMenu.setObjectName(u'FileImportMenu')
        self.FileExportMenu = QtGui.QMenu(self.FileMenu)
        self.FileExportMenu.setObjectName(u'FileExportMenu')
        self.OptionsMenu = QtGui.QMenu(self.MenuBar)
        self.OptionsMenu.setObjectName(u'OptionsMenu')
        self.OptionsViewMenu = QtGui.QMenu(self.OptionsMenu)
        self.OptionsViewMenu.setObjectName(u'OptionsViewMenu')
        self.ViewModeMenu = QtGui.QMenu(self.OptionsViewMenu)
        self.ViewModeMenu.setObjectName(u'ViewModeMenu')
        self.OptionsLanguageMenu = QtGui.QMenu(self.OptionsMenu)
        self.OptionsLanguageMenu.setObjectName(u'OptionsLanguageMenu')
        self.ToolsMenu = QtGui.QMenu(self.MenuBar)
        self.ToolsMenu.setObjectName(u'ToolsMenu')
        self.HelpMenu = QtGui.QMenu(self.MenuBar)
        self.HelpMenu.setObjectName(u'HelpMenu')
        self.mainWindow.setMenuBar(self.MenuBar)
        self.StatusBar = QtGui.QStatusBar(self.mainWindow)
        self.StatusBar.setObjectName(u'StatusBar')
        self.mainWindow.setStatusBar(self.StatusBar)
        # Create the MediaManager
        self.MediaManagerDock = QtGui.QDockWidget(self.mainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/system/system_mediamanager.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MediaManagerDock.setWindowIcon(icon)
        self.MediaManagerDock.setFloating(False)
        self.MediaManagerDock.setObjectName(u'MediaManagerDock')
        self.MediaManagerDock.setMinimumWidth(300)
        self.MediaManagerContents = QtGui.QWidget()
        self.MediaManagerContents.setObjectName(u'MediaManagerContents')
        self.MediaManagerLayout = QtGui.QHBoxLayout(self.MediaManagerContents)
        self.MediaManagerLayout.setContentsMargins(0, 2, 0, 0)
        self.MediaManagerLayout.setObjectName(u'MediaManagerLayout')
        self.MediaToolBox = QtGui.QToolBox(self.MediaManagerContents)
        self.MediaToolBox.setObjectName(u'MediaToolBox')
        self.MediaManagerLayout.addWidget(self.MediaToolBox)
        self.MediaManagerDock.setWidget(self.MediaManagerContents)
        self.mainWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(1), self.MediaManagerDock)
        # Create the service manager
        self.ServiceManagerDock = QtGui.QDockWidget(self.mainWindow)
        ServiceManagerIcon = QtGui.QIcon()
        ServiceManagerIcon.addPixmap(
            QtGui.QPixmap(u':/system/system_servicemanager.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ServiceManagerDock.setWindowIcon(ServiceManagerIcon)
        self.ServiceManagerDock.setFeatures(
            QtGui.QDockWidget.AllDockWidgetFeatures)
        self.ServiceManagerDock.setObjectName(u'ServiceManagerDock')
        self.ServiceManagerDock.setMinimumWidth(300)
        self.ServiceManagerContents = ServiceManager(self)
        self.ServiceManagerDock.setWidget(self.ServiceManagerContents)
        self.mainWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(2), self.ServiceManagerDock)
        # Create the theme manager
        self.ThemeManagerDock = QtGui.QDockWidget(self.mainWindow)
        ThemeManagerIcon = QtGui.QIcon()
        ThemeManagerIcon.addPixmap(
            QtGui.QPixmap(u':/system/system_thememanager.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ThemeManagerDock.setWindowIcon(ThemeManagerIcon)
        self.ThemeManagerDock.setFloating(False)
        self.ThemeManagerDock.setObjectName(u'ThemeManagerDock')
        self.ThemeManagerContents = ThemeManager(self)
        self.ThemeManagerDock.setWidget(self.ThemeManagerContents)
        self.mainWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(2), self.ThemeManagerDock)
        # Create the menu items
        self.FileNewItem = QtGui.QAction(self.mainWindow)
        self.FileNewItem.setIcon(
            self.ServiceManagerContents.Toolbar.getIconFromTitle(u'New Service'))
        self.FileNewItem.setObjectName(u'FileNewItem')
        self.FileOpenItem = QtGui.QAction(self.mainWindow)
        self.FileOpenItem.setIcon(
            self.ServiceManagerContents.Toolbar.getIconFromTitle(u'Open Service'))
        self.FileOpenItem.setObjectName(u'FileOpenItem')
        self.FileSaveItem = QtGui.QAction(self.mainWindow)
        self.FileSaveItem.setIcon(
            self.ServiceManagerContents.Toolbar.getIconFromTitle(u'Save Service'))
        self.FileSaveItem.setObjectName(u'FileSaveItem')
        self.FileSaveAsItem = QtGui.QAction(self.mainWindow)
        self.FileSaveAsItem.setObjectName(u'FileSaveAsItem')
        self.FileExitItem = QtGui.QAction(self.mainWindow)
        ExitIcon = QtGui.QIcon()
        ExitIcon.addPixmap(QtGui.QPixmap(u':/system/system_exit.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.FileExitItem.setIcon(ExitIcon)
        self.FileExitItem.setObjectName(u'FileExitItem')
        self.ImportThemeItem = QtGui.QAction(self.mainWindow)
        self.ImportThemeItem.setObjectName(u'ImportThemeItem')
        self.ImportLanguageItem = QtGui.QAction(self.mainWindow)
        self.ImportLanguageItem.setObjectName(u'ImportLanguageItem')
        self.ExportThemeItem = QtGui.QAction(self.mainWindow)
        self.ExportThemeItem.setObjectName(u'ExportThemeItem')
        self.ExportLanguageItem = QtGui.QAction(self.mainWindow)
        self.ExportLanguageItem.setObjectName(u'ExportLanguageItem')
        self.actionLook_Feel = QtGui.QAction(self.mainWindow)
        self.actionLook_Feel.setObjectName(u'actionLook_Feel')
        self.OptionsSettingsItem = QtGui.QAction(self.mainWindow)
        SettingsIcon = QtGui.QIcon()
        SettingsIcon.addPixmap(QtGui.QPixmap(u':/system/system_settings.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.OptionsSettingsItem.setIcon(SettingsIcon)
        self.OptionsSettingsItem.setObjectName(u'OptionsSettingsItem')
        self.ViewMediaManagerItem = QtGui.QAction(self.mainWindow)
        self.ViewMediaManagerItem.setCheckable(True)
        self.ViewMediaManagerItem.setChecked(True)
        self.ViewMediaManagerItem.setIcon(icon)
        self.ViewMediaManagerItem.setObjectName(u'ViewMediaManagerItem')
        self.ViewThemeManagerItem = QtGui.QAction(self.mainWindow)
        self.ViewThemeManagerItem.setCheckable(True)
        self.ViewThemeManagerItem.setChecked(True)
        self.ViewThemeManagerItem.setIcon(ThemeManagerIcon)
        self.ViewThemeManagerItem.setObjectName(u'ViewThemeManagerItem')
        self.ViewServiceManagerItem = QtGui.QAction(self.mainWindow)
        self.ViewServiceManagerItem.setCheckable(True)
        self.ViewServiceManagerItem.setChecked(True)
        self.ViewServiceManagerItem.setIcon(ServiceManagerIcon)
        self.ViewServiceManagerItem.setObjectName(u'ViewServiceManagerItem')
        self.ToolsAlertItem = QtGui.QAction(self.mainWindow)
        AlertIcon = QtGui.QIcon()
        AlertIcon.addPixmap(QtGui.QPixmap(u':/tools/tools_alert.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolsAlertItem.setIcon(AlertIcon)
        self.ToolsAlertItem.setObjectName(u'ToolsAlertItem')
        self.HelpDocumentationItem = QtGui.QAction(self.mainWindow)
        ContentsIcon = QtGui.QIcon()
        ContentsIcon.addPixmap(QtGui.QPixmap(u':/system/system_help_contents.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.HelpDocumentationItem.setIcon(ContentsIcon)
        self.HelpDocumentationItem.setObjectName(u'HelpDocumentationItem')
        self.HelpAboutItem = QtGui.QAction(self.mainWindow)
        AboutIcon = QtGui.QIcon()
        AboutIcon.addPixmap(QtGui.QPixmap(u':/system/system_about.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.HelpAboutItem.setIcon(AboutIcon)
        self.HelpAboutItem.setObjectName(u'HelpAboutItem')
        self.HelpOnlineHelpItem = QtGui.QAction(self.mainWindow)
        self.HelpOnlineHelpItem.setObjectName(u'HelpOnlineHelpItem')
        self.HelpWebSiteItem = QtGui.QAction(self.mainWindow)
        self.HelpWebSiteItem.setObjectName(u'HelpWebSiteItem')
        self.LanguageTranslateItem = QtGui.QAction(self.mainWindow)
        self.LanguageTranslateItem.setObjectName(u'LanguageTranslateItem')
        self.LanguageEnglishItem = QtGui.QAction(self.mainWindow)
        self.LanguageEnglishItem.setObjectName(u'LanguageEnglishItem')
        self.ToolsAddToolItem = QtGui.QAction(self.mainWindow)
        AddToolIcon = QtGui.QIcon()
        AddToolIcon.addPixmap(QtGui.QPixmap(u':/tools/tools_add.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolsAddToolItem.setIcon(AddToolIcon)
        self.ToolsAddToolItem.setObjectName(u'ToolsAddToolItem')
        self.action_Preview_Panel = QtGui.QAction(self.mainWindow)
        self.action_Preview_Panel.setCheckable(True)
        self.action_Preview_Panel.setChecked(True)
        self.action_Preview_Panel.setObjectName(u'action_Preview_Panel')
        self.ModeLiveItem = QtGui.QAction(self.mainWindow)
        self.ModeLiveItem.setObjectName(u'ModeLiveItem')
        self.FileImportMenu.addAction(self.ImportThemeItem)
        self.FileImportMenu.addAction(self.ImportLanguageItem)
        self.FileExportMenu.addAction(self.ExportThemeItem)
        self.FileExportMenu.addAction(self.ExportLanguageItem)
        self.FileMenu.addAction(self.FileNewItem)
        self.FileMenu.addAction(self.FileOpenItem)
        self.FileMenu.addAction(self.FileSaveItem)
        self.FileMenu.addAction(self.FileSaveAsItem)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.FileImportMenu.menuAction())
        self.FileMenu.addAction(self.FileExportMenu.menuAction())
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.FileExitItem)
        self.ViewModeMenu.addAction(self.ModeLiveItem)
        self.OptionsViewMenu.addAction(self.ViewModeMenu.menuAction())
        self.OptionsViewMenu.addSeparator()
        self.OptionsViewMenu.addAction(self.ViewMediaManagerItem)
        self.OptionsViewMenu.addAction(self.ViewServiceManagerItem)
        self.OptionsViewMenu.addAction(self.ViewThemeManagerItem)
        self.OptionsViewMenu.addSeparator()
        self.OptionsViewMenu.addAction(self.action_Preview_Panel)
        self.OptionsLanguageMenu.addAction(self.LanguageEnglishItem)
        self.OptionsLanguageMenu.addSeparator()
        self.OptionsLanguageMenu.addAction(self.LanguageTranslateItem)
        self.OptionsMenu.addAction(self.OptionsLanguageMenu.menuAction())
        self.OptionsMenu.addAction(self.OptionsViewMenu.menuAction())
        self.OptionsMenu.addSeparator()
        self.OptionsMenu.addAction(self.OptionsSettingsItem)
        self.ToolsMenu.addAction(self.ToolsAlertItem)
        self.ToolsMenu.addSeparator()
        self.ToolsMenu.addAction(self.ToolsAddToolItem)
        self.HelpMenu.addAction(self.HelpDocumentationItem)
        self.HelpMenu.addAction(self.HelpOnlineHelpItem)
        self.HelpMenu.addSeparator()
        self.HelpMenu.addAction(self.HelpWebSiteItem)
        self.HelpMenu.addAction(self.HelpAboutItem)
        self.MenuBar.addAction(self.FileMenu.menuAction())
        self.MenuBar.addAction(self.OptionsMenu.menuAction())
        self.MenuBar.addAction(self.ToolsMenu.menuAction())
        self.MenuBar.addAction(self.HelpMenu.menuAction())
        # Initialise the translation
        self.retranslateUi()
        self.MediaToolBox.setCurrentIndex(0)
        # Connect up some signals and slots
        QtCore.QObject.connect(self.FileExitItem,
            QtCore.SIGNAL(u'triggered()'), self.mainWindow.close)
        QtCore.QObject.connect(self.ImportThemeItem,
            QtCore.SIGNAL(u'triggered()'), self.ThemeManagerContents.onImportTheme)
        QtCore.QObject.connect(self.ExportThemeItem,
            QtCore.SIGNAL(u'triggered()'), self.ThemeManagerContents.onExportTheme)
        QtCore.QObject.connect(self.ViewMediaManagerItem,
            QtCore.SIGNAL(u'triggered(bool)'), self.MediaManagerDock.setVisible)
        QtCore.QObject.connect(self.ViewServiceManagerItem,
            QtCore.SIGNAL(u'triggered(bool)'), self.ServiceManagerDock.setVisible)
        QtCore.QObject.connect(self.ViewThemeManagerItem,
            QtCore.SIGNAL(u'triggered(bool)'), self.ThemeManagerDock.setVisible)
        QtCore.QObject.connect(self.action_Preview_Panel,
            QtCore.SIGNAL(u'toggled(bool)'), self.PreviewController.Panel.setVisible)
        QtCore.QObject.connect(self.MediaManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'), self.ViewMediaManagerItem.setChecked)
        QtCore.QObject.connect(self.ServiceManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'), self.ViewServiceManagerItem.setChecked)
        QtCore.QObject.connect(self.ThemeManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'), self.ViewThemeManagerItem.setChecked)
        QtCore.QObject.connect(self.HelpAboutItem,
            QtCore.SIGNAL(u'triggered()'), self.onHelpAboutItemClicked)
        QtCore.QObject.connect(self.ToolsAlertItem,
            QtCore.SIGNAL(u'triggered()'), self.onToolsAlertItemClicked)
        QtCore.QObject.connect(self.OptionsSettingsItem,
            QtCore.SIGNAL(u'triggered()'), self.onOptionsSettingsItemClicked)
        QtCore.QMetaObject.connectSlotsByName(self.mainWindow)

    def retranslateUi(self):
        """
        Set up the translation system
        """
        self.mainTitle = translate(u'mainWindow', u'OpenLP 2.0')
        self.mainWindow.setWindowTitle(self.mainTitle)
        self.FileMenu.setTitle(translate(u'mainWindow', u'&File'))
        self.FileImportMenu.setTitle(translate(u'mainWindow', u'&Import'))
        self.FileExportMenu.setTitle(translate(u'mainWindow', u'&Export'))
        self.OptionsMenu.setTitle(translate(u'mainWindow', u'&Options'))
        self.OptionsViewMenu.setTitle(translate(u'mainWindow', u'&View'))
        self.ViewModeMenu.setTitle(translate(u'mainWindow', u'M&ode'))
        self.OptionsLanguageMenu.setTitle(translate(u'mainWindow', u'&Language'))
        self.ToolsMenu.setTitle(translate(u'mainWindow', u'&Tools'))
        self.HelpMenu.setTitle(translate(u'mainWindow', u'&Help'))
        self.MediaManagerDock.setWindowTitle(
            translate(u'mainWindow', u'Media Manager'))
        self.ServiceManagerDock.setWindowTitle(
            translate(u'mainWindow', u'Service Manager'))
        self.ThemeManagerDock.setWindowTitle(
            translate(u'mainWindow', u'Theme Manager'))
        self.FileNewItem.setText(translate(u'mainWindow', u'&New'))
        self.FileNewItem.setToolTip(translate(u'mainWindow', u'New Service'))
        self.FileNewItem.setStatusTip(
            translate(u'mainWindow', u'Create a new Service'))
        self.FileNewItem.setShortcut(translate(u'mainWindow', u'Ctrl+N'))
        self.FileOpenItem.setText(translate(u'mainWindow', u'&Open'))
        self.FileOpenItem.setToolTip(translate(u'mainWindow', u'Open Service'))
        self.FileOpenItem.setStatusTip(
            translate(u'mainWindow', u'Open an existing service'))
        self.FileOpenItem.setShortcut(translate(u'mainWindow', u'Ctrl+O'))
        self.FileSaveItem.setText(translate(u'mainWindow', u'&Save'))
        self.FileSaveItem.setToolTip(translate(u'mainWindow', u'Save Service'))
        self.FileSaveItem.setStatusTip(
            translate(u'mainWindow', u'Save the current service to disk'))
        self.FileSaveItem.setShortcut(translate(u'mainWindow', u'Ctrl+S'))
        self.FileSaveAsItem.setText(translate(u'mainWindow', u'Save &As...'))
        self.FileSaveAsItem.setToolTip(
            translate(u'mainWindow', u'Save Service As'))
        self.FileSaveAsItem.setStatusTip(translate(u'mainWindow',
            u'Save the current service under a new name'))
        self.FileSaveAsItem.setShortcut(translate(u'mainWindow', u'F12'))
        self.FileExitItem.setText(translate(u'mainWindow', u'E&xit'))
        self.FileExitItem.setStatusTip(translate(u'mainWindow', u'Quit OpenLP'))
        self.FileExitItem.setShortcut(translate(u'mainWindow', u'Alt+F4'))
        self.ImportThemeItem.setText(translate(u'mainWindow', u'&Theme'))
        self.ImportLanguageItem.setText(translate(u'mainWindow', u'&Language'))
        self.ExportThemeItem.setText(translate(u'mainWindow', u'&Theme'))
        self.ExportLanguageItem.setText(translate(u'mainWindow', u'&Language'))
        self.actionLook_Feel.setText(translate(u'mainWindow', u'Look && &Feel'))
        self.OptionsSettingsItem.setText(translate(u'mainWindow', u'&Settings'))
        self.ViewMediaManagerItem.setText(
            translate(u'mainWindow', u'&Media Manager'))
        self.ViewMediaManagerItem.setToolTip(
            translate(u'mainWindow', u'Toggle Media Manager'))
        self.ViewMediaManagerItem.setStatusTip(translate(u'mainWindow',
            u'Toggle the visibility of the Media Manager'))
        self.ViewMediaManagerItem.setShortcut(translate(u'mainWindow', u'F8'))
        self.ViewThemeManagerItem.setText(
            translate(u'mainWindow', u'&Theme Manager'))
        self.ViewThemeManagerItem.setToolTip(
            translate(u'mainWindow', u'Toggle Theme Manager'))
        self.ViewThemeManagerItem.setStatusTip(translate(u'mainWindow',
            u'Toggle the visibility of the Theme Manager'))
        self.ViewThemeManagerItem.setShortcut(translate(u'mainWindow', u'F10'))
        self.ViewServiceManagerItem.setText(
            translate(u'mainWindow', u'&Service Manager'))
        self.ViewServiceManagerItem.setToolTip(
            translate(u'mainWindow', u'Toggle Service Manager'))
        self.ViewServiceManagerItem.setStatusTip(translate(u'mainWindow',
            u'Toggle the visibility of the Service Manager'))
        self.ViewServiceManagerItem.setShortcut(translate(u'mainWindow', u'F9'))
        self.ToolsAlertItem.setText(translate(u'mainWindow', u'&Alert'))
        self.ToolsAlertItem.setStatusTip(
            translate(u'mainWindow', u'Show an alert message'))
        self.ToolsAlertItem.setShortcut(translate(u'mainWindow', u'F7'))
        self.HelpDocumentationItem.setText(
            translate(u'mainWindow', u'&User Guide'))
        self.HelpAboutItem.setText(translate(u'mainWindow', u'&About'))
        self.HelpAboutItem.setStatusTip(
            translate(u'mainWindow', u'More information about OpenLP'))
        self.HelpAboutItem.setShortcut(translate(u'mainWindow', u'Ctrl+F1'))
        self.HelpOnlineHelpItem.setText(
            translate(u'mainWindow', u'&Online Help'))
        self.HelpWebSiteItem.setText(translate(u'mainWindow', u'&Web Site'))
        self.LanguageTranslateItem.setText(
            translate(u'mainWindow', u'&Translate'))
        self.LanguageTranslateItem.setStatusTip(translate(u'mainWindow',
            u'Translate the interface to your language'))
        self.LanguageEnglishItem.setText(translate(u'mainWindow', u'English'))
        self.LanguageEnglishItem.setStatusTip(translate(u'mainWindow',
            u'Set the interface language to English'))
        self.ToolsAddToolItem.setText(translate(u'mainWindow', u'&Add Tool...'))
        self.ToolsAddToolItem.setStatusTip(translate(u'mainWindow',
            u'Add an application to the list of tools'))
        self.action_Preview_Panel.setText(
            translate(u'mainWindow', u'&Preview Pane'))
        self.ModeLiveItem.setText(translate(u'mainWindow', u'&Live'))
