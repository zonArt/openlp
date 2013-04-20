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
The :mod:`ui` module provides the core user interface for OpenLP
"""


class HideMode(object):
    """
    This is an enumeration class which specifies the different modes of hiding the display.

    ``Blank``
        This mode is used to hide all output, specifically by covering the display with a black screen.

    ``Theme``
        This mode is used to hide all output, but covers the display with the current theme background, as opposed to
        black.

    ``Desktop``
        This mode hides all output by minimising the display, leaving the user's desktop showing.
    """
    Blank = 1
    Theme = 2
    Screen = 3


class AlertLocation(object):
    """
    This is an enumeration class which controls where Alerts are placed on the screen.

    ``Top``
        Place the text at the top of the screen.

    ``Middle``
        Place the text in the middle of the screen.

    ``Bottom``
        Place the text at the bottom of the screen.
    """
    Top = 0
    Middle = 1
    Bottom = 2


class DisplayControllerType(object):
    """
    This is an enumeration class which says where a display controller originated from.
    """
    Live = 0
    Preview = 1
    Plugin = 2


from firsttimeform import FirstTimeForm
from firsttimelanguageform import FirstTimeLanguageForm
from themelayoutform import ThemeLayoutForm
from themeform import ThemeForm
from filerenameform import FileRenameForm
from starttimeform import StartTimeForm
from maindisplay import MainDisplay, Display
from servicenoteform import ServiceNoteForm
from serviceitemeditform import ServiceItemEditForm
from slidecontroller import SlideController, DisplayController
from splashscreen import SplashScreen
from generaltab import GeneralTab
from themestab import ThemesTab
from advancedtab import AdvancedTab
from aboutform import AboutForm
from pluginform import PluginForm
from settingsform import SettingsForm
from formattingtagform import FormattingTagForm
from shortcutlistform import ShortcutListForm
from mediadockmanager import MediaDockManager
from servicemanager import ServiceManager
from thememanager import ThemeManager

__all__ = ['SplashScreen', 'AboutForm', 'SettingsForm', 'MainDisplay', 'SlideController', 'ServiceManager',
    'ThemeManager', 'MediaDockManager', 'ServiceItemEditForm', 'FirstTimeForm', 'FirstTimeLanguageForm', 'ThemeForm',
    'ThemeLayoutForm', 'FileRenameForm', 'StartTimeForm', 'MainDisplay', 'Display', 'ServiceNoteForm',
    'SlideController', 'DisplayController', 'GeneralTab', 'ThemesTab', 'AdvancedTab', 'PluginForm',
    'FormattingTagForm', 'ShortcutListForm']
