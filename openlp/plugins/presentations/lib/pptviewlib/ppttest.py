# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
    """
    Standalone Test Harness for the pptviewlib library
    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.pptid = -1
        self.setWindowTitle(u'PowerPoint Viewer Test')

        ppt_label = QtGui.QLabel(u'Open PowerPoint file')
        slide_label = QtGui.QLabel(u'Go to slide #')
        self.pptEdit = QtGui.QLineEdit()
        self.slideEdit = QtGui.QLineEdit()
        x_label = QtGui.QLabel(u'X pos')
        y_label = QtGui.QLabel(u'Y pos')
        width_label = QtGui.QLabel(u'Width')
        height_label = QtGui.QLabel(u'Height')
        self.xEdit = QtGui.QLineEdit(u'100')
        self.yEdit = QtGui.QLineEdit(u'100')
        self.widthEdit = QtGui.QLineEdit(u'900')
        self.heightEdit = QtGui.QLineEdit(u'700')
        self.total = QtGui.QLabel()
        ppt_btn = QtGui.QPushButton(u'Open')
        ppt_dlg_btn = QtGui.QPushButton(u'...')
        folder_label = QtGui.QLabel(u'Slide .bmp path')
        self.folderEdit = QtGui.QLineEdit(u'slide')
        slide_btn = QtGui.QPushButton(u'Go')
        prev = QtGui.QPushButton(u'Prev')
        next = QtGui.QPushButton(u'Next')
        blank = QtGui.QPushButton(u'Blank')
        unblank = QtGui.QPushButton(u'Unblank')
        restart = QtGui.QPushButton(u'Restart')
        close = QtGui.QPushButton(u'Close')
        resume = QtGui.QPushButton(u'Resume')
        stop = QtGui.QPushButton(u'Stop')
        grid = QtGui.QGridLayout()
        row = 0
        grid.addWidget(folder_label, 0, 0)
        grid.addWidget(self.folderEdit, 0, 1)
        row += 1
        grid.addWidget(x_label, row, 0)
        grid.addWidget(self.xEdit, row, 1)
        grid.addWidget(y_label, row, 2)
        grid.addWidget(self.yEdit, row, 3)
        row += 1
        grid.addWidget(width_label, row, 0)
        grid.addWidget(self.widthEdit, row, 1)
        grid.addWidget(height_label, row, 2)
        grid.addWidget(self.heightEdit, row, 3)
        row += 1
        grid.addWidget(ppt_label, row, 0)
        grid.addWidget(self.pptEdit, row, 1)
        grid.addWidget(ppt_dlg_btn, row, 2)
        grid.addWidget(ppt_btn, row, 3)
        row += 1
        grid.addWidget(slide_label, row, 0)
        grid.addWidget(self.slideEdit, row, 1)
        grid.addWidget(slide_btn, row, 2)
        row += 1
        grid.addWidget(prev, row, 0)
        grid.addWidget(next, row, 1)
        row += 1
        grid.addWidget(blank, row, 0)
        grid.addWidget(unblank, row, 1)
        row += 1
        grid.addWidget(restart, row, 0)
        grid.addWidget(close, row, 1)
        row += 1
        grid.addWidget(stop, row, 0)
        grid.addWidget(resume, row, 1)
        self.connect(ppt_btn, QtCore.SIGNAL(u'clicked()'), self.openClick)
        self.connect(ppt_dlg_btn, QtCore.SIGNAL(u'clicked()'), self.openDialog)
        self.connect(slide_btn, QtCore.SIGNAL(u'clicked()'), self.gotoClick)
        self.connect(prev, QtCore.SIGNAL(u'clicked()'), self.prevClick)
        self.connect(next, QtCore.SIGNAL(u'clicked()'), self.nextClick)
        self.connect(blank, QtCore.SIGNAL(u'clicked()'), self.blankClick)
        self.connect(unblank, QtCore.SIGNAL(u'clicked()'), self.unblankClick)
        self.connect(restart, QtCore.SIGNAL(u'clicked()'), self.restartClick)
        self.connect(close, QtCore.SIGNAL(u'clicked()'), self.closeClick)
        self.connect(stop, QtCore.SIGNAL(u'clicked()'), self.stopClick)
        self.connect(resume, QtCore.SIGNAL(u'clicked()'), self.resumeClick)
        self.setLayout(grid)
        self.resize(300, 150)

    def prevClick(self):
        if self.pptid < 0:
            return
        self.pptdll.PrevStep(self.pptid)
        self.updateCurrSlide()
        app.processEvents()

    def nextClick(self):
        if self.pptid < 0:
            return
        self.pptdll.NextStep(self.pptid)
        self.updateCurrSlide()
        app.processEvents()

    def blankClick(self):
        if self.pptid < 0:
            return
        self.pptdll.Blank(self.pptid)
        app.processEvents()

    def unblankClick(self):
        if self.pptid < 0:
            return
        self.pptdll.Unblank(self.pptid)
        app.processEvents()

    def restartClick(self):
        if self.pptid < 0:
            return
        self.pptdll.RestartShow(self.pptid)
        self.updateCurrSlide()
        app.processEvents()

    def stopClick(self):
        if self.pptid < 0:
            return
        self.pptdll.Stop(self.pptid)
        app.processEvents()

    def resumeClick(self):
        if self.pptid < 0:
            return
        self.pptdll.Resume(self.pptid)
        app.processEvents()

    def closeClick(self):
        if self.pptid < 0:
            return
        self.pptdll.ClosePPT(self.pptid)
        self.pptid = -1
        app.processEvents()

    def openClick(self):
        oldid = self.pptid;
        rect = RECT(int(self.xEdit.text()), int(self.yEdit.text()),
            int(self.widthEdit.text()), int(self.heightEdit.text()))
        filename = str(self.pptEdit.text().replace(u'/', u'\\'))
        folder = str(self.folderEdit.text().replace(u'/', u'\\'))
        print filename, folder
        self.pptid = self.pptdll.OpenPPT(filename, None, rect, folder)
        print u'id: ' + unicode(self.pptid)
        if oldid >= 0:
            self.pptdll.ClosePPT(oldid);
        slides = self.pptdll.GetSlideCount(self.pptid)
        print u'slidecount: ' + unicode(slides)
        self.total.setNum(self.pptdll.GetSlideCount(self.pptid))
        self.updateCurrSlide()

    def updateCurrSlide(self):
        if self.pptid < 0:
            return
        slide = unicode(self.pptdll.GetCurrentSlide(self.pptid))
        print u'currslide: ' + slide
        self.slideEdit.setText(slide)
        app.processEvents()

    def gotoClick(self):
        if self.pptid < 0:
            return
        print self.slideEdit.text()
        self.pptdll.GotoSlide(self.pptid, int(self.slideEdit.text()))
        self.updateCurrSlide()
        app.processEvents()

    def openDialog(self):
        self.pptEdit.setText(QtGui.QFileDialog.getOpenFileName(self,
            u'Open file'))

if __name__ == '__main__':
    pptdll = cdll.LoadLibrary(r'pptviewlib.dll')
    pptdll.SetDebug(1)
    print u'Begin...'
    app = QtGui.QApplication(sys.argv)
    window = PPTViewer()
    window.pptdll = pptdll
    window.show()
    sys.exit(app.exec_())
