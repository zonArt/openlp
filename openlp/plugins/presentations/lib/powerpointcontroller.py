# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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
try:
    from win32com.client import Dispatch
except:
    pass

# PPT API documentation:
# http://msdn.microsoft.com/en-us/library/aa269321(office.10).aspx

class PowerPointApp(object):
    def __init__(self):
        log.debug(u'Initialising')
        self.process = None
        self.document = None
        self.presentation = None
        self.startPowerpoint()

    def startPowerpoint(self):
        try:
            self._app = Dispatch(u'PowerPoint.Application')
        except:
            self._app = None
            return
        self._app.Visible = True
        self._app.WindowState = 2

    def getApp(self):
        if self._app == None:
            self.createApp()
            if self._app == None:
                return None
        if self._app.Windows.Count == 0:
            self.createApp()
        return self._app

    app = property(getApp)

    def quit(self):
        self._app.Quit()
        self._app = None

class PowerPointPres(object):

    def __init__(self, pptApp, filename):
        self.pptApp = pptApp
        self.filename = filename
        self.open()

    def getPres(self):
        if self._pres == None:
            for p in self.pptApp.app.Presentations:
                if p.FullName == self.filename:
                    self._pres = p
                    break
        if self._pres != None:
            try:
                x = self._pres.Name
            except:
                self._pres = None
        if self._pres == None:
            self.openPres()
        return self._pres

    pres = property(getPres)

    def open(self):
        self.pptApp.app.Presentations.Open(self.filename, False, False, True)
        self._pres = self.pptApp.app.Presentations(ppt.app.Presentations.Count)

    def close(self):
        self.pres.Close()
        self._pres = None

    def isActive(self):
        if self.pres.SlideShowWindow == None:
            return False
        if self.pres.SlideShowWindow.View == None:
            return False
        return True

    def resume(self):
        self.pres.SlideShowSettings.Run()
        self.pres.SlideShowWindow.View.State = 1
        self.pres.SlideShowWindow.Activate()

    def pause(self):
        if self.isActive():
            self.pres.SlideShowWindow.View.State = 2

    def blankScreen(self):
        if self.isActive():
            self.pres.SlideShowWindow.View.State = 3

    def stop(self):
        if self.isActive():
            self.pres.SlideShowWindow.View.Exit()

    def go(self):
        self.pres.SlideShowSettings.Run()

    def getCurrentSlideIndex(self):
        if self.isActive():
            return self.pres.SlideShowWindow.View.CurrentShowPosition
        else:
            return -1

    def setCurrentSlideIndex(self, slideno):
        if not self.isActive():
            self.resume()
        self.pres.SlideShowWindow.View.GotoSlide(slideno)

    #currentSlideIndex = property(getSlideNumber, setSlideNumber)

    def nextStep(self):
        if not self.isActive():
            self.resume()
        self.pres.SlideShowWindow.View.Next()

    def prevStep(self):
        if not self.isActive():
            self.resume()
        self.pres.SlideShowWindow.View.Previous()

    def moveWindow(self, top, height, left, width):
        if not self.isActive():
            self.resume()
        self.pres.SlideShowWindow.Top = top / 20
        self.pres.SlideShowWindow.Height = height / 20
        self.pres.SlideShowWindow.Left = left / 20
        self.pres.SlideShowWindow.Width = width / 20

class PowerPointSlide(object):
    def __init__(self, pres, index):
        self.pres = pres
        self.slide = pres.Slides[index]

    def preview(self):
        if self.preview == None:
            self.slide.Copy
            # import win32clipboard as w
            # import win32con
            # w.OpenClipboard()
            # self.preview = w.GetClipboardData.GetData(win32con.CF_BITMAP)
            # w.CloseClipboard()
        return self.preview

