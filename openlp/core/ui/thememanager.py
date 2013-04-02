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
"""
The Theme Manager manages adding, deleteing and modifying of themes.
"""
import os
import zipfile
import shutil
import logging
import re

from xml.etree.ElementTree import ElementTree, XML
from PyQt4 import QtCore, QtGui

from openlp.core.lib import ImageSource, OpenLPToolbar, Receiver, Registry, SettingsManager, Settings, UiStrings, \
    get_text_file_string, build_icon, translate, check_item_selected, check_directory_exists, create_thumb, \
    validate_thumb
from openlp.core.lib.theme import ThemeXML, BackgroundType, VerticalType, BackgroundGradientType
from openlp.core.lib.ui import critical_error_message_box, create_widget_action
from openlp.core.theme import Theme
from openlp.core.ui import FileRenameForm, ThemeForm
from openlp.core.utils import AppLocation, delete_file, locale_compare, get_filesystem_encoding

log = logging.getLogger(__name__)


class ThemeManager(QtGui.QWidget):
    """
    Manages the orders of Theme.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        QtGui.QWidget.__init__(self, parent)
        Registry().register(u'theme_manager', self)
        self.settingsSection = u'themes'
        self.themeForm = ThemeForm(self)
        self.fileRenameForm = FileRenameForm(self)
        # start with the layout
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.layout.setObjectName(u'layout')
        self.toolbar = OpenLPToolbar(self)
        self.toolbar.setObjectName(u'toolbar')
        self.toolbar.addToolbarAction(u'newTheme',
            text=UiStrings().NewTheme, icon=u':/themes/theme_new.png',
            tooltip=translate('OpenLP.ThemeManager', 'Create a new theme.'),
            triggers=self.onAddTheme)
        self.toolbar.addToolbarAction(u'editTheme',
            text=translate('OpenLP.ThemeManager', 'Edit Theme'),
            icon=u':/themes/theme_edit.png',
            tooltip=translate('OpenLP.ThemeManager', 'Edit a theme.'),
            triggers=self.on_edit_theme)
        self.deleteToolbarAction = self.toolbar.addToolbarAction(u'delete_theme',
            text=translate('OpenLP.ThemeManager', 'Delete Theme'),
            icon=u':/general/general_delete.png',
            tooltip=translate('OpenLP.ThemeManager', 'Delete a theme.'),
            triggers=self.on_delete_theme)
        self.toolbar.addSeparator()
        self.toolbar.addToolbarAction(u'importTheme',
            text=translate('OpenLP.ThemeManager', 'Import Theme'),
            icon=u':/general/general_import.png',
            tooltip=translate('OpenLP.ThemeManager', 'Import a theme.'),
            triggers=self.on_import_theme)
        self.toolbar.addToolbarAction(u'exportTheme',
            text=translate('OpenLP.ThemeManager', 'Export Theme'),
            icon=u':/general/general_export.png',
            tooltip=translate('OpenLP.ThemeManager', 'Export a theme.'),
            triggers=self.on_export_theme)
        self.layout.addWidget(self.toolbar)
        self.theme_widget = QtGui.QWidgetAction(self.toolbar)
        self.theme_widget.setObjectName(u'theme_widget')
        # create theme manager list
        self.theme_list_widget = QtGui.QListWidget(self)
        self.theme_list_widget.setAlternatingRowColors(True)
        self.theme_list_widget.setIconSize(QtCore.QSize(88, 50))
        self.theme_list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.theme_list_widget.setObjectName(u'theme_list_widget')
        self.layout.addWidget(self.theme_list_widget)
        QtCore.QObject.connect(self.theme_list_widget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'),
            self.context_menu)
        # build the context menu
        self.menu = QtGui.QMenu()
        self.edit_action = create_widget_action(self.menu,
            text=translate('OpenLP.ThemeManager', '&Edit Theme'),
            icon=u':/themes/theme_edit.png', triggers=self.on_edit_theme)
        self.copy_action = create_widget_action(self.menu,
            text=translate('OpenLP.ThemeManager', '&Copy Theme'),
            icon=u':/themes/theme_edit.png', triggers=self.on_copy_theme)
        self.rename_action = create_widget_action(self.menu,
            text=translate('OpenLP.ThemeManager', '&Rename Theme'),
            icon=u':/themes/theme_edit.png', triggers=self.on_rename_theme)
        self.delete_action = create_widget_action(self.menu,
            text=translate('OpenLP.ThemeManager', '&Delete Theme'),
            icon=u':/general/general_delete.png', triggers=self.on_delete_theme)
        self.menu.addSeparator()
        self.global_action = create_widget_action(self.menu,
            text=translate('OpenLP.ThemeManager', 'Set As &Global Default'),
            icon=u':/general/general_export.png',
            triggers=self.changeGlobalFromScreen)
        self.exportAction = create_widget_action(self.menu,
            text=translate('OpenLP.ThemeManager', '&Export Theme'),
            icon=u':/general/general_export.png', triggers=self.on_export_theme)
        # Signals
        QtCore.QObject.connect(self.theme_list_widget,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'), self.changeGlobalFromScreen)
        QtCore.QObject.connect(self.theme_list_widget,
            QtCore.SIGNAL(u'currentItemChanged(QListWidgetItem *, QListWidgetItem *)'), self.check_list_state)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_global'), self.change_global_from_tab)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'config_updated'), self.config_updated)
        # Variables
        self.theme_list = []
        self.path = AppLocation.get_section_data_path(self.settingsSection)
        check_directory_exists(self.path)
        self.thumbPath = os.path.join(self.path, u'thumbnails')
        check_directory_exists(self.thumbPath)
        self.themeForm.path = self.path
        self.oldBackgroundImage = None
        self.badV1NameChars = re.compile(r'[%+\[\]]')
        # Last little bits of setting up
        self.config_updated()

    def first_time(self):
        """
        Import new themes downloaded by the first time wizard
        """
        self.application.set_busy_cursor()
        files = SettingsManager.get_files(self.settingsSection, u'.otz')
        for theme_file in files:
            theme_file = os.path.join(self.path, theme_file)
            self.unzipTheme(theme_file, self.path)
            delete_file(theme_file)
        self.application.set_normal_cursor()


    def config_updated(self):
        """
        Triggered when Config dialog is updated.
        """
        self.global_theme = Settings().value(self.settingsSection + u'/global theme')

    def check_list_state(self, item):
        """
        If Default theme selected remove delete button.
        """
        if item is None:
            return
        real_theme_name = item.data(QtCore.Qt.UserRole)
        theme_name = item.text()
        # If default theme restrict actions
        if real_theme_name == theme_name:
            self.deleteToolbarAction.setVisible(True)
        else:
            self.deleteToolbarAction.setVisible(False)

    def context_menu(self, point):
        """
        Build the Right Click Context menu and set state depending on
        the type of theme.
        """
        item = self.theme_list_widget.itemAt(point)
        if item is None:
            return
        real_theme_name = item.data(QtCore.Qt.UserRole)
        theme_name = unicode(item.text())
        visible = real_theme_name == theme_name
        self.delete_action.setVisible(visible)
        self.rename_action.setVisible(visible)
        self.global_action.setVisible(visible)
        self.menu.exec_(self.theme_list_widget.mapToGlobal(point))

    def change_global_from_tab(self, theme_name):
        """
        Change the global theme when it is changed through the Themes settings
        tab
        """
        log.debug(u'change_global_from_tab %s', theme_name)
        for count in range(0, self.theme_list_widget.count()):
            # reset the old name
            item = self.theme_list_widget.item(count)
            old_name = item.text()
            new_name = item.data(QtCore.Qt.UserRole)
            if old_name != new_name:
                self.theme_list_widget.item(count).setText(new_name)
            # Set the new name
            if theme_name == new_name:
                name = translate('OpenLP.ThemeManager', '%s (default)') % new_name
                self.theme_list_widget.item(count).setText(name)
                self.deleteToolbarAction.setVisible(
                    item not in self.theme_list_widget.selectedItems())

    def changeGlobalFromScreen(self, index=-1):
        """
        Change the global theme when a theme is double clicked upon in the
        Theme Manager list
        """
        log.debug(u'changeGlobalFromScreen %s', index)
        selected_row = self.theme_list_widget.currentRow()
        for count in range(0, self.theme_list_widget.count()):
            item = self.theme_list_widget.item(count)
            old_name = item.text()
            # reset the old name
            if old_name != item.data(QtCore.Qt.UserRole):
                self.theme_list_widget.item(count).setText(item.data(QtCore.Qt.UserRole))
            # Set the new name
            if count == selected_row:
                self.global_theme = self.theme_list_widget.item(count).text()
                name = translate('OpenLP.ThemeManager', '%s (default)') % self.global_theme
                self.theme_list_widget.item(count).setText(name)
                Settings().setValue(self.settingsSection + u'/global theme', self.global_theme)
                Receiver.send_message(u'theme_update_global', self.global_theme)
                self._push_themes()

    def onAddTheme(self):
        """
        Loads a new theme with the default settings and then launches the theme
        editing form for the user to make their customisations.
        """
        theme = ThemeXML()
        theme.set_default_header_footer()
        self.themeForm.theme = theme
        self.themeForm.exec_()
        self.load_themes()

    def on_rename_theme(self):
        """
        Renames an existing theme to a new name
        """
        if self._validate_theme_action(translate('OpenLP.ThemeManager', 'You must select a theme to rename.'),
                translate('OpenLP.ThemeManager', 'Rename Confirmation'),
                translate('OpenLP.ThemeManager', 'Rename %s theme?'), False, False):
            item = self.theme_list_widget.currentItem()
            old_theme_name = item.data(QtCore.Qt.UserRole)
            self.fileRenameForm.fileNameEdit.setText(old_theme_name)
            if self.fileRenameForm.exec_():
                new_theme_name = self.fileRenameForm.fileNameEdit.text()
                if old_theme_name == new_theme_name:
                    return
                if self.check_if_theme_exists(new_theme_name):
                    old_theme_data = self.get_theme_data(old_theme_name)
                    self.cloneThemeData(old_theme_data, new_theme_name)
                    self.delete_theme(old_theme_name)
                    for plugin in self.plugin_manager.plugins:
                        if plugin.usesTheme(old_theme_name):
                            plugin.renameTheme(old_theme_name, new_theme_name)
                    self.renderer.update_theme(new_theme_name, old_theme_name)
                    self.load_themes()

    def on_copy_theme(self):
        """
        Copies an existing theme to a new name
        """
        item = self.theme_list_widget.currentItem()
        old_theme_name = item.data(QtCore.Qt.UserRole)
        self.fileRenameForm.fileNameEdit.setText(translate('OpenLP.ThemeManager',
            'Copy of %s', 'Copy of <theme name>') % old_theme_name)
        if self.fileRenameForm.exec_(True):
            new_theme_name = self.fileRenameForm.fileNameEdit.text()
            if self.check_if_theme_exists(new_theme_name):
                theme_data = self.get_theme_data(old_theme_name)
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
        self.save_theme(theme_data, save_from, save_to)
        self.load_themes()

    def on_edit_theme(self):
        """
        Loads the settings for the theme that is to be edited and launches the
        theme editing form so the user can make their changes.
        """
        if check_item_selected(self.theme_list_widget,
                translate('OpenLP.ThemeManager', 'You must select a theme to edit.')):
            item = self.theme_list_widget.currentItem()
            theme = self.get_theme_data(item.data(QtCore.Qt.UserRole))
            if theme.background_type == u'image':
                self.oldBackgroundImage = theme.background_filename
            self.themeForm.theme = theme
            self.themeForm.exec_(True)
            self.oldBackgroundImage = None
            self.renderer.update_theme(theme.theme_name)
            self.load_themes()

    def on_delete_theme(self):
        """
        Delete a theme
        """
        if self._validate_theme_action(translate('OpenLP.ThemeManager', 'You must select a theme to delete.'),
                translate('OpenLP.ThemeManager', 'Delete Confirmation'),
                translate('OpenLP.ThemeManager', 'Delete %s theme?')):
            item = self.theme_list_widget.currentItem()
            theme = item.text()
            row = self.theme_list_widget.row(item)
            self.theme_list_widget.takeItem(row)
            self.delete_theme(theme)
            self.renderer.update_theme(theme, only_delete=True)
            # As we do not reload the themes, push out the change. Reload the
            # list as the internal lists and events need to be triggered.
            self._push_themes()

    def delete_theme(self, theme):
        """
        Delete a theme.

        ``theme``
            The theme to delete.
        """
        self.theme_list.remove(theme)
        thumb = u'%s.png' % theme
        delete_file(os.path.join(self.path, thumb))
        delete_file(os.path.join(self.thumbPath, thumb))
        try:
            encoding = get_filesystem_encoding()
            shutil.rmtree(os.path.join(self.path, theme).encode(encoding))
        except OSError, shutil.Error:
            log.exception(u'Error deleting theme %s', theme)

    def on_export_theme(self):
        """
        Export the theme in a zip file
        """
        item = self.theme_list_widget.currentItem()
        if item is None:
            critical_error_message_box(message=translate('OpenLP.ThemeManager', 'You have not selected a theme.'))
            return
        theme = item.data(QtCore.Qt.UserRole)
        path = QtGui.QFileDialog.getExistingDirectory(self,
            translate('OpenLP.ThemeManager', 'Save Theme - (%s)') % theme,
            Settings().value(self.settingsSection + u'/last directory export'))
        self.application.set_busy_cursor()
        if path:
            Settings().setValue(self.settingsSection + u'/last directory export', path)
            theme_path = os.path.join(path, theme + u'.otz')
            theme_zip = None
            try:
                theme_zip = zipfile.ZipFile(theme_path, u'w')
                source = os.path.join(self.path, theme)
                for files in os.walk(source):
                    for name in files[2]:
                        theme_zip.write(
                            os.path.join(source, name).encode(u'utf-8'),
                            os.path.join(theme, name).encode(u'utf-8')
                        )
                QtGui.QMessageBox.information(self,
                    translate('OpenLP.ThemeManager', 'Theme Exported'),
                    translate('OpenLP.ThemeManager', 'Your theme has been successfully exported.'))
            except (IOError, OSError):
                log.exception(u'Export Theme Failed')
                critical_error_message_box(translate('OpenLP.ThemeManager', 'Theme Export Failed'),
                    translate('OpenLP.ThemeManager', 'Your theme could not be exported due to an error.'))
            finally:
                if theme_zip:
                    theme_zip.close()
        self.application.set_normal_cursor()


    def on_import_theme(self):
        """
        Opens a file dialog to select the theme file(s) to import before
        attempting to extract OpenLP themes from those files. This process
        will load both OpenLP version 1 and version 2 themes.
        """
        files = QtGui.QFileDialog.getOpenFileNames(self,
            translate('OpenLP.ThemeManager', 'Select Theme Import File'),
            Settings().value(self.settingsSection + u'/last directory import'),
            translate('OpenLP.ThemeManager', 'OpenLP Themes (*.theme *.otz)'))
        log.info(u'New Themes %s', unicode(files))
        if not files:
            return
        self.application.set_busy_cursor()
        for file_name in files:
            Settings().setValue(self.settingsSection + u'/last directory import', unicode(file_name))
            self.unzip_theme(file_name, self.path)
        self.load_themes()
        self.application.set_normal_cursor()

    def load_themes(self, first_time=False):
        """
        Loads the theme lists and triggers updates accross the whole system
        using direct calls or core functions and events for the plugins.
        The plugins will call back in to get the real list if they want it.
        """
        log.debug(u'Load themes from dir')
        self.theme_list = []
        self.theme_list_widget.clear()
        files = SettingsManager.get_files(self.settingsSection, u'.png')
        if first_time:
            self.first_time()
            files = SettingsManager.get_files(self.settingsSection, u'.png')
            # No themes have been found so create one
            if not files:
                theme = ThemeXML()
                theme.theme_name = UiStrings().Default
                self._write_theme(theme, None, None)
                Settings().setValue(self.settingsSection + u'/global theme', theme.theme_name)
                self.config_updated()
                files = SettingsManager.get_files(self.settingsSection, u'.png')
        # Sort the themes by its name considering language specific
        files.sort(key=lambda file_name: unicode(file_name), cmp=locale_compare)
        # now process the file list of png files
        for name in files:
            # check to see file is in theme root directory
            theme = os.path.join(self.path, name)
            if os.path.exists(theme):
                text_name = os.path.splitext(name)[0]
                if text_name == self.global_theme:
                    name = translate('OpenLP.ThemeManager', '%s (default)') % text_name
                else:
                    name = text_name
                thumb = os.path.join(self.thumbPath, u'%s.png' % text_name)
                item_name = QtGui.QListWidgetItem(name)
                if validate_thumb(theme, thumb):
                    icon = build_icon(thumb)
                else:
                    icon = create_thumb(theme, thumb)
                item_name.setIcon(icon)
                item_name.setData(QtCore.Qt.UserRole, text_name)
                self.theme_list_widget.addItem(item_name)
                self.theme_list.append(text_name)
        self._push_themes()

    def _push_themes(self):
        """
        Notify listeners that the theme list has been updated
        """
        Receiver.send_message(u'theme_update_list', self.get_themes())

    def get_themes(self):
        """
        Return the list of loaded themes
        """
        return self.theme_list

    def get_theme_data(self, theme_name):
        """
        Returns a theme object from an XML file

        ``theme_name``
            Name of the theme to load from file
        """
        log.debug(u'getthemedata for theme %s', theme_name)
        xml_file = os.path.join(self.path, unicode(theme_name), unicode(theme_name) + u'.xml')
        xml = get_text_file_string(xml_file)
        if not xml:
            log.debug(u'No theme data - using default theme')
            return ThemeXML()
        else:
            return self._create_theme_fom_Xml(xml, self.path)

    def over_write_message_box(self, theme_name):
        """
        Display a warning box to the user that a theme already exists
        """
        ret = QtGui.QMessageBox.question(self, translate('OpenLP.ThemeManager', 'Theme Already Exists'),
            translate('OpenLP.ThemeManager',
                'Theme %s already exists. Do you want to replace it?').replace('%s', theme_name),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
            QtGui.QMessageBox.No)
        return ret == QtGui.QMessageBox.Yes

    def unzip_theme(self, file_name, directory):
        """
        Unzip the theme, remove the preview file if stored
        Generate a new preview file. Check the XML theme version and upgrade if
        necessary.
        """
        log.debug(u'Unzipping theme %s', file_name)
        file_name = unicode(file_name)
        theme_zip = None
        out_file = None
        file_xml = None
        abort_import = True
        try:
            theme_zip = zipfile.ZipFile(file_name)
            xml_file = filter(lambda name: os.path.splitext(name)[1].lower() == u'.xml', theme_zip.namelist())
            if len(xml_file) != 1:
                log.exception(u'Theme contains "%s" XML files' % len(xml_file))
                raise Exception('validation')
            xml_tree = ElementTree(element=XML(theme_zip.read(xml_file[0]))).getroot()
            v1_background = xml_tree.find(u'BackgroundType')
            if v1_background is not None:
                theme_name, file_xml, out_file, abort_import = self.unzip_version_122(
                    directory, theme_zip, xml_file[0], xml_tree, v1_background, out_file)
            else:
                theme_name = xml_tree.find(u'name').text.strip()
                theme_folder = os.path.join(directory, theme_name)
                theme_exists = os.path.exists(theme_folder)
                if theme_exists and not self.over_write_message_box(theme_name):
                    abort_import = True
                    return
                else:
                    abort_import = False
                for name in theme_zip.namelist():
                    try:
                        uname = unicode(name, u'utf-8')
                    except UnicodeDecodeError:
                        log.exception(u'Theme file contains non utf-8 filename "%s"' %
                            name.decode(u'utf-8', u'replace'))
                        raise Exception(u'validation')
                    uname = uname.replace(u'/', os.path.sep)
                    split_name = uname.split(os.path.sep)
                    if split_name[-1] == u'' or len(split_name) == 1:
                        # is directory or preview file
                        continue
                    full_name = os.path.join(directory, uname)
                    check_directory_exists(os.path.dirname(full_name))
                    if os.path.splitext(uname)[1].lower() == u'.xml':
                        file_xml = unicode(theme_zip.read(name), u'utf-8')
                        out_file = open(full_name, u'w')
                        out_file.write(file_xml.encode(u'utf-8'))
                    else:
                        out_file = open(full_name, u'wb')
                        out_file.write(theme_zip.read(name))
                    out_file.close()
        except (IOError, zipfile.BadZipfile):
            log.exception(u'Importing theme from zip failed %s' % file_name)
            raise Exception(u'validation')
        except Exception as info:
            if unicode(info) == u'validation':
                critical_error_message_box(translate('OpenLP.ThemeManager',
                    'Validation Error'), translate('OpenLP.ThemeManager', 'File is not a valid theme.'))
            else:
                raise
        finally:
            # Close the files, to be able to continue creating the theme.
            if theme_zip:
                theme_zip.close()
            if out_file:
                out_file.close()
            if not abort_import:
                # As all files are closed, we can create the Theme.
                if file_xml:
                    theme = self._create_theme_fom_Xml(file_xml, self.path)
                    self.generate_and_save_image(directory, theme_name, theme)
                # Only show the error message, when IOError was not raised (in
                # this case the error message has already been shown).
                elif theme_zip is not None:
                    critical_error_message_box(
                        translate('OpenLP.ThemeManager', 'Validation Error'),
                        translate('OpenLP.ThemeManager', 'File is not a valid theme.'))
                    log.exception(u'Theme file does not contain XML data %s' % file_name)

    def unzip_version_122(self, dir_name, zip_file, xml_file, xml_tree, background, out_file):
        """
        Unzip openlp.org 1.2x theme file and upgrade the theme xml. When calling
        this method, please keep in mind, that some parameters are redundant.
        """
        theme_name = xml_tree.find(u'Name').text.strip()
        theme_name = self.badV1NameChars.sub(u'', theme_name)
        theme_folder = os.path.join(dir_name, theme_name)
        theme_exists = os.path.exists(theme_folder)
        if theme_exists and not self.over_write_message_box(theme_name):
            return '', '', '', True
        themedir = os.path.join(dir_name, theme_name)
        check_directory_exists(themedir)
        file_xml = unicode(zip_file.read(xml_file), u'utf-8')
        file_xml = self._migrate_version_122(file_xml)
        out_file = open(os.path.join(themedir, theme_name + u'.xml'), u'w')
        out_file.write(file_xml.encode(u'utf-8'))
        out_file.close()
        if background.text.strip() == u'2':
            image_name = xml_tree.find(u'BackgroundParameter1').text.strip()
            # image file has same extension and is in subfolder
            image_file = filter(lambda name: os.path.splitext(name)[1].lower()
                == os.path.splitext(image_name)[1].lower() and name.find(r'/'), zip_file.namelist())
            if len(image_file) >= 1:
                out_file = open(os.path.join(themedir, image_name), u'wb')
                out_file.write(zip_file.read(image_file[0]))
                out_file.close()
            else:
                log.exception(u'Theme file does not contain image file "%s"' % image_name.decode(u'utf-8', u'replace'))
                raise Exception(u'validation')
        return theme_name, file_xml, out_file, False

    def check_if_theme_exists(self, theme_name):
        """
        Check if theme already exists and displays error message

        ``theme_name``
            Name of the Theme to test
        """
        theme_dir = os.path.join(self.path, theme_name)
        if os.path.exists(theme_dir):
            critical_error_message_box(
                translate('OpenLP.ThemeManager', 'Validation Error'),
                translate('OpenLP.ThemeManager', 'A theme with this name already exists.'))
            return False
        return True

    def save_theme(self, theme, image_from, image_to):
        """
        Called by thememaintenance Dialog to save the theme
        and to trigger the reload of the theme list
        """
        self._write_theme(theme, image_from, image_to)
        if theme.background_type == BackgroundType.to_string(BackgroundType.Image):
            self.image_manager.update_image_border(theme.background_filename,
                ImageSource.Theme, QtGui.QColor(theme.background_border_color))
            self.image_manager.process_updates()

    def _write_theme(self, theme, image_from, image_to):
        """
        Writes the theme to the disk and handles the background image if
        necessary
        """
        name = theme.theme_name
        theme_pretty_xml = theme.extract_formatted_xml()
        log.debug(u'save_theme %s %s', name, theme_pretty_xml.decode(u'utf-8'))
        theme_dir = os.path.join(self.path, name)
        check_directory_exists(theme_dir)
        theme_file = os.path.join(theme_dir, name + u'.xml')
        if self.oldBackgroundImage and image_to != self.oldBackgroundImage:
            delete_file(self.oldBackgroundImage)
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
                shutil.copyfile(unicode(image_from).encode(encoding), unicode(image_to).encode(encoding))
            except IOError, shutil.Error:
                log.exception(u'Failed to save theme image')
        self.generate_and_save_image(self.path, name, theme)

    def generate_and_save_image(self, directory, name, theme):
        """
        Generate and save a preview image
        """
        log.debug(u'generate_and_save_image %s %s', directory, name)
        frame = self.generate_image(theme)
        sample_path_name = os.path.join(self.path, name + u'.png')
        if os.path.exists(sample_path_name):
            os.unlink(sample_path_name)
        frame.save(sample_path_name, u'png')
        thumb = os.path.join(self.thumbPath, u'%s.png' % name)
        create_thumb(sample_path_name, thumb, False)
        log.debug(u'Theme image written to %s', sample_path_name)

    def update_preview_images(self):
        """
        Called to update the themes' preview images.
        """
        self.main_window.displayProgressBar(len(self.theme_list))
        for theme in self.theme_list:
            self.main_window.incrementProgressBar()
            self.generate_and_save_image(self.path, theme, self.get_theme_data(theme))
        self.main_window.finishedProgressBar()
        self.load_themes()

    def generate_image(self, theme_data, forcePage=False):
        """
        Call the renderer to build a Sample Image

        ``theme_data``
            The theme to generated a preview for.

        ``forcePage``
            Flag to tell message lines per page need to be generated.
        """
        log.debug(u'generate_image \n%s ', theme_data)
        return self.renderer.generate_preview(theme_data, forcePage)

    def get_preview_image(self, theme):
        """
        Return an image representing the look of the theme

        ``theme``
            The theme to return the image for
        """
        log.debug(u'get_preview_image %s ', theme)
        image = os.path.join(self.path, theme + u'.png')
        return image

    def _create_theme_fom_Xml(self, theme_xml, path):
        """
        Return a theme object using information parsed from XML

        ``theme_xml``
            The XML data to load into the theme
        """
        theme = ThemeXML()
        theme.parse(theme_xml)
        theme.extend_image_filename(path)
        return theme

    def _validate_theme_action(self, select_text, confirm_title, confirm_text, testPlugin=True, confirm=True):
        """
        Check to see if theme has been selected and the destructive action
        is allowed.
        """
        self.global_theme = Settings().value(self.settingsSection + u'/global theme')
        if check_item_selected(self.theme_list_widget, select_text):
            item = self.theme_list_widget.currentItem()
            theme = item.text()
            # confirm deletion
            if confirm:
                answer = QtGui.QMessageBox.question(self, confirm_title, confirm_text % theme,
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
                    QtGui.QMessageBox.No)
                if answer == QtGui.QMessageBox.No:
                    return False
            # should be the same unless default
            if theme != item.data(QtCore.Qt.UserRole):
                critical_error_message_box(
                    message=translate('OpenLP.ThemeManager', 'You are unable to delete the default theme.'))
                return False
            # check for use in the system else where.
            if testPlugin:
                for plugin in self.plugin_manager.plugins:
                    if plugin.usesTheme(theme):
                        critical_error_message_box(translate('OpenLP.ThemeManager', 'Validation Error'),
                            translate('OpenLP.ThemeManager', 'Theme %s is used in the %s plugin.') %
                                (theme, plugin.name))
                        return False
            return True
        return False

    def _migrate_version_122(self, xml_data):
        """
        Convert the xml data from version 1 format to the current format.

        New fields are loaded with defaults to provide a complete, working
        theme containing all compatible customisations from the old theme.

        ``xml_data``
            Version 1 theme to convert
        """
        theme = Theme(xml_data)
        new_theme = ThemeXML()
        new_theme.theme_name = self.badV1NameChars.sub(u'', theme.Name)
        if theme.BackgroundType == 0:
            new_theme.background_type = BackgroundType.to_string(BackgroundType.Solid)
            new_theme.background_color = unicode(theme.BackgroundParameter1.name())
        elif theme.BackgroundType == 1:
            new_theme.background_type = BackgroundType.to_string(BackgroundType.Gradient)
            new_theme.background_direction = BackgroundGradientType.to_string(BackgroundGradientType.Horizontal)
            if theme.BackgroundParameter3.name() == 1:
                new_theme.background_direction = BackgroundGradientType.to_string(BackgroundGradientType.Horizontal)
            new_theme.background_start_color = unicode(theme.BackgroundParameter1.name())
            new_theme.background_end_color = unicode(theme.BackgroundParameter2.name())
        elif theme.BackgroundType == 2:
            new_theme.background_type = BackgroundType.to_string(BackgroundType.Image)
            new_theme.background_filename = unicode(theme.BackgroundParameter1)
        elif theme.BackgroundType == 3:
            new_theme.background_type = BackgroundType.to_string(BackgroundType.Transparent)
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
            new_theme.font_main_outline_color = unicode(theme.OutlineColor.name())
        vAlignCorrection = VerticalType.Top
        if theme.VerticalAlign == 2:
            vAlignCorrection = VerticalType.Middle
        elif theme.VerticalAlign == 1:
            vAlignCorrection = VerticalType.Bottom
        new_theme.display_horizontal_align = theme.HorizontalAlign
        new_theme.display_vertical_align = vAlignCorrection
        return new_theme.extract_xml()

    def _get_renderer(self):
        """
        Adds the Renderer to the class dynamically
        """
        if not hasattr(self, u'_renderer'):
            self._renderer = Registry().get(u'renderer')
        return self._renderer

    renderer = property(_get_renderer)

    def _get_image_manager(self):
        """
        Adds the image manager to the class dynamically
        """
        if not hasattr(self, u'_image_manager'):
            self._image_manager = Registry().get(u'image_manager')
        return self._image_manager

    image_manager = property(_get_image_manager)

    def _get_plugin_manager(self):
        """
        Adds the Renderer to the class dynamically
        """
        if not hasattr(self, u'_plugin_manager'):
            self._plugin_manager = Registry().get(u'plugin_manager')
        return self._plugin_manager

    plugin_manager = property(_get_plugin_manager)

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, u'_main_window'):
            self._main_window = Registry().get(u'main_window')
        return self._main_window

    main_window = property(_get_main_window)

    def _get_application(self):
        """
        Adds the openlp to the class dynamically
        """
        if not hasattr(self, u'_application'):
            self._application = Registry().get(u'application')
        return self._application

    application = property(_get_application)
