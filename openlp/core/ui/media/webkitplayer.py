# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
The :mod:`~openlp.core.ui.media.webkit` module contains our WebKit video player
"""
from PyQt4 import QtGui

import logging

from openlp.core.lib import Settings, translate
from openlp.core.ui.media import MediaState
from openlp.core.ui.media.mediaplayer import MediaPlayer

log = logging.getLogger(__name__)

VIDEO_CSS = u"""
#videobackboard {
    z-index:3;
    background-color: %(bgcolor)s;
}
#video1 {
    background-color: %(bgcolor)s;
    z-index:4;
}
#video2 {
    background-color: %(bgcolor)s;
    z-index:4;
}
"""

VIDEO_JS = u"""
    var video_timer = null;
    var current_video = '1';

    function show_video(state, path, volume, loop, varVal){
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
                vid.src = 'file:///' + path;
                vid2.src = 'file:///' + path;
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
                vid.currentTime = 0;
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
                show_video('load');
                show_video('play');
                show_video('setVisible',null,null,null,'visible');
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
                vid.currentTime = varVal;
                break;
            case 'isEnded':
                return vid.ended;
            case 'setVisible':
                vid.style.visibility = varVal;
                break;
            case 'setBackBoard':
                var back = document.getElementById('videobackboard');
                back.style.visibility = varVal;
                break;
       }
    }
"""

VIDEO_HTML = u"""
<div id="videobackboard" class="size" style="visibility:hidden"></div>
<video id="video1" class="size" style="visibility:hidden" autobuffer preload>
</video>
<video id="video2" class="size" style="visibility:hidden" autobuffer preload>
</video>
"""

FLASH_CSS = u"""
#flash {
    z-index:5;
}
"""

FLASH_JS = u"""
    function getFlashMovieObject(movieName)
    {
        if (window.document[movieName])
        {
            return window.document[movieName];
        }
        if (document.embeds && document.embeds[movieName])
            return document.embeds[movieName];
    }

    function show_flash(state, path, volume, varVal){
        var text = document.getElementById('flash');
        var flashMovie = getFlashMovieObject("OpenLPFlashMovie");
        var src = "src = 'file:///" + path + "'";
        var view_parm = " wmode='opaque'" +
            " width='100%%'" +
            " height='100%%'";
        var swf_parm = " name='OpenLPFlashMovie'" +
            " autostart='true' loop='false' play='true'" +
            " hidden='false' swliveconnect='true' allowscriptaccess='always'" +
            " volume='" + volume + "'";

        switch(state){
            case 'load':
                text.innerHTML = "<embed " + src + view_parm + swf_parm + "/>";
                flashMovie = getFlashMovieObject("OpenLPFlashMovie");
                flashMovie.Play();
                break;
            case 'play':
                flashMovie.Play();
                break;
            case 'pause':
                flashMovie.StopPlay();
                break;
            case 'stop':
                flashMovie.StopPlay();
                tempHtml = text.innerHTML;
                text.innerHTML = '';
                text.innerHTML = tempHtml;
                break;
            case 'close':
                flashMovie.StopPlay();
                text.innerHTML = '';
                break;
            case 'length':
                return flashMovie.TotalFrames();
            case 'currentTime':
                return flashMovie.CurrentFrame();
            case 'seek':
//                flashMovie.GotoFrame(varVal);
                break;
            case 'isEnded':
                return false;//TODO check flash end
            case 'setVisible':
                text.style.visibility = varVal;
                break;
        }
    }
"""

FLASH_HTML = u"""
<div id="flash" class="size" style="visibility:hidden"></div>
"""

VIDEO_EXT = [
    u'*.3gp',
    u'*.3gpp',
    u'*.3g2',
    u'*.3gpp2',
    u'*.aac',
    u'*.flv',
    u'*.f4a',
    u'*.f4b',
    u'*.f4p',
    u'*.f4v',
    u'*.mov',
    u'*.m4a',
    u'*.m4b',
    u'*.m4p',
    u'*.m4v',
    u'*.mkv',
    u'*.mp4',
    u'*.ogv',
    u'*.webm',
    u'*.mpg', u'*.wmv', u'*.mpeg', u'*.avi',
    u'*.swf'
]

AUDIO_EXT = [
    u'*.mp3',
    u'*.ogg'
]


class WebkitPlayer(MediaPlayer):
    """
    A specialised version of the MediaPlayer class, which provides a QtWebKit
    display.
    """

    def __init__(self, parent):
        """
        Constructor
        """
        MediaPlayer.__init__(self, parent, u'webkit')
        self.original_name = u'WebKit'
        self.display_name = u'&WebKit'
        self.parent = parent
        self.canBackground = True
        self.audio_extensions_list = AUDIO_EXT
        self.video_extensions_list = VIDEO_EXT

    def get_media_display_css(self):
        """
        Add css style sheets to htmlbuilder
        """
        background = QtGui.QColor(Settings().value(u'players/background color')).name()
        css = VIDEO_CSS % {u'bgcolor': background}
        return css + FLASH_CSS

    def get_media_display_javascript(self):
        """
        Add javascript functions to htmlbuilder
        """
        return VIDEO_JS + FLASH_JS

    def get_media_display_html(self):
        """
        Add html code to htmlbuilder
        """
        return VIDEO_HTML + FLASH_HTML

    def setup(self, display):
        """
        Set up the player
        """
        display.webView.resize(display.size())
        display.webView.raise_()
        self.hasOwnWidget = False

    def check_available(self):
        """
        Check the availability of the media player
        """
        return True

    def load(self, display):
        """
        Load a video
        """
        log.debug(u'load vid in Webkit Controller')
        controller = display.controller
        if display.hasAudio and not controller.media_info.is_background:
            volume = controller.media_info.volume
            vol = float(volume) / float(100)
        else:
            vol = 0
        path = controller.media_info.file_info.absoluteFilePath()
        if controller.media_info.is_background:
            loop = u'true'
        else:
            loop = u'false'
        display.webView.setVisible(True)
        if controller.media_info.file_info.suffix() == u'swf':
            controller.media_info.is_flash = True
            js = u'show_flash("load","%s");' % (path.replace(u'\\', u'\\\\'))
        else:
            js = u'show_video("init", "%s", %s, %s);' % (path.replace(u'\\', u'\\\\'), str(vol), loop)
        display.frame.evaluateJavaScript(js)
        return True

    def resize(self, display):
        """
        Resize the player
        """
        display.webView.resize(display.size())

    def play(self, display):
        """
        Play a video
        """
        controller = display.controller
        display.webLoaded = True
        length = 0
        start_time = 0
        if self.state != MediaState.Paused and controller.media_info.start_time > 0:
            start_time = controller.media_info.start_time
        self.set_visible(display, True)
        if controller.media_info.is_flash:
            display.frame.evaluateJavaScript(u'show_flash("play");')
        else:
            display.frame.evaluateJavaScript(u'show_video("play");')
        if start_time > 0:
            self.seek(display, controller.media_info.start_time * 1000)
        # TODO add playing check and get the correct media length
        controller.media_info.length = length
        self.state = MediaState.Playing
        display.webView.raise_()
        return True

    def pause(self, display):
        """
        Pause a video
        """
        controller = display.controller
        if controller.media_info.is_flash:
            display.frame.evaluateJavaScript(u'show_flash("pause");')
        else:
            display.frame.evaluateJavaScript(u'show_video("pause");')
        self.state = MediaState.Paused

    def stop(self, display):
        """
        Stop a video
        """
        controller = display.controller
        if controller.media_info.is_flash:
            display.frame.evaluateJavaScript(u'show_flash("stop");')
        else:
            display.frame.evaluateJavaScript(u'show_video("stop");')
        self.state = MediaState.Stopped

    def volume(self, display, vol):
        """
        Set the volume
        """
        controller = display.controller
        # 1.0 is the highest value
        if display.hasAudio:
            vol = float(vol) / float(100)
            if not controller.media_info.is_flash:
                display.frame.evaluateJavaScript(u'show_video(null, null, %s);' % str(vol))

    def seek(self, display, seekVal):
        """
        Go to a position in the video
        """
        controller = display.controller
        if controller.media_info.is_flash:
            seek = seekVal
            display.frame.evaluateJavaScript(u'show_flash("seek", null, null, "%s");' % (seek))
        else:
            seek = float(seekVal) / 1000
            display.frame.evaluateJavaScript(u'show_video("seek", null, null, null, "%f");' % (seek))

    def reset(self, display):
        """
        Reset the player
        """
        controller = display.controller
        if controller.media_info.is_flash:
            display.frame.evaluateJavaScript(u'show_flash("close");')
        else:
            display.frame.evaluateJavaScript(u'show_video("close");')
        self.state = MediaState.Off

    def set_visible(self, display, status):
        """
        Set the visibility
        """
        controller = display.controller
        if status:
            is_visible = "visible"
        else:
            is_visible = "hidden"
        if controller.media_info.is_flash:
            display.frame.evaluateJavaScript(u'show_flash("setVisible", null, null, "%s");' % (is_visible))
        else:
            display.frame.evaluateJavaScript(u'show_video("setVisible", null, null, null, "%s");' % (is_visible))

    def update_ui(self, display):
        """
        Update the UI
        """
        controller = display.controller
        if controller.media_info.is_flash:
            currentTime = display.frame.evaluateJavaScript(u'show_flash("currentTime");')
            length = display.frame.evaluateJavaScript(u'show_flash("length");')
        else:
            if display.frame.evaluateJavaScript(u'show_video("isEnded");') == 'true':
                self.stop(display)
            currentTime = display.frame.evaluateJavaScript(u'show_video("currentTime");')
            # check if conversion was ok and value is not 'NaN'
            if currentTime and currentTime != float('inf'):
                currentTime = int(currentTime * 1000)
            length = display.frame.evaluateJavaScript(u'show_video("length");')
            # check if conversion was ok and value is not 'NaN'
            if length and length != float('inf'):
                length = int(length * 1000)
        if currentTime > 0:
            controller.media_info.length = length
            controller.seekSlider.setMaximum(length)
            if not controller.seekSlider.isSliderDown():
                controller.seekSlider.blockSignals(True)
                controller.seekSlider.setSliderPosition(currentTime)
                controller.seekSlider.blockSignals(False)

    def get_info(self):
        """
        Return some information about this player
        """
        return(translate('Media.player', 'Webkit is a media player which runs '
            'inside a web browser. This player allows text over video to be '
            'rendered.') +
            u'<br/> <strong>' + translate('Media.player', 'Audio') +
            u'</strong><br/>' + unicode(AUDIO_EXT) + u'<br/><strong>' +
            translate('Media.player', 'Video') + u'</strong><br/>' +
            unicode(VIDEO_EXT) + u'<br/>')
