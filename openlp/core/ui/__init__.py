# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
    This is basically an enumeration class which specifies the mode of a Bible.
    Mode refers to whether or not a Bible in OpenLP is a full Bible or needs to
    be downloaded from the Internet on an as-needed basis.
    """
    Blank = 1
    Theme = 2
    Screen = 3

from slidecontroller import HideMode
from servicenoteform import ServiceNoteForm
from serviceitemeditform import ServiceItemEditForm
from screen import ScreenList
from maindisplay import MainDisplay
from maindisplay import VideoDisplay
from maindisplay import DisplayManager
from amendthemeform import AmendThemeForm
from slidecontroller import SlideController
from splashscreen import SplashScreen
from generaltab import GeneralTab
from themestab import ThemesTab
from advancedtab import AdvancedTab
from aboutform import AboutForm
from pluginform import PluginForm
from settingsform import SettingsForm
from mediadockmanager import MediaDockManager
from servicemanager import ServiceManager
from thememanager import ThemeManager
from mainwindow import MainWindow

__all__ = ['SplashScreen', 'AboutForm', 'SettingsForm', 'MainWindow',
    'MainDisplay', 'SlideController', 'ServiceManager', 'ThemeManager',
    'AmendThemeForm', 'MediaDockManager', 'ServiceItemEditForm']
