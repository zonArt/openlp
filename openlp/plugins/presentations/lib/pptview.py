import sys
import win32api
from PyQt4 import QtGui, QtCore
from ctypes import *
from ctypes.wintypes import RECT

pptdll = cdll.LoadLibrary(r"C:\Documents and Settings\jonathan\My Documents\Personal\openlp\openlp-2\trunk\openlp\libraries\pptviewlib\pptviewlib.dll')

class BoxLayout(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.pptid = -1
        self.setWindowTitle(u'box layout')

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
        grid.addWidget(stop, 4, 1)
        grid.addWidget(resume, 4, 2)
        grid.addWidget(pptwindow, 5, 0, 10, 3)
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
        self.slideEdit.setText(pptdll.GetCurrentSlide(self.pptid))
    
    def NextClick(self):
        if(self.pptid<0): return
        pptdll.NextStep(self.pptid)
        self.slideEdit.setText(pptdll.GetCurrentSlide(self.pptid))
    
    def BlankClick(self):
        if(self.pptid<0): return
        pptdll.Blank(self.pptid)
    
    def UnblankClick(self):
        if(self.pptid<0): return
        pptdll.Unblank(self.pptid)
    
    def RestartClick(self):
        if(self.pptid<0): return
        pptdll.RestartShow(self.pptid)
        self.slideEdit.setText(pptdll.GetCurrentSlide(self.pptid))
    
    def StopClick(self):
        if(self.pptid<0): return
        pptdll.Stop(self.pptid)
    
    def ResumeClick(self):
        if(self.pptid<0): return
        pptdll.Resume(self.pptid)

    def CloseClick(self):
        if(self.pptid<0): return
        pptdll.Close(self.pptid)
        self.pptid = -1

    def OpenClick(self):
        if(self.pptid>=0):
            self.CloseClick()
        rect = RECT()
        rect.left = 100
        rect.top = 100
        rect.width = 900
        rect.hight = 700
        #self.pptid = pptdll.OpenPPT(self.PPTEdit.text, None, rect, "c:\temp\slide')
        self.pptid = pptdll.OpenPPT(u'C:\\test 1.ppt", None, rect, "c:\temp\slide')
        self.total.setText(pptdll.GetSlideCount(self.pptid))
        self.slideEdit.setText(unicode(pptdll.GetCurrentSlide(self.pptid)))

    def GotoClick(self):
        if(self.pptid<0): return
        pptdll.GotoSlide(self.pptid, self.slideEdit.text)
        self.slideEdit.setText(pptdll.GetCurrentSlide(self.pptid))

    def OpenDialog(self):
        self.PPTEdit.setText(QtGui.QFileDialog.getOpenFileName(self, 'Open file'))

app = QtGui.QApplication(sys.argv)
qb = BoxLayout()
qb.show()
sys.exit(app.exec_())