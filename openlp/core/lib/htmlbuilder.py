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

    function startfade(newtext){
        var text1 = document.getElementById('lyrics');
        var text2 = document.getElementById('lyrics2');
        if(text2.style.opacity==''||parseFloat(text2.style.opacity) < 0.5){
            text2.innerHTML = text1.innerHTML;
            text2.style.opacity = text1.style.opacity;
        }
        text1.style.opacity = 0;
        text1.innerHTML = newtext;
        if(t!=null)
            clearTimeout(t);
        t = setTimeout('fade()', 50);
    }
    function fade(){
        var text1 = document.getElementById('lyrics');
        var text2 = document.getElementById('lyrics2');
        if(parseFloat(text1.style.opacity) < 1)
            text1.style.opacity = parseFloat(text1.style.opacity) + 0.02;
        if(parseFloat(text2.style.opacity) > 0)
            text2.style.opacity = parseFloat(text2.style.opacity) - 0.02;
        if((parseFloat(text1.style.opacity) < 1)||(parseFloat(text2.style.opacity) > 0))
            t = setTimeout('fade()', 50);
    }
</script>
</head>
<body>
<table id="lyricsmaintable" class="lyricstable">
    <tr><td id="lyricsmain" class="lyrics"></td></tr>
</table>
<table id="lyricsoutlinetable" class="lyricstable">
    <tr><td id="lyricsoutline" class="lyrics"></td></tr>
</table>
<div id="footer" class="footer"></div>
<div id="alert"></div>
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
    html = HTMLSRC % (build_video(width, height),
                      build_image(width, height),
                      build_lyrics(item),
                      build_footer(item),
                      build_alert(width, alert),
                      build_image(width, height),
                      build_blank(width, height),
                      build_image_src(item.bg_frame))
    print html
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
    .lyricstable { %s }
    .lyrics { %s }
    #lyricsmain { %s }
    #lyricsoutline { %s }
    #lyricsmaintable { z-index:4; }
    #lyricsoutlinetable { z-index:3; }
    table {border=0; margin=0; padding=0; }
    """
    theme = item.themedata
    position = u''
    outline = u'display: none;'
    shadow = u''
    fontworks = u''
    lyrics = u''
    lyricsmain = u''
    font = u''
    text = u''
    if theme:
        position =  u'position: absolute; left: %spx; top: %spx;' \
            ' width: %spx; height: %spx; ' % \
            (item.main.x(),  item.main.y(), item.main.width(),
            item.main.height())
        font = u' font-family %s; font-size: %spx;' % \
            (theme.font_main_name, theme.font_main_proportion)
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
        line_height = u'line-height: %d%%' % (100 + int(theme.font_main_line_adjustment))
        lyrics = u'%s %s %s %s' % (font, align, valign, line_height)
        if theme.display_outline:
            outline = u'-webkit-text-stroke: %sem %s;' % \
                (float(theme.display_outline_size) / 16,
                theme.display_outline_color)
        if theme.display_shadow:
            shadow_size = str(float(theme.display_shadow_size) / 16)
            shadow = u'text-shadow: %sem %sem %s;' % \
                (shadow_size,  shadow_size, theme.display_shadow_color)
        lyricsmain = u'color:%s; %s' % (theme.font_main_color,  shadow)
    lyrics_html = style % (position, lyrics, lyricsmain, outline)
    print lyrics_html
    return lyrics_html

def build_footer(item):
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
        if theme.display_verticalAlign == 2:
            valign = u'vertical-align:bottom;'
        elif theme.display_verticalAlign == 1:
            valign = u'vertical-align:middle;'
        else:
            valign = u'vertical-align:top;'
        text = u'color:%s; %s %s' % (theme.font_footer_color, align, valign)
    lyrics_html = lyrics % (position, font, text)
    print lyrics_html
    return lyrics_html


def build_alert(width, alertTab):
    alert = """
    #alert { position: absolute; left: 0px; top: 70px;
        width: %spx; height: 10px; z-index:6; font-size: %spx;
    }
    #alert p {
        background-color: %s;
    }
    """
    alertText = u''
    if alertTab:
        alertText = alert % (width, alertTab.font_size, alertTab.bg_color)
    return alertText
