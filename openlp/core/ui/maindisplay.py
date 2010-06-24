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

from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

from openlp.core.lib import Receiver, resize_image
from openlp.core.ui import HideMode

log = logging.getLogger(__name__)

class DisplayManager(QtGui.QWidget):
    """
    Wrapper class to hold the display widgets.
    I will provide API's in future to access the screens allow for
    extra displays to be added.
    RenderManager is poked in by MainWindow
    """
    def __init__(self, screens):
        QtGui.QWidget.__init__(self)
        self.screens = screens
        self.videoDisplay = VideoDisplay(self, screens)
        self.audioPlayer = AudioPlayer(self)
        self.mainDisplay = MainDisplay(self, screens)

    def setup(self):
        self.videoDisplay.setup()
        self.mainDisplay.setup()

    def close(self):
        self.videoDisplay.close()
        self.audioPlayer.close()
        self.mainDisplay.close()


class DisplayWidget(QtGui.QGraphicsView):
    """
    Customised version of QTableWidget which can respond to keyboard
    events.
    """
    log.info(u'MainDisplay loaded')

    def __init__(self, parent=None, name=None):
        QtGui.QWidget.__init__(self, None)
        self.parent = parent
        self.hotkey_map = {
            QtCore.Qt.Key_Return: 'servicemanager_next_item',
            QtCore.Qt.Key_Space: 'slidecontroller_live_next_noloop',
            QtCore.Qt.Key_Enter: 'slidecontroller_live_next_noloop',
            QtCore.Qt.Key_0: 'servicemanager_next_item',
            QtCore.Qt.Key_Backspace: 'slidecontroller_live_previous_noloop'}

    def keyPressEvent(self, event):
        if isinstance(event, QtGui.QKeyEvent):
            #here accept the event and do something
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
                self.resetDisplay()
                event.accept()
            event.ignore()
        else:
            event.ignore()

class MainDisplay(DisplayWidget):
    """
    This is the form that is used to display things on the projector.
    """
    log.info(u'MainDisplay Loaded')

    def __init__(self, parent, screens):
        """
        The constructor for the display form.

        ``parent``
            The parent widget.

        ``screens``
            The list of screens.
        """
        log.debug(u'Initialisation started')
        DisplayWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.parent = parent
        # WA_TranslucentBackground is not available in QT4.4
        try:
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        except AttributeError:
            pass
        self.screens = screens
        self.setupScene()
        self.setupImage()
        self.setupText()
        self.setupAlert()
        self.setupBlank()
        self.primary = True
        self.blankFrame = None
        self.frame = None
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'videodisplay_start'), self.hideDisplayForVideo)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'maindisplay_hide'), self.hideDisplay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'maindisplay_show'), self.showDisplay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'videodisplay_background'), self.hideDisplayForVideo)
        self.setVisible(False)

    def setup(self):
        """
        Sets up the screen on a particular screen.
        """
        log.debug(u'Setup %s for %s ' % (
            self.screens, self.screens.monitor_number))
        self.setVisible(False)
        self.screen = self.screens.current
        #Sort out screen locations and sizes
        self.setGeometry(self.screen[u'size'])
        self.scene.setSceneRect(0,0,self.size().width(), self.size().height())
        #Build a custom splash screen
        self.InitialFrame = QtGui.QImage(
            self.screen[u'size'].width(),
            self.screen[u'size'].height(),
            QtGui.QImage.Format_ARGB32_Premultiplied)
        splash_image = QtGui.QImage(u':/graphics/openlp-splash-screen.png')
        painter_image = QtGui.QPainter()
        painter_image.begin(self.InitialFrame)
        painter_image.fillRect(self.InitialFrame.rect(), QtCore.Qt.white)
        painter_image.drawImage(
            (self.screen[u'size'].width() - splash_image.width()) / 2,
            (self.screen[u'size'].height() - splash_image.height()) / 2,
            splash_image)
        self.display_image.setPixmap(QtGui.QPixmap.fromImage(self.InitialFrame))
        self.repaint()
        #Build a Black screen
        painter = QtGui.QPainter()
        self.blankFrame = QtGui.QImage(
            self.screen[u'size'].width(),
            self.screen[u'size'].height(),
            QtGui.QImage.Format_ARGB32_Premultiplied)
        painter.begin(self.blankFrame)
        painter.fillRect(self.blankFrame.rect(), QtCore.Qt.black)
        #build a blank transparent image
        self.transparent = QtGui.QPixmap(
            self.screen[u'size'].width(), self.screen[u'size'].height())
        self.transparent.fill(QtCore.Qt.transparent)
#        self.display_alert.setPixmap(self.transparent)
#        self.display_text.setPixmap(self.transparent)
        #self.frameView(self.transparent)
        # To display or not to display?
        if not self.screen[u'primary']:
            self.setVisible(True)
            self.primary = False
        else:
            self.setVisible(False)
            self.primary = True

    def setupScene(self):
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setSceneRect(0,0,self.size().width(), self.size().height())
        self.setScene(self.scene)

    def setupImage(self):
        self.display_image = QtGui.QGraphicsPixmapItem()
        self.display_image.setZValue(2)
        self.scene.addItem(self.display_image)

    def setupText(self):
        #self.display_text = QtGui.QGraphicsTextItem()
        self.display_text = QtGui.QGraphicsPixmapItem()
        #self.display_text.setPos(0,self.size().height()/2)
        #self.display_text.setTextWidth(self.size().width())
        self.display_text.setZValue(4)
        self.scene.addItem(self.display_text)

    def setupAlert(self):
        self.alertText = QtGui.QGraphicsTextItem()
        self.alertText.setPos(0,self.size().height()/2)
        self.alertText.setPos(0,self.size().height() - 76)
        self.alertText.setTextWidth(self.size().width())
        self.alertText.setZValue(8)
        self.scene.addItem(self.alertText)

    def setupBlank(self):
        self.display_blank = QtGui.QGraphicsPixmapItem()
        self.display_blank.setZValue(10)
        self.scene.addItem(self.display_blank)

    def resetDisplay(self):
        log.debug(u'resetDisplay')
        Receiver.send_message(u'slidecontroller_live_stop_loop')
        if self.primary:
            self.setVisible(False)
        else:
            self.showFullScreen()

    def hideDisplayForVideo(self):
        """
        Hides the main display if for the video to be played
        """
        self.hideDisplay(HideMode.Screen)

    def hideDisplay(self, mode=HideMode.Screen):
        """
        Hide the display by making all layers transparent
        Store the images so they can be replaced when required
        """
        log.debug(u'hideDisplay mode = %d', mode)
        self.storeImage = QtGui.QPixmap(self.display_image.pixmap())
        self.storeText = QtGui.QPixmap(self.display_text.pixmap())
        #self.display_alert.setPixmap(self.transparent)
        #self.display_text.setPixmap(self.transparent)
        if mode == HideMode.Screen:
            #self.display_image.setPixmap(self.transparent)
            self.setVisible(False)
        elif mode == HideMode.Blank:
            self.display_blank.setPixmap(
                QtGui.QPixmap.fromImage(self.blankFrame))
        else:
            if self.parent.renderManager.renderer.bg_frame:
                self.display_blank.setPixmap(QtGui.QPixmap.fromImage(
                    self.parent.renderManager.renderer.bg_frame))
            else:
                self.display_blank.setPixmap(
                    QtGui.QPixmap.fromImage(self.blankFrame))

    def showDisplay(self):
        """
        Show the stored layers so the screen reappears as it was
        originally.
        Make the stored images None to release memory.
        """
        log.debug(u'showDisplay')
        if self.storeImage:
            self.display_image.setPixmap(self.storeImage)
        if self.storeText:
            self.display_text.setPixmap(self.storeText)
        #self.display_alert.setPixmap(self.transparent)
        self.storeImage = None
        self.store = None
        Receiver.send_message(u'maindisplay_active')

    def addImageWithText(self, frame):
        log.debug(u'addImageWithText')
        frame = resize_image(
            frame, self.screen[u'size'].width(), self.screen[u'size'].height())
        self.display_image.setPixmap(QtGui.QPixmap.fromImage(frame))

    def setAlertSize(self, top, height):
        log.debug(u'setAlertSize')
#        self.display_alert.setGeometry(
#            QtCore.QRect(0, top,
#                        self.screen[u'size'].width(), height))

    def addAlertImage(self, frame, blank=False):
        log.debug(u'addAlertImage')
        if blank:
            self.display_alert.setPixmap(self.transparent)
        else:
            self.display_alert.setPixmap(frame)

    def frameView(self, frame, transition=False, display=True):
        """
        Called from a slide controller to display a frame
        if the alert is in progress the alert is added on top
        ``frame``
            Image frame to be rendered
        """
        log.debug(u'frameView %d' % display)
        print "display ", display
        if display:
            if transition:
                if self.frame is not None:
                    self.display_text.setPixmap(
                        QtGui.QPixmap.fromImage(self.frame))
                    self.update()
                self.frame = None
                if frame[u'trans'] is not None:
                    self.display_text.setPixmap(
                        QtGui.QPixmap.fromImage(frame[u'trans']))
                    self.repaint()
                    self.frame = frame[u'trans']
                self.display_text.setPixmap(
                    QtGui.QPixmap.fromImage(frame[u'main']))
                self.display_frame = frame[u'main']
                self.repaint()
            else:
                if isinstance(frame, QtGui.QPixmap):
                    self.display_text.setPixmap(frame)
                else:
                    self.display_text.setPixmap(QtGui.QPixmap.fromImage(frame))
                self.display_frame = frame
            if not self.isVisible() and self.screens.display:
                self.setVisible(True)
                self.showFullScreen()
        else:
            self.storeText = QtGui.QPixmap.fromImage(frame[u'main'])

class VideoDisplay(Phonon.VideoWidget):
    """
    This is the form that is used to display videos on the projector.
    """
    log.info(u'VideoDisplay Loaded')

    def __init__(self, parent, screens,
        aspect=Phonon.VideoWidget.AspectRatioWidget):
        """
        The constructor for the display form.

        ``parent``
            The parent widget.

        ``screens``
            The list of screens.
        """
        log.debug(u'VideoDisplay Initialisation started')
        Phonon.VideoWidget.__init__(self)
        self.setWindowTitle(u'OpenLP Video Display')
        self.parent = parent
        self.screens = screens
        self.hidden = False
        self.message = None
        self.mediaObject = Phonon.MediaObject()
        self.setAspectRatio(aspect)
        self.audioObject = Phonon.AudioOutput(Phonon.VideoCategory)
        Phonon.createPath(self.mediaObject, self)
        Phonon.createPath(self.mediaObject, self.audioObject)
        flags = QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog
#        # WindowsStaysOnBottomHint is not available in QT4.4
#        try:
#            flags = flags | QtCore.Qt.WindowStaysOnBottomHint
#        except AttributeError:
#            pass
        self.setWindowFlags(flags)

        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'maindisplay_hide'), self.mediaHide)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'maindisplay_show'), self.mediaShow)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'videodisplay_start'), self.onMediaQueue)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'videodisplay_play'), self.onMediaPlay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'videodisplay_pause'), self.onMediaPause)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'videodisplay_stop'), self.onMediaStop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'videodisplay_background'), self.onMediaBackground)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_updated'), self.setup)
        QtCore.QObject.connect(self.mediaObject,
            QtCore.SIGNAL(u'finished()'), self.onMediaBackground)
        self.setVisible(False)

    def keyPressEvent(self, event):
        if isinstance(event, QtGui.QKeyEvent):
            #here accept the event and do something
            if event.key() == QtCore.Qt.Key_Escape:
                self.onMediaStop()
                event.accept()
            event.ignore()
        else:
            event.ignore()

    def setup(self):
        """
        Sets up the screen on a particular screen.
        """
        log.debug(u'VideoDisplay Setup %s for %s ' % (self.screens,
             self.screens.monitor_number))
        self.screen = self.screens.current
        #Sort out screen locations and sizes
        self.setGeometry(self.screen[u'size'])
        # To display or not to display?
        if not self.screen[u'primary']: # and self.isVisible():
            #self.showFullScreen()
            self.setVisible(False)
            self.primary = False
        else:
            self.setVisible(False)
            self.primary = True

    def closeEvent(self, event):
        """
        Shutting down so clean up connections
        """
        self.onMediaStop()
        for pth in self.outputPaths():
          disconnected = pth.disconnect()

    def onMediaBackground(self, message=None):
        """
        Play a video triggered from the video plugin with the
        file name passed in on the event.
        Also triggered from the Finish event so the video will loop
        if it is triggered from the plugin
        """
        log.debug(u'VideoDisplay Queue new media message %s' % message)
        #If not file take the stored one
        if not message:
            message = self.message
        # still no file name then stop as it was a normal video stopping
        if message:
            self.mediaObject.setCurrentSource(Phonon.MediaSource(message))
            self.message = message
            self._play()

    def onMediaQueue(self, message):
        """
        Set up a video to play from the serviceitem.
        """
        log.debug(u'VideoDisplay Queue new media message %s' % message)
        file = os.path.join(message[0].get_frame_path(),
            message[0].get_frame_title())
        self.mediaObject.setCurrentSource(Phonon.MediaSource(file))
        self._play()

    def onMediaPlay(self):
        """
        Respond to the Play button on the slide controller unless the display
        has been hidden by the slidecontroller
        """
        if not self.hidden:
            log.debug(u'VideoDisplay Play the new media, Live ')
            self._play()

    def _play(self):
        """
        We want to play the video so start it and display the screen
        """
        log.debug(u'VideoDisplay _play called')
        self.mediaObject.play()
        self.setVisible(True)
        #self.showFullScreen()

    def onMediaPause(self):
        """
        Pause the video and refresh the screen
        """
        log.debug(u'VideoDisplay Media paused by user')
        self.mediaObject.pause()
        self.show()

    def onMediaStop(self):
        """
        Stop the video and clean up
        """
        log.debug(u'VideoDisplay Media stopped by user')
        self.message = None
        self.mediaObject.stop()
        self.onMediaFinish()

    def onMediaFinish(self):
        """
        Clean up the Object queue
        """
        log.debug(u'VideoDisplay Reached end of media playlist')
        self.mediaObject.clearQueue()
        self.setVisible(False)

    def mediaHide(self):
        """
        Hide the video display
        """
        self.mediaObject.pause()
        self.hidden = True
        self.setVisible(False)

    def mediaShow(self):
        """
        Show the video disaply if it was already hidden
        """
        if self.hidden:
            self.hidden = False
            self._play()

class AudioPlayer(QtCore.QObject):
    """
    This Class will play audio only allowing components to work witn a
    soundtrack which does not take over the user interface.
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
        QtCore.QObject.__init__(self)
        self.parent = parent
        self.message = None
        self.mediaObject = Phonon.MediaObject()
        self.audioObject = Phonon.AudioOutput(Phonon.VideoCategory)
        Phonon.createPath(self.mediaObject, self.audioObject)

#        QtCore.QObject.connect(Receiver.get_receiver(),
#            QtCore.SIGNAL(u'videodisplay_start'), self.onMediaQueue)
#        QtCore.QObject.connect(Receiver.get_receiver(),
#            QtCore.SIGNAL(u'videodisplay_play'), self.onMediaPlay)
#        QtCore.QObject.connect(Receiver.get_receiver(),
#            QtCore.SIGNAL(u'videodisplay_pause'), self.onMediaPause)
#        QtCore.QObject.connect(Receiver.get_receiver(),
#            QtCore.SIGNAL(u'videodisplay_stop'), self.onMediaStop)
#        QtCore.QObject.connect(Receiver.get_receiver(),
#            QtCore.SIGNAL(u'videodisplay_background'), self.onMediaBackground)
#        QtCore.QObject.connect(Receiver.get_receiver(),
#            QtCore.SIGNAL(u'config_updated'), self.setup)
#        QtCore.QObject.connect(self.mediaObject,
#            QtCore.SIGNAL(u'finished()'), self.onMediaBackground)

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
        for pth in self.mediaObject.outputPaths():
            disconnected = pth.disconnect()

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
