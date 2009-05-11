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
import os
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

from openlp.core.ui import AmendThemeForm, ServiceManager
from openlp.core import translate, fileToXML
from openlp.core.theme import Theme
from openlp.core.lib import Event, EventType, EventManager, OpenLPToolbar, ThemeXML, Renderer
from openlp.core.utils import ConfigHelper
from openlp.core.resources import *

import logging

class ThemeData(QAbstractListModel):
    """
    Tree of items for an order of Theme.
    Includes methods for reading and writing the contents to an OOS file
    Root contains a list of ThemeItems
    """
    global log
    log=logging.getLogger(u'ThemeData')

    def __init__(self):
        QAbstractListModel.__init__(self)
        self.items = []
        self.rowheight = 50
        self.maximagewidth = self.rowheight * 16 / 9.0;
        log.info(u'Starting')

    def clearItems(self):
        self.items = []

    def rowCount(self, parent):
        return len(self.items)

    def insertRow(self, row, filename):
        self.beginInsertRows(QModelIndex(), row, row)
        log.info(u'insert row %d:%s' % (row, filename))
        (prefix, shortfilename) = os.path.split(str(filename))
        log.info(u'shortfilename = %s' % shortfilename)
        theme = shortfilename.split(u'.')
        # create a preview image
        if os.path.exists(filename):
            preview = QPixmap(str(filename))
            width = self.maximagewidth
            height = self.rowheight
            preview = preview.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            realwidth = preview.width()
            realheight = preview.height()
            # and move it to the centre of the preview space
            pixmap = QPixmap(width, height)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.drawPixmap((width - realwidth) / 2, (height - realheight) / 2, preview)
        else:
            width = self.maximagewidth
            height = self.rowheight
            pixmap = QPixmap(width, height)
            pixmap.fill(Qt.transparent)
        # finally create the row
        self.items.insert(row, (filename, pixmap, shortfilename, theme[0]))
        log.info(u'Items: %s' % self.items)
        self.endInsertRows()

    def removeRow(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        self.items.pop(row)
        self.endRemoveRows()

    def addRow(self, item):
        self.insertRow(len(self.items), item)

    def data(self, index, role):
        row = index.row()
        if row > len(self.items):
            # if the last row is selected and deleted, we then get called with an empty row!
            return QVariant()
        if role == Qt.DisplayRole:
            retval = self.items[row][3]
        elif role == Qt.DecorationRole:
            retval = self.items[row][1]
        else:
            retval = QVariant()
        #log.info("Returning"+ str(retval))
        if type(retval) is not type(QVariant):
            return QVariant(retval)
        else:
            return retval

    def __iter__(self):
        for item in self.items:
            yield item

    def getValue(self, index):
        row = index.row()
        return self.items[row]

    def getItem(self, row):
        log.info(u'Get Item:%d -> %s' % (row, str(self.items)))
        return self.items[row]

    def getList(self):
        filelist = [item[3] for item in self.items]
        return filelist

class ThemeManager(QWidget):
    """
    Manages the orders of Theme.
    """
    global log
    log=logging.getLogger(u'ThemeManager')

    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent = parent
        self.Layout = QtGui.QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)
        self.amendThemeForm = AmendThemeForm(self)
        self.Toolbar = OpenLPToolbar(self)
        self.Toolbar.addToolbarButton(
            translate(u'ThemeManager', u'New Theme'), u':/themes/theme_new.png',
            translate(u'ThemeManager', u'Create a new theme'), self.onAddTheme)
        self.Toolbar.addToolbarButton(
            translate(u'ThemeManager', u'Edit Theme'), u':/themes/theme_edit.png',
            translate(u'ThemeManager', u'Edit a theme'), self.onEditTheme)
        self.Toolbar.addToolbarButton(
            translate(u'ThemeManager', u'Delete Theme'), u':/themes/theme_delete.png',
            translate(u'ThemeManager', u'Delete a theme'), self.onDeleteTheme)
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton(
            translate(u'ThemeManager', u'Import Theme'), u':/themes/theme_import.png',
            translate(u'ThemeManager', u'Import a theme'), self.onImportTheme)
        self.Toolbar.addToolbarButton(
            translate(u'ThemeManager', u'Export Theme'), u':/themes/theme_export.png',
            translate(u'ThemeManager', u'Export a theme'), self.onExportTheme)
        self.ThemeWidget = QtGui.QWidgetAction(self.Toolbar)
        self.Layout.addWidget(self.Toolbar)

        self.ThemeListView = QtGui.QListView(self)
        self.themeData = ThemeData()
        self.ThemeListView.setModel(self.themeData)
        self.ThemeListView.setAlternatingRowColors(True)
        self.Layout.addWidget(self.ThemeListView)

        self.themelist = []
        self.path = os.path.join(ConfigHelper.get_data_path(), u'themes')
        self.checkThemesExists(self.path)
        self.amendThemeForm.themePath(self.path)

    def onAddTheme(self):
        self.amendThemeForm.loadTheme(None)
        self.amendThemeForm.exec_()

    def onEditTheme(self):
        items = self.ThemeListView.selectedIndexes()
        for item in items:
            data = self.themeData.getValue(item)
            self.amendThemeForm.loadTheme(data[3])
        self.amendThemeForm.exec_()

    def onDeleteTheme(self):
        items = self.ThemeListView.selectedIndexes()
        theme = u''
        for item in items:
            data = self.themeData.getValue(item)
            theme = data[3]
        th = theme +  u'.png'
        try:
            os.remove(os.path.join(self.path, th))
        except:
            pass #if not present do not worry
        shutil.rmtree(os.path.join(self.path, theme))
        self.themeData.clearItems()
        self.loadThemes()

    def onExportTheme(self):
        pass

    def onImportTheme(self):
        files = QtGui.QFileDialog.getOpenFileNames(None,
            translate(u'ThemeManager', u'Select Import File'),
            self.path, u'Theme (*.theme)')
        log.info(u'New Themes %s', str(files))
        if len(files) > 0:
            for file in files:
                self.unzipTheme(file, self.path)
        self.themeData.clearItems()
        self.loadThemes()

    def loadThemes(self):
        log.debug(u'Load themes from dir')
        for root, dirs, files in os.walk(self.path):
            for name in files:
                if name.endswith(u'.png'):
                    self.themeData.addRow(os.path.join(self.path, name))
        self.eventManager.post_event(Event(EventType.ThemeListChanged))
        self.serviceManager.updateThemeList(self.getThemes())

    def getThemes(self):
        return self.themeData.getList()

    def getThemeData(self, themename):
        log.debug(u'getthemedata for theme %s', themename)
        xml_file = os.path.join(self.path, str(themename), str(themename) + u'.xml')
        try:
            xml = fileToXML(xml_file)
        except:
            newtheme = ThemeXML()
            newtheme.new_document(u'New Theme')
            newtheme.add_background_solid(str(u'#000000'))
            newtheme.add_font(str(QFont().family()), str(u'#FFFFFF'), str(30), u'False')
            newtheme.add_font(str(QFont().family()), str(u'#FFFFFF'), str(12), u'False', u'footer')
            newtheme.add_display(u'False', str(u'#FFFFFF'), u'False', str(u'#FFFFFF'),
                str(0), str(0), str(0))
            xml = newtheme.extract_xml()
        theme = ThemeXML()
        theme.parse(xml)
        return theme

    def checkThemesExists(self, dir):
        log.debug(u'check themes')
        if os.path.exists(dir) == False:
            os.mkdir(dir)

    def unzipTheme(self, filename, dir):
        """
        Unzip the theme, remove the preview file if stored
        Generate a new preview fileCheck the XML theme version and upgrade if
        necessary.
        """
        log.debug(u'Unzipping theme %s', filename)
        zip = zipfile.ZipFile(str(filename))
        filexml = None
        themename = None
        for file in zip.namelist():
            if file.endswith(os.path.sep):
                theme_dir = os.path.join(dir, file)
                if os.path.exists(theme_dir) == False:
                    os.mkdir(os.path.join(dir, file))
            else:
                fullpath = os.path.join(dir, file)
                names = file.split(os.path.sep)
                if len(names) > 1:
                    # not preview file
                    if themename is None:
                        themename = names[0]
                    xml_data = zip.read(file)
                    if os.path.splitext(file)[1].lower() in [u'.xml']:
                        if self.checkVersion1(xml_data):
                            # upgrade theme xml
                            filexml = self.migrateVersion122(filename, fullpath, xml_data)
                        else:
                            filexml = xml_data
                        outfile = open(fullpath, u'w')
                        outfile.write(filexml)
                        outfile.close()
                    else:
                        outfile = open(fullpath, u'w')
                        outfile.write(zip.read(file))
                        outfile.close()
        self.generateAndSaveImage(dir, themename, filexml)

    def checkVersion1(self, xmlfile):
        log.debug(u'checkVersion1 ')
        theme = xmlfile
        tree = ElementTree(element=XML(theme)).getroot()
        if tree.find(u'BackgroundType') is None:
            return False
        else:
            return True

    def migrateVersion122(self, filename, fullpath, xml_data):
        log.debug(u'migrateVersion122 %s %s', filename, fullpath)
        theme = Theme(xml_data)
        newtheme = ThemeXML()
        newtheme.new_document(theme.Name)
        if theme.BackgroundType == 0:
            newtheme.add_background_solid(str(theme.BackgroundParameter1.name()))
        elif theme.BackgroundType == 1:
            direction = u'vertical'
            if theme.BackgroundParameter3.name() == 1:
                direction = u'horizontal'
            newtheme.add_background_gradient(
                str(theme.BackgroundParameter1.name()),
                str(theme.BackgroundParameter2.name()), direction)
        else:
            newtheme.add_background_image(str(theme.BackgroundParameter1))

        newtheme.add_font(str(theme.FontName), str(theme.FontColor.name()),
            str(theme.FontProportion * 2), u'False')
        newtheme.add_font(str(theme.FontName), str(theme.FontColor.name()),
            str(12), u'False', u'footer')
        outline = False
        shadow = False
        if theme.Shadow == 1:
            shadow = True
        if theme.Outline == 1:
            outline = True
        newtheme.add_display(str(shadow), str(theme.ShadowColor.name()),
            str(outline), str(theme.OutlineColor.name()),
            str(theme.HorizontalAlign), str(theme.VerticalAlign),
            str(theme.WrapStyle))
        return newtheme.extract_xml()

    def saveTheme(self, name, theme_xml) :
        log.debug(u'saveTheme %s %s', name, theme_xml)
        self.generateAndSaveImage(self.path, name, theme_xml)
        theme_dir = os.path.join(self.path, name)
        if os.path.exists(theme_dir) == False:
            os.mkdir(os.path.join(self.path, name))
        theme_file = os.path.join(theme_dir, name + u'.xml')
        outfile = open(theme_file, u'w')
        outfile.write(theme_xml)
        outfile.close()
        self.themeData.clearItems()
        self.loadThemes()

    def generateAndSaveImage(self, dir, name, theme_xml):
        log.debug(u'generateAndSaveImage %s %s %s', dir, name, theme_xml)
        theme = ThemeXML()
        theme.parse(theme_xml)
        frame = self.generateImage(theme)
        im = frame.toImage()
        samplepathname = os.path.join(self.path, name + u'.png')
        if os.path.exists(samplepathname):
            os.unlink(samplepathname)
        im.save(samplepathname, u'png')
        log.debug(u'Theme image written to %s', samplepathname)

    def generateImage(self, themedata):
        log.debug(u'generateImage %s ', themedata)
        frame = self.renderManager.generate_preview(themedata)
        return frame

