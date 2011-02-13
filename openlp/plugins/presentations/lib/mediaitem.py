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

import logging
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import MediaManagerItem, build_icon, SettingsManager, \
    translate, check_item_selected, Receiver, ItemCapabilities
from openlp.core.lib.ui import UiStrings, critical_error_message_box, \
    media_item_combo_box
from openlp.plugins.presentations.lib import MessageListener

log = logging.getLogger(__name__)

class PresentationMediaItem(MediaManagerItem):
    """
    This is the Presentation media manager item for Presentation Items.
    It can present files using Openoffice and Powerpoint
    """
    log.info(u'Presentations Media Item loaded')

    def __init__(self, parent, icon, title, controllers):
        """
        Constructor. Setup defaults
        """
        self.controllers = controllers
        self.IconPath = u'presentations/presentation'
        self.Automatic = u''
        MediaManagerItem.__init__(self, parent, self, icon)
        self.message_listener = MessageListener(self)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'mediaitem_presentation_rebuild'), self.rebuild)

    def retranslateUi(self):
        """
        The name of the plugin media displayed in UI
        """
        self.OnNewPrompt = translate('PresentationPlugin.MediaItem',
            'Select Presentation(s)')
        self.Automatic = translate('PresentationPlugin.MediaItem',
            'Automatic')
        self.displayTypeLabel.setText(
            translate('PresentationPlugin.MediaItem', 'Present using:'))

    def buildFileMaskString(self):
        """
        Build the list of file extensions to be used in the Open file dialog
        """
        fileType = u''
        for controller in self.controllers:
            if self.controllers[controller].enabled():
                types = self.controllers[controller].supports + \
                    self.controllers[controller].alsosupports
                for type in types:
                    if fileType.find(type) == -1:
                        fileType += u'*.%s ' % type
                        self.parent.serviceManager.supportedSuffixes(type)
        self.OnNewFileMasks = unicode(translate('PresentationPlugin.MediaItem',
            'Presentations (%s)')) % fileType

    def requiredIcons(self):
        """
        Set which icons the media manager tab should show
        """
        MediaManagerItem.requiredIcons(self)
        self.hasFileIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False

    def addEndHeaderBar(self):
        """
        Display custom media manager items for presentations
        """
        self.presentationWidget = QtGui.QWidget(self)
        self.presentationWidget.setObjectName(u'presentationWidget')
        self.displayLayout = QtGui.QFormLayout(self.presentationWidget)
        self.displayLayout.setMargin(self.displayLayout.spacing())
        self.displayLayout.setObjectName(u'displayLayout')
        self.displayTypeLabel = QtGui.QLabel(self.presentationWidget)
        self.displayTypeLabel.setObjectName(u'displayTypeLabel')
        self.displayTypeComboBox = media_item_combo_box(
            self.presentationWidget, u'displayTypeComboBox')
        self.displayTypeLabel.setBuddy(self.displayTypeComboBox)
        self.displayLayout.addRow(self.displayTypeLabel,
            self.displayTypeComboBox)
        # Add the Presentation widget to the page layout
        self.pageLayout.addWidget(self.presentationWidget)

    def initialise(self):
        """
        Populate the media manager tab
        """
        self.listView.setIconSize(QtCore.QSize(88, 50))
        list = SettingsManager.load_list(
            self.settingsSection, u'presentations')
        self.loadList(list, True)
        self.populateDisplayTypes()

    def rebuild(self):
        """
        Rebuild the tab in the media manager when changes are made in
        the settings
        """
        self.populateDisplayTypes()
        self.buildFileMaskString()

    def populateDisplayTypes(self):
        """
        Load the combobox with the enabled presentation controllers,
        allowing user to select a specific app if settings allow
        """
        self.displayTypeComboBox.clear()
        for item in self.controllers:
            # load the drop down selection
            if self.controllers[item].enabled():
                self.displayTypeComboBox.addItem(item)
        if self.displayTypeComboBox.count() > 1:
            self.displayTypeComboBox.insertItem(0, self.Automatic)
            self.displayTypeComboBox.setCurrentIndex(0)
        if QtCore.QSettings().value(self.settingsSection + u'/override app',
            QtCore.QVariant(QtCore.Qt.Unchecked)) == QtCore.Qt.Checked:
            self.presentationWidget.show()
        else:
            self.presentationWidget.hide()

    def loadList(self, list, initialLoad=False):
        """
        Add presentations into the media manager
        This is called both on initial load of the plugin to populate with
        existing files, and when the user adds new files via the media manager
        """
        currlist = self.getFileList()
        titles = []
        for file in currlist:
            titles.append(os.path.split(file)[1])
        for file in list:
            if currlist.count(file) > 0:
                continue
            filename = os.path.split(unicode(file))[1]
            if titles.count(filename) > 0:
                if not initialLoad:
                    critical_error_message_box(
                        translate('PresentationPlugin.MediaItem',
                        'File Exists'),
                        translate('PresentationPlugin.MediaItem',
                        'A presentation with that filename already exists.'))
                continue
            controller_name = self.findControllerByType(filename)
            if controller_name:
                controller = self.controllers[controller_name]
                doc = controller.add_document(unicode(file))
                thumb = os.path.join(doc.get_thumbnail_folder(), u'icon.png')
                preview = doc.get_thumbnail_path(1, True)
                if not preview and not initialLoad:
                    doc.load_presentation()
                    preview = doc.get_thumbnail_path(1, True)
                doc.close_presentation()
                if preview and self.validate(preview, thumb):
                    icon = build_icon(thumb)
                else:
                    icon = build_icon(u':/general/general_delete.png')
            else:
                if initialLoad:
                    icon = build_icon(u':/general/general_delete.png')
                else:
                    critical_error_message_box(
                        self, translate('PresentationPlugin.MediaItem',
                        'Unsupported File'),
                        translate('PresentationPlugin.MediaItem',
                        'This type of presentation is not supported.'))
                    continue
            item_name = QtGui.QListWidgetItem(filename)
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(file))
            item_name.setIcon(icon)
            self.listView.addItem(item_name)

    def onDeleteClick(self):
        """
        Remove a presentation item from the list
        """
        if check_item_selected(self.listView, UiStrings.SelectDelete):
            items = self.listView.selectedIndexes()
            row_list = [item.row() for item in items]
            row_list.sort(reverse=True)
            for item in items:
                filepath = unicode(item.data(
                    QtCore.Qt.UserRole).toString())
                for cidx in self.controllers:
                    doc = self.controllers[cidx].add_document(filepath)
                    doc.presentation_deleted()
                    doc.close_presentation()
            for row in row_list:
                self.listView.takeItem(row)
            SettingsManager.set_list(self.settingsSection,
                self.settingsSection, self.getFileList())

    def generateSlideData(self, service_item, item=None, xmlVersion=False):
        """
        Load the relevant information for displaying the presentation
        in the slidecontroller. In the case of powerpoints, an image
        for each slide
        """
        items = self.listView.selectedIndexes()
        if len(items) > 1:
            return False
        service_item.title = unicode(self.displayTypeComboBox.currentText())
        service_item.shortname = unicode(self.displayTypeComboBox.currentText())
        service_item.add_capability(ItemCapabilities.ProvidesOwnDisplay)
        service_item.add_capability(ItemCapabilities.AllowsDetailedTitleDisplay)
        shortname = service_item.shortname
        if shortname:
            for item in items:
                bitem = self.listView.item(item.row())
                filename = unicode(bitem.data(QtCore.Qt.UserRole).toString())
                if os.path.exists(filename):
                    if shortname == self.Automatic:
                        service_item.shortname = \
                            self.findControllerByType(filename)
                        if not service_item.shortname:
                            return False
                    controller = self.controllers[service_item.shortname]
                    (path, name) = os.path.split(filename)
                    doc = controller.add_document(filename)
                    if doc.get_thumbnail_path(1, True) is None:
                        doc.load_presentation()
                    i = 1
                    img = doc.get_thumbnail_path(i, True)
                    if img:
                        while img:
                            service_item.add_from_command(path, name, img)
                            i = i + 1
                            img = doc.get_thumbnail_path(i, True)
                        doc.close_presentation()
                        return True
                    else:
                        # File is no longer present
                        critical_error_message_box(
                            translate('PresentationPlugin.MediaItem',
                            'Missing Presentation'),
                            unicode(translate('PresentationPlugin.MediaItem',
                            'The Presentation %s is incomplete,'
                            ' please reload.')) % filename)
                        return False
                else:
                    # File is no longer present
                    critical_error_message_box(
                        translate('PresentationPlugin.MediaItem',
                        'Missing Presentation'),
                        unicode(translate('PresentationPlugin.MediaItem',
                        'The Presentation %s no longer exists.')) % filename)
                    return False
        else:
            return False

    def findControllerByType(self, filename):
        """
        Determine the default application controller to use for the selected
        file type. This is used if "Automatic" is set as the preferred
        controller. Find the first (alphabetic) enabled controller which
        "supports" the extension. If none found, then look for a controller
        which "also supports" it instead.
        """
        filetype = filename.split(u'.')[1]
        if not filetype:
            return None
        for controller in self.controllers:
            if self.controllers[controller].enabled():
                if filetype in self.controllers[controller].supports:
                    return controller
        for controller in self.controllers:
            if self.controllers[controller].enabled():
                if filetype in self.controllers[controller].alsosupports:
                    return controller
        return None
