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

import logging
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import ItemCapabilities, MediaManagerItem, Registry, ServiceItemContext, Settings, \
    StringContent, TreeWidgetWithDnD, UiStrings, build_icon, check_directory_exists, check_item_selected, \
    create_thumb, translate, validate_thumb
from openlp.core.lib.ui import create_widget_action, critical_error_message_box
from openlp.core.utils import AppLocation, delete_file, locale_compare, get_images_filter
from openlp.plugins.images.forms import AddGroupForm, ChooseGroupForm
from openlp.plugins.images.lib.db import ImageFilenames, ImageGroups

log = logging.getLogger(__name__)


class ImageMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for images.
    """
    log.info(u'Image Media Item loaded')

    def __init__(self, parent, plugin, icon):
        self.IconPath = u'images/image'
        MediaManagerItem.__init__(self, parent, plugin, icon)
        self.quickPreviewAllowed = True
        self.hasSearch = True
        self.manager = plugin.manager
        self.choose_group_form = ChooseGroupForm(self)
        self.add_group_form = AddGroupForm(self)
        self.fill_groups_combobox(self.choose_group_form.group_combobox)
        self.fill_groups_combobox(self.add_group_form.parent_group_combobox)
        Registry().register_function(u'live_theme_changed', self.live_theme_changed)
        # Allow DnD from the desktop
        self.listView.activateDnD()

    def retranslateUi(self):
        self.onNewPrompt = translate('ImagePlugin.MediaItem',
            'Select Image(s)')
        file_formats = get_images_filter()
        self.onNewFileMasks = u'%s;;%s (*.*) (*)' % (file_formats, UiStrings().AllFiles)
        self.addGroupAction.setText(UiStrings().AddGroup)
        self.addGroupAction.setToolTip(UiStrings().AddGroup)
        self.replaceAction.setText(UiStrings().ReplaceBG)
        self.replaceAction.setToolTip(UiStrings().ReplaceLiveBG)
        self.resetAction.setText(UiStrings().ResetBG)
        self.resetAction.setToolTip(UiStrings().ResetLiveBG)

    def requiredIcons(self):
        MediaManagerItem.requiredIcons(self)
        self.hasFileIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False
        self.addToServiceItem = True

    def initialise(self):
        log.debug(u'initialise')
        self.listView.clear()
        self.listView.setIconSize(QtCore.QSize(88, 50))
        self.listView.setIndentation(self.listView.defaultIndentation)
        self.listView.allow_internal_dnd = True
        self.servicePath = os.path.join(AppLocation.get_section_data_path(self.settingsSection), u'thumbnails')
        check_directory_exists(self.servicePath)
        # Load images from the database
        self.loadFullList(
            self.manager.get_all_objects(ImageFilenames, order_by_ref=ImageFilenames.filename), initial_load=True)

    def addListViewToToolBar(self):
        """
        Creates the main widget for listing items the media item is tracking.
        This method overloads MediaManagerItem.addListViewToToolBar
        """
        # Add the List widget
        self.listView = TreeWidgetWithDnD(self, self.plugin.name)
        self.listView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listView.setAlternatingRowColors(True)
        self.listView.setObjectName(u'%sTreeView' % self.plugin.name)
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
            create_widget_action(self.listView, separator=True)
            create_widget_action(self.listView,
                text=translate('OpenLP.MediaManagerItem', '&Add to selected Service Item'),
                icon=u':/general/general_add.png',
                triggers=self.onAddEditClick)
        self.addCustomContextActions()
        # Create the context menu and add all actions from the listView.
        self.menu = QtGui.QMenu()
        self.menu.addActions(self.listView.actions())
        self.listView.doubleClicked.connect(self.onDoubleClicked)
        self.listView.itemSelectionChanged.connect(self.onSelectionChange)
        self.listView.customContextMenuRequested.connect(self.contextMenu)
        self.listView.addAction(self.replaceAction)

    def addCustomContextActions(self):
        create_widget_action(self.listView, separator=True)
        create_widget_action(self.listView,
            text=UiStrings().AddGroup,
            icon=u':/images/image_new_group.png',
            triggers=self.onAddGroupClick)
        create_widget_action(self.listView,
            text=self.plugin.getString(StringContent.Load)[u'tooltip'],
            icon=u':/general/general_open.png',
            triggers=self.onFileClick)

    def addStartHeaderBar(self):
        self.addGroupAction = self.toolbar.addToolbarAction(u'addGroupAction',
            icon=u':/images/image_new_group.png', triggers=self.onAddGroupClick)

    def addEndHeaderBar(self):
        self.replaceAction = self.toolbar.addToolbarAction(u'replaceAction',
            icon=u':/slides/slide_blank.png', triggers=self.onReplaceClick)
        self.resetAction = self.toolbar.addToolbarAction(u'resetAction',
            icon=u':/system/system_close.png', visible=False, triggers=self.onResetClick)

    def recursivelyDeleteGroup(self, image_group):
        """
        Recursively deletes a group and all groups and images in it
        """
        images = self.manager.get_all_objects(ImageFilenames, ImageFilenames.group_id == image_group.id)
        for image in images:
            delete_file(os.path.join(self.servicePath, os.path.split(image.filename)[1]))
            self.manager.delete_object(ImageFilenames, image.id)
        image_groups = self.manager.get_all_objects(ImageGroups, ImageGroups.parent_id == image_group.id)
        for group in image_groups:
            self.recursivelyDeleteGroup(group)
            self.manager.delete_object(ImageGroups, group.id)

    def onDeleteClick(self):
        """
        Remove an image item from the list
        """
        # Turn off auto preview triggers.
        self.listView.blockSignals(True)
        if check_item_selected(self.listView, translate('ImagePlugin.MediaItem',
            'You must select an image or group to delete.')):
            item_list = self.listView.selectedItems()
            self.application.set_busy_cursor()
            self.main_window.displayProgressBar(len(item_list))
            for row_item in item_list:
                if row_item:
                    item_data = row_item.data(0, QtCore.Qt.UserRole)
                    if isinstance(item_data, ImageFilenames):
                        delete_file(os.path.join(self.servicePath, row_item.text(0)))
                        if item_data.group_id == 0:
                            self.listView.takeTopLevelItem(self.listView.indexOfTopLevelItem(row_item))
                        else:
                            row_item.parent().removeChild(row_item)
                        self.manager.delete_object(ImageFilenames, row_item.data(0, QtCore.Qt.UserRole).id)
                    elif isinstance(item_data, ImageGroups):
                        if QtGui.QMessageBox.question(self.listView.parent(),
                            translate('ImagePlugin.MediaItem', 'Remove group'),
                            translate('ImagePlugin.MediaItem',
                            'Are you sure you want to remove "%s" and everything in it?') % item_data.group_name,
                            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes |
                            QtGui.QMessageBox.No)) == QtGui.QMessageBox.Yes:
                            self.recursivelyDeleteGroup(item_data)
                            self.manager.delete_object(ImageGroups, row_item.data(0, QtCore.Qt.UserRole).id)
                            if item_data.parent_id is 0:
                                self.listView.takeTopLevelItem(self.listView.indexOfTopLevelItem(row_item))
                            else:
                                row_item.parent().removeChild(row_item)
                            self.fill_groups_combobox(self.choose_group_form.group_combobox)
                            self.fill_groups_combobox(self.add_group_form.parent_group_combobox)
                self.main_window.incrementProgressBar()
            self.main_window.finishedProgressBar()
            self.application.set_normal_cursor()
        self.listView.blockSignals(False)

    def add_sub_groups(self, group_list, parent_group_id):
        """
        Recursively add subgroups to the given parent group in a QTreeWidget
        """
        image_groups = self.manager.get_all_objects(ImageGroups, ImageGroups.parent_id == parent_group_id)
        image_groups.sort(cmp=locale_compare, key=lambda group_object: group_object.group_name)
        folder_icon = build_icon(u':/images/image_group.png')
        for image_group in image_groups:
            group = QtGui.QTreeWidgetItem()
            group.setText(0, image_group.group_name)
            group.setData(0, QtCore.Qt.UserRole, image_group)
            group.setIcon(0, folder_icon)
            if parent_group_id is 0:
                self.listView.addTopLevelItem(group)
            else:
                group_list[parent_group_id].addChild(group)
            group_list[image_group.id] = group
            self.add_sub_groups(group_list, image_group.id)

    def fill_groups_combobox(self, combobox, parent_group_id=0, prefix=''):
        """
        Recursively add groups to the combobox in the 'Add group' dialog
        """
        if parent_group_id is 0:
            combobox.clear()
            combobox.top_level_group_added = False
        image_groups = self.manager.get_all_objects(ImageGroups, ImageGroups.parent_id == parent_group_id)
        image_groups.sort(cmp=locale_compare, key=lambda group_object: group_object.group_name)
        for image_group in image_groups:
            combobox.addItem(prefix + image_group.group_name, image_group.id)
            self.fill_groups_combobox(combobox, image_group.id, prefix + '   ')

    def expand_group(self, group_id, root_item=None):
        return_value = False
        if root_item is None:
            root_item = self.listView.invisibleRootItem()
        for i in range(root_item.childCount()):
            child = root_item.child(i)
            if self.expand_group(group_id, child):
                child.setExpanded(True)
                return_value = True
        if isinstance(root_item.data(0, QtCore.Qt.UserRole), ImageGroups):
            if root_item.data(0, QtCore.Qt.UserRole).id == group_id:
                return True
        return return_value

    def loadFullList(self, images, initial_load=False, open_group=None):
        """
        Replace the list of images and groups in the interface.
        """
        if not initial_load:
            self.application.set_busy_cursor()
            self.main_window.displayProgressBar(len(images))
        self.listView.clear()
        # Load the list of groups and add them to the treeView
        group_items = {}
        self.add_sub_groups(group_items, parent_group_id=0)
        if open_group is not None:
            self.expand_group(open_group.id)
        # Sort the images by its filename considering language specific
        # characters.
        images.sort(cmp=locale_compare, key=lambda image_object: os.path.split(unicode(image_object.filename))[1])
        for imageFile in images:
            log.debug(u'Loading image: %s', imageFile.filename)
            filename = os.path.split(imageFile.filename)[1]
            thumb = os.path.join(self.servicePath, filename)
            if not os.path.exists(imageFile.filename):
                icon = build_icon(u':/general/general_delete.png')
            else:
                if validate_thumb(imageFile.filename, thumb):
                    icon = build_icon(thumb)
                else:
                    icon = create_thumb(imageFile.filename, thumb)
            item_name = QtGui.QTreeWidgetItem(filename)
            item_name.setText(0, filename)
            item_name.setIcon(0, icon)
            item_name.setToolTip(0, imageFile.filename)
            item_name.setData(0, QtCore.Qt.UserRole, imageFile)
            if imageFile.group_id is 0:
                self.listView.addTopLevelItem(item_name)
            else:
                group_items[imageFile.group_id].addChild(item_name)
            if not initial_load:
                self.main_window.incrementProgressBar()
        if not initial_load:
            self.main_window.finishedProgressBar()
        self.application.set_normal_cursor()

    def validateAndLoad(self, files, target_group=None):
        """
        Process a list for files either from the File Dialog or from Drag and
        Drop. This method is overloaded from MediaManagerItem.

        ``files``
            The files to be loaded.
        """
        self.loadList(files, target_group)
        last_dir = os.path.split(unicode(files[0]))[0]
        Settings().setValue(self.settingsSection + u'/last directory', last_dir)

    def loadList(self, images, target_group=None, initial_load=False):
        """
        Add new images to the database. This method is called when adding images using the Add button or DnD.
        """
        self.application.set_busy_cursor()
        self.main_window.displayProgressBar(len(images))
        if target_group is None:
            # Find out if a group must be pre-selected
            preselect_group = None
            selected_items = self.listView.selectedItems()
            if len(selected_items) > 0:
                selected_item = selected_items[0]
                if isinstance(selected_item.data(0, QtCore.Qt.UserRole), ImageFilenames):
                    selected_item = selected_item.parent()
                if isinstance(selected_item, QtGui.QTreeWidgetItem):
                    if isinstance(selected_item.data(0, QtCore.Qt.UserRole), ImageGroups):
                        preselect_group = selected_item.data(0, QtCore.Qt.UserRole).id
            # Enable and disable parts of the 'choose group' form
            if preselect_group is None:
                self.choose_group_form.nogroup_radio_button.setChecked(True)
                self.choose_group_form.nogroup_radio_button.setFocus()
                self.choose_group_form.existing_radio_button.setChecked(False)
                self.choose_group_form.new_radio_button.setChecked(False)
            else:
                self.choose_group_form.nogroup_radio_button.setChecked(False)
                self.choose_group_form.existing_radio_button.setChecked(True)
                self.choose_group_form.new_radio_button.setChecked(False)
                self.choose_group_form.group_combobox.setFocus()
            if self.manager.get_object_count(ImageGroups) == 0:
                self.choose_group_form.existing_radio_button.setDisabled(True)
                self.choose_group_form.group_combobox.setDisabled(True)
            else:
                self.choose_group_form.existing_radio_button.setDisabled(False)
                self.choose_group_form.group_combobox.setDisabled(False)
            # Ask which group the images should be saved in
            if self.choose_group_form.exec_(selected_group=preselect_group):
                if self.choose_group_form.nogroup_radio_button.isChecked():
                    # User chose 'No group'
                    parent_group = ImageGroups()
                    parent_group.id = 0
                elif self.choose_group_form.existing_radio_button.isChecked():
                    # User chose 'Existing group'
                    group_id = self.choose_group_form.group_combobox.itemData(
                        self.choose_group_form.group_combobox.currentIndex(), QtCore.Qt.UserRole)
                    parent_group = self.manager.get_object_filtered(ImageGroups, ImageGroups.id == group_id)
                elif self.choose_group_form.new_radio_button.isChecked():
                    # User chose 'New group'
                    parent_group = ImageGroups()
                    parent_group.parent_id = 0
                    parent_group.group_name = self.choose_group_form.new_group_edit.text()
                    self.manager.save_object(parent_group)
        else:
            parent_group = target_group.data(0, QtCore.Qt.UserRole)
            if isinstance(parent_group, ImageFilenames):
                if parent_group.group_id == 0:
                    parent_group = ImageGroups()
                    parent_group.id = 0
                else:
                    parent_group = target_group.parent().data(0, QtCore.Qt.UserRole)
        # If no valid parent group is found, do nothing
        if not isinstance(parent_group, ImageGroups):
            return
        # Save the new images in the database
        self.save_new_images_list(images, group_id=parent_group.id, reload_list=False)
        self.loadFullList(self.manager.get_all_objects(ImageFilenames, order_by_ref=ImageFilenames.filename),
            initial_load=initial_load, open_group=parent_group)

    def save_new_images_list(self, images_list, group_id=0, reload_list=True):
        for filename in images_list:
            if type(filename) is not str and type(filename) is not unicode:
                continue
            log.debug(u'Adding new image: %s', filename)
            imageFile = ImageFilenames()
            imageFile.group_id = group_id
            imageFile.filename = unicode(filename)
            self.manager.save_object(imageFile)
            self.main_window.incrementProgressBar()
        if reload_list:
            self.loadFullList(self.manager.get_all_objects(ImageFilenames, order_by_ref=ImageFilenames.filename))

    def dnd_move_internal(self, target):
        """
        Handle drag-and-drop moving of images within the media manager
        """
        items_to_move = self.listView.selectedItems()
        # Determine group to move images to
        target_group = target
        if target_group is not None and isinstance(target_group.data(0, QtCore.Qt.UserRole), ImageFilenames):
            target_group = target.parent()
        # Move to toplevel
        if target_group is None:
            target_group = self.listView.invisibleRootItem()
            target_group.setData(0, QtCore.Qt.UserRole, ImageGroups())
            target_group.data(0, QtCore.Qt.UserRole).id = 0
        # Move images in the treeview
        items_to_save = []
        for item in items_to_move:
            if isinstance(item.data(0, QtCore.Qt.UserRole), ImageFilenames):
                if isinstance(item.parent(), QtGui.QTreeWidgetItem):
                    item.parent().removeChild(item)
                else:
                    self.listView.invisibleRootItem().removeChild(item)
                target_group.addChild(item)
                item.setSelected(True)
                item_data = item.data(0, QtCore.Qt.UserRole)
                item_data.group_id = target_group.data(0, QtCore.Qt.UserRole).id
                items_to_save.append(item_data)
        target_group.setExpanded(True)
        # Update the group ID's of the images in the database
        self.manager.save_objects(items_to_save)
        # Sort the target group
        group_items = []
        image_items = []
        for item in target_group.takeChildren():
            if isinstance(item.data(0, QtCore.Qt.UserRole), ImageGroups):
                group_items.append(item)
            if isinstance(item.data(0, QtCore.Qt.UserRole), ImageFilenames):
                image_items.append(item)
        group_items.sort(cmp=locale_compare, key=lambda item: item.text(0))
        target_group.addChildren(group_items)
        image_items.sort(cmp=locale_compare, key=lambda item: item.text(0))
        target_group.addChildren(image_items)

    def generateSlideData(self, service_item, item=None, xmlVersion=False,
        remote=False, context=ServiceItemContext.Service):
        background = QtGui.QColor(Settings().value(self.settingsSection + u'/background color'))
        if item:
            items = [item]
        else:
            items = self.listView.selectedItems()
            if not items:
                return False
        # Determine service item title
        if isinstance(items[0].data(0, QtCore.Qt.UserRole), ImageGroups):
            service_item.title = items[0].text(0)
        else:
            service_item.title = unicode(self.plugin.nameStrings[u'plural'])
        service_item.add_capability(ItemCapabilities.CanMaintain)
        service_item.add_capability(ItemCapabilities.CanPreview)
        service_item.add_capability(ItemCapabilities.CanLoop)
        service_item.add_capability(ItemCapabilities.CanAppend)
        # force a nonexistent theme
        service_item.theme = -1
        missing_items = []
        missing_items_filenames = []
        # Expand groups to images
        for bitem in items:
            if isinstance(bitem.data(0, QtCore.Qt.UserRole), ImageGroups) or bitem.data(0, QtCore.Qt.UserRole) is None:
                for index in range(0, bitem.childCount()):
                    if isinstance(bitem.child(index).data(0, QtCore.Qt.UserRole), ImageFilenames):
                        items.append(bitem.child(index))
                items.remove(bitem)
        # Don't try to display empty groups
        if not items:
            return False
        # Find missing files
        for bitem in items:
            filename = bitem.data(0, QtCore.Qt.UserRole).filename
            if not os.path.exists(filename):
                missing_items.append(bitem)
                missing_items_filenames.append(filename)
        for item in missing_items:
            items.remove(item)
        # We cannot continue, as all images do not exist.
        if not items:
            if not remote:
                critical_error_message_box(
                    translate('ImagePlugin.MediaItem', 'Missing Image(s)'),
                    translate('ImagePlugin.MediaItem', 'The following image(s) no longer exist: %s') %
                        u'\n'.join(missing_items_filenames))
            return False
        # We have missing as well as existing images. We ask what to do.
        elif missing_items and QtGui.QMessageBox.question(self,
            translate('ImagePlugin.MediaItem', 'Missing Image(s)'),
            translate('ImagePlugin.MediaItem', 'The following image(s) no longer exist: %s\n'
                'Do you want to add the other images anyway?') % u'\n'.join(missing_items_filenames),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)) == QtGui.QMessageBox.No:
            return False
        # Continue with the existing images.
        for bitem in items:
            filename = bitem.data(0, QtCore.Qt.UserRole).filename
            name = os.path.split(filename)[1]
            service_item.add_from_image(filename, name, background)
        return True

    def __checkObject(self, objects, newObject, edit):
        """
        Utility method to check for an existing object.

        ``edit``
            If we edit an item, this should be *True*.
        """
        if objects:
            # If we edit an existing object, we need to make sure that we do
            # not return False when nothing has changed.
            if edit:
                for object in objects:
                    if object.id != newObject.id:
                        return False
                return True
            else:
                return False
        else:
            return True

    def checkGroupName(self, newGroup, edit=False):
        """
        Returns *False* if the given Group already exists, otherwise *True*.
        """
        groups = self.manager.get_all_objects(ImageGroups, ImageGroups.group_name == newGroup.group_name)
        return self.__checkObject(groups, newGroup, edit)

    def onAddGroupClick(self):
        """
        Called to add a new group
        """
        # Find out if a group must be pre-selected
        preselect_group = 0
        selected_items = self.listView.selectedItems()
        if len(selected_items) > 0:
            selected_item = selected_items[0]
            if isinstance(selected_item.data(0, QtCore.Qt.UserRole), ImageFilenames):
                selected_item = selected_item.parent()
            if isinstance(selected_item, QtGui.QTreeWidgetItem):
                if isinstance(selected_item.data(0, QtCore.Qt.UserRole), ImageGroups):
                    preselect_group = selected_item.data(0, QtCore.Qt.UserRole).id
        # Show 'add group' dialog
        if self.add_group_form.exec_(show_top_level_group=True, selected_group=preselect_group):
            new_group = ImageGroups.populate(parent_id=self.add_group_form.parent_group_combobox.itemData(
                self.add_group_form.parent_group_combobox.currentIndex(), QtCore.Qt.UserRole),
                group_name=self.add_group_form.name_edit.text())
            if self.checkGroupName(new_group):
                if self.manager.save_object(new_group):
                    self.loadFullList(self.manager.get_all_objects(ImageFilenames,
                        order_by_ref=ImageFilenames.filename))
                    self.fill_groups_combobox(self.choose_group_form.group_combobox)
                    self.fill_groups_combobox(self.add_group_form.parent_group_combobox)
                else:
                    critical_error_message_box(
                        message=translate('ImagePlugin.AddGroupForm', 'Could not add the new group.'))
            else:
                critical_error_message_box(
                    message=translate('ImagePlugin.AddGroupForm', 'This group already exists.'))

    def onResetClick(self):
        """
        Called to reset the Live background with the image selected,
        """
        self.resetAction.setVisible(False)
        self.live_controller.display.reset_image()

    def live_theme_changed(self):
        """
        Triggered by the change of theme in the slide controller
        """
        self.resetAction.setVisible(False)

    def onReplaceClick(self):
        """
        Called to replace Live backgound with the image selected.
        """
        if check_item_selected(self.listView,
                translate('ImagePlugin.MediaItem', 'You must select an image to replace the background with.')):
            background = QtGui.QColor(Settings().value(self.settingsSection + u'/background color'))
            bitem = self.listView.selectedItems()[0]
            if not isinstance(bitem.data(0, QtCore.Qt.UserRole), ImageFilenames):
                # Only continue when an image is selected
                return
            filename = bitem.data(0, QtCore.Qt.UserRole).filename
            if os.path.exists(filename):
                if self.live_controller.display.direct_image(filename, background):
                    self.resetAction.setVisible(True)
                else:
                    critical_error_message_box(UiStrings().LiveBGError,
                        translate('ImagePlugin.MediaItem', 'There was no display item to amend.'))
            else:
                critical_error_message_box(UiStrings().LiveBGError,
                    translate('ImagePlugin.MediaItem', 'There was a problem replacing your background, '
                        'the image file "%s" no longer exists.') % filename)

    def search(self, string, showError):
        files = self.manager.get_all_objects(ImageFilenames, filter_clause=ImageFilenames.filename.contains(string),
            order_by_ref=ImageFilenames.filename)
        results = []
        for file_object in files:
            filename = os.path.split(unicode(file_object.filename))[1]
            results.append([file_object.filename, filename])
        return results
