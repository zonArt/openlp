# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
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
"""
Provides the generic functions for interfacing plugins with the Media Manager.
"""
import logging
import os
import re

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsManager, OpenLPToolbar, ServiceItem, \
    StringContent, build_icon, translate, Receiver, ListWidgetWithDnD, Settings
from openlp.core.lib.searchedit import SearchEdit
from openlp.core.lib.ui import UiStrings, create_widget_action, \
    critical_error_message_box

log = logging.getLogger(__name__)

class MediaManagerItem(QtGui.QWidget):
    """
    MediaManagerItem is a helper widget for plugins.

    None of the following *need* to be used, feel free to override
    them completely in your plugin's implementation. Alternatively,
    call them from your plugin before or after you've done extra
    things that you need to.

    **Constructor Parameters**

    ``parent``
        The parent widget. Usually this will be the *Media Manager*
        itself. This needs to be a class descended from ``QWidget``.

    ``plugin``
        The plugin widget. Usually this will be the *Plugin*
        itself. This needs to be a class descended from ``Plugin``.

    ``icon``
        Either a ``QIcon``, a resource path, or a file name. This is
        the icon which is displayed in the *Media Manager*.

    **Member Variables**

    When creating a descendant class from this class for your plugin,
    the following member variables should be set.

     ``self.onNewPrompt``

        Defaults to *'Select Image(s)'*.

     ``self.onNewFileMasks``
        Defaults to *'Images (*.jpg *jpeg *.gif *.png *.bmp)'*. This
        assumes that the new action is to load a file. If not, you
        need to override the ``OnNew`` method.

     ``self.PreviewFunction``
        This must be a method which returns a QImage to represent the
        item (usually a preview). No scaling is required, that is
        performed automatically by OpenLP when necessary. If this
        method is not defined, a default will be used (treat the
        filename as an image).
    """
    log.info(u'Media Item loaded')

    def __init__(self, parent=None, plugin=None, icon=None):
        """
        Constructor to create the media manager item.
        """
        QtGui.QWidget.__init__(self)
        self.hide()
        self.whitespace = re.compile(r'[\W_]+', re.UNICODE)
        self.plugin = plugin
        visible_title = self.plugin.getString(StringContent.VisibleName)
        self.title = unicode(visible_title[u'title'])
        self.settingsSection = self.plugin.name
        self.icon = None
        if icon:
            self.icon = build_icon(icon)
        self.toolbar = None
        self.remoteTriggered = None
        self.singleServiceItem = True
        self.quickPreviewAllowed = False
        self.hasSearch = False
        self.pageLayout = QtGui.QVBoxLayout(self)
        self.pageLayout.setSpacing(0)
        self.pageLayout.setMargin(0)
        self.requiredIcons()
        self.setupUi()
        self.retranslateUi()
        self.autoSelectId = -1
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_service_load' % self.plugin.name),
            self.serviceLoad)

    def requiredIcons(self):
        """
        This method is called to define the icons for the plugin.
        It provides a default set and the plugin is able to override
        the if required.
        """
        self.hasImportIcon = False
        self.hasNewIcon = True
        self.hasEditIcon = True
        self.hasFileIcon = False
        self.hasDeleteIcon = True
        self.addToServiceItem = False

    def retranslateUi(self):
        """
        This method is called automatically to provide OpenLP with the
        opportunity to translate the ``MediaManagerItem`` to another
        language.
        """
        pass

    def addToolbar(self):
        """
        A method to help developers easily add a toolbar to the media
        manager item.
        """
        if self.toolbar is None:
            self.toolbar = OpenLPToolbar(self)
            self.pageLayout.addWidget(self.toolbar)

    def setupUi(self):
        """
        This method sets up the interface on the button. Plugin
        developers use this to add and create toolbars, and the rest
        of the interface of the media manager item.
        """
        # Add a toolbar
        self.addToolbar()
        # Allow the plugin to define buttons at start of bar
        self.addStartHeaderBar()
        # Add the middle of the tool bar (pre defined)
        self.addMiddleHeaderBar()
        # Allow the plugin to define buttons at end of bar
        self.addEndHeaderBar()
        # Add the list view
        self.addListViewToToolBar()

    def addMiddleHeaderBar(self):
        """
        Create buttons for the media item toolbar
        """
        toolbar_actions = []
        ## Import Button ##
        if self.hasImportIcon:
            toolbar_actions.append([u'Import', StringContent.Import,
            u':/general/general_import.png', self.onImportClick])
        ## Load Button ##
        if self.hasFileIcon:
            toolbar_actions.append([u'Load', StringContent.Load,
                u':/general/general_open.png', self.onFileClick])
        ## New Button ##
        if self.hasNewIcon:
            toolbar_actions.append([u'New', StringContent.New,
                u':/general/general_new.png', self.onNewClick])
        ## Edit Button ##
        if self.hasEditIcon:
            toolbar_actions.append([u'Edit', StringContent.Edit,
                u':/general/general_edit.png', self.onEditClick])
        ## Delete Button ##
        if self.hasDeleteIcon:
            toolbar_actions.append([u'Delete', StringContent.Delete,
                u':/general/general_delete.png', self.onDeleteClick])
        ## Preview ##
        toolbar_actions.append([u'Preview', StringContent.Preview,
            u':/general/general_preview.png', self.onPreviewClick])
        ## Live Button ##
        toolbar_actions.append([u'Live', StringContent.Live,
            u':/general/general_live.png', self.onLiveClick])
        ## Add to service Button ##
        toolbar_actions.append([u'Service', StringContent.Service,
            u':/general/general_add.png', self.onAddClick])
        for action in toolbar_actions:
            if action[0] == StringContent.Preview:
                self.toolbar.addSeparator()
            self.toolbar.addToolbarAction(
                u'%s%sAction' % (self.plugin.name, action[0]),
                text=self.plugin.getString(action[1])[u'title'], icon=action[2],
                tooltip=self.plugin.getString(action[1])[u'tooltip'],
                triggers=action[3])

    def addListViewToToolBar(self):
        """
        Creates the main widget for listing items the media item is tracking
        """
        # Add the List widget
        self.listView = ListWidgetWithDnD(self, self.plugin.name)
        self.listView.setSpacing(1)
        self.listView.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.listView.setAlternatingRowColors(True)
        self.listView.setObjectName(u'%sListView' % self.plugin.name)
        # Add to pageLayout
        self.pageLayout.addWidget(self.listView)
        # define and add the context menu
        self.listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        if self.hasEditIcon:
            create_widget_action(self.listView,
                text=self.plugin.getString(StringContent.Edit)[u'title'],
                icon=u':/general/general_edit.png',
                triggers=self.onEditClick)
            create_widget_action(self.listView, separator=True)
        if self.hasDeleteIcon:
            create_widget_action(self.listView,
                text=self.plugin.getString(StringContent.Delete)[u'title'],
                icon=u':/general/general_delete.png',
                shortcuts=[QtCore.Qt.Key_Delete], triggers=self.onDeleteClick)
            create_widget_action(self.listView, separator=True)
        create_widget_action(self.listView,
            text=self.plugin.getString(StringContent.Preview)[u'title'],
            icon=u':/general/general_preview.png',
            shortcuts=[QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return],
            triggers=self.onPreviewClick)
        create_widget_action(self.listView,
            text=self.plugin.getString(StringContent.Live)[u'title'],
            icon=u':/general/general_live.png',
            shortcuts=[QtCore.Qt.ShiftModifier | QtCore.Qt.Key_Enter,
            QtCore.Qt.ShiftModifier | QtCore.Qt.Key_Return],
            triggers=self.onLiveClick)
        create_widget_action(self.listView,
            text=self.plugin.getString(StringContent.Service)[u'title'],
            icon=u':/general/general_add.png',
            shortcuts=[QtCore.Qt.Key_Plus, QtCore.Qt.Key_Equal],
            triggers=self.onAddClick)
        if self.addToServiceItem:
            create_widget_action(self.listView, text=translate(
                'OpenLP.MediaManagerItem', '&Add to selected Service Item'),
                icon=u':/general/general_add.png', triggers=self.onAddEditClick)
        self.addCustomContextActions()
        # Create the context menu and add all actions from the listView.
        self.menu = QtGui.QMenu()
        self.menu.addActions(self.listView.actions())
        QtCore.QObject.connect(self.listView,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
            self.onDoubleClicked)
        QtCore.QObject.connect(self.listView,
            QtCore.SIGNAL(u'itemSelectionChanged()'),
            self.onSelectionChange)
        QtCore.QObject.connect(self.listView,
            QtCore.SIGNAL('customContextMenuRequested(QPoint)'),
            self.contextMenu)

    def addSearchToToolBar(self):
        """
        Creates a search field with button and related signal handling.
        """
        self.searchWidget = QtGui.QWidget(self)
        self.searchWidget.setObjectName(u'searchWidget')
        self.searchLayout = QtGui.QVBoxLayout(self.searchWidget)
        self.searchLayout.setObjectName(u'searchLayout')
        self.searchTextLayout = QtGui.QFormLayout()
        self.searchTextLayout.setObjectName(u'searchTextLayout')
        self.searchTextLabel = QtGui.QLabel(self.searchWidget)
        self.searchTextLabel.setObjectName(u'searchTextLabel')
        self.searchTextEdit = SearchEdit(self.searchWidget)
        self.searchTextEdit.setObjectName(u'searchTextEdit')
        self.searchTextLabel.setBuddy(self.searchTextEdit)
        self.searchTextLayout.addRow(self.searchTextLabel, self.searchTextEdit)
        self.searchLayout.addLayout(self.searchTextLayout)
        self.searchButtonLayout = QtGui.QHBoxLayout()
        self.searchButtonLayout.setObjectName(u'searchButtonLayout')
        self.searchButtonLayout.addStretch()
        self.searchTextButton = QtGui.QPushButton(self.searchWidget)
        self.searchTextButton.setObjectName(u'searchTextButton')
        self.searchButtonLayout.addWidget(self.searchTextButton)
        self.searchLayout.addLayout(self.searchButtonLayout)
        self.pageLayout.addWidget(self.searchWidget)
        # Signals and slots
        QtCore.QObject.connect(self.searchTextEdit,
            QtCore.SIGNAL(u'returnPressed()'), self.onSearchTextButtonClicked)
        QtCore.QObject.connect(self.searchTextButton,
            QtCore.SIGNAL(u'clicked()'), self.onSearchTextButtonClicked)
        QtCore.QObject.connect(self.searchTextEdit,
            QtCore.SIGNAL(u'textChanged(const QString&)'),
            self.onSearchTextEditChanged)

    def addCustomContextActions(self):
        """
        Implement this method in your descendent media manager item to
        add any context menu items. This method is called automatically.
        """
        pass

    def initialise(self):
        """
        Implement this method in your descendent media manager item to
        do any UI or other initialisation. This method is called automatically.
        """
        pass

    def addStartHeaderBar(self):
        """
        Slot at start of toolbar for plugin to addwidgets
        """
        pass

    def addEndHeaderBar(self):
        """
        Slot at end of toolbar for plugin to add widgets
        """
        pass

    def onFileClick(self):
        """
        Add a file to the list widget to make it available for showing
        """
        files = QtGui.QFileDialog.getOpenFileNames(
            self, self.onNewPrompt,
            SettingsManager.get_last_dir(self.settingsSection),
            self.onNewFileMasks)
        log.info(u'New files(s) %s', files)
        if files:
            Receiver.send_message(u'cursor_busy')
            self.validateAndLoad(files)
        Receiver.send_message(u'cursor_normal')

    def loadFile(self, files):
        """
        Turn file from Drag and Drop into an array so the Validate code
        can run it.

        ``files``
        The list of files to be loaded
        """
        newFiles = []
        errorShown = False
        for file in files:
            type = file.split(u'.')[-1]
            if type.lower() not in self.onNewFileMasks:
                if not errorShown:
                    critical_error_message_box(
                        translate('OpenLP.MediaManagerItem',
                        'Invalid File Type'),
                        translate('OpenLP.MediaManagerItem',
                        'Invalid File %s.\nSuffix not supported') % file)
                    errorShown = True
            else:
                newFiles.append(file)
        if file:
            self.validateAndLoad(newFiles)

    def validateAndLoad(self, files):
        """
        Process a list for files either from the File Dialog or from Drag and
        Drop

        ``files``
            The files to be loaded.
        """
        names = []
        fullList = []
        for count in range(self.listView.count()):
            names.append(self.listView.item(count).text())
            fullList.append(self.listView.item(count).data(QtCore.Qt.UserRole))
        duplicatesFound = False
        filesAdded = False
        for file in files:
            filename = os.path.split(unicode(file))[1]
            if filename in names:
                duplicatesFound = True
            else:
                filesAdded = True
                fullList.append(file)
        if fullList and filesAdded:
            self.listView.clear()
            self.loadList(fullList)
            lastDir = os.path.split(unicode(files[0]))[0]
            SettingsManager.set_last_dir(self.settingsSection, lastDir)
            SettingsManager.set_list(self.settingsSection,
                self.settingsSection, self.getFileList())
        if duplicatesFound:
            critical_error_message_box(
                UiStrings().Duplicate,
                translate('OpenLP.MediaManagerItem',
                'Duplicate files were found on import and were ignored.'))

    def contextMenu(self, point):
        item = self.listView.itemAt(point)
        # Decide if we have to show the context menu or not.
        if item is None:
            return
        if not item.flags() & QtCore.Qt.ItemIsSelectable:
            return
        self.menu.exec_(self.listView.mapToGlobal(point))

    def getFileList(self):
        """
        Return the current list of files
        """
        count = 0
        filelist = []
        while count < self.listView.count():
            bitem = self.listView.item(count)
            filename = bitem.data(QtCore.Qt.UserRole)
            filelist.append(filename)
            count += 1
        return filelist

    def loadList(self, list):
        raise NotImplementedError(u'MediaManagerItem.loadList needs to be '
            u'defined by the plugin')

    def onNewClick(self):
        """
        Hook for plugins to define behaviour for adding new items.
        """
        pass

    def onEditClick(self):
        """
        Hook for plugins to define behaviour for editing items.
        """
        pass

    def onDeleteClick(self):
        raise NotImplementedError(u'MediaManagerItem.onDeleteClick needs to '
            u'be defined by the plugin')

    def onFocus(self):
        """
        Run when a tab in the media manager gains focus. This gives the media
        item a chance to focus any elements it wants to.
        """
        pass

    def generateSlideData(self, serviceItem, item=None, xmlVersion=False,
        remote=False):
        raise NotImplementedError(u'MediaManagerItem.generateSlideData needs '
            u'to be defined by the plugin')

    def onDoubleClicked(self):
        """
        Allows the list click action to be determined dynamically
        """
        if Settings().value(u'advanced/double click live', False):
            self.onLiveClick()
        else:
            self.onPreviewClick()

    def onSelectionChange(self):
        """
        Allows the change of current item in the list to be actioned
        """
        if Settings().value(u'advanced/single click preview',
            False) and self.quickPreviewAllowed \
            and self.listView.selectedIndexes() \
            and self.autoSelectId == -1:
            self.onPreviewClick(True)

    def onPreviewClick(self, keepFocus=False):
        """
        Preview an item by building a service item then adding that service
        item to the preview slide controller.
        """
        if not self.listView.selectedIndexes() and not self.remoteTriggered:
            QtGui.QMessageBox.information(self, UiStrings().NISp,
                translate('OpenLP.MediaManagerItem',
                'You must select one or more items to preview.'))
        else:
            log.debug(u'%s Preview requested', self.plugin.name)
            serviceItem = self.buildServiceItem()
            if serviceItem:
                serviceItem.from_plugin = True
                self.plugin.previewController.addServiceItem(serviceItem)
                if keepFocus:
                    self.listView.setFocus()

    def onLiveClick(self):
        """
        Send an item live by building a service item then adding that service
        item to the live slide controller.
        """
        if not self.listView.selectedIndexes():
            QtGui.QMessageBox.information(self, UiStrings().NISp,
                translate('OpenLP.MediaManagerItem',
                    'You must select one or more items to send live.'))
        else:
            self.goLive()

    def goLive(self, item_id=None, remote=False):
        log.debug(u'%s Live requested', self.plugin.name)
        item = None
        if item_id:
            item = self.createItemFromId(item_id)
        serviceItem = self.buildServiceItem(item, remote=remote)
        if serviceItem:
            if not item_id:
                serviceItem.from_plugin = True
            self.plugin.liveController.addServiceItem(serviceItem)

    def createItemFromId(self, item_id):
        item = QtGui.QListWidgetItem()
        item.setData(QtCore.Qt.UserRole, item_id)
        return item

    def onAddClick(self):
        """
        Add a selected item to the current service
        """
        if not self.listView.selectedIndexes() and not self.remoteTriggered:
            QtGui.QMessageBox.information(self, UiStrings().NISp,
                translate('OpenLP.MediaManagerItem',
                    'You must select one or more items to add.'))
        else:
            # Is it posssible to process multiple list items to generate
            # multiple service items?
            if self.singleServiceItem or self.remoteTriggered:
                log.debug(u'%s Add requested', self.plugin.name)
                self.addToService(replace=self.remoteTriggered)
            else:
                items = self.listView.selectedIndexes()
                for item in items:
                    self.addToService(item)

    def addToService(self, item=None, replace=None, remote=False):
        serviceItem = self.buildServiceItem(item, True, remote=remote)
        if serviceItem:
            serviceItem.from_plugin = False
            self.plugin.serviceManager.addServiceItem(serviceItem,
                replace=replace)

    def onAddEditClick(self):
        """
        Add a selected item to an existing item in the current service.
        """
        if not self.listView.selectedIndexes() and not self.remoteTriggered:
            QtGui.QMessageBox.information(self, UiStrings().NISp,
                translate('OpenLP.MediaManagerItem',
                    'You must select one or more items.'))
        else:
            log.debug(u'%s Add requested', self.plugin.name)
            serviceItem = self.plugin.serviceManager.getServiceItem()
            if not serviceItem:
                QtGui.QMessageBox.information(self, UiStrings().NISs,
                    translate('OpenLP.MediaManagerItem',
                        'You must select an existing service item to add to.'))
            elif self.plugin.name == serviceItem.name:
                self.generateSlideData(serviceItem)
                self.plugin.serviceManager.addServiceItem(serviceItem,
                    replace=True)
            else:
                # Turn off the remote edit update message indicator
                QtGui.QMessageBox.information(self,
                    translate('OpenLP.MediaManagerItem',
                        'Invalid Service Item'),
                    translate('OpenLP.MediaManagerItem',
                        'You must select a %s service item.') % self.title)

    def buildServiceItem(self, item=None, xmlVersion=False, remote=False):
        """
        Common method for generating a service item
        """
        serviceItem = ServiceItem(self.plugin)
        serviceItem.add_icon(self.plugin.iconPath)
        if self.generateSlideData(serviceItem, item, xmlVersion, remote):
            return serviceItem
        else:
            return None

    def serviceLoad(self, message):
        """
        Method to add processing when a service has been loaded and
        individual service items need to be processed by the plugins
        """
        pass

    def checkSearchResult(self):
        """
        Checks if the listView is empty and adds a "No Search Results" item.
        """
        if self.listView.count():
            return
        message = translate('OpenLP.MediaManagerItem', 'No Search Results')
        item = QtGui.QListWidgetItem(message)
        item.setFlags(QtCore.Qt.NoItemFlags)
        font = QtGui.QFont()
        font.setItalic(True)
        item.setFont(font)
        self.listView.addItem(item)

    def _getIdOfItemToGenerate(self, item, remoteItem):
        """
        Utility method to check items being submitted for slide generation.

        ``item``
            The item to check.

        ``remoteItem``
            The id to assign if the slide generation was remotely triggered.
        """
        if item is None:
            if self.remoteTriggered is None:
                item = self.listView.currentItem()
                if item is None:
                    return False
                item_id = item.data(QtCore.Qt.UserRole)
            else:
                item_id = remoteItem
        else:
            item_id = item.data(QtCore.Qt.UserRole)
        return item_id

    def saveAutoSelectId(self):
        """
        Sorts out, what item to select after loading a list.
        """
        # The item to select has not been set.
        if self.autoSelectId == -1:
            item = self.listView.currentItem()
            if item:
                self.autoSelectId = item.data(QtCore.Qt.UserRole)

    def search(self, string, showError=True):
        """
        Performs a plugin specific search for items containing ``string``
        """
        raise NotImplementedError(
            u'Plugin.search needs to be defined by the plugin')
