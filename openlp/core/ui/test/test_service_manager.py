# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import sys
import os
import os.path
import logging

from PyQt4 import QtGui

from openlp.core.ui import ServiceManager
from openlp.plugins.images.lib import ImageServiceItem

mypath = os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0, (os.path.join(mypath, '..', '..', '..', '..')))

logging.basicConfig(filename='test_service_manager.log', level=logging.INFO,
    filemode='w')

# # from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66062
# def whoami(depth=1):
#     return sys._getframe(depth).f_code.co_name
global app
global log
log = logging.getLogger(u'TestServiceManager')

class TestServiceManager_base:
    def __init__(self):
        pass

    def setup_class(self):
        log.info( "class setup" + unicode(self))
        try:
            if app is None:
                app = QtGui.QApplication([])
        except UnboundLocalError:
            app = QtGui.QApplication([])

    def teardown_class(self):
        pass

    def setup_method(self, method):
        log.info(u'Setup method:' + unicode(method))
        self.expected_answer = "Don't know yet"
        self.answer = None
        self.s = ServiceManager(None)
        log.info(u'--------------- Setup Done -------------')

    def teardown_method(self, method):
        self.s = None

    def select_row(self, row):
        # now select the line we just added
        # first get the index
        i = QModelIndex(self.s.service_data.index(0,0))
        # make a selection of it
        self.sm = QItemSelectionModel(self.s.service_data)
        self.sm.select(i, QItemSelectionModel.ClearAndSelect)
        log.info(unicode(self.sm.selectedIndexes()))
        self.s.TreeView.setSelectionModel(self.sm)
        log.info(u'Selected indexes = ' + unicode(
            self.s.TreeView.selectedIndexes()))

    def test_easy(self):
        log.info(u'test_easy')
        item = ImageServiceItem(None)
        item.add(u'test.gif')
        self.s.addServiceItem(item)
        answer = self.s.service_as_text()
        log.info(u'Answer = ' + unicode(answer))
        lines = answer.split(u'\n')
        log.info(u'lines = ' + unicode(lines))
        assert lines[0].startswith(u'# <openlp.plugins.images.imageserviceitem.ImageServiceItem object')
        assert lines[1] == "test.gif"
        log.info(u'done')

    def test_2items_as_separate_items(self):
        # If nothing is selected when item is added, a new base service item
        # is added
        log.info(u'test_2items_as_separate_items')
        item = ImageServiceItem(None)
        item.add(u'test.gif')
        self.s.addServiceItem(item)
        item = ImageServiceItem(None)
        item.add(u'test2.gif')
        item.add(u'test3.gif')
        self.s.addServiceItem(item)
        answer = self.s.service_as_text()
        log.info(u'Answer = ' + unicode(answer))
        lines = answer.split(u'\n')
        log.info(u'lines = ' + unicode(lines))
        assert lines[0].startswith(u'# <openlp.plugins.images.imageserviceitem.ImageServiceItem object')
        assert lines[1] == "test.gif"
        assert lines[2].startswith(u'# <openlp.plugins.images.imageserviceitem.ImageServiceItem object')
        assert lines[3] == "test2.gif"
        assert lines[4] == "test3.gif"
        log.info(u'done')

    def test_2items_merged(self):
        # If the first object is selected when item is added it should be
        # extended
        log.info(u'test_2items_merged')
        item = ImageServiceItem(None)
        item.add(u'test.gif')
        self.s.addServiceItem(item)
        self.select_row(0)
        log.info(u'Selected indexes = ' + unicode(
            self.s.TreeView.selectedIndexes()))
        item = ImageServiceItem(None)
        item.add(u'test2.gif')
        item.add(u'test3.gif')
        self.s.addServiceItem(item)
        answer = self.s.service_as_text()
        log.info(u'Answer = ' + unicode(answer))
        lines = answer.split(u'\n')
        log.info(u'lines = ' + unicode(lines))
        assert lines[0].startswith(u'# <openlp.plugins.images.imageserviceitem.ImageServiceItem object')
        assert lines[1] == "test.gif"
        assert lines[2] == "test2.gif"
        assert lines[3] == "test3.gif"
        log.info(u'done')

    # more tests to do:
    #  add different types of service item
    #  move up, down
    #  move to top, bottom
    #  new and save as
    #  deleting items


if __name__ == "__main__":
    t=TestServiceManager_base()
    t.setup_class()
    t.setup_method(None)
    t.test_easy()
    t.teardown_method(None)
    print "Pass"
    log.info(u'Pass')
