# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import types
from PyQt4 import QtCore, QtGui

def translate(context, text):
    return QtGui.QApplication.translate(context, text, None, QtGui.QApplication.UnicodeUTF8)

def file_to_xml(xmlfile):
    return open(xmlfile).read()

def str_to_bool(stringvalue):
    return stringvalue.strip().lower() in (u'true', u'yes', u'y')

def buildIcon(icon):
    ButtonIcon = None
    if type(icon) is QtGui.QIcon:
        ButtonIcon = icon
    elif type(icon) is types.StringType or type(icon) is types.UnicodeType:
        ButtonIcon = QtGui.QIcon()
        if icon.startswith(u':/'):
            ButtonIcon.addPixmap(QtGui.QPixmap(icon), QtGui.QIcon.Normal,
                QtGui.QIcon.Off)
        else:
            ButtonIcon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(icon)),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
    return ButtonIcon

def contextMenuAction(base, icon, text, slot):
    """
    Utility method to help build context menus for plugins
    """
    action = QtGui.QAction(text, base)
    action .setIcon(buildIcon(icon))
    QtCore.QObject.connect(action, QtCore.SIGNAL(u'triggered()'), slot)
    return action

def contextMenuSeparator(base):
    action = QtGui.QAction("", base)
    action.setSeparator(True)
    return action

from settingsmanager import SettingsManager
from pluginconfig import PluginConfig
from plugin import Plugin
from eventmanager import EventManager
from pluginmanager import PluginManager
from settingstab import SettingsTab
from mediamanageritem import MediaManagerItem
from event import Event
from event import EventType
from xmlrootclass import XmlRootClass
from serviceitem import ServiceItem
from eventreceiver import Receiver
from serviceitem import ServiceItem
from toolbar import OpenLPToolbar
from songxmlhandler import SongXMLBuilder
from songxmlhandler import SongXMLParser
from themexmlhandler import ThemeXML
from renderer import Renderer
from rendermanager import RenderManager
from mediamanageritem import MediaManagerItem
from baselistwithdnd import BaseListWithDnD
from listwithpreviews import ListWithPreviews

__all__ = [ 'translate', 'file_to_xml', 'str_to_bool',
            'contextMenuAction', 'contextMenuSeparator','ServiceItem']
