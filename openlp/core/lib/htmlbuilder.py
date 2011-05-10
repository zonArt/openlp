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

from PyQt4 import QtWebKit

from openlp.core.lib.theme import BackgroundType, BackgroundGradientType, \
    VerticalType, HorizontalType

log = logging.getLogger(__name__)

HTMLSRC = u"""
<html>
<head>
<title>OpenLP Display</title>
<style>
*{
    margin: 0;
    padding: 0;
    border: 0;
    overflow: hidden;
}
body {
    %s;
}
.size {
    position: absolute;
    left: 0px;
    top: 0px;
    width: %spx;
    height: %spx;
}
#black {
    z-index:8;
    background-color: black;
    display: none;
}
#bgimage {
    z-index:1;
}
#image {
    z-index:2;
}
#video1 {
    z-index:3;
}
#video2 {
    z-index:3;
}
#flash {
    z-index:4;
}
#alert {
    position: absolute;
    left: 0px;
    top: 0px;
    z-index:10;
    %s
}
#footer {
    position: absolute;
    z-index:6;
    %s
}
/* lyric css */
%s
sup {
    font-size:0.6em;
    vertical-align:top;
    position:relative;
    top:-0.3em;
}
</style>
<script language="javascript">
    var timer = null;
    var video_timer = null;
    var current_video = '1';
    var transition = %s;

    function show_video(state, path, volume, loop){
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
                vid.currentTime = path;
                break;
       }
    }

    function show_image(src){
        var img = document.getElementById('image');
        img.src = src;
        if(src == '')
            img.style.display = 'none';
        else
            img.style.display = 'block';
    }

    function show_blank(state){
        var black = 'none';
        var lyrics = '';
        var pause = false;
        switch(state){
            case 'theme':
                lyrics = 'hidden';
                pause = true;
                break;
            case 'black':
                black = 'block';
                pause = true;
                break;
            case 'desktop':
                pause = true;
                break;
        }
        document.getElementById('black').style.display = black;
        document.getElementById('lyricsmain').style.visibility = lyrics;
        document.getElementById('image').style.visibility = lyrics;
        outline = document.getElementById('lyricsoutline')
        if(outline!=null)
            outline.style.visibility = lyrics;
        shadow = document.getElementById('lyricsshadow')
        if(shadow!=null)
            shadow.style.visibility = lyrics;
        document.getElementById('footer').style.visibility = lyrics;
        var vid = document.getElementById('video');
        if(vid.src != ''){
            if(pause)
                vid.pause();
            else
                vid.play();
        }
    }

    function show_alert(alerttext, position){
        var text = document.getElementById('alert');
        text.innerHTML = alerttext;
        if(alerttext == '') {
            text.style.visibility = 'hidden';
            return 0;
        }
        if(position == ''){
            position = getComputedStyle(text, '').verticalAlign;
        }
        switch(position)
        {
            case 'top':
                text.style.top = '0px';
                break;
            case 'middle':
                text.style.top = ((window.innerHeight - text.clientHeight) / 2)
                    + 'px';
                break;
            case 'bottom':
                text.style.top = (window.innerHeight - text.clientHeight)
                    + 'px';
                break;
        }
        text.style.visibility = 'visible';
        return text.clientHeight;
    }

    function show_footer(footertext){
        document.getElementById('footer').innerHTML = footertext;
    }

    function show_text(newtext){
        if(timer != null)
            clearTimeout(timer);
        text_fade('lyricsmain', newtext);
        text_fade('lyricsoutline', newtext);
        text_fade('lyricsshadow', newtext);
        if(text_opacity()==1) return;
        timer = setTimeout(function(){
            show_text(newtext);
        }, 100);
    }

    function text_fade(id, newtext){
        /*
        Using -webkit-transition: opacity 1s linear; would have been preferred
        but it isn't currently quick enough when animating multiple layers of
        large areas of large text. Therefore do it manually as best we can.
        Hopefully in the future we can revisit and do more interesting
        transitions using -webkit-transition and -webkit-transform.
        However we need to ensure interrupted transitions (quickly change 2
        slides) still looks pretty and is zippy.
        */
        var text = document.getElementById(id);
        if(text==null) return;
        if(!transition){
            text.innerHTML = newtext;
            return;
        }
        if(newtext==text.innerHTML){
            text.style.opacity = parseFloat(text.style.opacity) + 0.3;
            if(text.style.opacity>0.7)
                text.style.opacity = 1;
        } else {
            text.style.opacity = parseFloat(text.style.opacity) - 0.3;
            if(text.style.opacity<=0.1){
                text.innerHTML = newtext;
            }
        }
    }

    function text_opacity(){
        var text = document.getElementById('lyricsmain');
        return getComputedStyle(text, '').opacity;
    }

    function show_text_complete(){
        return (text_opacity()==1);
    }

    function getFlashMovieObject(movieName)
    {
        if (window.document[movieName])
        {
            return window.document[movieName];
        }
        if (navigator.appName.indexOf("Microsoft Internet")==-1)
        {
            if (document.embeds && document.embeds[movieName])
            return document.embeds[movieName];
        }
    }

    function show_flash(state, path){
        var text = document.getElementById('flash');
        var flashMovie = getFlashMovieObject("OpenLPFlashMovie");
        var src = "src = 'file:///" + path + "'";
        var view_parm = " wmode='opaque'" +
            " width='" + window.innerWidth + "'" +
            " height='" + window.innerHeight + "'";
        var swf_parm = " autostart='false' loop='false' play='false'" +
            " hidden='false' swliveconnect='true'" +
            " name='OpenLPFlashMovie'>";

        switch(state){
            case 'load':
                text.innerHTML = "<embed " + src + view_parm + swf_parm + ">";
                flashMovie = getFlashMovieObject("OpenLPFlashMovie");
                text.style.visibility = 'visible';
                flashMovie.Play();
                break;
            case 'play':
                text.style.visibility = 'visible';
                flashMovie.Play();
                break;
            case 'rewind':
                ret = 'rewind';
                alert(' Wert: ' + flashMovie.TGetProperty("/", 4));
// flashMovie.TotalFrames()
// PercentLoaded()
// GotoFrame()
                break;
            case 'stop':
                flashMovie.StopPlay();
                text.innerHTML = '';
                text.style.visibility = 'hidden';
                break;
        }
    }

</script>
</head>
<body>
<img id="bgimage" class="size" %s />
<img id="image" class="size" %s />
<video id="video1" class="size" style="visibility:hidden" autobuffer preload>
</video>
<video id="video2" class="size" style="visibility:hidden" autobuffer preload>
</video>
<div id="flash" class="size" style="visibility:hidden"></div>
%s
<div id="footer" class="footer"></div>
<div id="black" class="size"></div>
<div id="alert" style="visibility:hidden;"></div>
</body>
</html>
    """

def build_html(item, screen, alert, islive, background, image=None):
    """
    Build the full web paged structure for display

    `item`
        Service Item to be displayed
    `screen`
        Current display information
    `alert`
        Alert display display information
    `islive`
        Item is going live, rather than preview/theme building
    `background`
        Theme background image - bytes
    `image`
        Image media item - bytes
    """
    width = screen[u'size'].width()
    height = screen[u'size'].height()
    theme = item.themedata
    webkitvers = webkit_version()
    # Image generated and poked in
    if background:
        bgimage_src = u'src="data:image/png;base64,%s"' % background
    elif item.bg_image_bytes:
        bgimage_src = u'src="data:image/png;base64,%s"' % item.bg_image_bytes
    else:
        bgimage_src = u'style="display:none;"'
    if image:
        image_src = u'src="data:image/png;base64,%s"' % image
    else:
        image_src = u'style="display:none;"'
    html = HTMLSRC % (build_background_css(item, width, height),
        width, height,
        build_alert_css(alert, width),
        build_footer_css(item, height),
        build_lyrics_css(item, webkitvers),
        u'true' if theme and theme.display_slide_transition and islive \
            else u'false',
        bgimage_src, image_src,
        build_lyrics_html(item, webkitvers))
    return html

def webkit_version():
    """
    Return the Webkit version in use.
    Note method added relatively recently, so return 0 if prior to this
    """
    try:
        webkitvers = float(QtWebKit.qWebKitVersion())
        log.debug(u'Webkit version = %s' % webkitvers)
    except AttributeError:
        webkitvers = 0
    return webkitvers

def build_background_css(item, width, height):
    """
    Build the background css

    `item`
        Service Item containing theme and location information

    """
    width = int(width) / 2
    theme = item.themedata
    background = u'background-color: black'
    if theme:
        if theme.background_type == \
            BackgroundType.to_string(BackgroundType.Solid):
            background = u'background-color: %s' % theme.background_color
        else:
            if theme.background_direction == BackgroundGradientType.to_string \
                (BackgroundGradientType.Horizontal):
                background = \
                    u'background: ' \
                    u'-webkit-gradient(linear, left top, left bottom, ' \
                    'from(%s), to(%s))' % (theme.background_start_color,
                    theme.background_end_color)
            elif theme.background_direction == \
                BackgroundGradientType.to_string( \
                BackgroundGradientType.LeftTop):
                background = \
                    u'background: ' \
                    u'-webkit-gradient(linear, left top, right bottom, ' \
                    'from(%s), to(%s))' % (theme.background_start_color,
                    theme.background_end_color)
            elif theme.background_direction == \
                BackgroundGradientType.to_string \
                (BackgroundGradientType.LeftBottom):
                background = \
                    u'background: ' \
                    u'-webkit-gradient(linear, left bottom, right top, ' \
                    'from(%s), to(%s))' % (theme.background_start_color,
                    theme.background_end_color)
            elif theme.background_direction == \
                BackgroundGradientType.to_string \
                (BackgroundGradientType.Vertical):
                background = \
                    u'background: -webkit-gradient(linear, left top, ' \
                    u'right top, from(%s), to(%s))' % \
                    (theme.background_start_color, theme.background_end_color)
            else:
                background = \
                    u'background: -webkit-gradient(radial, %s 50%%, 100, %s ' \
                    u'50%%, %s, from(%s), to(%s))' % (width, width, width,
                    theme.background_start_color, theme.background_end_color)
    return background

def build_lyrics_css(item, webkitvers):
    """
    Build the lyrics display css

    `item`
        Service Item containing theme and location information

    `webkitvers`
        The version of qtwebkit we're using

    """
    style = """
.lyricstable {
    z-index:5;
    position: absolute;
    display: table;
    %s
}
.lyricscell {
    display:table-cell;
    word-wrap: break-word;
    %s
}
.lyricsmain {
%s
}
.lyricsoutline {
%s
}
.lyricsshadow {
%s
}
    """
    theme = item.themedata
    lyricstable = u''
    lyrics = u''
    lyricsmain = u''
    outline = u''
    shadow = u''
    if theme and item.main:
        lyricstable = u'left: %spx; top: %spx;' % (item.main.x(), item.main.y())
        lyrics = build_lyrics_format_css(theme, item.main.width(),
            item.main.height())
        # For performance reasons we want to show as few DIV's as possible,
        # especially when animating/transitions.
        # However some bugs in older versions of qtwebkit mean we need to
        # perform workarounds and add extra divs. Only do these when needed.
        #
        # Before 533.3 the webkit-text-fill colour wasn't displayed, only the
        # stroke (outline) color. So put stroke layer underneath the main text.
        #
        # Before 534.4 the webkit-text-stroke was sometimes out of alignment
        # with the fill, or normal text. letter-spacing=1 is workaround
        # https://bugs.webkit.org/show_bug.cgi?id=44403
        #
        # Before 534.4 the text-shadow didn't get displayed when
        # webkit-text-stroke was used. So use an offset text layer underneath.
        # https://bugs.webkit.org/show_bug.cgi?id=19728
        if webkitvers >= 533.3:
            lyricsmain += build_lyrics_outline_css(theme)
        else:
            outline = build_lyrics_outline_css(theme)
        if theme.font_main_shadow:
            if theme.font_main_outline and webkitvers < 534.3:
                shadow = u'padding-left: %spx; padding-top: %spx;' % \
                    (int(theme.font_main_shadow_size) +
                    (int(theme.font_main_outline_size) * 2),
                    theme.font_main_shadow_size)
                shadow += build_lyrics_outline_css(theme, True)
            else:
                lyricsmain += u' text-shadow: %s %spx %spx;' % \
                    (theme.font_main_shadow_color, theme.font_main_shadow_size,
                    theme.font_main_shadow_size)
    lyrics_css = style % (lyricstable, lyrics, lyricsmain, outline, shadow)
    return lyrics_css

def build_lyrics_outline_css(theme, is_shadow=False):
    """
    Build the css which controls the theme outline
    Also used by renderer for splitting verses

    `theme`
        Object containing theme information

    `is_shadow`
        If true, use the shadow colors instead
    """
    if theme.font_main_outline:
        size = float(theme.font_main_outline_size) / 16
        if is_shadow:
            fill_color = theme.font_main_shadow_color
            outline_color = theme.font_main_shadow_color
        else:
            fill_color = theme.font_main_color
            outline_color = theme.font_main_outline_color
        return u' -webkit-text-stroke: %sem %s; ' \
            u'-webkit-text-fill-color: %s; ' % (size, outline_color, fill_color)
    else:
        return u''

def build_lyrics_format_css(theme, width, height):
    """
    Build the css which controls the theme format
    Also used by renderer for splitting verses

    `theme`
        Object containing theme information

    `width`
        Width of the lyrics block

    `height`
        Height of the lyrics block

    """
    align = HorizontalType.Names[theme.display_horizontal_align]
    valign = VerticalType.Names[theme.display_vertical_align]
    if theme.font_main_outline:
        left_margin = int(theme.font_main_outline_size) * 2
    else:
        left_margin = 0
    lyrics = u'white-space:pre-wrap; word-wrap: break-word; ' \
        'text-align: %s; vertical-align: %s; font-family: %s; ' \
        'font-size: %spt; color: %s; line-height: %d%%; margin:0;' \
        'padding:0; padding-left:%spx; width: %spx; height: %spx; ' % \
        (align, valign, theme.font_main_name, theme.font_main_size,
        theme.font_main_color, 100 + int(theme.font_main_line_adjustment),
        left_margin, width, height)
    if theme.font_main_outline:
        if webkit_version() < 534.3:
            lyrics += u' letter-spacing: 1px;'
    if theme.font_main_italics:
        lyrics += u' font-style:italic; '
    if theme.font_main_bold:
        lyrics += u' font-weight:bold; '
    return lyrics

def build_lyrics_html(item, webkitvers):
    """
    Build the HTML required to show the lyrics

    `item`
        Service Item containing theme and location information

    `webkitvers`
        The version of qtwebkit we're using
    """
    # Bugs in some versions of QtWebKit mean we sometimes need additional
    # divs for outline and shadow, since the CSS doesn't work.
    # To support vertical alignment middle and bottom, nested div's using
    # display:table/display:table-cell are required for each lyric block.
    lyrics = u''
    theme = item.themedata
    if webkitvers < 534.4 and theme and theme.font_main_outline:
        lyrics += u'<div class="lyricstable">' \
            u'<div id="lyricsshadow" style="opacity:1" ' \
            u'class="lyricscell lyricsshadow"></div></div>'
        if webkitvers < 533.3:
            lyrics += u'<div class="lyricstable">' \
                u'<div id="lyricsoutline" style="opacity:1" ' \
                u'class="lyricscell lyricsoutline"></div></div>'
    lyrics += u'<div class="lyricstable">' \
        u'<div id="lyricsmain" style="opacity:1" ' \
        u'class="lyricscell lyricsmain"></div></div>'
    return lyrics

def build_footer_css(item, height):
    """
    Build the display of the item footer

    `item`
        Service Item to be processed.
    """
    style = """
    left: %spx;
    bottom: %spx;
    width: %spx;
    font-family: %s;
    font-size: %spt;
    color: %s;
    text-align: left;
    white-space:nowrap;
    """
    theme = item.themedata
    if not theme or not item.footer:
        return u''
    bottom = height - int(item.footer.y()) - int(item.footer.height())
    lyrics_html = style % (item.footer.x(), bottom,
        item.footer.width(), theme.font_footer_name,
        theme.font_footer_size, theme.font_footer_color)
    return lyrics_html

def build_alert_css(alertTab, width):
    """
    Build the display of the footer

    `alertTab`
        Details from the Alert tab for fonts etc
    """
    style = """
    width: %spx;
    vertical-align: %s;
    font-family: %s;
    font-size: %spt;
    color: %s;
    background-color: %s;
    """
    if not alertTab:
        return u''
    align = VerticalType.Names[alertTab.location]
    alert = style % (width, align, alertTab.font_face, alertTab.font_size,
        alertTab.font_color, alertTab.bg_color)
    return alert
