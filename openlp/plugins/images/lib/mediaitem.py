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

from openlp.core.lib import MediaManagerItem, build_icon, ItemCapabilities, SettingsManager, translate, \
    check_item_selected, check_directory_exists, Receiver, create_thumb, validate_thumb, ServiceItemContext, Settings, \
    UiStrings
from openlp.core.lib.ui import critical_error_message_box
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
        self.choosegroupform = ChooseGroupForm(self)
        self.addgroupform = AddGroupForm(self)
        self.fillGroupsComboBox(self.choosegroupform.groupComboBox)
        self.fillGroupsComboBox(self.addgroupform.parentGroupComboBox)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'live_theme_changed'), self.liveThemeChanged)
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
        self.listView.doInternalDnD(True)
        self.servicePath = os.path.join(AppLocation.get_section_data_path(self.settingsSection), u'thumbnails')
        check_directory_exists(self.servicePath)
        # Import old images list
        images_old = Settings().value(self.settingsSection +  u'/images files')
        if len(images_old) > 0:
            for imageFile in images_old:
                imagefilename = ImageFilenames()
                imagefilename.group_id = 0
                imagefilename.filename = imageFile
                success = self.manager.save_object(imagefilename)
            Settings().setValue(self.settingsSection + u'/images files', [])
            Settings().remove(self.settingsSection + u'/images files')
            Settings().remove(self.settingsSection + u'/images count')
        # Load images from the database
        self.loadFullList(self.manager.get_all_objects(ImageFilenames, order_by_ref=ImageFilenames.filename), True)

    def addListViewToToolBar(self):
        MediaManagerItem.addListViewToToolBar(self)
        self.listView.addAction(self.replaceAction)

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
        if check_item_selected(self.listView, translate('ImagePlugin.MediaItem','You must select an image to delete.')):
            item_list = self.listView.selectedItems()
            Receiver.send_message(u'cursor_busy')
            self.main_window.displayProgressBar(len(item_list))
            for row_item in item_list:
                if row_item:
                    item_data = row_item.data(0, QtCore.Qt.UserRole)
                    if isinstance(item_data, ImageFilenames):
                        delete_file(os.path.join(self.servicePath, row_item.text(0)))
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
                            self.fillGroupsComboBox(self.choosegroupform.groupComboBox)
                            self.fillGroupsComboBox(self.addgroupform.parentGroupComboBox)
                self.main_window.incrementProgressBar()
            self.main_window.finishedProgressBar()
            Receiver.send_message(u'cursor_normal')
        self.listView.blockSignals(False)

    def addSubGroups(self, groupList, parentGroupId):
        """
        Recursively add subgroups to the given parent group
        """
        image_groups = self.manager.get_all_objects(ImageGroups, ImageGroups.parent_id == parentGroupId)
        image_groups.sort(cmp=locale_compare, key=lambda group_object: group_object.group_name)
        for image_group in image_groups:
            group = QtGui.QTreeWidgetItem()
            group.setText(0, image_group.group_name)
            group.setData(0, QtCore.Qt.UserRole, image_group)
            if parentGroupId is 0:
                self.listView.addTopLevelItem(group)
            else:
                groupList[parentGroupId].addChild(group)
            groupList[image_group.id] = group
            self.addSubGroups(groupList, image_group.id)

    def fillGroupsComboBox(self, comboBox, parentGroupId=0, prefix=''):
        """
        Recursively add groups to the combobox in the 'Add group' dialog
        """
        if parentGroupId is 0:
            comboBox.clear()
            comboBox.topLevelGroupAdded = False
        image_groups = self.manager.get_all_objects(ImageGroups, ImageGroups.parent_id == parentGroupId)
        image_groups.sort(cmp=locale_compare, key=lambda group_object: group_object.group_name)
        for image_group in image_groups:
            comboBox.addItem(prefix+image_group.group_name, image_group.id)
            self.fillGroupsComboBox(comboBox, image_group.id, prefix+'   ')

    def loadFullList(self, images, initialLoad=False):
        """
        Replace the list of images and groups in the interface.
        """
        if not initialLoad:
            Receiver.send_message(u'cursor_busy')
            self.main_window.displayProgressBar(len(images))
        self.listView.clear()
        # Load the list of groups and add them to the treeView
        group_items = {}
        self.addSubGroups(group_items, 0)
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
                if 0 not in group_items:
                    # The 'Imported' group is only displayed when there are files that were imported from the
                    # configuration file
                    imported_group = QtGui.QTreeWidgetItem()
                    imported_group.setText(0, translate('ImagePlugin.MediaItem', 'Imported'))
                    self.listView.insertTopLevelItem(0, imported_group)
                    group_items[0] = imported_group
            group_items[imageFile.group_id].addChild(item_name)
            if not initialLoad:
                self.main_window.incrementProgressBar()
        if not initialLoad:
            self.main_window.finishedProgressBar()
            Receiver.send_message(u'cursor_normal')

    def loadList(self, images, target_group=None, initialLoad=False):
        """
        Add new images to the database. This method is called when adding images using the Add button or DnD.
        """
        if target_group is None:
            # Ask which group the images should be saved in
            if self.choosegroupform.exec_():
                group_id = self.choosegroupform.groupComboBox.itemData(
                    self.choosegroupform.groupComboBox.currentIndex(), QtCore.Qt.UserRole)
            parent_group = self.manager.get_object_filtered(ImageGroups, ImageGroups.id == group_id)
        else:
            parent_group = target_group.data(0, QtCore.Qt.UserRole)
            if isinstance(parent_group, ImageFilenames):
                parent_group = target_group.parent().data(0, QtCore.Qt.UserRole)
        # If no valid parent group is found, do nothing
        if not isinstance(parent_group, ImageGroups):
            return
        # Save the new images in the database
        for filename in images:
            if type(filename) is not str and type(filename) is not unicode:
                continue
            log.debug(u'Adding new image: %s', filename)
            imageFile = ImageFilenames()
            imageFile.group_id = parent_group.id
            imageFile.filename = unicode(filename)
            success = self.manager.save_object(imageFile)
        self.loadFullList(self.manager.get_all_objects(ImageFilenames, order_by_ref=ImageFilenames.filename),
            initialLoad)

    def dndMoveInternal(self, target):
        """
        Handle drag-and-drop moving of images within the media manager
        """
        items_to_move = self.listView.selectedItems()
        # Determine group to move images to
        target_group = target
        if isinstance(target_group.data(0, QtCore.Qt.UserRole), ImageFilenames):
            target_group = target.parent()
        # Don't allow moving to the Imported group
        if target_group.data(0, QtCore.Qt.UserRole) is None:
            return
        # Move images in the treeview
        items_to_save = []
        for item in items_to_move:
            if isinstance(item.data(0, QtCore.Qt.UserRole), ImageFilenames):
                item.parent().removeChild(item)
                target_group.addChild(item)
                item_data = item.data(0, QtCore.Qt.UserRole)
                item_data.group_id = target_group.data(0, QtCore.Qt.UserRole).id
                items_to_save.append(item_data)
        target_group.sortChildren(0, QtCore.Qt.AscendingOrder)
        # Update the group ID's of the images in the database
        self.manager.save_objects(items_to_save)

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
        if self.addgroupform.exec_(showTopLevelGroup=True):
            new_group = ImageGroups.populate(parent_id=self.addgroupform.parentGroupComboBox.itemData(
                self.addgroupform.parentGroupComboBox.currentIndex(), QtCore.Qt.UserRole),
                group_name=self.addgroupform.nameEdit.text())
            if self.checkGroupName(new_group):
                if self.manager.save_object(new_group):
                    self.loadFullList(self.manager.get_all_objects(ImageFilenames,
                        order_by_ref=ImageFilenames.filename))
                    self.fillGroupsComboBox(self.choosegroupform.groupComboBox)
                    self.fillGroupsComboBox(self.addgroupform.parentGroupComboBox)
                else:
                    critical_error_message_box(
                        message=translate('ImagePlugin.AddGroupForm', 'Could not add the new group.'))
            else:
                critical_error_message_box(
                    message=translate('ImagePlugin.AddGroupForm', 'This group already exists.'))

    def onResetClick(self):
        """
        Called to reset the Live backgound with the image selected,
        """
        self.resetAction.setVisible(False)
        self.plugin.liveController.display.resetImage()

    def liveThemeChanged(self):
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
            filename = bitem.data(0, QtCore.Qt.UserRole).filename
            if os.path.exists(filename):
                if self.plugin.liveController.display.directImage(filename, background):
                    self.resetAction.setVisible(True)
                else:
                    critical_error_message_box(UiStrings().LiveBGError,
                        translate('ImagePlugin.MediaItem', 'There was no display item to amend.'))
            else:
                critical_error_message_box(UiStrings().LiveBGError,
                    translate('ImagePlugin.MediaItem', 'There was a problem replacing your background, '
                        'the image file "%s" no longer exists.') % filename)

    def search(self, string, showError):
        files = self.manager.get_all_objects(ImageFilenames, filter_clause=ImageFilenames.filename.contains(string), order_by_ref=ImageFilenames.filename)
        results = []
        for file in files:
            filename = os.path.split(unicode(file.filename))[1]
            results.append([file.filename, filename])
        return results
