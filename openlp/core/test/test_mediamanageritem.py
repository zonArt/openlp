import logging
import os
import sys

from PyQt4 import QtCore, QtGui

from openlp.core.lib import MediaManagerItem

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-30s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')

console=logging.StreamHandler()
# set a format which is simpler for console use
formatter = logging.Formatter(u'%(name)24s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
logging.getLogger(u'').addHandler(console)
log = logging.getLogger(u'')
logging.info(u'Logging started')
mypath = os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..' ,'..', '..')))

class TestMediaManager:
    def setup_class(self):
        self.app = QtGui.QApplication([])
        logging.info (u'App is ' + unicode(self.app))
        self.main_window = QtGui.QMainWindow()
        self.main_window.resize(200, 600)
        self.MediaManagerDock = QtGui.QDockWidget(self.main_window)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
	    QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
	    self.MediaManagerDock.sizePolicy().hasHeightForWidth())
        self.MediaManagerDock.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/system/system_mediamanager.png'),
	    QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MediaManagerDock.setWindowIcon(icon)
        self.MediaManagerDock.setFloating(False)
        self.MediaManagerContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
	    QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
	    self.MediaManagerContents.sizePolicy().hasHeightForWidth())
        self.MediaManagerContents.setSizePolicy(sizePolicy)
        self.MediaManagerLayout = QtGui.QHBoxLayout(self.MediaManagerContents)
        self.MediaManagerLayout.setContentsMargins(0, 2, 0, 0)
        self.MediaToolBox = QtGui.QToolBox(self.MediaManagerContents)
        self.MediaManagerDock.setWidget(self.MediaManagerContents)
        self.main_window.addDockWidget(QtCore.Qt.DockWidgetArea(1),
	    self.MediaManagerDock)
        self.MediaManagerLayout.addWidget(self.MediaToolBox)
    def test1(self):
        log=logging.getLogger(u'test1')
        log.info(u'Start')
        i1=MediaManagerItem(self.MediaToolBox)
        i2=MediaManagerItem(self.MediaToolBox)
        log.info(u'i1'+unicode(i1))
        log.info(u'i2'+unicode(i2))
        i1.addToolbar()
        i1.addToolbarButton(u'Test1', u'Test1', None)
        i2.addToolbar()
        i2.addToolbarButton(u'Test2', u'Test2', None)
        self.MediaToolBox.setItemText(self.MediaToolBox.indexOf(i1),
	    translate(u'main_window', u'Item1'))
        self.MediaToolBox.setItemText(self.MediaToolBox.indexOf(i2),
	    translate(u'main_window', u'Item2'))
        log.info(u'Show window')
        self.main_window.show()
        log.info(u'End')
        return 1

if __name__ == "__main__":
    t=TestMediaManager()
    t.setup_class()
    t.test1()
    log.info(u'exec')
    sys.exit(t.app.exec_())
