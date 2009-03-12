from PyQt4 import QtCore, QtGui
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-30s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')

console=logging.StreamHandler()
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)24s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
log=logging.getLogger('')

logging.info("Logging started")
import os, sys
mypath=os.path.split(os.path.abspath(__file__))[0]

sys.path.insert(0,(os.path.join(mypath, '..' ,'..', '..')))
from openlp.core.lib import MediaManagerItem
class TestMediaManager:
    def setup_class(self):
        self.app = QtGui.QApplication([])
        logging.info ("App is " + str(self.app))
        self.main_window = QtGui.QMainWindow()
        self.main_window.resize(200, 600)
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
        self.MediaManagerContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MediaManagerContents.sizePolicy().hasHeightForWidth())
        self.MediaManagerContents.setSizePolicy(sizePolicy)
        self.MediaManagerLayout = QtGui.QHBoxLayout(self.MediaManagerContents)
        self.MediaManagerLayout.setContentsMargins(0, 2, 0, 0)
        self.MediaToolBox = QtGui.QToolBox(self.MediaManagerContents)
        self.MediaManagerDock.setWidget(self.MediaManagerContents)
        self.main_window.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.MediaManagerDock)
        self.MediaManagerLayout.addWidget(self.MediaToolBox)
    def test1(self):
        log=logging.getLogger("test1")
        log.info("Start")
        i1=MediaManagerItem(self.MediaToolBox)
        i2=MediaManagerItem(self.MediaToolBox)
        log.info("i1"+str(i1))
        log.info("i2"+str(i2))
        i1.addToolbar()
        i1.addToolbarButton("Test1", "Test1", None)
        i2.addToolbar()
        i2.addToolbarButton("Test2", "Test2", None)
        self.MediaToolBox.setItemText(self.MediaToolBox.indexOf(i1), QtGui.QApplication.translate("main_window", "Item1", None, QtGui.QApplication.UnicodeUTF8))
        self.MediaToolBox.setItemText(self.MediaToolBox.indexOf(i2), QtGui.QApplication.translate("main_window", "Item2", None, QtGui.QApplication.UnicodeUTF8))
        log.info("Show window")
        self.main_window.show()
        log.info("End")
        return 1

if __name__=="__main__":
    t=TestMediaManager()
    t.setup_class()
    t.test1()
    log.info("exec")
    sys.exit(t.app.exec_())
