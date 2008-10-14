# -*- coding: utf-8 -*-

"""
This is the main window for openlp.org 2.0
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Ui_MainWindow(object):
    def setupDockWidget(self, window, name, dock_area, caption = None):
        dock = QDockWidget()
        dock.setObjectName(name)
        dock.setFeatures(\
            QDockWidget.DockWidgetFeatures(QDockWidget.AllDockWidgetFeatures))
        if caption is not None:
            dock.setWindowTitle(caption)
        window.addDockWidget(dock_area, dock)
        dock.show()
        return dock

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QSize(QRect(0,0,800,600).size()).expandedTo(MainWindow.minimumSizeHint()))

        sizePolicy = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setGeometry(QRect(0,30,800,547))

        sizePolicy = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        self.MediaManagerDock = self.setupDockWidget(MainWindow, "MediaManagerDock",
                                                     Qt.LeftDockWidgetArea, "Media Manager")
        self.MediaManagerContents = QWidget(self.MediaManagerDock)
        self.MediaManagerContents.setGeometry(QRect(0,21,790,88))
        self.MediaManagerContents.setObjectName("MediaManagerContents")
        self.MediaManagerLayout = QHBoxLayout(self.MediaManagerContents)
        self.MediaManagerLayout.setMargin(0)
        self.MediaManagerLayout.setObjectName("MediaManagerLayout")

        self.MediaManagerTabs = QTabWidget(self.MediaManagerContents)
        self.MediaManagerTabs.setObjectName("MediaManagerTabs")

        self.SongsTab = QWidget()
        self.SongsTab.setGeometry(QRect(0,0,786,60))
        self.SongsTab.setObjectName("SongsTab")
        self.MediaManagerTabs.addTab(self.SongsTab, "Songs")

        self.BiblesTab = QWidget()
        self.BiblesTab.setGeometry(QRect(0,0,786,60))
        self.BiblesTab.setObjectName("BiblesTab")
        self.MediaManagerTabs.addTab(self.BiblesTab, "Bibles")

        self.MediaManagerDock.setWidget(self.MediaManagerContents)
        self.MediaManagerLayout.addWidget(self.MediaManagerTabs)

        self.OrderOfServiceDock = self.setupDockWidget(MainWindow, "ThemeManagerDock",
                                                       Qt.RightDockWidgetArea, "Theme Manager")

        self.OrderOfServiceContents = QWidget(self.OrderOfServiceDock)
        self.OrderOfServiceContents.setGeometry(QRect(0,21,790,192))
        self.OrderOfServiceContents.setObjectName("OrderOfServiceContents")

        self.OrderOfServiceLayout = QHBoxLayout(self.OrderOfServiceContents)
        self.OrderOfServiceLayout.setMargin(0)
        self.OrderOfServiceLayout.setObjectName("OrderOfServiceLayout")

        self.OrderOfServiceListView = QListView(self.OrderOfServiceContents)
        self.OrderOfServiceListView.setObjectName("OrderOfServiceListView")
        self.OrderOfServiceLayout.addWidget(self.OrderOfServiceListView)
        self.OrderOfServiceDock.setWidget(self.OrderOfServiceContents)

        self.ThemeManagerDock = self.setupDockWidget(MainWindow, "ThemeManagerDock",
                                                     Qt.RightDockWidgetArea, "Theme Manager")

        self.ThemeManagerContents = QWidget(self.ThemeManagerDock)
        self.ThemeManagerContents.setGeometry(QRect(0,21,790,192))
        self.ThemeManagerContents.setObjectName("ThemeManagerContents")

        self.ThemeManagerLayout = QVBoxLayout(self.ThemeManagerContents)
        self.ThemeManagerLayout.setMargin(0)
        self.ThemeManagerLayout.setObjectName("ThemeManagerLayout")

        self.ThemeManagerListView = QListView(self.ThemeManagerContents)
        self.ThemeManagerListView.setObjectName("ThemeManagerListView")
        self.ThemeManagerLayout.addWidget(self.ThemeManagerListView)
        self.ThemeManagerDock.setWidget(self.ThemeManagerContents)

        MainWindow.setCentralWidget(self.centralwidget)

        # Menu bar at the top of the application
        self.MenuBar = QMenuBar(MainWindow)
        self.MenuBar.setGeometry(QRect(0,0,800,30))
        self.MenuBar.setObjectName("MenuBar")
        MainWindow.setMenuBar(self.MenuBar)

        # The File menu
        self.FileMenu = QMenu(self.MenuBar)
        self.FileMenu.setObjectName("FileMenu")
        # The Import submenu
        self.FileImportMenu = QMenu(self.FileMenu)
        self.FileImportMenu.setObjectName("FileImportMenu")
        # The Export submenu
        self.FileExportMenu = QMenu(self.FileMenu)
        self.FileExportMenu.setObjectName("FileExportMenu")

        # The Options menu
        self.OptionsMenu = QMenu(self.MenuBar)
        self.OptionsMenu.setObjectName("OptionsMenu")
        # The View submenu
        self.OptionsViewMenu = QMenu(self.OptionsMenu)
        self.OptionsViewMenu.setObjectName("OptionsViewMenu")

        # The Tools menu
        self.ToolsMenu = QMenu(self.MenuBar)
        self.ToolsMenu.setObjectName("ToolsMenu")

        # The Help menu
        self.HelpMenu = QMenu(self.MenuBar)
        self.HelpMenu.setObjectName("HelpMenu")

        # The status bar
        self.StatusBar = QStatusBar(MainWindow)
        self.StatusBar.setGeometry(QRect(0,577,800,23))
        self.StatusBar.setObjectName("StatusBar")
        MainWindow.setStatusBar(self.StatusBar)

        self.FileNewAction = QAction(MainWindow)
        self.FileNewAction.setObjectName("FileNewAction")

        self.FileOpenAction = QAction(MainWindow)
        self.FileOpenAction.setObjectName("FileOpenAction")

        self.FileSaveAction = QAction(MainWindow)
        self.FileSaveAction.setObjectName("FileSaveAction")

        self.FileSaveAsAction = QAction(MainWindow)
        self.FileSaveAsAction.setObjectName("FileSaveAsAction")

        self.FileExitAction = QAction(MainWindow)
        self.FileExitAction.setObjectName("FileExitAction")

        self.FileImportSongAction = QAction(MainWindow)
        self.FileImportSongAction.setObjectName("FileImportSongAction")

        self.FileImportBibleAction = QAction(MainWindow)
        self.FileImportBibleAction.setObjectName("FileImportBibleAction")

        self.FileImportThemeAction = QAction(MainWindow)
        self.FileImportThemeAction.setObjectName("FileImportThemeAction")

        self.FileImportLanguageAction = QAction(MainWindow)
        self.FileImportLanguageAction.setObjectName("FileImportLanguageAction")

        self.FileExportSongAction = QAction(MainWindow)
        self.FileExportSongAction.setObjectName("FileExportSongAction")

        self.FileExportBibleAction = QAction(MainWindow)
        self.FileExportBibleAction.setObjectName("FileExportBibleAction")

        self.FileExportThemeAction = QAction(MainWindow)
        self.FileExportThemeAction.setObjectName("FileExportThemeAction")

        self.FileExportLanguageAction = QAction(MainWindow)
        self.FileExportLanguageAction.setObjectName("FileExportLanguageAction")

        self.OptionsLanguageAction = QAction(MainWindow)
        self.OptionsLanguageAction.setObjectName("OptionsLanguageAction")

        self.OptionsLookFeelAction = QAction(MainWindow)
        self.OptionsLookFeelAction.setObjectName("OptionsLookFeelAction")

        self.OptionsSettingsAction = QAction(MainWindow)
        self.OptionsSettingsAction.setObjectName("OptionsSettingsAction")

        self.OptionsViewMediaManagerAction = QAction(MainWindow)
        self.OptionsViewMediaManagerAction.setObjectName("OptionsViewMediaManagerAction")

        self.OptionsViewThemeManagerAction = QAction(MainWindow)
        self.OptionsViewThemeManagerAction.setObjectName("OptionsViewThemeManagerAction")

        self.OptionsViewOrderOfServiceAction = QAction(MainWindow)
        self.OptionsViewOrderOfServiceAction.setObjectName("OptionsViewOrderOfServiceAction")

        self.ToolsAlertAction = QAction(MainWindow)
        self.ToolsAlertAction.setObjectName("ToolsAlertAction")

        self.HelpUserGuideAction = QAction(MainWindow)
        self.HelpUserGuideAction.setObjectName("HelpUserGuideAction")

        self.HelpAboutAction = QAction(MainWindow)
        self.HelpAboutAction.setObjectName("HelpAboutAction")

        self.HelpOnlineHelpAction = QAction(MainWindow)
        self.HelpOnlineHelpAction.setObjectName("HelpOnlineHelpAction")

        self.HelpWebSiteAction = QAction(MainWindow)
        self.HelpWebSiteAction.setObjectName("HelpWebSiteAction")

        self.FileImportMenu.addAction(self.FileImportSongAction)
        self.FileImportMenu.addAction(self.FileImportBibleAction)
        self.FileImportMenu.addAction(self.FileImportThemeAction)
        self.FileImportMenu.addAction(self.FileImportLanguageAction)

        self.FileExportMenu.addAction(self.FileExportSongAction)
        self.FileExportMenu.addAction(self.FileExportBibleAction)
        self.FileExportMenu.addAction(self.FileExportThemeAction)
        self.FileExportMenu.addAction(self.FileExportLanguageAction)

        self.FileMenu.addAction(self.FileNewAction)
        self.FileMenu.addAction(self.FileOpenAction)
        self.FileMenu.addAction(self.FileSaveAction)
        self.FileMenu.addAction(self.FileSaveAsAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.FileImportMenu.menuAction())
        self.FileMenu.addAction(self.FileExportMenu.menuAction())
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.FileExitAction)

        self.OptionsViewMenu.addAction(self.OptionsViewMediaManagerAction)
        self.OptionsViewMenu.addAction(self.OptionsViewThemeManagerAction)
        self.OptionsViewMenu.addAction(self.OptionsViewOrderOfServiceAction)

        self.OptionsMenu.addAction(self.OptionsLanguageAction)
        self.OptionsMenu.addAction(self.OptionsViewMenu.menuAction())
        self.OptionsMenu.addSeparator()
        self.OptionsMenu.addAction(self.OptionsSettingsAction)

        self.ToolsMenu.addAction(self.ToolsAlertAction)

        self.HelpMenu.addAction(self.HelpUserGuideAction)
        self.HelpMenu.addAction(self.HelpOnlineHelpAction)
        self.HelpMenu.addSeparator()
        self.HelpMenu.addAction(self.HelpWebSiteAction)
        self.HelpMenu.addAction(self.HelpAboutAction)

        self.MenuBar.addAction(self.FileMenu.menuAction())
        self.MenuBar.addAction(self.OptionsMenu.menuAction())
        self.MenuBar.addAction(self.ToolsMenu.menuAction())
        self.MenuBar.addAction(self.HelpMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.MediaManagerTabs.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QApplication.translate("MainWindow", "openlp.org 2.0", None, QApplication.UnicodeUTF8))
        self.MediaManagerDock.setWindowTitle(QApplication.translate("MainWindow", "Media Manager", None, QApplication.UnicodeUTF8))
        self.MediaManagerTabs.setTabText(self.MediaManagerTabs.indexOf(self.SongsTab), QApplication.translate("MainWindow", "Songs", None, QApplication.UnicodeUTF8))
        self.MediaManagerTabs.setTabText(self.MediaManagerTabs.indexOf(self.BiblesTab), QApplication.translate("MainWindow", "Bibles", None, QApplication.UnicodeUTF8))
        self.OrderOfServiceDock.setWindowTitle(QApplication.translate("MainWindow", "Order of Service", None, QApplication.UnicodeUTF8))
        self.FileMenu.setTitle(QApplication.translate("MainWindow", "&File", None, QApplication.UnicodeUTF8))
        self.FileImportMenu.setTitle(QApplication.translate("MainWindow", "&Import", None, QApplication.UnicodeUTF8))
        self.FileExportMenu.setTitle(QApplication.translate("MainWindow", "&Export", None, QApplication.UnicodeUTF8))
        self.OptionsMenu.setTitle(QApplication.translate("MainWindow", "&Options", None, QApplication.UnicodeUTF8))
        self.OptionsViewMenu.setTitle(QApplication.translate("MainWindow", "&View", None, QApplication.UnicodeUTF8))
        self.ToolsMenu.setTitle(QApplication.translate("MainWindow", "&Tools", None, QApplication.UnicodeUTF8))
        self.HelpMenu.setTitle(QApplication.translate("MainWindow", "&Help", None, QApplication.UnicodeUTF8))
        self.FileNewAction.setText(QApplication.translate("MainWindow", "&New", None, QApplication.UnicodeUTF8))
        self.FileOpenAction.setText(QApplication.translate("MainWindow", "&Open", None, QApplication.UnicodeUTF8))
        self.FileSaveAction.setText(QApplication.translate("MainWindow", "&Save", None, QApplication.UnicodeUTF8))
        self.FileSaveAsAction.setText(QApplication.translate("MainWindow", "Save &As...", None, QApplication.UnicodeUTF8))
        self.FileExitAction.setText(QApplication.translate("MainWindow", "E&xit", None, QApplication.UnicodeUTF8))
        self.FileImportSongAction.setText(QApplication.translate("MainWindow", "&Song", None, QApplication.UnicodeUTF8))
        self.FileImportBibleAction.setText(QApplication.translate("MainWindow", "&Bible", None, QApplication.UnicodeUTF8))
        self.FileImportThemeAction.setText(QApplication.translate("MainWindow", "&Theme", None, QApplication.UnicodeUTF8))
        self.FileImportLanguageAction.setText(QApplication.translate("MainWindow", "&Language", None, QApplication.UnicodeUTF8))
        self.FileExportSongAction.setText(QApplication.translate("MainWindow", "&Song", None, QApplication.UnicodeUTF8))
        self.FileExportBibleAction.setText(QApplication.translate("MainWindow", "&Bible", None, QApplication.UnicodeUTF8))
        self.FileExportThemeAction.setText(QApplication.translate("MainWindow", "&Theme", None, QApplication.UnicodeUTF8))
        self.FileExportLanguageAction.setText(QApplication.translate("MainWindow", "&Language", None, QApplication.UnicodeUTF8))
        self.OptionsLanguageAction.setText(QApplication.translate("MainWindow", "&Language", None, QApplication.UnicodeUTF8))
        self.OptionsLookFeelAction.setText(QApplication.translate("MainWindow", "Look && &Feel", None, QApplication.UnicodeUTF8))
        self.OptionsSettingsAction.setText(QApplication.translate("MainWindow", "&Settings", None, QApplication.UnicodeUTF8))
        self.OptionsViewMediaManagerAction.setText(QApplication.translate("MainWindow", "&Media Manager", None, QApplication.UnicodeUTF8))
        self.OptionsViewThemeManagerAction.setText(QApplication.translate("MainWindow", "&Theme Manager", None, QApplication.UnicodeUTF8))
        self.OptionsViewOrderOfServiceAction.setText(QApplication.translate("MainWindow", "&Order of Service", None, QApplication.UnicodeUTF8))
        self.ToolsAlertAction.setText(QApplication.translate("MainWindow", "&Alert", None, QApplication.UnicodeUTF8))
        self.HelpUserGuideAction.setText(QApplication.translate("MainWindow", "&User Guide", None, QApplication.UnicodeUTF8))
        self.HelpAboutAction.setText(QApplication.translate("MainWindow", "&About", None, QApplication.UnicodeUTF8))
        self.HelpOnlineHelpAction.setText(QApplication.translate("MainWindow", "&Online Help", None, QApplication.UnicodeUTF8))
        self.HelpWebSiteAction.setText(QApplication.translate("MainWindow", "&Web Site", None, QApplication.UnicodeUTF8))

    def on_FileExitAction_triggered(self):
        sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
