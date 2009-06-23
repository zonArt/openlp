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

# xxx this should be in core.lib probably
from openlp.plugins.images.lib import ListWithPreviews
class ImageList(QtGui.QListView):

    def __init__(self,parent=None,name=None):
        QtGui.QListView.__init__(self,parent)

    def mouseMoveEvent(self, event):
        """
        Drag and drop event does not care what data is selected
        as the recepient will use events to request the data move
        just tell it what plugin to call
        """
        if event.buttons() != QtCore.Qt.LeftButton:
            return
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        drag.setMimeData(mimeData)
        mimeData.setText(u'Image')
        dropAction = drag.start(QtCore.Qt.CopyAction)
        if dropAction == QtCore.Qt.CopyAction:
            self.close()


class MediaManagerItem(QtGui.QWidget):
    """
    MediaManagerItem is a helper widget for plugins.
    """
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

####################################################################################################
    ### None of the following *need* to be used, feel free to override
    ### them cmopletely in your plugin's implementation.  Alternatively, call them from your
    ### plugin before or after you've done etra things that you need to.
    ### in order for them to work, you need to have setup
    # self.translation_context
    # self.plugin_text_short # eg "Image" for the image plugin
    # self.config_section - where the items in the media manager are stored
    #   this could potentially be self.plugin_text_short.lower()
    
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
            translate(self.translation_context, u'Load '+self.plugin_text_short),
            translate(self.translation_context, u'Load item into openlp.org'),
            u':/images/image_load.png', self.onNewClick, u'ImageNewItem')
        ## Delete Song Button ##
        self.addToolbarButton(
            translate(self.translation_context, u'Delete '+self.plugin_text_short),
            translate(self.translation_context, u'Delete the selected item'),
            u':/images/image_delete.png', self.onDeleteClick, u'DeleteItem')
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview  Button ##
        self.addToolbarButton(
            translate(self.translation_context, u'Preview '+self.plugin_text_short),
            translate(self.translation_context, u'Preview the selected item'),
            u':/system/system_preview.png', self.onPreviewClick, u'PreviewItem')
        ## Live  Button ##
        self.addToolbarButton(
            translate(self.translation_context, u'Go Live'),
            translate(self.translation_context, u'Send the selected item live'),
            u':/system/system_live.png', self.onLiveClick, u'LiveItem')
        ## Add  Button ##
        self.addToolbarButton(
            translate(self.translation_context, u'Add '+self.plugin_text_short+u' To Service'),
            translate(self.translation_context, u'Add the selected item(s) to the service'),
            u':/system/system_add.png', self.onAddClick, self.plugin_text_short+u'AddItem')
        #Add the Image List widget
        self.ImageListView = ImageList()
        self.ImageListView.uniformItemSizes = True
        self.ImageListData = ListWithPreviews()
        self.ImageListView.setModel(self.ImageListData)
        self.ImageListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.ImageListView.setSpacing(1)
        self.ImageListView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.ImageListView.setAlternatingRowColors(True)
        self.ImageListView.setDragEnabled(True)
        self.ImageListView.setObjectName(self.plugin_text_short+u'ListView')
        self.PageLayout.addWidget(self.ImageListView)
        #define and add the context menu
        self.ImageListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ImageListView.addAction(self.contextMenuAction(
            self.ImageListView, ':/system/system_preview.png',
            translate(self.translation_context, u'&Preview '+self.plugin_text_short),
            self.onPreviewClick))
        self.ImageListView.addAction(self.contextMenuAction(
            self.ImageListView, ':/system/system_live.png',
            translate(self.translation_context, u'&Show Live'),
            self.onLiveClick))
        self.ImageListView.addAction(self.contextMenuAction(
            self.ImageListView, ':/system/system_add.png',
            translate(self.translation_context, u'&Add to Service'),
            self.onAddClick))
        QtCore.QObject.connect(self.ImageListView,
           QtCore.SIGNAL(u'doubleClicked(QModelIndex)'), self.onPreviewClick)

    def initialise(self):
        self.loadList(self.parent.config.load_list(self.config_section))

    def onNewClick(self):
        files = QtGui.QFileDialog.getOpenFileNames(None,
            translate(self.translation_context, self.on_new_prompt),
            self.parent.config.get_last_dir(),
            self.on_new_file_masks)
        log.info(u'New files(s)', unicode(files))
        if len(files) > 0:
            self.loadList(files)
            dir, filename = os.path.split(unicode(files[0]))
            self.parent.config.set_last_dir(dir)
            self.parent.config.set_list(self.config_section, self.ImageListData.getFileList())

    def loadList(self, list):
        for file in list:
            self.ImageListData.addRow(file)

    def onDeleteClick(self):
        indexes = self.ImageListView.selectedIndexes()
        for index in indexes:
            current_row = int(index.row())
            self.ImageListData.removeRow(current_row)
        self.parent.config.set_list(self.config_section, self.ImageListData.getFileList())

    def generateSlideData(self):
        assert (0, 'This fn needs to be defined by the plugin');

    def onPreviewClick(self):
        log.debug(self.plugin_text_short+u'Preview Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon(u':/media/media_image.png')
        self.generateSlideData(service_item)
        self.parent.preview_controller.addServiceItem(service_item)

    def onLiveClick(self):
        log.debug(self.plugin_text_short+u' Live Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon(u':/media/media_image.png')
        self.generateSlideData(service_item)
        self.parent.live_controller.addServiceItem(service_item)

    def onAddClick(self):
        log.debug(self.plugin_text_short+u' Add Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon(u':/media/media_image.png')
        self.generateSlideData(service_item)
        self.parent.service_manager.addServiceItem(service_item)
