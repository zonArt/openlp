from openlp.core.lib import Plugin
import logging

class testplugin1(Plugin):
    name="testplugin1"
    version=0
    global log
    log=logging.getLogger("testplugin1")
    log.info("Started")
    Weight=10
    def __init__(self):
        pass
        
