# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
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
from openlp.core.ui.media import MediaAPI, MediaState

log = logging.getLogger(__name__)

class WebkitAPI(MediaAPI):
    """
    Specialiced MediaAPI class
    to reflect Features of the QtWebkit API
    """

    def __init__(self, parent):
        MediaAPI.__init__(self, parent, u'Webkit')
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

    def getDisplayCss(self):
        """
        Add css style sheets to htmlbuilder
        """
        css = u'''
        #video1 {
            z-index:3;
        }
        #video2 {
            z-index:3;
        }
        #flash {
            z-index:4;
        }
        '''
        return css


    def getDisplayJavascript(self):
        """
        Add javascript functions to htmlbuilder
        """
        js = u'''
        var video_timer = null;
        var current_video = '1';

            function show_video(state, path, volume, loop, seekVal){
                // Note, the preferred method for looping would be to use the
                // video tag loop attribute.
                // But QtWebKit doesn't support this. Neither does it support the
                // onended event, hence the setInterval()
                // In addition, setting the currentTime attribute to zero to restart
                // the video raises an INDEX_SIZE_ERROR: DOM Exception 1
                // To complicate it further, sometimes vid.currentTime stops
                // slightly short of vid.duration and vid.ended is intermittent!
                //
                // Note, currently the background may go black between loops. Not
                // desirable. Need to investigate using two <video>'s, and hiding/
                // preloading one, and toggle between the two when looping.

                if(current_video=='1'){
                    var vid = document.getElementById('video1');
                    var vid2 = document.getElementById('video2');
                } else {
                    var vid = document.getElementById('video2');
                    var vid2 = document.getElementById('video1');
                }
                if(volume != null){
                    vid.volume = volume;
                    vid2.volume = volume;
                }
                switch(state){
                    case 'init':
                        vid.src = path;
                        vid2.src = path;
                        if(loop == null) loop = false;
                        vid.looping = loop;
                        vid2.looping = loop;
                        vid.load();
                        break;
                    case 'load':
                        vid2.style.visibility = 'hidden';
                        vid2.load();
                        break;
                    case 'play':
                        vid.play();
                        vid.style.visibility = 'visible';
                        if(vid.looping){
                            video_timer = setInterval(
                                function() {
                                    show_video('poll');
                                }, 200);
                        }
                        break;
                    case 'pause':
                        if(video_timer!=null){
                            clearInterval(video_timer);
                            video_timer = null;
                        }
                        vid.pause();
                        break;
                    case 'stop':
                        show_video('pause');
                        vid.style.visibility = 'hidden';
                        break;
                    case 'poll':
                        if(vid.ended||vid.currentTime+0.2>vid.duration)
                            show_video('swap');
                        break;
                    case 'swap':
                        show_video('pause');
                        if(current_video=='1')
                            current_video = '2';
                        else
                            current_video = '1';
                        show_video('play');
                        show_video('load');
                        break;
                    case 'close':
                        show_video('stop');
                        vid.src = '';
                        vid2.src = '';
                        break;
                     case 'length':
                        return vid.duration;
                    case 'currentTime':
                        return vid.currentTime;
                    case 'seek':
                        // doesnt work currently
                        //vid.currentTime = seekVal;
                        break;
               }
            }

            function getFlashMovieObject(movieName)
            {
                if (window.document[movieName])
                {
                    return window.document[movieName];
                }
                if (document.embeds && document.embeds[movieName])
                    return document.embeds[movieName];
            }

        // http://www.adobe.com/support/flash/publishexport/scriptingwithflash/scriptingwithflash_03.html
            function show_flash(state, path, volume, seekVal){
                var text = document.getElementById('flash');
                var flashMovie = getFlashMovieObject("OpenLPFlashMovie");
                var src = "src = 'file:///" + path + "'";
                var view_parm = " wmode='opaque'" +
                    " width='" + window.innerWidth + "'" +
                    " height='" + window.innerHeight + "'";
                var swf_parm = " name='OpenLPFlashMovie'" +
                    " autostart='true' loop='false' play='true'" +
                    " hidden='false' swliveconnect='true' allowscriptaccess='always'" +
                    " volume='" + volume + "'";

                switch(state){
                    case 'load':
                        text.innerHTML = "<embed " + src + view_parm + swf_parm + "/>";
                        flashMovie = getFlashMovieObject("OpenLPFlashMovie");
                        text.style.visibility = 'visible';
                        flashMovie.Play();
                        break;
                    case 'play':
                        text.style.visibility = 'visible';
                        flashMovie.Play();
                        break;
                    case 'pause':
                        flashMovie.StopPlay();
                        text.style.visibility = 'hidden';
                        break;
                    case 'stop':
                        flashMovie.StopPlay();
                        text.style.visibility = 'hidden';
                        tempHtml = text.innerHTML;
                        text.innerHTML = '';
                        text.innerHTML = tempHtml;
                        break;
                    case 'close':
                        flashMovie.StopPlay();
                        text.style.visibility = 'hidden';
                        text.innerHTML = '';
                        break;
                    case 'length':
                        return flashMovie.TotalFrames();
                    case 'currentTime':
                        return flashMovie.CurrentFrame();
                    case 'seek':
        //                flashMovie.GotoFrame(seekVal);
                        break;
                }
            }
        '''
        return js


    def getDisplayHtml(self):
        """
        Add html code to htmlbuilder
        """
        html = u'''
        <video id="video1" class="size" style="visibility:hidden" autobuffer preload>
        </video>
        <video id="video2" class="size" style="visibility:hidden" autobuffer preload>
        </video>
        <div id="flash" class="size" style="visibility:hidden"></div>
        '''
        return html

    def setup(self, display):
        display.webView.resize(display.size())
        display.webView.raise_()
        self.hasOwnWidget = False
        #display.webView.hide()

    def check_available(self):
        return True

    def load(self, display):
        log.debug(u'load vid in Webkit Controller')
        controller = display.controller
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
        controller = display.controller
        display.webView.resize(display.size())

    def play(self, display):
        controller = display.controller
        display.webLoaded = True
        self.set_visible(display, True)
        if controller.media_info.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("play");')
        else:
            display.frame.evaluateJavaScript(u'show_video("play");')
        self.state = MediaState.Playing

    def pause(self, display):
        controller = display.controller
        if controller.media_info.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("pause");')
        else:
            display.frame.evaluateJavaScript(u'show_video("pause");')
        self.state = MediaState.Paused

    def stop(self, display):
        controller = display.controller
        if controller.media_info.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("stop");')
        else:
            display.frame.evaluateJavaScript(u'show_video("stop");')
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        controller = display.controller
        # 1.0 is the highest value
        if display.hasVolume:
            vol = float(vol) / float(100)
            if not controller.media_info.isFlash:
                display.frame.evaluateJavaScript(
                    u'show_video(null, null, %s);' % str(vol))

    def seek(self, display, seekVal):
        controller = display.controller
        if controller.media_info.isFlash:
            seek = seekVal
            display.frame.evaluateJavaScript( \
                u'show_flash("seek", null, null, "%s");' % (seek))
        else:
            seek = float(seekVal)/1000
            display.frame.evaluateJavaScript( \
                u'show_video("seek", null, null, null, "%f");' % (seek))

    def reset(self, display):
        controller = display.controller
        if controller.media_info.isFlash:
            display.frame.evaluateJavaScript(u'show_flash("close");')
        else:
            display.frame.evaluateJavaScript(u'show_video("close");')
        self.state = MediaState.Off

    def set_visible(self, display, status):
        if self.hasOwnWidget:
            display.webView.setVisible(status)

    def update_ui(self, display):
        controller = display.controller
        if controller.media_info.isFlash:
            currentTime = display.frame.evaluateJavaScript( \
                u'show_flash("currentTime");').toInt()[0]
            length = display.frame.evaluateJavaScript( \
                u'show_flash("length");').toInt()[0]
        else:
            (currentTime, ok) = display.frame.evaluateJavaScript( \
                u'show_video("currentTime");').toFloat()
            # check if conversion was ok and value is not 'NaN'
            if ok and currentTime == currentTime:
                currentTime = int(currentTime*1000)
            (length, ok) = display.frame.evaluateJavaScript( \
                u'show_video("length");').toFloat()
            # check if conversion was ok and value is not 'NaN'
            if ok and length == length:
                length = int(length*1000)
        if currentTime > 0:
            controller.seekSlider.setMaximum(length)
            if not controller.seekSlider.isSliderDown():
                controller.seekSlider.setSliderPosition(currentTime)
