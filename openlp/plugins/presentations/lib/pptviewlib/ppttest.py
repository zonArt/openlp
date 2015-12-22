# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2015 OpenLP Developers                                   #
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
from PyQt5 import QtWidgets
from ctypes import *
from ctypes.wintypes import RECT


class PPTViewer(QtWidgets.QWidget):
    """
    Standalone Test Harness for the pptviewlib library
    """
    def __init__(self, parent=None):
        super(PPTViewer, self).__init__(parent)
        self.pptid = -1
        self.setWindowTitle('PowerPoint Viewer Test')

        ppt_label = QtWidgets.QLabel('Open PowerPoint file')
        slide_label = QtWidgets.QLabel('Go to slide #')
        self.pptEdit = QtWidgets.QLineEdit()
        self.slideEdit = QtWidgets.QLineEdit()
        x_label = QtWidgets.QLabel('X pos')
        y_label = QtWidgets.QLabel('Y pos')
        width_label = QtWidgets.QLabel('Width')
        height_label = QtWidgets.QLabel('Height')
        self.xEdit = QtWidgets.QLineEdit('100')
        self.yEdit = QtWidgets.QLineEdit('100')
        self.widthEdit = QtWidgets.QLineEdit('900')
        self.heightEdit = QtWidgets.QLineEdit('700')
        self.total = QtWidgets.QLabel()
        ppt_btn = QtWidgets.QPushButton('Open')
        ppt_dlg_btn = QtWidgets.QPushButton('...')
        folder_label = QtWidgets.QLabel('Slide .bmp path')
        self.folderEdit = QtWidgets.QLineEdit('slide')
        slide_btn = QtWidgets.QPushButton('Go')
        prev = QtWidgets.QPushButton('Prev')
        next = QtWidgets.QPushButton('Next')
        blank = QtWidgets.QPushButton('Blank')
        unblank = QtWidgets.QPushButton('Unblank')
        restart = QtWidgets.QPushButton('Restart')
        close = QtWidgets.QPushButton('Close')
        resume = QtWidgets.QPushButton('Resume')
        stop = QtWidgets.QPushButton('Stop')
        grid = QtWidgets.QGridLayout()
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
        ppt_btn.clicked.connect(self.openClick)
        ppt_dlg_btn.clicked.connect(self.openDialog)
        slide_btn.clicked.connect(self.gotoClick)
        prev.clicked.connect(self.prevClick)
        next.clicked.connect(self.nextClick)
        blank.clicked.connect(self.blankClick)
        unblank.clicked.connect(self.unblankClick)
        restart.clicked.connect(self.restartClick)
        close.clicked.connect(self.closeClick)
        stop.clicked.connect(self.stopClick)
        resume.clicked.connect(self.resumeClick)
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
        oldid = self.pptid
        rect = RECT(int(self.xEdit.text()), int(self.yEdit.text()),
                    int(self.widthEdit.text()), int(self.heightEdit.text()))
        filename = str(self.pptEdit.text().replace('/', '\\'))
        folder = str(self.folderEdit.text().replace('/', '\\'))
        print(filename, folder)
        self.pptid = self.pptdll.OpenPPT(filename, None, rect, folder)
        print('id: ' + str(self.pptid))
        if oldid >= 0:
            self.pptdll.ClosePPT(oldid)
        slides = self.pptdll.GetSlideCount(self.pptid)
        print('slidecount: ' + str(slides))
        self.total.setNum(self.pptdll.GetSlideCount(self.pptid))
        self.updateCurrSlide()

    def updateCurrSlide(self):
        if self.pptid < 0:
            return
        slide = str(self.pptdll.GetCurrentSlide(self.pptid))
        print('currslide: ' + slide)
        self.slideEdit.setText(slide)
        app.processEvents()

    def gotoClick(self):
        if self.pptid < 0:
            return
        print(self.slideEdit.text())
        self.pptdll.GotoSlide(self.pptid, int(self.slideEdit.text()))
        self.updateCurrSlide()
        app.processEvents()

    def openDialog(self):
        self.pptEdit.setText(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')[0])

if __name__ == '__main__':
    pptdll = cdll.LoadLibrary(r'pptviewlib.dll')
    pptdll.SetDebug(1)
    print('Begin...')
    app = QtWidgets.QApplication(sys.argv)
    window = PPTViewer()
    window.pptdll = pptdll
    window.show()
    sys.exit(app.exec())
