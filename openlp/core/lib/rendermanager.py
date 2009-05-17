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

from datetime import *
from PyQt4 import QtGui, QtCore, Qt
from renderer import  Renderer

import sys
import linecache

def traceit(frame, event, arg):
    """
    Code to allow calls to be traced by python runtime
    """
    if event == "line":
        lineno = frame.f_lineno
        filename = frame.f_globals["__file__"]
        if (filename.endswith(".pyc") or
            filename.endswith(".pyo")):
            filename = filename[:-1]
        name = frame.f_globals["__name__"]
        line = linecache.getline(filename, lineno)
        if name.startswith("openlp"):
            print "%s:%s: %s" % (name, lineno, line.rstrip())
    return traceit



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
        self.current_display = 0
        self.renderer = Renderer()
        self.calculate_default(self.screen_list[self.current_display]['size'])

    def set_override_theme(self, theme):
        log.debug(u'set override theme to %s',  theme)
        if theme is not None:
            self.theme = theme
        else:
            self.theme = self.default_theme
        if self.theme != self.renderer.theme_name:
            log.debug(u'theme is now %s',  self.theme)
            self.themedata = self.theme_manager.getThemeData(self.theme)
            self.calculate_default(self.screen_list[self.current_display]['size'])
            self.renderer.set_theme(self.themedata)
            self.build_text_rectangle(self.themedata)

    def build_text_rectangle(self, theme):
        log.debug(u'build_text_rectangle ')
        main_rect = None
        footer_rect = None

        if theme.font_main_override == False:
            main_rect = QtCore.QRect(10,0, self.width-1, self.height-1)
        else:
            main_rect = QtCore.QRect(int(theme.font_main_x) , int(theme.font_main_y),
                int(theme.font_main_width)-1, int(theme.font_main_height)-1)

        if theme.font_footer_override == False:
            footer_rect = QtCore.QRect(10,self.footer_start, self.width-1, self.height-self.footer_start)
        else:
            footer_rect = QtCore.QRect(int(theme.font_footer_x),int(theme.font_footer_y),
                int(theme.font_footer_width)-1, int(theme.font_footer_height)-1)

        self.renderer.set_text_rectangle(main_rect,footer_rect)

    def generate_preview(self, themedata):
        log.debug(u'generate preview')
        self.calculate_default(QtCore.QSize(800, 600))
        self.renderer.set_theme(themedata)
        self.build_text_rectangle(themedata)

        self.renderer.set_frame_dest(self.width, self.height, True)

        lines = []
        lines.append(u'Amazing Grace!')
        lines.append(u'How sweet the sound')
        lines.append(u'To save a wretch like me;')
        lines.append(u'I once was lost but now am found,')
        lines.append(u'Was blind, but now I see.')
        lines1 = []
        lines1.append(u'Amazing Grace (John Newton)' )
        lines1.append(u'Public Domain')
        lines1.append(u'CCLI xxx')
        return self.renderer.render_lines(lines, lines1)


    def format_slide(self, words, footer):
        log.debug(u'format slide')
        self.calculate_default(self.screen_list[self.current_display]['size'])
        self.build_text_rectangle(self.themedata)
        self.renderer.set_frame_dest(self.width, self.height)
        return self.renderer.format_slide(words, False)

    def generate_slide(self,main_text, footer_text):
        log.debug(u'generate slide')
        self.calculate_default(self.screen_list[self.current_display]['size'])
        self.build_text_rectangle(self.themedata)
        self.renderer.set_frame_dest(self.width, self.height)
        return self.renderer.render_lines(main_text, footer_text)

    def calculate_default(self, screen):
        log.debug(u'calculate default %s' , screen)
        self.width = screen.width()
        self.height = screen.height()
        log.debug(u'calculate default %d,%d' , self.width, self.height)
        self.footer_start = int(self.height*0.90) # 90% is start of footer

    def snoop_Image(self, image, image2=None):
        """
        Debugging method to allow images to be viewed
        """
        im = image.toImage()
        im.save("renderer.png", "png")
        if image2 is not None:
            im = image2.toImage()
            im.save("renderer2.png", "png")
