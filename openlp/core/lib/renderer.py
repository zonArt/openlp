# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
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
        log.debug(u'Initialisation started')
        self.theme_manager = theme_manager
        self.image_manager = image_manager
        self.screens = ScreenList.get_instance()
        self.service_theme = u''
        self.theme_level = u''
        self.override_background = None
        self.theme_data = None
        self.bg_frame = None
        self.force_page = False
        self.display = MainDisplay(None, self.image_manager, False)
        self.display.setup()

    def update_display(self):
        """
        Updates the render manager's information about the current screen.
        """
        log.debug(u'Update Display')
        self._calculate_default(self.screens.current[u'size'])
        if self.display:
            self.display.close()
        self.display = MainDisplay(None, self.image_manager, False)
        self.display.setup()
        self.bg_frame = None
        self.theme_data = None

    def set_global_theme(self, global_theme, theme_level=ThemeLevel.Global):
        """
        Set the global-level theme and the theme level.

        ``global_theme``
            The global-level theme to be set.

        ``theme_level``
            Defaults to ``ThemeLevel.Global``. The theme level, can be
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
        # if No file do not update cache
        if self.theme_data.background_filename:
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
        self.force_page = False

    def format_slide(self, text, item):
        """
        Calculate how much text can fit on a slide.

        ``text``
            The words to go on the slides.

        ``item``
            The :class:`~openlp.core.lib.serviceitem.ServiceItem` item object.
        """
        log.debug(u'format slide')
        # Add line endings after each line of text used for bibles.
        line_end = u'<br>'
        if item.is_capable(ItemCapabilities.NoLineBreaks):
            line_end = u' '
        # Bibles
        if item.is_capable(ItemCapabilities.AllowsWordSplit):
            pages = self._paginate_slide_words(text, line_end)
        else:
            # Clean up line endings.
            lines = self._lines_split(text)
            pages = self._paginate_slide(lines, line_end)
            #TODO: Maybe move the detection to _paginate_slide.
            if len(pages) > 1:
                # Songs and Custom
                if item.is_capable(ItemCapabilities.AllowsVirtualSplit):
                    # Do not forget the line breaks!
                    slides = text.split(u'[---]')
                    pages = []
                    for slide in slides:
                        lines = slide.strip(u'\n').split(u'\n')
                        pages.extend(self._paginate_slide(lines, line_end))
        new_pages = []
        for page in pages:
            while page.endswith(u'<br>'):
                page = page[:-4]
            new_pages.append(page)
        return new_pages

    def _calculate_default(self, screen):
        """
        Calculate the default dimentions of the screen.

        ``screen``
            The screen to calculate the default of.
        """
        log.debug(u'_calculate default %s', screen)
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
        log.debug(u'_set_text_rectangle %s , %s' % (rect_main, rect_footer))
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
            u'#main {position:absolute; top:0px; %s %s}</style></head><body>' \
            u'<div id="main">' % \
            (build_lyrics_format_css(self.theme_data, self.page_width,
            self.page_height), build_lyrics_outline_css(self.theme_data))

    def _paginate_slide(self, lines, line_end):
        """
        Figure out how much text can appear on a slide, using the current
        theme settings.

        ``lines``
            The text to be fitted on the slide split into lines.

        ``line_end``
            The text added after each line. Either ``u' '`` or ``u'<br>``.
        """
        log.debug(u'_paginate_slide - Start')
        formatted = []
        previous_html = u''
        previous_raw = u''
        separator = u'<br>'
        html_lines = map(expand_tags, lines)
        html = self.page_shell + separator.join(html_lines) + HTML_END
        self.web.setHtml(html)
        # Text too long so go to next page.
        if self.web_frame.contentsSize().height() > self.page_height:
            html_text, previous_raw = self._binary_chop(formatted,
                previous_html, previous_raw, html_lines, lines, separator, u'')
        else:
            previous_raw = separator.join(lines)
        if previous_raw:
            formatted.append(previous_raw)
        log.debug(u'_paginate_slide - End')
        return formatted

    def _paginate_slide_words(self, text, line_end):
        """
        Figure out how much text can appear on a slide, using the current
        theme settings. This version is to handle text which needs to be split
        into words to get it to fit.

        ``text``
            The words to be fitted on the slide split into lines.

        ``line_end``
            The text added after each line. Either ``u' '`` or ``u'<br>``. This
            is needed for bibles.
        """
        log.debug(u'_paginate_slide_words - Start')
        formatted = []
        previous_html = u''
        previous_raw = u''
        lines = text.split(u'\n')
        for line in lines:
            line = line.strip()
            html_line = expand_tags(line)
            html = self.page_shell + previous_html + html_line + HTML_END
            self.web.setHtml(html)
            # Text too long so go to next page.
            if self.web_frame.contentsSize().height() > self.page_height:
                # Check if there was a verse before the current one and append
                # it, when it fits on the page.
                if previous_html:
                    html = self.page_shell + previous_html + HTML_END
                    self.web.setHtml(html)
                    if self.web_frame.contentsSize().height() <= \
                        self.page_height:
                        formatted.append(previous_raw)
                        previous_html = u''
                        previous_raw = u''
                        html = self.page_shell + html_line + HTML_END
                        self.web.setHtml(html)
                        # Now check if the current verse will fit, if it does
                        # not we have to start to process the verse word by
                        # word.
                        if self.web_frame.contentsSize().height() <= \
                            self.page_height:
                            previous_html = html_line + line_end
                            previous_raw = line + line_end
                            continue
                # Figure out how many words of the line will fit on screen as
                # the line will not fit as a whole.
                raw_words = self._words_split(line)
                html_words = map(expand_tags, raw_words)
                previous_html, previous_raw = self._binary_chop(
                    formatted, previous_html, previous_raw, html_words,
                    raw_words, u' ', line_end)
            else:
                previous_html += html_line + line_end
                previous_raw += line + line_end
        formatted.append(previous_raw)
        log.debug(u'_paginate_slide_words - End')
        return formatted

    def _binary_chop(self, formatted, previous_html, previous_raw, html_list,
        raw_list, separator, line_end):
        """
        This implements the binary chop algorithm for faster rendering. However,
        it is assumed that this method is **only** called, when the text to be
        rendered does not fit as a whole.

        ``formatted``
            The list of slides.

        ``previous_html``
            The html text which is know to fit on a slide, but is not yet added
            to the list of slides. (unicode string)

        ``previous_raw``
            The raw text (with display tags) which is know to fit on a slide,
            but is not yet added to the list of slides. (unicode string)

        ``html_list``
            The text which does not fit on a slide and needs to be processed
            using the binary chop. The text contains html.

        ``raw_list``
            The text which does not fit on a slide and needs to be processed
            using the binary chop. The text can contain display tags.

        ``separator``
            The separator for the elements. For lines this is `u'<br>'`` and for
            words this is u' '.

        ``line_end``
            The text added after each "element line". Either ``u' '`` or
            ``u'<br>``. This is needed for bibles.
        """
        smallest_index = 0
        highest_index = len(html_list) - 1
        index = int(highest_index / 2)
        while True:
            html = self.page_shell + previous_html + \
                separator.join(html_list[:index + 1]).strip() + HTML_END
            self.web.setHtml(html)
            if self.web_frame.contentsSize().height() > self.page_height:
                # We know that it does not fit, so change/calculate the
                # new index and highest_index accordingly.
                highest_index = index
                index = int(index - (index - smallest_index) / 2)
            else:
                smallest_index = index
                index = int(index + (highest_index - index) / 2)
            # We found the number of words which will fit.
            if smallest_index == index or highest_index == index:
                index = smallest_index
                formatted.append(previous_raw.rstrip(u'<br>') +
                    separator.join(raw_list[:index + 1]))
                previous_html = u''
                previous_raw = u''
                # Stop here as the theme line count was requested.
                if self.force_page:
                    Receiver.send_message(u'theme_line_count', index + 1)
                    break
            else:
                continue
            # Check if the rest of the line fits on the slide. If it
            # does we do not have to do the much more intensive "word by
            # word" checking.
            html = self.page_shell + \
                separator.join(html_list[index + 1:]).strip() + HTML_END
            self.web.setHtml(html)
            if self.web_frame.contentsSize().height() <= self.page_height:
                previous_html = separator.join(
                    html_list[index + 1:]).strip() + line_end
                previous_raw = separator.join(
                    raw_list[index + 1:]).strip() + line_end
                break
            else:
                # The other words do not fit, thus reset the indexes,
                # create a new list and continue with "word by word".
                raw_list = raw_list[index + 1:]
                html_list = html_list[index + 1:]
                smallest_index = 0
                highest_index = len(html_list) - 1
                index = int(highest_index / 2)
        return previous_html, previous_raw

    def _words_split(self, line):
        """
        Split the slide up by word so can wrap better
        """
        # this parse we are to be wordy
        line = line.replace(u'\n', u' ')
        return line.split(u' ')

    def _lines_split(self, text):
        """
        Split the slide up by physical line
        """
        # this parse we do not want to use this so remove it
        text = text.replace(u'\n[---]', u'')
        lines = text.split(u'\n')
        return [line.replace(u'[---]', u'') for line in lines]
