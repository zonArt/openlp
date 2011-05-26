# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Millar, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Jeffrey Smith, Maikel            #
# Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund                    #
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
from openlp.core.lib import Receiver

from PyQt4 import QtCore, QtGui

class SplashScreen(QtGui.QSplashScreen):
    def __init__(self):
        QtGui.QSplashScreen.__init__(self)
        self.setupUi()
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'close_splash'), self.close)

    def setupUi(self):
        self.setObjectName(u'splash_screen')
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        splash_image = QtGui.QPixmap(u':/graphics/openlp-splash-screen.png')
        self.setPixmap(splash_image)
        self.setMask(splash_image.mask())
        self.resize(370, 370)
        QtCore.QMetaObject.connectSlotsByName(self)
