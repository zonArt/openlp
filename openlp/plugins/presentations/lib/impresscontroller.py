# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

# OOo API documentation:
# http://api.openoffice.org/docs/common/ref/com/sun/star/presentation/XSlideShowController.html
# http://docs.go-oo.org/sd/html/classsd_1_1SlideShow.html
# http://www.oooforum.org/forum/viewtopic.phtml?t=5252
# http://wiki.services.openoffice.org/wiki/Documentation/DevGuide/Working_with_Presentations
# http://mail.python.org/pipermail/python-win32/2008-January/006676.html
# http://www.linuxjournal.com/content/starting-stopping-and-connecting-openoffice-python
# http://nxsy.org/comparing-documents-with-openoffice-and-python

import logging
import os
import time

if os.name == u'nt':
    from win32com.client import Dispatch
else:
    import uno
    from com.sun.star.beans import PropertyValue

from PyQt4 import QtCore

from presentationcontroller import PresentationController

class ImpressController(PresentationController):
    """
    Class to control interactions with Impress presentations.
    It creates the runtime environment, loads and closes the presentation as
    well as triggering the correct activities based on the users input
    """
    global log
    log = logging.getLogger(u'ImpressController')
    log.info(u'loaded')

    def __init__(self, plugin):
        """
        Initialise the class
        """
        log.debug(u'Initialising')
        PresentationController.__init__(self, plugin, u'Impress')
        self.process = None
        self.document = None
        self.presentation = None
        self.controller = None

    def check_available(self):
        """
        Impress is able to run on this machine
        """
        log.debug(u'check_available')
        if os.name == u'nt':
            return self.get_com_servicemanager() is not None
        else:
            # If not windows, and we've got this far then probably
            # installed else the import uno would likely have failed
            return True

    def start_process(self):
        """
        Loads a running version of OpenOffice in the background.
        It is not displayed to the user but is available to the UNO interface
        when required.
        """
        log.debug(u'start Openoffice')
        if os.name == u'nt':
            self.manager = self.get_com_servicemanager()
            self.manager._FlagAsMethod(u'Bridge_GetStruct')
            self.manager._FlagAsMethod(u'Bridge_GetValueObject')
        else:
            # -headless
            cmd = u'openoffice.org -nologo -norestore -minimized -invisible -nofirststartwizard -accept="socket,host=localhost,port=2002;urp;"'
            self.process = QtCore.QProcess()
            self.process.startDetached(cmd)
            self.process.waitForStarted()

    def kill(self):
        """
        Called at system exit to clean up any running presentations
        """
        log.debug(u'Kill')
        self.close_presentation()
        if os.name != u'nt':
            desktop = self.get_uno_desktop()
            try:
                desktop.terminate()
            except:
                pass

    def load_presentation(self, presentation):
        """
        Called when a presentation is added to the SlideController.
        It builds the environment, starts communcations with the background
        OpenOffice task started earlier.  If OpenOffice is not present is is
        started.  Once the environment is available the presentation is loaded
        and started.

        ``presentation``
        The file name of the presentatios to the run.
        """
        log.debug(u'LoadPresentation')
        self.store_filename(presentation)
        if os.name == u'nt':
            desktop = self.get_com_desktop()
            if desktop is None:
                self.start_process()
                desktop = self.get_com_desktop()
            url = u'file:///' + presentation.replace(u'\\', u'/').replace(u':', u'|').replace(u' ', u'%20')
        else:
            desktop = self.get_uno_desktop()
            url = uno.systemPathToFileUrl(presentation)
        if desktop is None:
            return
        self.desktop = desktop
        properties = []
        properties.append(self.create_property(u'Minimized', True))
        properties = tuple(properties)
        try:
            self.document = desktop.loadComponentFromURL(url, u'_blank',
                0, properties)
        except:
            log.exception(u'Failed to load presentation')
            return
        self.presentation = self.document.getPresentation()
        self.presentation.Display = self.plugin.render_manager.screens.current_display + 1
        self.controller = None
        self.create_thumbnails()

    def create_thumbnails(self):
        """
        Create thumbnail images for presentation
        """
        if self.check_thumbnails():
            return

        if os.name == u'nt':
            thumbdir = u'file:///' + self.thumbnailpath.replace(
                u'\\', u'/').replace(u':', u'|').replace(u' ', u'%20')
        else:
            thumbdir = uno.systemPathToFileUrl(self.thumbnailpath)
        props = []
        props.append(self.create_property(u'FilterName', u'impress_png_Export'))
        props = tuple(props)
        doc = self.document
        pages = doc.getDrawPages()
        for idx in range(pages.getCount()):
            page = pages.getByIndex(idx)
            doc.getCurrentController().setCurrentPage(page)
            path = u'%s/%s%s.png'% (thumbdir, self.thumbnailprefix,
                    unicode(idx+1))
            try:
                doc.storeToURL(path , props)
            except:
                log.exception(u'%s\nUnable to store preview' % path)

    def create_property(self, name, value):
        if os.name == u'nt':
            prop = self.manager.Bridge_GetStruct(u'com.sun.star.beans.PropertyValue')
        else:
            prop = PropertyValue()
        prop.Name = name
        prop.Value = value
        return prop

    def get_uno_desktop(self):
        log.debug(u'getUNODesktop')
        ctx = None
        loop = 0
        context = uno.getComponentContext()
        resolver = context.ServiceManager.createInstanceWithContext(
            u'com.sun.star.bridge.UnoUrlResolver', context)
        while ctx is None and loop < 3:
            try:
                ctx = resolver.resolve(u'uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext')
            except:
                self.start_process()
                loop += 1
        try:
            self.manager = ctx.ServiceManager
            desktop = self.manager.createInstanceWithContext(
                "com.sun.star.frame.Desktop", ctx )
            return desktop
        except:
            log.exception(u'Failed to get UNO desktop')
            return None

    def get_com_desktop(self):
        log.debug(u'getCOMDesktop')
        try:
            desktop = self.manager.createInstance(u'com.sun.star.frame.Desktop')
            return desktop
        except:
            log.exception(u'Failed to get COM desktop')
        return None

    def get_com_servicemanager(self):
        log.debug(u'get_com_servicemanager')
        try:
            return Dispatch(u'com.sun.star.ServiceManager')
        except:
            log.exception(u'Failed to get COM service manager')
            return None

    def close_presentation(self):
        """
        Close presentation and clean up objects
        Triggerent by new object being added to SlideController orOpenLP
        being shut down
        """
        if self.document:
            if self.presentation:
                try:
                    self.presentation.end()
                    self.presentation = None
                    self.document.dispose()
                except:
                    #We tried!
                    pass
            self.document = None

    def is_loaded(self):
        if self.presentation is None or self.document is None:
            return False
        try:
            if self.document.getPresentation() is None:
                return False
        except:
            return False
        return True

    def is_active(self):
        if not self.is_loaded():
            return False
        if self.controller is None:
            return False
        return True

    def unblank_screen(self):
        return self.controller.resume()

    def blank_screen(self):
        self.controller.blankScreen(0)

    def stop_presentation(self):
        self.controller.deactivate()

    def start_presentation(self):
        if self.controller is None or not self.controller.isRunning():
            self.presentation.start()
            # start() returns before the getCurrentComponent is ready. Try for 5 seconds
            i = 1
            while self.desktop.getCurrentComponent() is None and i < 50:
                time.sleep(0.1)
                i = i + 1
            self.controller = self.desktop.getCurrentComponent().Presentation.getController()
        else:
            self.controller.activate()
            self.goto_slide(1)

    def get_slide_number(self):
        return self.controller.getCurrentSlideIndex() + 1

    def get_slide_count(self):
        return self.document.getDrawPages().getCount()

    def goto_slide(self, slideno):
        self.controller.gotoSlideIndex(slideno-1)

    def next_step(self):
       """
       Triggers the next effect of slide on the running presentation
       """
       self.controller.gotoNextEffect()

    def previous_step(self):
        """
        Triggers the previous slide on the running presentation
        """
        self.controller.gotoPreviousSlide()

    def get_slide_preview_file(self, slide_no):
        """
        Returns an image path containing a preview for the requested slide

        ``slide_no``
        The slide an image is required for, starting at 1
        """
        path = os.path.join(self.thumbnailpath,
            self.thumbnailprefix + unicode(slide_no) + u'.png')
        if os.path.isfile(path):
            return path
        else:
            return None
