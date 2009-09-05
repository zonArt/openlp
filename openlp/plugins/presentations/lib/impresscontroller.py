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
#http://www.linuxjournal.com/content/starting-stopping-and-connecting-openoffice-python
#http://nxsy.org/comparing-documents-with-openoffice-and-python

import logging
import os ,  subprocess
import time
import uno

from PyQt4 import QtCore, QtGui
from openlp.core.lib import translate

class ImpressController(object):
    global log
    log = logging.getLogger(u'ImpressController')

    def __init__(self):
        log.debug(u'Initialising')
        self.process = None
        self.startOpenoffice()

    def startOpenoffice(self):
        log.debug(u'start Openoffice')
        cmd = u'openoffice.org -nologo -norestore -minimized -headless ' + u'"' + u'-accept=socket,host=localhost,port=2002;urp;'+ u'"'
        print cmd
        self.process = QtCore.QProcess()
        self.process.startDetached(cmd)
        self.process.waitForStarted()

    def createResolver(self):
        self.localContext = uno.getComponentContext()
        self.resolver = self.localContext.ServiceManager.createInstanceWithContext(u'com.sun.star.bridge.UnoUrlResolver', self.localContext)
        try:
            self.ctx = self.resolver.resolve(u'uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext')
        except:
            return False
        return True

    def buildEnvironment(self):
        log.deug(u'buildEnvironment')
        self.smgr = self.ctx.ServiceManager
        self.desktop = self.smgr.createInstanceWithContext( "com.sun.star.frame.Desktop", self.ctx )

    def kill(self):
        log.debug(u'Kill')
        self.process.terminate()

    def loadPresentation(self, presentation):
        url = uno.systemPathToFileUrl(presentation)
        self.document = self.desktop(url, '_blank', 0, [])
        self.presentation = self.document.getPresentation()
        self.presentation.start()

    def closePresentation(self):
        self.document.dispose()

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
        self.presentation.gotoNextEffect()

    def prevStep(self):
        self.presentation.gotoPreviousSlide()

    def moveWindow(self, top, height, left, width):
        # position the window somehow
        pass
