# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

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

import sys
from PyQt4 import QtGui, QtCore, Qt

from copy import copy
from interpolate import interpolate

class Renderer:

    global log
    log=logging.getLogger(u'Renderer')
    log.info(u'Renderer Loaded')
    """All the functions for rendering a set of words onto a Device Context

    How to use:
    set the words to be displayed with a call to set_words_openlp() - this returns an array of screenfuls of data
    set a theme (if you need) with set_theme
    tell it which DC to render to with set_DC()
    set the borders of where you want the text (if not the whole DC) with set_text_rectangle()
    tell it to render a particular screenfull with render_screen(n)

    """
    def __init__(self):
        self._rect=None
        self._debug=0
        self.words=None
        self._right_margin = 64 # the amount of right indent
        self._shadow_offset=5
        self._outline_offset=2
        self._theme=None
        self._bg_image_filename=None
        self._paint=None

    def set_debug(self, debug):
        self._debug=debug

    def set_theme(self, theme):
        self._theme=theme
        if theme.BackgroundType == 2:
            self.set_bg_image(theme.BackgroundParameter1)

    def set_bg_image(self, filename):
        log.debug(u"set bg image %s", filename)
        self._bg_image_filename=filename
        if self._paint is not None:
            self.scale_bg_image()

    def scale_bg_image(self):
        assert self._paint
        i=QtGui.QImage(self._bg_image_filename)
        # rescale and offset
        imw=i.width();imh=i.height()
        dcw=self._paint.width()+1;dch=self._paint.height()
        imratio=imw/float(imh)
        dcratio=dcw/float(dch)
        log.debug(u"Image scaling params %s %s %s %s %s %s", imw, imh, imratio, dcw, dch, dcratio)
        if imratio > dcratio:
            scale=dcw/float(imw)
        elif imratio < dcratio:
            scale=dch/float(imh)
        else:
            scale=dcw/float(imw) # either will do
        neww=int(round(imw*scale))
        newh=int(round(imh*scale))
        self.background_offsetx=(dcw-neww)/2
        self.background_offsety=(dch-newh)/2
        self.img=QtGui.QPixmap.fromImage(i.scaled(QtCore.QSize(neww, newh), Qt.Qt.KeepAspectRatio))

    def set_paint_dest(self, p):
        self._paint=p
        if self._bg_image_filename is not None:
            self.scale_bg_image()

    def set_words_openlp(self, words):
#         log.debug(u" "set words openlp", words
        verses=[]
        words=words.replace("\r\n", "\n")
        verses_text=words.split('\n\n')
        for v in verses_text:
            lines=v.split('\n')
            verses.append(self.split_set_of_lines(lines)[0])
        self.words=verses
        verses_text=[]
        for v in verses:
            verses_text.append('\n'.join(v).lstrip()) # remove first \n

        return verses_text

    def render_screen(self, screennum):
        log.debug(u"render screen\n %s %s ", screennum, self.words[screennum])
        import time
        t=0.0
        words=self.words[screennum]
        retval=self._render_lines(words)
        return retval

    def set_text_rectangle(self, rect):
        """ Sets the rectangle within which text should be rendered"""
        self._rect=rect

    def _render_background(self):
        assert(self._theme)
        assert(self._paint)
        log.debug(u"render background %s %s", self._theme.BackgroundType)
        p=QtGui.QPainter()
        p.begin(self._paint)
        if self._theme.BackgroundType == 0:
            p.fillRect(self._paint.rect(), self._theme.BackgroundParameter1)
        elif self._theme.BackgroundType == 1: # gradient
            #TODO Add Theme code and fix direction

            gradient = QtGui.QLinearGradient(0, 0, self._paint.width(), self._paint.height())
            gradient.setColorAt(0, QtGui.QColor(255, 0, 0))
            gradient.setColorAt(0.5, QtGui.QColor(0, 255, 0))
            gradient.setColorAt(1, QtGui.QColor(0, 0, 255))
            p.setBrush(QtGui.QBrush(gradient))
            rectPath = QtGui.QPainterPath()

            MAX_X = self._paint.width()
            MAX_Y = self._paint.height()

            rectPath.moveTo(0, 0)
            rectPath.lineTo(0, MAX_Y)
            rectPath.lineTo(MAX_X, MAX_Y)
            rectPath.lineTo(MAX_X, 0)
            rectPath.closeSubpath()
            p.drawPath(rectPath)

        elif self._theme.BackgroundType == 2: # image
            r=self._paint.rect()
            log.debug(r.x(), r.y(), r.width(),r.height())
            log.debug(self._theme.BackgroundParameter2)
            if self._theme.BackgroundParameter2 is not None:
                p.fillRect(self._paint.rect(), self._theme.BackgroundParameter2)
            p.drawPixmap(self.background_offsetx,self.background_offsety, self.img)
        p.end()
        log.debug(u"render background done")

    def split_set_of_lines(self, lines):

        """Given a list of lines, decide how to split them best if they don't all fit on the screen
         - this is done by splitting at 1/2, 1/3 or 1/4 of the set
         If it doesn't fit, even at this size, just split at each opportunity

         We'll do this by getting the bounding box of each line, and then summing them appropriately

         Returns a list of [lists of lines], one set for each screenful
         """
#         log.debug(u" "Split set of lines"
        # Probably ought to save the rendering results to a pseudoDC for redrawing efficiency.  But let's not optimse prematurely!

        bboxes = []
        for line in lines:
            bboxes.append(self._render_single_line(line))
        numlines=len(lines)
        bottom=self._rect.bottom()
        for ratio in (numlines, numlines/2, numlines/3, numlines/4):
            good=1
            startline=0
            endline=startline+ratio
            while (endline<=numlines):
                by=0
                for (x,y) in bboxes[startline:endline]:
                    by+=y
                if by > bottom:
                    good=0
                    break
                startline+=ratio
                endline=startline+ratio
            if good==1:
                break

        retval=[]
        numlines_per_page=ratio
        if good:
            c=0
            thislines=[]
            while c < numlines:
                thislines.append(lines[c])
                c+=1
                if len(thislines) == numlines_per_page:
                    retval.append(thislines)
                    thislines=[]
        else:
#             log.debug(u" "Just split where you can"
            retval=[]
            startline=0
            endline=startline+1
            while (endline<=numlines):
                by=0
                for (x,y) in bboxes[startline:endline]:
                    by+=y
                if by > bottom:
                    retval.append(lines[startline:endline-1])
                    startline=endline-1
                    endline=startline # gets incremented below
                    by=0
                endline+=1

        return retval

    def _render_lines(self, lines):
        """render a set of lines according to the theme, return bounding box"""
        log.debug(u"_render_lines %s", lines)

        bbox=self._render_lines_unaligned(lines)
        print bbox

        t=self._theme
        x=self._rect.left()
        if t.VerticalAlign==0: # top align
            y = self._rect.top()
        elif t.VerticalAlign==1: # bottom align
            y=self._rect.bottom()-bbox.height()
        elif t.VerticalAlign==2: # centre align
            y=self._rect.top()+(self._rect.height()-bbox.height())/2
        else:
            assert(0, "Invalid value for theme.VerticalAlign:%d" % t.VerticalAlign)
        self._render_background()
        bbox=self._render_lines_unaligned(lines, (x,y))
        log.debug(u"render lines DONE")

        return bbox

    def _render_lines_unaligned(self, lines, tlcorner=(0,0)):

        """Given a list of lines to render, render each one in turn
        (using the _render_single_line fn - which may result in going
        off the bottom) They are expected to be pre-arranged to less
        than a screenful (eg. by using split_set_of_lines)

        Returns the bounding box of the text as QRect"""
        log.debug(u"render unaligned %s", lines)
        x,y=tlcorner
        brx=x
        bry=y
        for line in lines:
            if (line == ''):
                continue
            # render after current bottom, but at original left edge
            # keep track of right edge to see which is biggest
            (thisx, bry) = self._render_single_line(line, (x,bry))
            if (thisx > brx):
                brx=thisx
        retval=QtCore.QRect(x,y,brx-x, bry-y)
        if self._debug:
            p=QtGui.QPainter()
            p.begin(self._paint)
            p.setPen(QtGui.QPen(QtGui.QColor(0,0,255)))
            p.drawRect(retval)
            p.end()
        log.debug(u"render unaligned DONE")

        return  retval

    def _render_single_line(self, line, tlcorner=(0,0)):

        """render a single line of words onto the DC, top left corner
        specified.

        If the line is too wide for the context, it wraps, but
        right-aligns the surplus words in the manner of song lyrics

        Returns the bottom-right corner (of what was rendered) as a tuple(x,y).
        """
        log.debug(u"Render single line '%s' @ %s "%( line, tlcorner))
        x,y=tlcorner
        # We draw the text to see how big it is and then iterate to make it fit
        # when we line wrap we do in in the "lyrics" style, so the second line is
        # right aligned with a "hanging indent"

        # get the words
#         log.debug(u" "Getting the words split right"
        words=line.split(" ")
        thisline=' '.join(words)
        lastword=len(words)
        lines=[]
        maxx=self._rect.width(); maxy=self._rect.height();
        while (len(words)>0):
            w,h=self._get_extent_and_render(thisline)
            rhs=w+x
            if rhs < maxx-self._right_margin:
                lines.append(thisline)
                words=words[lastword:]
                thisline=' '.join(words)
                lastword=len(words)
            else:
                lastword-=1
                thisline=' '.join(words[:lastword])

#         log.debug(u" "This is how they split", lines
#         log.debug(u" "Now render them"
        startx=x
        starty=y
        rightextent=None
        t=self._theme
        align=t.HorizontalAlign
        wrapstyle=t.WrapStyle

        for linenum in range(len(lines)):
            line=lines[linenum]
            #find out how wide line is
            w,h=self._get_extent_and_render(line, tlcorner=(x,y), dodraw=False)

            if t.Shadow:
                w+=self._shadow_offset
                h+=self._shadow_offset
            if t.Outline:
                w+=2*self._outline_offset # pixels either side
                h+=2*self._outline_offset #  pixels top/bottom
            if align==0: # left align
                rightextent=x+w
                if wrapstyle==1 and linenum != 0: # shift right from last line's rh edge
                    rightextent=self._first_line_right_extent + self._right_margin
                    if rightextent > maxx:
                        rightextent = maxx
                    x = rightextent-w

            elif align==1: # right align
                rightextent=maxx
                x=maxx-w
            elif align==2: # centre
                x=(maxx-w)/2;
                rightextent=x+w
            # now draw the text, and any outlines/shadows
            if t.Shadow:
                self._get_extent_and_render(line, tlcorner=(x+self._shadow_offset,y+self._shadow_offset), dodraw=True, color = t.ShadowColor)
            if t.Outline:
                self._get_extent_and_render(line, (x+self._outline_offset,y), dodraw=True, color = t.OutlineColor)
                self._get_extent_and_render(line, (x,y+self._outline_offset), dodraw=True, color = t.OutlineColor)
                self._get_extent_and_render(line, (x,y-self._outline_offset), dodraw=True, color = t.OutlineColor)
                self._get_extent_and_render(line, (x-self._outline_offset,y), dodraw=True, color = t.OutlineColor)
                if self._outline_offset > 1:
                    self._get_extent_and_render(line, (x+self._outline_offset,y+self._outline_offset), dodraw=True, color = t.OutlineColor)
                    self._get_extent_and_render(line, (x-self._outline_offset,y+self._outline_offset), dodraw=True, color = t.OutlineColor)
                    self._get_extent_and_render(line, (x+self._outline_offset,y-self._outline_offset), dodraw=True, color = t.OutlineColor)
                    self._get_extent_and_render(line, (x-self._outline_offset,y-self._outline_offset), dodraw=True, color = t.OutlineColor)

            self._get_extent_and_render(line, tlcorner=(x,y), dodraw=True)
#             log.debug(u" "Line %2d: Render '%s' at (%d, %d) wh=(%d,%d)"%( linenum, line, x, y,w,h)
            y += h
            if linenum == 0:
                self._first_line_right_extent=rightextent
        # draw a box around the text - debug only
        if self._debug:
            p=QtGui.QPainter()
            p.begin(self._paint)
            p.setPen(QtGui.QPen(QtGui.QColor(0,255,0)))
            p.drawRect(startx,starty,rightextent-startx,y-starty)
            p.end()

        brcorner=(rightextent,y)
        return brcorner

    # xxx this is what to override for an SDL version
    def _get_extent_and_render(self, line, tlcorner=(0,0), dodraw=False, color=None, footer = False):
        """Find bounding box of text  - as render_single_line.
        If dodraw is set, actually draw the text to the current DC as well

        return width and height of text as a tuple (w,h)"""
        # setup defaults
        log.debug(u"_get_extent_and_render %s %s %s ", [line], tlcorner, dodraw)
        p=QtGui.QPainter()
        p.begin(self._paint)
        # 'twould be more efficient to set this once when theme changes
        # or p changes
        if footer :
           font=QtGui.QFont(self._theme.FontName,
                         12, # size
                         QtGui.QFont.Normal, # weight
                         0)# italic
        else:
            font=QtGui.QFont(self._theme.FontName,
                         self._theme.FontProportion, # size
                         QtGui.QFont.Normal, # weight
                         0)# italic
        # to make the unit tests monitor independent, we have to be able to
        # specify whether a font proportion is in pixels or points
        if self._theme.FontUnits.lower() == "pixels":
            log.debug(u"pixels")
            if footer:
                font.setPixelSize(12)
            else:
                font.setPixelSize(self._theme.FontProportion)
        log.debug(u'Font details %s %s %s %s', self._theme.FontName, self._theme.FontProportion,  font.family(), font.pointSize())
        p.setFont(font)
        if color == None:
            p.setPen(self._theme.FontColor)
        else:
            p.setPen(color)
        x,y=tlcorner
        metrics=QtGui.QFontMetrics(font)
        # xxx some fudges to make it exactly like wx!  Take 'em out later
        w=metrics.width(line)
        h=metrics.height()-2
        if dodraw:
            p.drawText(x,y+metrics.height()-metrics.descent()-1, line)
        p.end()
        return (w, h)
