# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
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
"""
The :mod:`maindisplay` module provides the functionality to display screens
and play multimedia within OpenLP.
"""
import logging
import os

from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.phonon import Phonon

from openlp.core.lib import Receiver, build_html, ServiceItem, image_to_byte, \
    translate

from openlp.core.ui import HideMode, ScreenList

log = logging.getLogger(__name__)

#http://www.steveheffernan.com/html5-video-player/demo-video-player.html
#http://html5demos.com/two-videos

class MainDisplay(QtGui.QGraphicsView):
    """
    This is the display screen.
    """
    def __init__(self, parent, imageManager, live):
        if live:
            QtGui.QGraphicsView.__init__(self)
        else:
            QtGui.QGraphicsView.__init__(self, parent)
        self.isLive = live
        self.imageManager = imageManager
        self.screens = ScreenList.get_instance()
        self.alertTab = None
        self.hideMode = None
        self.videoHide = False
        self.override = {}
        self.retranslateUi()
        self.mediaObject = None
        if live:
            self.audioPlayer = AudioPlayer(self)
        else:
            self.audioPlayer = None
        self.firstTime = True
        self.setStyleSheet(u'border: 0px; margin: 0px; padding: 0px;')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.X11BypassWindowManagerHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        if self.isLive:
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'maindisplay_hide'), self.hideDisplay)
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'maindisplay_show'), self.showDisplay)
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'openlp_phonon_creation'),
                self.createMediaObject)

    def retranslateUi(self):
        """
        Setup the interface translation strings.
        """
        self.setWindowTitle(translate('OpenLP.MainDisplay', 'OpenLP Display'))

    def setup(self):
        """
        Set up and build the output screen
        """
        log.debug(u'Start MainDisplay setup (live = %s)' % self.isLive)
        self.usePhonon = QtCore.QSettings().value(
            u'media/use phonon', QtCore.QVariant(True)).toBool()
        self.phononActive = False
        self.screen = self.screens.current
        self.setVisible(False)
        self.setGeometry(self.screen[u'size'])
        self.videoWidget = Phonon.VideoWidget(self)
        self.videoWidget.setVisible(False)
        self.videoWidget.setGeometry(QtCore.QRect(0, 0,
            self.screen[u'size'].width(), self.screen[u'size'].height()))
        if self.isLive:
            if not self.firstTime:
                self.createMediaObject()
        log.debug(u'Setup webView')
        self.webView = QtWebKit.QWebView(self)
        self.webView.setGeometry(0, 0,
            self.screen[u'size'].width(), self.screen[u'size'].height())
        self.page = self.webView.page()
        self.frame = self.page.mainFrame()
        QtCore.QObject.connect(self.webView,
            QtCore.SIGNAL(u'loadFinished(bool)'), self.isWebLoaded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.frame.setScrollBarPolicy(QtCore.Qt.Vertical,
            QtCore.Qt.ScrollBarAlwaysOff)
        self.frame.setScrollBarPolicy(QtCore.Qt.Horizontal,
            QtCore.Qt.ScrollBarAlwaysOff)
        if self.isLive:
            # Build the initial frame.
            self.black = QtGui.QImage(
                self.screen[u'size'].width(),
                self.screen[u'size'].height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
            painter_image = QtGui.QPainter()
            painter_image.begin(self.black)
            painter_image.fillRect(self.black.rect(), QtCore.Qt.black)
            # Build the initial frame.
            image_file = QtCore.QSettings().value(u'advanced/default image',
                QtCore.QVariant(u':/graphics/openlp-splash-screen.png'))\
                .toString()
            background_color = QtGui.QColor()
            background_color.setNamedColor(QtCore.QSettings().value(
                u'advanced/default color',
                QtCore.QVariant(u'#ffffff')).toString())
            if not background_color.isValid():
                background_color = QtCore.Qt.white
            splash_image = QtGui.QImage(image_file)
            self.initialFrame = QtGui.QImage(
                self.screen[u'size'].width(),
                self.screen[u'size'].height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
            painter_image = QtGui.QPainter()
            painter_image.begin(self.initialFrame)
            painter_image.fillRect(self.initialFrame.rect(), background_color)
            painter_image.drawImage(
                (self.screen[u'size'].width() - splash_image.width()) / 2,
                (self.screen[u'size'].height() - splash_image.height()) / 2,
                splash_image)
            serviceItem = ServiceItem()
            serviceItem.bg_image_bytes = image_to_byte(self.initialFrame)
            self.webView.setHtml(build_html(serviceItem, self.screen,
                self.alertTab, self.isLive, None))
            self.__hideMouse()
            # To display or not to display?
            if not self.screen[u'primary']:
                self.primary = False
            else:
                self.primary = True
        log.debug(u'Finished MainDisplay setup')

    def createMediaObject(self):
        self.firstTime = False
        log.debug(u'Creating Phonon objects - Start for %s', self.isLive)
        self.mediaObject = Phonon.MediaObject(self)
        self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self.mediaObject)
        Phonon.createPath(self.mediaObject, self.videoWidget)
        Phonon.createPath(self.mediaObject, self.audio)
        QtCore.QObject.connect(self.mediaObject,
            QtCore.SIGNAL(u'stateChanged(Phonon::State, Phonon::State)'),
            self.videoState)
        QtCore.QObject.connect(self.mediaObject,
            QtCore.SIGNAL(u'finished()'),
            self.videoFinished)
        QtCore.QObject.connect(self.mediaObject,
            QtCore.SIGNAL(u'tick(qint64)'),
            self.videoTick)
        log.debug(u'Creating Phonon objects - Finished for %s', self.isLive)

    def text(self, slide):
        """
        Add the slide text from slideController

        `slide`
            The slide text to be displayed
        """
        log.debug(u'text to display')
        # Wait for the webview to update before displaying text.
        while not self.webLoaded:
            Receiver.send_message(u'openlp_process_events')
        self.setGeometry(self.screen[u'size'])
        self.frame.evaluateJavaScript(u'show_text("%s")' %
            slide.replace(u'\\', u'\\\\').replace(u'\"', u'\\\"'))

    def alert(self, text):
        """
        Add the alert text

        `slide`
            The slide text to be displayed
        """
        log.debug(u'alert to display')
        if self.height() != self.screen[u'size'].height() or not \
            self.isVisible() or self.videoWidget.isVisible():
            shrink = True
        else:
            shrink = False
        js = u'show_alert("%s", "%s")' % (
            text.replace(u'\\', u'\\\\').replace(u'\"', u'\\\"'),
            u'top' if shrink else u'')
        height = self.frame.evaluateJavaScript(js)
        if shrink:
            if self.phononActive:
                shrinkItem = self.webView
            else:
                shrinkItem = self
            if text:
                alert_height = int(height.toString())
                shrinkItem.resize(self.width(), alert_height)
                shrinkItem.setVisible(True)
                if self.alertTab.location == 1:
                    shrinkItem.move(self.screen[u'size'].left(),
                    (self.screen[u'size'].height() - alert_height) / 2)
                elif self.alertTab.location == 2:
                    shrinkItem.move(self.screen[u'size'].left(),
                        self.screen[u'size'].height() - alert_height)
            else:
                shrinkItem.setVisible(False)
                self.setGeometry(self.screen[u'size'])

    def directImage(self, name, path, background):
        """
        API for replacement backgrounds so Images are added directly to cache
        """
        self.imageManager.add_image(name, path, u'image', background)
        if hasattr(self, u'serviceItem'):
            self.override[u'image'] = name
            self.override[u'theme'] = self.serviceItem.themedata.theme_name
            self.image(name)
            return True
        return False

    def image(self, name):
        """
        Add an image as the background. The image has already been added
        to the cache.

        `Image`
            The name of the image to be displayed
        """
        log.debug(u'image to display')
        image = self.imageManager.get_image_bytes(name)
        self.resetVideo()
        self.displayImage(image)

    def displayImage(self, image):
        """
        Display an image, as is.
        """
        self.setGeometry(self.screen[u'size'])
        if image:
            js = u'show_image("data:image/png;base64,%s");' % image
        else:
            js = u'show_image("");'
        self.frame.evaluateJavaScript(js)
        # Update the preview frame.
        if self.isLive:
            Receiver.send_message(u'maindisplay_active')

    def resetImage(self):
        """
        Reset the backgound image to the service item image.
        Used after Image plugin has changed the background
        """
        log.debug(u'resetImage')
        if hasattr(self, u'serviceItem'):
            self.displayImage(self.serviceItem.bg_image_bytes)
        else:
            self.displayImage(None)
        # clear the cache
        self.override = {}
        # Update the preview frame.
        if self.isLive:
            Receiver.send_message(u'maindisplay_active')

    def resetVideo(self):
        """
        Used after Video plugin has changed the background
        """
        log.debug(u'resetVideo')
        if self.phononActive:
            self.mediaObject.stop()
            self.mediaObject.clearQueue()
            self.webView.setVisible(True)
            self.videoWidget.setVisible(False)
            self.phononActive = False
        else:
            self.frame.evaluateJavaScript(u'show_video("close");')
        self.override = {}
        # Update the preview frame.
        if self.isLive:
            Receiver.send_message(u'maindisplay_active')

    def videoPlay(self):
        """
        Responds to the request to play a loaded video
        """
        log.debug(u'videoPlay')
        if self.phononActive:
            self.mediaObject.play()
        else:
            self.frame.evaluateJavaScript(u'show_video("play");')
        # show screen
        if self.isLive:
            self.setVisible(True)

    def videoPause(self):
        """
        Responds to the request to pause a loaded video
        """
        log.debug(u'videoPause')
        if self.phononActive:
            self.mediaObject.pause()
        else:
            self.frame.evaluateJavaScript(u'show_video("pause");')

    def videoStop(self):
        """
        Responds to the request to stop a loaded video
        """
        log.debug(u'videoStop')
        if self.phononActive:
            self.mediaObject.stop()
        else:
            self.frame.evaluateJavaScript(u'show_video("stop");')

    def videoVolume(self, volume):
        """
        Changes the volume of a running video
        """
        log.debug(u'videoVolume %d' % volume)
        vol = float(volume) / float(10)
        if self.phononActive:
            self.audio.setVolume(vol)
        else:
            self.frame.evaluateJavaScript(u'show_video(null, null, %s);' %
                str(vol))

    def video(self, videoPath, volume, isBackground=False):
        """
        Loads and starts a video to run with the option of sound
        """
        # We request a background video but have no service Item
        if isBackground and not hasattr(self, u'serviceItem'):
            return False
        if not self.mediaObject:
            self.createMediaObject()
        log.debug(u'video')
        self.webLoaded = True
        self.setGeometry(self.screen[u'size'])
        # We are running a background theme
        self.override[u'theme'] = u''
        self.override[u'video'] = True
        vol = float(volume) / float(10)
        if isBackground or not self.usePhonon:
            js = u'show_video("init", "%s", %s, true); show_video("play");' % \
                (videoPath.replace(u'\\', u'\\\\'), str(vol))
            self.frame.evaluateJavaScript(js)
        else:
            self.phononActive = True
            self.mediaObject.stop()
            self.mediaObject.clearQueue()
            self.mediaObject.setCurrentSource(Phonon.MediaSource(videoPath))
            # Need the timer to trigger set the trigger to 200ms
            # Value taken from web documentation.
            if self.serviceItem.end_time != 0:
                self.mediaObject.setTickInterval(200)
            self.mediaObject.play()
            self.webView.setVisible(False)
            self.videoWidget.setVisible(True)
            self.audio.setVolume(vol)
        # Update the preview frame.
        if self.isLive:
            Receiver.send_message(u'maindisplay_active')
        return True

    def videoState(self, newState, oldState):
        """
        Start the video at a predetermined point.
        """
        if newState == Phonon.PlayingState \
            and oldState != Phonon.PausedState \
            and self.serviceItem.start_time > 0:
            # set start time in milliseconds
            self.mediaObject.seek(self.serviceItem.start_time * 1000)

    def videoFinished(self):
        """
        Blank the Video when it has finished so the final frame is not left
        hanging
        """
        self.videoStop()
        self.hideDisplay(HideMode.Blank)
        self.phononActive = False
        self.videoHide = True

    def videoTick(self, tick):
        """
        Triggered on video tick every 200 milli seconds
        """
        if tick > self.serviceItem.end_time * 1000:
            self.videoFinished()

    def isWebLoaded(self):
        """
        Called by webView event to show display is fully loaded
        """
        log.debug(u'Webloaded')
        self.webLoaded = True

    def preview(self):
        """
        Generates a preview of the image displayed.
        """
        log.debug(u'preview for %s', self.isLive)
        Receiver.send_message(u'openlp_process_events')
        # We must have a service item to preview
        if self.isLive and hasattr(self, u'serviceItem'):
            # Wait for the fade to finish before geting the preview.
            # Important otherwise preview will have incorrect text if at all!
            if self.serviceItem.themedata and \
                self.serviceItem.themedata.display_slide_transition:
                while self.frame.evaluateJavaScript(u'show_text_complete()') \
                    .toString() == u'false':
                    Receiver.send_message(u'openlp_process_events')
        # Wait for the webview to update before geting the preview.
        # Important otherwise first preview will miss the background !
        while not self.webLoaded:
            Receiver.send_message(u'openlp_process_events')
        # if was hidden keep it hidden
        if self.isLive:
            if self.hideMode:
                self.hideDisplay(self.hideMode)
            else:
                # Single screen active
                if self.screens.display_count == 1:
                    # Only make visible if setting enabled
                    if QtCore.QSettings().value(u'general/display on monitor',
                        QtCore.QVariant(True)).toBool():
                        self.setVisible(True)
                else:
                    self.setVisible(True)
        preview = QtGui.QPixmap(self.screen[u'size'].width(),
            self.screen[u'size'].height())
        painter = QtGui.QPainter(preview)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.frame.render(painter)
        painter.end()
        return preview

    def buildHtml(self, serviceItem, image=None):
        """
        Store the serviceItem and build the new HTML from it. Add the
        HTML to the display
        """
        log.debug(u'buildHtml')
        self.webLoaded = False
        self.initialFrame = None
        self.serviceItem = serviceItem
        background = None
        # We have an image override so keep the image till the theme changes
        if self.override:
            # We have an video override so allow it to be stopped
            if u'video' in self.override:
                Receiver.send_message(u'video_background_replaced')
                self.override = {}
            # We have a different theme.
            elif self.override[u'theme'] != serviceItem.themedata.theme_name:
                Receiver.send_message(u'live_theme_changed')
                self.override = {}
            else:
                # replace the background
                background = self.imageManager. \
                    get_image_bytes(self.override[u'image'])
        if self.serviceItem.themedata.background_filename:
            self.serviceItem.bg_image_bytes = self.imageManager. \
                get_image_bytes(self.serviceItem.themedata.theme_name)
        if image:
            image_bytes = self.imageManager.get_image_bytes(image)
        else:
            image_bytes = None
        html = build_html(self.serviceItem, self.screen, self.alertTab,
            self.isLive, background, image_bytes)
        log.debug(u'buildHtml - pre setHtml')
        self.webView.setHtml(html)
        log.debug(u'buildHtml - post setHtml')
        if serviceItem.foot_text:
            self.footer(serviceItem.foot_text)
        # if was hidden keep it hidden
        if self.hideMode and self.isLive:
            if QtCore.QSettings().value(u'general/auto unblank',
                QtCore.QVariant(False)).toBool():
                Receiver.send_message(u'slidecontroller_live_unblank')
            else:
                self.hideDisplay(self.hideMode)
        # display hidden for video end we have a new item so must be shown
        if self.videoHide and self.isLive:
            self.videoHide = False
            self.showDisplay()
        self.__hideMouse()

    def footer(self, text):
        """
        Display the Footer
        """
        log.debug(u'footer')
        js = u'show_footer(\'' + \
            text.replace(u'\\', u'\\\\').replace(u'\'', u'\\\'') + u'\')'
        self.frame.evaluateJavaScript(js)

    def hideDisplay(self, mode=HideMode.Screen):
        """
        Hide the display by making all layers transparent
        Store the images so they can be replaced when required
        """
        log.debug(u'hideDisplay mode = %d', mode)
        if self.phononActive:
            self.videoPause()
        if mode == HideMode.Screen:
            self.frame.evaluateJavaScript(u'show_blank("desktop");')
            self.setVisible(False)
        elif mode == HideMode.Blank or self.initialFrame:
            self.frame.evaluateJavaScript(u'show_blank("black");')
        else:
            self.frame.evaluateJavaScript(u'show_blank("theme");')
        if mode != HideMode.Screen:
            if self.isHidden():
                self.setVisible(True)
            if self.phononActive:
                self.webView.setVisible(True)
        self.hideMode = mode

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
        if self.phononActive:
            self.webView.setVisible(False)
            self.videoPlay()
        self.hideMode = None
        # Trigger actions when display is active again
        if self.isLive:
            Receiver.send_message(u'maindisplay_active')

    def __hideMouse(self):
        # Hide mouse cursor when moved over display if enabled in settings
        if QtCore.QSettings().value(u'advanced/hide mouse',
            QtCore.QVariant(False)).toBool():
            self.setCursor(QtCore.Qt.BlankCursor)
            self.frame.evaluateJavaScript('document.body.style.cursor = "none"')
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.frame.evaluateJavaScript('document.body.style.cursor = "auto"')


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
        """
        log.debug(u'AudioPlayer Initialisation started')
        QtCore.QObject.__init__(self, parent)
        self.currentIndex = -1
        self.playlist = []
        self.mediaObject = Phonon.MediaObject()
        self.audioObject = Phonon.AudioOutput(Phonon.VideoCategory)
        Phonon.createPath(self.mediaObject, self.audioObject)
        QtCore.QObject.connect(self.mediaObject,
            QtCore.SIGNAL(u'aboutToFinish()'), self.onAboutToFinish)

    def __del__(self):
        """
        Shutting down so clean up connections
        """
        self.stop()
        for path in self.mediaObject.outputPaths():
            path.disconnect()

    def onAboutToFinish(self):
        """
        Just before the audio player finishes the current track, queue the next
        item in the playlist, if there is one.
        """
        self.currentIndex += 1
        if len(self.playlist) > self.currentIndex:
            self.mediaObject.enqueue(self.playlist[self.currentIndex])

    def connectVolumeSlider(self, slider):
        slider.setAudioOutput(self.audioObject)

    def reset(self):
        """
        Reset the audio player, clearing the playlist and the queue.
        """
        self.currentIndex = -1
        self.playlist = []
        self.stop()
        self.mediaObject.clear()

    def play(self):
        """
        We want to play the file so start it
        """
        log.debug(u'AudioPlayer.play() called')
        if self.currentIndex == -1:
            self.onAboutToFinish()
        self.mediaObject.play()

    def pause(self):
        """
        Pause the Audio
        """
        log.debug(u'AudioPlayer.pause() called')
        self.mediaObject.pause()

    def stop(self):
        """
        Stop the Audio and clean up
        """
        log.debug(u'AudioPlayer.stop() called')
        self.mediaObject.stop()

    def addToPlaylist(self, filenames):
        """
        Add another file to the playlist.

        ``filename``
            The file to add to the playlist.
        """
        if not isinstance(filenames, list):
            filenames = [filenames]
        for filename in filenames:
            self.playlist.append(Phonon.MediaSource(filename))

