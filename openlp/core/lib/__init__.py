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
The :mod:`lib` module contains most of the components and libraries that make
OpenLP work.
"""
import logging
import os

from PyQt4 import QtCore, QtGui, Qt

log = logging.getLogger(__name__)

class ServiceItemContext(object):
    """
    The context in which a Service Item is being generated
    """
    Preview = 0
    Live = 1
    Service = 2


class ImageSource(object):
    """
    This enumeration class represents different image sources. An image sources
    states where an image is used. This enumeration class is need in the context
    of the :class:~openlp.core.lib.imagemanager`.

    ``ImagePlugin``
        This states that an image is being used by the image plugin.

    ``Theme``
        This says, that the image is used by a theme.
    """
    ImagePlugin = 1
    Theme = 2


class MediaType(object):
    """
    An enumeration class for types of media.
    """
    Audio = 1
    Video = 2


class SlideLimits(object):
    """
    Provides an enumeration for behaviour of OpenLP at the end limits of each
    service item when pressing the up/down arrow keys
    """
    End = 1
    Wrap = 2
    Next = 3


class ServiceItemAction(object):
    """
    Provides an enumeration for the required action moving between service
    items by left/right arrow keys
    """
    Previous = 1
    PreviousLastSlide = 2
    Next = 3


def translate(context, text, comment=None, encoding=QtCore.QCoreApplication.CodecForTr, n=-1,
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
        if not file_handle.read(3) == '\xEF\xBB\xBF':
            # no BOM was found
            file_handle.seek(0)
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
            button_icon.addPixmap(QtGui.QPixmap(icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            button_icon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(icon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    elif isinstance(icon, QtGui.QImage):
        button_icon.addPixmap(QtGui.QPixmap.fromImage(icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        Allows to state a own size to use. Defaults to ``None``, which means
        that a default height of 88 is used.
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
    if not os.path.exists(thumb_path):
        return False
    image_date = os.stat(file_path).st_mtime
    thumb_date = os.stat(thumb_path).st_mtime
    return image_date <= thumb_date


def resize_image(image_path, width, height, background=u'#000000'):
    """
    Resize an image to fit on the current screen.

    ``image_path``
        The path to the image to resize.

    ``width``
        The new image width.

    ``height``
        The new image height.

    ``background``
        The background colour. Defaults to black.

    DO NOT REMOVE THE DEFAULT BACKGROUND VALUE!
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
    real_width = preview.width()
    real_height = preview.height()
    # and move it to the centre of the preview space
    new_image = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32_Premultiplied)
    painter = QtGui.QPainter(new_image)
    painter.fillRect(new_image.rect(), QtGui.QColor(background))
    painter.drawImage((width - real_width) / 2, (height - real_height) / 2, preview)
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
    for tag in FormattingTags.get_html_tags():
        text = text.replace(tag[u'start tag'], u'')
        text = text.replace(tag[u'end tag'], u'')
    return text


def expand_tags(text):
    """
    Expand tags HTML for display
    """
    for tag in FormattingTags.get_html_tags():
        text = text.replace(tag[u'start tag'], tag[u'start html'])
        text = text.replace(tag[u'end tag'], tag[u'end html'])
    return text


def check_directory_exists(directory, do_not_log=False):
    """
    Check a theme directory exists and if not create it

    ``directory``
        The directory to make sure exists

    ``do_not_log``
        To not log anything. This is need for the start up, when the log isn't ready.
    """
    if not do_not_log:
        log.debug(u'check_directory_exists %s' % directory)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except IOError:
        pass


def create_separated_list(stringlist):
    """
    Returns a string that represents a join of a list of strings with a
    localized separator. This function corresponds to
    QLocale::createSeparatedList which was introduced in Qt 4.8 and implements
    the algorithm from http://www.unicode.org/reports/tr35/#ListPatterns

    ``stringlist``
        List of unicode strings
    """
    if Qt.PYQT_VERSION_STR >= u'4.9' and Qt.qVersion() >= u'4.8':
        return QtCore.QLocale().createSeparatedList(stringlist)
    if not stringlist:
        return u''
    elif len(stringlist) == 1:
        return stringlist[0]
    elif len(stringlist) == 2:
        return translate('OpenLP.core.lib', '%1 and %2',
            'Locale list separator: 2 items') % (stringlist[0], stringlist[1])
    else:
        merged = translate('OpenLP.core.lib', '%1, and %2',
            u'Locale list separator: end') % (stringlist[-2], stringlist[-1])
        for index in reversed(range(1, len(stringlist) - 2)):
            merged = translate('OpenLP.core.lib', '%1, %2',
            u'Locale list separator: middle') % (stringlist[index], merged)
        return translate('OpenLP.core.lib', '%1, %2',
            u'Locale list separator: start') % (stringlist[0], merged)


from registry import Registry
from uistrings import UiStrings
from eventreceiver import Receiver
from screen import ScreenList
from settings import Settings
from listwidgetwithdnd import ListWidgetWithDnD
from formattingtags import FormattingTags
from spelltextedit import SpellTextEdit
from settingsmanager import SettingsManager
from plugin import PluginStatus, StringContent, Plugin
from pluginmanager import PluginManager
from settingstab import SettingsTab
from serviceitem import ServiceItem, ServiceItemType, ItemCapabilities
from htmlbuilder import build_html, build_lyrics_format_css, build_lyrics_outline_css
from toolbar import OpenLPToolbar
from dockwidget import OpenLPDockWidget
from imagemanager import ImageManager
from renderer import Renderer
from mediamanageritem import MediaManagerItem

