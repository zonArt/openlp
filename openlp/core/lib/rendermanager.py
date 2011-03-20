# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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

from PyQt4 import QtCore

from openlp.core.lib import Renderer, ServiceItem, ImageManager
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
FOOTER = [u'Arky Arky (Unknown)', u'Public Domain', u'CCLI 123456']

class RenderManager(object):
    """
    Class to pull all Renderer interactions into one place. The plugins will
    call helper methods to do the rendering but this class will provide
    display defense code.

    ``theme_manager``
        The ThemeManager instance, used to get the current theme details.

    ``screens``
        Contains information about the Screens.

    ``screen_number``
        Defaults to *0*. The index of the output/display screen.
    """
    log.info(u'RenderManager Loaded')

    def __init__(self, theme_manager, screens):
        """
        Initialise the render manager.
        """
        log.debug(u'Initilisation started')
        self.screens = screens
        self.image_manager = ImageManager()
        self.display = MainDisplay(self, screens, False)
        self.display.imageManager = self.image_manager
        self.theme_manager = theme_manager
        self.renderer = Renderer()
        self.calculate_default(self.screens.current[u'size'])
        self.theme = u''
        self.service_theme = u''
        self.theme_level = u''
        self.override_background = None
        self.theme_data = None
        self.force_page = False

    def update_display(self):
        """
        Updates the render manager's information about the current screen.
        """
        log.debug(u'Update Display')
        self.calculate_default(self.screens.current[u'size'])
        self.display = MainDisplay(self, self.screens, False)
        self.display.imageManager = self.image_manager
        self.display.setup()
        self.renderer.bg_frame = None
        self.theme_data = None
        self.image_manager.update_display(self.width, self.height)

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

    def set_override_theme(self, theme, overrideLevels=False):
        """
        Set the appropriate theme depending on the theme level.
        Called by the service item when building a display frame

        ``theme``
            The name of the song-level theme. None means the service
            item wants to use the given value.

        ``overrideLevels``
            Used to force the theme data passed in to be used.

        """
        log.debug(u'set override theme to %s', theme)
        theme_level = self.theme_level
        if overrideLevels:
            theme_level = ThemeLevel.Song
        if theme_level == ThemeLevel.Global:
            self.theme = self.global_theme
        elif theme_level == ThemeLevel.Service:
            if self.service_theme == u'':
                self.theme = self.global_theme
            else:
                self.theme = self.service_theme
        else:
            # Images have a theme of -1
            if theme and theme != -1:
                self.theme = theme
            elif theme_level == ThemeLevel.Song or \
                theme_level == ThemeLevel.Service:
                if self.service_theme == u'':
                    self.theme = self.global_theme
                else:
                    self.theme = self.service_theme
            else:
                self.theme = self.global_theme
        if self.theme != self.renderer.theme_name or self.theme_data is None \
            or overrideLevels:
            log.debug(u'theme is now %s', self.theme)
            # Force the theme to be the one passed in.
            if overrideLevels:
                self.theme_data = theme
            else:
                self.theme_data = self.theme_manager.getThemeData(self.theme)
            self.calculate_default(self.screens.current[u'size'])
            self.renderer.set_theme(self.theme_data)
            self.build_text_rectangle(self.theme_data)
            self.image_manager.add_image(self.theme_data.theme_name,
                self.theme_data.background_filename)
        return self.renderer._rect, self.renderer._rect_footer

    def build_text_rectangle(self, theme):
        """
        Builds a text block using the settings in ``theme``
        and the size of the display screen.height.

        ``theme``
            The theme to build a text block for.
        """
        log.debug(u'build_text_rectangle')
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
        self.renderer.set_text_rectangle(main_rect, footer_rect)

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
        self.calculate_default(self.screens.preview[u'size'])
        # build a service item to generate preview
        serviceItem = ServiceItem()
        serviceItem.theme = theme_data
        if self.force_page:
            # make big page for theme edit dialog to get line count
            serviceItem.add_from_text(u'', VERSE + VERSE + VERSE, FOOTER)
        else:
            self.image_manager.del_image(theme_data.theme_name)
            serviceItem.add_from_text(u'', VERSE, FOOTER)
        serviceItem.render_manager = self
        serviceItem.raw_footer = FOOTER
        serviceItem.render(True)
        if not self.force_page:
            self.display.buildHtml(serviceItem)
            raw_html = serviceItem.get_rendered_frame(0)
            preview = self.display.text(raw_html)
            # Reset the real screen size for subsequent render requests
            self.calculate_default(self.screens.current[u'size'])
            return preview

    def format_slide(self, words, line_break):
        """
        Calculate how much text can fit on a slide.

        ``words``
            The words to go on the slides.

        ``line_break``
            Add line endings after each line of text used for bibles.
        """
        log.debug(u'format slide')
        return self.renderer.format_slide(words, line_break, self.force_page)

    def calculate_default(self, screen):
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
