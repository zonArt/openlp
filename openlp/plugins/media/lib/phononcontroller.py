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

from openlp.plugins.media.lib import MediaController

class PhononController(MediaController):
    """
    """
    def __init__(self, parent):
        self.parent = parent
        MediaController.__init__(self, parent)

    def load(self, display, path, volume):
        display.phononActive = True
        display.mediaObject.stop()
        display.mediaObject.clearQueue()
        display.mediaObject.setCurrentSource(Phonon.MediaSource(path))
        # Need the timer to trigger set the trigger to 200ms
        # Value taken from web documentation.
        vol = float(volume) / float(10)
        if display.serviceItem.end_time != 0:
            display.mediaObject.setTickInterval(200)
        display.mediaObject.play()
        display.audio.setVolume(vol)
        self.Timer.setInterval(200)


    def play(self, display):
        display.mediaObject.play()
        display.parent.seekSlider.setMaximum(display.mediaObject.totalTime())

    def pause(self, display):
        display.mediaObject.pause()
        self.Timer.stop()

    def stop(self, display):
        display.mediaObject.stop()
        self.Timer.stop()

    def seek(self, display, seekVal):
        print "seek"
        display.mediaObject.seek(seekVal)

    def reset(self, display):
        display.mediaObject.stop()
        display.mediaObject.clearQueue()
        display.webView.setVisible(True)
        display.phononWidget.setVisible(False)
        display.phononActive = False
        self.Timer.stop()

    def updatePlayer(self):
        for controller in self.parent.curDisplayMediaController:
            if controller.getState() == 1:
                pass
