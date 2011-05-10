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

from openlp.plugins.media.lib import MediaController, MediaState

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

    def load(self, display, path, volume):
        print "load vid in Webkit Controller"
        vol = float(volume) / float(10)
        display.webView.setVisible(True)
        display.phononWidget.setVisible(False)
        display.vlcWidget.setVisible(False)
        if path.endswith(u'.swf'):
            js = u'show_flash("load","%s");' % \
                (path.replace(u'\\', u'\\\\'))
            self.isFlash = True
        else:
            js = u'show_video("init", "%s", %s, false);' % \
                (path.replace(u'\\', u'\\\\'), str(vol))
            self.isFlash = False
        display.frame.evaluateJavaScript(js)

    def resize(self, display, controller):
        if display == controller.previewDisplay:
            print display.size()
            display.webView.resize(display.size())

    def play(self, display):
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
            display.frame.evaluateJavaScript(u'show_video("seek", "%f");' % (float(seekVal)/1000))

    def reset(self, display):
        if self.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("close","");')
        else:
            display.frame.evaluateJavaScript(u'show_video("close");')

    def update_ui(self, controller, display):
        return
        if not self.isFlash:
            length = display.frame.evaluateJavaScript(u'show_video("length");')
            controller.seekSlider.setMaximum(length.toFloat()[0]*1000)
            if not controller.seekSlider.isSliderDown():
                currentTime = display.frame.evaluateJavaScript(u'show_video("currentTime");')
                controller.seekSlider.setSliderPosition(currentTime.toFloat()[0]*1000)

    def get_supported_file_types(self):
        pass
