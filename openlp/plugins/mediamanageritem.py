from PyQt4 import QtCore, QtGui
from openlp.resources import *
# from openlp.plugins import Plugin
import logging

import os, sys
mypath=os.path.split(os.path.abspath(__file__))[0]
class ToolbarButton(QtGui.QToolButton):
    def __init__(self, parent, name, pixmap, tooltiptext, statustip=None):
        self.log=logging.getLogger("TlrBtn%s"% name)
        self.log.info("loaded")
        self.log.info("create '%s', '%s'"%(name, pixmap))
        QtGui.QToolButton.__init__(self, parent.Toolbar)
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(pixmap), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(self.icon)
        self.setIconSize(QtCore.QSize(20, 20))
        self.setAutoRaise(True)
#         self.setObjectName("%sItem"%name)
        parent.ToolbarLayout.addWidget(self)
#         if statustip is None:
#             statustip=tooltiptext
#         self.setToolTip(QtGui.QApplication.translate("main_window", tooltiptext, None, QtGui.QApplication.UnicodeUTF8))
#         self.setText(QtGui.QApplication.translate("main_window", tooltiptext, None, QtGui.QApplication.UnicodeUTF8))
#         self.setStatusTip(QtGui.QApplication.translate("main_window", statustip, None, QtGui.QApplication.UnicodeUTF8))

class MediaManagerItem(QtGui.QWidget):
    name="Default_Item"
#     iconname=":/media/media_video.png" # xxx change this to some default bare icon
    iconname=None
    iconfile=os.path.join(mypath, "red-x.png")
    def __init__(self, app):
        self.log=logging.getLogger("MediaMgrItem_%s"%self.name)
        self.log.info("loaded")
        QtGui.QWidget.__init__(self)
        self.log.info("init")
        self.icon = QtGui.QIcon()
        if self.iconname is not None:
            self.icon.addPixmap(QtGui.QPixmap(self.iconname), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        if self.iconfile is not None:
            self.icon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(self.iconfile)), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.Layout = QtGui.QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)

        self.Toolbar = QtGui.QWidget(self)
        self.ToolbarLayout = QtGui.QHBoxLayout(self.Toolbar)
        self.ToolbarLayout.setSpacing(0)
        self.ToolbarLayout.setMargin(0)

        # setup toolbar

        self.log.info("Adding toolbar item")
#         self.ToolbarButtons=[]
#         self.ToolbarButtons.append(ToolbarButton(self, "LoadItem", ":/images/image_load.png", "Load something", "Load something in"))
#         self.ToolbarButtons.append(ToolbarButton(self, "DeleteItem", ":/images/image_delete.png", "Delete something", "Delete something from"))
        b=QtGui.QToolButton.__init__(self, self.Toolbar)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/image_load.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        b.setIcon(icon)
        b.setIconSize(QtCore.QSize(20, 20))
        b.setAutoRaise(True)
#         self.setObjectName("%sItem"%name)
        self.ToolbarLayout.addWidget(b)

        # Connect the dots! I mean, slots...
#         QtCore.QObject.connect(self.SongNewItem, QtCore.SIGNAL("clicked()"), self.onSongNewItemClick)
        QtCore.QObject.connect(self.ToolbarButtons[0], QtCore.SIGNAL("clicked()"), self.LoadItemclicked)
        QtCore.QObject.connect(self.ToolbarButtons[1], QtCore.SIGNAL("clicked()"), self.DeleteItemclicked)

        # add somewhere for "choosing" to happen
#         self.choose_area=QtGui.QWidget(self)
#         self.Layout.addWidget(self.choose_area)
#         self.choose_area.text="Stuff and Nonsense"

#     def onSongNewItemClick(self):
#         self.log.info("onSongNewItemClick")
        # xxx button events
#         app.connect(self.ToolbarButtons[0], QtCore.SIGNAL("triggered()"), self.LoadItemclicked)
#         QtCore.QObject.connect(self.ToolbarButtons[1], QtCore.SIGNAL("triggered()"), self.DeleteItemclicked)
        # add somewhere for "choosing" to happen
#         self.choose_area=QtGui.QWidget(self)
#         self.Layout.addWidget(self.choose_area)
#         self.choose_area.text="Stuff and Nonsense"

    def LoadItemclicked(self):
        self.log.info("LoadItemClicked")
        #self.choose_area.text+="+"
    def DeleteItemclicked(self):
        self.log.info("DeleteItemClicked")
        #self.choose_area.text+="-"
    def paintEvent(self, evt):
        pass
        #paint = QtGui.QPainter()#self.choose_area)
        #paint.begin(self)
        #paint.setPen(QtGui.QColor(168, 34, 3))
        #paint.setFont(QtGui.QFont('Decorative', 10))
        #paint.drawText(evt.rect(), QtCore.Qt.AlignCenter, self.choose_area.text)
        #paint.end()

        self.log.info("done paint")
