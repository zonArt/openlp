# import openlp.plugins
import os, sys
import logging
mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..' ,'..')))
from openlp.plugins.plugin import Plugin
class PluginManager:
    global log
    log=logging.getLogger("PluginMgr")
    log.info("Plugin manager loaded")
    def __init__(self, dir):
        log.info("Plugin manager initing")
        if not dir in sys.path:
            log.debug("Inserting %s into sys.path", dir)
            sys.path.insert(0, dir)
        self.basepath=os.path.abspath(dir)
        self.plugins=[]
        self.find_plugins(dir)
        log.info("Plugin manager done init")
    def find_plugins(self, dir):
        """Scan the directory dir for objects inheriting from openlp.plugin"""
        log.debug("find plugins" + str(dir))
        for root,dirs, files in os.walk(dir):
            for name in files:
                if name.endswith(".py") and not name.startswith("__"):
                    path=os.path.abspath(os.path.join(root,name))
                    modulename,pyext = os.path.splitext(path)
                    prefix=os.path.commonprefix([self.basepath, path])
                    # hack off the plugin base path
                    modulename=modulename[len(prefix)+1:]
                    modulename=modulename.replace('/','.')
                    
                    log.debug("Importing "+modulename+" from "+path)
                    try:
                        __import__(modulename, globals(), locals(), [])
                    except ImportError:
                        pass
        self.plugins=Plugin.__subclasses__()
        self.plugin_by_name={}
        for p in self.plugins:
            self.plugin_by_name[p.name]=p;
                    
                        
            
        
