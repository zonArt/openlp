# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import logging
import os,  os.path
import sys

from datetime import *
from PyQt4 import QtGui, QtCore, Qt

from copy import copy

class Renderer:

    global log
    log = logging.getLogger(u'Renderer')
    log.info(u'Renderer Loaded')
    """All the functions for rendering a set of words onto a Device Context

    How to use:
    set the words to be displayed with a call to format_slide() - this returns an array of screenfuls of data
    set a theme (if you need) with set_theme
    tell it which DC to render to with set_DC()
    set the borders of where you want the text (if not the whole DC) with set_text_rectangle()
    tell it to render a particular screenfull with render_screen(n)

    """
    def __init__(self):
        self._rect = None
        self._debug = 0
        #self.words = None
        self._right_margin = 64 # the amount of right indent
        self._shadow_offset = 5
        self._outline_offset = 2
        self.theme_name = None
        self._theme = None
        self._bg_image_filename = None
        self._frame = None
        self._bg_frame = None
        self.bg_image = None

    def set_debug(self, debug):
        self._debug=debug

    def set_theme(self, theme):
        """
        External API to pass in the theme to be used
        """
        log.debug(u'set theme')
        self._theme = theme
        self._bg_frame = None
        self.theme_name = theme.theme_name
        if theme.background_type == u'image':
            if theme.background_filename is not None:
                self.set_bg_image(theme.background_filename)

    def set_bg_image(self, filename):
        log.debug(u'set bg image %s', filename)
        self._bg_image_filename = str(filename)
        if self._frame is not None:
            self.scale_bg_image()

    def scale_bg_image(self):
        assert self._frame
        preview = QtGui.QPixmap(self._bg_image_filename)
        width = self._frame.width()
        height = self._frame.height()
        preview = preview.scaled(width, height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        realwidth = preview.width()
        realheight = preview.height()
        # and move it to the centre of the preview space
        self.bg_image = QtGui.QPixmap(width, height)
        self.bg_image.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(self.bg_image)
        self.background_offsetx = (width - realwidth) / 2
        self.background_offsety = (height - realheight) / 2
        painter.drawPixmap(self.background_offsetx, self.background_offsety , preview)

    def set_frame_dest(self, frame_width, frame_height, preview=False):
        """
        External API to pass the frame size to be painted
        """
        if preview == True:
            self._bg_frame = None
        log.debug(u'set frame dest (frame) w %d h %d',frame_width, frame_height)
        self._frame = QtGui.QPixmap(frame_width, frame_height)
        if self._bg_image_filename is not None:
            self.scale_bg_image()
        if self._bg_frame is None:
            self._generate_background_frame()

    def format_slide(self, words, footer):
        """
        External API to sort out the text to pe placed on the frame
        """
        print "########## Format Slide ##################"
        log.debug(u'format_slide %s', words)
        verses = []
        words = words.replace("\r\n", "\n")
        verses_text = words.split(u'\n\n')
        text = []
        for verse in verses_text:
            lines = verse.split(u'\n')
            for line in lines:
                text.append(line)

        print self._split_set_of_lines(text, False)
        print "text ", text
        return text

#    def render_screen(self, screennum):
#        log.debug(u'render screen\n %s %s ', screennum, self.words[screennum])
#        t = 0.0
#        words = self.words[screennum]
#        retval = self._render_lines(words)
#        return retval

    def set_text_rectangle(self, rect_main, rect_footer):
        """ Sets the rectangle within which text should be rendered"""
        self._rect = rect_main
        self._rect_footer = rect_footer

    def generate_frame_from_lines(self, lines, footer_lines=None):
        """
        Render a set of lines according to the theme, return bounding box
         """
        print "########## Generate frame from lines ##################"
        log.debug(u'generate_frame_from_lines - Start')

        print "Render Lines ", lines

        bbox = self._render_lines_unaligned(lines, False)
        if footer_lines is not None:
            bbox1 = self._render_lines_unaligned(footer_lines, True)

        # reset the frame. first time do not worrk about what you paint on.
        self._frame = QtGui.QPixmap(self._bg_frame)

        x, y = self._correctAlignment(self._rect, bbox)
        bbox = self._render_lines_unaligned(lines, False,  (x, y))

        if footer_lines is not None:
            bbox = self._render_lines_unaligned(footer_lines, True, (self._rect_footer.left(), self._rect_footer.top()) )
        log.debug(u'generate_frame_from_lines - Finish')

        return self._frame

    def _generate_background_frame(self):
        """
        Generate a background frame to the same size as the frame to be used
        Results cached for performance reasons.
        """
        assert(self._theme)
        self._bg_frame = QtGui.QPixmap(self._frame.width(), self._frame.height())
        log.debug(u'render background %s ', self._theme.background_type)
        bef = datetime.now()
        painter = QtGui.QPainter()
        painter.begin(self._bg_frame)
        if self._theme.background_type == u'solid':
            painter.fillRect(self._frame.rect(), QtGui.QColor(self._theme.background_color))
        elif self._theme.background_type == u'gradient' : # gradient
            gradient = None
            if self._theme.background_direction == u'horizontal':
                w = int(self._frame.width()) / 2
                gradient = QtGui.QLinearGradient(w, 0, w, self._frame.height()) # vertical
            elif self._theme.background_direction == u'vertical':
                h = int(self._frame.height()) / 2
                gradient = QtGui.QLinearGradient(0, h, self._frame.width(), h)   # Horizontal
            else:
                w = int(self._frame.width()) / 2
                h = int(self._frame.height()) / 2
                gradient = QtGui.QRadialGradient(w, h, w) # Circular

            gradient.setColorAt(0, QtGui.QColor(self._theme.background_startColor))
            gradient.setColorAt(1, QtGui.QColor(self._theme.background_endColor))

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

        elif self._theme.background_type== u'image': # image
            if self.bg_image is not None:
                painter.drawPixmap(0 ,0 , self.bg_image)
            else:
                painter.fillRect(self._frame.rect(), QtGui.QColor(u'#000000'))
        painter.end()
        aft = datetime.now()
        print "background time", bef, aft, aft-bef
        log.debug(u'render background finish')

    def _split_set_of_lines(self, lines, footer):
        """
        Given a list of lines, decide how to split them best if they don't all fit on the screen
         - this is done by splitting at 1/2, 1/3 or 1/4 of the set
         If it doesn't fit, even at this size, just split at each opportunity

         We'll do this by getting the bounding box of each line, and then summing them appropriately
         Returns a list of [lists of lines], one set for each screenful
         """


         ############  THIS IS WRONG SO FIX IT


        log.debug(u'Split set of lines')
        bboxes = []
        print "Lines ", lines
        for line in lines:
            bboxes.append(self._render_and_wrap_single_line(line, footer))
            #print line,  bboxes

        numlines = len(lines)
        bottom = self._rect.bottom()
        #for ratio in (numlines): #, numlines/2, numlines/3, numlines/4):
        ratio = numlines
        good = 1
        startline = 0
        endline = startline + ratio
        #print "A ",  numlines ,  startline,  endline
        #print "B ", bboxes
        while (endline <= numlines):
            by = 0
            for (x, y) in bboxes[startline:endline]:
                by += y
                #print by
            #print by , bottom
            if by > bottom:
                good=0
                break
            startline += ratio
            endline = startline+ratio
#        if good == 1:
#            break
       # print "---------"

        retval = []
        numlines_per_page = ratio
        if good:
            c = 0
            thislines = []
            while c < numlines:
                thislines.append(lines[c])
                c += 1
                if len(thislines) == numlines_per_page:
                    retval.append(thislines)
                    thislines = []
        else:
#             log.debug(u" "Just split where you can"
            retval = []
            startline = 0
            endline = startline+1
            while (endline <= numlines):
                by = 0
                for (x, y) in bboxes[startline:endline]:
                    by += y
                if by > bottom:
                    retval.append(lines[startline:endline-1])
                    startline = endline-1
                    endline = startline # gets incremented below
                    by = 0
                endline += 1
        print "retval ", retval
        return retval

    def _correctAlignment(self, rect, bbox):
        x = rect.left()
        if int(self._theme.display_verticalAlign) == 0: # top align
            y = rect.top()
        elif int(self._theme.display_verticalAlign) == 2: # bottom align
            y = rect.bottom() - bbox.height()
        elif int(self._theme.display_verticalAlign) == 1: # centre align
            y = rect.top() + (rect.height() - bbox.height()) / 2
        else:
            assert(0 , u'Invalid value for theme.VerticalAlign:%s' % self._theme.display_verticalAlign)
        return x, y

    def _render_lines_unaligned(self, lines,  footer,  tlcorner=(0,0)):
        """
        Given a list of lines to render, render each one in turn
        (using the _render_single_line fn - which may result in going
        off the bottom) They are expected to be pre-arranged to less
        than a screenful (eg. by using split_set_of_lines)

        Returns the bounding box of the text as QRect
        """
        log.debug(u'render lines unaligned Start')
        x, y = tlcorner
        brx = x
        bry = y
        print "A ", bry
        for line in lines:
            # render after current bottom, but at original left edge
            # keep track of right edge to see which is biggest
            (thisx, bry) = self._render_and_wrap_single_line(line, footer, (x , bry))
            if (thisx > brx):
                brx = thisx
            print "B ", bry
        retval = QtCore.QRect(x, y,brx-x, bry-y)
        if self._debug:
            painter = QtGui.QPainter()
            painter.begin(self._frame)
            painter.setPen(QtGui.QPen(QtGui.QColor(0,0,255)))
            painter.drawRect(retval)
            painter.end()
        log.debug(u'render lines unaligned Finish')
        return  retval

    def _render_and_wrap_single_line(self, line, footer, tlcorner=(0,0)):
        """
        Render a single line of words onto the DC, top left corner
        specified.

        If the line is too wide for the context, it wraps, but
        right-aligns the surplus words in the manner of song lyrics

        Returns the bottom-right corner (of what was rendered) as a tuple(x, y).
        """
        log.debug(u'Render single line %s @ %s '%( line, tlcorner))
        x, y = tlcorner
        # We draw the text to see how big it is and then iterate to make it fit
        # when we line wrap we do in in the "lyrics" style, so the second line is
        # right aligned with a "hanging indent"
        words = line.split(u' ')
        thisline = u' '.join(words)
        lastword = len(words)
        lines = []
        maxx = self._rect.width();
        maxy = self._rect.height();
        while (len(words) > 0):
            w , h = self._get_extent_and_render(thisline, footer)
            rhs = w + x
            if rhs < maxx - self._right_margin:
                lines.append(thisline)
                words = words[lastword:]
                thisline = ' '.join(words)
                lastword = len(words)
            else:
                lastword -= 1
                thisline = ' '.join(words[:lastword])
        startx = x
        starty = y
        rightextent = None
        if footer: # dont allow alignment messing with footers
            align = 0
        else:
            align = int(self._theme .display_horizontalAlign)

        print "wrap ", lines

        for linenum in range(len(lines)):
            line = lines[linenum]
            #find out how wide line is
            w , h = self._get_extent_and_render(line, footer,  tlcorner=(x, y), draw=False)
            if self._theme.display_shadow:
                w += self._shadow_offset
                h += self._shadow_offset
            if self._theme.display_outline:
                w += 2*self._outline_offset # pixels either side
                h += 2*self._outline_offset #  pixels top/bottom
            if align == 0: # left align
                rightextent = x + w
                if self._theme.display_wrapStyle == 1 and linenum != 0: # shift right from last line's rh edge
                    rightextent = self._first_line_right_extent + self._right_margin
                    if rightextent > maxx:
                        rightextent = maxx
                    x = rightextent - w
            elif align == 1: # right align
                rightextent = maxx
                x = maxx - w
            elif align == 2: # centre
                x = (maxx - w) / 2;
                rightextent = x + w
            # now draw the text, and any outlines/shadows
            if self._theme.display_shadow:
                self._get_extent_and_render(line, footer,tlcorner=(x+self._shadow_offset,y+self._shadow_offset),
                    draw=True, color = self._theme.display_shadow_color)
            if self._theme.display_outline:
                self._get_extent_and_render(line, footer,(x+self._outline_offset,y), draw=True,
                        color = self._theme.display_outline_color)
                self._get_extent_and_render(line, footer,(x, y+self._outline_offset), draw=True,
                        color = self._theme.display_outline_color)
                self._get_extent_and_render(line, footer,(x, y-self._outline_offset), draw=True,
                        color = self._theme.display_outline_color)
                self._get_extent_and_render(line, footer,(x-self._outline_offset,y), draw=True,
                        color = self._theme.display_outline_color)
                if self._outline_offset > 1:
                    self._get_extent_and_render(line, footer,(x+self._outline_offset,y+self._outline_offset), draw=True,
                        color = self._theme.display_outline_color)
                    self._get_extent_and_render(line, footer,(x-self._outline_offset,y+self._outline_offset), draw=True,
                        color = self._theme.display_outline_color)
                    self._get_extent_and_render(line, footer,(x+self._outline_offset,y-self._outline_offset), draw=True,
                        color = self._theme.display_outline_color)
                    self._get_extent_and_render(line, footer,(x-self._outline_offset,y-self._outline_offset), draw=True,
                        color = self._theme.display_outline_color)

            self._get_extent_and_render(line, footer,tlcorner=(x, y), draw=True)
            y += h
            if linenum == 0:
                self._first_line_right_extent = rightextent
        # draw a box around the text - debug only
        if self._debug:
            painter = QtGui.QPainter()
            painter.begin(self._frame)
            painter.setPen(QtGui.QPen(QtGui.QColor(0,255,0)))
            painter.drawRect(startx , starty , rightextent-startx , y-starty)
            painter.end()

        brcorner = (rightextent , y)
        log.debug(u'Render single line Finish')
        return brcorner

    # xxx this is what to override for an SDL version
    def _get_extent_and_render(self, line, footer,  tlcorner=(0,0), draw=False, color=None):
        """
        Find bounding box of text  - as render_single_line.
        If draw is set, actually draw the text to the current DC as well
        return width and height of text as a tuple (w,h)
        """
        # setup defaults
        #log.debug(u'_get_extent_and_render %s %s %s ', [line], tlcorner, draw)
        painter = QtGui.QPainter()
        painter.begin(self._frame)
        # 'twould be more efficient to set this once when theme changes
        # or p changes
        if footer :
            font = QtGui.QFont(self._theme.font_footer_name,
                         int(self._theme.font_footer_proportion), # size
                         QtGui.QFont.Normal, # weight
                         0)# italic
            font.setPixelSize(int(self._theme.font_footer_proportion))
        else:
            font = QtGui.QFont(self._theme.font_main_name,
                         int(self._theme.font_main_proportion), # size
                         QtGui.QFont.Normal, # weight
                         0)# italic
            font.setPixelSize(int(self._theme.font_main_proportion))
        painter.setFont(font)
        if color == None:
            if footer:
                painter.setPen(QtGui.QColor(self._theme.font_footer_color))
            else:
                painter.setPen(QtGui.QColor(self._theme.font_main_color))
        else:
            painter.setPen(QtGui.QColor(color))
        x, y = tlcorner
        metrics=QtGui.QFontMetrics(font)
        # xxx some fudges to make it exactly like wx!  Take 'em out later
        w = metrics.width(line)
        h = metrics.height() - 2
        if draw:
            painter.drawText(x, y + metrics.ascent() , line)
        painter.end()
        return (w, h)

    def snoop_Image(self, image, image2=None):
        """
        Debugging method to allow images to be viewed
        """
        im = image.toImage()
        im.save("renderer.png", "png")
        if image2 is not None:
            im = image2.toImage()
            im.save("renderer2.png", "png")
