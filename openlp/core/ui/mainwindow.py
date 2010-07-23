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
import re

from PyQt4 import QtCore, QtGui

from openlp.core.ui import AboutForm, SettingsForm, ServiceManager, \
    ThemeManager, SlideController, PluginForm, MediaDockManager, DisplayManager
from openlp.core.lib import RenderManager, build_icon, OpenLPDockWidget, \
    SettingsManager, PluginManager, Receiver, translate
from openlp.core.utils import check_latest_version, AppLocation, add_actions, \
    LanguageManager

log = logging.getLogger(__name__)

MEDIA_MANAGER_STYLE = """
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
    def __init__(self, parent, app_version):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
        self.app_version = app_version
        self.version_splitter = re.compile(
            r'([0-9]+).([0-9]+).([0-9]+)(?:-bzr([0-9]+))?')

    def run(self):
        """
        Run the thread.
        """
        time.sleep(1)
        Receiver.send_message(u'maindisplay_blank_check')
        version = check_latest_version(self.app_version)
        remote_version = {}
        local_version = {}
        match = self.version_splitter.match(version)
        if match:
            remote_version[u'major'] = int(match.group(1))
            remote_version[u'minor'] = int(match.group(2))
            remote_version[u'release'] = int(match.group(3))
            if len(match.groups()) > 3 and match.group(4):
                remote_version[u'revision'] = int(match.group(4))
        match = self.version_splitter.match(self.app_version[u'full'])
        if match:
            local_version[u'major'] = int(match.group(1))
            local_version[u'minor'] = int(match.group(2))
            local_version[u'release'] = int(match.group(3))
            if len(match.groups()) > 3 and match.group(4):
                local_version[u'revision'] = int(match.group(4))
        if remote_version[u'major'] > local_version[u'major'] or \
            remote_version[u'minor'] > local_version[u'minor'] or \
            remote_version[u'release'] > local_version[u'release']:
            Receiver.send_message(u'openlp_version_check', u'%s' % version)
        elif remote_version.get(u'revision') and \
            local_version.get(u'revision') and \
            remote_version[u'revision'] > local_version[u'revision']:
            Receiver.send_message(u'openlp_version_check', u'%s' % version)

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
        self.FileExitItem.setIcon(build_icon(u':/system/system_exit.png'))
        self.FileExitItem.setObjectName(u'FileExitItem')
        self.ImportThemeItem = QtGui.QAction(MainWindow)
        self.ImportThemeItem.setObjectName(u'ImportThemeItem')
        self.ImportLanguageItem = QtGui.QAction(MainWindow)
        self.ImportLanguageItem.setObjectName(u'ImportLanguageItem')
        self.ExportThemeItem = QtGui.QAction(MainWindow)
        self.ExportThemeItem.setObjectName(u'ExportThemeItem')
        self.ExportLanguageItem = QtGui.QAction(MainWindow)
        self.ExportLanguageItem.setObjectName(u'ExportLanguageItem')
        self.SettingsConfigureItem = QtGui.QAction(MainWindow)
        self.SettingsConfigureItem.setIcon(
            build_icon(u':/system/system_settings.png'))
        self.SettingsConfigureItem.setObjectName(u'SettingsConfigureItem')
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
        self.ViewServiceManagerItem = QtGui.QAction(MainWindow)
        self.ViewServiceManagerItem.setCheckable(True)
        self.ViewServiceManagerItem.setChecked(
            self.ServiceManagerDock.isVisible())
        self.ViewServiceManagerItem.setIcon(
            build_icon(u':/system/system_servicemanager.png'))
        self.ViewServiceManagerItem.setObjectName(u'ViewServiceManagerItem')
        self.SettingsPluginListItem = QtGui.QAction(MainWindow)
        self.SettingsPluginListItem.setIcon(
            build_icon(u':/system/settings_plugin_list.png'))
        self.SettingsPluginListItem.setObjectName(u'SettingsPluginListItem')
        self.HelpDocumentationItem = QtGui.QAction(MainWindow)
        self.HelpDocumentationItem.setIcon(
            build_icon(u':/system/system_help_contents.png'))
        self.HelpDocumentationItem.setObjectName(u'HelpDocumentationItem')
        self.HelpDocumentationItem.setEnabled(False)
        self.HelpAboutItem = QtGui.QAction(MainWindow)
        self.HelpAboutItem.setIcon(
            build_icon(u':/system/system_about.png'))
        self.HelpAboutItem.setObjectName(u'HelpAboutItem')
        self.HelpOnlineHelpItem = QtGui.QAction(MainWindow)
        self.HelpOnlineHelpItem.setObjectName(u'HelpOnlineHelpItem')
        self.HelpOnlineHelpItem.setEnabled(False)
        self.HelpWebSiteItem = QtGui.QAction(MainWindow)
        self.HelpWebSiteItem.setObjectName(u'HelpWebSiteItem')
        #i18n Language Items
        self.AutoLanguageItem = QtGui.QAction(MainWindow)
        self.AutoLanguageItem.setObjectName(u'AutoLanguageItem')
        self.AutoLanguageItem.setCheckable(True)
        self.LanguageGroup = QtGui.QActionGroup(MainWindow)
        qmList = LanguageManager.get_qm_list()
        savedLanguage = LanguageManager.get_language()
        self.AutoLanguageItem.setChecked(LanguageManager.AutoLanguage)
        for key in sorted(qmList.keys()):
            languageItem = QtGui.QAction(MainWindow)
            languageItem.setObjectName(key)
            languageItem.setCheckable(True)
            if qmList[key] == savedLanguage:
                languageItem.setChecked(True)
            add_actions(self.LanguageGroup, [languageItem])
        self.LanguageGroup.setDisabled(LanguageManager.AutoLanguage)
        self.ToolsAddToolItem = QtGui.QAction(MainWindow)
        self.ToolsAddToolItem.setIcon(build_icon(u':/tools/tools_add.png'))
        self.ToolsAddToolItem.setObjectName(u'ToolsAddToolItem')
        self.ViewPreviewPanel = QtGui.QAction(MainWindow)
        self.ViewPreviewPanel.setCheckable(True)
        previewVisible = QtCore.QSettings().value(
            u'user interface/preview panel', QtCore.QVariant(True)).toBool()
        self.ViewPreviewPanel.setChecked(previewVisible)
        self.ViewPreviewPanel.setObjectName(u'ViewPreviewPanel')
        self.PreviewController.Panel.setVisible(previewVisible)
        self.ViewLivePanel = QtGui.QAction(MainWindow)
        self.ViewLivePanel.setCheckable(True)
        liveVisible = QtCore.QSettings().value(u'user interface/live panel',
            QtCore.QVariant(True)).toBool()
        self.ViewLivePanel.setChecked(liveVisible)
        self.ViewLivePanel.setObjectName(u'ViewLivePanel')
        self.LiveController.Panel.setVisible(liveVisible)
        self.ModeDefaultItem = QtGui.QAction(MainWindow)
        self.ModeDefaultItem.setCheckable(True)
        self.ModeDefaultItem.setObjectName(u'ModeDefaultItem')
        self.ModeSetupItem = QtGui.QAction(MainWindow)
        self.ModeSetupItem.setCheckable(True)
        self.ModeSetupItem.setObjectName(u'ModeLiveItem')
        self.ModeLiveItem = QtGui.QAction(MainWindow)
        self.ModeLiveItem.setCheckable(True)
        self.ModeLiveItem.setObjectName(u'ModeLiveItem')
        self.ModeGroup = QtGui.QActionGroup(MainWindow)
        self.ModeGroup.addAction(self.ModeDefaultItem)
        self.ModeGroup.addAction(self.ModeSetupItem)
        self.ModeGroup.addAction(self.ModeLiveItem)
        self.ModeDefaultItem.setChecked(True)
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
            self.SettingsConfigureItem))
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
        MainWindow.mainTitle = translate('MainWindow', 'OpenLP 2.0')
        MainWindow.language = translate('MainWindow', 'English')
        MainWindow.setWindowTitle(MainWindow.mainTitle)
        self.FileMenu.setTitle(translate('MainWindow', '&File'))
        self.FileImportMenu.setTitle(translate('MainWindow', '&Import'))
        self.FileExportMenu.setTitle(translate('MainWindow', '&Export'))
        self.ViewMenu.setTitle(translate('MainWindow', '&View'))
        self.ViewModeMenu.setTitle(translate('MainWindow', 'M&ode'))
        self.ToolsMenu.setTitle(translate('MainWindow', '&Tools'))
        self.SettingsMenu.setTitle(translate('MainWindow', '&Settings'))
        self.SettingsLanguageMenu.setTitle(translate('MainWindow',
            '&Language'))
        self.HelpMenu.setTitle(translate('MainWindow', '&Help'))
        self.MediaManagerDock.setWindowTitle(
            translate('MainWindow', 'Media Manager'))
        self.ServiceManagerDock.setWindowTitle(
            translate('MainWindow', 'Service Manager'))
        self.ThemeManagerDock.setWindowTitle(
            translate('MainWindow', 'Theme Manager'))
        self.FileNewItem.setText(translate('MainWindow', '&New'))
        self.FileNewItem.setToolTip(translate('MainWindow', 'New Service'))
        self.FileNewItem.setStatusTip(
            translate('MainWindow', 'Create a new service.'))
        self.FileNewItem.setShortcut(translate('MainWindow', 'Ctrl+N'))
        self.FileOpenItem.setText(translate('MainWindow', '&Open'))
        self.FileOpenItem.setToolTip(translate('MainWindow', 'Open Service'))
        self.FileOpenItem.setStatusTip(
            translate('MainWindow', 'Open an existing service.'))
        self.FileOpenItem.setShortcut(translate('MainWindow', 'Ctrl+O'))
        self.FileSaveItem.setText(translate('MainWindow', '&Save'))
        self.FileSaveItem.setToolTip(translate('MainWindow', 'Save Service'))
        self.FileSaveItem.setStatusTip(
            translate('MainWindow', 'Save the current service to disk.'))
        self.FileSaveItem.setShortcut(translate('MainWindow', 'Ctrl+S'))
        self.FileSaveAsItem.setText(translate('MainWindow', 'Save &As...'))
        self.FileSaveAsItem.setToolTip(
            translate('MainWindow', 'Save Service As'))
        self.FileSaveAsItem.setStatusTip(translate('MainWindow',
            'Save the current service under a new name.'))
        self.FileSaveAsItem.setShortcut(translate('MainWindow', 'Ctrl+Shift+S'))
        self.FileExitItem.setText(translate('MainWindow', 'E&xit'))
        self.FileExitItem.setStatusTip(translate('MainWindow', 'Quit OpenLP'))
        self.FileExitItem.setShortcut(translate('MainWindow', 'Alt+F4'))
        self.ImportThemeItem.setText(translate('MainWindow', '&Theme'))
        self.ImportLanguageItem.setText(translate('MainWindow', '&Language'))
        self.ExportThemeItem.setText(translate('MainWindow', '&Theme'))
        self.ExportLanguageItem.setText(translate('MainWindow', '&Language'))
        self.SettingsConfigureItem.setText(translate('MainWindow',
            '&Configure OpenLP...'))
        self.ViewMediaManagerItem.setText(
            translate('MainWindow', '&Media Manager'))
        self.ViewMediaManagerItem.setToolTip(
            translate('MainWindow', 'Toggle Media Manager'))
        self.ViewMediaManagerItem.setStatusTip(translate('MainWindow',
            'Toggle the visibility of the media manager.'))
        self.ViewMediaManagerItem.setShortcut(translate('MainWindow', 'F8'))
        self.ViewThemeManagerItem.setText(
            translate('MainWindow', '&Theme Manager'))
        self.ViewThemeManagerItem.setToolTip(
            translate('MainWindow', 'Toggle Theme Manager'))
        self.ViewThemeManagerItem.setStatusTip(translate('MainWindow',
            'Toggle the visibility of the theme manager.'))
        self.ViewThemeManagerItem.setShortcut(translate('MainWindow', 'F10'))
        self.ViewServiceManagerItem.setText(
            translate('MainWindow', '&Service Manager'))
        self.ViewServiceManagerItem.setToolTip(
            translate('MainWindow', 'Toggle Service Manager'))
        self.ViewServiceManagerItem.setStatusTip(translate('MainWindow',
            'Toggle the visibility of the service manager.'))
        self.ViewServiceManagerItem.setShortcut(translate('MainWindow', 'F9'))
        self.ViewPreviewPanel.setText(
            translate('MainWindow', '&Preview Panel'))
        self.ViewPreviewPanel.setToolTip(
            translate('MainWindow', 'Toggle Preview Panel'))
        self.ViewPreviewPanel.setStatusTip(translate('MainWindow',
            'Toggle the visibility of the preview panel.'))
        self.ViewPreviewPanel.setShortcut(translate('MainWindow', 'F11'))
        self.ViewLivePanel.setText(
            translate('MainWindow', '&Live Panel'))
        self.ViewLivePanel.setToolTip(
            translate('MainWindow', 'Toggle Live Panel'))
        self.ViewLivePanel.setStatusTip(translate('MainWindow',
            'Toggle the visibility of the live panel.'))
        self.ViewLivePanel.setShortcut(translate('MainWindow', 'F12'))
        self.SettingsPluginListItem.setText(translate('MainWindow',
            '&Plugin List'))
        self.SettingsPluginListItem.setStatusTip(
            translate('MainWindow', 'List the Plugins'))
        self.SettingsPluginListItem.setShortcut(
            translate('MainWindow', 'Alt+F7'))
        self.HelpDocumentationItem.setText(
            translate('MainWindow', '&User Guide'))
        self.HelpAboutItem.setText(translate('MainWindow', '&About'))
        self.HelpAboutItem.setStatusTip(
            translate('MainWindow', 'More information about OpenLP'))
        self.HelpAboutItem.setShortcut(translate('MainWindow', 'Ctrl+F1'))
        self.HelpOnlineHelpItem.setText(
            translate('MainWindow', '&Online Help'))
        self.HelpWebSiteItem.setText(translate('MainWindow', '&Web Site'))
        self.AutoLanguageItem.setText(translate('MainWindow', '&Auto Detect'))
        self.AutoLanguageItem.setStatusTip(
            translate('MainWindow', 'Use the system language, if available.'))
        for item in self.LanguageGroup.actions():
            item.setText(item.objectName())
            item.setStatusTip(unicode(translate('MainWindow',
                'Set the interface language to %s')) % item.objectName())
        self.ToolsAddToolItem.setText(translate('MainWindow', 'Add &Tool...'))
        self.ToolsAddToolItem.setStatusTip(
            translate('MainWindow',
                'Add an application to the list of tools.'))
        self.ModeDefaultItem.setText(translate('MainWindow', '&Default'))
        self.ModeDefaultItem.setStatusTip(
            translate('MainWindow',
                'Set the view mode back to the default.'))
        self.ModeSetupItem.setText(translate('MainWindow', '&Setup'))
        self.ModeSetupItem.setStatusTip(
            translate('MainWindow',
                'Set the view mode to Setup.'))
        self.ModeLiveItem.setText(translate('MainWindow', '&Live'))
        self.ModeLiveItem.setStatusTip(
            translate('MainWindow',
                'Set the view mode to Live.'))


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
        # Set up settings sections for the main application
        # (not for use by plugins)
        self.uiSettingsSection = u'user interface'
        self.generalSettingsSection = u'general'
        self.serviceSettingsSection = u'servicemanager'
        self.songsSettingsSection = u'songs'
        self.serviceNotSaved = False
        self.settingsmanager = SettingsManager(screens)
        self.displayManager = DisplayManager(screens)
        self.aboutForm = AboutForm(self, applicationVersion)
        self.settingsForm = SettingsForm(self.screens, self, self)
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
            QtCore.SIGNAL(u'triggered(bool)'),
            self.toggleMediaManager)
        QtCore.QObject.connect(self.ViewServiceManagerItem,
            QtCore.SIGNAL(u'triggered(bool)'),
            self.toggleServiceManager)
        QtCore.QObject.connect(self.ViewThemeManagerItem,
            QtCore.SIGNAL(u'triggered(bool)'),
            self.toggleThemeManager)
        QtCore.QObject.connect(self.ViewPreviewPanel,
            QtCore.SIGNAL(u'toggled(bool)'),
            self.setPreviewPanelVisibility)
        QtCore.QObject.connect(self.ViewLivePanel,
            QtCore.SIGNAL(u'toggled(bool)'),
            self.setLivePanelVisibility)
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
            QtCore.SIGNAL(u'triggered()'), self.onOptionsSettingsItemClicked)
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
        #i18n set signals for languages
        QtCore.QObject.connect(self.AutoLanguageItem,
                QtCore.SIGNAL(u'toggled(bool)'),
                self.setAutoLanguage)
        self.LanguageGroup.triggered.connect(LanguageManager.set_language)
        QtCore.QObject.connect(self.ModeDefaultItem,
            QtCore.SIGNAL(u'triggered()'),
            self.onModeDefaultItemClicked)
        QtCore.QObject.connect(self.ModeSetupItem,
            QtCore.SIGNAL(u'triggered()'),
            self.onModeSetupItemClicked)
        QtCore.QObject.connect(self.ModeLiveItem,
            QtCore.SIGNAL(u'triggered()'),
            self.onModeLiveItemClicked)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_global'), self.defaultThemeChanged)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_version_check'), self.versionCheck)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'maindisplay_blank_check'), self.blankCheck)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_screen_changed'), self.screenChanged)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'maindisplay_status_text'), self.showStatusMessage)
        #warning cyclic dependency
        #RenderManager needs to call ThemeManager and
        #ThemeManager needs to call RenderManager
        self.RenderManager = RenderManager(
            self.ThemeManagerContents, self.screens)
        self.displayManager.renderManager = self.RenderManager
        #Define the media Dock Manager
        self.mediaDockManager = MediaDockManager(self.MediaToolBox)
        log.info(u'Load Plugins')
        #make the controllers available to the plugins
        self.plugin_helpers[u'preview'] = self.PreviewController
        self.plugin_helpers[u'live'] = self.LiveController
        self.plugin_helpers[u'render'] = self.RenderManager
        self.plugin_helpers[u'service'] = self.ServiceManagerContents
        self.plugin_helpers[u'settings form'] = self.settingsForm
        self.plugin_helpers[u'toolbox'] = self.mediaDockManager
        self.plugin_helpers[u'displaymanager'] = self.displayManager
        self.plugin_helpers[u'pluginmanager'] = self.plugin_manager
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
        LanguageManager.AutoLanguage = value
        LanguageManager.set_language(self.LanguageGroup.checkedAction())

    def versionCheck(self, version):
        """
        Checks the version of the Application called from openlp.pyw
        Triggered by delay thread.
        """
        app_version = self.applicationVersion[u'full']
        version_text = unicode(translate('MainWindow', 'Version %s of OpenLP '
            'is now available for download (you are currently running version '
            ' %s). \n\nYou can download the latest version from '
            'http://openlp.org'))
        QtGui.QMessageBox.question(self,
            translate('MainWindow', 'OpenLP Version Updated'),
            version_text % (version, app_version),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok),
            QtGui.QMessageBox.Ok)

    def show(self):
        """
        Show the main form, as well as the display form
        """
        QtGui.QWidget.show(self)
        #screen_number = self.getMonitorNumber()
        self.displayManager.setup()
        if self.displayManager.mainDisplay.isVisible():
            self.displayManager.mainDisplay.setFocus()
        self.activateWindow()
        if QtCore.QSettings().value(
            self.generalSettingsSection + u'/auto open',
            QtCore.QVariant(False)).toBool():
            self.ServiceManagerContents.onLoadService(True)

    def blankCheck(self):
        """
        Check and display message if screen blank on setup.
        Triggered by delay thread.
        """
        settings = QtCore.QSettings()
        settings.beginGroup(self.generalSettingsSection)
        if settings.value(u'screen blank', QtCore.QVariant(False)).toBool():
            self.LiveController.mainDisplaySetBackground()
            if settings.value(u'blank warning',
                QtCore.QVariant(False)).toBool():
                QtGui.QMessageBox.question(self,
                    translate('MainWindow', 'OpenLP Main Display Blanked'),
                    translate('MainWindow',
                         'The Main Display has been blanked out'))
        settings.endGroup()

    def versionThread(self):
        """
        Start an initial setup thread to delay notifications
        """
        vT = VersionThread(self, self.applicationVersion)
        vT.start()

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

    def onOptionsSettingsItemClicked(self):
        """
        Show the Settings dialog
        """
        self.settingsForm.exec_()

    def onModeDefaultItemClicked(self):
        """
        Put OpenLP into "Default" view mode.
        """
        self.MediaManagerDock.setVisible(True)
        self.ServiceManagerDock.setVisible(True)
        self.ThemeManagerDock.setVisible(True)
        self.setPreviewPanelVisibility(True)
        self.setLivePanelVisibility(True)

    def onModeSetupItemClicked(self):
        """
        Put OpenLP into "Setup" view mode.
        """
        self.MediaManagerDock.setVisible(True)
        self.ServiceManagerDock.setVisible(True)
        self.ThemeManagerDock.setVisible(False)
        self.setPreviewPanelVisibility(True)
        self.setLivePanelVisibility(False)

    def onModeLiveItemClicked(self):
        """
        Put OpenLP into "Live" view mode.
        """
        self.MediaManagerDock.setVisible(False)
        self.ServiceManagerDock.setVisible(True)
        self.ThemeManagerDock.setVisible(False)
        self.setPreviewPanelVisibility(False)
        self.setLivePanelVisibility(True)

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
                translate('MainWindow', 'Save Changes to Service?'),
                translate('MainWindow', 'Your service has changed. '
                    'Do you want to save those changes?'),
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
        if QtCore.QSettings().value(u'advanced/save current plugin',
            QtCore.QVariant(False)).toBool():
            QtCore.QSettings().setValue(u'advanced/current media plugin',
                QtCore.QVariant(self.MediaToolBox.currentIndex()))
        # Call the cleanup method to shutdown plugins.
        log.info(u'cleanup plugins')
        self.plugin_manager.finalise_plugins()
        # Save settings
        self.saveSettings()
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
            unicode(translate('MainWindow', 'Default Theme: %s')) % theme)

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
