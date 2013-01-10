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
This class contains the core default settings.
"""
import datetime
import logging
import os
import sys

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SlideLimits, ScreenList
from openlp.core.lib.theme import ThemeLevel
from openlp.core.lib.ui import UiStrings

log = logging.getLogger(__name__)

class Settings(QtCore.QSettings):
    """
    Class to wrap QSettings.

    * Exposes all the methods of QSettings.
    * Adds functionality for OpenLP Portable. If the ``defaultFormat`` is set to
    ``IniFormat``, and the path to the Ini file is set using ``setFilename``,
    then the Settings constructor (without any arguments) will create a Settings
    object for accessing settings stored in that Ini file.
    """
    __filePath__ = u''

    # Fix for bug #1014422.
    x11_bypass_default = True
    if sys.platform.startswith(u'linux'):
        # Default to False on Gnome.
        x11_bypass_default = bool(not os.environ.get(u'GNOME_DESKTOP_SESSION_ID'))
        # Default to False on XFce
        if os.environ.get(u'DESKTOP_SESSION') == u'xfce':
            x11_bypass_default = False

    __default_settings__ = {
        u'advanced/x11 bypass wm': x11_bypass_default,
        u'advanced/default service enabled': True,
        u'advanced/enable exit confirmation': True,
        u'advanced/save current plugin': False,
        u'advanced/single click preview': False,
        # 7 stands for now, 0 to 6 is Monday to Sunday.
        u'advanced/default service day': 7,
        u'advanced/max recent files': 20,
        u'advanced/is portable': False,
        u'advanced/hide mouse': True,
        u'advanced/current media plugin': -1,
        u'advanced/double click live': False,
        u'advanced/default service hour': 11,
        u'advanced/default color': u'#ffffff',
        u'advanced/default image': u':/graphics/openlp-splash-screen.png',
        u'advanced/expand service item': False,
        u'advanced/recent file count': 4,
        # TODO: Check if translate already works at this stage. If not move the string to Ui String class.
        u'advanced/default service name': UiStrings().DefaultServiceName,
        u'advanced/default service minute': 0,
        u'advanced/slide limits': SlideLimits.End,
        u'advanced/print slide text': False,
        u'advanced/add page break': False,
        u'advanced/print file meta data': False,
        u'advanced/print notes': False,
        u'advanced/display size': 0,
        u'displayTags/html_tags': u'',
        u'general/ccli number': u'',
        u'general/has run wizard': False,
        u'general/update check': True,
        u'general/language': u'[en]',
        u'general/songselect password': u'',
        u'general/recent files': [],
        u'general/save prompt': False,
        u'general/auto preview': False,
        u'general/override position': False,
        u'general/view mode': u'default',
        u'general/auto open': False,
        u'general/enable slide loop': True,
        u'general/show splash': True,
        u'general/screen blank': False,
        u'general/x position': 0, #ScreenList().current[u'size'].x()
        u'general/y position': 0, # ScreenList().current[u'size'].y()
        u'general/monitor': 0, # ScreenList().display_count - 1
        u'general/height': 1024, # ScreenList().current[u'size'].height()
        u'general/width': 1280, # ScreenList().current[u'size'].width()
        u'general/loop delay': 5,
        u'general/songselect username': u'',
        u'general/audio repeat list': False,
        u'general/auto unblank': False,
        u'general/display on monitor': True,
        u'general/audio start paused': True,
        u'general/last version test': datetime.datetime.now().date(),
        u'general/blank warning': False,
        u'shortcuts/viewPreviewPanel': [QtGui.QKeySequence(u'F11')],
        u'shortcuts/settingsImportItem': [],
        u'shortcuts/settingsPluginListItem': [QtGui.QKeySequence(u'Alt+F7')],
        u'shortcuts/modeLiveItem': [],
        u'shortcuts/songUsageStatus': [QtCore.Qt.Key_F4],
        u'shortcuts/nextTrackItem': [],
        u'shortcuts/makeLive': [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return],
        u'shortcuts/webSiteItem': [],
        u'shortcuts/shortcutAction_P': [QtGui.QKeySequence(u'P')],
        u'shortcuts/previousItem_live': [QtCore.Qt.Key_Up, QtCore.Qt.Key_PageUp],
        u'shortcuts/shortcutAction_V': [QtGui.QKeySequence(u'V')],
        u'shortcuts/fileOpenItem': [QtGui.QKeySequence(u'Ctrl+O')],
        u'shortcuts/viewMediaManagerItem': [QtGui.QKeySequence(u'F8')],
        u'shortcuts/desktopScreen': [QtGui.QKeySequence(u'D')],
        u'shortcuts/songExportItem': [],
        u'shortcuts/modeDefaultItem': [],
        u'shortcuts/audioPauseItem': [],
        u'shortcuts/themeScreen': [QtGui.QKeySequence(u'T')],
        u'shortcuts/expand': [QtCore.Qt.Key_Plus],
        u'shortcuts/exportThemeItem': [],
        u'shortcuts/viewThemeManagerItem': [QtGui.QKeySequence(u'F10')],
        u'shortcuts/playSlidesLoop': [],
        u'shortcuts/playSlidesOnce': [],
        u'shortcuts/toolsReindexItem': [],
        u'shortcuts/toolsAlertItem': [u'F7'],
        u'shortcuts/printServiceItem': [QtGui.QKeySequence(u'Ctrl+P')],
        u'shortcuts/moveUp': [QtCore.Qt.Key_PageUp],
        u'shortcuts/settingsShortcutsItem': [],
        u'shortcuts/nextItem_live': [QtCore.Qt.Key_Down, QtCore.Qt.Key_PageDown],
        u'shortcuts/moveTop': [QtCore.Qt.Key_Home],
        u'shortcuts/blankScreen': [QtCore.Qt.Key_Period],
        u'shortcuts/settingsConfigureItem': [],
        u'shortcuts/modeSetupItem': [],
        u'shortcuts/songUsageDelete': [],
        u'shortcuts/shortcutAction_C': [QtGui.QKeySequence(u'C')],
        u'shortcuts/shortcutAction_B': [QtGui.QKeySequence(u'B')],
        u'shortcuts/shortcutAction_E': [QtGui.QKeySequence(u'E')],
        u'shortcuts/shortcutAction_I': [QtGui.QKeySequence(u'I')],
        u'shortcuts/shortcutAction_O': [QtGui.QKeySequence(u'O')],
        u'shortcuts/importBibleItem': [],
        u'shortcuts/fileExitItem': [QtGui.QKeySequence(u'Alt+F4')],
        u'shortcuts/fileSaveItem': [QtGui.QKeySequence(u'Ctrl+S')],
        u'shortcuts/up': [QtCore.Qt.Key_Up],
        u'shortcuts/nextService': [QtCore.Qt.Key_Right],
        u'shortcuts/songImportItem': [],
        u'shortcuts/toolsOpenDataFolder': [],
        u'shortcuts/fileNewItem': [QtGui.QKeySequence(u'Ctrl+N')],
        u'shortcuts/aboutItem': [QtGui.QKeySequence(u'Ctrl+F1')],
        u'shortcuts/viewLivePanel': [QtGui.QKeySequence(u'F12')],
        u'shortcuts/songUsageReport': [],
        u'shortcuts/updateThemeImages': [],
        u'shortcuts/toolsAddToolItem': [],
        u'shortcuts/fileSaveAsItem': [QtGui.QKeySequence(u'Ctrl+Shift+S')],
        u'shortcuts/settingsExportItem': [],
        u'shortcuts/onlineHelpItem': [QtGui.QKeySequence(u'Alt+F1')],
        u'shortcuts/escapeItem': [QtCore.Qt.Key_Escape],
        u'shortcuts/displayTagItem': [],
        u'shortcuts/moveBottom': [QtCore.Qt.Key_End],
        u'shortcuts/toolsFirstTimeWizard': [],
        u'shortcuts/moveDown': [QtCore.Qt.Key_PageDown],
        u'shortcuts/collapse': [QtCore.Qt.Key_Minus],
        u'shortcuts/viewServiceManagerItem': [QtGui.QKeySequence(u'F9')],
        u'shortcuts/previousService': [QtCore.Qt.Key_Left],
        u'shortcuts/importThemeItem': [],
        u'shortcuts/down': [QtCore.Qt.Key_Down],
        u'themes/theme level': ThemeLevel.Song,
        u'themes/global theme': u'',
        u'themes/last directory': u'',
        u'user interface/main window position': QtCore.QPoint(),
        u'user interface/preview panel': True,
        u'user interface/live panel': True,
        u'user interface/main window geometry': QtCore.QByteArray(),
        u'user interface/preview splitter geometry': QtCore.QByteArray(),
        u'user interface/lock panel': False,
        u'user interface/mainwindow splitter geometry': QtCore.QByteArray(),
        u'user interface/live splitter geometry': QtCore.QByteArray(),
        u'user interface/main window state': QtCore.QByteArray(),

        u'servicemanager/service theme': u'',
        u'players/background color': u'#000000',

        # HAS TO BE HERE. Should be FIXED.
        u'media/players': u'webkit',
        u'media/override player': QtCore.Qt.Unchecked
    }

    @staticmethod
    def extendDefaultSettings(defaultValues):
        """

        """
        Settings.__default_settings__ = dict(defaultValues.items() + Settings.__default_settings__.items())

    @staticmethod
    def setFilename(iniFile):
        """
        Sets the complete path to an Ini file to be used by Settings objects.

        Does not affect existing Settings objects.
        """
        Settings.__filePath__ = iniFile

    def __init__(self, *args):
        if not args and Settings.__filePath__ and \
            Settings.defaultFormat() == Settings.IniFormat:
            QtCore.QSettings.__init__(self, Settings.__filePath__, Settings.IniFormat)
        else:
            QtCore.QSettings.__init__(self, *args)

    def value(self, key, defaultValue=0):
        """
        Returns the value for the given ``key``. The returned ``value`` is
        of the same type as the ``defaultValue``.

        ``key``
            The key to return the value from.

        ``defaultValue``
            The value to be returned if the given ``key`` is not present in the
            config. Note, the ``defaultValue``'s type defines the type the
            returned is converted to. In other words, if the ``defaultValue`` is
            a boolean, then the returned value will be converted to a boolean.

            **Note**, this method only converts a few types and might need to be
            extended if a certain type is missing!
        """
        if defaultValue:
            raise Exception(u'Should not happen')
        if u'/' not in key:
            key = u'/'.join((self.group(), key))
        # Check for none as u'' is passed as default and is valid! This is
        # needed because the settings export does not know the default values,
        # thus just passes None.
        defaultValue = Settings.__default_settings__[key]
#        try:
#            defaultValue = Settings.__default_settings__[key]
#        except KeyError:
#            return None

        #if defaultValue is None and not super(Settings, self).contains(key):
            #return None

        setting =  super(Settings, self).value(key, defaultValue)
        # On OS X (and probably on other platforms too) empty value from QSettings
        # is represented as type PyQt4.QtCore.QPyNullVariant. This type has to be
        # converted to proper 'None' Python type.
        if isinstance(setting, QtCore.QPyNullVariant) and setting.isNull():
            setting = None
        # Handle 'None' type (empty value) properly.
        if setting is None:
            # An empty string saved to the settings results in a None type being
            # returned. Convert it to empty unicode string.
            if isinstance(defaultValue, unicode):
                return u''
            # An empty list saved to the settings results in a None type being
            # returned.
            else:
                return []
        # Convert the setting to the correct type.
        if isinstance(defaultValue, bool):
            if isinstance(setting, bool):
                return setting
            # Sometimes setting is string instead of a boolean.
            return setting == u'true'
        if isinstance(defaultValue, int):
            return int(setting)
        return setting




