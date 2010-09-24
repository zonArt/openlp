# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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

import os
import zipfile
import shutil
import logging

from xml.etree.ElementTree import ElementTree, XML
from PyQt4 import QtCore, QtGui

from openlp.core.ui import AmendThemeForm
from openlp.core.theme import Theme
from openlp.core.lib import OpenLPToolbar, context_menu_action, \
    ThemeXML, str_to_bool, get_text_file_string, build_icon, Receiver, \
    context_menu_separator, SettingsManager, translate, check_item_selected
from openlp.core.utils import AppLocation, get_filesystem_encoding

log = logging.getLogger(__name__)

class ThemeManager(QtGui.QWidget):
    """
    Manages the orders of Theme.
    """
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.settingsSection = u'themes'
        self.serviceComboBox = self.parent.ServiceManagerContents.themeComboBox
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.amendThemeForm = AmendThemeForm(self)
        self.toolbar = OpenLPToolbar(self)
        self.toolbar.addToolbarButton(
            translate('OpenLP.ThemeManager', 'New Theme'),
            u':/themes/theme_new.png',
            translate('OpenLP.ThemeManager', 'Create a new theme.'),
            self.onAddTheme)
        self.toolbar.addToolbarButton(
            translate('OpenLP.ThemeManager', 'Edit Theme'),
            u':/themes/theme_edit.png',
            translate('OpenLP.ThemeManager', 'Edit a theme.'),
            self.onEditTheme)
        self.toolbar.addToolbarButton(
            translate('OpenLP.ThemeManager', 'Delete Theme'),
            u':/general/general_delete.png',
            translate('OpenLP.ThemeManager', 'Delete a theme.'),
            self.onDeleteTheme)
        self.toolbar.addSeparator()
        self.toolbar.addToolbarButton(
            translate('OpenLP.ThemeManager', 'Import Theme'),
            u':/general/general_import.png',
            translate('OpenLP.ThemeManager', 'Import a theme.'),
            self.onImportTheme)
        self.toolbar.addToolbarButton(
            translate('OpenLP.ThemeManager', 'Export Theme'),
            u':/general/general_export.png',
            translate('OpenLP.ThemeManager', 'Export a theme.'),
            self.onExportTheme)
        self.themeWidget = QtGui.QWidgetAction(self.toolbar)
        self.layout.addWidget(self.toolbar)
        self.themeListWidget = QtGui.QListWidget(self)
        self.themeListWidget.setAlternatingRowColors(True)
        self.themeListWidget.setIconSize(QtCore.QSize(88, 50))
        self.layout.addWidget(self.themeListWidget)
        self.themeListWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.themeListWidget.addAction(
            context_menu_action(self.themeListWidget,
            u':/themes/theme_edit.png',
            translate('OpenLP.ThemeManager', '&Edit Theme'),
            self.onEditTheme))
        self.themeListWidget.addAction(
            context_menu_separator(self.themeListWidget))
        self.themeListWidget.addAction(
            context_menu_action(self.themeListWidget,
                u':/general/general_delete.png',
                translate('OpenLP.ThemeManager', '&Delete Theme'),
            self.onDeleteTheme))
        self.themeListWidget.addAction(
            context_menu_action(self.themeListWidget,
                u':/general/general_export.png',
                translate('OpenLP.ThemeManager', 'Set As &Global Default'),
            self.changeGlobalFromScreen))
        self.themeListWidget.addAction(
            context_menu_action(self.themeListWidget,
                u':/general/general_export.png',
                translate('OpenLP.ThemeManager', 'E&xport Theme'),
                self.onExportTheme))
        self.themeListWidget.addAction(
            context_menu_separator(self.themeListWidget))
        #Signals
        QtCore.QObject.connect(self.themeListWidget,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
            self.changeGlobalFromScreen)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_global'), self.changeGlobalFromTab)
        #Variables
        self.themelist = []
        self.path = AppLocation.get_section_data_path(self.settingsSection)
        self.checkThemesExists(self.path)
        self.thumbPath = os.path.join(self.path, u'thumbnails')
        self.checkThemesExists(self.thumbPath)
        self.amendThemeForm.path = self.path
        self.oldBackgroundImage = None
        self.editingDefault = False
        # Last little bits of setting up
        self.global_theme = unicode(QtCore.QSettings().value(
            self.settingsSection + u'/global theme',
            QtCore.QVariant(u'')).toString())

    def changeGlobalFromTab(self, themeName):
        """
        Change the global theme when it is changed through the Themes settings
        tab
        """
        log.debug(u'changeGlobalFromTab %s', themeName)
        for count in range (0, self.themeListWidget.count()):
            # reset the old name
            item = self.themeListWidget.item(count)
            oldName = item.text()
            newName = unicode(item.data(QtCore.Qt.UserRole).toString())
            if oldName != newName:
                self.themeListWidget.item(count).setText(newName)
            # Set the new name
            if themeName == newName:
                name = unicode(translate('OpenLP.ThemeManager',
                    '%s (default)')) % newName
                self.themeListWidget.item(count).setText(name)

    def changeGlobalFromScreen(self, index = -1):
        """
        Change the global theme when a theme is double clicked upon in the
        Theme Manager list
        """
        log.debug(u'changeGlobalFromScreen %s', index)
        selected_row = self.themeListWidget.currentRow()
        for count in range (0, self.themeListWidget.count()):
            item = self.themeListWidget.item(count)
            oldName = item.text()
            # reset the old name
            if oldName != unicode(item.data(QtCore.Qt.UserRole).toString()):
                self.themeListWidget.item(count).setText(
                    unicode(item.data(QtCore.Qt.UserRole).toString()))
            # Set the new name
            if count == selected_row:
                self.global_theme = unicode(
                    self.themeListWidget.item(count).text())
                name = unicode(translate('OpenLP.ThemeManager',
                    '%s (default)')) % self.global_theme
                self.themeListWidget.item(count).setText(name)
                QtCore.QSettings().setValue(
                    self.settingsSection + u'/global theme',
                    QtCore.QVariant(self.global_theme))
                Receiver.send_message(u'theme_update_global',
                    self.global_theme)
                self.pushThemes()

    def onAddTheme(self):
        """
        Loads a new theme with the default settings and then launches the theme
        editing form for the user to make their customisations.
        """
        theme = self.createThemeFromXml(self.baseTheme(), self.path)
        self.amendThemeForm.loadTheme(theme)
        self.saveThemeName = u''
        self.amendThemeForm.exec_()

    def onEditTheme(self):
        """
        Loads the settings for the theme that is to be edited and launches the
        theme editing form so the user can make their changes.
        """
        if check_item_selected(self.themeListWidget,
            translate('OpenLP.ThemeManager',
            'You must select a theme to edit.')):
            item = self.themeListWidget.currentItem()
            themeName = unicode(item.text())
            if themeName != unicode(item.data(QtCore.Qt.UserRole).toString()):
                self.editingDefault = True
            theme = self.getThemeData(
                unicode(item.data(QtCore.Qt.UserRole).toString()))
            if theme.background_type == u'image':
                self.oldBackgroundImage = theme.background_filename
            self.amendThemeForm.loadTheme(theme)
            self.saveThemeName = unicode(
                item.data(QtCore.Qt.UserRole).toString())
            self.amendThemeForm.exec_()

    def onDeleteTheme(self):
        """
        Delete a theme
        """
        self.global_theme = unicode(QtCore.QSettings().value(
            self.settingsSection + u'/global theme',
            QtCore.QVariant(u'')).toString())
        if check_item_selected(self.themeListWidget,
            translate('OpenLP.ThemeManager',
            'You must select a theme to delete.')):
            item = self.themeListWidget.currentItem()
            theme = unicode(item.text())
            # confirm deletion
            answer = QtGui.QMessageBox.question(self,
                translate('OpenLP.ThemeManager', 'Delete Confirmation'),
                translate('OpenLP.ThemeManager', 'Delete theme?'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No), QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.No:
                return
            # should be the same unless default
            if theme != unicode(item.data(QtCore.Qt.UserRole).toString()):
                QtGui.QMessageBox.critical(self,
                    translate('OpenLP.ThemeManager', 'Error'),
                    translate('OpenLP.ThemeManager',
                        'You are unable to delete the default theme.'))
            else:
                for plugin in self.parent.plugin_manager.plugins:
                    if plugin.usesTheme(theme):
                        QtGui.QMessageBox.critical(self,
                            translate('OpenLP.ThemeManager', 'Error'),
                            unicode(translate('OpenLP.ThemeManager',
                                'Theme %s is used in the %s plugin.')) % \
                                (theme, plugin.name))
                        return
                if unicode(self.serviceComboBox.currentText()) == theme:
                    QtGui.QMessageBox.critical(self,
                        translate('OpenLP.ThemeManager', 'Error'),
                        unicode(translate('OpenLP.ThemeManager',
                        'Theme %s is used by the service manager.')) % theme)
                    return
                row = self.themeListWidget.row(item)
                self.themeListWidget.takeItem(row)
                self.deleteTheme(theme)

    def deleteTheme(self, theme):
        """
        Delete a theme.

        ``theme``
            The theme to delete.
        """
        self.themelist.remove(theme)
        thumb = theme + u'.png'
        try:
            os.remove(os.path.join(self.path, thumb))
            os.remove(os.path.join(self.thumbPath, thumb))
            encoding = get_filesystem_encoding()
            shutil.rmtree(os.path.join(self.path, theme).encode(encoding))
        except OSError:
            log.exception(u'Error deleting theme %s', theme)
        # As we do not reload the themes push out the change
        # Reaload the list as the internal lists and events need
        # to be triggered
        self.pushThemes()

    def onExportTheme(self):
        """
        Save the theme in a zip file
        """
        item = self.themeListWidget.currentItem()
        if item is None:
            QtGui.QMessageBox.critical(self,
                translate('OpenLP.ThemeManager', 'Error'),
                translate('OpenLP.ThemeManager',
                'You have not selected a theme.'))
            return
        theme = unicode(item.data(QtCore.Qt.UserRole).toString())
        path = QtGui.QFileDialog.getExistingDirectory(self,
            unicode(translate('OpenLP.ThemeManager',
            'Save Theme - (%s)')) %  theme,
            SettingsManager.get_last_dir(self.settingsSection, 1))
        path = unicode(path)
        if path:
            SettingsManager.set_last_dir(self.settingsSection, path, 1)
            themePath = os.path.join(path, theme + u'.otz')
            zip = None
            try:
                zip = zipfile.ZipFile(themePath, u'w')
                source = os.path.join(self.path, theme)
                for files in os.walk(source):
                    for name in files[2]:
                        zip.write(
                            os.path.join(source, name).encode(u'utf-8'),
                            os.path.join(theme, name).encode(u'utf-8'))
                QtGui.QMessageBox.information(self,
                    translate('OpenLP.ThemeManager', 'Theme Exported'),
                    translate('OpenLP.ThemeManager',
                        'Your theme has been successfully exported.'))
            except (IOError, OSError):
                log.exception(u'Export Theme Failed')
                QtGui.QMessageBox.critical(self,
                    translate('OpenLP.ThemeManager', 'Theme Export Failed'),
                    translate('OpenLP.ThemeManager',
                        'Your theme could not be exported due to an error.'))
            finally:
                if zip:
                    zip.close()

    def onImportTheme(self):
        """
        Opens a file dialog to select the theme file(s) to import before
        attempting to extract OpenLP themes from those files.  This process
        will load both OpenLP version 1 and version 2 themes.
        """
        files = QtGui.QFileDialog.getOpenFileNames(self,
            translate('OpenLP.ThemeManager', 'Select Theme Import File'),
            SettingsManager.get_last_dir(self.settingsSection),
            translate('OpenLP.ThemeManager', 'Theme (*.*)'))
        log.info(u'New Themes %s', unicode(files))
        if files:
            for file in files:
                SettingsManager.set_last_dir(
                    self.settingsSection, unicode(file))
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
        self.themeListWidget.clear()
        dirList = os.listdir(self.path)
        for name in dirList:
            if name.endswith(u'.png'):
                # check to see file is in theme root directory
                theme = os.path.join(self.path, name)
                if os.path.exists(theme):
                    textName = os.path.splitext(name)[0]
                    if textName == self.global_theme:
                        name = unicode(translate('OpenLP.ThemeManager',
                            '%s (default)')) % textName
                    else:
                        name = textName
                    thumb = os.path.join(self.thumbPath, u'%s.png' % textName)
                    item_name = QtGui.QListWidgetItem(name)
                    if os.path.exists(thumb):
                        icon = build_icon(thumb)
                    else:
                        icon = build_icon(theme)
                        pixmap = icon.pixmap(QtCore.QSize(88, 50))
                        pixmap.save(thumb, u'png')
                    item_name.setIcon(icon)
                    item_name.setData(QtCore.Qt.UserRole,
                        QtCore.QVariant(textName))
                    self.themeListWidget.addItem(item_name)
                    self.themelist.append(textName)
        self.pushThemes()

    def pushThemes(self):
        """
        Notify listeners that the theme list has been updated
        """
        Receiver.send_message(u'theme_update_list', self.getThemes())

    def getThemes(self):
        """
        Return the list of loaded themes
        """
        return self.themelist

    def getThemeData(self, themename):
        """
        Returns a theme object from an XML file

        ``themename``
            Name of the theme to load from file
        """
        log.debug(u'getthemedata for theme %s', themename)
        xml_file = os.path.join(self.path, unicode(themename),
            unicode(themename) + u'.xml')
        xml = get_text_file_string(xml_file)
        if not xml:
            xml = self.baseTheme()
        return self.createThemeFromXml(xml, self.path)

    def checkThemesExists(self, dir):
        """
        Check a theme directory exists and if not create it

        ``dir``
            Theme directory to make sure exists
        """
        log.debug(u'check themes')
        if not os.path.exists(dir):
            os.mkdir(dir)

    def unzipTheme(self, filename, dir):
        """
        Unzip the theme, remove the preview file if stored
        Generate a new preview fileCheck the XML theme version and upgrade if
        necessary.
        """
        log.debug(u'Unzipping theme %s', filename)
        filename = unicode(filename)
        zip = None
        outfile = None
        try:
            zip = zipfile.ZipFile(filename)
            filexml = None
            themename = None
            for file in zip.namelist():
                try:
                    ucsfile = file.decode(u'utf-8')
                except UnicodeDecodeError:
                    QtGui.QMessageBox.critical(
                        self, translate('OpenLP.ThemeManager', 'Error'),
                        translate('OpenLP.ThemeManager',
                            'File is not a valid theme.\n'
                            'The content encoding is not UTF-8.'))
                    log.exception(u'Filename "%s" is not valid UTF-8' %
                        file.decode(u'utf-8', u'replace'))
                    continue
                osfile = unicode(QtCore.QDir.toNativeSeparators(ucsfile))
                theme_dir = None
                if osfile.endswith(os.path.sep):
                    theme_dir = os.path.join(dir, osfile)
                    if not os.path.exists(theme_dir):
                        os.mkdir(os.path.join(dir, osfile))
                else:
                    fullpath = os.path.join(dir, osfile)
                    names = osfile.split(os.path.sep)
                    if len(names) > 1:
                        # not preview file
                        if themename is None:
                            themename = names[0]
                        if theme_dir is None:
                            theme_dir = os.path.join(dir, names[0])
                            if not os.path.exists(theme_dir):
                                os.mkdir(os.path.join(dir, names[0]))
                        if os.path.splitext(ucsfile)[1].lower() in [u'.xml']:
                            xml_data = zip.read(file)
                            try:
                                xml_data = xml_data.decode(u'utf-8')
                            except UnicodeDecodeError:
                                log.exception(u'Theme XML is not UTF-8 '
                                    u'encoded.')
                                break
                            filexml = self.checkVersionAndConvert(xml_data)
                            outfile = open(fullpath, u'w')
                            outfile.write(filexml.encode(u'utf-8'))
                        else:
                            outfile = open(fullpath, u'wb')
                            outfile.write(zip.read(file))
            if filexml:
                self.generateAndSaveImage(dir, themename, filexml)
            else:
                QtGui.QMessageBox.critical(self,
                    translate('OpenLP.ThemeManager', 'Error'),
                    translate('OpenLP.ThemeManager',
                        'File is not a valid theme.'))
                log.exception(u'Theme file does not contain XML data %s' %
                    filename)
        except (IOError, NameError):
            QtGui.QMessageBox.critical(self,
                translate('OpenLP.ThemeManager', 'Error'),
                translate('OpenLP.ThemeManager', 'File is not a valid theme.'))
            log.exception(u'Importing theme from zip failed %s' % filename)
        finally:
            if zip:
                zip.close()
            if outfile:
                outfile.close()

    def checkVersionAndConvert(self, xml_data):
        """
        Check if a theme is from OpenLP version 1

        ``xml_data``
            Theme XML to check the version of
        """
        log.debug(u'checkVersion1 ')
        theme = xml_data.encode(u'ascii', u'xmlcharrefreplace')
        tree = ElementTree(element=XML(theme)).getroot()
        # look for old version 1 tags
        if tree.find(u'BackgroundType') is None:
            return xml_data
        else:
            return self.migrateVersion122(xml_data)

    def migrateVersion122(self, xml_data):
        """
        Convert the xml data from version 1 format to the current format.

        New fields are loaded with defaults to provide a complete, working
        theme containing all compatible customisations from the old theme.

        ``xml_data``
            Version 1 theme to convert
        """
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
        vAlignCorrection = 0
        if theme.VerticalAlign == 2:
            vAlignCorrection = 1
        elif theme.VerticalAlign == 1:
            vAlignCorrection = 2
        newtheme.add_display(unicode(shadow),
            unicode(theme.ShadowColor.name()),
            unicode(outline), unicode(theme.OutlineColor.name()),
            unicode(theme.HorizontalAlign), unicode(vAlignCorrection),
            unicode(theme.WrapStyle), unicode(0))
        return newtheme.extract_xml()

    def saveTheme(self, name, theme_xml, theme_pretty_xml, image_from,
        image_to):
        """
        Called by thememaintenance Dialog to save the theme
        and to trigger the reload of the theme list
        """
        log.debug(u'saveTheme %s %s', name, theme_xml)
        theme_dir = os.path.join(self.path, name)
        if not os.path.exists(theme_dir):
            os.mkdir(os.path.join(self.path, name))
        theme_file = os.path.join(theme_dir, name + u'.xml')
        log.debug(theme_file)
        editedServiceTheme = False
        result = QtGui.QMessageBox.Yes
        if self.saveThemeName != name:
            if os.path.exists(theme_file):
                result = QtGui.QMessageBox.question(self,
                    translate('OpenLP.ThemeManager', 'Theme Exists'),
                    translate('OpenLP.ThemeManager',
                        'A theme with this name already '
                        'exists. Would you like to overwrite it?'),
                    (QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
                    QtGui.QMessageBox.No)
            if self.saveThemeName != u'':
                for plugin in self.parent.plugin_manager.plugins:
                    if plugin.usesTheme(self.saveThemeName):
                        plugin.renameTheme(self.saveThemeName, name)
                if unicode(self.serviceComboBox.currentText()) == name:
                    editedServiceTheme = True
                self.deleteTheme(self.saveThemeName)
        if result == QtGui.QMessageBox.Yes:
            # Save the theme, overwriting the existing theme if necessary.
            if image_to and self.oldBackgroundImage and \
                image_to != self.oldBackgroundImage:
                try:
                    os.remove(self.oldBackgroundImage)
                except OSError:
                    log.exception(u'Unable to remove old theme background')
            outfile = None
            try:
                outfile = open(theme_file, u'w')
                outfile.write(theme_pretty_xml)
            except IOError:
                log.exception(u'Saving theme to file failed')
            finally:
                if outfile:
                    outfile.close()
            if image_from and image_from != image_to:
                try:
                    encoding = get_filesystem_encoding()
                    shutil.copyfile(
                        unicode(image_from).encode(encoding),
                        unicode(image_to).encode(encoding))
                except IOError:
                    log.exception(u'Failed to save theme image')
            self.generateAndSaveImage(self.path, name, theme_xml)
            self.loadThemes()
            # Check if we need to set a new service theme
            if editedServiceTheme:
                newThemeIndex = self.serviceComboBox.findText(name)
                if newThemeIndex != -1:
                    self.serviceComboBox.setCurrentIndex(newThemeIndex)
            if self.editingDefault:
                if self.saveThemeName != name:
                    newThemeItem = self.themeListWidget.findItems(name,
                        QtCore.Qt.MatchExactly)[0]
                    newThemeIndex = self.themeListWidget.indexFromItem(
                        newThemeItem).row()
                    self.global_theme = unicode(
                        self.themeListWidget.item(newThemeIndex).text())
                    newName = unicode(translate('OpenLP.ThemeManager',
                        '%s (default)')) % self.global_theme
                    self.themeListWidget.item(newThemeIndex).setText(newName)
                    QtCore.QSettings().setValue(
                        self.settingsSection + u'/global theme',
                        QtCore.QVariant(self.global_theme))
                    Receiver.send_message(u'theme_update_global',
                        self.global_theme)
                self.editingDefault = False
                self.pushThemes()
        else:
            # Don't close the dialog - allow the user to change the name of
            # the theme or to cancel the theme dialog completely.
            return False

    def generateAndSaveImage(self, dir, name, theme_xml):
        log.debug(u'generateAndSaveImage %s %s %s', dir, name, theme_xml)
        theme = self.createThemeFromXml(theme_xml, dir)
        frame = self.generateImage(theme)
        samplepathname = os.path.join(self.path, name + u'.png')
        if os.path.exists(samplepathname):
            os.unlink(samplepathname)
        frame.save(samplepathname, u'png')
        thumb = os.path.join(self.thumbPath, u'%s.png' % name)
        icon = build_icon(frame)
        pixmap = icon.pixmap(QtCore.QSize(88, 50))
        pixmap.save(thumb, u'png')
        log.debug(u'Theme image written to %s', samplepathname)

    def generateImage(self, themedata):
        """
        Call the RenderManager to build a Sample Image
        """
        log.debug(u'generateImage \n%s ', themedata)
        return self.parent.RenderManager.generate_preview(themedata)

    def getPreviewImage(self, theme):
        """
        Return an image representing the look of the theme

        ``theme``
            The theme to return the image for
        """
        log.debug(u'getPreviewImage %s ', theme)
        image = os.path.join(self.path, theme + u'.png')
        return image

    def baseTheme(self):
        """
        Provide a base theme with sensible defaults
        """
        log.debug(u'base theme created')
        newtheme = ThemeXML()
        newtheme.new_document(
            unicode(translate('OpenLP.ThemeManager', 'New Theme')))
        newtheme.add_background_solid(u'#000000')
        newtheme.add_font(unicode(QtGui.QFont().family()), u'#FFFFFF',
            u'30', u'False')
        newtheme.add_font(unicode(QtGui.QFont().family()), u'#FFFFFF',
            u'12', u'False', u'footer')
        newtheme.add_display(u'False', u'#FFFFFF', u'False',
            unicode(u'#FFFFFF'), u'0', u'0', u'0', u'False')
        return newtheme.extract_xml()

    def createThemeFromXml(self, theme_xml, path):
        """
        Return a theme object using information parsed from XML

        ``theme_xml``
            The XML data to load into the theme
        """
        theme = ThemeXML()
        theme.parse(theme_xml)
        theme.extend_image_filename(path)
        return theme
