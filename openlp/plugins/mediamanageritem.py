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
        if statustip is None:
            statustip=tooltiptext
        self.setToolTip(QtGui.QApplication.translate("main_window", tooltiptext, None, QtGui.QApplication.UnicodeUTF8))
        self.setText(QtGui.QApplication.translate("main_window", tooltiptext, None, QtGui.QApplication.UnicodeUTF8))
        self.setStatusTip(QtGui.QApplication.translate("main_window", statustip, None, QtGui.QApplication.UnicodeUTF8))

class MediaManagerItem(QtGui.QWidget):
    log=logging.getLogger("MediaMgrItem")
    log.info("loaded")
    name="Default_Item"
#     iconname=":/media/media_video.png" # xxx change this to some default bare icon
    iconname=None
    iconfile=os.path.join(mypath, "red-x.png")
    def __init__(self):
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

        self.SongToolbar = QtGui.QWidget(self)
        self.SongToolbar.setObjectName("SongToolbar")
        self.SongToolbarLayout = QtGui.QHBoxLayout(self.SongToolbar)
        self.SongToolbarLayout.setSpacing(0)
        self.SongToolbarLayout.setMargin(0)
        self.SongToolbarLayout.setObjectName("SongToolbarLayout")
        self.SongNewItem = QtGui.QToolButton(self.SongToolbar)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/songs/song_new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SongNewItem.setIcon(icon1)
        self.SongNewItem.setIconSize(QtCore.QSize(20, 20))
        self.SongNewItem.setAutoRaise(True)
        self.SongNewItem.setObjectName("SongNewItem")
        self.SongToolbarLayout.addWidget(self.SongNewItem)

        self.SongEditItem = QtGui.QToolButton(self.SongToolbar)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/songs/song_edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SongEditItem.setIcon(icon2)
        self.SongEditItem.setIconSize(QtCore.QSize(20, 20))
        self.SongEditItem.setAutoRaise(True)
        self.SongEditItem.setObjectName("SongEditItem")
        self.SongToolbarLayout.addWidget(self.SongEditItem)
        self.SongDeleteItem = QtGui.QToolButton(self.SongToolbar)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/songs/song_delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SongDeleteItem.setIcon(icon3)
        self.SongDeleteItem.setIconSize(QtCore.QSize(20, 20))
        self.SongDeleteItem.setAutoRaise(True)
        self.SongDeleteItem.setObjectName("SongDeleteItem")
        self.SongToolbarLayout.addWidget(self.SongDeleteItem)
        self.SongLine = QtGui.QFrame(self.SongToolbar)
        self.SongLine.setMinimumSize(QtCore.QSize(0, 0))
        self.SongLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.SongLine.setLineWidth(1)
        self.SongLine.setMidLineWidth(0)
        self.SongLine.setFrameShape(QtGui.QFrame.VLine)
        self.SongLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.SongLine.setObjectName("SongLine")
        self.SongToolbarLayout.addWidget(self.SongLine)
        self.SongPreviewItem = QtGui.QToolButton(self.SongToolbar)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/system/system_preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SongPreviewItem.setIcon(icon4)
        self.SongPreviewItem.setIconSize(QtCore.QSize(20, 20))
        self.SongPreviewItem.setAutoRaise(True)
        self.SongPreviewItem.setObjectName("SongPreviewItem")
        self.SongToolbarLayout.addWidget(self.SongPreviewItem)
        self.SongLiveItem = QtGui.QToolButton(self.SongToolbar)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/system/system_live.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SongLiveItem.setIcon(icon5)
        self.SongLiveItem.setIconSize(QtCore.QSize(20, 20))
        self.SongLiveItem.setAutoRaise(True)
        self.SongLiveItem.setObjectName("SongLiveItem")
        self.SongToolbarLayout.addWidget(self.SongLiveItem)
        self.SongAddItem = QtGui.QToolButton(self.SongToolbar)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/system/system_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SongAddItem.setIcon(icon6)
        self.SongAddItem.setIconSize(QtCore.QSize(20, 20))
        self.SongAddItem.setAutoRaise(True)
        self.SongAddItem.setObjectName("SongAddItem")
        self.SongToolbarLayout.addWidget(self.SongAddItem)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.SongToolbarLayout.addItem(spacerItem)
        self.Layout.addWidget(self.SongToolbar)
        self.SongList = QtGui.QTableWidget(self)
        self.SongList.setObjectName("SongList")
        self.SongList.setColumnCount(0)
        self.SongList.setRowCount(0)
        self.Layout.addWidget(self.SongList)

        # Connect the dots! I mean, slots...
        QtCore.QObject.connect(self.SongNewItem, QtCore.SIGNAL("clicked()"), self.onSongNewItemClick)

    #
    #    # setup toolbar
    #    self.Toolbar = QtGui.QWidget(self)
    #    self.ToolbarLayout = QtGui.QHBoxLayout(self.Toolbar)
    #    self.ToolbarLayout.setSpacing(0)
    #    self.ToolbarLayout.setMargin(0)
    #
    #    self.log.info("Adding toolbar item")
    #    self.ToolbarButtons=[]
    #    self.ToolbarButtons.append(ToolbarButton(self, "LoadItem", ":/images/image_load.png", "Load something", "Load something in"))
    #    self.ToolbarButtons.append(ToolbarButton(self, "DeleteItem", ":/images/image_delete.png", "Delete something", "Delete something from"))
    #
    #    # xxx button events
    #    QtCore.QObject.connect(self.ToolbarButtons[0], QtCore.SIGNAL("clicked()"), self.LoadItemclicked)
    #    QtCore.QObject.connect(self.ToolbarButtons[1], QtCore.SIGNAL("clicked()"), self.DeleteItemclicked)
    #    # add somewhere for "choosing" to happen
    #    self.choose_area=QtGui.QWidget(self)
    #    self.Layout.addWidget(self.choose_area)
    #    self.choose_area.text="Stuff and Nonsense"

    def onSongNewItemClick(self):
        self.log.info("onSongNewItemClick")

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



         # add items
#         self.LoadItem = QtGui.QToolButton(self.Toolbar)
#         icon17 = QtGui.QIcon()
#         icon17.addPixmap(QtGui.QPixmap(":/images/image_load.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

#         self.LoadItem.setIcon(icon17)
#         self.LoadItem.setIconSize(QtCore.QSize(20, 20))
#         self.LoadItem.setAutoRaise(True)
#         self.LoadItem.setObjectName("LoadItem")
#         self.ToolbarLayout.addWidget(self.LoadItem)


#         self.ImageDeleteItem = QtGui.QToolButton(self.ImageToolbar)
#         icon18 = QtGui.QIcon()
#         icon18.addPixmap(QtGui.QPixmap(":/images/image_delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.ImageDeleteItem.setIcon(icon18)
#         self.ImageDeleteItem.setIconSize(QtCore.QSize(20, 20))
#         self.ImageDeleteItem.setAutoRaise(True)
#         self.ImageDeleteItem.setObjectName("ImageDeleteItem")
#         self.ImageToolbarLayout.addWidget(self.ImageDeleteItem)
#         self.ImageLine = QtGui.QFrame(self.ImageToolbar)
#         self.ImageLine.setFrameShape(QtGui.QFrame.VLine)
#         self.ImageLine.setFrameShadow(QtGui.QFrame.Sunken)
#         self.ImageLine.setObjectName("ImageLine")
#         self.ImageToolbarLayout.addWidget(self.ImageLine)
#         self.ImageLiveItem = QtGui.QToolButton(self.ImageToolbar)
#         self.ImageLiveItem.setIcon(icon5)
#         self.ImageLiveItem.setIconSize(QtCore.QSize(20, 20))
#         self.ImageLiveItem.setAutoRaise(True)
#         self.ImageLiveItem.setObjectName("ImageLiveItem")
#         self.ImageToolbarLayout.addWidget(self.ImageLiveItem)
#         self.ImageAddItem = QtGui.QToolButton(self.ImageToolbar)
#         self.ImageAddItem.setIcon(icon6)
#         self.ImageAddItem.setIconSize(QtCore.QSize(20, 20))
#         self.ImageAddItem.setAutoRaise(True)
#         self.ImageAddItem.setObjectName("ImageAddItem")
#         self.ImageToolbarLayout.addWidget(self.ImageAddItem)
#         spacerItem6 = QtGui.QSpacerItem(105, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
#         self.ImageToolbarLayout.addItem(spacerItem6)
#         self.Layout.addWidget(self.ImageToolbar)
#         self.ImageListView = QtGui.QListWidget(self.ImagePage)
#         self.ImageListView.setObjectName("ImageListView")
#         self.Layout.addWidget(self.ImageListView)
#         icon19 = QtGui.QIcon()
#         icon19.addPixmap(QtGui.QPixmap(":/media/media_image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.MediaToolBox.addItem(self.ImagePage, icon19, "")

#         self.ImageDeleteItem.setToolTip(QtGui.QApplication.translate("main_window", "Remove Video", None, QtGui.QApplication.UnicodeUTF8))
#         self.ImageDeleteItem.setText(QtGui.QApplication.translate("main_window", "Delete Image", None, QtGui.QApplication.UnicodeUTF8))
#         self.ImageLiveItem.setToolTip(QtGui.QApplication.translate("main_window", "Go Live!", None, QtGui.QApplication.UnicodeUTF8))
#         self.ImageAddItem.setToolTip(QtGui.QApplication.translate("main_window", "Add to Order of Service", None, QtGui.QApplication.UnicodeUTF8))
#         self.MediaToolBox.setItemText(self.MediaToolBox.indexOf(self.ImagePage), QtGui.QApplication.translate("main_window", "Images", None, QtGui.QApplication.UnicodeUTF8))

        #self.log.info("done init")

