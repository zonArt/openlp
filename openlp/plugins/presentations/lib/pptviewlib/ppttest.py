import sys
from PyQt4 import QtGui, QtCore
from ctypes import *
from ctypes.wintypes import RECT

class PPTViewer(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.pptid = -1
        self.setWindowTitle('PowerPoint Viewer Test')

        PPTLabel = QtGui.QLabel('Open PowerPoint file')
        slideLabel = QtGui.QLabel('Go to slide #')
        self.PPTEdit = QtGui.QLineEdit()
        self.slideEdit = QtGui.QLineEdit()
        self.total = QtGui.QLabel()
        PPTBtn = QtGui.QPushButton("Open")
        PPTDlgBtn = QtGui.QPushButton("...")
        slideBtn = QtGui.QPushButton("Go")
        prev = QtGui.QPushButton("Prev")
        next = QtGui.QPushButton("Next")
        blank = QtGui.QPushButton("Blank")
        unblank = QtGui.QPushButton("Unblank")
        restart = QtGui.QPushButton("Restart")
        close = QtGui.QPushButton("Close")
        resume = QtGui.QPushButton("Resume")
        stop = QtGui.QPushButton("Stop")
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
        self.connect(PPTBtn, QtCore.SIGNAL('clicked()'), self.OpenClick)
        self.connect(PPTDlgBtn, QtCore.SIGNAL('clicked()'), self.OpenDialog)
        self.connect(slideBtn, QtCore.SIGNAL('clicked()'), self.GotoClick)
        self.connect(prev, QtCore.SIGNAL('clicked()'), self.PrevClick)
        self.connect(next, QtCore.SIGNAL('clicked()'), self.NextClick)
        self.connect(blank, QtCore.SIGNAL('clicked()'), self.BlankClick)
        self.connect(unblank, QtCore.SIGNAL('clicked()'), self.UnblankClick)
        self.connect(restart, QtCore.SIGNAL('clicked()'), self.RestartClick)
        self.connect(close, QtCore.SIGNAL('clicked()'), self.CloseClick)
        self.connect(stop, QtCore.SIGNAL('clicked()'), self.StopClick)
        self.connect(resume, QtCore.SIGNAL('clicked()'), self.ResumeClick)

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
        filename = str(self.PPTEdit.text())
        print filename
        self.pptid = pptdll.OpenPPT(filename, None, rect, "c:\\temp\\slide")
        print "id: " + str(self.pptid)
        if oldid>=0:
            pptdll.ClosePPT(oldid);
        slides = pptdll.GetSlideCount(self.pptid)
        print "slidecount: " + str(slides)
        self.total.setNum(pptdll.GetSlideCount(self.pptid))
        self.UpdateCurrSlide()
            
    def UpdateCurrSlide(self):
        if(self.pptid<0): return
        slide = str(pptdll.GetCurrentSlide(self.pptid))
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
    #pptdll = cdll.LoadLibrary(r"C:\Documents and Settings\jonathan\Desktop\pptviewlib.dll")
    pptdll = cdll.LoadLibrary(r"pptviewlib.dll")
    pptdll.SetDebug(1)
    print "Begin..."
    app = QtGui.QApplication(sys.argv)
    qb = PPTViewer()
    qb.show()
    sys.exit(app.exec_())

