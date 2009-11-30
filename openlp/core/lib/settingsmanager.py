# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Tim Bentley, Jonathan Corwin, Michael      #
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

from openlp.core.lib import str_to_bool
from openlp.core.utils import ConfigHelper

class SettingsManager(object):
    """
    Class to control the size of the UI components so they size correctly.
    This class is created by the main window and then calculates the size of
    individual components.
    """
    def __init__(self, screen):
        self.screen = screen[0]
        self.width = self.screen[u'size'].width()
        self.height = self.screen[u'size'].height()
        self.mainwindow_height = self.height * 0.8
        mainwindow_docbars = self.width / 5
        self.mainwindow_left = 0
        self.mainwindow_right = 0
        if mainwindow_docbars > 300:
            self.mainwindow_left = 300
            self.mainwindow_right = 300
        else:
            self.mainwindow_left = mainwindow_docbars
            self.mainwindow_right = mainwindow_docbars
        self.slidecontroller = (self.width - (
            self.mainwindow_left + self.mainwindow_right) - 100 ) / 2
        self.slidecontroller_image = self.slidecontroller - 50

        self.showMediaManager = str_to_bool(ConfigHelper.get_config(
            u'user interface', u'media manager', True))
        self.showServiceManager = str_to_bool(ConfigHelper.get_config(
            u'user interface', u'service manager', True))
        self.showThemeManager = str_to_bool(ConfigHelper.get_config(
            u'user interface', u'theme manager', True))
        self.showPreviewPanel = str_to_bool(ConfigHelper.get_config(
            u'user interface', u'preview panel', True))

    def setUIItemVisibility(self, item=u'', isVisible=True):
        if item:
            if item == u'ThemeManagerDock':
                ConfigHelper.set_config(u'user interface',
                    u'theme manager', isVisible)
            elif item == u'ServiceManagerDock':
                ConfigHelper.set_config(u'user interface',
                    u'service manager', isVisible)
            elif item == u'MediaManagerDock':
                ConfigHelper.set_config(u'user interface',
                    u'media manager', isVisible)

    def togglePreviewPanel(self, isVisible):
        ConfigHelper.set_config(u'user interface', u'preview panel', isVisible)
