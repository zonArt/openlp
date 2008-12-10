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

import time
import sys
import os, os.path
from PyQt4 import QtGui, QtCore

mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..','..')))
from openlp.core.theme import Theme
from openlp.core import Renderer
# from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66062
def whoami(depth=1):
    return sys._getframe(depth).f_code.co_name

class TstFrame:
    # {{{ init

    def __init__(self, size):
        """Create the DemoPanel."""
        self.width=size.width();
        self.height=size.height();
        # create something to be painted into
        self._Buffer = QtGui.QPixmap(self.width, self.height)
    def GetPixmap(self):
        return self._Buffer

    # }}}

class TestRender_base:
    def __init__(self):
        if not os.path.exists("test_results"):
            os.mkdir("test_results")
        self.app=None
    def write_to_file(self, pixmap, name):
        im=pixmap.toImage()
        testpathname=os.path.join("test_results", name+".bmp")
        if os.path.exists(testpathname):
            os.unlink(testpathname)
        im.save(testpathname, "bmp")
        return im
    # xxx quitting the app still leaves it hanging aroudn so we die
    # when trying to start another one.  Not quitting doesn't help
    # though This means that the py.test runs both test modules in
    # sequence and the second one tries to create another application
    # which gives us errors :(

    def setup_class(self):
        print "class setup", self
        try:
            if self.app is None:
                pass
        except AttributeError: # didn't have one
            print "No app"
            self.app = None

        print "Test app (should be None)"
        if self.app is None:
            print "App is None"
            self.app = QtGui.QApplication([])
        else:
            print "class setup, app is", app
#             self.app = QtGui.QApplication([])

    def teardown_class(self):
        print "class quit", self, self.app
        self.app.quit()
#     def setup_module(self):
#         print "Module setup"
#         self.app = QtGui.QApplication([])
#     def teardown_module(self):
#         print "Module quit"
#         self.app.quit()
    def setup_method(self, method):
        print "SSsetup", method
        if not hasattr(self, "app"):
            self.app=None
        try: # see if we already have an app for some reason.
            # have to try and so something, cant just test against None
            print "app", self.app, ";;;"
            print self.app.quit()
            print "quitted"
        except RuntimeError: # not valid app, create one
            print "Runtime error"
        except AttributeError: # didn't have one
            print "Attribute error"
#             print "App", self.app
#         self.app = QtGui.QApplication([])
        print "Application created and sorted"
        self.size=QtCore.QSize(800,600)
        frame=TstFrame(size=self.size)
        self.frame=frame
        self.paintdest=frame.GetPixmap()
        self.r=Renderer()
        self.r.set_paint_dest(self.paintdest)
        self.expected_answer="Don't know yet"
        self.answer=None
        print "--------------- Setup Done -------------"

    def teardown_method(self, method):
        self.write_to_file(self.frame.GetPixmap(), "test_render")

class TestRender(TestRender_base):
    def __init__(self):
        TestRender_base.__init__(self)

    def setup_method(self, method):
        TestRender_base.setup_method(self, method)
        self.r.set_debug(1)
        themefile=os.path.abspath("data_for_tests/render_theme.xml")
        self.r.set_theme(Theme(themefile)) # set default theme
        self.r._render_background()
        self.r.set_text_rectangle(QtCore.QRect(0,0, self.size.width()-1, self.size.height()-1))
        self.msg=None

    def test_easy(self):
        answer=self.r._render_single_line("Test line", tlcorner=(0,100))
        assert (answer==(219,163))
    def test_longer(self):
        answer=self.r._render_single_line("Test line with more words than fit on one line",
                                         tlcorner=(10,10))
        assert (answer==(753,136))
    def test_even_longer(self):
        answer=self.r._render_single_line("Test line with more words than fit on either one or two lines",
                                         tlcorner=(10,10))
        assert(answer==(753,199))
    def test_lines(self):
        lines=[]
        lines.append("Line One")
        lines.append("Line Two")
        lines.append("Line Three and should be long enough to wrap")
        lines.append("Line Four and should be long enough to wrap also")
        answer=self.r._render_lines(lines)
        assert(answer==QtCore.QRect(0,0,741,378))

    def test_set_words_openlp(self):
        words="""
Verse 1: Line 1
Line 2

Verse 2: Line 1
Line 2

Verse 3: Line 1
Line 2
Line 3"""
        expected_answer=["Verse 1: Line 1\nLine 2","Verse 2: Line 1\nLine 2","Verse 3: Line 1\nLine 2\nLine 3"]
        answer=self.r.set_words_openlp(words)
        assert (answer==expected_answer)
    def test_render_screens(self):
        words="""
Verse 1: Line 1
Line 2

Verse 2: Line 1
Line 2

Verse 3: Line 1
Line 2
Line 3"""
        verses=self.r.set_words_openlp(words)
        expected_answer=["Verse 1: Line 1\nLine 2","Verse 2: Line 1\nLine 2","Verse 3: Line 1\nLine 2\nLine 3"]
        assert (verses==expected_answer)

        expected_answer=[QtCore.QRect(0,0,397,126), QtCore.QRect(0,0,397,126), QtCore.QRect(0,0,397,189)]
        for v in range(len(verses)):
            answer=self.r.render_screen(v)
#             print v, answer.x(), answer.y(), answer.width(), answer.height()
            assert(answer==expected_answer[v])
    def split_test(self, number, answer, expected_answers):
        lines=[]
        print "Split test", number, answer
        for i in range(number):
            extra=""
            if i == 51: # make an extra long line on line 51 to test wrapping
                extra="Some more words to make it wrap around don't you know until it wraps so many times we don't know what to do"
            lines.append("Line %d %s" % (i, extra))
        result=self.r.split_set_of_lines(lines)
        print "results---------------__", result
        for i in range(len(result)):
            self.setup_method(None)
            answer=self.r._render_lines(result[i])
            print answer
            self.write_to_file(self.frame.GetPixmap(), "split_test_%03d"% i)
            print number, i, answer.x(), answer.y(), answer.width(), answer.height()

            e=expected_answers[i]
            assert(answer==QtCore.QRect(e[0],e[1],e[2],e[3]))


    def test_splits(self):
        print "Test splits"
        self.split_test(100, 11, [(0,0,180,567), (0,0,214,567), (0,0,214,567), (0,0,214,567), (0,0,214,567), (0,0,214,378), (0,0,759,567),
                                  (0,0,214,567), (0,0,214,567), (0,0,214,567), (0,0,214,567), (0,0,214,567), (0,0,214,567)])
        self.split_test(30, 4, [ (0,0,180,441), (0,0,214,441), (0,0,214,441), (0,0,214,441)])
        self.split_test(20, 3, [(0,0,180,378), (0,0,214,378), (0,0,214,378)])
        self.split_test(12, 2, [(0,0,180,378), (0,0,214,378)])
        self.split_test(4, 1, [(0,0,180,252)])
        self.split_test(6, 1, [(0,0,180,378)])
        self.split_test(8, 1, [(0,0,180,504)])
if __name__=="__main__":

    t=TestRender()
    t.setup_class()
    t.setup_method(None)
    t.test_splits()
    t.teardown_method(None)

