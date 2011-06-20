# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

def translate(context, text, comment=None,
    encoding=QtCore.QCoreApplication.CodecForTr, n=-1,
    translate=QtCore.QCoreApplication.translate):
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
    return translate(context, text, comment, encoding, n)

def get_text_file_string(text_file):
    """
    Open a file and return its content as unicode string. If the supplied file
    name is not a file then the function returns False. If there is an error
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

def create_thumb(image_path, thumb_path, return_icon=True, size=None):
    """
    Create a thumbnail from the given image path and depending on
    ``return_icon`` it returns an icon from this thumb.

    ``image_path``
        The image file to create the icon from.

    ``thumb_path``
        The filename to save the thumbnail to.

    ``return_icon``
        States if an icon should be build and returned from the thumb. Defaults
        to ``True``.

    ``size``
        Defaults to ``None``.
    """
    ext = os.path.splitext(thumb_path)[1].lower()
    reader = QtGui.QImageReader(image_path)
    if size is None:
        ratio = float(reader.size().width()) / float(reader.size().height())
        reader.setScaledSize(QtCore.QSize(int(ratio * 88), 88))
    else:
        reader.setScaledSize(size)
    thumb = reader.read()
    thumb.save(thumb_path, ext[1:])
    if not return_icon:
        return
    if os.path.exists(thumb_path):
        return build_icon(unicode(thumb_path))
    # Fallback for files with animation support.
    return build_icon(unicode(image_path))

def validate_thumb(file_path, thumb_path):
    """
    Validates whether an file's thumb still exists and if is up to date.
    **Note**, you must **not** call this function, before checking the
    existence of the file.

    ``file_path``
        The path to the file. The file **must** exist!

    ``thumb_path``
        The path to the thumb.
    """
    if not os.path.exists(unicode(thumb_path)):
        return False
    image_date = os.stat(unicode(file_path)).st_mtime
    thumb_date = os.stat(unicode(thumb_path)).st_mtime
    return image_date <= thumb_date

def resize_image(image_path, width, height, background=QtCore.Qt.black):
    """
    Resize an image to fit on the current screen.

    ``image_path``
        The path to the image to resize.

    ``width``
        The new image width.

    ``height``
        The new image height.

    ``background``
        The background colour. Defaults to ``QtCore.Qt.black``.
    """
    log.debug(u'resize_image - start')
    reader = QtGui.QImageReader(image_path)
    # The image's ratio.
    image_ratio = float(reader.size().width()) / float(reader.size().height())
    resize_ratio = float(width) / float(height)
    # Figure out the size we want to resize the image to (keep aspect ratio).
    if image_ratio == resize_ratio:
        size = QtCore.QSize(width, height)
    elif image_ratio < resize_ratio:
        # Use the image's height as reference for the new size.
        size = QtCore.QSize(image_ratio * height, height)
    else:
        # Use the image's width as reference for the new size.
        size = QtCore.QSize(width, 1 / (image_ratio / width))
    reader.setScaledSize(size)
    preview = reader.read()
    if image_ratio == resize_ratio:
        # We neither need to centre the image nor add "bars" to the image.
        return preview
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
    text = text.replace(u'{br}', u'\n')
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
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except IOError:
        pass

from listwidgetwithdnd import ListWidgetWithDnD
from displaytags import DisplayTags
from eventreceiver import Receiver
from spelltextedit import SpellTextEdit
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
from imagemanager import ImageManager
from renderer import Renderer
from mediamanageritem import MediaManagerItem
from openlp.core.utils.actions import ActionList
