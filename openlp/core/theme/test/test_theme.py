import os
import os.path
import sys

from PyQt4 import QtGui

from openlp.core.theme import Theme

mypath = os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0, (os.path.join(mypath, '..', '..', '..', '..')))

print sys.path

def test_read_theme():
    dir = os.path.split(__file__)[0]
    # test we can read a theme
    theme = Theme(os.path.join(dir, 'test_theme.xml'))
    print theme
    assert(theme.BackgroundParameter1 == 'sunset1.jpg')
    assert(theme.BackgroundParameter2 is None)
    assert(theme.BackgroundParameter3 is None)
    assert(theme.BackgroundType == 2)
    assert(theme.FontColor == QtGui.QColor(255,255,255))
    assert(theme.FontName == 'Tahoma')
    assert(theme.FontProportion == 16)
    assert(theme.FontUnits == 'pixels')
    assert(theme.HorizontalAlign == 2)
    assert(theme.Name == 'openlp.org Packaged Theme')
    assert(theme.Outline == -1)
    assert(theme.OutlineColor == QtGui.QColor(255,0,0))
    assert(theme.Shadow == -1)
    assert(theme.ShadowColor == QtGui.QColor(0,0,1))
    assert(theme.VerticalAlign == 0)

def test_theme():
    # test we create a "blank" theme correctly
    theme = Theme()
    print theme
    assert(theme.BackgroundParameter1 == QtGui.QColor(0,0,0))
    assert(theme.BackgroundParameter2 is None)
    assert(theme.BackgroundParameter3 is None)
    assert(theme.BackgroundType == 0)
    assert(theme.FontColor == QtGui.QColor(255,255,255))
    assert(theme.FontName == 'Arial')
    assert(theme.FontProportion == 30)
    assert(theme.HorizontalAlign == 0)
    assert(theme.FontUnits == 'pixels')
    assert(theme.Name == 'BlankStyle')
    assert(theme.Outline == 0)
    assert(theme.Shadow == 0)
    assert(theme.VerticalAlign == 0)
 
    print "Tests passed"

if __name__ == "__main__":
    test_read_theme()
    test_theme()
