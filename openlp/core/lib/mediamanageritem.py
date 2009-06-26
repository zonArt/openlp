# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008-2009 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import types

from PyQt4 import QtCore, QtGui

from openlp.core.lib.toolbar import *
from openlp.core.lib import translate
from listwithpreviews import ListWithPreviews
from serviceitem import ServiceItem

class MediaManagerItem(QtGui.QWidget):
    """
    MediaManagerItem is a helper widget for plugins.
    """
    global log
    log = logging.getLogger(u'MediaManagerItem')
    log.info(u'Media Item loaded')

    def __init__(self, parent=None, icon=None, title=None):
        """
        Constructor to create the media manager item.
        """
        QtGui.QWidget.__init__(self)
        self.parent = parent
        if type(icon) is QtGui.QIcon:
            self.icon = icon
        elif type(icon) is types.StringType:
            self.icon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(icon)),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            self.icon = None
        if title is not None:
            self.title = title
        self.Toolbar = None
        #self.ConfigSection = None
        self.PageLayout = QtGui.QVBoxLayout(self)
        self.PageLayout.setSpacing(0)
        self.PageLayout.setMargin(0)
        self.setupUi()
        self.retranslateUi()
        self.initialise()

    def retranslateUi(self):
        pass

    def addToolbar(self):
        """
        A method to help developers easily add a toolbar to the media manager
        item.
        """
        if self.Toolbar is None:
            self.Toolbar = OpenLPToolbar(self)
            self.PageLayout.addWidget(self.Toolbar)

    def addToolbarButton(self, title, tooltip, icon, slot=None, objectname=None):
        """
        A method to help developers easily add a button to the toolbar.
        """
        # NB different order (when I broke this out, I wanted to not break compatability)
        # but it makes sense for the icon to come before the tooltip (as you have to have an icon, but not neccesarily a tooltip)
        self.Toolbar.addToolbarButton(title, icon, tooltip, slot, objectname)

    def addToolbarSeparator(self):
        """
        A very simple method to add a separator to the toolbar.
        """
        self.Toolbar.addSeparator()

    def contextMenuSeparator(self, base):
        action = QtGui.QAction(u'', base)
        action.setSeparator(True)
        return action

    def contextMenuAction(self, base, icon, text, slot):
        """
        Utility method to help build context menus for plugins
        """
        if type(icon) is QtGui.QIcon:
            ButtonIcon = icon
        elif type(icon) is types.StringType or type(icon) is types.UnicodeType:
            ButtonIcon = QtGui.QIcon()
            if icon.startswith(u':/'):
                ButtonIcon.addPixmap(QtGui.QPixmap(icon), QtGui.QIcon.Normal,
                    QtGui.QIcon.Off)
            else:
                ButtonIcon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(icon)),
                    QtGui.QIcon.Normal, QtGui.QIcon.Off)

        action = QtGui.QAction(text, base)
        action .setIcon(ButtonIcon)
        QtCore.QObject.connect(action, QtCore.SIGNAL(u'triggered()'), slot)
        return action

    ###########################################################################
    ### None of the following *need* to be used, feel free to override
    ### them cmopletely in your plugin's implementation.  Alternatively, call them from your
    ### plugin before or after you've done etra things that you need to.
    ### in order for them to work, you need to have setup
    # self.TranslationContext
    # self.PluginTextShort # eg "Image" for the image plugin
    # self.ConfigSection - where the items in the media manager are stored
    #   this could potentially be self.PluginTextShort.lower()
    #
    # self.OnNewPrompt=u'Select Image(s)'
    # self.OnNewFileMasks=u'Images (*.jpg *jpeg *.gif *.png *.bmp)'
    #   assumes that the new action is to load a file. If not, override onnew
    # self.ListViewWithDnD_class - there is a base list class with DnD assigned to it (openlp.core.lib.BaseListWithDnD())
    # each plugin needs to inherit a class from this and pass that *class* (not an instance) to here
    # via the ListViewWithDnD_class member
    # The assumption is that given that at least two plugins are of the form
    # "text with an icon" then all this will help
    # even for plugins of another sort, the setup of the right-click menu, common toolbar
    # will help to keep things consistent and ease the creation of new plugins

    # also a set of completely consistent action anesm then exist
    # (onPreviewClick() is always called that, rather than having the
    # name of the plugin added in as well... I regard that as a
    # feature, I guess others might differ!)

    def setupUi(self):
        # Add a toolbar
        self.addToolbar()
        # Create buttons for the toolbar
        ## New Song Button ##
        self.addToolbarButton(
            translate(self.TranslationContext, u'Load '+self.PluginTextShort),
            translate(self.TranslationContext, u'Load item into openlp.org'),
            u':/images/image_load.png', self.onNewClick, u'ImageNewItem')
        ## Delete Song Button ##
        self.addToolbarButton(
            translate(self.TranslationContext, u'Delete '+self.PluginTextShort),
            translate(self.TranslationContext, u'Delete the selected item'),
            u':/images/image_delete.png', self.onDeleteClick, u'DeleteItem')
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview  Button ##
        self.addToolbarButton(
            translate(self.TranslationContext, u'Preview '+self.PluginTextShort),
            translate(self.TranslationContext, u'Preview the selected item'),
            u':/system/system_preview.png', self.onPreviewClick, u'PreviewItem')
        ## Live  Button ##
        self.addToolbarButton(
            translate(self.TranslationContext, u'Go Live'),
            translate(self.TranslationContext, u'Send the selected item live'),
            u':/system/system_live.png', self.onLiveClick, u'LiveItem')
        ## Add  Button ##
        self.addToolbarButton(
            translate(self.TranslationContext, u'Add '+self.PluginTextShort+u' To Service'),
            translate(self.TranslationContext, u'Add the selected item(s) to the service'),
            u':/system/system_add.png', self.onAddClick, self.PluginTextShort+u'AddItem')
        #Add the List widget
        self.ListView = self.ListViewWithDnD_class()
        self.ListView.uniformItemSizes = True
        self.ListData = ListWithPreviews()
        self.ListView.setModel(self.ListData)
        self.ListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.ListView.setSpacing(1)
        self.ListView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.ListView.setAlternatingRowColors(True)
        self.ListView.setDragEnabled(True)
        self.ListView.setObjectName(self.PluginTextShort+u'ListView')
        self.PageLayout.addWidget(self.ListView)
        #define and add the context menu
        self.ListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ListView.addAction(self.contextMenuAction(
            self.ListView, ':/system/system_preview.png',
            translate(self.TranslationContext, u'&Preview '+self.PluginTextShort),
            self.onPreviewClick))
        self.ListView.addAction(self.contextMenuAction(
            self.ListView, ':/system/system_live.png',
            translate(self.TranslationContext, u'&Show Live'),
            self.onLiveClick))
        self.ListView.addAction(self.contextMenuAction(
            self.ListView, ':/system/system_add.png',
            translate(self.TranslationContext, u'&Add to Service'),
            self.onAddClick))
        QtCore.QObject.connect(self.ListView,
           QtCore.SIGNAL(u'doubleClicked(QModelIndex)'), self.onPreviewClick)

    def initialise(self):
        self.loadList(self.parent.config.load_list(self.ConfigSection))

    def onNewClick(self):
        files = QtGui.QFileDialog.getOpenFileNames(None,
            translate(self.TranslationContext, self.OnNewPrompt),
            self.parent.config.get_last_dir(),
            self.OnNewFileMasks)
        log.info(u'New files(s)', unicode(files))
        if len(files) > 0:
            self.loadList(files)
            dir, filename = os.path.split(unicode(files[0]))
            self.parent.config.set_last_dir(dir)
            self.parent.config.set_list(self.ConfigSection, self.ListData.getFileList())

    def loadList(self, list):
        for file in list:
            self.ListData.addRow(file)

    def onDeleteClick(self):
        indexes = self.ListView.selectedIndexes()
        for index in indexes:
            current_row = int(index.row())
            self.ListData.removeRow(current_row)
        self.parent.config.set_list(self.ConfigSection, self.ListData.getFileList())

    def generateSlideData(self):
        raise NotImplementedError(u'MediaManagerItem.generateSlideData needs to be defined by the plugin')

    def onPreviewClick(self):
        log.debug(self.PluginTextShort+u'Preview Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon(u':/media/media_image.png')
        self.generateSlideData(service_item)
        self.parent.preview_controller.addServiceItem(service_item)

    def onLiveClick(self):
        log.debug(self.PluginTextShort+u' Live Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon(u':/media/media_image.png')
        self.generateSlideData(service_item)
        self.parent.live_controller.addServiceItem(service_item)

    def onAddClick(self):
        log.debug(self.PluginTextShort+u' Add Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon(u':/media/media_image.png')
        self.generateSlideData(service_item)
        self.parent.service_manager.addServiceItem(service_item)
