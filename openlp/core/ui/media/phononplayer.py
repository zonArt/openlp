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
The :mod:`~openlp.core.ui.media.phononplayer` contains the Phonon player component.
"""
import logging
import mimetypes
from datetime import datetime

from PyQt4 import QtGui
from PyQt4.phonon import Phonon

from openlp.core.lib import Settings, translate

from openlp.core.ui.media import MediaState
from openlp.core.ui.media.mediaplayer import MediaPlayer


log = logging.getLogger(__name__)

ADDITIONAL_EXT = {
        u'audio/ac3': [u'.ac3'],
        u'audio/flac': [u'.flac'],
        u'audio/x-m4a': [u'.m4a'],
        u'audio/midi': [u'.mid', u'.midi'],
        u'audio/x-mp3': [u'.mp3'],
        u'audio/mpeg': [u'.mp3', u'.mp2', u'.mpga', u'.mpega', u'.m4a'],
        u'audio/qcelp': [u'.qcp'],
        u'audio/x-wma': [u'.wma'],
        u'audio/x-ms-wma': [u'.wma'],
        u'video/x-flv': [u'.flv'],
        u'video/x-matroska': [u'.mpv', u'.mkv'],
        u'video/x-wmv': [u'.wmv'],
        u'video/x-mpg': [u'.mpg'],
        u'video/mpeg': [u'.mp4', u'.mts', u'.mov'],
        u'video/x-ms-wmv': [u'.wmv']}

VIDEO_CSS = u"""
#videobackboard {
    z-index:3;
    background-color: %(bgcolor)s;
}
#video1 {
    background-color: %(bgcolor)s;
    z-index:4;
}
#video2 {
    background-color: %(bgcolor)s;
    z-index:4;
}
"""


class PhononPlayer(MediaPlayer):
    """
    A specialised version of the MediaPlayer class, which provides a Phonon
    display.
    """

    def __init__(self, parent):
        """
        Constructor
        """
        MediaPlayer.__init__(self, parent, u'phonon')
        self.original_name = u'Phonon'
        self.display_name = u'&Phonon'
        self.parent = parent
        self.additional_extensions = ADDITIONAL_EXT
        mimetypes.init()
        for mimetype in Phonon.BackendCapabilities.availableMimeTypes():
            mimetype = unicode(mimetype)
            if mimetype.startswith(u'audio/'):
                self._addToList(self.audio_extensions_list, mimetype)
            elif mimetype.startswith(u'video/'):
                self._addToList(self.video_extensions_list, mimetype)

    def _addToList(self, mimetype_list, mimetype):
        """
        Add mimetypes to the provided list
        """
        # Add all extensions which mimetypes provides us for supported types.
        extensions = mimetypes.guess_all_extensions(unicode(mimetype))
        for extension in extensions:
            ext = u'*%s' % extension
            if ext not in mimetype_list:
                mimetype_list.append(ext)
        log.info(u'MediaPlugin: %s extensions: %s' % (mimetype, u' '.join(extensions)))
        # Add extensions for this mimetype from self.additional_extensions.
        # This hack clears mimetypes' and operating system's shortcomings
        # by providing possibly missing extensions.
        if mimetype in self.additional_extensions.keys():
            for extension in self.additional_extensions[mimetype]:
                ext = u'*%s' % extension
                if ext not in mimetype_list:
                    mimetype_list.append(ext)
            log.info(u'MediaPlugin: %s additional extensions: %s' %
                (mimetype, u' '.join(self.additional_extensions[mimetype])))

    def setup(self, display):
        """
        Set up the player widgets
        """
        display.phononWidget = Phonon.VideoWidget(display)
        display.phononWidget.resize(display.size())
        display.mediaObject = Phonon.MediaObject(display)
        Phonon.createPath(display.mediaObject, display.phononWidget)
        if display.hasAudio:
            display.audio = Phonon.AudioOutput(Phonon.VideoCategory, display.mediaObject)
            Phonon.createPath(display.mediaObject, display.audio)
        display.phononWidget.raise_()
        display.phononWidget.hide()
        self.hasOwnWidget = True

    def check_available(self):
        """
        Check if the player is available
        """
        return True

    def load(self, display):
        """
        Load a video into the display
        """
        log.debug(u'load vid in Phonon Controller')
        controller = display.controller
        volume = controller.media_info.volume
        path = controller.media_info.file_info.absoluteFilePath()
        display.mediaObject.setCurrentSource(Phonon.MediaSource(path))
        if not self.media_state_wait(display, Phonon.StoppedState):
            return False
        self.volume(display, volume)
        return True

    def media_state_wait(self, display, mediaState):
        """
        Wait for the video to change its state
        Wait no longer than 5 seconds.
        """
        start = datetime.now()
        current_state = display.mediaObject.state()
        while current_state != mediaState:
            current_state = display.mediaObject.state()
            if current_state == Phonon.ErrorState:
                return False
            self.application.process_events()
            if (datetime.now() - start).seconds > 5:
                return False
        return True

    def resize(self, display):
        """
        Resize the display
        """
        display.phononWidget.resize(display.size())

    def play(self, display):
        """
        Play the current media item
        """
        controller = display.controller
        start_time = 0
        if display.mediaObject.state() != Phonon.PausedState and \
            controller.media_info.start_time > 0:
            start_time = controller.media_info.start_time
        display.mediaObject.play()
        if not self.media_state_wait(display, Phonon.PlayingState):
            return False
        if start_time > 0:
            self.seek(display, controller.media_info.start_time * 1000)
        self.volume(display, controller.media_info.volume)
        controller.media_info.length = int(display.mediaObject.totalTime() / 1000)
        controller.seekSlider.setMaximum(controller.media_info.length * 1000)
        self.state = MediaState.Playing
        display.phononWidget.raise_()
        return True

    def pause(self, display):
        """
        Pause the current media item
        """
        display.mediaObject.pause()
        if self.media_state_wait(display, Phonon.PausedState):
            self.state = MediaState.Paused

    def stop(self, display):
        """
        Stop the current media item
        """
        display.mediaObject.stop()
        self.set_visible(display, False)
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        """
        Set the volume
        """
        # 1.0 is the highest value
        if display.hasAudio:
            vol = float(vol) / float(100)
            display.audio.setVolume(vol)

    def seek(self, display, seekVal):
        """
        Go to a particular point in the current media item
        """
        display.mediaObject.seek(seekVal)

    def reset(self, display):
        """
        Reset the media player
        """
        display.mediaObject.stop()
        display.mediaObject.clearQueue()
        self.set_visible(display, False)
        display.phononWidget.setVisible(False)
        self.state = MediaState.Off

    def set_visible(self, display, status):
        """
        Set the visibility of the widget
        """
        if self.hasOwnWidget:
            display.phononWidget.setVisible(status)

    def update_ui(self, display):
        """
        Update the UI
        """
        if display.mediaObject.state() == Phonon.PausedState and self.state != MediaState.Paused:
            self.stop(display)
        controller = display.controller
        if controller.media_info.end_time > 0:
            if display.mediaObject.currentTime() > controller.media_info.end_time * 1000:
                self.stop(display)
                self.set_visible(display, False)
        if not controller.seekSlider.isSliderDown():
            controller.seekSlider.blockSignals(True)
            controller.seekSlider.setSliderPosition(display.mediaObject.currentTime())
            controller.seekSlider.blockSignals(False)

    def get_media_display_css(self):
        """
        Add css style sheets to htmlbuilder
        """
        background = QtGui.QColor(Settings().value(u'players/background color')).name()
        return VIDEO_CSS % {u'bgcolor': background}

    def get_info(self):
        """
        Return some info about this player
        """
        return(translate('Media.player', 'Phonon is a media player which '
            'interacts with the operating system to provide media capabilities.') +
            u'<br/> <strong>' + translate('Media.player', 'Audio') +
            u'</strong><br/>' + unicode(self.audio_extensions_list) +
            u'<br/><strong>' + translate('Media.player', 'Video') +
            u'</strong><br/>' + unicode(self.video_extensions_list) + u'<br/>')
