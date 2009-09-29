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

"""
The :mod:`lib` module contains most of the components and libraries that make
OpenLP work.
"""

import types

from PyQt4 import QtCore, QtGui

def translate(context, text):
    """
    A special shortcut method to wrap around the Qt4 translation functions.
    This abstracts the translation procedure so that we can change it if at a
    later date if necessary, without having to redo the whole of OpenLP.

    ``context``
        The translation context, used to give each string a context or a
        namespace.

    ``text``
        The text to put into the translation tables for translation.
    """
    return QtGui.QApplication.translate(
        context, text, None, QtGui.QApplication.UnicodeUTF8)

def file_to_xml(xmlfile):
    """
    Open a file and return the contents of the file.

    ``xmlfile``
        The name of the file.
    """
    return open(xmlfile).read()

def str_to_bool(stringvalue):
    """
    Convert a string version of a boolean into a real boolean.

    ``stringvalue``
        The string value to examine and convert to a boolean type.
    """
    if stringvalue is True or stringvalue is False:
        return stringvalue
    return stringvalue.strip().lower() in (u'true', u'yes', u'y')

def buildIcon(icon):
    """
    Build a QIcon instance from an existing QIcon, a resource location, or a
    physical file location. If the icon is a QIcon instance, that icon is
    simply returned. If not, it builds a QIcon instance from the resource or
    file name.

    ``icon``
        The icon to build. This can be a QIcon, a resource string in the form
        ``:/resource/file.png``, or a file location like ``/path/to/file.png``.
    """
    ButtonIcon = None
    if type(icon) is QtGui.QIcon:
        ButtonIcon = icon
    elif type(icon) is types.StringType or type(icon) is types.UnicodeType:
        ButtonIcon = QtGui.QIcon()
        if icon.startswith(u':/'):
            ButtonIcon.addPixmap(
                QtGui.QPixmap(icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            ButtonIcon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(icon)),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
    elif type(icon) is QtGui.QImage:
        ButtonIcon = QtGui.QIcon()
        ButtonIcon.addPixmap(
            QtGui.QPixmap.fromImage(icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    return ButtonIcon

def contextMenuAction(base, icon, text, slot):
    """
    Utility method to help build context menus for plugins
    """
    action = QtGui.QAction(text, base)
    action.setIcon(buildIcon(icon))
    QtCore.QObject.connect(action, QtCore.SIGNAL(u'triggered()'), slot)
    return action

def contextMenuSeparator(base):
    action = QtGui.QAction("", base)
    action.setSeparator(True)
    return action

from eventreceiver import Receiver
from settingsmanager import SettingsManager
from pluginconfig import PluginConfig
from plugin import PluginStatus, Plugin
from pluginmanager import PluginManager
from settingstab import SettingsTab
from mediamanageritem import MediaManagerItem
from xmlrootclass import XmlRootClass
from serviceitem import ServiceItem
from serviceitem import ServiceType
from serviceitem import ServiceItem
from toolbar import OpenLPToolbar
from dockwidget import OpenLPDockWidget
from songxmlhandler import SongXMLBuilder, SongXMLParser
from themexmlhandler import ThemeXML
from renderer import Renderer
from rendermanager import RenderManager
from mediamanageritem import MediaManagerItem
from baselistwithdnd import BaseListWithDnD

__all__ = [ 'translate', 'file_to_xml', 'str_to_bool',
            'contextMenuAction', 'contextMenuSeparator','ServiceItem']
