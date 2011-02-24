# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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
import logging
import os

from PyQt4 import QtCore

from openlp.core.utils import get_uno_command, get_uno_instance
from songimport import SongImport

log = logging.getLogger(__name__)

if os.name == u'nt':
    from win32com.client import Dispatch
    PAGE_BEFORE = 4
    PAGE_AFTER = 5
    PAGE_BOTH = 6
else:
    try:
        import uno
        from com.sun.star.style.BreakType import PAGE_BEFORE, PAGE_AFTER, \
            PAGE_BOTH
    except ImportError:
        pass

class OooImport(SongImport):
    """
    Import songs from Impress/Powerpoint docs using Impress
    """
    def __init__(self, master_manager, **kwargs):
        """
        Initialise the class. Requires a songmanager class which is passed
        to SongImport for writing song to disk
        """
        SongImport.__init__(self, master_manager, **kwargs)
        self.document = None
        self.process_started = False

    def do_import(self):
        self.stop_import_flag = False
        self.import_wizard.progressBar.setMaximum(0)
        self.start_ooo()
        for filename in self.import_source:
            if self.stop_import_flag:
                self.import_wizard.incrementProgressBar(u'Import cancelled', 0)
                return
            filename = unicode(filename)
            if os.path.isfile(filename):
                self.open_ooo_file(filename)
                if self.document:
                    self.process_ooo_document()
                    self.close_ooo_file()
        self.close_ooo()
        self.import_wizard.progressBar.setMaximum(1)
        self.import_wizard.incrementProgressBar(u'', 1)
        return True

    def process_ooo_document(self):
        """
        Handle the import process for OpenOffice files. This method facilitates
        allowing subclasses to handle specific types of OpenOffice files.
        """
        if self.document.supportsService(
            "com.sun.star.presentation.PresentationDocument"):
            self.process_pres()
        if self.document.supportsService("com.sun.star.text.TextDocument"):
            self.process_doc()

    def start_ooo(self):
        """
        Start OpenOffice.org process
        TODO: The presentation/Impress plugin may already have it running
        """
        if os.name == u'nt':
            self.start_ooo_process()
            self.desktop = self.manager.createInstance(
                u'com.sun.star.frame.Desktop')
        else:
            context = uno.getComponentContext()
            resolver = context.ServiceManager.createInstanceWithContext(
                u'com.sun.star.bridge.UnoUrlResolver', context)
            uno_instance = None
            loop = 0
            while uno_instance is None and loop < 5:
                try:
                    uno_instance = get_uno_instance(resolver)
                except:
                    log.exception("Failed to resolve uno connection")
                    self.start_ooo_process()
                    loop += 1
            manager = uno_instance.ServiceManager
            self.desktop = manager.createInstanceWithContext(
                "com.sun.star.frame.Desktop", uno_instance)

    def start_ooo_process(self):
        try:
            if os.name == u'nt':
                self.manager = Dispatch(u'com.sun.star.ServiceManager')
                self.manager._FlagAsMethod(u'Bridge_GetStruct')
                self.manager._FlagAsMethod(u'Bridge_GetValueObject')
            else:
                cmd = get_uno_command()
                process = QtCore.QProcess()
                process.startDetached(cmd)
                process.waitForStarted()
            self.process_started = True
        except:
            log.exception("start_ooo_process failed")

    def open_ooo_file(self, filepath):
        """
        Open the passed file in OpenOffice.org Impress
        """
        if os.name == u'nt':
            url = u'file:///' + filepath.replace(u'\\', u'/')
            url = url.replace(u':', u'|').replace(u' ', u'%20')
        else:
            url = uno.systemPathToFileUrl(filepath)
        properties = []
        properties = tuple(properties)
        try:
            self.document = self.desktop.loadComponentFromURL(url, u'_blank',
                0, properties)
            if not self.document.supportsService(
                "com.sun.star.presentation.PresentationDocument") and not \
                self.document.supportsService("com.sun.star.text.TextDocument"):
                self.close_ooo_file()
            else:
                self.import_wizard.incrementProgressBar(
                    u'Processing file ' + filepath, 0)
        except:
            log.exception("open_ooo_file failed")
        return

    def close_ooo_file(self):
        """
        Close file.
        """
        self.document.close(True)
        self.document = None

    def close_ooo(self):
        """
        Close OOo. But only if we started it and not on windows
        """
        if self.process_started:
            self.desktop.terminate()

    def process_pres(self):
        """
        Process the file
        """
        doc = self.document
        slides = doc.getDrawPages()
        text = u''
        for slide_no in range(slides.getCount()):
            if self.stop_import_flag:
                self.import_wizard.incrementProgressBar(u'Import cancelled', 0)
                return
            slide = slides.getByIndex(slide_no)
            slidetext = u''
            for idx in range(slide.getCount()):
                shape = slide.getByIndex(idx)
                if shape.supportsService("com.sun.star.drawing.Text"):
                    if shape.getString().strip() != u'':
                        slidetext += shape.getString().strip() + u'\n\n'
            if slidetext.strip() == u'':
                slidetext = u'\f'
            text += slidetext
        song = SongImport(self.manager)
        songs = SongImport.process_songs_text(self.manager, text)
        for song in songs:
            song.finish()
        return

    def process_doc(self):
        """
        Process the doc file, a paragraph at a time
        """
        text = u''
        paragraphs = self.document.getText().createEnumeration()
        while paragraphs.hasMoreElements():
            paratext = u''
            paragraph = paragraphs.nextElement()
            if paragraph.supportsService("com.sun.star.text.Paragraph"):
                textportions = paragraph.createEnumeration()
                while textportions.hasMoreElements():
                    textportion = textportions.nextElement()
                    if textportion.BreakType in (PAGE_BEFORE, PAGE_BOTH):
                        paratext += u'\f'
                    paratext += textportion.getString()
                    if textportion.BreakType in (PAGE_AFTER, PAGE_BOTH):
                        paratext += u'\f'
            text += paratext + u'\n'
        songs = SongImport.process_songs_text(self.manager, text)
        for song in songs:
            song.finish()
