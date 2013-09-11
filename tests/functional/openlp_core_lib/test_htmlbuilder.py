"""
Package to test the openlp.core.lib.htmlbuilder module.
"""

from unittest import TestCase
from mock import MagicMock, patch

from PyQt4 import QtCore

from openlp.core.lib.htmlbuilder import build_footer_css, build_lyrics_outline_css, build_lyrics_css


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
OUTLINE_CSS = ' -webkit-text-stroke: 0.125em #000000; -webkit-text-fill-color: #FFFFFF; '
LYRICS_CSS = 'white-space:pre-wrap; word-wrap: break-word; text-align: left; vertical-align: top; ' + \
    'font-family: Arial; font-size: 40pt; color: #FFFFFF; line-height: 100%; margin: 0;padding: 0; ' + \
    'padding-bottom: 0; padding-left: 0px; width: 1260px; height: 921px; '

class Htmbuilder(TestCase):
    def build_html(self):
        pass

    def build_background_css(self):
        pass

    def build_lyrics_css_test(self):
        """
        """
        with patch('openlp.core.lib.htmlbuilder.build_lyrics_format_css') as mocked_method:#
            mocked_method.return_value = ''
            item = MagicMock()
            item.main =
            item.themedata.font_main_shadow =
            item.themedata.font_main_shadow_color =
            item.themedata.font_main_shadow_size =
            item.themedata.font_main_shadow =
            print(build_lyrics_css(item))
            assert LYRICS_CSS == build_lyrics_css(item), 'The lyrics css should be equal.'

    def build_lyrics_outline_css_test(self):
        """
        Test the build_lyrics_outline_css() function
        """
        theme_data = MagicMock()
        theme_data.font_main_outline = True
        theme_data.font_main_outline_size = 2
        theme_data.font_main_color = '#FFFFFF'
        theme_data.font_main_outline_color = '#000000'
        assert OUTLINE_CSS == build_lyrics_outline_css(theme_data), 'The outline css should be equal.'


    def build_lyrics_format_css(self):
        """
        Test the build_lyrics_format_css() function
        """
        pass

    def build_footer_css_test(self):
       """
       Test the build_footer_css() function
       """
       # Create a theme.
       item = MagicMock()
       item.footer = QtCore.QRect(10, 921, 1260, 103)
       item.themedata.font_footer_name = 'Arial'
       item.themedata.font_footer_size = 12
       item.themedata.font_footer_color = '#FFFFFF'
       height = 1024
       assert FOOTER_CSS == build_footer_css(item, height), 'The footer strings should be equal.'

