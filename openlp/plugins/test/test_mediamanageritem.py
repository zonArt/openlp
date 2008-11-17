from PyQt4 import QtCore, QtGui
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')

console=logging.StreamHandler()
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
log=logging.getLogger('')

logging.info("Logging started")
import os, sys
mypath=os.path.split(os.path.abspath(__file__))[0]

sys.path.insert(0,(os.path.join(mypath, '..' ,'..', '..')))
from openlp.plugins import MediaManagerItem
class TestMediaManager:
    def setup_class(self):
        self.app = QtGui.QApplication([])
        logging.info ("App is " + str(self.app))
        self.main_window = QtGui.QMainWindow()
        self.main_window.resize(800, 600)
#         self.StatusBar = QtGui.QStatusBar(self.main_window)
#         self.StatusBar.setObjectName("StatusBar")
#         self.main_window.setStatusBar(self.StatusBar)
        self.MediaManagerDock = QtGui.QDockWidget(self.main_window)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MediaManagerDock.sizePolicy().hasHeightForWidth())
        self.MediaManagerDock.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/system/system_mediamanager.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MediaManagerDock.setWindowIcon(icon)
        self.MediaManagerDock.setFloating(False)
#         self.MediaManagerDock.setObjectName("MediaManagerDock")
        self.MediaManagerContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MediaManagerContents.sizePolicy().hasHeightForWidth())
        self.MediaManagerContents.setSizePolicy(sizePolicy)
#         self.MediaManagerContents.setObjectName("MediaManagerContents")
        self.MediaManagerLayout = QtGui.QHBoxLayout(self.MediaManagerContents)
        self.MediaManagerLayout.setContentsMargins(0, 2, 0, 0)
#         self.MediaManagerLayout.setObjectName("MediaManagerLayout")
        self.MediaToolBox = QtGui.QToolBox(self.MediaManagerContents)
#         self.MediaToolBox.setObjectName("MediaToolBox")
        self.MediaManagerDock.setWidget(self.MediaManagerContents)
        self.main_window.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.MediaManagerDock)
        self.MediaManagerLayout.addWidget(self.MediaToolBox)
    def test1(self):
        log=logging.getLogger("test1")
        log.info("Start")
        i1=MediaManagerItem()
        i2=MediaManagerItem()
        log.info("i1"+str(i1))
        log.info("i2"+str(i2))
        self.MediaToolBox.addItem(i1, i1.icon, "Test1")
        self.MediaToolBox.addItem(i2, i2.icon, "Test2")
        self.MediaToolBox.setItemText(self.MediaToolBox.indexOf(i1), QtGui.QApplication.translate("main_window", "Item1", None, QtGui.QApplication.UnicodeUTF8))
        self.MediaToolBox.setItemText(self.MediaToolBox.indexOf(i2), QtGui.QApplication.translate("main_window", "Item2", None, QtGui.QApplication.UnicodeUTF8))
        log.info("Show window")
        self.main_window.show()
#         self.app.exec_()
        log.info("End")
        return 1
    
if __name__=="__main__":
    t=TestMediaManager()
    t.setup_class()
    t.test1()
    log.info("exec")
    t.app.exec_()
