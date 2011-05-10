#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
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

from PyQt4.phonon import Phonon

from openlp.plugins.media.lib import MediaController, MediaState

class PhononController(MediaController):
    """
    Specialiced MediaController class
    to reflect Features of the Phonon backend
    """

    def __init__(self, parent):
        MediaController.__init__(self, parent)
        self.parent = parent
        self.additional_extensions = {
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
            u'video/x-ms-wmv': [u'.wmv']}


    def load(self, display, path, volume):
        print "load vid in Phonon Controller"
        display.phononActive = True
        display.mediaObject.stop()
        display.mediaObject.clearQueue()
        display.mediaObject.setCurrentSource(Phonon.MediaSource(path))
        # Need the timer to trigger set the trigger to 200ms
        # Value taken from web documentation.
        vol = float(volume) / float(10)
        display.audio.setVolume(vol)

    def resize(self, display):
        display.phononWidget.resize(display.size())

    def play(self, display):
        vol = float(display.parent.volume) / float(10)
        display.audio.setVolume(vol)
        display.mediaObject.play()
        self.state = MediaState.Playing

    def pause(self, display):
        display.mediaObject.pause()
        self.state = MediaState.Paused

    def stop(self, display):
        display.mediaObject.stop()
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        display.audio.setVolume(vol)

    def seek(self, display, seekVal):
        display.mediaObject.seek(seekVal)

    def reset(self, display):
        display.mediaObject.stop()
        display.mediaObject.clearQueue()
        display.phononWidget.setVisible(False)
        #display.webView.setVisible(True)

    def update_ui(self, controller, display):
        controller.seekSlider.setMaximum(display.mediaObject.totalTime())
        if not controller.seekSlider.isSliderDown():
            controller.seekSlider.setSliderPosition(display.mediaObject.currentTime())
#        if newState == Phonon.Playing \
#            and oldState != Phonon.Paused \
#            and self.serviceItem.start_time > 0:
#            # set start time in milliseconds
#            self.mediaObject.seek(self.serviceItem.start_time * 1000)

    def get_supported_file_types(self):
        pass
