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
The :mod:`slidecontroller` module contains the most important part of OpenLP - the slide controller
"""

import os
import logging
import copy
from collections import deque

from PyQt4 import QtCore, QtGui

from openlp.core.lib import OpenLPToolbar, ItemCapabilities, ServiceItem, ImageSource, SlideLimits, \
    ServiceItemAction, Settings, Registry, UiStrings, ScreenList, build_icon, build_html, translate
from openlp.core.ui import HideMode, MainDisplay, Display, DisplayControllerType
from openlp.core.lib.ui import create_action
from openlp.core.utils.actions import ActionList, CategoryOrder
from openlp.core.ui.listpreviewwidget import ListPreviewWidget

log = logging.getLogger(__name__)

# Threshold which has to be trespassed to toggle.
HIDE_MENU_THRESHOLD  = 27
AUDIO_TIME_LABEL_STYLESHEET = 'background-color: palette(background); ' \
    'border-top-color: palette(shadow); ' \
    'border-left-color: palette(shadow); ' \
    'border-bottom-color: palette(light); ' \
    'border-right-color: palette(light); ' \
    'border-radius: 3px; border-style: inset; ' \
    'border-width: 1; font-family: monospace; margin: 2px;'


class DisplayController(QtGui.QWidget):
    """
    Controller is a general display controller widget.
    """
    def __init__(self, parent, is_live=False):
        """
        Set up the general Controller.
        """
        super(DisplayController, self).__init__(parent)
        self.is_live = is_live
        self.display = None
        self.controller_type = DisplayControllerType.Plugin

    def send_to_plugins(self, *args):
        """
        This is the generic function to send signal for control widgets,
        created from within other plugins
        This function is needed to catch the current controller
        """
        sender = self.sender().objectName() if self.sender().objectName() else self.sender().text()
        controller = self
        Registry().execute('%s' % sender, [controller, args])


class SlideController(DisplayController):
    """
    SlideController is the slide controller widget. This widget is what the
    user uses to control the displaying of verses/slides/etc on the screen.
    """
    def __init__(self, parent, is_live=False):
        """
        Set up the Slide Controller.
        """
        super(SlideController, self).__init__(parent, is_live)
        Registry().register_function('bootstrap_post_set_up', self.screen_size_changed)
        self.screens = ScreenList()
        try:
            self.ratio = self.screens.current['size'].width() / self.screens.current['size'].height()
        except ZeroDivisionError:
            self.ratio = 1
        self.loop_list = [
            'play_slides_menu',
            'loop_separator',
            'delay_spin_box'
        ]
        # audioPauseItem is also in Settings so any changes need to be paired
        self.audio_list = [
            'audioPauseItem',
            'audio_time_label'
        ]
        self.wide_menu = [
            'blank_screen_button',
            'theme_screen_button',
            'desktop_screen_button'
        ]
        self.narrow_menu = [
            'hide_menu'
        ]
        self.timer_id = 0
        self.song_edit = False
        self.selected_row = 0
        self.service_item = None
        self.slide_limits = None
        self.update_slide_limits()
        self.panel = QtGui.QWidget(parent.control_splitter)
        self.slideList = {}
        self.slide_count = 0
        self.slide_image = None
        # Layout for holding panel
        self.panel_layout = QtGui.QVBoxLayout(self.panel)
        self.panel_layout.setSpacing(0)
        self.panel_layout.setMargin(0)
        # Type label for the top of the slide controller
        self.type_label = QtGui.QLabel(self.panel)
        if self.is_live:
            Registry().register('live_controller', self)
            self.type_label.setText(UiStrings().Live)
            self.split = 1
            self.type_prefix = 'live'
            self.keypress_queue = deque()
            self.keypress_loop = False
            self.category = UiStrings().LiveToolbar
            ActionList.get_instance().add_category(str(self.category), CategoryOrder.standard_toolbar)
        else:
            Registry().register('preview_controller', self)
            self.type_label.setText(UiStrings().Preview)
            self.split = 0
            self.type_prefix = 'preview'
            self.category = None
        self.type_label.setStyleSheet('font-weight: bold; font-size: 12pt;')
        self.type_label.setAlignment(QtCore.Qt.AlignCenter)
        self.panel_layout.addWidget(self.type_label)
        # Splitter
        self.splitter = QtGui.QSplitter(self.panel)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.panel_layout.addWidget(self.splitter)
        # Actual controller section
        self.controller = QtGui.QWidget(self.splitter)
        self.controller.setGeometry(QtCore.QRect(0, 0, 100, 536))
        self.controller.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum))
        self.controller_layout = QtGui.QVBoxLayout(self.controller)
        self.controller_layout.setSpacing(0)
        self.controller_layout.setMargin(0)
        # Controller list view
        self.preview_widget = ListPreviewWidget(self, self.ratio)
        self.controller_layout.addWidget(self.preview_widget)
        # Build the full toolbar
        self.toolbar = OpenLPToolbar(self)
        size_toolbar_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        size_toolbar_policy.setHorizontalStretch(0)
        size_toolbar_policy.setVerticalStretch(0)
        size_toolbar_policy.setHeightForWidth(self.toolbar.sizePolicy().hasHeightForWidth())
        self.toolbar.setSizePolicy(size_toolbar_policy)
        self.previous_item = create_action(self, 'previousItem_' + self.type_prefix,
            text=translate('OpenLP.SlideController', 'Previous Slide'), icon=':/slides/slide_previous.png',
            tooltip=translate('OpenLP.SlideController', 'Move to previous.'),
            can_shortcuts=True, context=QtCore.Qt.WidgetWithChildrenShortcut,
            category=self.category, triggers=self.on_slide_selected_previous)
        self.toolbar.addAction(self.previous_item)
        self.nextItem = create_action(self, 'nextItem_' + self.type_prefix,
            text=translate('OpenLP.SlideController', 'Next Slide'), icon=':/slides/slide_next.png',
            tooltip=translate('OpenLP.SlideController', 'Move to next.'),
            can_shortcuts=True, context=QtCore.Qt.WidgetWithChildrenShortcut,
            category=self.category, triggers=self.on_slide_selected_next_action)
        self.toolbar.addAction(self.nextItem)
        self.toolbar.addSeparator()
        self.controller_type = DisplayControllerType.Preview
        if self.is_live:
            self.controller_type = DisplayControllerType.Live
            # Hide Menu
            self.hide_menu = QtGui.QToolButton(self.toolbar)
            self.hide_menu.setObjectName('hide_menu')
            self.hide_menu.setText(translate('OpenLP.SlideController', 'Hide'))
            self.hide_menu.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
            self.hide_menu.setMenu(QtGui.QMenu(translate('OpenLP.SlideController', 'Hide'), self.toolbar))
            self.toolbar.add_toolbar_widget(self.hide_menu)
            self.blank_screen = create_action(self, 'blankScreen',
                text=translate('OpenLP.SlideController', 'Blank Screen'), icon=':/slides/slide_blank.png',
                checked=False, can_shortcuts=True, category=self.category, triggers=self.on_blank_display)
            self.theme_screen = create_action(self, 'themeScreen',
                text=translate('OpenLP.SlideController', 'Blank to Theme'), icon=':/slides/slide_theme.png',
                checked=False, can_shortcuts=True, category=self.category,
                triggers=self.on_theme_display)
            self.desktop_screen = create_action(self, 'desktopScreen',
                text=translate('OpenLP.SlideController', 'Show Desktop'), icon=':/slides/slide_desktop.png',
                checked=False, can_shortcuts=True, category=self.category,
                triggers=self.on_hide_display)
            self.hide_menu.setDefaultAction(self.blank_screen)
            self.hide_menu.menu().addAction(self.blank_screen)
            self.hide_menu.menu().addAction(self.theme_screen)
            self.hide_menu.menu().addAction(self.desktop_screen)
            # Wide menu of display control buttons.
            self.blank_screen_button = QtGui.QToolButton(self.toolbar)
            self.blank_screen_button.setObjectName('blank_screen_button')
            self.toolbar.add_toolbar_widget(self.blank_screen_button)
            self.blank_screen_button.setDefaultAction(self.blank_screen)
            self.theme_screen_button = QtGui.QToolButton(self.toolbar)
            self.theme_screen_button.setObjectName('theme_screen_button')
            self.toolbar.add_toolbar_widget(self.theme_screen_button)
            self.theme_screen_button.setDefaultAction(self.theme_screen)
            self.desktop_screen_button = QtGui.QToolButton(self.toolbar)
            self.desktop_screen_button.setObjectName('desktop_screen_button')
            self.toolbar.add_toolbar_widget(self.desktop_screen_button)
            self.desktop_screen_button.setDefaultAction(self.desktop_screen)
            self.toolbar.add_toolbar_action('loop_separator', separator=True)
            # Play Slides Menu
            self.play_slides_menu = QtGui.QToolButton(self.toolbar)
            self.play_slides_menu.setObjectName('play_slides_menu')
            self.play_slides_menu.setText(translate('OpenLP.SlideController', 'Play Slides'))
            self.play_slides_menu.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
            self.play_slides_menu.setMenu(QtGui.QMenu(translate('OpenLP.SlideController', 'Play Slides'), self.toolbar))
            self.toolbar.add_toolbar_widget(self.play_slides_menu)
            self.play_slides_loop = create_action(self, 'playSlidesLoop', text=UiStrings().PlaySlidesInLoop,
                icon=':/media/media_time.png', checked=False, can_shortcuts=True,
                category=self.category, triggers=self.on_play_slides_loop)
            self.play_slides_once = create_action(self, 'playSlidesOnce', text=UiStrings().PlaySlidesToEnd,
                icon=':/media/media_time.png', checked=False, can_shortcuts=True,
                category=self.category, triggers=self.on_play_slides_once)
            if Settings().value(self.main_window.advanced_settings_section + '/slide limits') == SlideLimits.Wrap:
                self.play_slides_menu.setDefaultAction(self.play_slides_loop)
            else:
                self.play_slides_menu.setDefaultAction(self.play_slides_once)
            self.play_slides_menu.menu().addAction(self.play_slides_loop)
            self.play_slides_menu.menu().addAction(self.play_slides_once)
            # Loop Delay Spinbox
            self.delay_spin_box = QtGui.QSpinBox()
            self.delay_spin_box.setObjectName('delay_spin_box')
            self.delay_spin_box.setRange(1, 180)
            self.delay_spin_box.setSuffix(UiStrings().Seconds)
            self.delay_spin_box.setToolTip(translate('OpenLP.SlideController', 'Delay between slides in seconds.'))
            self.toolbar.add_toolbar_widget(self.delay_spin_box)
        else:
            self.toolbar.add_toolbar_action('goLive', icon=':/general/general_live.png',
                tooltip=translate('OpenLP.SlideController', 'Move to live.'), triggers=self.on_go_live)
            self.toolbar.add_toolbar_action('addToService', icon=':/general/general_add.png',
                tooltip=translate('OpenLP.SlideController', 'Add to Service.'), triggers=self.on_preview_add_to_service)
            self.toolbar.addSeparator()
            self.toolbar.add_toolbar_action('editSong', icon=':/general/general_edit.png',
                tooltip=translate('OpenLP.SlideController', 'Edit and reload song preview.'), triggers=self.on_edit_song)
        self.controller_layout.addWidget(self.toolbar)
        # Build the Media Toolbar
        self.media_controller.register_controller(self)
        if self.is_live:
            # Build the Song Toolbar
            self.song_menu = QtGui.QToolButton(self.toolbar)
            self.song_menu.setObjectName('song_menu')
            self.song_menu.setText(translate('OpenLP.SlideController', 'Go To'))
            self.song_menu.setPopupMode(QtGui.QToolButton.InstantPopup)
            self.song_menu.setMenu(QtGui.QMenu(translate('OpenLP.SlideController', 'Go To'), self.toolbar))
            self.toolbar.add_toolbar_widget(self.song_menu)
            # Stuff for items with background audio.
            # FIXME: object name should be changed. But this requires that we migrate the shortcut.
            self.audio_pause_item = self.toolbar.add_toolbar_action('audioPauseItem',
                icon=':/slides/media_playback_pause.png', text=translate('OpenLP.SlideController', 'Pause Audio'),
                tooltip=translate('OpenLP.SlideController', 'Pause audio.'),
                checked=False, visible=False, category=self.category, context=QtCore.Qt.WindowShortcut,
                can_shortcuts=True, triggers=self.set_audio_pause_clicked)
            self.audio_menu = QtGui.QMenu(translate('OpenLP.SlideController', 'Background Audio'), self.toolbar)
            self.audio_pause_item.setMenu(self.audio_menu)
            self.audio_pause_item.setParent(self.toolbar)
            self.toolbar.widgetForAction(self.audio_pause_item).setPopupMode(
                QtGui.QToolButton.MenuButtonPopup)
            self.nextTrackItem = create_action(self, 'nextTrackItem', text=UiStrings().NextTrack,
                icon=':/slides/media_playback_next.png',
                tooltip=translate('OpenLP.SlideController', 'Go to next audio track.'),
                category=self.category, can_shortcuts=True, triggers=self.on_next_track_clicked)
            self.audio_menu.addAction(self.nextTrackItem)
            self.trackMenu = self.audio_menu.addMenu(translate('OpenLP.SlideController', 'Tracks'))
            self.audio_time_label = QtGui.QLabel(' 00:00 ', self.toolbar)
            self.audio_time_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
            self.audio_time_label.setStyleSheet(AUDIO_TIME_LABEL_STYLESHEET)
            self.audio_time_label.setObjectName('audio_time_label')
            self.toolbar.add_toolbar_widget(self.audio_time_label)
            self.toolbar.set_widget_visible(self.audio_list, False)
            self.toolbar.set_widget_visible(['song_menu'], False)
        # Screen preview area
        self.preview_frame = QtGui.QFrame(self.splitter)
        self.preview_frame.setGeometry(QtCore.QRect(0, 0, 300, 300 * self.ratio))
        self.preview_frame.setMinimumHeight(100)
        self.preview_frame.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored,
            QtGui.QSizePolicy.Label))
        self.preview_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.preview_frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.preview_frame.setObjectName('preview_frame')
        self.grid = QtGui.QGridLayout(self.preview_frame)
        self.grid.setMargin(8)
        self.grid.setObjectName('grid')
        self.slide_layout = QtGui.QVBoxLayout()
        self.slide_layout.setSpacing(0)
        self.slide_layout.setMargin(0)
        self.slide_layout.setObjectName('SlideLayout')
        self.preview_display = Display(self, self.is_live, self)
        self.preview_display.setGeometry(QtCore.QRect(0, 0, 300, 300))
        self.preview_display.screen = {'size': self.preview_display.geometry()}
        self.preview_display.setup()
        self.slide_layout.insertWidget(0, self.preview_display)
        self.preview_display.hide()
        # Actual preview screen
        self.slide_preview = QtGui.QLabel(self)
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.slide_preview.sizePolicy().hasHeightForWidth())
        self.slide_preview.setSizePolicy(size_policy)
        self.slide_preview.setFrameShape(QtGui.QFrame.Box)
        self.slide_preview.setFrameShadow(QtGui.QFrame.Plain)
        self.slide_preview.setLineWidth(1)
        self.slide_preview.setScaledContents(True)
        self.slide_preview.setObjectName('slide_preview')
        self.slide_layout.insertWidget(0, self.slide_preview)
        self.grid.addLayout(self.slide_layout, 0, 0, 1, 1)
        if self.is_live:
            self.current_shortcut = ''
            self.shortcutTimer = QtCore.QTimer()
            self.shortcutTimer.setObjectName('shortcutTimer')
            self.shortcutTimer.setSingleShot(True)
            shortcuts = [
                {'key': 'V', 'configurable': True, 'text': translate('OpenLP.SlideController', 'Go to "Verse"')},
                {'key': 'C', 'configurable': True, 'text': translate('OpenLP.SlideController', 'Go to "Chorus"')},
                {'key': 'B', 'configurable': True, 'text': translate('OpenLP.SlideController', 'Go to "Bridge"')},
                {'key': 'P', 'configurable': True,
                    'text': translate('OpenLP.SlideController', 'Go to "Pre-Chorus"')},
                {'key': 'I', 'configurable': True, 'text': translate('OpenLP.SlideController', 'Go to "Intro"')},
                {'key': 'E', 'configurable': True, 'text': translate('OpenLP.SlideController', 'Go to "Ending"')},
                {'key': 'O', 'configurable': True, 'text': translate('OpenLP.SlideController', 'Go to "Other"')}
            ]
            shortcuts.extend([{'key': str(number)} for number in range(10)])
            self.controller.addActions([create_action(self,
                'shortcutAction_%s' % s['key'], text=s.get('text'),
                can_shortcuts=True,
                context=QtCore.Qt.WidgetWithChildrenShortcut,
                category=self.category if s.get('configurable') else None,
                triggers=self._slide_shortcut_activated) for s in shortcuts])
            self.shortcutTimer.timeout.connect(self._slide_shortcut_activated)
        # Signals
        self.preview_widget.clicked.connect(self.on_slide_selected)
        if self.is_live:
            # Need to use event as called across threads and UI is updated
            QtCore.QObject.connect(self, QtCore.SIGNAL('slidecontroller_toggle_display'), self.toggle_display)
            Registry().register_function('slidecontroller_live_spin_delay', self.receive_spin_delay)
            self.toolbar.set_widget_visible(self.loop_list, False)
            self.toolbar.set_widget_visible(self.wide_menu, False)
        else:
            self.preview_widget.doubleClicked.connect(self.on_preview_add_to_service)
            self.toolbar.set_widget_visible(['editSong'], False)
        if self.is_live:
            self.set_live_hotkeys(self)
            self.__add_actions_to_widget(self.controller)
        else:
            self.controller.addActions([self.nextItem, self.previous_item])
        Registry().register_function('slidecontroller_%s_stop_loop' % self.type_prefix, self.on_stop_loop)
        Registry().register_function('slidecontroller_%s_change' % self.type_prefix, self.on_slide_change)
        Registry().register_function('slidecontroller_%s_blank' % self.type_prefix, self.on_slide_blank)
        Registry().register_function('slidecontroller_%s_unblank' % self.type_prefix, self.on_slide_unblank)
        Registry().register_function('slidecontroller_update_slide_limits', self.update_slide_limits)
        QtCore.QObject.connect(self, QtCore.SIGNAL('slidecontroller_%s_set' % self.type_prefix),
            self.on_slide_selected_index)
        QtCore.QObject.connect(self, QtCore.SIGNAL('slidecontroller_%s_next' % self.type_prefix),
            self.on_slide_selected_next)
        QtCore.QObject.connect(self, QtCore.SIGNAL('slidecontroller_%s_previous' % self.type_prefix),
            self.on_slide_selected_previous)

    def _slide_shortcut_activated(self):
        """
        Called, when a shortcut has been activated to jump to a chorus, verse,
        etc.

        **Note**: This implementation is based on shortcuts. But it rather works
        like "key sequenes". You have to press one key after the other and
        **not** at the same time.
        For example to jump to "V3" you have to press "V" and afterwards but
        within a time frame of 350ms you have to press "3".
        """
        try:
            from openlp.plugins.songs.lib import VerseType
            SONGS_PLUGIN_AVAILABLE = True
        except ImportError:
            SONGS_PLUGIN_AVAILABLE = False
        sender_name = self.sender().objectName()
        verse_type = sender_name[15:] if sender_name[:15] == 'shortcutAction_' else ''
        if SONGS_PLUGIN_AVAILABLE:
            if verse_type == 'V':
                self.current_shortcut = VerseType.translated_tags[VerseType.Verse]
            elif verse_type == 'C':
                self.current_shortcut = VerseType.translated_tags[VerseType.Chorus]
            elif verse_type == 'B':
                self.current_shortcut = VerseType.translated_tags[VerseType.Bridge]
            elif verse_type == 'P':
                self.current_shortcut = VerseType.translated_tags[VerseType.PreChorus]
            elif verse_type == 'I':
                self.current_shortcut = VerseType.translated_tags[VerseType.Intro]
            elif verse_type == 'E':
                self.current_shortcut = VerseType.translated_tags[VerseType.Ending]
            elif verse_type == 'O':
                self.current_shortcut = VerseType.translated_tags[VerseType.Other]
            elif verse_type.isnumeric():
                self.current_shortcut += verse_type
            self.current_shortcut = self.current_shortcut.upper()
        elif verse_type.isnumeric():
            self.current_shortcut += verse_type
        elif verse_type:
            self.current_shortcut = verse_type
        keys = list(self.slideList.keys())
        matches = [match for match in keys
            if match.startswith(self.current_shortcut)]
        if len(matches) == 1:
            self.shortcutTimer.stop()
            self.current_shortcut = ''
            self.preview_widget.change_slide(self.slideList[matches[0]])
            self.slide_selected()
        elif sender_name != 'shortcutTimer':
            # Start the time as we did not have any match.
            self.shortcutTimer.start(350)
        else:
            # The timer timed out.
            if self.current_shortcut in keys:
                # We had more than one match for example "V1" and "V10", but
                # "V1" was the slide we wanted to go.
                self.preview_widget.change_slide(self.slideList[self.current_shortcut])
                self.slide_selected()
           # Reset the shortcut.
            self.current_shortcut = ''

    def set_live_hotkeys(self, parent=None):
        """
        Set the live hotkeys
        """
        self.previousService = create_action(parent, 'previousService',
            text=translate('OpenLP.SlideController', 'Previous Service'),
            can_shortcuts=True, context=QtCore.Qt.WidgetWithChildrenShortcut, category=self.category,
            triggers=self.service_previous)
        self.nextService = create_action(parent, 'nextService',
            text=translate('OpenLP.SlideController', 'Next Service'),
            can_shortcuts=True, context=QtCore.Qt.WidgetWithChildrenShortcut, category=self.category,
            triggers=self.service_next)
        self.escapeItem = create_action(parent, 'escapeItem',
            text=translate('OpenLP.SlideController', 'Escape Item'),
            can_shortcuts=True, context=QtCore.Qt.WidgetWithChildrenShortcut, category=self.category,
            triggers=self.live_escape)

    def live_escape(self):
        """
        If you press ESC on the live screen it should close the display temporarily.
        """
        self.display.setVisible(False)
        self.media_controller.media_stop(self)

    def toggle_display(self, action):
        """
        Toggle the display settings triggered from remote messages.
        """
        if action == 'blank' or action == 'hide':
            self.on_blank_display(True)
        elif action == 'theme':
            self.on_theme_display(True)
        elif action == 'desktop':
            self.on_hide_display(True)
        elif action == 'show':
            self.on_blank_display(False)
            self.on_theme_display(False)
            self.on_hide_display(False)

    def service_previous(self):
        """
        Live event to select the previous service item from the service manager.
        """
        self.keypress_queue.append(ServiceItemAction.Previous)
        self._process_queue()

    def service_next(self):
        """
        Live event to select the next service item from the service manager.
        """
        self.keypress_queue.append(ServiceItemAction.Next)
        self._process_queue()

    def _process_queue(self):
        """
        Process the service item request queue.  The key presses can arrive
        faster than the processing so implement a FIFO queue.
        """
        if self.keypress_queue:
            while len(self.keypress_queue) and not self.keypress_loop:
                self.keypress_loop = True
                keypressCommand = self.keypress_queue.popleft()
                if keypressCommand == ServiceItemAction.Previous:
                    self.service_manager.previous_item()
                elif keypressCommand == ServiceItemAction.PreviousLastSlide:
                    # Go to the last slide of the previous item
                    self.service_manager.previous_item(last_slide=True)
                else:
                    self.service_manager.next_item()
            self.keypress_loop = False

    def screen_size_changed(self):
        """
        Settings dialog has changed the screen size of adjust output and screen previews.
        """
        # rebuild display as screen size changed
        if self.display:
            self.display.close()
        self.display = MainDisplay(self, self.is_live, self)
        self.display.setup()
        if self.is_live:
            self.__add_actions_to_widget(self.display)
            self.display.audio_player.connectSlot(QtCore.SIGNAL('tick(qint64)'), self.on_audio_time_remaining)
        # The SlidePreview's ratio.
        try:
            self.ratio = self.screens.current['size'].width() / self.screens.current['size'].height()
        except ZeroDivisionError:
            self.ratio = 1
        self.media_controller.setup_display(self.display, False)
        self.preview_size_changed()
        self.preview_widget.screen_size_changed(self.ratio)
        self.preview_display.setup()
        service_item = ServiceItem()
        self.preview_display.web_view.setHtml(build_html(service_item, self.preview_display.screen, None, self.is_live,
            plugins=self.plugin_manager.plugins))
        self.media_controller.setup_display(self.preview_display, True)
        if self.service_item:
            self.refresh_service_item()

    def __add_actions_to_widget(self, widget):
        """
        Add actions to the widget specified by `widget`
        """
        widget.addActions([
            self.previous_item, self.nextItem,
            self.previousService, self.nextService,
            self.escapeItem])

    def preview_size_changed(self):
        """
        Takes care of the SlidePreview's size. Is called when one of the the
        splitters is moved or when the screen size is changed. Note, that this
        method is (also) called frequently from the mainwindow *paintEvent*.
        """
        if self.ratio < self.preview_frame.width() / self.preview_frame.height():
            # We have to take the height as limit.
            max_height = self.preview_frame.height() - self.grid.margin() * 2
            self.slide_preview.setFixedSize(QtCore.QSize(max_height * self.ratio, max_height))
            self.preview_display.setFixedSize(QtCore.QSize(max_height * self.ratio, max_height))
            self.preview_display.screen = {
                'size': self.preview_display.geometry()}
        else:
            # We have to take the width as limit.
            max_width = self.preview_frame.width() - self.grid.margin() * 2
            self.slide_preview.setFixedSize(QtCore.QSize(max_width, max_width / self.ratio))
            self.preview_display.setFixedSize(QtCore.QSize(max_width, max_width / self.ratio))
            self.preview_display.screen = {'size': self.preview_display.geometry()}
        self.on_controller_size_changed(self.controller.width())

    def on_controller_size_changed(self, width):
        """
        Change layout of display control buttons on controller size change
        """
        if self.is_live:
            # Space used by the toolbar.
            used_space = self.toolbar.size().width() + self.hide_menu.size().width()
            # Add the threshold to prevent flickering.
            if width > used_space + HIDE_MENU_THRESHOLD and self.hide_menu.isVisible():
                self.toolbar.set_widget_visible(self.narrow_menu, False)
                self.toolbar.set_widget_visible(self.wide_menu)
            # Take away a threshold to prevent flickering.
            elif width < used_space - HIDE_MENU_THRESHOLD and not self.hide_menu.isVisible():
                self.toolbar.set_widget_visible(self.wide_menu, False)
                self.toolbar.set_widget_visible(self.narrow_menu)

    def on_song_bar_handler(self):
        """
        Some song handler
        """
        request = self.sender().text()
        slide_no = self.slideList[request]
        width = self.main_window.control_splitter.sizes()[self.split]
        self.preview_widget.replace_service_item(self.service_item, width, slide_no)
        self.slide_selected()

    def receive_spin_delay(self):
        """
        Adjusts the value of the ``delay_spin_box`` to the given one.
        """
        self.delay_spin_box.setValue(Settings().value('core/loop delay'))

    def update_slide_limits(self):
        """
        Updates the Slide Limits variable from the settings.
        """
        self.slide_limits = Settings().value(self.main_window.advanced_settings_section + '/slide limits')

    def enable_tool_bar(self, item):
        """
        Allows the toolbars to be reconfigured based on Controller Type and ServiceItem Type
        """
        if self.is_live:
            self.enable_live_tool_bar(item)
        else:
            self.enable_preview_tool_bar(item)

    def enable_live_tool_bar(self, item):
        """
        Allows the live toolbar to be customised
        """
        # Work-around for OS X, hide and then show the toolbar
        # See bug #791050
        self.toolbar.hide()
        self.mediabar.hide()
        self.song_menu.hide()
        self.toolbar.set_widget_visible(self.loop_list, False)
        self.toolbar.set_widget_visible(['song_menu'], False)
        # Reset the button
        self.play_slides_once.setChecked(False)
        self.play_slides_once.setIcon(build_icon(':/media/media_time.png'))
        self.play_slides_loop.setChecked(False)
        self.play_slides_loop.setIcon(build_icon(':/media/media_time.png'))
        if item.is_text():
            if Settings().value(self.main_window.songs_settings_section + '/display songbar') and self.slideList:
                self.toolbar.set_widget_visible(['song_menu'], True)
        if item.is_capable(ItemCapabilities.CanLoop) and len(item.get_frames()) > 1:
            self.toolbar.set_widget_visible(self.loop_list)
        if item.is_media():
            self.mediabar.show()
        self.previous_item.setVisible(not item.is_media())
        self.nextItem.setVisible(not item.is_media())
        # Work-around for OS X, hide and then show the toolbar
        # See bug #791050
        self.toolbar.show()

    def enable_preview_tool_bar(self, item):
        """
        Allows the Preview toolbar to be customised
        """
        # Work-around for OS X, hide and then show the toolbar
        # See bug #791050
        self.toolbar.hide()
        self.mediabar.hide()
        self.toolbar.set_widget_visible(['editSong'], False)
        if item.is_capable(ItemCapabilities.CanEdit) and item.from_plugin:
            self.toolbar.set_widget_visible(['editSong'])
        elif item.is_media():
            self.mediabar.show()
        self.previous_item.setVisible(not item.is_media())
        self.nextItem.setVisible(not item.is_media())
        # Work-around for OS X, hide and then show the toolbar
        # See bug #791050
        self.toolbar.show()

    def refresh_service_item(self):
        """
        Method to update the service item if the screen has changed
        """
        log.debug('refresh_service_item live = %s' % self.is_live)
        if self.service_item.is_text() or self.service_item.is_image():
            item = self.service_item
            item.render()
            self._process_item(item, self.selected_row)

    def add_service_item(self, item):
        """
        Method to install the service item into the controller
        Called by plugins
        """
        log.debug('add_service_item live = %s' % self.is_live)
        item.render()
        slide_no = 0
        if self.song_edit:
            slide_no = self.selected_row
        self.song_edit = False
        self._process_item(item, slide_no)

    def replace_service_manager_item(self, item):
        """
        Replacement item following a remote edit
        """
        if item == self.service_item:
            self._process_item(item, self.preview_widget.current_slide_number())

    def add_service_manager_item(self, item, slide_no):
        """
        Method to install the service item into the controller and request the correct toolbar for the plugin. Called by
        :class:`~openlp.core.ui.ServiceManager`
        """
        log.debug('add_service_manager_item live = %s' % self.is_live)
        # If no valid slide number is specified we take the first one, but we remember the initial value to see if we
        # should reload the song or not
        slidenum = slide_no
        if slide_no == -1:
            slidenum = 0
        # If service item is the same as the current one, only change slide
        if slide_no >= 0 and item == self.service_item:
            self.preview_widget.change_slide(slidenum)
            self.slide_selected()
        else:
            self._process_item(item, slidenum)
            if self.is_live and item.auto_play_slides_loop and item.timed_slide_interval > 0:
                self.play_slides_loop.setChecked(item.auto_play_slides_loop)
                self.delay_spin_box.setValue(int(item.timed_slide_interval))
                self.on_play_slides_loop()
            elif self.is_live and item.auto_play_slides_once and item.timed_slide_interval > 0:
                self.play_slides_once.setChecked(item.auto_play_slides_once)
                self.delay_spin_box.setValue(int(item.timed_slide_interval))
                self.on_play_slides_once()

    def _process_item(self, service_item, slideno):
        """
        Loads a ServiceItem into the system from ServiceManager. Display the slide number passed.
        """
        log.debug('processManagerItem live = %s' % self.is_live)
        self.on_stop_loop()
        old_item = self.service_item
        # take a copy not a link to the servicemanager copy.
        self.service_item = copy.copy(service_item)
        if old_item and self.is_live and old_item.is_capable(ItemCapabilities.ProvidesOwnDisplay):
            self._reset_blank()
        Registry().execute(
            '%s_start' % service_item.name.lower(), [service_item, self.is_live, self.hide_mode(), slideno])
        self.slideList = {}
        if self.is_live:
            self.song_menu.menu().clear()
            self.display.audio_player.reset()
            self.set_audio_items_visibility(False)
            self.audio_pause_item.setChecked(False)
            # If the current item has background audio
            if self.service_item.is_capable(ItemCapabilities.HasBackgroundAudio):
                log.debug('Starting to play...')
                self.display.audio_player.add_to_playlist(self.service_item.background_audio)
                self.trackMenu.clear()
                for counter in range(len(self.service_item.background_audio)):
                    action = self.trackMenu.addAction(os.path.basename(self.service_item.background_audio[counter]))
                    action.setData(counter)
                    action.triggered.connect(self.on_track_triggered)
                self.display.audio_player.repeat = Settings().value(
                    self.main_window.general_settings_section + '/audio repeat list')
                if Settings().value(self.main_window.general_settings_section + '/audio start paused'):
                    self.audio_pause_item.setChecked(True)
                    self.display.audio_player.pause()
                else:
                    self.display.audio_player.play()
                self.set_audio_items_visibility(True)
        row = 0
        width = self.main_window.control_splitter.sizes()[self.split]
        for framenumber, frame in enumerate(self.service_item.get_frames()):
            if self.service_item.is_text():
                if frame['verseTag']:
                    # These tags are already translated.
                    verse_def = frame['verseTag']
                    verse_def = '%s%s' % (verse_def[0], verse_def[1:])
                    two_line_def = '%s\n%s' % (verse_def[0], verse_def[1:])
                    row = two_line_def
                    if verse_def not in self.slideList:
                        self.slideList[verse_def] = framenumber
                        if self.is_live:
                            self.song_menu.menu().addAction(verse_def, self.on_song_bar_handler)
                else:
                    row += 1
                    self.slideList[str(row)] = row - 1
            else:
                row += 1
                self.slideList[str(row)] = row - 1
                # If current slide set background to image
                if not self.service_item.is_command() and framenumber == slideno:
                    self.service_item.bg_image_bytes = self.image_manager.get_image_bytes(frame['path'],
                        ImageSource.ImagePlugin)
        self.preview_widget.replace_service_item(self.service_item, width, slideno)
        self.enable_tool_bar(service_item)
        # Pass to display for viewing.
        # Postpone image build, we need to do this later to avoid the theme
        # flashing on the screen
        if not self.service_item.is_image():
            self.display.build_html(self.service_item)
        if service_item.is_media():
            self.on_media_start(service_item)
        self.slide_selected(True)
        if old_item:
            # Close the old item after the new one is opened
            # This avoids the service theme/desktop flashing on screen
            # However opening a new item of the same type will automatically
            # close the previous, so make sure we don't close the new one.
            if old_item.is_command() and not service_item.is_command():
                Registry().execute('%s_stop' % old_item.name.lower(), [old_item, self.is_live])
            if old_item.is_media() and not service_item.is_media():
                self.on_media_close()
        Registry().execute('slidecontroller_%s_started' % self.type_prefix, [service_item])

    # Screen event methods
    def on_slide_selected_index(self, message):
        """
        Go to the requested slide
        """
        index = int(message[0])
        if not self.service_item:
            return
        if self.service_item.is_command():
            Registry().execute('%s_slide' % self.service_item.name.lower(), [self.service_item, self.is_live, index])
            self.update_preview()
        else:
            self.preview_widget.change_slide(index)
            self.slide_selected()

    def main_display_set_background(self):
        """
        Allow the main display to blank the main display at startup time
        """
        log.debug('main_display_set_background live = %s' % self.is_live)
        display_type = Settings().value(self.main_window.general_settings_section + '/screen blank')
        if self.screens.which_screen(self.window()) != self.screens.which_screen(self.display):
            # Order done to handle initial conversion
            if display_type == 'themed':
                self.on_theme_display(True)
            elif display_type == 'hidden':
                self.on_hide_display(True)
            elif display_type == 'blanked':
                self.on_blank_display(True)
            else:
                Registry().execute('live_display_show')
        else:
            self.live_escape()

    def on_slide_blank(self):
        """
        Handle the slidecontroller blank event
        """
        self.on_blank_display(True)

    def on_slide_unblank(self):
        """
        Handle the slidecontroller unblank event
        """
        self.on_blank_display(False)

    def on_blank_display(self, checked=None):
        """
        Handle the blank screen button actions
        """
        if checked is None:
            checked = self.blank_screen.isChecked()
        log.debug('on_blank_display %s' % checked)
        self.hide_menu.setDefaultAction(self.blank_screen)
        self.blank_screen.setChecked(checked)
        self.theme_screen.setChecked(False)
        self.desktop_screen.setChecked(False)
        if checked:
            Settings().setValue(self.main_window.general_settings_section + '/screen blank', 'blanked')
        else:
            Settings().remove(self.main_window.general_settings_section + '/screen blank')
        self.blank_plugin()
        self.update_preview()
        self.on_toggle_loop()

    def on_theme_display(self, checked=None):
        """
        Handle the Theme screen button
        """
        if checked is None:
            checked = self.theme_screen.isChecked()
        log.debug('on_theme_display %s' % checked)
        self.hide_menu.setDefaultAction(self.theme_screen)
        self.blank_screen.setChecked(False)
        self.theme_screen.setChecked(checked)
        self.desktop_screen.setChecked(False)
        if checked:
            Settings().setValue(self.main_window.general_settings_section + '/screen blank', 'themed')
        else:
            Settings().remove(self.main_window.general_settings_section + '/screen blank')
        self.blank_plugin()
        self.update_preview()
        self.on_toggle_loop()

    def on_hide_display(self, checked=None):
        """
        Handle the Hide screen button
        """
        if checked is None:
            checked = self.desktop_screen.isChecked()
        log.debug('on_hide_display %s' % checked)
        self.hide_menu.setDefaultAction(self.desktop_screen)
        self.blank_screen.setChecked(False)
        self.theme_screen.setChecked(False)
        self.desktop_screen.setChecked(checked)
        if checked:
            Settings().setValue(self.main_window.general_settings_section + '/screen blank', 'hidden')
        else:
            Settings().remove(self.main_window.general_settings_section + '/screen blank')
        self.hide_plugin(checked)
        self.update_preview()
        self.on_toggle_loop()

    def blank_plugin(self):
        """
        Blank/Hide the display screen within a plugin if required.
        """
        hide_mode = self.hide_mode()
        log.debug('blank_plugin %s ', hide_mode)
        if self.service_item is not None:
            if hide_mode:
                if not self.service_item.is_command():
                    Registry().execute('live_display_hide', hide_mode)
                Registry().execute('%s_blank' % self.service_item.name.lower(),
                    [self.service_item, self.is_live, hide_mode])
            else:
                if not self.service_item.is_command():
                    Registry().execute('live_display_show')
                Registry().execute('%s_unblank' % self.service_item.name.lower(), [self.service_item, self.is_live])
        else:
            if hide_mode:
                Registry().execute('live_display_hide', hide_mode)
            else:
                Registry().execute('live_display_show')

    def hide_plugin(self, hide):
        """
        Tell the plugin to hide the display screen.
        """
        log.debug('hide_plugin %s ', hide)
        if self.service_item is not None:
            if hide:
                Registry().execute('live_display_hide', HideMode.Screen)
                Registry().execute('%s_hide' % self.service_item.name.lower(), [self.service_item, self.is_live])
            else:
                if not self.service_item.is_command():
                    Registry().execute('live_display_show')
                Registry().execute('%s_unblank' % self.service_item.name.lower(), [self.service_item, self.is_live])
        else:
            if hide:
                Registry().execute('live_display_hide', HideMode.Screen)
            else:
                Registry().execute('live_display_show')

    def on_slide_selected(self):
        """
        Slide selected in controller
        """
        self.slide_selected()

    def slide_selected(self, start=False):
        """
        Generate the preview when you click on a slide.
        if this is the Live Controller also display on the screen
        """
        row = self.preview_widget.current_slide_number()
        self.selected_row = 0
        if -1 < row < self.preview_widget.slide_count():
            if self.service_item.is_command():
                if self.is_live and not start:
                    Registry().execute('%s_slide' % self.service_item.name.lower(),
                        [self.service_item, self.is_live, row])
            else:
                to_display = self.service_item.get_rendered_frame(row)
                if self.service_item.is_text():
                    self.display.text(to_display)
                else:
                    if start:
                        self.display.build_html(self.service_item, to_display)
                    else:
                        self.display.image(to_display)
                    # reset the store used to display first image
                    self.service_item.bg_image_bytes = None
            self.update_preview()
            self.selected_row = row
            self.preview_widget.change_slide(row)
        Registry().execute('slidecontroller_%s_changed' % self.type_prefix, row)
        self.display.setFocus()

    def on_slide_change(self, row):
        """
        The slide has been changed. Update the slidecontroller accordingly
        """
        self.preview_widget.change_slide(row)
        self.update_preview()
        Registry().execute('slidecontroller_%s_changed' % self.type_prefix, row)

    def update_preview(self):
        """
        This updates the preview frame, for example after changing a slide or using *Blank to Theme*.
        """
        log.debug('update_preview %s ' % self.screens.current['primary'])
        if not self.screens.current['primary'] and self.service_item and \
                self.service_item.is_capable(ItemCapabilities.ProvidesOwnDisplay):
            # Grab now, but try again in a couple of seconds if slide change is slow
            QtCore.QTimer.singleShot(0.5, self.grab_maindisplay)
            QtCore.QTimer.singleShot(2.5, self.grab_maindisplay)
        else:
            self.slide_image = self.display.preview()
            self.slide_preview.setPixmap(self.slide_image)
        self.slide_count += 1

    def grab_maindisplay(self):
        """
        Creates an image of the current screen and updates the preview frame.
        """
        win_id = QtGui.QApplication.desktop().winId()
        rect = self.screens.current['size']
        win_image = QtGui.QPixmap.grabWindow(win_id, rect.x(), rect.y(), rect.width(), rect.height())
        self.slide_preview.setPixmap(win_image)
        self.slide_image = win_image

    def on_slide_selected_next_action(self, checked):
        """
        Wrapper function from create_action so we can throw away the
        incorrect parameter
        """
        self.on_slide_selected_next()

    def on_slide_selected_next(self, wrap=None):
        """
        Go to the next slide.
        """
        if not self.service_item:
            return
        Registry().execute('%s_next' % self.service_item.name.lower(), [self.service_item, self.is_live])
        if self.service_item.is_command() and self.is_live:
            self.update_preview()
        else:
            row = self.preview_widget.current_slide_number() + 1
            if row == self.preview_widget.slide_count():
                if wrap is None:
                    if self.slide_limits == SlideLimits.Wrap:
                        row = 0
                    elif self.is_live and self.slide_limits == SlideLimits.Next:
                        self.service_next()
                        return
                    else:
                        row = self.preview_widget.slide_count() - 1
                elif wrap:
                    row = 0
                else:
                    row = self.preview_widget.slide_count() - 1
            self.preview_widget.change_slide(row)
            self.slide_selected()

    def on_slide_selected_previous(self):
        """
        Go to the previous slide.
        """
        if not self.service_item:
            return
        Registry().execute('%s_previous' % self.service_item.name.lower(), [self.service_item, self.is_live])
        if self.service_item.is_command() and self.is_live:
            self.update_preview()
        else:
            row = self.preview_widget.current_slide_number() - 1
            if row == -1:
                if self.slide_limits == SlideLimits.Wrap:
                    row = self.preview_widget.slide_count() - 1
                elif self.is_live and self.slide_limits == SlideLimits.Next:
                    self.keypress_queue.append(ServiceItemAction.PreviousLastSlide)
                    self._process_queue()
                    return
                else:
                    row = 0
            self.preview_widget.change_slide(row)
            self.slide_selected()

    def on_toggle_loop(self):
        """
        Toggles the loop state.
        """
        hide_mode = self.hide_mode()
        if hide_mode is None and (self.play_slides_loop.isChecked() or self.play_slides_once.isChecked()):
            self.on_start_loop()
        else:
            self.on_stop_loop()

    def on_start_loop(self):
        """
        Start the timer loop running and store the timer id
        """
        if self.preview_widget.slide_count() > 1:
            self.timer_id = self.startTimer(int(self.delay_spin_box.value()) * 1000)

    def on_stop_loop(self):
        """
        Stop the timer loop running
        """
        if self.timer_id:
            self.killTimer(self.timer_id)
            self.timer_id = 0

    def on_play_slides_loop(self, checked=None):
        """
        Start or stop 'Play Slides in Loop'
        """
        if checked is None:
            checked = self.play_slides_loop.isChecked()
        else:
            self.play_slides_loop.setChecked(checked)
        log.debug('on_play_slides_loop %s' % checked)
        if checked:
            self.play_slides_loop.setIcon(build_icon(':/media/media_stop.png'))
            self.play_slides_loop.setText(UiStrings().StopPlaySlidesInLoop)
            self.play_slides_once.setIcon(build_icon(':/media/media_time.png'))
            self.play_slides_once.setText(UiStrings().PlaySlidesToEnd)
            self.play_slides_menu.setDefaultAction(self.play_slides_loop)
            self.play_slides_once.setChecked(False)
        else:
            self.play_slides_loop.setIcon(build_icon(':/media/media_time.png'))
            self.play_slides_loop.setText(UiStrings().PlaySlidesInLoop)
        self.on_toggle_loop()

    def on_play_slides_once(self, checked=None):
        """
        Start or stop 'Play Slides to End'
        """
        if checked is None:
            checked = self.play_slides_once.isChecked()
        else:
            self.play_slides_once.setChecked(checked)
        log.debug('on_play_slides_once %s' % checked)
        if checked:
            self.play_slides_once.setIcon(build_icon(':/media/media_stop.png'))
            self.play_slides_once.setText(UiStrings().StopPlaySlidesToEnd)
            self.play_slides_loop.setIcon(build_icon(':/media/media_time.png'))
            self.play_slides_loop.setText(UiStrings().PlaySlidesInLoop)
            self.play_slides_menu.setDefaultAction(self.play_slides_once)
            self.play_slides_loop.setChecked(False)
        else:
            self.play_slides_once.setIcon(build_icon(':/media/media_time'))
            self.play_slides_once.setText(UiStrings().PlaySlidesToEnd)
        self.on_toggle_loop()

    def set_audio_items_visibility(self, visible):
        """
        Set the visibility of the audio stuff
        """
        self.toolbar.set_widget_visible(self.audio_list, visible)

    def set_audio_pause_clicked(self, checked):
        """
        Pause the audio player
        """
        if not self.audio_pause_item.isVisible():
            return
        if checked:
            self.display.audio_player.pause()
        else:
            self.display.audio_player.play()

    def timerEvent(self, event):
        """
        If the timer event is for this window select next slide
        """
        if event.timerId() == self.timer_id:
            self.on_slide_selected_next(self.play_slides_loop.isChecked())

    def on_edit_song(self):
        """
        From the preview display requires the service Item to be editied
        """
        self.song_edit = True
        new_item = Registry().get(self.service_item.name).on_remote_edit(self.service_item.edit_id, True)
        if new_item:
            self.add_service_item(new_item)

    def on_preview_add_to_service(self):
        """
        From the preview display request the Item to be added to service
        """
        if self.service_item:
            self.service_manager.add_service_item(self.service_item)

    def on_go_live_click(self):
        """
        triggered by clicking the Preview slide items
        """
        if Settings().value('advanced/double click live'):
            # Live and Preview have issues if we have video or presentations
            # playing in both at the same time.
            if self.service_item.is_command():
                Registry().execute('%s_stop' % self.service_item.name.lower(), [self.service_item, self.is_live])
            if self.service_item.is_media():
                self.on_media_close()
            self.on_go_live()

    def on_go_live(self):
        """
        If preview copy slide item to live controller from Preview Controller
        """
        row = self.preview_widget.current_slide_number()
        if -1 < row < self.preview_widget.slide_count():
            if self.service_item.from_service:
                self.service_manager.preview_live(self.service_item.unique_identifier, row)
            else:
                self.live_controller.add_service_manager_item(self.service_item, row)

    def on_media_start(self, item):
        """
        Respond to the arrival of a media service item
        """
        log.debug('SlideController on_media_start')
        self.media_controller.video(self.controller_type, item, self.hide_mode())
        if not self.is_live:
            self.preview_display.show()
            self.slide_preview.hide()

    def on_media_close(self):
        """
        Respond to a request to close the Video
        """
        log.debug('SlideController on_media_close')
        self.media_controller.media_reset(self)
        self.preview_display.hide()
        self.slide_preview.show()

    def _reset_blank(self):
        """
        Used by command items which provide their own displays to reset the
        screen hide attributes
        """
        hide_mode = self.hide_mode()
        if hide_mode == HideMode.Blank:
            self.on_blank_display(True)
        elif hide_mode == HideMode.Theme:
            self.on_theme_display(True)
        elif hide_mode == HideMode.Screen:
            self.on_hide_display(True)
        else:
            self.hide_plugin(False)

    def hide_mode(self):
        """
        Determine what the hide mode should be according to the blank button
        """
        if not self.is_live:
            return None
        elif self.blank_screen.isChecked():
            return HideMode.Blank
        elif self.theme_screen.isChecked():
            return HideMode.Theme
        elif self.desktop_screen.isChecked():
            return HideMode.Screen
        else:
            return None

    def on_next_track_clicked(self):
        """
        Go to the next track when next is clicked
        """
        self.display.audio_player.next()

    def on_audio_time_remaining(self, time):
        """
        Update how much time is remaining
        """
        seconds = self.display.audio_player.media_object.remainingTime() // 1000
        minutes = seconds // 60
        seconds %= 60
        self.audio_time_label.setText(' %02d:%02d ' % (minutes, seconds))

    def on_track_triggered(self):
        """
        Start playing a track
        """
        action = self.sender()
        self.display.audio_player.go_to(action.data())

    def _get_plugin_manager(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, '_plugin_manager'):
            self._plugin_manager = Registry().get('plugin_manager')
        return self._plugin_manager

    plugin_manager = property(_get_plugin_manager)

    def _get_image_manager(self):
        """
        Adds the image manager to the class dynamically
        """
        if not hasattr(self, '_image_manager'):
            self._image_manager = Registry().get('image_manager')
        return self._image_manager

    image_manager = property(_get_image_manager)

    def _get_media_controller(self):
        """
        Adds the media controller to the class dynamically
        """
        if not hasattr(self, '_media_controller'):
            self._media_controller = Registry().get('media_controller')
        return self._media_controller

    media_controller = property(_get_media_controller)

    def _get_service_manager(self):
        """
        Adds the service manager to the class dynamically
        """
        if not hasattr(self, '_service_manager'):
            self._service_manager = Registry().get('service_manager')
        return self._service_manager

    service_manager = property(_get_service_manager)

    def _get_live_controller(self):
        """
        Adds the live controller to the class dynamically
        """
        if not hasattr(self, '_live_controller'):
            self._live_controller = Registry().get('live_controller')
        return self._live_controller

    live_controller = property(_get_live_controller)

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, '_main_window'):
            self._main_window = Registry().get('main_window')
        return self._main_window

    main_window = property(_get_main_window)

