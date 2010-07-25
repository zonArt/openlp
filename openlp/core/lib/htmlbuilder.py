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
<div id="lyrics" class="lyrics"></div>
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

def build_blank(width, height):
    """
    Build the blank display div

    `width`
        Screen width
    `height`
        Screen height
    """
    blank = """
    #blank {
        position: absolute;
        left: 0px;
        top: 0px;
        width: %spx
        height: %spx;
        z-index:10;
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

def build_lyrics(item):
    """
    Build the video display div

    `item`
        Service Item containing theme and location information
    """
    lyrics = """
    #lyrics {position: absolute; %s z-index:3; %s; %s %s }
    table {border=0;margin=0padding=0;}
    """
    theme = item.themedata
    lyrics_html = u''
    position = u''
    fontworks = u''
    font = u''
    text = u''
    if theme:
        position =  u' left: %spx; top: %spx; width: %spx; height: %spx; ' % \
            (item.main.x(),  item.main.y(), item.main.width(),
            item.main.height())
        font = u' font-family %s; font-size: %spx;' % \
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
        text = u'color:%s; %s %s' % (theme.font_main_color, align, valign)
        if theme.display_shadow and theme.display_outline:
            fontworks = u'text-shadow: -%spx 0 %s, 0 %spx %s, %spx 0 %s, 0 ' \
                '-%spx %s, %spx %spx %spx %s' % \
                (theme.display_outline_size, theme.display_outline_color,
                theme.display_outline_size, theme.display_outline_color,
                theme.display_outline_size, theme.display_outline_color,
                theme.display_outline_size, theme.display_outline_color,
                theme.display_shadow_size, theme.display_shadow_size,
                theme.display_shadow_size, theme.display_shadow_color)
        elif theme.display_shadow:
            fontworks = u'text-shadow: %spx %spx %spx %s' % \
                (theme.display_shadow_size, theme.display_shadow_size,
                theme.display_shadow_size, theme.display_shadow_color)
        elif theme.display_outline:
            fontworks = u'text-shadow: -%spx 0 %s, 0 %spx %s,' \
                ' %spx 0 %s, 0 -%spx %s' % \
                (theme.display_outline_size, theme.display_outline_color,
                theme.display_outline_size, theme.display_outline_color,
                theme.display_outline_size, theme.display_outline_color,
                theme.display_outline_size, theme.display_outline_color)
    lyrics_html = lyrics % (position, fontworks, font, text)
    print lyrics_html
    return lyrics_html

def build_footer(item):
    lyrics = """
    #footer {position: absolute; %s z-index:3; %s; %s }
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
            align = u'align=center;'
        elif theme.display_horizontalAlign == 1:
            align = u'align=right;'
        if theme.display_verticalAlign == 2:
            valign = u'vertical-align=top;'
        elif theme.display_verticalAlign == 1:
            valign = u'vertical-align=middle;'
        else:
            valign = u'vertical-align=bottom;'
        text = u'color:%s; %s %s' % (theme.font_footer_color, align, valign)
    lyrics_html = lyrics % (position, font, text)
    print lyrics_html
    return lyrics_html


def build_alert(width, alert):
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
