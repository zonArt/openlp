import logging
import os, sys
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
log=logging.getLogger(u'')

logging.info(u'Logging started')
mypath=os.path.split(os.path.abspath(__file__))[0]

sys.path.insert(0,(os.path.join(mypath, '..' ,'..', '..')))

# test the plugin manager with some plugins in the test_plugins directory
class TestPluginManager:
    def test_init(self):
        self.p=PluginManager(u'./testplugins')
        p=self.p
        p.find_plugins(u'./testplugins', None, None)
        assert (len(p.plugins)==2);
        # get list of the names of the plugins
        names=[plugin.name for plugin in p.plugins]
        # see which ones we've got
        assert (u'testplugin1" in names)
        assert (u'testplugin2" in names)
        # and not got - it's too deep in the hierarchy!
        assert (u'testplugin3" not in names)
        # test that the weighting is done right
        assert p.plugins[0].name=="testplugin2"
        assert p.plugins[1].name=="testplugin1"
if __name__=="__main__":
    log.debug(u'Starting')
    t=TestPluginManager()
    t.test_init()
    log.debug(u'List of plugins found:')
    for plugin in t.p.plugins:
        log.debug(u'Plugin %s, name=%s (version=%d)"%(unicode(plugin), plugin.name, plugin.version))