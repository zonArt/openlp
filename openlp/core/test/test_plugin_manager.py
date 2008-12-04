import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')

console=logging.StreamHandler()
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
log=logging.getLogger('')

logging.info("Logging started")
import os, sys
mypath=os.path.split(os.path.abspath(__file__))[0]

sys.path.insert(0,(os.path.join(mypath, '..' ,'..', '..')))
from openlp.core.pluginmanager import PluginManager

# test the plugin manager with some plugins in the test_plugins directory
class TestPluginManager:
    def test_init(self):
        p=PluginManager("./testplugins")
        assert (len(p.plugins)==2);
        # get list of the names of the plugins
        names=[plugin.name for plugin in p.plugins]
        # see which ones we've got
        assert ("testplugin1" in names)
        assert ("testplugin2" in names)
        # and not got!
        assert ("testplugin3" not in names)
        # test that the weighting is done right
        assert p.plugins[0].name=="testplugin2"
        assert p.plugins[1].name=="testplugin1"
if __name__=="__main__":
    log.debug("Starting")
    p=PluginManager("./testplugins")
    for plugin in p.plugins:
        log.debug("Plugin %s, name=%s (version=%d)"%(str(plugin), plugin.name, plugin.version))
