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
The :mod:`lib` module contains most of the components and libraries that make
OpenLP work.
"""
import logging
import os.path
import types

from PyQt4 import QtCore, QtGui

log = logging.getLogger(__name__)

base_html_expands = []

base_html_expands.append({u'desc': u'Red', u'start tag': u'{r}',
    u'start html': u'<span style="-webkit-text-fill-color:red">',
    u'end tag': u'{/r}', u'end html': u'</span>', u'protected': True})
base_html_expands.append({u'desc': u'Black', u'start tag': u'{b}',
    u'start html': u'<span style="-webkit-text-fill-color:black">',
    u'end tag': u'{/b}', u'end html': u'</span>', u'protected': True})
base_html_expands.append({u'desc': u'Blue', u'start tag': u'{bl}',
    u'start html': u'<span style="-webkit-text-fill-color:blue">',
    u'end tag': u'{/bl}', u'end html': u'</span>', u'protected': True})
base_html_expands.append({u'desc': u'Yellow', u'start tag': u'{y}',
    u'start html': u'<span style="-webkit-text-fill-color:yellow">',
    u'end tag': u'{/y}', u'end html': u'</span>', u'protected': True})
base_html_expands.append({u'desc': u'Green', u'start tag': u'{g}',
    u'start html': u'<span style="-webkit-text-fill-color:green">',
    u'end tag': u'{/g}', u'end html': u'</span>', u'protected': True})
base_html_expands.append({u'desc': u'Pink', u'start tag': u'{pk}',
    u'start html': u'<span style="-webkit-text-fill-color:#CC33CC">',
    u'end tag': u'{/pk}', u'end html': u'</span>', u'protected': True})
base_html_expands.append({u'desc': u'Orange', u'start tag': u'{o}',
    u'start html': u'<span style="-webkit-text-fill-color:#CC0033">',
    u'end tag': u'{/o}', u'end html': u'</span>', u'protected': True})
base_html_expands.append({u'desc': u'Purple', u'start tag': u'{pp}',
    u'start html': u'<span style="-webkit-text-fill-color:#9900FF">',
    u'end tag': u'{/pp}', u'end html': u'</span>', u'protected': True})
base_html_expands.append({u'desc': u'White', u'start tag': u'{w}',
    u'start html': u'<span style="-webkit-text-fill-color:white">',
    u'end tag': u'{/w}', u'end html': u'</span>', u'protected': True})
base_html_expands.append({u'desc': u'Superscript', u'start tag': u'{su}',
    u'start html': u'<sup>', u'end tag': u'{/su}', u'end html': u'</sup>',
    u'protected': True})
base_html_expands.append({u'desc': u'Subscript', u'start tag': u'{sb}',
    u'start html': u'<sub>', u'end tag': u'{/sb}', u'end html': u'</sub>',
    u'protected': True})
base_html_expands.append({u'desc': u'Paragraph', u'start tag': u'{p}',
    u'start html': u'<p>', u'end tag': u'{/p}', u'end html': u'</p>',
    u'protected': True})
base_html_expands.append({u'desc': u'Bold', u'start tag': u'{st}',
    u'start html': u'<strong>', u'end tag': u'{/st}', u'end html': u'</strong>',
    u'protected': True})
base_html_expands.append({u'desc': u'Italics', u'start tag': u'{it}',
    u'start html': u'<em>', u'end tag': u'{/it}', u'end html': u'</em>',
    u'protected': True})
base_html_expands.append({u'desc': u'Underline', u'start tag': u'{u}',
    u'start html': u'<span style="text-decoration: underline;">',
    u'end tag': u'{/u}', u'end html': u'</span>', u'protected': True})

def translate(context, text, comment=None,
    encoding=QtCore.QCoreApplication.CodecForTr, n=-1):
    """
    A special shortcut method to wrap around the Qt4 translation functions.
    This abstracts the translation procedure so that we can change it if at a
    later date if necessary, without having to redo the whole of OpenLP.

    ``context``
        The translation context, used to give each string a context or a
        namespace.

    ``text``
        The text to put into the translation tables for translation.

    ``comment``
        An identifying string for when the same text is used in different roles
        within the same context.
    """
    return QtCore.QCoreApplication.translate(
        context, text, comment, encoding, n)

def get_text_file_string(text_file):
    """
    Open a file and return its content as unicode string.  If the supplied file
    name is not a file then the function returns False.  If there is an error
    loading the file or the content can't be decoded then the function will
    return None.

    ``textfile``
        The name of the file.
    """
    if not os.path.isfile(text_file):
        return False
    file_handle = None
    content_string = None
    try:
        file_handle = open(text_file, u'r')
        content = file_handle.read()
        content_string = content.decode(u'utf-8')
    except (IOError, UnicodeError):
        log.exception(u'Failed to open text file %s' % text_file)
    finally:
        if file_handle:
            file_handle.close()
    return content_string

def str_to_bool(stringvalue):
    """
    Convert a string version of a boolean into a real boolean.

    ``stringvalue``
        The string value to examine and convert to a boolean type.
    """
    if isinstance(stringvalue, bool):
        return stringvalue
    return unicode(stringvalue).strip().lower() in (u'true', u'yes', u'y')

def build_icon(icon):
    """
    Build a QIcon instance from an existing QIcon, a resource location, or a
    physical file location. If the icon is a QIcon instance, that icon is
    simply returned. If not, it builds a QIcon instance from the resource or
    file name.

    ``icon``
        The icon to build. This can be a QIcon, a resource string in the form
        ``:/resource/file.png``, or a file location like ``/path/to/file.png``.
    """
    button_icon = QtGui.QIcon()
    if isinstance(icon, QtGui.QIcon):
        button_icon = icon
    elif isinstance(icon, basestring):
        if icon.startswith(u':/'):
            button_icon.addPixmap(QtGui.QPixmap(icon), QtGui.QIcon.Normal,
                QtGui.QIcon.Off)
        else:
            button_icon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(icon)),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
    elif isinstance(icon, QtGui.QImage):
        button_icon.addPixmap(QtGui.QPixmap.fromImage(icon),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
    return button_icon

def context_menu_action(base, icon, text, slot):
    """
    Utility method to help build context menus for plugins

    ``base``
        The parent menu to add this menu item to

    ``icon``
        An icon for this action

    ``text``
        The text to display for this action

    ``slot``
        The code to run when this action is triggered
    """
    action = QtGui.QAction(text, base)
    if icon:
        action.setIcon(build_icon(icon))
    QtCore.QObject.connect(action, QtCore.SIGNAL(u'triggered()'), slot)
    return action

def context_menu(base, icon, text):
    """
    Utility method to help build context menus for plugins

    ``base``
        The parent object to add this menu to

    ``icon``
        An icon for this menu

    ``text``
        The text to display for this menu
    """
    action = QtGui.QMenu(text, base)
    action.setIcon(build_icon(icon))
    return action

def context_menu_separator(base):
    """
    Add a separator to a context menu

    ``base``
        The menu object to add the separator to
    """
    action = QtGui.QAction(u'', base)
    action.setSeparator(True)
    return action

def image_to_byte(image):
    """
    Resize an image to fit on the current screen for the web and returns
    it as a byte stream.

    ``image``
        The image to converted.
    """
    log.debug(u'image_to_byte - start')
    byte_array = QtCore.QByteArray()
    # use buffer to store pixmap into byteArray
    buffie = QtCore.QBuffer(byte_array)
    buffie.open(QtCore.QIODevice.WriteOnly)
    image.save(buffie, "PNG")
    log.debug(u'image_to_byte - end')
    # convert to base64 encoding so does not get missed!
    return byte_array.toBase64()

def resize_image(image, width, height, background=QtCore.Qt.black):
    """
    Resize an image to fit on the current screen.

    ``image``
        The image to resize.

    ``width``
        The new image width.

    ``height``
        The new image height.

     ``background``
        The background colour defaults to black.

    """
    log.debug(u'resize_image - start')
    if isinstance(image, QtGui.QImage):
        preview = image
    else:
        preview = QtGui.QImage(image)
    if not preview.isNull():
        # Only resize if different size
        if preview.width() == width and preview.height == height:
            return preview
        preview = preview.scaled(width, height, QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
    realw = preview.width()
    realh = preview.height()
    # and move it to the centre of the preview space
    new_image = QtGui.QImage(width, height,
        QtGui.QImage.Format_ARGB32_Premultiplied)
    painter = QtGui.QPainter(new_image)
    painter.fillRect(new_image.rect(), background)
    painter.drawImage((width - realw) / 2, (height - realh) / 2, preview)
    return new_image

def check_item_selected(list_widget, message):
    """
    Check if a list item is selected so an action may be performed on it

    ``list_widget``
        The list to check for selected items

    ``message``
        The message to give the user if no item is selected
    """
    if not list_widget.selectedIndexes():
        QtGui.QMessageBox.information(list_widget.parent(),
            translate('OpenLP.MediaManagerItem', 'No Items Selected'), message)
        return False
    return True

def clean_tags(text):
    """
    Remove Tags from text for display
    """
    text = text.replace(u'<br>', u'\n')
    text = text.replace(u'&nbsp;', u' ')
    for tag in DisplayTags.get_html_tags():
        text = text.replace(tag[u'start tag'], u'')
        text = text.replace(tag[u'end tag'], u'')
    return text

def expand_tags(text):
    """
    Expand tags HTML for display
    """
    for tag in DisplayTags.get_html_tags():
        text = text.replace(tag[u'start tag'], tag[u'start html'])
        text = text.replace(tag[u'end tag'], tag[u'end html'])
    return text

def check_directory_exists(dir):
    """
    Check a theme directory exists and if not create it

    ``dir``
        Theme directory to make sure exists
    """
    log.debug(u'check_directory_exists %s' % dir)
    if not os.path.exists(dir):
        os.makedirs(dir)

from baselistwithdnd import BaseListWithDnD
from theme import ThemeLevel, ThemeXML, BackgroundGradientType, \
    BackgroundType, HorizontalType, VerticalType
from displaytags import DisplayTags
from spelltextedit import SpellTextEdit
from eventreceiver import Receiver
from imagemanager import ImageManager
from settingsmanager import SettingsManager
from plugin import PluginStatus, StringContent, Plugin
from pluginmanager import PluginManager
from settingstab import SettingsTab
from serviceitem import ServiceItem
from serviceitem import ServiceItemType
from serviceitem import ItemCapabilities
from htmlbuilder import build_html, build_lyrics_format_css, \
    build_lyrics_outline_css
from toolbar import OpenLPToolbar
from dockwidget import OpenLPDockWidget
from renderer import Renderer
from rendermanager import RenderManager
from mediamanageritem import MediaManagerItem
