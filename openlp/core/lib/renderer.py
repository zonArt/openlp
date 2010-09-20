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
"""
The :mod:`renderer` module enables OpenLP to take the input from plugins and
format it for the output display.
"""
import logging

from PyQt4 import QtGui, QtCore, QtWebKit

from openlp.core.lib import resize_image, expand_tags, \
    build_lyrics_format_css, build_lyrics_outline_css, image_to_byte


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
        self._bg_image_filename = None
        self.frame = None
        self.bg_frame = None
        self.bg_image = None
        self.bg_image_bytes = None

    def set_theme(self, theme):
        """
        Set the theme to be used.

        ``theme``
            The theme to be used.
        """
        log.debug(u'set theme')
        self._theme = theme
        self.bg_frame = None
        self.bg_image = None
        self.bg_image_bytes = None
        self._bg_image_filename = None
        self.theme_name = theme.theme_name
        if theme.background_type == u'image':
            if theme.background_filename:
                self._bg_image_filename = unicode(theme.background_filename)

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
        if self._theme.display_shadow:
            self.page_width -= int(self._theme.display_shadow_size)
            self.page_height -= int(self._theme.display_shadow_size)
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

        self.web = QtWebKit.QWebView()
        self.web.resize(self._rect.width(), self._rect.height())
        self.web.setVisible(False)
        self.web_frame = self.web.page().mainFrame()
        # Adjust width and height to account for shadow. outline done in css
        self.page_width = self._rect.width() - int(self._theme.display_shadow_size)
        self.page_height = self._rect.height() - int(self._theme.display_shadow_size)
        self.page_shell = u'<html><head><style>#main {%s %s}</style><body>' \
            u'<div id="main">' % \
            (build_lyrics_format_css(self._theme, self.page_width, self.page_height),
            build_lyrics_outline_css(self._theme))

    def set_frame_dest(self, frame_width, frame_height):
        """
        Set the size of the slide.

        ``frame_width``
            The width of the slide.

        ``frame_height``
            The height of the slide.

        """
        log.debug(u'set frame dest (frame) w %d h %d', frame_width,
            frame_height)
        self.frame = QtGui.QImage(frame_width, frame_height,
            QtGui.QImage.Format_ARGB32_Premultiplied)
        if self._bg_image_filename and not self.bg_image:
            self.bg_image = resize_image(self._bg_image_filename,
                self.frame.width(), self.frame.height())
        if self._theme.background_type == u'image':
            self.bg_frame = QtGui.QImage(self.frame.width(),
                self.frame.height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
            painter = QtGui.QPainter()
            painter.begin(self.bg_frame)
            painter.fillRect(self.frame.rect(), QtCore.Qt.black)
            if self.bg_image:
                painter.drawImage(0, 0, self.bg_image)
            painter.end()
            self.bg_image_bytes = image_to_byte(self.bg_frame)
        else:
            self.bg_frame = None
            self.bg_image_bytes = None

    def format_slide(self, words, line_break):
        """
        Figure out how much text can appear on a slide, using the current
        theme settings.

        ``words``
            The words to be fitted on the slide.
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
        for line in text:
            styled_line = expand_tags(line) + line_end
            styled_text += styled_line
            html = self.page_shell + styled_text + u'</div></body></html>'
            self.web.setHtml(html)
            # Text too long so go to next page
            if self.web_frame.contentsSize().height() > self.page_height:
                formatted.append(html_text)
                html_text = u''
                styled_text = styled_line
            html_text += line + line_end
        formatted.append(html_text)
        log.debug(u'format_slide - End')
        return formatted
