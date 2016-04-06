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
The :mod:`propresenter` module provides the functionality for importing
ProPresenter song files into the current installation database.
"""

import os
import base64
import logging
from lxml import objectify

from openlp.core.ui.wizard import WizardStrings
from openlp.plugins.songs.lib import strip_rtf
from .songimport import SongImport

log = logging.getLogger(__name__)


class ProPresenterImport(SongImport):
    """
    The :class:`ProPresenterImport` class provides OpenLP with the
    ability to import ProPresenter 4-6 song files.
    """
    def do_import(self):
        self.import_wizard.progress_bar.setMaximum(len(self.import_source))
        for file_path in self.import_source:
            if self.stop_import_flag:
                return
            self.import_wizard.increment_progress_bar(WizardStrings.ImportingType % os.path.basename(file_path))
            root = objectify.parse(open(file_path, 'rb')).getroot()
            self.process_song(root, file_path)

    def process_song(self, root, filename):
        self.set_defaults()

        # Extract ProPresenter versionNumber
        try:
            self.version = int(root.get('versionNumber'))
        except ValueError:
            log.debug('ProPresenter versionNumber invalid or missing')
            return

        # Title
        self.title = root.get('CCLISongTitle')
        if not self.title or self.title == '':
            self.title = os.path.basename(filename)
            if self.title[-5:-1] == '.pro':
                self.title = self.title[:-5]
        # Notes
        self.comments = root.get('notes')
        # Author
        for author_key in ['author', 'CCLIAuthor', 'artist', 'CCLIArtistCredits']:
            author = root.get(author_key)
            if author and len(author) > 0:
                self.parse_author(author)

        # ProPresenter 4
        if(self.version >= 400 and self.version < 500):
            self.copyright = root.get('CCLICopyrightInfo')
            self.ccli_number = root.get('CCLILicenseNumber')
            count = 0
            for slide in root.slides.RVDisplaySlide:
                count += 1
                if not hasattr(slide.displayElements, 'RVTextElement'):
                    log.debug('No text found, may be an image slide')
                    continue
                RTFData = slide.displayElements.RVTextElement.get('RTFData')
                rtf = base64.standard_b64decode(RTFData)
                words, encoding = strip_rtf(rtf.decode())
                self.add_verse(words, "v%d" % count)

        # ProPresenter 5
        elif(self.version >= 500 and self.version < 600):
            self.copyright = root.get('CCLICopyrightInfo')
            self.ccli_number = root.get('CCLILicenseNumber')
            count = 0
            for group in root.groups.RVSlideGrouping:
                for slide in group.slides.RVDisplaySlide:
                    count += 1
                    if not hasattr(slide.displayElements, 'RVTextElement'):
                        log.debug('No text found, may be an image slide')
                        continue
                    RTFData = slide.displayElements.RVTextElement.get('RTFData')
                    rtf = base64.standard_b64decode(RTFData)
                    words, encoding = strip_rtf(rtf.decode())
                    self.add_verse(words, "v%d" % count)

        # ProPresenter 6
        elif(self.version >= 600 and self.version < 700):
            self.copyright = root.get('CCLICopyrightYear')
            self.ccli_number = root.get('CCLISongNumber')
            count = 0
            for group in root.array.RVSlideGrouping:
                for slide in group.array.RVDisplaySlide:
                    count += 1
                    for item in slide.array:
                        if not (item.get('rvXMLIvarName') == "displayElements"):
                            continue
                        if not hasattr(item, 'RVTextElement'):
                            log.debug('No text found, may be an image slide')
                            continue
                        for contents in item.RVTextElement.NSString:
                            b64Data = contents.text
                            data = base64.standard_b64decode(b64Data)
                            words = None
                            if(contents.get('rvXMLIvarName') == "RTFData"):
                                words, encoding = strip_rtf(data.decode())
                                break
                        if words:
                            self.add_verse(words, "v%d" % count)

        if not self.finish():
            self.log_error(self.import_source)
