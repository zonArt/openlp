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

from openlp.core.lib import SlideLimits
from openlp.core.lib.theme import ThemeLevel
from openlp.core.lib import UiStrings


log = logging.getLogger(__name__)


# Fix for bug #1014422.
X11_BYPASS_DEFAULT = True
if sys.platform.startswith(u'linux'):
    # Default to False on Gnome.
    X11_BYPASS_DEFAULT = bool(not os.environ.get(u'GNOME_DESKTOP_SESSION_ID'))
    # Default to False on Xfce.
    if os.environ.get(u'DESKTOP_SESSION') == u'xfce':
        X11_BYPASS_DEFAULT = False


class Settings(QtCore.QSettings):
    """
    Class to wrap QSettings.

    * Exposes all the methods of QSettings.
    * Adds functionality for OpenLP Portable. If the ``defaultFormat`` is set to
    ``IniFormat``, and the path to the Ini file is set using ``set_filename``,
    then the Settings constructor (without any arguments) will create a Settings
    object for accessing settings stored in that Ini file.

    ``__default_settings__``
        This dict contains all core settings with their default values.

    ``__obsolete_settings__``
        Each entry is structured in the following way::

            (u'general/enable slide loop',  u'advanced/slide limits', [(SlideLimits.Wrap, True), (SlideLimits.End, False)])

        The first entry is the *old key*; it will be removed.

        The second entry is the *new key*; we will add it to the config. If this is just an empty string, we just remove
        the old key.

        The last entry is a list containing two-pair tuples. If the list is empty, no conversion is made. Otherwise each
        pair describes how to convert the old setting's value::

            (SlideLimits.Wrap, True)

        This means, that if the value of ``general/enable slide loop`` is equal (``==``) ``True`` then we set
        ``advanced/slide limits`` to ``SlideLimits.Wrap``. **NOTE**, this means that the rules have to cover all cases!
        So, if the type of the old value is bool, then there must be two rules.
    """
    __default_settings__ = {
        u'advanced/add page break': False,
        u'advanced/alternate rows': not sys.platform.startswith(u'win'),
        u'advanced/current media plugin': -1,
        u'advanced/data path': u'',
        u'advanced/default color': u'#ffffff',
        u'advanced/default image': u':/graphics/openlp-splash-screen.png',
        # 7 stands for now, 0 to 6 is Monday to Sunday.
        u'advanced/default service day': 7,
        u'advanced/default service enabled': True,
        u'advanced/default service hour': 11,
        u'advanced/default service minute': 0,
        u'advanced/default service name': UiStrings().DefaultServiceName,
        u'advanced/display size': 0,
        u'advanced/double click live': False,
        u'advanced/enable exit confirmation': True,
        u'advanced/expand service item': False,
        u'advanced/hide mouse': True,
        u'advanced/is portable': False,
        u'advanced/max recent files': 20,
        u'advanced/print file meta data': False,
        u'advanced/print notes': False,
        u'advanced/print slide text': False,
        u'advanced/recent file count': 4,
        u'advanced/save current plugin': False,
        u'advanced/slide limits': SlideLimits.End,
        u'advanced/single click preview': False,
        u'advanced/x11 bypass wm': X11_BYPASS_DEFAULT,
        u'crashreport/last directory': u'',
        u'displayTags/html_tags': u'',
        u'general/audio repeat list': False,
        u'general/auto open': False,
        u'general/auto preview': False,
        u'general/audio start paused': True,
        u'general/auto unblank': False,
        u'general/blank warning': False,
        u'general/ccli number': u'',
        u'general/has run wizard': False,
        u'general/language': u'[en]',
        # This defaults to yesterday in order to force the update check to run when you've never run it before.
        u'general/last version test': datetime.datetime.now().date() - datetime.timedelta(days=1),
        u'general/loop delay': 5,
        u'general/recent files': [],
        u'general/save prompt': False,
        u'general/screen blank': False,
        u'general/show splash': True,
        u'general/songselect password': u'',
        u'general/songselect username': u'',
        u'general/update check': True,
        u'general/view mode': u'default',
        # The other display settings (display position and dimensions) are defined in the ScreenList class due to a
        # circular dependency.
        u'general/display on monitor': True,
        u'general/override position': False,
        u'media/players': u'webkit',
        u'media/override player': QtCore.Qt.Unchecked,
        u'players/background color': u'#000000',
        u'servicemanager/last directory': u'',
        u'servicemanager/last file': u'',
        u'servicemanager/service theme': u'',
        u'SettingsImport/file_date_created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        u'SettingsImport/Make_Changes': u'At_Own_RISK',
        u'SettingsImport/type': u'OpenLP_settings_export',
        u'SettingsImport/version': u'',
        u'shortcuts/aboutItem': [QtGui.QKeySequence(u'Ctrl+F1')],
        u'shortcuts/audioPauseItem': [],
        u'shortcuts/displayTagItem': [],
        u'shortcuts/blankScreen': [QtCore.Qt.Key_Period],
        u'shortcuts/collapse': [QtCore.Qt.Key_Minus],
        u'shortcuts/desktopScreen': [QtGui.QKeySequence(u'D')],
        u'shortcuts/down': [QtCore.Qt.Key_Down],
        u'shortcuts/escapeItem': [QtCore.Qt.Key_Escape],
        u'shortcuts/expand': [QtCore.Qt.Key_Plus],
        u'shortcuts/exportThemeItem': [],
        u'shortcuts/fileNewItem': [QtGui.QKeySequence(u'Ctrl+N')],
        u'shortcuts/fileSaveAsItem': [QtGui.QKeySequence(u'Ctrl+Shift+S')],
        u'shortcuts/fileExitItem': [QtGui.QKeySequence(u'Alt+F4')],
        u'shortcuts/fileSaveItem': [QtGui.QKeySequence(u'Ctrl+S')],
        u'shortcuts/fileOpenItem': [QtGui.QKeySequence(u'Ctrl+O')],
        u'shortcuts/importThemeItem': [],
        u'shortcuts/importBibleItem': [],
        u'shortcuts/modeDefaultItem': [],
        u'shortcuts/modeLiveItem': [],
        u'shortcuts/make_live': [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return],
        u'shortcuts/moveUp': [QtCore.Qt.Key_PageUp],
        u'shortcuts/moveTop': [QtCore.Qt.Key_Home],
        u'shortcuts/modeSetupItem': [],
        u'shortcuts/moveBottom': [QtCore.Qt.Key_End],
        u'shortcuts/moveDown': [QtCore.Qt.Key_PageDown],
        u'shortcuts/nextTrackItem': [],
        u'shortcuts/nextItem_live': [QtCore.Qt.Key_Down, QtCore.Qt.Key_PageDown],
        u'shortcuts/nextService': [QtCore.Qt.Key_Right],
        u'shortcuts/offlineHelpItem': [],
        u'shortcuts/onlineHelpItem': [QtGui.QKeySequence(u'Alt+F1')],
        u'shortcuts/previousItem_live': [QtCore.Qt.Key_Up, QtCore.Qt.Key_PageUp],
        u'shortcuts/playSlidesLoop': [],
        u'shortcuts/playSlidesOnce': [],
        u'shortcuts/previousService': [QtCore.Qt.Key_Left],
        u'shortcuts/printServiceItem': [QtGui.QKeySequence(u'Ctrl+P')],
        u'shortcuts/songExportItem': [],
        u'shortcuts/songUsageStatus': [QtCore.Qt.Key_F4],
        u'shortcuts/settingsShortcutsItem': [],
        u'shortcuts/settingsImportItem': [],
        u'shortcuts/settingsPluginListItem': [QtGui.QKeySequence(u'Alt+F7')],
        u'shortcuts/songUsageDelete': [],
        u'shortcuts/settingsConfigureItem': [],
        u'shortcuts/shortcutAction_B': [QtGui.QKeySequence(u'B')],
        u'shortcuts/shortcutAction_C': [QtGui.QKeySequence(u'C')],
        u'shortcuts/shortcutAction_E': [QtGui.QKeySequence(u'E')],
        u'shortcuts/shortcutAction_I': [QtGui.QKeySequence(u'I')],
        u'shortcuts/shortcutAction_O': [QtGui.QKeySequence(u'O')],
        u'shortcuts/shortcutAction_P': [QtGui.QKeySequence(u'P')],
        u'shortcuts/shortcutAction_V': [QtGui.QKeySequence(u'V')],
        u'shortcuts/settingsExportItem': [],
        u'shortcuts/songUsageReport': [],
        u'shortcuts/songImportItem': [],
        u'shortcuts/themeScreen': [QtGui.QKeySequence(u'T')],
        u'shortcuts/toolsReindexItem': [],
        u'shortcuts/toolsAlertItem': [u'F7'],
        u'shortcuts/toolsFirstTimeWizard': [],
        u'shortcuts/toolsOpenDataFolder': [],
        u'shortcuts/toolsAddToolItem': [],
        u'shortcuts/updateThemeImages': [],
        u'shortcuts/up': [QtCore.Qt.Key_Up],
        u'shortcuts/viewThemeManagerItem': [QtGui.QKeySequence(u'F10')],
        u'shortcuts/viewMediaManagerItem': [QtGui.QKeySequence(u'F8')],
        u'shortcuts/viewPreviewPanel': [QtGui.QKeySequence(u'F11')],
        u'shortcuts/viewLivePanel': [QtGui.QKeySequence(u'F12')],
        u'shortcuts/viewServiceManagerItem': [QtGui.QKeySequence(u'F9')],
        u'shortcuts/webSiteItem': [],
        u'themes/global theme': u'',
        u'themes/last directory': u'',
        u'themes/last directory export': u'',
        u'themes/last directory import': u'',
        u'themes/theme level': ThemeLevel.Song,
        u'user interface/live panel': True,
        u'user interface/live splitter geometry': QtCore.QByteArray(),
        u'user interface/lock panel': False,
        u'user interface/main window geometry': QtCore.QByteArray(),
        u'user interface/main window position': QtCore.QPoint(0, 0),
        u'user interface/main window splitter geometry': QtCore.QByteArray(),
        u'user interface/main window state': QtCore.QByteArray(),
        u'user interface/preview panel': True,
        u'user interface/preview splitter geometry': QtCore.QByteArray()
    }
    __file_path__ = u''
    __obsolete_settings__ = [
        # Changed during 1.9.x development.
        (u'bibles/bookname language', u'bibles/book name language', []),
        (u'general/enable slide loop', u'advanced/slide limits', [(SlideLimits.Wrap, True), (SlideLimits.End, False)]),
        (u'songs/ccli number', u'general/ccli number', []),
        # Changed during 2.1.x development.
        (u'advanced/stylesheet fix', u'', []),
        (u'bibles/last directory 1', u'bibles/last directory import', []),
        (u'media/background color', u'players/background color', []),
        (u'themes/last directory', u'themes/last directory import', []),
        (u'themes/last directory 1', u'themes/last directory export', []),
        (u'songs/last directory 1', u'songs/last directory import', []),
        (u'songusage/last directory 1', u'songusage/last directory export', []),
        (u'user interface/mainwindow splitter geometry', u'user interface/main window splitter geometry', []),
        (u'shortcuts/makeLive', u'shortcuts/make_live', [])
    ]

    @staticmethod
    def extend_default_settings(default_values):
        """
        Static method to merge the given ``default_values`` with the ``Settings.__default_settings__``.

        ``default_values``
            A dict with setting keys and their default values.
        """
        Settings.__default_settings__ = dict(default_values.items() + Settings.__default_settings__.items())

    @staticmethod
    def set_filename(ini_file):
        """
        Sets the complete path to an Ini file to be used by Settings objects.

        Does not affect existing Settings objects.
        """
        Settings.__file_path__ = ini_file

    @staticmethod
    def set_up_default_values():
        """
        This static method is called on start up. It is used to perform any operation on the __default_settings__ dict.
        """
        # Make sure the string is translated (when building the dict the string is not translated because the translate
        # function was not set up as this stage).
        Settings.__default_settings__[u'advanced/default service name'] = UiStrings().DefaultServiceName

    def __init__(self, *args):
        """
        Constructor which checks if this should be a native settings object, or an INI file.
        """
        if not args and Settings.__file_path__ and Settings.defaultFormat() == Settings.IniFormat:
            QtCore.QSettings.__init__(self, Settings.__file_path__, Settings.IniFormat)
        else:
            QtCore.QSettings.__init__(self, *args)

    def remove_obsolete_settings(self):
        """
        This method is only called to clean up the config. It removes old settings and it renames settings. See
        ``__obsolete_settings__`` for more details.
        """
        for old_key, new_key, rules in Settings.__obsolete_settings__:
            # Once removed we don't have to do this again.
            if self.contains(old_key):
                if new_key:
                    # Get the value of the old_key.
                    old_value = super(Settings, self).value(old_key)
                    # When we want to convert the value, we have to figure out the default value (because we cannot get
                    # the default value from the central settings dict.
                    if rules:
                        default_value = rules[0][1]
                        old_value = self._convert_value(old_value, default_value)
                    # Iterate over our rules and check what the old_value should be "converted" to.
                    for new, old in rules:
                        # If the value matches with the condition (rule), then use the provided value. This is used to
                        # convert values. E. g. an old value 1 results in True, and 0 in False.
                        if old == old_value:
                            old_value = new
                            break
                    self.setValue(new_key, old_value)
                self.remove(old_key)

    def value(self, key):
        """
        Returns the value for the given ``key``. The returned ``value`` is of the same type as the default value in the
        *Settings.__default_settings__* dict.

        ``key``
            The key to return the value from.
        """
        # if group() is not empty the group has not been specified together with the key.
        if self.group():
            default_value = Settings.__default_settings__[self.group() + u'/' + key]
        else:
            default_value = Settings.__default_settings__[key]
        setting = super(Settings, self).value(key, default_value)
        return self._convert_value(setting, default_value)

    def _convert_value(self, setting, default_value):
        """
        This converts the given ``setting`` to the type of the given ``default_value``.

        ``setting``
            The setting to convert. This could be ``true`` for example.Settings()

        ``default_value``
            Indication the type the setting should be converted to. For example ``True`` (type is boolean), meaning that
            we convert the string ``true`` to a python boolean.

        **Note**, this method only converts a few types and might need to be extended if a certain type is missing!
        """
        # On OS X (and probably on other platforms too) empty value from QSettings is represented as type
        # PyQt4.QtCore.QPyNullVariant. This type has to be converted to proper 'None' Python type.
        if isinstance(setting, QtCore.QPyNullVariant) and setting.isNull():
            setting = None
        # Handle 'None' type (empty value) properly.
        if setting is None:
            # An empty string saved to the settings results in a None type being returned.
            # Convert it to empty unicode string.
            if isinstance(default_value, unicode):
                return u''
            # An empty list saved to the settings results in a None type being returned.
            else:
                return []
        # Convert the setting to the correct type.
        if isinstance(default_value, bool):
            if isinstance(setting, bool):
                return setting
            # Sometimes setting is string instead of a boolean.
            return setting == u'true'
        if isinstance(default_value, int):
            return int(setting)
        return setting
