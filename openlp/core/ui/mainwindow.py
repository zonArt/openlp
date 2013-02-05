# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
This is the main window, where all the action happens.
"""
import logging
import os
import sys
import shutil
from distutils import dir_util
from distutils.errors import DistutilsFileError
from tempfile import gettempdir
import time
from datetime import datetime

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Renderer, OpenLPDockWidget, PluginManager, Receiver, ImageManager, PluginStatus, Registry, \
    Settings, ScreenList, build_icon, check_directory_exists, translate
from openlp.core.lib.ui import UiStrings, create_action
from openlp.core.ui import AboutForm, SettingsForm, ServiceManager, ThemeManager, SlideController, PluginForm, \
    MediaDockManager, ShortcutListForm, FormattingTagForm
from openlp.core.ui.media import MediaController
from openlp.core.utils import AppLocation, LanguageManager, add_actions, get_application_version, \
    get_filesystem_encoding
from openlp.core.utils.actions import ActionList, CategoryOrder
from openlp.core.ui.firsttimeform import FirstTimeForm

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

PROGRESSBAR_STYLE = """
    QProgressBar{
       height: 10px;
    }
"""


class Ui_MainWindow(object):
    """
    This is the UI part of the main window.
    """
    def setupUi(self, main_window):
        """
        Set up the user interface
        """
        main_window.setObjectName(u'MainWindow')
        main_window.setWindowIcon(build_icon(u':/icon/openlp-logo-64x64.png'))
        main_window.setDockNestingEnabled(True)
        # Set up the main container, which contains all the other form widgets.
        self.mainContent = QtGui.QWidget(main_window)
        self.mainContent.setObjectName(u'mainContent')
        self.mainContentLayout = QtGui.QHBoxLayout(self.mainContent)
        self.mainContentLayout.setSpacing(0)
        self.mainContentLayout.setMargin(0)
        self.mainContentLayout.setObjectName(u'mainContentLayout')
        main_window.setCentralWidget(self.mainContent)
        self.controlSplitter = QtGui.QSplitter(self.mainContent)
        self.controlSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.controlSplitter.setObjectName(u'controlSplitter')
        self.mainContentLayout.addWidget(self.controlSplitter)
        # Create slide controllers
        self.previewController = SlideController(self)
        self.liveController = SlideController(self, True)
        previewVisible = Settings().value(u'user interface/preview panel')
        self.previewController.panel.setVisible(previewVisible)
        liveVisible = Settings().value(u'user interface/live panel')
        panelLocked = Settings().value(u'user interface/lock panel')
        self.liveController.panel.setVisible(liveVisible)
        # Create menu
        self.menuBar = QtGui.QMenuBar(main_window)
        self.menuBar.setObjectName(u'menuBar')
        self.fileMenu = QtGui.QMenu(self.menuBar)
        self.fileMenu.setObjectName(u'fileMenu')
        self.recentFilesMenu = QtGui.QMenu(self.fileMenu)
        self.recentFilesMenu.setObjectName(u'recentFilesMenu')
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
        main_window.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(main_window)
        self.statusBar.setObjectName(u'statusBar')
        main_window.setStatusBar(self.statusBar)
        self.loadProgressBar = QtGui.QProgressBar(self.statusBar)
        self.loadProgressBar.setObjectName(u'loadProgressBar')
        self.statusBar.addPermanentWidget(self.loadProgressBar)
        self.loadProgressBar.hide()
        self.loadProgressBar.setValue(0)
        self.loadProgressBar.setStyleSheet(PROGRESSBAR_STYLE)
        self.defaultThemeLabel = QtGui.QLabel(self.statusBar)
        self.defaultThemeLabel.setObjectName(u'defaultThemeLabel')
        self.statusBar.addPermanentWidget(self.defaultThemeLabel)
        # Create the MediaManager
        self.mediaManagerDock = OpenLPDockWidget(main_window, u'mediaManagerDock', u':/system/system_mediamanager.png')
        self.mediaManagerDock.setStyleSheet(MEDIA_MANAGER_STYLE)
        # Create the media toolbox
        self.mediaToolBox = QtGui.QToolBox(self.mediaManagerDock)
        self.mediaToolBox.setObjectName(u'mediaToolBox')
        self.mediaManagerDock.setWidget(self.mediaToolBox)
        main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.mediaManagerDock)
        # Create the service manager
        self.serviceManagerDock = OpenLPDockWidget(main_window, u'serviceManagerDock',
            u':/system/system_servicemanager.png')
        self.serviceManagerContents = ServiceManager(self.serviceManagerDock)
        self.serviceManagerDock.setWidget(self.serviceManagerContents)
        main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.serviceManagerDock)
        # Create the theme manager
        self.themeManagerDock = OpenLPDockWidget(main_window, u'themeManagerDock', u':/system/system_thememanager.png')
        self.themeManagerContents = ThemeManager(self.themeManagerDock)
        self.themeManagerContents.setObjectName(u'themeManagerContents')
        self.themeManagerDock.setWidget(self.themeManagerContents)
        main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.themeManagerDock)
        # Create the menu items
        action_list = ActionList.get_instance()
        action_list.add_category(UiStrings().File, CategoryOrder.standardMenu)
        self.fileNewItem = create_action(main_window, u'fileNewItem',
            icon=u':/general/general_new.png',
            shortcuts=[QtGui.QKeySequence(u'Ctrl+N')],
            category=UiStrings().File,
            triggers=self.serviceManagerContents.on_new_service_clicked)
        self.fileOpenItem = create_action(main_window, u'fileOpenItem',
            icon=u':/general/general_open.png',
            shortcuts=[QtGui.QKeySequence(u'Ctrl+O')],
            category=UiStrings().File,
            triggers=self.serviceManagerContents.on_load_service_clicked)
        self.fileSaveItem = create_action(main_window, u'fileSaveItem',
            icon=u':/general/general_save.png',
            shortcuts=[QtGui.QKeySequence(u'Ctrl+S')],
            category=UiStrings().File,
            triggers=self.serviceManagerContents.save_file)
        self.fileSaveAsItem = create_action(main_window, u'fileSaveAsItem',
            shortcuts=[QtGui.QKeySequence(u'Ctrl+Shift+S')],
            category=UiStrings().File,
            triggers=self.serviceManagerContents.save_file_as)
        self.printServiceOrderItem = create_action(main_window,
            u'printServiceItem', shortcuts=[QtGui.QKeySequence(u'Ctrl+P')],
            category=UiStrings().File,
            triggers=self.serviceManagerContents.print_service_order)
        self.fileExitItem = create_action(main_window, u'fileExitItem',
            icon=u':/system/system_exit.png',
            shortcuts=[QtGui.QKeySequence(u'Alt+F4')],
            category=UiStrings().File, triggers=main_window.close)
        # Give QT Extra Hint that this is the Exit Menu Item
        self.fileExitItem.setMenuRole(QtGui.QAction.QuitRole)
        action_list.add_category(UiStrings().Import, CategoryOrder.standardMenu)
        self.importThemeItem = create_action(main_window, u'importThemeItem', category=UiStrings().Import)
        self.importLanguageItem = create_action(main_window, u'importLanguageItem')
        action_list.add_category(UiStrings().Export, CategoryOrder.standardMenu)
        self.exportThemeItem = create_action(main_window, u'exportThemeItem', category=UiStrings().Export)
        self.exportLanguageItem = create_action(main_window, u'exportLanguageItem')
        action_list.add_category(UiStrings().View, CategoryOrder.standardMenu)
        self.viewMediaManagerItem = create_action(main_window,
            u'viewMediaManagerItem', shortcuts=[QtGui.QKeySequence(u'F8')],
            icon=u':/system/system_mediamanager.png',
            checked=self.mediaManagerDock.isVisible(),
            category=UiStrings().View, triggers=self.toggleMediaManager)
        self.viewThemeManagerItem = create_action(main_window,
            u'viewThemeManagerItem', shortcuts=[QtGui.QKeySequence(u'F10')],
            icon=u':/system/system_thememanager.png',
            checked=self.themeManagerDock.isVisible(),
            category=UiStrings().View, triggers=self.toggleThemeManager)
        self.viewServiceManagerItem = create_action(main_window,
            u'viewServiceManagerItem', shortcuts=[QtGui.QKeySequence(u'F9')],
            icon=u':/system/system_servicemanager.png',
            checked=self.serviceManagerDock.isVisible(),
            category=UiStrings().View, triggers=self.toggleServiceManager)
        self.viewPreviewPanel = create_action(main_window, u'viewPreviewPanel',
            shortcuts=[QtGui.QKeySequence(u'F11')], checked=previewVisible,
            category=UiStrings().View, triggers=self.setPreviewPanelVisibility)
        self.viewLivePanel = create_action(main_window, u'viewLivePanel',
            shortcuts=[QtGui.QKeySequence(u'F12')], checked=liveVisible,
            category=UiStrings().View, triggers=self.setLivePanelVisibility)
        self.lockPanel = create_action(main_window, u'lockPanel',
            checked=panelLocked, triggers=self.setLockPanel)
        action_list.add_category(UiStrings().ViewMode,
            CategoryOrder.standardMenu)
        self.modeDefaultItem = create_action(main_window, u'modeDefaultItem', checked=False,
            category=UiStrings().ViewMode)
        self.modeSetupItem = create_action(main_window, u'modeSetupItem', checked=False, category=UiStrings().ViewMode)
        self.modeLiveItem = create_action(main_window, u'modeLiveItem', checked=True, category=UiStrings().ViewMode)
        self.modeGroup = QtGui.QActionGroup(main_window)
        self.modeGroup.addAction(self.modeDefaultItem)
        self.modeGroup.addAction(self.modeSetupItem)
        self.modeGroup.addAction(self.modeLiveItem)
        self.modeDefaultItem.setChecked(True)
        action_list.add_category(UiStrings().Tools, CategoryOrder.standardMenu)
        self.toolsAddToolItem = create_action(main_window,
            u'toolsAddToolItem', icon=u':/tools/tools_add.png',
            category=UiStrings().Tools)
        self.toolsOpenDataFolder = create_action(main_window,
            u'toolsOpenDataFolder', icon=u':/general/general_open.png',
            category=UiStrings().Tools)
        self.toolsFirstTimeWizard = create_action(main_window,
            u'toolsFirstTimeWizard', icon=u':/general/general_revert.png',
            category=UiStrings().Tools)
        self.updateThemeImages = create_action(main_window,
            u'updateThemeImages', category=UiStrings().Tools)
        action_list.add_category(UiStrings().Settings,
            CategoryOrder.standardMenu)
        self.settingsPluginListItem = create_action(main_window,
            u'settingsPluginListItem',
            icon=u':/system/settings_plugin_list.png',
            shortcuts=[QtGui.QKeySequence(u'Alt+F7')],
            category=UiStrings().Settings, triggers=self.onPluginItemClicked)
        # i18n Language Items
        self.autoLanguageItem = create_action(main_window, u'autoLanguageItem',
            checked=LanguageManager.auto_language)
        self.languageGroup = QtGui.QActionGroup(main_window)
        self.languageGroup.setExclusive(True)
        self.languageGroup.setObjectName(u'languageGroup')
        add_actions(self.languageGroup, [self.autoLanguageItem])
        qmList = LanguageManager.get_qm_list()
        savedLanguage = LanguageManager.get_language()
        for key in sorted(qmList.keys()):
            languageItem = create_action(main_window, key, checked=qmList[key] == savedLanguage)
            add_actions(self.languageGroup, [languageItem])
        self.settingsShortcutsItem = create_action(main_window, u'settingsShortcutsItem',
            icon=u':/system/system_configure_shortcuts.png', category=UiStrings().Settings)
        # Formatting Tags were also known as display tags.
        self.formattingTagItem = create_action(main_window, u'displayTagItem',
            icon=u':/system/tag_editor.png', category=UiStrings().Settings)
        self.settingsConfigureItem = create_action(main_window, u'settingsConfigureItem',
            icon=u':/system/system_settings.png', category=UiStrings().Settings)
        # Give QT Extra Hint that this is the Preferences Menu Item
        self.settingsConfigureItem.setMenuRole(QtGui.QAction.PreferencesRole)
        self.settingsImportItem = create_action(main_window, u'settingsImportItem', category=UiStrings().Settings)
        self.settingsExportItem = create_action(main_window, u'settingsExportItem', category=UiStrings().Settings)
        action_list.add_category(UiStrings().Help, CategoryOrder.standardMenu)
        self.aboutItem = create_action(main_window, u'aboutItem', icon=u':/system/system_about.png',
            shortcuts=[QtGui.QKeySequence(u'Ctrl+F1')],
            category=UiStrings().Help, triggers=self.onAboutItemClicked)
        # Give QT Extra Hint that this is an About Menu Item
        self.aboutItem.setMenuRole(QtGui.QAction.AboutRole)
        if os.name == u'nt':
            self.localHelpFile = os.path.join(
                AppLocation.get_directory(AppLocation.AppDir), 'OpenLP.chm')
            self.offlineHelpItem = create_action(main_window, u'offlineHelpItem',
                icon=u':/system/system_help_contents.png',
                shortcuts=[QtGui.QKeySequence(u'F1')],
                category=UiStrings().Help, triggers=self.onOfflineHelpClicked)
        self.onlineHelpItem = create_action(main_window, u'onlineHelpItem',
            icon=u':/system/system_online_help.png',
            shortcuts=[QtGui.QKeySequence(u'Alt+F1')],
            category=UiStrings().Help, triggers=self.onOnlineHelpClicked)
        self.webSiteItem = create_action(main_window, u'webSiteItem', category=UiStrings().Help)
        add_actions(self.fileImportMenu, (self.settingsImportItem, None, self.importThemeItem, self.importLanguageItem))
        add_actions(self.fileExportMenu, (self.settingsExportItem, None, self.exportThemeItem, self.exportLanguageItem))
        add_actions(self.fileMenu, (self.fileNewItem, self.fileOpenItem,
            self.fileSaveItem, self.fileSaveAsItem, self.recentFilesMenu.menuAction(), None,
            self.fileImportMenu.menuAction(), self.fileExportMenu.menuAction(), None, self.printServiceOrderItem,
            self.fileExitItem))
        add_actions(self.viewModeMenu, (self.modeDefaultItem, self.modeSetupItem, self.modeLiveItem))
        add_actions(self.viewMenu, (self.viewModeMenu.menuAction(), None, self.viewMediaManagerItem,
            self.viewServiceManagerItem, self.viewThemeManagerItem, None, self.viewPreviewPanel,
            self.viewLivePanel, None, self.lockPanel))
        # i18n add Language Actions
        add_actions(self.settingsLanguageMenu, (self.autoLanguageItem, None))
        add_actions(self.settingsLanguageMenu, self.languageGroup.actions())
        # Order things differently in OS X so that Preferences menu item in the
        # app menu is correct (this gets picked up automatically by Qt).
        if sys.platform == u'darwin':
            add_actions(self.settingsMenu, (self.settingsPluginListItem, self.settingsLanguageMenu.menuAction(), None,
                self.settingsConfigureItem, self.settingsShortcutsItem, self.formattingTagItem))
        else:
            add_actions(self.settingsMenu, (self.settingsPluginListItem, self.settingsLanguageMenu.menuAction(), None,
                self.formattingTagItem, self.settingsShortcutsItem, self.settingsConfigureItem))
        add_actions(self.toolsMenu, (self.toolsAddToolItem, None))
        add_actions(self.toolsMenu, (self.toolsOpenDataFolder, None))
        add_actions(self.toolsMenu, (self.toolsFirstTimeWizard, None))
        add_actions(self.toolsMenu, [self.updateThemeImages])
        if os.name == u'nt':
            add_actions(self.helpMenu, (self.offlineHelpItem, self.onlineHelpItem, None, self.webSiteItem,
                self.aboutItem))
        else:
            add_actions(self.helpMenu, (self.onlineHelpItem, None, self.webSiteItem, self.aboutItem))
        add_actions(self.menuBar, (self.fileMenu.menuAction(), self.viewMenu.menuAction(), self.toolsMenu.menuAction(),
            self.settingsMenu.menuAction(), self.helpMenu.menuAction()))
        # Initialise the translation
        self.retranslateUi(main_window)
        self.mediaToolBox.setCurrentIndex(0)
        # Connect up some signals and slots
        QtCore.QObject.connect(self.fileMenu, QtCore.SIGNAL(u'aboutToShow()'), self.updateRecentFilesMenu)
        # Hide the entry, as it does not have any functionality yet.
        self.toolsAddToolItem.setVisible(False)
        self.importLanguageItem.setVisible(False)
        self.exportLanguageItem.setVisible(False)
        self.setLockPanel(panelLocked)
        self.settingsImported = False

    def retranslateUi(self, mainWindow):
        """
        Set up the translation system
        """
        mainWindow.mainTitle = UiStrings().OLPV2x
        mainWindow.setWindowTitle(mainWindow.mainTitle)
        self.fileMenu.setTitle(translate('OpenLP.MainWindow', '&File'))
        self.fileImportMenu.setTitle(translate('OpenLP.MainWindow', '&Import'))
        self.fileExportMenu.setTitle(translate('OpenLP.MainWindow', '&Export'))
        self.recentFilesMenu.setTitle(translate('OpenLP.MainWindow', '&Recent Files'))
        self.viewMenu.setTitle(translate('OpenLP.MainWindow', '&View'))
        self.viewModeMenu.setTitle(translate('OpenLP.MainWindow', 'M&ode'))
        self.toolsMenu.setTitle(translate('OpenLP.MainWindow', '&Tools'))
        self.settingsMenu.setTitle(translate('OpenLP.MainWindow', '&Settings'))
        self.settingsLanguageMenu.setTitle(translate('OpenLP.MainWindow', '&Language'))
        self.helpMenu.setTitle(translate('OpenLP.MainWindow', '&Help'))
        self.mediaManagerDock.setWindowTitle(translate('OpenLP.MainWindow', 'Media Manager'))
        self.serviceManagerDock.setWindowTitle(translate('OpenLP.MainWindow', 'Service Manager'))
        self.themeManagerDock.setWindowTitle(translate('OpenLP.MainWindow', 'Theme Manager'))
        self.fileNewItem.setText(translate('OpenLP.MainWindow', '&New'))
        self.fileNewItem.setToolTip(UiStrings().NewService)
        self.fileNewItem.setStatusTip(UiStrings().CreateService)
        self.fileOpenItem.setText(translate('OpenLP.MainWindow', '&Open'))
        self.fileOpenItem.setToolTip(UiStrings().OpenService)
        self.fileOpenItem.setStatusTip(translate('OpenLP.MainWindow', 'Open an existing service.'))
        self.fileSaveItem.setText(translate('OpenLP.MainWindow', '&Save'))
        self.fileSaveItem.setToolTip(UiStrings().SaveService)
        self.fileSaveItem.setStatusTip(translate('OpenLP.MainWindow', 'Save the current service to disk.'))
        self.fileSaveAsItem.setText(translate('OpenLP.MainWindow', 'Save &As...'))
        self.fileSaveAsItem.setToolTip(translate('OpenLP.MainWindow', 'Save Service As'))
        self.fileSaveAsItem.setStatusTip(translate('OpenLP.MainWindow', 'Save the current service under a new name.'))
        self.printServiceOrderItem.setText(UiStrings().PrintService)
        self.printServiceOrderItem.setStatusTip(translate('OpenLP.MainWindow', 'Print the current service.'))
        self.fileExitItem.setText(translate('OpenLP.MainWindow', 'E&xit'))
        self.fileExitItem.setStatusTip(translate('OpenLP.MainWindow', 'Quit OpenLP'))
        self.importThemeItem.setText(translate('OpenLP.MainWindow', '&Theme'))
        self.importLanguageItem.setText(translate('OpenLP.MainWindow', '&Language'))
        self.exportThemeItem.setText(translate('OpenLP.MainWindow', '&Theme'))
        self.exportLanguageItem.setText(translate('OpenLP.MainWindow', '&Language'))
        self.settingsShortcutsItem.setText(translate('OpenLP.MainWindow', 'Configure &Shortcuts...'))
        self.formattingTagItem.setText(translate('OpenLP.MainWindow', 'Configure &Formatting Tags...'))
        self.settingsConfigureItem.setText(translate('OpenLP.MainWindow', '&Configure OpenLP...'))
        self.settingsExportItem.setStatusTip(translate('OpenLP.MainWindow',
            'Export OpenLP settings to a specified *.config file'))
        self.settingsExportItem.setText(translate('OpenLP.MainWindow', 'Settings'))
        self.settingsImportItem.setStatusTip(translate('OpenLP.MainWindow',
            'Import OpenLP settings from a specified *.config file previously exported on this or another machine'))
        self.settingsImportItem.setText(translate('OpenLP.MainWindow', 'Settings'))
        self.viewMediaManagerItem.setText(translate('OpenLP.MainWindow', '&Media Manager'))
        self.viewMediaManagerItem.setToolTip(translate('OpenLP.MainWindow', 'Toggle Media Manager'))
        self.viewMediaManagerItem.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the media manager.'))
        self.viewThemeManagerItem.setText(translate('OpenLP.MainWindow', '&Theme Manager'))
        self.viewThemeManagerItem.setToolTip(translate('OpenLP.MainWindow', 'Toggle Theme Manager'))
        self.viewThemeManagerItem.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the theme manager.'))
        self.viewServiceManagerItem.setText(translate('OpenLP.MainWindow', '&Service Manager'))
        self.viewServiceManagerItem.setToolTip(translate('OpenLP.MainWindow', 'Toggle Service Manager'))
        self.viewServiceManagerItem.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the service manager.'))
        self.viewPreviewPanel.setText(translate('OpenLP.MainWindow', '&Preview Panel'))
        self.viewPreviewPanel.setToolTip(translate('OpenLP.MainWindow', 'Toggle Preview Panel'))
        self.viewPreviewPanel.setStatusTip(
            translate('OpenLP.MainWindow', 'Toggle the visibility of the preview panel.'))
        self.viewLivePanel.setText(translate('OpenLP.MainWindow', '&Live Panel'))
        self.viewLivePanel.setToolTip(translate('OpenLP.MainWindow', 'Toggle Live Panel'))
        self.lockPanel.setText(translate('OpenLP.MainWindow', 'L&ock Panels'))
        self.lockPanel.setStatusTip(translate('OpenLP.MainWindow', 'Prevent the panels being moved.'))
        self.viewLivePanel.setStatusTip(translate('OpenLP.MainWindow', 'Toggle the visibility of the live panel.'))
        self.settingsPluginListItem.setText(translate('OpenLP.MainWindow', '&Plugin List'))
        self.settingsPluginListItem.setStatusTip(translate('OpenLP.MainWindow', 'List the Plugins'))
        self.aboutItem.setText(translate('OpenLP.MainWindow', '&About'))
        self.aboutItem.setStatusTip(translate('OpenLP.MainWindow', 'More information about OpenLP'))
        if os.name == u'nt':
            self.offlineHelpItem.setText(translate('OpenLP.MainWindow', '&User Guide'))
        self.onlineHelpItem.setText(translate('OpenLP.MainWindow', '&Online Help'))
        self.webSiteItem.setText(translate('OpenLP.MainWindow', '&Web Site'))
        for item in self.languageGroup.actions():
            item.setText(item.objectName())
            item.setStatusTip(translate('OpenLP.MainWindow', 'Set the interface language to %s') % item.objectName())
        self.autoLanguageItem.setText(translate('OpenLP.MainWindow', '&Autodetect'))
        self.autoLanguageItem.setStatusTip(translate('OpenLP.MainWindow', 'Use the system language, if available.'))
        self.toolsAddToolItem.setText(translate('OpenLP.MainWindow', 'Add &Tool...'))
        self.toolsAddToolItem.setStatusTip(translate('OpenLP.MainWindow', 'Add an application to the list of tools.'))
        self.toolsOpenDataFolder.setText(translate('OpenLP.MainWindow', 'Open &Data Folder...'))
        self.toolsOpenDataFolder.setStatusTip(translate('OpenLP.MainWindow',
            'Open the folder where songs, bibles and other data resides.'))
        self.toolsFirstTimeWizard.setText(translate('OpenLP.MainWindow', 'Re-run First Time Wizard'))
        self.toolsFirstTimeWizard.setStatusTip(translate('OpenLP.MainWindow',
            'Re-run the First Time Wizard, importing songs, Bibles and themes.'))
        self.updateThemeImages.setText(translate('OpenLP.MainWindow', 'Update Theme Images'))
        self.updateThemeImages.setStatusTip(translate('OpenLP.MainWindow', 'Update the preview images for all themes.'))
        self.modeDefaultItem.setText(translate('OpenLP.MainWindow', '&Default'))
        self.modeDefaultItem.setStatusTip(translate('OpenLP.MainWindow', 'Set the view mode back to the default.'))
        self.modeSetupItem.setText(translate('OpenLP.MainWindow', '&Setup'))
        self.modeSetupItem.setStatusTip(translate('OpenLP.MainWindow', 'Set the view mode to Setup.'))
        self.modeLiveItem.setText(translate('OpenLP.MainWindow', '&Live'))
        self.modeLiveItem.setStatusTip(translate('OpenLP.MainWindow', 'Set the view mode to Live.'))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    The main window.
    """
    log.info(u'MainWindow loaded')

    def __init__(self):
        """
        This constructor sets up the interface, the various managers, and the
        plugins.
        """
        QtGui.QMainWindow.__init__(self)
        Registry().register(u'main_window', self)
        self.clipboard = self.application.clipboard()
        self.arguments = self.application.args
        # Set up settings sections for the main application (not for use by plugins).
        self.uiSettingsSection = u'user interface'
        self.generalSettingsSection = u'general'
        self.advancedSettingsSection = u'advanced'
        self.shortcutsSettingsSection = u'shortcuts'
        self.serviceManagerSettingsSection = u'servicemanager'
        self.songsSettingsSection = u'songs'
        self.themesSettingsSection = u'themes'
        self.playersSettingsSection = u'players'
        self.displayTagsSection = u'displayTags'
        self.headerSection = u'SettingsImport'
        Settings().set_up_default_values()
        Settings().remove_obsolete_settings()
        self.serviceNotSaved = False
        self.aboutForm = AboutForm(self)
        self.mediaController = MediaController(self)
        self.settingsForm = SettingsForm(self)
        self.formattingTagForm = FormattingTagForm(self)
        self.shortcutForm = ShortcutListForm(self)
        self.recentFiles = []
        # Set up the path with plugins
        plugin_path = AppLocation.get_directory(AppLocation.PluginsDir)
        self.plugin_manager = PluginManager(plugin_path)
        self.imageManager = ImageManager()
        # Set up the interface
        self.setupUi(self)
        # Register the active media players and suffixes
        self.mediaController.check_available_media_players()
        # Load settings after setupUi so default UI sizes are overwritten
        self.loadSettings()
        # Once settings are loaded update the menu with the recent files.
        self.updateRecentFilesMenu()
        self.pluginForm = PluginForm(self)
        self.newDataPath = u''
        self.copyData = False
        # Set up signals and slots
        QtCore.QObject.connect(self.importThemeItem, QtCore.SIGNAL(u'triggered()'),
            self.themeManagerContents.on_import_theme)
        QtCore.QObject.connect(self.exportThemeItem, QtCore.SIGNAL(u'triggered()'),
            self.themeManagerContents.on_export_theme)
        QtCore.QObject.connect(self.mediaManagerDock, QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.viewMediaManagerItem.setChecked)
        QtCore.QObject.connect(self.serviceManagerDock, QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.viewServiceManagerItem.setChecked)
        QtCore.QObject.connect(self.themeManagerDock, QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.viewThemeManagerItem.setChecked)
        QtCore.QObject.connect(self.webSiteItem, QtCore.SIGNAL(u'triggered()'), self.onHelpWebSiteClicked)
        QtCore.QObject.connect(self.toolsOpenDataFolder, QtCore.SIGNAL(u'triggered()'),
            self.onToolsOpenDataFolderClicked)
        QtCore.QObject.connect(self.toolsFirstTimeWizard, QtCore.SIGNAL(u'triggered()'), self.onFirstTimeWizardClicked)
        QtCore.QObject.connect(self.updateThemeImages, QtCore.SIGNAL(u'triggered()'), self.onUpdateThemeImages)
        QtCore.QObject.connect(self.formattingTagItem, QtCore.SIGNAL(u'triggered()'), self.onFormattingTagItemClicked)
        QtCore.QObject.connect(self.settingsConfigureItem, QtCore.SIGNAL(u'triggered()'),
            self.onSettingsConfigureItemClicked)
        QtCore.QObject.connect(self.settingsShortcutsItem, QtCore.SIGNAL(u'triggered()'),
            self.onSettingsShortcutsItemClicked)
        QtCore.QObject.connect(self.settingsImportItem, QtCore.SIGNAL(u'triggered()'),
            self.onSettingsImportItemClicked)
        QtCore.QObject.connect(self.settingsExportItem, QtCore.SIGNAL(u'triggered()'), self.onSettingsExportItemClicked)
        # i18n set signals for languages
        self.languageGroup.triggered.connect(LanguageManager.set_language)
        QtCore.QObject.connect(self.modeDefaultItem, QtCore.SIGNAL(u'triggered()'), self.onModeDefaultItemClicked)
        QtCore.QObject.connect(self.modeSetupItem, QtCore.SIGNAL(u'triggered()'), self.onModeSetupItemClicked)
        QtCore.QObject.connect(self.modeLiveItem, QtCore.SIGNAL(u'triggered()'), self.onModeLiveItemClicked)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'theme_update_global'), self.defaultThemeChanged)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'openlp_version_check'), self.versionNotice)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'live_display_blank_check'), self.blankCheck)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'config_screen_changed'), self.screenChanged)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'mainwindow_status_text'),
            self.showStatusMessage)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'cleanup'), self.clean_up)
        # Media Manager
        QtCore.QObject.connect(self.mediaToolBox, QtCore.SIGNAL(u'currentChanged(int)'), self.onMediaToolBoxChanged)
        self.application.set_busy_cursor()
        # Simple message boxes
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'openlp_error_message'), self.onErrorMessage)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'openlp_information_message'),
            self.onInformationMessage)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'set_new_data_path'), self.setNewDataPath)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'set_copy_data'), self.setCopyData)
        # warning cyclic dependency
        # renderer needs to call ThemeManager and
        # ThemeManager needs to call Renderer
        self.renderer = Renderer()
        # Define the media Dock Manager
        self.mediaDockManager = MediaDockManager(self.mediaToolBox)
        log.info(u'Load Plugins')
        self.plugin_manager.find_plugins(plugin_path)
        # hook methods have to happen after find_plugins. Find plugins needs
        # the controllers hence the hooks have moved from setupUI() to here
        # Find and insert settings tabs
        log.info(u'hook settings')
        self.plugin_manager.hook_settings_tabs(self.settingsForm)
        # Find and insert media manager items
        log.info(u'hook media')
        self.plugin_manager.hook_media_manager()
        # Call the hook method to pull in import menus.
        log.info(u'hook menus')
        self.plugin_manager.hook_import_menu(self.fileImportMenu)
        # Call the hook method to pull in export menus.
        self.plugin_manager.hook_export_menu(self.fileExportMenu)
        # Call the hook method to pull in tools menus.
        self.plugin_manager.hook_tools_menu(self.toolsMenu)
        # Call the initialise method to setup plugins.
        log.info(u'initialise plugins')
        self.plugin_manager.initialise_plugins()
        # Create the displays as all necessary components are loaded.
        self.previewController.screenSizeChanged()
        self.liveController.screenSizeChanged()
        log.info(u'Load data from Settings')
        if Settings().value(u'advanced/save current plugin'):
            savedPlugin = Settings().value(u'advanced/current media plugin')
            if savedPlugin != -1:
                self.mediaToolBox.setCurrentIndex(savedPlugin)
        self.settingsForm.postSetUp()
        # Once all components are initialised load the Themes
        log.info(u'Load Themes')
        self.themeManagerContents.load_themes(True)
        # Hide/show the theme combobox on the service manager
        self.serviceManagerContents.theme_change()
        # Reset the cursor
        self.application.set_normal_cursor()

    def setAutoLanguage(self, value):
        """
        Set the language to automatic.
        """
        self.languageGroup.setDisabled(value)
        LanguageManager.auto_language = value
        LanguageManager.set_language(self.languageGroup.checkedAction())

    def onMediaToolBoxChanged(self, index):
        """
        Focus a widget when the media toolbox changes.
        """
        widget = self.mediaToolBox.widget(index)
        if widget:
            widget.onFocus()

    def versionNotice(self, version):
        """
        Notifies the user that a newer version of OpenLP is available.
        Triggered by delay thread.
        """
        version_text = translate('OpenLP.MainWindow', 'Version %s of OpenLP is now available for download (you are '
            'currently running version %s). \n\nYou can download the latest version from http://openlp.org/.')
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
        if self.arguments:
            args = []
            for a in self.arguments:
                args.extend([a])
            filename = args[0]
            if not isinstance(filename, unicode):
                filename = unicode(filename, sys.getfilesystemencoding())
            self.serviceManagerContents.load_file(filename)
        elif Settings().value(self.generalSettingsSection + u'/auto open'):
            self.serviceManagerContents.load_Last_file()
        view_mode = Settings().value(u'%s/view mode' % self.generalSettingsSection)
        if view_mode == u'default':
            self.modeDefaultItem.setChecked(True)
        elif view_mode == u'setup':
            self.setViewMode(True, True, False, True, False)
            self.modeSetupItem.setChecked(True)
        elif view_mode == u'live':
            self.setViewMode(False, True, False, False, True)
            self.modeLiveItem.setChecked(True)

    def app_startup(self):
        """
        Give all the plugins a chance to perform some tasks at startup
        """
        self.application.process_events()
        for plugin in self.plugin_manager.plugins:
            if plugin.isActive():
                plugin.app_startup()
                self.application.process_events()

    def first_time(self):
        """
        Import themes if first time
        """
        self.application.process_events()
        for plugin in self.plugin_manager.plugins:
            if hasattr(plugin, u'first_time'):
                self.application.process_events()
                plugin.first_time()
        self.application.process_events()
        temp_dir = os.path.join(unicode(gettempdir()), u'openlp')
        shutil.rmtree(temp_dir, True)

    def onFirstTimeWizardClicked(self):
        """
        Re-run the first time wizard.  Prompts the user for run confirmation
        If wizard is run, songs, bibles and themes are imported.  The default
        theme is changed (if necessary).  The plugins in pluginmanager are
        set active/in-active to match the selection in the wizard.
        """
        answer = QtGui.QMessageBox.warning(self,
            translate('OpenLP.MainWindow', 'Re-run First Time Wizard?'),
            translate('OpenLP.MainWindow', 'Are you sure you want to re-run the First Time Wizard?\n\n'
                'Re-running this wizard may make changes to your current '
                'OpenLP configuration and possibly add songs to your '
                'existing songs list and change your default theme.'),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
                QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.No:
            return
        screens = ScreenList()
        first_run_wizard = FirstTimeForm(screens, self)
        first_run_wizard.exec_()
        if first_run_wizard.was_download_cancelled:
            return
        self.application.set_busy_cursor()
        self.first_time()
        for plugin in self.plugin_manager.plugins:
            self.activePlugin = plugin
            oldStatus = self.activePlugin.status
            self.activePlugin.setStatus()
            if oldStatus != self.activePlugin.status:
                if self.activePlugin.status == PluginStatus.Active:
                    self.activePlugin.toggleStatus(PluginStatus.Active)
                    self.activePlugin.app_startup()
                else:
                    self.activePlugin.toggleStatus(PluginStatus.Inactive)
        self.themeManagerContents.configUpdated()
        self.themeManagerContents.load_themes(True)
        Receiver.send_message(u'theme_update_global', self.themeManagerContents.global_theme)
        # Check if any Bibles downloaded.  If there are, they will be
        # processed.
        Receiver.send_message(u'bibles_load_list', True)
        self.application.set_normal_cursor()

    def blankCheck(self):
        """
        Check and display message if screen blank on setup.
        """
        settings = Settings()
        self.liveController.mainDisplaySetBackground()
        if settings.value(u'%s/screen blank' % self.generalSettingsSection):
            if settings.value(u'%s/blank warning' % self.generalSettingsSection):
                QtGui.QMessageBox.question(self, translate('OpenLP.MainWindow', 'OpenLP Main Display Blanked'),
                    translate('OpenLP.MainWindow', 'The Main Display has been blanked out'))

    def onErrorMessage(self, data):
        """
        Display an error message
        """
        self.application.close_splash_screen()
        QtGui.QMessageBox.critical(self, data[u'title'], data[u'message'])

    def warning_message(self, message):
        """
        Display a warning message
        """
        self.application.close_splash_screen()
        QtGui.QMessageBox.warning(self, message[u'title'], message[u'message'])

    def onInformationMessage(self, data):
        """
        Display an informational message
        """
        self.application.close_splash_screen()
        QtGui.QMessageBox.information(self, data[u'title'], data[u'message'])

    def onHelpWebSiteClicked(self):
        """
        Load the OpenLP website
        """
        import webbrowser
        webbrowser.open_new(u'http://openlp.org/')

    def onOfflineHelpClicked(self):
        """
        Load the local OpenLP help file
        """
        os.startfile(self.localHelpFile)

    def onOnlineHelpClicked(self):
        """
        Load the online OpenLP manual
        """
        import webbrowser
        webbrowser.open_new(u'http://manual.openlp.org/')

    def onAboutItemClicked(self):
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
        self.themeManagerContents.update_preview_images()

    def onFormattingTagItemClicked(self):
        """
        Show the Settings dialog
        """
        self.formattingTagForm.exec_()

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

    def onSettingsImportItemClicked(self):
        """
        Import settings from an export INI file
        """
        answer = QtGui.QMessageBox.critical(self, translate('OpenLP.MainWindow', 'Import settings?'),
            translate('OpenLP.MainWindow', 'Are you sure you want to import settings?\n\n'
                'Importing settings will make permanent changes to your current OpenLP configuration.\n\n'
                'Importing incorrect settings may cause erratic behaviour or OpenLP to terminate abnormally.'),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
                QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.No:
            return
        import_file_name = QtGui.QFileDialog.getOpenFileName(self, translate('OpenLP.MainWindow', 'Open File'), '',
            translate('OpenLP.MainWindow', 'OpenLP Export Settings Files (*.conf)'))
        if not import_file_name:
            return
        setting_sections = []
        # Add main sections.
        setting_sections.extend([self.generalSettingsSection])
        setting_sections.extend([self.advancedSettingsSection])
        setting_sections.extend([self.uiSettingsSection])
        setting_sections.extend([self.shortcutsSettingsSection])
        setting_sections.extend([self.serviceManagerSettingsSection])
        setting_sections.extend([self.themesSettingsSection])
        setting_sections.extend([self.playersSettingsSection])
        setting_sections.extend([self.displayTagsSection])
        setting_sections.extend([self.headerSection])
        setting_sections.extend([u'crashreport'])
        # Add plugin sections.
        for plugin in self.plugin_manager.plugins:
            setting_sections.extend([plugin.name])
        # Copy the settings file to the tmp dir, because we do not want to change the original one.
        temp_directory = os.path.join(unicode(gettempdir()), u'openlp')
        check_directory_exists(temp_directory)
        temp_config = os.path.join(temp_directory, os.path.basename(import_file_name))
        shutil.copyfile(import_file_name, temp_config)
        settings = Settings()
        import_settings = Settings(temp_config, Settings.IniFormat)
        # Remove/rename old settings to prepare the import.
        import_settings.remove_obsolete_settings()
        # Lets do a basic sanity check. If it contains this string we can
        # assume it was created by OpenLP and so we'll load what we can
        # from it, and just silently ignore anything we don't recognise
        if import_settings.value(u'SettingsImport/type') != u'OpenLP_settings_export':
            QtGui.QMessageBox.critical(self, translate('OpenLP.MainWindow', 'Import settings'),
                translate('OpenLP.MainWindow', 'The file you have selected does not appear to be a valid OpenLP '
                    'settings file.\n\nProcessing has terminated and no changes have been made.'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
            return
        import_keys = import_settings.allKeys()
        for section_key in import_keys:
            # We need to handle the really bad files.
            try:
                section, key = section_key.split(u'/')
            except ValueError:
                section = u'unknown'
                key = u''
            # Switch General back to lowercase.
            if section == u'General' or section == u'%General':
                section = u'general'
                section_key = section + "/" + key
            # Make sure it's a valid section for us.
            if not section in setting_sections:
                continue
        # We have a good file, import it.
        for section_key in import_keys:
            if u'eneral' in section_key:
                section_key = section_key.lower()
            value = import_settings.value(section_key)
            if value is not None:
                settings.setValue(u'%s' % (section_key), value)
        now = datetime.now()
        settings.beginGroup(self.headerSection)
        settings.setValue(u'file_imported', import_file_name)
        settings.setValue(u'file_date_imported', now.strftime("%Y-%m-%d %H:%M"))
        settings.endGroup()
        settings.sync()
        # We must do an immediate restart or current configuration will
        # overwrite what was just imported when application terminates
        # normally.   We need to exit without saving configuration.
        QtGui.QMessageBox.information(self, translate('OpenLP.MainWindow', 'Import settings'),
            translate('OpenLP.MainWindow', 'OpenLP will now close.  Imported settings will '
                'be applied the next time you start OpenLP.'),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
        self.settingsImported = True
        self.clean_up()
        QtCore.QCoreApplication.exit()

    def onSettingsExportItemClicked(self):
        """
        Export settings to a .conf file in INI format
        """
        export_file_name = QtGui.QFileDialog.getSaveFileName(self,
            translate('OpenLP.MainWindow', 'Export Settings File'), '',
            translate('OpenLP.MainWindow', 'OpenLP Export Settings File (*.conf)'))
        if not export_file_name:
            return
            # Make sure it's a .conf file.
        if not export_file_name.endswith(u'conf'):
            export_file_name += u'.conf'
        temp_file = os.path.join(unicode(gettempdir(),
            get_filesystem_encoding()), u'openlp', u'exportConf.tmp')
        self.saveSettings()
        setting_sections = []
        # Add main sections.
        setting_sections.extend([self.generalSettingsSection])
        setting_sections.extend([self.advancedSettingsSection])
        setting_sections.extend([self.uiSettingsSection])
        setting_sections.extend([self.shortcutsSettingsSection])
        setting_sections.extend([self.serviceManagerSettingsSection])
        setting_sections.extend([self.themesSettingsSection])
        setting_sections.extend([self.displayTagsSection])
        # Add plugin sections.
        for plugin in self.plugin_manager.plugins:
            setting_sections.extend([plugin.name])
        # Delete old files if found.
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(export_file_name):
            os.remove(export_file_name)
        settings = Settings()
        settings.remove(self.headerSection)
        # Get the settings.
        keys = settings.allKeys()
        export_settings = Settings(temp_file, Settings.IniFormat)
        # Add a header section.
        # This is to insure it's our conf file for import.
        now = datetime.now()
        application_version = get_application_version()
        # Write INI format using Qsettings.
        # Write our header.
        export_settings.beginGroup(self.headerSection)
        export_settings.setValue(u'Make_Changes', u'At_Own_RISK')
        export_settings.setValue(u'type', u'OpenLP_settings_export')
        export_settings.setValue(u'file_date_created', now.strftime("%Y-%m-%d %H:%M"))
        export_settings.setValue(u'version', application_version[u'full'])
        export_settings.endGroup()
        # Write all the sections and keys.
        for section_key in keys:
            # FIXME: We are conflicting with the standard "General" section.
            if u'eneral' in section_key:
                section_key = section_key.lower()
            key_value = settings.value(section_key)
            if key_value is not None:
                export_settings.setValue(section_key, key_value)
        export_settings.sync()
        # Temp CONF file has been written.  Blanks in keys are now '%20'.
        # Read the  temp file and output the user's CONF file with blanks to
        # make it more readable.
        temp_conf = open(temp_file, u'r')
        export_conf = open(export_file_name, u'w')
        for file_record in temp_conf:
            # Get rid of any invalid entries.
            if file_record.find(u'@Invalid()') == -1:
                file_record = file_record.replace(u'%20', u' ')
                export_conf.write(file_record)
        temp_conf.close()
        export_conf.close()
        os.remove(temp_file)

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
            settings = Settings()
            settings.setValue(u'%s/view mode' % self.generalSettingsSection, mode)
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
        self.application.set_busy_cursor()
        self.imageManager.update_display()
        self.renderer.update_display()
        self.previewController.screenSizeChanged()
        self.liveController.screenSizeChanged()
        self.setFocus()
        self.activateWindow()
        self.application.set_normal_cursor()

    def closeEvent(self, event):
        """
        Hook to close the main window and display windows on exit
        """
        # The MainApplication did not even enter the event loop (this happens
        # when OpenLP is not fully loaded). Just ignore the event.
        if not self.application.is_event_loop_active:
            event.ignore()
            return
        # If we just did a settings import, close without saving changes.
        if self.settingsImported:
            self.clean_up(False)
            event.accept()
        if self.serviceManagerContents.is_modified():
            ret = self.serviceManagerContents.save_modified_service()
            if ret == QtGui.QMessageBox.Save:
                if self.serviceManagerContents.decide_save_method():
                    self.clean_up()
                    event.accept()
                else:
                    event.ignore()
            elif ret == QtGui.QMessageBox.Discard:
                self.clean_up()
                event.accept()
            else:
                event.ignore()
        else:
            if Settings().value(u'advanced/enable exit confirmation'):
                ret = QtGui.QMessageBox.question(self, translate('OpenLP.MainWindow', 'Close OpenLP'),
                        translate('OpenLP.MainWindow', 'Are you sure you want to close OpenLP?'),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
                    QtGui.QMessageBox.Yes)
                if ret == QtGui.QMessageBox.Yes:
                    self.clean_up()
                    event.accept()
                else:
                    event.ignore()
            else:
                self.clean_up()
                event.accept()

    def clean_up(self, save_settings=True):
        """
        Runs all the cleanup code before OpenLP shuts down.

        ``save_settings``
            Switch to prevent saving settings. Defaults to **True**.
        """
        self.imageManager.stop_manager = True
        while self.imageManager.image_thread.isRunning():
            time.sleep(0.1)
        # Clean temporary files used by services
        self.serviceManagerContents.clean_up()
        if save_settings:
            if Settings().value(u'advanced/save current plugin'):
                Settings().setValue(u'advanced/current media plugin', self.mediaToolBox.currentIndex())
        # Call the cleanup method to shutdown plugins.
        log.info(u'cleanup plugins')
        self.plugin_manager.finalise_plugins()
        if save_settings:
            # Save settings
            self.saveSettings()
        # Check if we need to change the data directory
        if self.newDataPath:
            self.changeDataDirectory()
        # Close down the display
        if self.liveController.display:
            self.liveController.display.close()
            self.liveController.display = None
        # Allow the main process to exit
        self.application = None

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
        """
        Show a message in the status bar
        """
        self.statusBar.showMessage(message)

    def defaultThemeChanged(self, theme):
        """
        Update the default theme indicator in the status bar
        """
        self.defaultThemeLabel.setText(translate('OpenLP.MainWindow', 'Default Theme: %s') % theme)

    def toggleMediaManager(self):
        """
        Toggle the visibility of the media manager
        """
        self.mediaManagerDock.setVisible(not self.mediaManagerDock.isVisible())

    def toggleServiceManager(self):
        """
        Toggle the visibility of the service manager
        """
        self.serviceManagerDock.setVisible(not self.serviceManagerDock.isVisible())

    def toggleThemeManager(self):
        """
        Toggle the visibility of the theme manager
        """
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
        Settings().setValue(u'user interface/preview panel', visible)
        self.viewPreviewPanel.setChecked(visible)

    def setLockPanel(self, lock):
        """
        Sets the ability to stop the toolbars being changed.
        """
        if lock:
            self.themeManagerDock.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
            self.serviceManagerDock.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
            self.mediaManagerDock.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
            self.viewMediaManagerItem.setEnabled(False)
            self.viewServiceManagerItem.setEnabled(False)
            self.viewThemeManagerItem.setEnabled(False)
            self.viewPreviewPanel.setEnabled(False)
            self.viewLivePanel.setEnabled(False)
        else:
            self.themeManagerDock.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
            self.serviceManagerDock.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
            self.mediaManagerDock.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
            self.viewMediaManagerItem.setEnabled(True)
            self.viewServiceManagerItem.setEnabled(True)
            self.viewThemeManagerItem.setEnabled(True)
            self.viewPreviewPanel.setEnabled(True)
            self.viewLivePanel.setEnabled(True)
        Settings().setValue(u'user interface/lock panel', lock)

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
        Settings().setValue(u'user interface/live panel', visible)
        self.viewLivePanel.setChecked(visible)

    def loadSettings(self):
        """
        Load the main window settings.
        """
        log.debug(u'Loading QSettings')
        settings = Settings()
        # Remove obsolete entries.
        settings.remove(u'custom slide')
        settings.remove(u'service')
        settings.beginGroup(self.generalSettingsSection)
        self.recentFiles = settings.value(u'recent files')
        settings.endGroup()
        settings.beginGroup(self.uiSettingsSection)
        self.move(settings.value(u'main window position'))
        self.restoreGeometry(settings.value(u'main window geometry'))
        self.restoreState(settings.value(u'main window state'))
        self.liveController.splitter.restoreState(settings.value(u'live splitter geometry'))
        self.previewController.splitter.restoreState(settings.value(u'preview splitter geometry'))
        self.controlSplitter.restoreState(settings.value(u'main window splitter geometry'))
        settings.endGroup()

    def saveSettings(self):
        """
        Save the main window settings.
        """
        # Exit if we just did a settings import.
        if self.settingsImported:
            return
        log.debug(u'Saving QSettings')
        settings = Settings()
        settings.beginGroup(self.generalSettingsSection)
        settings.setValue(u'recent files', self.recentFiles)
        settings.endGroup()
        settings.beginGroup(self.uiSettingsSection)
        settings.setValue(u'main window position', self.pos())
        settings.setValue(u'main window state', self.saveState())
        settings.setValue(u'main window geometry', self.saveGeometry())
        settings.setValue(u'live splitter geometry', self.liveController.splitter.saveState())
        settings.setValue(u'preview splitter geometry', self.previewController.splitter.saveState())
        settings.setValue(u'main window splitter geometry', self.controlSplitter.saveState())
        settings.endGroup()

    def updateRecentFilesMenu(self):
        """
        Updates the recent file menu with the latest list of service files
        accessed.
        """
        recentFileCount = Settings().value(u'advanced/recent file count')
        existingRecentFiles = [recentFile for recentFile in self.recentFiles
            if os.path.isfile(unicode(recentFile))]
        recentFilesToDisplay = existingRecentFiles[0:recentFileCount]
        self.recentFilesMenu.clear()
        for fileId, filename in enumerate(recentFilesToDisplay):
            log.debug('Recent file name: %s', filename)
            action = create_action(self, u'',
                text=u'&%d %s' % (fileId + 1, os.path.splitext(os.path.basename(
                unicode(filename)))[0]), data=filename,
                triggers=self.serviceManagerContents.on_recent_service_clicked)
            self.recentFilesMenu.addAction(action)
        clearRecentFilesAction = create_action(self, u'',
            text=translate('OpenLP.MainWindow', 'Clear List', 'Clear List of recent files'),
            statustip=translate('OpenLP.MainWindow', 'Clear the list of recent files.'),
            enabled=bool(self.recentFiles),
            triggers=self.clearRecentFileMenu)
        add_actions(self.recentFilesMenu, (None, clearRecentFilesAction))
        clearRecentFilesAction.setEnabled(bool(self.recentFiles))

    def addRecentFile(self, filename):
        """
        Adds a service to the list of recently used files.

        ``filename``
            The service filename to add
        """
        # The maxRecentFiles value does not have an interface and so never gets
        # actually stored in the settings therefore the default value of 20 will
        # always be used.
        maxRecentFiles = Settings().value(u'advanced/max recent files')
        if filename:
            # Add some cleanup to reduce duplication in the recent file list
            filename = os.path.abspath(filename)
            # abspath() only capitalises the drive letter if it wasn't provided
            # in the given filename which then causes duplication.
            if filename[1:3] == ':\\':
                filename = filename[0].upper() + filename[1:]
            if filename in self.recentFiles:
                self.recentFiles.remove(filename)
            self.recentFiles.insert(0, filename)
            while len(self.recentFiles) > maxRecentFiles:
                self.recentFiles.pop()

    def clearRecentFileMenu(self):
        """
        Clears the recent files.
        """
        self.recentFiles = []

    def displayProgressBar(self, size):
        """
        Make Progress bar visible and set size
        """
        self.loadProgressBar.show()
        self.loadProgressBar.setMaximum(size)
        self.loadProgressBar.setValue(0)
        self.application.process_events()

    def incrementProgressBar(self):
        """
        Increase the Progress Bar value by 1
        """
        self.loadProgressBar.setValue(self.loadProgressBar.value() + 1)
        self.application.process_events()

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
            self.application.process_events()

    def setNewDataPath(self, new_data_path):
        """
        Set the new data path
        """
        self.newDataPath = new_data_path

    def setCopyData(self, copy_data):
        """
        Set the flag to copy the data
        """
        self.copyData = copy_data

    def changeDataDirectory(self):
        """
        Change the data directory.
        """
        log.info(u'Changing data path to %s' % self.newDataPath)
        old_data_path = unicode(AppLocation.get_data_path())
        # Copy OpenLP data to new location if requested.
        self.application.set_busy_cursor()
        if self.copyData:
            log.info(u'Copying data to new path')
            try:
                self.showStatusMessage(
                    translate('OpenLP.MainWindow', 'Copying OpenLP data to new data directory location - %s '
                    '- Please wait for copy to finish').replace('%s', self.newDataPath))
                dir_util.copy_tree(old_data_path, self.newDataPath)
                log.info(u'Copy sucessful')
            except (IOError, os.error, DistutilsFileError), why:
                self.application.set_normal_cursor()
                log.exception(u'Data copy failed %s' % unicode(why))
                QtGui.QMessageBox.critical(self, translate('OpenLP.MainWindow', 'New Data Directory Error'),
                    translate('OpenLP.MainWindow',
                        'OpenLP Data directory copy failed\n\n%s').replace('%s', unicode(why)),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                return False
        else:
            log.info(u'No data copy requested')
        # Change the location of data directory in config file.
        settings = QtCore.QSettings()
        settings.setValue(u'advanced/data path', self.newDataPath)
        # Check if the new data path is our default.
        if self.newDataPath == AppLocation.get_directory(AppLocation.DataDir):
            settings.remove(u'advanced/data path')
        self.application.set_normal_cursor()

    def _get_application(self):
        """
        Adds the openlp to the class dynamically
        """
        if not hasattr(self, u'_application'):
            self._application = Registry().get(u'application')
        return self._application

    application = property(_get_application)
