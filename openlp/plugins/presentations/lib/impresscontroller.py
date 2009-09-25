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

from PyQt4 import QtCore

class ImpressController(object):
    """
    Class to control interactions with Impress presentations.
    It creates the runtime environment, loads and closes the presentation as
    well as triggering the correct activities based on the users input
    """
    global log
    log = logging.getLogger(u'ImpressController')

    def __init__(self):
        log.debug(u'Initialising')
        self.process = None
        self.document = None
        self.presentation = None
        self.startOpenoffice()

    def startOpenoffice(self):
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
        self.closePresentation()

    def loadPresentation(self, presentation):
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
            desktop = self.getCOMDesktop()
            url = u'file:///' + presentation.replace(u'\\', u'/').replace(u':', u'|').replace(u' ', u'%20')
        else:
            desktop = self.getUNODesktop()
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
            self.xSlideShowController = \
                desktop.getCurrentComponent().Presentation.getController()
        except:
            log.exception(u'Failed to load presentation')

    def getUNODesktop(self):
        log.debug(u'getUNODesktop')
        ctx = None
        loop = 0
        context = uno.getComponentContext()
        resolver = context.ServiceManager.createInstanceWithContext(
            u'com.sun.star.bridge.UnoUrlResolver', context)
        while ctx == None and loop < 3:
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

    def getCOMDesktop(self):
        log.debug(u'getCOMDesktop')
        try:
            smgr = Dispatch("com.sun.star.ServiceManager")
            desktop = smgr.createInstance( "com.sun.star.frame.Desktop")
            return desktop
        except:
            log.exception(u'Failed to get COM desktop')
            return None

    def closePresentation(self):
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

    def isActive(self):
        return self.presentation.isRunning() and self.presentation.isActive()

    def resume(self):
        return self.presentation.resume()

    def pause(self):
        return self.presentation.pause()

    def blankScreen(self):
        self.presentation.blankScreen(0)

    def stop(self):
        self.presentation.deactivate()
        # self.presdoc.end()

    def go(self):
        self.presentation.activate()
        # self.presdoc.start()

    def getSlideNumber(self):
        return self.presentation.getCurrentSlideIndex

    def setSlideNumber(self, slideno):
        self.presentation.gotoSlideIndex(slideno)

    slideNumber = property(getSlideNumber, setSlideNumber)

    def nextStep(self):
       """
       Triggers the next effect of slide on the running presentation
       """
       self.xSlideShowController.gotoNextEffect()

    def previousStep(self):
        """
        Triggers the previous slide on the running presentation
        """
        self.xSlideShowController.gotoPreviousSlide()

