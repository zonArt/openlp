# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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

from PyQt4 import QtGui, QtCore, QtWebKit

from openlp.core.lib import FormattingTags, ImageSource, ItemCapabilities, Receiver, Registry, ScreenList, \
    ServiceItem, expand_tags, build_lyrics_format_css, build_lyrics_outline_css
from openlp.core.lib.theme import ThemeLevel
from openlp.core.ui import MainDisplay

log = logging.getLogger(__name__)

VERSE = u'The Lord said to {r}Noah{/r}: \n' \
    'There\'s gonna be a {su}floody{/su}, {sb}floody{/sb}\n' \
    'The Lord said to {g}Noah{/g}:\n' \
    'There\'s gonna be a {st}floody{/st}, {it}floody{/it}\n' \
    'Get those children out of the muddy, muddy \n' \
    '{r}C{/r}{b}h{/b}{bl}i{/bl}{y}l{/y}{g}d{/g}{pk}' \
    'r{/pk}{o}e{/o}{pp}n{/pp} of the Lord\n'
VERSE_FOR_LINE_COUNT = u'\n'.join(map(unicode, xrange(50)))
FOOTER = [u'Arky Arky (Unknown)', u'Public Domain', u'CCLI 123456']


class Renderer(object):
    """
    Class to pull all Renderer interactions into one place. The plugins will
    call helper methods to do the rendering but this class will provide
    display defense code.
    """
    log.info(u'Renderer Loaded')

    def __init__(self):
        """
        Initialise the renderer.

        ``image_manager``
            A image_manager instance which takes care of e. g. caching and
            resizing images.

        ``theme_manager``
            The theme_manager instance, used to get the current theme details.
        """
        log.debug(u'Initialisation started')
        self.screens = ScreenList()
        Registry().register(u'renderer', self)
        self.theme_level = ThemeLevel.Global
        self.global_theme_name = u''
        self.service_theme_name = u''
        self.item_theme_name = u''
        self.force_page = False
        self.display = MainDisplay(None, False, self)
        self.display.setup()
        self._theme_dimensions = {}
        self._calculate_default()
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'theme_update_global'), self.set_global_theme)
        self.web = QtWebKit.QWebView()
        self.web.setVisible(False)
        self.web_frame = self.web.page().mainFrame()

    def update_display(self):
        """
        Updates the renderer's information about the current screen.
        """
        log.debug(u'Update Display')
        self._calculate_default()
        if self.display:
            self.display.close()
        self.display = MainDisplay(None, False, self)
        self.display.setup()
        self._theme_dimensions = {}

    def update_theme(self, theme_name, old_theme_name=None, only_delete=False):
        """
        This method updates the theme in ``_theme_dimensions`` when a theme
        has been edited or renamed.

        ``theme_name``
            The current theme name.

        ``old_theme_name``
            The old theme name. Has only to be passed, when the theme has been
            renamed. Defaults to *None*.

        ``only_delete``
            Only remove the given ``theme_name`` from the ``_theme_dimensions``
            list. This can be used when a theme is permanently deleted.
        """
        if old_theme_name is not None and old_theme_name in self._theme_dimensions:
            del self._theme_dimensions[old_theme_name]
        if theme_name in self._theme_dimensions:
            del self._theme_dimensions[theme_name]
        if not only_delete:
            self._set_theme(theme_name)

    def _set_theme(self, theme_name):
        """
        Helper method to save theme names and theme data.

        ``theme_name``
            The theme name.
        """
        if theme_name not in self._theme_dimensions:
            theme_data = self.theme_manager.get_theme_data(theme_name)
            main_rect = self.get_main_rectangle(theme_data)
            footer_rect = self.get_footer_rectangle(theme_data)
            self._theme_dimensions[theme_name] = [theme_data, main_rect, footer_rect]
        else:
            theme_data, main_rect, footer_rect = self._theme_dimensions[theme_name]
        # if No file do not update cache
        if theme_data.background_filename:
            self.image_manager.add_image(theme_data.background_filename,
                ImageSource.Theme, QtGui.QColor(theme_data.background_border_color))

    def pre_render(self, override_theme_data=None):
        """
        Set up the theme to be used before rendering an item.

        ``override_theme_data``
            The theme data should be passed, when we want to use our own theme
            data, regardless of the theme level. This should for example be used
            in the theme manager. **Note**, this is **not** to be mixed up with
            the ``set_item_theme`` method.
        """
        # Just assume we use the global theme.
        theme_to_use = self.global_theme_name
        # The theme level is either set to Service or Item. Use the service
        # theme if one is set. We also have to use the service theme, even when
        # the theme level is set to Item, because the item does not necessarily
        # have to have a theme.
        if self.theme_level != ThemeLevel.Global:
            # When the theme level is at Service and we actually have a service
            # theme then use it.
            if self.service_theme_name:
                theme_to_use = self.service_theme_name
        # If we have Item level and have an item theme then use it.
        if self.theme_level == ThemeLevel.Song and self.item_theme_name:
            theme_to_use = self.item_theme_name
        if override_theme_data is None:
            if theme_to_use not in self._theme_dimensions:
                self._set_theme(theme_to_use)
            theme_data, main_rect, footer_rect = self._theme_dimensions[theme_to_use]
        else:
            # Ignore everything and use own theme data.
            theme_data = override_theme_data
            main_rect = self.get_main_rectangle(override_theme_data)
            footer_rect = self.get_footer_rectangle(override_theme_data)
        self._set_text_rectangle(theme_data, main_rect, footer_rect)
        return theme_data, self._rect, self._rect_footer

    def set_theme_level(self, theme_level):
        """
        Sets the theme level.

        ``theme_level``
            The theme level to be used.
        """
        self.theme_level = theme_level

    def set_global_theme(self, global_theme_name):
        """
        Set the global-level theme name.

        ``global_theme_name``
            The global-level theme's name.
        """
        self._set_theme(global_theme_name)
        self.global_theme_name = global_theme_name

    def set_service_theme(self, service_theme_name):
        """
        Set the service-level theme.

        ``service_theme_name``
            The service level theme's name.
        """
        self._set_theme(service_theme_name)
        self.service_theme_name = service_theme_name

    def set_item_theme(self, item_theme_name):
        """
        Set the item-level theme. **Note**, this has to be done for each item we
        are rendering.

        ``item_theme_name``
            The item theme's name.
        """
        self._set_theme(item_theme_name)
        self.item_theme_name = item_theme_name

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
        # build a service item to generate preview
        serviceItem = ServiceItem()
        if self.force_page:
            # make big page for theme edit dialog to get line count
            serviceItem.add_from_text(VERSE_FOR_LINE_COUNT)
        else:
            serviceItem.add_from_text(VERSE)
        serviceItem.raw_footer = FOOTER
        # if No file do not update cache
        if theme_data.background_filename:
            self.image_manager.add_image(theme_data.background_filename,
                ImageSource.Theme,
                QtGui.QColor(theme_data.background_border_color))
        theme_data, main, footer = self.pre_render(theme_data)
        serviceItem.themedata = theme_data
        serviceItem.main = main
        serviceItem.footer = footer
        serviceItem.render(True)
        if not self.force_page:
            self.display.buildHtml(serviceItem)
            raw_html = serviceItem.get_rendered_frame(0)
            self.display.text(raw_html, False)
            preview = self.display.preview()
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
        if item.is_capable(ItemCapabilities.CanWordSplit):
            pages = self._paginate_slide_words(text.split(u'\n'), line_end)
        # Songs and Custom
        elif item.is_capable(ItemCapabilities.CanSoftBreak):
            pages = []
            if u'[---]' in text:
                while True:
                    slides = text.split(u'\n[---]\n', 2)
                    # If there are (at least) two occurrences of [---] we use
                    # the first two slides (and neglect the last for now).
                    if len(slides) == 3:
                        html_text = expand_tags(u'\n'.join(slides[:2]))
                    # We check both slides to determine if the optional split is
                    # needed (there is only one optional split).
                    else:
                        html_text = expand_tags(u'\n'.join(slides))
                    html_text = html_text.replace(u'\n', u'<br>')
                    if self._text_fits_on_slide(html_text):
                        # The first two optional slides fit (as a whole) on one
                        # slide. Replace the first occurrence of [---].
                        text = text.replace(u'\n[---]', u'', 1)
                    else:
                        # The first optional slide fits, which means we have to
                        # render the first optional slide.
                        text_contains_split = u'[---]' in text
                        if text_contains_split:
                            try:
                                text_to_render, text = text.split(u'\n[---]\n', 1)
                            except ValueError:
                                text_to_render = text.split(u'\n[---]\n')[0]
                                text = u''
                            text_to_render, raw_tags, html_tags = self._get_start_tags(text_to_render)
                            if text:
                                text = raw_tags + text
                        else:
                            text_to_render = text
                            text = u''
                        lines = text_to_render.strip(u'\n').split(u'\n')
                        slides = self._paginate_slide(lines, line_end)
                        if len(slides) > 1 and text:
                            # Add all slides apart from the last one the list.
                            pages.extend(slides[:-1])
                            if  text_contains_split:
                                text = slides[-1] + u'\n[---]\n' + text
                            else:
                                text = slides[-1] + u'\n' + text
                            text = text.replace(u'<br>', u'\n')
                        else:
                            pages.extend(slides)
                    if u'[---]' not in text:
                        lines = text.strip(u'\n').split(u'\n')
                        pages.extend(self._paginate_slide(lines, line_end))
                        break
            else:
                # Clean up line endings.
                pages = self._paginate_slide(text.split(u'\n'), line_end)
        else:
            pages = self._paginate_slide(text.split(u'\n'), line_end)
        new_pages = []
        for page in pages:
            while page.endswith(u'<br>'):
                page = page[:-4]
            new_pages.append(page)
        return new_pages

    def _calculate_default(self):
        """
        Calculate the default dimensions of the screen.
        """
        screen_size = self.screens.current[u'size']
        self.width = screen_size.width()
        self.height = screen_size.height()
        self.screen_ratio = float(self.height) / float(self.width)
        log.debug(u'_calculate default %s, %f' % (screen_size,
            self.screen_ratio))
        # 90% is start of footer
        self.footer_start = int(self.height * 0.90)

    def get_main_rectangle(self, theme_data):
        """
        Calculates the placement and size of the main rectangle.

        ``theme_data``
            The theme information
        """
        if not theme_data.font_main_override:
            return QtCore.QRect(10, 0, self.width - 20, self.footer_start)
        else:
            return QtCore.QRect(theme_data.font_main_x, theme_data.font_main_y,
                theme_data.font_main_width - 1, theme_data.font_main_height - 1)

    def get_footer_rectangle(self, theme_data):
        """
        Calculates the placement and size of the footer rectangle.

        ``theme_data``
            The theme data.
        """
        if not theme_data.font_footer_override:
            return QtCore.QRect(10, self.footer_start, self.width - 20,
                self.height - self.footer_start)
        else:
            return QtCore.QRect(theme_data.font_footer_x,
                theme_data.font_footer_y, theme_data.font_footer_width - 1,
                theme_data.font_footer_height - 1)

    def _set_text_rectangle(self, theme_data, rect_main, rect_footer):
        """
        Sets the rectangle within which text should be rendered.

        ``theme_data``
            The theme data.

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
        if theme_data.font_main_shadow:
            self.page_width -= int(theme_data.font_main_shadow_size)
            self.page_height -= int(theme_data.font_main_shadow_size)
        # For the life of my I don't know why we have to completely kill the
        # QWebView in order for the display to work properly, but we do. See
        # bug #1041366 for an example of what happens if we take this out.
        self.web = None
        self.web = QtWebKit.QWebView()
        self.web.setVisible(False)
        self.web.resize(self.page_width, self.page_height)
        self.web_frame = self.web.page().mainFrame()
        # Adjust width and height to account for shadow. outline done in css.
        html = u"""<!DOCTYPE html><html><head><script>
            function show_text(newtext) {
                var main = document.getElementById('main');
                main.innerHTML = newtext;
                // We need to be sure that the page is loaded, that is why we
                // return the element's height (even though we do not use the
                // returned value).
                return main.offsetHeight;
            }
            </script><style>*{margin: 0; padding: 0; border: 0;}
            #main {position: absolute; top: 0px; %s %s}</style></head><body>
            <div id="main"></div></body></html>""" % \
            (build_lyrics_format_css(theme_data, self.page_width,
            self.page_height), build_lyrics_outline_css(theme_data))
        self.web.setHtml(html)
        self.empty_height = self.web_frame.contentsSize().height()

    def _paginate_slide(self, lines, line_end):
        """
        Figure out how much text can appear on a slide, using the current
        theme settings.
        **Note:** The smallest possible "unit" of text for a slide is one line.
        If the line is too long it will be cut off when displayed.

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
        # Text too long so go to next page.
        if not self._text_fits_on_slide(separator.join(html_lines)):
            html_text, previous_raw = self._binary_chop(formatted,
                previous_html, previous_raw, html_lines, lines, separator, u'')
        else:
            previous_raw = separator.join(lines)
        formatted.append(previous_raw)
        log.debug(u'_paginate_slide - End')
        return formatted

    def _paginate_slide_words(self, lines, line_end):
        """
        Figure out how much text can appear on a slide, using the current
        theme settings.
        **Note:** The smallest possible "unit" of text for a slide is one word.
        If one line is too long it will be processed word by word. This is
        sometimes need for **bible** verses.

        ``lines``
            The text to be fitted on the slide split into lines.

        ``line_end``
            The text added after each line. Either ``u' '`` or ``u'<br>``.
            This is needed for **bibles**.
        """
        log.debug(u'_paginate_slide_words - Start')
        formatted = []
        previous_html = u''
        previous_raw = u''
        for line in lines:
            line = line.strip()
            html_line = expand_tags(line)
            # Text too long so go to next page.
            if not self._text_fits_on_slide(previous_html + html_line):
                # Check if there was a verse before the current one and append
                # it, when it fits on the page.
                if previous_html:
                    if self._text_fits_on_slide(previous_html):
                        formatted.append(previous_raw)
                        previous_html = u''
                        previous_raw = u''
                        # Now check if the current verse will fit, if it does
                        # not we have to start to process the verse word by
                        # word.
                        if self._text_fits_on_slide(html_line):
                            previous_html = html_line + line_end
                            previous_raw = line + line_end
                            continue
                # Figure out how many words of the line will fit on screen as
                # the line will not fit as a whole.
                raw_words = self._words_split(line)
                html_words = map(expand_tags, raw_words)
                previous_html, previous_raw = \
                    self._binary_chop(formatted, previous_html, previous_raw, html_words, raw_words, u' ', line_end)
            else:
                previous_html += html_line + line_end
                previous_raw += line + line_end
        formatted.append(previous_raw)
        log.debug(u'_paginate_slide_words - End')
        return formatted

    def _get_start_tags(self, raw_text):
        """
        Tests the given text for not closed formatting tags and returns a tuple
        consisting of three unicode strings::

            (u'{st}{r}Text text text{/r}{/st}', u'{st}{r}', u'<strong>
            <span style="-webkit-text-fill-color:red">')

        The first unicode string is the text, with correct closing tags. The
        second unicode string are OpenLP's opening formatting tags and the third
        unicode string the html opening formatting tags.

        ``raw_text``
            The text to test. The text must **not** contain html tags, only
            OpenLP formatting tags are allowed::

                {st}{r}Text text text
        """
        raw_tags = []
        html_tags = []
        for tag in FormattingTags.get_html_tags():
            if tag[u'start tag'] == u'{br}':
                continue
            if raw_text.count(tag[u'start tag']) != raw_text.count(tag[u'end tag']):
                raw_tags.append((raw_text.find(tag[u'start tag']), tag[u'start tag'], tag[u'end tag']))
                html_tags.append((raw_text.find(tag[u'start tag']), tag[u'start html']))
        # Sort the lists, so that the tags which were opened first on the first
        # slide (the text we are checking) will be opened first on the next
        # slide as well.
        raw_tags.sort(key=lambda tag: tag[0])
        html_tags.sort(key=lambda tag: tag[0])
        # Create a list with closing tags for the raw_text.
        end_tags = []
        start_tags = []
        for tag in raw_tags:
            start_tags.append(tag[1])
            end_tags.append(tag[2])
        end_tags.reverse()
        # Remove the indexes.
        html_tags = [tag[1] for tag in html_tags]
        return raw_text + u''.join(end_tags), u''.join(start_tags), u''.join(html_tags)

    def _binary_chop(self, formatted, previous_html, previous_raw, html_list, raw_list, separator, line_end):
        """
        This implements the binary chop algorithm for faster rendering. This
        algorithm works line based (line by line) and word based (word by word).
        It is assumed that this method is **only** called, when the lines/words
        to be rendered do **not** fit as a whole.

        ``formatted``
            The list to append any slides.

        ``previous_html``
            The html text which is know to fit on a slide, but is not yet added
            to the list of slides. (unicode string)

        ``previous_raw``
            The raw text (with formatting tags) which is know to fit on a slide,
            but is not yet added to the list of slides. (unicode string)

        ``html_list``
            The elements which do not fit on a slide and needs to be processed
            using the binary chop. The text contains html.

        ``raw_list``
            The elements which do not fit on a slide and needs to be processed
            using the binary chop. The elements can contain formatting tags.

        ``separator``
            The separator for the elements. For lines this is ``u'<br>'`` and
            for words this is ``u' '``.

        ``line_end``
            The text added after each "element line". Either ``u' '`` or
            ``u'<br>``. This is needed for bibles.
        """
        smallest_index = 0
        highest_index = len(html_list) - 1
        index = int(highest_index / 2)
        while True:
            if not self._text_fits_on_slide(
                previous_html + separator.join(html_list[:index + 1]).strip()):
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
                text = previous_raw.rstrip(u'<br>') + separator.join(raw_list[:index + 1])
                text, raw_tags, html_tags = self._get_start_tags(text)
                formatted.append(text)
                previous_html = u''
                previous_raw = u''
                # Stop here as the theme line count was requested.
                if self.force_page:
                    Receiver.send_message(u'theme_line_count', index + 1)
                    break
            else:
                continue
            # Check if the remaining elements fit on the slide.
            if self._text_fits_on_slide(
                    html_tags + separator.join(html_list[index + 1:]).strip()):
                previous_html = html_tags + separator.join(html_list[index + 1:]).strip() + line_end
                previous_raw = raw_tags + separator.join(raw_list[index + 1:]).strip() + line_end
                break
            else:
                # The remaining elements do not fit, thus reset the indexes,
                # create a new list and continue.
                raw_list = raw_list[index + 1:]
                raw_list[0] = raw_tags + raw_list[0]
                html_list = html_list[index + 1:]
                html_list[0] = html_tags + html_list[0]
                smallest_index = 0
                highest_index = len(html_list) - 1
                index = int(highest_index / 2)
        return previous_html, previous_raw

    def _text_fits_on_slide(self, text):
        """
        Checks if the given ``text`` fits on a slide. If it does ``True`` is
        returned, otherwise ``False``.

        ``text``
            The text to check. It may contain HTML tags.
        """
        self.web_frame.evaluateJavaScript(u'show_text("%s")' % text.replace(u'\\', u'\\\\').replace(u'\"', u'\\\"'))
        return self.web_frame.contentsSize().height() <= self.empty_height

    def _words_split(self, line):
        """
        Split the slide up by word so can wrap better
        """
        # this parse we are to be wordy
        line = line.replace(u'\n', u' ')
        return line.split(u' ')

    def _get_image_manager(self):
        """
        Adds the image manager to the class dynamically
        """
        if not hasattr(self, u'_image_manager'):
            self._image_manager = Registry().get(u'image_manager')
        return self._image_manager

    image_manager = property(_get_image_manager)

    def _get_theme_manager(self):
        """
        Adds the theme manager to the class dynamically
        """
        if not hasattr(self, u'_theme_manager'):
            self._theme_manager = Registry().get(u'theme_manager')
        return self._theme_manager

    theme_manager = property(_get_theme_manager)

