import os
import sys
mypath=os.path.split(os.path.abspath(__file__))[0]

sys.path.insert(0,(os.path.join(mypath, '..' ,'..', '..')))
print sys.path

from openlp.theme import Theme
import os.path
from PyQt4 import QtGui
def test_read_theme():
    dir=os.path.split(__file__)[0]
    # test we can read a theme
    t=Theme(os.path.join(dir, "test_theme.xml"))
    print t
    assert(t.BackgroundParameter1 == "sunset1.jpg")
    assert(t.BackgroundParameter2 == None)
    assert(t.BackgroundParameter3 == None)
    assert(t.BackgroundType == 2)
    assert(t.FontColor == QtGui.QColor(255,255,255))
    assert(t.FontName == "Tahoma")
    assert(t.FontProportion == 16)
    assert(t.HorizontalAlign == 2)
    assert(t.Name == "openlp.org Packaged Theme")
    assert(t.Outline == -1)
    assert(t.OutlineColor == QtGui.QColor(255,0,0))
    assert(t.Shadow == -1)
    assert(t.ShadowColor == QtGui.QColor(0,0,1))
    assert(t.VerticalAlign == 0)
    # test we create a "blank" theme correctly
    t=Theme()
    print t
    assert(t.BackgroundParameter1 == QtGui.QColor(0,0,0))
    assert(t.BackgroundParameter2 == None)
    assert(t.BackgroundParameter3 == None)
    assert(t.BackgroundType == 0)
    assert(t.FontColor == QtGui.QColor(255,255,255))
    assert(t.FontName == "Arial")
    assert(t.FontProportion == 30)
    assert(t.HorizontalAlign == 0)
    assert(t.Name == "BlankStyle")
    assert(t.Outline == 0)
    assert(t.Shadow == 0)
    assert(t.VerticalAlign == 0)

 
    print "Tests passed"

def test_theme():
    test_read_theme()
    
if __name__=="__main__":
    test_read_theme()
