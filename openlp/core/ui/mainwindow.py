# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Eric Ludin, Edwin Lunando, Brian T. Meyer,    #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Erode Woldsund, Martin Zibricky                                             #
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
import shutil
from distutils import dir_util
from distutils.errors import DistutilsFileError
from tempfile import gettempdir
import time
from datetime import datetime

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Renderer, build_icon, OpenLPDockWidget, \
    PluginManager, Receiver, translate, ImageManager, PluginStatus
from openlp.core.lib.ui import UiStrings, create_action
from openlp.core.lib.settings import Settings
from openlp.core.lib import SlideLimits
from openlp.core.ui import AboutForm, SettingsForm, ServiceManager, \
    ThemeManager, SlideController, PluginForm, MediaDockManager, \
    ShortcutListForm, FormattingTagForm
from openlp.core.ui.media import MediaController
from openlp.core.utils import AppLocation, add_actions, LanguageManager, \
    get_application_version, get_filesystem_encoding
from openlp.core.utils.actions import ActionList, CategoryOrder
from openlp.core.ui.firsttimeform import FirstTimeForm
from openlp.core.ui import ScreenList

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
        previewVisible = Settings().value(
            u'user interface/preview panel', QtCore.QVariant(True)).toBool()
        self.previewController.panel.setVisible(previewVisible)
        liveVisible = Settings().value(u'user interface/live panel',
            QtCore.QVariant(True)).toBool()
        panelLocked = Settings().value(u'user interface/lock panel',
            QtCore.QVariant(False)).toBool()
        self.liveController.panel.setVisible(liveVisible)
        # Create menu
        self.menuBar = QtGui.QMenuBar(mainWindow)
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
        mainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(mainWindow)
        self.statusBar.setObjectName(u'statusBar')
        mainWindow.setStatusBar(self.statusBar)
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
        action_list.add_category(unicode(UiStrings().File),
            CategoryOrder.standardMenu)
        self.fileNewItem = create_action(mainWindow, u'fileNewItem',
            icon=u':/general/general_new.png',
            shortcuts=[QtGui.QKeySequence(u'Ctrl+N')],
            category=UiStrings().File,
            triggers=self.serviceManagerContents.onNewServiceClicked)
        self.fileOpenItem = create_action(mainWindow, u'fileOpenItem',
            icon=u':/general/general_open.png',
            shortcuts=[QtGui.QKeySequence(u'Ctrl+O')],
            category=UiStrings().File,
            triggers=self.serviceManagerContents.onLoadServiceClicked)
        self.fileSaveItem = create_action(mainWindow, u'fileSaveItem',
            icon=u':/general/general_save.png',
            shortcuts=[QtGui.QKeySequence(u'Ctrl+S')],
            category=UiStrings().File,
            triggers=self.serviceManagerContents.saveFile)
        self.fileSaveAsItem = create_action(mainWindow, u'fileSaveAsItem',
            shortcuts=[QtGui.QKeySequence(u'Ctrl+Shift+S')],
            category=UiStrings().File,
            triggers=self.serviceManagerContents.saveFileAs)
        self.printServiceOrderItem = create_action(mainWindow,
            u'printServiceItem', shortcuts=[QtGui.QKeySequence(u'Ctrl+P')],
            category=UiStrings().File,
            triggers=self.serviceManagerContents.printServiceOrder)
        self.fileExitItem = create_action(mainWindow, u'fileExitItem',
            icon=u':/system/system_exit.png',
            shortcuts=[QtGui.QKeySequence(u'Alt+F4')],
            category=UiStrings().File, triggers=mainWindow.close)
        # Give QT Extra Hint that this is the Exit Menu Item
        self.fileExitItem.setMenuRole(QtGui.QAction.QuitRole)
        action_list.add_category(unicode(UiStrings().Import),
            CategoryOrder.standardMenu)
        self.importThemeItem = create_action(mainWindow,
            u'importThemeItem', category=UiStrings().Import)
        self.importLanguageItem = create_action(mainWindow,
            u'importLanguageItem')#, category=UiStrings().Import)
        action_list.add_category(unicode(UiStrings().Export),
            CategoryOrder.standardMenu)
        self.exportThemeItem = create_action(mainWindow,
            u'exportThemeItem', category=UiStrings().Export)
        self.exportLanguageItem = create_action(mainWindow,
            u'exportLanguageItem')#, category=UiStrings().Export)
        action_list.add_category(unicode(UiStrings().View),
            CategoryOrder.standardMenu)
        self.viewMediaManagerItem = create_action(mainWindow,
            u'viewMediaManagerItem', shortcuts=[QtGui.QKeySequence(u'F8')],
            icon=u':/system/system_mediamanager.png',
            checked=self.mediaManagerDock.isVisible(),
            category=UiStrings().View, triggers=self.toggleMediaManager)
        self.viewThemeManagerItem = create_action(mainWindow,
            u'viewThemeManagerItem', shortcuts=[QtGui.QKeySequence(u'F10')],
            icon=u':/system/system_thememanager.png',
            checked=self.themeManagerDock.isVisible(),
            category=UiStrings().View, triggers=self.toggleThemeManager)
        self.viewServiceManagerItem = create_action(mainWindow,
            u'viewServiceManagerItem', shortcuts=[QtGui.QKeySequence(u'F9')],
            icon=u':/system/system_servicemanager.png',
            checked=self.serviceManagerDock.isVisible(),
            category=UiStrings().View, triggers=self.toggleServiceManager)
        self.viewPreviewPanel = create_action(mainWindow, u'viewPreviewPanel',
            shortcuts=[QtGui.QKeySequence(u'F11')], checked=previewVisible,
            category=UiStrings().View, triggers=self.setPreviewPanelVisibility)
        self.viewLivePanel = create_action(mainWindow, u'viewLivePanel',
            shortcuts=[QtGui.QKeySequence(u'F12')], checked=liveVisible,
            category=UiStrings().View, triggers=self.setLivePanelVisibility)
        self.lockPanel = create_action(mainWindow, u'lockPanel',
            checked=panelLocked, triggers=self.setLockPanel)
        action_list.add_category(unicode(UiStrings().ViewMode),
            CategoryOrder.standardMenu)
        self.modeDefaultItem = create_action(mainWindow, u'modeDefaultItem',
            checked=False, category=UiStrings().ViewMode)
        self.modeSetupItem = create_action(mainWindow, u'modeSetupItem',
            checked=False, category=UiStrings().ViewMode)
        self.modeLiveItem = create_action(mainWindow, u'modeLiveItem',
            checked=True, category=UiStrings().ViewMode)
        self.modeGroup = QtGui.QActionGroup(mainWindow)
        self.modeGroup.addAction(self.modeDefaultItem)
        self.modeGroup.addAction(self.modeSetupItem)
        self.modeGroup.addAction(self.modeLiveItem)
        self.modeDefaultItem.setChecked(True)
        action_list.add_category(unicode(UiStrings().Tools),
            CategoryOrder.standardMenu)
        self.toolsAddToolItem = create_action(mainWindow,
            u'toolsAddToolItem', icon=u':/tools/tools_add.png',
            category=UiStrings().Tools)
        self.toolsOpenDataFolder = create_action(mainWindow,
            u'toolsOpenDataFolder', icon=u':/general/general_open.png',
            category=UiStrings().Tools)
        self.toolsFirstTimeWizard = create_action(mainWindow,
            u'toolsFirstTimeWizard', icon=u':/general/general_revert.png',
            category=UiStrings().Tools)
        self.updateThemeImages = create_action(mainWindow,
            u'updateThemeImages', category=UiStrings().Tools)
        action_list.add_category(unicode(UiStrings().Settings),
            CategoryOrder.standardMenu)
        self.settingsPluginListItem = create_action(mainWindow,
            u'settingsPluginListItem',
            icon=u':/system/settings_plugin_list.png',
            shortcuts=[QtGui.QKeySequence(u'Alt+F7')],
            category=UiStrings().Settings, triggers=self.onPluginItemClicked)
        # i18n Language Items
        self.autoLanguageItem = create_action(mainWindow, u'autoLanguageItem',
            checked=LanguageManager.auto_language)
        self.languageGroup = QtGui.QActionGroup(mainWindow)
        self.languageGroup.setExclusive(True)
        self.languageGroup.setObjectName(u'languageGroup')
        add_actions(self.languageGroup, [self.autoLanguageItem])
        qmList = LanguageManager.get_qm_list()
        savedLanguage = LanguageManager.get_language()
        for key in sorted(qmList.keys()):
            languageItem = create_action(mainWindow, key,
                checked=qmList[key] == savedLanguage)
            add_actions(self.languageGroup, [languageItem])
        self.settingsShortcutsItem = create_action(mainWindow,
            u'settingsShortcutsItem',
            icon=u':/system/system_configure_shortcuts.png',
            category=UiStrings().Settings)
        # Formatting Tags were also known as display tags.
        self.formattingTagItem = create_action(mainWindow,
            u'displayTagItem', icon=u':/system/tag_editor.png',
            category=UiStrings().Settings)
        self.settingsConfigureItem = create_action(mainWindow,
            u'settingsConfigureItem', icon=u':/system/system_settings.png',
            category=UiStrings().Settings)
        # Give QT Extra Hint that this is the Preferences Menu Item
        self.settingsConfigureItem.setMenuRole(QtGui.QAction.PreferencesRole)
        self.settingsImportItem = create_action(mainWindow,
           u'settingsImportItem', category=UiStrings().Settings)
        self.settingsExportItem = create_action(mainWindow,
           u'settingsExportItem', category=UiStrings().Settings)
        action_list.add_category(unicode(UiStrings().Help),
            CategoryOrder.standardMenu)
        self.aboutItem = create_action(mainWindow, u'aboutItem',
            icon=u':/system/system_about.png',
            shortcuts=[QtGui.QKeySequence(u'Ctrl+F1')],
            category=UiStrings().Help, triggers=self.onAboutItemClicked)
        # Give QT Extra Hint that this is an About Menu Item
        self.aboutItem.setMenuRole(QtGui.QAction.AboutRole)
        if os.name == u'nt':
            self.localHelpFile = os.path.join(
                AppLocation.get_directory(AppLocation.AppDir), 'OpenLP.chm')
            self.offlineHelpItem = create_action(mainWindow, u'offlineHelpItem',
                icon=u':/system/system_help_contents.png',
                shortcuts=[QtGui.QKeySequence(u'F1')],
                category=UiStrings().Help, triggers=self.onOfflineHelpClicked)
        self.onlineHelpItem = create_action(mainWindow, u'onlineHelpItem',
            icon=u':/system/system_online_help.png',
            shortcuts=[QtGui.QKeySequence(u'Alt+F1')],
            category=UiStrings().Help, triggers=self.onOnlineHelpClicked)
        self.webSiteItem = create_action(mainWindow,
            u'webSiteItem', category=UiStrings().Help)
        add_actions(self.fileImportMenu, (self.settingsImportItem, None,
            self.importThemeItem, self.importLanguageItem))
        add_actions(self.fileExportMenu, (self.settingsExportItem, None,
            self.exportThemeItem, self.exportLanguageItem))
        add_actions(self.fileMenu, (self.fileNewItem, self.fileOpenItem,
            self.fileSaveItem, self.fileSaveAsItem,
            self.recentFilesMenu.menuAction(), None,
            self.fileImportMenu.menuAction(), self.fileExportMenu.menuAction(),
            None, self.printServiceOrderItem, self.fileExitItem))
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
                self.formattingTagItem))
        else:
            add_actions(self.settingsMenu, (self.settingsPluginListItem,
                self.settingsLanguageMenu.menuAction(), None,
                self.formattingTagItem, self.settingsShortcutsItem,
                self.settingsConfigureItem))
        add_actions(self.toolsMenu, (self.toolsAddToolItem, None))
        add_actions(self.toolsMenu, (self.toolsOpenDataFolder, None))
        add_actions(self.toolsMenu, (self.toolsFirstTimeWizard, None))
        add_actions(self.toolsMenu, [self.updateThemeImages])
        if os.name == u'nt':
            add_actions(self.helpMenu, (self.offlineHelpItem,
            self.onlineHelpItem, None, self.webSiteItem,
            self.aboutItem))
        else:
            add_actions(self.helpMenu, (self.onlineHelpItem, None,
                self.webSiteItem, self.aboutItem))
        add_actions(self.menuBar, (self.fileMenu.menuAction(),
            self.viewMenu.menuAction(), self.toolsMenu.menuAction(),
            self.settingsMenu.menuAction(), self.helpMenu.menuAction()))
        # Initialise the translation
        self.retranslateUi(mainWindow)
        self.mediaToolBox.setCurrentIndex(0)
        # Connect up some signals and slots
        QtCore.QObject.connect(self.fileMenu,
            QtCore.SIGNAL(u'aboutToShow()'), self.updateRecentFilesMenu)
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
        mainWindow.mainTitle = UiStrings().OLPV2
        mainWindow.setWindowTitle(mainWindow.mainTitle)
        self.fileMenu.setTitle(translate('OpenLP.MainWindow', '&File'))
        self.fileImportMenu.setTitle(translate('OpenLP.MainWindow', '&Import'))
        self.fileExportMenu.setTitle(translate('OpenLP.MainWindow', '&Export'))
        self.recentFilesMenu.setTitle(
            translate('OpenLP.MainWindow', '&Recent Files'))
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
        self.formattingTagItem.setText(
            translate('OpenLP.MainWindow', 'Configure &Formatting Tags...'))
        self.settingsConfigureItem.setText(
            translate('OpenLP.MainWindow', '&Configure OpenLP...'))
        self.settingsExportItem.setStatusTip(translate('OpenLP.MainWindow',
            'Export OpenLP settings to a specified *.config file'))
        self.settingsExportItem.setText(
            translate('OpenLP.MainWindow', 'Settings'))
        self.settingsImportItem.setStatusTip(translate('OpenLP.MainWindow',
            'Import OpenLP settings from a specified *.config file previously '
            'exported on this or another machine'))
        self.settingsImportItem.setText(
            translate('OpenLP.MainWindow', 'Settings'))
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
        self.lockPanel.setStatusTip(
            translate('OpenLP.MainWindow', 'Prevent the panels being moved.'))
        self.viewLivePanel.setStatusTip(translate('OpenLP.MainWindow',
            'Toggle the visibility of the live panel.'))
        self.settingsPluginListItem.setText(translate('OpenLP.MainWindow',
            '&Plugin List'))
        self.settingsPluginListItem.setStatusTip(
            translate('OpenLP.MainWindow', 'List the Plugins'))
        self.aboutItem.setText(translate('OpenLP.MainWindow', '&About'))
        self.aboutItem.setStatusTip(
            translate('OpenLP.MainWindow', 'More information about OpenLP'))
        if os.name == u'nt':
            self.offlineHelpItem.setText(
                translate('OpenLP.MainWindow', '&User Guide'))
        self.onlineHelpItem.setText(
            translate('OpenLP.MainWindow', '&Online Help'))
        self.webSiteItem.setText(
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
        self.toolsFirstTimeWizard.setText(
            translate('OpenLP.MainWindow', 'Re-run First Time Wizard'))
        self.toolsFirstTimeWizard.setStatusTip(translate('OpenLP.MainWindow',
            'Re-run the First Time Wizard, importing songs, Bibles and '
            'themes.'))
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

    def __init__(self, application):
        """
        This constructor sets up the interface, the various managers, and the
        plugins.
        """
        QtGui.QMainWindow.__init__(self)
        self.application = application
        self.clipboard = self.application.clipboard()
        self.arguments = self.application.args
        # Set up settings sections for the main application
        # (not for use by plugins)
        self.uiSettingsSection = u'user interface'
        self.generalSettingsSection = u'general'
        self.advancedSettingsSection = u'advanced'
        self.shortcutsSettingsSection = u'shortcuts'
        self.serviceManagerSettingsSection = u'servicemanager'
        self.songsSettingsSection = u'songs'
        self.themesSettingsSection = u'themes'
        self.displayTagsSection = u'displayTags'
        self.headerSection = u'SettingsImport'
        self.serviceNotSaved = False
        self.aboutForm = AboutForm(self)
        self.mediaController = MediaController(self)
        self.settingsForm = SettingsForm(self, self)
        self.formattingTagForm = FormattingTagForm(self)
        self.shortcutForm = ShortcutListForm(self)
        self.recentFiles = QtCore.QStringList()
        # Set up the path with plugins
        plugin_path = AppLocation.get_directory(AppLocation.PluginsDir)
        self.pluginManager = PluginManager(plugin_path)
        self.pluginHelpers = {}
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
        QtCore.QObject.connect(self.webSiteItem,
            QtCore.SIGNAL(u'triggered()'), self.onHelpWebSiteClicked)
        QtCore.QObject.connect(self.toolsOpenDataFolder,
            QtCore.SIGNAL(u'triggered()'), self.onToolsOpenDataFolderClicked)
        QtCore.QObject.connect(self.toolsFirstTimeWizard,
            QtCore.SIGNAL(u'triggered()'), self.onFirstTimeWizardClicked)
        QtCore.QObject.connect(self.updateThemeImages,
            QtCore.SIGNAL(u'triggered()'), self.onUpdateThemeImages)
        QtCore.QObject.connect(self.formattingTagItem,
            QtCore.SIGNAL(u'triggered()'), self.onFormattingTagItemClicked)
        QtCore.QObject.connect(self.settingsConfigureItem,
            QtCore.SIGNAL(u'triggered()'), self.onSettingsConfigureItemClicked)
        QtCore.QObject.connect(self.settingsShortcutsItem,
            QtCore.SIGNAL(u'triggered()'), self.onSettingsShortcutsItemClicked)
        QtCore.QObject.connect(self.settingsImportItem,
            QtCore.SIGNAL(u'triggered()'), self.onSettingsImportItemClicked)
        QtCore.QObject.connect(self.settingsExportItem,
            QtCore.SIGNAL(u'triggered()'), self.onSettingsExportItemClicked)
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
            QtCore.SIGNAL(u'live_display_blank_check'), self.blankCheck)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_screen_changed'), self.screenChanged)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'mainwindow_status_text'), self.showStatusMessage)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'cleanup'), self.cleanUp)
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
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'set_new_data_path'), self.setNewDataPath)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'set_copy_data'), self.setCopyData)
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
        self.pluginHelpers[u'mediacontroller'] = self.mediaController
        self.pluginManager.find_plugins(plugin_path, self.pluginHelpers)
        # hook methods have to happen after find_plugins. Find plugins needs
        # the controllers hence the hooks have moved from setupUI() to here
        # Find and insert settings tabs
        log.info(u'hook settings')
        self.pluginManager.hook_settings_tabs(self.settingsForm)
        # Find and insert media manager items
        log.info(u'hook media')
        self.pluginManager.hook_media_manager()
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
        if Settings().value(u'advanced/save current plugin',
            QtCore.QVariant(False)).toBool():
            savedPlugin = Settings().value(
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
        if self.arguments:
            args = []
            for a in self.arguments:
                args.extend([a])
            filename = args[0]
            if not isinstance(filename, unicode):
                filename = unicode(filename, sys.getfilesystemencoding())
            self.serviceManagerContents.loadFile(filename)
        elif Settings().value(
            self.generalSettingsSection + u'/auto open',
            QtCore.QVariant(False)).toBool():
            self.serviceManagerContents.loadLastFile()
        view_mode = Settings().value(u'%s/view mode' % \
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
            translate('OpenLP.MainWindow',
            'Are you sure you want to re-run the First Time Wizard?\n\n'
            'Re-running this wizard may make changes to your current '
            'OpenLP configuration and possibly add songs to your '
            'existing songs list and change your default theme.'),
            QtGui.QMessageBox.StandardButtons(
            QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No),
            QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.No:
            return
        Receiver.send_message(u'cursor_busy')
        screens = ScreenList()
        firstTime = FirstTimeForm(screens, self)
        firstTime.exec_()
        if firstTime.downloadCancelled:
            return
        self.firstTime()
        for plugin in self.pluginManager.plugins:
            self.activePlugin = plugin
            oldStatus = self.activePlugin.status
            self.activePlugin.setStatus()
            if oldStatus != self.activePlugin.status:
                if self.activePlugin.status == PluginStatus.Active:
                    self.activePlugin.toggleStatus(PluginStatus.Active)
                    self.activePlugin.appStartup()
                else:
                    self.activePlugin.toggleStatus(PluginStatus.Inactive)
        self.themeManagerContents.configUpdated()
        self.themeManagerContents.loadThemes(True)
        Receiver.send_message(u'theme_update_global',
            self.themeManagerContents.global_theme)
        # Check if any Bibles downloaded.  If there are, they will be
        # processed.
        Receiver.send_message(u'bibles_load_list', True)

    def blankCheck(self):
        """
        Check and display message if screen blank on setup.
        """
        settings = Settings()
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
        self.themeManagerContents.updatePreviewImages()

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
        answer = QtGui.QMessageBox.critical(self,
            translate('OpenLP.MainWindow', 'Import settings?'),
            translate('OpenLP.MainWindow',
            'Are you sure you want to import settings?\n\n'
            'Importing settings will make permanent changes to your current '
            'OpenLP configuration.\n\n'
            'Importing incorrect settings may cause erratic behaviour or '
            'OpenLP to terminate abnormally.'),
            QtGui.QMessageBox.StandardButtons(
            QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No),
            QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.No:
            return
        import_file_name = unicode(QtGui.QFileDialog.getOpenFileName(self,
                translate('OpenLP.MainWindow', 'Open File'),
                '',
                translate('OpenLP.MainWindow',
                'OpenLP Export Settings Files (*.conf)')))
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
        setting_sections.extend([self.displayTagsSection])
        setting_sections.extend([self.headerSection])
        setting_sections.extend([u'crashreport'])
        # Add plugin sections.
        for plugin in self.pluginManager.plugins:
            setting_sections.extend([plugin.name])
        settings = Settings()
        import_settings = Settings(import_file_name,
            Settings.IniFormat)
        import_keys = import_settings.allKeys()
        for section_key in import_keys:
            # We need to handle the really bad files.
            try:
                section, key = section_key.split(u'/')
            except ValueError:
                section = u'unknown'
                key = u''
            # Switch General back to lowercase.
            if section == u'General':
                section = u'general'
                section_key = section + "/" + key
            # Make sure it's a valid section for us.
            if not section in setting_sections:
                QtGui.QMessageBox.critical(self,
                    translate('OpenLP.MainWindow', 'Import settings'),
                    translate('OpenLP.MainWindow',
                    'The file you selected does appear to be a valid OpenLP '
                    'settings file.\n\n'
                    'Section [%s] is not valid \n\n'
                    'Processing has terminated and no changed have been made.'
                    ).replace('%s', section),
                    QtGui.QMessageBox.StandardButtons(
                    QtGui.QMessageBox.Ok))
                return
        # We have a good file, import it.
        for section_key in import_keys:
            value = import_settings.value(section_key)
            settings.setValue(u'%s' % (section_key),
                QtCore.QVariant(value))
        now = datetime.now()
        settings.beginGroup(self.headerSection)
        settings.setValue(u'file_imported', QtCore.QVariant(import_file_name))
        settings.setValue(u'file_date_imported',
            now.strftime("%Y-%m-%d %H:%M"))
        settings.endGroup()
        settings.sync()
        # We must do an immediate restart or current configuration will
        # overwrite what was just imported when application terminates
        # normally.   We need to exit without saving configuration.
        QtGui.QMessageBox.information(self,
            translate('OpenLP.MainWindow', 'Import settings'),
            translate('OpenLP.MainWindow',
            'OpenLP will now close.  Imported settings will '
            'be applied the next time you start OpenLP.'),
            QtGui.QMessageBox.StandardButtons(
            QtGui.QMessageBox.Ok))
        self.settingsImported = True
        self.cleanUp()
        QtCore.QCoreApplication.exit()

    def onSettingsExportItemClicked(self):
        """
        Export settings to a .conf file in INI format
        """
        export_file_name = unicode(QtGui.QFileDialog.getSaveFileName(self,
            translate('OpenLP.MainWindow', 'Export Settings File'), '',
            translate('OpenLP.MainWindow',
                'OpenLP Export Settings File (*.conf)')))
        if not export_file_name:
            return
            # Make sure it's a .conf file.
        if not export_file_name.endswith(u'conf'):
            export_file_name = export_file_name + u'.conf'
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
        for plugin in self.pluginManager.plugins:
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
        export_settings = Settings(temp_file,
            Settings.IniFormat)
        # Add a header section.
        # This is to insure it's our conf file for import.
        now = datetime.now()
        application_version = get_application_version()
        # Write INI format using Qsettings.
        # Write our header.
        export_settings.beginGroup(self.headerSection)
        export_settings.setValue(u'Make_Changes', u'At_Own_RISK')
        export_settings.setValue(u'type', u'OpenLP_settings_export')
        export_settings.setValue(u'file_date_created',
            now.strftime("%Y-%m-%d %H:%M"))
        export_settings.setValue(u'version', application_version[u'full'])
        export_settings.endGroup()
        # Write all the sections and keys.
        for section_key in keys:
            key_value = settings.value(section_key)
            export_settings.setValue(section_key, key_value)
        export_settings.sync()
        # Temp CONF file has been written.  Blanks in keys are now '%20'.
        # Read the  temp file and output the user's CONF file with blanks to
        # make it more readable.
        temp_conf = open(temp_file, u'r')
        export_conf = open(export_file_name,  u'w')
        for file_record in temp_conf:
            # Get rid of any invalid entries.
            if file_record.find(u'@Invalid()') == -1:
                file_record = file_record.replace(u'%20',  u' ')
                export_conf.write(file_record)
        temp_conf.close()
        export_conf.close()
        os.remove(temp_file)
        return

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
        self.imageManager.updateDisplay()
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
        # The MainApplication did not even enter the event loop (this happens
        # when OpenLP is not fully loaded). Just ignore the event.
        if not self.application.eventLoopIsActive:
            event.ignore()
            return
        # If we just did a settings import, close without saving changes.
        if self.settingsImported:
            self.cleanUp(False)
            event.accept()
        if self.serviceManagerContents.isModified():
            ret = self.serviceManagerContents.saveModifiedService()
            if ret == QtGui.QMessageBox.Save:
                if self.serviceManagerContents.decideSaveMethod():
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
            if Settings().value(u'advanced/enable exit confirmation',
                QtCore.QVariant(True)).toBool():
                ret = QtGui.QMessageBox.question(self,
                    translate('OpenLP.MainWindow', 'Close OpenLP'),
                    translate('OpenLP.MainWindow',
                        'Are you sure you want to close OpenLP?'),
                    QtGui.QMessageBox.StandardButtons(
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
                    QtGui.QMessageBox.Yes)
                if ret == QtGui.QMessageBox.Yes:
                    self.cleanUp()
                    event.accept()
                else:
                    event.ignore()
            else:
                self.cleanUp()
                event.accept()

    def cleanUp(self, save_settings=True):
        """
        Runs all the cleanup code before OpenLP shuts down.

        ``save_settings``
            Switch to prevent saving settings. Defaults to **True**.
        """
        self.imageManager.stopManager = True
        while self.imageManager.imageThread.isRunning():
            time.sleep(0.1)
        # Clean temporary files used by services
        self.serviceManagerContents.cleanUp()
        if save_settings:
            if Settings().value(u'advanced/save current plugin',
                QtCore.QVariant(False)).toBool():
                Settings().setValue(u'advanced/current media plugin',
                    QtCore.QVariant(self.mediaToolBox.currentIndex()))
        # Call the cleanup method to shutdown plugins.
        log.info(u'cleanup plugins')
        self.pluginManager.finalise_plugins()
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
        Settings().setValue(u'user interface/preview panel',
            QtCore.QVariant(visible))
        self.viewPreviewPanel.setChecked(visible)

    def setLockPanel(self, lock):
        """
        Sets the ability to stop the toolbars being changed.
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
        Settings().setValue(u'user interface/lock panel',
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
        Settings().setValue(u'user interface/live panel',
            QtCore.QVariant(visible))
        self.viewLivePanel.setChecked(visible)

    def loadSettings(self):
        """
        Load the main window settings.
        """
        log.debug(u'Loading QSettings')
       # Migrate Wrap Settings to Slide Limits Settings
        if Settings().contains(self.generalSettingsSection +
            u'/enable slide loop'):
            if Settings().value(self.generalSettingsSection +
                u'/enable slide loop', QtCore.QVariant(True)).toBool():
                Settings().setValue(self.advancedSettingsSection +
                    u'/slide limits', QtCore.QVariant(SlideLimits.Wrap))
            else:
                Settings().setValue(self.advancedSettingsSection +
                    u'/slide limits', QtCore.QVariant(SlideLimits.End))
            Settings().remove(self.generalSettingsSection +
                u'/enable slide loop')
            Receiver.send_message(u'slidecontroller_update_slide_limits')
        settings = Settings()
        # Remove obsolete entries.
        settings.remove(u'custom slide')
        settings.remove(u'service')
        settings.beginGroup(self.generalSettingsSection)
        self.recentFiles = settings.value(u'recent files').toStringList()
        settings.endGroup()
        settings.beginGroup(self.uiSettingsSection)
        self.move(settings.value(u'main window position',
            QtCore.QVariant(QtCore.QPoint(0, 0))).toPoint())
        self.restoreGeometry(
            settings.value(u'main window geometry').toByteArray())
        self.restoreState(settings.value(u'main window state').toByteArray())
        self.liveController.splitter.restoreState(
            settings.value(u'live splitter geometry').toByteArray())
        self.previewController.splitter.restoreState(
            settings.value(u'preview splitter geometry').toByteArray())
        self.controlSplitter.restoreState(
            settings.value(u'mainwindow splitter geometry').toByteArray())
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
        settings.setValue(u'live splitter geometry',
            QtCore.QVariant(self.liveController.splitter.saveState()))
        settings.setValue(u'preview splitter geometry',
            QtCore.QVariant(self.previewController.splitter.saveState()))
        settings.setValue(u'mainwindow splitter geometry',
            QtCore.QVariant(self.controlSplitter.saveState()))
        settings.endGroup()

    def updateRecentFilesMenu(self):
        """
        Updates the recent file menu with the latest list of service files
        accessed.
        """
        recentFileCount = Settings().value(
            u'advanced/recent file count', QtCore.QVariant(4)).toInt()[0]
        existingRecentFiles = [recentFile for recentFile in self.recentFiles
            if os.path.isfile(unicode(recentFile))]
        recentFilesToDisplay = existingRecentFiles[0:recentFileCount]
        self.recentFilesMenu.clear()
        for fileId, filename in enumerate(recentFilesToDisplay):
            log.debug('Recent file name: %s', filename)
            action = create_action(self, u'',
                text=u'&%d %s' % (fileId + 1, os.path.splitext(os.path.basename(
                unicode(filename)))[0]), data=filename,
                triggers=self.serviceManagerContents.onRecentServiceClicked)
            self.recentFilesMenu.addAction(action)
        clearRecentFilesAction = create_action(self, u'',
            text=translate('OpenLP.MainWindow', 'Clear List',
            'Clear List of recent files'),
            statustip=translate('OpenLP.MainWindow',
            'Clear the list of recent files.'),
            enabled=not self.recentFiles.isEmpty(),
            triggers=self.recentFiles.clear)
        add_actions(self.recentFilesMenu, (None, clearRecentFilesAction))
        clearRecentFilesAction.setEnabled(not self.recentFiles.isEmpty())

    def addRecentFile(self, filename):
        """
        Adds a service to the list of recently used files.

        ``filename``
            The service filename to add
        """
        # The maxRecentFiles value does not have an interface and so never gets
        # actually stored in the settings therefore the default value of 20 will
        # always be used.
        maxRecentFiles = Settings().value(u'advanced/max recent files',
            QtCore.QVariant(20)).toInt()[0]
        if filename:
            # Add some cleanup to reduce duplication in the recent file list
            filename = os.path.abspath(filename)
            # abspath() only capitalises the drive letter if it wasn't provided
            # in the given filename which then causes duplication.
            if filename[1:3] == ':\\':
                filename = filename[0].upper() + filename[1:]
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

    def setNewDataPath(self, new_data_path):
        self.newDataPath = new_data_path

    def setCopyData(self, copy_data):
        self.copyData = copy_data

    def changeDataDirectory(self):
        log.info(u'Changing data path to %s' % self.newDataPath )
        old_data_path = unicode(AppLocation.get_data_path())
        # Copy OpenLP data to new location if requested.
        if self.copyData:
            log.info(u'Copying data to new path')
            try:
                Receiver.send_message(u'openlp_process_events')
                Receiver.send_message(u'cursor_busy')
                self.showStatusMessage(
                    translate('OpenLP.MainWindow',
                    'Copying OpenLP data to new data directory location - %s '
                    '- Please wait for copy to finish'
                    ).replace('%s', self.newDataPath))
                dir_util.copy_tree(old_data_path, self.newDataPath)
                log.info(u'Copy sucessful')
            except (IOError, os.error, DistutilsFileError),  why:
                Receiver.send_message(u'cursor_normal')
                log.exception(u'Data copy failed %s' % unicode(why))
                QtGui.QMessageBox.critical(self,
                    translate('OpenLP.MainWindow', 'New Data Directory Error'),
                    translate('OpenLP.MainWindow',
                    'OpenLP Data directory copy failed\n\n%s'
                    ).replace('%s', unicode(why)),
                QtGui.QMessageBox.StandardButtons(
                QtGui.QMessageBox.Ok))
                return False
        else:
            log.info(u'No data copy requested')
        # Change the location of data directory in config file.
        settings = QtCore.QSettings()
        settings.setValue(u'advanced/data path', self.newDataPath)
        # Check if the new data path is our default.
        if self.newDataPath == AppLocation.get_directory(AppLocation.DataDir):
            settings.remove(u'advanced/data path')
