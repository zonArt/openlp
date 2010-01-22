    # -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

from PyQt4 import QtGui, QtCore
from openlp.core.lib import resize_image

class Renderer(object):
    """
    Genarates a pixmap image of a array of text. The Text is formatted to
    make sure it fits on the screen and if not extra frames are generated.
    """
    global log
    log = logging.getLogger(u'Renderer')
    log.info(u'Renderer Loaded')

    def __init__(self):
        """
        Initialise the renderer.
        """
        self._rect = None
        self._debug = False
        self._right_margin = 64 # the amount of right indent
        self._display_shadow_size_footer = 0
        self._display_outline_size_footer = 0
        self.theme_name = None
        self._theme = None
        self._bg_image_filename = None
        self._frame = None
        self._frameOp = None
        self.bg_frame = None
        self.bg_image = None

    def set_debug(self, debug):
        """
        Set the debug mode of the renderer.

        ``debug``
            The debug mode.
        """
        self._debug = debug

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
        self._bg_image_filename = None
        self.theme_name = theme.theme_name
        self._set_theme_font()
        if theme.background_type == u'image':
            if theme.background_filename:
                self.set_bg_image(theme.background_filename)

    def set_bg_image(self, filename):
        """
        Set a background image.

        ``filename``
            The name of the image file.
        """
        log.debug(u'set bg image %s', filename)
        self._bg_image_filename = unicode(filename)
        if self._frame:
            self.bg_image = resize_image(self._bg_image_filename,
                                         self._frame.width(),
                                         self._frame.height())

    def set_frame_dest(self, frame_width, frame_height, preview=False):
        """
        Set the size of the slide.

        ``frame_width``
            The width of the slide.

        ``frame_height``
            The height of the slide.

        ``preview``
            Defaults to *False*. Whether or not to generate a preview.
        """
        if preview:
            self.bg_frame = None
        log.debug(u'set frame dest (frame) w %d h %d', frame_width,
            frame_height)
        self._frame = QtGui.QImage(frame_width, frame_height,
            QtGui.QImage.Format_ARGB32_Premultiplied)
        self._frameOp = QtGui.QImage(frame_width, frame_height,
            QtGui.QImage.Format_ARGB32_Premultiplied)
        if self._bg_image_filename and not self.bg_image:
            self.bg_image = resize_image(self._bg_image_filename,
                                         self._frame.width(),
                                         self._frame.height())
        if self.bg_frame is None:
            self._generate_background_frame()

    def format_slide(self, words, footer):
        """
        Figure out how much text can appear on a slide, using the current
        theme settings.

        ``words``
            The words to be fitted on the slide.

        ``footer``
            The footer of the slide.
        """
        log.debug(u'format_slide - Start')
        words = words.replace(u'\r\n', u'\n')
        verses_text = words.split(u'\n')
        text = []
        for verse in verses_text:
            lines = verse.split(u'\n')
            for line in lines:
                text.append(line)
        split_text = self.pre_render_text(text)
        log.debug(u'format_slide - End')
        return split_text

    def pre_render_text(self, text):
        metrics = QtGui.QFontMetrics(self.mainFont)
        #work out line width
        line_width = self._rect.width() - self._right_margin
        #number of lines on a page - adjust for rounding up.
        line_height = metrics.height()
        if self._theme.display_shadow:
            line_height += int(self._theme.display_shadow_size)
        if self._theme.display_outline:
            #  pixels top/bottom
            line_height += 2 * int(self._theme.display_outline_size)
        page_length = int(self._rect.height() / line_height )
        #Average number of characters in line
        ave_line_width = line_width / metrics.averageCharWidth()
        #Maximum size of a character
        max_char_width = metrics.maxWidth()
        #Max characters pre line based on min size of a character
        char_per_line = line_width / metrics.width(u'i')
        log.debug(u'Page Length  area height %s , metrics %s , lines %s' %
                  (int(self._rect.height()), metrics.height(), page_length ))
        split_pages = []
        page = []
        split_lines = []
        count = 0
        for line in text:
            #Must be a blank line so keep it.
            if len(line) == 0:
                line = u' '
            while len(line) > 0:
                pos = char_per_line
                split_text = line[:pos]
                #line needs splitting
                if metrics.width(split_text, -1) > line_width:
                    #We have no spaces
                    if split_text.find(u' ') == -1:
                        #Move back 1 char at a time till it fits
                        while metrics.width(split_text, -1) > line_width:
                            split_text = split_text[:-1]
                            pos = len(split_text)
                    else:
                        #We have spaces so split at previous one
                        while metrics.width(split_text, -1) > line_width:
                            pos = split_text.rfind(u' ')
                            #no more spaces and we are still too long
                            if pos == -1:
                                while metrics.width(split_text, -1) > line_width:
                                    split_text = split_text[:-1]
                                    pos = len(split_text)
                            else:
                                split_text = line[:pos]
                split_lines.append(split_text)
                line = line[pos:].lstrip()
                #if we have more text add up to 10 spaces on the front.
                if len(line) > 0 and self._theme.font_main_indentation > 0:
                    line = u'%s%s' % \
                        (u'          '[:int(self._theme.font_main_indentation)], line)
                #Text fits in a line now
        for count, line in enumerate(split_lines):
            page.append(line)
            #last but one line and only 2 lines to go or end of page
            if (len(page) == page_length - 1 and len(split_lines) - 3 == count) or \
                len(page) == page_length:
                split_pages.append(page)
                page = []
        if len(page) > 0 and page != u' ':
            split_pages.append(page)
        return split_pages

    def set_text_rectangle(self, rect_main, rect_footer):
        """
        Sets the rectangle within which text should be rendered.

        ``rect_main``
            The main text block.

        ``rect_footer``
            The footer text block.
        """
        self._rect = rect_main
        self._rect_footer = rect_footer

    def generate_frame_from_lines(self, lines, footer_lines=None):
        """
        Render a set of lines according to the theme, and return the block
        dimensions.

        ``lines``
            The lines to be rendered.

        ``footer_lines``
            Defaults to *None*. The footer to render.
        """
        log.debug(u'generate_frame_from_lines - Start')
        bbox = self._render_lines_unaligned(lines, False)
        if footer_lines:
            bbox1 = self._render_lines_unaligned(footer_lines, True)
        # reset the frame. first time do not worry about what you paint on.
        self._frame = QtGui.QImage(self.bg_frame)
        self._frameOp = QtGui.QImage(self.bg_frame)
        x, y = self._correctAlignment(self._rect, bbox)
        bbox = self._render_lines_unaligned(lines, False, (x, y), True)
        if footer_lines:
            bbox = self._render_lines_unaligned(footer_lines, True,
                (self._rect_footer.left(), self._rect_footer.top()), True)
        log.debug(u'generate_frame_from_lines - Finish')
        if self._theme.display_slideTransition:
            return {u'main':self._frame, u'trans':self._frameOp}
        else:
            return {u'main':self._frame, u'trans':None}

    def _generate_background_frame(self):
        """
        Generate a background frame to the same size as the frame to be used.
        Results are cached for performance reasons.
        """
        assert(self._theme)
        if self._theme.background_mode == u'transparent':
            self.bg_frame = \
                QtGui.QPixmap(self._frame.width(), self._frame.height())
            self.bg_frame.fill(QtCore.Qt.transparent)
        else:
            self.bg_frame = QtGui.QImage(self._frame.width(), self._frame.height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
        log.debug(u'render background %s start', self._theme.background_type)
        painter = QtGui.QPainter()
        painter.begin(self.bg_frame)
        if self._theme.background_mode == u'transparent':
            painter.fillRect(self._frame.rect(), QtCore.Qt.transparent)
        else:
            if self._theme.background_type == u'solid':
                painter.fillRect(self._frame.rect(),
                    QtGui.QColor(self._theme.background_color))
            elif self._theme.background_type == u'gradient':
                # gradient
                gradient = None
                if self._theme.background_direction == u'horizontal':
                    w = int(self._frame.width()) / 2
                    # vertical
                    gradient = QtGui.QLinearGradient(w, 0, w,
                        self._frame.height())
                elif self._theme.background_direction == u'vertical':
                    h = int(self._frame.height()) / 2
                    # Horizontal
                    gradient = QtGui.QLinearGradient(0, h, self._frame.width(),
                        h)
                else:
                    w = int(self._frame.width()) / 2
                    h = int(self._frame.height()) / 2
                    # Circular
                    gradient = QtGui.QRadialGradient(w, h, w)
                gradient.setColorAt(0,
                    QtGui.QColor(self._theme.background_startColor))
                gradient.setColorAt(1,
                    QtGui.QColor(self._theme.background_endColor))
                painter.setBrush(QtGui.QBrush(gradient))
                rectPath = QtGui.QPainterPath()
                max_x = self._frame.width()
                max_y = self._frame.height()
                rectPath.moveTo(0, 0)
                rectPath.lineTo(0, max_y)
                rectPath.lineTo(max_x, max_y)
                rectPath.lineTo(max_x, 0)
                rectPath.closeSubpath()
                painter.drawPath(rectPath)
            elif self._theme.background_type == u'image':
                # image
                painter.fillRect(self._frame.rect(), QtCore.Qt.black)
                if self.bg_image:
                    painter.drawImage(0, 0, self.bg_image)
        painter.end()
        log.debug(u'render background End')

    def _correctAlignment(self, rect, bbox):
        """
        Corrects the vertical alignment of text.

        ``rect``
            The block dimentions.

        ``bbox``
            Footer dimensions?
        """
        x = rect.left()
        if self._theme.display_verticalAlign == 0:
            # top align
            y = rect.top()
        elif self._theme.display_verticalAlign == 2:
            # bottom align
            y = rect.bottom() - bbox.height()
        elif self._theme.display_verticalAlign == 1:
            # centre align
            y = rect.top() + (rect.height() - bbox.height()) / 2
        else:
            log.error(u'Invalid value for theme.VerticalAlign:%s',
                self._theme.display_verticalAlign)
        return x, y

    def _render_lines_unaligned(self, lines, footer, tlcorner=(0, 0),
        live=False):
        """
        Given a list of lines to render, render each one in turn (using the
        ``_render_single_line`` fn - which may result in going off the bottom).
        They are expected to be pre-arranged to less than a screenful (eg. by
        using split_set_of_lines).

        Returns the bounding box of the text as QRect.

        ``lines``
            The lines of text to render.

        ``footer``
            The slide footer.

        ``tlcorner``
            Defaults to *``(0, 0)``*. Co-ordinates of the top left corner.

        ``live``
            Defaults to *False*. Whether or not this is a live screen.
        """
        x, y = tlcorner
        brx = x
        bry = y
        for line in lines:
            # render after current bottom, but at original left edge
            # keep track of right edge to see which is biggest
            (thisx, bry) = self._render_and_wrap_single_line(line, footer,
                (x, bry), live)
            if (thisx > brx):
                brx = thisx
        retval = QtCore.QRect(x, y, brx - x, bry - y)
        if self._debug:
            painter = QtGui.QPainter()
            painter.begin(self._frame)
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 255)))
            painter.drawRect(retval)
            painter.end()
        return retval

    def _render_and_wrap_single_line(self, line, footer, tlcorner=(0, 0),
        live=False):
        """
        Render a single line of words onto the DC, top left corner specified.
        If the line is too wide for the context, it wraps, but right-aligns
        the surplus words in the manner of song lyrics.

        Returns the bottom-right corner (of what was rendered) as a tuple(x, y).

        ``line``
            Line of text to be rendered.

        ``footer``
            The footer of the slide.

        ``tlcorner``
            Defaults to *``(0, 0)``*. The top left corner.

        ``live``
            Defaults to *False*. Whether or not this is a live screen.
        """
        x, y = tlcorner
        maxx = self._rect.width();
        maxy = self._rect.height();
        lines = []
        lines.append(line)
        startx = x
        starty = y
        rightextent = None
        self.painter = QtGui.QPainter()
        self.painter.begin(self._frame)
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing);
        if self._theme.display_slideTransition:
            self.painter2 = QtGui.QPainter()
            self.painter2.begin(self._frameOp)
            self.painter2.setRenderHint(QtGui.QPainter.Antialiasing);
            self.painter2.setOpacity(0.7)
        # dont allow alignment messing with footers
        if footer:
            align = 0
            display_shadow_size = self._display_shadow_size_footer
            display_outline_size = self._display_outline_size_footer
        else:
            align = self._theme.display_horizontalAlign
            display_shadow_size = int(self._theme.display_shadow_size)
            display_outline_size = int(self._theme.display_outline_size)
        for linenum in range(len(lines)):
            line = lines[linenum]
            #find out how wide line is
            w, h = self._get_extent_and_render(line, footer, tlcorner=(x, y),
                draw=False)
            if self._theme.display_shadow:
                w += display_shadow_size
                h += display_shadow_size
            if self._theme.display_outline:
                # pixels either side
                w += 2 * display_outline_size
                #  pixels top/bottom
                h += 2 * display_outline_size
            if align == 0: # left align
                rightextent = x + w
                # shift right from last line's rh edge
                if self._theme.display_wrapStyle == 1 and linenum != 0:
                    rightextent = self._first_line_right_extent + \
                        self._right_margin
                    if rightextent > maxx:
                        rightextent = maxx
                    x = rightextent - w
            # right align
            elif align == 1:
                rightextent = maxx
                x = maxx - w
            # centre
            elif align == 2:
                x = (maxx - w) / 2;
                rightextent = x + w
            if live:
                # now draw the text, and any outlines/shadows
                if self._theme.display_shadow:
                    self._get_extent_and_render(line, footer,
                        tlcorner=(x + display_shadow_size, y + display_shadow_size),
                        draw=True, color = self._theme.display_shadow_color)
                if self._theme.display_outline:
                    self._get_extent_and_render(line, footer,
                        (x + display_outline_size, y), draw=True,
                        color = self._theme.display_outline_color)
                    self._get_extent_and_render(line, footer,
                        (x, y + display_outline_size), draw=True,
                        color = self._theme.display_outline_color)
                    self._get_extent_and_render(line, footer,
                        (x, y - display_outline_size), draw=True,
                        color = self._theme.display_outline_color)
                    self._get_extent_and_render(line, footer,
                        (x - display_outline_size, y), draw=True,
                        color = self._theme.display_outline_color)
                    if display_outline_size > 1:
                        self._get_extent_and_render(line, footer,
                            (x + display_outline_size, y + display_outline_size),
                            draw=True,
                            color = self._theme.display_outline_color)
                        self._get_extent_and_render(line, footer,
                            (x - display_outline_size, y + display_outline_size),
                            draw=True,
                            color = self._theme.display_outline_color)
                        self._get_extent_and_render(line, footer,
                            (x + display_outline_size, y - display_outline_size),
                            draw=True,
                            color = self._theme.display_outline_color)
                        self._get_extent_and_render(line, footer,
                            (x - display_outline_size, y - display_outline_size),
                            draw=True,
                            color = self._theme.display_outline_color)
                self._get_extent_and_render(line, footer,tlcorner=(x, y),
                    draw=True)
            y += h
            if linenum == 0:
                self._first_line_right_extent = rightextent
        # draw a box around the text - debug only

        if self._debug:
            self.painter.setPen(QtGui.QPen(QtGui.QColor(0,255,0)))
            self.painter.drawRect(startx, starty, rightextent-startx, y-starty)
        brcorner = (rightextent, y)
        self.painter.end()
        if self._theme.display_slideTransition:
            self.painter2.end()
        return brcorner

    def _set_theme_font(self):
        """
        Set the fonts from the current theme settings.
        """
        footer_weight = 50
        if self._theme.font_footer_weight == u'Bold':
            footer_weight = 75
        #TODO Add  myfont.setPixelSize((screen_height / 100) * font_size)
        self.footerFont = QtGui.QFont(self._theme.font_footer_name,
                     self._theme.font_footer_proportion, # size
                     footer_weight, # weight
                     self._theme.font_footer_italics) # italic
        self.footerFont.setPixelSize(self._theme.font_footer_proportion)
        main_weight = 50
        if self._theme.font_main_weight == u'Bold':
            main_weight = 75
        self.mainFont = QtGui.QFont(self._theme.font_main_name,
                     self._theme.font_main_proportion, # size
                     main_weight, # weight
                     self._theme.font_main_italics)# italic
        self.mainFont.setPixelSize(self._theme.font_main_proportion)

    def _get_extent_and_render(self, line, footer, tlcorner=(0, 0), draw=False,
        color=None):
        """
        Find bounding box of text - as render_single_line. If draw is set,
        actually draw the text to the current DC as well return width and
        height of text as a tuple (w, h).

        ``line``
            The line of text to render.

        ``footer``
            The footer text.

        ``tlcorner``
            Defaults to *``(0, 0)``*. The top left corner co-ordinates.

        ``draw``
            Defaults to *False*. Draw the text to the current surface.

        ``color``
            Defaults to *None*. The colour to draw with.
        """
        # setup defaults
        if footer :
            font = self.footerFont
        else:
            font = self.mainFont
        self.painter.setFont(font)
        if color is None:
            if footer:
                self.painter.setPen(QtGui.QColor(self._theme.font_footer_color))
            else:
                self.painter.setPen(QtGui.QColor(self._theme.font_main_color))
        else:
            self.painter.setPen(QtGui.QColor(color))
        x, y = tlcorner
        metrics = QtGui.QFontMetrics(font)
        w = metrics.width(line)
        h = metrics.height()
        if draw:
            self.painter.drawText(x, y + metrics.ascent(), line)
        if self._theme.display_slideTransition:
            # Print 2nd image with 70% weight
            self.painter2.setFont(font)
            if color is None:
                if footer:
                    self.painter2.setPen(QtGui.QColor(self._theme.font_footer_color))
                else:
                    self.painter2.setPen(QtGui.QColor(self._theme.font_main_color))
            else:
                self.painter2.setPen(QtGui.QColor(color))
            if draw:
                self.painter2.drawText(x, y + metrics.ascent(), line)
        return (w, h)

    def snoop_Image(self, image, image2=None):
        """
        Debugging method to allow images to be viewed.

        ``image``
            An image to save to disk.

        ``image2``
            Defaults to *None*. Another image to save to disk.
        """
        image.save(u'renderer.png', u'png')
        if image2:
            image2.save(u'renderer2.png', u'png')
