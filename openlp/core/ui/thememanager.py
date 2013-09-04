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

from openlp.core.lib import ImageSource, OpenLPToolbar, Registry, Settings, UiStrings, get_text_file_string, \
    build_icon, translate, check_item_selected, check_directory_exists, create_thumb, validate_thumb
from openlp.core.lib.theme import ThemeXML, BackgroundType, VerticalType, BackgroundGradientType
from openlp.core.lib.ui import critical_error_message_box, create_widget_action
from openlp.core.theme import Theme
from openlp.core.ui import FileRenameForm, ThemeForm
from openlp.core.utils import AppLocation, delete_file, get_locale_key, get_filesystem_encoding

log = logging.getLogger(__name__)


class ThemeManager(QtGui.QWidget):
    """
    Manages the orders of Theme.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        super(ThemeManager, self).__init__(parent)
        Registry().register('theme_manager', self)
        Registry().register_function('bootstrap_initialise', self.load_first_time_themes)
        Registry().register_function('bootstrap_post_set_up', self._push_themes)
        self.settings_section = 'themes'
        self.theme_form = ThemeForm(self)
        self.file_rename_form = FileRenameForm()
        # start with the layout
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.layout.setObjectName('layout')
        self.toolbar = OpenLPToolbar(self)
        self.toolbar.setObjectName('toolbar')
        self.toolbar.add_toolbar_action('newTheme',
            text=UiStrings().NewTheme, icon=':/themes/theme_new.png',
            tooltip=translate('OpenLP.ThemeManager', 'Create a new theme.'),
            triggers=self.on_add_theme)
        self.toolbar.add_toolbar_action('editTheme',
            text=translate('OpenLP.ThemeManager', 'Edit Theme'),
            icon=':/themes/theme_edit.png',
            tooltip=translate('OpenLP.ThemeManager', 'Edit a theme.'),
            triggers=self.on_edit_theme)
        self.delete_toolbar_action = self.toolbar.add_toolbar_action('delete_theme',
            text=translate('OpenLP.ThemeManager', 'Delete Theme'),
            icon=':/general/general_delete.png',
            tooltip=translate('OpenLP.ThemeManager', 'Delete a theme.'),
            triggers=self.on_delete_theme)
        self.toolbar.addSeparator()
        self.toolbar.add_toolbar_action('importTheme',
            text=translate('OpenLP.ThemeManager', 'Import Theme'),
            icon=':/general/general_import.png',
            tooltip=translate('OpenLP.ThemeManager', 'Import a theme.'),
            triggers=self.on_import_theme)
        self.toolbar.add_toolbar_action('exportTheme',
            text=translate('OpenLP.ThemeManager', 'Export Theme'),
            icon=':/general/general_export.png',
            tooltip=translate('OpenLP.ThemeManager', 'Export a theme.'),
            triggers=self.on_export_theme)
        self.layout.addWidget(self.toolbar)
        self.theme_widget = QtGui.QWidgetAction(self.toolbar)
        self.theme_widget.setObjectName('theme_widget')
        # create theme manager list
        self.theme_list_widget = QtGui.QListWidget(self)
        self.theme_list_widget.setAlternatingRowColors(True)
        self.theme_list_widget.setIconSize(QtCore.QSize(88, 50))
        self.theme_list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.theme_list_widget.setObjectName('theme_list_widget')
        self.layout.addWidget(self.theme_list_widget)
        self.theme_list_widget.customContextMenuRequested.connect(self.context_menu)
        # build the context menu
        self.menu = QtGui.QMenu()
        self.edit_action = create_widget_action(self.menu,
            text=translate('OpenLP.ThemeManager', '&Edit Theme'),
            icon=':/themes/theme_edit.png', triggers=self.on_edit_theme)
        self.copy_action = create_widget_action(self.menu,
            text=translate('OpenLP.ThemeManager', '&Copy Theme'),
            icon=':/themes/theme_edit.png', triggers=self.on_copy_theme)
        self.rename_action = create_widget_action(self.menu,
            text=translate('OpenLP.ThemeManager', '&Rename Theme'),
            icon=':/themes/theme_edit.png', triggers=self.on_rename_theme)
        self.delete_action = create_widget_action(self.menu,
            text=translate('OpenLP.ThemeManager', '&Delete Theme'),
            icon=':/general/general_delete.png', triggers=self.on_delete_theme)
        self.menu.addSeparator()
        self.global_action = create_widget_action(self.menu,
            text=translate('OpenLP.ThemeManager', 'Set As &Global Default'),
            icon=':/general/general_export.png',
            triggers=self.change_global_from_screen)
        self.exportAction = create_widget_action(self.menu,
            text=translate('OpenLP.ThemeManager', '&Export Theme'),
            icon=':/general/general_export.png', triggers=self.on_export_theme)
        # Signals
        self.theme_list_widget.doubleClicked.connect(self.change_global_from_screen)
        self.theme_list_widget.currentItemChanged.connect(self.check_list_state)
        Registry().register_function('theme_update_global', self.change_global_from_tab)
        # Variables
        self.theme_list = []
        self.path = AppLocation.get_section_data_path(self.settings_section)
        check_directory_exists(self.path)
        self.thumb_path = os.path.join(self.path, 'thumbnails')
        check_directory_exists(self.thumb_path)
        self.theme_form.path = self.path
        self.old_background_image = None
        self.bad_v1_name_chars = re.compile(r'[%+\[\]]')
        # Last little bits of setting up
        self.global_theme = Settings().value(self.settings_section + '/global theme')

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
            self.delete_toolbar_action.setVisible(True)
        else:
            self.delete_toolbar_action.setVisible(False)

    def context_menu(self, point):
        """
        Build the Right Click Context menu and set state depending on
        the type of theme.
        """
        item = self.theme_list_widget.itemAt(point)
        if item is None:
            return
        real_theme_name = item.data(QtCore.Qt.UserRole)
        theme_name = str(item.text())
        visible = real_theme_name == theme_name
        self.delete_action.setVisible(visible)
        self.rename_action.setVisible(visible)
        self.global_action.setVisible(visible)
        self.menu.exec_(self.theme_list_widget.mapToGlobal(point))

    def change_global_from_tab(self):
        """
        Change the global theme when it is changed through the Themes settings tab
        """
        self.global_theme = Settings().value(self.settings_section + '/global theme')
        log.debug('change_global_from_tab %s', self.global_theme)
        for count in range(0, self.theme_list_widget.count()):
            # reset the old name
            item = self.theme_list_widget.item(count)
            old_name = item.text()
            new_name = item.data(QtCore.Qt.UserRole)
            if old_name != new_name:
                self.theme_list_widget.item(count).setText(new_name)
            # Set the new name
            if self.global_theme == new_name:
                name = translate('OpenLP.ThemeManager', '%s (default)') % new_name
                self.theme_list_widget.item(count).setText(name)
                self.delete_toolbar_action.setVisible(item not in self.theme_list_widget.selectedItems())

    def change_global_from_screen(self, index=-1):
        """
        Change the global theme when a theme is double clicked upon in the
        Theme Manager list
        """
        log.debug('change_global_from_screen %s', index)
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
                Settings().setValue(self.settings_section + '/global theme', self.global_theme)
                Registry().execute('theme_update_global')
                self._push_themes()

    def on_add_theme(self):
        """
        Loads a new theme with the default settings and then launches the theme
        editing form for the user to make their customisations.
        """
        theme = ThemeXML()
        theme.set_default_header_footer()
        self.theme_form.theme = theme
        self.theme_form.exec_()
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
            self.file_rename_form.file_name_edit.setText(old_theme_name)
            if self.file_rename_form.exec_():
                new_theme_name = self.file_rename_form.file_name_edit.text()
                if old_theme_name == new_theme_name:
                    return
                if self.check_if_theme_exists(new_theme_name):
                    old_theme_data = self.get_theme_data(old_theme_name)
                    self.clone_theme_data(old_theme_data, new_theme_name)
                    self.delete_theme(old_theme_name)
                    for plugin in self.plugin_manager.plugins:
                        if plugin.uses_theme(old_theme_name):
                            plugin.rename_theme(old_theme_name, new_theme_name)
                    self.renderer.update_theme(new_theme_name, old_theme_name)
                    self.load_themes()

    def on_copy_theme(self):
        """
        Copies an existing theme to a new name
        """
        item = self.theme_list_widget.currentItem()
        old_theme_name = item.data(QtCore.Qt.UserRole)
        self.file_rename_form.file_name_edit.setText(translate('OpenLP.ThemeManager',
            'Copy of %s', 'Copy of <theme name>') % old_theme_name)
        if self.file_rename_form.exec_(True):
            new_theme_name = self.file_rename_form.file_name_edit.text()
            if self.check_if_theme_exists(new_theme_name):
                theme_data = self.get_theme_data(old_theme_name)
                self.clone_theme_data(theme_data, new_theme_name)

    def clone_theme_data(self, theme_data, new_theme_name):
        """
        Takes a theme and makes a new copy of it as well as saving it.
        """
        log.debug('clone_theme_data')
        save_to = None
        save_from = None
        if theme_data.background_type == 'image':
            save_to = os.path.join(self.path, new_theme_name, os.path.split(str(theme_data.background_filename))[1])
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
            if theme.background_type == 'image':
                self.old_background_image = theme.background_filename
            self.theme_form.theme = theme
            self.theme_form.exec_(True)
            self.old_background_image = None
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
        thumb = '%s.png' % theme
        delete_file(os.path.join(self.path, thumb))
        delete_file(os.path.join(self.thumb_path, thumb))
        try:
            encoding = get_filesystem_encoding()
            shutil.rmtree(os.path.join(self.path, theme).encode(encoding))
        except OSError as xxx_todo_changeme1:
            shutil.Error = xxx_todo_changeme1
            log.exception('Error deleting theme %s', theme)

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
            Settings().value(self.settings_section + '/last directory export'))
        self.application.set_busy_cursor()
        if path:
            Settings().setValue(self.settings_section + '/last directory export', path)
            theme_path = os.path.join(path, theme + '.otz')
            theme_zip = None
            try:
                theme_zip = zipfile.ZipFile(theme_path, 'w')
                source = os.path.join(self.path, theme)
                for files in os.walk(source):
                    for name in files[2]:
                        theme_zip.write(
                            os.path.join(source, name).encode('utf-8'), os.path.join(theme, name).encode('utf-8')
                        )
                QtGui.QMessageBox.information(self,
                    translate('OpenLP.ThemeManager', 'Theme Exported'),
                    translate('OpenLP.ThemeManager', 'Your theme has been successfully exported.'))
            except (IOError, OSError):
                log.exception('Export Theme Failed')
                critical_error_message_box(translate('OpenLP.ThemeManager', 'Theme Export Failed'),
                    translate('OpenLP.ThemeManager', 'Your theme could not be exported due to an error.'))
            finally:
                if theme_zip:
                    theme_zip.close()
        self.application.set_normal_cursor()

    def on_import_theme(self):
        """
        Opens a file dialog to select the theme file(s) to import before attempting to extract OpenLP themes from
        those files. This process will load both OpenLP version 1 and version 2 themes.
        """
        files = QtGui.QFileDialog.getOpenFileNames(self,
            translate('OpenLP.ThemeManager', 'Select Theme Import File'),
            Settings().value(self.settings_section + '/last directory import'),
            translate('OpenLP.ThemeManager', 'OpenLP Themes (*.theme *.otz)'))
        log.info('New Themes %s', str(files))
        if not files:
            return
        self.application.set_busy_cursor()
        for file_name in files:
            Settings().setValue(self.settings_section + '/last directory import', str(file_name))
            self.unzip_theme(file_name, self.path)
        self.load_themes()
        self.application.set_normal_cursor()

    def load_first_time_themes(self):
        """
        Imports any themes on start up and makes sure there is at least one theme
        """
        self.application.set_busy_cursor()
        files = AppLocation.get_files(self.settings_section, '.otz')
        for theme_file in files:
            theme_file = os.path.join(self.path, theme_file)
            self.unzip_theme(theme_file, self.path)
            delete_file(theme_file)
        files = AppLocation.get_files(self.settings_section, '.png')
        # No themes have been found so create one
        if not files:
            theme = ThemeXML()
            theme.theme_name = UiStrings().Default
            self._write_theme(theme, None, None)
            Settings().setValue(self.settings_section + '/global theme', theme.theme_name)
        self.application.set_normal_cursor()
        self.load_themes()

    def load_themes(self):
        """
        Loads the theme lists and triggers updates across the whole system
        using direct calls or core functions and events for the plugins.
        The plugins will call back in to get the real list if they want it.
        """
        log.debug('Load themes from dir')
        self.theme_list = []
        self.theme_list_widget.clear()
        files = AppLocation.get_files(self.settings_section, '.png')
        # Sort the themes by its name considering language specific
        files.sort(key=lambda file_name: get_locale_key(str(file_name)))
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
                thumb = os.path.join(self.thumb_path, '%s.png' % text_name)
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
        Registry().execute('theme_update_list', self.get_themes())

    def get_themes(self):
        """
        Return the list of loaded themes
        """
        log.debug('get themes')
        return self.theme_list

    def get_theme_data(self, theme_name):
        """
        Returns a theme object from an XML file

        ``theme_name``
            Name of the theme to load from file
        """
        log.debug('get theme data for theme %s', theme_name)
        xml_file = os.path.join(self.path, str(theme_name), str(theme_name) + '.xml')
        xml = get_text_file_string(xml_file)
        if not xml:
            log.debug('No theme data - using default theme')
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
        log.debug('Unzipping theme %s', file_name)
        file_name = str(file_name)
        theme_zip = None
        out_file = None
        file_xml = None
        abort_import = True
        try:
            theme_zip = zipfile.ZipFile(file_name)
            xml_file = [name for name in theme_zip.namelist() if os.path.splitext(name)[1].lower() == '.xml']
            if len(xml_file) != 1:
                log.exception('Theme contains "%s" XML files' % len(xml_file))
                raise Exception('validation')
            xml_tree = ElementTree(element=XML(theme_zip.read(xml_file[0]))).getroot()
            v1_background = xml_tree.find('BackgroundType')
            if v1_background is not None:
                theme_name, file_xml, out_file, abort_import = \
                    self.unzip_version_122(directory, theme_zip, xml_file[0], xml_tree, v1_background, out_file)
            else:
                theme_name = xml_tree.find('name').text.strip()
                theme_folder = os.path.join(directory, theme_name)
                theme_exists = os.path.exists(theme_folder)
                if theme_exists and not self.over_write_message_box(theme_name):
                    abort_import = True
                    return
                else:
                    abort_import = False
                for name in theme_zip.namelist():
                    name = name.replace('/', os.path.sep)
                    split_name = name.split(os.path.sep)
                    if split_name[-1] == '' or len(split_name) == 1:
                        # is directory or preview file
                        continue
                    full_name = os.path.join(directory, name)
                    check_directory_exists(os.path.dirname(full_name))
                    if os.path.splitext(name)[1].lower() == '.xml':
                        file_xml = str(theme_zip.read(name), 'utf-8')
                        out_file = open(full_name, 'w')
                        out_file.write(file_xml)
                    else:
                        out_file = open(full_name, 'wb')
                        out_file.write(theme_zip.read(name))
                    out_file.close()
        except (IOError, zipfile.BadZipfile):
            log.exception('Importing theme from zip failed %s' % file_name)
            raise Exception('validation')
        except Exception as info:
            if str(info) == 'validation':
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
                    log.exception('Theme file does not contain XML data %s' % file_name)

    def unzip_version_122(self, dir_name, zip_file, xml_file, xml_tree, background, out_file):
        """
        Unzip openlp.org 1.2x theme file and upgrade the theme xml. When calling
        this method, please keep in mind, that some parameters are redundant.
        """
        theme_name = xml_tree.find('Name').text.strip()
        theme_name = self.bad_v1_name_chars.sub('', theme_name)
        theme_folder = os.path.join(dir_name, theme_name)
        theme_exists = os.path.exists(theme_folder)
        if theme_exists and not self.over_write_message_box(theme_name):
            return '', '', '', True
        themedir = os.path.join(dir_name, theme_name)
        check_directory_exists(themedir)
        file_xml = str(zip_file.read(xml_file), 'utf-8')
        file_xml = self._migrate_version_122(file_xml)
        out_file = open(os.path.join(themedir, theme_name + '.xml'), 'w')
        out_file.write(file_xml.encode('utf-8'))
        out_file.close()
        if background.text.strip() == '2':
            image_name = xml_tree.find('BackgroundParameter1').text.strip()
            # image file has same extension and is in subfolder
            image_file = [name for name in zip_file.namelist() if os.path.splitext(name)[1].lower()
                == os.path.splitext(image_name)[1].lower() and name.find(r'/')]
            if len(image_file) >= 1:
                out_file = open(os.path.join(themedir, image_name), 'wb')
                out_file.write(zip_file.read(image_file[0]))
                out_file.close()
            else:
                log.exception('Theme file does not contain image file "%s"' % image_name.decode('utf-8', 'replace'))
                raise Exception('validation')
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
        log.debug('save_theme %s %s', name, theme_pretty_xml.decode('utf-8'))
        theme_dir = os.path.join(self.path, name)
        check_directory_exists(theme_dir)
        theme_file = os.path.join(theme_dir, name + '.xml')
        if self.old_background_image and image_to != self.old_background_image:
            delete_file(self.old_background_image)
        out_file = None
        try:
            out_file = open(theme_file, 'w')
            out_file.write(theme_pretty_xml.decode('UTF-8'))
        except IOError:
            log.exception('Saving theme to file failed')
        finally:
            if out_file:
                out_file.close()
        if image_from and image_from != image_to:
            try:
                encoding = get_filesystem_encoding()
                shutil.copyfile(str(image_from).encode(encoding), str(image_to).encode(encoding))
            except IOError as xxx_todo_changeme:
                shutil.Error = xxx_todo_changeme
                log.exception('Failed to save theme image')
        self.generate_and_save_image(self.path, name, theme)

    def generate_and_save_image(self, directory, name, theme):
        """
        Generate and save a preview image
        """
        log.debug('generate_and_save_image %s %s', directory, name)
        frame = self.generate_image(theme)
        sample_path_name = os.path.join(self.path, name + '.png')
        if os.path.exists(sample_path_name):
            os.unlink(sample_path_name)
        frame.save(sample_path_name, 'png')
        thumb = os.path.join(self.thumb_path, '%s.png' % name)
        create_thumb(sample_path_name, thumb, False)
        log.debug('Theme image written to %s', sample_path_name)

    def update_preview_images(self):
        """
        Called to update the themes' preview images.
        """
        log.debug('update_preview_images')
        self.main_window.display_progress_bar(len(self.theme_list))
        for theme in self.theme_list:
            self.main_window.increment_progress_bar()
            self.generate_and_save_image(self.path, theme, self.get_theme_data(theme))
        self.main_window.finished_progress_bar()
        self.load_themes()

    def generate_image(self, theme_data, forcePage=False):
        """
        Call the renderer to build a Sample Image

        ``theme_data``
            The theme to generated a preview for.

        ``forcePage``
            Flag to tell message lines per page need to be generated.
        """
        log.debug('generate_image \n%s ', theme_data)
        return self.renderer.generate_preview(theme_data, forcePage)

    def get_preview_image(self, theme):
        """
        Return an image representing the look of the theme

        ``theme``
            The theme to return the image for
        """
        log.debug('get_preview_image %s ', theme)
        image = os.path.join(self.path, theme + '.png')
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
        self.global_theme = Settings().value(self.settings_section + '/global theme')
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
                    if plugin.uses_theme(theme):
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
        new_theme.theme_name = self.bad_v1_name_chars.sub('', theme.Name)
        if theme.BackgroundType == BackgroundType.Solid:
            new_theme.background_type = BackgroundType.to_string(BackgroundType.Solid)
            new_theme.background_color = str(theme.BackgroundParameter1.name())
        elif theme.BackgroundType == BackgroundType.Horizontal:
            new_theme.background_type = BackgroundType.to_string(BackgroundType.Gradient)
            new_theme.background_direction = BackgroundGradientType.to_string(BackgroundGradientType.Horizontal)
            if theme.BackgroundParameter3.name() == 1:
                new_theme.background_direction = BackgroundGradientType.to_string(BackgroundGradientType.Horizontal)
            new_theme.background_start_color = str(theme.BackgroundParameter1.name())
            new_theme.background_end_color = str(theme.BackgroundParameter2.name())
        elif theme.BackgroundType == BackgroundType.Image:
            new_theme.background_type = BackgroundType.to_string(BackgroundType.Image)
            new_theme.background_filename = str(theme.BackgroundParameter1)
        elif theme.BackgroundType == BackgroundType.Transparent:
            new_theme.background_type = BackgroundType.to_string(BackgroundType.Transparent)
        new_theme.font_main_name = theme.FontName
        new_theme.font_main_color = str(theme.FontColor.name())
        new_theme.font_main_size = theme.FontProportion * 3
        new_theme.font_footer_name = theme.FontName
        new_theme.font_footer_color = str(theme.FontColor.name())
        new_theme.font_main_shadow = False
        if theme.Shadow == 1:
            new_theme.font_main_shadow = True
            new_theme.font_main_shadow_color = str(theme.ShadowColor.name())
        if theme.Outline == 1:
            new_theme.font_main_outline = True
            new_theme.font_main_outline_color = str(theme.OutlineColor.name())
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
        if not hasattr(self, '_renderer'):
            self._renderer = Registry().get('renderer')
        return self._renderer

    renderer = property(_get_renderer)

    def _get_image_manager(self):
        """
        Adds the image manager to the class dynamically
        """
        if not hasattr(self, '_image_manager'):
            self._image_manager = Registry().get('image_manager')
        return self._image_manager

    image_manager = property(_get_image_manager)

    def _get_plugin_manager(self):
        """
        Adds the Renderer to the class dynamically
        """
        if not hasattr(self, '_plugin_manager'):
            self._plugin_manager = Registry().get('plugin_manager')
        return self._plugin_manager

    plugin_manager = property(_get_plugin_manager)

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, '_main_window'):
            self._main_window = Registry().get('main_window')
        return self._main_window

    main_window = property(_get_main_window)

    def _get_application(self):
        """
        Adds the openlp to the class dynamically.
        Windows needs to access the application in a dynamic manner.
        """
        if os.name == 'nt':
            return Registry().get('application')
        else:
            if not hasattr(self, '_application'):
                self._application = Registry().get('application')
            return self._application

    application = property(_get_application)
