# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
The Media plugin
"""

import logging

from PyQt5 import QtCore

from openlp.core.common import Settings, translate, check_binary
from openlp.core.lib import Plugin, StringContent, build_icon
from openlp.plugins.media.lib import MediaMediaItem, MediaTab


log = logging.getLogger(__name__)


# Some settings starting with "media" are in core, because they are needed for core functionality.
__default_settings__ = {
    'media/media auto start': QtCore.Qt.Unchecked,
    'media/media files': []
}


class MediaPlugin(Plugin):
    """
    The media plugin adds the ability to playback audio and video content.
    """
    log.info('%s MediaPlugin loaded', __name__)

    def __init__(self):
        super(MediaPlugin, self).__init__('media', __default_settings__, MediaMediaItem)
        self.weight = -6
        self.icon_path = ':/plugins/plugin_media.png'
        self.icon = build_icon(self.icon_path)
        # passed with drag and drop messages
        self.dnd_id = 'Media'

    def initialise(self):
        """
        Override the inherited initialise() method in order to upgrade the media before trying to load it
        """
        super().initialise()

    def check_pre_conditions(self):
        """
        Check it we have a valid environment.
        :return: true or false
        """
        log.debug('check_installed Pdf')
        self.mudrawbin = ''
        self.gsbin = ''
        self.also_supports = []
        # Use the user defined program if given
        if Settings().value('presentations/enable_pdf_program'):
            pdf_program = Settings().value('presentations/pdf_program')
            program_type = self.check_binary('mediainfo')
            if program_type == 'gs':
                self.gsbin = pdf_program
            elif program_type == 'mudraw':
                self.mudrawbin = pdf_program
        else:
            # Fallback to autodetection
            application_path = AppLocation.get_directory(AppLocation.AppDir)
            if is_win():
                # for windows we only accept mudraw.exe in the base folder
                application_path = AppLocation.get_directory(AppLocation.AppDir)
                if os.path.isfile(os.path.join(application_path, 'mudraw.exe')):
                    self.mudrawbin = os.path.join(application_path, 'mudraw.exe')
            else:
                DEVNULL = open(os.devnull, 'wb')
                # First try to find mupdf
                self.mudrawbin = which('mudraw')
                # if mupdf isn't installed, fallback to ghostscript
                if not self.mudrawbin:
                    self.gsbin = which('gs')
                # Last option: check if mudraw is placed in OpenLP base folder
                if not self.mudrawbin and not self.gsbin:
                    application_path = AppLocation.get_directory(AppLocation.AppDir)
                    if os.path.isfile(os.path.join(application_path, 'mudraw')):
                        self.mudrawbin = os.path.join(application_path, 'mudraw')
        if self.mudrawbin:
            self.also_supports = ['xps', 'oxps']
            return True
        elif self.gsbin:
            return True
        else:
            return False

    def app_startup(self):
        """
        Override app_startup() in order to do nothing
        """
        pass

    def create_settings_tab(self, parent):
        """
        Create the settings Tab

        :param parent:
        """
        visible_name = self.get_string(StringContent.VisibleName)
        self.settings_tab = MediaTab(parent, self.name, visible_name['title'], self.icon_path)

    @staticmethod
    def about():
        """
        Return the about text for the plugin manager
        """
        about_text = translate('MediaPlugin', '<strong>Media Plugin</strong>'
                               '<br />The media plugin provides playback of audio and video.')
        return about_text

    def set_plugin_text_strings(self):
        """
        Called to define all translatable texts of the plugin
        """
        # Name PluginList
        self.text_strings[StringContent.Name] = {
            'singular': translate('MediaPlugin', 'Media', 'name singular'),
            'plural': translate('MediaPlugin', 'Media', 'name plural')
        }
        # Name for MediaDockManager, SettingsManager
        self.text_strings[StringContent.VisibleName] = {
            'title': translate('MediaPlugin', 'Media', 'container title')
        }
        # Middle Header Bar
        tooltips = {
            'load': translate('MediaPlugin', 'Load new media.'),
            'import': '',
            'new': translate('MediaPlugin', 'Add new media.'),
            'edit': translate('MediaPlugin', 'Edit the selected media.'),
            'delete': translate('MediaPlugin', 'Delete the selected media.'),
            'preview': translate('MediaPlugin', 'Preview the selected media.'),
            'live': translate('MediaPlugin', 'Send the selected media live.'),
            'service': translate('MediaPlugin', 'Add the selected media to the service.')
        }
        self.set_plugin_ui_text_strings(tooltips)

    def finalise(self):
        """
        Time to tidy up on exit.
        """
        log.info('Media Finalising')
        self.media_controller.finalise()
        Plugin.finalise(self)

    def get_display_css(self):
        """
        Add css style sheets to htmlbuilder.
        """
        return self.media_controller.get_media_display_css()

    def get_display_javascript(self):
        """
        Add javascript functions to htmlbuilder.
        """
        return self.media_controller.get_media_display_javascript()

    def get_display_html(self):
        """
        Add html code to htmlbuilder.
        """
        return self.media_controller.get_media_display_html()


def process_check_binary(program_path):
    """
    Function that checks whether a binary is either ghostscript or mudraw or neither.
    Is also used from presentationtab.py

    :param program_path:The full path to the binary to check.
    :return: Type of the binary, 'gs' if ghostscript, 'mudraw' if mudraw, None if invalid.
    """
    program_type = None
    runlog = check_binary(program_path)
    # Analyse the output to see it the program is mudraw, ghostscript or neither
    for line in runlog.splitlines():
        decoded_line = line.decode()
        found_mudraw = re.search('usage: mudraw.*', decoded_line, re.IGNORECASE)
        if found_mudraw:
            program_type = 'mudraw'
            break
        found_gs = re.search('GPL Ghostscript.*', decoded_line, re.IGNORECASE)
        if found_gs:
            program_type = 'gs'
            break
    log.debug('in check_binary, found: %s', program_type)
    return program_type
