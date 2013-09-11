"""
Package to test the openlp.core.lib.htmlbuilder module.
"""

from unittest import TestCase
from mock import MagicMock, patch

from PyQt4 import QtCore

from openlp.core.lib.htmlbuilder import build_html, build_background_css, build_lyrics_css, build_lyrics_outline_css, \
    build_lyrics_format_css, build_footer_css


BUILD_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>OpenLP Display</title>
<style>
*{
    margin: 0;
    padding: 0;
    border: 0;
    overflow: hidden;
    -webkit-user-select: none;
}
body {
    ;
}
.size {
    position: absolute;
    left: 0px;
    top: 0px;
    width: 100%;
    height: 100%;
}
#black {
    z-index: 8;
    background-color: black;
    display: none;
}
#bgimage {
    z-index: 1;
}
#image {
    z-index: 2;
}
plugin CSS
#footer {
    position: absolute;
    z-index: 6;
    dummy: dummy;
}
/* lyric css */

sup {
    font-size: 0.6em;
    vertical-align: top;
    position: relative;
    top: -0.3em;
}
</style>
<script>
    var timer = null;
    var transition = false;
    plugin JS

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
        switch(state){
            case 'theme':
                lyrics = 'hidden';
                break;
            case 'black':
                black = 'block';
                break;
            case 'desktop':
                break;
        }
        document.getElementById('black').style.display = black;
        document.getElementById('lyricsmain').style.visibility = lyrics;
        document.getElementById('image').style.visibility = lyrics;
        document.getElementById('footer').style.visibility = lyrics;
    }

    function show_footer(footertext){
        document.getElementById('footer').innerHTML = footertext;
    }

    function show_text(new_text){
        var match = /-webkit-text-fill-color:[^;"]+/gi;
        if(timer != null)
            clearTimeout(timer);
        /*
        QtWebkit bug with outlines and justify causing outline alignment
        problems. (Bug 859950) Surround each word with a <span> to workaround,
        but only in this scenario.
        */
        var txt = document.getElementById('lyricsmain');
        if(window.getComputedStyle(txt).textAlign == 'justify'){
            if(window.getComputedStyle(txt).webkitTextStrokeWidth != '0px'){
                new_text = new_text.replace(/(\s|&nbsp;)+(?![^<]*>)/g,
                    function(match) {
                        return '</span>' + match + '<span>';
                    });
                new_text = '<span>' + new_text + '</span>';
            }
        }
        text_fade('lyricsmain', new_text);
    }

    function text_fade(id, new_text){
        /*
        Show the text.
        */
        var text = document.getElementById(id);
        if(text == null) return;
        if(!transition){
            text.innerHTML = new_text;
            return;
        }
        // Fade text out. 0.1 to minimize the time "nothing" is shown on the screen.
        text.style.opacity = '0.1';
        // Fade new text in after the old text has finished fading out.
        timer = window.setTimeout(function(){_show_text(text, new_text)}, 400);
    }

    function _show_text(text, new_text) {
        /*
        Helper function to show the new_text delayed.
        */
        text.innerHTML = new_text;
        text.style.opacity = '1';
        // Wait until the text is completely visible. We want to save the timer id, to be able to call
        // clearTimeout(timer) when the text has changed before finishing fading.
        timer = window.setTimeout(function(){timer = null;}, 400);
    }

    function show_text_completed(){
        return (timer == null);
    }
</script>
</head>
<body>
<img id="bgimage" class="size" style="display:none;" />
<img id="image" class="size" style="display:none;" />
plugin HTML
<div class="lyricstable"><div id="lyricsmain" style="opacity:1" class="lyricscell lyricsmain"></div></div>
<div id="footer" class="footer"></div>
<div id="black" class="size"></div>
</body>
</html>
"""
BACKGROUND_CSS = """
"""
LYRICS_CSS = """
.lyricstable {
    z-index: 5;
    position: absolute;
    display: table;
    left: 10px; top: 20px;
}
.lyricscell {
    display: table-cell;
    word-wrap: break-word;
    -webkit-transition: opacity 0.4s ease;
    lyrics_format_css
}
.lyricsmain {
     text-shadow: #000000 5px 5px;
}
"""
LYRICS_OUTLINE_CSS = ' -webkit-text-stroke: 0.125em #000000; -webkit-text-fill-color: #FFFFFF; '
LYRICS_FORMAT_CSS = """
"""
FOOTER_CSS = """
    left: 10px;
    bottom: 0px;
    width: 1260px;
    font-family: Arial;
    font-size: 12pt;
    color: #FFFFFF;
    text-align: left;
    white-space: nowrap;
    """


class Htmbuilder(TestCase):
    def build_html_test(self):
        """
        Test the build_html() function
        """
        # GIVEN: Mocked arguments and function.
        with patch('openlp.core.lib.htmlbuilder.build_background_css') as mocked_build_background_css, \
                patch('openlp.core.lib.htmlbuilder.build_footer_css') as mocked_build_footer_css, \
                patch('openlp.core.lib.htmlbuilder.build_lyrics_css') as mocked_build_lyrics_css:
            # Mocked function.
            mocked_build_background_css.return_value = ''
            mocked_build_footer_css.return_value = 'dummy: dummy;'
            mocked_build_lyrics_css.return_value = ''
            # Mocked arguments.
            item = MagicMock()
            item.bg_image_bytes = None
            screen = MagicMock()
            is_live = False
            background = None
            plugin = MagicMock()
            plugin.get_display_css = MagicMock(return_value='plugin CSS')
            plugin.get_display_javascript = MagicMock(return_value='plugin JS')
            plugin.get_display_html = MagicMock(return_value='plugin HTML')
            plugins = [plugin]

            # WHEN: Create the html.
            html = build_html(item, screen, is_live, background, plugins=plugins)

            # THEN: The returned html should match.
            assert html == BUILD_HTML

    def build_background_css_tes(self):
        """
        Test the build_background_css() function
        """
        # THEN: The returned html should match.
        pass

    def build_lyrics_css_test(self):
        """
        Test the build_lyrics_css() function
        """
        # GIVEN: Mocked method and arguments.
        with patch('openlp.core.lib.htmlbuilder.build_lyrics_format_css') as mocked_build_lyrics_format_css, \
                patch('openlp.core.lib.htmlbuilder.build_lyrics_outline_css') as mocked_build_lyrics_outline_css:
            mocked_build_lyrics_format_css.return_value = 'lyrics_format_css'
            mocked_build_lyrics_outline_css.return_value = ''
            item = MagicMock()
            item.main = QtCore.QRect(10, 20, 10, 20)
            item.themedata.font_main_shadow = True
            item.themedata.font_main_shadow_color = '#000000'
            item.themedata.font_main_shadow_size = 5

            # WHEN: Create the css.
            css = build_lyrics_css(item)

            # THEN: The css should be equal.
            assert LYRICS_CSS == css, 'The lyrics css should be equal.'

    def build_lyrics_outline_css_test(self):
        """
        Test the build_lyrics_outline_css() function
        """
        # GIVEN: The mocked theme data.
        theme_data = MagicMock()
        theme_data.font_main_outline = True
        theme_data.font_main_outline_size = 2
        theme_data.font_main_color = '#FFFFFF'
        theme_data.font_main_outline_color = '#000000'

        # WHEN: Create the css.
        css = build_lyrics_outline_css(theme_data)

        # THEN: The css should be equal.
        assert LYRICS_OUTLINE_CSS == css, 'The outline css should be equal.'

    def build_lyrics_format_css_tes(self):
        """
        Test the build_lyrics_format_css() function
        """
        pass

    def build_footer_css_test(self):
       """
       Test the build_footer_css() function
       """
       # GIVEN: Create a theme.
       item = MagicMock()
       item.footer = QtCore.QRect(10, 921, 1260, 103)
       item.themedata.font_footer_name = 'Arial'
       item.themedata.font_footer_size = 12
       item.themedata.font_footer_color = '#FFFFFF'
       height = 1024

       # WHEN: create the css.
       css = build_footer_css(item, height)

       # THEN: THE css should be the same.
       assert FOOTER_CSS == css, 'The footer strings should be equal.'

