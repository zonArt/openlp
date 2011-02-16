# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
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
Provide the generic plugin functionality for OpenLP plugins.
"""
import logging

from PyQt4 import QtCore

from openlp.core.lib import Receiver
from openlp.core.lib.ui import UiStrings

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

    ``getMediaManagerItem()``
        Returns an instance of MediaManagerItem to be used in the Media Manager.

    ``addImportMenuItem(import_menu)``
        Add an item to the Import menu.

    ``addExportMenuItem(export_menu)``
        Add an item to the Export menu.

    ``getSettingsTab()``
        Returns an instance of SettingsTabItem to be used in the Settings
        dialog.

    ``addToMenu(menubar)``
        A method to add a menu item to anywhere in the menu, given the menu bar.

    ``handle_event(event)``
        A method use to handle events, given an Event object.

    ``about()``
        Used in the plugin manager, when a person clicks on the 'About' button.

    """
    log.info(u'loaded')

    def __init__(self, name, version=None, pluginHelpers=None,
        mediaItemClass=None, settingsTabClass=None):
        """
        This is the constructor for the plugin object. This provides an easy
        way for descendent plugins to populate common data. This method *must*
        be overridden, like so::

            class MyPlugin(Plugin):
                def __init__(self):
                    Plugin.__init__(self, u'MyPlugin', u'0.1')

        ``name``
            Defaults to *None*. The name of the plugin.

        ``version``
            Defaults to *None*. The version of the plugin.

        ``pluginHelpers``
            Defaults to *None*. A list of helper objects.

        ``mediaItemClass``
            The class name of the plugin's media item.

        ``settingsTabClass``
            The class name of the plugin's settings tab.
        """
        QtCore.QObject.__init__(self)
        self.name = name
        self.textStrings = {}
        self.setPluginTextStrings()
        self.nameStrings = self.textStrings[StringContent.Name]
        if version:
            self.version = version
        self.settingsSection = self.name.lower()
        self.icon = None
        self.mediaItemClass = mediaItemClass
        self.settingsTabClass = settingsTabClass
        self.weight = 0
        self.status = PluginStatus.Inactive
        # Set up logging
        self.log = logging.getLogger(self.name)
        self.previewController = pluginHelpers[u'preview']
        self.liveController = pluginHelpers[u'live']
        self.renderManager = pluginHelpers[u'render']
        self.serviceManager = pluginHelpers[u'service']
        self.settingsForm = pluginHelpers[u'settings form']
        self.mediadock = pluginHelpers[u'toolbox']
        self.pluginManager = pluginHelpers[u'pluginmanager']
        self.formparent = pluginHelpers[u'formparent']
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_add_service_item' % self.name),
            self.processAddServiceEvent)

    def checkPreConditions(self):
        """
        Provides the Plugin with a handle to check if it can be loaded.
        Failing Preconditions does not stop a settings Tab being created

        Returns True or False.
        """
        return True

    def setStatus(self):
        """
        Sets the status of the plugin
        """
        self.status = QtCore.QSettings().value(
            self.settingsSection + u'/status',
            QtCore.QVariant(PluginStatus.Inactive)).toInt()[0]

    def toggleStatus(self, new_status):
        """
        Changes the status of the plugin and remembers it
        """
        self.status = new_status
        QtCore.QSettings().setValue(
            self.settingsSection + u'/status', QtCore.QVariant(self.status))
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

    def getMediaManagerItem(self):
        """
        Construct a MediaManagerItem object with all the buttons and things
        you need, and return it for integration into openlp.org.
        """
        if self.mediaItemClass:
            return self.mediaItemClass(self, self, self.icon)
        return None

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

    def getSettingsTab(self):
        """
        Create a tab for the settings window to display the configurable
        options for this plugin to the user.
        """
        if self.settingsTabClass:
            return self.settingsTabClass(self.name,
                self.getString(StringContent.VisibleName)[u'title'])
        return None

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
        log.debug(u'processAddServiceEvent event called for plugin %s' %
            self.name)
        if replace:
            self.mediaItem.onAddEditClick()
        else:
            self.mediaItem.onAddClick()

    def about(self):
        """
        Show a dialog when the user clicks on the 'About' button in the plugin
        manager.
        """
        raise NotImplementedError(
            u'Plugin.about needs to be defined by the plugin')

    def initialise(self):
        """
        Called by the plugin Manager to initialise anything it needs.
        """
        if self.mediaItem:
            self.mediaItem.initialise()
        self.insertToolboxItem()

    def finalise(self):
        """
        Called by the plugin Manager to cleanup things.
        """
        self.removeToolboxItem()

    def removeToolboxItem(self):
        """
        Called by the plugin to remove toolbar
        """
        if self.mediaItem:
            self.mediadock.remove_dock(self.mediaItem)
        if self.settings_tab:
            self.settingsForm.removeTab(self.settings_tab)

    def insertToolboxItem(self):
        """
        Called by plugin to replace toolbar
        """
        if self.mediaItem:
            self.mediadock.insert_dock(self.mediaItem, self.icon, self.weight)
        if self.settings_tab:
            self.settingsForm.insertTab(self.settings_tab, self.weight)

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
        self.__setNameTextString(StringContent.Load,
            UiStrings.Load, tooltips[u'load'])
        ## Import Action ##
        self.__setNameTextString(StringContent.Import,
            UiStrings.Import, tooltips[u'import'])
        ## New Action ##
        self.__setNameTextString(StringContent.New,
            UiStrings.Add, tooltips[u'new'])
        ## Edit Action ##
        self.__setNameTextString(StringContent.Edit,
            UiStrings.Edit, tooltips[u'edit'])
        ## Delete Action ##
        self.__setNameTextString(StringContent.Delete,
            UiStrings.Delete, tooltips[u'delete'])
        ## Preview Action ##
        self.__setNameTextString(StringContent.Preview,
            UiStrings.Preview, tooltips[u'preview'])
        ## Send Live Action ##
        self.__setNameTextString(StringContent.Live,
            UiStrings.Live, tooltips[u'live'])
        ## Add to Service Action ##
        self.__setNameTextString(StringContent.Service,
            UiStrings.Service, tooltips[u'service'])

    def __setNameTextString(self, name, title, tooltip):
        """
        Utility method for creating a plugin's textStrings. This method makes
        use of the singular name of the plugin object so must only be called
        after this has been set.
        """
        self.textStrings[name] = {u'title': title, u'tooltip': tooltip}
