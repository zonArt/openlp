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

import os
import logging
from tempfile import NamedTemporaryFile
import re
from subprocess import check_output, CalledProcessError, STDOUT
#from PyQt4 import QtCore, QtGui

from openlp.core.utils import AppLocation
from openlp.core.lib import ScreenList, Settings
from .presentationcontroller import PresentationController, PresentationDocument


log = logging.getLogger(__name__)


class PdfController(PresentationController):
    """
    Class to control PDF presentations
    """
    log.info('PdfController loaded')

    def __init__(self, plugin):
        """
        Initialise the class
        """
        log.debug('Initialising')
        self.process = None
        PresentationController.__init__(self, plugin, 'Pdf', PdfDocument)
        self.supports = ['pdf']
        self.mudrawbin = ''
        self.gsbin = ''
        if self.check_installed() and self.mudrawbin != '':
            self.also_supports = ['xps']

    def check_binary(program_path):
        """
        Function that checks whether a binary is either ghostscript or mudraw or neither.
        """

        program_type = None
        runlog = ''
        try:
            runlog = check_output([program_path,  '--help'], stderr=STDOUT)
        except CalledProcessError as e:
            runlog = e.output
        except Exception:
            runlog = ''
            
        # Analyse the output to see it the program is mudraw, ghostscript or neither
        for line in runlog.splitlines():
            found_mudraw = re.search('usage: mudraw.*', line)
            if found_mudraw:
                program_type = 'mudraw'
                break
            found_gs = re.search('GPL Ghostscript.*', line)
            if found_gs:
                program_type = 'gs'
                break
        log.info('in check_binary, found: ' + program_type)
        return program_type



    def check_available(self):
        """
        PdfController is able to run on this machine.
        """
        log.debug('check_available Pdf')
        return self.check_installed()

    def check_installed(self):
        """
        Check the viewer is installed.
        """
        log.debug('check_installed Pdf')
        # Use the user defined program if given
        if (Settings().value('presentations/enable_given_pdf_program')):
            given_pdf_program = Settings().value('presentations/given_pdf_program')
            type = self.check_binary(given_pdf_program)
            if type == 'gs':
                self.gsbin = given_pdf_program
                return True
            elif type == 'mudraw':
                self.mudrawbin = given_pdf_program
                return True

        # Fallback to autodetection
        application_path = AppLocation.get_directory(AppLocation.AppDir)
        if os.name != 'nt':
            # First try to find mupdf
            try:
                self.mudrawbin = check_output(['which', 'mudraw']).decode(encoding='UTF-8').rstrip('\n')
            except CalledProcessError:
                self.mudrawbin = ''

            # if mupdf isn't installed, fallback to ghostscript
            if self.mudrawbin == '':
                try:
                    self.gsbin = check_output(['which', 'gs']).rstrip('\n')
                except CalledProcessError:
                    self.gsbin = ''
                
            # Last option: check if mudraw is placed in OpenLP base folder
            if self.mudrawbin == '' and self.gsbin == '':
                application_path = AppLocation.get_directory(AppLocation.AppDir)
                if os.path.isfile(application_path + '/../mudraw'):
                    self.mudrawbin = application_path + '/../mudraw'
        else:
            # for windows we only accept mudraw.exe in the base folder
            application_path = AppLocation.get_directory(AppLocation.AppDir)
            if os.path.isfile(application_path + '/../mudraw.exe'):
                self.mudrawbin = application_path + '/../mudraw.exe'
            
        if self.mudrawbin == '' and self.gsbin == '':
            return False
        else:
            return True
        
    def kill(self):
        """
        Called at system exit to clean up any running presentations
        """
        log.debug('Kill pdfviewer')
        while self.docs:
            self.docs[0].close_presentation()


class PdfDocument(PresentationDocument):
    """
    Class which holds information of a single presentation.
    """
    def __init__(self, controller, presentation):
        """
        Constructor, store information about the file and initialise.
        """
        log.debug('Init Presentation Pdf')
        PresentationDocument.__init__(self, controller, presentation)
        self.presentation = None
        self.blanked = False
        self.hidden = False
        self.image_files = []
        self.num_pages = -1

    def gs_get_resolution(self,  size):
        """ 
        Only used when using ghostscript
        Ghostscript can't scale automaticly while keeping aspect like mupdf, so we need
        to get the ratio bewteen the screen size and the PDF to scale
        """
        # Use a postscript script to get size of the pdf. It is assumed that all pages have same size
        postscript = '%!PS \n\
() = \n\
File dup (r) file runpdfbegin \n\
1 pdfgetpage dup \n\
/MediaBox pget { \n\
aload pop exch 4 1 roll exch sub 3 1 roll sub \n\
( Size: x: ) print =print (, y: ) print =print (\n) print \n\
} if \n\
flush \n\
quit \n\
'
        # Put postscript into tempfile
        tmpfile = NamedTemporaryFile(delete=False)
        tmpfile.write(postscript)
        tmpfile.close()
        
        # Run the script on the pdf to get the size
        runlog = []
        try:
            runlog = check_output([self.controller.gsbin, '-dNOPAUSE', '-dNODISPLAY', '-dBATCH', '-sFile=' + self.filepath, tmpfile.name])
        except CalledProcessError as e:
            log.debug(' '.join(e.cmd))
            log.debug(e.output)
        os.unlink(tmpfile.name)
        
        # Extract the pdf resolution from output, the format is " Size: x: <width>, y: <height>"
        width = 0
        height = 0
        for line in runlog.splitlines():
            try:
                width = re.search('.*Size: x: (\d+\.?\d*), y: \d+.*', line).group(1)
                height = re.search('.*Size: x: \d+\.?\d*, y: (\d+\.?\d*).*', line).group(1)
                break;
            except AttributeError:
                pass

        # Calculate the ratio from pdf to screen
        if width > 0 and height > 0:
            width_ratio = size.right() / float(width)
            height_ratio = size.bottom() / float(height)
            
            # return the resolution that should be used. 72 is default.
            if width_ratio > height_ratio:
                return int(height_ratio * 72)
            else:
                return int(width_ratio * 72)
        else:
            return 72

    def load_presentation(self):
        """
        Called when a presentation is added to the SlideController. It generates images from the PDF.
        """
        log.debug('load_presentation pdf')
        
        # Check if the images has already been created, and if yes load them
        if os.path.isfile(os.path.join(self.get_temp_folder(), 'mainslide001.png')):
            created_files = sorted(os.listdir(self.get_temp_folder()))
            for fn in created_files:
                if os.path.isfile(os.path.join(self.get_temp_folder(),  fn)):
                    self.image_files.append(os.path.join(self.get_temp_folder(), fn))
            self.num_pages = len(self.image_files)
            return True
        
        size = ScreenList().current['size']
        # Generate images from PDF that will fit the frame.
        runlog = ''
        try:
            if not os.path.isdir(self.get_temp_folder()):
                os.makedirs(self.get_temp_folder())
            if self.controller.mudrawbin != '':
                runlog = check_output([self.controller.mudrawbin, '-w', str(size.right()), '-h', str(size.bottom()), '-o', os.path.join(self.get_temp_folder(), 'mainslide%03d.png'), self.filepath])
            elif self.controller.gsbin != '':
                resolution = self.gs_get_resolution(size)
                runlog = check_output([self.controller.gsbin, '-dSAFER', '-dNOPAUSE', '-dBATCH', '-sDEVICE=png16m', '-r' + str(resolution), '-dTextAlphaBits=4', '-dGraphicsAlphaBits=4', '-sOutputFile=' + os.path.join(self.get_temp_folder(), 'mainslide%03d.png'), self.filepath])
            created_files = sorted(os.listdir(self.get_temp_folder()))
            for fn in created_files:
                if os.path.isfile(os.path.join(self.get_temp_folder(), fn)):
                    self.image_files.append(os.path.join(self.get_temp_folder(), fn))
        except Exception as e: 
            log.debug(e)
            log.debug(runlog)
            return False 
        self.num_pages = len(self.image_files)
        
        # Create thumbnails
        self.create_thumbnails()
        return True

    def create_thumbnails(self):
        """
        Generates thumbnails
        """
        log.debug('create_thumbnails pdf')
        if self.check_thumbnails():
            return
        log.debug('create_thumbnails proceeding')
        
        # use builtin function to create thumbnails from generated images
        index = 1
        for image in self.image_files:
            self.convert_thumbnail(image, index)
            index += 1

    def close_presentation(self):
        """
        Close presentation and clean up objects. Triggered by new object being added to SlideController or OpenLP being
        shut down.
        """
        log.debug('close_presentation pdf')
        self.controller.remove_doc(self)
        
    def is_loaded(self):
        """
        Returns true if a presentation is loaded.
        """
        log.debug('is_loaded pdf')
        if self.num_pages < 0:
            return False
        return True

    def is_active(self):
        """
        Returns true if a presentation is currently active.
        """
        log.debug('is_active pdf')
        return self.is_loaded() and not self.hidden

