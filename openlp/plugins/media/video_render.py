# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
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
import os
from PyQt4 import QtCore, QtGui

# xxx this needs a try, except once we've decided what to do if it fails
from PyQt4.phonon import Phonon

# from openlp.core.lib import Plugin, MediaManagerItem, SettingsTab
# from openlp.plugins.media.lib import MediaTab,MediaMediaItem

"""Renders a video to some surface or other """

class w(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.resize(640,480)
        self.setWindowTitle(u'simple media player')
        self.show()

if __name__==u'__main__':
    app = QtGui.QApplication([])
#     widget = QtGui.QWidget()
#     widget.resize(320, 240)
#     widget.setWindowTitle(u'simple')
#     widget.show()
#     QCore.QCoreApplication.setApplicationName(u'OpenLP')
    mainwindow=w()
    widget=QtGui.QWidget(mainwindow)
    mainwindow.setCentralWidget(widget)
    widget.setLayout(QtGui.QVBoxLayout(widget))
#     videofile=u'r-128.rm'
    videofile=u'/extra_space/Download/coa360download56Kbps240x160.mpg'
    source=Phonon.MediaSource(videofile)

    media=Phonon.MediaObject(widget)
    media.setCurrentSource(source)

    video=Phonon.VideoWidget(widget)
    audio=Phonon.AudioOutput(Phonon.MusicCategory)
#     controller=Phonon.MediaController(media)
    Phonon.createPath(media, video);
    Phonon.createPath(media, audio);
#     player=Phonon.VideoPlayer(Phonon.VideoCategory, widget)
    slider=Phonon.SeekSlider(media, mainwindow)
    widget.layout().addWidget(slider)
    widget.layout().addWidget(video)
    slider.show()
    
    video.show()
    media.play()
    app.exec_()
