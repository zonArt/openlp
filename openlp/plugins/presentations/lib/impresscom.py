#from win32com.client import Dispatch

# OOo API documentation:
# http://api.openoffice.org/docs/common/ref/com/sun/star/presentation/XSlideShowController.html
# http://docs.go-oo.org/sd/html/classsd_1_1SlideShow.html
# http://www.oooforum.org/forum/viewtopic.phtml?t=5252
# http://wiki.services.openoffice.org/wiki/Documentation/DevGuide/Working_with_Presentations
# http://mail.python.org/pipermail/python-win32/2008-January/006676.html

class ImpressCOMApp(object):
    def __init__(self):
        self.createApp()

    def createApp(self):
        try:
            self._sm = Dispatch(u'com.sun.star.ServiceManager')
            self._app = self._sm.createInstance( "com.sun.star.frame.Desktop" )
        except:
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
    ooo = ImpressCOMApp()
    show = ImpressCOMPres(ooo, u'c:/test1.ppt')
    show.go()
    show.resume()
    show.nextStep()
