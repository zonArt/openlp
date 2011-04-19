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

from openlp.plugins.media.lib import MediaController

class WebkitController(MediaController):
    """
    Specialiced MediaController class
    to reflect Features of the QtWebkit backend
    """
    def __init__(self, parent):
        self.parent = parent
        MediaController.__init__(self, parent)
        self.isFlash = False

    def load(self, display, path, volume):
        vol = float(volume) / float(10)
        display.webView.setVisible(True)
        display.phononWidget.setVisible(False)
        if path.endswith(u'.swf'):
            js = u'show_flash("load","%s");' % \
                (path.replace(u'\\', u'\\\\'))
            self.isFlash = True
        else:
            js = u'show_video("init", "%s", %s, false); show_video("play");' % \
                (path.replace(u'\\', u'\\\\'), str(vol))
            self.isFlash = False
        display.frame.evaluateJavaScript(js)

    def play(self, display):
        if self.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("play","");')
        else:
            display.frame.evaluateJavaScript(u'show_video("play");')


    def pause(self, display):
        if self.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("pause","");')
        else:
            display.frame.evaluateJavaScript(u'show_video("pause");')

    def stop(self, display):
        if self.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("stop","");')
        else:
            display.frame.evaluateJavaScript(u'show_video("stop");')

    def seek(self, display, seekVal):
        pass

    def reset(self, display):
        display.frame.evaluateJavaScript(u'show_video("close");')

    def updateUI(self, display):
        pass

    def getSupportedFileTypes(self):
        pass
