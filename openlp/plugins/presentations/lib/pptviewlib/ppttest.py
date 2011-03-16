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

import sys
from PyQt4 import QtGui, QtCore
from ctypes import *
from ctypes.wintypes import RECT

class PPTViewer(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.pptid = -1
        self.setWindowTitle(u'PowerPoint Viewer Test')

        PPTLabel = QtGui.QLabel(u'Open PowerPoint file')
        slideLabel = QtGui.QLabel(u'Go to slide #')
        self.PPTEdit = QtGui.QLineEdit()
        self.slideEdit = QtGui.QLineEdit()
        self.total = QtGui.QLabel()
        PPTBtn = QtGui.QPushButton(u'Open')
        PPTDlgBtn = QtGui.QPushButton(u'...')
        slideBtn = QtGui.QPushButton(u'Go')
        prev = QtGui.QPushButton(u'Prev')
        next = QtGui.QPushButton(u'Next')
        blank = QtGui.QPushButton(u'Blank')
        unblank = QtGui.QPushButton(u'Unblank')
        restart = QtGui.QPushButton(u'Restart')
        close = QtGui.QPushButton(u'Close')
        resume = QtGui.QPushButton(u'Resume')
        stop = QtGui.QPushButton(u'Stop')
        pptwindow = QtGui.QWidget()

        grid = QtGui.QGridLayout()
        grid.addWidget(PPTLabel, 0, 0)
        grid.addWidget(self.PPTEdit, 0, 1)
        grid.addWidget(PPTDlgBtn, 0, 2)
        grid.addWidget(PPTBtn, 0, 3)
        grid.addWidget(slideLabel, 1, 0)
        grid.addWidget(self.slideEdit, 1, 1)
        grid.addWidget(slideBtn, 1, 3)
        grid.addWidget(prev, 2, 0)
        grid.addWidget(next, 2, 1)
        grid.addWidget(blank, 3, 0)
        grid.addWidget(unblank, 3, 1)
        grid.addWidget(restart, 4, 0)
        grid.addWidget(close, 4, 1)
        grid.addWidget(stop, 5, 0)
        grid.addWidget(resume, 5, 1)
        grid.addWidget(pptwindow, 6, 0, 10, 3)
        self.connect(PPTBtn, QtCore.SIGNAL(u'clicked()'), self.OpenClick)
        self.connect(PPTDlgBtn, QtCore.SIGNAL(u'clicked()'), self.OpenDialog)
        self.connect(slideBtn, QtCore.SIGNAL(u'clicked()'), self.GotoClick)
        self.connect(prev, QtCore.SIGNAL(u'clicked()'), self.PrevClick)
        self.connect(next, QtCore.SIGNAL(u'clicked()'), self.NextClick)
        self.connect(blank, QtCore.SIGNAL(u'clicked()'), self.BlankClick)
        self.connect(unblank, QtCore.SIGNAL(u'clicked()'), self.UnblankClick)
        self.connect(restart, QtCore.SIGNAL(u'clicked()'), self.RestartClick)
        self.connect(close, QtCore.SIGNAL(u'clicked()'), self.CloseClick)
        self.connect(stop, QtCore.SIGNAL(u'clicked()'), self.StopClick)
        self.connect(resume, QtCore.SIGNAL(u'clicked()'), self.ResumeClick)

        self.setLayout(grid)

        self.resize(300, 150)

    def PrevClick(self):
        if self.pptid<0: return
        pptdll.PrevStep(self.pptid)
        self.UpdateCurrSlide()
        app.processEvents()

    def NextClick(self):
        if(self.pptid<0): return
        pptdll.NextStep(self.pptid)
        self.UpdateCurrSlide()
        app.processEvents()

    def BlankClick(self):
        if(self.pptid<0): return
        pptdll.Blank(self.pptid)
        app.processEvents()

    def UnblankClick(self):
        if(self.pptid<0): return
        pptdll.Unblank(self.pptid)
        app.processEvents()

    def RestartClick(self):
        if(self.pptid<0): return
        pptdll.RestartShow(self.pptid)
        self.UpdateCurrSlide()
        app.processEvents()

    def StopClick(self):
        if(self.pptid<0): return
        pptdll.Stop(self.pptid)
        app.processEvents()

    def ResumeClick(self):
        if(self.pptid<0): return
        pptdll.Resume(self.pptid)
        app.processEvents()

    def CloseClick(self):
        if(self.pptid<0): return
        pptdll.ClosePPT(self.pptid)
        self.pptid = -1
        app.processEvents()

    def OpenClick(self):
        oldid = self.pptid;
        rect = RECT(100,100,900,700)
        filename = str(self.PPTEdit.text().replace(u'/', u'\\'))        
        print filename
        self.pptid = pptdll.OpenPPT(filename, None, rect, 'c:\\temp\\slide')
        print "id: " + unicode(self.pptid)
        if oldid>=0:
            pptdll.ClosePPT(oldid);
        slides = pptdll.GetSlideCount(self.pptid)
        print "slidecount: " + unicode(slides)
        self.total.setNum(pptdll.GetSlideCount(self.pptid))
        self.UpdateCurrSlide()

    def UpdateCurrSlide(self):
        if(self.pptid<0): return
        slide = unicode(pptdll.GetCurrentSlide(self.pptid))
        print "currslide: " + slide
        self.slideEdit.setText(slide)
        app.processEvents()

    def GotoClick(self):
        if(self.pptid<0): return
        print self.slideEdit.text()
        pptdll.GotoSlide(self.pptid, int(self.slideEdit.text()))
        self.UpdateCurrSlide()
        app.processEvents()

    def OpenDialog(self):
        self.PPTEdit.setText(QtGui.QFileDialog.getOpenFileName(self, 'Open file'))

if __name__ == '__main__':
    #pptdll = cdll.LoadLibrary(r'C:\Documents and Settings\jonathan\Desktop\pptviewlib.dll')
    pptdll = cdll.LoadLibrary(r'pptviewlib.dll')
    pptdll.SetDebug(1)
    print "Begin..."
    app = QtGui.QApplication(sys.argv)
    qb = PPTViewer()
    qb.show()
    sys.exit(app.exec_())
