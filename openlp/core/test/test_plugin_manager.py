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

import logging
import os
import sys

from openlp.core.lib.pluginmanager import PluginManager

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')

console=logging.StreamHandler()
# set a format which is simpler for console use
formatter = logging.Formatter(u'%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
logging.getLogger(u'').addHandler(console)
log = logging.getLogger(u'')
logging.info(u'Logging started')
mypath = os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..' ,'..', '..')))

# test the plugin manager with some plugins in the test_plugins directory
class TestPluginManager:
    def test_init(self):
        self.p = PluginManager(u'./testplugins')
        p = self.p
        p.find_plugins(u'./testplugins', None, None)
        assert(len(p.plugins) == 2)
        # get list of the names of the plugins
        names = [plugin.name for plugin in p.plugins]
        # see which ones we've got
        assert(u'testplugin1' in names)
        assert(u'testplugin2' in names)
        # and not got - it's too deep in the hierarchy!
        assert(u'testplugin3' not in names)
        # test that the weighting is done right
        assert(p.plugins[0].name == "testplugin2")
        assert(p.plugins[1].name == "testplugin1")

if __name__ == "__main__":
    log.debug(u'Starting')
    t = TestPluginManager()
    t.test_init()
    log.debug(u'List of plugins found:')
    for plugin in t.p.plugins:
        log.debug(u'Plugin %s, name=%s (version=%d)' %(unicode(plugin),
        plugin.name, plugin.version))
