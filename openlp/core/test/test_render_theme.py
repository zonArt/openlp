"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import sys
import os

from PyQt4 import QtGui, QtCore

from openlp.core.theme import Theme
from test_render import TestRender_base, whoami

pypath = os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0, (os.path.join(mypath, '..', '..', '..')))

def compare_images(goldenim, testim, threshold=0.01):
    # easy test first
    if goldenim == testim:
        return 1
    # how close are they?  Calculated the sum of absolute differences in
    # each channel of each pixel and divide by the number of pixels in the image
    # if this sum is < threshold, the images are deemed to be "close enough"
    sad=0;
    for x in range(goldenim.width()):
        for y in range(goldenim.height()):
            p1=goldenim.pixel(x,y)
            p2=testim.pixel(x,y)
            sad += abs((p1&0xFF)-(p2&0xFF))
            sad += abs((p1>>8&0xFF)-(p2>>8&0xFF))
            sad += abs((p1>>16&0xFF)-(p2>>16&0xFF))
    sad /= float(goldenim.width()*goldenim.height())
    if (sad < threshold):
        return 1

    return 0
    

class TestRenderTheme(TestRender_base):
    # {{{ Basics

    def __init__(self):
        TestRender_base.__init__(self)

    def setup_method(self, method):
        TestRender_base.setup_method(self, method)
        print "Theme setup", method
#         print "setup theme"
        self.r.set_theme(Theme(u'blank_theme.xml')) # set "blank" theme
        self.r.set_text_rectangle(QtCore.QRect(0,0, self.size.width(),
            self.size.height()))
        words = """How sweet the name of Jesus sounds
In a believer's ear!
It soothes his sorrows, heals his wounds,
And drives away his fear.
"""
        verses = self.r.set_words_openlp(words)
#         usually the same
        self.expected_answer = QtCore.QRect(0, 0, 559, 342)
        self.msg = None
        self.bmpname = "Not set a bitmap yet"
        print "------------- setup done --------------"

    def teardown_method(self, method):
        print "============ teardown =============", method, self.bmpname
        if self.bmpname != None:
            assert (self.compare_DC_to_file(self.bmpname))
        if self.expected_answer != None: # result=None => No result to check
            assert self.expected_answer == self.answer
        print "============ teardown done ========="

    def compare_DC_to_file(self, name):
        """writes DC out to a bitmap file and then compares it with a golden
        one returns True if OK, False if not (so you can assert on it)

        """
        print "--- compare DC to file --- ", name
        p = self.frame.GetPixmap()
        im = self.write_to_file(p, name)
        print "Compare"
        goldenfilename=os.path.join(u'golden_bitmaps",name+".bmp')
        if os.path.exists(goldenfilename):
            goldenim = QtGui.QImage(goldenfilename)
        else:
            print "File", goldenfilename, "not found"
            return False
        if (compare_images(goldenim, im)):
            print name, "Images match"
            return True
        else:
            print name, goldenfilename, "Images don't match"
            return False

    def test_theme_basic(self):
        self.answer = self.r.render_screen(0)
        self.bmpname = whoami()
        print self.r._theme.FontProportion
        print self.answer, self.expected_answer, \
            self.answer == self.expected_answer
#         self.msg=self.bmpname

    # }}}

    # {{{ Gradients
    def test_gradient_h(self):
        # normally we wouldn't hack with these directly!
        self.r._theme.BackgroundType = 1
        self.r._theme.BackgroundParameter1 = QtGui.QColor(255,0,0)
        self.r._theme.BackgroundParameter2 = QtGui.QColor(255,255,0)
        self.r._theme.BackgroundParameter3 = 1
        self.answer = self.r.render_screen(0)
        self.bmpname = whoami()

    def test_gradient_v(self):
        # normally we wouldn't hack with these directly!
        self.r._theme.BackgroundType = 1
        self.r._theme.BackgroundParameter1 = QtGui.QColor(255,0,0)
        self.r._theme.BackgroundParameter2 = QtGui.QColor(255,255,0)
        self.r._theme.BackgroundParameter3 = 0
        self.answer = self.r.render_screen(0)
        self.bmpname = whoami()
    # }}}

    # {{{ backgrounds
    def test_bg_stretch_y(self):
        t = Theme(u'blank_theme.xml')
        t.BackgroundType = 2
        t.BackgroundParameter1 = os.path.join(u'data_for_tests',
            'snowsmall.jpg')
        t.BackgroundParameter2 = QtGui.QColor(0,0,64)
        t.BackgroundParameter3 = 0
        t.Name = "stretch y"
        self.r.set_theme(t)
        print "render"
        self.answer = self.r.render_screen(0)
        print "whoami"
        self.bmpname = whoami()
        print "fone"

    def test_bg_shrink_y(self):
        t = Theme(u'blank_theme.xml')
        t.BackgroundType = 2
        t.BackgroundParameter1 = os.path.join(u'data_for_tests', 'snowbig.jpg')
        t.BackgroundParameter2 = QtGui.QColor(0,0,64)
        t.BackgroundParameter3 = 0
        t.Name = "shrink y"
        self.r.set_theme(t)
        self.answer = self.r.render_screen(0)
        self.bmpname = whoami()

    def test_bg_stretch_x(self):
        t = Theme(u'blank_theme.xml')
        t.BackgroundType = 2
        t.BackgroundParameter1 = os.path.join(u'data_for_tests',
	        'treessmall.jpg')
        t.BackgroundParameter2 = QtGui.QColor(0,0,64)
        t.BackgroundParameter3 = 0
        t.VerticalAlign = 2
        t.Name = "stretch x"
        self.r.set_theme(t)
        self.answer = self.r.render_screen(0)
        self.expected_answer = QtCore.QRect(0, 129, 559, 342)
        self.bmpname = whoami()

    def test_bg_shrink_x(self):
        t = Theme(u'blank_theme.xml')
        t.BackgroundType = 2
        t.BackgroundParameter1 = os.path.join(u'data_for_tests',
            'treesbig.jpg')
        t.BackgroundParameter2 = QtGui.QColor(0,0,64)
        t.BackgroundParameter3 = 0
        t.VerticalAlign = 2
        t.Name = "shrink x"
        self.r.set_theme(t)
        self.expected_answer = QtCore.QRect(0, 129, 559, 342)
        self.answer = self.r.render_screen(0)
        self.bmpname = whoami()
    # }}}

    # {{{ Vertical alignment
    def test_theme_vertical_align_top(self):
        t = Theme(u'blank_theme.xml')
        t.BackgroundType = 0
        t.BackgroundParameter1 = QtGui.QColor(0,0,64)
        t.VerticalAlign = 0
        t.Name = "valign top"
        self.r.set_theme(t)
        self.answer = self.r.render_screen(0)
        self.bmpname = whoami()

    def test_theme_vertical_align_bot(self):
        t = Theme(u'blank_theme.xml')
        t.BackgroundType = 0
        t.BackgroundParameter1 = QtGui.QColor(0,0,64)
        t.VerticalAlign = 1
        t.Name = "valign bot"
        self.r.set_theme(t)
        self.answer = self.r.render_screen(0)
        self.expected_answer = QtCore.QRect(0, 257, 559, 342)
        self.bmpname = whoami()

    def test_theme_vertical_align_cen(self):
        t = Theme(u'blank_theme.xml')
        t.BackgroundType = 0
        t.BackgroundParameter1 = QtGui.QColor(0,0,64)
        t.VerticalAlign = 2
        t.Name = "valign cen"
        self.r.set_theme(t)
        self.answer = self.r.render_screen(0)
        self.expected_answer = QtCore.QRect(0, 129, 559, 342)
        self.bmpname = whoami()
    # }}}

    # {{{ Horzontal alignment
    def test_theme_horizontal_align_left(self):
        t = Theme(u'blank_theme.xml')
        t.BackgroundType = 0
        t.BackgroundParameter1 = QtGui.QColor(0,0,64)
        t.VerticalAlign = 0
        t.HorizontalAlign = 0
        t.Name = "halign left"
        self.r.set_theme(t)
        self.answer = self.r.render_screen(0)
        self.bmpname = whoami()

    def test_theme_horizontal_align_right(self):
        t = Theme(u'blank_theme.xml')
        t.BackgroundType = 0
        t.BackgroundParameter1 = QtGui.QColor(0,0,64)
        t.VerticalAlign = 0
        t.HorizontalAlign = 1
        t.Name = "halign right"
        self.r.set_theme(t)
        self.expected_answer = QtCore.QRect(0, 0, 800, 342)
        self.answer = self.r.render_screen(0)
        self.bmpname = whoami()

    def test_theme_horizontal_align_centre(self):
        t = Theme(u'blank_theme.xml')
        t.BackgroundType = 0
        t.BackgroundParameter1 = QtGui.QColor(0,0,64)
        t.VerticalAlign = 0
        t.HorizontalAlign = 2
        t.Name = "halign centre"
        self.r.set_theme(t)
        self.answer = self.r.render_screen(0)
        self.expected_answer = QtCore.QRect(0, 0, 679, 342)
        self.bmpname = whoami()

    def test_theme_horizontal_align_left_lyric(self):
        t = Theme(u'blank_theme.xml')
        t.BackgroundType = 0
        t.BackgroundParameter1 = QtGui.QColor(0,0,64)
        t.VerticalAlign = 0
        t.HorizontalAlign = 0
        t.WrapStyle = 1
        t.Name = "halign left lyric"
        self.r.set_theme(t)
        self.answer = self.r.render_screen(0)
        self.expected_answer = QtCore.QRect(0, 0, 778, 342)
        self.bmpname = whoami()
    # }}}

    # {{{ Shadows and outlines
    def test_theme_shadow_outline(self):
        t = Theme(u'blank_theme.xml')

        t.BackgroundType = 0
        t.BackgroundParameter1 = QtGui.QColor(0,0,0);
        t.Name="shadow/outline"
        t.Shadow = 1
        t.Outline = 1
        t.ShadowColor = QtGui.QColor(64,128,0)
        t.OutlineColor = QtGui.QColor(128,0,0)
        self.r.set_debug(1)
        self.r.set_theme(t)
        self.answer = self.r.render_screen(0)
        hoffset = self.r._shadow_offset+2*(self.r._outline_offset)
        voffset = hoffset * (len(self.r.words[0])+1)

        self.expected_answer = QtCore.QRect(0, 0, 559+hoffset, 342+voffset)
        self.bmpname = whoami()
    # }}}

    def test_theme_font(self):
        t = Theme(u'blank_theme.xml')
        t.BackgroundType = 0
        t.BackgroundParameter1 = QtGui.QColor(0,0,64)
        t.Name = "font"
        t.FontName = "Times New Roman"
        self.r.set_theme(t)
        self.answer = self.r.render_screen(0)
        self.expected_answer = QtCore.QRect(0, 0, 499, 336)
        self.bmpname=whoami()


if __name__ == "__main__":
    t = TestRenderTheme()
    t.setup_class()
    t.setup_method(None)
    t.test_bg_stretch_y()
    t.teardown_method(None)
