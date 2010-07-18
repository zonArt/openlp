# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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
<div id="lyrics" class="lyrics"></div>
<div id="lyrics2" class="lyrics"></div>
<div id="alert"></div>
<video id="video"></video>
%s
</body>
</html>
    """
def build_html(item, screen, alert):
    width = screen[u'size'].width()
    height = screen[u'size'].height()
    html = HTMLSRC % (build_video(width, height),
                      build_image(width, height),
                      build_lyrics(item, width, height),
                      build_alert(width, height, alert),
                      build_image(width, height),
                      build_image_src(item.bg_frame))
    return html

def build_video(width, height):
    video = """
    #video {
        position: absolute;
        left: 0px;
        top: 0px;
        width: %spx
        height: %spx;
        z-index:1;
    }
    """
    return video % (width, height)


def build_image(width, height):
    image = """
    #image {
        position: absolute;
        left: 0px;
        top: 0px;
        width: %spx;
        height: %spx;
        z-index:2;
    }
    """
    return image % (width, height)

def build_image_src(image):
    #    <img src="" height="480" width="640" />
    image_src = """
    <img src="data:image/png;base64,%s">";
    """
    return image_src % image_to_byte(image)

def build_lyrics(item, width, height):
    lyrics = """
    #lyrics {
        position: absolute;
        %s
        z-index:3;
        %s;
        %s;
        %s
        %s
    }
    """
    theme = item.themedata
    lyrics_html = u''
    position = u''
    shadow = u''
    outline = u''
    font = u''
    text = u''
    if theme:
        position =  u' left: %spx; top: %spx; width: %spx; height: %spx; ' %\
            (item.main.x(),  item.main.y(), item.main.width(), item.main.height())
        font = u' font-family %s; font-size: %spx;' %\
            (theme.font_main_name, theme.font_main_proportion)
        align = u''
        if theme.display_horizontalAlign == 2:
            align = u'align=center;'
        elif theme.display_horizontalAlign == 1:
            align = u'align=right;'
        if theme.display_verticalAlign == 2:
            valign = u'vertical-align=top;'
        elif theme.display_verticalAlign == 1:
            valign = u'vertical-align=middle;'
        else:
            valign = u'vertical-align=bottom;'
        text = u'color:%s;%s%s' % (theme.font_main_color, align, valign)
        if theme.display_shadow:
            shadow = u'text-shadow: %spx %spx %spx %s' %\
                (theme.display_shadow_size, theme.display_shadow_size,
                theme.display_shadow_size, theme.display_shadow_color)
        if theme.display_outline:
            # 1px is the blur radius
            outline = u'text-outline: %spx 1px %s' %\
                (theme.display_outline_size, theme.display_outline_color)
            outline = u'text-shadow: -1px 0 white, 0 1px white, 1px 0 white, 0 -1px white'
    lyrics_html = lyrics % (position, shadow, outline, font, text)
    print lyrics_html
    return lyrics_html

def build_alert(width, height, alert):
    alert = """
    #alert {
        position: absolute;
        left: 0px;
        top: 70px;
        width: %spx;
        height: 10px;
        z-index:4;
        font-size: 50px;
    }
    #alert p {
        background-color: red;
    }
    """
    return alert % (width)
