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

from renderer import Renderer
from openlp.core.lib import ThemeLevel

class RenderManager(object):
    """
    Class to pull all Renderer interactions into one place. The plugins will
    call helper methods to do the rendering but this class will provide
    display defense code.

    ``theme_manager``
        The ThemeManager instance, used to get the current theme details.

    ``screen_list``
        The list of screens available.

    ``screen_number``
        Defaults to *0*. The index of the output/display screen.
    """
    global log
    log = logging.getLogger(u'RenderManager')
    log.info(u'RenderManager Loaded')

    def __init__(self, theme_manager, screen_list, screen_number=0):
        """
        Initialise the render manager.
        """
        log.debug(u'Initilisation started')
        self.screen_list = screen_list
        self.theme_manager = theme_manager
        self.displays = len(screen_list)
        if (screen_number + 1) > len(screen_list):
            self.current_display = 0
        else:
            self.current_display = screen_number
        self.renderer = Renderer()
        self.calculate_default(self.screen_list[self.current_display][u'size'])
        self.theme = u''
        self.service_theme = u''
        self.theme_level = u''
        self.override_background = None
        self.themedata = None
        self.save_bg_frame = None
        self.override_background_changed = False

    def update_display(self, screen_number):
        """
        Updates the render manager's information about the current screen.

        ``screen_number``
            The updated index of the output/display screen.
        """
        log.debug(u'Update Display')
        if self.current_display != screen_number:
            self.current_display = screen_number
            self.calculate_default(
                self.screen_list[self.current_display][u'size'])

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

    def set_service_theme(self, service_theme):
        """
        Set the service-level theme.

        ``service_theme``
            The service-level theme to be set.
        """
        self.service_theme = service_theme

    def set_override_theme(self, theme):
        """
        Set the appropriate theme depending on the theme level.

        ``theme``
            The name of the song-level theme.
        """
        log.debug(u'set override theme to %s', theme)
        if self.theme_level == ThemeLevel.Global:
            self.theme = self.global_theme
        elif self.theme_level == ThemeLevel.Service:
            if self.service_theme == u'':
                self.theme = self.global_theme
            else:
                self.theme = self.service_theme
        else:
            if theme:
                self.theme = theme
            elif self.theme_level == ThemeLevel.Song or \
                self.theme_level == ThemeLevel.Service:
                if self.service_theme == u'':
                    self.theme = self.global_theme
                else:
                    self.theme = self.service_theme
            else:
                self.theme = self.global_theme
        if self.theme != self.renderer.theme_name or self.themedata is None:
            log.debug(u'theme is now %s', self.theme)
            self.themedata = self.theme_manager.getThemeData(self.theme)
            self.calculate_default(
                self.screen_list[self.current_display][u'size'])
            self.renderer.set_theme(self.themedata)
            self.build_text_rectangle(self.themedata)
        #Replace the backgrount image from renderer with one from image
        if self.override_background:
            if self.save_bg_frame is None:
                self.save_bg_frame = self.renderer.bg_frame
            if self.override_background_changed:
                self.renderer.bg_frame = self.resize_image(
                    self.override_background)
                self.override_background_changed = False
        else:
            if self.override_background_changed:
                self.renderer.bg_frame = self.resize_image(
                    self.override_background)
                self.override_background_changed = False
            if self.save_bg_frame:
                self.renderer.bg_frame = self.save_bg_frame
                self.save_bg_frame = None

    def build_text_rectangle(self, theme):
        """
        Builds a text block using the settings in ``theme``.
        One is needed per slide

        ``theme``
            The theme to build a text block for.
        """
        log.debug(u'build_text_rectangle')
        main_rect = None
        footer_rect = None
        if not theme.font_main_override:
            main_rect = QtCore.QRect(10, 0, self.width - 1,
                self.footer_start - 20)
        else:
            main_rect = QtCore.QRect(theme.font_main_x, theme.font_main_y,
                theme.font_main_width - 1, theme.font_main_height - 1)
        if not theme.font_footer_override:
            footer_rect = QtCore.QRect(10, self.footer_start, self.width - 1,
                self.height-self.footer_start)
        else:
            footer_rect = QtCore.QRect(theme.font_footer_x,
                theme.font_footer_y, theme.font_footer_width - 1,
                theme.font_footer_height - 1)
        self.renderer.set_text_rectangle(main_rect, footer_rect)

    def generate_preview(self, themedata):
        """
        Generate a preview of a theme.

        ``themedata``
            The theme to generated a preview for.
        """
        log.debug(u'generate preview')
        self.calculate_default(QtCore.QSize(1024, 768))
        self.renderer.set_theme(themedata)
        self.build_text_rectangle(themedata)
        self.renderer.set_frame_dest(self.width, self.height, True)
        verse = u'Amazing Grace!\n'\
        'How sweet the sound\n'\
        'To save a wretch like me;\n'\
        'I once was lost but now am found,\n'\
        'Was blind, but now I see.'
        footer = []
        footer.append(u'Amazing Grace (John Newton)' )
        footer.append(u'Public Domain')
        footer.append(u'CCLI 123456')
        formatted = self.renderer.format_slide(verse, False)
        return self.renderer.generate_frame_from_lines(formatted[0], footer)[u'main']

    def format_slide(self, words):
        """
        Calculate how much text can fit on a slide.

        ``words``
            The words to go on the slides.
        """
        log.debug(u'format slide')
        self.build_text_rectangle(self.themedata)
        return self.renderer.format_slide(words, False)

    def generate_slide(self, main_text, footer_text):
        """
        Generate the actual slide image.

        ``main_text``
            The text for the main area of the slide.

        ``footer_text``
            The text for the slide footer.
        """
        log.debug(u'generate slide')
        self.build_text_rectangle(self.themedata)
        self.renderer.set_frame_dest(self.width, self.height)
        return self.renderer.generate_frame_from_lines(main_text, footer_text)

    def resize_image(self, image, width=0, height=0):
        """
        Resize an image to fit on the current screen.

        ``image``
            The image to resize.
        """
        preview = QtGui.QImage(image)
        if width == 0:
            w = self.width
            h = self.height
        else:
            w = width
            h = height
        preview = preview.scaled(w, h, QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        realw = preview.width();
        realh = preview.height()
        # and move it to the centre of the preview space
        newImage = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32_Premultiplied)
        newImage.fill(QtCore.Qt.black)
        painter = QtGui.QPainter(newImage)
        painter.drawImage((w - realw) / 2, (h - realh) / 2, preview)
        return newImage

    def calculate_default(self, screen):
        """
        Calculate the default dimentions of the screen.

        ``screen``
            The QWidget instance of the screen.
        """
        log.debug(u'calculate default %s', screen)
        #size fixed so reflects the preview size.
        if self.current_display == 0:
            self.width = 1024
            self.height = 768
        else:
            self.width = screen.width()
            self.height = screen.height()
        self.screen_ratio = float(self.height) / float(self.width)
        log.debug(u'calculate default %d, %d, %f',
            self.width, self.height, self.screen_ratio )
        # 90% is start of footer
        self.footer_start = int(self.height * 0.90)