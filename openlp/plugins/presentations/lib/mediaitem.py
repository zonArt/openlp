# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
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
import logging
import os

from PyQt4 import QtCore, QtGui
from openlp.plugins.presentations.lib import FileListData
from openlp.core.lib import MediaManagerItem, ServiceItem, translate, BaseListWithDnD

# We have to explicitly create separate classes for each plugin
# in order for DnD to the Service manager to work correctly.
class PresentationListView(BaseListWithDnD):
    def __init__(self, parent=None):
        self.PluginName = u'Presentation'
        BaseListWithDnD.__init__(self, parent)

class PresentationMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Custom Slides.
    """
    global log
    log=logging.getLogger(u'PresentationsMediaItem')
    log.info(u'Presentations Media Item loaded')

    def __init__(self, parent, icon, title):
        self.TranslationContext = u'PresentationPlugin'
        self.PluginTextShort = u'Presentation'
        self.ConfigSection = u'presentation'
        self.hasFileIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False
        self.IconPath = u'presentations/presentation'
        self.OnNewPrompt = u'Select Presentation(s)'
        self.OnNewFileMasks = u'Presentations (*.ppt *.pps *.odp)'
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = PresentationListView
        MediaManagerItem.__init__(self, parent, icon, title)

    def addHeaderBar(self):
        self.PresentationWidget = QtGui.QWidget(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PresentationWidget.sizePolicy().hasHeightForWidth())
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

        self.DisplayTypeLabel.setText(translate(u'PresentationMediaItem', u'Present using:'))

        # Add the Presentation widget to the page layout
        self.PageLayout.addWidget(self.PresentationWidget)

    def initialise(self):
        list = self.parent.config.load_list(u'presentations')
        self.loadPresentationList(list)
        self.DisplayTypeComboBox.addItem(u'Impress')
#        self.DisplayTypeComboBox.addItem(u'Powerpoint')
#        self.DisplayTypeComboBox.addItem(u'Keynote')

    def loadList(self, list):
        for file in list:
            (path, filename) = os.path.split(unicode(file))
            item_name = QtGui.QListWidgetItem(filename)
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(file))
            self.ListView.addItem(item_name)

    def getFileList(self):
        count = 0
        while  count < len(self.ListView):
            filelist = [set.ListView.item(count).text()]
            count += 1
        return filelist

    def loadPresentationList(self, list):
        pass
#        for files in list:
#            self.PresentationsListData.addRow(files)

    def onPresentationDeleteClick(self):
        indexes = self.PresentationsListView.selectedIndexes()
        for index in indexes:
            current_row = int(index.row())
            self.PresentationsListData.removeRow(current_row)
        self.parent.config.set_list(u'Presentations', self.PresentationsListData.getFileList())
