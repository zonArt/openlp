from PyQt4 import QtCore, QtGui
from openlp.resources import *
# from openlp.plugins import Plugin
import logging

class ToolbarButton(QtGui.QToolButton):
    log=logging.getLogger("ToolbarBtn")
    log.info("loaded")
    def __init__(self, parent, name, pixmap, tooltiptext, statustip=None):
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
        # xxx button events
        
class MediaManagerItem(QtGui.QWidget):
    log=logging.getLogger("MediaMgrItem")
    log.info("loaded")
    name="Default_Item"
    iconname=":/media/media_video.png" # xxx change this to some default bare icon
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.log.info("init")
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(self.iconname), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.Layout = QtGui.QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)

        # setup toolbar
        self.Toolbar = QtGui.QWidget(self)
        self.ToolbarLayout = QtGui.QHBoxLayout(self.Toolbar)
        self.ToolbarLayout.setSpacing(0)
        self.ToolbarLayout.setMargin(0)

        self.log.info("Adding toolbar item")
        self.ToolbarButtons=[]
        self.ToolbarButtons.append(ToolbarButton(self, "LoadItem", ":/images/image_load.png", "Load something", "Load something in"))
        self.ToolbarButtons.append(ToolbarButton(self, "DeleteItem", ":/images/image_delete.png", "Delete something", "Delete something from"))

        # add somewhere for "choosing" to happen
        self.choose_area=QtGui.QWidget(self)
        self.Layout.addWidget(self.choose_area)
        self.choose_area.text="Stuff and Nonsense"

    def paintEvent(self, evt):
        paint = QtGui.QPainter()#self.choose_area)
        paint.begin(self)
        paint.setPen(QtGui.QColor(168, 34, 3))
        paint.setFont(QtGui.QFont('Decorative', 10))
        paint.drawText(evt.rect(), QtCore.Qt.AlignCenter, self.choose_area.text)
        paint.end()



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

        self.log.info("done init")
        
