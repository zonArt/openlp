# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
import locale
import re

from xml.etree.ElementTree import ElementTree, XML
from PyQt4 import QtCore, QtGui

from openlp.core.lib import OpenLPToolbar, get_text_file_string, build_icon, \
    Receiver, SettingsManager, translate, check_item_selected, \
    check_directory_exists, create_thumb, validate_thumb
from openlp.core.lib.theme import ThemeXML, BackgroundType, VerticalType, \
    BackgroundGradientType
from openlp.core.lib.ui import UiStrings, critical_error_message_box, \
    context_menu_action, context_menu_separator
from openlp.core.theme import Theme
from openlp.core.ui import FileRenameForm, ThemeForm
from openlp.core.utils import AppLocation, delete_file, get_filesystem_encoding

log = logging.getLogger(__name__)

class ThemeManager(QtGui.QWidget):
    """
    Manages the orders of Theme.
    """
    def __init__(self, mainwindow, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.mainwindow = mainwindow
        self.settingsSection = u'themes'
        self.themeForm = ThemeForm(self)
        self.fileRenameForm = FileRenameForm(self)
        # start with the layout
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.layout.setObjectName(u'layout')
        self.toolbar = OpenLPToolbar(self)
        self.toolbar.addToolbarButton(UiStrings().NewTheme,
            u':/themes/theme_new.png',
            translate('OpenLP.ThemeManager', 'Create a new theme.'),
            self.onAddTheme)
        self.toolbar.addToolbarButton(
            translate('OpenLP.ThemeManager', 'Edit Theme'),
            u':/themes/theme_edit.png',
            translate('OpenLP.ThemeManager', 'Edit a theme.'),
            self.onEditTheme)
        self.deleteToolbarAction = self.toolbar.addToolbarButton(
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
        self.toolbar.setObjectName(u'toolbar')
        self.layout.addWidget(self.toolbar)
        self.themeWidget = QtGui.QWidgetAction(self.toolbar)
        self.themeWidget.setObjectName(u'themeWidget')
        # create theme manager list
        self.themeListWidget = QtGui.QListWidget(self)
        self.themeListWidget.setAlternatingRowColors(True)
        self.themeListWidget.setIconSize(QtCore.QSize(88, 50))
        self.themeListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.themeListWidget.setObjectName(u'themeListWidget')
        self.layout.addWidget(self.themeListWidget)
        QtCore.QObject.connect(self.themeListWidget,
            QtCore.SIGNAL('customContextMenuRequested(QPoint)'),
            self.contextMenu)
        # build the context menu
        self.menu = QtGui.QMenu()
        self.editAction = context_menu_action(
            self.menu, u':/themes/theme_edit.png',
            translate('OpenLP.ThemeManager', '&Edit Theme'), self.onEditTheme)
        self.copyAction = context_menu_action(
            self.menu, u':/themes/theme_edit.png',
            translate('OpenLP.ThemeManager', '&Copy Theme'), self.onCopyTheme)
        self.renameAction = context_menu_action(
            self.menu, u':/themes/theme_edit.png',
            translate('OpenLP.ThemeManager', '&Rename Theme'),
            self.onRenameTheme)
        self.deleteAction = context_menu_action(
            self.menu, u':/general/general_delete.png',
            translate('OpenLP.ThemeManager', '&Delete Theme'),
            self.onDeleteTheme)
        context_menu_separator(self.menu)
        self.globalAction = context_menu_action(
            self.menu, u':/general/general_export.png',
            translate('OpenLP.ThemeManager', 'Set As &Global Default'),
            self.changeGlobalFromScreen)
        self.exportAction = context_menu_action(
            self.menu, u':/general/general_export.png',
            translate('OpenLP.ThemeManager', '&Export Theme'),
            self.onExportTheme)
        # Signals
        QtCore.QObject.connect(self.themeListWidget,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
            self.changeGlobalFromScreen)
        QtCore.QObject.connect(self.themeListWidget, QtCore.SIGNAL(
            u'currentItemChanged(QListWidgetItem *, QListWidgetItem *)'),
            self.checkListState)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_global'), self.changeGlobalFromTab)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_updated'), self.configUpdated)
        # Variables
        self.theme_list = []
        self.path = AppLocation.get_section_data_path(self.settingsSection)
        check_directory_exists(self.path)
        self.thumb_path = os.path.join(self.path, u'thumbnails')
        check_directory_exists(self.thumb_path)
        self.themeForm.path = self.path
        self.old_background_image = None
        self.bad_v1_name_chars = re.compile(r'[%+\[\]]')
        # Last little bits of setting up
        self.configUpdated()

    def firstTime(self):
        """
        Import new themes downloaded by the first time wizard
        """
        Receiver.send_message(u'cursor_busy')
        encoding = get_filesystem_encoding()
        files = SettingsManager.get_files(self.settingsSection, u'.otz')
        for file in files:
            file = os.path.join(self.path, file).encode(encoding)
            self.unzipTheme(file, self.path)
            delete_file(file)
        Receiver.send_message(u'cursor_normal')

    def configUpdated(self):
        """
        Triggered when Config dialog is updated.
        """
        self.global_theme = unicode(QtCore.QSettings().value(
            self.settingsSection + u'/global theme',
            QtCore.QVariant(u'')).toString())

    def checkListState(self, item):
        """
        If Default theme selected remove delete button.
        """
        if item is None:
            return
        real_theme_name = unicode(item.data(QtCore.Qt.UserRole).toString())
        theme_name = unicode(item.text())
        # If default theme restrict actions
        if real_theme_name == theme_name:
            self.deleteToolbarAction.setVisible(True)
        else:
            self.deleteToolbarAction.setVisible(False)

    def contextMenu(self, point):
        """
        Build the Right Click Context menu and set state depending on
        the type of theme.
        """
        item = self.themeListWidget.itemAt(point)
        if item is None:
            return
        real_theme_name = unicode(item.data(QtCore.Qt.UserRole).toString())
        theme_name = unicode(item.text())
        self.deleteAction.setVisible(False)
        self.renameAction.setVisible(False)
        self.globalAction.setVisible(False)
        # If default theme restrict actions
        if real_theme_name == theme_name:
            self.deleteAction.setVisible(True)
            self.renameAction.setVisible(True)
            self.globalAction.setVisible(True)
        self.menu.exec_(self.themeListWidget.mapToGlobal(point))

    def changeGlobalFromTab(self, theme_name):
        """
        Change the global theme when it is changed through the Themes settings
        tab
        """
        log.debug(u'changeGlobalFromTab %s', theme_name)
        for count in range (0, self.themeListWidget.count()):
            # reset the old name
            item = self.themeListWidget.item(count)
            old_name = item.text()
            new_name = unicode(item.data(QtCore.Qt.UserRole).toString())
            if old_name != new_name:
                self.themeListWidget.item(count).setText(new_name)
            # Set the new name
            if theme_name == new_name:
                name = unicode(translate('OpenLP.ThemeManager',
                    '%s (default)')) % new_name
                self.themeListWidget.item(count).setText(name)

    def changeGlobalFromScreen(self, index=-1):
        """
        Change the global theme when a theme is double clicked upon in the
        Theme Manager list
        """
        log.debug(u'changeGlobalFromScreen %s', index)
        selected_row = self.themeListWidget.currentRow()
        for count in range (0, self.themeListWidget.count()):
            item = self.themeListWidget.item(count)
            old_name = item.text()
            # reset the old name
            if old_name != unicode(item.data(QtCore.Qt.UserRole).toString()):
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
                self._pushThemes()

    def onAddTheme(self):
        """
        Loads a new theme with the default settings and then launches the theme
        editing form for the user to make their customisations.
        """
        theme = ThemeXML()
        self.themeForm.theme = theme
        self.themeForm.exec_()

    def onRenameTheme(self):
        """
        Renames an existing theme to a new name
        """
        if self._validate_theme_action(unicode(translate('OpenLP.ThemeManager',
            'You must select a theme to rename.')),
            unicode(translate('OpenLP.ThemeManager', 'Rename Confirmation')),
            unicode(translate('OpenLP.ThemeManager', 'Rename %s theme?')),
            False, False):
            item = self.themeListWidget.currentItem()
            old_theme_name = unicode(item.data(QtCore.Qt.UserRole).toString())
            self.fileRenameForm.fileNameEdit.setText(old_theme_name)
            if self.fileRenameForm.exec_():
                new_theme_name = unicode(self.fileRenameForm.fileNameEdit.text())
                if old_theme_name == new_theme_name:
                    return
                if self.checkIfThemeExists(new_theme_name):
                    old_theme_data = self.getThemeData(old_theme_name)
                    self.cloneThemeData(old_theme_data, new_theme_name)
                    self.deleteTheme(old_theme_name)
                    for plugin in self.mainwindow.pluginManager.plugins:
                        if plugin.usesTheme(old_theme_name):
                            plugin.renameTheme(old_theme_name, new_theme_name)
                    self.loadThemes()

    def onCopyTheme(self):
        """
        Copies an existing theme to a new name
        """
        item = self.themeListWidget.currentItem()
        old_theme_name = unicode(item.data(QtCore.Qt.UserRole).toString())
        self.fileRenameForm.fileNameEdit.setText(
            unicode(translate('OpenLP.ThemeManager',
            'Copy of %s', 'Copy of <theme name>')) % old_theme_name)
        if self.fileRenameForm.exec_(True):
            new_theme_name = unicode(self.fileRenameForm.fileNameEdit.text())
            if self.checkIfThemeExists(new_theme_name):
                theme_data = self.getThemeData(old_theme_name)
                self.cloneThemeData(theme_data, new_theme_name)

    def cloneThemeData(self, theme_data, new_theme_name):
        """
        Takes a theme and makes a new copy of it as well as saving it.
        """
        log.debug(u'cloneThemeData')
        save_to = None
        save_from = None
        if theme_data.background_type == u'image':
            save_to = os.path.join(self.path, new_theme_name,
                os.path.split(unicode(theme_data.background_filename))[1])
            save_from = theme_data.background_filename
        theme_data.theme_name = new_theme_name
        theme_data.extend_image_filename(self.path)
        self.saveTheme(theme_data, save_from, save_to)

    def onEditTheme(self):
        """
        Loads the settings for the theme that is to be edited and launches the
        theme editing form so the user can make their changes.
        """
        if check_item_selected(self.themeListWidget,
            translate('OpenLP.ThemeManager',
            'You must select a theme to edit.')):
            item = self.themeListWidget.currentItem()
            theme = self.getThemeData(
                unicode(item.data(QtCore.Qt.UserRole).toString()))
            if theme.background_type == u'image':
                self.old_background_image = theme.background_filename
            self.themeForm.theme = theme
            self.themeForm.exec_(True)
            self.old_background_image = None

    def onDeleteTheme(self):
        """
        Delete a theme
        """
        if self._validate_theme_action(unicode(translate('OpenLP.ThemeManager',
            'You must select a theme to delete.')),
            unicode(translate('OpenLP.ThemeManager', 'Delete Confirmation')),
            unicode(translate('OpenLP.ThemeManager', 'Delete %s theme?'))):
            item = self.themeListWidget.currentItem()
            theme = unicode(item.text())
            row = self.themeListWidget.row(item)
            self.themeListWidget.takeItem(row)
            self.deleteTheme(theme)
            # As we do not reload the themes, push out the change. Reload the
            # list as the internal lists and events need to be triggered.
            self._pushThemes()

    def deleteTheme(self, theme):
        """
        Delete a theme.

        ``theme``
            The theme to delete.
        """
        self.theme_list.remove(theme)
        thumb = u'%s.png' % theme
        delete_file(os.path.join(self.path, thumb))
        delete_file(os.path.join(self.thumb_path, thumb))
        try:
            encoding = get_filesystem_encoding()
            shutil.rmtree(os.path.join(self.path, theme).encode(encoding))
        except OSError:
            log.exception(u'Error deleting theme %s', theme)

    def onExportTheme(self):
        """
        Export the theme in a zip file
        """
        item = self.themeListWidget.currentItem()
        if item is None:
            critical_error_message_box(message=translate('OpenLP.ThemeManager',
                'You have not selected a theme.'))
            return
        theme = unicode(item.data(QtCore.Qt.UserRole).toString())
        path = QtGui.QFileDialog.getExistingDirectory(self,
            unicode(translate('OpenLP.ThemeManager',
            'Save Theme - (%s)')) % theme,
            SettingsManager.get_last_dir(self.settingsSection, 1))
        path = unicode(path)
        Receiver.send_message(u'cursor_busy')
        if path:
            SettingsManager.set_last_dir(self.settingsSection, path, 1)
            theme_path = os.path.join(path, theme + u'.otz')
            zip = None
            try:
                zip = zipfile.ZipFile(theme_path, u'w')
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
                critical_error_message_box(
                    translate('OpenLP.ThemeManager', 'Theme Export Failed'),
                    translate('OpenLP.ThemeManager',
                    'Your theme could not be exported due to an error.'))
            finally:
                if zip:
                    zip.close()
        Receiver.send_message(u'cursor_normal')

    def onImportTheme(self):
        """
        Opens a file dialog to select the theme file(s) to import before
        attempting to extract OpenLP themes from those files. This process
        will load both OpenLP version 1 and version 2 themes.
        """
        files = QtGui.QFileDialog.getOpenFileNames(self,
            translate('OpenLP.ThemeManager', 'Select Theme Import File'),
            SettingsManager.get_last_dir(self.settingsSection),
            unicode(translate('OpenLP.ThemeManager',
            'OpenLP Themes (*.theme *.otz)')))
        log.info(u'New Themes %s', unicode(files))
        if not files:
            return
        Receiver.send_message(u'cursor_busy')
        for file in files:
            SettingsManager.set_last_dir(self.settingsSection, unicode(file))
            self.unzipTheme(file, self.path)
        self.loadThemes()
        Receiver.send_message(u'cursor_normal')

    def loadThemes(self, firstTime=False):
        """
        Loads the theme lists and triggers updates accross the whole system
        using direct calls or core functions and events for the plugins.
        The plugins will call back in to get the real list if they want it.
        """
        log.debug(u'Load themes from dir')
        self.theme_list = []
        self.themeListWidget.clear()
        files = SettingsManager.get_files(self.settingsSection, u'.png')
        if firstTime:
            self.firstTime()
            files = SettingsManager.get_files(self.settingsSection, u'.png')
            # No themes have been found so create one
            if len(files) == 0:
                theme = ThemeXML()
                theme.theme_name = UiStrings().Default
                self._writeTheme(theme, None, None)
                QtCore.QSettings().setValue(
                    self.settingsSection + u'/global theme',
                    QtCore.QVariant(theme.theme_name))
                self.configUpdated()
                files = SettingsManager.get_files(self.settingsSection, u'.png')
        # Sort the themes by its name considering language specific characters.
        # lower() is needed for windows!
        files.sort(key=lambda file_name: unicode(file_name).lower(),
           cmp=locale.strcoll)
        # now process the file list of png files
        for name in files:
            # check to see file is in theme root directory
            theme = os.path.join(self.path, name)
            if os.path.exists(theme):
                text_name = os.path.splitext(name)[0]
                if text_name == self.global_theme:
                    name = unicode(translate('OpenLP.ThemeManager',
                        '%s (default)')) % text_name
                else:
                    name = text_name
                thumb = os.path.join(self.thumb_path, u'%s.png' % text_name)
                item_name = QtGui.QListWidgetItem(name)
                if validate_thumb(theme, thumb):
                    icon = build_icon(thumb)
                else:
                    icon = create_thumb(theme, thumb)
                item_name.setIcon(icon)
                item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(text_name))
                self.themeListWidget.addItem(item_name)
                self.theme_list.append(text_name)
        self._pushThemes()

    def _pushThemes(self):
        """
        Notify listeners that the theme list has been updated
        """
        Receiver.send_message(u'theme_update_list', self.getThemes())

    def getThemes(self):
        """
        Return the list of loaded themes
        """
        return self.theme_list

    def getThemeData(self, theme_name):
        """
        Returns a theme object from an XML file

        ``theme_name``
            Name of the theme to load from file
        """
        log.debug(u'getthemedata for theme %s', theme_name)
        xml_file = os.path.join(self.path, unicode(theme_name),
            unicode(theme_name) + u'.xml')
        xml = get_text_file_string(xml_file)
        if not xml:
            log.debug("No theme data - using default theme")
            return ThemeXML()
        else:
            return self._createThemeFromXml(xml, self.path)
            
    def overWriteMessageBox(self, theme_name):
        ret = QtGui.QMessageBox.question(self,
            translate('OpenLP.ThemeManager', 'Theme Already Exists'), 
            translate('OpenLP.ThemeManager',  
                'Theme %s already exists. Do you want to replace it?' 
                % theme_name),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No),
            QtGui.QMessageBox.No)
        return ret == QtGui.QMessageBox.Yes

    def unzipTheme(self, file_name, dir):
        """
        Unzip the theme, remove the preview file if stored
        Generate a new preview file. Check the XML theme version and upgrade if
        necessary.
        """
        log.debug(u'Unzipping theme %s', file_name)
        file_name = unicode(file_name)
        zip = None
        out_file = None
        file_xml = None
        try:
            zip = zipfile.ZipFile(file_name)
            xml_file = filter(lambda name:
                os.path.splitext(name)[1].lower() == u'.xml', zip.namelist())
            if len(xml_file) != 1:
                log.exception(u'Theme contains "%s" XML files' % len(xml_file))
                raise Exception(u'validation')
            xml_tree = ElementTree(element=XML(zip.read(xml_file[0]))).getroot()
            v1_background = xml_tree.find(u'BackgroundType')
            if v1_background is not None:
                theme_name, file_xml, out_file, abort_import = self.unzipVersion122(dir, zip,
                    xml_file[0], xml_tree, v1_background, out_file)
            else:
                theme_name = xml_tree.find(u'name').text.strip()
                theme_folder = os.path.join(dir, theme_name)
                theme_exists = os.path.exists(theme_folder)
                if theme_exists and not self.overWriteMessageBox(theme_name):
                    abort_import = True
                    return
                else:
                    abort_import = False
                for name in zip.namelist():
                    try:
                        uname = unicode(name, u'utf-8')
                    except UnicodeDecodeError:
                        log.exception(u'Theme file contains non utf-8 filename'
                            u' "%s"' % name.decode(u'utf-8', u'replace'))
                        raise Exception(u'validation')
                    uname = unicode(QtCore.QDir.toNativeSeparators(uname))
                    split_name = uname.split(os.path.sep)
                    if split_name[-1] == u'' or len(split_name) == 1:
                        # is directory or preview file
                        continue
                    full_name = os.path.join(dir, uname)
                    check_directory_exists(os.path.dirname(full_name))
                    if os.path.splitext(uname)[1].lower() == u'.xml':
                        file_xml = unicode(zip.read(name), u'utf-8')
                        out_file = open(full_name, u'w')
                        out_file.write(file_xml.encode(u'utf-8'))
                    else:
                        out_file = open(full_name, u'wb')
                        out_file.write(zip.read(name))
                    out_file.close()
        except (IOError, zipfile.BadZipfile):
            log.exception(u'Importing theme from zip failed %s' % file_name)
            raise Exception(u'validation')
        except Exception as info:
            if unicode(info) == u'validation':
                critical_error_message_box(translate('OpenLP.ThemeManager',
                    'Validation Error'), translate('OpenLP.ThemeManager',
                    'File is not a valid theme.'))
            else:
                raise
        finally:
            # Close the files, to be able to continue creating the theme.
            if zip:
                zip.close()
            if out_file:
                out_file.close()
            if not abort_import:
                # As all files are closed, we can create the Theme.
                if file_xml:
                    theme = self._createThemeFromXml(file_xml, self.path)
                    self.generateAndSaveImage(dir, theme_name, theme)
                # Only show the error message, when IOError was not raised (in this
                # case the error message has already been shown).
                elif zip is not None:
                    critical_error_message_box(
                        translate('OpenLP.ThemeManager', 'Validation Error'),
                        translate('OpenLP.ThemeManager',
                        'File is not a valid theme.'))
                    log.exception(u'Theme file does not contain XML data %s' %
                        file_name)

    def unzipVersion122(self, dir, zip, xml_file, xml_tree, background, out_file):
        """
        Unzip openlp.org 1.2x theme file and upgrade the theme xml. When calling
        this method, please keep in mind, that some parameters are redundant.
        """
        theme_name = xml_tree.find(u'Name').text.strip()
        theme_name = self.bad_v1_name_chars.sub(u'', theme_name)
        theme_folder = os.path.join(dir, theme_name)
        theme_exists = os.path.exists(theme_folder)
        if theme_exists and not self.overWriteMessageBox(theme_name):
            return '', '', '', True
        themedir = os.path.join(dir, theme_name)
        check_directory_exists(themedir)
        file_xml = unicode(zip.read(xml_file), u'utf-8')
        file_xml = self._migrateVersion122(file_xml)
        out_file = open(os.path.join(themedir, theme_name + u'.xml'), u'w')
        out_file.write(file_xml.encode(u'utf-8'))
        out_file.close()
        if background.text.strip() == u'2':
            image_name = xml_tree.find(u'BackgroundParameter1').text.strip()
            # image file has same extension and is in subfolder
            imagefile = filter(lambda name: os.path.splitext(name)[1].lower()
                == os.path.splitext(image_name)[1].lower() and name.find(r'/'),
                zip.namelist())
            if len(imagefile) >= 1:
                out_file = open(os.path.join(themedir, image_name), u'wb')
                out_file.write(zip.read(imagefile[0]))
                out_file.close()
            else:
                log.exception(u'Theme file does not contain image file "%s"' %
                    image_name.decode(u'utf-8', u'replace'))
                raise Exception(u'validation')
        return theme_name, file_xml, out_file, False

    def checkIfThemeExists(self, theme_name):
        """
        Check if theme already exists and displays error message

        ``theme_name``
            Name of the Theme to test
        """
        theme_dir = os.path.join(self.path, theme_name)
        if os.path.exists(theme_dir):
            critical_error_message_box(
                translate('OpenLP.ThemeManager', 'Validation Error'),
                translate('OpenLP.ThemeManager',
                'A theme with this name already exists.'))
            return False
        return True

    def saveTheme(self, theme, image_from, image_to):
        """
        Called by thememaintenance Dialog to save the theme
        and to trigger the reload of the theme list
        """
        self._writeTheme(theme, image_from, image_to)
        if theme.background_type == \
            BackgroundType.to_string(BackgroundType.Image):
            self.mainwindow.imageManager.update_image(theme.theme_name,
                u'theme', QtGui.QColor(theme.background_border_color))
            self.mainwindow.imageManager.process_updates()
        self.loadThemes()

    def _writeTheme(self, theme, image_from, image_to):
        """
        Writes the theme to the disk and handles the background image if
        necessary
        """
        name = theme.theme_name
        theme_pretty_xml = theme.extract_formatted_xml()
        log.debug(u'saveTheme %s %s', name, theme_pretty_xml.decode(u'utf-8'))
        theme_dir = os.path.join(self.path, name)
        check_directory_exists(theme_dir)
        theme_file = os.path.join(theme_dir, name + u'.xml')
        if self.old_background_image and \
            image_to != self.old_background_image:
            delete_file(self.old_background_image)
        out_file = None
        try:
            out_file = open(theme_file, u'w')
            out_file.write(theme_pretty_xml)
        except IOError:
            log.exception(u'Saving theme to file failed')
        finally:
            if out_file:
                out_file.close()
        if image_from and image_from != image_to:
            try:
                encoding = get_filesystem_encoding()
                shutil.copyfile(
                    unicode(image_from).encode(encoding),
                    unicode(image_to).encode(encoding))
            except IOError:
                log.exception(u'Failed to save theme image')
        self.generateAndSaveImage(self.path, name, theme)

    def generateAndSaveImage(self, dir, name, theme):
        log.debug(u'generateAndSaveImage %s %s', dir, name)
        frame = self.generateImage(theme)
        sample_path_name = os.path.join(self.path, name + u'.png')
        if os.path.exists(sample_path_name):
            os.unlink(sample_path_name)
        frame.save(sample_path_name, u'png')
        thumb = os.path.join(self.thumb_path, u'%s.png' % name)
        create_thumb(sample_path_name, thumb, False)
        log.debug(u'Theme image written to %s', sample_path_name)

    def updatePreviewImages(self):
        """
        Called to update the themes' preview images.
        """
        self.mainwindow.displayProgressBar(len(self.theme_list))
        for theme in self.theme_list:
            self.mainwindow.incrementProgressBar()
            self.generateAndSaveImage(
                self.path, theme, self.getThemeData(theme))
        self.mainwindow.finishedProgressBar()
        self.loadThemes()

    def generateImage(self, theme_data, forcePage=False):
        """
        Call the renderer to build a Sample Image

        ``theme_data``
            The theme to generated a preview for.

        ``forcePage``
            Flag to tell message lines per page need to be generated.
        """
        log.debug(u'generateImage \n%s ', theme_data)
        return self.mainwindow.renderer.generate_preview(
            theme_data, forcePage)

    def getPreviewImage(self, theme):
        """
        Return an image representing the look of the theme

        ``theme``
            The theme to return the image for
        """
        log.debug(u'getPreviewImage %s ', theme)
        image = os.path.join(self.path, theme + u'.png')
        return image

    def _createThemeFromXml(self, theme_xml, path):
        """
        Return a theme object using information parsed from XML

        ``theme_xml``
            The XML data to load into the theme
        """
        theme = ThemeXML()
        theme.parse(theme_xml)
        theme.extend_image_filename(path)
        return theme

    def _validate_theme_action(self, select_text, confirm_title, confirm_text,
        testPlugin=True, confirm=True):
        """
        Check to see if theme has been selected and the destructive action
        is allowed.
        """
        self.global_theme = unicode(QtCore.QSettings().value(
            self.settingsSection + u'/global theme',
            QtCore.QVariant(u'')).toString())
        if check_item_selected(self.themeListWidget, select_text):
            item = self.themeListWidget.currentItem()
            theme = unicode(item.text())
            # confirm deletion
            if confirm:
                answer = QtGui.QMessageBox.question(self, confirm_title,
                    confirm_text % theme, QtGui.QMessageBox.StandardButtons(
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
                    QtGui.QMessageBox.No)
                if answer == QtGui.QMessageBox.No:
                    return False
            # should be the same unless default
            if theme != unicode(item.data(QtCore.Qt.UserRole).toString()):
                critical_error_message_box(
                    message=translate('OpenLP.ThemeManager',
                    'You are unable to delete the default theme.'))
                return False
            # check for use in the system else where.
            if testPlugin:
                for plugin in self.mainwindow.pluginManager.plugins:
                    if plugin.usesTheme(theme):
                        critical_error_message_box(
                            translate('OpenLP.ThemeManager',
                            'Validation Error'),
                            unicode(translate('OpenLP.ThemeManager',
                            'Theme %s is used in the %s plugin.')) % \
                            (theme, plugin.name))
                        return False
            return True
        return False

    def _migrateVersion122(self, xml_data):
        """
        Convert the xml data from version 1 format to the current format.

        New fields are loaded with defaults to provide a complete, working
        theme containing all compatible customisations from the old theme.

        ``xml_data``
            Version 1 theme to convert
        """
        theme = Theme(xml_data)
        new_theme = ThemeXML()
        new_theme.theme_name = self.bad_v1_name_chars.sub(u'', theme.Name)
        if theme.BackgroundType == 0:
            new_theme.background_type = \
                BackgroundType.to_string(BackgroundType.Solid)
            new_theme.background_color = \
                unicode(theme.BackgroundParameter1.name())
        elif theme.BackgroundType == 1:
            new_theme.background_type = \
                BackgroundType.to_string(BackgroundType.Gradient)
            new_theme.background_direction = \
                BackgroundGradientType. \
                to_string(BackgroundGradientType.Horizontal)
            if theme.BackgroundParameter3.name() == 1:
                new_theme.background_direction = \
                    BackgroundGradientType. \
                    to_string(BackgroundGradientType.Horizontal)
            new_theme.background_start_color = \
                unicode(theme.BackgroundParameter1.name())
            new_theme.background_end_color = \
                unicode(theme.BackgroundParameter2.name())
        elif theme.BackgroundType == 2:
            new_theme.background_type = \
                BackgroundType.to_string(BackgroundType.Image)
            new_theme.background_filename = unicode(theme.BackgroundParameter1)
        elif theme.BackgroundType == 3:
            new_theme.background_type = \
                BackgroundType.to_string(BackgroundType.Transparent)
        new_theme.font_main_name = theme.FontName
        new_theme.font_main_color = unicode(theme.FontColor.name())
        new_theme.font_main_size = theme.FontProportion * 3
        new_theme.font_footer_name = theme.FontName
        new_theme.font_footer_color = unicode(theme.FontColor.name())
        new_theme.font_main_shadow = False
        if theme.Shadow == 1:
            new_theme.font_main_shadow = True
            new_theme.font_main_shadow_color = unicode(theme.ShadowColor.name())
        if theme.Outline == 1:
            new_theme.font_main_outline = True
            new_theme.font_main_outline_color = \
                unicode(theme.OutlineColor.name())
        vAlignCorrection = VerticalType.Top
        if theme.VerticalAlign == 2:
            vAlignCorrection = VerticalType.Middle
        elif theme.VerticalAlign == 1:
            vAlignCorrection = VerticalType.Bottom
        new_theme.display_horizontal_align = theme.HorizontalAlign
        new_theme.display_vertical_align = vAlignCorrection
        return new_theme.extract_xml()

