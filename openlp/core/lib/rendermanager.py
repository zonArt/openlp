# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 - 2009Martin Thompson, Tim Bentley

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
from PyQt4 import QtGui, QtCore, Qt
from renderer import  Renderer

class RenderManager:
    """
    Class to pull all Renderer interactions into one place.
    The plugins will call helper methods to do the rendering but
    this class will provide display defense code.
    """
    global log
    log=logging.getLogger(u'RenderManager')
    log.info(u'RenderManager Loaded')

    def __init__(self, theme_manager, screen_list):
        log.debug(u'Initilisation started')
        self.screen_list = screen_list
        self.theme_manager = theme_manager
        self.displays = len(screen_list)
        self.current_display = 1
        self.renderer = Renderer(None)
        self.calculate_default(self.screen_list[self.current_display-1][1])
        self.frame = None

    def set_default_theme(self, theme):
        log.debug("default theme set to %s",  theme)
        self.default_theme = self.theme_manager.getThemeData(theme)
        self.renderer.set_theme(self.default_theme)

        self.renderer.set_text_rectangle(QtCore.QRect(10,0, self.width-1, self.height-1),
            QtCore.QRect(10,self.footer_start, self.width-1, self.height-self.footer_start))


    def set_theme(self, theme):
        log.debug("theme set to %s",  theme)
        self.theme = theme
        self.renderer.set_theme(self.theme)

        self.renderer.set_text_rectangle(QtCore.QRect(10,0, self.width-1, self.height-1),
            QtCore.QRect(10,self.footer_start, self.width-1, self.height-self.footer_start))
        if theme.font_main_override == False:
            pass
        if theme.font_footer_override == False:
            pass

    def generate_preview(self):
        self.calculate_default(QtCore.QSize(800,600))

        self.renderer.set_text_rectangle(QtCore.QRect(10,0, self.width-1, self.height-1),
            QtCore.QRect(10,self.footer_start, self.width-1, self.height-self.footer_start))

        frame = QtGui.QPixmap(self.width, self.height)
        self.renderer.set_paint_dest(frame)

        lines=[]
        lines.append(u'Amazing Grace!')
        lines.append(u'How sweet the sound')
        lines.append(u'To save a wretch like me;')
        lines.append(u'I once was lost but now am found,')
        lines.append(u'Was blind, but now I see.')
        lines1=[]
        lines1.append(u'Amazing Grace (John Newton)' )
        lines1.append(u'CCLI xxx (c)Openlp.org')
        answer=self.renderer.render_lines(lines, lines1)
        return frame

    def format_slide(self, words, footer):
        self.calculate_default(QtCore.QSize(800,600))

        self.renderer.set_text_rectangle(QtCore.QRect(10,0, self.width-1, self.height-1),
            QtCore.QRect(10,self.footer_start, self.width-1, self.height-self.footer_start))

        return self.renderer.format_slide(words, footer)

    def generate_slide(self,main_text, footer_text, preview=True):
        if preview == True:
            self.calculate_default(QtCore.QSize(800,600))

        self.renderer.set_text_rectangle(QtCore.QRect(10,0, self.width-1, self.height-1),
            QtCore.QRect(10,self.footer_start, self.width-1, self.height-self.footer_start))

        #frame = QtGui.QPixmap(self.width, self.height)
        #self.renderer.set_paint_dest(frame)
        #print main_text
        answer=self.renderer.render_lines(main_text, footer_text)
        return self.frame

    def calculate_default(self, screen):
        self.width = screen.width()
        self.height = screen.height()
        self.footer_start = int(self.height*0.95) # 95% is start of footer
        #update the rederer frame
        self.frame = QtGui.QPixmap(self.width, self.height)
        self.renderer.set_paint_dest(self.frame)
