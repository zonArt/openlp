from openlp.core import Renderer
from openlp.theme import Theme
import sys
import time

from PyQt4 import QtGui, QtCore
words="""How sweet the name of Jesus sounds
In a believer's ear!
It soothes his sorrows, heals his wounds,
And drives away his fear.
"""

class TstFrame(QtGui.QMainWindow):
    """ We simply derive a new class of QMainWindow"""

    # {{{ init

    def __init__(self, *args, **kwargs):
        """Create the DemoPanel."""
        QtGui.QMainWindow.__init__(self)
        self.resize(1024,768)
        self.size=(1024,768)
        
        self.v=0
        self._font=QtGui.QFont('Decorative', 32)
        self.framecount=0
        self.totaltime = 0
        self.dir=1
        self.y=1
#         self.startTimer(10)
        self.frame=QtGui.QFrame()
        self.setCentralWidget(self.frame)
        self.r=Renderer()
        self.r.set_theme(Theme('demo_theme.xml'))
        
        self.r.set_text_rectangle(self.frame.frameRect())
        self.r.set_paint_dest(self)
        self.r.set_words_openlp(words)
    def timerEvent(self, event):
        self.update()
    def paintEvent(self, event):
        self.r.set_text_rectangle(self.frame.frameRect())
        self.r.scale_bg_image()
        t1=time.clock()
        self.r.render_screen(0)
        t2 = time.clock()
        deltat=t2-t1
        self.totaltime += deltat
        self.framecount+=1
        print "Timing result: %5.3ffps" %(self.framecount/float(self.totaltime))
        
    # }}}

class Demo:
    def __init__(self):
        app = QtGui.QApplication(sys.argv)
        main=TstFrame()
        main.show()
        sys.exit(app.exec_())


if __name__=="__main__":
    t=Demo()

