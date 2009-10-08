# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

import os
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.ui import AboutForm, SettingsForm, AlertForm, \
    ServiceManager, ThemeManager, MainDisplay, SlideController, \
    PluginForm, MediaDockManager
from openlp.core.lib import translate, RenderManager, PluginConfig, \
    OpenLPDockWidget, SettingsManager, PluginManager, Receiver, \
    buildIcon


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
        MainIcon = buildIcon(u':/icon/openlp-logo-16x16.png')
        MainWindow.setWindowIcon(MainIcon)
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
        self.ControlSplitter.setObjectName(u'ControlSplitter')
        self.MainContentLayout.addWidget(self.ControlSplitter)
        # Create slide controllers
        self.PreviewController = SlideController(self, self.settingsmanager)
        self.LiveController = SlideController(self, self.settingsmanager, True)
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
        MainWindow.setMenuBar(self.MenuBar)
        self.StatusBar = QtGui.QStatusBar(MainWindow)
        self.StatusBar.setObjectName(u'StatusBar')
        MainWindow.setStatusBar(self.StatusBar)
        self.DefaultThemeLabel = QtGui.QLabel(self.StatusBar)
        self.DefaultThemeLabel.setObjectName(u'DefaultThemeLabel')
        self.StatusBar.addPermanentWidget(self.DefaultThemeLabel)
        # Create the MediaManager
        self.MediaManagerDock = OpenLPDockWidget(MainWindow)
        MediaManagerIcon = buildIcon(u':/system/system_mediamanager.png')
        self.MediaManagerDock.setWindowIcon(MediaManagerIcon)
        self.MediaManagerDock.setObjectName(u'MediaManagerDock')
        self.MediaManagerDock.setMinimumWidth(
            self.settingsmanager.mainwindow_left)
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
        self.MediaManagerDock.setVisible(self.settingsmanager.showMediaManager)
        # Create the service manager
        self.ServiceManagerDock = OpenLPDockWidget(MainWindow)
        ServiceManagerIcon = buildIcon(u':/system/system_servicemanager.png')
        self.ServiceManagerDock.setWindowIcon(ServiceManagerIcon)
        self.ServiceManagerDock.setObjectName(u'ServiceManagerDock')
        self.ServiceManagerDock.setMinimumWidth(
            self.settingsmanager.mainwindow_right)
        self.ServiceManagerContents = ServiceManager(self)
        self.ServiceManagerDock.setWidget(self.ServiceManagerContents)
        MainWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(2), self.ServiceManagerDock)
        self.ServiceManagerDock.setVisible(
            self.settingsmanager.showServiceManager)
        # Create the theme manager
        self.ThemeManagerDock = OpenLPDockWidget(MainWindow)
        ThemeManagerIcon = buildIcon(u':/system/system_thememanager.png')
        self.ThemeManagerDock.setWindowIcon(ThemeManagerIcon)
        self.ThemeManagerDock.setObjectName(u'ThemeManagerDock')
        self.ThemeManagerContents = ThemeManager(self)
        self.ThemeManagerDock.setWidget(self.ThemeManagerContents)
        MainWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(2), self.ThemeManagerDock)
        self.ThemeManagerDock.setVisible(self.settingsmanager.showThemeManager)
        # Create the menu items
        self.FileNewItem = QtGui.QAction(MainWindow)
        self.FileNewItem.setIcon(
            self.ServiceManagerContents.Toolbar.getIconFromTitle(
            u'New Service'))
        self.FileNewItem.setObjectName(u'FileNewItem')
        self.FileOpenItem = QtGui.QAction(MainWindow)
        self.FileOpenItem.setIcon(
            self.ServiceManagerContents.Toolbar.getIconFromTitle(
            u'Open Service'))
        self.FileOpenItem.setObjectName(u'FileOpenItem')
        self.FileSaveItem = QtGui.QAction(MainWindow)
        self.FileSaveItem.setIcon(
            self.ServiceManagerContents.Toolbar.getIconFromTitle(
            u'Save Service'))
        self.FileSaveItem.setObjectName(u'FileSaveItem')
        self.FileSaveAsItem = QtGui.QAction(MainWindow)
        self.FileSaveAsItem.setObjectName(u'FileSaveAsItem')
        self.FileExitItem = QtGui.QAction(MainWindow)
        ExitIcon = buildIcon(u':/system/system_exit.png')
        self.FileExitItem.setIcon(ExitIcon)
        self.FileExitItem.setObjectName(u'FileExitItem')
        self.ImportThemeItem = QtGui.QAction(MainWindow)
        self.ImportThemeItem.setObjectName(u'ImportThemeItem')
        self.ImportLanguageItem = QtGui.QAction(MainWindow)
        self.ImportLanguageItem.setObjectName(u'ImportLanguageItem')
        self.ExportThemeItem = QtGui.QAction(MainWindow)
        self.ExportThemeItem.setObjectName(u'ExportThemeItem')
        self.ExportLanguageItem = QtGui.QAction(MainWindow)
        self.ExportLanguageItem.setObjectName(u'ExportLanguageItem')
        self.actionLook_Feel = QtGui.QAction(MainWindow)
        self.actionLook_Feel.setObjectName(u'actionLook_Feel')
        self.OptionsSettingsItem = QtGui.QAction(MainWindow)
        SettingsIcon = buildIcon(u':/system/system_settings.png')
        self.OptionsSettingsItem.setIcon(SettingsIcon)
        self.OptionsSettingsItem.setObjectName(u'OptionsSettingsItem')
        self.ViewMediaManagerItem = QtGui.QAction(MainWindow)
        self.ViewMediaManagerItem.setCheckable(True)
        self.ViewMediaManagerItem.setChecked(
            self.settingsmanager.showMediaManager)
        self.ViewMediaManagerItem.setIcon(MediaManagerIcon)
        self.ViewMediaManagerItem.setObjectName(u'ViewMediaManagerItem')
        self.ViewThemeManagerItem = QtGui.QAction(MainWindow)
        self.ViewThemeManagerItem.setCheckable(True)
        self.ViewThemeManagerItem.setChecked(
            self.settingsmanager.showThemeManager)
        self.ViewThemeManagerItem.setIcon(ThemeManagerIcon)
        self.ViewThemeManagerItem.setObjectName(u'ViewThemeManagerItem')
        self.ViewServiceManagerItem = QtGui.QAction(MainWindow)
        self.ViewServiceManagerItem.setCheckable(True)
        self.ViewServiceManagerItem.setChecked(
            self.settingsmanager.showServiceManager)
        self.ViewServiceManagerItem.setIcon(ServiceManagerIcon)
        self.ViewServiceManagerItem.setObjectName(u'ViewServiceManagerItem')
        self.ToolsAlertItem = QtGui.QAction(MainWindow)
        AlertIcon = buildIcon(u':/tools/tools_alert.png')
        self.ToolsAlertItem.setIcon(AlertIcon)
        self.ToolsAlertItem.setObjectName(u'ToolsAlertItem')
        self.PluginItem = QtGui.QAction(MainWindow)
        #PluginIcon = buildIcon(u':/tools/tools_alert.png')
        self.PluginItem.setIcon(AlertIcon)
        self.PluginItem.setObjectName(u'PluginItem')
        self.HelpDocumentationItem = QtGui.QAction(MainWindow)
        ContentsIcon = buildIcon(u':/system/system_help_contents.png')
        self.HelpDocumentationItem.setIcon(ContentsIcon)
        self.HelpDocumentationItem.setObjectName(u'HelpDocumentationItem')
        self.HelpAboutItem = QtGui.QAction(MainWindow)
        AboutIcon = buildIcon(u':/system/system_about.png')
        self.HelpAboutItem.setIcon(AboutIcon)
        self.HelpAboutItem.setObjectName(u'HelpAboutItem')
        self.HelpOnlineHelpItem = QtGui.QAction(MainWindow)
        self.HelpOnlineHelpItem.setObjectName(u'HelpOnlineHelpItem')
        self.HelpWebSiteItem = QtGui.QAction(MainWindow)
        self.HelpWebSiteItem.setObjectName(u'HelpWebSiteItem')
        self.LanguageTranslateItem = QtGui.QAction(MainWindow)
        self.LanguageTranslateItem.setObjectName(u'LanguageTranslateItem')
        self.LanguageEnglishItem = QtGui.QAction(MainWindow)
        self.LanguageEnglishItem.setObjectName(u'LanguageEnglishItem')
        self.ToolsAddToolItem = QtGui.QAction(MainWindow)
        AddToolIcon = buildIcon(u':/tools/tools_add.png')
        self.ToolsAddToolItem.setIcon(AddToolIcon)
        self.ToolsAddToolItem.setObjectName(u'ToolsAddToolItem')
        self.action_Preview_Panel = QtGui.QAction(MainWindow)
        self.action_Preview_Panel.setCheckable(True)
        self.action_Preview_Panel.setChecked(
            self.settingsmanager.showPreviewPanel)
        self.action_Preview_Panel.setObjectName(u'action_Preview_Panel')
        self.PreviewController.Panel.setVisible(
            self.settingsmanager.showPreviewPanel)
        self.ModeLiveItem = QtGui.QAction(MainWindow)
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
        self.ToolsMenu.addAction(self.PluginItem)
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
        self.retranslateUi(MainWindow)
        self.MediaToolBox.setCurrentIndex(0)
        # Connect up some signals and slots
        QtCore.QObject.connect(self.FileExitItem,
            QtCore.SIGNAL(u'triggered()'), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Set up the translation system
        """
        MainWindow.mainTitle = translate(u'mainWindow', u'OpenLP 2.0')
        MainWindow.defaultThemeText = translate(u'mainWindow',
            'Default Theme: ')
        MainWindow.setWindowTitle(MainWindow.mainTitle)
        self.FileMenu.setTitle(translate(u'mainWindow', u'&File'))
        self.FileImportMenu.setTitle(translate(u'mainWindow', u'&Import'))
        self.FileExportMenu.setTitle(translate(u'mainWindow', u'&Export'))
        self.OptionsMenu.setTitle(translate(u'mainWindow', u'&Options'))
        self.OptionsViewMenu.setTitle(translate(u'mainWindow', u'&View'))
        self.ViewModeMenu.setTitle(translate(u'mainWindow', u'M&ode'))
        self.OptionsLanguageMenu.setTitle(translate(u'mainWindow',
            u'&Language'))
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
        self.action_Preview_Panel.setText(
            translate(u'mainWindow', u'&Preview Panel'))
        self.action_Preview_Panel.setToolTip(
            translate(u'mainWindow', u'Toggle Preview Panel'))
        self.action_Preview_Panel.setStatusTip(translate(u'mainWindow',
            u'Toggle the visibility of the Preview Panel'))
        self.action_Preview_Panel.setShortcut(translate(u'mainWindow', u'F11'))
        self.ToolsAlertItem.setText(translate(u'mainWindow', u'Nursery &Alert'))
        self.ToolsAlertItem.setStatusTip(
            translate(u'mainWindow', u'Show an alert message'))
        self.ToolsAlertItem.setShortcut(translate(u'mainWindow', u'F7'))
        self.PluginItem.setText(translate(u'mainWindow', u'&Plugin List'))
        self.PluginItem.setStatusTip(
            translate(u'mainWindow', u'List the Plugins'))
        self.PluginItem.setShortcut(translate(u'mainWindow', u'Alt+F7'))
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


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
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
        QtGui.QMainWindow.__init__(self)
        self.closeEvent = self.onCloseEvent
        self.screenList = screens
        self.serviceNotSaved = False
        self.settingsmanager = SettingsManager(screens)
        self.mainDisplay = MainDisplay(self, screens)
        self.generalConfig = PluginConfig(u'General')
        self.alertForm = AlertForm(self)
        self.pluginForm = PluginForm(self)
        self.aboutForm = AboutForm(self)
        self.settingsForm = SettingsForm(self.screenList, self)
        # Set up the path with plugins
        pluginpath = os.path.split(os.path.abspath(__file__))[0]
        pluginpath = os.path.abspath(
            os.path.join(pluginpath, u'..', u'..', u'plugins'))
        self.plugin_manager = PluginManager(pluginpath)
        self.plugin_helpers = {}
        # Set up the interface
        self.setupUi(self)
        # Set up signals and slots
        QtCore.QObject.connect(self.ImportThemeItem,
            QtCore.SIGNAL(u'triggered()'),
            self.ThemeManagerContents.onImportTheme)
        QtCore.QObject.connect(self.ExportThemeItem,
            QtCore.SIGNAL(u'triggered()'),
            self.ThemeManagerContents.onExportTheme)
        QtCore.QObject.connect(self.ViewMediaManagerItem,
            QtCore.SIGNAL(u'triggered(bool)'),
            self.toggleMediaManager)
        QtCore.QObject.connect(self.ViewServiceManagerItem,
            QtCore.SIGNAL(u'triggered(bool)'),
            self.toggleServiceManager)
        QtCore.QObject.connect(self.ViewThemeManagerItem,
            QtCore.SIGNAL(u'triggered(bool)'),
            self.toggleThemeManager)
        QtCore.QObject.connect(self.action_Preview_Panel,
            QtCore.SIGNAL(u'toggled(bool)'),
            self.togglePreviewPanel)
        QtCore.QObject.connect(self.MediaManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.ViewMediaManagerItem.setChecked)
        QtCore.QObject.connect(self.ServiceManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.ViewServiceManagerItem.setChecked)
        QtCore.QObject.connect(self.ThemeManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.ViewThemeManagerItem.setChecked)
        QtCore.QObject.connect(self.PreviewController.Panel,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.action_Preview_Panel.setChecked)
        QtCore.QObject.connect(self.HelpAboutItem,
            QtCore.SIGNAL(u'triggered()'), self.onHelpAboutItemClicked)
        QtCore.QObject.connect(self.ToolsAlertItem,
            QtCore.SIGNAL(u'triggered()'), self.onToolsAlertItemClicked)
        QtCore.QObject.connect(self.PluginItem,
            QtCore.SIGNAL(u'triggered()'), self.onPluginItemClicked)
        QtCore.QObject.connect(self.OptionsSettingsItem,
            QtCore.SIGNAL(u'triggered()'), self.onOptionsSettingsItemClicked)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'update_global_theme'), self.defaultThemeChanged)
        QtCore.QObject.connect(self.FileNewItem,
            QtCore.SIGNAL(u'triggered()'),
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
        #warning cyclic dependency
        #RenderManager needs to call ThemeManager and
        #ThemeManager needs to call RenderManager
        self.RenderManager = RenderManager(self.ThemeManagerContents,
            self.screenList, self.getMonitorNumber())
        #Define the media Dock Manager
        self.mediaDockManager = MediaDockManager(self.MediaToolBox)
        log.info(u'Load Plugins')
        #make the controllers available to the plugins
        self.plugin_helpers[u'preview'] = self.PreviewController
        self.plugin_helpers[u'live'] = self.LiveController
        self.plugin_helpers[u'render'] = self.RenderManager
        self.plugin_helpers[u'service'] = self.ServiceManagerContents
        self.plugin_helpers[u'settings'] = self.settingsForm
        self.plugin_helpers[u'toolbox'] = self.mediaDockManager
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
        self.settingsForm.postSetUp()


    def getMonitorNumber(self):
        """
        Set up the default behaviour of the monitor configuration in
        here. Currently it is set to default to monitor 0 if the saved
        monitor number does not exist.
        """
        screen_number = int(self.generalConfig.get_config(u'Monitor', 0))

        monitor_exists = False
        for screen in self.screenList:
            if screen[u'number'] == screen_number:
                monitor_exists = True
        if not monitor_exists:
            screen_number = 0

        return screen_number

    def show(self):
        """
        Show the main form, as well as the display form
        """
        self.showMaximized()
        screen_number = self.getMonitorNumber()
        self.mainDisplay.setup(screen_number)
        self.setFocus()

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

    def onPluginItemClicked(self):
        """
        Show the Plugin form
        """
        self.pluginForm.load()
        self.pluginForm.exec_()

    def onOptionsSettingsItemClicked(self):
        """
        Show the Settings dialog
        """
        self.settingsForm.exec_()
        screen_number = self.getMonitorNumber()
        self.RenderManager.update_display(screen_number)
        self.mainDisplay.setup(screen_number)

    def onCloseEvent(self, event):
        """
        Hook to close the main window and display windows on exit
        """
        if self.serviceNotSaved == True:
            ret = QtGui.QMessageBox.question(None,
                translate(u'mainWindow', u'Save Changes to Service?'),
                translate(u'mainWindow', u'Your service has changed, do you want to save those changes?'),
                QtGui.QMessageBox.StandardButtons(
                    QtGui.QMessageBox.Cancel |
                    QtGui.QMessageBox.Discard |
                    QtGui.QMessageBox.Save),
                QtGui.QMessageBox.Save)
            if ret == QtGui.QMessageBox.Save:
                self.ServiceManagerContents.onSaveService()
                self.mainDisplay.close()
                self.cleanUp()
                event.accept()
            elif ret == QtGui.QMessageBox.Discard:
                self.mainDisplay.close()
                self.cleanUp()
                event.accept()
            else:
                event.ignore()
        else:
            self.mainDisplay.close()
            self.cleanUp()
            event.accept()

    def cleanUp(self):
        """
        Runs all the cleanup code before OpenLP shuts down
        """
        # Clean temporary files used by services
        self.ServiceManagerContents.cleanUp()
        # Call the cleanup method to shutdown plugins.
        log.info(u'cleanup plugins')
        self.plugin_manager.finalise_plugins()

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
        if reset == True:
            self.serviceNotSaved = False
            title = u'%s - %s' % (self.mainTitle, service_name)
        else:
            self.serviceNotSaved = True
            title = u'%s - %s*' % (self.mainTitle, service_name)
        self.setWindowTitle(title)

    def defaultThemeChanged(self, theme):
        self.DefaultThemeLabel.setText(self.defaultThemeText + theme)

    def toggleMediaManager(self, visible):
        if self.MediaManagerDock.isVisible() != visible:
            self.MediaManagerDock.setVisible(visible)
            self.settingsmanager.setUIItemVisibility(
                self.MediaManagerDock.objectName(), visible)

    def toggleServiceManager(self, visible):
        if self.ServiceManagerDock.isVisible() != visible:
            self.ServiceManagerDock.setVisible(visible)
            self.settingsmanager.setUIItemVisibility(
                self.ServiceManagerDock.objectName(), visible)

    def toggleThemeManager(self, visible):
        if self.ThemeManagerDock.isVisible() != visible:
            self.ThemeManagerDock.setVisible(visible)
            self.settingsmanager.setUIItemVisibility(
                self.ThemeManagerDock.objectName(), visible)

    def togglePreviewPanel(self):
        previewBool = self.PreviewController.Panel.isVisible()
        self.PreviewController.Panel.setVisible(not previewBool)
        self.settingsmanager.togglePreviewPanel(not previewBool)
