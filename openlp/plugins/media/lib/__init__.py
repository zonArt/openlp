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

class MediaBackends(object):
    """
    An enumeration for possible Backends.
    """
    Webkit = 0
    Phonon = 1
    Vlc = 2

class MediaStates(object):
    """
    An enumeratioin for possible States of the Media Player
    (copied from Phonon::State
    """
    LoadingState = 0
    StoppedState = 1
    PlayingState = 2
    PausedState = 4
    OffState = 6

class MediaController(object):
    """
    Specialiced MediaController class
    to reflect Features of the related backend
    """
    def __init__(self, parent):
        self.parent = parent
        self.state = MediaStates.OffState

    def load(self, display, path, volume):
        pass

    def play(self, display):
        pass

    def pause(self, display):
        pass

    def stop(self, display):
        pass

    def seek(self, display, seekVal):
        pass

    def reset(self, display):
        pass

    def updateUI(self, display):
        pass

    def getSupportedFileTypes(self):
        pass

from mediaitem import MediaMediaItem
from mediatab import MediaTab
from mediacontroller import MediaManager
from webkitcontroller import WebkitController
#from phononcontroller import PhononController
#from vlccontroller import VlcController

__all__ = ['MediaMediaItem']
