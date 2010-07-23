# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

from openlp.core.lib import Receiver, resize_image, build_html, ServiceItem, image_to_byte
from openlp.core.ui import HideMode

log = logging.getLogger(__name__)

#http://www.steveheffernan.com/html5-video-player/demo-video-player.html

##        QtCore.QObject.connect(Receiver.get_receiver(),
##            QtCore.SIGNAL(u'maindisplay_hide'), self.hideDisplay)
##        QtCore.QObject.connect(Receiver.get_receiver(),
##            QtCore.SIGNAL(u'maindisplay_show'), self.showDisplay)
##        QtCore.QObject.connect(Receiver.get_receiver(),
##            QtCore.SIGNAL(u'videodisplay_start'), self.onStartVideo)
##        QtCore.QObject.connect(Receiver.get_receiver(),
##            QtCore.SIGNAL(u'videodisplay_stop'), self.onStopVideo)
##        QtCore.QObject.connect(Receiver.get_receiver(),
##            QtCore.SIGNAL(u'config_updated'), self.setup)


class DisplayWidget(QtGui.QGraphicsView):
    """
    Customised version of QTableWidget which can respond to keyboard
    events.
    """
    log.info(u'Display Widget loaded')

    def __init__(self, live, parent=None, name=None):
        QtGui.QGraphicsView.__init__(self)
        self.parent = parent
        self.live = live
#        self.hotkey_map = {
#            QtCore.Qt.Key_Return: 'servicemanager_next_item',
#            QtCore.Qt.Key_Space: 'slidecontroller_live_next_noloop',
#            QtCore.Qt.Key_Enter: 'slidecontroller_live_next_noloop',
#            QtCore.Qt.Key_0: 'servicemanager_next_item',
#            QtCore.Qt.Key_Backspace: 'slidecontroller_live_previous_noloop'}

    def keyPressEvent(self, event):
        # Key events only needed for live
        if not self.live:
            return
#        if isinstance(event, QtGui.QKeyEvent):
#            #here accept the event and do something
#            if event.key() == QtCore.Qt.Key_Up:
#                Receiver.send_message(u'slidecontroller_live_previous')
#                event.accept()
#            elif event.key() == QtCore.Qt.Key_Down:
#                Receiver.send_message(u'slidecontroller_live_next')
#                event.accept()
#            elif event.key() == QtCore.Qt.Key_PageUp:
#                Receiver.send_message(u'slidecontroller_live_first')
#                event.accept()
#            elif event.key() == QtCore.Qt.Key_PageDown:
#                Receiver.send_message(u'slidecontroller_live_last')
#                event.accept()
#            elif event.key() in self.hotkey_map:
#                Receiver.send_message(self.hotkey_map[event.key()])
#                event.accept()
#            elif event.key() == QtCore.Qt.Key_Escape:
#                self.resetDisplay()
#                event.accept()
#            event.ignore()
#        else:
#            event.ignore()

class MainDisplay(DisplayWidget):

    def __init__(self, parent, screens, live):
        DisplayWidget.__init__(self, live, parent=None)
        self.parent = parent
        self.screens = screens
        self.isLive = live
        self.setWindowTitle(u'OpenLP Display')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint)

        self.currvideo = False
        self.video1 = "c:\\users\\jonathan\\Desktop\\Wildlife.wmv"
        self.video2 = "c:\\users\\jonathan\\Desktop\\movie.ogg"
        self.currslide = False
        self.slide1 = "<sup>[1:1]</sup> In the beginning God created the heavens and the earth.<br/><br/><sup> [1:2]</sup> Now the earth was formless and empty, darkness was over the surface of the deep, and the Spirit of God was hovering over the waters.<br/><br/><sup>[1:3]</sup> And God said, \"Let there be light,\" and there was light.<br/><br/><sup>[1:4]</sup> God saw that the light was good, and he separated the light from the darkness.<br/><br/>"
        self.slide2 = "<br /><br />This is the chorus<br />Blah Blah Blah<br />Blah Blah Blah<br />Blah Blah Blah<br />Blah Blah Blah<br />Blah Blah Blah"
        self.alerttext = "<p>Red Alert! Raise Shields!</p>"

    def setup(self):
        log.debug(u'Setup %s for %s ' % (
            self.screens, self.screens.monitor_number))
        self.screen = self.screens.current
        self.setVisible(False)
        self.setGeometry(self.screen[u'size'])
        self.webView = QtWebKit.QWebView(self)
        self.webView.setGeometry(0, 0, self.screen[u'size'].width(), self.screen[u'size'].height())
        self.page = self.webView.page()
        self.frame = self.page.mainFrame()
        QtCore.QObject.connect(self.webView,
            QtCore.SIGNAL(u'loadFinished(bool)'), self.loaded)
        self.frame.setScrollBarPolicy(QtCore.Qt.Vertical,
            QtCore.Qt.ScrollBarAlwaysOff)
        self.frame.setScrollBarPolicy(QtCore.Qt.Horizontal,
            QtCore.Qt.ScrollBarAlwaysOff)
        if self.isLive:
            #Build the initial frame.
            initialFrame = QtGui.QImage(
                self.screens.current[u'size'].width(),
                self.screens.current[u'size'].height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
            splash_image = QtGui.QImage(u':/graphics/openlp-splash-screen.png')
            painter_image = QtGui.QPainter()
            painter_image.begin(initialFrame)
            painter_image.fillRect(initialFrame.rect(), QtCore.Qt.white)
            painter_image.drawImage(
                (self.screens.current[u'size'].width() - splash_image.width()) / 2,
                (self.screens.current[u'size'].height() - splash_image.height()) / 2,
                splash_image)
            serviceItem = ServiceItem()
            serviceItem.bg_frame = initialFrame
            self.webView.setHtml(build_html(serviceItem, self.screen, None))
            self.show()

    def next(self):
        if self.currslide:
            self.frame.evaluateJavaScript("startfade('" + self.slide2 + "')")
            #self.frame.findFirstElement('div#lyrics').setInnerXml(self.slide2)
        else:
            self.frame.evaluateJavaScript("startfade('" + self.slide1 + "')")
            #self.frame.findFirstElement('div#lyrics').setInnerXml(self.slide1)
        self.currslide = not self.currslide

    def text(self, slide):
        print slide
        self.frame.findFirstElement('div#lyrics').setInnerXml(slide)
        return self.preview()

    def alert(self):
        self.frame.findFirstElement('div#alert').setInnerXml(self.alerttext)

    def image(self, image):
        image = resize_image(image, self.screen[u'size'].width(),
            self.screen[u'size'].height())
        self.frame.evaluateJavaScript(
            "document.getElementById('video').style.visibility = 'hidden'")
        self.frame.evaluateJavaScript(
            "document.getElementById('image').style.visibility = 'visible'")
        self.frame.findFirstElement('img').setAttribute(
            'src', unicode('data:image/png;base64,%s' % image_to_byte(image)))

    def reset(self):
        self.frame.findFirstElement('img').setAttribute(
            'src', unicode('data:image/png;base64,%s' % image_to_byte(self.serviceItem.bg_frame)))

    def video(self, videoPath, noSound=False):
        if self.currimage:
            self.frame.findFirstElement('video').setAttribute('src', videoPath)
        self.frame.evaluateJavaScript(
            "document.getElementById('video').style.visibility = 'visible'")
        self.frame.evaluateJavaScript(
            "document.getElementById('image').style.visibility = 'hidden'")
        self.frame.evaluateJavaScript("document.getElementById('video').play()")
        self.currimage = not self.currimage

    def loaded(self):
        self.loaded = True

    def preview(self):
        # Wait for the webview to update before geting the preview.
        # Important otherwise first preview will miss the background !
        while not self.loaded:
            Receiver.send_message(u'openlp_process_events')
        preview = QtGui.QImage(self.screen[u'size'].width(),
            self.screen[u'size'].height(),
            QtGui.QImage.Format_ARGB32_Premultiplied)
        painter = QtGui.QPainter(preview)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.frame.render(painter)
        painter.end()
        if log.isEnabledFor(logging.DEBUG):
            #save preview for debugging
            preview.save("temp.png", "png")
        return preview

    def buildHtml(self, serviceItem):
        """
        Store the serviceItem and build the new HTML from it. Add the
        HTML to the display
        """
        self.loaded = False
        self.serviceItem = serviceItem
        html = build_html(self.serviceItem, self.screen, None)
        self.webView.setHtml(html)
        if serviceItem.footer:
            self.frame.findFirstElement('div#footer').setInnerXml(serviceItem.foot_text)

    def hideDisplay(self, mode=HideMode.Screen):
        """
        Hide the display by making all layers transparent
        Store the images so they can be replaced when required
        """
        log.debug(u'hideDisplay mode = %d', mode)
        #self.displayText.setPixmap(self.transparent)
        if mode == HideMode.Screen:
            #self.display_image.setPixmap(self.transparent)
            self.setVisible(False)
        elif mode == HideMode.Blank:
            self.displayBlank.setPixmap(
                QtGui.QPixmap.fromImage(self.blankFrame))
        else:
            if self.parent.renderManager.renderer.bg_frame:
                self.displayBlank.setPixmap(QtGui.QPixmap.fromImage(
                    self.parent.renderManager.renderer.bg_frame))
            else:
                self.displayBlank.setPixmap(
                    QtGui.QPixmap.fromImage(self.blankFrame))
        if mode != HideMode.Screen and self.isHidden():
            self.setVisible(True)

    def showDisplay(self, message=u''):
        """
        Show the stored layers so the screen reappears as it was
        originally.
        Make the stored images None to release memory.
        """
        log.debug(u'showDisplay')
        self.displayBlank.setPixmap(self.transparent)
        if self.isHidden():
            self.setVisible(True)
        #Trigger actions when display is active again
        Receiver.send_message(u'maindisplay_active')

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
        file = os.path.join(message[0].get_frame_path(),
            message[0].get_frame_title())
        self.mediaObject.setCurrentSource(Phonon.MediaSource(file))
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
