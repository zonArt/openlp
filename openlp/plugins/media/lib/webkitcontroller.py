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

import logging

from PyQt4 import QtCore, QtGui, QtWebKit
from openlp.plugins.media.lib import MediaController, MediaState

log = logging.getLogger(__name__)

class WebkitController(MediaController):
    """
    Specialiced MediaController class
    to reflect Features of the QtWebkit backend
    """

    def __init__(self, parent):
        MediaController.__init__(self, parent)
        self.parent = parent
        self.isFlash = False
        self.additional_extensions = {
            u'video/shockwave': [u'.swf']}

    def setup(self, display):
#        if display == self.parent.previewController.previewDisplay or \
#            display == self.parent.liveController.previewDisplay:
#            display.webView.resize(display.size())
        display.webView.raise_()
        self.hasOwnWidget = False

    @staticmethod
    def is_available():
        return True

    def get_supported_file_types(self):
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
        log.debug(u'load vid in Webkit Controller')
        vol = float(volume) / float(10)
        display.webView.setVisible(True)
        if path.endswith(u'.swf'):
            js = u'show_flash("load","%s");' % \
                (path.replace(u'\\', u'\\\\'))
            self.isFlash = True
        else:
            js = u'show_video("init", "%s", %s, false);' % \
                (path.replace(u'\\', u'\\\\'), str(vol))
            self.isFlash = False
        display.frame.evaluateJavaScript(js)
        return True

    def resize(self, display, controller):
        if display == controller.previewDisplay:
            display.webView.resize(display.size())

    def play(self, display):
        self.set_visible(display, True)
        if self.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("play","");')
        else:
            display.frame.evaluateJavaScript(u'show_video("play");')
        self.state = MediaState.Playing

    def pause(self, display):
        if self.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("pause","");')
        else:
            display.frame.evaluateJavaScript(u'show_video("pause");')
        self.state = MediaState.Paused

    def stop(self, display):
        if self.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("stop","");')
        else:
            display.frame.evaluateJavaScript(u'show_video("stop");')
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        if not self.isFlash:
            display.frame.evaluateJavaScript(u'show_video(null, null, %s);' %
                str(vol))

    def seek(self, display, seekVal):
        if not self.isFlash:
            seek = float(seekVal)/1000
            display.frame.evaluateJavaScript( \
                u'show_video("seek", null, null, null, "%f");' % (seek))

    def reset(self, display):
        if self.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("close","");')
        else:
            display.frame.evaluateJavaScript(u'show_video("close");')
        self.state = MediaState.Off

    def set_visible(self, display, status):
        if self.hasOwnWidget:
            display.webView.setVisible(status)

    def update_ui(self, controller, display):
        if not self.isFlash:
            currentTime = display.frame.evaluateJavaScript( \
                u'show_video("currentTime");')
            length = display.frame.evaluateJavaScript(u'show_video("length");')
            if int(currentTime.toFloat()[0]*1000) > 0:
                controller.seekSlider.setMaximum(int(length.toFloat()[0]*1000))
                if not controller.seekSlider.isSliderDown():
                    controller.seekSlider.setSliderPosition( \
                        int(currentTime.toFloat()[0]*1000))

    def get_supported_file_types(self):
        pass
