# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
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

if os.name == u'nt':
    from win32com.client import Dispatch
else:
    import uno

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
        if os.name != u'nt':
            # -headless
            cmd = u'openoffice.org -nologo -norestore -minimized -invisible ' + u'"' + u'-accept=socket,host=localhost,port=2002;urp;'+ u'"'
            self.process = QtCore.QProcess()
            self.process.startDetached(cmd)
            self.process.waitForStarted()

    def kill(self):
        """
        Called at system exit to clean up any running presentations
        """
        log.debug(u'Kill')
        self.close_presentation()

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
        if os.name == u'nt':
            desktop = self.get_com_desktop()
            url = u'file:///' + presentation.replace(u'\\', u'/').replace(u':', u'|').replace(u' ', u'%20')
        else:
            desktop = self.get_uno_desktop()
            url = uno.systemPathToFileUrl(presentation)
        if desktop is None:
            return
        try:
            properties = []
            properties = tuple(properties)
            self.document = desktop.loadComponentFromURL(
                url, "_blank", 0, properties)
            self.presentation = self.document.getPresentation()
            self.presentation.start()
            self.controller = \
                desktop.getCurrentComponent().Presentation.getController()
        except:
            log.exception(u'Failed to load presentation')

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
                self.startOpenoffice()
                loop += 1
        try:
            smgr = ctx.ServiceManager
            desktop = smgr.createInstanceWithContext(
                "com.sun.star.frame.Desktop", ctx )
            return desktop
        except:
            log.exception(u'Failed to get UNO desktop')
            return None

    def get_com_desktop(self):
        log.debug(u'getCOMDesktop')
        try:
            smgr = self.get_com_servicemanager()
            desktop = smgr.createInstance( "com.sun.star.frame.Desktop")
            return desktop
        except:
            log.exception(u'Failed to get COM desktop')
            return None

    def get_com_servicemanager(self):
        log.debug(u'get_com_servicemanager')
        try:
            return Dispatch("com.sun.star.ServiceManager")
        except:
            log.exception(u'Failed to get COM service manager')
            return None

    def close_presentation(self):
        """
        Close presentation and clean up objects
        Triggerent by new object being added to SlideController orOpenLP
        being shut down
        """
        if self.document is not None:
            if self.presentation is not None:
                self.presentation.end()
                self.presentation = None
            self.document.dispose()
            self.document = None

    def is_loaded(self):
        return self.presentation is not None and self.document is not None

    def is_active(self):
        if not self.is_loaded():
            return False
        return self.presentation.isRunning() and self.presentation.isActive()

    def unblank_screen(self):
        return self.presentation.resume()

    def blank_screen(self):
        self.presentation.blankScreen(0)

    def stop_presentation(self):
        self.presentation.deactivate()
        # self.presdoc.end()

    def start_presentation(self):
        self.presentation.activate()
        # self.presdoc.start()

    def get_slide_number(self):
        return self.presentation.getCurrentSlideIndex

    def goto_slide(self, slideno):
        self.presentation.gotoSlideIndex(slideno)

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

    # def get_slide_preview_file(self, slide_no):

