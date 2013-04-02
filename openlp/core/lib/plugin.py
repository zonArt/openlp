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
Provide the generic plugin functionality for OpenLP plugins.
"""
import logging

from PyQt4 import QtCore

from openlp.core.lib import Receiver, Settings, Registry, UiStrings
from openlp.core.utils import get_application_version

log = logging.getLogger(__name__)


class PluginStatus(object):
    """
    Defines the status of the plugin
    """
    Active = 1
    Inactive = 0
    Disabled = -1


class StringContent(object):
    """
    Provide standard strings for objects to use.
    """
    Name = u'name'
    Import = u'import'
    Load = u'load'
    New = u'new'
    Edit = u'edit'
    Delete = u'delete'
    Preview = u'preview'
    Live = u'live'
    Service = u'service'
    VisibleName = u'visible_name'


class Plugin(QtCore.QObject):
    """
    Base class for openlp plugins to inherit from.

    **Basic Attributes**

    ``name``
        The name that should appear in the plugins list.

    ``version``
        The version number of this iteration of the plugin.

    ``settingsSection``
        The namespace to store settings for the plugin.

    ``icon``
        An instance of QIcon, which holds an icon for this plugin.

    ``log``
        A log object used to log debugging messages. This is pre-instantiated.

    ``weight``
        A numerical value used to order the plugins.

    **Hook Functions**

    ``checkPreConditions()``
        Provides the Plugin with a handle to check if it can be loaded.

    ``createMediaManagerItem()``
        Creates a new instance of MediaManagerItem to be used in the Media
        Manager.

    ``addImportMenuItem(import_menu)``
        Add an item to the Import menu.

    ``addExportMenuItem(export_menu)``
        Add an item to the Export menu.

    ``createSettingsTab()``
        Creates a new instance of SettingsTabItem to be used in the Settings
        dialog.

    ``addToMenu(menubar)``
        A method to add a menu item to anywhere in the menu, given the menu bar.

    ``handle_event(event)``
        A method use to handle events, given an Event object.

    ``about()``
        Used in the plugin manager, when a person clicks on the 'About' button.

    """
    log.info(u'loaded')

    def __init__(self, name, default_settings, media_item_class=None, settings_tab_class=None, version=None):
        """
        This is the constructor for the plugin object. This provides an easy
        way for descendent plugins to populate common data. This method *must*
        be overridden, like so::

            class MyPlugin(Plugin):
                def __init__(self):
                    Plugin.__init__(self, u'MyPlugin', version=u'0.1')

        ``name``
            Defaults to *None*. The name of the plugin.

        ``default_settings``
            A dict containing the plugin's settings. The value to each key is the default value to be used.

        ``media_item_class``
            The class name of the plugin's media item.

        ``settings_tab_class``
            The class name of the plugin's settings tab.

        ``version``
            Defaults to *None*, which means that the same version number is used as OpenLP's version number.
        """
        log.debug(u'Plugin %s initialised' % name)
        QtCore.QObject.__init__(self)
        self.name = name
        self.textStrings = {}
        self.setPluginTextStrings()
        self.nameStrings = self.textStrings[StringContent.Name]
        if version:
            self.version = version
        else:
            self.version = get_application_version()[u'version']
        self.settingsSection = self.name
        self.icon = None
        self.mediaItemClass = media_item_class
        self.settingsTabClass = settings_tab_class
        self.settingsTab = None
        self.mediaItem = None
        self.weight = 0
        self.status = PluginStatus.Inactive
        # Add the default status to the default settings.
        default_settings[name + u'/status'] = PluginStatus.Inactive
        default_settings[name + u'/last directory'] = u''
        # Append a setting for files in the mediamanager (note not all plugins
        # which have a mediamanager need this).
        if media_item_class is not None:
            default_settings[u'%s/%s files' % (name, name)] = []
        # Add settings to the dict of all settings.
        Settings.extend_default_settings(default_settings)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'%s_add_service_item' % self.name),
            self.processAddServiceEvent)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'%s_config_updated' % self.name),
            self.configUpdated)

    def checkPreConditions(self):
        """
        Provides the Plugin with a handle to check if it can be loaded.
        Failing Preconditions does not stop a settings Tab being created

        Returns ``True`` or ``False``.
        """
        return True

    def setStatus(self):
        """
        Sets the status of the plugin
        """
        self.status = Settings().value(self.settingsSection + u'/status')

    def toggleStatus(self, new_status):
        """
        Changes the status of the plugin and remembers it
        """
        self.status = new_status
        Settings().setValue(self.settingsSection + u'/status', self.status)
        if new_status == PluginStatus.Active:
            self.initialise()
        elif new_status == PluginStatus.Inactive:
            self.finalise()

    def isActive(self):
        """
        Indicates if the plugin is active

        Returns True or False.
        """
        return self.status == PluginStatus.Active

    def createMediaManagerItem(self):
        """
        Construct a MediaManagerItem object with all the buttons and things
        you need, and return it for integration into OpenLP.
        """
        if self.mediaItemClass:
            self.mediaItem = self.mediaItemClass(self.main_window.mediaDockManager.media_dock, self, self.icon)

    def addImportMenuItem(self, importMenu):
        """
        Create a menu item and add it to the "Import" menu.

        ``importMenu``
            The Import menu.
        """
        pass

    def addExportMenuItem(self, exportMenu):
        """
        Create a menu item and add it to the "Export" menu.

        ``exportMenu``
            The Export menu
        """
        pass

    def addToolsMenuItem(self, toolsMenu):
        """
        Create a menu item and add it to the "Tools" menu.

        ``toolsMenu``
            The Tools menu
        """
        pass

    def createSettingsTab(self, parent):
        """
        Create a tab for the settings window to display the configurable options
        for this plugin to the user.
        """
        if self.settingsTabClass:
            self.settingsTab = self.settingsTabClass(parent, self.name,
                self.getString(StringContent.VisibleName)[u'title'], self.iconPath)

    def addToMenu(self, menubar):
        """
        Add menu items to the menu, given the menubar.

        ``menubar``
            The application's menu bar.
        """
        pass

    def processAddServiceEvent(self, replace=False):
        """
        Generic Drag and drop handler triggered from service_manager.
        """
        log.debug(u'processAddServiceEvent event called for plugin %s' % self.name)
        if replace:
            self.mediaItem.onAddEditClick()
        else:
            self.mediaItem.onAddClick()

    def about(self):
        """
        Show a dialog when the user clicks on the 'About' button in the plugin
        manager.
        """
        raise NotImplementedError(u'Plugin.about needs to be defined by the plugin')

    def initialise(self):
        """
        Called by the plugin Manager to initialise anything it needs.
        """
        if self.mediaItem:
            self.mediaItem.initialise()
            self.main_window.mediaDockManager.insert_dock(self.mediaItem, self.icon, self.weight)

    def finalise(self):
        """
        Called by the plugin Manager to cleanup things.
        """
        if self.mediaItem:
            self.main_window.mediaDockManager.remove_dock(self.mediaItem)

    def app_startup(self):
        """
        Perform tasks on application startup
        """
        # FIXME: Remove after 2.2 release.
        # This is needed to load the list of images/media/presentation from the config saved
        # before the settings rewrite.
        if self.mediaItemClass is not None:
            # We need QSettings instead of Settings here to bypass our central settings dict.
            # Do NOT do this anywhere else!
            settings = QtCore.QSettings()
            settings.beginGroup(self.settingsSection)
            if settings.contains(u'%s count' % self.name):
                list_count = int(settings.value(u'%s count' % self.name, 0))
                loaded_list = []
                if list_count:
                    for counter in range(list_count):
                        item = settings.value(u'%s %d' % (self.name, counter), u'')
                        if item:
                            loaded_list.append(item)
                        settings.remove(u'%s %d' % (self.name, counter))
                settings.remove(u'%s count' % self.name)
                # Now save the list to the config using our Settings class.
                Settings().setValue(u'%s/%s files' % (self.settingsSection, self.name), loaded_list)
            settings.endGroup()

    def usesTheme(self, theme):
        """
        Called to find out if a plugin is currently using a theme.

        Returns True if the theme is being used, otherwise returns False.
        """
        return False

    def renameTheme(self, oldTheme, newTheme):
        """
        Renames a theme a plugin is using making the plugin use the new name.

        ``oldTheme``
            The name of the theme the plugin should stop using.

        ``newTheme``
            The new name the plugin should now use.
        """
        pass

    def getString(self, name):
        """
        encapsulate access of plugins translated text strings
        """
        return self.textStrings[name]

    def setPluginUiTextStrings(self, tooltips):
        """
        Called to define all translatable texts of the plugin
        """
        ## Load Action ##
        self.__setNameTextString(StringContent.Load, UiStrings().Load, tooltips[u'load'])
        ## Import Action ##
        self.__setNameTextString(StringContent.Import, UiStrings().Import, tooltips[u'import'])
        ## New Action ##
        self.__setNameTextString(StringContent.New, UiStrings().Add, tooltips[u'new'])
        ## Edit Action ##
        self.__setNameTextString(StringContent.Edit, UiStrings().Edit, tooltips[u'edit'])
        ## Delete Action ##
        self.__setNameTextString(StringContent.Delete, UiStrings().Delete, tooltips[u'delete'])
        ## Preview Action ##
        self.__setNameTextString(StringContent.Preview, UiStrings().Preview, tooltips[u'preview'])
        ## Send Live Action ##
        self.__setNameTextString(StringContent.Live, UiStrings().Live, tooltips[u'live'])
        ## Add to Service Action ##
        self.__setNameTextString(StringContent.Service, UiStrings().Service, tooltips[u'service'])

    def __setNameTextString(self, name, title, tooltip):
        """
        Utility method for creating a plugin's textStrings. This method makes
        use of the singular name of the plugin object so must only be called
        after this has been set.
        """
        self.textStrings[name] = {u'title': title, u'tooltip': tooltip}

    def getDisplayCss(self):
        """
        Add css style sheets to htmlbuilder.
        """
        return u''

    def getDisplayJavaScript(self):
        """
        Add javascript functions to htmlbuilder.
        """
        return u''

    def refreshCss(self, frame):
        """
        Allow plugins to refresh javascript on displayed screen.

        ``frame``
            The Web frame holding the page.
        """
        return u''

    def getDisplayHtml(self):
        """
        Add html code to htmlbuilder.
        """
        return u''

    def configUpdated(self):
        """
        The plugin's config has changed
        """
        pass

    def new_service_created(self):
        """
        The plugin's needs to handle a new song creation
        """
        pass

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, u'_main_window'):
            self._main_window = Registry().get(u'main_window')
        return self._main_window

    main_window = property(_get_main_window)

    def _get_application(self):
        """
        Adds the openlp to the class dynamically
        """
        if not hasattr(self, u'_application'):
            self._application = Registry().get(u'application')
        return self._application

    application = property(_get_application)
