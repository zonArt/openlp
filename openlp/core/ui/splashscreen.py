# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from PyQt4 import QtCore, QtGui
from openlp.core.lib import buildIcon

class SplashScreen(object):
    def __init__(self, version):
        self.splash_screen = QtGui.QSplashScreen()
        self.setupUi()
        self.message = self.splash_screen.trUtf8('Starting')\
            + '..... ' + version

    def setupUi(self):
        self.splash_screen.setObjectName(u'splash_screen')
        self.splash_screen.setWindowModality(QtCore.Qt.NonModal)
        self.splash_screen.setEnabled(True)
        self.splash_screen.resize(370, 370)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.splash_screen.sizePolicy().hasHeightForWidth())
        self.splash_screen.setSizePolicy(sizePolicy)
        self.splash_screen.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        icon = buildIcon(u':/icon/openlp-logo-16x16.png')
        self.splash_screen.setWindowIcon(icon)
        splash_image = QtGui.QPixmap(u':/graphics/openlp-splash-screen.png')
        self.splash_screen.setPixmap(splash_image)
        self.splash_screen.setMask(splash_image.mask())
        self.splash_screen.setWindowFlags(
            QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.splash_screen)

    def retranslateUi(self):
        self.splash_screen.setWindowTitle(
            self.splash_screen.trUtf8('Splash Screen'))

    def show(self):
        self.splash_screen.show()
        self.splash_screen.showMessage(self.message,
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.black)
        self.splash_screen.repaint()

    def finish(self, widget):
        self.splash_screen.finish(widget)
