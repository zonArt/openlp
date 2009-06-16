from openlp.core.lib import Plugin
import logging

class testplugin1(Plugin):
    name="testplugin1"
    version=0
    global log
    log=logging.getLogger(u'testplugin1')
    log.info(u'Started')
    weight=10
    def __init__(self):
        pass
        