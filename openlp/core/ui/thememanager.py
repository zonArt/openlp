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
import shutil

from time import sleep
from copy import deepcopy
from xml.etree.ElementTree import ElementTree, XML
from PyQt4 import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from openlp.core.ui import AmendThemeForm
from openlp.core import translate
from openlp.core.theme import Theme
from openlp.core.lib import Event
from openlp.core.lib import EventType
from openlp.core.lib import EventManager
from openlp.core.lib import OpenLPToolbar
from openlp.core.lib import ThemeXML
from openlp.core.lib import Renderer
from openlp.core.utils import ConfigHelper


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
        log.info(u'Starting')

    def clearItems(self):
        self.items=[]

    def columnCount(self, parent):
        return 1; # always only a single column (for now)

    def rowCount(self, parent):
        return len(self.items)

    def insertRow(self, row, filename):
        self.beginInsertRows(QModelIndex(),row,row)
        log.info(u'insert row %d:%s'%(row,filename))
        (prefix, shortfilename) = os.path.split(str(filename))
        log.info(u'shortfilename=%s'%(shortfilename))
        theme = shortfilename.split(u'.')
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
        self.items.insert(row,(filename, p, shortfilename, theme[0]))
        log.info(u'Items: %s' % self.items)
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
            retval= self.items[row][3]
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

    def getValue(self, index):
        row = index.row()
        return self.items[row]

    def getItem(self, row):
        log.info(u'Get Item:%d -> %s' %(row, str(self.items)))
        return self.items[row]

    def getList(self):
        filelist = [item[3] for item in self.items];
        return filelist

class ThemeManager(QWidget):
    """
    Manages the orders of Theme.
    """
    global log
    log=logging.getLogger(u'ThemeManager')

    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent=parent
        self.Layout = QtGui.QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)
        self.amendThemeForm = AmendThemeForm(self)
        self.Toolbar = OpenLPToolbar(self)
        self.Toolbar.addToolbarButton(translate('ThemeManager',u'New Theme'), ":/themes/theme_new.png",
            translate('ThemeManager',u'Allows a Theme to be created'), self.onAddTheme)
        self.Toolbar.addToolbarButton(translate('ThemeManager',u'Edit Theme'), ":/themes/theme_edit.png",
            translate('ThemeManager',u'Allows a Theme to be amended'), self.onEditTheme)
        self.Toolbar.addToolbarButton(translate('ThemeManager',u'Delete Theme'), ":/themes/theme_delete.png",
            translate('ThemeManager',u'Allows a Theme to be deleted'), self.onDeleteTheme)
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton(translate('ThemeManager',u'Import Theme'), ":/themes/theme_import.png",
            translate('ThemeManager',u'Allows Themes to be imported'), self.onImportTheme)
        self.Toolbar.addToolbarButton(translate('ThemeManager',u'Export Theme'), ":/themes/theme_export.png",
            translate('ThemeManager',u'Allows Themes to be exported'), self.onExportTheme)
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
        self.amendThemeForm.themePath(self.path)

    def setEventManager(self, eventManager):
        self.eventManager = eventManager

    def onAddTheme(self):
        self.amendThemeForm.loadTheme(None)
        self.amendThemeForm.exec_()

    def onEditTheme(self):
        items = self.ThemeListView.selectedIndexes()
        for item in items:
            data = self.Theme_data.getValue(item)
            self.amendThemeForm.loadTheme(data[3])
        self.amendThemeForm.exec_()

    def onDeleteTheme(self):
        items = self.ThemeListView.selectedIndexes()
        theme = ''
        for item in items:
            data = self.Theme_data.getValue(item)
            theme = data[3]
        th = theme +  u'.png'
        try:
            os.remove(os.path.join(self.path, th))
        except:
            pass #if not present do not worry
        shutil.rmtree(os.path.join(self.path, theme))
        self.Theme_data.clearItems()
        self.loadThemes()

    def onExportTheme(self):
        pass

    def onImportTheme(self):
        files = QtGui.QFileDialog.getOpenFileNames(None,
            translate('ThemeManager', u'Select Import File'),
            self.path,
            u'Theme (*.theme)')
        log.info(u'New Themes %s', str(files))
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
                if name.endswith(u'.png'):
                    self.Theme_data.addRow(os.path.join(self.path, name))

        self.eventManager.post_event(Event(EventType.ThemeListChanged))

    def getThemes(self):
        return self.Theme_data.getList()

    def checkThemesExists(self, dir):
        log.debug(u'check themes')
        if os.path.exists(dir) == False:
            os.mkdir(dir)

    def unzipTheme(self, filename, dir):
        """
        Unzip the theme , remove the preview file if stored
        Generate a new preview fileCheck the XML theme version and upgrade if
        necessary.
        """
        log.debug(u'Unzipping theme %s', filename)
        zip = zipfile.ZipFile(str(filename))
        filexml = None
        themename = None
        for file in zip.namelist():
            if file.endswith('/'):
                theme_dir = os.path.join(dir, file)
                if os.path.exists(theme_dir) == False:
                    os.mkdir(os.path.join(dir, file))
            else:
                fullpath = os.path.join(dir, file)
                names = file.split(u'/')
                if len(names) > 1: # not preview file
                    if themename is None:
                        themename = names[0]
                    xml_data = zip.read(file)
                    if os.path.splitext (file) [1].lower ()  in [u'.xml']:
                        if self.checkVersion1(xml_data):
                            filexml = self.migrateVersion122(filename, fullpath, xml_data) # upgrade theme xml
                        else:
                            file_xml = xml_data
                        outfile = open(fullpath, 'w')
                        outfile.write(filexml)
                        outfile.close()
                    else:
                        outfile = open(fullpath, 'w')
                        outfile.write(zip.read(file))
                        outfile.close()
        self.generateAndSaveImage(dir,themename, filexml)

    def checkVersion1(self, xmlfile):
        log.debug(u'checkVersion1 ')
        t = xmlfile
        tree = ElementTree(element=XML(t)).getroot()
        if tree.find(u'BackgroundType') is None :
            return False
        else:
            return True

    def migrateVersion122(self, filename , fullpath, xml_data):
        log.debug(u'migrateVersion122 %s %s', filename , fullpath)
        t=Theme(xml_data)

        newtheme = ThemeXML()
        newtheme.new_document(t.Name)
        if t.BackgroundType == 0:
            newtheme.add_background_solid(str(t.BackgroundParameter1.name()))
        elif t.BackgroundType == 1:
            direction = "vertical"
            if t.BackgroundParameter3.name() == 1:
                direction = "horizontal"
            newtheme.add_background_gradient(str(t.BackgroundParameter1.name()), str(t.BackgroundParameter2.name()), direction)
        else:
            newtheme.add_background_image(str(t.BackgroundParameter1))

        newtheme.add_font(str(t.FontName), str(t.FontColor.name()), str(t.FontProportion * 2), u'True')
        newtheme.add_font(str(t.FontName), str(t.FontColor.name()), str(12), u'True', u'footer')
        outline = False
        shadow = False
        if t.Shadow == 1:
            shadow = True
        if t.Outline == 1:
            outline = True
        newtheme.add_display(str(shadow), str(t.ShadowColor.name()), str(outline), str(t.OutlineColor.name()),
            str(t.HorizontalAlign), str(t.VerticalAlign), str(t.WrapStyle))
        return newtheme.extract_xml()

    def generateAndSaveImage(self, dir, name, theme_xml):
        log.debug(u'generateImage %s %s %s', dir, name, theme_xml)
        theme = ThemeXML()
        theme.parse(theme_xml)

        frame = self.generateImage(theme)

        im=frame.toImage()
        samplepathname=os.path.join(dir, name+u'.png')
        if os.path.exists(samplepathname):
            os.unlink(samplepathname)
        im.save(samplepathname, u'png')
        log.debug(u'Theme image written to %s',samplepathname)

    def generateImage(self, theme):
        log.debug(u'generateImage %s ',  theme)
        size=QtCore.QSize(800,600)
        frame = QtGui.QPixmap(size.width(), size.height())
        renderer=Renderer(self.path)
        renderer.set_paint_dest(frame)

        renderer.set_theme(theme) # set default theme
        #renderer._render_background()
        renderer.set_text_rectangle(QtCore.QRect(0,0, size.width()-1, size.height()-1), QtCore.QRect(10,560, size.width()-1, size.height()-1))

        lines=[]
        lines.append(u'Amazing Grace!')
        lines.append(u'How sweet the sound')
        lines.append(u'To save a wretch like me;')
        lines.append(u'I once was lost but now am found,')
        lines.append(u'Was blind, but now I see.')
        lines1=[]
        lines1.append(u'Amazing Grace (John Newton)' )
        lines1.append(u'CCLI xxx (c)Openlp.org')
        answer=renderer.render_lines(lines, lines1)
        return frame

