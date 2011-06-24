# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
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

import logging
import os
import sys
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
        self.mainContent = QtGui.QWidget(mainWindow)
        self.mainContent.setObjectName(u'mainContent')
        self.mainContentLayout = QtGui.QHBoxLayout(self.mainContent)
        self.mainContentLayout.setSpacing(0)
        self.mainContentLayout.setMargin(0)
        self.mainContentLayout.setObjectName(u'mainContentLayout')
        mainWindow.setCentralWidget(self.mainContent)
        self.controlSplitter = QtGui.QSplitter(self.mainContent)
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
        panelLocked = QtCore.QSettings().value(u'user interface/lock panel',
            QtCore.QVariant(False)).toBool()
        self.liveController.panel.setVisible(liveVisible)
        # Create menu
        self.menuBar = QtGui.QMenuBar(mainWindow)
        self.menuBar.setObjectName(u'menuBar')
        self.fileMenu = QtGui.QMenu(self.menuBar)
        self.fileMenu.setObjectName(u'fileMenu')
        self.fileImportMenu = QtGui.QMenu(self.fileMenu)
        self.fileImportMenu.setObjectName(u'fileImportMenu')
        self.fileExportMenu = QtGui.QMenu(self.fileMenu)
        self.fileExportMenu.setObjectName(u'fileExportMenu')
        # View Menu
        self.viewMenu = QtGui.QMenu(self.menuBar)
        self.viewMenu.setObjectName(u'viewMenu')
        self.viewModeMenu = QtGui.QMenu(self.viewMenu)
        self.viewModeMenu.setObjectName(u'viewModeMenu')
        # Tools Menu
        self.toolsMenu = QtGui.QMenu(self.menuBar)
        self.toolsMenu.setObjectName(u'toolsMenu')
        # Settings Menu
        self.settingsMenu = QtGui.QMenu(self.menuBar)
        self.settingsMenu.setObjectName(u'settingsMenu')
        self.settingsLanguageMenu = QtGui.QMenu(self.settingsMenu)
        self.settingsLanguageMenu.setObjectName(u'settingsLanguageMenu')
        # Help Menu
        self.helpMenu = QtGui.QMenu(self.menuBar)
        self.helpMenu.setObjectName(u'helpMenu')
        mainWindow.setMenuBar(self.menuBar)
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
        self.mediaToolBox = QtGui.QToolBox(self.mediaManagerDock)
        self.mediaToolBox.setObjectName(u'mediaToolBox')
        self.mediaManagerDock.setWidget(self.mediaToolBox)
        mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
            self.mediaManagerDock)
        # Create the service manager
        self.serviceManagerDock = OpenLPDockWidget(mainWindow,
            u'serviceManagerDock', u':/system/system_servicemanager.png')
        self.serviceManagerContents = ServiceManager(mainWindow,
            self.serviceManagerDock)
        self.serviceManagerDock.setWidget(self.serviceManagerContents)
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
        self.fileNewItem = shortcut_action(mainWindow, u'fileNewItem',
            [QtGui.QKeySequence(u'Ctrl+N')],
            self.serviceManagerContents.onNewServiceClicked,
            u':/general/general_new.png', category=UiStrings().File)
        self.fileOpenItem = shortcut_action(mainWindow, u'fileOpenItem',
            [QtGui.QKeySequence(u'Ctrl+O')],
            self.serviceManagerContents.onLoadServiceClicked,
            u':/general/general_open.png', category=UiStrings().File)
        self.fileSaveItem = shortcut_action(mainWindow, u'fileSaveItem',
            [QtGui.QKeySequence(u'Ctrl+S')],
            self.serviceManagerContents.saveFile,
            u':/general/general_save.png', category=UiStrings().File)
        self.fileSaveAsItem = shortcut_action(mainWindow, u'fileSaveAsItem',
            [QtGui.QKeySequence(u'Ctrl+Shift+S')],
            self.serviceManagerContents.saveFileAs, category=UiStrings().File)
        self.printServiceOrderItem = shortcut_action(mainWindow,
            u'printServiceItem', [QtGui.QKeySequence(u'Ctrl+P')],
            self.serviceManagerContents.printServiceOrder,
            category=UiStrings().File)
        self.fileExitItem = shortcut_action(mainWindow, u'fileExitItem',
            [QtGui.QKeySequence(u'Alt+F4')], mainWindow.close,
            u':/system/system_exit.png', category=UiStrings().File)
        action_list.add_category(UiStrings().Import, CategoryOrder.standardMenu)
        self.importThemeItem = base_action(
            mainWindow, u'importThemeItem', UiStrings().Import)
        self.importLanguageItem = base_action(
            mainWindow, u'importLanguageItem')#, UiStrings().Import)
        action_list.add_category(UiStrings().Export, CategoryOrder.standardMenu)
        self.exportThemeItem = base_action(
            mainWindow, u'exportThemeItem', UiStrings().Export)
        self.exportLanguageItem = base_action(
            mainWindow, u'exportLanguageItem')#, UiStrings().Export)
        action_list.add_category(UiStrings().View, CategoryOrder.standardMenu)
        self.viewMediaManagerItem = shortcut_action(mainWindow,
            u'viewMediaManagerItem', [QtGui.QKeySequence(u'F8')],
            self.toggleMediaManager, u':/system/system_mediamanager.png',
            self.mediaManagerDock.isVisible(), UiStrings().View)
        self.viewThemeManagerItem = shortcut_action(mainWindow,
            u'viewThemeManagerItem', [QtGui.QKeySequence(u'F10')],
            self.toggleThemeManager,  u':/system/system_thememanager.png',
            self.themeManagerDock.isVisible(), UiStrings().View)
        self.viewServiceManagerItem = shortcut_action(mainWindow,
            u'viewServiceManagerItem', [QtGui.QKeySequence(u'F9')],
            self.toggleServiceManager, u':/system/system_servicemanager.png',
            self.serviceManagerDock.isVisible(), UiStrings().View)
        self.viewPreviewPanel = shortcut_action(mainWindow,
            u'viewPreviewPanel', [QtGui.QKeySequence(u'F11')],
            self.setPreviewPanelVisibility, checked=previewVisible,
            category=UiStrings().View)
        self.viewLivePanel = shortcut_action(mainWindow, u'viewLivePanel',
            [QtGui.QKeySequence(u'F12')], self.setLivePanelVisibility,
            checked=liveVisible, category=UiStrings().View)
        self.lockPanel = shortcut_action(mainWindow, u'lockPanel',
            None, self.setLockPanel,
            checked=panelLocked, category=None)
        action_list.add_category(UiStrings().ViewMode,
            CategoryOrder.standardMenu)
        self.modeDefaultItem = checkable_action(
            mainWindow, u'modeDefaultItem', category=UiStrings().ViewMode)
        self.modeSetupItem = checkable_action(
            mainWindow, u'modeLiveItem', category=UiStrings().ViewMode)
        self.modeLiveItem = checkable_action(
            mainWindow, u'modeLiveItem', True, UiStrings().ViewMode)
        self.modeGroup = QtGui.QActionGroup(mainWindow)
        self.modeGroup.addAction(self.modeDefaultItem)
        self.modeGroup.addAction(self.modeSetupItem)
        self.modeGroup.addAction(self.modeLiveItem)
        self.modeDefaultItem.setChecked(True)
        action_list.add_category(UiStrings().Tools, CategoryOrder.standardMenu)
        self.toolsAddToolItem = icon_action(mainWindow, u'toolsAddToolItem',
            u':/tools/tools_add.png', category=UiStrings().Tools)
        self.toolsOpenDataFolder = icon_action(mainWindow,
            u'toolsOpenDataFolder', u':/general/general_open.png',
            category=UiStrings().Tools)
        self.updateThemeImages = base_action(mainWindow,
            u'updateThemeImages', category=UiStrings().Tools)
        action_list.add_category(UiStrings().Settings,
            CategoryOrder.standardMenu)
        self.settingsPluginListItem = shortcut_action(mainWindow,
            u'settingsPluginListItem', [QtGui.QKeySequence(u'Alt+F7')],
            self.onPluginItemClicked, u':/system/settings_plugin_list.png',
            category=UiStrings().Settings)
        # i18n Language Items
        self.autoLanguageItem = checkable_action(mainWindow,
            u'autoLanguageItem', LanguageManager.auto_language)
        self.languageGroup = QtGui.QActionGroup(mainWindow)
        self.languageGroup.setExclusive(True)
        self.languageGroup.setObjectName(u'languageGroup')
        add_actions(self.languageGroup, [self.autoLanguageItem])
        qmList = LanguageManager.get_qm_list()
        savedLanguage = LanguageManager.get_language()
        for key in sorted(qmList.keys()):
            languageItem = checkable_action(
                mainWindow, key, qmList[key] == savedLanguage)
            add_actions(self.languageGroup, [languageItem])
        self.settingsShortcutsItem = icon_action(mainWindow,
            u'settingsShortcutsItem',
            u':/system/system_configure_shortcuts.png',
            category=UiStrings().Settings)
        self.displayTagItem = icon_action(mainWindow,
            u'displayTagItem', u':/system/tag_editor.png',
            category=UiStrings().Settings)
        self.settingsConfigureItem = icon_action(mainWindow,
            u'settingsConfigureItem', u':/system/system_settings.png',
            category=UiStrings().Settings)
        action_list.add_category(UiStrings().Help, CategoryOrder.standardMenu)
        self.helpDocumentationItem = icon_action(mainWindow,
            u'helpDocumentationItem', u':/system/system_help_contents.png',
            category=None)#UiStrings().Help)
        self.helpDocumentationItem.setEnabled(False)
        self.helpAboutItem = shortcut_action(mainWindow, u'helpAboutItem',
            [QtGui.QKeySequence(u'Ctrl+F1')], self.onHelpAboutItemClicked,
            u':/system/system_about.png', category=UiStrings().Help)
        self.helpOnlineHelpItem = shortcut_action(
            mainWindow, u'helpOnlineHelpItem', [QtGui.QKeySequence(u'F1')],
            self.onHelpOnlineHelpClicked, u':/system/system_online_help.png',
            category=UiStrings().Help)
        self.helpWebSiteItem = base_action(
            mainWindow, u'helpWebSiteItem', category=UiStrings().Help)
        add_actions(self.fileImportMenu,
            (self.importThemeItem, self.importLanguageItem))
        add_actions(self.fileExportMenu,
            (self.exportThemeItem, self.exportLanguageItem))
        self.fileMenuActions = (self.fileNewItem, self.fileOpenItem,
            self.fileSaveItem, self.fileSaveAsItem, None,
            self.printServiceOrderItem, None, self.fileImportMenu.menuAction(),
            self.fileExportMenu.menuAction(), self.fileExitItem)
        add_actions(self.viewModeMenu, (self.modeDefaultItem,
            self.modeSetupItem, self.modeLiveItem))
        add_actions(self.viewMenu, (self.viewModeMenu.menuAction(),
            None, self.viewMediaManagerItem, self.viewServiceManagerItem,
            self.viewThemeManagerItem, None, self.viewPreviewPanel,
            self.viewLivePanel, None, self.lockPanel))
        # i18n add Language Actions
        add_actions(self.settingsLanguageMenu, (self.autoLanguageItem, None))
        add_actions(self.settingsLanguageMenu, self.languageGroup.actions())
        # Order things differently in OS X so that Preferences menu item in the
        # app menu is correct (this gets picked up automatically by Qt).
        if sys.platform == u'darwin':
            add_actions(self.settingsMenu, (self.settingsPluginListItem,
                self.settingsLanguageMenu.menuAction(), None,
                self.settingsConfigureItem, self.settingsShortcutsItem,
                self.displayTagItem))
        else:
            add_actions(self.settingsMenu, (self.settingsPluginListItem,
                self.settingsLanguageMenu.menuAction(), None,
                self.displayTagItem, self.settingsShortcutsItem,
                self.settingsConfigureItem))
        add_actions(self.toolsMenu, (self.toolsAddToolItem, None))
        add_actions(self.toolsMenu, (self.toolsOpenDataFolder, None))
        add_actions(self.toolsMenu, [self.updateThemeImages])
        add_actions(self.helpMenu, (self.helpDocumentationItem,
            self.helpOnlineHelpItem, None, self.helpWebSiteItem,
            self.helpAboutItem))
        add_actions(self.menuBar, (self.fileMenu.menuAction(),
            self.viewMenu.menuAction(), self.toolsMenu.menuAction(),
            self.settingsMenu.menuAction(), self.helpMenu.menuAction()))
        # Initialise the translation
        self.retranslateUi(mainWindow)
        self.mediaToolBox.setCurrentIndex(0)
        # Connect up some signals and slots
        QtCore.QObject.connect(self.fileMenu,
            QtCore.SIGNAL(u'aboutToShow()'), self.updateFileMenu)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)
        # Hide the entry, as it does not have any functionality yet.
        self.toolsAddToolItem.setVisible(False)
        self.importLanguageItem.setVisible(False)
        self.exportLanguageItem.setVisible(False)
        self.helpDocumentationItem.setVisible(False)
        self.setLockPanel(panelLocked)

    def retranslateUi(self, mainWindow):
        """
        Set up the translation system
        """
        mainWindow.mainTitle = UiStrings().OLPV2
        mainWindow.setWindowTitle(mainWindow.mainTitle)
        self.fileMenu.setTitle(translate('OpenLP.MainWindow', '&File'))
        self.fileImportMenu.setTitle(translate('OpenLP.MainWindow', '&Import'))
        self.fileExportMenu.setTitle(translate('OpenLP.MainWindow', '&Export'))
        self.viewMenu.setTitle(translate('OpenLP.MainWindow', '&View'))
        self.viewModeMenu.setTitle(translate('OpenLP.MainWindow', 'M&ode'))
        self.toolsMenu.setTitle(translate('OpenLP.MainWindow', '&Tools'))
        self.settingsMenu.setTitle(translate('OpenLP.MainWindow', '&Settings'))
        self.settingsLanguageMenu.setTitle(translate('OpenLP.MainWindow',
            '&Language'))
        self.helpMenu.setTitle(translate('OpenLP.MainWindow', '&Help'))
        self.mediaManagerDock.setWindowTitle(
            translate('OpenLP.MainWindow', 'Media Manager'))
        self.serviceManagerDock.setWindowTitle(
            translate('OpenLP.MainWindow', 'Service Manager'))
        self.themeManagerDock.setWindowTitle(
            translate('OpenLP.MainWindow', 'Theme Manager'))
        self.fileNewItem.setText(translate('OpenLP.MainWindow', '&New'))
        self.fileNewItem.setToolTip(UiStrings().NewService)
        self.fileNewItem.setStatusTip(UiStrings().CreateService)
        self.fileOpenItem.setText(translate('OpenLP.MainWindow', '&Open'))
        self.fileOpenItem.setToolTip(UiStrings().OpenService)
        self.fileOpenItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Open an existing service.'))
        self.fileSaveItem.setText(translate('OpenLP.MainWindow', '&Save'))
        self.fileSaveItem.setToolTip(UiStrings().SaveService)
        self.fileSaveItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Save the current service to disk.'))
        self.fileSaveAsItem.setText(
            translate('OpenLP.MainWindow', 'Save &As...'))
        self.fileSaveAsItem.setToolTip(
            translate('OpenLP.MainWindow', 'Save Service As'))
        self.fileSaveAsItem.setStatusTip(translate('OpenLP.MainWindow',
            'Save the current service under a new name.'))
        self.printServiceOrderItem.setText(UiStrings().PrintService)
        self.printServiceOrderItem.setStatusTip(translate('OpenLP.MainWindow',
            'Print the current service.'))
        self.fileExitItem.setText(
            translate('OpenLP.MainWindow', 'E&xit'))
        self.fileExitItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Quit OpenLP'))
        self.importThemeItem.setText(
            translate('OpenLP.MainWindow', '&Theme'))
        self.importLanguageItem.setText(
            translate('OpenLP.MainWindow', '&Language'))
        self.exportThemeItem.setText(
            translate('OpenLP.MainWindow', '&Theme'))
        self.exportLanguageItem.setText(
            translate('OpenLP.MainWindow', '&Language'))
        self.settingsShortcutsItem.setText(
            translate('OpenLP.MainWindow', 'Configure &Shortcuts...'))
        self.displayTagItem.setText(
            translate('OpenLP.MainWindow', '&Configure Display Tags'))
        self.settingsConfigureItem.setText(
            translate('OpenLP.MainWindow', '&Configure OpenLP...'))
        self.viewMediaManagerItem.setText(
            translate('OpenLP.MainWindow', '&Media Manager'))
        self.viewMediaManagerItem.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Media Manager'))
        self.viewMediaManagerItem.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the media manager.'))
        self.viewThemeManagerItem.setText(
            translate('OpenLP.MainWindow', '&Theme Manager'))
        self.viewThemeManagerItem.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Theme Manager'))
        self.viewThemeManagerItem.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the theme manager.'))
        self.viewServiceManagerItem.setText(
            translate('OpenLP.MainWindow', '&Service Manager'))
        self.viewServiceManagerItem.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Service Manager'))
        self.viewServiceManagerItem.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the service manager.'))
        self.viewPreviewPanel.setText(
            translate('OpenLP.MainWindow', '&Preview Panel'))
        self.viewPreviewPanel.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Preview Panel'))
        self.viewPreviewPanel.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the preview panel.'))
        self.viewLivePanel.setText(
            translate('OpenLP.MainWindow', '&Live Panel'))
        self.viewLivePanel.setToolTip(
            translate('OpenLP.MainWindow', 'Toggle Live Panel'))
        self.lockPanel.setText(
            translate('OpenLP.MainWindow', 'L&ock Panels'))
        self.lockPanel.setToolTip(
            translate('OpenLP.MainWindow', 'Prevent Panels changing'))
        self.viewLivePanel.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the live panel.'))
        self.settingsPluginListItem.setText(translate('OpenLP.MainWindow',
            '&Plugin List'))
        self.settingsPluginListItem.setStatusTip(
            translate('OpenLP.MainWindow', 'List the Plugins'))
        self.helpDocumentationItem.setText(
            translate('OpenLP.MainWindow', '&User Guide'))
        self.helpAboutItem.setText(translate('OpenLP.MainWindow', '&About'))
        self.helpAboutItem.setStatusTip(
            translate('OpenLP.MainWindow', 'More information about OpenLP'))
        self.helpOnlineHelpItem.setText(
            translate('OpenLP.MainWindow', '&Online Help'))
        self.helpWebSiteItem.setText(
            translate('OpenLP.MainWindow', '&Web Site'))
        for item in self.languageGroup.actions():
            item.setText(item.objectName())
            item.setStatusTip(unicode(translate('OpenLP.MainWindow',
                'Set the interface language to %s')) % item.objectName())
        self.autoLanguageItem.setText(
            translate('OpenLP.MainWindow', '&Autodetect'))
        self.autoLanguageItem.setStatusTip(translate('OpenLP.MainWindow',
            'Use the system language, if available.'))
        self.toolsAddToolItem.setText(
            translate('OpenLP.MainWindow', 'Add &Tool...'))
        self.toolsAddToolItem.setStatusTip(translate('OpenLP.MainWindow',
            'Add an application to the list of tools.'))
        self.toolsOpenDataFolder.setText(
            translate('OpenLP.MainWindow', 'Open &Data Folder...'))
        self.toolsOpenDataFolder.setStatusTip(translate('OpenLP.MainWindow',
            'Open the folder where songs, bibles and other data resides.'))
        self.updateThemeImages.setText(
            translate('OpenLP.MainWindow', 'Update Theme Images'))
        self.updateThemeImages.setStatusTip(
            translate('OpenLP.MainWindow', 'Update the preview images for all '
                'themes.'))
        self.modeDefaultItem.setText(
            translate('OpenLP.MainWindow', '&Default'))
        self.modeDefaultItem.setStatusTip(translate('OpenLP.MainWindow',
            'Set the view mode back to the default.'))
        self.modeSetupItem.setText(translate('OpenLP.MainWindow', '&Setup'))
        self.modeSetupItem.setStatusTip(
            translate('OpenLP.MainWindow', 'Set the view mode to Setup.'))
        self.modeLiveItem.setText(translate('OpenLP.MainWindow', '&Live'))
        self.modeLiveItem.setStatusTip(
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
        self.imageManager = ImageManager()
        # Set up the interface
        self.setupUi(self)
        # Load settings after setupUi so default UI sizes are overwritten
        self.loadSettings()
        # Once settings are loaded update FileMenu with recentFiles
        self.updateFileMenu()
        self.pluginForm = PluginForm(self)
        # Set up signals and slots
        QtCore.QObject.connect(self.importThemeItem,
            QtCore.SIGNAL(u'triggered()'),
            self.themeManagerContents.onImportTheme)
        QtCore.QObject.connect(self.exportThemeItem,
            QtCore.SIGNAL(u'triggered()'),
            self.themeManagerContents.onExportTheme)
        QtCore.QObject.connect(self.mediaManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.viewMediaManagerItem.setChecked)
        QtCore.QObject.connect(self.serviceManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.viewServiceManagerItem.setChecked)
        QtCore.QObject.connect(self.themeManagerDock,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.viewThemeManagerItem.setChecked)
        QtCore.QObject.connect(self.helpWebSiteItem,
            QtCore.SIGNAL(u'triggered()'), self.onHelpWebSiteClicked)
        QtCore.QObject.connect(self.toolsOpenDataFolder,
            QtCore.SIGNAL(u'triggered()'), self.onToolsOpenDataFolderClicked)
        QtCore.QObject.connect(self.updateThemeImages,
            QtCore.SIGNAL(u'triggered()'), self.onUpdateThemeImages)
        QtCore.QObject.connect(self.displayTagItem,
            QtCore.SIGNAL(u'triggered()'), self.onDisplayTagItemClicked)
        QtCore.QObject.connect(self.settingsConfigureItem,
            QtCore.SIGNAL(u'triggered()'), self.onSettingsConfigureItemClicked)
        QtCore.QObject.connect(self.settingsShortcutsItem,
            QtCore.SIGNAL(u'triggered()'), self.onSettingsShortcutsItemClicked)
        # i18n set signals for languages
        self.languageGroup.triggered.connect(LanguageManager.set_language)
        QtCore.QObject.connect(self.modeDefaultItem,
            QtCore.SIGNAL(u'triggered()'), self.onModeDefaultItemClicked)
        QtCore.QObject.connect(self.modeSetupItem,
            QtCore.SIGNAL(u'triggered()'), self.onModeSetupItemClicked)
        QtCore.QObject.connect(self.modeLiveItem,
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
        # Media Manager
        QtCore.QObject.connect(self.mediaToolBox,
            QtCore.SIGNAL(u'currentChanged(int)'), self.onMediaToolBoxChanged)
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
        self.renderer = Renderer(self.imageManager, self.themeManagerContents)
        # Define the media Dock Manager
        self.mediaDockManager = MediaDockManager(self.mediaToolBox)
        log.info(u'Load Plugins')
        # make the controllers available to the plugins
        self.pluginHelpers[u'preview'] = self.previewController
        self.pluginHelpers[u'live'] = self.liveController
        self.pluginHelpers[u'renderer'] = self.renderer
        self.pluginHelpers[u'service'] = self.serviceManagerContents
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
        self.pluginManager.hook_import_menu(self.fileImportMenu)
        # Call the hook method to pull in export menus.
        self.pluginManager.hook_export_menu(self.fileExportMenu)
        # Call the hook method to pull in tools menus.
        self.pluginManager.hook_tools_menu(self.toolsMenu)
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
                self.mediaToolBox.setCurrentIndex(savedPlugin)
        self.settingsForm.postSetUp()
        # Once all components are initialised load the Themes
        log.info(u'Load Themes')
        self.themeManagerContents.loadThemes(True)
        # Hide/show the theme combobox on the service manager
        self.serviceManagerContents.themeChange()
        # Reset the cursor
        Receiver.send_message(u'cursor_normal')

    def setAutoLanguage(self, value):
        self.languageGroup.setDisabled(value)
        LanguageManager.auto_language = value
        LanguageManager.set_language(self.languageGroup.checkedAction())

    def onMediaToolBoxChanged(self, index):
        widget = self.mediaToolBox.widget(index)
        if widget:
            widget.onFocus()

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
        if len(self.arguments):
            args = []
            for a in self.arguments:
                args.extend([a])
            self.serviceManagerContents.loadFile(unicode(args[0]))
        elif QtCore.QSettings().value(
            self.generalSettingsSection + u'/auto open',
            QtCore.QVariant(False)).toBool():
            self.serviceManagerContents.loadLastFile()
        view_mode = QtCore.QSettings().value(u'%s/view mode' % \
            self.generalSettingsSection, u'default').toString()
        if view_mode == u'default':
            self.modeDefaultItem.setChecked(True)
        elif view_mode == u'setup':
            self.setViewMode(True, True, False, True, False)
            self.modeSetupItem.setChecked(True)
        elif view_mode == u'live':
            self.setViewMode(False, True, False, False, True)
            self.modeLiveItem.setChecked(True)

    def appStartup(self):
        """
        Give all the plugins a chance to perform some tasks at startup
        """
        Receiver.send_message(u'openlp_process_events')
        for plugin in self.pluginManager.plugins:
            if plugin.isActive():
                plugin.appStartup()
                Receiver.send_message(u'openlp_process_events')

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
        """
        settings = QtCore.QSettings()
        self.liveController.mainDisplaySetBackground()
        if settings.value(u'%s/screen blank' % self.generalSettingsSection,
            QtCore.QVariant(False)).toBool():
            if settings.value(u'%s/blank warning' % self.generalSettingsSection,
                QtCore.QVariant(False)).toBool():
                QtGui.QMessageBox.question(self,
                    translate('OpenLP.MainWindow',
                        'OpenLP Main Display Blanked'),
                    translate('OpenLP.MainWindow',
                         'The Main Display has been blanked out'))

    def onErrorMessage(self, data):
        Receiver.send_message(u'close_splash')
        QtGui.QMessageBox.critical(self, data[u'title'], data[u'message'])

    def onWarningMessage(self, data):
        Receiver.send_message(u'close_splash')
        QtGui.QMessageBox.warning(self, data[u'title'], data[u'message'])

    def onInformationMessage(self, data):
        Receiver.send_message(u'close_splash')
        QtGui.QMessageBox.information(self, data[u'title'], data[u'message'])

    def onHelpWebSiteClicked(self):
        """
        Load the OpenLP website
        """
        import webbrowser
        webbrowser.open_new(u'http://openlp.org/')

    def onHelpOnlineHelpClicked(self):
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

    def onUpdateThemeImages(self):
        """
        Updates the new theme preview images.
        """
        self.themeManagerContents.updatePreviewImages()

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
        The screen has changed so we have to update components such as the
        renderer.
        """
        log.debug(u'screenChanged')
        Receiver.send_message(u'cursor_busy')
        self.imageManager.update_display()
        self.renderer.update_display()
        self.previewController.screenSizeChanged()
        self.liveController.screenSizeChanged()
        self.setFocus()
        self.activateWindow()
        Receiver.send_message(u'cursor_normal')

    def closeEvent(self, event):
        """
        Hook to close the main window and display windows on exit
        """
        if self.serviceManagerContents.isModified():
            ret = self.serviceManagerContents.saveModifiedService()
            if ret == QtGui.QMessageBox.Save:
                if self.serviceManagerContents.saveFile():
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
        self.serviceManagerContents.cleanUp()
        if QtCore.QSettings().value(u'advanced/save current plugin',
            QtCore.QVariant(False)).toBool():
            QtCore.QSettings().setValue(u'advanced/current media plugin',
                QtCore.QVariant(self.mediaToolBox.currentIndex()))
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
        self.serviceManagerDock.setVisible(
            not self.serviceManagerDock.isVisible())

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
        self.viewPreviewPanel.setChecked(visible)

    def setLockPanel(self, lock):
        """
        Sets the ability to stiop the toolbars being changed.
        """
        if lock:
            self.themeManagerDock.setFeatures(
                QtGui.QDockWidget.NoDockWidgetFeatures)
            self.serviceManagerDock.setFeatures(
                QtGui.QDockWidget.NoDockWidgetFeatures)
            self.mediaManagerDock.setFeatures(
                QtGui.QDockWidget.NoDockWidgetFeatures)
            self.viewMediaManagerItem.setEnabled(False)
            self.viewServiceManagerItem.setEnabled(False)
            self.viewThemeManagerItem.setEnabled(False)
            self.viewPreviewPanel.setEnabled(False)
            self.viewLivePanel.setEnabled(False)
        else:
            self.themeManagerDock.setFeatures(
                QtGui.QDockWidget.AllDockWidgetFeatures)
            self.serviceManagerDock.setFeatures(
                QtGui.QDockWidget.AllDockWidgetFeatures)
            self.mediaManagerDock.setFeatures(
                QtGui.QDockWidget.AllDockWidgetFeatures)
            self.viewMediaManagerItem.setEnabled(True)
            self.viewServiceManagerItem.setEnabled(True)
            self.viewThemeManagerItem.setEnabled(True)
            self.viewPreviewPanel.setEnabled(True)
            self.viewLivePanel.setEnabled(True)
        QtCore.QSettings().setValue(u'user interface/lock panel',
            QtCore.QVariant(lock))

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
        self.viewLivePanel.setChecked(visible)

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
        self.fileMenu.clear()
        add_actions(self.fileMenu, self.fileMenuActions[:-1])
        existingRecentFiles = [recentFile for recentFile in self.recentFiles
            if QtCore.QFile.exists(recentFile)]
        recentFilesToDisplay = existingRecentFiles[0:recentFileCount]
        if recentFilesToDisplay:
            self.fileMenu.addSeparator()
            for fileId, filename in enumerate(recentFilesToDisplay):
                log.debug('Recent file name: %s', filename)
                action =  base_action(self, u'')
                action.setText(u'&%d %s' %
                    (fileId + 1, QtCore.QFileInfo(filename).fileName()))
                action.setData(QtCore.QVariant(filename))
                self.connect(action, QtCore.SIGNAL(u'triggered()'),
                    self.serviceManagerContents.onRecentServiceClicked)
                self.fileMenu.addAction(action)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileMenuActions[-1])

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
