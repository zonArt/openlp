# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2009 Raoul Snyman
Portions copyright (c) 2009 Martin Thompson, Tim Bentley,

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
import os,os.path
import sys
import zipfile

from time import sleep
from copy import deepcopy
from xml.etree.ElementTree import ElementTree, XML
from PyQt4 import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# from openlp.core.resources import *
# from openlp.core.ui import AboutForm, AlertForm, SettingsForm, SlideController
from openlp.core import translate
from openlp.core.lib import OpenLPToolbar
from openlp.core.utils import ConfigHelper
#from openlp.core.lib import ThemeItem

# from openlp.core import PluginManager
import logging

class ThemeData(QAbstractItemModel):
    """
    Tree of items for an order of Theme.
    Includes methods for reading and writing the contents to an OOS file
    Root contains a list of ThemeItems
    """
    global log
    log=logging.getLogger(u'ThemeData')
    def __init__(self):
        QAbstractItemModel.__init__(self)
        self.items=[]
        self.rowheight=50
        self.maximagewidth=self.rowheight*16/9.0;
        log.info("Starting")

    def clearItems(self):
        self.items=[]

    def columnCount(self, parent):
        return 1; # always only a single column (for now)

    def rowCount(self, parent):
        return len(self.items)

    def insertRow(self, row, filename):
        self.beginInsertRows(QModelIndex(),row,row)
        log.info("insert row %d:%s"%(row,filename))
        (prefix, shortfilename) = os.path.split(str(filename))
        log.info("shortfilename=%s"%(shortfilename))
        # create a preview image
        if os.path.exists(filename):
            preview = QPixmap(str(filename))
            w=self.maximagewidth;h=self.rowheight
            preview = preview.scaled(w,h, Qt.KeepAspectRatio)
            realw=preview.width(); realh=preview.height()
            # and move it to the centre of the preview space
            p=QPixmap(w,h)
            p.fill(Qt.transparent)
            painter=QPainter(p)
            painter.drawPixmap((w-realw)/2,(h-realh)/2,preview)
        else:
            w=self.maximagewidth;h=self.rowheight
            p=QPixmap(w,h)
            p.fill(Qt.transparent)
        # finally create the row
        self.items.insert(row,(filename, p, shortfilename))
        log.info("Items: %s" % self.items)
        self.endInsertRows()

    def removeRow(self, row):
        self.beginRemoveRows(QModelIndex(), row,row)
        self.items.pop(row)
        self.endRemoveRows()

    def addRow(self, item):
        self.insertRow(len(self.items), item)

    def index(self, row, col, parent = QModelIndex()):
        return self.createIndex(row,col)

    def parent(self, index=QModelIndex()):
        return QModelIndex() # no children as yet

    def data(self, index, role):
        row=index.row()
        if row > len(self.items): # if the last row is selected and deleted, we then get called with an empty row!
            return QVariant()
        if role==Qt.DisplayRole:
            retval= self.items[row][2]
        elif role == Qt.DecorationRole:
            retval= self.items[row][1]
        else:
            retval= QVariant()
#         log.info("Returning"+ str(retval))
        if type(retval) is not type(QVariant):
            return QVariant(retval)
        else:
            return retval

    def __iter__(self):
        for i in self.items:
            yield i

    def item(self, row):
        log.info("Get Item:%d -> %s" %(row, str(self.items)))
        return self.items[row]

class ThemeManager(QWidget):
    """
    Manages the orders of Theme.  C
    """
    global log
    log=logging.getLogger(u'ThemeManager')

    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent=parent
        self.Layout = QtGui.QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)
        self.Toolbar = OpenLPToolbar(self)
        self.Toolbar.addToolbarButton("New Theme", ":/themes/theme_new.png")
        self.Toolbar.addToolbarButton("Edit Theme", ":/themes/theme_edit.png")
        self.Toolbar.addToolbarButton("Delete Theme", ":/themes/theme_delete.png")
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton("Import Theme", ":/themes/theme_import.png",
            u'Allows Themes to be imported', self.onImportTheme)
        self.Toolbar.addToolbarButton("Export Theme", ":/themes/theme_export.png")
        self.ThemeWidget = QtGui.QWidgetAction(self.Toolbar)
        self.Toolbar.addAction(self.ThemeWidget)

        self.Layout.addWidget(self.Toolbar)

        self.ThemeListView = QtGui.QListView(self)
        self.Theme_data=ThemeData()
        self.ThemeListView.setModel(self.Theme_data)
        self.ThemeListView.setAlternatingRowColors(True)
        self.Layout.addWidget(self.ThemeListView)
        self.ThemeListView.setAlternatingRowColors(True)

        self.themelist= []
        self.path = os.path.join(ConfigHelper.get_data_path(), u'themes')
        self.checkThemesExists(self.path)
        self.loadThemes() # load the themes

#    def addThemeItem(self, item):
#        """Adds Theme item"""
#        log.info("addThemeItem")
#        indexes=self.TreeView.selectedIndexes()
#        assert len(indexes) <= 1 # can only have one selected index in this view
#        if indexes == []:
#            log.info("No row")
#            row = None
#            selected_item = None
#        else:
#            row=indexes[0].row()
#            # if currently selected is of correct type, add it to it
#            log.info("row:%d"%row)
#            selected_item=self.Theme_data.item(row)
#        if type(selected_item) == type(item):
#            log.info("Add to existing item")
#            selected_item.add(item)
#        else:
#            log.info("Create new item")
#            if row is None:
#                self.Theme_data.addRow(item)
#            else:
#                self.Theme_data.insertRow(row+1, item)
#
#    def removeThemeItem(self):
#        """Remove currently selected item"""
#        pass
#
#    def oos_as_text(self):
#        text=[]
#        log.info( "oos as text")
#        log.info("Data:"+str(self.Theme_data))
#        for i in self.Theme_data:
#            text.append("# " + str(i))
#            text.append(i.get_oos_text())
#        return '\n'.join(text)
#
#    def write_oos(self, filename):
#        """
#        Write a full OOS file out - iterate over plugins and call their respective methods
#        This format is totally arbitrary testing purposes - something sensible needs to go in here!
#        """
#        oosfile=open(filename, "w")
#        oosfile.write("# BEGIN OOS\n")
#        oosfile.write(self.oos_as_text)
#        oosfile.write("# END OOS\n")
#        oosfile.close()

    def onImportTheme(self):
        files = QtGui.QFileDialog.getOpenFileNames(None,
            translate('ThemeManager', u'Select Import File'),
            self.path,
            u'Theme (*.theme)')
        log.info(u'New Themes) %s', str(files))
        if len(files) > 0:
            for file in files:
                self.unzipTheme(file, self.path)
        self.Theme_data.clearItems()
        self.loadThemes()

    def loadThemes(self):
        log.debug(u'Load themes from dir')
#        self.themelist = [u'African Sunset', u'Snowy Mountains', u'Wilderness', u'Wet and Windy London']
        for root, dirs, files in os.walk(self.path):
            for name in files:
                if name.endswith(u'.bmp'):
                    self.Theme_data.addRow(os.path.join(self.path, name))

    def getThemes(self):
        return self.themelist

    def checkThemesExists(self, dir):
        log.debug(u'check themes')
        if os.path.exists(dir) == False:
            os.mkdir(dir)

    def unzipTheme(self, filename, dir):
        log.debug(u'Unzipping theme %s', filename)
        zip = zipfile.ZipFile(str(filename))
        for file in zip.namelist():
            if file.endswith('/'):
                theme_dir = os.path.join(dir, file)
                if os.path.exists(theme_dir) == False:
                    os.mkdir(os.path.join(dir, file))
            else:
                fullpath = os.path.join(dir, file)
                if file.endswith(u'.xml'):
                    self.checkVersion1(fullpath)
                outfile = open(fullpath, 'w')
                outfile.write(zip.read(file))
                outfile.close()

    def checkVersion1(self, xmlfile):
        file=open(xmlfile)
        t=''.join(file.readlines()) # read the file and change list to a string
        tree = ElementTree(element=XML(t)).getroot()
        print "AA"
        print tree.find('BackgroundType')
        print "AAA"
