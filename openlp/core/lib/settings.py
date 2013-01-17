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

        The second entry is the *new key*; we will add it to the config.

        The last entry is a list containing two-pair tuples. If the list is empty, no conversion is made. Otherwise each
        pair describes how to convert the old setting's value::

            (SlideLimits.Wrap, True)

        This means, that if the value of ``general/enable slide loop`` is equal (``==``) ``True`` then we set
        ``advanced/slide limits`` to ``SlideLimits.Wrap``. **NOTE**, this means that the rules have to cover all cases!
        So, if the type of the old value is bool, then there must be two rules.
    """
    __default_settings__ = {
        u'advanced/x11 bypass wm': X11_BYPASS_DEFAULT,
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
        u'advanced/default service name': u'',#UiStrings().DefaultServiceName,
        u'advanced/default service minute': 0,
        u'advanced/slide limits': SlideLimits.End,
        u'advanced/print slide text': False,
        u'advanced/add page break': False,
        u'advanced/print file meta data': False,
        u'advanced/print notes': False,
        u'advanced/display size': 0,
        u'crashreport/last directory': u'',
        u'displayTags/html_tags': u'',
        u'general/ccli number': u'',
        u'general/has run wizard': False,
        u'general/update check': True,
        u'general/language': u'[en]',
        u'general/songselect password': u'',
        u'general/recent files': [],
        u'general/save prompt': False,
        u'general/auto preview': False,
        u'general/view mode': u'default',
        u'general/auto open': False,
        u'general/enable slide loop': True,
        u'general/show splash': True,
        u'general/screen blank': False,
        u'general/override position': False,
        # Display defaults are set in core/lib/screen.py due to a circle dependency.
        u'general/x position': -1,
        u'general/y position': -1,
        u'general/monitor': -1,
        u'general/height': -1,
        u'general/width': -1,
        u'general/loop delay': 5,
        u'general/songselect username': u'',
        u'general/audio repeat list': False,
        u'general/auto unblank': False,
        u'general/display on monitor': True,
        u'general/audio start paused': True,
        # This defaults to yesterday in order to force the update check to run when you've never run it before.
        u'general/last version test': datetime.datetime.now().date() - datetime.timedelta(days=1),
        u'general/blank warning': False,
        u'players/background color': u'#000000',
        u'servicemanager/service theme': u'',
        u'servicemanager/last directory': u'',
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
        u'themes/last directory export': u'',
        u'themes/last directory import': u'',
        u'user interface/main window position': QtCore.QPoint(0, 0),
        u'user interface/preview panel': True,
        u'user interface/live panel': True,
        u'user interface/main window geometry': QtCore.QByteArray(),
        u'user interface/preview splitter geometry': QtCore.QByteArray(),
        u'user interface/lock panel': False,
        u'user interface/mainwindow splitter geometry': QtCore.QByteArray(),
        u'user interface/live splitter geometry': QtCore.QByteArray(),
        u'user interface/main window state': QtCore.QByteArray(),
        u'media/players': u'webkit',
        u'media/override player': QtCore.Qt.Unchecked
    }
    __file_path__ = u''
    __obsolete_settings__ = [
        (u'bibles/bookname language', u'bibles/book name language', []),
        (u'general/enable slide loop',  u'advanced/slide limits', [(SlideLimits.Wrap, True), (SlideLimits.End, False)])
#        song usage/last directory 1 -> last directory import
#        bibles/last directory 1 -> bibles/last directory backup
#        themes/last directory -> themes/last directory import
#        themes/last directory 1-> themes/last directory export
#        songs/last directory 1 -> songs/last directory error log
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
    def set_filename(iniFile):
        """
        Sets the complete path to an Ini file to be used by Settings objects.

        Does not affect existing Settings objects.
        """
        Settings.__file_path__ = iniFile

    @staticmethod
    def set_up_default_values():
        """
        This static method is called on start up. It is used to perform any operation on the __default_settings__ dict.
        """
        # Make sure the string is translated (when building the dict the string is not translated because the translate
        # function was not set up as this stage).
        Settings.__default_settings__[u'advanced/default service name'] = UiStrings().DefaultServiceName

    def __init__(self, *args):
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
                    # Iterate over our rules and check what the old_value should be "converted" to.
                    for new, old in rules:
                        # If the value matches with the condition (rule), then use the provided value. This is used to
                        # convert values. E. g. an old value 1 results in True, and 0 in False.
                        if old == old_value:
                            old_value = new
                            break
                    self.setValue(new_key, old_value)
                self.remove(old_key)

    def value(self, key, default_value=None):
        """
        Returns the value for the given ``key``. The returned ``value`` is of the same type as the default value in the
        *Settings.__default_settings__* dict.

        **Note**, this method only converts a few types and might need to be extended if a certain type is missing!

        ``key``
            The key to return the value from.

        ``default_value``
            **Note**, do **not** use this. It is *only* for dynamic keys such as ``something %d``.
        """
        # FIXME: remove default_value
        if default_value is None:
            # if group() is not empty the group has not been specified together with the key.
            if self.group():
                default_value = Settings.__default_settings__[self.group() + u'/' + key]
            else:
                default_value = Settings.__default_settings__[key]
        setting = super(Settings, self).value(key, default_value)
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

