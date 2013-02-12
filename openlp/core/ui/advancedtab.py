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
The :mod:`advancedtab` provides an advanced settings facility.
"""
from datetime import datetime, timedelta
import logging
import os
import sys

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab, Receiver, Settings, UiStrings, translate, build_icon
from openlp.core.utils import AppLocation, format_time, get_images_filter
from openlp.core.lib import SlideLimits

log = logging.getLogger(__name__)


class AdvancedTab(SettingsTab):
    """
    The :class:`AdvancedTab` manages the advanced settings tab including the UI
    and the loading and saving of the displayed settings.
    """
    def __init__(self, parent):
        """
        Initialise the settings tab
        """
        self.display_changed = False
        self.default_image = u':/graphics/openlp-splash-screen.png'
        self.default_color = u'#ffffff'
        self.data_exists = False
        self.iconPath = u':/system/system_settings.png'
        advanced_translated = translate('OpenLP.AdvancedTab', 'Advanced')
        SettingsTab.__init__(self, parent, u'Advanced', advanced_translated)

    def setupUi(self):
        """
        Configure the UI elements for the tab.
        """
        self.setObjectName(u'AdvancedTab')
        SettingsTab.setupUi(self)
        self.ui_group_box = QtGui.QGroupBox(self.leftColumn)
        self.ui_group_box.setObjectName(u'ui_group_box')
        self.ui_layout = QtGui.QFormLayout(self.ui_group_box)
        self.ui_layout.setObjectName(u'ui_layout')
        self.recent_label = QtGui.QLabel(self.ui_group_box)
        self.recent_label.setObjectName(u'recent_label')
        self.recent_spin_box = QtGui.QSpinBox(self.ui_group_box)
        self.recent_spin_box.setObjectName(u'recent_spin_box')
        self.recent_spin_box.setMinimum(0)
        self.ui_layout.addRow(self.recent_label, self.recent_spin_box)
        self.media_plugin_check_box = QtGui.QCheckBox(self.ui_group_box)
        self.media_plugin_check_box.setObjectName(u'media_plugin_check_box')
        self.ui_layout.addRow(self.media_plugin_check_box)
        self.double_click_live_check_box = QtGui.QCheckBox(self.ui_group_box)
        self.double_click_live_check_box.setObjectName(u'double_click_live_check_box')
        self.ui_layout.addRow(self.double_click_live_check_box)
        self.single_click_preview_check_box = QtGui.QCheckBox(self.ui_group_box)
        self.single_click_preview_check_box.setObjectName(u'single_click_preview_check_box')
        self.ui_layout.addRow(self.single_click_preview_check_box)
        self.expand_service_item_check_box = QtGui.QCheckBox(self.ui_group_box)
        self.expand_service_item_check_box.setObjectName(u'expand_service_item_check_box')
        self.ui_layout.addRow(self.expand_service_item_check_box)
        self.enable_auto_close_check_box = QtGui.QCheckBox(self.ui_group_box)
        self.enable_auto_close_check_box.setObjectName(u'enable_auto_close_check_box')
        self.ui_layout.addRow(self.enable_auto_close_check_box)
        self.leftLayout.addWidget(self.ui_group_box)
        # Default service name
        self.service_name_group_box = QtGui.QGroupBox(self.leftColumn)
        self.service_name_group_box.setObjectName(u'service_name_group_box')
        self.service_name_layout = QtGui.QFormLayout(self.service_name_group_box)
        self.service_name_check_box = QtGui.QCheckBox(self.service_name_group_box)
        self.service_name_check_box.setObjectName(u'service_name_check_box')
        self.service_name_layout.setObjectName(u'service_name_layout')
        self.service_name_layout.addRow(self.service_name_check_box)
        self.service_name_time_label = QtGui.QLabel(self.service_name_group_box)
        self.service_name_time_label.setObjectName(u'service_name_time_label')
        self.service_name_day = QtGui.QComboBox(self.service_name_group_box)
        self.service_name_day.addItems([u'', u'', u'', u'', u'', u'', u'', u''])
        self.service_name_day.setObjectName(u'service_name_day')
        self.service_name_time = QtGui.QTimeEdit(self.service_name_group_box)
        self.service_name_time.setObjectName(u'service_name_time')
        self.service_name_time_layout = QtGui.QHBoxLayout()
        self.service_name_time_layout.setObjectName(u'service_name_time_layout')
        self.service_name_time_layout.addWidget(self.service_name_day)
        self.service_name_time_layout.addWidget(self.service_name_time)
        self.service_name_layout.addRow(self.service_name_time_label, self.service_name_time_layout)
        self.service_name_label = QtGui.QLabel(self.service_name_group_box)
        self.service_name_label.setObjectName(u'service_name_label')
        self.service_name_edit = QtGui.QLineEdit(self.service_name_group_box)
        self.service_name_edit.setObjectName(u'service_name_edit')
        self.service_name_edit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'[^/\\?*|<>\[\]":+]+'), self))
        self.service_name_revert_button = QtGui.QToolButton(self.service_name_group_box)
        self.service_name_revert_button.setObjectName(u'service_name_revert_button')
        self.service_name_revert_button.setIcon(build_icon(u':/general/general_revert.png'))
        self.service_name_button_layout = QtGui.QHBoxLayout()
        self.service_name_button_layout.setObjectName(u'service_name_button_layout')
        self.service_name_button_layout.addWidget(self.service_name_edit)
        self.service_name_button_layout.addWidget(self.service_name_revert_button)
        self.service_name_layout.addRow(self.service_name_label, self.service_name_button_layout)
        self.service_name_example_label = QtGui.QLabel(self.service_name_group_box)
        self.service_name_example_label.setObjectName(u'service_name_example_label')
        self.service_name_example = QtGui.QLabel(self.service_name_group_box)
        self.service_name_example.setObjectName(u'service_name_example')
        self.service_name_layout.addRow(self.service_name_example_label, self.service_name_example)
        self.leftLayout.addWidget(self.service_name_group_box)
        # Data Directory
        self.data_directory_group_box = QtGui.QGroupBox(self.leftColumn)
        self.data_directory_group_box.setObjectName(u'data_directory_group_box')
        self.data_directory_layout = QtGui.QFormLayout(self.data_directory_group_box)
        self.data_directory_layout.setObjectName(u'data_directory_layout')
        self.data_directory_current_label = QtGui.QLabel(self.data_directory_group_box)
        self.data_directory_current_label.setObjectName(u'data_directory_current_label')
        self.data_directory_label = QtGui.QLabel(self.data_directory_group_box)
        self.data_directory_label.setObjectName(u'data_directory_label')
        self.data_directory_new_label = QtGui.QLabel(self.data_directory_group_box)
        self.data_directory_new_label.setObjectName(u'data_directory_current_label')
        self.new_data_directory_edit = QtGui.QLineEdit(self.data_directory_group_box)
        self.new_data_directory_edit.setObjectName(u'new_data_directory_edit')
        self.new_data_directory_edit.setReadOnly(True)
        self.new_data_directory_has_files_label = QtGui.QLabel(self.data_directory_group_box)
        self.new_data_directory_has_files_label.setObjectName(u'new_data_directory_has_files_label')
        self.new_data_directory_has_files_label.setWordWrap(True)
        self.data_directory_browse_button = QtGui.QToolButton(self.data_directory_group_box)
        self.data_directory_browse_button.setObjectName(u'data_directory_browse_button')
        self.data_directory_browse_button.setIcon(build_icon(u':/general/general_open.png'))
        self.data_directory_default_button = QtGui.QToolButton(self.data_directory_group_box)
        self.data_directory_default_button.setObjectName(u'data_directory_default_button')
        self.data_directory_default_button.setIcon(build_icon(u':/general/general_revert.png'))
        self.data_directory_cancel_button = QtGui.QToolButton(self.data_directory_group_box)
        self.data_directory_cancel_button.setObjectName(u'data_directory_cancel_button')
        self.data_directory_cancel_button.setIcon(build_icon(u':/general/general_delete.png'))
        self.new_data_directory_label_layout = QtGui.QHBoxLayout()
        self.new_data_directory_label_layout.setObjectName(u'new_data_directory_label_layout')
        self.new_data_directory_label_layout.addWidget(self.new_data_directory_edit)
        self.new_data_directory_label_layout.addWidget(self.data_directory_browse_button)
        self.new_data_directory_label_layout.addWidget(self.data_directory_default_button)
        self.data_directory_copy_check_layout = QtGui.QHBoxLayout()
        self.data_directory_copy_check_layout.setObjectName(u'data_directory_copy_check_layout')
        self.data_directory_copy_check_box = QtGui.QCheckBox(self.data_directory_group_box)
        self.data_directory_copy_check_box.setObjectName(u'data_directory_copy_check_box')
        self.data_directory_copy_check_layout.addWidget(self.data_directory_copy_check_box)
        self.data_directory_copy_check_layout.addStretch()
        self.data_directory_copy_check_layout.addWidget(self.data_directory_cancel_button)
        self.data_directory_layout.addRow(self.data_directory_current_label, self.data_directory_label)
        self.data_directory_layout.addRow(self.data_directory_new_label, self.new_data_directory_label_layout)
        self.data_directory_layout.addRow(self.data_directory_copy_check_layout)
        self.data_directory_layout.addRow(self.new_data_directory_has_files_label)
        self.leftLayout.addWidget(self.data_directory_group_box)
        self.leftLayout.addStretch()
        # Default Image
        self.default_image_group_box = QtGui.QGroupBox(self.rightColumn)
        self.default_image_group_box.setObjectName(u'default_image_group_box')
        self.default_image_layout = QtGui.QFormLayout(self.default_image_group_box)
        self.default_image_layout.setObjectName(u'default_image_layout')
        self.default_color_label = QtGui.QLabel(self.default_image_group_box)
        self.default_color_label.setObjectName(u'default_color_label')
        self.default_color_button = QtGui.QPushButton(self.default_image_group_box)
        self.default_color_button.setObjectName(u'default_color_button')
        self.default_image_layout.addRow(self.default_color_label, self.default_color_button)
        self.default_file_label = QtGui.QLabel(self.default_image_group_box)
        self.default_file_label.setObjectName(u'default_file_label')
        self.default_file_edit = QtGui.QLineEdit(self.default_image_group_box)
        self.default_file_edit.setObjectName(u'default_file_edit')
        self.default_browse_button = QtGui.QToolButton(self.default_image_group_box)
        self.default_browse_button.setObjectName(u'default_browse_button')
        self.default_browse_button.setIcon(build_icon(u':/general/general_open.png'))
        self.default_revert_button = QtGui.QToolButton(self.default_image_group_box)
        self.default_revert_button.setObjectName(u'default_revert_button')
        self.default_revert_button.setIcon(build_icon(u':/general/general_revert.png'))
        self.default_file_layout = QtGui.QHBoxLayout()
        self.default_file_layout.setObjectName(u'default_file_layout')
        self.default_file_layout.addWidget(self.default_file_edit)
        self.default_file_layout.addWidget(self.default_browse_button)
        self.default_file_layout.addWidget(self.default_revert_button)
        self.default_image_layout.addRow(self.default_file_label, self.default_file_layout)
        self.rightLayout.addWidget(self.default_image_group_box)
        # Hide mouse
        self.hide_mouse_group_box = QtGui.QGroupBox(self.rightColumn)
        self.hide_mouse_group_box.setObjectName(u'hide_mouse_group_box')
        self.hide_mouse_layout = QtGui.QVBoxLayout(self.hide_mouse_group_box)
        self.hide_mouse_layout.setObjectName(u'hide_mouse_layout')
        self.hide_mouse_check_box = QtGui.QCheckBox(self.hide_mouse_group_box)
        self.hide_mouse_check_box.setObjectName(u'hide_mouse_check_box')
        self.hide_mouse_layout.addWidget(self.hide_mouse_check_box)
        self.rightLayout.addWidget(self.hide_mouse_group_box)
        # Service Item Slide Limits
        self.slide_group_box = QtGui.QGroupBox(self.rightColumn)
        self.slide_group_box.setObjectName(u'slide_group_box')
        self.slide_layout = QtGui.QVBoxLayout(self.slide_group_box)
        self.slide_layout.setObjectName(u'slide_layout')
        self.slide_label = QtGui.QLabel(self.slide_group_box)
        self.slide_label.setWordWrap(True)
        self.slide_layout.addWidget(self.slide_label)
        self.end_slide_radio_button = QtGui.QRadioButton(self.slide_group_box)
        self.end_slide_radio_button.setObjectName(u'end_slide_radio_button')
        self.slide_layout.addWidget(self.end_slide_radio_button)
        self.wrap_slide_radio_button = QtGui.QRadioButton(self.slide_group_box)
        self.wrap_slide_radio_button.setObjectName(u'wrap_slide_radio_button')
        self.slide_layout.addWidget(self.wrap_slide_radio_button)
        self.next_item_radio_button = QtGui.QRadioButton(self.slide_group_box)
        self.next_item_radio_button.setObjectName(u'next_item_radio_button')
        self.slide_layout.addWidget(self.next_item_radio_button)
        self.rightLayout.addWidget(self.slide_group_box)
        # Display Workarounds
        self.display_workaround_group_box = QtGui.QGroupBox(self.leftColumn)
        self.display_workaround_group_box.setObjectName(u'display_workaround_group_box')
        self.display_workaround_layout = QtGui.QVBoxLayout(self.display_workaround_group_box)
        self.display_workaround_layout.setObjectName(u'display_workaround_layout')
        self.x11_bypass_check_box = QtGui.QCheckBox(self.display_workaround_group_box)
        self.x11_bypass_check_box.setObjectName(u'x11_bypass_check_box')
        self.display_workaround_layout.addWidget(self.x11_bypass_check_box)
        self.alternate_rows_check_box = QtGui.QCheckBox(self.display_workaround_group_box)
        self.alternate_rows_check_box.setObjectName(u'alternate_rows_check_box')
        self.display_workaround_layout.addWidget(self.alternate_rows_check_box)
        self.rightLayout.addWidget(self.display_workaround_group_box)
        self.rightLayout.addStretch()
        self.should_update_service_name_example = False
        QtCore.QObject.connect(self.service_name_check_box, QtCore.SIGNAL(u'toggled(bool)'),
            self.service_name_check_box_toggled)
        QtCore.QObject.connect(self.service_name_day, QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.on_service_name_day_changed)
        QtCore.QObject.connect(self.service_name_time, QtCore.SIGNAL(u'timeChanged(QTime)'),
            self.update_service_name_example)
        QtCore.QObject.connect(self.service_name_edit, QtCore.SIGNAL(u'textChanged(QString)'),
            self.update_service_name_example)
        QtCore.QObject.connect(self.service_name_revert_button, QtCore.SIGNAL(u'clicked()'),
            self.on_service_name_revert_button_clicked)
        QtCore.QObject.connect(self.default_color_button, QtCore.SIGNAL(u'clicked()'),
            self.on_default_color_button_clicked)
        QtCore.QObject.connect(self.default_browse_button, QtCore.SIGNAL(u'clicked()'),
            self.on_default_browse_button_clicked)
        QtCore.QObject.connect(self.default_revert_button, QtCore.SIGNAL(u'clicked()'),
            self.on_default_revert_button_clicked)
        QtCore.QObject.connect(self.x11_bypass_check_box, QtCore.SIGNAL(u'toggled(bool)'),
            self.on_X11_bypass_check_box_toggled)
        QtCore.QObject.connect(self.alternate_rows_check_box,QtCore.SIGNAL(u'toggled(bool)'),
            self.on_alternate_rows_check_box_toggled)
        QtCore.QObject.connect(self.data_directory_browse_button, QtCore.SIGNAL(u'clicked()'),
            self.on_data_directory_browse_button_clicked)
        QtCore.QObject.connect(self.data_directory_default_button, QtCore.SIGNAL(u'clicked()'),
            self.on_data_directory_default_button_clicked)
        QtCore.QObject.connect(self.data_directory_cancel_button, QtCore.SIGNAL(u'clicked()'),
            self.on_data_directory_cancel_button_clicked)
        QtCore.QObject.connect(self.data_directory_copy_check_box, QtCore.SIGNAL(u'toggled(bool)'),
            self.on_data_directory_copy_check_box_toggled)
        QtCore.QObject.connect(self.end_slide_radio_button, QtCore.SIGNAL(u'clicked()'),
            self.on_end_slide_button_clicked)
        QtCore.QObject.connect(self.wrap_slide_radio_button, QtCore.SIGNAL(u'clicked()'),
            self.on_wrap_slide_button_clicked)
        QtCore.QObject.connect(self.next_item_radio_button, QtCore.SIGNAL(u'clicked()'),
            self.on_next_item_button_clicked)


    def retranslateUi(self):
        """
        Setup the interface translation strings.
        """
        self.tabTitleVisible = UiStrings().Advanced
        self.ui_group_box.setTitle(translate('OpenLP.AdvancedTab', 'UI Settings'))
        self.data_directory_group_box.setTitle(translate('OpenLP.AdvancedTab', 'Data Location'))
        self.recent_label.setText(translate('OpenLP.AdvancedTab', 'Number of recent files to display:'))
        self.media_plugin_check_box.setText(translate('OpenLP.AdvancedTab',
            'Remember active media manager tab on startup'))
        self.double_click_live_check_box.setText(translate('OpenLP.AdvancedTab',
            'Double-click to send items straight to live'))
        self.single_click_preview_check_box.setText(translate('OpenLP.AdvancedTab',
            'Preview items when clicked in Media Manager'))
        self.expand_service_item_check_box.setText(translate('OpenLP.AdvancedTab',
            'Expand new service items on creation'))
        self.enable_auto_close_check_box.setText(translate('OpenLP.AdvancedTab',
            'Enable application exit confirmation'))
        self.service_name_group_box.setTitle(translate('OpenLP.AdvancedTab', 'Default Service Name'))
        self.service_name_check_box.setText(translate('OpenLP.AdvancedTab', 'Enable default service name'))
        self.service_name_time_label.setText(translate('OpenLP.AdvancedTab', 'Date and Time:'))
        self.service_name_day.setItemText(0, translate('OpenLP.AdvancedTab', 'Monday'))
        self.service_name_day.setItemText(1, translate('OpenLP.AdvancedTab', 'Tuesday'))
        self.service_name_day.setItemText(2, translate('OpenLP.AdvancedTab', 'Wednesday'))
        self.service_name_day.setItemText(3, translate('OpenLP.AdvancedTab', 'Thurdsday'))
        self.service_name_day.setItemText(4, translate('OpenLP.AdvancedTab', 'Friday'))
        self.service_name_day.setItemText(5, translate('OpenLP.AdvancedTab', 'Saturday'))
        self.service_name_day.setItemText(6, translate('OpenLP.AdvancedTab', 'Sunday'))
        self.service_name_day.setItemText(7, translate('OpenLP.AdvancedTab', 'Now'))
        self.service_name_time.setToolTip(translate('OpenLP.AdvancedTab',
            'Time when usual service starts.'))
        self.service_name_label.setText(translate('OpenLP.AdvancedTab', 'Name:'))
        self.service_name_edit.setToolTip(translate('OpenLP.AdvancedTab', 'Consult the OpenLP manual for usage.'))
        self.service_name_revert_button.setToolTip(
            translate('OpenLP.AdvancedTab', 'Revert to the default service name "%s".') %
                UiStrings().DefaultServiceName)
        self.service_name_example_label.setText(translate('OpenLP.AdvancedTab', 'Example:'))
        self.hide_mouse_group_box.setTitle(translate('OpenLP.AdvancedTab', 'Mouse Cursor'))
        self.hide_mouse_check_box.setText(translate('OpenLP.AdvancedTab', 'Hide mouse cursor when over display window'))
        self.default_image_group_box.setTitle(translate('OpenLP.AdvancedTab', 'Default Image'))
        self.default_color_label.setText(translate('OpenLP.AdvancedTab', 'Background color:'))
        self.default_color_button.setToolTip(translate('OpenLP.AdvancedTab', 'Click to select a color.'))
        self.default_file_label.setText(translate('OpenLP.AdvancedTab', 'Image file:'))
        self.default_browse_button.setToolTip(translate('OpenLP.AdvancedTab', 'Browse for an image file to display.'))
        self.default_revert_button.setToolTip(translate('OpenLP.AdvancedTab', 'Revert to the default OpenLP logo.'))
        self.data_directory_current_label.setText(translate('OpenLP.AdvancedTab', 'Current path:'))
        self.data_directory_new_label.setText(translate('OpenLP.AdvancedTab', 'Custom path:'))
        self.data_directory_browse_button.setToolTip(translate('OpenLP.AdvancedTab',
            'Browse for new data file location.'))
        self.data_directory_default_button.setToolTip(
            translate('OpenLP.AdvancedTab', 'Set the data location to the default.'))
        self.data_directory_cancel_button.setText(translate('OpenLP.AdvancedTab', 'Cancel'))
        self.data_directory_cancel_button.setToolTip(
            translate('OpenLP.AdvancedTab', 'Cancel OpenLP data directory location change.'))
        self.data_directory_copy_check_box.setText(translate('OpenLP.AdvancedTab', 'Copy data to new location.'))
        self.data_directory_copy_check_box.setToolTip(translate(
            'OpenLP.AdvancedTab', 'Copy the OpenLP data files to the new location.'))
        self.new_data_directory_has_files_label.setText(
            translate('OpenLP.AdvancedTab', '<strong>WARNING:</strong> New data directory location contains '
                'OpenLP data files.  These files WILL be replaced during a copy.'))
        self.display_workaround_group_box.setTitle(translate('OpenLP.AdvancedTab', 'Display Workarounds'))
        self.x11_bypass_check_box.setText(translate('OpenLP.AdvancedTab','Bypass X11 Window Manager'))
        self.alternate_rows_check_box.setText(translate('OpenLP.AdvancedTab', 'Use alternating row colours in lists'))
        # Slide Limits
        self.slide_group_box.setTitle(translate('OpenLP.GeneralTab', 'Service Item Slide Limits'))
        self.slide_label.setText(translate('OpenLP.GeneralTab', 'Behavior of next/previous on the last/first slide:'))
        self.end_slide_radio_button.setText(translate('OpenLP.GeneralTab', '&Remain on Slide'))
        self.wrap_slide_radio_button.setText(translate('OpenLP.GeneralTab', '&Wrap around'))
        self.next_item_radio_button.setText(translate('OpenLP.GeneralTab', '&Move to next/previous service item'))

    def load(self):
        """
        Load settings from disk.
        """
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        # The max recent files value does not have an interface and so never
        # gets actually stored in the settings therefore the default value of
        # 20 will always be used.
        self.recent_spin_box.setMaximum(settings.value(u'max recent files'))
        self.recent_spin_box.setValue(settings.value(u'recent file count'))
        self.media_plugin_check_box.setChecked(settings.value(u'save current plugin'))
        self.double_click_live_check_box.setChecked(settings.value(u'double click live'))
        self.single_click_preview_check_box.setChecked(settings.value(u'single click preview'))
        self.expand_service_item_check_box.setChecked(settings.value(u'expand service item'))
        self.enable_auto_close_check_box.setChecked(settings.value(u'enable exit confirmation'))
        self.hide_mouse_check_box.setChecked(settings.value(u'hide mouse'))
        self.service_name_day.setCurrentIndex(settings.value(u'default service day'))
        self.service_name_time.setTime(QtCore.QTime(settings.value(u'default service hour'),
            settings.value(u'default service minute')))
        self.should_update_service_name_example = True
        self.service_name_edit.setText(settings.value(u'default service name'))
        default_service_enabled = settings.value(u'default service enabled')
        self.service_name_check_box.setChecked(default_service_enabled)
        self.service_name_check_box_toggled(default_service_enabled)
        self.x11_bypass_check_box.setChecked(settings.value(u'x11 bypass wm'))
        self.default_color = settings.value(u'default color')
        self.default_file_edit.setText(settings.value(u'default image'))
        self.slide_limits = settings.value(u'slide limits')
        # Prevent the dialog displayed by the alternate_rows_check_box to display.
        self.alternate_rows_check_box.blockSignals(True)
        self.alternate_rows_check_box.setChecked(settings.value(u'alternate rows'))
        self.alternate_rows_check_box.blockSignals(False)
        if self.slide_limits == SlideLimits.End:
            self.end_slide_radio_button.setChecked(True)
        elif self.slide_limits == SlideLimits.Wrap:
            self.wrap_slide_radio_button.setChecked(True)
        else:
            self.next_item_radio_button.setChecked(True)
        settings.endGroup()
        self.data_directory_copy_check_box.hide()
        self.new_data_directory_has_files_label.hide()
        self.data_directory_cancel_button.hide()
        # Since data location can be changed, make sure the path is present.
        self.current_data_path = AppLocation.get_data_path()
        if not os.path.exists(self.current_data_path):
            log.error(u'Data path not found %s' % self.current_data_path)
            answer = QtGui.QMessageBox.critical(self,
                translate('OpenLP.AdvancedTab',
                'Data Directory Error'),
                translate('OpenLP.AdvancedTab',
                'OpenLP data directory was not found\n\n%s\n\n'
                'This data directory was previously changed from the OpenLP '
                'default location.  If the new location was on removable '
                'media, that media needs to be made available.\n\n'
                'Click "No" to stop loading OpenLP. allowing you to fix '
                'the the problem.\n\n'
                'Click "Yes" to reset the data directory to the default '
                'location.').replace('%s', self.current_data_path),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
                QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.No:
                log.info(u'User requested termination')
                Receiver.send_message(u'cleanup')
                sys.exit()
            # Set data location to default.
            settings.remove(u'advanced/data path')
            self.current_data_path = AppLocation.get_data_path()
            log.warning(u'User requested data path set to default %s' % self.current_data_path)
        self.data_directory_label.setText(os.path.abspath(self.current_data_path))
        self.default_color_button.setStyleSheet(u'background-color: %s' % self.default_color)
        # Don't allow data directory move if running portable.
        if settings.value(u'advanced/is portable'):
            self.data_directory_group_box.hide()

    def save(self):
        """
        Save settings to disk.
        """
        settings = Settings()
        settings.beginGroup(self.settingsSection)
        settings.setValue(u'default service enabled', self.service_name_check_box.isChecked())
        service_name = self.service_name_edit.text()
        preset_is_valid = self.generate_service_name_example()[0]
        if service_name == UiStrings().DefaultServiceName or not preset_is_valid:
            settings.remove(u'default service name')
            self.service_name_edit.setText(service_name)
        else:
            settings.setValue(u'default service name', service_name)
        settings.setValue(u'default service day', self.service_name_day.currentIndex())
        settings.setValue(u'default service hour', self.service_name_time.time().hour())
        settings.setValue(u'default service minute', self.service_name_time.time().minute())
        settings.setValue(u'recent file count', self.recent_spin_box.value())
        settings.setValue(u'save current plugin', self.media_plugin_check_box.isChecked())
        settings.setValue(u'double click live', self.double_click_live_check_box.isChecked())
        settings.setValue(u'single click preview', self.single_click_preview_check_box.isChecked())
        settings.setValue(u'expand service item', self.expand_service_item_check_box.isChecked())
        settings.setValue(u'enable exit confirmation', self.enable_auto_close_check_box.isChecked())
        settings.setValue(u'hide mouse', self.hide_mouse_check_box.isChecked())
        settings.setValue(u'x11 bypass wm', self.x11_bypass_check_box.isChecked())
        settings.setValue(u'alternate rows', self.alternate_rows_check_box.isChecked())
        settings.setValue(u'default color', self.default_color)
        settings.setValue(u'default image', self.default_file_edit.text())
        settings.setValue(u'slide limits', self.slide_limits)
        settings.endGroup()
        if self.display_changed:
            Receiver.send_message(u'config_screen_changed')
            self.display_changed = False
        Receiver.send_message(u'slidecontroller_update_slide_limits')

    def cancel(self):
        """
        Dialogue was cancelled, remove any pending data path change.
        """
        self.on_data_directory_cancel_button_clicked()
        SettingsTab.cancel(self)

    def service_name_check_box_toggled(self, default_service_enabled):
        """
        Service Name options changed
        """
        self.service_name_day.setEnabled(default_service_enabled)
        time_enabled = default_service_enabled and self.service_name_day.currentIndex() is not 7
        self.service_name_time.setEnabled(time_enabled)
        self.service_name_edit.setEnabled(default_service_enabled)
        self.service_name_revert_button.setEnabled(default_service_enabled)

    def generate_service_name_example(self):
        """
        Display an example of the template used
        """
        preset_is_valid = True
        if self.service_name_day.currentIndex() == 7:
            local_time = datetime.now()
        else:
            now = datetime.now()
            day_delta = self.service_name_day.currentIndex() - now.weekday()
            if day_delta < 0:
                day_delta += 7
            time = now + timedelta(days=day_delta)
            local_time = time.replace(
                hour=self.service_name_time.time().hour(),
                minute=self.service_name_time.time().minute()
            )
        try:
            service_name_example = format_time(unicode(self.service_name_edit.text()), local_time)
        except ValueError:
            preset_is_valid = False
            service_name_example = translate('OpenLP.AdvancedTab', 'Syntax error.')
        return preset_is_valid, service_name_example

    def update_service_name_example(self, returned_value):
        """
        Update the example service name.
        """
        if not self.should_update_service_name_example:
            return
        name_example = self.generate_service_name_example()[1]
        self.service_name_example.setText(name_example)

    def on_service_name_day_changed(self, service_day):
        """
        React to the day of the service name changing.
        """
        self.service_name_time.setEnabled(service_day is not 7)
        self.update_service_name_example(None)

    def on_service_name_revert_button_clicked(self):
        """
        Revert to the default service name.
        """
        self.service_name_edit.setText(UiStrings().DefaultServiceName)
        self.service_name_edit.setFocus()

    def on_default_color_button_clicked(self):
        """
        Select the background colour of the default display screen.
        """
        new_color = QtGui.QColorDialog.getColor(
            QtGui.QColor(self.default_color), self)
        if new_color.isValid():
            self.default_color = new_color.name()
            self.default_color_button.setStyleSheet(u'background-color: %s' % self.default_color)

    def on_default_browse_button_clicked(self):
        """
        Select an image for the default display screen.
        """
        file_filters = u'%s;;%s (*.*) (*)' % (get_images_filter(), UiStrings().AllFiles)
        filename = QtGui.QFileDialog.getOpenFileName(self,
            translate('OpenLP.AdvancedTab', 'Open File'), '', file_filters)
        if filename:
            self.default_file_edit.setText(filename)
        self.default_file_edit.setFocus()

    def on_data_directory_browse_button_clicked(self):
        """
        Browse for a new data directory location.
        """
        old_root_path = unicode(self.data_directory_label.text())
        # Get the new directory location.
        new_data_path = QtGui.QFileDialog.getExistingDirectory(
            self, translate('OpenLP.AdvancedTab', 'Select Data Directory Location'), old_root_path,
            options=QtGui.QFileDialog.ShowDirsOnly)
        # Set the new data path.
        if new_data_path:
            new_data_path = os.path.normpath(new_data_path)
            if self.current_data_path.lower() == new_data_path.lower():
                self.on_data_directory_cancel_button_clicked()
                return
        else:
            return
        # Make sure they want to change the data.
        answer = QtGui.QMessageBox.question(self,
            translate('OpenLP.AdvancedTab', 'Confirm Data Directory Change'),
            translate('OpenLP.AdvancedTab', 'Are you sure you want to change the location of the OpenLP '
                'data directory to:\n\n%s\n\n '
                'The data directory will be changed when OpenLP is closed.').replace('%s', new_data_path),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No), QtGui.QMessageBox.No)
        if answer != QtGui.QMessageBox.Yes:
            return
        # Check if data already exists here.
        self.check_data_overwrite(new_data_path)
        # Save the new location.
        Receiver.send_message(u'set_new_data_path', new_data_path)
        self.new_data_directory_edit.setText(new_data_path)
        self.data_directory_cancel_button.show()

    def on_data_directory_default_button_clicked(self):
        """
        Re-set the data directory location to the 'default' location.
        """
        new_data_path = AppLocation.get_directory(AppLocation.DataDir)
        if self.current_data_path.lower() != new_data_path.lower():
            # Make sure they want to change the data location back to the
            # default.
            answer = QtGui.QMessageBox.question(self,
                translate('OpenLP.AdvancedTab', 'Reset Data Directory'),
                translate('OpenLP.AdvancedTab', 'Are you sure you want to change the location of the OpenLP '
                'data directory to the default location?\n\nThis location will be used after OpenLP is closed.'),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No), QtGui.QMessageBox.No)
            if answer != QtGui.QMessageBox.Yes:
                return
            self.check_data_overwrite(new_data_path)
            # Save the new location.
            Receiver.send_message(u'set_new_data_path', new_data_path)
            self.new_data_directory_edit.setText(os.path.abspath(new_data_path))
            self.data_directory_cancel_button.show()
        else:
            # We cancel the change in case user changed their mind.
            self.on_data_directory_cancel_button_clicked()

    def on_data_directory_copy_check_box_toggled(self):
        """
        Copy existing data when you change your data directory.
        """
        Receiver.send_message(u'set_copy_data',
            self.data_directory_copy_check_box.isChecked())
        if self.data_exists:
            if self.data_directory_copy_check_box.isChecked():
                self.new_data_directory_has_files_label.show()
            else:
                self.new_data_directory_has_files_label.hide()

    def check_data_overwrite(self, data_path ):
        """
        Check if there's already data in the target directory.
        """
        test_path = os.path.join(data_path, u'songs')
        self.data_directory_copy_check_box.show()
        if os.path.exists(test_path):
            self.data_exists = True
            # Check is they want to replace existing data.
            answer = QtGui.QMessageBox.warning(self,
                translate('OpenLP.AdvancedTab', 'Overwrite Existing Data'),
                translate('OpenLP.AdvancedTab', 'WARNING: \n\nThe location you have selected \n\n%s\n\n'
                'appears to contain OpenLP data files. Do you wish to replace these files with the current data files?'
                ).replace('%s', os.path.abspath(data_path,)),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No), QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes:
                self.data_directory_copy_check_box.setChecked(True)
                self.new_data_directory_has_files_label.show()
            else:
                self.data_directory_copy_check_box.setChecked(False)
                self.new_data_directory_has_files_label.hide()
        else:
            self.data_exists = False
            self.data_directory_copy_check_box.setChecked(True)
            self.new_data_directory_has_files_label.hide()

    def on_data_directory_cancel_button_clicked(self):
        """
        Cancel the data directory location change
        """
        self.new_data_directory_edit.clear()
        self.data_directory_copy_check_box.setChecked(False)
        Receiver.send_message(u'set_new_data_path', u'')
        Receiver.send_message(u'set_copy_data', False)
        self.data_directory_copy_check_box.hide()
        self.data_directory_cancel_button.hide()
        self.new_data_directory_has_files_label.hide()

    def on_default_revert_button_clicked(self):
        """
        Revert the default screen back to the default settings.
        """
        self.default_file_edit.setText(u':/graphics/openlp-splash-screen.png')
        self.default_file_edit.setFocus()

    def on_X11_bypass_check_box_toggled(self, checked):
        """
        Toggle X11 bypass flag on maindisplay depending on check box state.

        ``checked``
            The state of the check box (boolean).
        """
        self.display_changed = True

    def on_alternate_rows_check_box_toggled(self, checked):
        """
        Notify user about required restart.

        ``checked``
            The state of the check box (boolean).
        """
        QtGui.QMessageBox.information(self,
            translate('OpenLP.AdvancedTab', 'Restart Required'),
            translate('OpenLP.AdvancedTab', 'This change will only take effect once OpenLP has been restarted.'))

    def on_end_slide_button_clicked(self):
        """
        Stop at the end either top ot bottom
        """
        self.slide_limits = SlideLimits.End

    def on_wrap_slide_button_clicked(self):
        """
        Wrap round the service item
        """
        self.slide_limits = SlideLimits.Wrap

    def on_next_item_button_clicked(self):
        """
        Advance to the next service item
        """
        self.slide_limits = SlideLimits.Next
