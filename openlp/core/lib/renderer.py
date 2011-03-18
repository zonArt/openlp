# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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
The :mod:`renderer` module enables OpenLP to take the input from plugins and
format it for the output display.
"""
import logging

from PyQt4 import QtWebKit

from openlp.core.lib import expand_tags, build_lyrics_format_css, \
    build_lyrics_outline_css, Receiver

log = logging.getLogger(__name__)

class Renderer(object):
    """
    Genarates a pixmap image of a array of text. The Text is formatted to
    make sure it fits on the screen and if not extra frames are generated.
    """
    log.info(u'Renderer Loaded')

    def __init__(self):
        """
        Initialise the renderer.
        """
        self._rect = None
        self.theme_name = None
        self._theme = None

    def set_theme(self, theme):
        """
        Set the theme to be used.

        ``theme``
            The theme to be used.
        """
        log.debug(u'set theme')
        self._theme = theme
        self.theme_name = theme.theme_name

    def set_text_rectangle(self, rect_main, rect_footer):
        """
        Sets the rectangle within which text should be rendered.

        ``rect_main``
            The main text block.

        ``rect_footer``
            The footer text block.
        """
        log.debug(u'set_text_rectangle %s , %s' % (rect_main, rect_footer))
        self._rect = rect_main
        self._rect_footer = rect_footer
        self.page_width = self._rect.width()
        self.page_height = self._rect.height()
        if self._theme.font_main_shadow:
            self.page_width -= int(self._theme.font_main_shadow_size)
            self.page_height -= int(self._theme.font_main_shadow_size)
        self.web = QtWebKit.QWebView()
        self.web.setVisible(False)
        self.web.resize(self.page_width, self.page_height)
        self.web_frame = self.web.page().mainFrame()
        # Adjust width and height to account for shadow. outline done in css
        self.page_shell = u'<html><head><style>' \
            u'*{margin: 0; padding: 0; border: 0;} '\
            u'#main {position:absolute; top:0px; %s %s}</style><body>' \
            u'<div id="main">' % \
            (build_lyrics_format_css(self._theme, self.page_width,
            self.page_height), build_lyrics_outline_css(self._theme))

    def format_slide(self, words, line_break, force_page=False):
        """
        Figure out how much text can appear on a slide, using the current
        theme settings.

        ``words``
            The words to be fitted on the slide.

        ``line_break``
            Add line endings after each line of text used for bibles.

        ``force_page``
            Flag to tell message lines in page.

        """
        log.debug(u'format_slide - Start')
        line_end = u''
        if line_break:
            line_end = u'<br>'
        words = words.replace(u'\r\n', u'\n')
        verses_text = words.split(u'\n')
        text = []
        for verse in verses_text:
            lines = verse.split(u'\n')
            for line in lines:
                text.append(line)
        formatted = []
        html_text = u''
        styled_text = u''
        line_count = 0
        for line in text:
            if line_count != -1:
                line_count += 1
            styled_line = expand_tags(line) + line_end
            styled_text += styled_line
            html = self.page_shell + styled_text + u'</div></body></html>'
            self.web.setHtml(html)
            # Text too long so go to next page
            if self.web_frame.contentsSize().height() > self.page_height:
                if force_page and line_count > 0:
                    Receiver.send_message(u'theme_line_count', line_count)
                line_count = -1
                if html_text.endswith(u'<br>'):
                    html_text = html_text[:len(html_text)-4]
                formatted.append(html_text)
                html_text = u''
                styled_text = styled_line
            html_text += line + line_end
        if html_text.endswith(u'<br>'):
            html_text = html_text[:len(html_text)-4]
        formatted.append(html_text)
        log.debug(u'format_slide - End')
        return formatted
