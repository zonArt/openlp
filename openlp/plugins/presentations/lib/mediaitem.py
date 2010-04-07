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

from openlp.core.lib import MediaManagerItem, BaseListWithDnD
from openlp.plugins.presentations.lib import MessageListener

log = logging.getLogger(__name__)

# We have to explicitly create separate classes for each plugin
# in order for DnD to the Service manager to work correctly.
class PresentationListView(BaseListWithDnD):
    def __init__(self, parent=None):
        self.PluginName = u'Presentations'
        BaseListWithDnD.__init__(self, parent)

class PresentationMediaItem(MediaManagerItem):
    """
    This is the Presentation media manager item for Presentation Items.
    It can present files using Openoffice
    """
    log.info(u'Presentations Media Item loaded')

    def __init__(self, parent, icon, title, controllers):
        self.controllers = controllers
        self.PluginNameShort = u'Presentation'
        self.ConfigSection = title
        self.IconPath = u'presentations/presentation'
        self.Automatic = u''
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = PresentationListView
        MediaManagerItem.__init__(self, parent, icon, title)
        self.message_listener = MessageListener(self)

    def initPluginNameVisible(self):
        self.PluginNameVisible = self.trUtf8('Presentation')

    def retranslateUi(self):
        self.OnNewPrompt = self.trUtf8('Select Presentation(s)')
        self.Automatic = self.trUtf8('Automatic')
        fileType = u''
        for controller in self.controllers:
            if self.controllers[controller].enabled:
                types = self.controllers[controller].supports + self.controllers[controller].alsosupports
                for type in types:
                    if fileType.find(type) == -1:
                        fileType += u'*%s ' % type
        self.OnNewFileMasks = self.trUtf8('Presentations (%s)' % fileType)

    def requiredIcons(self):
        MediaManagerItem.requiredIcons(self)
        self.hasFileIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False

    def addEndHeaderBar(self):
        self.PresentationWidget = QtGui.QWidget(self)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.PresentationWidget.sizePolicy().hasHeightForWidth())
        self.PresentationWidget.setSizePolicy(sizePolicy)
        self.PresentationWidget.setObjectName(u'PresentationWidget')
        self.DisplayLayout = QtGui.QGridLayout(self.PresentationWidget)
        self.DisplayLayout.setObjectName(u'DisplayLayout')
        self.DisplayTypeComboBox = QtGui.QComboBox(self.PresentationWidget)
        self.DisplayTypeComboBox.setObjectName(u'DisplayTypeComboBox')
        self.DisplayLayout.addWidget(self.DisplayTypeComboBox, 0, 1, 1, 2)
        self.DisplayTypeLabel = QtGui.QLabel(self.PresentationWidget)
        self.DisplayTypeLabel.setObjectName(u'SearchTypeLabel')
        self.DisplayLayout.addWidget(self.DisplayTypeLabel, 0, 0, 1, 1)
        self.DisplayTypeLabel.setText(self.trUtf8('Present using:'))
        # Add the Presentation widget to the page layout
        self.PageLayout.addWidget(self.PresentationWidget)

    def initialise(self):
        list = self.parent.config.load_list(u'presentations')
        self.loadList(list)
        for item in self.controllers:
            #load the drop down selection
            if self.controllers[item].enabled:
                self.DisplayTypeComboBox.addItem(item)
        if self.DisplayTypeComboBox.count() > 1:
            self.DisplayTypeComboBox.insertItem(0, self.Automatic)
            self.DisplayTypeComboBox.setCurrentIndex(0)

    def loadList(self, list):
        currlist = self.getFileList()
        titles = []
        for file in currlist:
            titles.append(os.path.split(file)[1])
        for file in list:
            if currlist.count(file) > 0:
                continue
            (path, filename) = os.path.split(unicode(file))
            if titles.count(filename) > 0:
                QtGui.QMessageBox.critical(
                    self, self.trUtf8('File exists'), self.trUtf8(
                        'A presentation with that filename already exists.'),
                    QtGui.QMessageBox.Ok)
            else:
                item_name = QtGui.QListWidgetItem(filename)
                item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(file))
                self.ListView.addItem(item_name)

    def onDeleteClick(self):
        item = self.ListView.currentItem()
        if item:
            row = self.ListView.row(item)
            self.ListView.takeItem(row)
            self.parent.config.set_list(
                self.ConfigSection, self.getFileList())
            filepath = unicode((item.data(QtCore.Qt.UserRole)).toString())
            for cidx in self.controllers:
                doc = self.controllers[cidx].add_doc(filepath)
                doc.presentation_deleted()
                doc.close_presentation()

    def generateSlideData(self, service_item):
        items = self.ListView.selectedIndexes()
        if len(items) > 1:
            return False
        service_item.title = unicode(self.DisplayTypeComboBox.currentText())
        service_item.shortname = unicode(self.DisplayTypeComboBox.currentText())
        shortname = service_item.shortname
        for item in items:
            bitem = self.ListView.item(item.row())
            filename = unicode((bitem.data(QtCore.Qt.UserRole)).toString())
            if shortname == self.Automatic:
                service_item.shortname = self.findControllerByType(filename)
                if not service_item.shortname:
                    return False
            controller = self.controllers[service_item.shortname]
            (path, name) = os.path.split(filename)
            doc = controller.add_doc(filename)
            if doc.get_slide_preview_file(1) is None:
                doc.load_presentation()
            i = 1
            img = doc.get_slide_preview_file(i)
            while img:
                service_item.add_from_command(path, name, img)
                i = i + 1
                img = doc.get_slide_preview_file(i)
            doc.close_presentation()
        return True

    def findControllerByType(self, filename):
        filetype = os.path.splitext(filename)[1]
        if not filetype:
            return None
        for controller in self.controllers:
            if self.controllers[controller].enabled:
                if filetype in self.controllers[controller].supports:
                    return controller
        for controller in self.controllers:
            if self.controllers[controller].enabled:
                if filetype in self.controllers[controller].alsosupports:
                    return controller
        return None
