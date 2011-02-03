# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import context_menu_action, context_menu_separator, \
    SettingsManager, OpenLPToolbar, ServiceItem, StringContent, build_icon, \
    translate, Receiver

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

     ``self.OnNewPrompt``
        Defaults to *'Select Image(s)'*.

     ``self.OnNewFileMasks``
        Defaults to *'Images (*.jpg *jpeg *.gif *.png *.bmp)'*. This
        assumes that the new action is to load a file. If not, you
        need to override the ``OnNew`` method.

     ``self.ListViewWithDnD_class``
        This must be a **class**, not an object, descended from
        ``openlp.core.lib.BaseListWithDnD`` that is not used in any
        other part of OpenLP.

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
        self.parent = parent
        #TODO: plugin should not be the parent in future
        self.plugin = parent # plugin
        visible_title = self.plugin.getString(StringContent.VisibleName)
        self.title = unicode(visible_title[u'title'])
        self.settingsSection = self.plugin.name.lower()
        self.icon = None
        if icon:
            self.icon = build_icon(icon)
        self.toolbar = None
        self.remoteTriggered = None
        self.singleServiceItem = True
        self.pageLayout = QtGui.QVBoxLayout(self)
        self.pageLayout.setSpacing(0)
        self.pageLayout.setMargin(0)
        self.requiredIcons()
        self.setupUi()
        self.retranslateUi()
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_service_load' % self.parent.name.lower()),
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
            string cotaining either the absolute path to the image, or an
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
        ## Import Button ##
        if self.hasImportIcon:
            import_string = self.plugin.getString(StringContent.Import)
            self.addToolbarButton(
                import_string[u'title'],
                import_string[u'tooltip'],
                u':/general/general_import.png', self.onImportClick)
        ## Load Button ##
        if self.hasFileIcon:
            load_string = self.plugin.getString(StringContent.Load)
            self.addToolbarButton(
                load_string[u'title'],
                load_string[u'tooltip'],
                u':/general/general_open.png', self.onFileClick)
        ## New Button ##
        if self.hasNewIcon:
            new_string = self.plugin.getString(StringContent.New)
            self.addToolbarButton(
                new_string[u'title'],
                new_string[u'tooltip'],
                u':/general/general_new.png', self.onNewClick)
        ## Edit Button ##
        if self.hasEditIcon:
            edit_string = self.plugin.getString(StringContent.Edit)
            self.addToolbarButton(
                edit_string[u'title'],
                edit_string[u'tooltip'],
                u':/general/general_edit.png', self.onEditClick)
        ## Delete Button ##
        if self.hasDeleteIcon:
            delete_string = self.plugin.getString(StringContent.Delete)
            self.addToolbarButton(
                delete_string[u'title'],
                delete_string[u'tooltip'],
                u':/general/general_delete.png', self.onDeleteClick)
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview ##
        preview_string = self.plugin.getString(StringContent.Preview)
        self.addToolbarButton(
            preview_string[u'title'],
            preview_string[u'tooltip'],
            u':/general/general_preview.png', self.onPreviewClick)
        ## Live Button ##
        live_string = self.plugin.getString(StringContent.Live)
        self.addToolbarButton(
            live_string[u'title'],
            live_string[u'tooltip'],
            u':/general/general_live.png', self.onLiveClick)
        ## Add to service Button ##
        service_string = self.plugin.getString(StringContent.Service)
        self.addToolbarButton(
            service_string[u'title'],
            service_string[u'tooltip'],
            u':/general/general_add.png', self.onAddClick)

    def addListViewToToolBar(self):
        """
        Creates the main widget for listing items the media item is tracking
        """
        # Add the List widget
        self.listView = self.ListViewWithDnD_class(self)
        self.listView.uniformItemSizes = True
        self.listView.setSpacing(1)
        self.listView.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.listView.setAlternatingRowColors(True)
        self.listView.setDragEnabled(True)
        self.listView.setObjectName(u'%sListView' % self.plugin.name)
        # Add to pageLayout
        self.pageLayout.addWidget(self.listView)
        # define and add the context menu
        self.listView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        name_string = self.plugin.getString(StringContent.Name)
        if self.hasEditIcon:
            self.listView.addAction(
                context_menu_action(
                    self.listView, u':/general/general_edit.png',
                    self.plugin.getString(StringContent.Edit)[u'title'],
                    self.onEditClick))
            self.listView.addAction(context_menu_separator(self.listView))
        if self.hasDeleteIcon:
            self.listView.addAction(
                context_menu_action(
                    self.listView, u':/general/general_delete.png',
                    self.plugin.getString(StringContent.Delete)[u'title'],
                    self.onDeleteClick))
            self.listView.addAction(context_menu_separator(self.listView))
        self.listView.addAction(
            context_menu_action(
                self.listView, u':/general/general_preview.png',
                self.plugin.getString(StringContent.Preview)[u'title'],
                self.onPreviewClick))
        self.listView.addAction(
            context_menu_action(
                self.listView, u':/general/general_live.png',
                self.plugin.getString(StringContent.Live)[u'title'],
                self.onLiveClick))
        self.listView.addAction(
            context_menu_action(
                self.listView, u':/general/general_add.png',
                self.plugin.getString(StringContent.Service)[u'title'],
                self.onAddClick))
        if self.addToServiceItem:
            self.listView.addAction(
                context_menu_action(
                    self.listView, u':/general/general_add.png',
                    translate('OpenLP.MediaManagerItem',
                    '&Add to selected Service Item'),
                    self.onAddEditClick))
        QtCore.QObject.connect(self.listView,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
            self.onClickPressed)

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
            self, self.OnNewPrompt,
            SettingsManager.get_last_dir(self.settingsSection),
            self.OnNewFileMasks)
        log.info(u'New files(s) %s', unicode(files))
        if files:
            Receiver.send_message(u'cursor_busy')
            self.loadList(files)
            lastDir = os.path.split(unicode(files[0]))[0]
            SettingsManager.set_last_dir(self.settingsSection, lastDir)
            SettingsManager.set_list(self.settingsSection,
                self.settingsSection, self.getFileList())
        Receiver.send_message(u'cursor_normal')

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

    def validate(self, file, thumb):
        """
        Validates to see if the file still exists or thumbnail is up to date
        """
        if not os.path.exists(file):
            return False
        if os.path.exists(thumb):
            filedate = os.stat(file).st_mtime
            thumbdate = os.stat(thumb).st_mtime
            # if file updated rebuild icon
            if filedate > thumbdate:
                self.iconFromFile(file, thumb)
        else:
            self.iconFromFile(file, thumb)
        return True

    def iconFromFile(self, file, thumb):
        """
        Create a thumbnail icon from a given file

        ``file``
            The file to create the icon from

        ``thumb``
            The filename to save the thumbnail to
        """
        icon = build_icon(unicode(file))
        pixmap = icon.pixmap(QtCore.QSize(88, 50))
        ext = os.path.splitext(thumb)[1].lower()
        pixmap.save(thumb, ext[1:])
        return icon

    def loadList(self, list):
        raise NotImplementedError(u'MediaManagerItem.loadList needs to be '
            u'defined by the plugin')

    def onNewClick(self):
        raise NotImplementedError(u'MediaManagerItem.onNewClick needs to be '
            u'defined by the plugin')

    def onEditClick(self):
        raise NotImplementedError(u'MediaManagerItem.onEditClick needs to be '
            u'defined by the plugin')

    def onDeleteClick(self):
        raise NotImplementedError(u'MediaManagerItem.onDeleteClick needs to '
            u'be defined by the plugin')

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

    def onPreviewClick(self):
        """
        Preview an item by building a service item then adding that service
        item to the preview slide controller.
        """
        if not self.listView.selectedIndexes() and not self.remoteTriggered:
            QtGui.QMessageBox.information(self,
                translate('OpenLP.MediaManagerItem', 'No Items Selected'),
                translate('OpenLP.MediaManagerItem',
                'You must select one or more items to preview.'))
        else:
            log.debug(u'%s Preview requested', self.plugin.name)
            serviceItem = self.buildServiceItem()
            if serviceItem:
                serviceItem.from_plugin = True
                self.parent.previewController.addServiceItem(serviceItem)

    def onLiveClick(self):
        """
        Send an item live by building a service item then adding that service
        item to the live slide controller.
        """
        if not self.listView.selectedIndexes():
            QtGui.QMessageBox.information(self,
                translate('OpenLP.MediaManagerItem', 'No Items Selected'),
                translate('OpenLP.MediaManagerItem',
                    'You must select one or more items to send live.'))
        else:
            log.debug(u'%s Live requested', self.plugin.name)
            serviceItem = self.buildServiceItem()
            if serviceItem:
                serviceItem.from_plugin = True
                self.parent.liveController.addServiceItem(serviceItem)

    def onAddClick(self):
        """
        Add a selected item to the current service
        """
        if not self.listView.selectedIndexes() and not self.remoteTriggered:
            QtGui.QMessageBox.information(self,
                translate('OpenLP.MediaManagerItem', 'No Items Selected'),
                translate('OpenLP.MediaManagerItem',
                    'You must select one or more items.'))
        else:
            # Is it posssible to process multiple list items to generate
            # multiple service items?
            if self.singleServiceItem or self.remoteTriggered:
                log.debug(u'%s Add requested', self.plugin.name)
                serviceItem = self.buildServiceItem(None, True)
                if serviceItem:
                    serviceItem.from_plugin = False
                    self.parent.serviceManager.addServiceItem(serviceItem,
                        replace=self.remoteTriggered)
            else:
                items = self.listView.selectedIndexes()
                for item in items:
                    serviceItem = self.buildServiceItem(item, True)
                    if serviceItem:
                        serviceItem.from_plugin = False
                        self.parent.serviceManager.addServiceItem(serviceItem)

    def onAddEditClick(self):
        """
        Add a selected item to an existing item in the current service.
        """
        if not self.listView.selectedIndexes() and not self.remoteTriggered:
            QtGui.QMessageBox.information(self,
                translate('OpenLP.MediaManagerItem', 'No items selected'),
                translate('OpenLP.MediaManagerItem',
                    'You must select one or more items'))
        else:
            log.debug(u'%s Add requested', self.plugin.name)
            serviceItem = self.parent.serviceManager.getServiceItem()
            if not serviceItem:
                QtGui.QMessageBox.information(self,
                    translate('OpenLP.MediaManagerItem',
                        'No Service Item Selected'),
                    translate('OpenLP.MediaManagerItem',
                        'You must select an existing service item to add to.'))
            elif self.plugin.name.lower() == serviceItem.name.lower():
                self.generateSlideData(serviceItem)
                self.parent.serviceManager.addServiceItem(serviceItem,
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
        serviceItem = ServiceItem(self.parent)
        serviceItem.add_icon(self.parent.icon_path)
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
