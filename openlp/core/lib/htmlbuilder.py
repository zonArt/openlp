# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

from openlp.core.lib import image_to_byte

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
#image {
    z-index:1;
}
#video {
    z-index:2;
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
    z-index:5;
    %s
}
/* lyric css */
%s

</style>
<script language="javascript">
    var timer = null;
    var transition = %s;

    function show_video(state, path, volume, loop){
        var vid = document.getElementById('video');
        if(path != null)
            vid.src = path;
        if(loop != null){
            if(loop)
                vid.loop = 'loop';
            else
                vid.loop = '';
        }
        if(volume != null){
            vid.volume = volume;
        }
        switch(state){
            case 'play':
                vid.play();
                vid.style.display = 'block';
                break;
            case 'pause':
                vid.pause();
                vid.style.display = 'block';
                break;
            case 'stop':
                vid.pause();
                vid.style.display = 'none';
                break;
            case 'close':
                vid.pause();
                vid.style.display = 'none';
                vid.src = '';
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
</script>
</head>
<body>
<img id="image" class="size" src="%s" />
<video id="video" class="size"></video>
%s
<div id="footer" class="footer"></div>
<div id="black" class="size"></div>
<div id="alert" style="visibility:hidden;"></div>
</body>
</html>
    """

def build_html(item, screen, alert, islive):
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
    """
    width = screen[u'size'].width()
    height = screen[u'size'].height()
    theme = item.themedata
    webkitvers = webkit_version()
    if item.bg_frame:
        image = u'data:image/png;base64,%s' % image_to_byte(item.bg_frame)
    else:
        image = u''
    html = HTMLSRC % (build_background_css(item, width, height),
        width, height,
        build_alert_css(alert, width),
        build_footer_css(item, height),
        build_lyrics_css(item, webkitvers),
        u'true' if theme and theme.display_slideTransition and islive \
            else u'false',
        image,
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
        if theme.background_type == u'solid':
            background = u'background-color: %s' % theme.background_color
        else:
            if theme.background_direction == u'horizontal':
                background = \
                    u'background: ' \
                    u'-webkit-gradient(linear, left top, left bottom, ' \
                    'from(%s), to(%s))' % (theme.background_startColor,
                    theme.background_endColor)
            elif theme.background_direction == u'vertical':
                background = \
                    u'background: -webkit-gradient(linear, left top, ' \
                    u'right top, from(%s), to(%s))' % \
                    (theme.background_startColor, theme.background_endColor)
            else:
                background = \
                    u'background: -webkit-gradient(radial, %s 50%%, 100, %s ' \
                    u'50%%, %s, from(%s), to(%s))' % (width, width, width,
                    theme.background_startColor, theme.background_endColor)
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
    z-index:4;
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
        lyricstable = u'left: %spx; top: %spx;' % \
            (item.main.x(), item.main.y())
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
        if theme.display_shadow:
            if theme.display_outline and webkitvers < 534.3:
                shadow = u'padding-left: %spx; padding-top: %spx ' % \
                    (theme.display_shadow_size, theme.display_shadow_size)
                shadow += build_lyrics_outline_css(theme, True)
            else:
                lyricsmain += u' text-shadow: %s %spx %spx;' % \
                    (theme.display_shadow_color, theme.display_shadow_size,
                    theme.display_shadow_size)
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
    if theme.display_outline:
        size = float(theme.display_outline_size) / 16
        if is_shadow:
            fill_color = theme.display_shadow_color
            outline_color = theme.display_shadow_color
        else:
            fill_color = theme.font_main_color
            outline_color = theme.display_outline_color
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
    if theme.display_horizontalAlign == 2:
        align = u'center'
    elif theme.display_horizontalAlign == 1:
        align = u'right'
    else:
        align = u'left'
    if theme.display_verticalAlign == 2:
        valign = u'bottom'
    elif theme.display_verticalAlign == 1:
        valign = u'middle'
    else:
        valign = u'top'
    lyrics = u'white-space:pre-wrap; word-wrap: break-word; ' \
        'text-align: %s; vertical-align: %s; font-family: %s; ' \
        'font-size: %spt; color: %s; line-height: %d%%; ' \
        'margin:0; padding:0; width: %spx; height: %spx; ' % \
        (align, valign, theme.font_main_name, theme.font_main_proportion,
        theme.font_main_color, 100 + int(theme.font_main_line_adjustment),
        width, height)
    if theme.display_outline:
        if webkit_version() < 534.3:
            lyrics += u' letter-spacing: 1px;'
    if theme.font_main_italics:
        lyrics += u' font-style:italic; '
    if theme.font_main_weight == u'Bold':
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
    if webkitvers < 534.4 and theme and theme.display_outline:
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
        theme.font_footer_proportion, theme.font_footer_color)
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
    align = u''
    if alertTab.location == 2:
        align = u'bottom'
    elif alertTab.location == 1:
        align = u'middle'
    else:
        align = u'top'
    alert = style % (width, align, alertTab.font_face, alertTab.font_size,
        alertTab.font_color, alertTab.bg_color)
    return alert
