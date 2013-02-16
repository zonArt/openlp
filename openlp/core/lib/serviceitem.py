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
The :mod:`serviceitem` provides the service item functionality including the
type and capability of an item.
"""

import cgi
import datetime
import logging
import os
import uuid

from PyQt4 import QtGui

from openlp.core.lib import ImageSource, Settings, Registry, build_icon, clean_tags, expand_tags, translate

log = logging.getLogger(__name__)


class ServiceItemType(object):
    """
    Defines the type of service item
    """
    Text = 1
    Image = 2
    Command = 3


class ItemCapabilities(object):
    """
    Provides an enumeration of a service item's capabilities

    ``CanPreview``
            The capability to allow the ServiceManager to add to the preview
            tab when making the previous item live.

    ``CanEdit``
            The capability to allow the ServiceManager to allow the item to be
             edited

    ``CanMaintain``
            The capability to allow the ServiceManager to allow the item to be
             reordered.

    ``RequiresMedia``
            Determines is the serviceItem needs a Media Player

    ``CanLoop``
            The capability to allow the SlideController to allow the loop
            processing.

    ``CanAppend``
            The capability to allow the ServiceManager to add leaves to the
            item

    ``NoLineBreaks``
            The capability to remove lines breaks in the renderer

    ``OnLoadUpdate``
            The capability to update MediaManager when a service Item is
            loaded.

    ``AddIfNewItem``
            Not Used

    ``ProvidesOwnDisplay``
            The capability to tell the SlideController the service Item has a
            different display.

    ``HasDetailedTitleDisplay``
            ServiceItem provides a title

    ``HasVariableStartTime``
            The capability to tell the ServiceManager that a change to start
            time is possible.

    ``CanSoftBreak``
            The capability to tell the renderer that Soft Break is allowed

    ``CanWordSplit``
            The capability to tell the renderer that it can split words is
            allowed

    ``HasBackgroundAudio``
            That a audio file is present with the text.

    ``CanAutoStartForLive``
            The capability to ignore the do not play if display blank flag.

    """
    CanPreview = 1
    CanEdit = 2
    CanMaintain = 3
    RequiresMedia = 4
    CanLoop = 5
    CanAppend = 6
    NoLineBreaks = 7
    OnLoadUpdate = 8
    AddIfNewItem = 9
    ProvidesOwnDisplay = 10
    HasDetailedTitleDisplay = 11
    HasVariableStartTime = 12
    CanSoftBreak = 13
    CanWordSplit = 14
    HasBackgroundAudio = 15
    CanAutoStartForLive = 16


class ServiceItem(object):
    """
    The service item is a base class for the plugins to use to interact with
    the service manager, the slide controller, and the projection screen
    compositor.
    """
    log.info(u'Service Item created')

    def __init__(self, plugin=None):
        """
        Set up the service item.

        ``plugin``
            The plugin that this service item belongs to.
        """
        if plugin:
            self.name = plugin.name
        self.title = u''
        self.shortname = u''
        self.audit = u''
        self.items = []
        self.iconic_representation = None
        self.raw_footer = []
        self.foot_text = u''
        self.theme = None
        self.service_item_type = None
        self._raw_frames = []
        self._display_frames = []
        self.unique_identifier = 0
        self.notes = u''
        self.from_plugin = False
        self.capabilities = []
        self.is_valid = True
        self.icon = None
        self.themedata = None
        self.main = None
        self.footer = None
        self.bg_image_bytes = None
        self.search_string = u''
        self.data_string = u''
        self.edit_id = None
        self.xml_version = None
        self.start_time = 0
        self.end_time = 0
        self.media_length = 0
        self.from_service = False
        self.image_border = u'#000000'
        self.background_audio = []
        self.theme_overwritten = False
        self.temporary_edit = False
        self.auto_play_slides_once = False
        self.auto_play_slides_loop = False
        self.timed_slide_interval = 0
        self.will_auto_start = False
        self.has_original_files = True
        self._new_item()

    def _new_item(self):
        """
        Method to set the internal id of the item. This is used to compare
        service items to see if they are the same.
        """
        self.unique_identifier = unicode(uuid.uuid1())
        self.validate_item()

    def add_capability(self, capability):
        """
        Add an ItemCapability to a ServiceItem

        ``capability``
            The capability to add
        """
        self.capabilities.append(capability)

    def is_capable(self, capability):
        """
        Tell the caller if a ServiceItem has a capability

        ``capability``
            The capability to test for
        """
        return capability in self.capabilities

    def add_icon(self, icon):
        """
        Add an icon to the service item. This is used when displaying the
        service item in the service manager.

        ``icon``
            A string to an icon in the resources or on disk.
        """
        self.icon = icon
        self.iconic_representation = build_icon(icon)

    def render(self, provides_own_theme_data=False):
        """
        The render method is what generates the frames for the screen and
        obtains the display information from the renderer. At this point all
        slides are built for the given display size.

        ``provides_own_theme_data``
            This switch disables the usage of the item's theme. However, this is
            disabled by default. If this is used, it has to be taken care, that
            the renderer knows the correct theme data. However, this is needed
            for the theme manager.
        """
        log.debug(u'Render called')
        self._display_frames = []
        self.bg_image_bytes = None
        if not provides_own_theme_data:
            self.renderer.set_item_theme(self.theme)
            self.themedata, self.main, self.footer = self.renderer.pre_render()
        if self.service_item_type == ServiceItemType.Text:
            log.debug(u'Formatting slides: %s' % self.title)
            # Save rendered pages to this dict. In the case that a slide is used
            # twice we can use the pages saved to the dict instead of rendering
            # them again.
            previous_pages = {}
            for slide in self._raw_frames:
                verse_tag = slide[u'verseTag']
                if verse_tag in previous_pages and previous_pages[verse_tag][0] == slide[u'raw_slide']:
                    pages = previous_pages[verse_tag][1]
                else:
                    pages = self.renderer.format_slide(slide[u'raw_slide'], self)
                    previous_pages[verse_tag] = (slide[u'raw_slide'], pages)
                for page in pages:
                    page = page.replace(u'<br>', u'{br}')
                    html = expand_tags(cgi.escape(page.rstrip()))
                    self._display_frames.append({
                        u'title': clean_tags(page),
                        u'text': clean_tags(page.rstrip()),
                        u'html': html.replace(u'&amp;nbsp;', u'&nbsp;'),
                        u'verseTag': verse_tag
                    })
        elif self.service_item_type == ServiceItemType.Image or self.service_item_type == ServiceItemType.Command:
            pass
        else:
            log.error(u'Invalid value renderer: %s' % self.service_item_type)
        self.title = clean_tags(self.title)
        # The footer should never be None, but to be compatible with a few
        # nightly builds between 1.9.4 and 1.9.5, we have to correct this to
        # avoid tracebacks.
        if self.raw_footer is None:
            self.raw_footer = []
        self.foot_text = u'<br>'.join(filter(None, self.raw_footer))

    def add_from_image(self, path, title, background=None):
        """
        Add an image slide to the service item.

        ``path``
            The directory in which the image file is located.

        ``title``
            A title for the slide in the service item.
        """
        if background:
            self.image_border = background
        self.service_item_type = ServiceItemType.Image
        self._raw_frames.append({u'title': title, u'path': path})
        self.image_manager.add_image(path, ImageSource.ImagePlugin, self.image_border)
        self._new_item()

    def add_from_text(self, raw_slide, verse_tag=None):
        """
        Add a text slide to the service item.

        ``raw_slide``
            The raw text of the slide.
        """
        if verse_tag:
            verse_tag = verse_tag.upper()
        self.service_item_type = ServiceItemType.Text
        title = raw_slide[:30].split(u'\n')[0]
        self._raw_frames.append({u'title': title, u'raw_slide': raw_slide, u'verseTag': verse_tag})
        self._new_item()

    def add_from_command(self, path, file_name, image):
        """
        Add a slide from a command.

        ``path``
            The title of the slide in the service item.

        ``file_name``
            The title of the slide in the service item.

        ``image``
            The command of/for the slide.
        """
        self.service_item_type = ServiceItemType.Command
        self._raw_frames.append({u'title': file_name, u'image': image, u'path': path})
        self._new_item()

    def get_service_repr(self, lite_save):
        """
        This method returns some text which can be saved into the service
        file to represent this item.
        """
        service_header = {
            u'name': self.name,
            u'plugin': self.name,
            u'theme': self.theme,
            u'title': self.title,
            u'icon': self.icon,
            u'footer': self.raw_footer,
            u'type': self.service_item_type,
            u'audit': self.audit,
            u'notes': self.notes,
            u'from_plugin': self.from_plugin,
            u'capabilities': self.capabilities,
            u'search': self.search_string,
            u'data': self.data_string,
            u'xml_version': self.xml_version,
            u'auto_play_slides_once': self.auto_play_slides_once,
            u'auto_play_slides_loop': self.auto_play_slides_loop,
            u'timed_slide_interval': self.timed_slide_interval,
            u'start_time': self.start_time,
            u'end_time': self.end_time,
            u'media_length': self.media_length,
            u'background_audio': self.background_audio,
            u'theme_overwritten': self.theme_overwritten,
            u'will_auto_start': self.will_auto_start
        }
        service_data = []
        if self.service_item_type == ServiceItemType.Text:
            service_data = [slide for slide in self._raw_frames]
        elif self.service_item_type == ServiceItemType.Image:
            if lite_save:
                for slide in self._raw_frames:
                    service_data.append({u'title': slide[u'title'], u'path': slide[u'path']})
            else:
                service_data = [slide[u'title'] for slide in self._raw_frames]
        elif self.service_item_type == ServiceItemType.Command:
            for slide in self._raw_frames:
                service_data.append({u'title': slide[u'title'], u'image': slide[u'image'], u'path': slide[u'path']})
        return {u'header': service_header, u'data': service_data}

    def set_from_service(self, serviceitem, path=None):
        """
        This method takes a service item from a saved service file (passed
        from the ServiceManager) and extracts the data actually required.

        ``serviceitem``
            The item to extract data from.

        ``path``
            Defaults to *None*. This is the service manager path for things
            which have their files saved with them or None when the saved
            service is lite and the original file paths need to be preserved..
        """
        log.debug(u'set_from_service called with path %s' % path)
        header = serviceitem[u'serviceitem'][u'header']
        self.title = header[u'title']
        self.name = header[u'name']
        self.service_item_type = header[u'type']
        self.shortname = header[u'plugin']
        self.theme = header[u'theme']
        self.add_icon(header[u'icon'])
        self.raw_footer = header[u'footer']
        self.audit = header[u'audit']
        self.notes = header[u'notes']
        self.from_plugin = header[u'from_plugin']
        self.capabilities = header[u'capabilities']
        # Added later so may not be present in older services.
        self.search_string = header.get(u'search', u'')
        self.data_string = header.get(u'data', u'')
        self.xml_version = header.get(u'xml_version')
        self.start_time = header.get(u'start_time', 0)
        self.end_time = header.get(u'end_time', 0)
        self.media_length = header.get(u'media_length', 0)
        self.auto_play_slides_once = header.get(u'auto_play_slides_once', False)
        self.auto_play_slides_loop = header.get(u'auto_play_slides_loop', False)
        self.timed_slide_interval = header.get(u'timed_slide_interval', 0)
        self.will_auto_start = header.get(u'will_auto_start', False)
        self.has_original_files = True
        if u'background_audio' in header:
            self.background_audio = []
            for filename in header[u'background_audio']:
                # Give them real file paths
                self.background_audio.append(os.path.join(path, filename))
        self.theme_overwritten = header.get(u'theme_overwritten', False)
        if self.service_item_type == ServiceItemType.Text:
            for slide in serviceitem[u'serviceitem'][u'data']:
                self._raw_frames.append(slide)
        elif self.service_item_type == ServiceItemType.Image:
            settingsSection = serviceitem[u'serviceitem'][u'header'][u'name']
            background = QtGui.QColor(Settings().value(settingsSection + u'/background color'))
            if path:
                self.has_original_files = False
                for text_image in serviceitem[u'serviceitem'][u'data']:
                    filename = os.path.join(path, text_image)
                    self.add_from_image(filename, text_image, background)
            else:
                for text_image in serviceitem[u'serviceitem'][u'data']:
                    self.add_from_image(text_image[u'path'], text_image[u'title'], background)
        elif self.service_item_type == ServiceItemType.Command:
            for text_image in serviceitem[u'serviceitem'][u'data']:
                if path:
                    self.has_original_files = False
                    self.add_from_command(path, text_image[u'title'], text_image[u'image'])
                else:
                    self.add_from_command(text_image[u'path'], text_image[u'title'], text_image[u'image'])
        self._new_item()

    def get_display_title(self):
        """
        Returns the title of the service item.
        """
        if self.is_text():
            return self.title
        else:
            if ItemCapabilities.HasDetailedTitleDisplay in self.capabilities:
                return self._raw_frames[0][u'title']
            elif len(self._raw_frames) > 1:
                return self.title
            else:
                return self._raw_frames[0][u'title']

    def merge(self, other):
        """
        Updates the unique_identifier with the value from the original one
        The unique_identifier is unique for a given service item but this allows one to
        replace an original version.

        ``other``
            The service item to be merged with
        """
        self.unique_identifier = other.unique_identifier
        self.notes = other.notes
        self.temporary_edit = other.temporary_edit
        # Copy theme over if present.
        if other.theme is not None:
            self.theme = other.theme
            self._new_item()
        self.render()
        if self.is_capable(ItemCapabilities.HasBackgroundAudio):
            log.debug(self.background_audio)

    def __eq__(self, other):
        """
        Confirms the service items are for the same instance
        """
        if not other:
            return False
        return self.unique_identifier == other.unique_identifier

    def __ne__(self, other):
        """
        Confirms the service items are not for the same instance
        """
        return self.unique_identifier != other.unique_identifier

    def is_media(self):
        """
        Confirms if the ServiceItem is media
        """
        return ItemCapabilities.RequiresMedia in self.capabilities

    def is_command(self):
        """
        Confirms if the ServiceItem is a command
        """
        return self.service_item_type == ServiceItemType.Command

    def is_image(self):
        """
        Confirms if the ServiceItem is an image
        """
        return self.service_item_type == ServiceItemType.Image

    def uses_file(self):
        """
        Confirms if the ServiceItem uses a file
        """
        return self.service_item_type == ServiceItemType.Image or self.service_item_type == ServiceItemType.Command

    def is_text(self):
        """
        Confirms if the ServiceItem is text
        """
        return self.service_item_type == ServiceItemType.Text

    def set_media_length(self, length):
        """
        Stores the media length of the item

        ``length``
            The length of the media item
        """
        self.media_length = length
        if length > 0:
            self.add_capability(ItemCapabilities.HasVariableStartTime)

    def get_frames(self):
        """
        Returns the frames for the ServiceItem
        """
        if self.service_item_type == ServiceItemType.Text:
            return self._display_frames
        else:
            return self._raw_frames

    def get_rendered_frame(self, row):
        """
        Returns the correct frame for a given list and renders it if required.
        ``row``
            The service item slide to be returned
        """
        if self.service_item_type == ServiceItemType.Text:
            return self._display_frames[row][u'html'].split(u'\n')[0]
        elif self.service_item_type == ServiceItemType.Image:
            return self._raw_frames[row][u'path']
        else:
            return self._raw_frames[row][u'image']

    def get_frame_title(self, row=0):
        """
        Returns the title of the raw frame
        """
        try:
            return self._raw_frames[row][u'title']
        except IndexError:
            return u''

    def get_frame_path(self, row=0, frame=None):
        """
        Returns the path of the raw frame
        """
        if not frame:
            try:
                frame = self._raw_frames[row]
            except IndexError:
                return u''
        if self.is_image():
            path_from = frame[u'path']
        else:
            path_from = os.path.join(frame[u'path'], frame[u'title'])
        return path_from

    def remove_frame(self, frame):
        """
        Remove the specified frame from the item
        """
        if frame in self._raw_frames:
            self._raw_frames.remove(frame)

    def get_media_time(self):
        """
        Returns the start and finish time for a media item
        """
        start = None
        end = None
        if self.start_time != 0:
            start = translate('OpenLP.ServiceItem', '<strong>Start</strong>: %s') % \
                unicode(datetime.timedelta(seconds=self.start_time))
        if self.media_length != 0:
            end = translate('OpenLP.ServiceItem', '<strong>Length</strong>: %s') % \
                unicode(datetime.timedelta(seconds=self.media_length))
        if not start and not end:
            return u''
        elif start and not end:
            return start
        elif not start and end:
            return end
        else:
            return u'%s <br>%s' % (start, end)

    def update_theme(self, theme):
        """
        updates the theme in the service item

        ``theme``
            The new theme to be replaced in the service item
        """
        self.theme_overwritten = (theme is None)
        self.theme = theme
        self._new_item()
        self.render()

    def remove_invalid_frames(self, invalid_paths=None):
        """
        Remove invalid frames, such as ones where the file no longer exists.
        """
        if self.uses_file():
            for frame in self.get_frames():
                if self.get_frame_path(frame=frame) in invalid_paths:
                    self.remove_frame(frame)

    def missing_frames(self):
        """
        Returns if there are any frames in the service item
        """
        return not bool(self._raw_frames)

    def validate_item(self, suffix_list=None):
        """
        Validates a service item to make sure it is valid
        """
        self.is_valid = True
        for frame in self._raw_frames:
            if self.is_image() and not os.path.exists((frame[u'path'])):
                self.is_valid = False
            elif self.is_command():
                file_name = os.path.join(frame[u'path'], frame[u'title'])
                if not os.path.exists(file_name):
                    self.is_valid = False
                if suffix_list and not self.is_text():
                    file_suffix = frame[u'title'].split(u'.')[-1]
                    if file_suffix.lower() not in suffix_list:
                        self.is_valid = False

    def _get_renderer(self):
        """
        Adds the Renderer to the class dynamically
        """
        if not hasattr(self, u'_renderer'):
            self._renderer = Registry().get(u'renderer')
        return self._renderer

    renderer = property(_get_renderer)

    def _get_image_manager(self):
        """
        Adds the image manager to the class dynamically
        """
        if not hasattr(self, u'_image_manager'):
            self._image_manager = Registry().get(u'image_manager')
        return self._image_manager

    image_manager = property(_get_image_manager)
