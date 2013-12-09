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
"""
The Theme Controller helps manages adding, deleteing and modifying of themes.
"""
import logging
import os

from openlp.core.common import AppLocation, Settings, check_directory_exists

log = logging.getLogger(__name__)


class ThemeManagerHelper(object):
    """
    Manages the non ui theme functions.
    """
    def initialise(self):
        """
        Setup the manager
        """
        log.debug('initialise called')
        self.global_theme = Settings().value(self.settings_section + '/global theme')
        self.build_theme_path()
        self.load_first_time_themes()

    def build_theme_path(self):
        """
        Set up the theme path variables
        """
        log.debug('build theme path called')
        self.path = AppLocation.get_section_data_path(self.settings_section)
        check_directory_exists(self.path)
        self.thumb_path = os.path.join(self.path, 'thumbnails')
        check_directory_exists(self.thumb_path)
        self.theme_form.path = self.path