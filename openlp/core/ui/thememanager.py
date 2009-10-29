# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

import os
import zipfile
import shutil
import logging

from xml.etree.ElementTree import ElementTree, XML
from PyQt4 import QtCore, QtGui

from openlp.core.ui import AmendThemeForm
from openlp.core.theme import Theme
from openlp.core.lib import PluginConfig, OpenLPToolbar, ThemeXML, \
    str_to_bool, file_to_xml, buildIcon, Receiver, contextMenuAction, \
    contextMenuSeparator
from openlp.core.utils import ConfigHelper

class ThemeManager(QtGui.QWidget):
    """
    Manages the orders of Theme.
    """
    global log
    log = logging.getLogger(u'ThemeManager')

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.Layout = QtGui.QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)
        self.amendThemeForm = AmendThemeForm(self)
        self.Toolbar = OpenLPToolbar(self)
        self.Toolbar.addToolbarButton(
            self.trUtf8(u'New Theme'), u':/themes/theme_new.png',
            self.trUtf8(u'Create a new theme'), self.onAddTheme)
        self.Toolbar.addToolbarButton(
            self.trUtf8(u'Edit Theme'), u':/themes/theme_edit.png',
            self.trUtf8(u'Edit a theme'), self.onEditTheme)
        self.Toolbar.addToolbarButton(
            self.trUtf8(u'Delete Theme'), u':/themes/theme_delete.png',
            self.trUtf8(u'Delete a theme'), self.onDeleteTheme)
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton(
            self.trUtf8(u'Import Theme'), u':/themes/theme_import.png',
            self.trUtf8(u'Import a theme'), self.onImportTheme)
        self.Toolbar.addToolbarButton(
            self.trUtf8(u'Export Theme'), u':/themes/theme_export.png',
            self.trUtf8(u'Export a theme'), self.onExportTheme)
        self.ThemeWidget = QtGui.QWidgetAction(self.Toolbar)
        self.Layout.addWidget(self.Toolbar)
        self.ThemeListWidget = QtGui.QListWidget(self)
        self.ThemeListWidget.setAlternatingRowColors(True)
        self.ThemeListWidget.setIconSize(QtCore.QSize(88,50))
        self.Layout.addWidget(self.ThemeListWidget)
        self.ThemeListWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ThemeListWidget.addAction(
            contextMenuAction(self.ThemeListWidget, u':/themes/theme_edit.png',
            self.trUtf8(u'Edit a theme'), self.onEditTheme))
        self.ThemeListWidget.addAction(contextMenuSeparator(self.ThemeListWidget))
        self.ThemeListWidget.addAction(
            contextMenuAction(self.ThemeListWidget, u':/themes/theme_delete.png',
            self.trUtf8(u'Delete theme'), self.onDeleteTheme))
        self.ThemeListWidget.addAction(
            contextMenuAction(self.ThemeListWidget, u':/themes/theme_export.png',
            self.trUtf8(u'Make Global'), self.changeGlobalFromScreen))
        self.ThemeListWidget.addAction(
            contextMenuAction(self.ThemeListWidget, u':/themes/theme_export.png',
            self.trUtf8(u'Export theme'), self.onExportTheme))
        self.ThemeListWidget.addAction(contextMenuSeparator(self.ThemeListWidget))
        #Signals
        QtCore.QObject.connect(self.ThemeListWidget,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
            self.changeGlobalFromScreen)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'update_global_theme'), self.changeGlobalFromTab)
        #Variables
        self.themelist = []
        self.path = os.path.join(ConfigHelper.get_data_path(), u'themes')
        self.checkThemesExists(self.path)
        self.amendThemeForm.path = self.path
        # Last little bits of setting up
        self.config = PluginConfig(u'themes')
        self.servicePath = self.config.get_data_path()
        self.global_theme = unicode(
            self.config.get_config(u'theme global theme', u''))

    def changeGlobalFromTab(self, themeName):
        log.debug(u'changeGlobalFromTab %s', themeName)
        for count in range (0, self.ThemeListWidget.count()):
            #reset the old name
            item = self.ThemeListWidget.item(count)
            oldName = item.text()
            newName = unicode(item.data(QtCore.Qt.UserRole).toString())
            if oldName != newName:
                self.ThemeListWidget.item(count).setText(newName)
            #Set the new name
            if themeName == newName:
                name = u'%s (%s)' % (newName, self.trUtf8(u'default'))
                self.ThemeListWidget.item(count).setText(name)

    def changeGlobalFromScreen(self, index = -1):
        log.debug(u'changeGlobalFromScreen %s', index)
        selected_row = self.ThemeListWidget.currentRow()
        for count in range (0, self.ThemeListWidget.count()):
            item = self.ThemeListWidget.item(count)
            oldName = item.text()
            #reset the old name
            if oldName != unicode(item.data(QtCore.Qt.UserRole).toString()):
                self.ThemeListWidget.item(count).setText(
                    unicode(item.data(QtCore.Qt.UserRole).toString()))
            #Set the new name
            if count == selected_row:
                self.global_theme = unicode(
                    self.ThemeListWidget.item(count).text())
                name = u'%s (%s)' % (self.global_theme, self.trUtf8(u'default'))
                self.ThemeListWidget.item(count).setText(name)
                self.config.set_config(u'theme global theme', self.global_theme)
                Receiver().send_message(
                    u'update_global_theme', self.global_theme)
                self.pushThemes()

    def onAddTheme(self):
        self.amendThemeForm.loadTheme(None)
        self.saveThemeName = u''
        self.amendThemeForm.exec_()

    def onEditTheme(self):
        item = self.ThemeListWidget.currentItem()
        if item is not None:
            self.amendThemeForm.loadTheme(
                unicode(item.data(QtCore.Qt.UserRole).toString()))
            self.saveThemeName = unicode(item.data(QtCore.Qt.UserRole).toString())
            self.amendThemeForm.exec_()

    def onDeleteTheme(self):
        self.global_theme = unicode(
            self.config.get_config(u'theme global theme', u''))
        item = self.ThemeListWidget.currentItem()
        if item is not None:
            theme = unicode(item.text())
            # should be the same unless default
            if theme != unicode(item.data(QtCore.Qt.UserRole).toString()):
                QtGui.QMessageBox.critical(
                    self, self.trUtf8(u'Error'),
                    self.trUtf8(u'You are unable to delete the default theme!'),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
            else:
                self.themelist.remove(theme)
                th = theme + u'.png'
                row = self.ThemeListWidget.row(item)
                self.ThemeListWidget.takeItem(row)
                try:
                    os.remove(os.path.join(self.path, th))
                except:
                    #if not present do not worry
                    pass
                try:
                    shutil.rmtree(os.path.join(self.path, theme))
                except:
                    #if not present do not worry
                    pass
                # As we do not reload the themes push out the change
                # Reaload the list as the internal lists and events need
                # to be triggered
                self.pushThemes()

    def onExportTheme(self):
        """
        Save the theme in a zip file
        """
        item = self.ThemeListWidget.currentItem()
        if item is None:
            QtGui.QMessageBox.critical(self, self.trUtf8(u'Error'),
                self.trUtf8(u'You have not selected a theme!'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
            return
        theme = unicode(item.data(QtCore.Qt.UserRole).toString())
        path = QtGui.QFileDialog.getExistingDirectory(self,
            unicode(self.trUtf8(u'Save Theme - (%s)')) %  theme,
            self.config.get_last_dir(1) )
        path = unicode(path)
        if path != u'':
            self.config.set_last_dir(path, 1)
            themePath = os.path.join(path, theme + u'.theme')
            zip = zipfile.ZipFile(themePath, u'w')
            source = os.path.join(self.path, theme)
            for root, dirs, files in os.walk(source):
                for name in files:
                    zip.write(
                        os.path.join(source, name), os.path.join(theme, name))
            zip.close()

    def onImportTheme(self):
        files = QtGui.QFileDialog.getOpenFileNames(
            self, self.trUtf8(u'Select Theme Import File'),
            self.config.get_last_dir(), u'Theme (*.*)')
        log.info(u'New Themes %s', unicode(files))
        if len(files) > 0:
            for file in files:
                self.config.set_last_dir(filename)
                self.unzipTheme(file, self.path)
        self.loadThemes()

    def loadThemes(self):
        """
        Loads the theme lists and triggers updates accross the whole system
        using direct calls or core functions and events for the plugins.
        The plugins will call back in to get the real list if they want it.
        """
        log.debug(u'Load themes from dir')
        self.themelist = []
        self.ThemeListWidget.clear()
        for root, dirs, files in os.walk(self.path):
            for name in files:
                if name.endswith(u'.png'):
                    #check to see file is in theme root directory
                    theme = os.path.join(self.path, name)
                    if os.path.exists(theme):
                        (path, filename) = os.path.split(unicode(file))
                        textName = os.path.splitext(name)[0]
                        if textName == self.global_theme:
                            name = u'%s (%s)' % (textName,
                                self.trUtf8(u'default'))
                        else:
                            name = textName
                        item_name = QtGui.QListWidgetItem(name)
                        item_name.setIcon(buildIcon(theme))
                        item_name.setData(QtCore.Qt.UserRole,
                            QtCore.QVariant(textName))
                        self.ThemeListWidget.addItem(item_name)
                        self.themelist.append(textName)
        self.pushThemes()

    def pushThemes(self):
        Receiver().send_message(u'update_themes', self.getThemes() )

    def getThemes(self):
        return self.themelist

    def getThemeData(self, themename):
        log.debug(u'getthemedata for theme %s', themename)
        xml_file = os.path.join(self.path, unicode(themename),
            unicode(themename) + u'.xml')
        try:
            xml = file_to_xml(xml_file)
        except:
            xml = basTheme()
        theme = ThemeXML()
        theme.parse(xml)
        self.cleanTheme(theme)
        theme.extend_image_filename(self.path)
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
        filename = unicode(filename)
        try:
            zip = zipfile.ZipFile(filename)
        except:
            QtGui.QMessageBox.critical(
                self, self.trUtf8(u'Error'),
                self.trUtf8(u'File is not a valid theme!'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
            return
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
                            filexml = self.migrateVersion122(filename,
                                fullpath, xml_data)
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
        """
        Am I a version 1 theme
        """
        log.debug(u'checkVersion1 ')
        theme = xmlfile
        tree = ElementTree(element=XML(theme)).getroot()
        if tree.find(u'BackgroundType') is None:
            return False
        else:
            return True

    def migrateVersion122(self, filename, fullpath, xml_data):
        """
        Called by convert the xml data from version 1 format
        to the current format.
        New fields are defaulted but the new theme is useable
        """
        log.debug(u'migrateVersion122 %s %s', filename, fullpath)
        theme = Theme(xml_data)
        newtheme = ThemeXML()
        newtheme.new_document(theme.Name)
        if theme.BackgroundType == 0:
            newtheme.add_background_solid(unicode(
                theme.BackgroundParameter1.name()))
        elif theme.BackgroundType == 1:
            direction = u'vertical'
            if theme.BackgroundParameter3.name() == 1:
                direction = u'horizontal'
            newtheme.add_background_gradient(
                unicode(theme.BackgroundParameter1.name()),
                unicode(theme.BackgroundParameter2.name()), direction)
        else:
            newtheme.add_background_image(unicode(theme.BackgroundParameter1))

        newtheme.add_font(unicode(theme.FontName),
            unicode(theme.FontColor.name()),
            unicode(theme.FontProportion * 3), u'False')
        newtheme.add_font(unicode(theme.FontName),
            unicode(theme.FontColor.name()),
            unicode(12), u'False', u'footer')
        outline = False
        shadow = False
        if theme.Shadow == 1:
            shadow = True
        if theme.Outline == 1:
            outline = True
        newtheme.add_display(unicode(shadow), unicode(theme.ShadowColor.name()),
            unicode(outline), unicode(theme.OutlineColor.name()),
            unicode(theme.HorizontalAlign), unicode(theme.VerticalAlign),
            unicode(theme.WrapStyle))
        return newtheme.extract_xml()

    def saveTheme(self, name, theme_xml, theme_pretty_xml, image_from,
        image_to) :
        """
        Called by thememaintenance Dialog to save the theme
        and to trigger the reload of the theme list
        """
        log.debug(u'saveTheme %s %s', name, theme_xml)
        theme_dir = os.path.join(self.path, name)
        if os.path.exists(theme_dir) == False:
            os.mkdir(os.path.join(self.path, name))
        theme_file = os.path.join(theme_dir, name + u'.xml')
        log.debug(theme_file)
        result = QtGui.QMessageBox.Yes
        if self.saveThemeName != name:
            if os.path.exists(theme_file):
                result = QtGui.QMessageBox.question(
                    self, self.trUtf8(u'Theme Exists'),
                    self.trUtf8(u'A theme with this name already exists, '
                        u'would you like to overwrite it?'),
                    (QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
                    QtGui.QMessageBox.No)
            else:
                result == QtGui.QMessageBox.Yes
        if result == QtGui.QMessageBox.Yes:
            # Save the theme, overwriting the existing theme if necessary.
            outfile = open(theme_file, u'w')
            outfile.write(theme_pretty_xml)
            outfile.close()
            if image_from is not None and image_from != image_to:
                print "if", image_from
                print "it", image_to
                shutil.copyfile(image_from, image_to)
            self.generateAndSaveImage(self.path, name, theme_xml)
            self.loadThemes()
        else:
            # Don't close the dialog - allow the user to change the name of
            # the theme or to cancel the theme dialog completely.
            return False

    def generateAndSaveImage(self, dir, name, theme_xml):
        log.debug(u'generateAndSaveImage %s %s %s', dir, name, theme_xml)
        theme = ThemeXML()
        theme.parse(theme_xml)
        theme.extend_image_filename(dir)
        frame = self.generateImage(theme)
        samplepathname = os.path.join(self.path, name + u'.png')
        if os.path.exists(samplepathname):
            os.unlink(samplepathname)
        frame.save(samplepathname, u'png')
        log.debug(u'Theme image written to %s', samplepathname)

    def generateImage(self, themedata):
        """
        Call the RenderManager to build a Sample Image
        """
        log.debug(u'generateImage %s ', themedata)
        frame = self.parent.RenderManager.generate_preview(themedata)
        return frame

    def getPreviewImage(self, theme):
        log.debug(u'getPreviewImage %s ', theme)
        image = os.path.join(self.path, theme + u'.png')
        return image

    def baseTheme(self):
        log.debug(u'base theme created')
        newtheme = ThemeXML()
        newtheme.new_document(unicode(self.trUtf8(u'New Theme')))
        newtheme.add_background_solid(unicode(u'#000000'))
        newtheme.add_font(unicode(QtGui.QFont().family()), unicode(u'#FFFFFF'),
            unicode(30), u'False')
        newtheme.add_font(unicode(QtGui.QFont().family()), unicode(u'#FFFFFF'),
            unicode(12), u'False', u'footer')
        newtheme.add_display(u'False', unicode(u'#FFFFFF'), u'False',
            unicode(u'#FFFFFF'), unicode(0), unicode(0), unicode(0))
        return newtheme.extract_xml()

    def cleanTheme(self, theme):
        theme.background_color = theme.background_color.strip()
        theme.background_direction = theme.background_direction.strip()
        theme.background_endColor = theme.background_endColor.strip()
        if theme.background_filename:
            theme.background_filename = theme.background_filename.strip()
        #theme.background_mode
        theme.background_startColor = theme.background_startColor.strip()
        #theme.background_type
        if theme.display_display:
            theme.display_display = theme.display_display.strip()
        theme.display_horizontalAlign = theme.display_horizontalAlign.strip()
        theme.display_outline = str_to_bool(theme.display_outline)
        #theme.display_outline_color
        theme.display_shadow = str_to_bool(theme.display_shadow)
        #theme.display_shadow_color
        theme.display_verticalAlign = theme.display_verticalAlign.strip()
        theme.display_wrapStyle = theme.display_wrapStyle.strip()
        theme.font_footer_color = theme.font_footer_color.strip()
        theme.font_footer_height = theme.font_footer_height.strip()
        theme.font_footer_italics = str_to_bool(theme.font_footer_italics)
        theme.font_footer_name = theme.font_footer_name.strip()
        #theme.font_footer_override
        theme.font_footer_proportion = theme.font_footer_proportion.strip()
        theme.font_footer_weight = theme.font_footer_weight.strip()
        theme.font_footer_width = theme.font_footer_width.strip()
        theme.font_footer_x = theme.font_footer_x.strip()
        theme.font_footer_y = theme.font_footer_y.strip()
        theme.font_main_color = theme.font_main_color.strip()
        theme.font_main_height = theme.font_main_height.strip()
        theme.font_main_italics = str_to_bool(theme.font_main_italics)
        theme.font_main_indentation = int(theme.font_main_indentation)
        theme.font_main_name = theme.font_main_name.strip()
        #theme.font_main_override
        theme.font_main_proportion = theme.font_main_proportion.strip()
        theme.font_main_weight = theme.font_main_weight.strip()
        theme.font_main_x = theme.font_main_x.strip()
        theme.font_main_y = theme.font_main_y.strip()
        #theme.theme_mode
        theme.theme_name = theme.theme_name.strip()
        #theme.theme_version
