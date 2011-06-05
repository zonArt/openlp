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

from openlp.core.lib import OpenLPToolbar, translate
from openlp.plugins.media.lib import MediaAPI, MediaState

log = logging.getLogger(__name__)

class WebkitAPI(MediaAPI):
    """
    Specialiced MediaAPI class
    to reflect Features of the QtWebkit API
    """

    def __init__(self, parent):
        MediaAPI.__init__(self, parent)
        self.parent = parent
        self.canBackground = True
        self.video_extensions_list = [
             u'*.3gp'
            , u'*.3gpp'
            , u'*.3g2'
            , u'*.3gpp2'
            , u'*.aac'
            , u'*.flv'
            , u'*.f4a'
            , u'*.f4b'
            , u'*.f4p'
            , u'*.f4v'
            , u'*.mov'
            , u'*.m4a'
            , u'*.m4b'
            , u'*.m4p'
            , u'*.m4v'
            , u'*.mkv'
            , u'*.mp4'
            , u'*.mp3'
            , u'*.ogg'
            , u'*.ogv'
            , u'*.webm'
            , u'*.swf', u'*.mpg', u'*.wmv',  u'*.mpeg', u'*.avi'
        ]

    def setup_controls(self, controller, control_panel):
        # no special controls
        pass

    def setup(self, display):
        display.webView.raise_()
        self.hasOwnWidget = False

    @staticmethod
    def is_available():
        return True

    def get_supported_file_types(self):
        pass

    def load(self, display):
        log.debug(u'load vid in Webkit Controller')
        controller = display.parent
        volume = controller.media_info.volume
        vol = float(volume) / float(100)
        path = controller.media_info.file_info.absoluteFilePath()
        if controller.media_info.is_background:
            loop = u'true'
        else:
            loop = u'false'
        display.webView.setVisible(True)
        if controller.media_info.file_info.suffix() == u'swf':
            controller.media_info.isFlash = True
            js = u'show_flash("load","%s");' % \
                (path.replace(u'\\', u'\\\\'))
        else:
            js = u'show_video("init", "%s", %s, %s);' % \
                (path.replace(u'\\', u'\\\\'), str(vol), loop)
        display.frame.evaluateJavaScript(js)
        return True

    def resize(self, display):
        controller = display.parent
        if display == controller.previewDisplay:
            display.webView.resize(display.size())

    def play(self, display):
        controller = display.parent
        #display.override[u'theme'] = u''
        #display.override[u'video'] = True
        display.webLoaded = True
        self.set_visible(display, True)
        if controller.media_info.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("play");')
        else:
            display.frame.evaluateJavaScript(u'show_video("play");')
        self.state = MediaState.Playing

    def pause(self, display):
        controller = display.parent
        if controller.media_info.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("pause");')
        else:
            display.frame.evaluateJavaScript(u'show_video("pause");')
        self.state = MediaState.Paused

    def stop(self, display):
        controller = display.parent
        if controller.media_info.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("stop");')
        else:
            display.frame.evaluateJavaScript(u'show_video("stop");')
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        controller = display.parent
        # 1.0 is the highest value
        vol = float(vol) / float(100)
        if not controller.media_info.isFlash:
            display.frame.evaluateJavaScript(u'show_video(null, null, %s);' %
                str(vol))

    def seek(self, display, seekVal):
        controller = display.parent
        if controller.media_info.isFlash:
            seek = seekVal
            display.frame.evaluateJavaScript( \
                u'show_flash("seek", null, null, "%s");' % (seek))
        else:
            seek = float(seekVal)/1000
            display.frame.evaluateJavaScript( \
                u'show_video("seek", null, null, null, "%f");' % (seek))

    def reset(self, display):
        controller = display.parent
        if controller.media_info.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("close");')
        else:
            display.frame.evaluateJavaScript(u'show_video("close");')
        self.state = MediaState.Off

    def set_visible(self, display, status):
        if self.hasOwnWidget:
            display.webView.setVisible(status)

    def update_ui(self, display):
        controller = display.parent
        if controller.media_info.isFlash:
            currentTime = display.frame.evaluateJavaScript( \
                u'show_flash("currentTime");').toInt()[0]
            length = display.frame.evaluateJavaScript( \
                u'show_flash("length");').toInt()[0]
        else:
            (currentTime, ok) = display.frame.evaluateJavaScript( \
                u'show_video("currentTime");').toFloat()
            if ok:
                currentTime = int(currentTime*1000)
            (length, ok) = display.frame.evaluateJavaScript( \
                u'show_video("length");').toFloat()
            if ok:
                length = int(length*1000)
        if currentTime > 0:
            controller.seekSlider.setMaximum(length)
            if not controller.seekSlider.isSliderDown():
                controller.seekSlider.setSliderPosition(currentTime)

    def get_supported_file_types(self):
        pass
