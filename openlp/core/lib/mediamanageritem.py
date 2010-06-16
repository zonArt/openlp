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
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import context_menu_action, context_menu_separator, \
    SettingsManager, OpenLPToolbar, ServiceItem, build_icon

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

    ``icon``
        Either a ``QIcon``, a resource path, or a file name. This is
        the icon which is displayed in the *Media Manager*.

    ``title``
        The title visible on the item in the *Media Manager*.

    **Member Variables**

    When creating a descendant class from this class for your plugin,
    the following member variables should be set.

    ``self.PluginNameShort``
        The shortened (usually singular) name for the plugin e.g. *'Song'*
        for the Songs plugin.

    ``self.PluginNameVisible``
        The user visible name for a plugin which should use a suitable
        translation function.

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

    def __init__(self, parent=None, icon=None, title=None):
        """
        Constructor to create the media manager item.
        """
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.settingsSection = title.lower()
        if isinstance(icon, QtGui.QIcon):
            self.icon = icon
        elif isinstance(icon, basestring):
            self.icon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(icon)),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            self.icon = None
        if title:
            self.title = title
        self.Toolbar = None
        self.remoteTriggered = None
        self.ServiceItemIconName = None
        self.singleServiceItem = True
        self.addToServiceItem = False
        self.PageLayout = QtGui.QVBoxLayout(self)
        self.PageLayout.setSpacing(0)
        self.PageLayout.setContentsMargins(4, 0, 4, 0)
        self.requiredIcons()
        self.initPluginNameVisible()
        self.setupUi()
        self.retranslateUi()

    def initPluginNameVisible(self):
        pass

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
        if self.Toolbar is None:
            self.Toolbar = OpenLPToolbar(self)
            self.PageLayout.addWidget(self.Toolbar)

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

        ``objectname``
            The name of the button.
        """
        # NB different order (when I broke this out, I didn't want to
        # break compatability), but it makes sense for the icon to
        # come before the tooltip (as you have to have an icon, but
        # not neccesarily a tooltip)
        self.Toolbar.addToolbarButton(title, icon, tooltip, slot, checkable)

    def addToolbarSeparator(self):
        """
        A very simple method to add a separator to the toolbar.
        """
        self.Toolbar.addSeparator()

    def setupUi(self):
        """
        This method sets up the interface on the button. Plugin
        developers use this to add and create toolbars, and the rest
        of the interface of the media manager item.
        """
        # Add a toolbar
        self.addToolbar()
        #Allow the plugin to define buttons at start of bar
        self.addStartHeaderBar()
        #Add the middle of the tool bar (pre defined)
        self.addMiddleHeaderBar()
        #Allow the plugin to define buttons at end of bar
        self.addEndHeaderBar()
        #Add the list view
        self.addListViewToToolBar()

    def addMiddleHeaderBar(self):
        # Create buttons for the toolbar
        ## Import Button ##
        if self.hasImportIcon:
            self.addToolbarButton(
                u'Import %s' % self.PluginNameShort,
                u'%s %s' % (self.trUtf8('Import a'), self.PluginNameVisible),
                u':/general/general_import.png', self.onImportClick)
        ## File Button ##
        if self.hasFileIcon:
            self.addToolbarButton(
                u'Load %s' % self.PluginNameShort,
                u'%s %s' % (self.trUtf8('Load a new'), self.PluginNameVisible),
                u':/general/general_open.png', self.onFileClick)
        ## New Button ##
        if self.hasNewIcon:
            self.addToolbarButton(
                u'New %s' % self.PluginNameShort,
                u'%s %s' % (self.trUtf8('Add a new'), self.PluginNameVisible),
                u':/general/general_new.png', self.onNewClick)
        ## Edit Button ##
        if self.hasEditIcon:
            self.addToolbarButton(
                u'Edit %s' % self.PluginNameShort,
                u'%s %s' % (self.trUtf8('Edit the selected'),
                    self.PluginNameVisible),
                u':/general/general_edit.png', self.onEditClick)
        ## Delete Button ##
        if self.hasDeleteIcon:
            self.addToolbarButton(
                u'Delete %s' % self.PluginNameShort,
                self.trUtf8('Delete the selected item'),
                u':/general/general_delete.png', self.onDeleteClick)
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview ##
        self.addToolbarButton(
            u'Preview %s' % self.PluginNameShort,
            self.trUtf8('Preview the selected item'),
            u':/general/general_preview.png', self.onPreviewClick)
        ## Live  Button ##
        self.addToolbarButton(
            u'Go Live',
            self.trUtf8('Send the selected item live'),
            u':/general/general_live.png', self.onLiveClick)
        ## Add to service Button ##
        self.addToolbarButton(
            u'Add %s to Service' % self.PluginNameShort,
            self.trUtf8('Add the selected item(s) to the service'),
            u':/general/general_add.png', self.onAddClick)

    def addListViewToToolBar(self):
        #Add the List widget
        self.ListView = self.ListViewWithDnD_class(self)
        self.ListView.uniformItemSizes = True
        self.ListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.ListView.setSpacing(1)
        self.ListView.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.ListView.setAlternatingRowColors(True)
        self.ListView.setDragEnabled(True)
        self.ListView.setObjectName(u'%sListView' % self.PluginNameShort)
        #Add tp PageLayout
        self.PageLayout.addWidget(self.ListView)
        #define and add the context menu
        self.ListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        if self.hasEditIcon:
            self.ListView.addAction(
                context_menu_action(
                    self.ListView, u':/general/general_edit.png',
                    u'%s %s' % (self.trUtf8('&Edit'), self.PluginNameVisible),
                    self.onEditClick))
            self.ListView.addAction(context_menu_separator(self.ListView))
        if self.hasDeleteIcon:
            self.ListView.addAction(
                context_menu_action(
                    self.ListView, u':/general/general_delete.png',
                    u'%s %s' % (self.trUtf8('&Delete'), self.PluginNameVisible),
                    self.onDeleteClick))
            self.ListView.addAction(context_menu_separator(self.ListView))
        self.ListView.addAction(
            context_menu_action(
                self.ListView, u':/general/general_preview.png',
                u'%s %s' % (self.trUtf8('&Preview'), self.PluginNameVisible),
                self.onPreviewClick))
        self.ListView.addAction(
            context_menu_action(
                self.ListView, u':/general/general_live.png',
                self.trUtf8('&Show Live'), self.onLiveClick))
        self.ListView.addAction(
            context_menu_action(
                self.ListView, u':/general/general_add.png',
                self.trUtf8('&Add to Service'), self.onAddClick))
        if self.addToServiceItem:
            self.ListView.addAction(
                context_menu_action(
                    self.ListView, u':/general/general_add.png',
                    self.trUtf8('&Add to selected Service Item'),
                    self.onAddEditClick))
        QtCore.QObject.connect(
            self.ListView, QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
            self.onPreviewClick)

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

    def checkItemSelected(self, message):
        """
        Check if a list item is selected so an action may be performed on it

        ``message``
            The message to give the user if no item is selected
        """
        if not self.ListView.selectedIndexes():
            QtGui.QMessageBox.information(self,
                self.trUtf8('No Items Selected'), message)
            return False
        return True

    def onFileClick(self):
        files = QtGui.QFileDialog.getOpenFileNames(
            self, self.OnNewPrompt,
            SettingsManager.get_last_dir(self.settingsSection),
            self.OnNewFileMasks)
        log.info(u'New files(s) %s', unicode(files))
        if files:
            self.loadList(files)
            lastDir = os.path.split(unicode(files[0]))[0]
            SettingsManager.set_last_dir(self.settingsSection, lastDir)
            SettingsManager.set_list(self.settingsSection,
                self.settingsSection, self.getFileList())

    def getFileList(self):
        count = 0
        filelist = []
        while count < self.ListView.count():
            bitem = self.ListView.item(count)
            filename = unicode(bitem.data(QtCore.Qt.UserRole).toString())
            filelist.append(filename)
            count += 1
        return filelist

    def validate(self, file, thumb):
        """
        Validates to see if the file still exists or thumbnail is up to date
        """
        if os.path.exists(file):
            filedate = os.stat(file).st_mtime
            thumbdate = os.stat(thumb).st_mtime
            #if file updated rebuild icon
            if filedate > thumbdate:
                self.IconFromFile(file, thumb)
            return True
        return False

    def IconFromFile(self, file, thumb):
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

    def generateSlideData(self, service_item, item):
        raise NotImplementedError(u'MediaManagerItem.generateSlideData needs '
            u'to be defined by the plugin')

    def onPreviewClick(self):
        if not self.ListView.selectedIndexes() and not self.remoteTriggered:
            QtGui.QMessageBox.information(self,
                self.trUtf8('No Items Selected'),
                self.trUtf8('You must select one or more items to preview.'))
        else:
            log.debug(self.PluginNameShort + u' Preview requested')
            service_item = self.buildServiceItem()
            if service_item:
                service_item.from_plugin = True
                self.parent.preview_controller.addServiceItem(service_item)

    def onLiveClick(self):
        if not self.ListView.selectedIndexes():
            QtGui.QMessageBox.information(self,
                self.trUtf8('No Items Selected'),
                self.trUtf8('You must select one or more items to send live.'))
        else:
            log.debug(self.PluginNameShort + u' Live requested')
            service_item = self.buildServiceItem()
            if service_item:
                service_item.from_plugin = True
                self.parent.live_controller.addServiceItem(service_item)

    def onAddClick(self):
        if not self.ListView.selectedIndexes() and not self.remoteTriggered:
            QtGui.QMessageBox.information(self,
                self.trUtf8('No Items Selected'),
                self.trUtf8('You must select one or more items.'))
        else:
            #Is it posssible to process multiple list items to generate multiple
            #service items?
            if self.singleServiceItem or self.remoteTriggered:
                log.debug(self.PluginNameShort + u' Add requested')
                service_item = self.buildServiceItem()
                if service_item:
                    service_item.from_plugin = False
                    self.parent.service_manager.addServiceItem(service_item,
                        replace=self.remoteTriggered)
            else:
                items = self.ListView.selectedIndexes()
                for item in items:
                    service_item = self.buildServiceItem(item)
                    if service_item:
                        service_item.from_plugin = False
                        self.parent.service_manager.addServiceItem(service_item)

    def onAddEditClick(self):
        if not self.ListView.selectedIndexes() and not self.remoteTriggered:
            QtGui.QMessageBox.information(self,
                self.trUtf8('No items selected'),
                self.trUtf8('You must select one or more items'))
        else:
            log.debug(self.PluginNameShort + u' Add requested')
            service_item = self.parent.service_manager.getServiceItem()
            if not service_item:
                QtGui.QMessageBox.information(self,
                    self.trUtf8('No Service Item Selected'),
                    self.trUtf8(
                        'You must select an existing service item to add to.'))
            elif self.title.lower() == service_item.name.lower():
                self.generateSlideData(service_item)
                self.parent.service_manager.addServiceItem(service_item,
                    replace=True)
            else:
                #Turn off the remote edit update message indicator
                QtGui.QMessageBox.information(self,
                    self.trUtf8('Invalid Service Item'),
                    self.trUtf8(unicode(
                        'You must select a %s service item.' % self.title)))

    def buildServiceItem(self, item=None):
        """
        Common method for generating a service item
        """
        service_item = ServiceItem(self.parent)
        if self.ServiceItemIconName:
            service_item.add_icon(self.ServiceItemIconName)
        else:
            service_item.add_icon(
                u':/media/media_' + self.PluginNameShort.lower() + u'.png')
        if self.generateSlideData(service_item, item):
            return service_item
        else:
            return None
