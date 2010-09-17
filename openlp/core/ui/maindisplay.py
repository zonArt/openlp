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

import logging
import os

from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.phonon import Phonon

from openlp.core.lib import Receiver, resize_image, build_html, ServiceItem, \
    image_to_byte
from openlp.core.ui import HideMode

log = logging.getLogger(__name__)

#http://www.steveheffernan.com/html5-video-player/demo-video-player.html

class DisplayWidget(QtGui.QGraphicsView):
    """
    Customised version of QTableWidget which can respond to keyboard
    events.
    """
    log.info(u'Display Widget loaded')

    def __init__(self, live, parent=None):
        QtGui.QGraphicsView.__init__(self)
        self.parent = parent
        self.live = live
        self.hotkey_map = {
            QtCore.Qt.Key_Return: 'servicemanager_next_item',
            QtCore.Qt.Key_Space: 'slidecontroller_live_next_noloop',
            QtCore.Qt.Key_Enter: 'slidecontroller_live_next_noloop',
            QtCore.Qt.Key_0: 'servicemanager_next_item',
            QtCore.Qt.Key_Backspace: 'slidecontroller_live_previous_noloop'}
        self.setStyleSheet(u'border: none;')

    def keyPressEvent(self, event):
        """
        Handle key events from display screen
        """
        # Key events only needed for live
        if not self.live:
            return
        if isinstance(event, QtGui.QKeyEvent):
            # Here accept the event and do something
            if event.key() == QtCore.Qt.Key_Up:
                Receiver.send_message(u'slidecontroller_live_previous')
                event.accept()
            elif event.key() == QtCore.Qt.Key_Down:
                Receiver.send_message(u'slidecontroller_live_next')
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageUp:
                Receiver.send_message(u'slidecontroller_live_first')
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageDown:
                Receiver.send_message(u'slidecontroller_live_last')
                event.accept()
            elif event.key() in self.hotkey_map:
                Receiver.send_message(self.hotkey_map[event.key()])
                event.accept()
            elif event.key() == QtCore.Qt.Key_Escape:
                self.setVisible(False)
                self.videoStop()
                event.accept()
            event.ignore()
        else:
            event.ignore()

class MainDisplay(DisplayWidget):

    def __init__(self, parent, screens, live):
        DisplayWidget.__init__(self, live, parent=None)
        self.parent = parent
        self.screens = screens
        self.isLive = live
        self.alertTab = None
        self.hide_mode = None
        self.setWindowTitle(u'OpenLP Display')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint)
        if self.isLive:
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'maindisplay_hide'), self.hideDisplay)
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'maindisplay_show'), self.showDisplay)

    def setup(self):
        """
        Set up and build the output screen
        """
        log.debug(u'Setup live = %s for %s ' % (self.isLive,
            self.screens.monitor_number))
        self.screen = self.screens.current
        self.setVisible(False)
        self.setGeometry(self.screen[u'size'])
        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)
        self.webView = QtWebKit.QGraphicsWebView()
        self.scene.addItem(self.webView)
        self.webView.resize(self.screen[u'size'].width(),
            self.screen[u'size'].height())
        self.page = self.webView.page()
        self.frame = self.page.mainFrame()
        QtCore.QObject.connect(self.webView,
            QtCore.SIGNAL(u'loadFinished(bool)'), self.isLoaded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.frame.setScrollBarPolicy(QtCore.Qt.Vertical,
            QtCore.Qt.ScrollBarAlwaysOff)
        self.frame.setScrollBarPolicy(QtCore.Qt.Horizontal,
            QtCore.Qt.ScrollBarAlwaysOff)
        if self.isLive:
            # Build the initial frame.
            self.black = QtGui.QImage(
                self.screens.current[u'size'].width(),
                self.screens.current[u'size'].height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
            painter_image = QtGui.QPainter()
            painter_image.begin(self.black)
            painter_image.fillRect(self.black.rect(), QtCore.Qt.black)
            # Build the initial frame.
            initialFrame = QtGui.QImage(
                self.screens.current[u'size'].width(),
                self.screens.current[u'size'].height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
            splash_image = QtGui.QImage(u':/graphics/openlp-splash-screen.png')
            painter_image = QtGui.QPainter()
            painter_image.begin(initialFrame)
            painter_image.fillRect(initialFrame.rect(), QtCore.Qt.white)
            painter_image.drawImage(
                (self.screens.current[u'size'].width() \
                    - splash_image.width()) / 2,
                (self.screens.current[u'size'].height() \
                    - splash_image.height()) / 2,
                splash_image)
            serviceItem = ServiceItem()
            serviceItem.bg_frame = initialFrame
            self.webView.setHtml(build_html(serviceItem, self.screen,
                self.parent.alertTab, self.isLive))
            self.initialFrame = True
            # To display or not to display?
            if not self.screen[u'primary']:
                self.show()
                self.primary = False
            else:
                self.primary = True

    def text(self, slide):
        """
        Add the slide text from slideController

        `slide`
            The slide text to be displayed
        """
        log.debug(u'text')
        self.frame.evaluateJavaScript(u'show_text("%s")' % \
            slide.replace(u'\\', u'\\\\').replace(u'\"', u'\\\"'))
        return self.preview()

    def alert(self, text):
        """
        Add the alert text

        `slide`
            The slide text to be displayed
        """
        log.debug(u'alert')
        if self.height() != self.screen[u'size'].height() \
            or not self.isVisible():
            shrink = True
        else:
            shrink = False
        js =  u'show_alert("%s", "%s")' % (
            text.replace(u'\\', u'\\\\').replace(u'\"', u'\\\"'),
            u'top' if shrink else u'')
        height = self.frame.evaluateJavaScript(js)
        if shrink:
            if text:
                self.resize(self.width(), int(height.toString()))
                self.setVisible(True)
            else:
                self.setGeometry(self.screen[u'size'])
                self.setVisible(False)

    def image(self, image):
        """
        Add an image as the background.  The image is converted to a
        bytestream on route.

        `Image`
            The Image to be displayed can be QImage or QPixmap
        """
        log.debug(u'image')
        image = resize_image(image, self.screen[u'size'].width(),
            self.screen[u'size'].height())
        self.resetVideo()
        self.displayImage(image)
        # show screen
        if self.isLive:
            self.setVisible(True)

    def displayImage(self, image):
        """
        Display an image, as is.
        """
        if image:
            js = u'show_image("data:image/png;base64,%s");' % \
                image_to_byte(image)
        else:
            js = u'show_image("");'
        self.frame.evaluateJavaScript(js)

    def resetImage(self):
        """
        Reset the backgound image to the service item image.
        Used after Image plugin has changed the background
        """
        log.debug(u'resetImage')
        self.displayImage(self.serviceItem.bg_frame)

    def resetVideo(self):
        """
        Used after Video plugin has changed the background
        """
        log.debug(u'resetVideo')
        self.frame.evaluateJavaScript(u'show_video("close");')

    def videoPlay(self):
        """
        Responds to the request to play a loaded video
        """
        log.debug(u'videoPlay')
        self.frame.evaluateJavaScript(u'show_video("play");')
        # show screen
        if self.isLive:
            self.setVisible(True)

    def videoPause(self):
        """
        Responds to the request to pause a loaded video
        """
        log.debug(u'videoPause')
        self.frame.evaluateJavaScript(u'show_video("pause");')

    def videoStop(self):
        """
        Responds to the request to stop a loaded video
        """
        log.debug(u'videoStop')
        self.frame.evaluateJavaScript(u'show_video("stop");')

    def videoVolume(self, volume):
        """
        Changes the volume of a running video
        """
        log.debug(u'videoVolume %d' % volume)
        self.frame.evaluateJavaScript(u'show_video(null, null, %s);' %
            str(float(volume)/float(10)))

    def video(self, videoPath, volume):
        """
        Loads and starts a video to run with the option of sound
        """
        log.debug(u'video')
        self.loaded = True
        js = u'show_video("play", "%s", %s, true);' % \
            (videoPath.replace(u'\\', u'\\\\'), str(float(volume)/float(10)))
        self.frame.evaluateJavaScript(js)
        return self.preview()

    def isLoaded(self):
        """
        Called by webView event to show display is fully loaded
        """
        log.debug(u'loaded')
        self.loaded = True

    def preview(self):
        """
        Generates a preview of the image displayed.
        """
        log.debug(u'preview for %s', self.isLive)
        # We must have a service item to preview
        if not hasattr(self, u'serviceItem'):
            return
        Receiver.send_message(u'openlp_process_events')
        if self.isLive:
            # Wait for the fade to finish before geting the preview.
            # Important otherwise preview will have incorrect text if at all !
            if self.serviceItem.themedata and \
                self.serviceItem.themedata.display_slideTransition:
                while self.frame.evaluateJavaScript(u'show_text_complete()') \
                    .toString() == u'false':
                    Receiver.send_message(u'openlp_process_events')
        # Wait for the webview to update before geting the preview.
        # Important otherwise first preview will miss the background !
        while not self.loaded:
            Receiver.send_message(u'openlp_process_events')
        if self.isLive:
            self.setVisible(True)
        preview = QtGui.QImage(self.screen[u'size'].width(),
            self.screen[u'size'].height(),
            QtGui.QImage.Format_ARGB32_Premultiplied)
        painter = QtGui.QPainter(preview)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.frame.render(painter)
        painter.end()
        # Make display show up if in single screen mode
        return preview

    def buildHtml(self, serviceItem):
        """
        Store the serviceItem and build the new HTML from it. Add the
        HTML to the display
        """
        log.debug(u'buildHtml')
        self.loaded = False
        self.initialFrame = False
        self.serviceItem = serviceItem
        html = build_html(self.serviceItem, self.screen, self.parent.alertTab,
            self.isLive)
        log.debug(u'buildHtml - pre setHtml')
        self.webView.setHtml(html)
        log.debug(u'buildHtml - post setHtml')
        if serviceItem.foot_text and serviceItem.foot_text:
            self.footer(serviceItem.foot_text)
        # if was hidden keep it hidden
        if self.hide_mode and self.isLive:
            self.hideDisplay(self.hide_mode)

    def footer(self, text):
        """
        Display the Footer
        """
        log.debug(u'footer')
        js =  "show_footer('" + \
            text.replace("\\", "\\\\").replace("\'", "\\\'") + "')"
        self.frame.evaluateJavaScript(js)

    def hideDisplay(self, mode=HideMode.Screen):
        """
        Hide the display by making all layers transparent
        Store the images so they can be replaced when required
        """
        log.debug(u'hideDisplay mode = %d', mode)
        if mode == HideMode.Screen:
            self.frame.evaluateJavaScript(u'show_blank("desktop");')
            self.setVisible(False)
        elif mode == HideMode.Blank or self.initialFrame:
            self.frame.evaluateJavaScript(u'show_blank("black");')
        else:
            self.frame.evaluateJavaScript(u'show_blank("theme");')
        if mode != HideMode.Screen and self.isHidden():
            self.setVisible(True)
        self.hide_mode = mode

    def showDisplay(self):
        """
        Show the stored layers so the screen reappears as it was
        originally.
        Make the stored images None to release memory.
        """
        log.debug(u'showDisplay')
        self.frame.evaluateJavaScript('show_blank("show");')
        if self.isHidden():
            self.setVisible(True)
        # Trigger actions when display is active again
        Receiver.send_message(u'maindisplay_active')
        self.hide_mode = None

class AudioPlayer(QtCore.QObject):
    """
    This Class will play audio only allowing components to work with a
    soundtrack independent of the user interface.
    """
    log.info(u'AudioPlayer Loaded')

    def __init__(self, parent):
        """
        The constructor for the display form.

        ``parent``
            The parent widget.

        ``screens``
            The list of screens.
        """
        log.debug(u'AudioPlayer Initialisation started')
        QtCore.QObject.__init__(self, parent)
        self.message = None
        self.mediaObject = Phonon.MediaObject()
        self.audioObject = Phonon.AudioOutput(Phonon.VideoCategory)
        Phonon.createPath(self.mediaObject, self.audioObject)

    def setup(self):
        """
        Sets up the Audio Player for use
        """
        log.debug(u'AudioPlayer Setup')

    def close(self):
        """
        Shutting down so clean up connections
        """
        self.onMediaStop()
        for path in self.mediaObject.outputPaths():
            path.disconnect()

    def onMediaQueue(self, message):
        """
        Set up a video to play from the serviceitem.
        """
        log.debug(u'AudioPlayer Queue new media message %s' % message)
        mfile = os.path.join(message[0].get_frame_path(),
            message[0].get_frame_title())
        self.mediaObject.setCurrentSource(Phonon.MediaSource(mfile))
        self.onMediaPlay()

    def onMediaPlay(self):
        """
        We want to play the play so start it
        """
        log.debug(u'AudioPlayer _play called')
        self.mediaObject.play()

    def onMediaPause(self):
        """
        Pause the Audio
        """
        log.debug(u'AudioPlayer Media paused by user')
        self.mediaObject.pause()

    def onMediaStop(self):
        """
        Stop the Audio and clean up
        """
        log.debug(u'AudioPlayer Media stopped by user')
        self.message = None
        self.mediaObject.stop()
        self.onMediaFinish()

    def onMediaFinish(self):
        """
        Clean up the Object queue
        """
        log.debug(u'AudioPlayer Reached end of media playlist')
        self.mediaObject.clearQueue()
