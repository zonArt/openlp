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
from time import sleep

from PyQt4 import *
from PyQt4 import QtCore, QtGui

from openlp.core.ui import AboutForm, SettingsForm, AlertForm, \
                           SlideController, ServiceManager, ThemeManager, MainDisplay
from openlp.core.lib import Plugin, MediaManagerItem, SettingsTab, EventManager, RenderManager

from openlp.core import PluginManager, translate

class MainWindow(object):
    global log
    log=logging.getLogger(u'MainWindow')
    log.info(u'MainWindow loaded')

    def __init__(self, screens):
        self.main_window = QtGui.QMainWindow()
        self.main_window.__class__.closeEvent = self.onCloseEvent
        self.main_display = MainDisplay(None, screens)
        self.screen_list = screens
        self.EventManager = EventManager()
        self.alert_form = AlertForm()
        self.about_form = AboutForm()
        self.settings_form = SettingsForm(self.screen_list, self)

        pluginpath = os.path.split(os.path.abspath(__file__))[0]
        pluginpath = os.path.abspath(os.path.join(pluginpath, u'..', u'..', u'plugins'))
        self.plugin_manager = PluginManager(pluginpath)
        self.plugin_helpers = {}

        self.setupUi()

        #warning cyclic dependency
        #RenderManager needs to call ThemeManager and
        #ThemeManager needs to call RenderManager
        self.RenderManager = RenderManager(self.ThemeManagerContents, self.screen_list)

        log.info(u'Load Plugins')
        self.plugin_helpers[u'preview'] = self.PreviewController
        self.plugin_helpers[u'live'] = self.LiveController
        self.plugin_helpers[u'event'] = self.EventManager
        self.plugin_helpers[u'theme'] = self.ThemeManagerContents
        self.plugin_helpers[u'render'] = self.RenderManager
        self.plugin_helpers[u'service'] = self.ServiceManagerContents

        self.plugin_manager.find_plugins(pluginpath, self.plugin_helpers, self.EventManager)
        # hook methods have to happen after find_plugins.  Find plugins needs the controllers
        # hence the hooks have moved from setupUI() to here

        # Find and insert media manager items
        log.info(u'hook media')
        self.plugin_manager.hook_media_manager(self.MediaToolBox)

        # Find and insert settings tabs
        log.info(u'hook settings')
        self.plugin_manager.hook_settings_tabs(self.settings_form)

        # Call the hook method to pull in import menus.
        log.info(u'hook menus')
        self.plugin_manager.hook_import_menu(self.FileImportMenu)

        # Call the hook method to pull in export menus.
        self.plugin_manager.hook_export_menu(self.FileExportMenu)

        # Call the initialise method to setup plugins.
        log.info(u'initialise plugins')
        self.plugin_manager.initialise_plugins()

        # Once all components are initialised load the Themes
        log.info(u'Load Themes and Managers')
        self.PreviewController.ServiceManager = self.ServiceManagerContents
        self.LiveController.ServiceManager = self.ServiceManagerContents

        self.ThemeManagerContents.EventManager = self.EventManager
        self.ThemeManagerContents.RenderManager = self.RenderManager
        self.ThemeManagerContents.ServiceManager = self.ServiceManagerContents
        #self.ThemeManagerContents.ThemesTab = self.ServiceManagerContents.ThemesTab

        self.ServiceManagerContents.RenderManager = self.RenderManager
        self.ServiceManagerContents.EventManager = self.EventManager
        self.ServiceManagerContents.LiveController = self.LiveController
        self.ServiceManagerContents.PreviewController = self.PreviewController

        self.ThemeManagerContents.loadThemes()

        # Initialise SlideControllers
        log.info(u'Set Up SlideControllers')
        self.LiveController.mainDisplay = self.main_display

    def onCloseEvent(self, event):
        """
        Hook to close the main window and display windows on exit
        """
        self.main_display.close()
        event.accept()

    def setupUi(self):
        self.main_window.setObjectName(u'main_window')
        self.main_window.resize(1087, 847)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_window.sizePolicy().hasHeightForWidth())
        self.main_window.setSizePolicy(sizePolicy)
        main_icon = QtGui.QIcon()
        main_icon.addPixmap(QtGui.QPixmap(u':/icon/openlp-logo-16x16.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.main_window.setWindowIcon(main_icon)
        self.MainContent = QtGui.QWidget(self.main_window)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainContent.sizePolicy().hasHeightForWidth())
        self.MainContent.setSizePolicy(sizePolicy)
        self.MainContent.setObjectName(u'MainContent')
        self.MainContentLayout = QtGui.QHBoxLayout(self.MainContent)
        self.MainContentLayout.setSpacing(0)
        self.MainContentLayout.setMargin(0)
        self.MainContentLayout.setObjectName(u'MainContentLayout')
        self.main_window.setCentralWidget(self.MainContent)
        self.ControlSplitter = QtGui.QSplitter(self.MainContent)
        self.ControlSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.ControlSplitter.setObjectName(u'ControlSplitter')
        self.MainContentLayout.addWidget(self.ControlSplitter)
        self.PreviewController = SlideController(self.ControlSplitter, False)
        self.LiveController = SlideController(self.ControlSplitter, True)
        self.MenuBar = QtGui.QMenuBar(self.main_window)
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
        self.main_window.setMenuBar(self.MenuBar)
        self.StatusBar = QtGui.QStatusBar(self.main_window)
        self.StatusBar.setObjectName(u'StatusBar')
        self.main_window.setStatusBar(self.StatusBar)
        self.MediaManagerDock = QtGui.QDockWidget(self.main_window)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MediaManagerDock.sizePolicy().hasHeightForWidth())
        self.MediaManagerDock.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/system/system_mediamanager.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.MediaManagerDock.setWindowIcon(icon)
        self.MediaManagerDock.setFloating(False)
        self.MediaManagerDock.setObjectName(u'MediaManagerDock')
        self.MediaManagerDock.setMinimumWidth(250)
        self.MediaManagerContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MediaManagerContents.sizePolicy().hasHeightForWidth())
        self.MediaManagerContents.setSizePolicy(sizePolicy)
        self.MediaManagerContents.setObjectName(u'MediaManagerContents')
        self.MediaManagerLayout = QtGui.QHBoxLayout(self.MediaManagerContents)
        self.MediaManagerLayout.setContentsMargins(0, 2, 0, 0)
        self.MediaManagerLayout.setObjectName(u'MediaManagerLayout')
        self.MediaToolBox = QtGui.QToolBox(self.MediaManagerContents)
        self.MediaToolBox.setObjectName(u'MediaToolBox')

        self.MediaManagerLayout.addWidget(self.MediaToolBox)
        self.MediaManagerDock.setWidget(self.MediaManagerContents)
        self.main_window.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.MediaManagerDock)
        #Sevice Manager Defined
        self.ServiceManagerDock = QtGui.QDockWidget(self.main_window)
        ServiceManagerIcon = QtGui.QIcon()
        ServiceManagerIcon.addPixmap(QtGui.QPixmap(u':/system/system_servicemanager.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ServiceManagerDock.setWindowIcon(ServiceManagerIcon)
        self.ServiceManagerDock.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.ServiceManagerDock.setObjectName(u'ServiceManagerDock')
        self.ServiceManagerContents = ServiceManager(self)
        self.ServiceManagerDock.setWidget(self.ServiceManagerContents)
        self.main_window.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.ServiceManagerDock)
        #Theme Manager Defined
        self.ThemeManagerDock = QtGui.QDockWidget(self.main_window)
        ThemeManagerIcon = QtGui.QIcon()
        ThemeManagerIcon.addPixmap(QtGui.QPixmap(u':/system/system_thememanager.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ThemeManagerDock.setWindowIcon(ThemeManagerIcon)
        self.ThemeManagerDock.setFloating(False)
        self.ThemeManagerDock.setObjectName(u'ThemeManagerDock')

        self.ThemeManagerContents = ThemeManager(self)

        self.ThemeManagerDock.setWidget(self.ThemeManagerContents)
        self.main_window.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.ThemeManagerDock)

        self.FileNewItem = QtGui.QAction(self.main_window)
        self.FileNewItem.setIcon(
            self.ServiceManagerContents.Toolbar.getIconFromTitle(u'New Service'))
        self.FileNewItem.setObjectName(u'FileNewItem')
        self.FileOpenItem = QtGui.QAction(self.main_window)
        self.FileOpenItem.setIcon(
            self.ServiceManagerContents.Toolbar.getIconFromTitle(u'Open Service'))
        self.FileOpenItem.setObjectName(u'FileOpenItem')
        self.FileSaveItem = QtGui.QAction(self.main_window)
        self.FileSaveItem.setIcon(
            self.ServiceManagerContents.Toolbar.getIconFromTitle(u'Save Service'))
        self.FileSaveItem.setObjectName(u'FileSaveItem')
        self.FileSaveAsItem = QtGui.QAction(self.main_window)
        self.FileSaveAsItem.setObjectName(u'FileSaveAsItem')
        self.FileExitItem = QtGui.QAction(self.main_window)
        ExitIcon = QtGui.QIcon()
        ExitIcon.addPixmap(QtGui.QPixmap(u':/system/system_exit.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.FileExitItem.setIcon(ExitIcon)
        self.FileExitItem.setObjectName(u'FileExitItem')
        self.ImportThemeItem = QtGui.QAction(self.main_window)
        self.ImportThemeItem.setObjectName(u'ImportThemeItem')
        self.ImportLanguageItem = QtGui.QAction(self.main_window)
        self.ImportLanguageItem.setObjectName(u'ImportLanguageItem')
        self.ExportThemeItem = QtGui.QAction(self.main_window)
        self.ExportThemeItem.setObjectName(u'ExportThemeItem')
        self.ExportLanguageItem = QtGui.QAction(self.main_window)
        self.ExportLanguageItem.setObjectName(u'ExportLanguageItem')
        self.actionLook_Feel = QtGui.QAction(self.main_window)
        self.actionLook_Feel.setObjectName(u'actionLook_Feel')
        self.OptionsSettingsItem = QtGui.QAction(self.main_window)
        SettingsIcon = QtGui.QIcon()
        SettingsIcon.addPixmap(QtGui.QPixmap(u':/system/system_settings.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.OptionsSettingsItem.setIcon(SettingsIcon)
        self.OptionsSettingsItem.setObjectName(u'OptionsSettingsItem')
        self.ViewMediaManagerItem = QtGui.QAction(self.main_window)
        self.ViewMediaManagerItem.setCheckable(True)
        self.ViewMediaManagerItem.setChecked(True)
        self.ViewMediaManagerItem.setIcon(icon)
        self.ViewMediaManagerItem.setObjectName(u'ViewMediaManagerItem')
        self.ViewThemeManagerItem = QtGui.QAction(self.main_window)
        self.ViewThemeManagerItem.setCheckable(True)
        self.ViewThemeManagerItem.setChecked(True)
        self.ViewThemeManagerItem.setIcon(ThemeManagerIcon)
        self.ViewThemeManagerItem.setObjectName(u'ViewThemeManagerItem')
        self.ViewServiceManagerItem = QtGui.QAction(self.main_window)
        self.ViewServiceManagerItem.setCheckable(True)
        self.ViewServiceManagerItem.setChecked(True)
        self.ViewServiceManagerItem.setIcon(ServiceManagerIcon)
        self.ViewServiceManagerItem.setObjectName(u'ViewServiceManagerItem')
        self.ToolsAlertItem = QtGui.QAction(self.main_window)
        AlertIcon = QtGui.QIcon()
        AlertIcon.addPixmap(QtGui.QPixmap(u':/tools/tools_alert.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolsAlertItem.setIcon(AlertIcon)
        self.ToolsAlertItem.setObjectName(u'ToolsAlertItem')
        self.HelpDocumentationItem = QtGui.QAction(self.main_window)
        ContentsIcon = QtGui.QIcon()
        ContentsIcon.addPixmap(QtGui.QPixmap(u':/system/system_help_contents.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.HelpDocumentationItem.setIcon(ContentsIcon)
        self.HelpDocumentationItem.setObjectName(u'HelpDocumentationItem')
        self.HelpAboutItem = QtGui.QAction(self.main_window)
        AboutIcon = QtGui.QIcon()
        AboutIcon.addPixmap(QtGui.QPixmap(u':/system/system_about.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.HelpAboutItem.setIcon(AboutIcon)
        self.HelpAboutItem.setObjectName(u'HelpAboutItem')
        self.HelpOnlineHelpItem = QtGui.QAction(self.main_window)
        self.HelpOnlineHelpItem.setObjectName(u'HelpOnlineHelpItem')
        self.HelpWebSiteItem = QtGui.QAction(self.main_window)
        self.HelpWebSiteItem.setObjectName(u'HelpWebSiteItem')
        self.LanguageTranslateItem = QtGui.QAction(self.main_window)
        self.LanguageTranslateItem.setObjectName(u'LanguageTranslateItem')
        self.LanguageEnglishItem = QtGui.QAction(self.main_window)
        self.LanguageEnglishItem.setObjectName(u'LanguageEnglishItem')
        self.ToolsAddToolItem = QtGui.QAction(self.main_window)
        AddToolIcon = QtGui.QIcon()
        AddToolIcon.addPixmap(QtGui.QPixmap(u':/tools/tools_add.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolsAddToolItem.setIcon(AddToolIcon)
        self.ToolsAddToolItem.setObjectName(u'ToolsAddToolItem')
        self.action_Preview_Panel = QtGui.QAction(self.main_window)
        self.action_Preview_Panel.setCheckable(True)
        self.action_Preview_Panel.setChecked(True)
        self.action_Preview_Panel.setObjectName(u'action_Preview_Panel')
        self.ModeLiveItem = QtGui.QAction(self.main_window)
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

        self.retranslateUi()
        self.MediaToolBox.setCurrentIndex(0)
        QtCore.QObject.connect(self.FileExitItem,
            QtCore.SIGNAL(u'triggered()'), self.main_window.close)
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
        QtCore.QMetaObject.connectSlotsByName(self.main_window)


    def retranslateUi(self):
        self.main_window.setWindowTitle(translate(u'main_window', u'openlp.org 2.0'))
        self.FileMenu.setTitle(translate(u'main_window', u'&File'))
        self.FileImportMenu.setTitle(translate(u'main_window', u'&Import'))
        self.FileExportMenu.setTitle(translate(u'main_window', u'&Export'))
        self.OptionsMenu.setTitle(translate(u'main_window', u'&Options'))
        self.OptionsViewMenu.setTitle(translate(u'main_window', u'&View'))
        self.ViewModeMenu.setTitle(translate(u'main_window', u'M&ode'))
        self.OptionsLanguageMenu.setTitle(translate(u'main_window', u'&Language'))
        self.ToolsMenu.setTitle(translate(u'main_window', u'&Tools'))
        self.HelpMenu.setTitle(translate(u'main_window', u'&Help'))
        self.MediaManagerDock.setWindowTitle(translate(u'main_window', u'Media Manager'))
        self.ServiceManagerDock.setWindowTitle(translate(u'main_window', u'Service Manager'))
#        self.ServiceManagerContents.MoveTopButton.setText(translate(u'main_window', u'Move To Top'))
#        self.ServiceManagerContents.MoveUpButton.setText(translate(u'main_window', u'Move Up'))
#        self.ServiceManagerContents.MoveDownButton.setText(translate(u'main_window', u'Move Down'))
#        self.ServiceManagerContents.MoveBottomButton.setText(translate(u'main_window', u'Move To Bottom'))
#        self.ServiceManagerContents.NewItem.setText(translate(u'main_window', u'New Service'))
#        self.ServiceManagerContents.OpenItem.setText(translate(u'main_window', u'Open Service'))
#        self.ServiceManagerContents.SaveItem.setText(translate(u'main_window', u'Save Service'))
#        self.ServiceManagerContents.ThemeComboBox.setItemText(0, translate(u'main_window', u'African Sunset'))
#        self.ServiceManagerContents.ThemeComboBox.setItemText(1, translate(u'main_window', u'Snowy Mountains'))
#        self.ServiceManagerContents.ThemeComboBox.setItemText(2, translate(u'main_window', u'Wilderness'))
        self.ThemeManagerDock.setWindowTitle(translate(u'main_window', u'Theme Manager'))
#        self.ThemeNewItem.setText(translate(u'main_window', u'New Theme'))
#        self.ThemeEditItem.setText(translate(u'main_window', u'Edit Theme'))
#        self.ThemeDeleteButton.setText(translate(u'main_window', u'Delete Theme'))
#        self.ThemeImportButton.setText(translate(u'main_window', u'Import Theme'))
#        self.ThemeExportButton.setText(translate(u'main_window', u'Export Theme'))
        self.FileNewItem.setText(translate(u'main_window', u'&New'))
        self.FileNewItem.setToolTip(translate(u'main_window', u'New Service'))
        self.FileNewItem.setStatusTip(translate(u'main_window', u'Create a new Service'))
        self.FileNewItem.setShortcut(translate(u'main_window', u'Ctrl+N'))
        self.FileOpenItem.setText(translate(u'main_window', u'&Open'))
        self.FileOpenItem.setToolTip(translate(u'main_window', u'Open Service'))
        self.FileOpenItem.setStatusTip(translate(u'main_window', u'Open an existing service'))
        self.FileOpenItem.setShortcut(translate(u'main_window', u'Ctrl+O'))
        self.FileSaveItem.setText(translate(u'main_window', u'&Save'))
        self.FileSaveItem.setToolTip(translate(u'main_window', u'Save Service'))
        self.FileSaveItem.setStatusTip(translate(u'main_window', u'Save the current service to disk'))
        self.FileSaveItem.setShortcut(translate(u'main_window', u'Ctrl+S'))
        self.FileSaveAsItem.setText(translate(u'main_window', u'Save &As...'))
        self.FileSaveAsItem.setToolTip(translate(u'main_window', u'Save Service As'))
        self.FileSaveAsItem.setStatusTip(translate(u'main_window', u'Save the current service under a new name'))
        self.FileSaveAsItem.setShortcut(translate(u'main_window', u'F12'))
        self.FileExitItem.setText(translate(u'main_window', u'E&xit'))
        self.FileExitItem.setStatusTip(translate(u'main_window', u'Quit OpenLP 2.0'))
        self.FileExitItem.setShortcut(translate(u'main_window', u'Alt+F4'))
        self.ImportThemeItem.setText(translate(u'main_window', u'&Theme'))
        self.ImportLanguageItem.setText(translate(u'main_window', u'&Language'))
        self.ExportThemeItem.setText(translate(u'main_window', u'&Theme'))
        self.ExportLanguageItem.setText(translate(u'main_window', u'&Language'))
        self.actionLook_Feel.setText(translate(u'main_window', u'Look && &Feel'))
        self.OptionsSettingsItem.setText(translate(u'main_window', u'&Settings'))
        self.ViewMediaManagerItem.setText(translate(u'main_window', u'&Media Manager'))
        self.ViewMediaManagerItem.setToolTip(translate(u'main_window', u'Toggle Media Manager'))
        self.ViewMediaManagerItem.setStatusTip(translate(u'main_window', u'Toggle the visibility of the Media Manager'))
        self.ViewMediaManagerItem.setShortcut(translate(u'main_window', u'F8'))
        self.ViewThemeManagerItem.setText(translate(u'main_window', u'&Theme Manager'))
        self.ViewThemeManagerItem.setToolTip(translate(u'main_window', u'Toggle Theme Manager'))
        self.ViewThemeManagerItem.setStatusTip(translate(u'main_window', u'Toggle the visibility of the Theme Manager'))
        self.ViewThemeManagerItem.setShortcut(translate(u'main_window', u'F10'))
        self.ViewServiceManagerItem.setText(translate(u'main_window', u'&Service Manager'))
        self.ViewServiceManagerItem.setToolTip(translate(u'main_window', u'Toggle Service Manager'))
        self.ViewServiceManagerItem.setStatusTip(translate(u'main_window', u'Toggle the visibility of the Service Manager'))
        self.ViewServiceManagerItem.setShortcut(translate(u'main_window', u'F9'))
        self.ToolsAlertItem.setText(translate(u'main_window', u'&Alert'))
        self.ToolsAlertItem.setStatusTip(translate(u'main_window', u'Show an alert message'))
        self.ToolsAlertItem.setShortcut(translate(u'main_window', u'F7'))
        self.HelpDocumentationItem.setText(translate(u'main_window', u'&User Guide'))
        self.HelpAboutItem.setText(translate(u'main_window', u'&About'))
        self.HelpAboutItem.setStatusTip(translate(u'main_window', u'More information about OpenLP'))
        self.HelpAboutItem.setShortcut(translate(u'main_window', u'Ctrl+F1'))
        self.HelpOnlineHelpItem.setText(translate(u'main_window', u'&Online Help'))
        self.HelpWebSiteItem.setText(translate(u'main_window', u'&Web Site'))
        self.LanguageTranslateItem.setText(translate(u'main_window', u'&Translate'))
        self.LanguageTranslateItem.setStatusTip(translate(u'main_window', u'Translate the interface to your language'))
        self.LanguageEnglishItem.setText(translate(u'main_window', u'English'))
        self.LanguageEnglishItem.setStatusTip(translate(u'main_window', u'Set the interface language to English'))
        self.ToolsAddToolItem.setText(translate(u'main_window', u'&Add Tool...'))
        self.ToolsAddToolItem.setStatusTip(translate(u'main_window', u'Add an application to the list of tools'))
        self.action_Preview_Panel.setText(translate(u'main_window', u'&Preview Pane'))
        self.ModeLiveItem.setText(translate(u'main_window', u'&Live'))

    def show(self):
        self.main_window.showMaximized()
        self.main_display.setup(0)
        self.main_display.show()

    def onHelpAboutItemClicked(self):
        self.about_form.exec_()

    def onToolsAlertItemClicked(self):
        self.alert_form.exec_()

    def onOptionsSettingsItemClicked(self):
        self.settings_form.exec_()
