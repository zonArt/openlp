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
    padding:0
}
%s
%s
%s
%s
%s
%s
%s
</style>
<script language="javascript">
    var t = null;
    var transition = %s;

    function displayAlert(alert){
        var text1 = document.getElementById('alertmain');
        text1.innerHTML = newtext;
    }

    function startfade(newtext){
        var text1 = document.getElementById('lyricsmain');
        var texto1 = document.getElementById('lyricsoutline');
        var texts1 = document.getElementById('lyricsshadow');
        if(!transition){
            text1.innerHTML = newtext;
            texto1.innerHTML = newtext;
            texts1.innerHTML = newtext;
            return;
        }
        var text2 = document.getElementById('lyricsmain2');
        var texto2 = document.getElementById('lyricsoutline2');
        var texts2 = document.getElementById('lyricsshadow2');
        if(text2.style.opacity==''||parseFloat(text2.style.opacity) < 0.5){
            text2.innerHTML = text1.innerHTML;
            text2.style.opacity = text1.style.opacity;
            texto2.innerHTML = text1.innerHTML;
            texto2.style.opacity = text1.style.opacity;
            texts2.innerHTML = text1.innerHTML;
            texts2.style.opacity = text1.style.opacity;
        }
        text1.style.opacity = 0;
        text1.innerHTML = newtext;
        texto1.style.opacity = 0;
        texto1.innerHTML = newtext;
        texts1.style.opacity = 0;
        texts1.innerHTML = newtext;
        // temp:
        texts2.style.opacity = 0;
        // end temp
        if(t!=null)
            clearTimeout(t);
        t = setTimeout('fade()', 50);
    }
    function fade(){
        var text1 = document.getElementById('lyricsmain');
        var texto1 = document.getElementById('lyricsoutline');
        var texts1 = document.getElementById('lyricsshadow');
        var text2 = document.getElementById('lyricsmain2');
        var texto2 = document.getElementById('lyricsoutline2');
        var texts2 = document.getElementById('lyricsshadow2');
        if(parseFloat(text1.style.opacity) < 1){
            text1.style.opacity = parseFloat(text1.style.opacity) + 0.1;
            texto1.style.opacity = parseFloat(texto1.style.opacity) + 0.1;
            //texts1.style.opacity = parseFloat(texts1.style.opacity) + 0.1;
        }
        if(parseFloat(text2.style.opacity) > 0){
            text2.style.opacity = parseFloat(text2.style.opacity) - 0.1;
            texto2.style.opacity = parseFloat(texto2.style.opacity) - 0.1;
            //texts2.style.opacity = parseFloat(texts2.style.opacity) - 0.1;
        }
        if((parseFloat(text1.style.opacity) < 1)||(parseFloat(text2.style.opacity) > 0))
            t = setTimeout('fade()', 50);
        else{
            text1.style.opacity = 1
            texto1.style.opacity = 1
            texts1.style.opacity = 1
            text2.style.opacity = 0
            texto2.style.opacity = 0
            texts2.style.opacity = 0
        }
    }
</script>
</head>
<body>
<table class="lyricstable lyricscommon">
    <tr><td id="lyricsmain" class="lyrics"></td></tr>
</table>
<table class="lyricsoutlinetable lyricscommon">
    <tr><td id="lyricsoutline" class="lyricsoutline lyrics"></td></tr>
</table>
<table class="lyricsshadowtable lyricscommon">
    <tr><td id="lyricsshadow" class="lyricsshadow lyrics"></td></tr>
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
<table class="alerttable alertcommon">
    <tr><td id="alertmain" class="alert"></td></tr>
</table>
<div id="footer" class="footer"></div>
<video id="video"></video>
<blank id="blank"></blank>
%s
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
    html = HTMLSRC % (build_video(width, height),
                      build_image(width, height),
                      build_lyrics(item),
                      build_footer(item),
                      build_alert(width, height, alert),
                      build_image(width, height),
                      build_blank(width, height),
                      "true" if theme and
                        theme.display_slideTransition else "false",
                      build_image_src(item.bg_frame))
    return html

def build_video(width, height):
    """
    Build the video display div

    `width`
        Screen width
    `height`
        Screen height
    """
    video = """
    #video { position: absolute; left: 0px; top: 0px;
        width: %spx; height: %spx; z-index:1; }
    """
    return video % (width, height)

def build_blank(width, height):
    """
    Build the blank display div

    `width`
        Screen width
    `height`
        Screen height
    """
    blank = """
    #blank { position: absolute; left: 0px; top: 0px;
        width: %spx; height: %spx; z-index:10;
    }
    """
    return blank % (width, height)

def build_image(width, height):
    """
    Build the image display div

    `width`
        Screen width
    `height`
        Screen height
    """
    image = """
    #image { position: absolute; left: 0px; top: 0px;
        width: %spx; height: %spx; z-index:2;
    }
    """
    return image % (width, height)

def build_image_src(image):
    """
    Build display for the backgroung image

    `image`
        Image to be displayed
    """
    image_src = """
    <img src="data:image/png;base64,%s">
    """
    return image_src % image_to_byte(image)

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
    table {border=0; margin=0; padding=0; }
     """
    theme = item.themedata
    lyricscommon = u''
    lyricstable = u''
    outlinetable = u''
    shadowtable = u''
    lyrics = u''
    outline = u'display: none;'
    shadow = u'display: none;'
    if theme:
        lyricscommon =  u'width: %spx; height: %spx; ' \
            u'font-family %s; font-size: %spx; color: %s; line-height: %d%%' % \
            (item.main.width(), item.main.height(),
            theme.font_main_name, theme.font_main_proportion,
            theme.font_main_color, 100 + int(theme.font_main_line_adjustment))
        lyricstable = u'left: %spx; top: %spx;' % \
            (item.main.x(), item.main.y())
        outlinetable = u'left: %spx; top: %spx;' % \
            (item.main.x(),  item.main.y())
        shadowtable = u'left: %spx; top: %spx;' % \
            (item.main.x() + float(theme.display_shadow_size),
            item.main.y() + float(theme.display_shadow_size))
        align = u''
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
            outline = u'-webkit-text-stroke: %sem %s; ' % \
                (float(theme.display_outline_size) / 16,
                theme.display_outline_color)
            if theme.display_shadow:
                shadow = u'-webkit-text-stroke: %sem %s; ' % \
                    (float(theme.display_outline_size) / 16,
                    theme.display_shadow_color)
        else:
            if theme.display_shadow:
                shadow = u'color: %s;' % (theme.display_shadow_color)
    lyrics_html = style % (lyricscommon, lyricstable, outlinetable,
        shadowtable, lyrics, outline, shadow)
    print lyrics_html
    return lyrics_html

def build_footer(item):
    """
    Build the display of the item footer

    `item`
        Service Item to be processed.
    """
    lyrics = """
    #footer {position: absolute; %s z-index:5; %s; %s }
    """
    theme = item.themedata
    lyrics_html = u''
    position = u''
    font = u''
    text = u''
    if theme:
        position =  u' left: %spx; top: %spx; width: %spx; height: %spx; ' % \
            (item.footer.x(),  item.footer.y(), item.footer.width(),
            item.footer.height())
        font = u' font-family %s; font-size: %spx;' % \
            (theme.font_footer_name, theme.font_footer_proportion)
        align = u''
        if theme.display_horizontalAlign == 2:
            align = u'align:center;'
        elif theme.display_horizontalAlign == 1:
            align = u'align:right;'
        text = u'color:%s; %s ' % (theme.font_footer_color, align)
    lyrics_html = lyrics % (position, font, text)
    return lyrics_html

def build_alert(width, height, alertTab):
    """
    Build the display of the footer

    `width`
        Screen Width
    `height`
        Screen height
    `alertTab`
        Details from the Alert tab for fonts etc
    """
    style = """
    .alertcommon { position: absolute; %s }
    .alerttable { z-index:8;  %s }
    .alert { %s }
    table {border=0; margin=0; padding=0; }
     """
    alertcommon = u''
    alerttable = u''
    valign = u''
    if alertTab:
        alertcommon = u'width: %spx; height: %spx; ' \
            u'font-family %s; font-size: %spx; color: %s; ' % \
            (width, height, alertTab.font_face, alertTab.font_size,
            alertTab.bg_color)
        alerttable = u'left: %spx; top: %spx;' % (0, 0)
        if alertTab.location == 2:
            valign = u'vertical-align:bottom;'
        elif alertTab.location == 1:
            valign = u'vertical-align:middle;'
        else:
            valign = u'vertical-align:top;'
    alert_html = style % (alertcommon, alerttable, valign)
    print alert_html
    return alert_html
