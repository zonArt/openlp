class Plugin(object):
    """Base class for openlp plugins to inherit from.

    Basic attributes are:
    name: the name that should appear in the plugins list
    version: The version number of this iteration of the plugin (just an incrementing integer!)
    paint_context: A list of paint contexts?
    """
    name="Base Plugin"
    version=0
    
    
    def __init__(self):
        self.paint_context=None
        self.prefshandler=None # this will be a PrefsPage object if it needs one
        self.media_manager_item=None # this will be a MediaManagerItem if it needs one
    def write_oos_data(self, data):
        """OOS data is passed to this function, which should return a string which can be written to the OOS file"""
        pass
    def read_oos_data(self, str):
        """data from the OOS file is passed in.  This function parses and sets up the internals of the plugin"""
        pass

    def render(self, screen=None):
        """render the screenth screenful of data to self.paint_conext"""
        pass

    def __repr__(self):
        return '<Plugin %s>' % (
            self.__class__.__name__
        )

        
