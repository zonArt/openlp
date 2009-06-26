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

import os ,  subprocess
import time
import uno

class Openoffice(object):
    def __init__(self):
        self.startOpenoffice()

    def createResolver(self):
        self.localContext = uno.getComponentContext()
        self.resolver = self.localContext.ServiceManager.createInstanceWithContext(u'com.sun.star.bridge.UnoUrlResolver', self.localContext)
        try:
            self.ctx = self.resolver.resolve(u'uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext')
        except:
            return False
        return True

    def buildEnvironment(self):
        self.smgr = self.ctx.ServiceManager
        self.desktop = self.smgr.createInstanceWithContext( "com.sun.star.frame.Desktop", self.ctx )
        self.model = self.desktop.getCurrentComponent()
        text = self.model.Text
        cursor = text.createTextCursor()
        text.insertString(cursor, "Hello world", 0)
        self.ctx.ServiceManager
        self.createApp()
        if self._sm == None:
            # start OO here
            # Create output log file
            time.sleep(10)
            self.createApp()

    def startOpenoffice(self):
        cmd = u'openoffice.org -nologo, -norestore, -minimized, -impress,' + u'"' + u'-accept=socket,host=localhost,port=2002;urp;'+ u'"'
        retval = subprocess.Popen(cmd,  shell=True)
        self.oopid = retval.pid

    def checkOoPid(self):
        if os.name == u'nt':
            import win32api
            handle = win32api.OpenProcess(PROCESS_TERMINATE, False, self.oopid)
            #todo need some code here
            return True
        elif os.name == u'mac':
            pass
        else:
            procfile = open("/proc/%d/stat" %(self.oopid))
            file = procfile.readline().split()[1]
            print file
            if file == u'(soffice)' or file == u'(openoffice.org)':
                return True
            return False

    def createApp(self):
        try:
            self._app = self._sm.createInstance( "com.sun.star.frame.Desktop" )
            print "started"
        except:
            print "oops"
            self._sm = None
            self._app = None
            return

    def getApp(self):
        if self._app == None:
            self.createApp()
            if self._app == None:
                return None
        return self._app

    app = property(getApp)

    def quit(self):
        self._app.Terminate()
        self._app = None
        self._sm = None

class ImpressCOMPres(object):

    def __init__(self, oooApp, filename):
        self.oooApp = oooApp
        self.filename = filename
        self.open()

    def getPres(self):
        if self._pres == None:
            self.open()
        return self._pres

    pres = property(getPres)

    def open(self):
        self.comp = self.oooApp.app.loadComponentFromURL(u'file:///' + self.filename, '_blank', 0, [])
        self.presdoc = self.comp.getPresentation()
        self.presdoc.start()
        self._pres = self.presdoc.getController()

    def close(self):
        self.pres.deactivate()
        self.presdoc.end()
        self.comp.dispose()
        self._pres = None
        self.presdoc = None
        self.comp = None

    def isActive(self):
        return self.pres.isRunning() and self.pres.isActive()

    def resume(self):
        return self.pres.resume()

    def pause(self):
        return self.pres.pause()

    def blankScreen(self):
        self.pres.blankScreen(0)

    def stop(self):
        self.pres.deactivate()
        # self.presdoc.end()

    def go(self):
        self.pres.activate()
        # self.presdoc.start()

    def getSlideNumber(self):
        return self.pres.getCurrentSlideIndex

    def setSlideNumber(self, slideno):
        self.pres.gotoSlideIndex(slideno)

    slideNumber = property(getSlideNumber, setSlideNumber)

    def nextStep(self):
        self.pres.gotoNextEffect()

    def prevStep(self):
        self.pres.gotoPreviousSlide()

    def moveWindow(self, top, height, left, width):
        # position the window somehow
        pass

class ImpressCOMSlide(object):
    def __init__(self, pres, index):
        self.pres = pres
        self.slide = pres.getSlideByIndex(index)

    def preview(self):
        if self.preview == None:
            # get a slide somehow
            pass
        return self.preview

if __name__ == '__main__':
    ooo = Openoffice()
    ooo.createResolver()
    #show = ImpressCOMPres(ooo, u'/home/timali/test1.odp')
    #show.go()
    #show.resume()
    #show.nextStep()
