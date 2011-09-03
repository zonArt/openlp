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
"""
Provides the generic functions for interfacing plugins with the Media Manager.
"""
import logging
import os
import re

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsManager, OpenLPToolbar, ServiceItem, \
    StringContent, build_icon, translate, Receiver, ListWidgetWithDnD
from openlp.core.lib.ui import UiStrings, context_menu_action, \
    context_menu_separator, critical_error_message_box

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
        self.auto_select_id = -1
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

    def addToolbarButton(
        self, title, tooltip, icon, slot=None, checkable=False):
        """
        A method to help developers easily add a button to the toolbar.

        ``title``
            The title of the button.

        ``tooltip``
            The tooltip to be displayed when the mouse hovers over the
            button.

        ``icon``
            The icon of the button. This can be an instance of QIcon, or a
            string containing either the absolute path to the image, or an
            internal resource path starting with ':/'.

        ``slot``
            The method to call when the button is clicked.

        ``checkable``
            If *True* the button has two, *off* and *on*, states. Default is
            *False*, which means the buttons has only one state.
        """
        # NB different order (when I broke this out, I didn't want to
        # break compatability), but it makes sense for the icon to
        # come before the tooltip (as you have to have an icon, but
        # not neccesarily a tooltip)
        return self.toolbar.addToolbarButton(title, icon, tooltip, slot,
            checkable)

    def addToolbarSeparator(self):
        """
        A very simple method to add a separator to the toolbar.
        """
        self.toolbar.addSeparator()

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
            toolbar_actions.append([StringContent.Import,
            u':/general/general_import.png', self.onImportClick])
        ## Load Button ##
        if self.hasFileIcon:
            toolbar_actions.append([StringContent.Load,
                u':/general/general_open.png', self.onFileClick])
        ## New Button ##
        if self.hasNewIcon:
            toolbar_actions.append([StringContent.New,
                u':/general/general_new.png', self.onNewClick])
        ## Edit Button ##
        if self.hasEditIcon:
            toolbar_actions.append([StringContent.Edit,
                u':/general/general_edit.png', self.onEditClick])
        ## Delete Button ##
        if self.hasDeleteIcon:
            toolbar_actions.append([StringContent.Delete,
                u':/general/general_delete.png', self.onDeleteClick])
        ## Preview ##
        toolbar_actions.append([StringContent.Preview,
            u':/general/general_preview.png', self.onPreviewClick])
        ## Live Button ##
        toolbar_actions.append([StringContent.Live,
            u':/general/general_live.png', self.onLiveClick])
        ## Add to service Button ##
        toolbar_actions.append([StringContent.Service,
            u':/general/general_add.png', self.onAddClick])
        for action in toolbar_actions:
            if action[0] == StringContent.Preview:
                self.addToolbarSeparator()
            self.addToolbarButton(
                self.plugin.getString(action[0])[u'title'],
                self.plugin.getString(action[0])[u'tooltip'],
                action[1], action[2])

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
            context_menu_action(
                self.listView, u':/general/general_edit.png',
                self.plugin.getString(StringContent.Edit)[u'title'],
                self.onEditClick)
            context_menu_separator(self.listView)
        if self.hasDeleteIcon:
            context_menu_action(
                self.listView, u':/general/general_delete.png',
                self.plugin.getString(StringContent.Delete)[u'title'],
                self.onDeleteClick, [QtCore.Qt.Key_Delete])
            context_menu_separator(self.listView)
        context_menu_action(
            self.listView, u':/general/general_preview.png',
            self.plugin.getString(StringContent.Preview)[u'title'],
            self.onPreviewClick, [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return])
        context_menu_action(
            self.listView, u':/general/general_live.png',
            self.plugin.getString(StringContent.Live)[u'title'],
            self.onLiveClick, [QtCore.Qt.ShiftModifier + QtCore.Qt.Key_Enter,
            QtCore.Qt.ShiftModifier + QtCore.Qt.Key_Return])
        context_menu_action(
            self.listView, u':/general/general_add.png',
            self.plugin.getString(StringContent.Service)[u'title'],
            self.onAddClick, [QtCore.Qt.Key_Plus, QtCore.Qt.Key_Equal])
        if self.addToServiceItem:
            context_menu_action(
                self.listView, u':/general/general_add.png',
                translate('OpenLP.MediaManagerItem',
                '&Add to selected Service Item'), self.onAddEditClick)
        self.addCustomContextActions()
        # Create the context menu and add all actions from the listView.
        self.menu = QtGui.QMenu()
        self.menu.addActions(self.listView.actions())
        QtCore.QObject.connect(self.listView,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
            self.onClickPressed)
        QtCore.QObject.connect(self.listView,
            QtCore.SIGNAL(u'itemSelectionChanged()'),
            self.onSelectionChange)
        QtCore.QObject.connect(self.listView,
            QtCore.SIGNAL('customContextMenuRequested(QPoint)'),
            self.contextMenu)

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
        log.info(u'New files(s) %s', unicode(files))
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
                        unicode(translate('OpenLP.MediaManagerItem',
                        'Invalid File %s.\nSuffix not supported'))
                        % file)
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
         The files to be loaded
        """
        names = []
        for count in range(0, self.listView.count()):
            names.append(unicode(self.listView.item(count).text()))
        newFiles = []
        duplicatesFound = False
        for file in files:
            filename = os.path.split(unicode(file))[1]
            if filename in names:
                duplicatesFound = True
            else:
                newFiles.append(file)
        if newFiles:
            self.loadList(newFiles)
            lastDir = os.path.split(unicode(files[0]))[0]
            SettingsManager.set_last_dir(self.settingsSection, lastDir)
            SettingsManager.set_list(self.settingsSection,
                self.settingsSection, self.getFileList())
        if duplicatesFound:
            critical_error_message_box(
                UiStrings().Duplicate,
                unicode(translate('OpenLP.MediaManagerItem',
                'Duplicate files were found on import and were ignored.')))

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
            filename = unicode(bitem.data(QtCore.Qt.UserRole).toString())
            filelist.append(filename)
            count += 1
        return filelist

    def validate(self, image, thumb):
        """
        Validates whether an image still exists and, if it does, is the
        thumbnail representation of the image up to date.
        """
        if not os.path.exists(unicode(image)):
            return False
        if os.path.exists(thumb):
            imageDate = os.stat(unicode(image)).st_mtime
            thumbDate = os.stat(unicode(thumb)).st_mtime
            # If image has been updated rebuild icon
            if imageDate > thumbDate:
                self.iconFromFile(image, thumb)
        else:
            self.iconFromFile(image, thumb)
        return True

    def iconFromFile(self, image_path, thumb_path):
        """
        Create a thumbnail icon from a given image.

        ``image_path``
            The image file to create the icon from.

        ``thumb_path``
            The filename to save the thumbnail to.
        """
        ext = os.path.splitext(thumb_path)[1].lower()
        reader = QtGui.QImageReader(image_path)
        ratio = float(reader.size().width()) / float(reader.size().height())
        reader.setScaledSize(QtCore.QSize(int(ratio * 88), 88))
        thumb = reader.read()
        thumb.save(thumb_path, ext[1:])
        if os.path.exists(thumb_path):
            return build_icon(unicode(thumb_path))
        # Fallback for files with animation support.
        return build_icon(unicode(image_path))

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

    def generateSlideData(self, serviceItem, item=None, xmlVersion=False):
        raise NotImplementedError(u'MediaManagerItem.generateSlideData needs '
            u'to be defined by the plugin')

    def onClickPressed(self):
        """
        Allows the list click action to be determined dynamically
        """
        if QtCore.QSettings().value(u'advanced/double click live',
            QtCore.QVariant(False)).toBool():
            self.onLiveClick()
        else:
            self.onPreviewClick()

    def onSelectionChange(self):
        """
        Allows the change of current item in the list to be actioned
        """
        if QtCore.QSettings().value(u'advanced/single click preview',
            QtCore.QVariant(False)).toBool() and self.quickPreviewAllowed \
            and self.listView.selectedIndexes() \
            and self.auto_select_id == -1:
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

    def goLive(self, item_id=None):
        log.debug(u'%s Live requested', self.plugin.name)
        item = None
        if item_id:
            item = self.createItemFromId(item_id)
        serviceItem = self.buildServiceItem(item)
        if serviceItem:
            if not item_id:
                serviceItem.from_plugin = True
            self.plugin.liveController.addServiceItem(serviceItem)

    def createItemFromId(self, item_id):
        item = QtGui.QListWidgetItem()
        item.setData(QtCore.Qt.UserRole, QtCore.QVariant(item_id))
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

    def addToService(self, item=None, replace=None):
        serviceItem = self.buildServiceItem(item, True)
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
                    unicode(translate('OpenLP.MediaManagerItem',
                        'You must select a %s service item.')) % self.title)

    def buildServiceItem(self, item=None, xmlVersion=False):
        """
        Common method for generating a service item
        """
        serviceItem = ServiceItem(self.plugin)
        serviceItem.add_icon(self.plugin.icon_path)
        if self.generateSlideData(serviceItem, item, xmlVersion):
            return serviceItem
        else:
            return None

    def serviceLoad(self, message):
        """
        Method to add processing when a service has been loaded and
        individual service items need to be processed by the plugins
        """
        pass

    def check_search_result(self):
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
                item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            else:
                item_id = remoteItem
        else:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        return item_id

    def save_auto_select_id(self):
        """
        Sorts out, what item to select after loading a list.
        """
        # The item to select has not been set.
        if self.auto_select_id == -1:
            item = self.listView.currentItem()
            if item:
                self.auto_select_id = item.data(QtCore.Qt.UserRole).toInt()[0]

    def search(self, string):
        """
        Performs a plugin specific search for items containing ``string``
        """
        raise NotImplementedError(
            u'Plugin.search needs to be defined by the plugin')
