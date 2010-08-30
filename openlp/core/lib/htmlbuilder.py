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

from openlp.core.lib import image_to_byte

HTMLSRC = u"""
<html>
<head>
<title>OpenLP Display</title>
<style>
*{
    margin: 0;
    padding: 0;
    border: 0;
}
body {
    background-color: black;
}
.dim {
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
        document.getElementById('lyricsmain1').style.visibility = lyrics;
        document.getElementById('lyricsoutline1').style.visibility = lyrics;
        document.getElementById('lyricsshadow1').style.visibility = lyrics;
        document.getElementById('lyricsmain2').style.visibility = lyrics;
        document.getElementById('lyricsoutline2').style.visibility = lyrics;
        document.getElementById('lyricsshadow2').style.visibility = lyrics;
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
            position = window.getComputedStyle(text, '').verticalAlign;
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
        var textitem = document.getElementById('lyricsmain1');
        if(window.getComputedStyle(textitem, '').opacity==1){
            var item = '1';
        } else {
            var item = '2';
        }
        text_fade_all(item, true);
        text_fade_all((item=='')?'2':'1', false, newtext);
    }
    function text_fade_all(item, fadeout, newtext){
        text_fade('lyricsmain' + item, fadeout, newtext);
        text_fade('lyricsoutline' + item, fadeout, newtext);
        text_fade('lyricsshadow' + item, fadeout, newtext);
    }
    function text_fade(id, fadeout, newtext){
        var textitem = document.getElementById(id);
        if(fadeout) {
            textitem.className += ' fadeout';
        } else {
            textitem.innerHTML = newtext;
            window.setTimeout(function() {
                textitem.className = textitem.className.replace(' fadeout', '');
            }, 0);
        }
    }
    function show_text_complete(){
       var item = document.getElementById('lyricsmain1');
       return (window.getComputedStyle(item, '').opacity == 1);
    }
    
</script>
</head>
<body>
<!--
Using tables, rather than div's to make use of the vertical-align style that
doesn't work on div's. This avoids the need to do positioning manually which
could get messy when changing verses esp. with transitions

Would prefer to use a single table and make use of -webkit-text-fill-color
-webkit-text-stroke and text-shadow styles, but they have problems working/
co-operating in qwebkit. https://bugs.webkit.org/show_bug.cgi?id=43187
Therefore one table for text, one for outline and one for shadow.
-->
<table class="lyricstable lyricscommon">
    <tr><td id="lyricsmain1" class="lyrics"></td></tr>
</table>
<table class="lyricsoutlinetable lyricscommon">
    <tr><td id="lyricsoutline1" class="lyricsoutline lyrics"></td></tr>
</table>
<table class="lyricsshadowtable lyricscommon">
    <tr><td id="lyricsshadow1" class="lyricsshadow lyrics"></td></tr>
</table>
<table class="lyricstable lyricscommon">
    <tr><td id="lyricsmain2" class="lyrics"></td></tr>
</table>
<table class="lyricsoutlinetable lyricscommon">
    <tr><td id="lyricsoutline2" class="lyricsoutline lyrics"></td></tr>
</table>
<table class="lyricsshadowtable lyricscommon">
    <tr><td id="lyricsshadow2" class="lyricsshadow lyrics"></td></tr>
</table>
<div id="alert" style="visibility:hidden;"></div>
<div id="footer" class="footer"></div>
<video class="dim" id="video"></video>
<div class="dim" id="black"></div>
<img class="dim" id="image" src="%s" />
</body>
</html>
    """

def build_html(item, screen, alert):
    """
    Build the full web paged structure for display

    `item`
        Service Item to be displayed
    `screen`
        Current display information
    `alert`
        Alert display display information
    """
    width = screen[u'size'].width()
    height = screen[u'size'].height()
    theme = item.themedata
    if item.bg_frame:
        image = u'data:image/png;base64,%s' % image_to_byte(item.bg_frame)
    else:
        image = u''
    html = HTMLSRC % (width, height,
        build_alert(alert, width),
        build_footer(item),
        build_lyrics(item),
        image)
    return html

def build_lyrics(item):
    """
    Build the video display div

    `item`
        Service Item containing theme and location information
    """
    style = """
.lyricscommon { position: absolute;  %s }
.lyricstable { z-index:4;  %s }
.lyricsoutlinetable { z-index:3; %s }
.lyricsshadowtable { z-index:2; %s }
.lyrics { %s }
.lyricsoutline { %s }
.lyricsshadow { %s }
td { opacity: 1; %s }
td.fadeout { opacity: 0; }
     """
    theme = item.themedata
    lyricscommon = u''
    lyricstable = u''
    outlinetable = u''
    shadowtable = u''
    lyrics = u''
    outline = u'display: none;'
    shadow = u'display: none;'
    transition = u''
    if theme:
        lyricscommon =  u'width: %spx; height: %spx; word-wrap: break-word;  ' \
            u'font-family: %s; font-size: %spx; color: %s; line-height: %d%%;' % \
            (item.main.width(), item.main.height(),
            theme.font_main_name, theme.font_main_proportion,
            theme.font_main_color, 100 + int(theme.font_main_line_adjustment))
        lyricstable = u'left: %spx; top: %spx;' % \
            (item.main.x(), item.main.y())
        outlinetable = u'left: %spx; top: %spx;' % \
            (item.main.x(), item.main.y())
        shadowtable = u'left: %spx; top: %spx;' % \
            (item.main.x() + float(theme.display_shadow_size),
            item.main.y() + float(theme.display_shadow_size))
        align = u''
        if theme.display_slideTransition:
            transition = u'-webkit-transition: opacity 5s ease-in-out;'
        if theme.display_horizontalAlign == 2:
            align = u'text-align:center;'
        elif theme.display_horizontalAlign == 1:
            align = u'text-align:right;'
        else:
            align = u'text-align:left;'
        if theme.display_verticalAlign == 2:
            valign = u'vertical-align:bottom;'
        elif theme.display_verticalAlign == 1:
            valign = u'vertical-align:middle;'
        else:
            valign = u'vertical-align:top;'
        lyrics = u'%s %s' % (align, valign)
        if theme.display_outline:
            lyricscommon += u' letter-spacing: 1px;'
            outline = u'-webkit-text-stroke: %sem %s; ' % \
                (float(theme.display_outline_size) / 16,
                theme.display_outline_color)
            if theme.display_shadow:
                shadow = u'-webkit-text-stroke: %sem %s; ' \
                    u'-webkit-text-fill-color: %s; '% \
                    (float(theme.display_outline_size) / 16,
                    theme.display_shadow_color, theme.display_shadow_color)
        else:
            if theme.display_shadow:
                shadow = u'color: %s;' % (theme.display_shadow_color)
    lyrics_html = style % (lyricscommon, lyricstable, outlinetable,
        shadowtable, lyrics, outline, shadow, transition)
    return lyrics_html

def build_footer(item):
    """
    Build the display of the item footer

    `item`
        Service Item to be processed.
    """
    style = """
left: %spx;
top: %spx;
width: %spx;
height: %spx;
font-family: %s;
font-size: %spx;
color: %s;
text-align: %s;
    """
    theme = item.themedata
    if not theme:
        return u''
    if theme.display_horizontalAlign == 2:
        align = u'center'
    elif theme.display_horizontalAlign == 1:
        align = u'right'
    else:
        align = u'left'
    lyrics_html = style % (item.footer.x(), item.footer.y(),
        item.footer.width(), item.footer.height(), theme.font_footer_name,
        theme.font_footer_proportion, theme.font_footer_color, align)
    return lyrics_html

def build_alert(alertTab, width):
    """
    Build the display of the footer

    `alertTab`
        Details from the Alert tab for fonts etc
    """
    style = """
width: %s;
vertical-align: %s;
font-family: %s;
font-size: %spx;
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
