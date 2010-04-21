# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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
import time

from PyQt4 import QtCore, QtGui

from openlp.core.ui import AboutForm, SettingsForm,  \
    ServiceManager, ThemeManager, SlideController, \
    PluginForm, MediaDockManager, DisplayManager
from openlp.core.lib import RenderManager, PluginConfig, build_icon, \
    OpenLPDockWidget, SettingsManager, PluginManager, Receiver, str_to_bool
from openlp.core.utils import check_latest_version, AppLocation

log = logging.getLogger(__name__)

media_manager_style = """
  QToolBox::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 palette(button), stop: 1.0 palette(dark));
    border-width: 1px;
    border-style: outset;
    border-color: palette(dark);
    border-radius: 5px;
  }
  QToolBox::tab:selected {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 palette(light), stop: 1.0 palette(button));
    border-color: palette(button);
  }
"""
class VersionThread(QtCore.QThread):
    """
    A special Qt thread class to fetch the version of OpenLP from the website.
    This is threaded so that it doesn't affect the loading time of OpenLP.
    """
    def __init__(self, parent, app_version, generalConfig):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
        self.app_version = app_version
        self.generalConfig = generalConfig

    def run(self):
        """
        Run the thread.
        """
        time.sleep(1)
        Receiver.send_message(u'blank_check')
        version = check_latest_version(self.generalConfig, self.app_version)
        #new version has arrived
        if version != self.app_version[u'full']:
            Receiver.send_message(u'version_check', u'%s' % version)

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
        MediaManagerIcon = build_icon(u':/system/system_mediamanager.png')
        self.MediaManagerDock.setWindowIcon(MediaManagerIcon)
        self.MediaManagerDock.setStyleSheet(media_manager_style)
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
        self.MediaManagerDock.setVisible(self.settingsmanager.showMediaManager)
        # Create the service manager
        self.ServiceManagerDock = OpenLPDockWidget(MainWindow)
        ServiceManagerIcon = build_icon(u':/system/system_servicemanager.png')
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
        ThemeManagerIcon = build_icon(u':/system/system_thememanager.png')
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
        ExitIcon = build_icon(u':/system/system_exit.png')
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
        SettingsIcon = build_icon(u':/system/system_settings.png')
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
        self.PluginItem = QtGui.QAction(MainWindow)
        #self.PluginItem.setIcon(AlertIcon)
        self.PluginItem.setObjectName(u'PluginItem')
        self.HelpDocumentationItem = QtGui.QAction(MainWindow)
        ContentsIcon = build_icon(u':/system/system_help_contents.png')
        self.HelpDocumentationItem.setIcon(ContentsIcon)
        self.HelpDocumentationItem.setObjectName(u'HelpDocumentationItem')
        self.HelpAboutItem = QtGui.QAction(MainWindow)
        AboutIcon = build_icon(u':/system/system_about.png')
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
        AddToolIcon = build_icon(u':/tools/tools_add.png')
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
        MainWindow.mainTitle = self.trUtf8('OpenLP 2.0')
        MainWindow.defaultThemeText = self.trUtf8(
            'Default Theme: ')
        MainWindow.setWindowTitle(MainWindow.mainTitle)
        self.FileMenu.setTitle(self.trUtf8('&File'))
        self.FileImportMenu.setTitle(self.trUtf8('&Import'))
        self.FileExportMenu.setTitle(self.trUtf8('&Export'))
        self.OptionsMenu.setTitle(self.trUtf8('&Options'))
        self.OptionsViewMenu.setTitle(self.trUtf8('&View'))
        self.ViewModeMenu.setTitle(self.trUtf8('M&ode'))
        self.OptionsLanguageMenu.setTitle(self.trUtf8(
            u'&Language'))
        self.ToolsMenu.setTitle(self.trUtf8('&Tools'))
        self.HelpMenu.setTitle(self.trUtf8('&Help'))
        self.MediaManagerDock.setWindowTitle(
            self.trUtf8('Media Manager'))
        self.ServiceManagerDock.setWindowTitle(
            self.trUtf8('Service Manager'))
        self.ThemeManagerDock.setWindowTitle(
            self.trUtf8('Theme Manager'))
        self.FileNewItem.setText(self.trUtf8('&New'))
        self.FileNewItem.setToolTip(self.trUtf8('New Service'))
        self.FileNewItem.setStatusTip(self.trUtf8('Create a new Service'))
        self.FileNewItem.setShortcut(self.trUtf8('Ctrl+N'))
        self.FileOpenItem.setText(self.trUtf8('&Open'))
        self.FileOpenItem.setToolTip(self.trUtf8('Open Service'))
        self.FileOpenItem.setStatusTip(self.trUtf8('Open an existing service'))
        self.FileOpenItem.setShortcut(self.trUtf8('Ctrl+O'))
        self.FileSaveItem.setText(self.trUtf8('&Save'))
        self.FileSaveItem.setToolTip(self.trUtf8('Save Service'))
        self.FileSaveItem.setStatusTip(
            self.trUtf8('Save the current service to disk'))
        self.FileSaveItem.setShortcut(self.trUtf8('Ctrl+S'))
        self.FileSaveAsItem.setText(self.trUtf8('Save &As...'))
        self.FileSaveAsItem.setToolTip(self.trUtf8('Save Service As'))
        self.FileSaveAsItem.setStatusTip(
            self.trUtf8('Save the current service under a new name'))
        self.FileSaveAsItem.setShortcut(self.trUtf8('F12'))
        self.FileExitItem.setText(self.trUtf8('E&xit'))
        self.FileExitItem.setStatusTip(self.trUtf8('Quit OpenLP'))
        self.FileExitItem.setShortcut(self.trUtf8('Alt+F4'))
        self.ImportThemeItem.setText(self.trUtf8('&Theme'))
        self.ImportLanguageItem.setText(self.trUtf8('&Language'))
        self.ExportThemeItem.setText(self.trUtf8('&Theme'))
        self.ExportLanguageItem.setText(self.trUtf8('&Language'))
        self.actionLook_Feel.setText(self.trUtf8('Look && &Feel'))
        self.OptionsSettingsItem.setText(self.trUtf8('&Settings'))
        self.ViewMediaManagerItem.setText(self.trUtf8('&Media Manager'))
        self.ViewMediaManagerItem.setToolTip(self.trUtf8('Toggle Media Manager'))
        self.ViewMediaManagerItem.setStatusTip(
            self.trUtf8('Toggle the visibility of the Media Manager'))
        self.ViewMediaManagerItem.setShortcut(self.trUtf8('F8'))
        self.ViewThemeManagerItem.setText(self.trUtf8('&Theme Manager'))
        self.ViewThemeManagerItem.setToolTip(self.trUtf8('Toggle Theme Manager'))
        self.ViewThemeManagerItem.setStatusTip(
            self.trUtf8('Toggle the visibility of the Theme Manager'))
        self.ViewThemeManagerItem.setShortcut(self.trUtf8('F10'))
        self.ViewServiceManagerItem.setText(self.trUtf8('&Service Manager'))
        self.ViewServiceManagerItem.setToolTip(
            self.trUtf8('Toggle Service Manager'))
        self.ViewServiceManagerItem.setStatusTip(
            self.trUtf8('Toggle the visibility of the Service Manager'))
        self.ViewServiceManagerItem.setShortcut(self.trUtf8('F9'))
        self.action_Preview_Panel.setText(self.trUtf8('&Preview Panel'))
        self.action_Preview_Panel.setToolTip(self.trUtf8('Toggle Preview Panel'))
        self.action_Preview_Panel.setStatusTip(
            self.trUtf8('Toggle the visibility of the Preview Panel'))
        self.action_Preview_Panel.setShortcut(self.trUtf8('F11'))
        self.PluginItem.setText(self.trUtf8('&Plugin List'))
        self.PluginItem.setStatusTip(self.trUtf8('List the Plugins'))
        self.PluginItem.setShortcut(self.trUtf8('Alt+F7'))
        self.HelpDocumentationItem.setText(self.trUtf8('&User Guide'))
        self.HelpAboutItem.setText(self.trUtf8('&About'))
        self.HelpAboutItem.setStatusTip(
            self.trUtf8('More information about OpenLP'))
        self.HelpAboutItem.setShortcut(self.trUtf8('Ctrl+F1'))
        self.HelpOnlineHelpItem.setText(self.trUtf8('&Online Help'))
        self.HelpWebSiteItem.setText(self.trUtf8('&Web Site'))
        self.LanguageTranslateItem.setText(self.trUtf8('&Translate'))
        self.LanguageTranslateItem.setStatusTip(
            self.trUtf8('Translate the interface to your language'))
        self.LanguageEnglishItem.setText(self.trUtf8('English'))
        self.LanguageEnglishItem.setStatusTip(
            self.trUtf8('Set the interface language to English'))
        self.ToolsAddToolItem.setText(self.trUtf8('Add &Tool...'))
        self.ToolsAddToolItem.setStatusTip(
            self.trUtf8('Add an application to the list of tools'))
        self.action_Preview_Panel.setText(self.trUtf8('&Preview Pane'))
        self.ModeLiveItem.setText(self.trUtf8('&Live'))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    The main window.
    """
    log.info(u'MainWindow loaded')

    def __init__(self, screens, applicationVersion):
        """
        This constructor sets up the interface, the various managers, and the
        plugins.
        """
        QtGui.QMainWindow.__init__(self)
        self.screens = screens
        self.applicationVersion = applicationVersion
        self.serviceNotSaved = False
        self.settingsmanager = SettingsManager(screens)
        self.generalConfig = PluginConfig(u'General')
        self.displayManager = DisplayManager(screens)
        self.aboutForm = AboutForm(self, applicationVersion)
        self.settingsForm = SettingsForm(self.screens, self, self)
        # Set up the path with plugins
        pluginpath = AppLocation.get_directory(AppLocation.PluginsDir)
        self.plugin_manager = PluginManager(pluginpath)
        self.plugin_helpers = {}
        # Set up the interface
        self.setupUi(self)
        self.pluginForm = PluginForm(self)
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
        QtCore.QObject.connect(self.PluginItem,
            QtCore.SIGNAL(u'triggered()'), self.onPluginItemClicked)
        QtCore.QObject.connect(self.OptionsSettingsItem,
            QtCore.SIGNAL(u'triggered()'), self.onOptionsSettingsItemClicked)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'update_global_theme'), self.defaultThemeChanged)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'version_check'), self.versionCheck)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'blank_check'), self.blankCheck)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'screen_changed'), self.screenChanged)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'status_message'), self.showStatusMessage)
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
                                            self.screens)
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
        self.plugin_helpers[u'maindisplay'] = self.displayManager.mainDisplay
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

    def versionCheck(self, version):
        """
        Checks the version of the Application called from openlp.pyw
        Triggered by delay thread.
        """
        app_version = self.applicationVersion[u'full']
        version_text = unicode(self.trUtf8('Version %s of OpenLP is now '
            'available for download (you are currently running version %s).'
            '\n\nYou can download the latest version from http://openlp.org'))
        QtGui.QMessageBox.question(self,
            self.trUtf8('OpenLP Version Updated'),
            version_text % (version, app_version),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok),
            QtGui.QMessageBox.Ok)

    def show(self):
        """
        Show the main form, as well as the display form
        """
        self.showMaximized()
        #screen_number = self.getMonitorNumber()
        self.displayManager.setup()
        if self.displayManager.mainDisplay.isVisible():
            self.displayManager.mainDisplay.setFocus()
        self.activateWindow()
        if str_to_bool(self.generalConfig.get_config(u'auto open', False)):
            self.ServiceManagerContents.onLoadService(True)

    def blankCheck(self):
        """
        Check and display message if screen blank on setup.
        Triggered by delay thread.
        """
        if str_to_bool(self.generalConfig.get_config(u'screen blank', False)) \
        and str_to_bool(self.generalConfig.get_config(u'blank warning', False)):
            self.LiveController.onBlankDisplay(True)
            QtGui.QMessageBox.question(self,
                self.trUtf8('OpenLP Main Display Blanked'),
                self.trUtf8('The Main Display has been blanked out'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok),
                QtGui.QMessageBox.Ok)

    def versionThread(self):
        """
        Start an initial setup thread to delay notifications
        """
        vT = VersionThread(self, self.applicationVersion, self.generalConfig)
        vT.start()

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

    def onOptionsSettingsItemClicked(self):
        """
        Show the Settings dialog
        """
        self.settingsForm.exec_()

    def screenChanged(self):
        """
        The screen has changed to so tell the displays to update_display
        their locations
        """
        self.RenderManager.update_display()
        self.displayManager.setup()
        self.setFocus()
        self.activateWindow()

    def closeEvent(self, event):
        """
        Hook to close the main window and display windows on exit
        """
        if self.serviceNotSaved:
            ret = QtGui.QMessageBox.question(self,
                self.trUtf8('Save Changes to Service?'),
                self.trUtf8('Your service has changed, do you want to save those changes?'),
                QtGui.QMessageBox.StandardButtons(
                    QtGui.QMessageBox.Cancel |
                    QtGui.QMessageBox.Discard |
                    QtGui.QMessageBox.Save),
                QtGui.QMessageBox.Save)
            if ret == QtGui.QMessageBox.Save:
                self.ServiceManagerContents.onSaveService()
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
        # Call the cleanup method to shutdown plugins.
        log.info(u'cleanup plugins')
        self.plugin_manager.finalise_plugins()
        #Close down the displays
        self.displayManager.close()

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
            u'%s %s' % (self.defaultThemeText, theme))

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
