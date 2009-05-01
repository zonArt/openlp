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

from openlp.core import PluginManager

class MainWindow(object):
    global log
    log=logging.getLogger(u'MainWindow')
    log.info(u'MainWindow loaded')

    def __init__(self, screens):
        self.main_window = QtGui.QMainWindow()
        self.main_display = MainDisplay(None, screens)
        self.screen_list = screens
        self.EventManager = EventManager()
        self.alert_form = AlertForm()
        self.about_form = AboutForm()
        self.settings_form = SettingsForm(self.screen_list)

        pluginpath = os.path.split(os.path.abspath(__file__))[0]
        pluginpath = os.path.abspath(os.path.join(pluginpath, '..', '..','plugins'))
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
        self.plugin_helpers[u'theme'] = self.ThemeManagerContents  # Theme manger
        self.plugin_helpers[u'render'] = self.RenderManager

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
        log.info(u'Load Themes')
        self.ThemeManagerContents.eventManager = self.EventManager
        self.ThemeManagerContents.renderManager = self.RenderManager
        self.ServiceManagerContents.renderManager = self.RenderManager
        self.ThemeManagerContents.serviceManager = self.ServiceManagerContents
        self.ThemeManagerContents.loadThemes()

    def setupUi(self):
        self.main_window.setObjectName("main_window")
        self.main_window.resize(1087, 847)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_window.sizePolicy().hasHeightForWidth())
        self.main_window.setSizePolicy(sizePolicy)
        main_icon = QtGui.QIcon()
        main_icon.addPixmap(QtGui.QPixmap(":/icon/openlp.org-icon-32.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.main_window.setWindowIcon(main_icon)
        self.MainContent = QtGui.QWidget(self.main_window)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainContent.sizePolicy().hasHeightForWidth())
        self.MainContent.setSizePolicy(sizePolicy)
        self.MainContent.setObjectName("MainContent")
        self.MainContentLayout = QtGui.QHBoxLayout(self.MainContent)
        self.MainContentLayout.setSpacing(0)
        self.MainContentLayout.setMargin(0)
        self.MainContentLayout.setObjectName("MainContentLayout")
        self.main_window.setCentralWidget(self.MainContent)
        self.ControlSplitter = QtGui.QSplitter(self.MainContent)
        self.ControlSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.ControlSplitter.setObjectName("ControlSplitter")
        self.MainContentLayout.addWidget(self.ControlSplitter)
        self.PreviewController = SlideController(self.ControlSplitter)
        self.LiveController = SlideController(self.ControlSplitter)
        self.MenuBar = QtGui.QMenuBar(self.main_window)
        self.MenuBar.setGeometry(QtCore.QRect(0, 0, 1087, 27))
        self.MenuBar.setObjectName("MenuBar")
        self.FileMenu = QtGui.QMenu(self.MenuBar)
        self.FileMenu.setObjectName("FileMenu")
        self.FileImportMenu = QtGui.QMenu(self.FileMenu)
        self.FileImportMenu.setObjectName("FileImportMenu")

        self.FileExportMenu = QtGui.QMenu(self.FileMenu)
        self.FileExportMenu.setObjectName("FileExportMenu")
        self.OptionsMenu = QtGui.QMenu(self.MenuBar)
        self.OptionsMenu.setObjectName("OptionsMenu")
        self.OptionsViewMenu = QtGui.QMenu(self.OptionsMenu)
        self.OptionsViewMenu.setObjectName("OptionsViewMenu")
        self.ViewModeMenu = QtGui.QMenu(self.OptionsViewMenu)
        self.ViewModeMenu.setObjectName("ViewModeMenu")
        self.OptionsLanguageMenu = QtGui.QMenu(self.OptionsMenu)
        self.OptionsLanguageMenu.setObjectName("OptionsLanguageMenu")
        self.ToolsMenu = QtGui.QMenu(self.MenuBar)
        self.ToolsMenu.setObjectName("ToolsMenu")
        self.HelpMenu = QtGui.QMenu(self.MenuBar)
        self.HelpMenu.setObjectName("HelpMenu")
        self.main_window.setMenuBar(self.MenuBar)
        self.StatusBar = QtGui.QStatusBar(self.main_window)
        self.StatusBar.setObjectName("StatusBar")
        self.main_window.setStatusBar(self.StatusBar)
        self.MediaManagerDock = QtGui.QDockWidget(self.main_window)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MediaManagerDock.sizePolicy().hasHeightForWidth())
        self.MediaManagerDock.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/system/system_mediamanager.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.MediaManagerDock.setWindowIcon(icon)
        self.MediaManagerDock.setFloating(False)
        self.MediaManagerDock.setObjectName("MediaManagerDock")
        self.MediaManagerDock.setMinimumWidth(250)
        self.MediaManagerContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MediaManagerContents.sizePolicy().hasHeightForWidth())
        self.MediaManagerContents.setSizePolicy(sizePolicy)
        self.MediaManagerContents.setObjectName("MediaManagerContents")
        self.MediaManagerLayout = QtGui.QHBoxLayout(self.MediaManagerContents)
        self.MediaManagerLayout.setContentsMargins(0, 2, 0, 0)
        self.MediaManagerLayout.setObjectName("MediaManagerLayout")
        self.MediaToolBox = QtGui.QToolBox(self.MediaManagerContents)
        #self.MediaToolBox.setTabSpacing(0)
        self.MediaToolBox.setObjectName("MediaToolBox")

        self.MediaManagerLayout.addWidget(self.MediaToolBox)
        self.MediaManagerDock.setWidget(self.MediaManagerContents)
        self.main_window.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.MediaManagerDock)
        #Sevice Manager Defined
        self.ServiceManagerDock = QtGui.QDockWidget(self.main_window)
        ServiceManagerIcon = QtGui.QIcon()
        ServiceManagerIcon.addPixmap(QtGui.QPixmap(":/system/system_servicemanager.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ServiceManagerDock.setWindowIcon(ServiceManagerIcon)
        self.ServiceManagerDock.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.ServiceManagerDock.setObjectName("ServiceManagerDock")
        self.ServiceManagerContents = ServiceManager(self)
        self.ServiceManagerDock.setWidget(self.ServiceManagerContents)
        self.main_window.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.ServiceManagerDock)
        #Theme Manager Defined
        self.ThemeManagerDock = QtGui.QDockWidget(self.main_window)
        ThemeManagerIcon = QtGui.QIcon()
        ThemeManagerIcon.addPixmap(QtGui.QPixmap(":/system/system_thememanager.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ThemeManagerDock.setWindowIcon(ThemeManagerIcon)
        self.ThemeManagerDock.setFloating(False)
        self.ThemeManagerDock.setObjectName("ThemeManagerDock")

        self.ThemeManagerContents = ThemeManager(self)

        self.ThemeManagerDock.setWidget(self.ThemeManagerContents)
        self.main_window.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.ThemeManagerDock)

        self.FileNewItem = QtGui.QAction(self.main_window)
        self.FileNewItem.setIcon(self.ServiceManagerContents.Toolbar.getIconFromTitle("New Service"))
        self.FileNewItem.setObjectName("FileNewItem")
        self.FileOpenItem = QtGui.QAction(self.main_window)
        self.FileOpenItem.setIcon(self.ServiceManagerContents.Toolbar.getIconFromTitle("Open Service"))
        self.FileOpenItem.setObjectName("FileOpenItem")
        self.FileSaveItem = QtGui.QAction(self.main_window)
        self.FileSaveItem.setIcon(self.ServiceManagerContents.Toolbar.getIconFromTitle("Save Service"))
        self.FileSaveItem.setObjectName("FileSaveItem")
        self.FileSaveAsItem = QtGui.QAction(self.main_window)
        self.FileSaveAsItem.setObjectName("FileSaveAsItem")
        self.FileExitItem = QtGui.QAction(self.main_window)
        icon34 = QtGui.QIcon()
        icon34.addPixmap(QtGui.QPixmap(":/system/system_exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.FileExitItem.setIcon(icon34)
        self.FileExitItem.setObjectName("FileExitItem")
        self.ImportThemeItem = QtGui.QAction(self.main_window)
        self.ImportThemeItem.setObjectName("ImportThemeItem")
        self.ImportLanguageItem = QtGui.QAction(self.main_window)
        self.ImportLanguageItem.setObjectName("ImportLanguageItem")
        self.ExportThemeItem = QtGui.QAction(self.main_window)
        self.ExportThemeItem.setObjectName("ExportThemeItem")
        self.ExportLanguageItem = QtGui.QAction(self.main_window)
        self.ExportLanguageItem.setObjectName("ExportLanguageItem")
        self.actionLook_Feel = QtGui.QAction(self.main_window)
        self.actionLook_Feel.setObjectName("actionLook_Feel")
        self.OptionsSettingsItem = QtGui.QAction(self.main_window)
        icon35 = QtGui.QIcon()
        icon35.addPixmap(QtGui.QPixmap(":/system/system_settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.OptionsSettingsItem.setIcon(icon35)
        self.OptionsSettingsItem.setObjectName("OptionsSettingsItem")
        self.ViewMediaManagerItem = QtGui.QAction(self.main_window)
        self.ViewMediaManagerItem.setCheckable(True)
        self.ViewMediaManagerItem.setChecked(True)
        self.ViewMediaManagerItem.setIcon(icon)
        self.ViewMediaManagerItem.setObjectName("ViewMediaManagerItem")
        self.ViewThemeManagerItem = QtGui.QAction(self.main_window)
        self.ViewThemeManagerItem.setCheckable(True)
        self.ViewThemeManagerItem.setChecked(True)
        self.ViewThemeManagerItem.setIcon(ThemeManagerIcon)
        self.ViewThemeManagerItem.setObjectName("ViewThemeManagerItem")
        self.ViewServiceManagerItem = QtGui.QAction(self.main_window)
        self.ViewServiceManagerItem.setCheckable(True)
        self.ViewServiceManagerItem.setChecked(True)
        self.ViewServiceManagerItem.setIcon(ServiceManagerIcon)
        self.ViewServiceManagerItem.setObjectName("ViewServiceManagerItem")
        self.ToolsAlertItem = QtGui.QAction(self.main_window)
        icon36 = QtGui.QIcon()
        icon36.addPixmap(QtGui.QPixmap(":/tools/tools_alert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolsAlertItem.setIcon(icon36)
        self.ToolsAlertItem.setObjectName("ToolsAlertItem")
        self.HelpDocumentationItem = QtGui.QAction(self.main_window)
        self.HelpDocumentationItem.setObjectName("HelpDocumentationItem")
        self.HelpAboutItem = QtGui.QAction(self.main_window)
        self.HelpAboutItem.setObjectName("HelpAboutItem")
        self.HelpOnlineHelpItem = QtGui.QAction(self.main_window)
        self.HelpOnlineHelpItem.setObjectName("HelpOnlineHelpItem")
        self.HelpWebSiteItem = QtGui.QAction(self.main_window)
        self.HelpWebSiteItem.setObjectName("HelpWebSiteItem")
        self.LanguageTranslateItem = QtGui.QAction(self.main_window)
        self.LanguageTranslateItem.setObjectName("LanguageTranslateItem")
        self.LanguageEnglishItem = QtGui.QAction(self.main_window)
        self.LanguageEnglishItem.setObjectName("LanguageEnglishItem")
        self.ToolsAddToolItem = QtGui.QAction(self.main_window)
        icon37 = QtGui.QIcon()
        icon37.addPixmap(QtGui.QPixmap(":/tools/tools_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolsAddToolItem.setIcon(icon37)
        self.ToolsAddToolItem.setObjectName("ToolsAddToolItem")
        self.action_Preview_Pane = QtGui.QAction(self.main_window)
        self.action_Preview_Pane.setCheckable(True)
        self.action_Preview_Pane.setChecked(True)
        self.action_Preview_Pane.setObjectName("action_Preview_Pane")
        self.ModeLiveItem = QtGui.QAction(self.main_window)
        self.ModeLiveItem.setObjectName("ModeLiveItem")
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
        self.OptionsViewMenu.addAction(self.action_Preview_Pane)
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
        QtCore.QObject.connect(self.FileExitItem, QtCore.SIGNAL("triggered()"), self.main_window.close)
        QtCore.QObject.connect(self.ViewMediaManagerItem, QtCore.SIGNAL("triggered(bool)"), self.MediaManagerDock.setVisible)
        QtCore.QObject.connect(self.ViewServiceManagerItem, QtCore.SIGNAL("triggered(bool)"), self.ServiceManagerDock.setVisible)
        QtCore.QObject.connect(self.ViewThemeManagerItem, QtCore.SIGNAL("triggered(bool)"), self.ThemeManagerDock.setVisible)
        QtCore.QObject.connect(self.action_Preview_Pane, QtCore.SIGNAL("toggled(bool)"), self.PreviewController.Pane.setVisible)
        QtCore.QObject.connect(self.MediaManagerDock, QtCore.SIGNAL("visibilityChanged(bool)"), self.ViewMediaManagerItem.setChecked)
        QtCore.QObject.connect(self.ServiceManagerDock, QtCore.SIGNAL("visibilityChanged(bool)"), self.ViewServiceManagerItem.setChecked)
        QtCore.QObject.connect(self.ThemeManagerDock, QtCore.SIGNAL("visibilityChanged(bool)"), self.ViewThemeManagerItem.setChecked)
        QtCore.QMetaObject.connectSlotsByName(self.main_window)
        QtCore.QObject.connect(self.HelpAboutItem, QtCore.SIGNAL("triggered()"), self.onHelpAboutItemClicked)
        QtCore.QObject.connect(self.ToolsAlertItem, QtCore.SIGNAL("triggered()"), self.onToolsAlertItemClicked)
        QtCore.QObject.connect(self.OptionsSettingsItem, QtCore.SIGNAL("triggered()"), self.onOptionsSettingsItemClicked)


    def retranslateUi(self):
        self.main_window.setWindowTitle(QtGui.QApplication.translate("main_window", "openlp.org 2.0", None, QtGui.QApplication.UnicodeUTF8))
        self.FileMenu.setTitle(QtGui.QApplication.translate("main_window", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.FileImportMenu.setTitle(QtGui.QApplication.translate("main_window", "&Import", None, QtGui.QApplication.UnicodeUTF8))
        self.FileExportMenu.setTitle(QtGui.QApplication.translate("main_window", "&Export", None, QtGui.QApplication.UnicodeUTF8))
        self.OptionsMenu.setTitle(QtGui.QApplication.translate("main_window", "&Options", None, QtGui.QApplication.UnicodeUTF8))
        self.OptionsViewMenu.setTitle(QtGui.QApplication.translate("main_window", "&View", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewModeMenu.setTitle(QtGui.QApplication.translate("main_window", "M&ode", None, QtGui.QApplication.UnicodeUTF8))
        self.OptionsLanguageMenu.setTitle(QtGui.QApplication.translate("main_window", "&Language", None, QtGui.QApplication.UnicodeUTF8))
        self.ToolsMenu.setTitle(QtGui.QApplication.translate("main_window", "&Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.HelpMenu.setTitle(QtGui.QApplication.translate("main_window", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.MediaManagerDock.setWindowTitle(QtGui.QApplication.translate("main_window", "Media Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.ServiceManagerDock.setWindowTitle(QtGui.QApplication.translate("main_window", "Service Manager", None, QtGui.QApplication.UnicodeUTF8))
#         self.ServiceManagerContents.MoveTopButton.setText(QtGui.QApplication.translate("main_window", "Move To Top", None, QtGui.QApplication.UnicodeUTF8))
#         self.ServiceManagerContents.MoveUpButton.setText(QtGui.QApplication.translate("main_window", "Move Up", None, QtGui.QApplication.UnicodeUTF8))
#         self.ServiceManagerContents.MoveDownButton.setText(QtGui.QApplication.translate("main_window", "Move Down", None, QtGui.QApplication.UnicodeUTF8))
#         self.ServiceManagerContents.MoveBottomButton.setText(QtGui.QApplication.translate("main_window", "Move To Bottom", None, QtGui.QApplication.UnicodeUTF8))
#         self.ServiceManagerContents.NewItem.setText(QtGui.QApplication.translate("main_window", "New Service", None, QtGui.QApplication.UnicodeUTF8))
#         self.ServiceManagerContents.OpenItem.setText(QtGui.QApplication.translate("main_window", "Open Service", None, QtGui.QApplication.UnicodeUTF8))
#         self.ServiceManagerContents.SaveItem.setText(QtGui.QApplication.translate("main_window", "Save Service", None, QtGui.QApplication.UnicodeUTF8))
#         self.ServiceManagerContents.ThemeComboBox.setItemText(0, QtGui.QApplication.translate("main_window", "African Sunset", None, QtGui.QApplication.UnicodeUTF8))
#         self.ServiceManagerContents.ThemeComboBox.setItemText(1, QtGui.QApplication.translate("main_window", "Snowy Mountains", None, QtGui.QApplication.UnicodeUTF8))
#         self.ServiceManagerContents.ThemeComboBox.setItemText(2, QtGui.QApplication.translate("main_window", "Wilderness", None, QtGui.QApplication.UnicodeUTF8))
        self.ThemeManagerDock.setWindowTitle(QtGui.QApplication.translate("main_window", "Theme Manager", None, QtGui.QApplication.UnicodeUTF8))
#        self.ThemeNewItem.setText(QtGui.QApplication.translate("main_window", "New Theme", None, QtGui.QApplication.UnicodeUTF8))
#        self.ThemeEditItem.setText(QtGui.QApplication.translate("main_window", "Edit Theme", None, QtGui.QApplication.UnicodeUTF8))
#        self.ThemeDeleteButton.setText(QtGui.QApplication.translate("main_window", "Delete Theme", None, QtGui.QApplication.UnicodeUTF8))
#        self.ThemeImportButton.setText(QtGui.QApplication.translate("main_window", "Import Theme", None, QtGui.QApplication.UnicodeUTF8))
#        self.ThemeExportButton.setText(QtGui.QApplication.translate("main_window", "Export Theme", None, QtGui.QApplication.UnicodeUTF8))
        self.FileNewItem.setText(QtGui.QApplication.translate("main_window", "&New", None, QtGui.QApplication.UnicodeUTF8))
        self.FileNewItem.setToolTip(QtGui.QApplication.translate("main_window", "New Service", None, QtGui.QApplication.UnicodeUTF8))
        self.FileNewItem.setStatusTip(QtGui.QApplication.translate("main_window", "Create a new Service", None, QtGui.QApplication.UnicodeUTF8))
        self.FileNewItem.setShortcut(QtGui.QApplication.translate("main_window", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.FileOpenItem.setText(QtGui.QApplication.translate("main_window", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.FileOpenItem.setToolTip(QtGui.QApplication.translate("main_window", "Open Service", None, QtGui.QApplication.UnicodeUTF8))
        self.FileOpenItem.setStatusTip(QtGui.QApplication.translate("main_window", "Open an existing service", None, QtGui.QApplication.UnicodeUTF8))
        self.FileOpenItem.setShortcut(QtGui.QApplication.translate("main_window", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.FileSaveItem.setText(QtGui.QApplication.translate("main_window", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.FileSaveItem.setToolTip(QtGui.QApplication.translate("main_window", "Save Service", None, QtGui.QApplication.UnicodeUTF8))
        self.FileSaveItem.setStatusTip(QtGui.QApplication.translate("main_window", "Save the current service to disk", None, QtGui.QApplication.UnicodeUTF8))
        self.FileSaveItem.setShortcut(QtGui.QApplication.translate("main_window", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.FileSaveAsItem.setText(QtGui.QApplication.translate("main_window", "Save &As...", None, QtGui.QApplication.UnicodeUTF8))
        self.FileSaveAsItem.setToolTip(QtGui.QApplication.translate("main_window", "Save Service As", None, QtGui.QApplication.UnicodeUTF8))
        self.FileSaveAsItem.setStatusTip(QtGui.QApplication.translate("main_window", "Save the current service under a new name", None, QtGui.QApplication.UnicodeUTF8))
        self.FileSaveAsItem.setShortcut(QtGui.QApplication.translate("main_window", "F12", None, QtGui.QApplication.UnicodeUTF8))
        self.FileExitItem.setText(QtGui.QApplication.translate("main_window", "E&xit", None, QtGui.QApplication.UnicodeUTF8))
        self.FileExitItem.setStatusTip(QtGui.QApplication.translate("main_window", "Quit OpenLP 2.0", None, QtGui.QApplication.UnicodeUTF8))
        self.FileExitItem.setShortcut(QtGui.QApplication.translate("main_window", "Alt+F4", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportThemeItem.setText(QtGui.QApplication.translate("main_window", "&Theme", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportLanguageItem.setText(QtGui.QApplication.translate("main_window", "&Language", None, QtGui.QApplication.UnicodeUTF8))
        self.ExportThemeItem.setText(QtGui.QApplication.translate("main_window", "&Theme", None, QtGui.QApplication.UnicodeUTF8))
        self.ExportLanguageItem.setText(QtGui.QApplication.translate("main_window", "&Language", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLook_Feel.setText(QtGui.QApplication.translate("main_window", "Look && &Feel", None, QtGui.QApplication.UnicodeUTF8))
        self.OptionsSettingsItem.setText(QtGui.QApplication.translate("main_window", "&Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewMediaManagerItem.setText(QtGui.QApplication.translate("main_window", "&Media Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewMediaManagerItem.setToolTip(QtGui.QApplication.translate("main_window", "Toggle Media Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewMediaManagerItem.setStatusTip(QtGui.QApplication.translate("main_window", "Toggle the visibility of the Media Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewMediaManagerItem.setShortcut(QtGui.QApplication.translate("main_window", "F8", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewThemeManagerItem.setText(QtGui.QApplication.translate("main_window", "&Theme Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewThemeManagerItem.setToolTip(QtGui.QApplication.translate("main_window", "Toggle Theme Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewThemeManagerItem.setStatusTip(QtGui.QApplication.translate("main_window", "Toggle the visibility of the Theme Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewThemeManagerItem.setShortcut(QtGui.QApplication.translate("main_window", "F10", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewServiceManagerItem.setText(QtGui.QApplication.translate("main_window", "&Service Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewServiceManagerItem.setToolTip(QtGui.QApplication.translate("main_window", "Toggle Service Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewServiceManagerItem.setStatusTip(QtGui.QApplication.translate("main_window", "Toggle the visibility of the Service Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.ViewServiceManagerItem.setShortcut(QtGui.QApplication.translate("main_window", "F9", None, QtGui.QApplication.UnicodeUTF8))
        self.ToolsAlertItem.setText(QtGui.QApplication.translate("main_window", "&Alert", None, QtGui.QApplication.UnicodeUTF8))
        self.ToolsAlertItem.setStatusTip(QtGui.QApplication.translate("main_window", "Show an alert message", None, QtGui.QApplication.UnicodeUTF8))
        self.ToolsAlertItem.setShortcut(QtGui.QApplication.translate("main_window", "F7", None, QtGui.QApplication.UnicodeUTF8))
        self.HelpDocumentationItem.setText(QtGui.QApplication.translate("main_window", "&User Guide", None, QtGui.QApplication.UnicodeUTF8))
        self.HelpAboutItem.setText(QtGui.QApplication.translate("main_window", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.HelpAboutItem.setStatusTip(QtGui.QApplication.translate("main_window", "More information about OpenLP", None, QtGui.QApplication.UnicodeUTF8))
        self.HelpAboutItem.setShortcut(QtGui.QApplication.translate("main_window", "Ctrl+F1", None, QtGui.QApplication.UnicodeUTF8))
        self.HelpOnlineHelpItem.setText(QtGui.QApplication.translate("main_window", "&Online Help", None, QtGui.QApplication.UnicodeUTF8))
        self.HelpWebSiteItem.setText(QtGui.QApplication.translate("main_window", "&Web Site", None, QtGui.QApplication.UnicodeUTF8))
        self.LanguageTranslateItem.setText(QtGui.QApplication.translate("main_window", "&Translate", None, QtGui.QApplication.UnicodeUTF8))
        self.LanguageTranslateItem.setStatusTip(QtGui.QApplication.translate("main_window", "Translate the interface to your language", None, QtGui.QApplication.UnicodeUTF8))
        self.LanguageEnglishItem.setText(QtGui.QApplication.translate("main_window", "English", None, QtGui.QApplication.UnicodeUTF8))
        self.LanguageEnglishItem.setStatusTip(QtGui.QApplication.translate("main_window", "Set the interface language to English", None, QtGui.QApplication.UnicodeUTF8))
        self.ToolsAddToolItem.setText(QtGui.QApplication.translate("main_window", "&Add Tool...", None, QtGui.QApplication.UnicodeUTF8))
        self.ToolsAddToolItem.setStatusTip(QtGui.QApplication.translate("main_window", "Add an application to the list of tools", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Preview_Pane.setText(QtGui.QApplication.translate("main_window", "&Preview Pane", None, QtGui.QApplication.UnicodeUTF8))
        self.ModeLiveItem.setText(QtGui.QApplication.translate("main_window", "&Live", None, QtGui.QApplication.UnicodeUTF8))

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
