# -*- coding: utf-8 -*-

"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

# Form implementation generated from reading ui file 'openlp/resources/forms/self.splash_screen.ui'
#
# Created: Mon Nov  3 20:17:05 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

from openlp.resources import *

class SplashScreen(object):
    def __init__(self):
        self.splash_screen = QtGui.QSplashScreen()
        self.setupUi()

    def setupUi(self):
        self.splash_screen.setObjectName("splash_screen")
        self.splash_screen.setWindowModality(QtCore.Qt.NonModal)
        self.splash_screen.setEnabled(True)
        self.splash_screen.resize(400, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splash_screen.sizePolicy().hasHeightForWidth())
        self.splash_screen.setSizePolicy(sizePolicy)
        self.splash_screen.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/openlp.org-icon-32.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.splash_screen.setWindowIcon(icon)
        #self.verticalLayout = QtGui.QVBoxLayout(self.splash_screen)
        #self.verticalLayout.setSpacing(0)
        #self.verticalLayout.setMargin(0)
        #self.verticalLayout.setObjectName("verticalLayout")
        #self.SplashImage = QtGui.QLabel(self.splash_screen)
        #self.SplashImage.setPixmap(QtGui.QPixmap(":/graphics/splash-screen-new.bmp"))
        #self.SplashImage.setObjectName("SplashImage")
        #self.verticalLayout.addWidget(self.SplashImage)
        self.splash_screen.setPixmap(QtGui.QPixmap(":/graphics/splash-screen-new.bmp"))
        self.splash_screen.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.splash_screen)

    def retranslateUi(self):
        self.splash_screen.setWindowTitle(QtGui.QApplication.translate("splash_screen", "Splash Screen", None, QtGui.QApplication.UnicodeUTF8))

    def show(self):
        self.splash_screen.show()
        self.splash_screen.showMessage(u'Starting...', QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom,  QtCore.Qt.black)
        self.splash_screen.repaint()

    def finish(self, widget):
        self.splash_screen.finish(widget)
