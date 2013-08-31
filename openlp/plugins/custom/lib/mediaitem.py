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

import logging

from PyQt4 import QtCore, QtGui
from sqlalchemy.sql import or_, func, and_

from openlp.core.lib import Registry, MediaManagerItem, ItemCapabilities, ServiceItemContext, Settings, PluginStatus,\
    UiStrings, check_item_selected, translate
from openlp.plugins.custom.forms.editcustomform import EditCustomForm
from openlp.plugins.custom.lib import CustomXMLParser, CustomXMLBuilder
from openlp.plugins.custom.lib.db import CustomSlide

log = logging.getLogger(__name__)


class CustomSearch(object):
    """
    An enumeration for custom search methods.
    """
    Titles = 1
    Themes = 2


class CustomMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Custom Slides.
    """
    log.info('Custom Media Item loaded')

    def __init__(self, parent, plugin):
        self.icon_path = 'custom/custom'
        super(CustomMediaItem, self).__init__(parent, plugin)
        self.edit_custom_form = EditCustomForm(self, self.main_window, self.plugin.manager)
        self.single_service_item = False
        self.quick_preview_allowed = True
        self.has_search = True
        # Holds information about whether the edit is remotely triggered and
        # which Custom is required.
        self.remote_custom = -1
        self.manager = plugin.manager

    def add_end_header_bar(self):
        self.toolbar.addSeparator()
        self.add_search_to_toolbar()
        # Signals and slots
        QtCore.QObject.connect(self.search_text_edit, QtCore.SIGNAL('cleared()'), self.on_clear_text_button_click)
        QtCore.QObject.connect(self.search_text_edit, QtCore.SIGNAL('searchTypeChanged(int)'),
            self.on_search_text_button_clicked)
        Registry().register_function('custom_load_list', self.load_list)
        Registry().register_function('custom_preview', self.on_preview_click)
        Registry().register_function('custom_create_from_service', self.create_from_service_item)

    def config_update(self):
        """
        Config has been updated so reload values
        """
        log.debug('Config loaded')
        self.add_custom_from_service = Settings().value(self.settings_section + '/add custom from service')

    def retranslateUi(self):
        self.search_text_label.setText('%s:' % UiStrings().Search)
        self.search_text_button.setText(UiStrings().Search)

    def initialise(self):
        self.search_text_edit.set_search_types([
            (CustomSearch.Titles, ':/songs/song_search_title.png',
            translate('SongsPlugin.MediaItem', 'Titles'),
            translate('SongsPlugin.MediaItem', 'Search Titles...')),
            (CustomSearch.Themes, ':/slides/slide_theme.png', UiStrings().Themes, UiStrings().SearchThemes)
        ])
        self.search_text_edit.set_current_search_type(Settings().value('%s/last search type' % self.settings_section))
        self.load_list(self.manager.get_all_objects(CustomSlide, order_by_ref=CustomSlide.title))
        self.config_update()

    def load_list(self, custom_slides, target_group=None):
        # Sort out what custom we want to select after loading the list.
        self.save_auto_select_id()
        self.list_view.clear()
        custom_slides.sort()
        for custom_slide in custom_slides:
            custom_name = QtGui.QListWidgetItem(custom_slide.title)
            custom_name.setData(QtCore.Qt.UserRole, custom_slide.id)
            self.list_view.addItem(custom_name)
            # Auto-select the custom.
            if custom_slide.id == self.auto_select_id:
                self.list_view.setCurrentItem(custom_name)
        self.auto_select_id = -1
        # Called to redisplay the custom list screen edith from a search
        # or from the exit of the Custom edit dialog. If remote editing is
        # active trigger it and clean up so it will not update again.

    def on_new_click(self):
        self.edit_custom_form.load_custom(0)
        self.edit_custom_form.exec_()
        self.on_clear_text_button_click()
        self.on_selection_change()

    def on_remote_edit(self, custom_id, preview=False):
        """
        Called by ServiceManager or SlideController by event passing the custom Id in the payload along with an
        indicator to say which type of display is required.
        """
        custom_id = int(custom_id)
        valid = self.manager.get_object(CustomSlide, custom_id)
        if valid:
            self.edit_custom_form.load_custom(custom_id, preview)
            if self.edit_custom_form.exec_() == QtGui.QDialog.Accepted:
                self.remote_triggered = True
                self.remote_custom = custom_id
                self.auto_select_id = -1
                self.on_search_text_button_clicked()
                item = self.build_service_item(remote=True)
                self.remote_triggered = None
                self.remote_custom = 1
                if item:
                    return item
        return None

    def on_edit_click(self):
        """
        Edit a custom item
        """
        if check_item_selected(self.list_view, UiStrings().SelectEdit):
            item = self.list_view.currentItem()
            item_id = item.data(QtCore.Qt.UserRole)
            self.edit_custom_form.load_custom(item_id, False)
            self.edit_custom_form.exec_()
            self.auto_select_id = -1
            self.on_search_text_button_clicked()

    def on_delete_click(self):
        """
        Remove a custom item from the list and database
        """
        if check_item_selected(self.list_view, UiStrings().SelectDelete):
            items = self.list_view.selectedIndexes()
            if QtGui.QMessageBox.question(self,
                    UiStrings().ConfirmDelete,
                    translate('CustomPlugin.MediaItem',
                        'Are you sure you want to delete the %n selected custom slide(s)?', '',
                    QtCore.QCoreApplication.CodecForTr, len(items)),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
                    QtGui.QMessageBox.Yes) == QtGui.QMessageBox.No:
                return
            row_list = [item.row() for item in self.list_view.selectedIndexes()]
            row_list.sort(reverse=True)
            id_list = [(item.data(QtCore.Qt.UserRole)) for item in self.list_view.selectedIndexes()]
            for id in id_list:
                self.plugin.manager.delete_object(CustomSlide, id)
            self.on_search_text_button_clicked()

    def on_focus(self):
        self.search_text_edit.setFocus()

    def generate_slide_data(self, service_item, item=None, xmlVersion=False,
        remote=False, context=ServiceItemContext.Service):
        """
        Generate the slide data. Needs to be implemented by the plugin.
        """
        item_id = self._get_id_of_item_to_generate(item, self.remote_custom)
        service_item.add_capability(ItemCapabilities.CanEdit)
        service_item.add_capability(ItemCapabilities.CanPreview)
        service_item.add_capability(ItemCapabilities.CanLoop)
        service_item.add_capability(ItemCapabilities.CanSoftBreak)
        service_item.add_capability(ItemCapabilities.OnLoadUpdate)
        custom_slide = self.plugin.manager.get_object(CustomSlide, item_id)
        title = custom_slide.title
        credit = custom_slide.credits
        service_item.edit_id = item_id
        theme = custom_slide.theme_name
        if theme:
            service_item.theme = theme
        custom_xml = CustomXMLParser(custom_slide.text)
        verse_list = custom_xml.get_verses()
        raw_slides = [verse[1] for verse in verse_list]
        service_item.title = title
        for slide in raw_slides:
            service_item.add_from_text(slide)
        if Settings().value(self.settings_section + '/display footer') or credit:
            service_item.raw_footer.append(' '.join([title, credit]))
        else:
            service_item.raw_footer.append('')
        return True

    def on_search_text_button_clicked(self):
        # Save the current search type to the configuration.
        Settings().setValue('%s/last search type' % self.settings_section, self.search_text_edit.current_search_type())
        # Reload the list considering the new search type.
        search_keywords = self.search_text_edit.displayText()
        search_type = self.search_text_edit.current_search_type()
        if search_type == CustomSearch.Titles:
            log.debug('Titles Search')
            search_results = self.plugin.manager.get_all_objects(CustomSlide,
                CustomSlide.title.like('%' + self.whitespace.sub(' ', search_keywords) + '%'),
                    order_by_ref=CustomSlide.title)
            self.load_list(search_results)
        elif search_type == CustomSearch.Themes:
            log.debug('Theme Search')
            search_results = self.plugin.manager.get_all_objects(CustomSlide,
                CustomSlide.theme_name.like('%' + self.whitespace.sub(' ', search_keywords) + '%'),
                    order_by_ref=CustomSlide.title)
            self.load_list(search_results)
        self.check_search_result()

    def on_search_text_edit_changed(self, text):
        """
        If search as type enabled invoke the search on each key press. If the Title is being searched do not start until
        2 characters have been entered.
        """
        search_length = 2
        if len(text) > search_length:
            self.on_search_text_button_clicked()
        elif not text:
            self.on_clear_text_button_click()

    def service_load(self, item):
        """
        Triggered by a song being loaded by the service manager.
        """
        log.debug('service_load')
        if self.plugin.status != PluginStatus.Active:
            return
        custom = self.plugin.manager.get_object_filtered(CustomSlide,
            and_(CustomSlide.title == item.title, CustomSlide.theme_name == item.theme,
                CustomSlide.credits == item.raw_footer[0][len(item.title) + 1:]))
        if custom:
            item.edit_id = custom.id
            return item
        else:
            if self.add_custom_from_service:
                self.create_from_service_item(item)

    def create_from_service_item(self, item):
        """
        Create a custom slide from a text service item
        """
        custom = CustomSlide()
        custom.title = item.title
        if item.theme:
            custom.theme_name = item.theme
        else:
            custom.theme_name = ''
        footer = ' '.join(item.raw_footer)
        if footer:
            if footer.startswith(item.title):
                custom.credits = footer[len(item.title) + 1:]
            else:
                custom.credits = footer
        else:
            custom.credits = ''
        custom_xml = CustomXMLBuilder()
        for (idx, slide) in enumerate(item._raw_frames):
            custom_xml.add_verse_to_lyrics('custom', str(idx + 1), slide['raw_slide'])
        custom.text = str(custom_xml.extract_xml(), 'utf-8')
        self.plugin.manager.save_object(custom)
        self.on_search_text_button_clicked()

    def on_clear_text_button_click(self):
        """
        Clear the search text.
        """
        self.search_text_edit.clear()
        self.on_search_text_button_clicked()

    def search(self, string, showError):
        search_results = self.manager.get_all_objects(CustomSlide,
            or_(func.lower(CustomSlide.title).like('%' + string.lower() + '%'),
                func.lower(CustomSlide.text).like('%' + string.lower() + '%')),
            order_by_ref=CustomSlide.title)
        return [[custom.id, custom.title] for custom in search_results]

