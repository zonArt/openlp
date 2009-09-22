# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

#from slidecontroller import MasterToolbar
from maindisplay import MainDisplay
from amendthemeform import AmendThemeForm
from slidecontroller import SlideController
from splashscreen import SplashScreen
from alertstab import AlertsTab
from generaltab import GeneralTab
from themestab import ThemesTab
from about import AboutForm
from alertform import AlertForm
from plugindialoglistform import PluginForm
from settingsform import SettingsForm
from servicemanager import ServiceManager
from thememanager import ThemeManager
from mainwindow import MainWindow

__all__ = ['SplashScreen', 'AboutForm', 'SettingsForm', 'MasterToolbar',
           'MainWindow', 'MainDisplay', 'SlideController', 'ServiceManager',
           'ThemeManager', 'AmendThemeForm']
