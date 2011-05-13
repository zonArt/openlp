# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

from PyQt4 import QtCore, QtWebKit

from openlp.core.lib import ServiceItem, expand_tags, \
    build_lyrics_format_css, build_lyrics_outline_css, Receiver, \
    ItemCapabilities
from openlp.core.lib.theme import ThemeLevel
from openlp.core.ui import MainDisplay, ScreenList

log = logging.getLogger(__name__)

VERSE = u'The Lord said to {r}Noah{/r}: \n' \
    'There\'s gonna be a {su}floody{/su}, {sb}floody{/sb}\n' \
    'The Lord said to {g}Noah{/g}:\n' \
    'There\'s gonna be a {st}floody{/st}, {it}floody{/it}\n' \
    'Get those children out of the muddy, muddy \n' \
    '{r}C{/r}{b}h{/b}{bl}i{/bl}{y}l{/y}{g}d{/g}{pk}' \
    'r{/pk}{o}e{/o}{pp}n{/pp} of the Lord\n'
FOOTER = [u'Arky Arky (Unknown)', u'Public Domain', u'CCLI 123456']

HTML_END = u'</div></body></html>'

class Renderer(object):
    """
    Class to pull all Renderer interactions into one place. The plugins will
    call helper methods to do the rendering but this class will provide
    display defense code.
    """
    log.info(u'Renderer Loaded')

    def __init__(self, image_manager, theme_manager):
        """
        Initialise the render manager.

    ``image_manager``
        A ImageManager instance which takes care of e. g. caching and resizing
        images.

    ``theme_manager``
        The ThemeManager instance, used to get the current theme details.
        """
        log.debug(u'Initilisation started')
        self.theme_manager = theme_manager
        self.image_manager = image_manager
        self.screens = ScreenList.get_instance()
        self.service_theme = u''
        self.theme_level = u''
        self.override_background = None
        self.theme_data = None
        self.bg_frame = None
        self.force_page = False
        self.display = MainDisplay(self, self.image_manager, False)
        self.display.setup()

    def update_display(self):
        """
        Updates the render manager's information about the current screen.
        """
        log.debug(u'Update Display')
        self._calculate_default(self.screens.current[u'size'])
        self.display = MainDisplay(self, self.image_manager, False)
        self.display.setup()
        self.bg_frame = None
        self.theme_data = None

    def set_global_theme(self, global_theme, theme_level=ThemeLevel.Global):
        """
        Set the global-level theme and the theme level.

        ``global_theme``
            The global-level theme to be set.

        ``theme_level``
            Defaults to *``ThemeLevel.Global``*. The theme level, can be
            ``ThemeLevel.Global``, ``ThemeLevel.Service`` or
            ``ThemeLevel.Song``.
        """
        self.global_theme = global_theme
        self.theme_level = theme_level
        self.global_theme_data = \
            self.theme_manager.getThemeData(self.global_theme)
        self.theme_data = None

    def set_service_theme(self, service_theme):
        """
        Set the service-level theme.

        ``service_theme``
            The service-level theme to be set.
        """
        self.service_theme = service_theme
        self.theme_data = None

    def set_override_theme(self, override_theme, override_levels=False):
        """
        Set the appropriate theme depending on the theme level.
        Called by the service item when building a display frame

        ``theme``
            The name of the song-level theme. None means the service
            item wants to use the given value.

        ``override_levels``
            Used to force the theme data passed in to be used.

        """
        log.debug(u'set override theme to %s', override_theme)
        theme_level = self.theme_level
        if override_levels:
            theme_level = ThemeLevel.Song
        if theme_level == ThemeLevel.Global:
            theme = self.global_theme
        elif theme_level == ThemeLevel.Service:
            if self.service_theme == u'':
                theme = self.global_theme
            else:
                theme = self.service_theme
        else:
            # Images have a theme of -1
            if override_theme and override_theme != -1:
                theme = override_theme
            elif theme_level == ThemeLevel.Song or \
                theme_level == ThemeLevel.Service:
                if self.service_theme == u'':
                    theme = self.global_theme
                else:
                    theme = self.service_theme
            else:
                theme = self.global_theme
        log.debug(u'theme is now %s', theme)
        # Force the theme to be the one passed in.
        if override_levels:
            self.theme_data = override_theme
        else:
            self.theme_data = self.theme_manager.getThemeData(theme)
        self._calculate_default(self.screens.current[u'size'])
        self._build_text_rectangle(self.theme_data)
        self.image_manager.add_image(self.theme_data.theme_name,
            self.theme_data.background_filename)
        return self._rect, self._rect_footer

    def generate_preview(self, theme_data, force_page=False):
        """
        Generate a preview of a theme.

        ``theme_data``
            The theme to generated a preview for.

        ``force_page``
            Flag to tell message lines per page need to be generated.
        """
        log.debug(u'generate preview')
        # save value for use in format_slide
        self.force_page = force_page
        # set the default image size for previews
        self._calculate_default(self.screens.preview[u'size'])
        # build a service item to generate preview
        serviceItem = ServiceItem()
        serviceItem.theme = theme_data
        if self.force_page:
            # make big page for theme edit dialog to get line count
            serviceItem.add_from_text(u'', VERSE + VERSE + VERSE)
        else:
            self.image_manager.del_image(theme_data.theme_name)
            serviceItem.add_from_text(u'', VERSE)
        serviceItem.renderer = self
        serviceItem.raw_footer = FOOTER
        serviceItem.render(True)
        if not self.force_page:
            self.display.buildHtml(serviceItem)
            raw_html = serviceItem.get_rendered_frame(0)
            preview = self.display.text(raw_html)
            # Reset the real screen size for subsequent render requests
            self._calculate_default(self.screens.current[u'size'])
            return preview

    def format_slide(self, text, line_break, item):
        """
        Calculate how much text can fit on a slide.

        ``text``
            The words to go on the slides.

        ``line_break``
            Add line endings after each line of text used for bibles.
        """
        log.debug(u'format slide')
        # clean up line endings
        lines = self._lines_split(text)
        pages = self._paginate_slide(lines, line_break, self.force_page)
        if len(pages) > 1:
            # Songs and Custom
            if item.is_capable(ItemCapabilities.AllowsVirtualSplit):
                # Do not forget the line breaks !
                slides = text.split(u'[---]')
                pages = []
                for slide in slides:
                    lines = slide.strip(u'\n').split(u'\n')
                    new_pages = self._paginate_slide(lines, line_break,
                        self.force_page)
                    pages.extend(new_pages)
            # Bibles
            elif item.is_capable(ItemCapabilities.AllowsWordSplit):
                pages = self._paginate_slide_words(text, line_break)
        return pages

    def _calculate_default(self, screen):
        """
        Calculate the default dimentions of the screen.

        ``screen``
            The QSize of the screen.
        """
        log.debug(u'calculate default %s', screen)
        self.width = screen.width()
        self.height = screen.height()
        self.screen_ratio = float(self.height) / float(self.width)
        log.debug(u'calculate default %d, %d, %f',
            self.width, self.height, self.screen_ratio)
        # 90% is start of footer
        self.footer_start = int(self.height * 0.90)

    def _build_text_rectangle(self, theme):
        """
        Builds a text block using the settings in ``theme``
        and the size of the display screen.height.
        Note the system has a 10 pixel border round the screen

        ``theme``
            The theme to build a text block for.
        """
        log.debug(u'_build_text_rectangle')
        main_rect = None
        footer_rect = None
        if not theme.font_main_override:
            main_rect = QtCore.QRect(10, 0, self.width - 20, self.footer_start)
        else:
            main_rect = QtCore.QRect(theme.font_main_x, theme.font_main_y,
                theme.font_main_width - 1, theme.font_main_height - 1)
        if not theme.font_footer_override:
            footer_rect = QtCore.QRect(10, self.footer_start, self.width - 20,
                self.height - self.footer_start)
        else:
            footer_rect = QtCore.QRect(theme.font_footer_x,
                theme.font_footer_y, theme.font_footer_width - 1,
                theme.font_footer_height - 1)
        self._set_text_rectangle(main_rect, footer_rect)

    def _set_text_rectangle(self, rect_main, rect_footer):
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
        if self.theme_data.font_main_shadow:
            self.page_width -= int(self.theme_data.font_main_shadow_size)
            self.page_height -= int(self.theme_data.font_main_shadow_size)
        self.web = QtWebKit.QWebView()
        self.web.setVisible(False)
        self.web.resize(self.page_width, self.page_height)
        self.web_frame = self.web.page().mainFrame()
        # Adjust width and height to account for shadow. outline done in css
        self.page_shell = u'<html><head><style>' \
            u'*{margin: 0; padding: 0; border: 0;} '\
            u'#main {position:absolute; top:0px; %s %s}</style><body>' \
            u'<div id="main">' % \
            (build_lyrics_format_css(self.theme_data, self.page_width,
            self.page_height), build_lyrics_outline_css(self.theme_data))

    def _paginate_slide(self, lines, line_break, force_page=False):
        """
        Figure out how much text can appear on a slide, using the current
        theme settings.

        ``lines``
            The words to be fitted on the slide split into lines.

        ``line_break``
            Add line endings after each line of text (used for bibles).

        ``force_page``
            Flag to tell message lines in page.

        """
        log.debug(u'_paginate_slide - Start')
        line_end = u''
        if line_break:
            line_end = u'<br>'
        formatted = []
        html_text = u''
        styled_text = u''
        line_count = 0
        for line in lines:
            if line_count != -1:
                line_count += 1
            styled_line = expand_tags(line) + line_end
            styled_text += styled_line
            html = self.page_shell + styled_text + HTML_END
            self.web.setHtml(html)
            # Text too long so go to next page
            if self.web_frame.contentsSize().height() > self.page_height:
                if force_page and line_count > 0:
                    Receiver.send_message(u'theme_line_count', line_count)
                line_count = -1
                while html_text.endswith(u'<br>'):
                    html_text = html_text[:-4]
                formatted.append(html_text)
                html_text = u''
                styled_text = styled_line
            html_text += line + line_end
        while html_text.endswith(u'<br>'):
            html_text = html_text[:-4]
        formatted.append(html_text)
        log.debug(u'_paginate_slide - End')
        return formatted

    def _paginate_slide_words(self, text, line_break):
        """
        Figure out how much text can appear on a slide, using the current
        theme settings. This version is to handle text which needs to be split
        into words to get it to fit.

        ``text``
            The words to be fitted on the slide split into lines.

        ``line_break``
            Add line endings after each line of text used for bibles.

        """
        log.debug(u'_paginate_slide_words - Start')
        line_end = u''
        if line_break:
            line_end = u'<br>'
        formatted = []
        previous_html = u''
        previous_raw = u''
        lines = text.split(u'\n')
        for line in lines:
            styled_line = expand_tags(line)
            html = self.page_shell + previous_html + styled_line + HTML_END
            self.web.setHtml(html)
            # Text too long so go to next page
            if self.web_frame.contentsSize().height() > self.page_height:
                # Check if there was a verse before the current one and append
                # it, when it fits on the page.
                if previous_html:
                    html = self.page_shell + previous_html + HTML_END
                    self.web.setHtml(html)
                    if self.web_frame.contentsSize().height() <= \
                        self.page_height:
                        while previous_raw.endswith(u'<br>'):
                            previous_raw = previous_raw[:-4]
                        formatted.append(previous_raw)
                        previous_html = u''
                        previous_raw = u''
                        html = self.page_shell + styled_line + HTML_END
                        self.web.setHtml(html)
                        # Now check if the current verse will fit, if it does
                        # not we have to start to process the verse word by
                        # word.
                        if self.web_frame.contentsSize().height() <= \
                            self.page_height:
                            previous_html = styled_line + line_end
                            previous_raw = line + line_end
                            continue
                words = self._words_split(line)
                for word in words:
                    styled_word = expand_tags(word)
                    html = self.page_shell + previous_html + styled_word + \
                        HTML_END
                    self.web.setHtml(html)
                    # Text too long so go to next page
                    if self.web_frame.contentsSize().height() > \
                        self.page_height:
                        while previous_raw.endswith(u'<br>'):
                            previous_raw = previous_raw[:-4]
                        formatted.append(previous_raw)
                        previous_html = u''
                        previous_raw = u''
                    previous_html += styled_word
                    previous_raw += word
                previous_html += line_end
                previous_raw += line_end
            else:
                previous_html += styled_line + line_end
                previous_raw += line + line_end
        while previous_raw.endswith(u'<br>'):
            previous_raw = previous_raw[:-4]
        formatted.append(previous_raw)
        log.debug(u'_paginate_slide_words - End')
        return formatted

    def _words_split(self, line):
        """
        Split the slide up by word so can wrap better
        """
        # this parse we are to be wordy
        line = line.replace(u'\n', u' ')
        words = line.split(u' ')
        return [word + u' ' for word in words]

    def _lines_split(self, text):
        """
        Split the slide up by physical line
        """
        # this parse we do not want to use this so remove it
        text = text.replace(u'\n[---]', u'')
        lines = text.split(u'\n')
        return [line.replace(u'[---]', u'') for line in lines]
