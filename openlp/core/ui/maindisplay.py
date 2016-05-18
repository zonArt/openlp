# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
The :mod:`maindisplay` module provides the functionality to display screens and play multimedia within OpenLP.

Some of the code for this form is based on the examples at:

* `http://www.steveheffernan.com/html5-video-player/demo-video-player.html`_
* `http://html5demos.com/two-videos`_

"""

import html
import logging
import os

from PyQt5 import QtCore, QtWidgets, QtWebKit, QtWebKitWidgets, QtOpenGL, QtGui, QtMultimedia

from openlp.core.common import AppLocation, Registry, RegistryProperties, OpenLPMixin, Settings, translate,\
    is_macosx, is_win
from openlp.core.lib import ServiceItem, ImageSource, ScreenList, build_html, expand_tags, image_to_byte
from openlp.core.lib.theme import BackgroundType
from openlp.core.ui import HideMode, AlertLocation, DisplayControllerType

if is_macosx():
    from ctypes import pythonapi, c_void_p, c_char_p, py_object

    from sip import voidptr
    from objc import objc_object
    from AppKit import NSMainMenuWindowLevel, NSWindowCollectionBehaviorManaged

log = logging.getLogger(__name__)

OPAQUE_STYLESHEET = """
QWidget {
    border: 0px;
    margin: 0px;
    padding: 0px;
}
QGraphicsView {}
"""
TRANSPARENT_STYLESHEET = """
QWidget {
    border: 0px;
    margin: 0px;
    padding: 0px;
}
QGraphicsView {
    background: transparent;
    border: 0px;
}
"""


class Display(QtWidgets.QGraphicsView):
    """
    This is a general display screen class. Here the general display settings will done. It will be used as
    specialized classes by Main Display and Preview display.
    """
    def __init__(self, parent):
        """
        Constructor
        """
        self.is_live = False
        if hasattr(parent, 'is_live') and parent.is_live:
            self.is_live = True
        if self.is_live:
            self.parent = lambda: parent
        super(Display, self).__init__()
        self.controller = parent
        self.screen = {}

    def setup(self):
        """
        Set up and build the screen base
        """
        self.setGeometry(self.screen['size'])
        self.web_view = QtWebKitWidgets.QWebView(self)
        self.web_view.setGeometry(0, 0, self.screen['size'].width(), self.screen['size'].height())
        self.web_view.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        palette = self.web_view.palette()
        palette.setBrush(QtGui.QPalette.Base, QtCore.Qt.transparent)
        self.web_view.page().setPalette(palette)
        self.web_view.setAttribute(QtCore.Qt.WA_OpaquePaintEvent, False)
        self.page = self.web_view.page()
        self.frame = self.page.mainFrame()
        if self.is_live and log.getEffectiveLevel() == logging.DEBUG:
            self.web_view.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        self.web_view.loadFinished.connect(self.is_web_loaded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.frame.setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
        self.frame.setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, event):
        """
        React to resizing of this display

        :param event: The event to be handled
        """
        if hasattr(self, 'web_view'):
            self.web_view.setGeometry(0, 0, self.width(), self.height())

    def is_web_loaded(self, field=None):
        """
        Called by webView event to show display is fully loaded
        """
        self.web_loaded = True


class MainDisplay(OpenLPMixin, Display, RegistryProperties):
    """
    This is the display screen as a specialized class from the Display class
    """
    def __init__(self, parent):
        """
        Constructor
        """
        super(MainDisplay, self).__init__(parent)
        self.screens = ScreenList()
        self.rebuild_css = False
        self.hide_mode = None
        self.override = {}
        self.retranslateUi()
        self.media_object = None
        if self.is_live:
            self.audio_player = AudioPlayer(self)
        else:
            self.audio_player = None
        self.first_time = True
        self.web_loaded = True
        self.setStyleSheet(OPAQUE_STYLESHEET)
        window_flags = QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint
        if Settings().value('advanced/x11 bypass wm'):
            window_flags |= QtCore.Qt.X11BypassWindowManagerHint
        # TODO: The following combination of window_flags works correctly
        # on Mac OS X. For next OpenLP version we should test it on other
        # platforms. For OpenLP 2.0 keep it only for OS X to not cause any
        # regressions on other platforms.
        if is_macosx():
            window_flags = QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window
        self.setWindowFlags(window_flags)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.set_transparency(False)
        if is_macosx():
            if self.is_live:
                # Get a pointer to the underlying NSView
                try:
                    nsview_pointer = self.winId().ascapsule()
                except:
                    nsview_pointer = voidptr(self.winId()).ascapsule()
                # Set PyCapsule name so pyobjc will accept it
                pythonapi.PyCapsule_SetName.restype = c_void_p
                pythonapi.PyCapsule_SetName.argtypes = [py_object, c_char_p]
                pythonapi.PyCapsule_SetName(nsview_pointer, c_char_p(b"objc.__object__"))
                # Covert the NSView pointer into a pyobjc NSView object
                self.pyobjc_nsview = objc_object(cobject=nsview_pointer)
                # Set the window level so that the MainDisplay is above the menu bar and dock
                self.pyobjc_nsview.window().setLevel_(NSMainMenuWindowLevel + 2)
                # Set the collection behavior so the window is visible when Mission Control is activated
                self.pyobjc_nsview.window().setCollectionBehavior_(NSWindowCollectionBehaviorManaged)
                if self.screens.current['primary']:
                    # Connect focusWindowChanged signal so we can change the window level when the display is not in
                    # focus on the primary screen
                    self.application.focusWindowChanged.connect(self.change_window_level)
        if self.is_live:
            Registry().register_function('live_display_hide', self.hide_display)
            Registry().register_function('live_display_show', self.show_display)
            Registry().register_function('update_display_css', self.css_changed)
        self.close_display = False

    def closeEvent(self, event):
        """
        Catch the close event, and check that the close event is triggered by OpenLP closing the display.
        On Windows this event can be triggered by pressing ALT+F4, which we want to ignore.

        :param event: The triggered event
        """
        if self.close_display:
            super().closeEvent(event)
        else:
            event.ignore()

    def close(self):
        """
        Remove registered function on close.
        """
        if self.is_live:
            if is_macosx():
                # Block signals so signal we are disconnecting can't get called while we disconnect it
                self.blockSignals(True)
                if self.screens.current['primary']:
                    self.application.focusWindowChanged.disconnect()
                self.blockSignals(False)
            Registry().remove_function('live_display_hide', self.hide_display)
            Registry().remove_function('live_display_show', self.show_display)
            Registry().remove_function('update_display_css', self.css_changed)
        self.close_display = True
        super().close()

    def set_transparency(self, enabled):
        """
        Set the transparency of the window

        :param enabled: Is transparency enabled
        """
        if enabled:
            self.setAutoFillBackground(False)
            self.setStyleSheet(TRANSPARENT_STYLESHEET)
        else:
            self.setAttribute(QtCore.Qt.WA_NoSystemBackground, False)
            self.setStyleSheet(OPAQUE_STYLESHEET)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, enabled)
        self.repaint()

    def css_changed(self):
        """
        We need to rebuild the CSS on the live display.
        """
        for plugin in self.plugin_manager.plugins:
            plugin.refresh_css(self.frame)

    def retranslateUi(self):
        """
        Setup the interface translation strings.
        """
        self.setWindowTitle(translate('OpenLP.MainDisplay', 'OpenLP Display'))

    def setup(self):
        """
        Set up and build the output screen
        """
        self.log_debug('Start MainDisplay setup (live = {islive})'.format(islive=self.is_live))
        self.screen = self.screens.current
        self.setVisible(False)
        Display.setup(self)
        if self.is_live:
            # Build the initial frame.
            background_color = QtGui.QColor()
            background_color.setNamedColor(Settings().value('core/logo background color'))
            if not background_color.isValid():
                background_color = QtCore.Qt.white
            image_file = Settings().value('core/logo file')
            splash_image = QtGui.QImage(image_file)
            self.initial_fame = QtGui.QImage(
                self.screen['size'].width(),
                self.screen['size'].height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
            painter_image = QtGui.QPainter()
            painter_image.begin(self.initial_fame)
            painter_image.fillRect(self.initial_fame.rect(), background_color)
            painter_image.drawImage(
                (self.screen['size'].width() - splash_image.width()) // 2,
                (self.screen['size'].height() - splash_image.height()) // 2,
                splash_image)
            service_item = ServiceItem()
            service_item.bg_image_bytes = image_to_byte(self.initial_fame)
            self.web_view.setHtml(build_html(service_item, self.screen, self.is_live, None,
                                  plugins=self.plugin_manager.plugins))
            self._hide_mouse()

    def text(self, slide, animate=True):
        """
        Add the slide text from slideController

        :param slide: The slide text to be displayed
        :param animate: Perform transitions if applicable when setting the text
        """
        # Wait for the webview to update before displaying text.
        while not self.web_loaded:
            self.application.process_events()
        self.setGeometry(self.screen['size'])
        if animate:
            # NOTE: Verify this works with ''.format()
            _text = slide.replace('\\', '\\\\').replace('\"', '\\\"')
            self.frame.evaluateJavaScript('show_text("{text}")'.format(text=_text))
        else:
            # This exists for https://bugs.launchpad.net/openlp/+bug/1016843
            # For unknown reasons if evaluateJavaScript is called
            # from the themewizard, then it causes a crash on
            # Windows if there are many items in the service to re-render.
            # Setting the div elements direct seems to solve the issue
            self.frame.findFirstElement("#lyricsmain").setInnerXml(slide)

    def alert(self, text, location):
        """
        Display an alert.

        :param text: The text to be displayed.
        :param location: Where on the screen is the text to be displayed
        """
        # First we convert <>& marks to html variants, then apply
        # formattingtags, finally we double all backslashes for JavaScript.
        text_prepared = expand_tags(html.escape(text)).replace('\\', '\\\\').replace('\"', '\\\"')
        if self.height() != self.screen['size'].height() or not self.isVisible():
            shrink = True
            js = 'show_alert("{text}", "{top}")'.format(text=text_prepared, top='top')
        else:
            shrink = False
            js = 'show_alert("{text}", "")'.format(text=text_prepared)
        height = self.frame.evaluateJavaScript(js)
        if shrink:
            if text:
                alert_height = int(height)
                self.resize(self.width(), alert_height)
                self.setVisible(True)
                if location == AlertLocation.Middle:
                    self.move(self.screen['size'].left(), (self.screen['size'].height() - alert_height) // 2)
                elif location == AlertLocation.Bottom:
                    self.move(self.screen['size'].left(), self.screen['size'].height() - alert_height)
            else:
                self.setVisible(False)
                self.setGeometry(self.screen['size'])
        # Workaround for bug #1531319, should not be needed with PyQt 5.6.
        if is_win():
            self.shake_web_view()

    def direct_image(self, path, background):
        """
        API for replacement backgrounds so Images are added directly to cache.

        :param path: Path to Image
        :param background: The background color
        """
        self.image_manager.add_image(path, ImageSource.ImagePlugin, background)
        if not hasattr(self, 'service_item'):
            return False
        self.override['image'] = path
        self.override['theme'] = self.service_item.theme_data.background_filename
        self.image(path)
        # Update the preview frame.
        if self.is_live:
            self.live_controller.update_preview()
        return True

    def image(self, path):
        """
        Add an image as the background. The image has already been added to the
        cache.

        :param path: The path to the image to be displayed. **Note**, the path is only passed to identify the image.
            If the image has changed it has to be re-added to the image manager.
        """
        image = self.image_manager.get_image_bytes(path, ImageSource.ImagePlugin)
        self.controller.media_controller.media_reset(self.controller)
        self.display_image(image)

    def display_image(self, image):
        """
        Display an image, as is.

        :param image: The image to be displayed
        """
        self.setGeometry(self.screen['size'])
        if image:
            js = 'show_image("data:image/png;base64,{image}");'.format(image=image)
        else:
            js = 'show_image("");'
        self.frame.evaluateJavaScript(js)

    def reset_image(self):
        """
        Reset the background image to the service item image. Used after the image plugin has changed the background.
        """
        if hasattr(self, 'service_item'):
            self.display_image(self.service_item.bg_image_bytes)
        else:
            self.display_image(None)
        # Update the preview frame.
        if self.is_live:
            self.live_controller.update_preview()
        # clear the cache
        self.override = {}

    def preview(self):
        """
        Generates a preview of the image displayed.
        """
        was_visible = self.isVisible()
        self.application.process_events()
        # We must have a service item to preview.
        if self.is_live and hasattr(self, 'service_item'):
            # Wait for the fade to finish before geting the preview.
            # Important otherwise preview will have incorrect text if at all!
            if self.service_item.theme_data and self.service_item.theme_data.display_slide_transition:
                # Workaround for bug #1531319, should not be needed with PyQt 5.6.
                if is_win():
                    fade_shake_timer = QtCore.QTimer(self)
                    fade_shake_timer.setInterval(25)
                    fade_shake_timer.timeout.connect(self.shake_web_view)
                    fade_shake_timer.start()
                while not self.frame.evaluateJavaScript('show_text_completed()'):
                    self.application.process_events()
                # Workaround for bug #1531319, should not be needed with PyQt 5.6.
                if is_win():
                    fade_shake_timer.stop()
        # Wait for the webview to update before getting the preview.
        # Important otherwise first preview will miss the background !
        while not self.web_loaded:
            self.application.process_events()
        # if was hidden keep it hidden
        if self.is_live:
            if self.hide_mode:
                self.hide_display(self.hide_mode)
            # Only continue if the visibility wasn't changed during method call.
            elif was_visible == self.isVisible():
                # Single screen active
                if self.screens.display_count == 1:
                    # Only make visible if setting enabled.
                    if Settings().value('core/display on monitor'):
                        self.setVisible(True)
                else:
                    self.setVisible(True)
        # Workaround for bug #1531319, should not be needed with PyQt 5.6.
        if is_win():
            self.shake_web_view()
        return self.grab()

    def build_html(self, service_item, image_path=''):
        """
        Store the service_item and build the new HTML from it. Add the HTML to the display

        :param service_item: The Service item to be used
        :param image_path: Where the image resides.
        """
        self.web_loaded = False
        self.initial_fame = None
        self.service_item = service_item
        background = None
        # We have an image override so keep the image till the theme changes.
        if self.override:
            # We have an video override so allow it to be stopped.
            if 'video' in self.override:
                Registry().execute('video_background_replaced')
                self.override = {}
            # We have a different theme.
            elif self.override['theme'] != service_item.theme_data.background_filename:
                Registry().execute('live_theme_changed')
                self.override = {}
            else:
                # replace the background
                background = self.image_manager.get_image_bytes(self.override['image'], ImageSource.ImagePlugin)
        self.set_transparency(self.service_item.theme_data.background_type ==
                              BackgroundType.to_string(BackgroundType.Transparent))
        image_bytes = None
        if self.service_item.theme_data.background_type == 'image':
            if self.service_item.theme_data.background_filename:
                self.service_item.bg_image_bytes = self.image_manager.get_image_bytes(
                    self.service_item.theme_data.background_filename, ImageSource.Theme)
            if image_path:
                image_bytes = self.image_manager.get_image_bytes(image_path, ImageSource.ImagePlugin)
        html = build_html(self.service_item, self.screen, self.is_live, background, image_bytes,
                          plugins=self.plugin_manager.plugins)
        self.web_view.setHtml(html)
        if service_item.foot_text:
            self.footer(service_item.foot_text)
        # if was hidden keep it hidden
        if self.hide_mode and self.is_live and not service_item.is_media():
            if Settings().value('core/auto unblank'):
                Registry().execute('slidecontroller_live_unblank')
            else:
                self.hide_display(self.hide_mode)
        if self.service_item.theme_data.background_type == 'video' and self.is_live:
            if self.service_item.theme_data.background_filename:
                service_item = ServiceItem()
                service_item.title = 'webkit'
                service_item.processor = 'webkit'
                path = os.path.join(AppLocation.get_section_data_path('themes'),
                                    self.service_item.theme_data.theme_name)
                service_item.add_from_command(path,
                                              self.service_item.theme_data.background_filename,
                                              ':/media/slidecontroller_multimedia.png')
                self.media_controller.video(DisplayControllerType.Live, service_item, video_behind_text=True)
        self._hide_mouse()

    def footer(self, text):
        """
        Display the Footer

        :param text: footer text to be displayed
        """
        js = 'show_footer(\'' + text.replace('\\', '\\\\').replace('\'', '\\\'') + '\')'
        self.frame.evaluateJavaScript(js)

    def hide_display(self, mode=HideMode.Screen):
        """
        Hide the display by making all layers transparent Store the images so they can be replaced when required

        :param mode: How the screen is to be hidden
        """
        self.log_debug('hide_display mode = {mode:d}'.format(mode=mode))
        if self.screens.display_count == 1:
            # Only make visible if setting enabled.
            if not Settings().value('core/display on monitor'):
                return
        if mode == HideMode.Screen:
            self.frame.evaluateJavaScript('show_blank("desktop");')
            self.setVisible(False)
        elif mode == HideMode.Blank or self.initial_fame:
            self.frame.evaluateJavaScript('show_blank("black");')
        else:
            self.frame.evaluateJavaScript('show_blank("theme");')
        if mode != HideMode.Screen:
            if self.isHidden():
                self.setVisible(True)
                self.web_view.setVisible(True)
            # Workaround for bug #1531319, should not be needed with PyQt 5.6.
            if is_win():
                self.shake_web_view()
        self.hide_mode = mode

    def show_display(self):
        """
        Show the stored layers so the screen reappears as it was originally.
        Make the stored images None to release memory.
        """
        if self.screens.display_count == 1:
            # Only make visible if setting enabled.
            if not Settings().value('core/display on monitor'):
                return
        self.frame.evaluateJavaScript('show_blank("show");')
        # Check if setting for hiding logo on startup is enabled.
        # If it is, display should remain hidden, otherwise logo is shown. (from def setup)
        if self.isHidden() and not Settings().value('core/logo hide on startup'):
            self.setVisible(True)
        self.hide_mode = None
        # Trigger actions when display is active again.
        if self.is_live:
            Registry().execute('live_display_active')
            # Workaround for bug #1531319, should not be needed with PyQt 5.6.
            if is_win():
                self.shake_web_view()

    def _hide_mouse(self):
        """
        Hide mouse cursor when moved over display.
        """
        if Settings().value('advanced/hide mouse'):
            self.setCursor(QtCore.Qt.BlankCursor)
            self.frame.evaluateJavaScript('document.body.style.cursor = "none"')
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.frame.evaluateJavaScript('document.body.style.cursor = "auto"')

    def change_window_level(self, window):
        """
        Changes the display window level on Mac OS X so that the main window can be brought into focus but still allow
        the main display to be above the menu bar and dock when it in focus.

        :param window: Window from our application that focus changed to or None if outside our application
        """
        if is_macosx():
            if window:
                # Get different window ids' as int's
                try:
                    window_id = window.winId().__int__()
                    main_window_id = self.main_window.winId().__int__()
                    self_id = self.winId().__int__()
                except:
                    return
                # If the passed window has the same id as our window make sure the display has the proper level and
                # collection behavior.
                if window_id == self_id:
                    self.pyobjc_nsview.window().setLevel_(NSMainMenuWindowLevel + 2)
                    self.pyobjc_nsview.window().setCollectionBehavior_(NSWindowCollectionBehaviorManaged)
                # Else set the displays window level back to normal since we are trying to focus a window other than
                # the display.
                else:
                    self.pyobjc_nsview.window().setLevel_(0)
                    self.pyobjc_nsview.window().setCollectionBehavior_(NSWindowCollectionBehaviorManaged)
                    # If we are trying to focus the main window raise it now to complete the focus change.
                    if window_id == main_window_id:
                        self.main_window.raise_()

    def shake_web_view(self):
        """
        Resizes the web_view a bit to force an update. Workaround for bug #1531319, should not be needed with PyQt 5.6.
        """
        self.web_view.setGeometry(0, 0, self.width(), self.height() - 1)
        self.web_view.setGeometry(0, 0, self.width(), self.height())


class AudioPlayer(OpenLPMixin, QtCore.QObject):
    """
    This Class will play audio only allowing components to work with a soundtrack independent of the user interface.
    """
    position_changed = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        """
        The constructor for the display form.

        :param parent:  The parent widget.
        """
        super(AudioPlayer, self).__init__(parent)
        self.player = QtMultimedia.QMediaPlayer()
        self.playlist = QtMultimedia.QMediaPlaylist(self.player)
        self.volume_slider = None
        self.player.setPlaylist(self.playlist)
        self.player.positionChanged.connect(self._on_position_changed)

    def __del__(self):
        """
        Shutting down so clean up connections
        """
        self.stop()

    def _on_position_changed(self, position):
        """
        Emit a signal when the position of the media player updates
        """
        self.position_changed.emit(position)

    def set_volume_slider(self, slider):
        """
        Connect the volume slider to the media player
        :param slider:
        """
        self.volume_slider = slider
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(self.player.volume())
        self.volume_slider.valueChanged.connect(self.set_volume)

    def set_volume(self, volume):
        """
        Set the volume of the media player

        :param volume:
        """
        self.player.setVolume(volume)

    def reset(self):
        """
        Reset the audio player, clearing the playlist and the queue.
        """
        self.stop()
        self.playlist.clear()

    def play(self):
        """
        We want to play the file so start it
        """
        self.player.play()

    def pause(self):
        """
        Pause the Audio
        """
        self.player.pause()

    def stop(self):
        """
        Stop the Audio and clean up
        """
        self.player.stop()

    def add_to_playlist(self, file_names):
        """
        Add another file to the playlist.

        :param file_names:  A list with files to be added to the playlist.
        """
        if not isinstance(file_names, list):
            file_names = [file_names]
        for file_name in file_names:
            self.playlist.addMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file_name)))

    def next(self):
        """
        Skip forward to the next track in the list
        """
        self.player.next()

    def go_to(self, index):
        """
        Go to a particular track in the list

        :param index: The track to go to
        """
        self.playlist.setCurrentIndex(index)
        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.play()
