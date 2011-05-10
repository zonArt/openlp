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

import sys

from openlp.plugins.media.lib import MediaController, MediaState

class VlcController(MediaController):
    """
    Specialiced MediaController class
    to reflect Features of the Vlc backend
    """
    def __init__(self, parent):
        MediaController.__init__(self, parent)
        self.parent = parent
        self.supported_file_types = ['avi']
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
        print "load vid in Vlc Controller"
        vol = float(volume) / float(10)

        # create the media
        display.vlcMedia = display.vlcInstance.media_new(unicode(path))
        # put the media in the media player
        display.vlcMediaPlayer.set_media(display.vlcMedia)

        # parse the metadata of the file
        display.vlcMedia.parse()

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform == "linux2": # for Linux using the X Server
            display.vlcMediaPlayer.set_xwindow(int(display.vlcWidget.winId()))
        elif sys.platform == "win32": # for Windows
            display.vlcMediaPlayer.set_hwnd(int(display.vlcWidget.winId()))
        elif sys.platform == "darwin": # for MacOS
            display.vlcMediaPlayer.set_agl(int(display.vlcWidget.winId()))

    def resize(self, display):
        display.vlcWidget.resize(display.size())

    def play(self, display):
        display.vlcMediaPlayer.play()
        self.state = MediaState.Playing

    def pause(self, display):
        display.vlcMediaPlayer.pause()
        self.state = MediaState.Paused

    def stop(self, display):
        display.vlcMediaPlayer.stop()
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        pass

    def seek(self, display, seekVal):
        if display.vlcMediaPlayer.is_seekable():
            display.vlcMediaPlayer.set_position(seekVal/1000.0)

    def reset(self, display):
        display.vlcWidget.setVisible(False)
        #display.webView.setVisible(True)

    def update_ui(self, controller, display):
        controller.seekSlider.setMaximum(1000)
        if not controller.seekSlider.isSliderDown():
            currentPos = display.vlcMediaPlayer.get_position() * 1000
            controller.seekSlider.setSliderPosition(currentPos)

    def get_supported_file_types(self):
        pass
